<?php
/**
 * Solicitud de mediación estudiantil (HU-12 · RF-13 · IR-08 · RN-02, RN-03 · RNF-04, RNF-08).
 *
 * Reutiliza el patrón del buzón (includes/buzon.php): formulario de Fluent Forms creado por código,
 * validación del correo @alum.us.es también en el servidor y un tipo de contenido privado donde se
 * guarda cada solicitud. Depende de buzon.php (cadus_buzon_email, cadus_buzon_input, cadus_buzon_campo,
 * cadus_buzon_lock, cadus_buzon_tablas_disponibles y cadus_buzon_formulario_existe).
 *
 * Datos de IR-08: solicitante, Facultad o Escuela, descripción del conflicto, fecha de la solicitud
 * (la fecha de publicación del contenido) y estado de la solicitud.
 *
 * Privacidad: las solicitudes no son públicas ni accesibles por la API REST. Solo las ven quienes
 * tienen la capacidad read_private_cadus_mediaciones (Ejecutiva y administrador).
 */

if (!defined('ABSPATH')) {
    exit;
}

function cadus_mediacion_estados(): array
{
    return ['pendiente' => 'Pendiente', 'en_proceso' => 'En proceso', 'cerrada' => 'Cerrada'];
}

/** Nombres de las Facultades y Escuelas disponibles (taxonomía cadus_centro del directorio). */
function cadus_mediacion_centros(): array
{
    $terms = get_terms(['taxonomy' => 'cadus_centro', 'hide_empty' => false, 'orderby' => 'name']);
    return is_wp_error($terms) ? [] : array_values(array_map('strval', wp_list_pluck($terms, 'name')));
}

function cadus_mediacion_registrar(): void
{
    register_post_type('cadus_mediacion', [
        'label' => 'Solicitudes de mediación',
        'labels' => [
            'name' => 'Solicitudes de mediación', 'singular_name' => 'Solicitud de mediación',
            'add_new' => 'Añadir solicitud', 'add_new_item' => 'Añadir solicitud de mediación',
            'edit_item' => 'Editar solicitud', 'new_item' => 'Nueva solicitud',
            'view_item' => 'Ver solicitud', 'search_items' => 'Buscar solicitudes',
            'not_found' => 'No se han encontrado solicitudes',
            'not_found_in_trash' => 'No hay solicitudes en la papelera',
            'all_items' => 'Todas las solicitudes', 'menu_name' => 'Mediaciones',
        ],
        'public' => false, 'publicly_queryable' => false, 'exclude_from_search' => true,
        'show_ui' => true, 'show_in_rest' => false, 'has_archive' => false,
        'rewrite' => false, 'query_var' => false, 'can_export' => false,
        'menu_icon' => 'dashicons-format-chat', 'supports' => ['title', 'editor'],
        'capability_type' => ['cadus_mediacion', 'cadus_mediaciones'], 'map_meta_cap' => true,
        'capabilities' => [
            'create_posts' => 'create_cadus_mediaciones',
            'read' => 'read_private_cadus_mediaciones',
        ],
    ]);
}

/** Impide que una edición administrativa convierta una solicitud en contenido público. */
function cadus_mediacion_forzar_privacidad(array $data): array
{
    if (($data['post_type'] ?? '') === 'cadus_mediacion') {
        if (!in_array($data['post_status'], ['trash', 'auto-draft'], true)) {
            $data['post_status'] = 'private';
        }
        // El solicitante no es autor del contenido ni adquiere permisos de lectura por autoría.
        $data['post_author'] = 0;
        $data['post_password'] = '';
        $data['comment_status'] = 'closed';
        $data['ping_status'] = 'closed';
    }
    return $data;
}

function cadus_mediacion_es_formulario($form): bool
{
    $id = is_object($form) ? (int) ($form->id ?? 0) : 0;
    return cadus_buzon_ff_disponible() && $id > 0 && $id === (int) get_option('cadus_mediacion_form_id', 0);
}

