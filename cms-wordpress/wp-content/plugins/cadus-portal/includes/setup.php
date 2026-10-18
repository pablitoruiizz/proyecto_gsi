<?php
/**
 * Configuración inicial del sitio: páginas, menú, noticias, tema e identidad visual.
 * Trazabilidad: HU-01, HU-02, HU-18 · RF-01, RF-02 · UI-01, UI-02 · IR-01, IR-02, IR-03.
 *
 * Todo es idempotente: se puede ejecutar varias veces sin duplicar contenido ni pisar lo que el equipo haya editado.
 * Los textos de ejemplo están marcados como tales y deben sustituirse por contenido real validado con el cliente.
 */

if (!defined('ABSPATH')) {
    exit;
}

add_shortcode('cadus_ultimas_noticias', 'cadus_shortcode_ultimas');
add_shortcode('cadus_noticias', 'cadus_shortcode_noticias');
add_action('wp_head', 'cadus_estilos');

/* ----------------------------------------------------------------- estilos y shortcodes */

function cadus_estilos(): void
{
    echo '<style id="cadus-portal">'
        . '.cadus-banner{background:#1f3a5f;color:#fff;padding:56px 24px;border-radius:10px;text-align:center;margin-bottom:32px}'
        . '.cadus-banner h1{color:#fff;margin:0 0 12px}.cadus-banner p{margin:0 0 20px;font-size:1.1em}'
        . '.cadus-boton{display:inline-block;background:#f2b705;color:#1f3a5f!important;padding:10px 22px;border-radius:6px;font-weight:700;text-decoration:none;margin:4px}'
        . '.cadus-tarjetas{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;margin:24px 0}'
        . '.cadus-tarjeta{border:1px solid #d6dde6;border-radius:8px;padding:18px;background:#fff}'
        . '.cadus-tarjeta h3{margin-top:0}.cadus-meta{color:#5a6a7e;font-size:.9em}'
        . '.cadus-tabla{width:100%;border-collapse:collapse}.cadus-tabla th,.cadus-tabla td{border-bottom:1px solid #d6dde6;padding:8px;text-align:left}'
        . '.cadus-tabla th{background:#f2f5f7}.cadus-ficha{list-style:none;padding-left:0}'
        . '.cadus-filtros{display:flex;flex-wrap:wrap;gap:8px;align-items:end;margin-bottom:20px}'
        . '.cadus-aviso{background:#fff8e1;border-left:4px solid #f2b705;padding:10px 14px;margin:16px 0}'
        . '</style>';
}

function cadus_tarjeta_noticia(WP_Post $p): string
{
    $cats = get_the_category($p->ID);
    $nombres = $cats ? implode(', ', wp_list_pluck($cats, 'name')) : 'Sin categoría';
    return '<article class="cadus-tarjeta"><div class="cadus-meta">' . esc_html(get_the_date('d/m/Y', $p)) . ' · ' . esc_html($nombres) . '</div>'
        . '<h3><a href="' . esc_url(get_permalink($p)) . '">' . esc_html(get_the_title($p)) . '</a></h3>'
        . '<p>' . esc_html(wp_trim_words(get_the_excerpt($p), 28)) . '</p></article>';
}

/** [cadus_ultimas_noticias n="3"]: comunicados recientes para la portada (HU-01). */
function cadus_shortcode_ultimas($atts): string
{
    $n = max(1, min(12, (int) (shortcode_atts(['n' => 3], $atts)['n'])));
    $posts = get_posts(['numberposts' => $n, 'post_status' => 'publish']);
    if (!$posts) {
        return '<p>Todavía no hay comunicados publicados.</p>';
    }
    return '<div class="cadus-tarjetas">' . implode('', array_map('cadus_tarjeta_noticia', $posts)) . '</div>';
}

