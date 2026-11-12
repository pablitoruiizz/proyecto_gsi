<?php
/**
 * Prueba de HU-23 con datos de ejemplo (anonimización a los 2 años).
 *
 * Uso, desde la raíz del repositorio y con XAMPP en marcha:
 *     C:\xampp\php\php.exe scripts\pruebas\hu23_prueba_retencion.php          # crea, ejecuta, comprueba
 *     C:\xampp\php\php.exe scripts\pruebas\hu23_prueba_retencion.php limpiar  # borra los datos de ejemplo
 *
 * Solo se ejecuta por línea de comandos. Crea elementos con el código PRUEBA-HU23-* y distintas fechas de resolución,
 * lanza la misma función que la tarea programada y comprueba el resultado. El plazo cuenta desde que se resuelven. Ejecuta la anonimización real sobre la base indicada
 * en wp-config.php: úsalo en la base local o en la del servidor del equipo, nunca con datos reales de más de 2 años.
 */
if (PHP_SAPI !== 'cli') {
    exit('Solo desde la línea de comandos.');
}
require dirname(__DIR__, 2) . '/cms-wordpress/wp-load.php';

global $wpdb;

function hu23_ids_de_prueba(): array
{
    global $wpdb;
    return array_map('intval', $wpdb->get_col($wpdb->prepare(
        "SELECT post_id FROM {$wpdb->postmeta} WHERE meta_key = '_cadus_codigo' AND meta_value LIKE %s",
        'PRUEBA-HU23-%'
    )));
}

function hu23_limpiar(): void
{
    global $wpdb;
    foreach (hu23_ids_de_prueba() as $id) {
        foreach ($wpdb->get_col($wpdb->prepare("SELECT ID FROM {$wpdb->posts} WHERE post_parent = %d", $id)) as $hijo) {
            wp_delete_post((int) $hijo, true);
        }
        wp_delete_post($id, true);
    }
}

if (($argv[1] ?? '') === 'limpiar') {
    hu23_limpiar();
    exit("Datos de ejemplo de HU-23 borrados.\n");
}

hu23_limpiar(); // empezar siempre limpio

/**
 * Crea un ticket o una mediación de ejemplo con datos personales.
 * $dias_resuelto: hace cuántos días se cerró (null = no se cierra, o se cierra sin fecha guardada como los anteriores a HU-23).
 */
function hu23_crear(string $tipo, string $letra, string $estado, ?int $dias_resuelto, string $estado_post = 'private', ?int $dias_modificado = null): int
{
    global $wpdb;
    $creado = gmdate('Y-m-d H:i:s', time() - 4 * 365 * DAY_IN_SECONDS); // creados hace 4 años: la fecha de creación no cuenta
    $codigo = 'PRUEBA-HU23-' . $letra;
    $id = wp_insert_post(wp_slash([
        'post_type' => $tipo, 'post_status' => $estado_post, 'post_author' => 0,
        'post_title' => '[' . $codigo . '] ' . ($tipo === 'cadus_ticket' ? 'Asunto con datos de ' . $letra : 'Facultad de Derecho'),
        'post_content' => 'Texto personal del estudiante ' . $letra . ', con su teléfono 600 000 000.',
        'post_date' => $creado, 'post_date_gmt' => $creado,
    ]), true);
    if (is_wp_error($id)) {
        exit('No se pudo crear ' . $codigo . ': ' . $id->get_error_message() . "\n");
    }
    $meta = [
        '_cadus_codigo' => $codigo, '_cadus_email' => 'alumno' . strtolower($letra) . '@alum.us.es',
        '_cadus_consentimiento' => 'aceptado el ' . $creado . ' · aviso de privacidad de octubre de 2026',
    ];
    if ($tipo === 'cadus_ticket') {
        $meta += ['_cadus_tipo' => 'Consulta', '_cadus_respuestas' => [['fecha' => $creado, 'texto' => 'Respuesta con el nombre de ' . $letra]]];
    } else {
        $meta += ['_cadus_solicitante' => 'Solicitante ' . $letra, '_cadus_centro' => 'Facultad de Derecho'];
    }
    foreach ($meta as $clave => $valor) {
        update_post_meta($id, $clave, $valor);
    }
    update_post_meta($id, '_cadus_estado', $estado); // al cerrar, el plugin guarda _cadus_resuelto con la fecha de hoy
    if ($dias_resuelto !== null) {
        update_post_meta($id, '_cadus_resuelto', gmdate('Y-m-d H:i:s', time() - $dias_resuelto * DAY_IN_SECONDS));
    } elseif ($dias_modificado !== null) {
        delete_post_meta($id, '_cadus_resuelto'); // como un elemento cerrado antes de existir HU-23
        $modificado = gmdate('Y-m-d H:i:s', time() - $dias_modificado * DAY_IN_SECONDS);
        $wpdb->update($wpdb->posts, ['post_modified' => $modificado, 'post_modified_gmt' => $modificado], ['ID' => $id]);
        clean_post_cache($id);
    }
    return (int) $id;
}

