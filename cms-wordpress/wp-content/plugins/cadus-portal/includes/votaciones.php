<?php
/**
 * Convocatorias de votación vinculadas a una asamblea del calendario (HU-11 · RF-12 · IR-07 · RN-05 · UI-02).
 *
 * Reutiliza lo que ya existe en el portal:
 *  - Las asambleas son eventos de The Events Calendar (tipo «tribe_events», módulo includes/calendario.php, HU-10).
 *    Si el equipo clasifica sus eventos con una categoría «asamblea» o «asambleas», solo se ofrecen esos.
 *  - Los menús de administración y la barra superior se amplían con los filtros cadus_menus_admin y
 *    cadus_barra_nuevos (includes/admin.php), igual que hacen calendario.php y mediacion.php.
 *  - Las capacidades del tipo se añaden con cadus_caps_cpt() (includes/roles.php) al Ejecutivo y al administrador,
 *    una sola vez por versión, como hace el calendario: no hace falta tocar la lista de roles.php.
 *
 * Qué hace:
 *  - Tipo de contenido «Convocatoria de votación» (cadus_votacion): título, descripción, asamblea vinculada,
 *    apertura, cierre e ID de la encuesta de YOP Poll que sirve de papeleta.
 *  - RN-05: una votación no se publica sin una asamblea ya creada en el calendario (y un periodo válido); si se intenta,
 *    vuelve a borrador con un aviso. Se comprueba en save_post, por lo que también vale para la edición rápida o en lote.
 *  - La papeleta (shortcode [yop_poll id="N"]) solo se muestra mientras la votación está abierta según las fechas de
 *    la convocatoria; antes y después se informa de cuándo abre o de que ha cerrado.
 *  - Página pública «Votaciones» ([cadus_votaciones]), bloque de la portada tras «¡Últimos eventos!» y listado de las
 *    votaciones vinculadas en la ficha de cada asamblea del calendario.
 *
 * Si The Events Calendar no está activo, el formulario pasa a un modo provisional con el título y la fecha de la
 * asamblea escritos a mano (alternativa prevista para el Sprint 2). Sin YOP Poll, la votación se publica pero sin papeleta.
 * El tipo no se expone por la API REST (show_in_rest false) para que RN-05 no se pueda saltar con una API paralela.
 */

if (!defined('ABSPATH')) {
    exit;
}

define('CADUS_VOTACIONES_VERSION', '1');

add_action('init', 'cadus_votaciones_registrar');
add_action('init', 'cadus_votaciones_migrar', 30);
add_filter('cadus_menus_admin', 'cadus_votaciones_menus_admin', 10, 2);
add_filter('cadus_barra_nuevos', 'cadus_votaciones_barra_nuevos', 10, 2);
add_filter('use_block_editor_for_post_type', 'cadus_votaciones_editor_clasico', 10, 2);
add_action('add_meta_boxes_cadus_votacion', 'cadus_votaciones_metaboxes');
add_action('save_post_cadus_votacion', 'cadus_votaciones_guardar', 10, 2);
add_action('transition_post_status', 'cadus_votaciones_cambio_estado', 10, 3);
add_filter('redirect_post_location', 'cadus_votaciones_redireccion', 10, 2);
add_action('admin_notices', 'cadus_votaciones_avisos');
add_filter('manage_cadus_votacion_posts_columns', 'cadus_votaciones_columnas');
add_action('manage_cadus_votacion_posts_custom_column', 'cadus_votaciones_columna', 10, 2);
add_filter('the_content', 'cadus_votaciones_en_contenido');
add_shortcode('cadus_votaciones', 'cadus_votaciones_shortcode');
add_shortcode('cadus_votaciones_portada', 'cadus_votaciones_portada_shortcode');
add_filter('do_shortcode_tag', 'cadus_votaciones_tras_eventos', 10, 2);
add_action('template_redirect', 'cadus_votaciones_sin_cache');

/* --------------------------------------------------------------------- tipo de contenido */

function cadus_votaciones_registrar(): void
{
    register_post_type('cadus_votacion', [
        'label' => 'Votaciones',
        'labels' => [
            'name' => 'Votaciones', 'singular_name' => 'Convocatoria de votación',
            'add_new' => 'Añadir votación', 'add_new_item' => 'Añadir convocatoria de votación',
            'edit_item' => 'Editar convocatoria de votación', 'new_item' => 'Nueva convocatoria',
            'view_item' => 'Ver votación', 'search_items' => 'Buscar votaciones',
            'not_found' => 'No se han encontrado votaciones', 'not_found_in_trash' => 'No hay votaciones en la papelera',
            'all_items' => 'Todas las votaciones', 'menu_name' => 'Votaciones',
        ],
        'public' => true, 'has_archive' => false, 'rewrite' => ['slug' => 'votacion'],
        'show_ui' => true, 'show_in_rest' => false, 'can_export' => true,
        'menu_icon' => 'dashicons-yes-alt', 'supports' => ['title', 'editor'],
        'capability_type' => ['cadus_votacion', 'cadus_votacions'], 'map_meta_cap' => true,
    ]);
}

