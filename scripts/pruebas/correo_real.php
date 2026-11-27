<?php
if (PHP_SAPI !== 'cli') { http_response_code(403); exit('Solo desde la línea de comandos.'); }
/**
 * Prueba P5 (E3-04): envío REAL de los correos del portal a una dirección de prueba.
 * Requiere que wp-config.php defina un SMTP (constantes CADUS_SMTP_*, ver includes/correo.php).
 * Uso: php scripts/pruebas/correo_real.php destino@ejemplo.org
 * Envía a ese destino, y solo a él: (1) el aviso de ticket nuevo que iría a la Ejecutiva, (2) el aviso de respuesta al estudiante y
 * (3) el correo de «¿Has olvidado tu contraseña?» de la cuenta test-estudiante (si existe). Crea un ticket de prueba y lo borra al terminar.
 */
$_SERVER['HTTP_HOST'] = 'localhost';
define('WP_USE_THEMES', false);
require dirname(__DIR__, 2) . '/cms-wordpress/wp-load.php';

$destino = $argv[1] ?? '';
if (!is_email($destino)) { exit("Indica una dirección de destino válida.\n"); }
if (!defined('CADUS_SMTP_SERVIDOR')) { exit("Falta el SMTP: define CADUS_SMTP_SERVIDOR (y las demás CADUS_SMTP_*) en wp-config.php.\n"); }
echo 'SMTP: ', CADUS_SMTP_SERVIDOR, ':', defined('CADUS_SMTP_PUERTO') ? CADUS_SMTP_PUERTO : 587, ' · remitente: ', cadus_correo_remitente(), "\n";

// al cambiar el correo de test-estudiante WordPress avisa a la dirección vieja (un example.org que rebota): no se quiere ese envío
add_filter('send_email_change_email', '__return_false');
add_filter('send_password_change_email', '__return_false');
add_action('wp_mail_failed', function ($e) { echo '  ERROR de envío: ', $e->get_error_message(), "\n"; });
add_filter('cadus_buzon_correo_avisos', function () use ($destino) { return $destino; }); // el aviso «a la Ejecutiva» va también al destino de prueba

$id = wp_insert_post(['post_type' => 'cadus_ticket', 'post_status' => 'private', 'post_title' => '[CAD-2026-99999] Prueba de correo (borrar)',
    'post_content' => 'Ticket de prueba del envío de correo'], true);
if (is_wp_error($id)) { exit($id->get_error_message() . "\n"); }
update_post_meta($id, '_cadus_codigo', 'CAD-2026-99999');
update_post_meta($id, '_cadus_tipo', 'Consulta');
update_post_meta($id, '_cadus_email', $destino);

echo "1. Aviso de ticket nuevo (Ejecutiva): ", cadus_buzon_avisar_ejecutiva($id) ? 'enviado' : 'FALLÓ', "\n";
echo "2. Aviso de respuesta (estudiante): ", cadus_buzon_avisar_estudiante($id, 'en_proceso') ? 'enviado' : 'FALLÓ', "\n";

$u = get_user_by('login', 'test-estudiante');
if ($u) {
    $antes = $u->user_email;
    wp_update_user(['ID' => $u->ID, 'user_email' => $destino]);
    $r = retrieve_password('test-estudiante');
    echo "3. Contraseña olvidada (test-estudiante): ", $r === true ? 'enviado' : 'FALLÓ (' . (is_wp_error($r) ? $r->get_error_message() : 'sin detalle') . ')', "\n";
    wp_update_user(['ID' => $u->ID, 'user_email' => $antes]);
} else {
    echo "3. Contraseña olvidada: omitido (no existe test-estudiante)\n";
}

wp_delete_post($id, true);
echo "Ticket de prueba borrado. Revisa la bandeja de $destino (y el correo no deseado).\n";
