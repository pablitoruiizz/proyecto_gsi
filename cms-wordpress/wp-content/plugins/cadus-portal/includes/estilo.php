<?php
/** Capa visual y de movimiento del portal (Claude): assets/cadus.css y assets/cadus.js. */

if (!defined('ABSPATH')) {
    exit;
}

/** La portada se reconoce por su hero (no por ser la página de inicio): así el CSS no toca otras portadas. */
add_filter('body_class', function (array $clases): array {
    $p = is_singular() ? get_post() : null;
    if ($p && has_shortcode($p->post_content, 'cadus_hero')) {
        $clases[] = 'cadus-portada';
    } else {
        $clases[] = 'cadus-interior'; // resto del portal: fichas, listados, formularios, entradas, búsqueda, 404 y calendario
    }
    return $clases;
});

add_action('wp_enqueue_scripts', function () {
    $css = CADUS_PORTAL_DIR . 'assets/cadus.css';
    $js = CADUS_PORTAL_DIR . 'assets/cadus.js';
    // Debe cargar después del CSS de Blocksy para ganar a su overflow-x del body (si no, se rompe el sticky de los pasos).
    $deps = wp_style_is('ct-main-styles', 'registered') ? ['ct-main-styles'] : [];
    wp_enqueue_style('cadus-portal', CADUS_PORTAL_URL . 'assets/cadus.css', $deps, (string) filemtime($css));
    wp_add_inline_style('cadus-portal', ':root{--cadus-logo:url("' . esc_url_raw(CADUS_PORTAL_URL . 'assets/logo-cadus.png') . '");'
        . '}');
    $css_int = CADUS_PORTAL_DIR . 'assets/cadus-interior.css';
    wp_enqueue_style('cadus-interior', CADUS_PORTAL_URL . 'assets/cadus-interior.css', ['cadus-portal'], (string) filemtime($css_int));
    wp_enqueue_script('cadus-portal', CADUS_PORTAL_URL . 'assets/cadus.js', [], (string) filemtime($js), ['strategy' => 'defer', 'in_footer' => true]);
}, 20);

/** WordPress titula el archivo del calendario «Archivos Eventos»: se sustituye por un título útil. */
add_filter('get_the_archive_title', function ($titulo) {
    return function_exists('is_post_type_archive') && is_post_type_archive('tribe_events') ? 'Calendario de asambleas y eventos' : $titulo;
});

/**
 * Privacidad del equipo: las entradas y fichas no muestran su autor (en este portal firma el CADUS, no la persona que
 * publica), no hay archivos de autor y no se piden avatares a Gravatar (una petición a un tercero con la IP del visitante).
 */
add_filter('pre_option_show_avatars', '__return_zero');
add_filter('pre_get_avatar', '__return_empty_string'); // el tema pide el avatar con get_avatar(): evita la imagen de Gravatar
add_filter('author_link', function () {
    return home_url('/');
});
add_action('template_redirect', function () {
    if (is_author()) {
        global $wp_query;
        $wp_query->set_404();
        status_header(404);
        nocache_headers();
    }
});
// Blocksy pide el avatar con get_avatar_url(): se sustituye por un píxel transparente propio (sin petición externa).
add_filter('get_avatar_url', function () {
    return 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
}, PHP_INT_MAX);

/** Sin comentarios públicos: el portal es institucional y las consultas van por el buzón (RN-03). */
add_filter('comments_open', '__return_false', PHP_INT_MAX);
add_filter('pings_open', '__return_false', PHP_INT_MAX);

/** Textos del tema sin traducir (falta el paquete de idioma de Blocksy): se cubren los que ve el visitante. */
add_filter('gettext', function ($traduccion, $original, $dominio) {
    static $es = [
        'Skip to content' => 'Saltar al contenido',
        "Oops! That page can't be found." => 'Vaya, no encontramos esa página',
        'Oops! That page can’t be found.' => 'Vaya, no encontramos esa página',
        'Oops! That page can&rsquo;t be found.' => 'Vaya, no encontramos esa página',
        'It looks like nothing was found at this location. Maybe try to search for something else?' => 'No hay nada en esta dirección. Prueba a buscar lo que necesitas o vuelve al inicio.',
        'Search' => 'Buscar',
        'Leave a Reply' => 'Deja un comentario',
        'Search Results for' => 'Resultados de la búsqueda de',
        'Nothing Found' => 'Sin resultados',
        'Read More' => 'Leer más',
    ];
    return $dominio === 'blocksy' && isset($es[$original]) ? $es[$original] : $traduccion;
}, 10, 3);
