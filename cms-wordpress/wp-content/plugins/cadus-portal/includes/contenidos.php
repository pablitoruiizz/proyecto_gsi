<?php
/**
 * Contenidos propios del portal: actas y normativas (HU-03, HU-04) y delegaciones (HU-05, HU-06).
 * Trazabilidad: RF-03, RF-04, RF-05, RF-06, RF-07, RN-01, RN-04, IR-04, IR-05, UI-03, UI-05.
 *
 * Aprobación previa (RN-01): el flujo usa los estados nativos de WordPress. Quien no tiene la capacidad
 * publish_cadus_actas (todos salvo la Ejecutiva y el administrador) solo puede dejar el acta como
 * "Pendiente de revisión"; solo la Ejecutiva la publica.
 * Edición de fichas (RN-04): un delegado solo edita las delegaciones de las que es autor; el resto
 * requiere edit_others_cadus_delegacions (Ejecutiva y administrador).
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('init', 'cadus_registrar_contenidos');
add_action('acf/init', 'cadus_registrar_campos');
add_filter('the_content', 'cadus_ficha_en_contenido');
add_shortcode('cadus_actas', 'cadus_shortcode_actas');
add_shortcode('cadus_directorio', 'cadus_shortcode_directorio');

function cadus_registrar_contenidos(): void
{
    register_taxonomy('cadus_tipo_documento', ['cadus_acta'], [
        'labels' => ['name' => 'Tipos de documento', 'singular_name' => 'Tipo de documento', 'menu_name' => 'Tipos de documento'],
        'hierarchical' => true,
        'public' => true,
        'show_in_rest' => true,
        'rewrite' => ['slug' => 'tipo-documento'],
    ]);

    register_post_type('cadus_acta', [
        'labels' => [
            'name' => 'Actas y normativas', 'singular_name' => 'Acta o normativa', 'add_new' => 'Añadir documento',
            'add_new_item' => 'Añadir acta o normativa', 'edit_item' => 'Editar acta o normativa',
            'all_items' => 'Todas las actas y normativas', 'menu_name' => 'Actas y normativas',
        ],
        'public' => true,
        'has_archive' => 'actas',
        'rewrite' => ['slug' => 'acta'],
        'menu_icon' => 'dashicons-media-document',
        'supports' => ['title', 'editor', 'excerpt'],
        'taxonomies' => ['cadus_tipo_documento'],
        'capability_type' => ['cadus_acta', 'cadus_actas'],
        'map_meta_cap' => true,
        'show_in_rest' => true,
    ]);

    register_taxonomy('cadus_centro', ['cadus_delegacion'], [
        'labels' => ['name' => 'Facultades y escuelas', 'singular_name' => 'Facultad o escuela', 'menu_name' => 'Facultades y escuelas'],
        'hierarchical' => true,
        'public' => true,
        'show_in_rest' => true,
        'rewrite' => ['slug' => 'centro'],
    ]);

    register_post_type('cadus_delegacion', [
        'labels' => [
            'name' => 'Delegaciones', 'singular_name' => 'Delegación', 'add_new' => 'Añadir delegación',
            'add_new_item' => 'Añadir delegación de centro', 'edit_item' => 'Editar delegación',
            'all_items' => 'Todas las delegaciones', 'menu_name' => 'Delegaciones',
        ],
        'public' => true,
        'has_archive' => 'delegaciones-centro',
        'rewrite' => ['slug' => 'delegacion'],
        'menu_icon' => 'dashicons-groups',
        'supports' => ['title', 'editor', 'author'],
        'taxonomies' => ['cadus_centro'],
        'capability_type' => ['cadus_delegacion', 'cadus_delegacions'],
        'map_meta_cap' => true,
        'show_in_rest' => true,
    ]);
}

/** Campos ACF definidos por código para que viajen con el repositorio. */
function cadus_registrar_campos(): void
{
    if (!function_exists('acf_add_local_field_group')) {
        return;
    }
    acf_add_local_field_group([
        'key' => 'group_cadus_acta',
        'title' => 'Datos del documento',
        'fields' => [
            ['key' => 'field_cadus_acta_fecha', 'label' => 'Fecha', 'name' => 'fecha', 'type' => 'date_picker',
                'display_format' => 'd/m/Y', 'return_format' => 'Ymd', 'first_day' => 1, 'required' => 1],
            ['key' => 'field_cadus_acta_pleno', 'label' => 'Pleno asociado', 'name' => 'pleno', 'type' => 'text'],
            ['key' => 'field_cadus_acta_pdf', 'label' => 'Archivo PDF', 'name' => 'archivo_pdf', 'type' => 'file',
                'return_format' => 'array', 'library' => 'all', 'mime_types' => 'pdf', 'required' => 1],
        ],
        'location' => [[['param' => 'post_type', 'operator' => '==', 'value' => 'cadus_acta']]],
        'position' => 'normal',
    ]);
    acf_add_local_field_group([
        'key' => 'group_cadus_delegacion',
        'title' => 'Ficha de la delegación',
        'fields' => [
            ['key' => 'field_cadus_deleg_delegado', 'label' => 'Delegado o representante', 'name' => 'delegado', 'type' => 'text'],
            ['key' => 'field_cadus_deleg_correo', 'label' => 'Correo de contacto', 'name' => 'correo', 'type' => 'email'],
            ['key' => 'field_cadus_deleg_tel', 'label' => 'Teléfono', 'name' => 'telefono', 'type' => 'text'],
            ['key' => 'field_cadus_deleg_horario', 'label' => 'Horario de atención', 'name' => 'horario', 'type' => 'text'],
            ['key' => 'field_cadus_deleg_enlaces', 'label' => 'Enlaces de interés (uno por línea)', 'name' => 'enlaces', 'type' => 'textarea', 'rows' => 4],
        ],
        'location' => [[['param' => 'post_type', 'operator' => '==', 'value' => 'cadus_delegacion']]],
        'position' => 'normal',
    ]);
}