/** [cadus_noticias]: listado con filtro por categoría, año y palabra clave (HU-02, RF-02). */
function cadus_shortcode_noticias(): string
{
    $q = isset($_GET['q']) ? sanitize_text_field(wp_unslash($_GET['q'])) : '';
    $cat = isset($_GET['cat']) ? absint($_GET['cat']) : 0;
    $anio = isset($_GET['anio']) ? absint($_GET['anio']) : 0;
    $pag = isset($_GET['pag']) ? max(1, absint($_GET['pag'])) : 1;
    $args = ['post_type' => 'post', 'post_status' => 'publish', 'posts_per_page' => 6, 'paged' => $pag];
    if ($q !== '') {
        $args['s'] = $q;
    }
    if ($cat) {
        $args['cat'] = $cat;
    }
    if ($anio) {
        $args['year'] = $anio;
    }
    $consulta = new WP_Query($args);
    $base = get_permalink();
    $opciones = '<option value="0">Todas las categorías</option>';
    foreach (get_categories(['hide_empty' => false]) as $c) {
        $opciones .= '<option value="' . (int) $c->term_id . '"' . selected($cat, $c->term_id, false) . '>' . esc_html($c->name) . '</option>';
    }
    $anios = '<option value="0">Todos los años</option>';
    for ($a = (int) gmdate('Y'); $a >= (int) gmdate('Y') - 5; $a--) {
        $anios .= '<option value="' . $a . '"' . selected($anio, $a, false) . '>' . $a . '</option>';
    }
    $html = '<form class="cadus-filtros" method="get" action="' . esc_url($base) . '" role="search" aria-label="Filtrar noticias">'
        . '<label>Palabra clave<br><input type="search" name="q" value="' . esc_attr($q) . '"></label>'
        . '<label>Categoría<br><select name="cat">' . $opciones . '</select></label>'
        . '<label>Año<br><select name="anio">' . $anios . '</select></label>'
        . '<button type="submit" class="cadus-boton">Filtrar</button></form>';
    if (!$consulta->have_posts()) {
        return $html . '<p>No hay comunicados que coincidan con el filtro.</p>';
    }
    $html .= '<div class="cadus-tarjetas">';
    foreach ($consulta->posts as $p) {
        $html .= cadus_tarjeta_noticia($p);
    }
    $html .= '</div>';
    $paginas = paginate_links([
        'base' => esc_url_raw(add_query_arg('pag', '%#%', $base)), 'format' => '', 'current' => $pag, 'total' => max(1, (int) $consulta->max_num_pages),
        'add_args' => array_filter(['q' => $q, 'cat' => $cat ?: null, 'anio' => $anio ?: null]),
    ]);
    return $html . ($paginas ? '<nav class="cadus-paginacion">' . $paginas . '</nav>' : '');
}

/* ----------------------------------------------------------------- utilidades de contenido */

function cadus_b_html(string $html): string { return "<!-- wp:html -->\n" . $html . "\n<!-- /wp:html -->\n\n"; }
function cadus_b_p(string $t): string { return "<!-- wp:paragraph -->\n<p>" . $t . "</p>\n<!-- /wp:paragraph -->\n\n"; }
function cadus_b_h(string $t, int $n = 2): string { return '<!-- wp:heading {"level":' . $n . "} -->\n<h{$n} class=\"wp-block-heading\">" . $t . "</h{$n}>\n<!-- /wp:heading -->\n\n"; }
function cadus_b_sc(string $sc): string { return "<!-- wp:shortcode -->\n" . $sc . "\n<!-- /wp:shortcode -->\n\n"; }


/** Busca un contenido por título exacto y tipo (sustituye a get_page_by_title, obsoleta). */
function cadus_post_por_titulo(string $titulo, string $tipo): ?WP_Post
{
    $q = new WP_Query(['post_type' => $tipo, 'title' => $titulo, 'post_status' => 'any', 'posts_per_page' => 1, 'no_found_rows' => true]);
    return $q->have_posts() ? $q->posts[0] : null;
}

/** Busca contenido sembrado por su marca estable; si no la tiene, lo localiza por título y se la añade. */
function cadus_buscar_semilla(string $clave, string $tipo, string $titulo = ''): ?WP_Post
{
    $q = new WP_Query(['post_type' => $tipo, 'post_status' => 'any', 'meta_key' => '_cadus_semilla', 'meta_value' => $clave,
        'posts_per_page' => 1, 'no_found_rows' => true]);
    if ($q->have_posts()) {
        return $q->posts[0];
    }
    if ($titulo !== '') {
        $p = cadus_post_por_titulo($titulo, $tipo);
        if ($p) {
            update_post_meta($p->ID, '_cadus_semilla', $clave);
            return $p;
        }
    }
    return null;
}

