<?php
/**
 * Acceso y gestión desde el portal (HU-24 · RF-14 · RF-15 · UI-09 · UI-10).
 *
 * Pensado para personas con pocos conocimientos informáticos: quien entra con la cuenta del CADUS (o con la de una
 * delegación) no tiene que pasar por el panel de administración de WordPress.
 *  - «Acceso» (/acceso/): inicio de sesión dentro del portal. Los errores vuelven a esta página.
 *  - «Gestión» (/gestion/): cada rol ve solo lo que puede hacer.
 *      Ejecutiva y administrador: nueva noticia, nuevo evento (aparece en el calendario), nueva acta o normativa con su PDF
 *      y gestión de las delegaciones (datos de cada una y relevo de su cuenta).
 *      Delegación: edita solo la ficha de su propia delegación (RN-04).
 *  - El menú muestra «Acceder» a quien no ha entrado y «Gestión» y «Salir» a quien sí.
 *
 * Los permisos son los de WordPress (los mismos que en el panel), así que no se amplía ningún permiso: este módulo solo ofrece
 * formularios más sencillos. Las acciones están separadas en funciones que devuelven el resultado o un WP_Error, para probarlas
 * sin navegador (scripts/pruebas/gestion.php).
 *
 * Privacidad y seguridad: todos los formularios llevan nonce y se comprueban los permisos en el servidor; las páginas no se
 * cachean ni se indexan; el PDF se valida (extensión, tipo real y tamaño).
 */

if (!defined('ABSPATH')) {
    exit;
}

define('CADUS_GESTION_VERSION', '1');
const CADUS_GESTION_PDF_MAX = 10 * MB_IN_BYTES;

add_action('init', 'cadus_gestion_paginas', 40);
add_action('template_redirect', 'cadus_gestion_sin_cache');
add_filter('wp_robots', 'cadus_gestion_sin_indexar');
add_shortcode('cadus_acceso', 'cadus_gestion_acceso');
add_shortcode('cadus_gestion', 'cadus_gestion_panel');
add_filter('wp_nav_menu_items', 'cadus_gestion_menu_sesion', 20, 2);
add_action('wp_login_failed', 'cadus_gestion_login_fallido');
add_action('wp_head', 'cadus_gestion_estilos', 7);
add_action('admin_post_cadus_gestion', 'cadus_gestion_procesar');

/* --------------------------------------------------------------------- páginas y direcciones */

/** Crea «Acceso» y «Gestión» una sola vez por versión (no pisa lo que el equipo cambie después). */
function cadus_gestion_paginas(): void
{
    if (get_option('cadus_gestion_version') === CADUS_GESTION_VERSION || !function_exists('cadus_pagina')) {
        return;
    }
    cadus_pagina('acceso', 'Acceso', cadus_b_sc('[cadus_acceso]'));
    cadus_pagina('gestion', 'Gestión', cadus_b_sc('[cadus_gestion]'));
    update_option('cadus_gestion_version', CADUS_GESTION_VERSION);
}

function cadus_gestion_url_pagina(string $slug): string
{
    $p = get_page_by_path($slug);
    return $p instanceof WP_Post ? (string) get_permalink($p) : ($slug === 'acceso' ? wp_login_url() : home_url('/'));
}

function cadus_gestion_es_pagina(): bool
{
    $p = get_queried_object();
    return $p instanceof WP_Post && (has_shortcode($p->post_content, 'cadus_acceso') || has_shortcode($p->post_content, 'cadus_gestion'));
}

function cadus_gestion_sin_cache(): void
{
    if (cadus_gestion_es_pagina()) {
        if (!defined('DONOTCACHEPAGE')) {
            define('DONOTCACHEPAGE', true);
        }
        nocache_headers();
    }
}

function cadus_gestion_sin_indexar(array $robots): array
{
    if (cadus_gestion_es_pagina()) {
        $robots['noindex'] = true;
        $robots['nofollow'] = true;
    }
    return $robots;
}

/* --------------------------------------------------------------------- qué puede hacer cada rol */

/**
 * Tareas disponibles para un usuario, según los permisos de WordPress.
 * @return string[] noticia, evento, acta, delegaciones (todas), delegacion (solo la suya)
 */
function cadus_gestion_tareas(WP_User $usuario): array
{
    if (!$usuario->exists()) {
        return [];
    }
    $t = [];
    if (user_can($usuario, 'edit_posts')) {
        $t[] = 'noticia';
    }
    if (function_exists('cadus_calendario_activo') && cadus_calendario_activo() && user_can($usuario, 'edit_tribe_events')) {
        $t[] = 'evento';
    }
    if (user_can($usuario, 'create_cadus_actas')) {
        $t[] = 'acta';
    }
    if (user_can($usuario, 'edit_others_cadus_delegacions')) {
        $t[] = 'delegaciones';
    } elseif (user_can($usuario, 'edit_cadus_delegacions')) {
        $t[] = 'delegacion';
    }
    return $t;
}

/* --------------------------------------------------------------------- menú y acceso */

/** «Acceder» para quien no ha entrado; «Gestión» y «Salir» para quien sí (WP Fastest Cache no sirve páginas en caché a quien ha entrado). */
function cadus_gestion_menu_sesion(string $items, $args): string
{
    $lugar = is_object($args) ? (string) ($args->theme_location ?? '') : '';
    if (!in_array($lugar, ['menu_1', 'menu_mobile'], true)) {
        return $items;
    }
    $usuario = wp_get_current_user();
    $enlace = static fn(string $url, string $texto, string $clase = ''): string
        => '<li class="menu-item cadus-menu-sesion ' . esc_attr($clase) . '"><a href="' . esc_url($url) . '" class="ct-menu-link">' . esc_html($texto) . '</a></li>';
    if (!$usuario->exists()) {
        return $items . $enlace(cadus_gestion_url_pagina('acceso'), 'Acceder', 'cadus-menu-acceder');
    }
    if (cadus_gestion_tareas($usuario)) {
        $solo_suya = cadus_gestion_tareas($usuario) === ['delegacion'];
        $items .= $enlace(cadus_gestion_url_pagina('gestion'), $solo_suya ? 'Mi delegación' : 'Gestión', 'cadus-menu-gestion');
    }
    return $items . $enlace(wp_logout_url(home_url('/')), 'Salir', 'cadus-menu-salir');
}

/** Un error de acceso desde la página del portal vuelve a ella en vez de a la pantalla de WordPress. */
function cadus_gestion_login_fallido(): void
{
    if (($_POST['cadus_acceso'] ?? '') === '1') {
        wp_safe_redirect(add_query_arg('acceso', 'error', cadus_gestion_url_pagina('acceso')));
        exit;
    }
}

