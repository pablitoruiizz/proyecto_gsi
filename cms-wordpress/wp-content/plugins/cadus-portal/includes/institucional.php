<?php
/**
 * Contenido institucional real de «Qué es el CADUS» y «Gobierno y estatutos» (E2-11 · HU-03 · RF-03).
 *
 * Sustituye los textos provisionales del Sprint 1 por un texto basado en la normativa publicada:
 *  - Estatutos de la Universidad de Sevilla, aprobados por Decreto 98/2025, de 30 de abril (BOE n.º 121, de 20/05/2025), art. 21.
 *  - Reglamento de Elecciones a Órganos de Representación Estudiantil de la US (REOREUS), aprobado por el
 *    Pleno del CADUS el 12/05/2022.
 * Redactado por Miguel Ángel Camacho (miembro del CADUS, contacto con el cliente) el 12/11/2026.
 *
 * Solo se reemplaza una página si todavía tiene el texto provisional (nadie la ha editado). Si la Ejecutiva
 * ya ha escrito su propio texto, no se toca. En una instalación nueva, las páginas nacen con este contenido.
 */

if (!defined('ABSPATH')) {
    exit;
}

define('CADUS_INSTITUCIONAL_VERSION', '1');

const CADUS_URL_ESTATUTOS = 'https://www.boe.es/boe/dias/2025/05/20/pdfs/BOE-A-2025-9917.pdf';
const CADUS_URL_REOREUS = 'https://edwww.us.es/sites/default/files/secretaria-general/consulta-us/2022_05_Reglamento_Elecciones_Organos_Representacion_Estudiantil_US.pdf';

add_action('init', function () {
    if (is_admin() && get_option('cadus_portal_version') && get_option('cadus_institucional_version') !== CADUS_INSTITUCIONAL_VERSION) {
        cadus_actualizar_institucional();
    }
}, 25);

/** Enlace externo a un documento oficial, con aviso para lectores de pantalla de que abre un PDF. */
function cadus_inst_enlace(string $url, string $texto): string
{
    return '<a href="' . esc_url($url) . '" rel="noopener">' . esc_html($texto) . '<span class="screen-reader-text"> (PDF, sitio externo)</span></a>';
}

function cadus_contenido_que_es(): string
{
    return cadus_b_p('El <strong>Consejo de Alumnos y Alumnas de la Universidad de Sevilla (CADUS)</strong> es el órgano colegiado superior de representación y coordinación del estudiantado de la Universidad de Sevilla. Está formado por todos los miembros de las delegaciones de estudiantes de los centros (artículo 21 de los Estatutos de la Universidad).')
        . cadus_b_p('Dicho de otra forma: cada facultad o escuela tiene su <a href="' . esc_url(home_url('/delegaciones/')) . '">delegación de estudiantes</a>, y todas juntas forman el CADUS. Es la voz del alumnado ante el Rectorado, el Consejo de Gobierno y el resto de órganos de la Universidad.')
        . cadus_b_h('Qué hace el CADUS')
        . cadus_b_html('<ul>'
            . '<li>Coordina y lleva a cabo las iniciativas que salen de las asambleas de los centros y de la Universidad.</li>'
            . '<li>Coordina a quienes representan al estudiantado en los órganos de gobierno.</li>'
            . '<li>Vela por que se cumplan y respeten los derechos y deberes del estudiantado.</li>'
            . '<li>Es oído cuando se elaboran normas que afectan directamente al estudiantado, y hace propuestas a los órganos de gobierno.</li>'
            . '<li>Fomenta el asociacionismo y la participación estudiantil.</li>'
            . '<li>Participa en el reparto de becas, ayudas y créditos, y decide cómo se distribuyen sus propios recursos.</li>'
            . '<li>Aprueba su reglamento de funcionamiento y su reglamento de elecciones, que ratifica el Consejo de Gobierno.</li>'
            . '</ul>')
        . cadus_b_h('Cómo te puede ayudar')
        . cadus_b_html('<ul>'
            . '<li><a href="' . esc_url(home_url('/atencion-al-estudiante/buzon-de-consultas/')) . '">Buzón de consultas y reclamaciones</a>: cuéntanos tu problema y te responderemos en un máximo de 4 días hábiles desde que revisemos tu consulta.</li>'
            . '<li><a href="' . esc_url(home_url('/atencion-al-estudiante/mediacion-estudiantil/')) . '">Mediación estudiantil</a>: si tienes un conflicto en tu centro, el CADUS puede mediar.</li>'
            . '<li><a href="' . esc_url(home_url('/delegaciones/')) . '">Tu delegación de centro</a>: es tu primer contacto para lo que pasa en tu facultad o escuela.</li>'
            . '<li><a href="' . esc_url(home_url('/eventos/')) . '">Calendario</a>: asambleas, cursos y votaciones abiertas al estudiantado.</li>'
            . '</ul>')
        . cadus_b_h('Dónde estamos')
        . cadus_b_p('Pabellón de Uruguay, Av. de Chile s/n, 41013 Sevilla · Teléfono <a href="tel:954486022">954 48 60 22</a> · <a href="mailto:dcadus@us.es">dcadus@us.es</a>')
        . cadus_b_p('Más información sobre el gobierno del CADUS y la normativa en <a href="' . esc_url(home_url('/que-es-el-cadus/gobierno-y-estatutos/')) . '">Gobierno y estatutos</a>.');
}