/** Lee un campo de ACF con alternativa a los metadatos si ACF no está activo. */
function cadus_campo(string $nombre, int $id)
{
    if (function_exists('get_field')) {
        return get_field($nombre, $id);
    }
    return get_post_meta($id, $nombre, true);
}

/** URL del PDF, tanto si ACF devuelve un array como si solo hay un ID de adjunto (sin ACF). */
function cadus_url_pdf($valor): string
{
    if (is_array($valor)) {
        return (string) ($valor['url'] ?? '');
    }
    return is_numeric($valor) ? (string) wp_get_attachment_url((int) $valor) : '';
}

/** Muestra la ficha (datos y botón de descarga) bajo el contenido de actas y delegaciones. */
function cadus_ficha_en_contenido(string $contenido): string
{
    if (!is_singular(['cadus_acta', 'cadus_delegacion']) || !in_the_loop() || !is_main_query()) {
        return $contenido;
    }
    $id = get_the_ID();
    $html = '';
    if (get_post_type() === 'cadus_acta') {
        $tipos = wp_get_post_terms($id, 'cadus_tipo_documento', ['fields' => 'names']);
        $fecha = cadus_campo('fecha', $id);
        $fecha_txt = $fecha ? date_i18n('j \d\e F \d\e Y', strtotime((string) $fecha)) : '—';
        $pdf = cadus_campo('archivo_pdf', $id);
        $url = cadus_url_pdf($pdf);
        $html .= '<dl class="cadus-ficha">';
        $html .= '<div class="cadus-ficha__fila"><dt>Tipo</dt><dd>' . esc_html(!is_wp_error($tipos) && $tipos ? implode(', ', $tipos) : '—') . '</dd></div>';
        $html .= '<div class="cadus-ficha__fila"><dt>Fecha</dt><dd>' . esc_html($fecha_txt) . '</dd></div>';
        $html .= '<div class="cadus-ficha__fila"><dt>Pleno asociado</dt><dd>' . esc_html((string) cadus_campo('pleno', $id) ?: '—') . '</dd></div>';
        $html .= '<div class="cadus-ficha__fila"><dt>Estado</dt><dd>Aprobada y publicada por la Ejecutiva</dd></div></dl>';
        if ($url) {
            $html .= '<p><a class="cadus-boton" href="' . esc_url($url) . '" download>Descargar PDF<span class="screen-reader-text">: ' . esc_html(get_the_title()) . '</span></a></p>';
        }
        $listado = 'actas-y-normativa';
    } else {
        $enlaces = array_filter(array_map('trim', explode("\n", (string) cadus_campo('enlaces', $id))));
        $html .= '<dl class="cadus-ficha">';
        $html .= '<div class="cadus-ficha__fila"><dt>Delegado/a</dt><dd>' . esc_html((string) cadus_campo('delegado', $id) ?: 'Por completar') . '</dd></div>';
        $correo = (string) cadus_campo('correo', $id);
        $html .= '<div class="cadus-ficha__fila"><dt>Correo</dt><dd>' . ($correo ? '<a href="' . esc_url('mailto:' . $correo) . '">' . esc_html($correo) . '</a>' : 'Por completar') . '</dd></div>';
        $html .= '<div class="cadus-ficha__fila"><dt>Teléfono</dt><dd>' . esc_html((string) cadus_campo('telefono', $id) ?: 'Por completar') . '</dd></div>';
        $html .= '<div class="cadus-ficha__fila"><dt>Horario de atención</dt><dd>' . esc_html((string) cadus_campo('horario', $id) ?: 'Por completar') . '</dd></div>';
        if ($enlaces) {
            $html .= '<div class="cadus-ficha__fila"><dt>Enlaces de interés</dt><dd><ul>';
            foreach ($enlaces as $e) {
                $html .= '<li><a href="' . esc_url($e) . '">' . esc_html($e) . '</a></li>';
            }
            $html .= '</ul></dd></div>';
        }
        $html .= '</dl>';
        $listado = 'delegaciones';
    }
    return $contenido . $html . '<p><a class="cadus-chip" href="' . esc_url(cadus_inicio_url($listado)) . '">← Volver al listado</a></p>';
}