/** [cadus_acceso]: formulario de inicio de sesión del portal. La autenticación la hace wp-login.php (con Wordfence). */
function cadus_gestion_acceso(): string
{
    $usuario = wp_get_current_user();
    if ($usuario->exists()) {
        $html = '<p>' . esc_html('Has entrado como ' . $usuario->display_name . '.') . '</p><p>';
        if (cadus_gestion_tareas($usuario)) {
            $html .= '<a class="cadus-boton" href="' . esc_url(cadus_gestion_url_pagina('gestion')) . '">Ir a la gestión</a> ';
        }
        return $html . '<a class="cadus-chip" href="' . esc_url(wp_logout_url(home_url('/'))) . '">Salir</a></p>';
    }
    $error = isset($_GET['acceso']) && $_GET['acceso'] === 'error'
        ? '<p class="cadus-aviso cadus-aviso--error" role="alert">' . esc_html('El usuario o la contraseña no son correctos. Si no los recuerdas, usa «¿Has olvidado tu contraseña?».') . '</p>' : '';
    $id = wp_unique_id('cadus_acceso_');
    return '<div class="cadus-gestion cadus-gestion--acceso">' . $error
        . '<p>' . esc_html('Este acceso es para la Ejecutiva del CADUS y para las delegaciones de centro. Los estudiantes no necesitan iniciar sesión: pueden enviar consultas y solicitudes desde Atención al estudiante.') . '</p>'
        . '<form method="post" action="' . esc_url(wp_login_url()) . '" class="cadus-form">'
        . '<input type="hidden" name="redirect_to" value="' . esc_url(cadus_gestion_url_pagina('gestion')) . '">'
        . '<input type="hidden" name="cadus_acceso" value="1">'
        . '<p><label for="' . esc_attr($id) . '_usuario">' . esc_html('Usuario o correo') . '</label>'
        . '<input class="cadus-campo" id="' . esc_attr($id) . '_usuario" name="log" type="text" autocomplete="username" required aria-required="true"></p>'
        . '<p><label for="' . esc_attr($id) . '_clave">' . esc_html('Contraseña') . '</label>'
        . '<input class="cadus-campo" id="' . esc_attr($id) . '_clave" name="pwd" type="password" autocomplete="current-password" required aria-required="true"></p>'
        . '<p><button type="submit" class="cadus-boton">' . esc_html('Entrar') . '</button> '
        . '<a href="' . esc_url(wp_lostpassword_url(cadus_gestion_url_pagina('acceso'))) . '">' . esc_html('¿Has olvidado tu contraseña?') . '</a></p>'
        . '</form></div>';
}

/* --------------------------------------------------------------------- utilidades */

function cadus_gestion_texto(array $d, string $clave, int $max = 200): string
{
    $v = isset($d[$clave]) && is_string($d[$clave]) ? sanitize_text_field(wp_unslash($d[$clave])) : '';
    return mb_substr($v, 0, $max);
}

function cadus_gestion_largo(array $d, string $clave, int $max = 20000): string
{
    $v = isset($d[$clave]) && is_string($d[$clave]) ? trim(wp_unslash($d[$clave])) : '';
    return mb_substr($v, 0, $max);
}

/** Convierte el texto de un cuadro de varias líneas en párrafos seguros. */
function cadus_gestion_html_seguro(string $texto): string
{
    return wp_kses_post(wpautop($texto));
}

/** Guarda un campo de ACF (por clave) o, si ACF no está activo, un metadato con el mismo nombre. */
function cadus_gestion_campo(string $clave_acf, string $nombre, $valor, int $id): void
{
    if (function_exists('update_field')) {
        update_field($clave_acf, $valor, $id);
    } else {
        update_post_meta($id, $nombre, $valor);
    }
}

function cadus_gestion_error(string $codigo, string $mensaje, int $estado = 400): WP_Error
{
    return new WP_Error($codigo, $mensaje, ['status' => $estado]);
}

/** Fecha «AAAA-MM-DD» y hora «HH:MM» en la zona horaria del sitio, o null si no son válidas. */
function cadus_gestion_momento(string $fecha, string $hora): ?DateTimeImmutable
{
    $m = DateTimeImmutable::createFromFormat('!Y-m-d H:i', $fecha . ' ' . $hora, wp_timezone());
    $e = DateTimeImmutable::getLastErrors();
    return $m && (!$e || ($e['warning_count'] === 0 && $e['error_count'] === 0)) ? $m : null;
}

function cadus_gestion_termino(int $id, string $taxonomia): ?WP_Term
{
    $t = $id > 0 ? get_term($id, $taxonomia) : null;
    return $t instanceof WP_Term ? $t : null;
}

/* --------------------------------------------------------------------- acciones (devuelven resultado o WP_Error) */

/** @return array{id:int,url:string,mensaje:string}|WP_Error */
function cadus_gestion_crear_noticia(array $d, WP_User $u)
{
    if (!user_can($u, 'edit_posts')) {
        return cadus_gestion_error('permiso', 'No tienes permiso para crear noticias.', 403);
    }
    $titulo = cadus_gestion_texto($d, 'titulo', 150);
    $texto = cadus_gestion_largo($d, 'texto');
    $cat = cadus_gestion_termino((int) ($d['categoria'] ?? 0), 'category');
    if (mb_strlen($titulo) < 3 || $texto === '' || !$cat) {
        return cadus_gestion_error('datos', 'Escribe el título, el texto y elige la categoría.');
    }
    $publica = user_can($u, 'publish_posts');
    $id = wp_insert_post([
        'post_type' => 'post', 'post_title' => $titulo, 'post_content' => cadus_gestion_html_seguro($texto),
        'post_excerpt' => cadus_gestion_texto($d, 'resumen', 300), 'post_status' => $publica ? 'publish' : 'pending',
        'post_category' => [$cat->term_id], 'post_author' => $u->ID,
    ], true);
    if (is_wp_error($id)) {
        return cadus_gestion_error('guardar', 'No se ha podido guardar la noticia.', 500);
    }
    delete_transient('cadus_portada_datos');
    return ['id' => (int) $id, 'url' => (string) get_permalink($id),
        'mensaje' => $publica ? 'La noticia «' . $titulo . '» está publicada.' : 'La noticia «' . $titulo . '» se ha guardado para su revisión.'];
}

