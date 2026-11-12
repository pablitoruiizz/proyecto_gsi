<?php
/**
 * Relevo de la cuenta de una delegación (HU-22 · RF-14 · RN-04).
 *
 * Modelo (decidido con el CADUS el 09/11/2026): hay UNA cuenta por delegación, con el correo institucional
 * de la delegación. La cuenta representa a la delegación, no a la persona, así que en el relevo no se crea
 * ni se borra ninguna cuenta: la misma cuenta pasa al equipo entrante. Con ello la ficha, sus entradas y
 * el historial siguen donde estaban y la delegación nunca tiene dos cuentas activas.
 *
 * Quién puede hacerlo, con efecto inmediato:
 *  - El delegado saliente, solo sobre la cuenta con la que ha entrado (su propia delegación).
 *  - Cualquier miembro de la Ejecutiva (cuenta `cadus` o rol Ejecutivo) sobre cualquier cuenta de delegación.
 *  Nunca sobre cuentas de administrador, de la Ejecutiva o con varios roles.
 *
 * Qué hace:
 *  - «Contraseña nueva»: pone la contraseña que se indica (se entrega en mano al equipo entrante).
 *    No necesita correo, así que funciona también en un servidor sin correo saliente.
 *  - «Enlace al correo de la delegación»: pone una contraseña aleatoria que nadie conoce y envía el enlace
 *    para elegir una nueva (necesita correo saliente, p. ej. SMTP con dcadus@us.es).
 *  En los dos casos se cierran TODAS las sesiones abiertas de la cuenta, así que el equipo anterior pierde
 *  el acceso en ese momento, también en otros navegadores y móviles.
 *
 * Privacidad: la contraseña no se guarda en claro ni se muestra después. El historial del relevo solo
 * guarda la fecha, el modo y la cuenta que lo hizo (no nombres de personas).
 */

if (!defined('ABSPATH')) {
    exit;
}

const CADUS_RELEVO_PAGINA = 'cadus-relevo';
const CADUS_RELEVO_PADRE = 'edit.php?post_type=cadus_delegacion';
const CADUS_RELEVO_MIN = 12; // longitud mínima de la contraseña nueva

add_action('admin_menu', 'cadus_relevo_menu');
add_action('admin_post_cadus_relevo', 'cadus_relevo_procesar');
add_filter('login_message', 'cadus_relevo_mensaje_login');
add_filter('cadus_menus_admin', function (array $menus, string $rol): array {
    // La lista cerrada de HU-19a quita los submenús que no conoce: se añade aquí el del relevo.
    if (in_array($rol, ['cadus_delegado', 'cadus_ejecutiva'], true) && isset($menus[CADUS_RELEVO_PADRE])) {
        $menus[CADUS_RELEVO_PADRE][] = CADUS_RELEVO_PAGINA;
    }
    return $menus;
}, 20, 2);

/** La Ejecutiva gestiona el relevo de cualquier delegación; el administrador también. */
function cadus_relevo_es_ejecutiva(?WP_User $usuario = null): bool
{
    $usuario = $usuario ?: wp_get_current_user();
    return $usuario->exists() && (in_array('administrator', $usuario->roles, true) || in_array('cadus_ejecutiva', $usuario->roles, true));
}

/** Solo las cuentas que son únicamente de delegación pueden pasar por el relevo. */
function cadus_relevo_es_cuenta_delegacion($usuario): bool
{
    return $usuario instanceof WP_User && $usuario->exists() && array_values($usuario->roles) === ['cadus_delegado'];
}

/** ¿Puede $actor hacer el relevo de la cuenta $cuenta? */
function cadus_relevo_puede(WP_User $actor, $cuenta): bool
{
    if (!cadus_relevo_es_cuenta_delegacion($cuenta)) {
        return false;
    }
    if (cadus_relevo_es_ejecutiva($actor)) {
        return true;
    }
    // El delegado solo sobre su propia cuenta, que es la de su delegación.
    return cadus_relevo_es_cuenta_delegacion($actor) && $actor->ID === $cuenta->ID;
}

/** Fichas de delegación de las que es autora una cuenta. */
function cadus_relevo_fichas(int $usuario_id): array
{
    return get_posts(['post_type' => 'cadus_delegacion', 'post_status' => 'any', 'author' => $usuario_id,
        'numberposts' => -1, 'orderby' => 'title', 'order' => 'ASC']);
}