/** Mantiene la semántica y el aria-current de WordPress al vestir su paginación. */
function cadus_paginacion($paginas): string
{
    if (!$paginas) {
        return '';
    }
    $marcado = new WP_HTML_Tag_Processor($paginas);
    while ($marcado->next_tag()) {
        if (in_array($marcado->get_tag(), ['A', 'SPAN'], true)) {
            $marcado->add_class('cadus-chip');
        }
    }
    return '<nav class="cadus-paginacion" aria-label="Paginación">' . $marcado->get_updated_html() . '</nav>';
}

/** [cadus_actas]: listado de actas y normativas filtrable por tipo y ordenado por fecha (HU-04). */
function cadus_shortcode_actas(): string
{
    $tipo = isset($_GET['tipo']) && is_string($_GET['tipo']) ? sanitize_title(wp_unslash($_GET['tipo'])) : '';
    $pag = isset($_GET['pag']) ? max(1, absint($_GET['pag'])) : 1;
    $args = [
        'post_type' => 'cadus_acta', 'post_status' => 'publish', 'posts_per_page' => 20, 'paged' => $pag,
        'meta_query' => [
            'relation' => 'OR',
            'con_fecha' => ['key' => 'fecha', 'compare' => 'EXISTS'],
            'sin_fecha' => ['key' => 'fecha', 'compare' => 'NOT EXISTS'],
        ],
        'orderby' => ['con_fecha' => 'DESC', 'date' => 'DESC'],
    ];
    if ($tipo) {
        $args['tax_query'] = [['taxonomy' => 'cadus_tipo_documento', 'field' => 'slug', 'terms' => $tipo]];
    }
    $consulta = new WP_Query($args);
    $base = get_permalink();
    $html = '<nav class="cadus-filtros-tipo" aria-label="Filtrar por tipo"><a class="cadus-chip" href="' . esc_url($base) . '"' . ($tipo === '' ? ' aria-current="true"' : '') . '>Todos</a>';
    $terminos = get_terms(['taxonomy' => 'cadus_tipo_documento', 'hide_empty' => false]);
    foreach (is_wp_error($terminos) ? [] : $terminos as $t) {
        $html .= '<a class="cadus-chip" href="' . esc_url(add_query_arg('tipo', $t->slug, $base)) . '"' . ($tipo === $t->slug ? ' aria-current="true"' : '') . '>' . esc_html($t->name) . '</a>';
    }
    $html .= '</nav>';
    if (!$consulta->have_posts()) {
        return $html . '<p class="cadus-vacio">No hay documentos publicados para este filtro.</p>';
    }
    // Roles explícitos: el CSS móvil cambia el display de las partes de la tabla.
    $html .= '<table class="cadus-tabla" role="table"><caption class="screen-reader-text">Actas y normativa publicadas</caption><thead role="rowgroup"><tr role="row"><th scope="col" role="columnheader">Fecha</th><th scope="col" role="columnheader">Documento</th><th scope="col" role="columnheader">Tipo</th><th scope="col" role="columnheader">PDF</th></tr></thead><tbody role="rowgroup">';
    while ($consulta->have_posts()) {
        $consulta->the_post();
        $id = get_the_ID();
        $fecha = cadus_campo('fecha', $id);
        $pdf = cadus_campo('archivo_pdf', $id);
        $tipos = wp_get_post_terms($id, 'cadus_tipo_documento', ['fields' => 'names']);
        $html .= '<tr role="row"><td role="cell" data-label="Fecha">' . esc_html($fecha ? date_i18n('d/m/Y', strtotime((string) $fecha)) : '—') . '</td>'
            . '<td role="cell" data-label="Documento"><a href="' . esc_url(get_permalink()) . '">' . esc_html(get_the_title()) . '</a></td>'
            . '<td role="cell" data-label="Tipo">' . esc_html(!is_wp_error($tipos) && $tipos ? implode(', ', $tipos) : '—') . '</td>'
            . '<td role="cell" data-label="PDF">' . (cadus_url_pdf($pdf) ? '<a class="cadus-descarga" href="' . esc_url(cadus_url_pdf($pdf)) . '" download>Descargar PDF<span class="screen-reader-text">: ' . esc_html(get_the_title()) . '</span></a>' : '—') . '</td></tr>';
    }
    wp_reset_postdata();
    $paginas = paginate_links([
        'base' => esc_url_raw(add_query_arg('pag', '%#%', $base)), 'format' => '', 'current' => $pag,
        'total' => max(1, (int) $consulta->max_num_pages), 'add_args' => array_filter(['tipo' => $tipo ?: null]),
    ]);
    return $html . '</tbody></table>' . cadus_paginacion($paginas);
}

