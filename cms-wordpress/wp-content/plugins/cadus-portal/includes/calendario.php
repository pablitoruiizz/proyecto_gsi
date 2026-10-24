<?php
/**
 * Calendario de asambleas y eventos con The Events Calendar (HU-10 · RF-11 · UI-02).
 *
 * El plugin The Events Calendar aporta el tipo de contenido «tribe_events», las vistas de calendario
 * (mes, lista y día) y la página pública del calendario. Este módulo solo lo integra en el portal:
 *  - la sección «¡Últimos eventos!» de la portada muestra los próximos eventos del calendario;
 *  - el acceso «Calendario» de la portada y el menú principal enlazan con la página del calendario;
 *  - el rol Ejecutivo del CADUS puede crear, editar y publicar eventos, lugares y organizadores;
 *  - el menú de administración de la Ejecutiva incluye «Eventos» (lista cerrada de HU-19a).
 *
 * Si The Events Calendar no está activo, nada de esto se aplica y la portada sigue usando
 * las entradas de la categoría Eventos, como en el Sprint 1.
 */

if (!defined('ABSPATH')) {
    exit;
}

define('CADUS_CALENDARIO_VERSION', '1');

add_action('init', 'cadus_calendario_migrar', 30);
add_action('transition_post_status', 'cadus_calendario_cambio_estado', 10, 3);
add_action('deleted_post', 'cadus_calendario_borrado', 10, 2);
add_filter('cadus_menus_admin', 'cadus_calendario_menus_admin', 10, 2);
add_filter('cadus_barra_nuevos', 'cadus_calendario_barra_nuevos', 10, 2);

function cadus_calendario_activo(): bool
{
    return function_exists('tribe_get_events') && post_type_exists('tribe_events');
}

/** URL pública del calendario; The Events Calendar la adapta al dominio y al idioma (p. ej. /eventos/). */
function cadus_calendario_url(): string
{
    return cadus_calendario_activo() ? (string) get_post_type_archive_link('tribe_events') : '';
}

/**
 * Próximos eventos (y los que están en curso) con el formato que espera la portada.
 * Solo eventos publicados y sin contraseña: el resultado se guarda en una caché compartida por todos los visitantes.
 * @return array<int, array{titulo: string, url: string, fecha: string}>
 */
function cadus_calendario_eventos(int $n = 4): array
{
    $eventos = tribe_get_events([
        'posts_per_page' => $n,
        'post_status' => 'publish',
        'ends_after' => 'now',
        'orderby' => 'event_date',
        'order' => 'ASC',
    ]);
    $resultado = [];
    foreach (is_array($eventos) ? $eventos : [] as $evento) {
        if (!$evento instanceof WP_Post || $evento->post_status !== 'publish' || $evento->post_password !== '') {
            continue;
        }
        $resultado[] = [
            'titulo' => get_the_title($evento),
            'url' => (string) get_permalink($evento),
            'fecha' => (string) tribe_get_start_date($evento, false, 'Y-m-d'),
        ];
    }
    return $resultado;
}

/** Al crear, editar o borrar un evento se recalculan los datos de la portada. */
function cadus_calendario_cambio_estado(string $nuevo, string $anterior, WP_Post $post): void
{
    if ($post->post_type === 'tribe_events') {
        delete_transient('cadus_portada_datos');
    }
}

function cadus_calendario_borrado(int $id, WP_Post $post): void
{
    cadus_calendario_cambio_estado('', '', $post);
}

/* --------------------------------------------------------------------- permisos y menú (una vez por versión) */

/** Capacidades de eventos, lugares y organizadores (los tres tipos de The Events Calendar). */
function cadus_calendario_caps(): array
{
    $caps = [];
    foreach ([['tribe_event', 'tribe_events'], ['tribe_venue', 'tribe_venues'], ['tribe_organizer', 'tribe_organizers']] as [$s, $p]) {
        $caps = array_merge($caps, cadus_caps_cpt($s, $p));
    }
    return $caps;
}

/**
 * Se ejecuta una sola vez, la primera vez que The Events Calendar está activo.
 * The Events Calendar solo da permisos a los roles estándar de WordPress; el Ejecutivo del CADUS es un rol propio.
 */
