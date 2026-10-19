<?php
/** Portada inmersiva: hero, accesos rápidos, buscador y pasos del buzón (Codex). */

if (!defined('ABSPATH')) {
    exit;
}

define('CADUS_INICIO_VERSION', '2');
add_action('init', 'cadus_actualizar_inicio', 20);
add_action('transition_post_status', 'cadus_inicio_cambio_estado', 10, 3);
add_action('deleted_post', 'cadus_inicio_borrado', 10, 2);
add_shortcode('cadus_hero', 'cadus_shortcode_hero');
add_shortcode('cadus_buscador', 'cadus_shortcode_buscador');
add_shortcode('cadus_accesos', 'cadus_shortcode_accesos');
add_shortcode('cadus_pasos', 'cadus_shortcode_pasos');

/** Cuenta solo publicaciones; nunca expone cifras de tickets ni borradores. */
function cadus_inicio_datos(): array
{
    $datos = get_transient('cadus_inicio_datos');
    if (is_array($datos)) {
        return $datos;
    }
    $datos = [];
    foreach (['cadus_acta', 'cadus_delegacion', 'post'] as $tipo) {
        $datos[$tipo] = (int) wp_count_posts($tipo)->publish;
    }
    set_transient('cadus_inicio_datos', $datos, 5 * MINUTE_IN_SECONDS);
    return $datos;
}

/** WordPress llama a este gancho también al guardar sin cambiar de estado. */
function cadus_inicio_cambio_estado(string $nuevo, string $anterior, WP_Post $post): void
{
    if (in_array($post->post_type, ['post', 'cadus_acta', 'cadus_delegacion'], true)) {
        delete_transient('cadus_inicio_datos');
    }
}

function cadus_inicio_borrado(int $id, WP_Post $post): void
{
    cadus_inicio_cambio_estado('', '', $post);
}

/** La marca de siembra permite resolver enlaces aunque se renombre una página. */
function cadus_inicio_url(string $ruta): string
{
    $pagina = cadus_buscar_semilla('pagina:' . $ruta, 'page') ?? get_page_by_path($ruta);
    return $pagina ? (string) get_permalink($pagina) : home_url('/' . $ruta . '/');
}

function cadus_shortcode_hero(): string
{
    $datos = cadus_inicio_datos();
    $html = '<section class="cadus-hero" data-cadus-hero aria-labelledby="cadus-hero-titulo">'
        . '<div class="cadus-hero__fondo" aria-hidden="true">';
    for ($i = 1; $i <= 3; $i++) {
        $html .= '<span class="cadus-hero__forma cadus-hero__forma--' . esc_attr((string) $i) . '"></span>';
    }
    $html .= '</div><div class="cadus-hero__contenido">'
        . '<p class="cadus-hero__etiqueta">' . esc_html('Consejo de Alumnos · Universidad de Sevilla') . '</p>'
        . '<h1 id="cadus-hero-titulo" class="cadus-hero__titulo">';
    foreach (['La voz del alumnado', 'de la Universidad de Sevilla'] as $linea) {
        $html .= '<span class="cadus-linea"><span class="cadus-linea__texto">' . esc_html($linea) . '</span></span> ';
    }
    $html .= '</h1><p class="cadus-hero__lema">' . esc_html('Consulta tus derechos, encuentra tu delegación y haznos llegar tus dudas.') . '</p>'
        . '<div class="cadus-hero__acciones"><a class="cadus-boton" href="'
        . esc_url(cadus_inicio_url('atencion-al-estudiante/buzon-de-consultas')) . '">' . esc_html('Enviar una consulta') . '</a>'
        . '<a class="cadus-boton cadus-boton--claro" href="' . esc_url(cadus_inicio_url('delegaciones')) . '">'
        . esc_html('Buscar mi delegación') . '</a></div><ul class="cadus-hero__datos">';
    foreach (['cadus_acta' => 'actas y normativas publicadas', 'cadus_delegacion' => 'delegaciones publicadas', 'post' => 'comunicados publicados'] as $tipo => $texto) {
        $html .= '<li><strong class="cadus-dato" data-cadus-contar="' . esc_attr((string) $datos[$tipo]) . '">'
            . esc_html((string) $datos[$tipo]) . '</strong> <span>' . esc_html($texto) . '</span></li>';
    }
    return $html . '</ul></div></section>';
}

