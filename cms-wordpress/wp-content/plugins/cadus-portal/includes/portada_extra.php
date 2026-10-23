<?php
/** Secciones de la portada: presentación, noticias, eventos, trabajo y contacto. */

if (!defined('ABSPATH')) {
    exit;
}

add_shortcode('cadus_intro', 'cadus_shortcode_intro');
add_shortcode('cadus_novedades', 'cadus_shortcode_novedades');
add_shortcode('cadus_eventos', 'cadus_shortcode_eventos');
add_shortcode('cadus_trabajo', 'cadus_shortcode_trabajo');
add_shortcode('cadus_contacto', 'cadus_shortcode_contacto');
add_action('blocksy:footer:before', 'cadus_pie_global');
add_action('wp_footer', 'cadus_pie_global', 5);
add_action('transition_post_status', 'cadus_portada_cambio_estado', 10, 3);
add_action('deleted_post', 'cadus_portada_post_borrado', 10, 2);
add_action('set_object_terms', 'cadus_portada_cambio_relaciones', 10, 4);
add_action('deleted_term_relationships', 'cadus_portada_cambio_relaciones', 10, 3);
add_action('created_term', 'cadus_portada_cambio_categoria', 10, 3);
add_action('edited_term', 'cadus_portada_cambio_categoria', 10, 3);
add_action('delete_term', 'cadus_portada_cambio_categoria', 10, 3);
add_action('edited_term_taxonomy', 'cadus_portada_cambio_recuento', 10, 2);

function cadus_portada_invalidar_cache(): void
{
    delete_transient('cadus_portada_datos');
}

/** También se ejecuta al guardar una entrada sin cambiar su estado. */
function cadus_portada_cambio_estado(string $nuevo, string $anterior, WP_Post $post): void
{
    if ($post->post_type === 'post') {
        cadus_portada_invalidar_cache();
    }
}

function cadus_portada_post_borrado(int $id, WP_Post $post): void
{
    cadus_portada_cambio_estado('', '', $post);
}

/** Los dos ganchos de relaciones sitúan la taxonomía en argumentos distintos. */
function cadus_portada_cambio_relaciones($objeto, $terminos, $tercero, $taxonomia = null): void
{
    if (($taxonomia ?? $tercero) === 'category') {
        cadus_portada_invalidar_cache();
    }
}

function cadus_portada_cambio_categoria($term_id, $tt_id, string $taxonomia): void
{
    if ($taxonomia === 'category') {
        cadus_portada_invalidar_cache();
    }
}

function cadus_portada_cambio_recuento($tt_id, string $taxonomia): void
{
    if ($taxonomia === 'category') {
        cadus_portada_invalidar_cache();
    }
}

/** Origen de los eventos de la portada (HU-10).
 * Con The Events Calendar activo se muestran los próximos eventos del calendario (calendario.php).
 * Sin él, se usan las entradas de la categoría Eventos con su fecha de publicación, como en el Sprint 1.
 * Devuelve datos de presentación para que el marcado no dependa del tipo de calendario.
 * @return array<int, array{titulo: string, url: string, fecha: string}>
 */
function cadus_eventos_origen(): array
{
    if (function_exists('cadus_calendario_activo') && cadus_calendario_activo()) {
        return cadus_calendario_eventos(4);
    }
    $categoria = get_term_by('slug', 'eventos', 'category') ?: get_term_by('name', 'Eventos', 'category');
    if (!$categoria) {
        return [];
    }
    $entradas = get_posts([
        'post_type' => 'post', 'post_status' => 'publish', 'has_password' => false,
        'posts_per_page' => 4, 'orderby' => ['date' => 'DESC', 'ID' => 'DESC'],
        'ignore_sticky_posts' => true, 'no_found_rows' => true,
        'tax_query' => [[
            'taxonomy' => 'category', 'field' => 'term_id', 'terms' => [(int) $categoria->term_id],
            'include_children' => false,
        ]],
    ]);
    return array_map(static function (WP_Post $post): array {
        return [
            'titulo' => get_the_title($post),
            'url' => (string) get_permalink($post),
            'fecha' => get_the_date('Y-m-d', $post),
        ];
    }, $entradas);
}

