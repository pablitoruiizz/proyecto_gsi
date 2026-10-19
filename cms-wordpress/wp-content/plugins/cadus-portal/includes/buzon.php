<?php
/**
 * Buzón del CADUS: formulario, tickets privados y seguimiento (RF-08/09, HU-07/08).
 */
if (!defined('ABSPATH')) {
    exit;
}

require_once __DIR__ . '/privacidad.php';

/** Lee un campo escalar sin aceptar matrices inesperadas. */
function cadus_buzon_input(array $data, string $key, bool $multiline = false): string
{
    if (!isset($data[$key]) || !is_string($data[$key])) {
        return '';
    }
    $value = wp_unslash($data[$key]);
    return $multiline ? sanitize_textarea_field($value) : sanitize_text_field($value);
}

/** Valida antes de sanear para no convertir un correo inválido en otro válido. */
function cadus_buzon_email(string $value): string
{
    $value = strtolower(trim($value));
    return is_email($value) && str_ends_with($value, '@alum.us.es') ? sanitize_email($value) : '';
}

function cadus_buzon_estados(): array
{
    return ['abierto' => 'Abierto', 'en_proceso' => 'En proceso', 'cerrado' => 'Cerrado'];
}

/** Los bloqueos de MySQL se liberan también cuando se cierra la conexión. */
function cadus_buzon_lock(string $resource): string
{
    global $wpdb;
    $name = 'cadus_buzon_' . md5(DB_NAME . ':' . $wpdb->prefix . ':' . $resource);
    return '1' === (string) $wpdb->get_var($wpdb->prepare('SELECT GET_LOCK(%s, %d)', $name, 5)) ? $name : '';
}

function cadus_buzon_unlock(string $name): void
{
    global $wpdb;
    if ($name !== '') {
        $wpdb->get_var($wpdb->prepare('SELECT RELEASE_LOCK(%s)', $name));
    }
}

function cadus_buzon_registrar_ticket(): void
{
    register_post_type('cadus_ticket', [
        'label' => 'Tickets del buzón',
        'labels' => [
            'name' => 'Tickets del buzón', 'singular_name' => 'Ticket del buzón',
            'add_new' => 'Añadir ticket', 'add_new_item' => 'Añadir ticket',
            'edit_item' => 'Editar ticket', 'new_item' => 'Nuevo ticket',
            'view_item' => 'Ver ticket', 'search_items' => 'Buscar tickets',
            'not_found' => 'No se han encontrado tickets',
            'not_found_in_trash' => 'No hay tickets en la papelera',
            'all_items' => 'Todos los tickets', 'menu_name' => 'Tickets del buzón',
        ],
        'public' => false, 'publicly_queryable' => false, 'exclude_from_search' => true,
        'show_ui' => true, 'show_in_rest' => false, 'has_archive' => false,
        'rewrite' => false, 'query_var' => false, 'can_export' => false,
        'menu_icon' => 'dashicons-email-alt', 'supports' => ['title', 'editor'],
        'capability_type' => ['cadus_ticket', 'cadus_tickets'], 'map_meta_cap' => true,
        'capabilities' => [
            'create_posts' => 'create_cadus_tickets',
            'read' => 'read_private_cadus_tickets',
        ],
    ]);
}

/** Impide que una edición administrativa convierta un ticket en contenido público. */
function cadus_buzon_forzar_privacidad(array $data): array
{
    if (($data['post_type'] ?? '') === 'cadus_ticket') {
        if (!in_array($data['post_status'], ['trash', 'auto-draft'], true)) {
            $data['post_status'] = 'private';
        }
        // El remitente no es autor del post ni adquiere permisos de lectura por autoría.
        $data['post_author'] = 0;
        $data['post_password'] = '';
        $data['comment_status'] = 'closed';
        $data['ping_status'] = 'closed';
    }
    return $data;
}

function cadus_buzon_ff_disponible(): bool
{
    return defined('FLUENTFORM') || function_exists('fluentForm');
}