/** Crea el formulario una sola vez; devuelve 0 si Fluent Forms no está disponible. */
function cadus_mediacion_crear_formulario(): int
{
    global $wpdb;
    if (!cadus_buzon_tablas_disponibles()) {
        return 0;
    }
    $lock = cadus_buzon_lock('crear_formulario_mediacion');
    if ($lock === '') {
        return 0;
    }
    try {
        // Lectura directa tras el bloqueo: otra petición pudo actualizar la opción.
        $form_id = (int) $wpdb->get_var($wpdb->prepare(
            "SELECT option_value FROM {$wpdb->options} WHERE option_name = %s", 'cadus_mediacion_form_id'
        ));
        if (cadus_buzon_formulario_existe($form_id)) {
            return $form_id;
        }
        $nombre = cadus_buzon_campo('input_text', 'solicitante', 'Nombre y apellidos', 0);
        $nombre['attributes']['type'] = 'text';

        $email = cadus_buzon_campo('input_email', 'email', 'Correo universitario', 1);
        $email['attributes']['type'] = 'email';
        $email['attributes']['placeholder'] = 'usuario@alum.us.es';
        $email['settings']['validation_rules']['email'] = [
            'value' => true, 'message' => 'Introduce un correo electrónico válido.', 'global' => false,
        ];

        // Las opciones se toman de la taxonomía del directorio en el momento de crear el formulario.
        // Si se añade un centro después, hay que añadirlo también en el editor de Fluent Forms.
        $centro = cadus_buzon_campo('select', 'centro', 'Facultad o Escuela', 2);
        $centro['settings']['placeholder'] = 'Selecciona tu centro';
        $centro['settings']['advanced_options'] = array_map(
            static fn(string $c): array => ['label' => $c, 'value' => $c, 'calc_value' => ''],
            cadus_mediacion_centros()
        );

        $descripcion = cadus_buzon_campo('textarea', 'descripcion', 'Descripción del conflicto', 3);
        $descripcion['attributes']['rows'] = 6;
        $descripcion['attributes']['cols'] = 2;

        $consent = cadus_buzon_campo('input_checkbox', 'consentimiento', 'Consentimiento RGPD', 4);
        $consent['attributes']['type'] = 'checkbox';
        $consent['attributes']['value'] = [];
        $consent['settings']['advanced_options'] = [[
            'label' => 'Consiento el tratamiento de mis datos por el CADUS para gestionar esta solicitud de mediación, conforme al RGPD.',
            'value' => 'acepto', 'calc_value' => '', 'image' => '',
        ]];
        $consent['settings']['validation_rules']['required']['message'] = 'Debes aceptar el tratamiento de tus datos.';

        $fields = [
            'fields' => [$nombre, $email, $centro, $descripcion, $consent],
            'submitButton' => [
                'uniqElKey' => 'el_cadus_mediacion_enviar', 'element' => 'button',
                'attributes' => ['type' => 'submit', 'class' => ''],
                'settings' => [
                    'align' => 'left', 'button_style' => 'default', 'container_class' => '',
                    'help_message' => '', 'background_color' => '#9b1735', 'button_size' => 'md',
                    'color' => '#ffffff', 'button_ui' => ['type' => 'default', 'text' => 'Solicitar mediación', 'img_url' => ''],
                ],
                'editor_options' => ['title' => 'Solicitar mediación'],
            ],
        ];
        $settings = [
            'confirmation' => [
                'redirectTo' => 'samePage', 'messageToShow' => 'Gracias por contactar con el CADUS.',
                'customPage' => null, 'samePageFormBehavior' => 'hide_form', 'customUrl' => null,
            ],
            'restrictions' => [
                'limitNumberOfEntries' => ['enabled' => false, 'numberOfEntries' => null, 'period' => 'total', 'limitReachedMsg' => 'Se ha alcanzado el límite de envíos.'],
                'scheduleForm' => [
                    'enabled' => false, 'start' => null, 'end' => null,
                    'selectedDays' => ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                    'pendingMsg' => 'La mediación todavía no está abierta.', 'expiredMsg' => 'La mediación está cerrada.',
                ],
                'requireLogin' => ['enabled' => false, 'requireLoginMsg' => 'Debes iniciar sesión para enviar el formulario.'],
                'denyEmptySubmission' => ['enabled' => true, 'message' => 'Completa los campos obligatorios.'],
            ],
            'layout' => [
                'labelPlacement' => 'top', 'helpMessagePlacement' => 'with_label',
                'errorMessagePlacement' => 'inline', 'cssClassName' => '', 'asteriskPlacement' => 'asterisk-right',
            ],
            'delete_entry_on_submission' => 'no',
            'appendSurveyResult' => ['enabled' => false, 'showLabel' => false, 'showCount' => false],
        ];
        $now = current_time('mysql');
        if (!$wpdb->insert($wpdb->prefix . 'fluentform_forms', [
            'title' => 'Solicitud de mediación estudiantil', 'type' => 'form', 'status' => 'published',
            'created_by' => get_current_user_id(), 'created_at' => $now, 'updated_at' => $now,
            'form_fields' => wp_json_encode($fields, JSON_UNESCAPED_UNICODE),
        ], ['%s', '%s', '%s', '%d', '%s', '%s', '%s'])) {
            return 0;
        }
        $form_id = (int) $wpdb->insert_id;
        $metas = [
            'formSettings' => wp_json_encode($settings, JSON_UNESCAPED_UNICODE),
            'advancedValidationSettings' => wp_json_encode([
                'status' => false, 'type' => 'all', 'conditions' => [['field' => '', 'operator' => '=', 'value' => '']],
                'error_message' => 'Comprueba los datos introducidos.', 'validation_type' => 'fail_on_condition_met',
            ], JSON_UNESCAPED_UNICODE),
            'template_name' => 'cadus_mediacion',
        ];
        foreach ($metas as $key => $value) {
            if (!$wpdb->insert($wpdb->prefix . 'fluentform_form_meta', [
                'form_id' => $form_id, 'meta_key' => $key, 'value' => $value,
            ], ['%d', '%s', '%s'])) {
                $wpdb->delete($wpdb->prefix . 'fluentform_form_meta', ['form_id' => $form_id], ['%d']);
                $wpdb->delete($wpdb->prefix . 'fluentform_forms', ['id' => $form_id], ['%d']);
                return 0;
            }
        }
        update_option('cadus_mediacion_form_id', $form_id, false);
        if ((int) $wpdb->get_var($wpdb->prepare(
            "SELECT option_value FROM {$wpdb->options} WHERE option_name = %s", 'cadus_mediacion_form_id'
        )) !== $form_id) {
            $wpdb->delete($wpdb->prefix . 'fluentform_form_meta', ['form_id' => $form_id], ['%d']);
            $wpdb->delete($wpdb->prefix . 'fluentform_forms', ['id' => $form_id], ['%d']);
            return 0;
        }
        return $form_id;
    } finally {
        cadus_buzon_unlock($lock);
    }
}

