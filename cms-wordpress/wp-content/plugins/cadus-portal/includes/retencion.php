<?php
/**
 * Conservación de datos (HU-23): anonimización de tickets y mediaciones a los 2 años.
 * Trazabilidad: HU-23 · RN-03 (privacidad del buzón y la mediación) · RGPD.
 *
 * Una tarea diaria de WP-Cron busca los tickets (cadus_ticket) y las solicitudes de mediación (cadus_mediacion)
 * RESUELTOS hace más de 2 años (cadus_retencion_anios()) y los ANONIMIZA en lugar de borrarlos: se conserva la referencia,
 * el tipo, el estado, el centro y la fecha (sirven para estadísticas), y se eliminan los datos personales:
 * correo, solicitante, texto escrito por el estudiante, respuestas del equipo y archivos adjuntos.
 *
 * El plazo cuenta desde que se resuelven (así lo indicó el CADUS en la entrevista del 26/10), no desde que se crean:
 * un ticket abierto no se toca nunca, y si se reabre se vuelve a contar desde el siguiente cierre.
 * La fecha de resolución se guarda en _cadus_resuelto al pasar el estado a Cerrado/Cerrada; los elementos que ya
 * estaban cerrados antes de HU-23 no la tienen y se usa su fecha de última modificación.
 *
 * Detalles que importan:
 * - Las consultas usan $wpdb directamente: WP-Cron no es CLI ni panel autorizado, así que los filtros de
 *   privacidad.php ocultarían estos tipos a cualquier WP_Query y la tarea no encontraría nada.
 * - La anonimización escribe en la base de datos sin pasar por wp_update_post(), para no disparar los avisos por
 *   correo ni el guardado del panel (save_post_cadus_*).
 * - Es idempotente: lo ya anonimizado lleva la marca _cadus_anonimizado y no se vuelve a tratar. Un elemento anonimizado
 *   queda inmutable: el buzón y la mediación no admiten ya cambios de estado ni respuestas nuevas.
 * - Cada elemento se trata bajo el mismo bloqueo que el guardado del buzón y se revalida (estado y fecha de resolución)
 *   dentro de él; si falla el borrado de algo, no se marca como hecho y se reintenta en la siguiente ejecución.
 * - WP-Cron solo se dispara cuando WordPress atiende una visita; las páginas que sirve Apache desde la caché no lo activan.
 *   En el servidor de destino conviene una tarea del sistema que lo lance (por ejemplo, cada hora:
 *   `wget -q -O - https://DOMINIO/wp-cron.php?doing_wp_cron` o `wp cron event run cadus_retencion_diaria`) y
 *   comprobar la fecha de la última ejecución en la opción `cadus_retencion_ultima`.
 * - WP-CLI (si está instalado): `wp cadus retencion --simular` cuenta sin cambiar nada; `wp cadus retencion` ejecuta.
 */
if (!defined('ABSPATH')) {
    exit;
}

/** Años de conservación. Se puede cambiar con el filtro cadus_retencion_anios; nunca baja de 1. */
function cadus_retencion_anios(): int
{
    return max(1, (int) apply_filters('cadus_retencion_anios', 2));
}

/** Guarda cuándo se resuelve un ticket o una mediación; si se reabre, borra la fecha. */
function cadus_retencion_marcar_resolucion($meta_id, $id, $clave, $valor): void
{
    if ($clave !== '_cadus_estado' || !cadus_privacidad_tipo(get_post_type((int) $id))
        || get_post_meta((int) $id, '_cadus_anonimizado', true) !== '') {
        return;
    }
    if (in_array($valor, ['cerrado', 'cerrada'], true)) {
        update_post_meta((int) $id, '_cadus_resuelto', gmdate('Y-m-d H:i:s'));
    } else {
        delete_post_meta((int) $id, '_cadus_resuelto');
    }
}
add_action('added_post_meta', 'cadus_retencion_marcar_resolucion', 10, 4);
add_action('updated_post_meta', 'cadus_retencion_marcar_resolucion', 10, 4);

