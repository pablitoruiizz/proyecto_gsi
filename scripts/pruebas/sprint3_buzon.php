<?php
/**
 * Sprint 3 · buzón: campo trampa y límite de envíos (HU-17a), búsqueda del panel sin datos del estudiante (HU-16b)
 * y aviso a la Ejecutiva con los datos mínimos (E3-08). Amplía la batería de privacidad (RN-03).
 * Solo CLI. Todo lo que crea lleva una marca y se borra con «cleanup». La usa sprint3_buzon.py.
 *   php sprint3_buzon.php status | fixture | cleanup
 */
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
$_SERVER['HTTP_HOST'] = 'localhost';
$_SERVER['REMOTE_ADDR'] = '192.0.2.93';
define('WP_HTTP_BLOCK_EXTERNAL', true);
require dirname(__DIR__, 2) . '/cms-wordpress/wp-load.php';
global $wpdb;
const S3_SECRETO = 'S3-BUZON-SECRETO';
const S3_ASUNTO = 'S3-BUZON-ASUNTO';
const S3_NOMBRE = 'S3-BUZON-NOMBRE';
const S3_CENTRO = 'S3-CENTRO-TEMPORAL';
const S3_MARCA = 'claude-s3-buzon';
const S3_CORREO_PRUEBA = 'avisos-prueba@example.invalid';
$action = $argv[1] ?? 'status';
$form_id = (int) get_option('cadus_buzon_form_id');
$form = (object) ['id' => $form_id];
$checks = [];
function s3_check(string $label, $ok): void { $GLOBALS['checks'][$label] = (bool) $ok; }
function s3_ids(): array {
    global $wpdb;
    return array_map('intval', $wpdb->get_col($wpdb->prepare("SELECT DISTINCT p.ID FROM {$wpdb->posts} p LEFT JOIN {$wpdb->postmeta} m ON m.post_id=p.ID
        WHERE (m.meta_key='_rn03_audit' AND m.meta_value=%s) OR (p.post_type='cadus_ticket' AND p.post_content=%s)", S3_MARCA, S3_SECRETO)));
}
function s3_status(): array {
    global $wpdb, $form_id;
    return [
        'tickets' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type='cadus_ticket'"),
        'propios' => count(s3_ids()),
        'ff_entries' => (int) $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->prefix}fluentform_submissions WHERE form_id=%d", $form_id)),
        'usuarios_temporales' => (int) $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->users} WHERE user_login LIKE 's3\\_buz\\_%'"),
        'centro_temporal' => term_exists(S3_CENTRO, 'cadus_centro') ? 1 : 0,
    ];
}
function s3_data(): array {
    global $form_id;
    return ['solicitante' => S3_NOMBRE, 'email' => 'prueba@alum.us.es', 'centro' => cadus_mediacion_centros()[0],
        'asunto' => S3_ASUNTO, 'tipo' => 'Consulta', 'descripcion' => S3_SECRETO, 'consentimiento' => ['acepto'],
        '_fluentform_' . $form_id . '_fluentformnonce' => wp_create_nonce('fluentform-submit-form'),
        'item_' . $form_id . '__fluent_sf' => ''];
}
function s3_clave(string $prefijo, string $ip): string { return 'cadus_' . $prefijo . '_' . hash_hmac('sha256', $ip, wp_salt('nonce')); }
function s3_buscar(string $termino): array {
    return array_map('intval', (new WP_Query(['post_type' => 'cadus_ticket', 'post_status' => 'private', 'fields' => 'ids',
        's' => $termino, 'posts_per_page' => 50, 'no_found_rows' => true]))->posts);
}
// Ninguna prueba CLI emite correo de verdad: se captura para inspeccionarlo.
$mails = [];
add_filter('pre_wp_mail', function ($null, $atts) use (&$mails) { $mails[] = $atts; return true; }, 10, 2);

if ($action === 'cleanup') {
    require_once ABSPATH . 'wp-admin/includes/user.php';
    foreach (get_users(['meta_key' => '_rn03_audit', 'meta_value' => S3_MARCA]) as $user) {
        wp_delete_user($user->ID); // Incluye todas sus sesiones.
    }
    foreach (s3_ids() as $id) {
        $entry = (int) get_post_meta($id, '_cadus_entrada_ff', true);
        if ($entry) { cadus_privacidad_purgar_ff($entry, [], $form); }
        wp_delete_post($id, true);
    }
    $term = get_term_by('name', S3_CENTRO, 'cadus_centro');
    if ($term) { wp_delete_term((int) $term->term_id, 'cadus_centro'); }
    foreach (['buz', 'med'] as $prefijo) { delete_transient(s3_clave($prefijo, '192.0.2.93')); }
    $backup = get_option('_s3_buzon_backup');
    if (is_array($backup)) {
        foreach ((array) ($backup['limites'] ?? []) as $key => $saved) {
            if (is_array($saved) && (int) ($saved['fin'] ?? 0) > time()) {
                set_transient($key, $saved, $saved['fin'] - time());
            } else { delete_transient($key); }
        }
        if (($backup['correo'] ?? null) === null) { delete_option('cadus_buzon_correo_avisos'); }
        else { update_option('cadus_buzon_correo_avisos', $backup['correo']); }
    }
    delete_option('_s3_buzon_backup');
    echo wp_json_encode(s3_status()), "\n";
    exit;
}
if ($action === 'fixture') {
    try {
        if (!cadus_buzon_formulario_existe($form_id)) { throw new RuntimeException('No existe el formulario del buzón'); }
        // Se guardan el límite real de localhost y el correo de avisos para restaurarlos en cleanup.
        $limites = [];
        foreach (['127.0.0.1', '::1'] as $ip) { $limites[s3_clave('buz', $ip)] = get_transient(s3_clave('buz', $ip)); }
        s3_check('E3-08 · el aviso va por defecto a dcadus@us.es', get_option('cadus_buzon_correo_avisos', null) !== null
            || cadus_buzon_correo_avisos() === 'dcadus@us.es');
        if (!add_option('_s3_buzon_backup', ['limites' => $limites, 'correo' => get_option('cadus_buzon_correo_avisos', null)], '', false)) {
            throw new RuntimeException('Ejecuta cleanup antes de repetir la batería');
        }
        // Las pruebas por HTTP no pueden interceptar el correo: mientras duran, el aviso va a una dirección que no existe.
        update_option('cadus_buzon_correo_avisos', S3_CORREO_PRUEBA);

        // --- HU-17a: nonce y campo trampa activos en los dos formularios privados, y solo en ellos.
        $med_id = (int) get_option('cadus_mediacion_form_id');
        foreach (['fluentform/nonce_verify' => 'nonce', 'fluentform/honeypot_status' => 'campo trampa'] as $hook => $nombre) {
            s3_check("HU-17a · $nombre obligatorio en el buzón", apply_filters($hook, false, $form_id) === true);
            s3_check("HU-17a · $nombre obligatorio en la mediación", $med_id > 0 && apply_filters($hook, false, $med_id) === true);
            s3_check("HU-17a · $nombre no se impone a otros formularios", apply_filters($hook, false, 999999) === false);
        }
        s3_check('HU-17a · mensaje del campo trampa en español', str_contains((string) apply_filters('fluentform/honeypot_spam_message', 'x', $form_id), 'No hemos podido'));

        // --- E3-08: el formulario tiene los datos mínimos y los centros se leen de la taxonomía.
        cadus_buzon_asegurar_campos();
        $campos = json_decode((string) $wpdb->get_var($wpdb->prepare("SELECT form_fields FROM {$wpdb->prefix}fluentform_forms WHERE id=%d", $form_id)), true);
        $nombres = array_map(static fn($c) => $c['attributes']['name'] ?? '', $campos['fields'] ?? []);
        s3_check('E3-08 · el formulario pide nombre, correo y centro', !array_diff(['solicitante', 'email', 'centro', 'asunto', 'tipo', 'descripcion', 'consentimiento'], $nombres));
        s3_check('E3-08 · el formulario no pide más datos personales', !array_diff($nombres, ['solicitante', 'email', 'centro', 'asunto', 'tipo', 'descripcion', 'consentimiento']));
        wp_insert_term(S3_CENTRO, 'cadus_centro');
        $campo_centro = ['element' => 'select', 'attributes' => ['name' => 'centro'], 'settings' => ['advanced_options' => []]];
        $al_dia = apply_filters('fluentform/rendering_field_data_select', $campo_centro, $form);
        s3_check('E3-08 · un centro nuevo aparece en el desplegable sin tocar el formulario',
            in_array(S3_CENTRO, array_column($al_dia['settings']['advanced_options'], 'value'), true));
        s3_check('E3-08 · el desplegable de otro formulario no se toca',
            apply_filters('fluentform/rendering_field_data_select', $campo_centro, (object) ['id' => 999999]) === $campo_centro);
        s3_check('E3-08 · validación acepta el centro nuevo', cadus_buzon_validar([], array_replace(s3_data(), ['centro' => S3_CENTRO]), $form, []) === []);

        $sensible = false;
        add_filter('query', function ($sql) use (&$sensible) {
            if (preg_match('/^\s*(INSERT|UPDATE)/i', $sql) && str_contains($sql, 'fluentform_')
                && (str_contains($sql, S3_SECRETO) || str_contains($sql, S3_NOMBRE) || str_contains($sql, S3_ASUNTO) || str_contains($sql, 'prueba@alum.us.es'))) {
                $sensible = true;
            }
            return $sql;
        });
        $data = s3_data();
        $nonce_key = '_fluentform_' . $form_id . '_fluentformnonce';
        foreach (['sin nonce' => [$nonce_key => ''], 'nonce falso' => [$nonce_key => 'falso'],
            'sin nombre' => ['solicitante' => ''], 'centro inventado' => ['centro' => 'CENTRO-INVENTADO'],
            'dominio ajeno' => ['email' => 'prueba@example.com'], 'sin consentimiento' => ['consentimiento' => []]] as $label => $change) {
            try {
                (new FluentForm\App\Services\Form\SubmissionHandlerService())->handleSubmission(array_replace($data, $change), $form_id);
                s3_check('Servicio rechaza ' . $label, false);
            } catch (FluentForm\Framework\Validator\ValidationException $e) {
                $field = array_key_first($change);
                $field = str_contains($field, 'nonce') ? '_fluentformnonce' : $field;
                s3_check('Servicio rechaza ' . $label, in_array($e->getCode(), [422, 423], true) && isset($e->errors()['errors'][$field]));
            }
        }
        s3_check('Los envíos rechazados no gastan intentos del límite', get_transient(s3_clave('buz', '192.0.2.93')) === false);
        s3_check('Los envíos rechazados no avisan a la Ejecutiva', $mails === []);

        $result = (new FluentForm\App\Services\Form\SubmissionHandlerService())->handleSubmission($data, $form_id);
        $id = cadus_buzon_ticket_por_entrada((int) $result['insert_id']);
        if (!$id) { throw new RuntimeException('No se creó el ticket'); }
        update_post_meta($id, '_rn03_audit', S3_MARCA);
        $code = (string) get_post_meta($id, '_cadus_codigo', true);
        s3_check('E3-08 · el ticket guarda nombre, centro y correo', get_post_meta($id, '_cadus_solicitante', true) === S3_NOMBRE
            && get_post_meta($id, '_cadus_centro', true) === $data['centro'] && get_post_meta($id, '_cadus_email', true) === $data['email']);
        s3_check('Confirmación con el código y sin datos del estudiante', str_contains($result['result']['message'], $code)
            && !str_contains($result['result']['message'], S3_NOMBRE) && !str_contains($result['result']['message'], $data['email'])
            && !str_contains($result['result']['message'], S3_SECRETO));
        s3_check('Sin INSERT/UPDATE sensible en las tablas de Fluent Forms', !$sensible);
        s3_check('Sin copia del envío en Fluent Forms', s3_status()['ff_entries'] === 0);

        // --- E3-08: un único aviso a la Ejecutiva, sin datos del estudiante ni contenido (RN-03).
        $mail = $mails[0] ?? [];
        $texto = wp_json_encode($mail, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        s3_check('E3-08 · un único correo por ticket nuevo', count($mails) === 1);
        s3_check('E3-08 · el correo va a la dirección de avisos', ($mail['to'] ?? '') === S3_CORREO_PRUEBA);
        s3_check('E3-08 · el correo lleva el código y el enlace al panel', str_contains($texto, $code) && str_contains($texto, 'post.php?post=' . $id));
        $fugas = array_filter([S3_NOMBRE, S3_ASUNTO, S3_SECRETO, 'prueba@alum.us.es', $data['centro']], static fn($s) => str_contains($texto, $s));
        s3_check('E3-08 · el correo no lleva nombre, correo, centro, asunto ni descripción', $fugas === []);
        s3_check('E3-08 · el envío del aviso queda anotado en el ticket', !in_array(get_post_meta($id, '_cadus_aviso_ejecutiva', true), ['', 'error'], true));
        cadus_buzon_crear_ticket($result['insert_id'], $data, $form);
        s3_check('Repetir la acción no duplica el ticket ni el aviso', count(s3_ids()) === 1 && count($mails) === 1);

        // --- HU-16b: la búsqueda del panel solo mira el título (código y asunto).
        $hex = substr($code, -12);
        s3_check('HU-16b · busca por asunto', s3_buscar(S3_ASUNTO) === [$id]);
        s3_check('HU-16b · busca por un trozo del código', s3_buscar($hex) === [$id]);
        s3_check('HU-16b · no busca en la descripción', s3_buscar(S3_SECRETO) === []);
        s3_check('HU-16b · no busca por el correo del estudiante', s3_buscar('prueba@alum.us.es') === []);
        s3_check('HU-16b · no busca por el nombre del estudiante', s3_buscar(S3_NOMBRE) === []);
        $q = new WP_Query();
        $q->set('post_type', 'post');
        $columnas = ['post_title', 'post_excerpt', 'post_content'];
        s3_check('HU-16b · la búsqueda de noticias no cambia', apply_filters('post_search_columns', $columnas, 'x', $q) === $columnas);
        $q->set('post_type', 'cadus_mediacion');
        s3_check('HU-16b · la búsqueda de mediaciones tampoco mira la descripción', apply_filters('post_search_columns', $columnas, 'x', $q) === ['post_title']);
        s3_check('HU-16b · el listado sigue sin título, autor, correo ni nombre',
            array_keys(cadus_buzon_columnas([])) === ['cb', 'cadus_codigo', 'cadus_tipo', 'cadus_estado', 'date']);

        // --- HU-17a: 10 envíos válidos por IP cada 15 minutos, con cuenta separada de la mediación.
        $limit = [];
        for ($i = 0; $i < 10; ++$i) { $limit[] = cadus_privacidad_permitir_buzon(); }
        s3_check('HU-17a · límite del buzón: uno gastado, nueve permitidos y el siguiente denegado',
            $limit === [true, true, true, true, true, true, true, true, true, false]);
        try {
            (new FluentForm\App\Services\Form\SubmissionHandlerService())->handleSubmission(s3_data(), $form_id);
            s3_check('HU-17a · el servicio aplica el límite', false);
        } catch (FluentForm\Framework\Validator\ValidationException $e) {
            s3_check('HU-17a · el servicio aplica el límite', isset($e->errors()['errors']['buzon']));
        }
        s3_check('HU-17a · superar el límite no crea ticket ni aviso', count(s3_ids()) === 1 && count($mails) === 1);
        s3_check('HU-17a · el límite de la mediación va aparte', cadus_privacidad_permitir_mediacion() === true);
        delete_transient(s3_clave('buz', '192.0.2.93'));

        // --- Sesiones temporales para comprobar el panel por HTTP (Ejecutiva y delegado).
        $auth = [];
        foreach (['cadus_ejecutiva', 'cadus_delegado'] as $role) {
            $uid = wp_insert_user(['user_login' => 's3_buz_' . bin2hex(random_bytes(8)), 'user_pass' => wp_generate_password(40),
                'role' => $role, 'user_email' => '', 'meta_input' => ['_rn03_audit' => S3_MARCA]]);
            if (is_wp_error($uid)) { throw new RuntimeException('No se pudo crear el usuario temporal'); }
            $token = WP_Session_Tokens::get_instance($uid)->create(time() + 1800);
            $auth[$role] = ['cookie' => AUTH_COOKIE . '=' . wp_generate_auth_cookie($uid, time() + 1800, 'auth', $token)
                . '; ' . LOGGED_IN_COOKIE . '=' . wp_generate_auth_cookie($uid, time() + 1800, 'logged_in', $token), 'nonce' => ''];
        }
        $centro = $data['centro'];
        echo wp_json_encode(compact('id', 'code', 'hex', 'form_id', 'centro', 'checks', 'auth')), "\n";
        exit;
    } catch (Throwable $error) {
        echo wp_json_encode(['error' => get_class($error) . ': ' . $error->getMessage(), 'checks' => $checks]), "\n";
        exit(1);
    }
}
echo wp_json_encode(s3_status()), "\n";
