<?php
/**
 * Alta de las cuentas reales del CADUS con su rol (E2-01) a partir de usuarios-reales.csv.
 *
 * Uso (CLI, desde la raíz del repositorio):
 *   php scripts/roles/aplicar_usuarios.php            → ensayo en seco: muestra qué se haría y no cambia nada
 *   php scripts/roles/aplicar_usuarios.php --aplicar  → crea o actualiza las cuentas
 *   php scripts/roles/aplicar_usuarios.php --aplicar --avisar → además envía a cada persona el enlace para elegir su contraseña
 *
 * CSV (UTF-8, separador coma, cabecera obligatoria): usuario,nombre,correo,rol,delegacion
 *   rol = ejecutivo | delegado | estudiante   ·   delegacion = título exacto de la delegación (solo para delegados)
 * Reglas: nunca se guardan ni muestran contraseñas (se genera una aleatoria que nadie ve; cada persona la cambia con el enlace
 * de «contraseña olvidada»); no se tocan las cuentas de administrador; un delegado queda como autor de SU delegación,
 * que es lo que le permite editarla y nada más (RN-04).
 */
if (PHP_SAPI !== 'cli') {
    exit('Solo desde la línea de comandos.');
}
$_SERVER['HTTP_HOST'] = 'localhost';
define('WP_USE_THEMES', false);
require dirname(__DIR__, 2) . '/cms-wordpress/wp-load.php';

$aplicar = in_array('--aplicar', $argv, true);
$avisar = in_array('--avisar', $argv, true);
const ROLES = ['ejecutivo' => 'cadus_ejecutiva', 'delegado' => 'cadus_delegado', 'estudiante' => 'cadus_estudiante'];

$delegaciones = get_posts(['post_type' => 'cadus_delegacion', 'post_status' => 'any', 'numberposts' => -1]);
$por_titulo = [];
foreach ($delegaciones as $d) {
    $por_titulo[mb_strtolower(trim($d->post_title))] = $d;
}

$ruta = __DIR__ . '/usuarios-reales.csv';
$filas = [];
if (is_readable($ruta) && ($f = fopen($ruta, 'r'))) {
    $cabecera = array_map('trim', fgetcsv($f) ?: []);
    while (($r = fgetcsv($f)) !== false) {
        if (count($r) >= 4 && trim((string) $r[0]) !== '') {
            $filas[] = array_combine($cabecera, array_pad(array_map('trim', $r), count($cabecera), ''));
        }
    }
    fclose($f);
}

echo $aplicar ? "MODO APLICAR\n" : "ENSAYO EN SECO (no se cambia nada; usa --aplicar para ejecutar)\n";
echo "Delegaciones existentes: " . ($por_titulo ? implode(' | ', array_map(fn($d) => $d->post_title, $delegaciones)) : '(ninguna)') . "\n";
if (!$filas) {
    echo "usuarios-reales.csv no tiene filas: rellénalo con los datos que facilite el CADUS.\n";
    exit(0);
}

$errores = 0;
foreach ($filas as $fila) {
    $login = sanitize_user($fila['usuario'] ?? '', true);
    $correo = sanitize_email($fila['correo'] ?? '');
    $rol = ROLES[strtolower($fila['rol'] ?? '')] ?? '';
    $existente = get_user_by('login', $login) ?: get_user_by('email', $correo);
    $problema = '';
    if ($login === '' || !is_email($correo)) {
        $problema = 'usuario o correo no válidos';
    } elseif ($rol === '') {
        $problema = 'rol desconocido (usa ejecutivo, delegado o estudiante)';
    } elseif ($existente && in_array('administrator', $existente->roles, true)) {
        $problema = 'es administrador: no se modifica desde este script';
    } elseif ($rol === 'cadus_delegado' && !isset($por_titulo[mb_strtolower($fila['delegacion'] ?? '')])) {
        $problema = 'delegado sin delegación válida (título exacto)';
    }
    if ($problema) {
        ++$errores;
        echo "  ✗ {$login}: {$problema}\n";
        continue;
    }
    echo '  ' . ($existente ? '↻ actualizar ' : '+ crear ') . "{$login} ({$correo}) → {$rol}"
        . ($rol === 'cadus_delegado' ? " · delegación «{$fila['delegacion']}»" : '') . "\n";
    if (!$aplicar) {
        continue;
    }
    if ($existente) {
        $id = $existente->ID;
        wp_update_user(['ID' => $id, 'display_name' => $fila['nombre'] ?: $existente->display_name, 'role' => $rol]);
    } else {
        $id = wp_insert_user(['user_login' => $login, 'user_email' => $correo, 'display_name' => $fila['nombre'] ?: $login,
            'user_pass' => wp_generate_password(32, true, true), 'role' => $rol]);
        if (is_wp_error($id)) {
            ++$errores;
            echo '    ✗ ' . $id->get_error_message() . "\n";
            continue;
        }
    }
    if ($rol === 'cadus_delegado') {
        $d = $por_titulo[mb_strtolower($fila['delegacion'])];
        wp_update_post(['ID' => $d->ID, 'post_author' => $id]);
    }
    if ($avisar) {
        wp_new_user_notification($id, null, 'user'); // requiere correo saliente configurado en el servidor
    }
}
echo $errores ? "Terminado con {$errores} fila(s) con problemas.\n" : "Terminado sin problemas.\n";