/** El formulario de la convocatoria usa metacajas clásicas: el editor de bloques no las necesita. */
function cadus_votaciones_editor_clasico($usar, string $tipo)
{
    return $tipo === 'cadus_votacion' ? false : $usar;
}

/* --------------------------------------------------------------------- calendario (asambleas) */

function cadus_votaciones_hay_calendario(): bool
{
    return function_exists('cadus_calendario_activo') ? cadus_calendario_activo() : post_type_exists('tribe_events');
}

/** Categorías de asambleas del calendario, si el equipo las usa (slug «asamblea» o «asambleas»). */
function cadus_votaciones_categorias_asamblea(): array
{
    if (!taxonomy_exists('tribe_events_cat')) {
        return [];
    }
    $slugs = array_values(array_filter(['asamblea', 'asambleas'], static fn(string $s): bool => (bool) term_exists($s, 'tribe_events_cat')));
    if (!$slugs && is_admin()) {
        // La categoría de asambleas se crea sola al abrir el formulario de una convocatoria.
        $nuevo = wp_insert_term('Asambleas', 'tribe_events_cat', ['slug' => 'asambleas']);
        $slugs = is_wp_error($nuevo) ? [] : ['asambleas'];
    }
    return $slugs;
}

/** Asamblea válida (RN-05): evento publicado o programado del calendario que está en la categoría «Asambleas». */
function cadus_votaciones_es_asamblea(int $id): bool
{
    if ($id <= 0 || !cadus_votaciones_hay_calendario() || get_post_type($id) !== 'tribe_events') {
        return false;
    }
    if (!in_array(get_post_status($id), ['publish', 'future'], true)) {
        return false;
    }
    $categorias = cadus_votaciones_categorias_asamblea();
    return $categorias && has_term($categorias, 'tribe_events_cat', $id);
}

/** Marca de tiempo de inicio de un evento del calendario (0 si no se puede leer). */
function cadus_votaciones_inicio_evento(int $id): int
{
    $texto = function_exists('tribe_get_start_date') ? (string) tribe_get_start_date($id, true, 'Y-m-d H:i:s') : '';
    if ($texto === '') {
        $texto = (string) get_post_meta($id, '_EventStartDate', true);
    }
    return cadus_votaciones_ts_sql($texto);
}

/**
 * Asambleas que se ofrecen en el formulario, de la más reciente a la más antigua.
 * @return array<int, array{titulo: string, ts: int}>
 */
function cadus_votaciones_asambleas(): array
{
    if (!cadus_votaciones_hay_calendario()) {
        return [];
    }
    $args = ['post_type' => 'tribe_events', 'post_status' => ['publish', 'future'], 'posts_per_page' => 100, 'no_found_rows' => true];
    $categorias = cadus_votaciones_categorias_asamblea();
    if (!$categorias) {
        return [];
    }
    $args['tax_query'] = [['taxonomy' => 'tribe_events_cat', 'field' => 'slug', 'terms' => $categorias]];
    if (function_exists('tribe_get_events')) {
        // «custom» sin fechas: todos los eventos, también los ya celebrados.
        $consulta = tribe_get_events($args + ['eventDisplay' => 'custom', 'orderby' => 'event_date', 'order' => 'DESC']);
    } else {
        $consulta = get_posts($args + ['meta_key' => '_EventStartDate', 'orderby' => 'meta_value', 'order' => 'DESC']);
    }
    $lista = [];
    foreach (is_array($consulta) ? $consulta : [] as $evento) {
        if ($evento instanceof WP_Post) {
            $lista[(int) $evento->ID] = ['titulo' => get_the_title($evento), 'ts' => cadus_votaciones_inicio_evento((int) $evento->ID)];
        }
    }
    return $lista;
}

/* --------------------------------------------------------------------- fechas */

/** Marca de tiempo de un valor «Y-m-d\TH:i» (campo datetime-local) en la zona horaria del sitio; 0 si no es válido. */
function cadus_votaciones_ts(string $local): int
{
    if (!preg_match('/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/', $local)) {
        return 0;
    }
    try {
        return (new DateTimeImmutable($local, wp_timezone()))->getTimestamp();
    } catch (Exception $e) {
        return 0;
    }
}

