<?php
/**
 * Panel de inicio del Escritorio con accesos directos por rol (HU-19b · RF-15).
 *
 * Un único panel «Accesos rápidos del CADUS» con una tarjeta por área. Cada tarjeta solo aparece
 * si el usuario tiene permiso sobre ese contenido, así que el mismo código sirve para todos los roles:
 *  - Ejecutivo: noticias, actas (con las pendientes de aprobar, RN-01), delegaciones, tickets y eventos.
 *  - Delegado: solo sus propias delegaciones (RN-04).
 *  - Administrador: todo, además de los paneles normales de WordPress.
 *  - Estudiante: no entra en el Escritorio (admin.php lo lleva a la web).
 *
 * Privacidad de los tickets (RN-03): el panel solo muestra cuántos hay en cada estado, nunca asuntos,
 * correos ni textos, y solo a quien puede gestionarlos.
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('wp_dashboard_setup', 'cadus_escritorio_preparar', 999);
add_action('admin_head-index.php', 'cadus_escritorio_estilos');

/** Los roles del portal ven un Escritorio limpio: solo el panel del CADUS. */
function cadus_escritorio_preparar(): void
{
    global $wp_meta_boxes;
    if (cadus_rol_admin(wp_get_current_user()) !== '') {
        foreach ((array) ($wp_meta_boxes['dashboard'] ?? []) as $contexto => $prioridades) {
            foreach ((array) $prioridades as $cajas) {
                foreach (array_keys((array) $cajas) as $id) {
                    remove_meta_box($id, 'dashboard', $contexto);
                }
            }
        }
        remove_action('welcome_panel', 'wp_welcome_panel');
    }
    if (cadus_escritorio_tarjetas() !== []) {
        wp_add_dashboard_widget('cadus_accesos', 'Accesos rápidos del CADUS', 'cadus_escritorio_panel', null, null, 'normal', 'high');
    }
}

/** Número de contenidos de un tipo en un estado (respeta la papelera: no la cuenta). */
function cadus_escritorio_contar(string $tipo, string $estado): int
{
    $cuenta = wp_count_posts($tipo);
    return isset($cuenta->$estado) ? (int) $cuenta->$estado : 0;
}

/**
 * Tarjetas que puede ver el usuario actual.
 * @return array<int, array{icono: string, titulo: string, datos: string[], enlaces: array<int, array{0: string, 1: string, 2?: bool}>, aviso?: string}>
 */
function cadus_escritorio_tarjetas(): array
{
    $tarjetas = [];

    // Noticias y comunicados (HU-01)
    if (current_user_can('edit_posts')) {
        $tarjetas[] = [
            'icono' => 'dashicons-megaphone', 'titulo' => 'Noticias y comunicados',
            'datos' => [
                sprintf('%d publicadas', cadus_escritorio_contar('post', 'publish')),
                sprintf('%d borradores', cadus_escritorio_contar('post', 'draft')),
            ],
            'enlaces' => [
                ['Nueva noticia', admin_url('post-new.php'), true],
                ['Ver todas', admin_url('edit.php')],
            ],
        ];
    }

    // Actas y normativas (HU-03, RN-01): quien puede publicarlas ve las pendientes de aprobar.
    if (current_user_can('edit_cadus_actas')) {
        $pendientes = cadus_escritorio_contar('cadus_acta', 'pending');
        $tarjeta = [
            'icono' => 'dashicons-media-document', 'titulo' => 'Actas y normativa',
            'datos' => [
                sprintf('%d publicadas', cadus_escritorio_contar('cadus_acta', 'publish')),
                sprintf('%d pendientes de revisión', $pendientes),
            ],
            'enlaces' => [
                ['Nueva acta', admin_url('post-new.php?post_type=cadus_acta'), true],
                ['Ver todas', admin_url('edit.php?post_type=cadus_acta')],
            ],
        ];
        if ($pendientes > 0 && current_user_can('publish_cadus_actas')) {
            $tarjeta['aviso'] = sprintf(_n('%d acta espera tu aprobación', '%d actas esperan tu aprobación', $pendientes, 'cadus-portal'), $pendientes);
            $tarjeta['enlaces'][] = ['Revisar pendientes', admin_url('edit.php?post_type=cadus_acta&post_status=pending')];
        }
        $tarjetas[] = $tarjeta;
    }

    // Delegaciones (HU-06, RN-04): la Ejecutiva ve todas; el delegado, solo las suyas.
    if (current_user_can('edit_cadus_delegacions')) {
        if (current_user_can('edit_others_cadus_delegacions')) {
            $tarjetas[] = [
                'icono' => 'dashicons-location', 'titulo' => 'Delegaciones',
                'datos' => [sprintf('%d publicadas', cadus_escritorio_contar('cadus_delegacion', 'publish'))],
                'enlaces' => [
                    ['Nueva delegación', admin_url('post-new.php?post_type=cadus_delegacion'), true],
                    ['Ver todas', admin_url('edit.php?post_type=cadus_delegacion')],
                ],
            ];
        } else {
            $propias = get_posts([
                'post_type' => 'cadus_delegacion', 'author' => get_current_user_id(),
                'post_status' => ['publish', 'draft', 'pending', 'private'], 'posts_per_page' => 5,
                'orderby' => 'title', 'order' => 'ASC', 'no_found_rows' => true,
            ]);
            $enlaces = [];
            foreach ($propias as $delegacion) {
                $enlaces[] = ['Editar ' . get_the_title($delegacion), (string) get_edit_post_link($delegacion->ID, 'raw'), true];
            }
            $enlaces[] = ['Ver mis delegaciones', admin_url('edit.php?post_type=cadus_delegacion&author=' . get_current_user_id())];
            $tarjetas[] = [
                'icono' => 'dashicons-location', 'titulo' => 'Mi delegación',
                'datos' => [$propias ? 'Mantén al día el contacto y el horario de atención.' : 'Todavía no tienes ninguna delegación asignada.'],
                'enlaces' => $enlaces,
            ];
        }
    }

    // Tickets del buzón (HU-09, RN-03): solo cifras por estado y solo para quien los gestiona.
    if (current_user_can('edit_others_cadus_tickets') && function_exists('cadus_buzon_estados')) {
        $datos = [];
        foreach (cadus_buzon_estados() as $estado => $nombre) {
            $consulta = new WP_Query([
                'post_type' => 'cadus_ticket', 'post_status' => ['private', 'publish', 'draft', 'pending'],
                'fields' => 'ids', 'posts_per_page' => 1,
                'meta_query' => [['key' => '_cadus_estado', 'value' => $estado]],
            ]);
            $datos[] = sprintf('%s: %d', $nombre, (int) $consulta->found_posts);
        }
        $tarjetas[] = [
            'icono' => 'dashicons-email-alt', 'titulo' => 'Tickets del buzón',
            'datos' => $datos,
            'enlaces' => [['Gestionar tickets', admin_url('edit.php?post_type=cadus_ticket'), true]],
        ];
    }

    // Calendario de asambleas y eventos (HU-10), si The Events Calendar está activo.
    if (function_exists('cadus_calendario_activo') && cadus_calendario_activo() && current_user_can('edit_tribe_events')) {
        $proximos = count(cadus_calendario_eventos(50));
        $tarjetas[] = [
            'icono' => 'dashicons-calendar-alt', 'titulo' => 'Calendario',
            'datos' => [sprintf(_n('%d evento próximo', '%d eventos próximos', $proximos, 'cadus-portal'), $proximos)],
            'enlaces' => [
                ['Nuevo evento', admin_url('post-new.php?post_type=tribe_events'), true],
                ['Ver todos', admin_url('edit.php?post_type=tribe_events')],
                ['Ver el calendario', cadus_calendario_url()],
            ],
        ];
    }

    return $tarjetas;
}