function cadus_relevo_menu(): void
{
    $usuario = wp_get_current_user();
    if (!cadus_relevo_es_ejecutiva($usuario) && !cadus_relevo_es_cuenta_delegacion($usuario)) {
        return;
    }
    add_submenu_page(CADUS_RELEVO_PADRE, 'Relevo de la cuenta', 'Relevo de la cuenta', 'read', CADUS_RELEVO_PAGINA, 'cadus_relevo_pagina');
}

/** Pantalla del relevo: el delegado ve su cuenta; la Ejecutiva, todas las de delegación. */
function cadus_relevo_pagina(): void
{
    $actor = wp_get_current_user();
    $ejecutiva = cadus_relevo_es_ejecutiva($actor);
    if (!$ejecutiva && !cadus_relevo_es_cuenta_delegacion($actor)) {
        wp_die('No tienes permisos para hacer relevos.', 'Acceso denegado', ['response' => 403]);
    }
    $cuentas = $ejecutiva ? get_users(['role' => 'cadus_delegado', 'orderby' => 'display_name']) : [$actor];
    $cuentas = array_values(array_filter($cuentas, 'cadus_relevo_es_cuenta_delegacion'));

    echo '<div class="wrap"><h1>Relevo de la cuenta de la delegación</h1>';
    cadus_relevo_aviso();
    echo '<p>La cuenta es de la <strong>delegación</strong>, no de la persona: en el relevo no se crea otra cuenta, '
        . 'sino que esta pasa al equipo entrante con una contraseña nueva. Al hacerlo se cierran todas sus sesiones '
        . 'y el equipo anterior pierde el acceso en ese momento. La ficha de la delegación sigue en la misma cuenta.</p>';

    if ($ejecutiva) {
        cadus_relevo_tabla($cuentas);
    }
    if (!$cuentas) {
        echo '<p>No hay cuentas de delegación. Se crean desde <em>Usuarios › Añadir nuevo</em> o con <code>scripts/roles/aplicar_usuarios.php</code>.</p></div>';
        return;
    }

    $sugerida = wp_generate_password(16, false);
    echo '<h2>' . ($ejecutiva ? 'Hacer un relevo' : 'Pasar la cuenta al equipo entrante') . '</h2>';
    echo '<form method="post" action="' . esc_url(admin_url('admin-post.php')) . '">';
    echo '<input type="hidden" name="action" value="cadus_relevo">';
    wp_nonce_field('cadus_relevo', 'cadus_relevo_nonce');
    echo '<table class="form-table" role="presentation"><tbody>';

    echo '<tr><th scope="row"><label for="cadus-relevo-cuenta">Cuenta</label></th><td>';
    if ($ejecutiva) {
        echo '<select name="cuenta" id="cadus-relevo-cuenta" required><option value="">Elige la delegación…</option>';
        foreach ($cuentas as $c) {
            $fichas = wp_list_pluck(cadus_relevo_fichas($c->ID), 'post_title');
            echo '<option value="' . esc_attr((string) $c->ID) . '">' . esc_html(($fichas ? implode(', ', $fichas) : $c->display_name) . " ({$c->user_login})") . '</option>';
        }
        echo '</select>';
    } else {
        $fichas = wp_list_pluck(cadus_relevo_fichas($actor->ID), 'post_title');
        echo '<input type="hidden" name="cuenta" value="' . esc_attr((string) $actor->ID) . '">';
        echo '<strong>' . esc_html($fichas ? implode(', ', $fichas) : $actor->display_name) . '</strong> · usuario <code>' . esc_html($actor->user_login) . '</code> · ' . esc_html($actor->user_email);
        if (!$fichas) {
            echo '<p class="description">Esta cuenta aún no tiene asignada ninguna ficha de delegación: pídeselo a la Ejecutiva.</p>';
        }
    }
    echo '</td></tr>';

    echo '<tr><th scope="row">Cómo se entrega</th><td><fieldset>'
        . '<label><input type="radio" name="modo" value="contrasena" checked> <strong>Contraseña nueva</strong>: la escribes aquí y se la das en mano al equipo entrante (no necesita correo).</label><br>'
        . '<label><input type="radio" name="modo" value="enlace"> <strong>Enlace al correo de la delegación</strong>: el equipo entrante elige su contraseña desde el correo (necesita correo saliente en el servidor).</label>'
        . '</fieldset></td></tr>';

    echo '<tr><th scope="row"><label for="cadus-relevo-clave">Contraseña nueva</label></th><td>'
        . '<input type="text" class="regular-text code" name="clave" id="cadus-relevo-clave" value="' . esc_attr($sugerida) . '" autocomplete="new-password" spellcheck="false" minlength="' . CADUS_RELEVO_MIN . '">'
        . '<p class="description">Te proponemos una al azar; puedes cambiarla (mínimo ' . CADUS_RELEVO_MIN . ' caracteres). Anótala antes de confirmar: después no se vuelve a mostrar. Solo se usa con «Contraseña nueva».</p></td></tr>';

    echo '<tr><th scope="row">Confirmación</th><td><label><input type="checkbox" name="confirmo" value="1" required> '
        . esc_html($ejecutiva ? 'Entiendo que el equipo actual de esa delegación perderá el acceso ahora mismo.' : 'Entiendo que perderé el acceso ahora mismo, también en esta sesión.')
        . '</label></td></tr>';
    echo '</tbody></table>';
    submit_button('Hacer el relevo', 'primary', 'submit', true);
    echo '</form></div>';
}