/** Marca de tiempo de una fecha «Y-m-d», «Y-m-d H:i» o «Y-m-d H:i:s» en la zona horaria del sitio; 0 si no es válida. */
function cadus_votaciones_ts_sql(string $fecha): int
{
    $fecha = trim($fecha);
    if (!preg_match('/^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}(:\d{2})?)?$/', $fecha)) {
        return 0;
    }
    try {
        return (new DateTimeImmutable($fecha, wp_timezone()))->getTimestamp();
    } catch (Exception $e) {
        return 0;
    }
}

function cadus_votaciones_formato(int $ts): string
{
    return $ts ? wp_date('j \d\e F \d\e Y, H:i', $ts) : '—';
}

/** Datos de la votación: periodo, ID de la encuesta y asamblea vinculada. */
function cadus_votaciones_datos(int $id): array
{
    $asamblea = null;
    $evento = (int) get_post_meta($id, '_cadus_vot_asamblea', true);
    if ($evento > 0 && get_post_type($evento) === 'tribe_events' && in_array(get_post_status($evento), ['publish', 'future'], true)) {
        $asamblea = ['titulo' => get_the_title($evento), 'ts' => cadus_votaciones_inicio_evento($evento), 'url' => (string) get_permalink($evento)];
    } elseif ((string) get_post_meta($id, '_cadus_vot_asamblea_titulo', true) !== '') {
        $asamblea = [
            'titulo' => (string) get_post_meta($id, '_cadus_vot_asamblea_titulo', true),
            'ts' => cadus_votaciones_ts_sql((string) get_post_meta($id, '_cadus_vot_asamblea_fecha', true)),
            'url' => (string) get_post_meta($id, '_cadus_vot_asamblea_url', true),
        ];
    }
    return [
        'apertura' => cadus_votaciones_ts((string) get_post_meta($id, '_cadus_vot_apertura', true)),
        'cierre' => cadus_votaciones_ts((string) get_post_meta($id, '_cadus_vot_cierre', true)),
        'poll' => (int) get_post_meta($id, '_cadus_vot_poll', true),
        'asamblea' => $asamblea,
    ];
}

/** Fase según las fechas de la convocatoria: proxima, abierta o cerrada. */
function cadus_votaciones_fase(array $datos, ?int $ahora = null): string
{
    $ahora = $ahora ?? time();
    if (!$datos['apertura'] || !$datos['cierre'] || $ahora < $datos['apertura']) {
        return 'proxima';
    }
    return $ahora <= $datos['cierre'] ? 'abierta' : 'cerrada';
}

function cadus_votaciones_etiqueta_fase(string $fase): string
{
    return ['proxima' => 'Próxima', 'abierta' => 'Abierta', 'cerrada' => 'Cerrada'][$fase] ?? '';
}

/* --------------------------------------------------------------------- formulario de la convocatoria */

function cadus_votaciones_metaboxes(): void
{
    add_meta_box('cadus_votacion_datos', 'Datos de la votación', 'cadus_votaciones_caja', 'cadus_votacion', 'normal', 'high');
}