/**
 * Punto de entrada idempotente para la activación: crea el formulario y la página
 * «Mediación estudiantil» dentro de «Atención al estudiante». No pisa páginas existentes.
 */
function cadus_mediacion_setup(): void
{
    cadus_mediacion_crear_formulario();
    $atencion = get_page_by_path('atencion-al-estudiante');
    if ($atencion && function_exists('cadus_pagina')) {
        cadus_pagina(
            'mediacion-estudiantil',
            'Mediación estudiantil',
            cadus_b_p('Si tienes un conflicto con otro estudiante, un profesor o un órgano de tu centro y quieres que el CADUS medie, rellena este formulario. La Ejecutiva revisará tu solicitud y se pondrá en contacto contigo.')
            . cadus_b_sc('[cadus_mediacion]'),
            (int) $atencion->ID
        );
    }
}

/** Añade «Mediación estudiantil» al menú principal (bajo «Atención al estudiante») si aún no está. */
function cadus_mediacion_asegurar_menu(int $menu_id): void
{
    $pagina = get_page_by_path('atencion-al-estudiante/mediacion-estudiantil');
    $atencion = get_page_by_path('atencion-al-estudiante');
    if (!$menu_id || !$pagina || !$atencion) {
        return;
    }
    $padre = 0;
    foreach ((array) wp_get_nav_menu_items($menu_id) as $item) {
        if ((int) $item->object_id === (int) $pagina->ID) {
            return; // ya está en el menú
        }
        if ((int) $item->object_id === (int) $atencion->ID) {
            $padre = (int) $item->ID;
        }
    }
    wp_update_nav_menu_item($menu_id, 0, [
        'menu-item-title' => get_the_title($pagina->ID), 'menu-item-object' => 'page',
        'menu-item-object-id' => (int) $pagina->ID, 'menu-item-type' => 'post_type',
        'menu-item-status' => 'publish', 'menu-item-parent-id' => $padre,
    ]);
}