/** [cadus_directorio]: directorio de delegaciones agrupado por facultad o escuela (HU-05). */
function cadus_shortcode_directorio(): string
{
    $centros = get_terms(['taxonomy' => 'cadus_centro', 'hide_empty' => true, 'orderby' => 'name']);
    if (is_wp_error($centros) || !$centros) {
        return '<p class="cadus-vacio">El directorio se está completando.</p>';
    }
    $html = '<div class="cadus-centros">';
    $indice = 0;
    foreach ($centros as $centro) {
        $consulta = new WP_Query([
            'post_type' => 'cadus_delegacion', 'post_status' => 'publish', 'posts_per_page' => -1, 'orderby' => 'title', 'order' => 'ASC',
            'tax_query' => [['taxonomy' => 'cadus_centro', 'field' => 'term_id', 'terms' => $centro->term_id]],
        ]);
        if (!$consulta->have_posts()) {
            continue;
        }
        $html .= '<section class="cadus-centro" data-reveal style="--i:' . esc_attr((string) $indice++) . '"><h2 class="cadus-centro__titulo">' . esc_html($centro->name) . '</h2><ul class="cadus-delegaciones">';
        while ($consulta->have_posts()) {
            $consulta->the_post();
            $id = get_the_ID();
            $deleg = (string) cadus_campo('delegado', $id);
            $horario = (string) cadus_campo('horario', $id);
            $correo = (string) cadus_campo('correo', $id);
            $meta = array_filter([$deleg ? 'Delegado/a: ' . $deleg : '', $correo, $horario], static fn($valor) => $valor !== '');
            $html .= '<li class="cadus-delegacion-card"><a class="cadus-delegacion-card__enlace" href="' . esc_url(get_permalink()) . '">'
                . '<span class="cadus-delegacion-card__nombre">' . esc_html(get_the_title()) . '</span>'
                . ($meta ? '<span class="cadus-delegacion-card__meta">' . esc_html(implode(' · ', $meta)) . '</span>' : '')
                . '<span class="cadus-delegacion-card__ver">Ver ficha</span></a></li>';
        }
        wp_reset_postdata();
        $html .= '</ul></section>';
    }
    return $html . '</div>';
}