function cadus_calendario_migrar(): void
{
    // Autorreparable: si la versión ya está aplicada pero la Ejecutiva ha perdido los permisos de eventos
    // (p. ej. porque otro proceso reescribió la lista de roles con una copia antigua), se vuelven a conceder.
    $permisos_ok = true;
    foreach (['cadus_ejecutiva', 'administrator'] as $slug) {
        $rol = get_role($slug);
        foreach ($rol ? cadus_calendario_caps() : [] as $cap) {
            $permisos_ok = $permisos_ok && $rol->has_cap($cap);
        }
    }
    if (!cadus_calendario_activo() || (get_option('cadus_calendario_version') === CADUS_CALENDARIO_VERSION && $permisos_ok)) {
        return;
    }
    foreach (['cadus_ejecutiva', 'administrator'] as $slug) {
        $rol = get_role($slug);
        if ($rol) {
            foreach (cadus_calendario_caps() as $cap) {
                $rol->add_cap($cap);
            }
        }
    }
    cadus_calendario_menu();
    update_option('cadus_calendario_version', CADUS_CALENDARIO_VERSION);
}

/** Menú asignado a la cabecera; si no hay ninguno, el que crea el plugin. */
function cadus_calendario_menu_principal(): ?WP_Term
{
    $ubicaciones = get_nav_menu_locations();
    $menu = !empty($ubicaciones['menu_1']) ? wp_get_nav_menu_object((int) $ubicaciones['menu_1']) : false;
    if (!$menu) {
        $menu = wp_get_nav_menu_object('Menú principal CADUS');
    }
    return $menu instanceof WP_Term ? $menu : null;
}

/** Añade «Calendario» detrás de «Noticias y comunicados»; después el equipo puede moverlo en Apariencia › Menús. */
function cadus_calendario_menu(): void
{
    $menu = cadus_calendario_menu_principal();
    if (!$menu) {
        return;
    }
    $items = (array) wp_get_nav_menu_items($menu->term_id, ['post_status' => 'any']);
    $orden = 0;
    foreach ($items as $item) {
        if ($item->type === 'post_type_archive' && $item->object === 'tribe_events') {
            return; // ya está en el menú
        }
        if ($item->type === 'post_type' && (int) $item->menu_item_parent === 0
            && get_post_field('post_name', (int) $item->object_id) === 'noticias') {
            $orden = (int) $item->menu_order;
        }
    }
    if ($orden > 0) {
        // Hace hueco detrás de Noticias desplazando una posición los elementos siguientes.
        foreach ($items as $item) {
            if ((int) $item->menu_order > $orden) {
                wp_update_post(['ID' => $item->ID, 'menu_order' => (int) $item->menu_order + 1]);
            }
        }
    }
    // Tipo «archivo»: la URL se calcula en cada visita, así que sigue funcionando al cambiar de dominio o servidor.
    wp_update_nav_menu_item($menu->term_id, 0, [
        'menu-item-title' => 'Calendario',
        'menu-item-type' => 'post_type_archive',
        'menu-item-object' => 'tribe_events',
        'menu-item-status' => 'publish',
        'menu-item-position' => $orden > 0 ? $orden + 1 : count($items) + 1,
    ]);
}

/* --------------------------------------------------------------------- administración por rol (HU-19a) */

/** Añade «Eventos» a la lista cerrada de menús de la Ejecutiva. */
function cadus_calendario_menus_admin(array $menus, string $rol): array
{
    if ($rol === 'cadus_ejecutiva' && cadus_calendario_activo()) {
        $menus['edit.php?post_type=tribe_events'] = [
            'edit.php?post_type=tribe_events',
            'post-new.php?post_type=tribe_events',
            'edit-tags.php?taxonomy=tribe_events_cat&post_type=tribe_events',
            'edit-tags.php?taxonomy=post_tag&post_type=tribe_events',
            'edit.php?post_type=tribe_venue',
            'edit.php?post_type=tribe_organizer',
        ];
    }
    return $menus;
}

/** Permite «Nuevo › Evento» en la barra superior de la Ejecutiva. */
function cadus_calendario_barra_nuevos(array $nuevos, string $rol): array
{
    if ($rol === 'cadus_ejecutiva' && cadus_calendario_activo()) {
        $nuevos[] = 'new-tribe_events';
    }
    return $nuevos;
}
