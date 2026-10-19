<?php
/**
 * Plugin Name: CADUS Portal
 * Description: Plugin propio del portal del CADUS: roles, actas y normativas, delegaciones, buzón de consultas y contenido base del sitio.
 * Version: 1.0.0
 * Author: Equipo GSI - CADUS
 * Text Domain: cadus-portal
 * Requires PHP: 8.0
 */

if (!defined('ABSPATH')) {
    exit;
}

define('CADUS_PORTAL_VERSION', '1.0.0');
define('CADUS_PORTAL_DIR', plugin_dir_path(__FILE__));
define('CADUS_PORTAL_URL', plugin_dir_url(__FILE__));

require_once CADUS_PORTAL_DIR . 'includes/roles.php';        // roles y capacidades (HU-13)
require_once CADUS_PORTAL_DIR . 'includes/admin.php';        // menús de administración por rol (HU-19a)
require_once CADUS_PORTAL_DIR . 'includes/contenidos.php';    // actas, delegaciones, directorio (HU-03..06)
require_once CADUS_PORTAL_DIR . 'includes/buzon.php';         // buzón, tickets y seguimiento (HU-07, HU-08)
require_once CADUS_PORTAL_DIR . 'includes/setup.php';         // páginas, menú, noticias y tema (HU-01, HU-02, HU-18)
require_once CADUS_PORTAL_DIR . 'includes/inicio.php';        // portada inmersiva: hero, accesos y buscador
require_once CADUS_PORTAL_DIR . 'includes/portada_extra.php'; // presentación, novedades, eventos, trabajo y contacto
require_once CADUS_PORTAL_DIR . 'includes/galeria.php';       // galería de fotos del CADUS
require_once CADUS_PORTAL_DIR . 'includes/estilo.php';        // estilos y movimiento

register_activation_hook(__FILE__, 'cadus_portal_activar');