/** Refuerza las reglas también si el formulario se modifica posteriormente en el editor (RN-02). */
function cadus_mediacion_validar($errors, $form_data, $form, $fields)
{
    if (!cadus_mediacion_es_formulario($form)) {
        return $errors;
    }
    // Fluent Forms entrega datos deserializados, sin las barras de las superglobales.
    $data = is_array($form_data) ? wp_slash($form_data) : [];
    $errors = is_array($errors) ? $errors : [];
    foreach (['solicitante', 'email', 'centro', 'descripcion', 'consentimiento'] as $key) {
        if (isset($errors[$key]) && !is_array($errors[$key])) {
            $errors[$key] = (array) $errors[$key];
        }
    }
    $raw_email = isset($data['email']) && is_string($data['email']) ? trim(wp_unslash($data['email'])) : '';
    if (cadus_buzon_email($raw_email) === '') {
        $errors['email'][] = 'Utiliza un correo universitario válido terminado en @alum.us.es.';
    }
    foreach (['solicitante', 'descripcion'] as $key) {
        if (cadus_buzon_input($data, $key, $key === 'descripcion') === '') {
            $errors[$key][] = 'Este campo es obligatorio.';
        }
    }
    if (!in_array(cadus_buzon_input($data, 'centro'), cadus_mediacion_centros(), true)) {
        $errors['centro'][] = 'Selecciona tu Facultad o Escuela.';
    }
    $consent = $data['consentimiento'] ?? [];
    $consent = is_array($consent) ? array_values($consent) : [$consent];
    if (count($consent) !== 1 || cadus_buzon_input(['valor' => $consent[0] ?? ''], 'valor') !== 'acepto') {
        $errors['consentimiento'][] = 'Debes aceptar el tratamiento de tus datos.';
    }
    return $errors;
}

/** Consulta interna: no depende de permisos de la sesión pública ni de WP_Query. */
function cadus_mediacion_por_entrada(int $entry_id): int
{
    global $wpdb;
    return (int) $wpdb->get_var($wpdb->prepare(
        "SELECT p.ID FROM {$wpdb->posts} p INNER JOIN {$wpdb->postmeta} m ON m.post_id = p.ID
         WHERE p.post_type = %s AND m.meta_key = %s AND m.meta_value = %s ORDER BY p.ID LIMIT 1",
        'cadus_mediacion', '_cadus_entrada_ff', (string) $entry_id
    ));
}

/** Un bloqueo por envío evita duplicados si Fluent Forms repite su acción. */
function cadus_mediacion_crear(int|string $insert_id, $form_data, $form): void
{
    $form_data = cadus_privacidad_datos_originales($form_data, $form);
    if (!cadus_mediacion_es_formulario($form) || (int) $insert_id < 1 || !is_array($form_data)) {
        return;
    }
    if (cadus_mediacion_validar([], $form_data, $form, [])) {
        return;
    }
    $form_data = wp_slash($form_data);
    $lock = cadus_buzon_lock('mediacion_entrada_' . (int) $insert_id);
    if ($lock === '') {
        return;
    }
    try {
        if (cadus_mediacion_por_entrada((int) $insert_id)) {
            return;
        }
        $centro = cadus_buzon_input($form_data, 'centro');
        $date = current_time('mysql');
        $post_id = wp_insert_post(wp_slash([
            'post_type' => 'cadus_mediacion', 'post_status' => 'private', 'post_author' => 0,
            'post_title' => 'Mediación · ' . $centro,
            'post_content' => cadus_buzon_input($form_data, 'descripcion', true),
            'post_date' => $date, 'comment_status' => 'closed', 'ping_status' => 'closed',
        ]), true);
        if (is_wp_error($post_id) || !$post_id) {
            return;
        }
        // El ID mantiene la unicidad; 128 bits aleatorios impiden adivinar referencias nuevas.
        $code = sprintf('MED-%s-%05d-%s', substr($date, 0, 4), $post_id, strtoupper(bin2hex(random_bytes(16))));
        $meta = [
            '_cadus_codigo' => $code, '_cadus_email' => cadus_buzon_email(wp_unslash($form_data['email'])),
            '_cadus_solicitante' => cadus_buzon_input($form_data, 'solicitante'),
            '_cadus_centro' => $centro, '_cadus_estado' => 'pendiente',
            '_cadus_entrada_ff' => (int) $insert_id,
        ];
        foreach ($meta as $key => $value) {
            if (!add_post_meta($post_id, $key, wp_slash($value), true)) {
                wp_delete_post($post_id, true);
                return;
            }
        }
        $updated = wp_update_post(wp_slash(['ID' => $post_id, 'post_title' => '[' . $code . '] ' . $centro]), true);
        if (is_wp_error($updated) || !$updated) {
            wp_delete_post($post_id, true);
        }
    } finally {
        cadus_buzon_unlock($lock);
    }
}