function cadus_escritorio_panel(): void
{
    $html = '<div class="cadus-escritorio">';
    foreach (cadus_escritorio_tarjetas() as $tarjeta) {
        $html .= '<section class="cadus-escritorio__tarjeta"><h3><span class="dashicons ' . esc_attr($tarjeta['icono'])
            . '" aria-hidden="true"></span> ' . esc_html($tarjeta['titulo']) . '</h3><ul class="cadus-escritorio__datos">';
        foreach ($tarjeta['datos'] as $dato) {
            $html .= '<li>' . esc_html($dato) . '</li>';
        }
        $html .= '</ul>';
        if (!empty($tarjeta['aviso'])) {
            $html .= '<p class="cadus-escritorio__aviso">' . esc_html($tarjeta['aviso']) . '</p>';
        }
        $html .= '<p class="cadus-escritorio__enlaces">';
        foreach ($tarjeta['enlaces'] as $enlace) {
            $clase = !empty($enlace[2]) ? 'button button-primary' : 'button';
            $html .= '<a class="' . $clase . '" href="' . esc_url($enlace[1]) . '">' . esc_html($enlace[0]) . '</a> ';
        }
        $html .= '</p></section>';
    }
    $html .= '</div><p class="cadus-escritorio__pie"><a href="' . esc_url(home_url('/')) . '">' . esc_html('Ver el portal')
        . '</a> · <a href="' . esc_url(admin_url('profile.php')) . '">' . esc_html('Mi perfil') . '</a></p>';
    echo $html; // phpcs:ignore WordPress.Security.EscapeOutput -- todo se escapa al montar $html
}

function cadus_escritorio_estilos(): void
{
    echo '<style id="cadus-escritorio">'
        . '.cadus-escritorio{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px}'
        . '.cadus-escritorio__tarjeta{border:1px solid #dcdcde;border-top:4px solid #8d0739;border-radius:6px;padding:12px 14px;background:#fff}'
        . '.cadus-escritorio__tarjeta h3{display:flex;align-items:center;gap:6px;margin:0 0 8px;font-size:15px}'
        . '.cadus-escritorio__tarjeta h3 .dashicons{color:#8d0739}'
        . '.cadus-escritorio__datos{margin:0 0 10px;color:#50575e}.cadus-escritorio__datos li{margin:0 0 2px}'
        . '.cadus-escritorio__aviso{margin:0 0 10px;padding:6px 10px;background:#fff8e1;border-left:4px solid #faba09}'
        . '.cadus-escritorio__enlaces{display:flex;flex-wrap:wrap;gap:6px;margin:0}'
        . '.cadus-escritorio__enlaces .button{white-space:normal;height:auto;max-width:100%;text-align:center}'
        . '.cadus-escritorio .button-primary{background:#8d0739;border-color:#8d0739}'
        . '.cadus-escritorio .button-primary:hover,.cadus-escritorio .button-primary:focus{background:#6b052b;border-color:#6b052b}'
        . '.cadus-escritorio__pie{margin:14px 0 0}'
        // Para los roles del portal el panel es lo único del Escritorio: ocupa todo el ancho.
        . (cadus_rol_admin(wp_get_current_user()) !== '' ? '#dashboard-widgets #postbox-container-1{width:100%!important}' : '')
        . '</style>';
}
