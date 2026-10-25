<?php
/**
 * Carga 2 eventos y 1 convocatoria de votación de EJEMPLO (marcados «(ejemplo)») para la demostración del calendario.
 * Se puede repetir: no duplica nada. Para retirarlos, bórralos desde Eventos y Votaciones, o ejecuta con --quitar.
 * Uso: php scripts/entrega/cargar_eventos_ejemplo.php [--quitar]
 */
$_SERVER['HTTP_HOST'] = 'localhost';
require __DIR__ . '/../../cms-wordpress/wp-load.php';

if (!function_exists('tribe_create_event')) {
    exit("The Events Calendar no está activo.\n");
}
$quitar = in_array('--quitar', $argv, true);
$existe = function (string $titulo, string $tipo): ?int {
    $q = get_posts(['post_type' => $tipo, 'title' => $titulo, 'post_status' => 'any', 'numberposts' => 1, 'fields' => 'ids']);
    return $q ? (int) $q[0] : null;
};

$eventos = [
    ['Asamblea general ordinaria (ejemplo)', '2026-11-12', '18:00', '20:00', 'Convocatoria de ejemplo para la demostración del portal. Sustituir por la asamblea real.'],
    ['Jornada de bienvenida al alumnado (ejemplo)', '2026-11-19', '11:00', '14:00', 'Evento de ejemplo para la demostración del portal. Sustituir por un evento real.'],
];
$ids = [];
foreach ($eventos as [$titulo, $dia, $ini, $fin, $texto]) {
    $id = $existe($titulo, 'tribe_events');
    if ($quitar) {
        if ($id) { wp_delete_post($id, true); echo "borrado: $titulo\n"; }
        continue;
    }
    if (!$id) {
        $id = tribe_create_event([
            'post_title' => $titulo, 'post_content' => $texto, 'post_status' => 'publish',
            'EventStartDate' => $dia, 'EventStartHour' => substr($ini, 0, 2), 'EventStartMinute' => substr($ini, 3, 2),
            'EventEndDate' => $dia, 'EventEndHour' => substr($fin, 0, 2), 'EventEndMinute' => substr($fin, 3, 2),
        ]);
        echo "creado evento $id: $titulo\n";
    }
    $ids[$titulo] = $id;
}

$tituloVot = 'Votación de los estatutos (ejemplo)';
$vot = $existe($tituloVot, 'cadus_votacion');
if ($quitar) {
    if ($vot) { wp_delete_post($vot, true); echo "borrada: $tituloVot\n"; }
} elseif (!$vot) {
    $vot = wp_insert_post([
        'post_type' => 'cadus_votacion', 'post_title' => $tituloVot, 'post_status' => 'publish',
        'post_content' => 'Convocatoria de ejemplo vinculada a la asamblea general ordinaria. Sustituir por una votación real.',
        'meta_input' => [
            '_cadus_vot_asamblea' => $ids['Asamblea general ordinaria (ejemplo)'],
            '_cadus_vot_apertura' => '2026-11-12T18:30',
            '_cadus_vot_cierre' => '2026-11-13T20:00',
        ],
    ]);
    echo "creada votación $vot: $tituloVot (estado " . get_post_status($vot) . ")\n";
}
delete_transient('cadus_portada_datos');
if (isset($GLOBALS['wp_fastest_cache']) && method_exists($GLOBALS['wp_fastest_cache'], 'deleteCache')) {
    $GLOBALS['wp_fastest_cache']->deleteCache(true);
}
echo "listo\n";
