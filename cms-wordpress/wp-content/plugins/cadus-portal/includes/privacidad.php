<?php
/** Privacidad del buzón (RN-03): defensas independientes de la configuración del sitio. */
if (!defined('ABSPATH')) {
    exit;
}

/** Lista cerrada, incluso si otro rol recibe accidentalmente capacidades de tickets. */
function cadus_privacidad_equipo($user): bool
{
    return $user instanceof WP_User && (bool) array_intersect(['administrator', 'cadus_ejecutiva'], $user->roles);
}

add_filter('user_has_cap', function (array $caps, array $required, array $args, WP_User $user): array {
    if (!cadus_privacidad_equipo($user)) {
        foreach (array_unique(array_merge(array_keys($caps), $required)) as $cap) {
            if (str_contains($cap, 'cadus_ticket')) {
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
        $where .= " AND {$wpdb->posts}.post_type <> 'cadus_ticket'"
            . " AND NOT EXISTS (SELECT 1 FROM {$wpdb->posts} cadus_parent WHERE cadus_parent.ID = {$wpdb->posts}.post_parent AND cadus_parent.post_type = 'cadus_ticket')";
    }
    return $where;
}, PHP_INT_MAX);

/** WordPress puede ignorar post_type no consultables y devolver la portada (200). */
add_action('template_redirect', function (): void {
    $types = isset($_GET['post_type']) ? (array) $_GET['post_type'] : [];
    if (in_array('cadus_ticket', $types, true) || isset($_GET['cadus_ticket'])) {
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
    unset($types['cadus_ticket']);
    return $types;
});
add_filter('wpseo_sitemap_exclude_post_type', function ($excluded, $type) {
    return $type === 'cadus_ticket' ? true : $excluded;
}, 10, 2);
add_filter('wp_revisions_to_keep', function ($number, $post) {
    return $post->post_type === 'cadus_ticket' ? 0 : $number;
}, 10, 2);
add_filter('bulk_actions-edit-cadus_ticket', function (array $actions): array {
    unset($actions['edit']); // Evita publicar, modificar autor o estado en lote.
    return $actions;
});
add_filter('quick_edit_enabled_for_post_type', function ($enabled, $type) {
    return $type === 'cadus_ticket' ? false : $enabled;
}, 10, 2);
add_filter('the_title', function ($title, $id) {
    global $pagenow;
    // Las etiquetas accesibles y acciones de fila también incluyen el título.
    if (is_admin() && $pagenow === 'edit.php' && get_post_type($id) === 'cadus_ticket') {
        return (string) get_post_meta($id, '_cadus_codigo', true) ?: 'Ticket';
    }
    return $title;
}, 10, 2);
add_filter('the_posts', function (array $posts): array {
    global $pagenow;
    if (is_admin() && $pagenow === 'edit.php') {
        foreach ($posts as $index => $post) {
            if ($post instanceof WP_Post && $post->post_type === 'cadus_ticket') {
                // WP 7.1 lee post_title directamente para aria-label. Solo la copia de presentación.
                $posts[$index] = clone $post;
                $posts[$index]->post_title = (string) get_post_meta($post->ID, '_cadus_codigo', true) ?: 'Ticket';
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
        if ($post && get_post_type($post->post_parent) === 'cadus_ticket') {
            return new WP_Error('rest_no_route', 'No se ha encontrado ninguna ruta que coincida.', ['status' => 404]);
        }
    }
    return $result;
}, 10, 3);

/** Guarda los datos solo en memoria, antes de cualquier INSERT de Fluent Forms. */
function cadus_privacidad_capturar_ff($data, $form_id)
{
    if ((int) $form_id === (int) get_option('cadus_buzon_form_id', 0) && (int) $form_id > 0) {
        $GLOBALS['cadus_privacidad_ff_original'] = $data;
        return [];
    }
    return $data;
}

function cadus_privacidad_datos_originales($data, $form)
{
    return cadus_buzon_es_formulario($form) && isset($GLOBALS['cadus_privacidad_ff_original'])
        ? $GLOBALS['cadus_privacidad_ff_original'] : $data;
}

add_filter('fluentform/insert_response_data', 'cadus_privacidad_capturar_ff', PHP_INT_MAX, 2);
add_filter('fluentform/filter_insert_data', function ($data) {
    if ((int) ($data['form_id'] ?? 0) === (int) get_option('cadus_buzon_form_id', 0)) {
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
    return (int) $form_id === (int) get_option('cadus_buzon_form_id', 0) ? [] : $types;
}, PHP_INT_MAX, 2);

/** El ticket ya existe; su vínculo de idempotencia no depende de conservar la entrada. */
function cadus_privacidad_purgar_ff($entry_id, $data, $form): void
{
    if (!cadus_buzon_es_formulario($form)) {
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

// Defensa adicional en el punto donde WP Fastest Cache decide escribir el HTML.
add_filter('wpfc_buffer_callback_filter', function ($buffer) {
    return defined('DONOTCACHEPAGE') && DONOTCACHEPAGE ? '' : $buffer;
}, PHP_INT_MAX);