/** Tabla de la Ejecutiva: una fila por cuenta, con sus fichas y el último relevo; avisa de fichas sin cuenta. */
function cadus_relevo_tabla(array $cuentas): void
{
    echo '<h2>Cuentas de las delegaciones</h2><table class="widefat striped"><thead><tr>'
        . '<th>Delegación</th><th>Usuario</th><th>Correo</th><th>Último relevo</th></tr></thead><tbody>';
    foreach ($cuentas as $c) {
        $fichas = wp_list_pluck(cadus_relevo_fichas($c->ID), 'post_title');
        $historial = (array) get_user_meta($c->ID, 'cadus_relevos', true);
        $ultimo = end($historial);
        echo '<tr><td>' . ($fichas ? esc_html(implode(', ', $fichas)) : '<em>Sin ficha asignada</em>') . '</td>'
            . '<td><code>' . esc_html($c->user_login) . '</code></td><td>' . esc_html($c->user_email) . '</td>'
            . '<td>' . (is_array($ultimo) && !empty($ultimo['fecha'])
                ? esc_html(wp_date('d/m/Y H:i', (int) $ultimo['fecha']) . ' · ' . ($ultimo['modo'] === 'enlace' ? 'enlace por correo' : 'contraseña nueva') . ' · por ' . $ultimo['por'])
                : '—') . '</td></tr>';
    }
    echo '</tbody></table>';

    // Una sola cuenta activa por delegación: las fichas sin cuenta de delegación quedan señaladas.
    $huerfanas = [];
    foreach (get_posts(['post_type' => 'cadus_delegacion', 'post_status' => 'any', 'numberposts' => -1, 'orderby' => 'title', 'order' => 'ASC']) as $ficha) {
        if (!cadus_relevo_es_cuenta_delegacion(get_userdata((int) $ficha->post_author))) {
            $huerfanas[] = $ficha->post_title;
        }
    }
    if ($huerfanas) {
        echo '<p class="description">' . esc_html(sprintf('%d ficha(s) sin cuenta de delegación (las edita la Ejecutiva): %s.', count($huerfanas), implode(', ', $huerfanas))) . '</p>';
    }
}

