<?php
/**
 * Correo saliente del portal (aviso de ticket nuevo, aviso de respuesta, contraseña olvidada y relevo de cuenta).
 *
 * 1. Remitente válido: WordPress usa «wordpress@» más el dominio del sitio y, con «localhost», PHPMailer lo rechaza («dirección no
 *    válida») y no sale nada. Si el remitente por defecto no es válido, se usa el de CADUS_SMTP_REMITENTE o, si no existe, el correo de
 *    los avisos del buzón.
 * 2. SMTP opcional: si el servidor no tiene correo propio, el envío se hace por un SMTP configurado en wp-config.php. Las credenciales
 *    NO van en el repositorio ni en la base de datos. Constantes (todas opcionales; sin CADUS_SMTP_SERVIDOR no se toca el envío):
 *      define('CADUS_SMTP_SERVIDOR',  'smtp.gmail.com');
 *      define('CADUS_SMTP_PUERTO',    587);              // por defecto 587
 *      define('CADUS_SMTP_SEGURIDAD', 'tls');            // 'tls' (por defecto), 'ssl' o '' (sin cifrar, solo para pruebas locales)
 *      define('CADUS_SMTP_USUARIO',   'cuenta@ejemplo.org');
 *      define('CADUS_SMTP_CLAVE',     '…');              // con Gmail, una «contraseña de aplicación»
 *      define('CADUS_SMTP_REMITENTE', 'cuenta@ejemplo.org'); // por defecto, el usuario
 *
 * Es la parte de la prueba P5 (envío real de correo) del registro E3-04.
 */
if (!defined('ABSPATH')) {
    exit;
}

function cadus_correo_remitente(): string
{
    if (defined('CADUS_SMTP_REMITENTE') && is_email((string) CADUS_SMTP_REMITENTE)) {
        return (string) CADUS_SMTP_REMITENTE;
    }
    if (defined('CADUS_SMTP_USUARIO') && is_email((string) CADUS_SMTP_USUARIO)) {
        return (string) CADUS_SMTP_USUARIO;
    }
    return function_exists('cadus_buzon_correo_avisos') ? cadus_buzon_correo_avisos() : '';
}

add_filter('wp_mail_from', function ($desde) {
    $valido = is_email((string) $desde) && !preg_match('/@localhost$/i', (string) $desde);
    $propio = cadus_correo_remitente();
    // con un SMTP configurado el remitente tiene que ser el de la cuenta (Gmail y similares rechazan otros)
    return (defined('CADUS_SMTP_SERVIDOR') || !$valido) && $propio !== '' ? $propio : $desde;
});

add_filter('wp_mail_from_name', function ($nombre) {
    return $nombre === 'WordPress' ? 'CADUS' : $nombre;
});

add_action('phpmailer_init', function ($mailer) {
    if (!defined('CADUS_SMTP_SERVIDOR') || (string) CADUS_SMTP_SERVIDOR === '') {
        return;
    }
    $mailer->isSMTP();
    $mailer->Host = (string) CADUS_SMTP_SERVIDOR;
    $mailer->Port = defined('CADUS_SMTP_PUERTO') ? (int) CADUS_SMTP_PUERTO : 587;
    $seguridad = defined('CADUS_SMTP_SEGURIDAD') ? (string) CADUS_SMTP_SEGURIDAD : 'tls';
    $mailer->SMTPSecure = in_array($seguridad, ['tls', 'ssl'], true) ? $seguridad : '';
    $mailer->SMTPAutoTLS = $seguridad !== '';
    if (defined('CADUS_SMTP_USUARIO') && (string) CADUS_SMTP_USUARIO !== '') {
        $mailer->SMTPAuth = true;
        $mailer->Username = (string) CADUS_SMTP_USUARIO;
        $mailer->Password = defined('CADUS_SMTP_CLAVE') ? (string) CADUS_SMTP_CLAVE : '';
    }
});