function cadus_buzon_tablas_disponibles(): bool
{
    global $wpdb;
    if (!cadus_buzon_ff_disponible()) {
        return false;
    }
    foreach (['fluentform_forms', 'fluentform_form_meta'] as $suffix) {
        $table = $wpdb->prefix . $suffix;
        if ($wpdb->get_var($wpdb->prepare('SHOW TABLES LIKE %s', $wpdb->esc_like($table))) !== $table) {
            return false;
        }
    }
    return true;
}

function cadus_buzon_formulario_existe(int $form_id): bool
{
    global $wpdb;
    return $form_id > 0 && (int) $wpdb->get_var($wpdb->prepare(
        "SELECT id FROM {$wpdb->prefix}fluentform_forms WHERE id = %d", $form_id
    )) === $form_id;
}

/** Estructura común del editor de Fluent Forms, basada en su formulario de ejemplo. */
function cadus_buzon_campo(string $element, string $name, string $label, int $index): array
{
    $templates = ['select' => 'select', 'textarea' => 'inputTextarea', 'input_checkbox' => 'inputCheckable'];
    return [
        'index' => $index, 'element' => $element, 'uniqElKey' => 'el_cadus_buzon_' . $name,
        'attributes' => ['name' => $name, 'value' => '', 'id' => '', 'class' => '', 'placeholder' => ''],
        'settings' => [
            'container_class' => '', 'label' => $label, 'label_placement' => '',
            'admin_field_label' => $label, 'help_message' => '', 'conditional_logics' => [],
            'validation_rules' => ['required' => [
                'value' => true, 'message' => 'Este campo es obligatorio.', 'global' => false,
            ]],
        ],
        'editor_options' => ['title' => $label, 'template' => $templates[$element] ?? 'inputText'],
    ];
}

