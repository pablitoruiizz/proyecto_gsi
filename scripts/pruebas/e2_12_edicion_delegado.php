<?php
if (PHP_SAPI !== 'cli') { http_response_code(403); exit('Solo desde la línea de comandos.'); }
/**
 * E2-12 (RN-04): comprobación de la edición restringida de las fichas de delegaciones y de su completitud.
 * Usa las cuentas locales `test-delegado` (rol Delegado) y `test-ejecutivo`. Para probar el caso positivo asigna una ficha
 * a `test-delegado` un momento e intenta devolverla a su autor original; lo verifica leyendo el autor después y, si no se
 * pudo devolver, termina con error y dice qué hay que hacer a mano.
 * Termina con código 0 solo si todas las expectativas se cumplen.
 * Uso: php scripts/pruebas/e2_12_edicion_delegado.php
 */
$_SERVER['HTTP_HOST'] = 'localhost';
define('WP_USE_THEMES', false);
require __DIR__ . '/../../cms-wordpress/wp-load.php';

$fallos = 0;
$espera = function (string $texto, bool $cumple) use (&$fallos): void {
    echo ($cumple ? '[ok]    ' : '[FALLO] '), $texto, "\n";
    $fallos += $cumple ? 0 : 1;
};

$u = get_user_by('login', 'test-delegado');
$ejecutiva = get_user_by('login', 'test-ejecutivo');
if (!$u || !$ejecutiva) { exit("Faltan las cuentas de prueba test-delegado y test-ejecutivo.\n"); }
$todas = get_posts(['post_type' => 'cadus_delegacion', 'post_status' => 'any', 'numberposts' => -1, 'fields' => 'ids']);
if (count($todas) < 2) { exit("Hacen falta al menos 2 fichas de delegación.\n"); }
echo "fichas: ", count($todas), "\n";
$edita = fn() => array_values(array_filter($todas, fn($id) => user_can($u, 'edit_post', $id)));

// precondición: el delegado no es ya autor de ninguna ficha (si no, el caso 1 no es válido)
$ya = get_posts(['post_type' => 'cadus_delegacion', 'post_status' => 'any', 'author' => $u->ID, 'numberposts' => -1, 'fields' => 'ids']);
if ($ya) { exit("test-delegado ya es autor de las fichas " . implode(',', $ya) . ": devuélvelas a su autor original y repite.\n"); }
$espera('1) sin ficha asignada, test-delegado no edita ninguna', count($edita()) === 0);

// con una ficha asignada edita solo esa y no puede borrarla
$propia = $todas[0];
$orig = (int) get_post_field('post_author', $propia);
$r = wp_update_post(['ID' => $propia, 'post_author' => $u->ID], true);
if (is_wp_error($r)) { exit("No se pudo asignar la ficha $propia: " . $r->get_error_message() . "\n"); }
clean_user_cache($u->ID);
$espera("   la ficha $propia queda asignada a test-delegado", (int) get_post_field('post_author', $propia) === $u->ID);
try {
    $solo = $edita();
    $espera("2) con la ficha $propia asignada, edita solo esa", $solo === [$propia]);
    $espera('3) no puede borrar su propia ficha', !user_can($u, 'delete_post', $propia));
} finally {
    $r = wp_update_post(['ID' => $propia, 'post_author' => $orig], true);
    $devuelta = (int) get_post_field('post_author', $propia) === $orig;
    $espera("   la ficha $propia vuelve a su autor original ($orig)", !is_wp_error($r) && $devuelta);
    if (!$devuelta) { echo "   HAY QUE DEVOLVERLA A MANO: Delegaciones > ficha $propia > Autor = usuario $orig\n"; }
}
$espera('4) la Ejecutiva edita una ficha ajena (decisión X7)', user_can($ejecutiva, 'edit_post', $todas[1]));

// completitud de las fichas publicadas (informativo)
$faltan = ['correo' => [], 'telefono' => [], 'horario' => [], 'miembros' => []];
foreach ($todas as $id) {
    if (get_post_status($id) !== 'publish') { continue; }
    foreach ($faltan as $k => $_) { if (!get_post_meta($id, $k, true)) { $faltan[$k][] = get_the_title($id); } }
}
foreach ($faltan as $k => $l) { echo "5) fichas publicadas sin $k: ", count($l), $l && count($l) < 10 ? ' (' . implode('; ', $l) . ')' : '', "\n"; }

echo $fallos ? "terminado con $fallos fallo(s)\n" : "todas las expectativas se cumplen\n";
exit($fallos ? 1 : 0);
