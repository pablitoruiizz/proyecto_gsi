<?php
/**
 * Pruebas del acceso y la gestión desde el portal (HU-24): permisos por rol, validaciones y resultados.
 * Uso, desde la raíz del repositorio y con el sitio local arrancado:  php scripts/pruebas/gestion.php
 * Crea cuentas, contenidos y archivos temporales y los borra al terminar (no deja nada en el sitio).
 */
if (PHP_SAPI !== 'cli') {
    http_response_code(403);
    exit('Solo desde la línea de comandos.');
}
$_SERVER['HTTP_HOST'] = 'localhost';
require __DIR__ . '/../../cms-wordpress/wp-load.php';

$ok = 0;
$fallos = 0;
function comprobar(string $nombre, bool $cond, string $detalle = ''): void
{
    global $ok, $fallos;
    $cond ? $ok++ : $fallos++;
    echo ($cond ? 'OK    ' : 'FALLO ') . $nombre . ($detalle !== '' && !$cond ? '  → ' . $detalle : '') . "\n";
}
function es_error($r, string $codigo = ''): bool
{
    return is_wp_error($r) && ($codigo === '' || $r->get_error_code() === $codigo);
}

$sufijo = wp_generate_password(6, false, false);
$usuarios = [];
$posts = [];
$terminos = [];
$archivos = [];
$restaurar_der = null; // ficha real de Derecho que la prueba modifica: se restaura siempre, también si la prueba falla

function crear_usuario(string $rol, string $sufijo): WP_User
{
    global $usuarios;
    $login = "prueba_{$rol}_{$sufijo}";
    $id = wp_insert_user(['user_login' => $login, 'user_pass' => wp_generate_password(24), 'user_email' => "{$login}@example.test", 'role' => $rol]);
    if (is_wp_error($id)) {
        exit('No se ha podido crear la cuenta de prueba: ' . $id->get_error_message() . "\n");
    }
    $usuarios[] = (int) $id;
    return get_userdata((int) $id);
}

$ejecutiva = crear_usuario('cadus_ejecutiva', $sufijo);
$admin = crear_usuario('administrator', $sufijo);
$delegado = crear_usuario('cadus_delegado', $sufijo);
$delegado2 = crear_usuario('cadus_delegado', $sufijo . 'b');
$estudiante = crear_usuario('cadus_estudiante', $sufijo);
$anonimo = new WP_User(0);

