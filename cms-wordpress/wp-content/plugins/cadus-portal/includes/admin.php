<?php
/** Menús y accesos de administración por rol (HU-19a). */

if (!defined('ABSPATH')) {
    exit;
}

add_action('admin_menu', 'cadus_filtrar_menus_admin', 999);
add_action('admin_bar_menu', 'cadus_filtrar_barra_admin', 999);
add_action('admin_init', 'cadus_bloquear_pantallas_comentarios');
add_filter('map_meta_cap', 'cadus_bloquear_edicion_comentarios', 10, 3);
add_filter('login_redirect', 'cadus_redirigir_login', 10, 3);

/** Solo se filtran usuarios con un único rol CADUS; administrador y multirrol se conservan. */
function cadus_rol_admin($usuario): string
{
    if (!$usuario instanceof WP_User || count($usuario->roles) !== 1) {
        return '';
    }
    $rol = reset($usuario->roles);
    return in_array($rol, ['cadus_ejecutiva', 'cadus_delegado', 'cadus_estudiante'], true) ? $rol : '';
}

/** Lista cerrada de menús y sus submenús; no incorpora accesos de plugins futuros. */
function cadus_menus_admin(string $rol): array
{
    $menus = ['profile.php' => ['profile.php']];
    if ($rol === 'cadus_estudiante') {
        return $menus;
    }

    $menus['index.php'] = ['index.php'];
    $menus['upload.php'] = ['upload.php', 'media-new.php'];
    $menus['edit.php?post_type=cadus_delegacion'] = [
        'edit.php?post_type=cadus_delegacion', 'post-new.php?post_type=cadus_delegacion',
    ];
    if ($rol === 'cadus_ejecutiva') {
        $menus['edit.php'] = ['edit.php', 'post-new.php', 'edit-tags.php?taxonomy=category', 'edit-tags.php?taxonomy=post_tag'];
        $menus['edit.php?post_type=page'] = ['edit.php?post_type=page', 'post-new.php?post_type=page'];
        $menus['edit.php?post_type=cadus_acta'] = [
            'edit.php?post_type=cadus_acta', 'post-new.php?post_type=cadus_acta',
            'edit-tags.php?taxonomy=cadus_tipo_documento&post_type=cadus_acta',
        ];
        $menus['edit.php?post_type=cadus_delegacion'][] = 'edit-tags.php?taxonomy=cadus_centro&post_type=cadus_delegacion';
        $menus['edit.php?post_type=cadus_ticket'] = ['edit.php?post_type=cadus_ticket', 'post-new.php?post_type=cadus_ticket'];
    }
    // Los módulos nuevos (p. ej. el calendario, HU-10) añaden aquí sus menús sin tocar esta lista.
    return apply_filters('cadus_menus_admin', $menus, $rol);
}

function cadus_filtrar_menus_admin(): void
{
    global $menu, $submenu;
    $rol = cadus_rol_admin(wp_get_current_user());
    if ($rol === '') {
        return;
    }

    $permitidos = cadus_menus_admin($rol);
    foreach ((array) $menu as $entrada) {
        if (!isset($permitidos[$entrada[2]])) {
            remove_menu_page($entrada[2]);
        }
    }
    foreach ((array) $submenu as $padre => $entradas) {
        foreach ($entradas as $entrada) {
            // WordPress usa &amp; en los submenús de taxonomías de los tipos propios.
            $slug = str_replace('&amp;', '&', $entrada[2]);
            if (!in_array($slug, $permitidos[$padre] ?? [], true)) {
                remove_submenu_page($padre, $entrada[2]);
            }
        }
    }
}

function cadus_filtrar_barra_admin(WP_Admin_Bar $barra): void
{
    $rol = cadus_rol_admin(wp_get_current_user());
    if ($rol === '') {
        return;
    }

    // Conserva cuenta, salida y navegación al sitio; el resto necesita autorización explícita.
    $permitidos = ['menu-toggle', 'top-secondary', 'my-account', 'user-actions', 'user-info',
        'edit-profile', 'logout', 'site-name', 'view-site', 'search'];
    $nuevos = [];
    if ($rol !== 'cadus_estudiante') {
        $permitidos[] = 'dashboard';
        $nuevos = ['new-media', 'new-cadus_delegacion'];
        if ($rol === 'cadus_ejecutiva') {
            $nuevos = array_merge($nuevos, ['new-post', 'new-page', 'new-cadus_acta', 'new-cadus_ticket']);
        }
        $nuevos = apply_filters('cadus_barra_nuevos', $nuevos, $rol);
    }
    $permitidos = array_merge($permitidos, $nuevos);
    $destino_nuevo = '';
    foreach ((array) $barra->get_nodes() as $nodo) {
        if (in_array($nodo->id, $nuevos, true) && $destino_nuevo === '') {
            $destino_nuevo = $nodo->href;
        }
    }
    if ($destino_nuevo !== '') {
        $permitidos[] = 'new-content';
        // El enlace del padre tampoco debe apuntar a un tipo de contenido oculto.
        $barra->add_node(['id' => 'new-content', 'href' => $destino_nuevo]);
    }
    foreach ((array) $barra->get_nodes() as $nodo) {
        if (!in_array($nodo->id, $permitidos, true)) {
            $barra->remove_node($nodo->id);
        }
    }
    if ($rol === 'cadus_estudiante' && !is_admin() && $barra->get_node('site-name')) {
        $barra->add_node(['id' => 'site-name', 'href' => admin_url('profile.php')]);
    }
}

/** edit-comments.php exige edit_posts: retirar moderate_comments por sí solo no bloquea la URL. */
function cadus_bloquear_pantallas_comentarios(): void
{
    global $pagenow;
    if (cadus_rol_admin(wp_get_current_user()) !== '' && in_array($pagenow, ['edit-comments.php', 'comment.php'], true)) {
        wp_die('No tienes permisos para gestionar comentarios.', 'Acceso denegado', ['response' => 403]);
    }
}

/** También impide editar/moderar comentarios mediante las comprobaciones de capacidad de AJAX y REST. */
function cadus_bloquear_edicion_comentarios(array $caps, string $cap, int $usuario_id): array
{
    if ($cap === 'edit_comment' && cadus_rol_admin(get_userdata($usuario_id)) !== '') {
        return ['do_not_allow'];
    }
    return $caps;
}

/** Respeta el destino solicitado y solo cambia el inicio predeterminado de ejecutivo y delegado. */
function cadus_redirigir_login(string $destino, string $solicitado, $usuario): string
{
    // El formulario de wp-login.php envía siempre «wp-admin/» como destino: eso equivale a no pedir ninguno.
    if ($solicitado !== '' && !in_array(untrailingslashit($solicitado), [untrailingslashit(admin_url()), 'wp-admin'], true)) {
        return $destino;
    }
    $rol = cadus_rol_admin($usuario);
    if ($rol === 'cadus_delegado') {
        return admin_url('edit.php?post_type=cadus_delegacion');
    }
    if ($rol === 'cadus_ejecutiva') {
        return admin_url();
    }
    if ($rol === 'cadus_estudiante') {
        return home_url('/'); // no tiene nada que hacer en el escritorio
    }
    return $destino;
}