function cadus_votaciones_caja(WP_Post $post): void
{
    wp_nonce_field('cadus_votacion_guardar', 'cadus_votacion_nonce');
    $asamblea = (int) get_post_meta($post->ID, '_cadus_vot_asamblea', true);
    $poll = (int) get_post_meta($post->ID, '_cadus_vot_poll', true);

    echo '<h4>Asamblea vinculada (obligatoria · RN-05)</h4>';
    if (cadus_votaciones_hay_calendario()) {
        $lista = cadus_votaciones_asambleas();
        if ($asamblea && !isset($lista[$asamblea]) && get_post($asamblea)) {
            $lista = [$asamblea => ['titulo' => get_the_title($asamblea), 'ts' => cadus_votaciones_inicio_evento($asamblea)]] + $lista;
        }
        echo '<p><label for="cadus_vot_asamblea">Convocatoria de asamblea del calendario</label><br>'
            . '<select id="cadus_vot_asamblea" name="cadus_vot_asamblea" class="widefat"><option value="0">— Elige una asamblea —</option>';
        foreach ($lista as $id => $evento) {
            echo '<option value="' . (int) $id . '"' . selected($asamblea, $id, false) . '>'
                . esc_html($evento['titulo'] . ($evento['ts'] ? ' · ' . wp_date('d/m/Y H:i', $evento['ts']) : '')) . '</option>';
        }
        echo '</select></p>';
        if (!$lista) {
            echo '<p class="description">Todavía no hay asambleas en el calendario. Crea primero la convocatoria de la asamblea en Eventos.</p>';
        }
    } else {
        echo '<p class="description"><strong>Modo provisional:</strong> The Events Calendar no está activo, así que la asamblea se indica a mano. '
            . 'Con el calendario activo, este campo pasa a ser un selector de asambleas.</p>'
            . '<p><label for="cadus_vot_asamblea_titulo">Título de la asamblea</label><br>'
            . '<input type="text" class="widefat" id="cadus_vot_asamblea_titulo" name="cadus_vot_asamblea_titulo" value="'
            . esc_attr((string) get_post_meta($post->ID, '_cadus_vot_asamblea_titulo', true)) . '"></p>'
            . '<p><label for="cadus_vot_asamblea_fecha">Fecha de la asamblea</label><br>'
            . '<input type="date" id="cadus_vot_asamblea_fecha" name="cadus_vot_asamblea_fecha" value="'
            . esc_attr(substr((string) get_post_meta($post->ID, '_cadus_vot_asamblea_fecha', true), 0, 10)) . '"></p>'
            . '<p><label for="cadus_vot_asamblea_url">Enlace a la convocatoria (opcional)</label><br>'
            . '<input type="url" class="widefat" id="cadus_vot_asamblea_url" name="cadus_vot_asamblea_url" value="'
            . esc_attr((string) get_post_meta($post->ID, '_cadus_vot_asamblea_url', true)) . '"></p>';
    }

    echo '<h4>Periodo de votación</h4><p>'
        . '<label for="cadus_vot_apertura">Apertura</label> <input type="datetime-local" id="cadus_vot_apertura" name="cadus_vot_apertura" value="'
        . esc_attr((string) get_post_meta($post->ID, '_cadus_vot_apertura', true)) . '"> '
        . '<label for="cadus_vot_cierre">Cierre</label> <input type="datetime-local" id="cadus_vot_cierre" name="cadus_vot_cierre" value="'
        . esc_attr((string) get_post_meta($post->ID, '_cadus_vot_cierre', true)) . '"></p>'
        . '<p class="description">Hora del sitio (' . esc_html(wp_timezone_string()) . '). El cierre debe ser posterior a la apertura. '
        . 'Configura las mismas fechas en YOP Poll para que ambas coincidan.</p>';

    echo '<h4>Papeleta en YOP Poll</h4><p><label for="cadus_vot_poll">ID de la encuesta</label> '
        . '<input type="number" min="0" step="1" id="cadus_vot_poll" name="cadus_vot_poll" value="' . ($poll ?: '') . '"></p>'
        . '<p class="description">Crea la encuesta en YOP Poll y copia su ID. Se muestra en la página de la votación solo mientras esté abierta.</p>'
        . '<p class="description">Una votación sin asamblea vinculada ni periodo válido no se puede publicar: se guarda como borrador.</p>';
}

function cadus_votaciones_guardar(int $post_id, WP_Post $post): void
{
    if (wp_is_post_autosave($post_id) || wp_is_post_revision($post_id)) {
        return;
    }
    $nonce = isset($_POST['cadus_votacion_nonce']) ? sanitize_text_field(wp_unslash($_POST['cadus_votacion_nonce'])) : '';
    if ($nonce !== '' && wp_verify_nonce($nonce, 'cadus_votacion_guardar') && current_user_can('edit_post', $post_id)) {
        $texto = static function (string $clave): string {
            return isset($_POST[$clave]) && is_string($_POST[$clave]) ? sanitize_text_field(wp_unslash($_POST[$clave])) : '';
        };
        $guardar = static function (string $meta, $valor) use ($post_id): void {
            if ($valor === '' || $valor === 0) {
                delete_post_meta($post_id, $meta);
            } else {
                update_post_meta($post_id, $meta, $valor);
            }
        };
        $momento = static fn(string $v): string => cadus_votaciones_ts($v) ? $v : '';
        $fecha = static fn(string $v): string => preg_match('/^\d{4}-\d{2}-\d{2}$/', $v) ? $v : '';
        $guardar('_cadus_vot_asamblea', absint($texto('cadus_vot_asamblea')));
        $guardar('_cadus_vot_asamblea_titulo', $texto('cadus_vot_asamblea_titulo'));
        $guardar('_cadus_vot_asamblea_fecha', $fecha($texto('cadus_vot_asamblea_fecha')));
        $guardar('_cadus_vot_asamblea_url', isset($_POST['cadus_vot_asamblea_url']) && is_string($_POST['cadus_vot_asamblea_url'])
            ? esc_url_raw(wp_unslash($_POST['cadus_vot_asamblea_url'])) : '');
        $guardar('_cadus_vot_apertura', $momento($texto('cadus_vot_apertura')));
        $guardar('_cadus_vot_cierre', $momento($texto('cadus_vot_cierre')));
        $guardar('_cadus_vot_poll', absint($texto('cadus_vot_poll')));
    }
    cadus_votaciones_exigir_requisitos($post_id, $post);
    if (get_post_status($post_id) === 'publish') {
        cadus_votaciones_vaciar_cache();
    }
}