/** La búsqueda nativa interpreta post_type vacío como todos los tipos buscables. */
function cadus_shortcode_buscador(): string
{
    $html = '<form class="cadus-buscador" role="search" method="get" action="' . esc_url(home_url('/')) . '">'
        . '<label class="screen-reader-text" for="cadus-q">' . esc_html('Buscar en el portal del CADUS') . '</label>'
        . '<input id="cadus-q" type="search" name="s" placeholder="' . esc_attr('Busca noticias, actas o tu delegación') . '" required>'
        . '<select name="post_type" aria-label="' . esc_attr('Dónde buscar') . '">';
    foreach (['' => 'Todo', 'post' => 'Comunicados', 'cadus_acta' => 'Actas y normativas', 'cadus_delegacion' => 'Delegaciones'] as $tipo => $texto) {
        $html .= '<option value="' . esc_attr($tipo) . '">' . esc_html($texto) . '</option>';
    }
    return $html . '</select><button class="cadus-boton" type="submit">' . esc_html('Buscar') . '</button></form>';
}

/** Iconos locales y decorativos; las etiquetas de las tarjetas dan el nombre accesible. */
function cadus_inicio_icono(string $nombre): string
{
    $trazos = [
        'comunicados' => '<path d="M3 10v4h4l10 5V5L7 10H3Zm4 4 2 7h3l-2-6M21 9v6"/>',
        'actas' => '<path d="M14 3H5v18h14V8l-5-5Zm0 0v5h5M8 12h8M8 16h8"/>',
        'delegaciones' => '<path d="M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
        'buzon' => '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
        'seguimiento' => '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        'calendario' => '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4M17 3v4M3 10h18m-14 5 3 3 6-5"/>',
    ];
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
        . ($trazos[$nombre] ?? '') . '</svg>';
}

function cadus_shortcode_accesos(): string
{
    $datos = cadus_inicio_datos();
    $accesos = [
        ['comunicados', 'noticias', 'Comunicados', 'Mantente al día de las novedades del CADUS.',
            sprintf(_n('%s comunicado', '%s comunicados', $datos['post'], 'cadus-portal'), $datos['post'])],
        ['actas', 'actas-y-normativa', 'Actas y normativa', 'Consulta los acuerdos y descarga la normativa.',
            sprintf(_n('%s documento', '%s documentos', $datos['cadus_acta'], 'cadus-portal'), $datos['cadus_acta'])],
        ['delegaciones', 'delegaciones', 'Delegaciones', 'Encuentra a los representantes de tu centro.',
            sprintf(_n('%s delegación', '%s delegaciones', $datos['cadus_delegacion'], 'cadus-portal'), $datos['cadus_delegacion'])],
        ['buzon', 'atencion-al-estudiante/buzon-de-consultas', 'Buzón de consultas', 'Envía tus dudas o reclamaciones académicas.', 'Con tu correo @alum.us.es'],
        ['seguimiento', 'atencion-al-estudiante/seguimiento-de-ticket', 'Seguimiento de ticket', 'Consulta el estado y las respuestas a tu solicitud.', 'Con tu código y correo'],
        ['calendario', '', 'Calendario y votaciones', 'Asambleas, eventos y participación estudiantil.', 'En preparación'],
    ];
    $html = '<ul class="cadus-accesos">';
    foreach ($accesos as $i => [$icono, $ruta, $titulo, $texto, $meta]) {
        $html .= '<li class="cadus-acceso' . ($ruta === '' ? ' cadus-acceso--pronto' : '') . '"'
            . ($ruta === '' ? ' aria-disabled="true"' : '') . ' data-reveal style="--i:' . esc_attr((string) $i) . '">';
        if ($ruta !== '') {
            $html .= '<a class="cadus-acceso__enlace" href="' . esc_url(cadus_inicio_url($ruta)) . '">';
        } else {
            $html .= '<span class="cadus-acceso__etiqueta">' . esc_html('Próximamente') . '</span>';
        }
        $html .= '<span class="cadus-acceso__icono">' . cadus_inicio_icono($icono) . '</span>'
            . '<span class="cadus-acceso__titulo">' . esc_html($titulo) . '</span>'
            . '<span class="cadus-acceso__texto">' . esc_html($texto) . '</span>'
            . '<span class="cadus-acceso__meta">' . esc_html($meta) . '</span>';
        $html .= ($ruta !== '' ? '</a>' : '') . '</li>';
    }
    return $html . '</ul>';
}