/** @return array{id:int,url:string,mensaje:string}|WP_Error */
function cadus_gestion_crear_evento(array $d, WP_User $u)
{
    if (!function_exists('cadus_calendario_activo') || !cadus_calendario_activo() || !function_exists('tribe_create_event')) {
        return cadus_gestion_error('calendario', 'El calendario no está activo.', 503);
    }
    if (!user_can($u, 'edit_tribe_events')) {
        return cadus_gestion_error('permiso', 'No tienes permiso para crear eventos.', 403);
    }
    $titulo = cadus_gestion_texto($d, 'titulo', 150);
    // La categoría es opcional (un evento general no es ni asamblea ni curso), pero si se indica tiene que existir.
    $id_cat = (int) ($d['categoria'] ?? 0);
    $cat = $id_cat > 0 ? cadus_gestion_termino($id_cat, 'tribe_events_cat') : null;
    $inicio = cadus_gestion_momento(cadus_gestion_texto($d, 'fecha', 10), cadus_gestion_texto($d, 'hora', 5) ?: '10:00');
    if (mb_strlen($titulo) < 3 || ($id_cat > 0 && !$cat) || !$inicio) {
        return cadus_gestion_error('datos', 'Escribe el título y elige la fecha del evento.');
    }
    $fin = $inicio->modify('+1 hour');
    if (cadus_gestion_texto($d, 'hora_fin', 5) !== '' || cadus_gestion_texto($d, 'fecha_fin', 10) !== '') {
        $fin = cadus_gestion_momento(cadus_gestion_texto($d, 'fecha_fin', 10) ?: $inicio->format('Y-m-d'), cadus_gestion_texto($d, 'hora_fin', 5) ?: $inicio->modify('+1 hour')->format('H:i'));
        if (!$fin || $fin <= $inicio) {
            return cadus_gestion_error('datos', 'El final del evento debe ser posterior al principio.');
        }
    }
    $publica = user_can($u, 'publish_tribe_events');
    $args = [
        'post_title' => $titulo, 'post_content' => cadus_gestion_html_seguro(cadus_gestion_largo($d, 'descripcion')),
        'post_status' => $publica ? 'publish' : 'pending', 'post_author' => $u->ID,
        'EventStartDate' => $inicio->format('Y-m-d'), 'EventStartHour' => $inicio->format('H'), 'EventStartMinute' => $inicio->format('i'),
        'EventEndDate' => $fin->format('Y-m-d'), 'EventEndHour' => $fin->format('H'), 'EventEndMinute' => $fin->format('i'),
        'EventTimezone' => wp_timezone_string(),
    ];
    $lugar = cadus_gestion_texto($d, 'lugar', 150);
    if ($lugar !== '') {
        $args['Venue'] = ['Venue' => $lugar];
    }
    $id = tribe_create_event($args);
    if (!$id) {
        return cadus_gestion_error('guardar', 'No se ha podido guardar el evento.', 500);
    }
    if ($cat) {
        wp_set_object_terms((int) $id, [$cat->term_id], 'tribe_events_cat');
    }
    delete_transient('cadus_portada_datos');
    return ['id' => (int) $id, 'url' => (string) get_permalink($id),
        'mensaje' => $publica ? 'El evento «' . $titulo . '» ya está en el calendario.' : 'El evento «' . $titulo . '» se ha guardado para su revisión.'];
}

/**
 * @param array{name?:string,tmp_name?:string,size?:int,error?:int} $archivo
 * @return array{id:int,url:string,mensaje:string}|WP_Error
 */