/** Motivos por los que la votación no cumple RN-05 o no tiene un periodo válido (lista vacía si es correcta). */
function cadus_votaciones_errores(int $id): array
{
    $errores = [];
    if (cadus_votaciones_hay_calendario()) {
        if (!cadus_votaciones_es_asamblea((int) get_post_meta($id, '_cadus_vot_asamblea', true))) {
            $errores[] = 'Debe vincularse a una asamblea ya creada en el calendario (RN-05).';
        }
    } else {
        // Sin The Events Calendar no hay asambleas que vincular: la votación se queda en borrador (RN-05).
        $errores[] = 'The Events Calendar no está activo: sin calendario no se puede vincular la votación a una asamblea (RN-05).';
    }
    $apertura = cadus_votaciones_ts((string) get_post_meta($id, '_cadus_vot_apertura', true));
    $cierre = cadus_votaciones_ts((string) get_post_meta($id, '_cadus_vot_cierre', true));
    if (!$apertura || !$cierre) {
        $errores[] = 'Indica la fecha y hora de apertura y de cierre de la votación.';
    } elseif ($cierre <= $apertura) {
        $errores[] = 'El cierre debe ser posterior a la apertura.';
    }
    return $errores;
}

/** RN-05 en el servidor: una votación publicada o programada que no cumple vuelve a borrador. */
function cadus_votaciones_exigir_requisitos(int $id, WP_Post $post): void
{
    if (!in_array($post->post_status, ['publish', 'future'], true)) {
        return;
    }
    $errores = cadus_votaciones_errores($id);
    if (!$errores) {
        return;
    }
    remove_action('save_post_cadus_votacion', 'cadus_votaciones_guardar', 10);
    wp_update_post(['ID' => $id, 'post_status' => 'draft']);
    add_action('save_post_cadus_votacion', 'cadus_votaciones_guardar', 10, 2);
    set_transient('cadus_votaciones_aviso_' . get_current_user_id(), $errores, MINUTE_IN_SECONDS);
}

/** Tras volver a borrador, WordPress debe mostrar el mensaje de borrador y no el de publicada. */
function cadus_votaciones_redireccion(string $ubicacion, int $post_id): string
{
    if (get_post_type($post_id) === 'cadus_votacion' && get_transient('cadus_votaciones_aviso_' . get_current_user_id())) {
        return add_query_arg('message', 10, $ubicacion);
    }
    return $ubicacion;
}

function cadus_votaciones_avisos(): void
{
    $clave = 'cadus_votaciones_aviso_' . get_current_user_id();
    $errores = get_transient($clave);
    $pantalla = function_exists('get_current_screen') ? get_current_screen() : null;
    if (!$errores || !$pantalla || $pantalla->post_type !== 'cadus_votacion') {
        return;
    }
    delete_transient($clave);
    echo '<div class="notice notice-error"><p><strong>La votación no se ha publicado y se ha guardado como borrador.</strong></p><ul>';
    foreach ((array) $errores as $error) {
        echo '<li>' . esc_html((string) $error) . '</li>';
    }
    echo '</ul></div>';
}

/** La portada puede estar en la caché de página: se vacía al publicar, editar o retirar una votación. */
function cadus_votaciones_vaciar_cache(): void
{
    do_action('wpfc_clear_all_cache');
}

function cadus_votaciones_cambio_estado(string $nuevo, string $anterior, WP_Post $post): void
{
    if ($post->post_type === 'cadus_votacion' && ($nuevo === 'publish' || $anterior === 'publish')) {
        cadus_votaciones_vaciar_cache();
    }
}

/* --------------------------------------------------------------------- listado de administración */

function cadus_votaciones_columnas(array $columnas): array
{
    $nuevas = [];
    foreach ($columnas as $clave => $texto) {
        $nuevas[$clave] = $texto;
        if ($clave === 'title') {
            $nuevas['cadus_asamblea'] = 'Asamblea';
            $nuevas['cadus_periodo'] = 'Periodo';
            $nuevas['cadus_fase'] = 'Estado';
        }
    }
    unset($nuevas['date']);
    return $nuevas;
}

function cadus_votaciones_columna(string $columna, int $post_id): void
{
    $datos = cadus_votaciones_datos($post_id);
    if ($columna === 'cadus_asamblea') {
        echo esc_html($datos['asamblea']['titulo'] ?? '— sin asamblea —');
    } elseif ($columna === 'cadus_periodo') {
        echo esc_html(cadus_votaciones_formato($datos['apertura']) . ' → ' . cadus_votaciones_formato($datos['cierre']));
    } elseif ($columna === 'cadus_fase') {
        echo esc_html(cadus_votaciones_etiqueta_fase(cadus_votaciones_fase($datos)));
    }
}