function cadus_contenido_gobierno(): string
{
    return cadus_b_p('El CADUS se organiza en dos niveles: el <strong>Pleno</strong>, donde están todas las delegaciones de centro, y la <strong>Delegación del CADUS</strong>, el equipo que lo dirige durante el curso (en esta web, «la Ejecutiva»).')
        . cadus_b_h('Órganos')
        . cadus_b_html('<dl class="cadus-ficha">'
            . '<div class="cadus-ficha__fila"><dt>Pleno del CADUS</dt><dd>Reúne a las delegaciones de estudiantes de los centros. Cada delegación de centro propio tiene un voto. Elige a la Comisión Electoral y toma los grandes acuerdos del CADUS, como sus reglamentos.</dd></div>'
            . '<div class="cadus-ficha__fila"><dt>Delegación del CADUS (Ejecutiva)</dt><dd>Equipo elegido cada curso por las delegaciones de centro, mediante candidaturas colectivas. Representa al CADUS y lo dirige durante su mandato. En esta web atiende el buzón y la mediación y publica las noticias, las actas y la normativa.</dd></div>'
            . '<div class="cadus-ficha__fila"><dt>Delegado o Delegada del CADUS</dt><dd>Lo designa la Delegación del CADUS entre sus miembros. Necesita mayoría absoluta en la primera votación, o mayoría simple en la segunda entre los dos más votados. Representa al CADUS ante los órganos de gobierno de la Universidad y sigue en el cargo hasta que se proclama la nueva Delegación.</dd></div>'
            . '<div class="cadus-ficha__fila"><dt>Comisión Electoral</dt><dd>Cinco miembros elegidos por el Pleno en su primera sesión del curso. Es el órgano electoral del CADUS: organiza y supervisa las elecciones de representación estudiantil.</dd></div>'
            . '<div class="cadus-ficha__fila"><dt>Delegaciones de centro</dt><dd>Una por cada facultad o escuela. Representan y coordinan al estudiantado de su centro, y sus miembros forman el CADUS. Se renuevan cada curso. <a href="' . esc_url(home_url('/delegaciones/')) . '">Ver el directorio</a>.</dd></div>'
            . '</dl>')
        . cadus_b_h('Cómo se elige')
        . cadus_b_p('Cada curso se eligen primero los delegados de grupo y de curso, después las delegaciones de centro y, por último, la Delegación del CADUS, que votan las delegaciones de centro (un voto por delegación). Las candidaturas deben respetar la paridad.')
        . cadus_b_h('Normativa')
        . cadus_b_html('<ul>'
            . '<li>' . cadus_inst_enlace(CADUS_URL_ESTATUTOS, 'Estatutos de la Universidad de Sevilla') . ' (Decreto 98/2025, de 30 de abril; BOE n.º 121, de 20 de mayo de 2025). El artículo 21 regula el CADUS.</li>'
            . '<li>' . cadus_inst_enlace(CADUS_URL_REOREUS, 'Reglamento de Elecciones a Órganos de Representación Estudiantil (REOREUS)') . ', aprobado por el Pleno del CADUS el 12 de mayo de 2022.</li>'
            . '<li>Las actas de los plenos y la normativa interna del CADUS están en <a href="' . esc_url(home_url('/actas-y-normativa/')) . '">Actas y normativa</a>.</li>'
            . '</ul>');
}

/** ¿Sigue la página con el texto provisional del Sprint 1? Entonces nadie la ha editado y se puede sustituir. */
function cadus_inst_es_provisional(?WP_Post $pagina, string $marca): bool
{
    return $pagina instanceof WP_Post && strpos((string) $pagina->post_content, $marca) !== false
        && mb_strlen(wp_strip_all_tags($pagina->post_content)) < 600;
}

function cadus_actualizar_institucional(): void
{
    $kses = (bool) has_filter('content_save_pre', 'wp_filter_post_kses');
    if ($kses) {
        kses_remove_filters();
    }
    $paginas = [
        ['que-es-el-cadus', 'Qué es el CADUS', 'Texto provisional: el contenido institucional definitivo', 'cadus_contenido_que_es', 0],
        ['que-es-el-cadus/gobierno-y-estatutos', 'Gobierno y estatutos', 'Contenido pendiente de recibir de la Delegación General', 'cadus_contenido_gobierno', 1],
    ];
    foreach ($paginas as [$ruta, $titulo, $marca, $contenido, $hija]) {
        $pagina = cadus_buscar_semilla('pagina:' . $ruta, 'page') ?? get_page_by_path($ruta);
        if (cadus_inst_es_provisional($pagina, $marca)) {
            wp_update_post(['ID' => $pagina->ID, 'post_content' => $contenido()]);
        } elseif (!$pagina) {
            $padre = $hija ? (cadus_buscar_semilla('pagina:que-es-el-cadus', 'page') ?? get_page_by_path('que-es-el-cadus')) : null;
            cadus_pagina(basename($ruta), $titulo, $contenido(), $padre ? (int) $padre->ID : 0);
        }
    }
    if ($kses) {
        kses_init_filters();
    }
    update_option('cadus_institucional_version', CADUS_INSTITUCIONAL_VERSION);
}
