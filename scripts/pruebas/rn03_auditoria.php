<?php
/** Pruebas internas RN-03, complementarias a la batería independiente de Claude. */
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
$_SERVER['HTTP_HOST'] = 'localhost';
$_SERVER['REMOTE_ADDR'] = '192.0.2.91';
define('WP_HTTP_BLOCK_EXTERNAL', true);
require dirname(__DIR__, 2) . '/cms-wordpress/wp-load.php';
global $wpdb;
$action = $argv[1] ?? 'status';
$checks = [];
function rn03_check($label, $ok): void { $GLOBALS['checks'][$label] = (bool) $ok; }
function rn03_ids(): array {
    global $wpdb;
    return $wpdb->get_col("SELECT post_id FROM {$wpdb->postmeta} WHERE meta_key='_rn03_audit' AND meta_value='codex-rn03'");
}
if ($action === 'cleanup') {
    $state = json_decode(stream_get_contents(STDIN), true) ?: [];
    foreach (($state['sessions'] ?? []) as $session) {
        WP_Session_Tokens::get_instance((int) $session['uid'])->destroy($session['token']);
    }
    require_once ABSPATH . 'wp-admin/includes/user.php';
    foreach (get_users(['meta_key' => '_rn03_audit', 'meta_value' => 'codex-rn03']) as $user) {
        wp_delete_user($user->ID);
    }
    foreach (rn03_ids() as $id) {
        $entry = (int) get_post_meta($id, '_cadus_entrada_ff', true);
        if ($entry) { cadus_privacidad_purgar_ff($entry, [], (object) ['id' => (int) get_option('cadus_buzon_form_id')]); }
        wp_delete_post((int) $id, true);
    }
    delete_transient('cadus_seg_' . hash_hmac('sha256', '192.0.2.91', wp_salt('nonce')));
} elseif ($action === 'fixture') {
    $form_id = (int) get_option('cadus_buzon_form_id');
    $mail_count = 0;
    add_filter('pre_wp_mail', function ($result) use (&$mail_count) { ++$mail_count; return true; });
    $ff_sensitive_insert = false;
    add_filter('query', function ($sql) use (&$ff_sensitive_insert) {
        if (preg_match('/^\s*(INSERT|UPDATE)/i', $sql) && str_contains($sql, 'fluentform_')
            && (str_contains($sql, 'RN03-CODEX-SECRETO') || str_contains($sql, 'prueba@alum.us.es'))) {
            $ff_sensitive_insert = true;
        }
        return $sql;
    });
    $data = ['email' => 'prueba@alum.us.es', 'asunto' => 'RN03-CODEX-ASUNTO',
        'descripcion' => 'RN03-CODEX-SECRETO', 'tipo' => 'Reclamación académica', 'consentimiento' => ['acepto'],
        '__fluent_form_embded_post_id' => 18, '_fluentform_' . $form_id . '_fluentformnonce' => wp_create_nonce('fluentform_submit')];
    try {
        $result = (new FluentForm\App\Services\Form\SubmissionHandlerService())->handleSubmission($data, $form_id);
        $id = cadus_buzon_ticket_por_entrada((int) $result['insert_id']);
        if (!$id) { throw new RuntimeException('No se creó el ticket'); }
        update_post_meta($id, '_rn03_audit', 'codex-rn03');
        $code = get_post_meta($id, '_cadus_codigo', true);
        rn03_check('Fluent Forms: envío real conserva contenido en ticket', get_post_field('post_content', $id) === 'RN03-CODEX-SECRETO');
        rn03_check('Código nuevo con 128 bits aleatorios', (bool) preg_match('/^CAD-\d{4}-\d{5,20}-[A-F0-9]{32}$/', $code));
        rn03_check('Confirmación muestra código nuevo', str_contains($result['result']['message'], $code));
        rn03_check('Sin INSERT sensible en tablas FF', !$ff_sensitive_insert);
        foreach (['fluentform_submissions' => 'id', 'fluentform_entry_details' => 'submission_id', 'fluentform_submission_meta' => 'response_id'] as $table => $key) {
            $count = $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->prefix}{$table} WHERE {$key}=%d", $result['insert_id']));
            rn03_check($table . ': sin copia del envío', $count !== null && (int) $count === 0 && !$wpdb->last_error);
        }
        rn03_check('Sin wp_mail', $mail_count === 0);
        rn03_check('Feeds/notificaciones FF bloqueados aunque se configuren', apply_filters('fluentform/global_notification_active_types', ['notifications' => 'email_notifications'], $form_id) === []);
        rn03_check('Otros formularios conservan sus feeds', isset(apply_filters('fluentform/global_notification_active_types', ['notifications' => 'email_notifications'], -1)['notifications']));
        rn03_check('Sin revisiones', !post_type_supports('cadus_ticket', 'revisions') && wp_revisions_to_keep(get_post($id)) === 0);
        rn03_check('Sin exportación', !get_post_type_object('cadus_ticket')->can_export);
        $columns = cadus_buzon_columnas(['title' => 'Título', 'author' => 'Autor', 'date' => 'Fecha']);
        rn03_check('Listado minimizado', !isset($columns['title'], $columns['author']) && !isset($columns['cadus_email']));
        rn03_check('Sin edición masiva', !isset(apply_filters('bulk_actions-edit-cadus_ticket', ['edit' => 'Editar'])['edit']));
        rn03_check('Yoast excluye tipo', apply_filters('wpseo_sitemap_exclude_post_type', false, 'cadus_ticket'));
        foreach (['administrator', 'cadus_ejecutiva', 'cadus_delegado', 'cadus_estudiante', 'subscriber', 'editor'] as $role) {
            $user = new WP_User(); $user->ID = 999999; $user->roles = [$role]; $user->caps = [$role => true]; $user->get_role_caps();
            $allowed = in_array($role, ['administrator', 'cadus_ejecutiva'], true);
            foreach (['read_post', 'edit_post', 'delete_post'] as $cap) {
                rn03_check($role . ': ' . $cap, user_can($user, $cap, $id) === $allowed);
            }
            $user->allcaps['edit_cadus_tickets'] = true;
            rn03_check($role . ': concesión accidental no evita lista cerrada', user_can($user, 'edit_cadus_tickets') === $allowed);
        }
        $nonce = wp_create_nonce('cadus_seguimiento');
        $_POST = ['cadus_seguimiento_nonce' => $nonce, 'cadus_codigo' => $code, 'cadus_correo' => 'PRUEBA@alum.us.es'];
        rn03_check('Seguimiento acepta nuevo código + correo normalizado', str_contains(cadus_buzon_resultado_seguimiento(), 'RN03-CODEX-ASUNTO'));
        $_POST['cadus_correo'] = 'otro@alum.us.es';
        $wrong_email = cadus_buzon_resultado_seguimiento();
        $_POST['cadus_codigo'] = 'CAD-2026-77777';
        rn03_check('Error idéntico código inexistente / correo incorrecto', $wrong_email === cadus_buzon_resultado_seguimiento());
        $legacy = wp_insert_post(['post_type' => 'cadus_ticket', 'post_status' => 'private', 'post_title' => 'RN03-LEGACY']);
        update_post_meta($legacy, '_rn03_audit', 'codex-rn03');
        update_post_meta($legacy, '_cadus_codigo', 'CAD-2026-77777');
        update_post_meta($legacy, '_cadus_email', 'prueba@alum.us.es');
        $_POST['cadus_correo'] = 'prueba@alum.us.es';
        rn03_check('Compatible con código antiguo', str_contains(cadus_buzon_resultado_seguimiento(), 'RN03-LEGACY'));
        $limit = []; for ($i = 0; $i < 7; $i++) { $limit[] = cadus_buzon_permitir_intento(); }
        rn03_check('Límite 10/15 min (4 consultas + 6 permitidas y una denegada)', $limit === [true,true,true,true,true,true,false]);
        $attachment = wp_insert_post(['post_type' => 'attachment', 'post_status' => 'inherit', 'post_parent' => $id,
            'post_title' => 'RN03-ADJUNTO', 'post_mime_type' => 'text/plain']);
        update_post_meta($attachment, '_rn03_audit', 'codex-rn03');
        $sessions = []; $auth = [];
        foreach (['administrator', 'cadus_ejecutiva', 'cadus_delegado', 'cadus_estudiante'] as $role) {
            $users = get_users(['role' => $role, 'number' => $role === 'cadus_ejecutiva' ? 2 : 1]);
            $needed = $role === 'cadus_ejecutiva' ? 2 : 1;
            while (count($users) < $needed) {
                // Sin correo cuando prueba@ ya está ocupado; nunca direcciones reales ni avisos.
                $uid = wp_insert_user(['user_login' => 'rn03_' . bin2hex(random_bytes(8)),
                    'user_pass' => wp_generate_password(40), 'role' => $role,
                    'user_email' => email_exists('prueba@alum.us.es') ? '' : 'prueba@alum.us.es']);
                if (is_wp_error($uid)) { throw new RuntimeException('No se pudo crear usuario de prueba'); }
                update_user_meta($uid, '_rn03_audit', 'codex-rn03');
                $users[] = get_user_by('ID', $uid);
            }
            foreach ($users as $index => $user) {
                $token = WP_Session_Tokens::get_instance($user->ID)->create(time() + 1800);
                $sessions[] = ['uid' => $user->ID, 'token' => $token];
                wp_set_current_user($user->ID);
                $auth[$role . ($index ? '_otra' : '')] = ['cookie' => AUTH_COOKIE . '=' . wp_generate_auth_cookie($user->ID, time() + 1800, 'auth', $token)
                    . '; ' . LOGGED_IN_COOKIE . '=' . wp_generate_auth_cookie($user->ID, time() + 1800, 'logged_in', $token)];
                // El nonce REST se calcula con ese token, sin emitir cookies ni cambiar contraseñas.
                $_COOKIE[LOGGED_IN_COOKIE] = wp_generate_auth_cookie($user->ID, time() + 1800, 'logged_in', $token);
                $auth[$role . ($index ? '_otra' : '')]['nonce'] = wp_create_nonce('wp_rest');
            }
        }
        echo wp_json_encode(compact('id', 'legacy', 'attachment', 'code', 'checks', 'auth', 'sessions')), "\n";
        exit;
    } catch (Throwable $error) {
        echo wp_json_encode(['error' => get_class($error) . ': ' . $error->getMessage(), 'checks' => $checks]), "\n";
        exit(1);
    }
}
echo wp_json_encode(['tickets' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type='cadus_ticket'"),
    'propios' => count(rn03_ids()), 'ff_entries' => (int) $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->prefix}fluentform_submissions WHERE form_id=%d", get_option('cadus_buzon_form_id')))]), "\n";