function cadus_gestion_crear_acta(array $d, array $archivo, WP_User $u)
{
    if (!user_can($u, 'create_cadus_actas') || !user_can($u, 'upload_files')) {
        return cadus_gestion_error('permiso', 'No tienes permiso para crear actas.', 403);
    }
    $titulo = cadus_gestion_texto($d, 'titulo', 150);
    $tipo = cadus_gestion_termino((int) ($d['tipo'] ?? 0), 'cadus_tipo_documento');
    $fecha = cadus_gestion_texto($d, 'fecha', 10);
    if (mb_strlen($titulo) < 3 || !$tipo || !cadus_gestion_momento($fecha, '00:00')) {
        return cadus_gestion_error('datos', 'Escribe el título, la fecha y elige si es un acta o una normativa.');
    }
    $tmp = (string) ($archivo['tmp_name'] ?? '');
    if (($archivo['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK || $tmp === '' || !is_file($tmp)) {
        return cadus_gestion_error('pdf', 'Adjunta el documento en PDF.');
    }
    if ((int) ($archivo['size'] ?? 0) > CADUS_GESTION_PDF_MAX || filesize($tmp) > CADUS_GESTION_PDF_MAX) {
        return cadus_gestion_error('pdf', 'El PDF pesa más de 10 MB.');
    }
    // Si el servidor no puede comprobar el tipo real del archivo, no se acepta: es mejor rechazar que dar por bueno un PDF falso.
    $tipo_real = function_exists('finfo_open') ? (string) finfo_file(finfo_open(FILEINFO_MIME_TYPE), $tmp) : '';
    if (strtolower(pathinfo((string) ($archivo['name'] ?? ''), PATHINFO_EXTENSION)) !== 'pdf' || $tipo_real !== 'application/pdf') {
        return cadus_gestion_error('pdf', 'El archivo debe ser un PDF.');
    }

    $id = wp_insert_post(['post_type' => 'cadus_acta', 'post_title' => $titulo, 'post_status' => 'draft', 'post_author' => $u->ID], true);
    if (is_wp_error($id)) {
        return cadus_gestion_error('guardar', 'No se ha podido guardar el documento.', 500);
    }
    require_once ABSPATH . 'wp-admin/includes/file.php';
    require_once ABSPATH . 'wp-admin/includes/media.php';
    require_once ABSPATH . 'wp-admin/includes/image.php';
    $adjunto = media_handle_sideload(
        ['name' => sanitize_file_name((string) $archivo['name']), 'tmp_name' => $tmp], (int) $id, $titulo
    );
    if (is_wp_error($adjunto)) {
        wp_delete_post((int) $id, true);
        return cadus_gestion_error('pdf', 'No se ha podido guardar el PDF.', 500);
    }
    cadus_gestion_campo('field_cadus_acta_fecha', 'fecha', str_replace('-', '', $fecha), (int) $id);
    cadus_gestion_campo('field_cadus_acta_pleno', 'pleno', cadus_gestion_texto($d, 'pleno', 150), (int) $id);
    cadus_gestion_campo('field_cadus_acta_pdf', 'archivo_pdf', (int) $adjunto, (int) $id);
    wp_set_object_terms((int) $id, [$tipo->term_id], 'cadus_tipo_documento');
    // RN-01: solo quien puede publicar actas (la Ejecutiva) las publica; el resto las deja pendientes de revisión.
    $publica = user_can($u, 'publish_cadus_actas');
    wp_update_post(['ID' => (int) $id, 'post_status' => $publica ? 'publish' : 'pending']);
    return ['id' => (int) $id, 'url' => (string) get_permalink($id),
        'mensaje' => $publica ? '«' . $titulo . '» está publicada en Actas y normativa.' : '«' . $titulo . '» queda pendiente de la aprobación de la Ejecutiva.'];
}

/** Líneas de enlaces válidas (http o https) o null si alguna no lo es. */
function cadus_gestion_enlaces(string $texto): ?string
{
    $limpias = [];
    foreach (array_filter(array_map('trim', preg_split('/\R/', $texto) ?: [])) as $linea) {
        $url = esc_url_raw($linea, ['http', 'https']);
        $host = $url !== '' ? (string) wp_parse_url($url, PHP_URL_HOST) : '';
        if ($host === '' || !str_contains($host, '.') || !filter_var($url, FILTER_VALIDATE_URL)) {
            return null; // no se consulta el DNS: un enlace válido hoy puede no resolverse desde este servidor
        }
        $limpias[] = $url;
    }
    return implode("\n", $limpias);
}

/** Valida y guarda los datos de contacto de una ficha. @return int|WP_Error id de la ficha */
function cadus_gestion_datos_ficha(array $d, int $id)
{
    $correo = cadus_gestion_texto($d, 'correo', 120);
    if ($correo !== '' && !is_email($correo)) {
        return cadus_gestion_error('datos', 'El correo de contacto no es válido.');
    }
    $enlaces = cadus_gestion_enlaces(cadus_gestion_largo($d, 'enlaces', 2000));
    if ($enlaces === null) {
        return cadus_gestion_error('datos', 'Cada enlace de interés debe ser una dirección web completa (empieza por http:// o https://), una por línea.');
    }
    $instagram = cadus_gestion_enlaces(cadus_gestion_texto($d, 'instagram', 200));
    if ($instagram !== null && $instagram !== '' && (!str_starts_with($instagram, 'https://')
        || !in_array(strtolower((string) wp_parse_url($instagram, PHP_URL_HOST)), ['instagram.com', 'www.instagram.com'], true))) {
        $instagram = null; // el campo se muestra como perfil de Instagram: no puede apuntar a otro sitio
    }
    if ($instagram === null) {
        return cadus_gestion_error('datos', 'El Instagram debe ser una dirección de instagram.com que empiece por https://.');
    }
    cadus_gestion_campo('field_cadus_deleg_delegado', 'delegado', cadus_gestion_texto($d, 'delegado', 120), $id);
    cadus_gestion_campo('field_cadus_deleg_correo', 'correo', $correo, $id);
    cadus_gestion_campo('field_cadus_deleg_tel', 'telefono', cadus_gestion_texto($d, 'telefono', 40), $id);
    cadus_gestion_campo('field_cadus_deleg_horario', 'horario', cadus_gestion_texto($d, 'horario', 160), $id);
    cadus_gestion_campo('field_cadus_deleg_enlaces', 'enlaces', $enlaces, $id);
    $miembros = implode("\n", array_filter(array_map(static fn($l) => sanitize_text_field($l), preg_split('/\R/', cadus_gestion_largo($d, 'miembros', 4000)) ?: [])));
    cadus_gestion_campo('field_cadus_deleg_miembros', 'miembros', $miembros, $id);
    cadus_gestion_campo('field_cadus_deleg_instagram', 'instagram', $instagram, $id);
    return $id;
}

/** @return array{id:int,url:string,mensaje:string}|WP_Error */
function cadus_gestion_guardar_delegacion(array $d, WP_User $u)
{
    $id = (int) ($d['ficha'] ?? 0);
    $ficha = $id > 0 ? get_post($id) : null;
    if (!$ficha instanceof WP_Post || $ficha->post_type !== 'cadus_delegacion') {
        return cadus_gestion_error('datos', 'No se encuentra la ficha de la delegación.', 404);
    }
    if (!user_can($u, 'edit_post', $id)) {
        return cadus_gestion_error('permiso', 'Solo puedes editar la ficha de tu propia delegación.', 403);
    }
    // Primero se valida todo y después se escribe: un error no deja la ficha a medio guardar.
    $cuenta = (int) ($d['cuenta'] ?? 0);
    $cambia_cuenta = $cuenta > 0 && $cuenta !== (int) $ficha->post_author && user_can($u, 'edit_others_cadus_delegacions');
    if ($cambia_cuenta) {
        if (!function_exists('cadus_relevo_es_cuenta_delegacion') || !cadus_relevo_es_cuenta_delegacion(get_userdata($cuenta))) {
            return cadus_gestion_error('datos', 'La cuenta elegida no es una cuenta de delegación.');
        }
        if (cadus_relevo_fichas($cuenta)) {
            return cadus_gestion_error('datos', 'Esa cuenta ya tiene una delegación: cada delegación tiene una sola cuenta.');
        }
    }
    $r = cadus_gestion_datos_ficha($d, $id);
    if (is_wp_error($r)) {
        return $r;
    }
    if (user_can($u, 'edit_others_cadus_delegacions')) {
        $titulo = cadus_gestion_texto($d, 'titulo', 150);
        if ($titulo !== '' && $titulo !== $ficha->post_title) {
            wp_update_post(['ID' => $id, 'post_title' => $titulo]);
        }
        $centro = cadus_gestion_termino((int) ($d['centro'] ?? 0), 'cadus_centro');
        if ($centro) {
            wp_set_object_terms($id, [$centro->term_id], 'cadus_centro');
        } elseif (isset($d['centro']) && (int) $d['centro'] === 0) {
            wp_set_object_terms($id, [], 'cadus_centro'); // «Sin asignar»
        }
    }
    if ($cambia_cuenta) {
        wp_update_post(['ID' => $id, 'post_author' => $cuenta]);
    }
    // Los metadatos solos no avisan a la caché de página (WP Fastest Cache escucha transition_post_status): se registra la edición.
    wp_update_post(['ID' => $id]);
    return ['id' => $id, 'url' => (string) get_permalink($id), 'mensaje' => 'Se han guardado los datos de «' . get_the_title($id) . '».'];
}

/** @return array{id:int,url:string,mensaje:string}|WP_Error */
function cadus_gestion_nueva_delegacion(array $d, WP_User $u)
{
    if (!user_can($u, 'create_cadus_delegacions') || !user_can($u, 'publish_cadus_delegacions') || !user_can($u, 'edit_others_cadus_delegacions')) {
        return cadus_gestion_error('permiso', 'No tienes permiso para crear delegaciones.', 403);
    }
    $titulo = cadus_gestion_texto($d, 'titulo', 150);
    $centro = cadus_gestion_termino((int) ($d['centro'] ?? 0), 'cadus_centro');
    if (mb_strlen($titulo) < 3 || !$centro) {
        return cadus_gestion_error('datos', 'Escribe el nombre de la delegación y elige la facultad o escuela.');
    }
    $autor = $u->ID;
    $cuenta = (int) ($d['cuenta'] ?? 0);
    if ($cuenta > 0) {
        $c = get_userdata($cuenta);
        if (!function_exists('cadus_relevo_es_cuenta_delegacion') || !cadus_relevo_es_cuenta_delegacion($c)) {
            return cadus_gestion_error('datos', 'La cuenta elegida no es una cuenta de delegación.');
        }
        if (cadus_relevo_fichas($cuenta)) {
            return cadus_gestion_error('datos', 'Esa cuenta ya tiene una delegación: cada delegación tiene una sola cuenta.');
        }
        $autor = $cuenta;
    }
    $id = wp_insert_post(['post_type' => 'cadus_delegacion', 'post_title' => $titulo, 'post_status' => 'publish', 'post_author' => $autor], true);
    if (is_wp_error($id)) {
        return cadus_gestion_error('guardar', 'No se ha podido crear la delegación.', 500);
    }
    wp_set_object_terms((int) $id, [$centro->term_id], 'cadus_centro');
    $r = cadus_gestion_datos_ficha($d, (int) $id);
    if (is_wp_error($r)) {
        wp_delete_post((int) $id, true);
        return $r;
    }
    return ['id' => (int) $id, 'url' => (string) get_permalink($id), 'mensaje' => 'La delegación «' . $titulo . '» está creada.'];
}

/* --------------------------------------------------------------------- recepción de los formularios */

/** Clave del aviso: por usuario y por sesión, para que dos personas con la cuenta única del CADUS no se lean los avisos. */
function cadus_gestion_clave_msg(): string
{
    return 'cadus_gestion_msg_' . get_current_user_id() . '_' . substr(md5((string) wp_get_session_token()), 0, 12);
}

/** Lo que se escribió en el último formulario con error ([] si no hay): sirve para no obligar a repetirlo. */
function cadus_gestion_previo(?array $nuevo = null): array
{
    static $previo = [];
    if ($nuevo !== null) {
        $previo = $nuevo;
    }
    return $previo;
}

function cadus_gestion_volver(string $tipo, string $texto, string $ancla = '', array $previo = []): void
{
    set_transient(cadus_gestion_clave_msg(), [$tipo, $texto, $previo], 120);
    wp_safe_redirect(cadus_gestion_url_pagina('gestion') . ($ancla !== '' ? '#' . $ancla : ''));
    exit;
}

function cadus_gestion_procesar(): void
{
    $usuario = wp_get_current_user();
    $tarea = isset($_POST['cadus_tarea']) && is_string($_POST['cadus_tarea']) ? sanitize_key(wp_unslash($_POST['cadus_tarea'])) : '';
    $validas = ['noticia', 'evento', 'acta', 'delegacion', 'delegacion_nueva'];
    if (!$usuario->exists() || !in_array($tarea, $validas, true)
        || !wp_verify_nonce(isset($_POST['cadus_nonce']) && is_string($_POST['cadus_nonce']) ? sanitize_text_field(wp_unslash($_POST['cadus_nonce'])) : '', 'cadus_gestion_' . $tarea)) {
        wp_die('La sesión ha caducado o la petición no es válida. Vuelve a la gestión e inténtalo de nuevo.', 'Gestión', ['response' => 403]);
    }
    switch ($tarea) {
        case 'noticia':
            $r = cadus_gestion_crear_noticia($_POST, $usuario);
            $ancla = 'noticia';
            break;
        case 'evento':
            $r = cadus_gestion_crear_evento($_POST, $usuario);
            $ancla = 'evento';
            break;
        case 'acta':
            $f = isset($_FILES['pdf']) && is_array($_FILES['pdf']) ? $_FILES['pdf'] : [];
            $r = $f && !empty($f['tmp_name']) && is_string($f['tmp_name']) && is_uploaded_file($f['tmp_name'])
                ? cadus_gestion_crear_acta($_POST, $f, $usuario)
                : cadus_gestion_error('pdf', 'Adjunta el documento en PDF.');
            $ancla = 'acta';
            break;
        case 'delegacion':
            $r = cadus_gestion_guardar_delegacion($_POST, $usuario);
            $ancla = 'delegaciones';
            break;
        default:
            $r = cadus_gestion_nueva_delegacion($_POST, $usuario);
            $ancla = 'delegaciones';
    }
    if (is_wp_error($r)) {
        // Se conserva lo escrito (menos los secretos y los archivos) para volver a mostrarlo en el formulario.
        $datos = [];
        foreach ($_POST as $k => $v) {
            if (is_string($v) && !in_array($k, ['cadus_nonce', 'action', 'cadus_tarea'], true)) {
                $datos[sanitize_key($k)] = mb_substr(wp_unslash($v), 0, 20000);
            }
        }
        cadus_gestion_volver('error', $r->get_error_message(), $ancla, ['tarea' => $tarea, 'datos' => $datos]);
    }
    cadus_gestion_volver('ok', $r['mensaje'] . ($r['url'] !== '' && !in_array($tarea, ['delegacion'], true) ? ' ' . $r['url'] : ''), $ancla);
}

/* --------------------------------------------------------------------- página de gestión */

function cadus_gestion_mensaje(): string
{
    $clave = cadus_gestion_clave_msg();
    $msg = get_transient($clave);
    if (!is_array($msg)) {
        return '';
    }
    delete_transient($clave);
    cadus_gestion_previo(is_array($msg[2] ?? null) ? $msg[2] : []);
    // El enlace al contenido creado va al final del mensaje: se separa para escapar cada parte.
    $partes = explode(' ', (string) $msg[1]);
    $url = filter_var(end($partes), FILTER_VALIDATE_URL) ? array_pop($partes) : '';
    $texto = implode(' ', $partes);
    $ok = $msg[0] === 'ok';
    return '<div class="cadus-aviso ' . ($ok ? 'cadus-aviso--ok' : 'cadus-aviso--error') . '" role="' . ($ok ? 'status' : 'alert') . '" tabindex="-1" id="cadus-gestion-mensaje">'
        . esc_html($texto) . ($url !== '' ? ' <a href="' . esc_url($url) . '">' . esc_html('Verlo en el portal') . '</a>' : '') . '</div>'
        . '<script>(function(){var m=document.getElementById("cadus-gestion-mensaje");if(m){m.focus();}})();</script>';
}

/** Vuelve a poner en el formulario con error lo que la persona había escrito. */
function cadus_gestion_rellenar(string $html): string
{
    $previo = cadus_gestion_previo();
    if (empty($previo['tarea']) || empty($previo['datos']) || !method_exists('WP_HTML_Tag_Processor', 'set_modifiable_text')) {
        return $html;
    }
    $d = $previo['datos'];
    $p = new WP_HTML_Tag_Processor($html);
    $en = false;
    $select = '';
    while ($p->next_tag()) {
        $tag = $p->get_tag();
        $nombre = (string) $p->get_attribute('name');
        if ($tag === 'INPUT' && $nombre === 'cadus_tarea') {
            $en = $p->get_attribute('value') === $previo['tarea'] && $previo['tarea'] !== 'delegacion';
            continue;
        }
        if ($tag === 'INPUT' && $nombre === 'ficha' && $previo['tarea'] === 'delegacion') {
            $en = (string) $p->get_attribute('value') === (string) ($d['ficha'] ?? '');
            continue;
        }
        if (!$en) {
            continue;
        }
        if ($tag === 'SELECT') {
            $select = $nombre;
        } elseif ($tag === 'OPTION' && $select !== '' && isset($d[$select])) {
            if ((string) $p->get_attribute('value') === (string) $d[$select]) {
                $p->set_attribute('selected', true);
            } else {
                $p->remove_attribute('selected');
            }
        } elseif ($tag === 'TEXTAREA' && isset($d[$nombre])) {
            $p->set_modifiable_text(esc_textarea((string) $d[$nombre])); // set_modifiable_text no escapa: sin esto «</textarea>» rompería el formulario
        } elseif ($tag === 'INPUT' && isset($d[$nombre]) && !in_array((string) $p->get_attribute('type'), ['hidden', 'file', 'password'], true)) {
            $p->set_attribute('value', (string) $d[$nombre]);
        }
    }
    return $p->get_updated_html();
}

function cadus_gestion_campo_html(string $id, string $etiqueta, string $nombre, string $tipo = 'text', string $valor = '', bool $obligatorio = false, string $ayuda = ''): string
{
    $desc = $ayuda !== '' ? ' aria-describedby="' . esc_attr($id . '_ayuda') . '"' : '';
    $req = $obligatorio ? ' required aria-required="true"' : '';
    $entrada = $tipo === 'textarea'
        ? '<textarea class="cadus-campo" id="' . esc_attr($id) . '" name="' . esc_attr($nombre) . '" rows="5"' . $req . $desc . '>' . esc_textarea($valor) . '</textarea>'
        : '<input class="cadus-campo" id="' . esc_attr($id) . '" name="' . esc_attr($nombre) . '" type="' . esc_attr($tipo) . '" value="' . esc_attr($valor) . '"' . $req . $desc . '>';
    return '<p class="cadus-form__fila"><label for="' . esc_attr($id) . '">' . esc_html($etiqueta) . ($obligatorio ? ' <span class="cadus-obligatorio">(obligatorio)</span>' : '') . '</label>'
        . $entrada . ($ayuda !== '' ? '<small id="' . esc_attr($id . '_ayuda') . '">' . esc_html($ayuda) . '</small>' : '') . '</p>';
}

/** @param array<int,string> $opciones id => nombre */
function cadus_gestion_select_html(string $id, string $etiqueta, string $nombre, array $opciones, int $actual = 0, bool $obligatorio = true, string $vacio = 'Elige una opción'): string
{
    $o = '<option value="">' . esc_html($vacio) . '</option>';
    foreach ($opciones as $valor => $texto) {
        $o .= '<option value="' . esc_attr((string) $valor) . '"' . selected($actual, $valor, false) . '>' . esc_html($texto) . '</option>';
    }
    return '<p class="cadus-form__fila"><label for="' . esc_attr($id) . '">' . esc_html($etiqueta) . ($obligatorio ? ' <span class="cadus-obligatorio">(obligatorio)</span>' : '') . '</label>'
        . '<select class="cadus-campo" id="' . esc_attr($id) . '" name="' . esc_attr($nombre) . '"' . ($obligatorio ? ' required aria-required="true"' : '') . '>' . $o . '</select></p>';
}

function cadus_gestion_terminos(string $taxonomia, array $excluir = []): array
{
    $t = get_terms(['taxonomy' => $taxonomia, 'hide_empty' => false, 'orderby' => 'name']);
    $r = [];
    foreach (is_array($t) ? $t : [] as $x) {
        if ($x instanceof WP_Term && !in_array($x->slug, $excluir, true)) {
            $r[$x->term_id] = $x->name;
        }
    }
    return $r;
}

function cadus_gestion_formulario(string $tarea, string $contenido, string $boton, bool $archivos = false): string
{
    return '<form method="post" action="' . esc_url(admin_url('admin-post.php')) . '" class="cadus-form"' . ($archivos ? ' enctype="multipart/form-data"' : '') . '>'
        . '<input type="hidden" name="action" value="cadus_gestion"><input type="hidden" name="cadus_tarea" value="' . esc_attr($tarea) . '">'
        . '<input type="hidden" name="cadus_nonce" value="' . esc_attr(wp_create_nonce('cadus_gestion_' . $tarea)) . '">'
        . $contenido . '<p><button type="submit" class="cadus-boton">' . esc_html($boton) . '</button></p></form>';
}

function cadus_gestion_seccion_noticia(): string
{
    $c = cadus_gestion_terminos('category', ['uncategorized', 'sin-categoria']);
    return '<section class="cadus-gestion__seccion" id="noticia" aria-labelledby="noticia-t"><h2 id="noticia-t">Nueva noticia o comunicado</h2>'
        . '<p>Aparece en «Noticias y comunicados» y en la portada.</p>'
        . cadus_gestion_formulario('noticia',
            cadus_gestion_campo_html('g_not_titulo', 'Título', 'titulo', 'text', '', true)
            . cadus_gestion_select_html('g_not_cat', 'Categoría', 'categoria', $c)
            . cadus_gestion_campo_html('g_not_resumen', 'Resumen (una frase)', 'resumen', 'text', '', false, 'Se muestra en el listado de noticias.')
            . cadus_gestion_campo_html('g_not_texto', 'Texto', 'texto', 'textarea', '', true, 'Separa los párrafos con una línea en blanco.'),
            'Publicar la noticia')
        . '</section>';
}

function cadus_gestion_seccion_evento(): string
{
    $c = cadus_gestion_terminos('tribe_events_cat');
    return '<section class="cadus-gestion__seccion" id="evento" aria-labelledby="evento-t"><h2 id="evento-t">Nuevo evento del calendario</h2>'
        . '<p>Aparece en el calendario y en «Próximos eventos» de la portada.</p>'
        . cadus_gestion_formulario('evento',
            cadus_gestion_campo_html('g_ev_titulo', 'Título', 'titulo', 'text', '', true)
            . cadus_gestion_select_html('g_ev_cat', 'Tipo de evento', 'categoria', $c, 0, false, 'Evento general (sin tipo)')
            . cadus_gestion_campo_html('g_ev_fecha', 'Fecha', 'fecha', 'date', '', true)
            . cadus_gestion_campo_html('g_ev_hora', 'Hora de inicio', 'hora', 'time', '10:00', true)
            . cadus_gestion_campo_html('g_ev_fecha_fin', 'Fecha de fin', 'fecha_fin', 'date', '', false, 'Solo si termina otro día.')
            . cadus_gestion_campo_html('g_ev_hora_fin', 'Hora de fin', 'hora_fin', 'time', '', false, 'Si la dejas vacía, dura una hora.')
            . cadus_gestion_campo_html('g_ev_lugar', 'Lugar', 'lugar', 'text')
            . cadus_gestion_campo_html('g_ev_desc', 'Descripción', 'descripcion', 'textarea'),
            'Añadir al calendario')
        . '</section>';
}

function cadus_gestion_seccion_acta(): string
{
    $t = cadus_gestion_terminos('cadus_tipo_documento');
    return '<section class="cadus-gestion__seccion" id="acta" aria-labelledby="acta-t"><h2 id="acta-t">Nueva acta o normativa</h2>'
        . '<p>Se publica en «Actas y normativa» con su PDF para descargar.</p>'
        . cadus_gestion_formulario('acta',
            cadus_gestion_campo_html('g_ac_titulo', 'Título', 'titulo', 'text', '', true)
            . cadus_gestion_select_html('g_ac_tipo', 'Tipo de documento', 'tipo', $t)
            . cadus_gestion_campo_html('g_ac_fecha', 'Fecha del documento', 'fecha', 'date', '', true)
            . cadus_gestion_campo_html('g_ac_pleno', 'Pleno asociado', 'pleno', 'text', '', false, 'Por ejemplo: Pleno ordinario de octubre.')
            . '<p class="cadus-form__fila"><label for="g_ac_pdf">Archivo PDF <span class="cadus-obligatorio">(obligatorio)</span></label>'
            . '<input class="cadus-campo" id="g_ac_pdf" name="pdf" type="file" accept="application/pdf,.pdf" required aria-required="true" aria-describedby="g_ac_pdf_ayuda">'
            . '<small id="g_ac_pdf_ayuda">Solo PDF, hasta 10 MB.</small></p>',
            'Publicar el documento', true)
        . '</section>';
}

/** @param array<int,string> $libres cuentas de delegación que todavía no tienen ficha (id => nombre) */
function cadus_gestion_ficha_html(WP_Post $f, WP_User $u, array $centros, array $libres = []): string
{
    $id = (int) $f->ID;
    $centro_actual = wp_get_post_terms($id, 'cadus_centro', ['fields' => 'ids']);
    $ejecutiva = user_can($u, 'edit_others_cadus_delegacions');
    $autor = get_userdata((int) $f->post_author);
    $campos = '<input type="hidden" name="ficha" value="' . esc_attr((string) $id) . '">';
    if ($ejecutiva) {
        $campos .= cadus_gestion_campo_html("g_d{$id}_titulo", 'Nombre de la delegación', 'titulo', 'text', $f->post_title, true)
            . cadus_gestion_select_html("g_d{$id}_centro", 'Facultad o escuela', 'centro', $centros, is_array($centro_actual) && $centro_actual ? (int) $centro_actual[0] : 0, false, 'Sin asignar');
        if ($libres) {
            $campos .= cadus_gestion_select_html("g_d{$id}_cuenta", 'Pasar la ficha a otra cuenta de delegación', 'cuenta', $libres, 0, false, 'Sin cambios');
        }
    }
    $campos .= cadus_gestion_campo_html("g_d{$id}_delegado", 'Delegado o delegada actual', 'delegado', 'text', (string) cadus_campo('delegado', $id))
        . cadus_gestion_campo_html("g_d{$id}_correo", 'Correo de contacto', 'correo', 'email', (string) cadus_campo('correo', $id))
        . cadus_gestion_campo_html("g_d{$id}_tel", 'Teléfono', 'telefono', 'text', (string) cadus_campo('telefono', $id))
        . cadus_gestion_campo_html("g_d{$id}_horario", 'Horario de atención', 'horario', 'text', (string) cadus_campo('horario', $id))
        . cadus_gestion_campo_html("g_d{$id}_insta", 'Instagram', 'instagram', 'text', (string) cadus_campo('instagram', $id), false, 'Dirección completa, por ejemplo https://www.instagram.com/tu_delegacion')
        . cadus_gestion_campo_html("g_d{$id}_miembros", 'Miembros de la delegación', 'miembros', 'textarea', (string) cadus_campo('miembros', $id), false, 'Uno por línea: apellidos, nombre.')
        . cadus_gestion_campo_html("g_d{$id}_enlaces", 'Enlaces de interés', 'enlaces', 'textarea', (string) cadus_campo('enlaces', $id), false, 'Uno por línea, con la dirección completa (https://…).');
    $cuenta = '';
    if ($ejecutiva && cadus_relevo_es_cuenta_delegacion($autor)) {
        $cuenta = '<p class="cadus-gestion__cuenta">Cuenta de la delegación: <code>' . esc_html($autor->user_login) . '</code> (' . esc_html($autor->user_email) . '). '
            . '<a href="' . esc_url(admin_url(CADUS_RELEVO_PADRE . '&page=' . CADUS_RELEVO_PAGINA)) . '">Cambiar el equipo de la cuenta (relevo)</a></p>';
    }
    $delegado = (string) cadus_campo('delegado', $id);
    return '<details class="cadus-gestion__ficha"' . (!$ejecutiva || (($previo = cadus_gestion_previo())['tarea'] ?? '') === 'delegacion' && (string) ($previo['datos']['ficha'] ?? '') === (string) $id ? ' open' : '') . '><summary>' . esc_html($f->post_title)
        . ($delegado !== '' ? ' — ' . esc_html($delegado) : ' — ' . esc_html('delegado por completar')) . '</summary>'
        . $cuenta . cadus_gestion_formulario('delegacion', $campos, 'Guardar los datos') . '</details>';
}

function cadus_gestion_seccion_delegaciones(WP_User $u, bool $todas): string
{
    $fichas = $todas
        ? get_posts(['post_type' => 'cadus_delegacion', 'post_status' => ['publish', 'draft', 'pending'], 'numberposts' => -1, 'orderby' => 'title', 'order' => 'ASC'])
        : cadus_relevo_fichas($u->ID);
    $centros = cadus_gestion_terminos('cadus_centro');
    $libres = [];
    if ($todas) {
        foreach (get_users(['role' => 'cadus_delegado', 'orderby' => 'display_name']) as $c) {
            if (cadus_relevo_es_cuenta_delegacion($c) && !cadus_relevo_fichas($c->ID)) {
                $libres[$c->ID] = $c->display_name . ' (' . $c->user_login . ')';
            }
        }
    }
    $html = '<section class="cadus-gestion__seccion" id="delegaciones" aria-labelledby="deleg-t"><h2 id="deleg-t">'
        . ($todas ? 'Delegaciones' : 'Mi delegación') . '</h2>';
    $html .= $todas
        ? '<p>' . esc_html(count($fichas) . ' delegaciones. Abre una para cambiar su delegado, su contacto o su horario.') . '</p>'
        : '<p>Estos son los datos que ve el público. Solo puedes editar los de tu delegación.</p>';
    foreach ($fichas as $f) {
        if ($f instanceof WP_Post && user_can($u, 'edit_post', $f->ID)) {
            $html .= cadus_gestion_ficha_html($f, $u, $centros, $libres);
        }
    }
    if (!$fichas) {
        $html .= '<p class="cadus-aviso">No hay ninguna ficha asignada a esta cuenta. Pide a la Ejecutiva que la asigne.</p>';
    }
    if ($todas && user_can($u, 'create_cadus_delegacions')) {
        $cuentas = $libres;
        $html .= '<details class="cadus-gestion__ficha"' . ((cadus_gestion_previo()['tarea'] ?? '') === 'delegacion_nueva' ? ' open' : '') . '><summary>Añadir una delegación nueva</summary>'
            . cadus_gestion_formulario('delegacion_nueva',
                cadus_gestion_campo_html('g_dn_titulo', 'Nombre de la delegación', 'titulo', 'text', '', true)
                . cadus_gestion_select_html('g_dn_centro', 'Facultad o escuela', 'centro', $centros)
                . cadus_gestion_select_html('g_dn_cuenta', 'Cuenta de la delegación', 'cuenta', $cuentas, 0, false, 'Sin cuenta todavía')
                . cadus_gestion_campo_html('g_dn_delegado', 'Delegado o delegada actual', 'delegado')
                . cadus_gestion_campo_html('g_dn_correo', 'Correo de contacto', 'correo', 'email')
                . cadus_gestion_campo_html('g_dn_tel', 'Teléfono', 'telefono')
                . cadus_gestion_campo_html('g_dn_horario', 'Horario de atención', 'horario')
                . cadus_gestion_campo_html('g_dn_insta', 'Instagram', 'instagram', 'text', '', false, 'Dirección completa, por ejemplo https://www.instagram.com/tu_delegacion')
                . cadus_gestion_campo_html('g_dn_miembros', 'Miembros de la delegación', 'miembros', 'textarea', '', false, 'Uno por línea: apellidos, nombre.')
                . cadus_gestion_campo_html('g_dn_enlaces', 'Enlaces de interés', 'enlaces', 'textarea', '', false, 'Uno por línea, con la dirección completa (https://…).'),
                'Crear la delegación')
            . '</details>';
    }
    return $html . '</section>';
}

/** [cadus_gestion]: cada rol ve solo lo que puede hacer. */
function cadus_gestion_panel(): string
{
    $u = wp_get_current_user();
    if (!$u->exists()) {
        return '<div class="cadus-gestion"><p>' . esc_html('Para gestionar el portal tienes que iniciar sesión.') . '</p>'
            . '<p><a class="cadus-boton" href="' . esc_url(cadus_gestion_url_pagina('acceso')) . '">Acceder</a></p></div>';
    }
    $tareas = cadus_gestion_tareas($u);
    if (!$tareas) {
        return '<div class="cadus-gestion"><p class="cadus-aviso">' . esc_html('Tu cuenta no tiene tareas de gestión en el portal.') . '</p></div>';
    }
    $nombres = ['noticia' => ['noticia', 'Nueva noticia'], 'evento' => ['evento', 'Nuevo evento'], 'acta' => ['acta', 'Nueva acta o normativa'],
        'delegaciones' => ['delegaciones', 'Delegaciones'], 'delegacion' => ['delegaciones', 'Mi delegación']];
    $indice = '';
    foreach ($tareas as $t) {
        $indice .= '<li><a class="cadus-chip" href="#' . esc_attr($nombres[$t][0]) . '">' . esc_html($nombres[$t][1]) . '</a></li>';
    }
    $html = '<div class="cadus-gestion">' . cadus_gestion_mensaje()
        . '<p>' . esc_html('Has entrado como ' . $u->display_name . '. Aquí tienes lo que puedes hacer sin entrar en el panel de administración.') . '</p>'
        . '<nav aria-label="' . esc_attr('Tareas de gestión') . '"><ul class="cadus-gestion__indice">' . $indice . '</ul></nav>';
    foreach ($tareas as $t) {
        $html .= match ($t) {
            'noticia' => cadus_gestion_seccion_noticia(),
            'evento' => cadus_gestion_seccion_evento(),
            'acta' => cadus_gestion_seccion_acta(),
            'delegaciones' => cadus_gestion_seccion_delegaciones($u, true),
            default => cadus_gestion_seccion_delegaciones($u, false),
        };
    }
    return cadus_gestion_rellenar($html) . '<p><a class="cadus-chip" href="' . esc_url(wp_logout_url(home_url('/'))) . '">Salir</a></p></div>';
}

function cadus_gestion_estilos(): void
{
    if (!cadus_gestion_es_pagina()) {
        return;
    }
    echo '<style id="cadus-gestion">'
        . '.cadus-gestion{max-width:860px}.cadus-gestion__indice{list-style:none;display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:16px 0 28px}'
        . '.cadus-gestion__seccion{border:1px solid #cfcfcf;border-radius:10px;padding:20px 22px;margin:0 0 28px;background:#fff;scroll-margin-top:90px}'
        . '.cadus-gestion__seccion h2{margin-top:0;color:#8d0739}.cadus-form__fila{display:flex;flex-direction:column;gap:6px;margin:0 0 16px}'
        . '.cadus-form label{font-weight:700;color:#222}.cadus-obligatorio{font-weight:400;color:#595959}.cadus-form small{color:#595959}'
        . '.cadus-gestion .cadus-campo{width:100%;min-height:44px;padding:10px 12px;border:2px solid #595959;border-radius:6px;font:inherit;background:#fff;color:#222}'
        . '.cadus-gestion textarea.cadus-campo{min-height:120px}'
        . '.cadus-gestion button.cadus-boton{min-height:44px;border:0;cursor:pointer;background:#8d0739;color:#fff!important;font:inherit;font-weight:700;padding:10px 24px;border-radius:6px}'
        . '.cadus-gestion button.cadus-boton:hover{background:#6b052b}'
        . '.cadus-gestion a:focus-visible,.cadus-gestion button:focus-visible,.cadus-gestion input:focus-visible,.cadus-gestion select:focus-visible,.cadus-gestion textarea:focus-visible,.cadus-gestion summary:focus-visible,.cadus-aviso:focus-visible{outline:3px solid #1a1a1a;outline-offset:3px;box-shadow:0 0 0 6px #faba09}'
        . '.cadus-gestion__ficha{border:1px solid #cfcfcf;border-radius:8px;margin:0 0 12px;padding:4px 16px;background:#fafafa}'
        . '.cadus-gestion__ficha summary{cursor:pointer;font-weight:700;padding:12px 0;min-height:44px}.cadus-gestion__cuenta{color:#333}'
        . '.cadus-aviso--ok{border-left-color:#1b5e20;background:#e8f5e9;color:#10300f}.cadus-aviso--error{border-left-color:#b3261e;background:#fdecea;color:#5f1511}'
        . '@media (prefers-reduced-motion:reduce){.cadus-gestion *{transition:none!important;animation:none!important}}'
        . '</style>';
}