/* --------------------------------------------------------------------- permisos, menú y página (una vez por versión) */

/** Añade «Votaciones» a la lista cerrada de menús de la Ejecutiva (HU-19a). */
function cadus_votaciones_menus_admin(array $menus, string $rol): array
{
    if ($rol === 'cadus_ejecutiva') {
        $menus['edit.php?post_type=cadus_votacion'] = ['edit.php?post_type=cadus_votacion', 'post-new.php?post_type=cadus_votacion'];
    }
    return $menus;
}

/** Permite «Nuevo › Votación» en la barra superior de la Ejecutiva. */
function cadus_votaciones_barra_nuevos(array $nuevos, string $rol): array
{
    if ($rol === 'cadus_ejecutiva') {
        $nuevos[] = 'new-cadus_votacion';
    }
    return $nuevos;
}

/**
 * Se ejecuta una sola vez por versión, desde el panel y con los roles ya creados:
 * da al Ejecutivo y al administrador las capacidades del tipo y crea la página «Votaciones» con su entrada de menú.
 * No pisa páginas ni elementos de menú existentes.
 */
function cadus_votaciones_migrar(): void
{
    if (!is_admin() || get_option('cadus_votaciones_version') === CADUS_VOTACIONES_VERSION || !get_role('cadus_ejecutiva')) {
        return;
    }
    foreach (['cadus_ejecutiva', 'administrator'] as $slug) {
        $rol = get_role($slug);
        if ($rol) {
            foreach (cadus_caps_cpt('cadus_votacion', 'cadus_votacions') as $cap) {
                $rol->add_cap($cap);
            }
        }
    }
    if (function_exists('cadus_pagina') && function_exists('cadus_b_p') && function_exists('cadus_b_sc')) {
        $pagina = cadus_pagina(
            'votaciones',
            'Votaciones',
            cadus_b_p('Convocatorias de votación del CADUS. Cada votación está vinculada a una asamblea del calendario y solo se puede votar mientras está abierta.')
                . cadus_b_sc('[cadus_votaciones]')
        );
        if ($pagina) {
            cadus_votaciones_menu($pagina);
        }
    }
    update_option('cadus_votaciones_version', CADUS_VOTACIONES_VERSION);
}

/** «Votaciones» cuelga de «Calendario» si el calendario está en el menú; si no, queda al final. */
function cadus_votaciones_menu(int $pagina): void
{
    $menu = function_exists('cadus_calendario_menu_principal') ? cadus_calendario_menu_principal() : wp_get_nav_menu_object('Menú principal CADUS');
    if (!$menu instanceof WP_Term) {
        return;
    }
    $padre = 0;
    foreach ((array) wp_get_nav_menu_items($menu->term_id, ['post_status' => 'any']) as $item) {
        if ($item->type === 'post_type' && (int) $item->object_id === $pagina) {
            return; // ya está en el menú
        }
        if ($item->type === 'post_type_archive' && $item->object === 'tribe_events') {
            $padre = (int) $item->ID;
        }
    }
    wp_update_nav_menu_item($menu->term_id, 0, [
        'menu-item-title' => 'Votaciones', 'menu-item-object' => 'page', 'menu-item-object-id' => $pagina,
        'menu-item-type' => 'post_type', 'menu-item-status' => 'publish', 'menu-item-parent-id' => $padre,
    ]);
}

/* --------------------------------------------------------------------- páginas públicas */

/** La fase cambia con el tiempo: la lista y la ficha de cada votación no se guardan en la caché de página. */
function cadus_votaciones_sin_cache(): void
{
    $objeto = get_queried_object();
    if (!is_singular('cadus_votacion') && !($objeto instanceof WP_Post && has_shortcode($objeto->post_content, 'cadus_votaciones'))) {
        return;
    }
    if (!defined('DONOTCACHEPAGE')) {
        define('DONOTCACHEPAGE', true);
    }
    do_action('wpfc_exclude_current_page'); // WP Fastest Cache no siempre respeta la constante (ver buzon.php)
    if (!headers_sent()) {
        nocache_headers();
    }
}

/** Votaciones publicadas con sus datos y su fase. */
function cadus_votaciones_listar(int $limite = 50): array
{
    $lista = [];
    foreach (get_posts(['post_type' => 'cadus_votacion', 'post_status' => 'publish', 'posts_per_page' => $limite,
        'has_password' => false, 'orderby' => 'date', 'order' => 'DESC', 'no_found_rows' => true]) as $post) {
        $datos = cadus_votaciones_datos((int) $post->ID);
        $lista[] = ['post' => $post, 'datos' => $datos, 'fase' => cadus_votaciones_fase($datos)];
    }
    return $lista;
}

