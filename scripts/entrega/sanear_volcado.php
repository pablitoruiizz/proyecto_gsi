<?php
if (PHP_SAPI !== 'cli') { http_response_code(403); exit('Solo desde la línea de comandos.'); }
/**
 * Sanea una COPIA de la base de datos del portal para entregarla al profesor: cuentas de demostración, sin datos personales,
 * sin sesiones, sin registros de Wordfence ni de estadísticas y sin claves de instalación.
 * Uso: php scripts/entrega/sanear_volcado.php <base_copia>
 *   1. Restaura el volcado completo en una base nueva (por ejemplo bd_cadus_demo) con mysql.
 *   2. php scripts/entrega/sanear_volcado.php bd_cadus_demo      (se niega a tocar la base real del sitio)
 *   3. CADUS_DB_NAME=bd_cadus_demo php scripts/entrega/volcado_bd.php cms-wordpress/backup-db/bd_cadus_v1_sprint3_demo.sql
 * Escribe cms-wordpress/backup-db/LEEME-volcado-demo.md (ignorado por Git) con las cuentas de demostración y su contraseña.
 */
$_SERVER['HTTP_HOST'] = 'localhost';
require __DIR__ . '/../../cms-wordpress/wp-load.php';
global $wpdb;

$copia = $argv[1] ?? '';
if ($copia === '' || $copia === DB_NAME || !preg_match('/^[A-Za-z0-9_]+$/', $copia)) {
    exit("Indica una base de datos COPIA distinta de la del sitio (" . DB_NAME . ").\n");
}
$wpdb->select($copia); // no devuelve nada, ni si va bien ni si falla: se comprueba con una consulta
if ($wpdb->get_var('SELECT DATABASE()') !== $copia) {
    exit("No se puede abrir la base $copia.\n");
}
$p = $wpdb->prefix; // wp_
$wpdb->query("SET FOREIGN_KEY_CHECKS=0");

// ---- contraseña de demostración (aleatoria; solo queda en el LEEME del volcado)
$clave = wp_generate_password(14, false);
$hash = wp_hash_password($clave);

// ---- usuarios: 1 = administración, 130 = Ejecutiva (rol), 131 = delegación (rol)
$dominio = 'example.org';
$demo = [
    1   => ['demo-admin', 'Demo administración', 'administrator'],
    130 => ['demo-ejecutiva', 'Demo Ejecutiva', 'cadus_ejecutiva'],
    131 => ['demo-delegado', 'Demo delegación', 'cadus_delegado'],
];
$wpdb->query("DELETE FROM {$p}usermeta WHERE user_id NOT IN (1,130)");
$wpdb->query("DELETE FROM {$p}users WHERE ID NOT IN (1,130)");
$wpdb->query("UPDATE {$p}posts SET post_author = 1 WHERE post_author NOT IN (0,1,130)");
$wpdb->query("UPDATE {$p}postmeta SET meta_value = '1' WHERE meta_key = '_edit_last' AND meta_value NOT IN ('1','130')");
$ahora = gmdate('Y-m-d H:i:s');
foreach ($demo as $id => [$login, $nombre, $rol]) {
    $existe = (int) $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$p}users WHERE ID = %d", $id));
    $campos = ['user_login' => $login, 'user_pass' => $hash, 'user_nicename' => $login, 'user_email' => "$login@$dominio",
        'user_url' => '', 'display_name' => $nombre, 'user_activation_key' => '', 'user_status' => 0];
    if ($existe) {
        $wpdb->update("{$p}users", $campos, ['ID' => $id]);
    } else {
        $wpdb->insert("{$p}users", $campos + ['ID' => $id, 'user_registered' => $ahora]);
    }
    $wpdb->query($wpdb->prepare("DELETE FROM {$p}usermeta WHERE user_id = %d", $id));
    $meta = ['nickname' => $login, 'first_name' => '', 'last_name' => '', 'description' => '', 'rich_editing' => 'true',
        'syntax_highlighting' => 'true', 'comment_shortcuts' => 'false', 'admin_color' => 'fresh', 'use_ssl' => '0',
        'show_admin_bar_front' => 'true', 'locale' => '', "{$p}capabilities" => serialize([$rol => true]),
        "{$p}user_level" => $rol === 'administrator' ? '10' : '0'];
    foreach ($meta as $k => $v) {
        $wpdb->insert("{$p}usermeta", ['user_id' => $id, 'meta_key' => $k, 'meta_value' => $v]);
    }
}
$wpdb->query("UPDATE {$p}posts SET post_author = 131 WHERE ID = 32 AND post_type = 'cadus_delegacion'"); // ficha de la ETSII: la edita demo-delegado

// ---- opciones
$wpdb->update("{$p}options", ['option_value' => "demo-admin@$dominio"], ['option_name' => 'admin_email']);
$wpdb->query("DELETE FROM {$p}options WHERE option_name IN ('new_admin_email','wp_statistics_daily_salt','recovery_keys','recovery_mode_email_last_sent')"
    . " OR option_name LIKE '\\_transient\\_%' OR option_name LIKE '\\_site\\_transient\\_%' OR option_name LIKE 'wp\\_statistics\\_cache%'");
