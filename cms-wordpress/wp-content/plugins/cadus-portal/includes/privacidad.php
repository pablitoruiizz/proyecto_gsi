<?php
/** Privacidad del buzón y mediación (RN-03): independiente de la configuración del sitio. */
if (!defined('ABSPATH')) {
    exit;
}

function cadus_privacidad_tipos(): array
{
    return ['cadus_ticket', 'cadus_mediacion'];
}

function cadus_privacidad_tipo($type): bool
{
    return in_array($type, cadus_privacidad_tipos(), true);
}

function cadus_privacidad_formulario($id): bool
{
    return (int) $id > 0 && in_array((int) $id, [
        (int) get_option('cadus_buzon_form_id', 0), (int) get_option('cadus_mediacion_form_id', 0),
    ], true);
}

/** Lista cerrada, incluso si otro rol recibe accidentalmente capacidades privadas. */
function cadus_privacidad_equipo($user): bool
{
    return $user instanceof WP_User && (bool) array_intersect(['administrator', 'cadus_ejecutiva'], $user->roles);
}

add_filter('user_has_cap', function (array $caps, array $required, array $args, WP_User $user): array {
    if (!cadus_privacidad_equipo($user)) {
        foreach (array_unique(array_merge(array_keys($caps), $required)) as $cap) {
            // El prefijo singular cubre también cadus_tickets y cadus_mediaciones.
            if (str_contains($cap, 'cadus_ticket') || str_contains($cap, 'cadus_mediacion')) {
                $caps[$cap] = false;
            }
        }
    }
    return $caps;
}, PHP_INT_MAX, 4);

/** CLI de mantenimiento y panel autorizado; nunca las consultas del sitio ni REST. */
function cadus_privacidad_consulta_interna(): bool
{
    return (PHP_SAPI === 'cli' && !(defined('REST_REQUEST') && REST_REQUEST))
        || (is_admin() && !(defined('REST_REQUEST') && REST_REQUEST) && cadus_privacidad_equipo(wp_get_current_user()));
}

add_action('pre_get_posts', function (WP_Query $query): void {
    if (!cadus_privacidad_consulta_interna()) {
        // Incluye get_posts()/widgets que normalmente suprimen filtros SQL.
        $query->set('suppress_filters', false);
    }
}, PHP_INT_MAX);

add_filter('posts_where', function (string $where): string {
    global $wpdb;
    if (!cadus_privacidad_consulta_interna()) {
        $types = implode(',', array_fill(0, count(cadus_privacidad_tipos()), '%s'));
        $where .= $wpdb->prepare(" AND {$wpdb->posts}.post_type NOT IN ($types)"
            . " AND NOT EXISTS (SELECT 1 FROM {$wpdb->posts} cadus_parent WHERE cadus_parent.ID = {$wpdb->posts}.post_parent AND cadus_parent.post_type IN ($types))",
            array_merge(cadus_privacidad_tipos(), cadus_privacidad_tipos()));
    }
    return $where;
}, PHP_INT_MAX);

/** WordPress puede ignorar post_type no consultables y devolver la portada (200). */
add_action('template_redirect', function (): void {
    $types = isset($_GET['post_type']) ? (array) $_GET['post_type'] : [];
    if (array_intersect(cadus_privacidad_tipos(), array_filter($types, 'is_string'))
        || array_intersect(cadus_privacidad_tipos(), array_keys($_GET))) {
        global $wp_query;
        $wp_query->set_404();
        $wp_query->posts = [];
        $wp_query->post_count = 0;
        status_header(404);
        cadus_buzon_no_cache();
        remove_action('template_redirect', 'redirect_canonical');
    }
}, -1);