function cadus_shortcode_pasos(): string
{
    $html = '<section class="cadus-seccion cadus-seccion--pasos"><h2 class="cadus-seccion__titulo" data-reveal>'
        . esc_html('Cómo funciona el buzón') . '</h2><ol class="cadus-pasos">';
    $pasos = [
        ['Escribe tu consulta', 'Cuéntanos tu duda o reclamación con tu correo @alum.us.es.'],
        ['Recibe tu código de seguimiento', 'Al enviar la consulta verás tu código CAD-AAAA-NNNNN. Guárdalo para seguir tu solicitud.'],
        ['Consulta el estado cuando quieras', 'Introduce tu código y tu correo en Seguimiento de ticket para ver el estado y las respuestas.'],
    ];
    foreach ($pasos as $i => [$titulo, $texto]) {
        $html .= '<li class="cadus-paso" data-reveal style="--i:' . esc_attr((string) $i) . '">'
            . '<span class="cadus-paso__numero">' . esc_html((string) ($i + 1)) . '</span>'
            . '<h3 class="cadus-paso__titulo">' . esc_html($titulo) . '</h3><p>' . esc_html($texto) . '</p></li>';
    }
    return $html . '</ol><a class="cadus-boton" href="' . esc_url(cadus_inicio_url('atencion-al-estudiante/buzon-de-consultas')) . '">'
        . esc_html('Enviar una consulta') . '</a></section>';
}

/** Un grupo semántico mantiene los bloques editables sin partir etiquetas HTML entre bloques. */
function cadus_inicio_seccion(string $titulo, string $shortcode, string $variante = ''): string
{
    $clases = trim('cadus-seccion ' . $variante);
    return '<!-- wp:group {"tagName":"section","className":"' . $clases . '"} -->' . "\n"
        . '<section class="wp-block-group ' . $clases . '">' . "\n"
        . cadus_b_html('<h2 class="cadus-seccion__titulo" data-reveal>' . esc_html($titulo) . '</h2>')
        . cadus_b_sc($shortcode) . "</section>\n<!-- /wp:group -->\n\n";
}

/** Contenido de la portada: cada sección lleva su variante de color como clase (sin depender de :has()). */
function cadus_inicio_contenido(): string
{
    return cadus_b_sc('[cadus_hero]')
        . cadus_b_sc('[cadus_intro]')
        . cadus_inicio_seccion('Todo lo que necesitas', '[cadus_accesos]', 'cadus-seccion--accesos')
        . cadus_b_sc('[cadus_novedades]')
        . cadus_b_sc('[cadus_eventos]')
        . cadus_b_sc('[cadus_trabajo]')
        . cadus_inicio_seccion('Así se vive el CADUS', '[cadus_galeria]', 'cadus-seccion--galeria')
        . cadus_inicio_seccion('Encuentra rápido lo que buscas', '[cadus_buscador]', 'cadus-seccion--buscador')
        . cadus_b_sc('[cadus_pasos]')
        . cadus_b_sc('[cadus_contacto]');
}