/** Tarjeta de una votación con el formato del diseño interior (cadus-interior.css). */
function cadus_votaciones_tarjeta(array $v): string
{
    $post = $v['post'];
    $datos = $v['datos'];
    $asamblea = $datos['asamblea'];
    $titulo = get_the_title($post);
    $html = '<article class="cadus-tarjeta"><p class="cadus-meta">' . esc_html(cadus_votaciones_etiqueta_fase($v['fase'])) . '</p>'
        . '<h3><a href="' . esc_url(get_permalink($post)) . '">' . esc_html($titulo) . '</a></h3>';
    if ($asamblea) {
        $html .= '<p>' . esc_html('Asamblea: ' . $asamblea['titulo'] . ($asamblea['ts'] ? ' · ' . wp_date('d/m/Y', $asamblea['ts']) : '')) . '</p>';
    }
    return $html . '<p>Del <time datetime="' . esc_attr(wp_date('c', $datos['apertura'])) . '">' . esc_html(cadus_votaciones_formato($datos['apertura']))
        . '</time> al <time datetime="' . esc_attr(wp_date('c', $datos['cierre'])) . '">' . esc_html(cadus_votaciones_formato($datos['cierre'])) . '</time></p>'
        . '<a class="cadus-boton" href="' . esc_url(get_permalink($post)) . '">Ver votación<span class="screen-reader-text">: '
        . esc_html($titulo) . '</span></a></article>';
}

/** [cadus_votaciones]: votaciones abiertas, próximas y las diez últimas cerradas. */
function cadus_votaciones_shortcode(): string
{
    $grupos = ['abierta' => [], 'proxima' => [], 'cerrada' => []];
    foreach (cadus_votaciones_listar() as $v) {
        $grupos[$v['fase']][] = $v;
    }
    if (!array_filter($grupos)) {
        return '<p class="cadus-vacio">No hay votaciones convocadas por ahora. Las convocatorias se publican aquí, vinculadas a cada asamblea.</p>';
    }
    usort($grupos['abierta'], static fn(array $x, array $y): int => $x['datos']['cierre'] <=> $y['datos']['cierre']);
    usort($grupos['proxima'], static fn(array $x, array $y): int => $x['datos']['apertura'] <=> $y['datos']['apertura']);
    usort($grupos['cerrada'], static fn(array $x, array $y): int => $y['datos']['cierre'] <=> $x['datos']['cierre']);
    $titulos = ['abierta' => 'Votaciones abiertas', 'proxima' => 'Próximas votaciones', 'cerrada' => 'Votaciones cerradas'];
    $html = '';
    foreach ($grupos as $fase => $items) {
        if (!$items) {
            continue;
        }
        // Sin contenedor común: el diseño interior da formato a los hijos directos del contenido.
        $html .= '<h2>' . esc_html($titulos[$fase]) . '</h2><div class="cadus-tarjetas">';
        foreach ($fase === 'cerrada' ? array_slice($items, 0, 10) : $items as $v) {
            $html .= cadus_votaciones_tarjeta($v);
        }
        $html .= '</div>';
    }
    return $html;
}

/**
 * [cadus_votaciones_portada]: bloque de la portada con las votaciones abiertas o próximas (IR-01 · UI-02), con el formato de «¡Últimos eventos!».
 * No muestra la fase, solo las fechas: el HTML de la portada puede estar en caché; la fase real se ve en cada votación.
 */