/** Tickets y mediaciones cerrados hace más de N años y aún sin anonimizar (fecha de resolución en GMT). */
function cadus_retencion_candidatos(int $limite, int $ahora, int $solo_id = 0): array
{
    global $wpdb;
    $corte = gmdate('Y-m-d H:i:s', strtotime('-' . cadus_retencion_anios() . ' years', $ahora));
    $tipos = cadus_privacidad_tipos();
    $marcas = implode(',', array_fill(0, count($tipos), '%s'));
    $filtro_id = $solo_id > 0 ? ' AND p.ID = %d' : '';
    $args = array_merge(['_cadus_estado', '_cadus_resuelto', '_cadus_anonimizado'], $tipos, [$corte], $solo_id > 0 ? [$solo_id] : [], [$limite]);
    $sql = $wpdb->prepare(
        "SELECT p.ID, p.post_type FROM {$wpdb->posts} p
         JOIN {$wpdb->postmeta} e ON e.post_id = p.ID AND e.meta_key = %s AND e.meta_value IN ('cerrado', 'cerrada')
         LEFT JOIN {$wpdb->postmeta} r ON r.post_id = p.ID AND r.meta_key = %s
         LEFT JOIN {$wpdb->postmeta} m ON m.post_id = p.ID AND m.meta_key = %s
         WHERE p.post_type IN ($marcas) AND p.post_status <> 'auto-draft' AND m.meta_id IS NULL
           AND COALESCE(NULLIF(r.meta_value, ''), p.post_modified_gmt) < %s{$filtro_id}
         ORDER BY p.ID ASC LIMIT %d",
        $args
    );
    return $wpdb->get_results($sql, ARRAY_A) ?: [];
}

/**
 * Anonimiza un ticket o una mediación. Devuelve true si queda anonimizado, 'omitido' si dejó de ser candidato
 * (por ejemplo, se reabrió mientras tanto) y false si algo falla (entonces NO se marca como hecho y se reintenta).
 * Toma el mismo bloqueo que el guardado del buzón y revalida el estado y la fecha de resolución dentro de él.
 */
function cadus_retencion_anonimizar(int $id, string $tipo, int $ahora)
{
    global $wpdb;
    $lock = cadus_buzon_lock('editar_' . $id);
    if ($lock === '') {
        return false;
    }
    try {
        // Otra petición pudo reabrir el elemento después de elegirlo como candidato: se revisa de nuevo con datos frescos.
        wp_cache_delete($id, 'post_meta');
        if (!cadus_retencion_candidatos(1, $ahora, $id)) {
            return 'omitido';
        }
        $fecha = gmdate('Y-m-d H:i:s', $ahora);
        $codigo = (string) get_post_meta($id, '_cadus_codigo', true);
        $prefijo = $codigo !== '' ? '[' . $codigo . '] ' : '';
        $titulo = $tipo === 'cadus_ticket'
            ? $prefijo . 'Consulta anonimizada'
            : $prefijo . (string) get_post_meta($id, '_cadus_centro', true);

        // Datos personales en la propia entrada: el título de un ticket es el asunto escrito por el estudiante, y
        // WordPress deriva de él la dirección (post_name), que también se sustituye.
        $hecho = $wpdb->update(
            $wpdb->posts,
            [
                'post_title' => $titulo,
                'post_name' => 'anonimizado-' . $id,
                'post_content' => 'Contenido eliminado por conservación de datos el ' . gmdate('d/m/Y', $ahora) . '.',
                'post_excerpt' => '',
                'post_modified' => current_time('mysql'),
                'post_modified_gmt' => $fecha,
            ],
            ['ID' => $id],
            ['%s', '%s', '%s', '%s', '%s', '%s'],
            ['%d']
        );
        if ($hecho === false) {
            return false;
        }

        // Datos personales en los metadatos. Se conservan código, tipo, estado, centro, consentimiento y vínculo interno.
        $claves = ['_cadus_email', '_cadus_solicitante', '_cadus_respuestas'];
        foreach ($claves as $clave) {
            delete_post_meta($id, $clave);
        }

        // Archivos adjuntos y revisiones: se borran de verdad. Consulta directa por el mismo motivo que arriba.
        $sql_hijos = $wpdb->prepare(
            "SELECT ID, post_type FROM {$wpdb->posts} WHERE post_parent = %d AND post_type IN ('attachment', 'revision')",
            $id
        );
        $hijos = $wpdb->get_results($sql_hijos, ARRAY_A);
        if ($hijos === null) {
            return false;
        }
        foreach ($hijos as $hijo) {
            $borrado = $hijo['post_type'] === 'attachment'
                ? wp_delete_attachment((int) $hijo['ID'], true)
                : wp_delete_post((int) $hijo['ID'], true);
            if (!$borrado) {
                return false;
            }
        }

        // Comprobación final: si queda algo, no se marca como anonimizado y la próxima ejecución lo reintenta.
        $marcas = implode(',', array_fill(0, count($claves), '%s'));
        $restos_meta = $wpdb->get_var($wpdb->prepare(
            "SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE post_id = %d AND meta_key IN ($marcas)",
            array_merge([$id], $claves)
        ));
        $restos_hijos = $wpdb->get_var(str_replace('SELECT ID, post_type', 'SELECT COUNT(*)', $sql_hijos));
        if ($restos_meta === null || (int) $restos_meta > 0 || $restos_hijos === null || (int) $restos_hijos > 0) {
            return false;
        }

        clean_post_cache($id);
        update_post_meta($id, '_cadus_anonimizado', $fecha);
        return get_post_meta($id, '_cadus_anonimizado', true) === $fecha;
    } finally {
        cadus_buzon_unlock($lock);
    }
}