/** Reconoce únicamente las plantillas anteriores completas, sin bloques ni textos añadidos. */
function cadus_inicio_es_plantilla_anterior(string $contenido): bool
{
    foreach (['cadus_intro', 'cadus_novedades', 'cadus_eventos', 'cadus_trabajo', 'cadus_contacto'] as $shortcode) {
        if (has_shortcode($contenido, $shortcode)) {
            return false;
        }
    }
    if (has_shortcode($contenido, 'cadus_hero') && has_shortcode($contenido, 'cadus_pasos')) {
        $anterior = cadus_b_sc('[cadus_hero]')
            . cadus_inicio_seccion('Todo lo que necesitas', '[cadus_accesos]', 'cadus-seccion--accesos')
            . cadus_inicio_seccion('Así se vive el CADUS', '[cadus_galeria]', 'cadus-seccion--galeria')
            . cadus_inicio_seccion('Encuentra rápido lo que buscas', '[cadus_buscador]', 'cadus-seccion--buscador')
            . cadus_inicio_seccion('Comunicados recientes', '[cadus_ultimas_noticias n="3"]', 'cadus-seccion--noticias')
            . cadus_b_sc('[cadus_pasos]');
    } else {
        // Siembra original de setup.php: permite instalar desde cero sin aceptar cualquier cadus-banner.
        $anterior = cadus_b_html('<div class="cadus-banner"><h1>CADUS</h1><p>Consejo de Alumnos de la Universidad de Sevilla</p>'
                . '<a class="cadus-boton" href="' . esc_url(home_url('/delegaciones/')) . '">Delegaciones de alumnos</a>'
                . '<a class="cadus-boton" href="' . esc_url(home_url('/atencion-al-estudiante/buzon-de-consultas/')) . '">Buzón de consultas</a></div>')
            . cadus_b_h('Comunicados recientes')
            . cadus_b_sc('[cadus_ultimas_noticias n="3"]')
            . cadus_b_h('Participación estudiantil')
            . cadus_b_p('El calendario de asambleas, eventos y votaciones se publicará en la próxima versión del portal.');
    }
    // Gutenberg puede serializar -- como \u002d\u002d en el JSON. Se comparan todos los bloques,
    // atributos y HTML, admitiendo solo esa representación equivalente, no ediciones del equipo.
    return parse_blocks($contenido) === parse_blocks($anterior);
}

/** Migra también instalaciones nuevas en el primer init posterior a la siembra. */
function cadus_actualizar_inicio(): void
{
    if (get_option('cadus_inicio_version') === CADUS_INICIO_VERSION) {
        return;
    }
    $pagina = cadus_buscar_semilla('pagina:inicio', 'page') ?? get_page_by_path('inicio');
    if (!$pagina) {
        return;
    }
    $hash = get_option('cadus_inicio_contenido_hash', '');
    $es_generado = is_string($hash) && $hash !== ''
        ? hash_equals($hash, hash('sha256', $pagina->post_content))
        : cadus_inicio_es_plantilla_anterior($pagina->post_content);
    if (!$es_generado) {
        error_log('CADUS: portada conservada porque el equipo ya ha editado su contenido.');
        update_option('cadus_inicio_version', CADUS_INICIO_VERSION);
        return;
    }
    $contenido = cadus_inicio_contenido();
    $resultado = wp_update_post(['ID' => $pagina->ID, 'post_content' => wp_slash($contenido)], true);
    if (is_wp_error($resultado) || !$resultado) {
        error_log('CADUS: no se pudo actualizar la portada; se reintentará en la siguiente petición.');
        return;
    }
    // Se guarda lo realmente persistido, tras los filtros de WordPress al escribir.
    update_option('cadus_inicio_contenido_hash', hash('sha256', (string) get_post_field('post_content', $pagina->ID, 'raw')));
    update_option('cadus_inicio_version', CADUS_INICIO_VERSION);
}