add_filter('wp_sitemaps_post_types', function (array $types): array {
    foreach (cadus_privacidad_tipos() as $type) {
        unset($types[$type]);
    }
    return $types;
});
add_filter('wpseo_sitemap_exclude_post_type', function ($excluded, $type) {
    return cadus_privacidad_tipo($type) ? true : $excluded;
}, 10, 2);
add_filter('wp_revisions_to_keep', function ($number, $post) {
    return cadus_privacidad_tipo($post->post_type) ? 0 : $number;
}, 10, 2);
foreach (cadus_privacidad_tipos() as $type) {
    add_filter('bulk_actions-edit-' . $type, function (array $actions): array {
        unset($actions['edit']); // Evita publicar, modificar autor o estado en lote.
        return $actions;
    });
}
add_filter('quick_edit_enabled_for_post_type', function ($enabled, $type) {
    return cadus_privacidad_tipo($type) ? false : $enabled;
}, 10, 2);
add_filter('the_title', function ($title, $id) {
    global $pagenow;
    // Las etiquetas accesibles y acciones de fila también incluyen el título.
    if (is_admin() && $pagenow === 'edit.php' && cadus_privacidad_tipo(get_post_type($id))) {
        return (string) get_post_meta($id, '_cadus_codigo', true) ?: 'Referencia';
    }
    return $title;
}, 10, 2);
add_filter('the_posts', function (array $posts): array {
    global $pagenow;
    if (is_admin() && $pagenow === 'edit.php') {
        foreach ($posts as $index => $post) {
            if ($post instanceof WP_Post && cadus_privacidad_tipo($post->post_type)) {
                // WP 7.1 lee post_title directamente para aria-label. Solo la copia de presentación.
                $posts[$index] = clone $post;
                $posts[$index]->post_title = (string) get_post_meta($post->ID, '_cadus_codigo', true) ?: 'Referencia';
                $posts[$index]->post_content = '';
                $posts[$index]->post_excerpt = '';
            }
        }
    }
    return $posts;
}, 10);

/** El controlador de un medio individual usa get_post(), no WP_Query. */
add_filter('rest_pre_dispatch', function ($result, $server, WP_REST_Request $request) {
    if (preg_match('#^/wp/v2/media/([0-9]+)(?:/|$)#', $request->get_route(), $match)) {
        $post = get_post((int) $match[1]);
        if ($post && cadus_privacidad_tipo(get_post_type($post->post_parent))) {
            return new WP_Error('rest_no_route', 'No se ha encontrado ninguna ruta que coincida.', ['status' => 404]);
        }
    }
    return $result;
}, 10, 3);

/** Guarda los datos solo en memoria, antes de cualquier INSERT de Fluent Forms. */
function cadus_privacidad_capturar_ff($data, $form_id)
{
    if (cadus_privacidad_formulario($form_id)) {
        cadus_buzon_no_cache();
        $GLOBALS['cadus_privacidad_ff_original'][(int) $form_id] = $data;
        return [];
    }
    return $data;
}

function cadus_privacidad_datos_originales($data, $form)
{
    $id = is_object($form) ? (int) ($form->id ?? 0) : 0;
    return cadus_privacidad_formulario($id) && isset($GLOBALS['cadus_privacidad_ff_original'][$id])
        ? $GLOBALS['cadus_privacidad_ff_original'][$id] : $data;
}

add_filter('fluentform/insert_response_data', 'cadus_privacidad_capturar_ff', PHP_INT_MAX, 2);
add_filter('fluentform/filter_insert_data', function ($data) {
    if (cadus_privacidad_formulario($data['form_id'] ?? 0)) {
        $data['response'] = '{}';
        foreach (['ip', 'source_url', 'browser', 'device', 'country'] as $key) {
            $data[$key] = '';
        }
        $data['user_id'] = 0;
    }
    return $data;
}, PHP_INT_MAX);

// No correos, integraciones, colas ni logs con el contenido de este formulario.
add_filter('fluentform/global_notification_active_types', function ($types, $form_id) {
    return cadus_privacidad_formulario($form_id) ? [] : $types;
}, PHP_INT_MAX, 2);

/** El vínculo de idempotencia no depende de conservar la entrada. También purga si falla. */
function cadus_privacidad_purgar_ff($entry_id, $data, $form): void
{
    if (!is_object($form) || !cadus_privacidad_formulario($form->id ?? 0)) {
        return;
    }
    global $wpdb;
    foreach (['fluentform_entry_details' => 'submission_id', 'fluentform_submission_meta' => 'response_id'] as $suffix => $key) {
        $wpdb->delete($wpdb->prefix . $suffix, [$key => (int) $entry_id], ['%d']);
    }
    $wpdb->delete($wpdb->prefix . 'fluentform_submissions', ['id' => (int) $entry_id, 'form_id' => (int) $form->id], ['%d', '%d']);
}
add_action('fluentform/before_submission_confirmation', 'cadus_privacidad_purgar_ff', PHP_INT_MAX, 3);

