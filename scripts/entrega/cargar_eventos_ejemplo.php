<?php
if (PHP_SAPI !== 'cli') { http_response_code(403); exit('Solo desde la línea de comandos.'); }
/**
 * Carga el calendario de la demostración:
 *  - actividades REALES del CADUS, ya celebradas, con la fecha y el enlace de www.cadus.us.es (jornadas de formación,
 *    plazos de los Premios CADUS y plenos); y
 *  - dos eventos FUTUROS INVENTADOS, marcados «(ejemplo)», para ver cómo se ven los próximos eventos y una votación
 *    vinculada a una asamblea (RN-05). Sustituirlos por los reales cuando el CADUS los convoque.
 * Cada elemento que crea lleva la marca `_cadus_semilla` (evento:<título> o votacion:<título>). Se puede repetir sin
 * duplicar: busca por esa marca y actualiza título, texto y fechas de lo que cargó él; si no encuentra la marca, adopta
 * (y marca) un elemento sin marca con el mismo título, que es lo que dejó una versión anterior del script. Con --quitar
 * borra solo lo marcado.
 * Uso: php scripts/entrega/cargar_eventos_ejemplo.php [--quitar]
 */
$_SERVER['HTTP_HOST'] = 'localhost';
require __DIR__ . '/../../cms-wordpress/wp-load.php';

if (!function_exists('tribe_create_event')) {
    exit("The Events Calendar no está activo.\n");
}
$quitar = in_array('--quitar', $argv, true);
$fallos = 0;

/**
 * Busca por marca (y, si $adoptar, por título entre los elementos sin marca). Consulta directa: The Events Calendar
 * oculta en get_posts() los eventos ya pasados y el script duplicaría.
 */