/** Crea una página si no existe (por ruta) y devuelve su ID. No sobrescribe páginas existentes. */
function cadus_pagina(string $slug, string $titulo, string $contenido, int $padre = 0): int
{
    $ruta = $padre ? get_page_uri($padre) . '/' . $slug : $slug;
    $existente = cadus_buscar_semilla('pagina:' . $ruta, 'page') ?? get_page_by_path($ruta);
    if ($existente) {
        update_post_meta($existente->ID, '_cadus_semilla', 'pagina:' . $ruta);
        return (int) $existente->ID;
    }
    $id = (int) wp_insert_post([
        'post_type' => 'page', 'post_status' => 'publish', 'post_title' => $titulo, 'post_name' => $slug,
        'post_content' => $contenido, 'post_parent' => $padre, 'post_author' => 1,
    ]);
    if ($id) {
        update_post_meta($id, '_cadus_semilla', 'pagina:' . $ruta);
    }
    return $id;
}

/** Copia un archivo del plugin a la biblioteca de medios y devuelve el ID del adjunto. */
function cadus_adjuntar(string $archivo_relativo, string $titulo): int
{
    require_once ABSPATH . 'wp-admin/includes/file.php';
    require_once ABSPATH . 'wp-admin/includes/media.php';
    require_once ABSPATH . 'wp-admin/includes/image.php';
    $existentes = get_posts(['post_type' => 'attachment', 'post_status' => 'inherit', 'title' => $titulo, 'numberposts' => 1]);
    if ($existentes) {
        return (int) $existentes[0]->ID;
    }
    $origen = CADUS_PORTAL_DIR . $archivo_relativo;
    if (!is_readable($origen)) {
        return 0;
    }
    $bits = wp_upload_bits(basename($origen), null, (string) file_get_contents($origen));
    if (!empty($bits['error'])) {
        return 0;
    }
    $tipo = wp_check_filetype($bits['file']);
    $id = wp_insert_attachment(['post_mime_type' => $tipo['type'], 'post_title' => $titulo, 'post_status' => 'inherit'], $bits['file']);
    if (!is_wp_error($id)) {
        wp_update_attachment_metadata($id, wp_generate_attachment_metadata($id, $bits['file']));
        return (int) $id;
    }
    return 0;
}

/* ----------------------------------------------------------------- activación */

/** Enlaces permanentes por nombre; se fijan antes de registrar los tipos de contenido para que sus URL no arrastren el prefijo anterior. */
function cadus_fijar_enlaces(): void
{
    global $wp_rewrite;
    if (!get_option('cadus_portal_version') && get_option('permalink_structure') !== '/%postname%/') {
        $wp_rewrite->set_permalink_structure('/%postname%/');
    }
}

function cadus_portal_activar(): void
{
    cadus_registrar_roles();
    cadus_fijar_enlaces();
    cadus_registrar_contenidos();
    cadus_portal_configurar();
    flush_rewrite_rules();
}