/** Obliga a mostrar la confirmación en la página aunque se configure una redirección. */
function cadus_mediacion_confirmacion($confirmation, $form_data, $form)
{
    if (cadus_mediacion_es_formulario($form)) {
        $confirmation = is_array($confirmation) ? $confirmation : [];
        $confirmation['redirectTo'] = 'samePage';
        $confirmation['samePageFormBehavior'] = 'hide_form';
        $confirmation['messageToShow'] = 'Gracias por contactar con el CADUS.';
    }
    return $confirmation;
}

/** Mensaje de confirmación con la referencia de la solicitud; si no se creó, se avisa del fallo. */
function cadus_mediacion_mensaje_confirmacion($message, $insert_id, $form_data, $form)
{
    if (!cadus_mediacion_es_formulario($form)) {
        return $message;
    }
    $form_data = cadus_privacidad_datos_originales($form_data, $form);
    $post_id = cadus_mediacion_por_entrada((int) $insert_id);
    $code = $post_id ? (string) get_post_meta($post_id, '_cadus_codigo', true) : '';
    $email = is_array($form_data) && is_string($form_data['email'] ?? null)
        ? cadus_buzon_email($form_data['email']) : '';
    if ($code === '' || $email === '' || get_post_status($post_id) !== 'private'
        || !hash_equals(hash('sha256', (string) get_post_meta($post_id, '_cadus_email', true)), hash('sha256', $email))) {
        // No se conserva una copia sensible en Fluent Forms, tampoco si falla la creación.
        wp_send_json(['errors' => ['mediacion' => [
            'No hemos podido registrar tu solicitud. Contacta con el CADUS e indica que no recibiste una referencia.',
        ]]], 500);
        return '';
    }
    return '<p>' . esc_html('Gracias por contactar con el CADUS. Hemos registrado tu solicitud de mediación con la referencia:')
        . ' <strong>' . esc_html($code) . '</strong>.</p><p>'
        . esc_html('La Ejecutiva la revisará y se pondrá en contacto contigo en tu correo universitario. Guarda esta referencia.') . '</p>';
}

/** [cadus_mediacion]: aviso de privacidad y formulario de la solicitud (HU-12). */
function cadus_mediacion_shortcode(): string
{
    $no_disponible = '<p>' . esc_html('La solicitud de mediación no está disponible temporalmente. Disculpa las molestias.') . '</p>';
    if (!cadus_buzon_tablas_disponibles() || !shortcode_exists('fluentform')) {
        return $no_disponible;
    }
    $form_id = (int) get_option('cadus_mediacion_form_id', 0);
    if (!cadus_buzon_formulario_existe($form_id)) {
        $form_id = current_user_can('manage_options') ? cadus_mediacion_crear_formulario() : 0;
    }
    if (!$form_id) {
        return $no_disponible;
    }
    return '<div class="cadus-aviso">' . esc_html('Tus datos se tratarán conforme al RGPD para gestionar tu solicitud. Las solicitudes de mediación solo son visibles para la Ejecutiva del CADUS, con acceso técnico de administración. Solo pueden solicitarla estudiantes con correo @alum.us.es.')
        . '</div>' . do_shortcode('[fluentform id="' . absint($form_id) . '"]');
}

function cadus_mediacion_metaboxes($post): void
{
    if (!current_user_can('read_private_cadus_mediaciones') || !current_user_can('edit_post', $post->ID)) {
        return;
    }
    add_meta_box('cadus_mediacion_datos', 'Datos de la solicitud', 'cadus_mediacion_datos_box', 'cadus_mediacion', 'normal');
    add_meta_box('cadus_mediacion_estado', 'Estado', 'cadus_mediacion_estado_box', 'cadus_mediacion', 'side');
}

function cadus_mediacion_datos_box($post): void
{
    $filas = [
        'Referencia' => '_cadus_codigo', 'Solicitante' => '_cadus_solicitante',
        'Correo' => '_cadus_email', 'Facultad o Escuela' => '_cadus_centro',
    ];
    echo '<ul>';
    foreach ($filas as $etiqueta => $clave) {
        echo '<li><strong>' . esc_html($etiqueta) . ':</strong> ' . esc_html((string) get_post_meta($post->ID, $clave, true)) . '</li>';
    }
    echo '<li><strong>' . esc_html('Fecha de la solicitud') . ':</strong> ' . esc_html(get_the_date('d/m/Y H:i', $post)) . '</li></ul>';
}