$existe = function (string $clave, string $titulo, string $tipo, bool $adoptar) {
    global $wpdb;
    $id = $wpdb->get_var($wpdb->prepare(
        "SELECT p.ID FROM {$wpdb->posts} p JOIN {$wpdb->postmeta} m ON m.post_id = p.ID AND m.meta_key = '_cadus_semilla'
         WHERE m.meta_value = %s AND p.post_type = %s AND p.post_status <> 'trash' ORDER BY p.ID LIMIT 1", $clave, $tipo));
    if (!$id && $adoptar) {
        $id = $wpdb->get_var($wpdb->prepare(
            "SELECT p.ID FROM {$wpdb->posts} p LEFT JOIN {$wpdb->postmeta} m ON m.post_id = p.ID AND m.meta_key = '_cadus_semilla'
             WHERE p.post_type = %s AND p.post_title = %s AND p.post_status <> 'trash' AND m.meta_id IS NULL ORDER BY p.ID LIMIT 1", $tipo, $titulo));
        if ($id) {
            update_post_meta((int) $id, '_cadus_semilla', $clave);
            echo "adoptado (sin marca): $titulo\n";
        }
    }
    return $id ? (int) $id : null;
};
$fuente = fn(string $url) => ' Fuente: <a href="' . esc_url($url) . '">www.cadus.us.es</a>.';

// [título, inicio, fin, hora inicio, hora fin (vacías = todo el día), texto]
$eventos = [
    ['IV Jornadas de Formación del CADUS', '2025-03-07', '2025-03-09', '', '',
        'Formación para los miembros de las Delegaciones de Centro en tres líneas: una básica y dos avanzadas.' . $fuente('https://www.cadus.us.es/ivjornadasformacion/')],
    ['Pleno Extraordinario del CADUS', '2026-06-17', '2026-06-17', '', '',
        'Sesión extraordinaria del Pleno. El acta está en Actas y normativa.' . $fuente('https://www.cadus.us.es/plenos/pleno-extraordinario-del-17-de-junio-de-2026/')],
    ['Premios CADUS (4.ª edición): presentación de candidaturas', '2026-09-14', '2026-09-20', '', '',
        'Plazo para presentar candidaturas a los IV Premios CADUS.' . $fuente('https://www.cadus.us.es/iv-edicion-de-los-premios-cadus/')],
    ['Premios CADUS (4.ª edición): resolución de los candidatos seleccionados', '2026-09-28', '2026-09-28', '', '',
        'El Comité Evaluador publica la propuesta de resolución de los IV Premios CADUS.' . $fuente('https://www.cadus.us.es/iv-edicion-de-los-premios-cadus/')],
    ['Pleno Ordinario del CADUS', '2026-09-29', '2026-09-29', '', '',
        'Sesión ordinaria del Pleno. Están publicadas la convocatoria y el informe de la Delegación; el acta todavía no.' . $fuente('https://www.cadus.us.es/plenos/pleno-ordinario-del-29-de-septiembre-de-2026/')],
    // Futuros INVENTADOS, para ver los próximos eventos y una votación vinculada
    ['Asamblea general ordinaria (ejemplo)', '2026-11-26', '2026-11-26', '18:00', '20:00',
        'Convocatoria inventada para la demostración del portal. Sustituir por la asamblea real.'],
    ['Jornada de formación para delegaciones (ejemplo)', '2026-12-03', '2026-12-03', '10:00', '14:00',
        'Evento inventado para la demostración del portal. Sustituir por la jornada real.'],
];
$retirados = ['Jornada de bienvenida al alumnado (ejemplo)']; // ejemplo antiguo (sin marca) que ya no se usa

if (!$quitar && !term_exists('asambleas', 'tribe_events_cat')) {
    wp_insert_term('Asambleas', 'tribe_events_cat', ['slug' => 'asambleas']);
}
foreach ($retirados as $titulo) {
    if (!$quitar && ($id = $existe('evento:' . sanitize_title($titulo), $titulo, 'tribe_events', true))) {
        wp_delete_post($id, true);
        echo "borrado: $titulo\n";
    }
}
$ids = [];
foreach ($eventos as [$titulo, $ini, $fin, $h1, $h2, $texto]) {
    $clave = 'evento:' . sanitize_title($titulo);
    $id = $existe($clave, $titulo, 'tribe_events', !$quitar);
    if ($quitar) {
        if ($id) { wp_delete_post($id, true); echo "borrado: $titulo\n"; }
        continue;
    }
    $dia = $h1 === '';
    $args = [
        'post_title' => $titulo, 'post_content' => $texto, 'post_status' => 'publish', 'EventAllDay' => $dia,
        'EventStartDate' => $ini, 'EventEndDate' => $fin,
        'EventStartHour' => $dia ? '00' : substr($h1, 0, 2), 'EventStartMinute' => $dia ? '00' : substr($h1, 3, 2),
        'EventEndHour' => $dia ? '23' : substr($h2, 0, 2), 'EventEndMinute' => $dia ? '59' : substr($h2, 3, 2),
    ];
    if ($id) {
        $r = tribe_update_event($id, $args);
        echo "actualizado evento $id: $titulo\n";
    } else {
        $r = $id = tribe_create_event($args);
        echo "creado evento " . ($id ?: '(falló)') . ": $titulo\n";
    }
    if (!$id || is_wp_error($id) || !$r) {
        $fallos++;
        echo "  ERROR: no se pudo guardar «$titulo»\n";
        continue;
    }
    update_post_meta((int) $id, '_cadus_semilla', $clave);
    $ids[$titulo] = (int) $id;
    if (str_starts_with($titulo, 'Asamblea')) {
        // RN-05: solo las asambleas admiten votaciones vinculadas
        if (is_wp_error(wp_set_object_terms((int) $id, 'asambleas', 'tribe_events_cat'))) {
            $fallos++;
            echo "  ERROR: no se pudo marcar «$titulo» como asamblea\n";
        }
    }
}

$tituloVot = 'Votación de los estatutos (ejemplo)';
$claveVot = 'votacion:' . sanitize_title($tituloVot);
$vot = $existe($claveVot, $tituloVot, 'cadus_votacion', !$quitar);
if ($quitar) {
    if ($vot) { wp_delete_post($vot, true); echo "borrada: $tituloVot\n"; }
} else {
    $asamblea = $ids['Asamblea general ordinaria (ejemplo)'] ?? 0;
    // misma regla que valida el servidor al guardar una votación (RN-05)
    if (!$asamblea || (function_exists('cadus_votaciones_es_asamblea') && !cadus_votaciones_es_asamblea($asamblea))) {
        $fallos++;
        echo "ERROR: la asamblea no es válida para vincular la votación; no se crea ni se actualiza «$tituloVot»\n";
    } else {
        $meta = ['_cadus_vot_asamblea' => $asamblea, '_cadus_vot_apertura' => '2026-11-26T18:30', '_cadus_vot_cierre' => '2026-11-27T20:00'];
        if (!$vot) {
            $vot = wp_insert_post([
                'post_type' => 'cadus_votacion', 'post_title' => $tituloVot, 'post_status' => 'publish',
                'post_content' => 'Convocatoria inventada para la demostración, vinculada a la asamblea general ordinaria. Sustituir por una votación real.',
                'meta_input' => $meta + ['_cadus_semilla' => $claveVot],
            ]);
            echo "creada votación $vot: $tituloVot (estado " . get_post_status($vot) . ")\n";
        } else {
            foreach ($meta as $k => $v) { update_post_meta($vot, $k, $v); }
            echo "actualizada votación $vot: $tituloVot\n";
        }
    }
}
delete_transient('cadus_portada_datos');
if (isset($GLOBALS['wp_fastest_cache']) && method_exists($GLOBALS['wp_fastest_cache'], 'deleteCache')) {
    $GLOBALS['wp_fastest_cache']->deleteCache(true);
}
echo $fallos ? "terminado con $fallos error(es)\n" : "listo\n";
exit($fallos ? 1 : 0);