function cadus_portal_configurar(): void
{
    // Identidad y portada: solo en la primera activación, para no pisar lo que el equipo cambie después.
    $primera = !get_option('cadus_portal_version');

    // Taxonomías base
    foreach (['Becas', 'Movilidad', 'Normativa', 'Eventos'] as $c) {
        if (!term_exists($c, 'category')) {
            wp_insert_term($c, 'category');
        }
    }
    foreach (['Acta', 'Normativa'] as $t) {
        if (!term_exists($t, 'cadus_tipo_documento')) {
            wp_insert_term($t, 'cadus_tipo_documento');
        }
    }
    $centros = ['Escuela Técnica Superior de Ingeniería Informática', 'Facultad de Derecho', 'Facultad de Ciencias de la Educación',
        'Facultad de Filología', 'Facultad de Psicología', 'Facultad de Matemáticas'];
    foreach ($centros as $c) {
        if (!term_exists($c, 'cadus_centro')) {
            wp_insert_term($c, 'cadus_centro');
        }
    }

    // Tema e identidad visual (HU-18)
    if ($primera && wp_get_theme('blocksy')->exists() && get_option('stylesheet') !== 'blocksy') {
        switch_theme('blocksy');
    }
    if ($primera) {
        $logo = cadus_adjuntar('assets/logo-cadus.png', 'Logotipo CADUS (provisional)');
        if ($logo) {
            set_theme_mod('custom_logo', $logo);
        }
        update_option('blogdescription', 'Consejo de Alumnos de la Universidad de Sevilla');
    }
    if ($primera) {
    set_theme_mod('colorPalette', [
        'color1' => ['color' => '#1f3a5f'], 'color2' => ['color' => '#14284a'], 'color3' => ['color' => '#3a4f66'], 'color4' => ['color' => '#12213b'],
        'color5' => ['color' => '#d6dde6'], 'color6' => ['color' => '#f2f5f7'], 'color7' => ['color' => '#fafbfc'], 'color8' => ['color' => '#ffffff'],
    ]);
    }

    // Páginas (HU-01, HU-03..HU-08)
    $inicio = cadus_pagina('inicio', 'Inicio',
        cadus_b_html('<div class="cadus-banner"><h1>CADUS</h1><p>Consejo de Alumnos de la Universidad de Sevilla</p>'
            . '<a class="cadus-boton" href="' . esc_url(home_url('/delegaciones/')) . '">Delegaciones de alumnos</a>'
            . '<a class="cadus-boton" href="' . esc_url(home_url('/atencion-al-estudiante/buzon-de-consultas/')) . '">Buzón de consultas</a></div>')
        . cadus_b_h('Comunicados recientes')
        . cadus_b_sc('[cadus_ultimas_noticias n="3"]')
        . cadus_b_h('Participación estudiantil')
        . cadus_b_p('El calendario de asambleas, eventos y votaciones se publicará en la próxima versión del portal.'));
    $que_es = cadus_pagina('que-es-el-cadus', 'Qué es el CADUS',
        cadus_b_p('El CADUS es el Consejo de Alumnos de la Universidad de Sevilla, la organización de representación estudiantil de la universidad.')
        . cadus_b_p('Este portal ofrece información y comunicados, las actas y normativas, el directorio de delegaciones de alumnos de cada centro y un buzón para consultas y reclamaciones.')
        . '<div class="cadus-aviso">' . 'Texto provisional: el contenido institucional definitivo está pendiente de validar con la Delegación General del CADUS.' . '</div>');
    cadus_pagina('gobierno-y-estatutos', 'Gobierno y estatutos',
        cadus_b_p('Aquí se publicarán la estructura de gobierno del CADUS y sus estatutos.')
        . '<div class="cadus-aviso">Contenido pendiente de recibir de la Delegación General del CADUS.</div>', $que_es);
    cadus_pagina('noticias', 'Noticias y comunicados',
        cadus_b_p('Comunicados del CADUS clasificados por áreas: becas, movilidad, normativa y eventos.') . cadus_b_sc('[cadus_noticias]'));
    cadus_pagina('actas-y-normativa', 'Actas y normativa',
        cadus_b_p('Actas de los plenos y normativas aprobadas por la Ejecutiva, disponibles para su descarga en PDF.') . cadus_b_sc('[cadus_actas]'));
    cadus_pagina('delegaciones', 'Delegaciones de alumnos',
        cadus_b_p('Directorio de las delegaciones de alumnos agrupado por facultad o escuela.') . cadus_b_sc('[cadus_directorio]'));
    $atencion = cadus_pagina('atencion-al-estudiante', 'Atención al estudiante',
        cadus_b_p('Si necesitas plantear una consulta o una reclamación académica, usa el buzón. Recibirás un código para seguir el estado de tu solicitud.')
        . cadus_b_html('<div class="cadus-tarjetas">'
            . '<div class="cadus-tarjeta"><h3>Buzón de consultas</h3><p>Envía tu consulta o reclamación.</p><a class="cadus-boton" href="' . esc_url(home_url('/atencion-al-estudiante/buzon-de-consultas/')) . '">Ir al buzón</a></div>'
            . '<div class="cadus-tarjeta"><h3>Seguimiento de ticket</h3><p>Consulta el estado con tu código.</p><a class="cadus-boton" href="' . esc_url(home_url('/atencion-al-estudiante/seguimiento-de-ticket/')) . '">Seguir mi ticket</a></div>'
            . '<div class="cadus-tarjeta"><h3>Preguntas frecuentes</h3><p>Dudas habituales sobre el buzón.</p><a class="cadus-boton" href="' . esc_url(home_url('/atencion-al-estudiante/preguntas-frecuentes/')) . '">Ver preguntas</a></div></div>'));
    cadus_pagina('buzon-de-consultas', 'Buzón de consultas y reclamaciones', cadus_b_sc('[cadus_buzon]'), $atencion);
    cadus_pagina('seguimiento-de-ticket', 'Seguimiento de ticket', cadus_b_sc('[cadus_seguimiento]'), $atencion);
    cadus_pagina('preguntas-frecuentes', 'Preguntas frecuentes',
        cadus_b_html('<details><summary><strong>¿Quién puede usar el buzón?</strong></summary><p>Los estudiantes con correo institucional @alum.us.es. Las solicitudes enviadas desde otras direcciones se rechazan.</p></details>'
            . '<details><summary><strong>¿Cómo sé en qué estado está mi consulta?</strong></summary><p>Al enviarla recibes un código de seguimiento con el formato CAD-AAAA-NNNNN. Introdúcelo junto con tu correo en la página de seguimiento.</p></details>'
            . '<details><summary><strong>¿Quién puede ver mi reclamación?</strong></summary><p>Solo tú y la Ejecutiva del CADUS. Los datos se tratan conforme al RGPD.</p></details>'
            . '<details><summary><strong>¿Cómo se publican las actas?</strong></summary><p>Un miembro de la Ejecutiva debe aprobar cada acta o normativa antes de que se publique.</p></details>'
            . '<details><summary><strong>¿Cómo contacto con la delegación de mi centro?</strong></summary><p>Consulta el directorio de delegaciones, donde aparece el contacto y el horario de atención de cada una.</p></details>'), $atencion);
    cadus_pagina('contacto', 'Contacto',
        cadus_b_p('<strong>CADUS – Consejo de Alumnos de la Universidad de Sevilla</strong>')
        . cadus_b_p('Pabellón de Uruguay, Av. de Chile, s/n, 41013 Sevilla')
        . cadus_b_p('Correo: <a href="mailto:cadus@us.es">cadus@us.es</a>'));

    // Noticias de ejemplo (HU-01): se marcan como ejemplo para sustituirlas por comunicados reales
    $ejemplos = [
        ['Comunicado de ejemplo sobre becas', 'Becas', 'Texto de ejemplo para comprobar la plantilla de comunicados de la categoría Becas.'],
        ['Comunicado de ejemplo sobre movilidad', 'Movilidad', 'Texto de ejemplo para comprobar la plantilla de comunicados de la categoría Movilidad.'],
        ['Comunicado de ejemplo sobre normativa', 'Normativa', 'Texto de ejemplo para comprobar la plantilla de comunicados de la categoría Normativa.'],
        ['Comunicado de ejemplo sobre eventos', 'Eventos', 'Texto de ejemplo para comprobar la plantilla de comunicados de la categoría Eventos.'],
    ];
    foreach ($ejemplos as $i => [$titulo, $categoria, $texto]) {
        if (cadus_buscar_semilla('noticia:' . sanitize_title($categoria), 'post', $titulo)) {
            continue;
        }
        $term = get_term_by('name', $categoria, 'category');
        $nuevo = wp_insert_post([
            'post_type' => 'post', 'post_status' => 'publish', 'post_title' => $titulo, 'post_author' => 1,
            'post_content' => cadus_b_p($texto . ' Sustituir por el comunicado real.'), 'post_category' => $term ? [(int) $term->term_id] : [],
            'post_date' => gmdate('Y-m-d H:i:s', time() - ($i + 1) * DAY_IN_SECONDS),
        ]);
        if ($nuevo && !is_wp_error($nuevo)) {
            update_post_meta($nuevo, '_cadus_semilla', 'noticia:' . sanitize_title($categoria));
        }
    }
    foreach ($primera ? ['hola-mundo' => 'post', 'pagina-ejemplo' => 'page'] : [] as $slug => $tipo) {
        $viejo = get_page_by_path($slug, OBJECT, $tipo);
        if ($viejo) {
            wp_trash_post($viejo->ID);
        }
    }

    // Actas y normativas de ejemplo (HU-03, HU-04)
    $pdf = cadus_adjuntar('assets/documento-ejemplo.pdf', 'Documento PDF de ejemplo');
    $docs = [
        ['Acta del pleno ordinario (ejemplo)', 'Acta', '20261015', 'Pleno ordinario', 'publish'],
        ['Reglamento interno (ejemplo)', 'Normativa', '20260920', 'Pleno ordinario', 'publish'],
        ['Acta pendiente de aprobación (ejemplo)', 'Acta', '20261016', 'Pleno extraordinario', 'pending'],
    ];
    foreach ($docs as [$titulo, $tipo, $fecha, $pleno, $estado]) {
        if (cadus_buscar_semilla('acta:' . sanitize_title($titulo), 'cadus_acta', $titulo)) {
            continue;
        }
        $id = wp_insert_post([
            'post_type' => 'cadus_acta', 'post_status' => $estado, 'post_title' => $titulo, 'post_author' => 1,
            'post_content' => cadus_b_p('Documento de ejemplo. Sustituir por el documento real.'),
        ]);
        if ($id && !is_wp_error($id)) {
            update_post_meta($id, '_cadus_semilla', 'acta:' . sanitize_title($titulo));
            wp_set_object_terms($id, $tipo, 'cadus_tipo_documento');
            update_post_meta($id, 'fecha', $fecha);
            update_post_meta($id, '_fecha', 'field_cadus_acta_fecha');
            update_post_meta($id, 'pleno', $pleno);
            update_post_meta($id, '_pleno', 'field_cadus_acta_pleno');
            if ($pdf) {
                update_post_meta($id, 'archivo_pdf', $pdf);
                update_post_meta($id, '_archivo_pdf', 'field_cadus_acta_pdf');
            }
        }
    }

    // Delegaciones de ejemplo (HU-05, HU-06): una por centro, con los datos por completar
    foreach ($centros as $centro) {
        $titulo = 'Delegación de ' . $centro;
        if (cadus_buscar_semilla('delegacion:' . sanitize_title($centro), 'cadus_delegacion', $titulo)) {
            continue;
        }
        $id = wp_insert_post([
            'post_type' => 'cadus_delegacion', 'post_status' => 'publish', 'post_title' => $titulo, 'post_author' => 1,
            'post_content' => cadus_b_p('Ficha pendiente de completar por el delegado o representante del centro.'),
        ]);
        if ($id && !is_wp_error($id)) {
            update_post_meta($id, '_cadus_semilla', 'delegacion:' . sanitize_title($centro));
            wp_set_object_terms($id, $centro, 'cadus_centro');
        }
    }

    // Buzón (HU-07): lo implementa includes/buzon.php
    if (function_exists('cadus_buzon_setup')) {
        cadus_buzon_setup();
    }

    // Menú principal y portada estática (HU-01, UI-02)
    $nombre_menu = 'Menú principal CADUS';
    $menu = wp_get_nav_menu_object($nombre_menu);
    if (!$menu) {
        $menu_id = wp_create_nav_menu($nombre_menu);
        $ruta = fn(string $r) => ($p = get_page_by_path($r)) ? (int) $p->ID : 0;
        $orden = [
            ['inicio', 0], ['que-es-el-cadus', 0], ['que-es-el-cadus/gobierno-y-estatutos', 1], ['noticias', 0], ['actas-y-normativa', 0],
            ['delegaciones', 0], ['atencion-al-estudiante', 0], ['atencion-al-estudiante/buzon-de-consultas', 1],
            ['atencion-al-estudiante/seguimiento-de-ticket', 1], ['atencion-al-estudiante/preguntas-frecuentes', 1], ['contacto', 0],
        ];
        $padres = [];
        foreach ($orden as [$r, $nivel]) {
            $pid = $ruta($r);
            if (!$pid) {
                continue;
            }
            $item = wp_update_nav_menu_item($menu_id, 0, [
                'menu-item-title' => get_the_title($pid), 'menu-item-object' => 'page', 'menu-item-object-id' => $pid,
                'menu-item-type' => 'post_type', 'menu-item-status' => 'publish', 'menu-item-parent-id' => $nivel ? end($padres) : 0,
            ]);
            if (!$nivel) {
                $padres[] = $item;
            }
        }
    } else {
        $menu_id = (int) $menu->term_id;
    }
    if ($primera) {
        set_theme_mod('nav_menu_locations', ['menu_1' => $menu_id, 'menu_mobile' => $menu_id]);
        update_option('show_on_front', 'page');
        update_option('page_on_front', $inicio);
    }

    update_option('cadus_portal_version', CADUS_PORTAL_VERSION);
}
