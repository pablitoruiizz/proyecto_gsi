<?php
if (PHP_SAPI !== 'cli') { http_response_code(403); exit('Solo desde la línea de comandos.'); }
/**
 * Carga en The Events Calendar los eventos reales del CADUS que hay en eventos-reales.csv (E2-19 · HU-10 · RF-11).
 *
 * Cada evento queda en su categoría («Asambleas» o «Cursos», E3-07) y con su lugar. Se puede repetir sin duplicar:
 * un evento con el mismo título y la misma fecha se actualiza en lugar de crearse otra vez.
 *
 * Uso (desde la raíz del repositorio):
 *   php scripts/eventos/cargar_eventos_reales.php                     ensayo: dice qué haría, sin cambiar nada
 *   php scripts/eventos/cargar_eventos_reales.php --aplicar           crea o actualiza los eventos
 *   php scripts/eventos/cargar_eventos_reales.php --aplicar --retirar-ejemplos
 *                                                                     además borra los eventos y la votación «(ejemplo)»
 *
 * CSV (separado por «;», con cabecera): titulo;fecha;inicio;fin;lugar;categoria;descripcion
 *   fecha dd/mm/aaaa · inicio y fin hh:mm (vacíos = todo el día) · categoria Asamblea o Curso (o vacío) · lugar y descripcion opcionales.
 */
$_SERVER['HTTP_HOST'] = $_SERVER['HTTP_HOST'] ?? 'localhost';
require __DIR__ . '/../../cms-wordpress/wp-load.php';

if (!function_exists('tribe_create_event')) {
    exit("The Events Calendar no está activo.\n");
}
$aplicar = in_array('--aplicar', $argv, true);
$retirar = in_array('--retirar-ejemplos', $argv, true);
$csv = __DIR__ . '/eventos-reales.csv';
if (!is_readable($csv)) {
    exit("No encuentro $csv.\n");
}

$categorias = ['asamblea' => 'asambleas', 'asambleas' => 'asambleas', 'curso' => 'cursos', 'cursos' => 'cursos', '' => ''];
$fichero = fopen($csv, 'r');
$cabecera = array_map(static fn($c) => strtolower(trim((string) $c, " \xEF\xBB\xBF")), (array) fgetcsv($fichero, 0, ';'));
if ($cabecera !== ['titulo', 'fecha', 'inicio', 'fin', 'lugar', 'categoria', 'descripcion']) {
    exit("La cabecera del CSV debe ser: titulo;fecha;inicio;fin;lugar;categoria;descripcion\n");
}

$errores = 0;
$linea = 1;
$filas = [];
while (($fila = fgetcsv($fichero, 0, ';')) !== false) {
    $linea++;
    if (!array_filter($fila, static fn($v) => trim((string) $v) !== '')) {
        continue;
    }
    [$titulo, $fecha, $ini, $fin, $lugar, $cat, $texto] = array_map(static fn($v) => trim((string) $v), array_pad($fila, 7, ''));
    $dia = DateTime::createFromFormat('!d/m/Y', $fecha);
    $problema = '';
    if ($titulo === '') {
        $problema = 'falta el título';
    } elseif (!$dia || $dia->format('d/m/Y') !== $fecha) {
        $problema = "fecha «{$fecha}» no válida (dd/mm/aaaa)";
    } elseif (($ini !== '' && !preg_match('/^\d{2}:\d{2}$/', $ini)) || ($fin !== '' && !preg_match('/^\d{2}:\d{2}$/', $fin))) {
        $problema = 'las horas van como hh:mm';
    } elseif ($ini !== '' && $fin !== '' && $fin <= $ini) {
        $problema = 'la hora de fin es anterior a la de inicio';
    } elseif (!array_key_exists(strtolower($cat), $categorias)) {
        $problema = "categoría «{$cat}» desconocida (Asamblea o Curso)";
    }
    if ($problema) {
        echo "✗ línea $linea: $problema\n";
        $errores++;
        continue;
    }
    $filas[] = compact('titulo', 'dia', 'ini', 'fin', 'lugar', 'cat', 'texto');
}
fclose($fichero);
if ($errores) {
    exit("Corrige las $errores línea(s) y vuelve a ejecutarlo. No se ha cambiado nada.\n");
}