// También purga el camino de spam que salta before_submission_confirmation.
add_filter('fluentform/submission_message_parse', function ($message, $id, $data, $form) {
    cadus_privacidad_purgar_ff($id, $data, $form);
    return $message;
}, 98, 4);

/** El nonce existe en el HTML de FF, pero su comprobación está desactivada por defecto. */
foreach (['fluentform/nonce_verify', 'fluentform/honeypot_status'] as $hook) {
    add_filter($hook, function ($enabled, $form_id) {
        return (int) $form_id > 0 && (int) $form_id === (int) get_option('cadus_mediacion_form_id', 0)
            ? true : $enabled;
    }, PHP_INT_MAX, 2);
}

/** Límite independiente del seguimiento; sin guardar correo ni IP en claro. */
function cadus_privacidad_permitir_mediacion(): bool
{
    $ip = cadus_buzon_input($_SERVER, 'REMOTE_ADDR');
    $ip = filter_var($ip, FILTER_VALIDATE_IP) ? $ip : 'sin_ip';
    $key = 'cadus_med_' . hash_hmac('sha256', $ip, wp_salt('nonce'));
    $lock = cadus_buzon_lock($key);
    if ($lock === '') {
        return false;
    }
    try {
        if (!wp_using_ext_object_cache()) {
            wp_cache_delete('_transient_' . $key, 'options');
            wp_cache_delete('_transient_timeout_' . $key, 'options');
        }
        $window = get_transient($key);
        $now = time();
        if (!is_array($window) || (int) ($window['fin'] ?? 0) <= $now) {
            $window = ['intentos' => 0, 'fin' => $now + 15 * MINUTE_IN_SECONDS];
        }
        if ((int) $window['intentos'] >= 10) {
            return false;
        }
        ++$window['intentos'];
        return set_transient($key, $window, max(1, (int) $window['fin'] - $now));
    } finally {
        cadus_buzon_unlock($lock);
    }
}
add_filter('fluentform/validation_errors', function ($errors, $data, $form) {
    if (cadus_mediacion_es_formulario($form) && !$errors && !cadus_privacidad_permitir_mediacion()) {
        $errors['mediacion'][] = 'Has alcanzado el límite de envíos. Espera quince minutos antes de volver a intentarlo.';
    }
    return $errors;
}, PHP_INT_MAX, 3);

/** Antes de validar, incluso los errores de nonce y antispam deben ser no-store. */
add_filter('fluentform/nonce_verify', function ($enabled, $form_id) {
    if (cadus_privacidad_formulario($form_id)) {
        cadus_buzon_no_cache();
    }
    return $enabled;
}, PHP_INT_MAX, 2);
add_action('template_redirect', function (): void {
    $post = get_queried_object();
    if ($post instanceof WP_Post && (has_shortcode($post->post_content, 'cadus_mediacion')
        || has_shortcode($post->post_content, 'cadus_buzon'))) {
        cadus_buzon_no_cache();
    }
}, 0);
// También funciona si se inserta directamente [fluentform id="..."] o desde una plantilla.
add_action('fluentform/before_form_render', function ($form): void {
    if (cadus_privacidad_formulario($form->id ?? 0)) {
        cadus_buzon_no_cache();
    }
}, 0);
add_action('admin_init', function (): void {
    $id = absint($_GET['post'] ?? $_POST['post_ID'] ?? 0);
    $post = $id ? get_post($id) : null;
    if (cadus_privacidad_tipo($_GET['post_type'] ?? '')
        || ($post && (cadus_privacidad_tipo($post->post_type) || cadus_privacidad_tipo(get_post_type($post->post_parent))))) {
        cadus_buzon_no_cache();
    }
});

// Defensa adicional en el punto donde WP Fastest Cache decide escribir el HTML.
add_filter('wpfc_buffer_callback_filter', function ($buffer) {
    return defined('DONOTCACHEPAGE') && DONOTCACHEPAGE ? '' : $buffer;
}, PHP_INT_MAX);