$cerrado = 'cerrado';
$casos = [
    // letra => [tipo, estado, días desde la resolución, estado de la entrada, días desde la última modificación, ¿anonimizar?, descripción]
    'A' => ['cadus_ticket', $cerrado, 3 * 365, 'private', null, true, 'ticket cerrado hace 3 años, con un adjunto'],
    'B' => ['cadus_ticket', $cerrado, 365, 'private', null, false, 'ticket cerrado hace 1 año'],
    'C' => ['cadus_mediacion', 'cerrada', 2 * 365 + 5, 'private', null, true, 'mediación cerrada hace 2 años y 5 días'],
    'D' => ['cadus_mediacion', 'cerrada', 180, 'private', null, false, 'mediación cerrada hace 6 meses'],
    'E' => ['cadus_ticket', $cerrado, 2 * 365 - 5, 'private', null, false, 'ticket a 5 días de cumplir 2 años cerrado'],
    'F' => ['cadus_ticket', 'abierto', null, 'private', null, false, 'ticket abierto, creado hace 4 años'],
    'G' => ['cadus_ticket', $cerrado, null, 'private', 3 * 365, true, 'ticket cerrado antes de HU-23 (sin fecha guardada)'],
    'H' => ['cadus_ticket', $cerrado, 900 + 365, 'trash', null, true, 'ticket cerrado hace 3 años, en la papelera'],
    'I' => ['cadus_ticket', $cerrado, 3 * 365, 'private', null, false, 'ticket cerrado hace 3 años y reabierto después'],
];
$ids = [];
foreach ($casos as $letra => [$tipo, $estado, $dias, $estado_post, $modif]) {
    $ids[$letra] = hu23_crear($tipo, $letra, $estado, $dias, $estado_post, $modif);
}
update_post_meta($ids['I'], '_cadus_estado', 'en_proceso'); // reabrir: el plugin borra la fecha de resolución
$adjunto = wp_insert_attachment(['post_title' => 'adjunto-PRUEBA-HU23', 'post_mime_type' => 'text/plain', 'post_status' => 'inherit'], false, $ids['A']);

$simulado = cadus_retencion_ejecutar(null, true);
echo "Simulación (no cambia nada): {$simulado['cadus_ticket']} tickets y {$simulado['cadus_mediacion']} mediaciones.\n";
$real = cadus_retencion_ejecutar();
echo "Ejecución real: {$real['cadus_ticket']} tickets y {$real['cadus_mediacion']} mediaciones, {$real['errores']} errores.\n";
$segunda = cadus_retencion_ejecutar();
$repetida = $segunda['cadus_ticket'] + $segunda['cadus_mediacion'];

echo "\n#  Caso                                                  Esperado       Resultado\n";
$fallos = 0;
foreach ($casos as $letra => [$tipo, $estado, $dias, $estado_post, $modif, $debe, $descripcion]) {
    $id = $ids[$letra];
    $marcado = get_post_meta($id, '_cadus_anonimizado', true) !== '';
    $sin_correo = get_post_meta($id, '_cadus_email', true) === '';
    $sin_texto = strpos((string) get_post_field('post_content', $id), 'teléfono') === false;
    $ok = $debe
        ? ($marcado && $sin_correo && $sin_texto && get_post_meta($id, '_cadus_codigo', true) !== '')
        : (!$marcado && !$sin_correo && !$sin_texto);
    if ($letra === 'A') {
        $ok = $ok && !get_post($adjunto);
    }
    if ($letra === 'I') {
        $ok = $ok && get_post_meta($id, '_cadus_resuelto', true) === '';
    }
    $fallos += $ok ? 0 : 1;
    printf("%s  %-53s %-14s %s\n", $letra, $descripcion, $debe ? 'anonimizar' : 'conservar', $ok ? 'OK' : 'FALLO');
}
$ok_total = $simulado['cadus_ticket'] === 3 && $simulado['cadus_mediacion'] === 1 && $real['cadus_ticket'] === 3
    && $real['cadus_mediacion'] === 1 && $real['errores'] === 0;
printf("\nRecuento de la simulación y de la ejecución (3 tickets y 1 mediación): %s\n", $ok_total ? 'OK' : 'FALLO');
printf("Segunda ejecución sin cambios (idempotente): %s\n", $repetida === 0 ? 'OK' : 'FALLO');
$fallos += ($ok_total ? 0 : 1) + ($repetida === 0 ? 0 : 1);
echo "\nPara ver el resultado en el panel, abre Tickets y Mediaciones con la Ejecutiva; después ejecuta el script con «limpiar».\n";
exit($fallos === 0 ? 0 : 1);
