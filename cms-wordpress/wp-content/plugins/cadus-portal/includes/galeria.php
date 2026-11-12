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
        ['sede-cadus', 'Fachada de la sede del CADUS, en el Pabellón de Uruguay, con el cartel del consejo.', 'Nuestra casa: el Pabellón de Uruguay'],
        ['plaza-de-espana', 'Grupo numeroso de estudiantes posando en la Plaza de España de Sevilla.', 'Encuentros de delegaciones'],
        ['asamblea-rectorado', 'Estudiantes reunidos frente al edificio histórico del Rectorado de la Universidad de Sevilla.', 'Asambleas ante el Rectorado'],
        ['multitud', 'Vista aérea de una multitud de estudiantes concentrados en una calle de Sevilla.', 'Cuando el alumnado se une'],
    ];
    // HU-20a: cada foto está ya recortada a 3:4 (como se muestra) en 360 y 720 px, en WebP y en JPEG para
    // navegadores antiguos (scripts/imagenes/optimizar_imagenes.py). El navegador elige el tamaño con «sizes»:
    // cuatro columnas en escritorio y dos en móvil. Ancho y alto fijos evitan saltos al cargar (CLS).
    $base = CADUS_PORTAL_URL . 'assets/fotos/';
    $sizes = '(max-width: 760px) 50vw, (max-width: 1240px) 25vw, 300px';
    $html = '<ul class="cadus-fotos">';
    foreach ($fotos as $i => [$archivo, $alt, $pie]) {
        $srcset = static fn(string $ext): string => esc_url($base . "{$archivo}-360.{$ext}") . ' 360w, ' . esc_url($base . "{$archivo}-720.{$ext}") . ' 720w';
        $html .= '<li class="cadus-foto" data-reveal style="--i:' . esc_attr((string) $i) . '"><figure><picture>'
            . '<source type="image/webp" srcset="' . $srcset('webp') . '" sizes="' . esc_attr($sizes) . '">'
            . '<img src="' . esc_url($base . $archivo . '-720.jpg') . '" srcset="' . $srcset('jpg') . '" sizes="' . esc_attr($sizes) . '"'
            . ' width="720" height="960" alt="' . esc_attr($alt) . '" loading="lazy" decoding="async">'
            . '</picture><figcaption>' . esc_html($pie) . '</figcaption></figure></li>';
    }
    return $html . '</ul>';
}
