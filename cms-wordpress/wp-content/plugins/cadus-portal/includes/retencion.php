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
 * - Es idempotente: lo ya anonimizado lleva la marca _cadus_anonimizado y no se vuelve a tratar.
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
    if ($clave !== '_cadus_estado' || !cadus_privacidad_tipo(get_post_type((int) $id))) {
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
function cadus_retencion_candidatos(int $limite, int $ahora): array
{
    global $wpdb;
    $corte = gmdate('Y-m-d H:i:s', strtotime('-' . cadus_retencion_anios() . ' years', $ahora));
    $tipos = cadus_privacidad_tipos();
    $marcas = implode(',', array_fill(0, count($tipos), '%s'));
    $sql = $wpdb->prepare(
        "SELECT p.ID, p.post_type FROM {$wpdb->posts} p
         JOIN {$wpdb->postmeta} e ON e.post_id = p.ID AND e.meta_key = %s AND e.meta_value IN ('cerrado', 'cerrada')
         LEFT JOIN {$wpdb->postmeta} r ON r.post_id = p.ID AND r.meta_key = %s
         LEFT JOIN {$wpdb->postmeta} m ON m.post_id = p.ID AND m.meta_key = %s
         WHERE p.post_type IN ($marcas) AND p.post_status <> 'auto-draft' AND m.meta_id IS NULL
           AND COALESCE(NULLIF(r.meta_value, ''), p.post_modified_gmt) < %s
         ORDER BY p.ID ASC LIMIT %d",
        array_merge(['_cadus_estado', '_cadus_resuelto', '_cadus_anonimizado'], $tipos, [$corte, $limite])
    );
    return $wpdb->get_results($sql, ARRAY_A) ?: [];
}

/** Anonimiza un ticket o una mediación. Devuelve false si algo falla (no se marca como hecho). */
function cadus_retencion_anonimizar(int $id, string $tipo, int $ahora): bool
{
    global $wpdb;
    $fecha = gmdate('Y-m-d H:i:s', $ahora);
    $codigo = (string) get_post_meta($id, '_cadus_codigo', true);
    $prefijo = $codigo !== '' ? '[' . $codigo . '] ' : '';
    $titulo = $tipo === 'cadus_ticket'
        ? $prefijo . 'Consulta anonimizada'
        : $prefijo . (string) get_post_meta($id, '_cadus_centro', true);

    // Datos personales en la propia entrada: el título de un ticket es el asunto escrito por el estudiante.
    $hecho = $wpdb->update(
        $wpdb->posts,
        [
            'post_title' => $titulo,
            'post_content' => 'Contenido eliminado por conservación de datos el ' . gmdate('d/m/Y', $ahora) . '.',
            'post_excerpt' => '',
            'post_modified' => current_time('mysql'),
            'post_modified_gmt' => $fecha,
        ],
        ['ID' => $id],
        ['%s', '%s', '%s', '%s', '%s'],
        ['%d']
    );
    if ($hecho === false) {
        return false;
    }

    // Datos personales en los metadatos. Se conservan código, tipo, estado, centro, consentimiento y vínculo interno.
    foreach (['_cadus_email', '_cadus_solicitante', '_cadus_respuestas'] as $clave) {
        delete_post_meta($id, $clave);
    }

    // Archivos adjuntos y revisiones: se borran de verdad. Consulta directa por el mismo motivo que arriba.
    $hijos = $wpdb->get_results($wpdb->prepare(
        "SELECT ID, post_type FROM {$wpdb->posts} WHERE post_parent = %d AND post_type IN ('attachment', 'revision')",
        $id
    ), ARRAY_A) ?: [];
    foreach ($hijos as $hijo) {
        $hijo['post_type'] === 'attachment'
            ? wp_delete_attachment((int) $hijo['ID'], true)
            : wp_delete_post((int) $hijo['ID'], true);
    }

    clean_post_cache($id);
    update_post_meta($id, '_cadus_anonimizado', $fecha);
    return true;
}

/**
 * Ejecuta la anonimización. Con $simular solo cuenta lo que se tocaría.
 * Devuelve ['cadus_ticket' => n, 'cadus_mediacion' => n, 'errores' => n, 'simulado' => bool].
 */
function cadus_retencion_ejecutar(?int $ahora = null, bool $simular = false): array
{
    $ahora = $ahora ?? time();
    $resumen = ['cadus_ticket' => 0, 'cadus_mediacion' => 0, 'errores' => 0, 'simulado' => $simular];

    // Por tandas, para no agotar el tiempo de una petición de WP-Cron si hubiera muchas.
    for ($tanda = 0; $tanda < 10; $tanda++) {
        $lote = cadus_retencion_candidatos($simular ? 1000 : 100, $ahora);
        if (!$lote) {
            break;
        }
        foreach ($lote as $fila) {
            if ($simular || cadus_retencion_anonimizar((int) $fila['ID'], (string) $fila['post_type'], $ahora)) {
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