/** Solo entradas publicadas; nunca consulta tickets, borradores ni contenido protegido. */
function cadus_portada_datos(): array
{
    $datos = get_transient('cadus_portada_datos');
    if (is_array($datos)) {
        return $datos;
    }
    $datos = [
        'noticias' => get_posts([
            'post_type' => 'post', 'post_status' => 'publish', 'has_password' => false,
            'posts_per_page' => 8, 'orderby' => ['date' => 'DESC', 'ID' => 'DESC'],
            'ignore_sticky_posts' => true, 'no_found_rows' => true,
        ]),
        'categorias' => get_categories(['hide_empty' => true, 'orderby' => 'name', 'order' => 'ASC']),
        'eventos' => cadus_eventos_origen(),
    ];
    set_transient('cadus_portada_datos', $datos, 5 * MINUTE_IN_SECONDS);
    return $datos;
}

function cadus_shortcode_intro(): string
{
    $texto = 'Con más de 40 años de historia, es el interlocutor del estudiantado ante los sectores universitarios y, por supuesto, por la participación activa del estudiantado, buscando siempre la mejora de la calidad de la enseñanza y el reconocimiento de sus derechos como integrantes de la comunidad universitaria hispalense.';
    return '<section class="cadus-seccion cadus-seccion--intro" aria-labelledby="cadus-intro-titulo"><div class="cadus-intro">'
        . '<p class="cadus-intro__numero" aria-hidden="true">' . esc_html('40') . '</p><div class="cadus-intro__texto">'
        . '<h2 id="cadus-intro-titulo" class="cadus-seccion__titulo" data-reveal>' . esc_html('Más de 40 años dando voz al alumnado') . '</h2>'
        . '<p class="cadus-intro__parrafo" data-reveal>' . esc_html($texto) . '</p>'
        . '<a class="cadus-boton" href="' . esc_url(cadus_inicio_url('que-es-el-cadus')) . '">' . esc_html('Saber más') . '</a>'
        . '</div></div></section>';
}

function cadus_shortcode_novedades(): string
{
    $datos = cadus_portada_datos();
    $html = '<section class="cadus-seccion cadus-seccion--novedades"><h2 class="cadus-seccion__titulo" data-reveal>'
        . esc_html('¡Últimas noticias!') . '</h2>'
        . '<div class="cadus-filtros" data-cadus-filtros hidden role="group" aria-label="' . esc_attr('Filtrar por categoría') . '">'
        . '<button class="cadus-chip" type="button" data-cadus-filtro="todo" aria-pressed="true">' . esc_html('Todo') . '</button>';
    foreach ($datos['categorias'] as $categoria) {
        $html .= '<button class="cadus-chip" type="button" data-cadus-filtro="' . esc_attr($categoria->slug) . '" aria-pressed="false">'
            . esc_html($categoria->name) . '</button>';
    }
    $html .= '</div><div class="cadus-carrusel" data-cadus-carrusel><ul class="cadus-carrusel__pista" tabindex="0" aria-label="'
        . esc_attr('Noticias recientes') . '">';
    foreach ($datos['noticias'] as $i => $post) {
        $categorias = get_the_category($post->ID);
        $url = get_permalink($post);
        $titulo = get_the_title($post);
        $resumen = wp_trim_words(wp_strip_all_tags(strip_shortcodes($post->post_excerpt !== '' ? $post->post_excerpt : $post->post_content)), 22, '…');
        $html .= '<li class="cadus-noticia" data-cadus-categorias="' . esc_attr(implode(' ', wp_list_pluck($categorias, 'slug')))
            . '" data-reveal style="--i:' . esc_attr((string) $i) . '"><article><p class="cadus-noticia__meta">'
            . '<time class="cadus-noticia__fecha" datetime="' . esc_attr(get_the_date('Y-m-d', $post)) . '">'
            . esc_html(get_the_date('d-m-Y', $post)) . '</time> <span class="cadus-noticia__cat">'
            . esc_html(implode(', ', wp_list_pluck($categorias, 'name'))) . '</span></p>'
            . '<h3 class="cadus-noticia__titulo"><a href="' . esc_url($url) . '">' . esc_html($titulo) . '</a></h3>'
            . '<p class="cadus-noticia__texto">' . esc_html($resumen) . '</p>'
            . '<a class="cadus-noticia__enlace" href="' . esc_url($url) . '">' . esc_html('¡Quiero saber más!')
            . '<span class="screen-reader-text">' . esc_html(': ' . $titulo) . '</span></a></article></li>';
    }
    $html .= '</ul><div class="cadus-carrusel__mandos" data-cadus-mandos hidden>'
        . '<button class="cadus-carrusel__ant" type="button" aria-label="' . esc_attr('Noticias anteriores') . '">' . esc_html('←') . '</button>'
        . '<button class="cadus-carrusel__sig" type="button" aria-label="' . esc_attr('Noticias siguientes') . '">' . esc_html('→') . '</button></div></div>';
    if (!$datos['noticias']) {
        $html .= '<p>' . esc_html('Pronto publicaremos nuevas noticias.') . '</p>';
    }
    return $html . '<a class="cadus-boton cadus-boton--claro" href="' . esc_url(cadus_inicio_url('noticias')) . '">'
        . esc_html('Ver todas las noticias') . '</a></section>';
}