/** Procesa el formulario. Todas las comprobaciones se repiten aquí, en el servidor. */
function cadus_relevo_procesar(): void
{
    $actor = wp_get_current_user();
    if (!$actor->exists() || !check_admin_referer('cadus_relevo', 'cadus_relevo_nonce')) {
        wp_die('Sesión caducada. Vuelve a intentarlo.', 'Relevo', ['response' => 403]);
    }
    $cuenta = get_userdata(absint($_POST['cuenta'] ?? 0));
    if (!cadus_relevo_puede($actor, $cuenta)) {
        wp_die('Solo puedes hacer el relevo de la cuenta de tu propia delegación.', 'Acceso denegado', ['response' => 403]);
    }
    $modo = sanitize_key(wp_unslash($_POST['modo'] ?? ''));
    if (!in_array($modo, ['contrasena', 'enlace'], true)) {
        cadus_relevo_volver('error', 'Elige cómo se entrega la cuenta.');
    }
    if (empty($_POST['confirmo'])) {
        cadus_relevo_volver('error', 'Marca la casilla de confirmación.');
    }

    if ($modo === 'contrasena') {
        // Las contraseñas no se sanean (cambiaría su valor): solo se quitan las barras que añade WordPress.
        $clave = (string) wp_unslash($_POST['clave'] ?? '');
        if (mb_strlen($clave) < CADUS_RELEVO_MIN || trim($clave) !== $clave) {
            cadus_relevo_volver('error', sprintf('La contraseña debe tener al menos %d caracteres y no empezar ni terminar con espacios.', CADUS_RELEVO_MIN));
        }
        wp_set_password($clave, $cuenta->ID);
    } else {
        // Contraseña aleatoria que nadie conoce: el equipo anterior no puede seguir entrando mientras llega el enlace.
        wp_set_password(wp_generate_password(32, true, true), $cuenta->ID);
        $enviado = retrieve_password($cuenta->user_login);
    }
    // Efecto inmediato: fuera todas las sesiones de la cuenta, en cualquier navegador o dispositivo.
    WP_Session_Tokens::get_instance($cuenta->ID)->destroy_all();

    $historial = array_slice(array_filter((array) get_user_meta($cuenta->ID, 'cadus_relevos', true), 'is_array'), -19);
    $historial[] = ['fecha' => time(), 'modo' => $modo, 'por' => $actor->ID === $cuenta->ID ? 'la propia delegación' : $actor->user_login];
    update_user_meta($cuenta->ID, 'cadus_relevos', $historial);
    do_action('cadus_relevo_hecho', $cuenta->ID, $actor->ID, $modo);

    $sin_correo = $modo === 'enlace' && is_wp_error($enviado ?? null);
    if ($actor->ID === $cuenta->ID) {
        // El delegado saliente se ha quedado sin sesión: se le lleva al acceso con un aviso.
        wp_clear_auth_cookie();
        wp_safe_redirect(add_query_arg('cadus_relevo', $sin_correo ? 'sin-correo' : 'hecho', wp_login_url()));
        exit;
    }
    if ($sin_correo) {
        cadus_relevo_volver('aviso', "Relevo hecho y sesiones cerradas, pero el correo no se ha podido enviar a {$cuenta->user_email}. Repite el relevo con «Contraseña nueva».");
    }
    cadus_relevo_volver('ok', $modo === 'enlace'
        ? "Relevo hecho: sesiones cerradas y enlace enviado a {$cuenta->user_email}."
        : "Relevo hecho: la cuenta {$cuenta->user_login} tiene la contraseña nueva y se han cerrado todas sus sesiones.");
}

/** Vuelve a la pantalla con un mensaje (efímero, solo para quien hizo la acción). */
function cadus_relevo_volver(string $tipo, string $texto): void
{
    set_transient('cadus_relevo_msg_' . get_current_user_id(), [$tipo, $texto], 60);
    wp_safe_redirect(admin_url(CADUS_RELEVO_PADRE . '&page=' . CADUS_RELEVO_PAGINA));
    exit;
}

function cadus_relevo_aviso(): void
{
    $clave = 'cadus_relevo_msg_' . get_current_user_id();
    $msg = get_transient($clave);
    if (is_array($msg)) {
        delete_transient($clave);
        $clase = ['ok' => 'notice-success', 'aviso' => 'notice-warning', 'error' => 'notice-error'][$msg[0]] ?? 'notice-info';
        echo '<div class="notice ' . esc_attr($clase) . '"><p>' . esc_html($msg[1]) . '</p></div>';
    }
}

/** Aviso en la pantalla de acceso tras el relevo hecho por el propio delegado. */
function cadus_relevo_mensaje_login(string $mensaje): string
{
    $estado = sanitize_key($_GET['cadus_relevo'] ?? '');
    if ($estado === 'hecho') {
        $mensaje .= '<p class="message">Relevo hecho. La cuenta de la delegación ya es del equipo entrante y se han cerrado todas las sesiones.</p>';
    } elseif ($estado === 'sin-correo') {
        $mensaje .= '<p class="message">Relevo hecho y sesiones cerradas, pero el correo con el enlace no se ha podido enviar. Pide a la Ejecutiva una contraseña nueva para la delegación.</p>';
    }
    return $mensaje;
}
