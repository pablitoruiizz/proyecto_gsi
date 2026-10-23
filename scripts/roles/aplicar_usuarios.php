<?php
/**
 * Alta de las cuentas institucionales de las delegaciones (E2-01) a partir de usuarios-reales.csv.
 * Las cuentas son de órganos, no de personas: el CADUS se renueva cada año (ver README.md).
 *
 * Uso (CLI, desde la raíz del repositorio):
 *   php scripts/roles/aplicar_usuarios.php            → ensayo en seco: muestra qué se haría y no cambia nada
 *   php scripts/roles/aplicar_usuarios.php --aplicar  → crea o actualiza las cuentas
 *   php scripts/roles/aplicar_usuarios.php --aplicar --avisar → además envía a cada cuenta el enlace para elegir su contraseña
 *
 * CSV (UTF-8, separador coma, cabecera obligatoria): usuario,nombre,correo,rol,delegacion
 *   rol = ejecutivo | delegado | estudiante; vacío = delegado
 *   delegacion = título exacto de la ficha de la delegación; vacío = se busca una ficha cuyo título sea igual al «nombre».
 *   Si la ficha todavía no existe, la cuenta se crea igualmente y se avisa: al volver a ejecutar el script se asigna.
 * Reglas: nunca se guardan ni muestran contraseñas (se genera una aleatoria que nadie ve; cada titular la cambia con el enlace
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
    // Quita la marca BOM que añade Excel al guardar en UTF-8.
    $cabecera = array_map(fn($c) => trim(preg_replace('/^\xEF\xBB\xBF/', '', (string) $c)), fgetcsv($f) ?: []);
    while (($r = fgetcsv($f)) !== false) {
        // Las columnas vacías del final (rol, delegacion) son opcionales.
        if (count($r) >= 3 && trim((string) $r[0]) !== '') {
            $r = array_slice(array_pad(array_map('trim', $r), count($cabecera), ''), 0, count($cabecera));
            $filas[] = array_combine($cabecera, $r);
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
    $rol = ROLES[strtolower(($fila['rol'] ?? '') !== '' ? $fila['rol'] : 'delegado')] ?? '';
    // Sin columna «delegacion», la ficha se busca por el nombre de la cuenta.
    $titulo = ($fila['delegacion'] ?? '') !== '' ? $fila['delegacion'] : ($fila['nombre'] ?? '');
    $ficha = $por_titulo[mb_strtolower($titulo)] ?? null;
    $existente = get_user_by('login', $login) ?: get_user_by('email', $correo);
    $problema = '';
    if ($login === '' || !is_email($correo)) {
        $problema = 'usuario o correo no válidos';
    } elseif ($rol === '') {
        $problema = 'rol desconocido (usa ejecutivo, delegado o estudiante)';
    } elseif ($existente && in_array('administrator', $existente->roles, true)) {
        $problema = 'es administrador: no se modifica desde este script';
    }
    if ($problema) {
        ++$errores;
        echo "  ✗ {$login}: {$problema}\n";
        continue;
    }
    echo '  ' . ($existente ? '↻ actualizar ' : '+ crear ') . "{$login} ({$correo}) → {$rol}"
        . ($rol === 'cadus_delegado' ? ($ficha ? " · ficha «{$ficha->post_title}»" : " · ⚠ no hay ninguna ficha titulada «{$titulo}»: se asignará al volver a ejecutar cuando exista") : '') . "\n";
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
    if ($rol === 'cadus_delegado' && $ficha) {
        wp_update_post(['ID' => $ficha->ID, 'post_author' => $id]);
    }
    if ($avisar) {
        wp_new_user_notification($id, null, 'user'); // requiere correo saliente configurado en el servidor
    }
}
echo $errores ? "Terminado con {$errores} fila(s) con problemas.\n" : "Terminado sin problemas.\n";