function cadus_mediacion_estado_box($post): void
{
    wp_nonce_field('cadus_mediacion_guardar_' . $post->ID, 'cadus_mediacion_nonce');
    $state = get_post_meta($post->ID, '_cadus_estado', true) ?: 'pendiente';
    echo '<label for="cadus_mediacion_estado_valor">' . esc_html('Estado de la solicitud') . '</label> ';
    echo '<select id="cadus_mediacion_estado_valor" name="cadus_mediacion_estado">';
    foreach (cadus_mediacion_estados() as $value => $label) {
        echo '<option value="' . esc_attr($value) . '"' . selected($state, $value, false) . '>' . esc_html($label) . '</option>';
    }
    echo '</select>';
}

function cadus_mediacion_guardar($post_id, $post, $update): void
{
    if ((defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) || wp_is_post_revision($post_id)
        || !current_user_can('read_private_cadus_mediaciones') || !current_user_can('edit_post', $post_id)
        || !wp_verify_nonce(cadus_buzon_input($_POST, 'cadus_mediacion_nonce'), 'cadus_mediacion_guardar_' . $post_id)) {
        return;
    }
    $state = cadus_buzon_input($_POST, 'cadus_mediacion_estado');
    if (isset(cadus_mediacion_estados()[$state]) && get_post_meta($post_id, '_cadus_estado', true) !== $state) {
        update_post_meta($post_id, '_cadus_estado', $state);
    }
}

function cadus_mediacion_columnas(array $columns): array
{
    return ['cb' => $columns['cb'] ?? '<input type="checkbox">', 'cadus_codigo' => 'Referencia',
        'cadus_estado' => 'Estado', 'date' => 'Fecha'];
}

function cadus_mediacion_columna(string $column, int $post_id): void
{
    if (!current_user_can('read_private_cadus_mediaciones') || !current_user_can('read_post', $post_id)) {
        return;
    }
    $keys = ['cadus_codigo' => '_cadus_codigo', 'cadus_solicitante' => '_cadus_solicitante',
        'cadus_centro' => '_cadus_centro', 'cadus_estado' => '_cadus_estado'];
    if (isset($keys[$column])) {
        $value = (string) get_post_meta($post_id, $keys[$column], true);
        if ($column === 'cadus_codigo') {
            echo '<a href="' . esc_url(admin_url('post.php?post=' . $post_id . '&action=edit')) . '">'
                . esc_html($value ?: 'Solicitud') . '</a>';
            return;
        }
        echo esc_html($column === 'cadus_estado' ? (cadus_mediacion_estados()[$value] ?? 'Desconocido') : $value);
    }
}

add_action('init', 'cadus_mediacion_registrar');
add_filter('wp_insert_post_data', 'cadus_mediacion_forzar_privacidad', 99, 1);
add_filter('fluentform/validation_errors', 'cadus_mediacion_validar', 10, 4);
add_action('fluentform/submission_inserted', 'cadus_mediacion_crear', 10, 3);
add_filter('fluentform/form_submission_confirmation', 'cadus_mediacion_confirmacion', 99, 3);
add_filter('fluentform/submission_message_parse', 'cadus_mediacion_mensaje_confirmacion', 99, 4);
add_action('add_meta_boxes_cadus_mediacion', 'cadus_mediacion_metaboxes', 10, 1);
add_action('save_post_cadus_mediacion', 'cadus_mediacion_guardar', 10, 3);
add_filter('manage_cadus_mediacion_posts_columns', 'cadus_mediacion_columnas');
add_action('manage_cadus_mediacion_posts_custom_column', 'cadus_mediacion_columna', 10, 2);
add_shortcode('cadus_mediacion', 'cadus_mediacion_shortcode');

/** Menú de administración de la Ejecutiva (lista cerrada de HU-19a): las solicitudes de mediación. */
add_filter('cadus_menus_admin', function (array $menus, string $rol): array {
    if ($rol === 'cadus_ejecutiva') {
        $menus['edit.php?post_type=cadus_mediacion'] = ['edit.php?post_type=cadus_mediacion', 'post-new.php?post_type=cadus_mediacion'];
    }
    return $menus;
}, 10, 2);
