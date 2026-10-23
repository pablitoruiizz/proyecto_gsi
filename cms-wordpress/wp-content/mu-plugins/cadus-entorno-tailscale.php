<?php
/**
 * Plugin Name: CADUS · Entorno compartido por Tailscale
 * Description: En desarrollo, usa como dirección del sitio la misma por la que se entra (localhost o Tailscale), para que estilos, imágenes y enlaces carguen para todo el equipo. No actúa con un dominio real.
 * Author: Equipo GSI - CADUS
 *
 * Problema: WordPress guarda una única dirección del sitio (p. ej. http://localhost/proyecto_gsi/cms-wordpress).
 * Quien entra por Tailscale (http://100.x.y.z/...) recibe la página, pero los CSS y JS apuntan a «localhost»,
 * es decir, a su propio ordenador, y la web se ve sin estilos.
 *
 * Solución: si se entra por localhost o por Tailscale (IP 100.64.0.0/10 o nombre *.ts.net) y la dirección guardada
 * también es de desarrollo, se sustituye su servidor por el de la petición actual, conservando la ruta.
 * Con un dominio real (cadus.us.es) no cambia nada. Es un mu-plugin: se carga siempre y no hay que activarlo.
 * Equivale a definir WP_HOME y WP_SITEURL en wp-config.php, que no se versiona.
 */

if (!defined('ABSPATH')) {
    exit;
}

/** ¿Es un servidor de desarrollo? localhost, 127.0.0.1, IP de Tailscale (100.64.0.0/10) o MagicDNS (*.ts.net). */
function cadus_entorno_es_desarrollo(string $host): bool
{
    $host = strtolower(preg_replace('/:\d+$/', '', $host));
    if (in_array($host, ['localhost', '127.0.0.1'], true) || str_ends_with($host, '.ts.net')) {
        return true;
    }
    if (filter_var($host, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
        $partes = explode('.', $host);
        return (int) $partes[0] === 100 && (int) $partes[1] >= 64 && (int) $partes[1] <= 127;
    }
    return false;
}

/** Servidor de la petición actual, solo si es de desarrollo y con un formato válido; si no, cadena vacía. */
function cadus_entorno_host_actual(): string
{
    $host = (string) ($_SERVER['HTTP_HOST'] ?? '');
    if ($host === '' || !preg_match('/^[A-Za-z0-9.\-]+(:\d{1,5})?$/', $host)) {
        return ''; // WP-CLI, tareas programadas o una cabecera manipulada: no se toca nada
    }
    return cadus_entorno_es_desarrollo($host) ? $host : '';
}

/** Cambia el servidor de una URL guardada por el actual, si ambos son de desarrollo. */
function cadus_entorno_url(string $url): string
{
    $actual = cadus_entorno_host_actual();
    $guardado = (string) wp_parse_url($url, PHP_URL_HOST);
    $puerto = wp_parse_url($url, PHP_URL_PORT);
    if ($actual === '' || $guardado === '' || !cadus_entorno_es_desarrollo($guardado)) {
        return $url;
    }
    $origen = $guardado . ($puerto ? ':' . $puerto : '');
    return (string) preg_replace('#^(https?://)' . preg_quote($origen, '#') . '#i', '${1}' . $actual, $url, 1);
}

add_filter('option_home', 'cadus_entorno_url');
add_filter('option_siteurl', 'cadus_entorno_url');

/** Las imágenes y enlaces escritos dentro del contenido guardan la dirección antigua: se corrigen al mostrarlos. */
add_filter('the_content', function (string $contenido): string {
    $actual = untrailingslashit((string) get_option('home'));         // con el servidor de esta visita
    remove_filter('option_home', 'cadus_entorno_url');
    $guardada = untrailingslashit((string) get_option('home'));       // la que hay en la base de datos
    add_filter('option_home', 'cadus_entorno_url');
    return $actual === $guardada ? $contenido : str_replace($guardada, $actual, $contenido);
}, 99);
