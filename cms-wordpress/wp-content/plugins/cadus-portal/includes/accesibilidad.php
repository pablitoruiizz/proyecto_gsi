<?php
/**
 * Accesibilidad del portal: contraste, foco visible, teclado y enlace «Saltar al contenido» (HU-15a · RNF-03).
 *
 * Qué hace:
 *  - Carga assets/cadus-accesibilidad.css, después de cadus.css y cadus-interior.css, con las correcciones que dio la
 *    auditoría de contraste y foco (anillos de foco sobre fondos de color, campos de texto sin borde, enlaces del
 *    resultado del seguimiento) y el estilo del enlace «Saltar al contenido».
 *  - Carga assets/cadus-accesibilidad.js: al usar ese enlace el foco pasa al <main>.
 *  - Traduce los textos accesibles de la cabecera y del menú plegable de Blocksy que el lector de pantalla leería en
 *    inglés (falta el paquete de idioma del tema; estilo.php cubre otros textos y este filtro no los repite).
 *
 * Las comprobaciones y su resultado están en tests/HU-14a-HU-15a-portada.md.
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('wp_enqueue_scripts', function () {
    $css = CADUS_PORTAL_DIR . 'assets/cadus-accesibilidad.css';
    $js = CADUS_PORTAL_DIR . 'assets/cadus-accesibilidad.js';
    // Después de cadus-interior (que ya depende de cadus-portal): con la misma especificidad gana lo que se carga último.
    wp_enqueue_style('cadus-accesibilidad', CADUS_PORTAL_URL . 'assets/cadus-accesibilidad.css', ['cadus-interior'], (string) filemtime($css));
    wp_enqueue_script('cadus-accesibilidad', CADUS_PORTAL_URL . 'assets/cadus-accesibilidad.js', [], (string) filemtime($js), ['strategy' => 'defer', 'in_footer' => true]);
}, 30);

/** Textos de la cabecera y del menú plegable de Blocksy sin traducir que ve (u oye) el visitante. */
add_filter('gettext', function ($traduccion, $original, $dominio) {
    static $es = [
        'Menu' => 'Menú',
        'Close drawer' => 'Cerrar el menú',
        'Offcanvas modal' => 'Menú de navegación',
        'Expand dropdown menu' => 'Desplegar el submenú',
        'Search modal' => 'Búsqueda',
        'Close search modal' => 'Cerrar la búsqueda',
        'Go to top' => 'Volver al principio de la página',
    ];
    return $dominio === 'blocksy' && isset($es[$original]) ? $es[$original] : $traduccion;
}, 10, 3);
