<?php
/** Galería de la portada con fotos del propio CADUS (assets/fotos/). */

if (!defined('ABSPATH')) {
    exit;
}

add_shortcode('cadus_galeria', 'cadus_shortcode_galeria');

/** Fotos tomadas de cadus.us.es (propiedad del CADUS): confirmar su uso y la autorización de las personas que aparecen. */
function cadus_shortcode_galeria(): string
{
    $fotos = [
        ['sede-cadus', 1400, 933, 'Fachada de la sede del CADUS, en el Pabellón de Uruguay, con el cartel del consejo.', 'Nuestra casa: el Pabellón de Uruguay'],
        ['plaza-de-espana', 1280, 960, 'Grupo numeroso de estudiantes posando en la Plaza de España de Sevilla.', 'Encuentros de delegaciones'],
        ['asamblea-rectorado', 1280, 960, 'Estudiantes reunidos frente al edificio histórico del Rectorado de la Universidad de Sevilla.', 'Asambleas ante el Rectorado'],
        ['multitud', 1080, 1080, 'Vista aérea de una multitud de estudiantes concentrados en una calle de Sevilla.', 'Cuando el alumnado se une'],
    ];
    $html = '<ul class="cadus-fotos">';
    foreach ($fotos as $i => [$archivo, $ancho, $alto, $alt, $pie]) {
        $html .= '<li class="cadus-foto" data-reveal style="--i:' . esc_attr((string) $i) . '"><figure>'
            . '<img src="' . esc_url(CADUS_PORTAL_URL . 'assets/fotos/' . $archivo . '.jpg') . '" width="' . (int) $ancho . '" height="' . (int) $alto
            . '" alt="' . esc_attr($alt) . '" loading="lazy" decoding="async">'
            . '<figcaption>' . esc_html($pie) . '</figcaption></figure></li>';
    }
    return $html . '</ul>';
}