try {
    echo "== Tareas por rol\n";
    comprobar('la Ejecutiva ve noticia, evento, acta y delegaciones', cadus_gestion_tareas($ejecutiva) === ['noticia', 'evento', 'acta', 'delegaciones'], json_encode(cadus_gestion_tareas($ejecutiva)));
    comprobar('el administrador (cuenta cadus) ve lo mismo', cadus_gestion_tareas($admin) === ['noticia', 'evento', 'acta', 'delegaciones'], json_encode(cadus_gestion_tareas($admin)));
    comprobar('el delegado solo ve su delegación', cadus_gestion_tareas($delegado) === ['delegacion'], json_encode(cadus_gestion_tareas($delegado)));
    comprobar('el estudiante no tiene tareas', cadus_gestion_tareas($estudiante) === []);
    comprobar('un visitante no tiene tareas', cadus_gestion_tareas($anonimo) === []);

    echo "== Páginas y menú\n";
    comprobar('existe la página /acceso/ con el formulario', ($p = get_page_by_path('acceso')) && has_shortcode($p->post_content, 'cadus_acceso'));
    comprobar('existe la página /gestion/ con el panel', ($p = get_page_by_path('gestion')) && has_shortcode($p->post_content, 'cadus_gestion'));
    wp_set_current_user(0);
    $menu = cadus_gestion_menu_sesion('', (object) ['theme_location' => 'menu_1']);
    comprobar('el visitante ve «Acceder» en el menú y no «Gestión»', str_contains($menu, 'Acceder') && !str_contains($menu, 'Gestión'));
    comprobar('el menú de otra ubicación no se toca', cadus_gestion_menu_sesion('<li>x</li>', (object) ['theme_location' => 'footer']) === '<li>x</li>');
    wp_set_current_user($ejecutiva->ID);
    $menu = cadus_gestion_menu_sesion('', (object) ['theme_location' => 'menu_1']);
    comprobar('la Ejecutiva ve «Gestión» y «Salir» y no «Acceder»', str_contains($menu, 'Gestión') && str_contains($menu, 'Salir') && !str_contains($menu, 'Acceder'));
    wp_set_current_user($delegado->ID);
    $menu = cadus_gestion_menu_sesion('', (object) ['theme_location' => 'menu_1']);
    comprobar('el delegado ve «Mi delegación»', str_contains($menu, 'Mi delegación'));
    wp_set_current_user($estudiante->ID);
    $menu = cadus_gestion_menu_sesion('', (object) ['theme_location' => 'menu_1']);
    comprobar('el estudiante solo ve «Salir»', str_contains($menu, 'Salir') && !str_contains($menu, 'Gestión') && !str_contains($menu, 'Mi delegación'));

    wp_set_current_user($ejecutiva->ID); // como en la web, quien actúa es el usuario con la sesión abierta (The Events Calendar comprueba sus permisos)
    echo "== Noticia\n";
    $cat = get_term_by('name', 'Becas', 'category') ?: get_terms(['taxonomy' => 'category', 'hide_empty' => false])[0];
    $datos = ['titulo' => 'Prueba de gestión ' . $sufijo, 'texto' => "Primer párrafo.\n\nSegundo <script>alert(1)</script> párrafo.", 'resumen' => 'Resumen de prueba', 'categoria' => $cat->term_id];
    $r = cadus_gestion_crear_noticia($datos, $ejecutiva);
    comprobar('la Ejecutiva publica una noticia', is_array($r) && get_post_status($r['id']) === 'publish', is_wp_error($r) ? $r->get_error_message() : '');
    if (is_array($r)) {
        $posts[] = $r['id'];
        $cont = get_post_field('post_content', $r['id']);
        comprobar('el texto se convierte en párrafos y se quita el script', str_contains($cont, '<p>') && !str_contains($cont, '<script'), $cont);
        comprobar('la noticia tiene la categoría elegida', has_term($cat->term_id, 'category', $r['id']));
    }
    comprobar('el delegado no puede crear noticias (403)', es_error(cadus_gestion_crear_noticia($datos, $delegado), 'permiso'));
    comprobar('sin título se rechaza', es_error(cadus_gestion_crear_noticia(['titulo' => '', 'texto' => 'x', 'categoria' => $cat->term_id] + $datos, $ejecutiva), 'datos'));
    comprobar('con una categoría que no existe se rechaza', es_error(cadus_gestion_crear_noticia(['categoria' => 999999] + $datos, $ejecutiva), 'datos'));

    echo "== Evento\n";
    $cat_ev = get_term_by('slug', 'asambleas', 'tribe_events_cat');
    comprobar('existe la categoría «Asambleas» del calendario', (bool) $cat_ev);
    $manana = (new DateTimeImmutable('tomorrow', wp_timezone()))->format('Y-m-d');
    $datos = ['titulo' => 'Asamblea de prueba ' . $sufijo, 'categoria' => $cat_ev->term_id, 'fecha' => $manana, 'hora' => '17:30', 'lugar' => 'Salón de actos de prueba ' . $sufijo, 'descripcion' => 'Orden del día.'];
    $r = cadus_gestion_crear_evento($datos, $ejecutiva);
    comprobar('la Ejecutiva crea un evento publicado', is_array($r) && get_post_status($r['id']) === 'publish', is_wp_error($r) ? $r->get_error_message() : '');
    if (is_array($r)) {
        $posts[] = $r['id'];
        do_action('shutdown'); // al terminar la petición web, The Events Calendar vuelca el evento a sus tablas del calendario
        comprobar('el evento empieza el día y la hora indicados', tribe_get_start_date($r['id'], true, 'Y-m-d H:i') === $manana . ' 17:30', tribe_get_start_date($r['id'], true, 'Y-m-d H:i'));
        comprobar('el evento termina una hora después por defecto', tribe_get_end_date($r['id'], true, 'Y-m-d H:i') === $manana . ' 18:30', tribe_get_end_date($r['id'], true, 'Y-m-d H:i'));
        comprobar('el evento tiene la categoría «Asambleas»', has_term($cat_ev->term_id, 'tribe_events_cat', $r['id']));
        comprobar('el evento tiene el lugar indicado', html_entity_decode((string) tribe_get_venue($r['id'])) === 'Salón de actos de prueba ' . $sufijo, (string) tribe_get_venue($r['id']));
        delete_transient('cadus_portada_datos');
        $proximos = array_column(cadus_calendario_eventos(50), 'titulo');
        comprobar('el evento aparece en los próximos eventos de la portada', in_array('Asamblea de prueba ' . $sufijo, $proximos, true));
    }
    comprobar('el delegado no puede crear eventos (403)', es_error(cadus_gestion_crear_evento($datos, $delegado), 'permiso'));
    $general = cadus_gestion_crear_evento(['categoria' => 0, 'titulo' => 'Evento general ' . $sufijo] + $datos, $ejecutiva);
    comprobar('un evento general (sin tipo) se crea sin categoría', is_array($general) && !wp_get_object_terms($general['id'], 'tribe_events_cat'), is_wp_error($general) ? $general->get_error_message() : '');
    if (is_array($general)) {
        $posts[] = $general['id'];
    }
    comprobar('una categoría que no existe se rechaza', es_error(cadus_gestion_crear_evento(['categoria' => 999999] + $datos, $ejecutiva), 'datos'));
    comprobar('una fecha imposible se rechaza', es_error(cadus_gestion_crear_evento(['fecha' => '2026-02-31'] + $datos, $ejecutiva), 'datos'));
    comprobar('un final anterior al principio se rechaza', es_error(cadus_gestion_crear_evento(['hora_fin' => '09:00'] + $datos, $ejecutiva), 'datos'));

    echo "== Acta o normativa\n";
    $tipo = get_terms(['taxonomy' => 'cadus_tipo_documento', 'hide_empty' => false]);
    if (!$tipo) {
        $t = wp_insert_term('Acta de prueba ' . $sufijo, 'cadus_tipo_documento');
        $terminos[] = [(int) $t['term_id'], 'cadus_tipo_documento'];
        $tipo = [get_term((int) $t['term_id'], 'cadus_tipo_documento')];
    }
    $tmp_dir = get_temp_dir();
    $pdf = $tmp_dir . "prueba_{$sufijo}.pdf";
    file_put_contents($pdf, "%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF\n");
    $archivos[] = $pdf;
    $falso = $tmp_dir . "falso_{$sufijo}.pdf";
    file_put_contents($falso, "esto no es un pdf, es texto\n");
    $archivos[] = $falso;
    $datos = ['titulo' => 'Acta de prueba ' . $sufijo, 'tipo' => $tipo[0]->term_id, 'fecha' => '2026-11-12', 'pleno' => 'Pleno de prueba'];
    $copia = $tmp_dir . "copia_{$sufijo}.pdf"; // la subida mueve el archivo: se le pasa una copia
    copy($pdf, $copia);
    $archivos[] = $copia;
    $r = cadus_gestion_crear_acta($datos, ['name' => 'acta.pdf', 'tmp_name' => $copia, 'size' => filesize($pdf), 'error' => UPLOAD_ERR_OK], $ejecutiva);
    comprobar('la Ejecutiva publica un acta con su PDF', is_array($r) && get_post_status($r['id']) === 'publish', is_wp_error($r) ? $r->get_error_message() : '');
    if (is_array($r)) {
        $posts[] = $r['id'];
        $adj = (int) (is_array($v = cadus_campo('archivo_pdf', $r['id'])) ? ($v['ID'] ?? 0) : $v);
        if ($adj) {
            $posts[] = $adj;
        }
        comprobar('el acta guarda la fecha, el pleno y el PDF', cadus_campo('fecha', $r['id']) === '20261112' && cadus_campo('pleno', $r['id']) === 'Pleno de prueba' && cadus_url_pdf(cadus_campo('archivo_pdf', $r['id'])) !== '', json_encode([cadus_campo('fecha', $r['id']), cadus_campo('pleno', $r['id'])]));
        comprobar('el acta tiene el tipo elegido', has_term($tipo[0]->term_id, 'cadus_tipo_documento', $r['id']));
    }
    comprobar('un archivo que no es PDF se rechaza', es_error(cadus_gestion_crear_acta($datos, ['name' => 'acta.pdf', 'tmp_name' => $falso, 'size' => filesize($falso), 'error' => UPLOAD_ERR_OK], $ejecutiva), 'pdf'));
    comprobar('un PDF con otra extensión se rechaza', es_error(cadus_gestion_crear_acta($datos, ['name' => 'acta.exe', 'tmp_name' => $pdf, 'size' => filesize($pdf), 'error' => UPLOAD_ERR_OK], $ejecutiva), 'pdf'));
    comprobar('sin archivo se rechaza', es_error(cadus_gestion_crear_acta($datos, [], $ejecutiva), 'pdf'));
    comprobar('el delegado no puede crear actas (403)', es_error(cadus_gestion_crear_acta($datos, ['name' => 'a.pdf', 'tmp_name' => $pdf, 'size' => 1, 'error' => UPLOAD_ERR_OK], $delegado), 'permiso'));
    $huerfanos = get_posts(['post_type' => 'cadus_acta', 'post_status' => 'any', 'title' => 'Acta de prueba ' . $sufijo, 'numberposts' => -1]);
    comprobar('los intentos fallidos no dejan actas a medias', count($huerfanos) === 1, (string) count($huerfanos));

    echo "== Delegaciones\n";
    $centro = get_terms(['taxonomy' => 'cadus_centro', 'hide_empty' => false]);
    if (!$centro) {
        $t = wp_insert_term('Centro de prueba ' . $sufijo, 'cadus_centro');
        $terminos[] = [(int) $t['term_id'], 'cadus_centro'];
        $centro = [get_term((int) $t['term_id'], 'cadus_centro')];
    }
    $datos = ['titulo' => 'Delegación de prueba ' . $sufijo, 'centro' => $centro[0]->term_id, 'delegado' => 'Persona de prueba', 'correo' => 'delegacion@example.test',
        'telefono' => '954 000 000', 'horario' => 'Lunes de 10 a 12', 'enlaces' => "https://example.test/a\nhttps://example.test/b", 'cuenta' => $delegado->ID];
    $r = cadus_gestion_nueva_delegacion($datos, $ejecutiva);
    comprobar('la Ejecutiva crea una delegación con su cuenta', is_array($r) && (int) get_post_field('post_author', $r['id']) === $delegado->ID, is_wp_error($r) ? $r->get_error_message() : '');
    $ficha = is_array($r) ? $r['id'] : 0;
    $posts[] = $ficha;
    comprobar('la ficha guarda los datos de contacto', $ficha && cadus_campo('delegado', $ficha) === 'Persona de prueba' && cadus_campo('horario', $ficha) === 'Lunes de 10 a 12' && substr_count((string) cadus_campo('enlaces', $ficha), "\n") === 1);
    comprobar('una cuenta con delegación no puede tener otra', es_error(cadus_gestion_nueva_delegacion(['titulo' => 'Otra ' . $sufijo] + $datos, $ejecutiva), 'datos'));
    comprobar('una cuenta que no es de delegación se rechaza', es_error(cadus_gestion_nueva_delegacion(['cuenta' => $estudiante->ID, 'titulo' => 'Otra ' . $sufijo] + $datos, $ejecutiva), 'datos'));
    comprobar('el delegado no puede crear delegaciones (403)', es_error(cadus_gestion_nueva_delegacion($datos, $delegado), 'permiso'));
    comprobar('un correo mal escrito se rechaza', es_error(cadus_gestion_nueva_delegacion(['correo' => 'no-es-un-correo', 'cuenta' => 0, 'titulo' => 'Otra ' . $sufijo] + $datos, $ejecutiva), 'datos'));
    comprobar('un enlace sin http se rechaza', es_error(cadus_gestion_nueva_delegacion(['enlaces' => 'javascript:alert(1)', 'cuenta' => 0, 'titulo' => 'Otra ' . $sufijo] + $datos, $ejecutiva), 'datos'));
    comprobar('los intentos fallidos no dejan fichas a medias', count(get_posts(['post_type' => 'cadus_delegacion', 'post_status' => 'any', 'title' => 'Otra ' . $sufijo, 'numberposts' => -1])) === 0);

    $edicion = ['ficha' => $ficha, 'delegado' => 'Nueva persona', 'correo' => 'nueva@example.test', 'telefono' => '600 000 000', 'horario' => 'Martes', 'enlaces' => 'https://example.test/c'];
    $r2 = cadus_gestion_guardar_delegacion($edicion, $delegado);
    comprobar('el delegado edita la ficha de su propia delegación', is_array($r2) && cadus_campo('delegado', $ficha) === 'Nueva persona', is_wp_error($r2) ? $r2->get_error_message() : '');
    comprobar('el delegado no puede cambiar el nombre de la delegación', get_the_title($ficha) === 'Delegación de prueba ' . $sufijo);
    comprobar('otro delegado no puede editar esa ficha (403)', es_error(cadus_gestion_guardar_delegacion($edicion, $delegado2), 'permiso'));
    comprobar('el estudiante no puede editar fichas (403)', es_error(cadus_gestion_guardar_delegacion($edicion, $estudiante), 'permiso'));
    $r3 = cadus_gestion_guardar_delegacion(['titulo' => 'Delegación renombrada ' . $sufijo] + $edicion, $ejecutiva);
    comprobar('la Ejecutiva edita cualquier ficha y puede cambiar su nombre', is_array($r3) && get_the_title($ficha) === 'Delegación renombrada ' . $sufijo, is_wp_error($r3) ? $r3->get_error_message() : '');
    comprobar('un identificador que no es de una ficha se rechaza', es_error(cadus_gestion_guardar_delegacion(['ficha' => $posts[0] ?? 1] + $edicion, $ejecutiva), 'datos'));

    echo "== Delegaciones: Instagram, miembros, cuenta y «Sin asignar»\n";
    $r4 = cadus_gestion_guardar_delegacion(['instagram' => 'https://www.instagram.com/prueba_' . $sufijo, 'miembros' => "Pérez Ruiz, Ana\n  \nLópez Gil, Luis"] + $edicion, $ejecutiva);
    comprobar('se guardan el Instagram y los miembros (sin líneas vacías)', is_array($r4) && cadus_campo('instagram', $ficha) === 'https://www.instagram.com/prueba_' . $sufijo && cadus_delegacion_miembros($ficha) === ['Pérez Ruiz, Ana', 'López Gil, Luis'], is_wp_error($r4) ? $r4->get_error_message() : '');
    comprobar('un Instagram que no es una dirección web se rechaza', es_error(cadus_gestion_guardar_delegacion(['instagram' => 'solo_un_usuario'] + $edicion, $ejecutiva), 'datos'));
    $r5 = cadus_gestion_guardar_delegacion(['cuenta' => $delegado2->ID] + $edicion, $ejecutiva);
    comprobar('la Ejecutiva pasa la ficha a otra cuenta de delegación', is_array($r5) && (int) get_post_field('post_author', $ficha) === $delegado2->ID, is_wp_error($r5) ? $r5->get_error_message() : '');
    comprobar('el delegado anterior ya no puede editarla y el nuevo sí', es_error(cadus_gestion_guardar_delegacion($edicion, $delegado), 'permiso') && is_array(cadus_gestion_guardar_delegacion($edicion, $delegado2)));
    cadus_gestion_guardar_delegacion(['cuenta' => $delegado->ID] + $edicion, $delegado2);
    comprobar('un delegado no puede cambiar la cuenta de su ficha', (int) get_post_field('post_author', $ficha) === $delegado2->ID);
    comprobar('una cuenta que no es de delegación no se admite al cambiar', es_error(cadus_gestion_guardar_delegacion(['cuenta' => $estudiante->ID] + $edicion, $ejecutiva), 'datos'));
    cadus_gestion_guardar_delegacion(['centro' => 0] + $edicion, $ejecutiva);
    comprobar('«Sin asignar» quita de verdad el centro', !wp_get_post_terms($ficha, 'cadus_centro', ['fields' => 'ids']));
    comprobar('un visitante no puede crear actas', es_error(cadus_gestion_crear_acta(['titulo' => 'x'], [], new WP_User(0)), 'permiso'));
    wp_set_current_user($ejecutiva->ID);
    cadus_gestion_previo(['tarea' => 'noticia', 'datos' => ['titulo' => 'Titulo "con comillas" ' . $sufijo, 'categoria' => '', 'texto' => "Primera línea\nSegunda <b>línea</b>"]]);
    $html = cadus_gestion_panel();
    comprobar('un formulario con error vuelve a mostrar lo escrito y lo escapa', str_contains($html, 'value="Titulo &quot;con comillas&quot; ' . $sufijo . '"') && str_contains($html, 'Segunda &lt;b&gt;línea&lt;/b&gt;') && !str_contains($html, '<b>línea</b>'));
    cadus_gestion_previo([]);
    comprobar('sin error los formularios salen vacíos', !str_contains(cadus_gestion_panel(), 'con comillas'));

    comprobar('un Instagram de otro dominio se rechaza', es_error(cadus_gestion_guardar_delegacion(['instagram' => 'https://ejemplo.test/perfil'] + $edicion, $ejecutiva), 'datos'));
    comprobar('un Instagram con http se rechaza', es_error(cadus_gestion_guardar_delegacion(['instagram' => 'http://www.instagram.com/x'] + $edicion, $ejecutiva), 'datos'));
    $autor_antes = (int) get_post_field('post_author', $ficha);
    $t_antes = cadus_campo('delegado', $ficha);
    comprobar('una cuenta no válida no deja la ficha a medio guardar', es_error(cadus_gestion_guardar_delegacion(['cuenta' => $estudiante->ID, 'delegado' => 'No debe guardarse'] + $edicion, $ejecutiva), 'datos')
        && cadus_campo('delegado', $ficha) === $t_antes && (int) get_post_field('post_author', $ficha) === $autor_antes);

    echo "== Carga de las delegaciones de cadus.us.es\n";
    $json = json_decode((string) file_get_contents(CADUS_PORTAL_DIR . 'data/delegaciones.json'), true);
    $total_fichas = fn() => count(get_posts(['post_type' => 'cadus_delegacion', 'post_status' => 'any', 'numberposts' => -1, 'meta_key' => '_cadus_semilla', 'fields' => 'ids']));
    $antes_n = $total_fichas();
    $res = cadus_delegaciones_cargar();
    comprobar('hay 27 delegaciones en los datos y la carga no crea duplicados', count($json) === 27 && $res['creadas'] === 0 && $total_fichas() === $antes_n, json_encode($res));
    $deleg_der = cadus_buscar_semilla('delegacion:' . sanitize_title('Facultad de Derecho'), 'cadus_delegacion');
    if ($deleg_der) {
        $guardado = cadus_campo('miembros', $deleg_der->ID);
        $correo_g = cadus_campo('correo', $deleg_der->ID);
        $centros_der_orig = array_map('intval', wp_get_post_terms($deleg_der->ID, 'cadus_centro', ['fields' => 'ids']));
        $restaurar_der = ['id' => (int) $deleg_der->ID, 'miembros' => $guardado, 'centros' => $centros_der_orig];
        cadus_gestion_campo('field_cadus_deleg_miembros', 'miembros', '', $deleg_der->ID);
        wp_set_object_terms($deleg_der->ID, [], 'cadus_centro');
        cadus_delegaciones_cargar();
        comprobar('lo que se vacía a propósito no se repone al recargar', cadus_campo('miembros', $deleg_der->ID) === '' && !wp_get_post_terms($deleg_der->ID, 'cadus_centro', ['fields' => 'ids']));
        cadus_gestion_campo('field_cadus_deleg_miembros', 'miembros', $guardado, $deleg_der->ID);
        wp_set_object_terms($deleg_der->ID, $centros_der_orig, 'cadus_centro');
        comprobar('las fichas importadas tienen escudo (salvo Doctorado y Odontología)', count(array_filter($json, fn($x) => $x['escudo'] !== '')) === 25 && (int) cadus_campo('escudo', $deleg_der->ID) > 0);
    }

    echo "== Formularios por HTTP (nonce, tarea, permisos, archivo falso)\n";
    $base = rtrim(home_url(), '/');
    $clave_e = wp_generate_password(20);
    $clave_d = wp_generate_password(20);
    wp_set_password($clave_e, $ejecutiva->ID);
    wp_set_password($clave_d, $delegado2->ID);
    $peticion = function (string $metodo, string $url, array $campos = [], string $jar = '', array $archivo = [], array $cabeceras = [], ?string $json = null) {
        $ch = curl_init($url);
        $opt = [CURLOPT_RETURNTRANSFER => true, CURLOPT_HEADER => true, CURLOPT_FOLLOWLOCATION => false, CURLOPT_TIMEOUT => 60, CURLOPT_USERAGENT => 'pruebas-gestion', CURLOPT_HTTPHEADER => $cabeceras];
        if ($jar !== '') {
            $opt[CURLOPT_COOKIEJAR] = $jar;
            $opt[CURLOPT_COOKIEFILE] = $jar;
        }
        if ($metodo === 'POST') {
            $opt[CURLOPT_POST] = true;
            if ($archivo) {
                $campos['pdf'] = new CURLFile($archivo[0], $archivo[1], $archivo[2]);
            }
            $opt[CURLOPT_POSTFIELDS] = $json ?? ($archivo ? $campos : http_build_query($campos));
        }
        curl_setopt_array($ch, $opt);
        $res = (string) curl_exec($ch);
        $tam = (int) curl_getinfo($ch, CURLINFO_HEADER_SIZE);
        $codigo = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        curl_close($ch);
        return ['codigo' => $codigo, 'cab' => substr($res, 0, $tam), 'cuerpo' => substr($res, $tam)];
    };
    $entrar = function (string $login, string $clave) use ($peticion, $base): string {
        $jar = tempnam(sys_get_temp_dir(), 'jar');
        $peticion('POST', $base . '/wp-login.php', ['log' => $login, 'pwd' => $clave, 'wp-submit' => 'Acceder', 'testcookie' => '1'], $jar);
        return str_contains((string) file_get_contents($jar), 'wordpress_logged_in_') ? $jar : '';
    };
    $nonce_de = fn(string $html, string $tarea): string => preg_match('/name="cadus_tarea" value="' . $tarea . '"><input type="hidden" name="cadus_nonce" value="([a-f0-9]+)"/', $html, $m) ? $m[1] : '';
    // Acceso tal como lo envía el formulario del portal (campos cadus_acceso y redirect_to), no solo wp-login.php a secas.
    $campos_portal = ['cadus_acceso' => '1', 'redirect_to' => cadus_gestion_url_pagina('gestion')]; // exactamente los campos del formulario [cadus_acceso]
    $jar_mal = tempnam(sys_get_temp_dir(), 'jar');
    $archivos[] = $jar_mal;
    $mal = $peticion('POST', $base . '/wp-login.php', ['log' => $ejecutiva->user_login, 'pwd' => 'clave-incorrecta-' . $sufijo] + $campos_portal, $jar_mal);
    comprobar('con una contraseña mala el acceso desde el portal vuelve a la página de acceso con el aviso', $mal['codigo'] === 302 && str_contains($mal['cab'], 'acceso=error') && !str_contains((string) file_get_contents($jar_mal), 'wordpress_logged_in_'), $mal['codigo'] . ' ' . substr($mal['cab'], 0, 200));
    $jar_bien = tempnam(sys_get_temp_dir(), 'jar');
    $archivos[] = $jar_bien;
    $bien = $peticion('POST', $base . '/wp-login.php', ['log' => $ejecutiva->user_login, 'pwd' => $clave_e] + $campos_portal, $jar_bien);
    comprobar('con las credenciales correctas el acceso desde el portal lleva a /gestion/ con la sesión abierta', $bien['codigo'] === 302 && str_contains($bien['cab'], '/gestion/') && str_contains((string) file_get_contents($jar_bien), 'wordpress_logged_in_'), $bien['codigo'] . ' ' . substr($bien['cab'], 0, 200));
    $jar_e = $entrar($ejecutiva->user_login, $clave_e);
    $jar_d = $entrar($delegado2->user_login, $clave_d);
    if ($jar_e === '' || $jar_d === '') {
        comprobar('se puede iniciar sesión por HTTP con las cuentas de prueba (si falla, Wordfence puede estar bloqueando el acceso)', false);
    } else {
        $archivos[] = $jar_e;
        $archivos[] = $jar_d;
        $pagina = $peticion('GET', $base . '/gestion/', [], $jar_e);
        comprobar('/gestion/ no se cachea', str_contains(strtolower($pagina['cab']), 'no-store') || str_contains(strtolower($pagina['cab']), 'no-cache'));
        comprobar('/gestion/ lleva noindex', str_contains(strtolower($pagina['cuerpo']), 'noindex'));
        $n_not = $nonce_de($pagina['cuerpo'], 'noticia');
        $n_acta = $nonce_de($pagina['cuerpo'], 'acta');
        comprobar('la página entrega un nonce distinto por formulario', $n_not !== '' && $n_acta !== '' && $n_not !== $n_acta);
        $envio = $base . '/wp-admin/admin-post.php';
        $buenos = ['action' => 'cadus_gestion', 'cadus_tarea' => 'noticia', 'cadus_nonce' => $n_not];
        $cuantas = fn() => count(get_posts(['post_type' => 'post', 'post_status' => 'any', 'numberposts' => -1, 's' => $sufijo]));
        $antes = $cuantas();

        $peticion('POST', $envio, $buenos + ['titulo' => 'Sin sesión ' . $sufijo, 'categoria' => '1', 'texto' => 'Texto de prueba'], '');
        comprobar('sin iniciar sesión no se crea nada', $cuantas() === $antes);
        $r = $peticion('POST', ['cadus_nonce' => 'abc123'] + $buenos ? $envio : $envio, ['cadus_nonce' => 'abc123'] + $buenos + ['titulo' => 'Nonce malo ' . $sufijo], $jar_e);
        comprobar('un nonce incorrecto da 403 y no crea nada', $r['codigo'] === 403 && $cuantas() === $antes, (string) $r['codigo']);
        $r = $peticion('POST', $envio, ['cadus_tarea' => 'evento'] + $buenos + ['titulo' => 'Nonce de otra tarea ' . $sufijo], $jar_e);
        comprobar('el nonce de una tarea no vale para otra (403)', $r['codigo'] === 403 && $cuantas() === $antes, (string) $r['codigo']);
        $r = $peticion('POST', $envio, ['cadus_tarea' => 'borrar_todo'] + $buenos, $jar_e);
        comprobar('una tarea que no existe da 403', $r['codigo'] === 403, (string) $r['codigo']);
        $r = $peticion('POST', $envio, $buenos + ['titulo' => 'Ab'], $jar_e);
        comprobar('un error de validación redirige a /gestion/', $r['codigo'] === 302 && str_contains($r['cab'], '/gestion/'), (string) $r['codigo']);
        $despues = $peticion('GET', $base . '/gestion/', [], $jar_e);
        comprobar('el error sale con role="alert" y se conserva lo escrito', str_contains($despues['cuerpo'], 'role="alert"') && str_contains($despues['cuerpo'], 'value="Ab"'));
        // Creación válida por HTTP (no solo llamando a la función): redirige a /gestion/ con el aviso de éxito y publica la noticia
        $n_ok = $nonce_de($peticion('GET', $base . '/gestion/', [], $jar_e)['cuerpo'], 'noticia');
        $cat_http = get_term_by('name', 'Becas', 'category') ?: get_terms(['taxonomy' => 'category', 'hide_empty' => false])[0];
        $antes_http = $cuantas();
        $r = $peticion('POST', $envio, ['action' => 'cadus_gestion', 'cadus_tarea' => 'noticia', 'cadus_nonce' => $n_ok, 'titulo' => 'Noticia por HTTP ' . $sufijo, 'categoria' => (string) $cat_http->term_id, 'texto' => 'Texto de prueba por HTTP.'], $jar_e);
        wp_cache_flush(); // la petición HTTP escribió en otro proceso: se descarta la caché de consultas de este
        $creada = get_posts(['post_type' => 'post', 'post_status' => 'any', 'numberposts' => 1, 's' => 'Noticia por HTTP ' . $sufijo]);
        comprobar('una noticia válida enviada por HTTP se crea publicada y redirige a /gestion/', $r['codigo'] === 302 && str_contains($r['cab'], '/gestion/') && $cuantas() === $antes_http + 1 && $creada && $creada[0]->post_status === 'publish', $r['codigo'] . ' antes=' . $antes_http . ' ahora=' . $cuantas() . ' estado=' . ($creada ? $creada[0]->post_status : 'sin crear') . ' ' . substr($r['cab'], 0, 160));
        $otra_sesion = $entrar($ejecutiva->user_login, $clave_e);
        if ($otra_sesion !== '') {
            $archivos[] = $otra_sesion;
            $n2 = $nonce_de($peticion('GET', $base . '/gestion/', [], $jar_e)['cuerpo'], 'noticia');
            $peticion('POST', $envio, ['cadus_nonce' => $n2] + $buenos + ['titulo' => 'Zz'], $jar_e);
            $ajena = $peticion('GET', $base . '/gestion/', [], $otra_sesion);
            comprobar('el aviso de una sesión no lo lee otra sesión de la misma cuenta', !str_contains($ajena['cuerpo'], 'role="alert"'));
            $propia = $peticion('GET', $base . '/gestion/', [], $jar_e);
            comprobar('…y la sesión que lo provocó sí lo recibe', str_contains($propia['cuerpo'], 'role="alert"'));
        }
        $falso = tempnam(sys_get_temp_dir(), 'pdf');
        file_put_contents($falso, 'esto es texto, no un PDF');
        $archivos[] = $falso;
        $actas_antes = count(get_posts(['post_type' => 'cadus_acta', 'post_status' => 'any', 'numberposts' => -1, 's' => $sufijo]));
        $tipo_id = (string) (array_key_first(cadus_gestion_terminos('cadus_tipo_documento')) ?? 0);
        $peticion('POST', $envio, ['action' => 'cadus_gestion', 'cadus_tarea' => 'acta', 'cadus_nonce' => $n_acta, 'titulo' => 'Acta falsa ' . $sufijo, 'tipo' => $tipo_id, 'fecha' => '2026-11-01'], $jar_e, [$falso, 'application/pdf', 'falso.pdf']);
        $tras = $peticion('GET', $base . '/gestion/', [], $jar_e);
        comprobar('un texto renombrado a .pdf se rechaza y no crea el acta', str_contains($tras['cuerpo'], 'debe ser un PDF') && count(get_posts(['post_type' => 'cadus_acta', 'post_status' => 'any', 'numberposts' => -1, 's' => $sufijo])) === $actas_antes);

        $pd = $peticion('GET', $base . '/gestion/', [], $jar_d);
        $n_deleg = $nonce_de($pd['cuerpo'], 'delegacion');
        $otras = get_posts(['post_type' => 'cadus_delegacion', 'post_status' => 'publish', 'numberposts' => 1, 'author__not_in' => [$delegado2->ID]]);
        if ($n_deleg !== '' && $otras) {
            $otra = (int) $otras[0]->ID;
            $titulo_otra = get_the_title($otra);
            $peticion('POST', $envio, ['action' => 'cadus_gestion', 'cadus_tarea' => 'delegacion', 'cadus_nonce' => $n_deleg, 'ficha' => (string) $otra, 'delegado' => 'Intruso ' . $sufijo], $jar_d);
            clean_post_cache($otra);
            comprobar('un delegado no puede editar por HTTP la ficha de otra delegación', cadus_campo('delegado', $otra) !== 'Intruso ' . $sufijo && get_the_title($otra) === $titulo_otra);
        } else {
            comprobar('hay fichas ajenas y el delegado ve su formulario', false, 'nonce=' . $n_deleg);
        }

        // La API REST no puede saltarse lo que el panel impide al delegado (título, centro, estado)
        $nonce_rest = trim($peticion('GET', $base . '/wp-admin/admin-ajax.php?action=rest-nonce', [], $jar_d)['cuerpo']);
        $mi = (int) (cadus_relevo_fichas($delegado2->ID)[0]->ID ?? 0);
        if ($mi && $nonce_rest !== '') {
            $titulo_mi = get_the_title($mi);
            $centros_mi = wp_get_post_terms($mi, 'cadus_centro', ['fields' => 'ids']);
            $cab = ['Content-Type: application/json', 'X-WP-Nonce: ' . $nonce_rest];
            $rest = $base . '/wp-json/wp/v2/cadus_delegacion/' . $mi;
            $a = $peticion('POST', $rest, [], $jar_d, [], $cab, json_encode(['title' => 'Cambiado por REST ' . $sufijo]));
            $b = $peticion('POST', $rest, [], $jar_d, [], $cab, json_encode(['cadus_centro' => []]));
            $c = $peticion('POST', $rest, [], $jar_d, [], $cab, json_encode(['status' => 'draft']));
            clean_post_cache($mi);
            comprobar('el delegado no cambia por REST el título, el centro ni el estado de su ficha', get_the_title($mi) === $titulo_mi && wp_get_post_terms($mi, 'cadus_centro', ['fields' => 'ids']) === $centros_mi && get_post_status($mi) === 'publish', $a['codigo'] . '/' . $b['codigo'] . '/' . $c['codigo']);
            comprobar('…y la API responde 403', $a['codigo'] === 403 && $b['codigo'] === 403 && $c['codigo'] === 403, $a['codigo'] . '/' . $b['codigo'] . '/' . $c['codigo']);
            $contenido_mi = (string) get_post_field('post_content', $mi);
            $d_ = $peticion('POST', $rest, [], $jar_d, [], $cab, json_encode(['content' => 'Texto editado por su delegado ' . $sufijo]));
            $e_ = $peticion('POST', $rest, [], $jar_d, [], $cab, json_encode(['excerpt' => 'Extracto editado por su delegado ' . $sufijo]));
            clean_post_cache($mi);
            comprobar('RN-04: el delegado tampoco cambia por REST el texto libre (contenido ni extracto) de su ficha', $d_['codigo'] === 403 && $e_['codigo'] === 403 && (string) get_post_field('post_content', $mi) === $contenido_mi, $d_['codigo'] . '/' . $e_['codigo']);
        } else {
            comprobar('se obtiene el nonce de la API REST para probar las restricciones', false, 'nonce=' . $nonce_rest);
        }
    }

    echo "== Panel (lo que ve cada rol)\n";
    wp_set_current_user(0);
    $html = cadus_gestion_panel();
    comprobar('el visitante ve el aviso y el enlace a Acceder, sin formularios', str_contains($html, 'Acceder') && !str_contains($html, '<form'));
    wp_set_current_user($ejecutiva->ID);
    $html = cadus_gestion_panel();
    comprobar('la Ejecutiva ve los cuatro bloques y la delegación creada', str_contains($html, 'id="noticia"') && str_contains($html, 'id="evento"') && str_contains($html, 'id="acta"') && str_contains($html, 'id="delegaciones"') && str_contains($html, 'Delegación renombrada ' . $sufijo));
    comprobar('cada formulario lleva su nonce y los campos con etiqueta', substr_count($html, 'name="cadus_nonce"') >= 4 && substr_count($html, '<label for=') >= 15);
    wp_set_current_user($delegado->ID);
    $html = cadus_gestion_panel();
    comprobar('el delegado solo ve su delegación, sin noticia, evento ni acta', str_contains($html, 'Mi delegación') && !str_contains($html, 'id="noticia"') && !str_contains($html, 'id="evento"') && !str_contains($html, 'id="acta"'));
    comprobar('el delegado no ve la creación de delegaciones ni el nombre editable', !str_contains($html, 'Añadir una delegación nueva') && !str_contains($html, 'Nombre de la delegación'));
    wp_set_current_user($delegado->ID); // la ficha pasó a la cuenta delegado2 en las pruebas anteriores
    comprobar('un delegado sin ficha ve el aviso, no las de los demás', str_contains(cadus_gestion_panel(), 'No hay ninguna ficha asignada') && !str_contains(cadus_gestion_panel(), 'Delegación renombrada'));
    wp_set_current_user($estudiante->ID);
    comprobar('el estudiante ve que no tiene tareas', str_contains(cadus_gestion_panel(), 'no tiene tareas') && !str_contains(cadus_gestion_panel(), '<form'));
    wp_set_current_user(0);
    $acceso = cadus_gestion_acceso();
    comprobar('el formulario de acceso envía a wp-login.php (donde actúa Wordfence)', str_contains($acceso, 'wp-login.php') && str_contains($acceso, 'name="log"') && str_contains($acceso, 'name="pwd"'));
} finally {
    echo "== Limpieza\n";
    wp_set_current_user(0);
    if ($restaurar_der) {
        cadus_gestion_campo('field_cadus_deleg_miembros', 'miembros', $restaurar_der['miembros'], $restaurar_der['id']);
        wp_set_object_terms($restaurar_der['id'], $restaurar_der['centros'], 'cadus_centro');
    }
    foreach (array_unique(array_filter($posts)) as $id) {
        wp_delete_post((int) $id, true);
    }
    foreach (get_posts(['post_type' => ['post', 'tribe_events', 'cadus_acta', 'cadus_delegacion', 'attachment'], 'post_status' => 'any', 'numberposts' => -1, 's' => $sufijo]) as $p) {
        wp_delete_post($p->ID, true);
    }
    foreach (get_posts(['post_type' => 'tribe_venue', 'post_status' => 'any', 'numberposts' => -1, 's' => 'Salón de actos de prueba ' . $sufijo]) as $p) {
        wp_delete_post($p->ID, true);
    }
    foreach ($terminos as [$id, $tax]) {
        wp_delete_term($id, $tax);
    }
    require_once ABSPATH . 'wp-admin/includes/user.php';
    foreach ($usuarios as $id) {
        wp_delete_user($id);
    }
    foreach ($archivos as $a) {
        @unlink($a);
    }
    delete_transient('cadus_portada_datos');
    $restos = count(get_users(['search' => '*' . $sufijo . '*', 'search_columns' => ['user_login']]))
        + count(get_posts(['post_type' => 'any', 'post_status' => 'any', 's' => $sufijo, 'numberposts' => -1]));
    comprobar('no queda ninguna cuenta ni contenido de prueba', $restos === 0, (string) $restos);
}
echo "\n{$ok} correctas, {$fallos} fallos\n";
exit($fallos ? 1 : 0);