/** Evento con el mismo título que empieza el mismo día (para no duplicar). */
$buscar = static function (string $titulo, string $ymd): ?int {
    foreach (get_posts(['post_type' => 'tribe_events', 'title' => $titulo, 'post_status' => 'any', 'numberposts' => -1, 'fields' => 'ids']) as $id) {
        if (strpos((string) get_post_meta($id, '_EventStartDate', true), $ymd) === 0) {
            return (int) $id;
        }
    }
    return null;
};
$lugar_id = static function (string $nombre): int {
    if ($nombre === '') {
        return 0;
    }
    $q = get_posts(['post_type' => 'tribe_venue', 'title' => $nombre, 'post_status' => 'any', 'numberposts' => 1, 'fields' => 'ids']);
    return $q ? (int) $q[0] : (int) tribe_create_venue(['Venue' => $nombre, 'post_status' => 'publish']);
};

foreach ($filas as $f) {
    $ymd = $f['dia']->format('Y-m-d');
    $existente = $buscar($f['titulo'], $ymd);
    $accion = $existente ? 'actualizar' : 'crear';
    $cat = $categorias[strtolower($f['cat'])];
    echo ($aplicar ? '✓ ' : '· ') . "$accion «{$f['titulo']}» el {$f['dia']->format('d/m/Y')}"
        . ($f['ini'] !== '' ? " {$f['ini']}–{$f['fin']}" : ' (todo el día)') . ($cat ? " [$cat]" : '') . "\n";
    if (!$aplicar) {
        continue;
    }
    $todo_el_dia = $f['ini'] === '';
    $fin = $f['fin'] !== '' ? $f['fin'] : $f['ini'];
    $datos = [
        'post_title' => $f['titulo'], 'post_content' => $f['texto'], 'post_status' => 'publish',
        'EventStartDate' => $ymd, 'EventEndDate' => $ymd, 'EventAllDay' => $todo_el_dia ? 'yes' : '',
        'EventStartHour' => $todo_el_dia ? '00' : substr($f['ini'], 0, 2), 'EventStartMinute' => $todo_el_dia ? '00' : substr($f['ini'], 3, 2),
        'EventEndHour' => $todo_el_dia ? '23' : substr($fin, 0, 2), 'EventEndMinute' => $todo_el_dia ? '59' : substr($fin, 3, 2),
    ];
    if ($f['lugar'] !== '') {
        $datos['EventVenueID'] = $lugar_id($f['lugar']);
    }
    $id = $existente ? (int) tribe_update_event($existente, $datos) : (int) tribe_create_event($datos);
    if ($id && $cat) {
        wp_set_object_terms($id, $cat, 'tribe_events_cat');
    }
}

if ($retirar) {
    $ejemplos = array_merge(
        get_posts(['post_type' => 'tribe_events', 's' => '(ejemplo)', 'post_status' => 'any', 'numberposts' => -1]),
        get_posts(['post_type' => 'cadus_votacion', 's' => '(ejemplo)', 'post_status' => 'any', 'numberposts' => -1])
    );
    foreach ($ejemplos as $p) {
        if (strpos($p->post_title, '(ejemplo)') === false) {
            continue;
        }
        echo ($aplicar ? '✓ borrar' : '· borrar') . " «{$p->post_title}»\n";
        if ($aplicar) {
            wp_delete_post($p->ID, true);
        }
    }
}

if ($aplicar) {
    delete_transient('cadus_portada_datos');
    if (isset($GLOBALS['wp_fastest_cache']) && method_exists($GLOBALS['wp_fastest_cache'], 'deleteCache')) {
        $GLOBALS['wp_fastest_cache']->deleteCache(true);
    }
}
echo $aplicar ? "Listo.\n" : "Ensayo terminado: añade --aplicar para guardar los cambios.\n";
