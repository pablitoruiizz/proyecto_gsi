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
    wp_enqueue_script('cadus-portal', CADUS_PORTAL_URL . 'assets/cadus.js', [], (string) filemtime($js), ['strategy' => 'defer', 'in_footer' => true]);
}, 20);