function cadus_shortcode_eventos(): string
{
    $eventos = cadus_portada_datos()['eventos'];
    $html = '<section class="cadus-seccion cadus-seccion--eventos"><h2 class="cadus-seccion__titulo" data-reveal>'
        . esc_html('¡Últimos eventos!') . '</h2>';
    if (!$eventos) {
        return $html . '<p class="cadus-evento__vacio">' . esc_html('Pronto publicaremos los próximos eventos.') . '</p></section>';
    }
    $meses = [1 => 'ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
    $html .= '<ul class="cadus-eventos">';
    foreach ($eventos as $i => $evento) {
        $html .= '<li class="cadus-evento" data-reveal style="--i:' . esc_attr((string) $i) . '">'
            . '<a class="cadus-evento__enlace" href="' . esc_url($evento['url']) . '">'
            . '<time class="cadus-evento__fecha" datetime="' . esc_attr($evento['fecha']) . '">'
            . '<span class="cadus-evento__dia">' . esc_html(substr($evento['fecha'], 8, 2)) . '</span>'
            . '<span class="cadus-evento__mes">' . esc_html($meses[(int) substr($evento['fecha'], 5, 2)]) . '</span></time>'
            . '<span class="cadus-evento__titulo">' . esc_html($evento['titulo']) . '</span>'
            . '<span class="cadus-evento__ver">' . esc_html('Ver más') . '</span></a></li>';
    }
    return $html . '</ul></section>';
}

function cadus_shortcode_trabajo(): string
{
    // Textos de la web oficial: deben revisarse con el CADUS, especialmente los objetivos fechados.
    $areas = [
        ['Política Universitaria', [
            'Reforma de los estatutos de la US', 'Garantizar que se mantengan los derechos de los estudiantes',
            'Implementar mistral', 'Modificación del RFCADUS', 'Mejorar la situación de los dobles grados',
        ], 'actas-y-normativa', 'Ver actas y normativa'],
        ['Vida Universitaria', [
            'Organizar II Encuentro de las Delegaciones de la US', 'I Plan VU del CADUS', 'Aumentar la participación estudiantil',
            'Campaña Orgullo 2024', 'Organizar IV Jornadas de Formación del CADUS',
        ], 'noticias', 'Ver noticias'],
        ['Comunicación', ['Llevar las RRSS', 'Generar contenido para RRSS', 'Generar contenido para las campañas'], '', ''],
        ['Gerencia', ['Reformar la web del CADUS'], '', ''],
    ];
    $html = '<section class="cadus-seccion cadus-seccion--trabajo"><h2 class="cadus-seccion__titulo" data-reveal>'
        . esc_html('Nuestro trabajo') . '</h2><div class="cadus-trabajo">';
    foreach ($areas as $i => [$titulo, $objetivos, $ruta, $boton]) {
        $html .= '<article class="cadus-lista" data-reveal style="--i:' . esc_attr((string) $i) . '"><h3 class="cadus-lista__titulo">'
            . esc_html($titulo) . '</h3><ul class="cadus-lista__items">';
        foreach ($objetivos as $objetivo) {
            $html .= '<li>' . esc_html($objetivo) . '</li>';
        }
        $html .= '</ul>';
        if ($ruta !== '') {
            $html .= '<a class="cadus-boton" href="' . esc_url(cadus_inicio_url($ruta)) . '">' . esc_html($boton) . '</a>';
        }
        $html .= '</article>';
    }
    return $html . '</div></section>';
}

/** Pie fuera del main de Blocksy; wp_footer sirve de alternativa en otras plantillas. */
function cadus_pie_global(): void
{
    if (is_admin() || is_feed() || is_embed() || wp_doing_ajax()
        || (defined('REST_REQUEST') && REST_REQUEST) || !empty($GLOBALS['cadus_contacto_mostrado'])) {
        return;
    }
    $pagina = is_singular() ? get_queried_object() : null;
    if ($pagina instanceof WP_Post && has_shortcode($pagina->post_content, 'cadus_hero')) {
        return;
    }
    echo '<footer class="cadus-pie-global" aria-label="Contacto del CADUS">'
        . do_shortcode('[cadus_contacto]') . '</footer>';
}

function cadus_shortcode_contacto(): string
{
    // No insertar el cierre visual del sitio en canales de datos ni en administración.
    if (is_admin() || is_feed() || wp_doing_ajax() || (defined('REST_REQUEST') && REST_REQUEST)) {
        return '';
    }
    $GLOBALS['cadus_contacto_mostrado'] = true;
    $enlaces = [
        ['CADUS', cadus_inicio_url('que-es-el-cadus'), false],
        ['MIC', 'https://www.cadus.us.es/manual-basico-de-identidad-visual-corporativa/', true],
        ['Glosario', 'https://www.cadus.us.es/glosario/', true],
        ['Finger Rules', 'https://www.cadus.us.es/finger-rules/', true],
        ['Política de datos', 'https://www.cadus.us.es/politica-de-proteccion-y-tratamiento-de-datos/', true],
        ['Incidencias', cadus_inicio_url('atencion-al-estudiante/buzon-de-consultas'), false],
    ];
    $html = '<section class="cadus-seccion cadus-seccion--contacto" aria-labelledby="cadus-contacto-titulo">'
        . '<p class="cadus-contacto__marca" aria-hidden="true">' . esc_html('CADUS') . '</p>'
        . '<h2 id="cadus-contacto-titulo" class="cadus-seccion__titulo">' . esc_html('Consejo de Alumnos de la Universidad de Sevilla') . '</h2>'
        . '<div class="cadus-contacto"><address class="cadus-contacto__datos">'
        . '<span class="cadus-contacto__linea">' . esc_html('Av. de Chile s/n, 41013 Sevilla') . '</span>'
        . '<a href="' . esc_url('tel:954486022') . '">' . esc_html('954 48 60 22') . '</a>'
        . '<a href="' . esc_url('mailto:dcadus@us.es') . '">' . esc_html('dcadus@us.es') . '</a>'
        . '<a href="' . esc_url('https://www.instagram.com/igcadus/') . '" rel="noopener">' . esc_html('Instagram @igcadus') . '</a>'
        . '</address><ul class="cadus-contacto__enlaces">';
    foreach ($enlaces as [$texto, $url, $externo]) {
        $html .= '<li><a href="' . esc_url($url) . '"' . ($externo ? ' rel="noopener"' : '') . '>'
            . esc_html($texto . ($externo ? ' (web oficial del CADUS)' : '')) . '</a></li>';
    }
    // Blocksy coloca main-container antes de su cabecera: destino real, incluso sin JavaScript.
    return $html . '</ul></div><p class="cadus-contacto__legal">' . esc_html('© ' . wp_date('Y') . ' CADUS')
        . ' <a class="cadus-contacto__subir" href="#main-container">' . esc_html('Subir ↑') . '</a></p></section>';
}