$wpdb->query("DELETE FROM {$p}options WHERE option_value LIKE '%100.106.47.100%' OR option_value LIKE '%OneDrive%' OR option_value LIKE '%ruizv%'");
$wpdb->query("UPDATE {$p}yoast_indexable SET permalink = REPLACE(permalink, 'http://100.106.47.100', 'http://localhost')");

// ---- Wordfence y estadísticas: registros, caché y claves
foreach ($wpdb->get_col("SHOW TABLES LIKE '{$p}wf%'") as $t) {
    if (!in_array($t, ["{$p}wfconfig", "{$p}wfls_settings"], true)) {
        $wpdb->query("TRUNCATE TABLE `$t`");
    }
}
$wpdb->query("DELETE FROM {$p}wfconfig WHERE name IN ('apiKey','encKey','longEncKey','wfsbskip','wp_site_url','whitelistHash','activatingIP','lastEmailAddress')"
    . " OR val REGEXP '@|[0-9]+\\\\.[0-9]+\\\\.[0-9]+\\\\.[0-9]+' OR val LIKE '%Users%'");
$wpdb->query("DELETE FROM {$p}wfls_settings WHERE name REGEXP 'secret|site-key|whitelisted|shared-'");
foreach (['statistics_visitor', 'statistics_visitor_relationships', 'statistics_events'] as $t) {
    $wpdb->query("TRUNCATE TABLE `{$p}$t`");
}
$wpdb->query("SET FOREIGN_KEY_CHECKS=1");

// ---- informe
$u = $wpdb->get_results("SELECT ID, user_login, user_email FROM {$p}users ORDER BY ID", ARRAY_A);
echo "Usuarios que quedan: " . count($u) . "\n";
foreach ($u as $f) { echo "  {$f['ID']} {$f['user_login']} {$f['user_email']}\n"; }
echo "usermeta: " . $wpdb->get_var("SELECT COUNT(*) FROM {$p}usermeta") . " | session_tokens: " . $wpdb->get_var("SELECT COUNT(*) FROM {$p}usermeta WHERE meta_key = 'session_tokens'") . "\n";
echo "wfconfig: " . $wpdb->get_var("SELECT COUNT(*) FROM {$p}wfconfig") . " filas | wflogins: " . $wpdb->get_var("SELECT COUNT(*) FROM {$p}wflogins") . " | visitantes: " . $wpdb->get_var("SELECT COUNT(*) FROM {$p}statistics_visitor") . "\n";

$leeme = "# Volcado de demostración de la base de datos del portal CADUS\n\n"
    . "`bd_cadus_v1_sprint3.sql` es una **copia saneada** de la base `bd_cadus` para evaluar el portal: conserva la estructura, los roles, las páginas, las noticias, las actas, las 27 fichas de delegaciones, el calendario y la configuración del plugin.\n\n"
    . "## Qué se quitó\n"
    . "- Las cuentas reales del equipo y sus correos personales, contraseñas cifradas, sesiones y datos de perfil.\n"
    . "- Los registros de inicio de sesión, de actividad y de diagnóstico de Wordfence, y su clave de instalación.\n"
    . "- Los visitantes de las estadísticas, las cachés temporales y las sales.\n"
    . "- No hay tickets, solicitudes de mediación ni cuentas de prueba.\n\n"
    . "## Cuentas de demostración\n"
    . "| Usuario | Rol | Correo (ficticio) |\n|---|---|---|\n"
    . "| `demo-admin` | Administrador | demo-admin@$dominio |\n"
    . "| `demo-ejecutiva` | Ejecutivo del CADUS | demo-ejecutiva@$dominio |\n"
    . "| `demo-delegado` | Delegado de centro (edita solo la ficha de la delegación de la ETSII) | demo-delegado@$dominio |\n\n"
    . "Contraseña de las tres: `$clave`. Son cuentas de demostración: cambia la contraseña si el portal se publica.\n\n"
    . "## Cómo restaurarlo\n"
    . "1. Crear la base `bd_cadus` con cotejamiento `utf8mb4_unicode_ci` e importar el `.sql` (phpMyAdmin › Importar, o `mysql`).\n"
    . "2. Copiar WordPress y `wp-content` y crear `wp-config.php` con los datos de esa base y claves propias.\n"
    . "3. Si la dirección web no es `http://localhost/proyecto_gsi/cms-wordpress`, cambiar `siteurl` y `home` en *Ajustes › Generales*.\n"
    . "4. Entrar con una de las cuentas anteriores y vaciar la caché de WP Fastest Cache.\n\n"
    . "Wordfence no tiene su clave de instalación: al abrirlo pedirá registrarse de nuevo (es opcional para evaluar el portal).\n";
file_put_contents(__DIR__ . '/../../cms-wordpress/backup-db/LEEME-volcado-demo.md', $leeme);
echo "LEEME-volcado-demo.md escrito (con la contraseña de demostración).\n";