/**
 * Ejecuta la anonimización. Con $simular solo cuenta lo que se tocaría.
 * Devuelve ['cadus_ticket' => n, 'cadus_mediacion' => n, 'omitidos' => n, 'errores' => n, 'simulado' => bool].
 */
function cadus_retencion_ejecutar(?int $ahora = null, bool $simular = false): array
{
    $ahora = $ahora ?? time();
    $resumen = ['cadus_ticket' => 0, 'cadus_mediacion' => 0, 'omitidos' => 0, 'errores' => 0, 'simulado' => $simular];

    // Por tandas, para no agotar el tiempo de una petición de WP-Cron si hubiera muchas.
    for ($tanda = 0; $tanda < 10; $tanda++) {
        $lote = cadus_retencion_candidatos($simular ? 1000 : 100, $ahora);
        if (!$lote) {
            break;
        }
        foreach ($lote as $fila) {
            $resultado = $simular ? true : cadus_retencion_anonimizar((int) $fila['ID'], (string) $fila['post_type'], $ahora);
            if ($resultado === 'omitido') {
                ++$resumen['omitidos'];
            } elseif ($resultado === true) {
                ++$resumen[$fila['post_type']];
            } else {
                ++$resumen['errores'];
                error_log('CADUS retención: no se pudo anonimizar el elemento ' . (int) $fila['ID']);
            }
        }
        // En simulación una sola consulta basta; con errores se para para no repetir los mismos elementos.
        if ($simular || $resumen['errores'] > 0) {
            break;
        }
    }

    if (!$simular) {
        update_option('cadus_retencion_ultima', $resumen + ['fecha' => gmdate('Y-m-d H:i:s', $ahora)], false);
    }
    return $resumen;
}

add_action('cadus_retencion_diaria', function (): void {
    cadus_retencion_ejecutar();
});

add_action('init', function (): void {
    if (!wp_next_scheduled('cadus_retencion_diaria')) {
        wp_schedule_event(time() + HOUR_IN_SECONDS, 'daily', 'cadus_retencion_diaria');
    }
});

if (defined('WP_CLI') && WP_CLI) {
    WP_CLI::add_command('cadus retencion', function ($args, $asoc): void {
        $r = cadus_retencion_ejecutar(null, isset($asoc['simular']));
        WP_CLI::success(sprintf(
            '%s: %d tickets y %d mediaciones, %d errores.',
            $r['simulado'] ? 'Simulación' : 'Anonimizados', $r['cadus_ticket'], $r['cadus_mediacion'], $r['errores']
        ));
    });
}
