<?php
/** RN-03/HU-12: fixtures sintéticos y servicio real FF. Solo CLI; limpieza por marca. */
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
$_SERVER['HTTP_HOST'] = 'localhost';
$_SERVER['REMOTE_ADDR'] = '192.0.2.92';
define('WP_HTTP_BLOCK_EXTERNAL', true);
require dirname(__DIR__, 2) . '/cms-wordpress/wp-load.php';
global $wpdb;
const RN03_MED = 'RN03-MEDIACION-SECRETO';
const RN03_MED_USER = 'RN03-MEDIACION-SOLICITANTE';
const RN03_MED_MARK = 'codex-rn03-mediacion';
$action = $argv[1] ?? 'status';
$form_id = (int) get_option('cadus_mediacion_form_id');
$form = (object) ['id' => $form_id];
$checks = [];
function med_check($label, $ok): void { $GLOBALS['checks'][$label] = (bool) $ok; }
function med_ids(): array {
    global $wpdb;
    return $wpdb->get_col($wpdb->prepare("SELECT DISTINCT p.ID FROM {$wpdb->posts} p LEFT JOIN {$wpdb->postmeta} m ON m.post_id=p.ID
        WHERE (m.meta_key='_rn03_audit' AND m.meta_value=%s) OR (p.post_type='cadus_mediacion' AND p.post_content=%s)", RN03_MED_MARK, RN03_MED));
}
function med_status(): array {
    global $wpdb;
    $forms = [(int) get_option('cadus_buzon_form_id'), (int) get_option('cadus_mediacion_form_id')];
    return [
        'tickets' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type='cadus_ticket'"),
        'solicitudes' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type='cadus_mediacion'"),
        'propios' => count(med_ids()),
        'ff_entries' => (int) $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->prefix}fluentform_submissions WHERE form_id IN (%d,%d)", $forms)),
        'ff_details' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->prefix}fluentform_entry_details"),
        'ff_meta' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->prefix}fluentform_submission_meta"),
        'usuarios_temporales' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->users} WHERE user_login LIKE 'rn03\\_%'"),
    ];
}
function med_data(): array {
    $id = (int) get_option('cadus_mediacion_form_id');
    return ['email' => 'prueba@alum.us.es', 'solicitante' => RN03_MED_USER, 'descripcion' => RN03_MED,
        'centro' => cadus_mediacion_centros()[0], 'consentimiento' => ['acepto'],
        '_fluentform_' . $id . '_fluentformnonce' => wp_create_nonce('fluentform-submit-form'),
        'item_' . $id . '__fluent_sf' => ''];
}
// Ninguna prueba CLI puede emitir correo, ni al crear usuarios ni desde FF.
$mails = 0;
add_filter('pre_wp_mail', function () use (&$mails) { ++$mails; return true; });
if ($action === 'cleanup') {
    require_once ABSPATH . 'wp-admin/includes/user.php';
    foreach (get_users(['meta_key' => '_rn03_audit', 'meta_value' => RN03_MED_MARK]) as $user) {
        wp_delete_user($user->ID); // Incluye todas sus sesiones.
    }
    foreach (med_ids() as $id) {
        $entry = (int) get_post_meta($id, '_cadus_entrada_ff', true);
        if ($entry) { cadus_privacidad_purgar_ff($entry, [], $form); }
        wp_delete_post((int) $id, true);
    }
    delete_transient('cadus_med_' . hash_hmac('sha256', '192.0.2.92', wp_salt('nonce')));
    foreach ((array) get_option('_rn03_med_rate_backup', []) as $key => $saved) {
        if (is_array($saved) && (int) ($saved['fin'] ?? 0) > time()) {
            set_transient($key, $saved, $saved['fin'] - time());
        } else { delete_transient($key); }
    }
    delete_option('_rn03_med_rate_backup');
} elseif ($action === 'cache') {
    // Solo las páginas de formularios privados, a través de la API pública de WP Fastest Cache.
    foreach (['atencion-al-estudiante/mediacion-estudiantil', 'atencion-al-estudiante/buzon-de-consultas'] as $path) {
        $page = get_page_by_path($path);
        if ($page && function_exists('wpfc_clear_post_cache_by_id')) { wpfc_clear_post_cache_by_id($page->ID); }
    }
} elseif ($action === 'fallos') {
    // Intercepta wp_send_json de forma local para inspeccionar el error sin abortar ni emitir correo.
    define('DOING_AJAX', true);
    add_filter('wp_die_ajax_handler', function () {
        return static function () { throw new RuntimeException('rn03_json_interceptado'); };
    });
    $status = 0;
    add_filter('status_header', function ($header, $code) use (&$status) { $status = $code; return $header; }, 10, 2);
    $entry_id = 0;
    add_action('fluentform/submission_inserted', function ($id) use (&$entry_id) { $entry_id = (int) $id; }, 0);
    remove_action('fluentform/submission_inserted', 'cadus_mediacion_crear', 10);
    ob_start();
    try {
        (new FluentForm\App\Services\Form\SubmissionHandlerService())->handleSubmission(med_data(), $form_id);
    } catch (RuntimeException $e) {
        if ($e->getMessage() !== 'rn03_json_interceptado') { throw $e; }
    }
    $body = json_decode(ob_get_clean(), true);
    med_check('Fallo de creación devuelve 500 explícito, sin referencia', $status === 500 && isset($body['errors']['mediacion']));
    med_check('Fallo de creación no deja entrada ni datos FF', $entry_id > 0 && med_status()['ff_entries'] === 0
        && med_status()['ff_details'] === 0 && med_status()['ff_meta'] === 0);
    // El camino de spam omite before_submission_confirmation: prueba la purga alternativa.
    $wpdb->insert($wpdb->prefix . 'fluentform_submissions', ['form_id' => $form_id, 'response' => '{}', 'status' => 'spam']);
    $spam_id = (int) $wpdb->insert_id;
    ob_start();
    try { apply_filters('fluentform/submission_message_parse', 'Gracias', $spam_id, [], $form); }
    catch (RuntimeException $e) { if ($e->getMessage() !== 'rn03_json_interceptado') { throw $e; } }
    ob_end_clean();
    med_check('Camino de spam purga sin before_submission_confirmation', $spam_id > 0 && med_status()['ff_entries'] === 0);
    cadus_privacidad_purgar_ff($entry_id, [], $form);
    cadus_privacidad_purgar_ff($spam_id, [], $form);
    delete_transient('cadus_med_' . hash_hmac('sha256', '192.0.2.92', wp_salt('nonce')));
    echo wp_json_encode(['checks' => $checks]), "\n";
    exit;
} elseif ($action === 'fixture') {
    try {
        $backup = [];
        foreach (['127.0.0.1', '::1'] as $ip) {
            $key = 'cadus_med_' . hash_hmac('sha256', $ip, wp_salt('nonce'));
            $backup[$key] = get_transient($key);
        }
        if (!add_option('_rn03_med_rate_backup', $backup, '', false)) {
            throw new RuntimeException('Ejecuta cleanup antes de repetir la batería');
        }
        $sensitive = false;
        add_filter('query', function ($sql) use (&$sensitive) {
            if (preg_match('/^\s*(INSERT|UPDATE)/i', $sql) && str_contains($sql, 'fluentform_')
                && (str_contains($sql, RN03_MED) || str_contains($sql, RN03_MED_USER) || str_contains($sql, 'prueba@alum.us.es'))) {
                $sensitive = true;
            }
            return $sql;
        });
        $data = med_data();
        foreach (['sin nonce' => ['_fluentform_' . $form_id . '_fluentformnonce' => ''],
            'nonce falso' => ['_fluentform_' . $form_id . '_fluentformnonce' => 'falso'],
            'dominio ajeno' => ['email' => 'prueba@example.com'],
            'subdominio impostor' => ['email' => 'prueba@alum.us.es.example.com'],
            'centro ajeno' => ['centro' => 'CENTRO-INVENTADO'],
            'sin consentimiento' => ['consentimiento' => []],
            'sin descripción' => ['descripcion' => '']] as $label => $change) {
            try {
                (new FluentForm\App\Services\Form\SubmissionHandlerService())->handleSubmission(array_replace($data, $change), $form_id);
                med_check('Servicio rechaza ' . $label, false);
            } catch (FluentForm\Framework\Validator\ValidationException $e) {
                $field = array_key_first($change);
                $field = str_contains($field, 'nonce') ? '_fluentformnonce' : $field;
                med_check('Servicio rechaza ' . $label, in_array($e->getCode(), [422, 423], true) && isset($e->errors()['errors'][$field]));
            }
        }
        $result = (new FluentForm\App\Services\Form\SubmissionHandlerService())->handleSubmission($data, $form_id);
        $id = cadus_mediacion_por_entrada((int) $result['insert_id']);
        if (!$id) { throw new RuntimeException('No se creó la solicitud'); }
        update_post_meta($id, '_rn03_audit', RN03_MED_MARK);
        $code = get_post_meta($id, '_cadus_codigo', true);
        med_check('Servicio real conserva nombre, correo y conflicto en CPT', get_post_field('post_content', $id) === RN03_MED
            && get_post_meta($id, '_cadus_email', true) === $data['email'] && get_post_meta($id, '_cadus_solicitante', true) === RN03_MED_USER);
        med_check('Referencia con 128 bits aleatorios', (bool) preg_match('/^MED-\d{4}-\d{5,20}-[A-F0-9]{32}$/', $code));
        med_check('Confirmación solo referencia, sin datos ni redirección', str_contains($result['result']['message'], $code)
            && !str_contains($result['result']['message'], RN03_MED) && !str_contains($result['result']['message'], $data['email'])
            && !str_contains($result['result']['message'], RN03_MED_USER) && empty($result['result']['redirectUrl']));
        cadus_mediacion_crear($result['insert_id'], $data, $form);
        med_check('Repetición de acción idempotente', count(med_ids()) === 1);
        med_check('Nunca INSERT/UPDATE sensible en FF', !$sensitive);
        foreach (['fluentform_submissions' => 'id', 'fluentform_entry_details' => 'submission_id', 'fluentform_submission_meta' => 'response_id'] as $table => $key) {
            med_check($table . ': sin copia', (int) $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->prefix}{$table} WHERE {$key}=%d", $result['insert_id'])) === 0 && !$wpdb->last_error);
        }
        med_check('Sin wp_mail', $mails === 0);
        med_check('Feeds bloqueados aunque se activen', apply_filters('fluentform/global_notification_active_types', ['notifications' => 'email_notifications'], $form_id) === []);
        med_check('Otros formularios mantienen feeds', isset(apply_filters('fluentform/global_notification_active_types', ['notifications' => 'email_notifications'], -1)['notifications']));
        med_check('Sin revisiones/exportación/REST', wp_revisions_to_keep(get_post($id)) === 0
            && !get_post_type_object('cadus_mediacion')->can_export && !get_post_type_object('cadus_mediacion')->show_in_rest);
        med_check('Sin edición masiva/rápida', !isset(apply_filters('bulk_actions-edit-cadus_mediacion', ['edit' => 'Editar'])['edit'])
            && !apply_filters('quick_edit_enabled_for_post_type', true, 'cadus_mediacion'));
        med_check('Sitemaps nativo y Yoast excluyen mediación', !isset(apply_filters('wp_sitemaps_post_types', ['cadus_mediacion' => true])['cadus_mediacion'])
            && apply_filters('wpseo_sitemap_exclude_post_type', false, 'cadus_mediacion'));
        med_check('Listado sin nombre, centro, correo, título ni autor', array_keys(cadus_mediacion_columnas([])) === ['cb', 'cadus_codigo', 'cadus_estado', 'date']);
        wp_update_post(['ID' => $id, 'post_status' => 'publish', 'post_author' => 1]);
        med_check('Fuerza privado y autor cero al editar', get_post_status($id) === 'private' && (int) get_post_field('post_author', $id) === 0);
        foreach (['administrator', 'cadus_ejecutiva', 'cadus_delegado', 'cadus_estudiante', 'subscriber', 'editor'] as $role) {
            $user = new WP_User(); $user->ID = 999999; $user->roles = [$role]; $user->caps = [$role => true]; $user->get_role_caps();
            $allowed = in_array($role, ['administrator', 'cadus_ejecutiva'], true);
            foreach (['read_post', 'edit_post', 'delete_post'] as $cap) {
                med_check($role . ' ' . $cap, user_can($user, $cap, $id) === $allowed);
            }
            foreach (['read_cadus_mediacion', 'edit_cadus_mediacion', 'delete_cadus_mediacion',
                'read_private_cadus_mediaciones', 'edit_cadus_mediaciones', 'create_cadus_mediaciones', 'publish_cadus_mediaciones'] as $cap) {
                $user->allcaps[$cap] = true;
                med_check($role . ' concesión accidental ' . $cap, user_can($user, $cap, $id) === $allowed);
            }
        }
        $limit = []; for ($i = 0; $i < 10; ++$i) { $limit[] = cadus_privacidad_permitir_mediacion(); }
        med_check('10 envíos/15 min: uno consumido, nueve permitidos y uno denegado', $limit === [true,true,true,true,true,true,true,true,true,false]);
        try {
            (new FluentForm\App\Services\Form\SubmissionHandlerService())->handleSubmission($data, $form_id);
            med_check('Servicio aplica límite', false);
        } catch (FluentForm\Framework\Validator\ValidationException $e) { med_check('Servicio aplica límite', $e->getCode() === 423 && isset($e->errors()['errors']['mediacion'])); }
        $attachment = wp_insert_post(['post_type' => 'attachment', 'post_status' => 'inherit', 'post_parent' => $id,
            'post_title' => 'RN03-MEDIACION-ADJUNTO', 'post_mime_type' => 'text/plain']);
        update_post_meta($attachment, '_rn03_audit', RN03_MED_MARK);
        $auth = [];
        foreach (['administrator', 'cadus_ejecutiva', 'cadus_ejecutiva', 'cadus_delegado', 'cadus_estudiante'] as $index => $role) {
            $uid = wp_insert_user(['user_login' => 'rn03_med_' . bin2hex(random_bytes(8)),
                'user_pass' => wp_generate_password(40), 'role' => $role, 'user_email' => '',
                'meta_input' => ['_rn03_audit' => RN03_MED_MARK]]);
            if (is_wp_error($uid)) { throw new RuntimeException('No se pudo crear usuario temporal'); }
            $token = WP_Session_Tokens::get_instance($uid)->create(time() + 1800);
            wp_set_current_user($uid);
            $_COOKIE[LOGGED_IN_COOKIE] = wp_generate_auth_cookie($uid, time() + 1800, 'logged_in', $token);
            $auth[$role . ($index === 2 ? '_otra' : '')] = [
                'cookie' => AUTH_COOKIE . '=' . wp_generate_auth_cookie($uid, time() + 1800, 'auth', $token) . '; ' . LOGGED_IN_COOKIE . '=' . $_COOKIE[LOGGED_IN_COOKIE],
                'nonce' => wp_create_nonce('wp_rest'),
            ];
        }
        // Consulta REST con filtros suprimidos: la defensa debe reactivarlos, incluso en CLI.
        define('REST_REQUEST', true);
        $found = get_posts(['post_type' => ['cadus_mediacion', 'attachment'], 'post_status' => 'any', 'include' => [$id, $attachment], 'suppress_filters' => true]);
        med_check('WP_Query REST excluye CPT e hijos aun con suppress_filters', $found === []);
        $centro = $data['centro'];
        echo wp_json_encode(compact('id', 'attachment', 'code', 'form_id', 'centro', 'checks', 'auth')), "\n";
        exit;
    } catch (Throwable $error) {
        echo wp_json_encode(['error' => get_class($error) . ': ' . $error->getMessage(), 'checks' => $checks]), "\n";
        exit(1);
    }
}
echo wp_json_encode(med_status()), "\n";
