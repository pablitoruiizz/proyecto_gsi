<?php
/**
 * Volcado de la base de datos del portal con PHP (para cuando mysqldump no puede conectar con caching_sha2_password).
 * Uso: php scripts/entrega/volcado_bd.php [ruta.sql]   (por defecto cms-wordpress/backup-db/bd_cadus_v1_sprint2.sql)
 * El fichero contiene hashes de contraseñas y datos del sitio: no se sube a GitHub (ver cms-wordpress/backup-db/README.md).
 */
$_SERVER['HTTP_HOST'] = 'localhost';
require __DIR__ . '/../../cms-wordpress/wp-load.php';
global $wpdb;

$destino = $argv[1] ?? __DIR__ . '/../../cms-wordpress/backup-db/bd_cadus_v1_sprint2.sql';
$f = fopen($destino, 'w');
fwrite($f, "-- Volcado de la base de datos del portal CADUS (Sprint 2)\n-- Generado el " . gmdate('Y-m-d H:i:s') . " UTC con scripts/entrega/volcado_bd.php\n");
fwrite($f, "-- Base: " . DB_NAME . " · MySQL " . $wpdb->db_version() . "\n\n");
fwrite($f, "/*!40101 SET NAMES utf8mb4 */;\nSET FOREIGN_KEY_CHECKS=0;\nSET UNIQUE_CHECKS=0;\nSET SQL_MODE='NO_AUTO_VALUE_ON_ZERO';\n\n");

$tablas = $wpdb->get_col('SHOW TABLES');
$filas_total = 0;
foreach ($tablas as $tabla) {
    $crear = $wpdb->get_row("SHOW CREATE TABLE `$tabla`", ARRAY_N);
    fwrite($f, "--\n-- Tabla `$tabla`\n--\n\nDROP TABLE IF EXISTS `$tabla`;\n" . $crear[1] . ";\n\n");
    $columnas = $wpdb->get_results("SHOW COLUMNS FROM `$tabla`", ARRAY_A);
    $numericas = [];
    $binarias = [];
    foreach ($columnas as $i => $c) {
        $numericas[$i] = (bool) preg_match('/^(tinyint|smallint|mediumint|int|bigint|decimal|float|double)/i', $c['Type']);
        $binarias[$i] = (bool) preg_match('/binary|blob/i', $c['Type']);
    }
    $desde = 0;
    $paso = 200;
    while (true) {
        $filas = $wpdb->get_results("SELECT * FROM `$tabla` LIMIT $desde, $paso", ARRAY_N);
        if (!$filas) {
            break;
        }
        $valores = [];
        foreach ($filas as $fila) {
            $celdas = [];
            foreach ($fila as $i => $v) {
                $celdas[] = $v === null ? 'NULL' : ($numericas[$i] ? $v : ($binarias[$i] ? ($v === '' ? "''" : '0x' . bin2hex($v)) : "'" . $wpdb->_real_escape($v) . "'"));
            }
            $valores[] = '(' . implode(',', $celdas) . ')';
        }
        fwrite($f, "INSERT INTO `$tabla` VALUES " . implode(",\n", $valores) . ";\n");
        $filas_total += count($filas);
        $desde += $paso;
    }
    fwrite($f, "\n");
}
fwrite($f, "SET FOREIGN_KEY_CHECKS=1;\nSET UNIQUE_CHECKS=1;\n-- Fin del volcado\n");
fclose($f);
echo count($tablas), " tablas, $filas_total filas -> ", realpath($destino), "\n";