function cadus_votaciones_portada_shortcode(): string
{
    $activas = array_values(array_filter(cadus_votaciones_listar(), static fn(array $v): bool => $v['fase'] !== 'cerrada'));
    if (!$activas) {
        return '';
    }
    usort($activas, static function (array $x, array $y): int {
        $orden = ['abierta' => 0, 'proxima' => 1];
        return [$orden[$x['fase']], $x['datos']['apertura']] <=> [$orden[$y['fase']], $y['datos']['apertura']];
    });
    $meses = [1 => 'ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
    $html = '<section class="cadus-seccion cadus-seccion--eventos cadus-seccion--votaciones"><h2 class="cadus-seccion__titulo" data-reveal>'
        . esc_html('Participa en las votaciones') . '</h2><ul class="cadus-eventos">';
    foreach (array_slice($activas, 0, 3) as $i => $v) {
        $inicio = $v['datos']['apertura'];
        $html .= '<li class="cadus-evento" data-reveal style="--i:' . esc_attr((string) $i) . '">'
            . '<a class="cadus-evento__enlace" href="' . esc_url(get_permalink($v['post'])) . '">'
            . '<time class="cadus-evento__fecha" datetime="' . esc_attr(wp_date('Y-m-d', $inicio)) . '">'
            . '<span class="cadus-evento__dia">' . esc_html(wp_date('d', $inicio)) . '</span>'
            . '<span class="cadus-evento__mes">' . esc_html($meses[(int) wp_date('n', $inicio)]) . '</span></time>'
            . '<span class="cadus-evento__titulo">' . esc_html(get_the_title($v['post'])) . '</span>'
            . '<span class="cadus-evento__ver">' . esc_html('Del ' . wp_date('d/m', $inicio) . ' al ' . wp_date('d/m', $v['datos']['cierre'])) . '</span></a></li>';
    }
    return $html . '</ul></section>';
}

/** El bloque de votaciones sigue a «¡Últimos eventos!» en la portada, sin tocar inicio.php ni portada_extra.php. */
function cadus_votaciones_tras_eventos($salida, $etiqueta)
{
    return $etiqueta === 'cadus_eventos' ? (string) $salida . cadus_votaciones_portada_shortcode() : $salida;
}

/** Votaciones publicadas vinculadas a una asamblea del calendario. */
function cadus_votaciones_de_asamblea(int $evento): array
{
    $lista = [];
    foreach (get_posts(['post_type' => 'cadus_votacion', 'post_status' => 'publish', 'posts_per_page' => 20, 'has_password' => false,
        'meta_key' => '_cadus_vot_asamblea', 'meta_value' => $evento, 'no_found_rows' => true]) as $post) {
        $datos = cadus_votaciones_datos((int) $post->ID);
        $lista[] = ['post' => $post, 'datos' => $datos, 'fase' => cadus_votaciones_fase($datos)];
    }
    return $lista;
}

/** Ficha de la votación (asamblea, periodo y papeleta) y, en cada asamblea del calendario, sus votaciones vinculadas. */
function cadus_votaciones_en_contenido(string $contenido): string
{
    if (!in_the_loop() || !is_main_query()) {
        return $contenido;
    }
    if (is_singular('tribe_events')) {
        $votaciones = cadus_votaciones_de_asamblea((int) get_the_ID());
        if (!$votaciones) {
            return $contenido;
        }
        $html = '<h2>Votaciones de esta asamblea</h2><ul class="cadus-votaciones__vinculadas">';
        foreach ($votaciones as $v) {
            $html .= '<li><a href="' . esc_url(get_permalink($v['post'])) . '">' . esc_html(get_the_title($v['post'])) . '</a> · '
                . esc_html(cadus_votaciones_etiqueta_fase($v['fase'])) . '</li>';
        }
        return $contenido . $html . '</ul>';
    }
    if (!is_singular('cadus_votacion')) {
        return $contenido;
    }
    $datos = cadus_votaciones_datos((int) get_the_ID());
    $fase = cadus_votaciones_fase($datos);
    $asamblea = $datos['asamblea'];
    $fila = static fn(string $dt, string $dd): string => '<div class="cadus-ficha__fila"><dt>' . esc_html($dt) . '</dt><dd>' . $dd . '</dd></div>';
    $html = '<dl class="cadus-ficha">' . $fila('Estado', esc_html(cadus_votaciones_etiqueta_fase($fase)));
    if ($asamblea) {
        $nombre = esc_html($asamblea['titulo']) . ($asamblea['ts'] ? ' · ' . esc_html(wp_date('j \d\e F \d\e Y, H:i', $asamblea['ts'])) : '');
        $html .= $fila('Asamblea', $asamblea['url'] !== '' ? '<a href="' . esc_url($asamblea['url']) . '">' . $nombre . '</a>' : $nombre);
    }
    $html .= $fila('Apertura', esc_html(cadus_votaciones_formato($datos['apertura']))) . $fila('Cierre', esc_html(cadus_votaciones_formato($datos['cierre']))) . '</dl>';
    if ($fase === 'proxima') {
        $html .= '<div class="cadus-aviso">La votación todavía no está abierta. Podrás votar aquí a partir del ' . esc_html(cadus_votaciones_formato($datos['apertura'])) . '.</div>';
    } elseif ($fase === 'cerrada') {
        $html .= '<div class="cadus-aviso">La votación se cerró el ' . esc_html(cadus_votaciones_formato($datos['cierre'])) . '.</div>';
    } elseif ($datos['poll'] > 0 && shortcode_exists('yop_poll')) {
        $html .= '<div class="cadus-votacion__papeleta">' . do_shortcode('[yop_poll id="' . (int) $datos['poll'] . '"]') . '</div>';
    } else {
        $html .= '<div class="cadus-aviso">La papeleta de esta votación todavía no está disponible. Vuelve a intentarlo en unos minutos.</div>';
    }
    if (function_exists('cadus_inicio_url')) {
        $html .= '<p><a class="cadus-chip" href="' . esc_url(cadus_inicio_url('votaciones')) . '">← Volver a las votaciones</a></p>';
    }
    return $contenido . $html;
}