/** Crea el formulario una sola vez; devuelve 0 si Fluent Forms no está disponible. */
function cadus_buzon_crear_formulario(): int
{
    global $wpdb;
    if (!cadus_buzon_tablas_disponibles()) {
        return 0;
    }
    $lock = cadus_buzon_lock('crear_formulario');
    if ($lock === '') {
        return 0;
    }
    try {
        // Lectura directa tras el bloqueo: otra petición pudo actualizar la opción.
        $form_id = (int) $wpdb->get_var($wpdb->prepare(
            "SELECT option_value FROM {$wpdb->options} WHERE option_name = %s", 'cadus_buzon_form_id'
        ));
        if (cadus_buzon_formulario_existe($form_id)) {
            return $form_id;
        }
        $email = cadus_buzon_campo('input_email', 'email', 'Correo universitario', 0);
        $email['attributes']['type'] = 'email';
        $email['attributes']['placeholder'] = 'usuario@alum.us.es';
        $email['settings']['validation_rules']['email'] = [
            'value' => true, 'message' => 'Introduce un correo electrónico válido.', 'global' => false,
        ];
        $subject = cadus_buzon_campo('input_text', 'asunto', 'Asunto', 1);
        $subject['attributes']['type'] = 'text';
        $type = cadus_buzon_campo('select', 'tipo', 'Tipo', 2);
        $type['settings']['placeholder'] = 'Selecciona un tipo';
        $type['settings']['advanced_options'] = [
            ['label' => 'Consulta', 'value' => 'Consulta', 'calc_value' => ''],
            ['label' => 'Reclamación académica', 'value' => 'Reclamación académica', 'calc_value' => ''],
        ];
        $description = cadus_buzon_campo('textarea', 'descripcion', 'Descripción', 3);
        $description['attributes']['rows'] = 6;
        $description['attributes']['cols'] = 2;
        $consent = cadus_buzon_campo('input_checkbox', 'consentimiento', 'Consentimiento RGPD', 4);
        $consent['attributes']['type'] = 'checkbox';
        $consent['attributes']['value'] = [];
        $consent['settings']['advanced_options'] = [[
            'label' => 'Consiento el tratamiento de mis datos por el CADUS para gestionar esta consulta o reclamación, conforme al RGPD.',
            'value' => 'acepto', 'calc_value' => '', 'image' => '',
        ]];
        $consent['settings']['validation_rules']['required']['message'] = 'Debes aceptar el tratamiento de tus datos.';
        $fields = [
            'fields' => [$email, $subject, $type, $description, $consent],
            'submitButton' => [
                'uniqElKey' => 'el_cadus_buzon_enviar', 'element' => 'button',
                'attributes' => ['type' => 'submit', 'class' => ''],
                'settings' => [
                    'align' => 'left', 'button_style' => 'default', 'container_class' => '',
                    'help_message' => '', 'background_color' => '#9b1735', 'button_size' => 'md',
                    'color' => '#ffffff', 'button_ui' => ['type' => 'default', 'text' => 'Enviar al CADUS', 'img_url' => ''],
                ],
                'editor_options' => ['title' => 'Enviar al CADUS'],
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
                    'pendingMsg' => 'El buzón todavía no está abierto.', 'expiredMsg' => 'El buzón está cerrado.',
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
            'title' => 'Buzón de consultas y reclamaciones', 'type' => 'form', 'status' => 'published',
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
            'template_name' => 'cadus_buzon',
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
        update_option('cadus_buzon_form_id', $form_id, false);
        if ((int) $wpdb->get_var($wpdb->prepare(
            "SELECT option_value FROM {$wpdb->options} WHERE option_name = %s", 'cadus_buzon_form_id'
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

/** Punto de entrada idempotente para la activación; no registra tipos ni hooks. */
function cadus_buzon_setup(): int
{
    return cadus_buzon_crear_formulario();
}

function cadus_buzon_es_formulario($form): bool
{
    $id = is_object($form) ? (int) ($form->id ?? 0) : 0;
    return cadus_buzon_ff_disponible() && $id > 0 && $id === (int) get_option('cadus_buzon_form_id', 0);
}

/** Refuerza las reglas también si el formulario se modifica posteriormente en el editor. */
function cadus_buzon_validar($errors, $form_data, $form, $fields)
{
    if (!cadus_buzon_es_formulario($form)) {
        return $errors;
    }
    // Fluent Forms ya entrega datos deserializados, sin las barras de las superglobales.
    // Se adapta su formato al lector común para conservar las barras escritas por el alumno.
    $data = is_array($form_data) ? wp_slash($form_data) : [];
    $errors = is_array($errors) ? $errors : [];
    foreach (['email', 'asunto', 'descripcion', 'tipo', 'consentimiento'] as $key) {
        if (isset($errors[$key]) && !is_array($errors[$key])) {
            $errors[$key] = (array) $errors[$key];
        }
    }
    $raw_email = isset($data['email']) && is_string($data['email']) ? trim(wp_unslash($data['email'])) : '';
    if (cadus_buzon_email($raw_email) === '') {
        $errors['email'][] = 'Utiliza un correo universitario válido terminado en @alum.us.es.';
    }
    foreach (['asunto', 'descripcion'] as $key) {
        if (cadus_buzon_input($data, $key, $key === 'descripcion') === '') {
            $errors[$key][] = 'Este campo es obligatorio.';
        }
    }
    if (!in_array(cadus_buzon_input($data, 'tipo'), ['Consulta', 'Reclamación académica'], true)) {
        $errors['tipo'][] = 'Selecciona Consulta o Reclamación académica.';
    }
    $consent = $data['consentimiento'] ?? [];
    $consent = is_array($consent) ? array_values($consent) : [$consent];
    if (count($consent) !== 1 || cadus_buzon_input(['valor' => $consent[0] ?? ''], 'valor') !== 'acepto') {
        $errors['consentimiento'][] = 'Debes aceptar el tratamiento de tus datos.';
    }
    return $errors;
}

/** Consulta interna: no depende de permisos de la sesión pública ni de WP_Query. */
function cadus_buzon_ticket_por_entrada(int $entry_id): int
{
    global $wpdb;
    return (int) $wpdb->get_var($wpdb->prepare(
        "SELECT p.ID FROM {$wpdb->posts} p INNER JOIN {$wpdb->postmeta} m ON m.post_id = p.ID
         WHERE p.post_type = %s AND m.meta_key = %s AND m.meta_value = %s ORDER BY p.ID LIMIT 1",
        'cadus_ticket', '_cadus_entrada_ff', (string) $entry_id
    ));
}

/** Un bloqueo por envío evita duplicados si Fluent Forms repite su acción. */
function cadus_buzon_crear_ticket($insert_id, $form_data, $form): void
{
    $form_data = cadus_privacidad_datos_originales($form_data, $form);
    if (!cadus_buzon_es_formulario($form) || (int) $insert_id < 1 || !is_array($form_data)) {
        return;
    }
    if (cadus_buzon_validar([], $form_data, $form, [])) {
        return;
    }
    $form_data = wp_slash($form_data);
    $lock = cadus_buzon_lock('entrada_' . (int) $insert_id);
    if ($lock === '') {
        return;
    }
    try {
        if (cadus_buzon_ticket_por_entrada((int) $insert_id)) {
            return;
        }
        $subject = cadus_buzon_input($form_data, 'asunto');
        $type = cadus_buzon_input($form_data, 'tipo');
        $date = current_time('mysql');
        $post_id = wp_insert_post(wp_slash([
            'post_type' => 'cadus_ticket', 'post_status' => 'private', 'post_author' => 0,
            'post_title' => $subject, 'post_content' => cadus_buzon_input($form_data, 'descripcion', true),
            'post_date' => $date, 'comment_status' => 'closed', 'ping_status' => 'closed',
        ]), true);
        if (is_wp_error($post_id) || !$post_id) {
            return;
        }
        // El ID mantiene la unicidad; 128 bits aleatorios impiden adivinar nuevos códigos.
        $code = sprintf('CAD-%s-%05d-%s', substr($date, 0, 4), $post_id, strtoupper(bin2hex(random_bytes(16))));
        $meta = [
            '_cadus_codigo' => $code, '_cadus_email' => cadus_buzon_email(wp_unslash($form_data['email'])),
            '_cadus_tipo' => $type, '_cadus_estado' => 'abierto',
            '_cadus_confidencial' => $type === 'Reclamación académica' ? '1' : '0',
            '_cadus_entrada_ff' => (int) $insert_id,
        ];
        foreach ($meta as $key => $value) {
            if (!add_post_meta($post_id, $key, wp_slash($value), true)) {
                wp_delete_post($post_id, true);
                return;
            }
        }
        $updated = wp_update_post(wp_slash(['ID' => $post_id, 'post_title' => '[' . $code . '] ' . $subject]), true);
        if (is_wp_error($updated) || !$updated) {
            wp_delete_post($post_id, true);
        }
    } finally {
        cadus_buzon_unlock($lock);
    }
}

/** Obliga a mostrar la confirmación en la página aunque se configure una redirección. */
function cadus_buzon_confirmacion($confirmation, $form_data, $form)
{
    if (cadus_buzon_es_formulario($form)) {
        $confirmation = is_array($confirmation) ? $confirmation : [];
        $confirmation['redirectTo'] = 'samePage';
        $confirmation['samePageFormBehavior'] = 'hide_form';
        $confirmation['messageToShow'] = 'Gracias por contactar con el CADUS.';
    }
    return $confirmation;
}

/** Hook de cuatro argumentos presente tanto en el servicio actual como en el manejador antiguo. */
function cadus_buzon_mensaje_confirmacion($message, $insert_id, $form_data, $form)
{
    if (!cadus_buzon_es_formulario($form)) {
        return $message;
    }
    $form_data = cadus_privacidad_datos_originales($form_data, $form);
    $post_id = cadus_buzon_ticket_por_entrada((int) $insert_id);
    $code = $post_id ? (string) get_post_meta($post_id, '_cadus_codigo', true) : '';
    $email = is_array($form_data) && is_string($form_data['email'] ?? null)
        ? cadus_buzon_email($form_data['email']) : '';
    if ($code === '' || $email === '' || get_post_status($post_id) !== 'private'
        || !hash_equals(hash('sha256', (string) get_post_meta($post_id, '_cadus_email', true)), hash('sha256', $email))) {
        // No se conserva una copia sensible en Fluent Forms, tampoco si falla el ticket.
        // Su controlador espera «errors» en la raíz, sin el envoltorio de wp_send_json_error.
        wp_send_json(['errors' => ['buzon' => [
            'No hemos podido generar tu ticket. Contacta con el CADUS e indica que no recibiste un código de seguimiento.',
        ]]], 500);
        return '';
    }
    return '<p>' . esc_html('Gracias por contactar con el CADUS. Tu código de seguimiento es:')
        . ' <strong>' . esc_html($code) . '</strong>.</p><p>'
        . esc_html('Guarda este código. Podrás consultar el estado y las respuestas con él y tu correo universitario.') . '</p>';
}

function cadus_buzon_shortcode(): string
{
    if (!cadus_buzon_tablas_disponibles() || !shortcode_exists('fluentform')) {
        return '<p>' . esc_html('El buzón no está disponible temporalmente. Disculpa las molestias.') . '</p>';
    }
    $form_id = (int) get_option('cadus_buzon_form_id', 0);
    if (!cadus_buzon_formulario_existe($form_id)) {
        $form_id = current_user_can('manage_options') ? cadus_buzon_crear_formulario() : 0;
    }
    if (!$form_id) {
        return '<p>' . esc_html('El buzón no está disponible temporalmente. Disculpa las molestias.') . '</p>';
    }
    return '<p>' . esc_html('Tus datos se tratarán conforme al RGPD para atender tu solicitud. Las reclamaciones solo son visibles para el remitente y la Ejecutiva del CADUS, con acceso técnico de administración. Guarda tu código y no lo compartas.')
        . '</p>' . do_shortcode('[fluentform id="' . absint($form_id) . '"]');
}

function cadus_buzon_metaboxes($post): void
{
    if (!current_user_can('read_private_cadus_tickets') || !current_user_can('edit_post', $post->ID)) {
        return;
    }
    add_meta_box('cadus_ticket_estado', 'Estado', 'cadus_buzon_estado_box', 'cadus_ticket', 'side');
    add_meta_box('cadus_ticket_respuestas', 'Respuestas', 'cadus_buzon_respuestas_box', 'cadus_ticket', 'normal');
}

function cadus_buzon_estado_box($post): void
{
    wp_nonce_field('cadus_ticket_guardar_' . $post->ID, 'cadus_ticket_nonce');
    $state = get_post_meta($post->ID, '_cadus_estado', true) ?: 'abierto';
    echo '<p><strong>' . esc_html((string) get_post_meta($post->ID, '_cadus_codigo', true)) . '</strong></p>';
    echo '<label for="cadus_ticket_estado_valor">' . esc_html('Estado del ticket') . '</label> ';
    echo '<select id="cadus_ticket_estado_valor" name="cadus_ticket_estado">';
    foreach (cadus_buzon_estados() as $value => $label) {
        echo '<option value="' . esc_attr($value) . '"' . selected($state, $value, false) . '>' . esc_html($label) . '</option>';
    }
    echo '</select>';
}

/** Solo se muestran texto y fecha: no se expone la identidad interna de quien responde. */
function cadus_buzon_respuestas_html(int $post_id): string
{
    $answers = get_post_meta($post_id, '_cadus_respuestas', true);
    $html = '';
    foreach (is_array($answers) ? $answers : [] as $answer) {
        if (!is_array($answer) || !is_string($answer['texto'] ?? null) || !is_string($answer['fecha'] ?? null)) {
            continue;
        }
        $html .= '<li><p><strong>' . esc_html($answer['fecha']) . '</strong></p><p>'
            . nl2br(esc_html($answer['texto'])) . '</p></li>';
    }
    return $html !== '' ? '<ol>' . $html . '</ol>' : '<p>' . esc_html('Todavía no hay respuestas.') . '</p>';
}

function cadus_buzon_respuestas_box($post): void
{
    echo cadus_buzon_respuestas_html((int) $post->ID);
    echo '<p><label for="cadus_ticket_respuesta">' . esc_html('Respuesta para el estudiante') . '</label></p>';
    echo '<textarea id="cadus_ticket_respuesta" name="cadus_ticket_respuesta" rows="6" class="widefat"></textarea>';
    echo '<p>' . esc_html('Al actualizar el ticket se añadirá esta respuesta al seguimiento. No se enviará ningún correo.') . '</p>';
}

function cadus_buzon_guardar_ticket($post_id, $post, $update): void
{
    if ((defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) || wp_is_post_revision($post_id)
        || !current_user_can('read_private_cadus_tickets') || !current_user_can('edit_post', $post_id)
        || !wp_verify_nonce(cadus_buzon_input($_POST, 'cadus_ticket_nonce'), 'cadus_ticket_guardar_' . $post_id)) {
        return;
    }
    $state = cadus_buzon_input($_POST, 'cadus_ticket_estado');
    $answer = cadus_buzon_input($_POST, 'cadus_ticket_respuesta', true);
    $lock = cadus_buzon_lock('editar_' . (int) $post_id);
    if ($lock === '') {
        wp_die(esc_html('No se han guardado el estado ni la respuesta. Vuelve atrás e inténtalo de nuevo.'));
    }
    $failed = false;
    try {
        // Evita sobrescribir respuestas añadidas mientras esta petición esperaba el bloqueo.
        wp_cache_delete($post_id, 'post_meta');
        if (isset(cadus_buzon_estados()[$state])) {
            $old_state = get_post_meta($post_id, '_cadus_estado', true);
            if ($old_state !== $state && !update_post_meta($post_id, '_cadus_estado', $state)) {
                $failed = true;
            }
        }
        if ($answer !== '') {
            $answers = get_post_meta($post_id, '_cadus_respuestas', true);
            $answers = is_array($answers) ? $answers : [];
            $answers[] = ['texto' => $answer, 'fecha' => current_time('mysql'), 'autor' => get_current_user_id()];
            if (!update_post_meta($post_id, '_cadus_respuestas', wp_slash($answers))) {
                $failed = true;
            }
        }
    } finally {
        cadus_buzon_unlock($lock);
    }
    if ($failed) {
        wp_die(esc_html('No se han podido guardar todos los cambios del buzón. Revisa el ticket antes de volver a enviar la respuesta.'));
    }
}

function cadus_buzon_columnas(array $columns): array
{
    return ['cb' => $columns['cb'] ?? '<input type="checkbox">', 'cadus_codigo' => 'Código',
        'cadus_estado' => 'Estado', 'date' => 'Fecha'];
}

function cadus_buzon_columna(string $column, int $post_id): void
{
    if (!current_user_can('read_private_cadus_tickets') || !current_user_can('read_post', $post_id)) {
        return;
    }
    $keys = ['cadus_codigo' => '_cadus_codigo', 'cadus_email' => '_cadus_email', 'cadus_tipo' => '_cadus_tipo', 'cadus_estado' => '_cadus_estado'];
    if (isset($keys[$column])) {
        $value = (string) get_post_meta($post_id, $keys[$column], true);
        if ($column === 'cadus_codigo') {
            echo '<a href="' . esc_url(admin_url('post.php?post=' . $post_id . '&action=edit')) . '">'
                . esc_html($value ?: 'Ticket') . '</a>';
            return;
        }
        echo esc_html($column === 'cadus_estado' ? (cadus_buzon_estados()[$value] ?? 'Desconocido') : $value);
    }
}

/** No se confía en cabeceras de proxy aportadas por el cliente. Máximo 10 intentos/15 minutos. */
function cadus_buzon_permitir_intento(): bool
{
    $ip = cadus_buzon_input($_SERVER, 'REMOTE_ADDR');
    $ip = filter_var($ip, FILTER_VALIDATE_IP) ? $ip : 'sin_ip';
    $key = 'cadus_seg_' . hash_hmac('sha256', $ip, wp_salt('nonce'));
    $lock = cadus_buzon_lock($key);
    if ($lock === '') {
        return false;
    }
    try {
        // Las transients en opciones también tienen caché local a cada petición.
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

/** Evita que una caché de página conserve resultados privados del seguimiento. */
function cadus_buzon_no_cache(): void
{
    if (!defined('DONOTCACHEPAGE')) {
        define('DONOTCACHEPAGE', true);
    }
    // WP Fastest Cache solo respeta la constante en algunos casos (p. ej. Divi).
    do_action('wpfc_exclude_current_page');
    if (!headers_sent()) {
        nocache_headers();
        header('Cache-Control: no-store, no-cache, must-revalidate, private, max-age=0');
        header('Referrer-Policy: no-referrer');
        header('X-Robots-Tag: noindex, nofollow, noarchive');
    }
}

function cadus_buzon_privacidad_seguimiento(): void
{
    $post = get_queried_object();
    if (isset($_POST['cadus_seguimiento_enviar'])
        || ($post instanceof WP_Post && has_shortcode($post->post_content, 'cadus_seguimiento'))) {
        cadus_buzon_no_cache();
    }
}

/** La única lectura pública requiere simultáneamente código y correo. */
function cadus_buzon_resultado_seguimiento(): string
{
    global $wpdb;
    if (!wp_verify_nonce(cadus_buzon_input($_POST, 'cadus_seguimiento_nonce'), 'cadus_seguimiento')) {
        return '<p role="alert">' . esc_html('La sesión del formulario ha caducado. Recarga la página e inténtalo de nuevo.') . '</p>';
    }
    if (!cadus_buzon_permitir_intento()) {
        return '<p role="alert">' . esc_html('Has alcanzado el límite de consultas. Espera 15 minutos antes de volver a intentarlo.') . '</p>';
    }
    $code = strtoupper(cadus_buzon_input($_POST, 'cadus_codigo'));
    $raw_email = isset($_POST['cadus_correo']) && is_string($_POST['cadus_correo']) ? wp_unslash($_POST['cadus_correo']) : '';
    $email = cadus_buzon_email($raw_email);
    $ticket = null;
    if (preg_match('/\ACAD-[0-9]{4}-[0-9]{5,20}(?:-[A-F0-9]{32})?\z/', $code) && $email !== '') {
        $ticket = $wpdb->get_row($wpdb->prepare(
            "SELECT p.ID, p.post_title, p.post_date, e.meta_value AS correo FROM {$wpdb->posts} p
             INNER JOIN {$wpdb->postmeta} c ON c.post_id = p.ID AND c.meta_key = %s
             INNER JOIN {$wpdb->postmeta} e ON e.post_id = p.ID AND e.meta_key = %s
             WHERE p.post_type = %s AND p.post_status = %s AND BINARY c.meta_value = BINARY %s
             LIMIT 1",
            '_cadus_codigo', '_cadus_email', 'cadus_ticket', 'private', $code
        ));
    }
    // Hashes de longitud fija: también se compara si el código no existe.
    $email_ok = hash_equals(hash('sha256', strtolower((string) ($ticket->correo ?? ''))), hash('sha256', $email));
    if (!$ticket || $email === '' || !$email_ok) {
        return '<p role="status">' . esc_html('No hemos encontrado ningún ticket con esos datos') . '</p>';
    }
    $subject = $ticket->post_title;
    $prefix = '[' . $code . '] ';
    if (str_starts_with($subject, $prefix)) {
        $subject = substr($subject, strlen($prefix));
    }
    $state = (string) get_post_meta($ticket->ID, '_cadus_estado', true);
    $details = [
        'Tipo' => (string) get_post_meta($ticket->ID, '_cadus_tipo', true), 'Asunto' => $subject,
        'Estado' => cadus_buzon_estados()[$state] ?? 'Desconocido', 'Fecha' => $ticket->post_date,
    ];
    $html = '<section aria-label="' . esc_attr('Resultado del seguimiento') . '"><h3>' . esc_html($code) . '</h3><dl>';
    foreach ($details as $label => $value) {
        $html .= '<dt>' . esc_html($label) . '</dt><dd>' . esc_html($value) . '</dd>';
    }
    return $html . '</dl><h4>' . esc_html('Respuestas') . '</h4>' . cadus_buzon_respuestas_html((int) $ticket->ID) . '</section>';
}

function cadus_buzon_seguimiento_shortcode(): string
{
    cadus_buzon_no_cache();
    $html = '';
    if (cadus_buzon_input($_SERVER, 'REQUEST_METHOD') === 'POST'
        && cadus_buzon_input($_POST, 'cadus_seguimiento_enviar') === '1') {
        // Un shortcode repetido en la misma página solo consume un intento.
        static $result = null;
        if ($result === null) {
            $result = cadus_buzon_resultado_seguimiento();
        }
        $html = $result;
    }
    $id = wp_unique_id('cadus_seguimiento_');
    $html .= '<form method="post" autocomplete="off">'
        . wp_nonce_field('cadus_seguimiento', 'cadus_seguimiento_nonce', false, false)
        . '<input type="hidden" name="cadus_seguimiento_enviar" value="1">'
        . '<p><label for="' . esc_attr($id . '_codigo') . '">' . esc_html('Código de seguimiento') . '</label> '
        . '<input id="' . esc_attr($id . '_codigo') . '" name="cadus_codigo" type="text" maxlength="62" placeholder="Código recibido al enviar" required></p>'
        . '<p><label for="' . esc_attr($id . '_correo') . '">' . esc_html('Correo universitario') . '</label> '
        . '<input id="' . esc_attr($id . '_correo') . '" name="cadus_correo" type="email" maxlength="254" required></p>'
        . '<button type="submit">' . esc_html('Consultar seguimiento') . '</button></form>';
    return $html;
}

add_action('init', 'cadus_buzon_registrar_ticket');
add_filter('wp_insert_post_data', 'cadus_buzon_forzar_privacidad', 99, 1);
add_filter('fluentform/validation_errors', 'cadus_buzon_validar', 10, 4);
add_action('fluentform/submission_inserted', 'cadus_buzon_crear_ticket', 10, 3);
add_filter('fluentform/form_submission_confirmation', 'cadus_buzon_confirmacion', 99, 3);
add_filter('fluentform/submission_message_parse', 'cadus_buzon_mensaje_confirmacion', 99, 4);
add_action('add_meta_boxes_cadus_ticket', 'cadus_buzon_metaboxes', 10, 1);
add_action('save_post_cadus_ticket', 'cadus_buzon_guardar_ticket', 10, 3);
add_filter('manage_cadus_ticket_posts_columns', 'cadus_buzon_columnas');
add_action('manage_cadus_ticket_posts_custom_column', 'cadus_buzon_columna', 10, 2);
add_action('template_redirect', 'cadus_buzon_privacidad_seguimiento');
add_shortcode('cadus_buzon', 'cadus_buzon_shortcode');
add_shortcode('cadus_seguimiento', 'cadus_buzon_seguimiento_shortcode');
