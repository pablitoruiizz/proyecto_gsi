<?php
// Auditoría CLI: únicamente contadores/configuración no personal.
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
$_SERVER['HTTP_HOST'] = 'localhost';
define('WP_HTTP_BLOCK_EXTERNAL', true); // Evita comprobaciones remotas durante la auditoría CLI.
require dirname(__DIR__, 2) . '/cms-wordpress/wp-load.php';
global $wpdb;
if (($argv[1] ?? '') === 'listado') {
    $user = get_users(['role' => 'administrator', 'number' => 1])[0];
    $manager = WP_Session_Tokens::get_instance($user->ID);
    $token = $manager->create(time() + 60);
    try {
        $response = wp_remote_get(admin_url('edit.php?post_type=cadus_ticket'), ['headers' => ['Cookie' =>
            AUTH_COOKIE . '=' . wp_generate_auth_cookie($user->ID, time() + 60, 'auth', $token)
            . '; ' . LOGGED_IN_COOKIE . '=' . wp_generate_auth_cookie($user->ID, time() + 60, 'logged_in', $token)]]);
        $body = wp_remote_retrieve_body($response);
        foreach (['RN03-CODEX-ASUNTO', 'RN03-CODEX-SECRETO', 'prueba@alum.us.es'] as $marker) {
            $start = 0;
            while (($position = strpos($body, $marker, $start)) !== false) {
                echo substr($body, max(0, $position - 100), 230), "\n";
                $start = $position + strlen($marker);
            }
        }
    } finally { $manager->destroy($token); }
    exit;
}
$form = (int) get_option('cadus_buzon_form_id');
$info = ['wp' => get_bloginfo('version'), 'form_id' => $form,
    'plugins' => get_option('active_plugins'),
    'tickets' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type='cadus_ticket'"),
    'ff_entries' => (int) $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->prefix}fluentform_submissions WHERE form_id=%d", $form)),
    'ff_notifications' => (int) $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->prefix}fluentform_form_meta WHERE form_id=%d AND meta_key='notifications'", $form)),
    'ff_details_total' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->prefix}fluentform_entry_details"),
    'ff_meta_total' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->prefix}fluentform_submission_meta"),
    'usuarios_prueba' => count(get_users(['meta_key' => '_rn03_audit', 'meta_value' => 'codex-rn03'])),
    'yoast_tickets' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->prefix}yoast_indexable WHERE object_sub_type='cadus_ticket'"),
    'debug' => [WP_DEBUG, defined('WP_DEBUG_LOG') ? WP_DEBUG_LOG : false, ini_get('error_log')],
    'ff_tables' => $wpdb->get_col("SHOW TABLES LIKE '{$wpdb->prefix}fluentform%'"),
];
$info['ff_routes'] = array_values(array_filter(array_keys(rest_get_server()->get_routes()), static fn($r) => stripos($r, 'fluent') !== false));
echo wp_json_encode($info, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), "\n";
