<?php
/**
 * Crea la cuenta única del CADUS (E2-01): usuario «cadus», correo dcadus@us.es, rol Administrador.
 * La usan todos los miembros de la Ejecutiva y desde ella se da acceso a los delegados.
 * No guarda ni muestra ninguna contraseña (se genera una aleatoria que nadie ve) y NO envía ningún correo:
 * la primera vez se entra con «¿Has olvidado tu contraseña?» y el enlace llega a dcadus@us.es.
 * Se puede repetir: si la cuenta existe, no hace nada.
 * Uso: php scripts/roles/crear_cuenta_cadus.php
 */
if (PHP_SAPI !== 'cli') {
    exit('Solo desde la línea de comandos.');
}
$_SERVER['HTTP_HOST'] = 'localhost';
define('WP_USE_THEMES', false);
require dirname(__DIR__, 2) . '/cms-wordpress/wp-load.php';

const CADUS_USUARIO = 'cadus';
const CADUS_CORREO = 'dcadus@us.es';

$existente = get_user_by('login', CADUS_USUARIO) ?: get_user_by('email', CADUS_CORREO);
if ($existente) {
    echo "La cuenta ya existe: {$existente->user_login} ({$existente->user_email}) · roles: " . implode(', ', $existente->roles) . "\n";
    exit(0);
}
add_filter('pre_wp_mail', '__return_true'); // nada de correo desde este script
$id = wp_insert_user([
    'user_login' => CADUS_USUARIO,
    'user_email' => CADUS_CORREO,
    'display_name' => 'CADUS',
    'nickname' => 'CADUS',
    'user_pass' => wp_generate_password(40, true, true),
    'role' => 'administrator',
]);
if (is_wp_error($id)) {
    fwrite(STDERR, 'No se pudo crear la cuenta: ' . $id->get_error_message() . "\n");
    exit(1);
}
echo "Cuenta creada: " . CADUS_USUARIO . ' (' . CADUS_CORREO . ") · rol administrator · id $id\n";
echo "Para entrar la primera vez: «¿Has olvidado tu contraseña?» con el usuario cadus.\n";
