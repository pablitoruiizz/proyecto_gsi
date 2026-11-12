<?php
/**
 * Optimización de las imágenes que sube el equipo (HU-20a · RNF de rendimiento).
 *
 * WordPress ya genera varios tamaños de cada imagen, añade srcset/sizes y carga diferida (loading="lazy")
 * en el contenido, y da prioridad a la primera imagen. Este módulo ajusta lo que falta para la web del CADUS:
 *  - Las fotos de más de 1920 px (las de móvil suelen tener 4000 px) se reducen a 1920 px al subirlas;
 *    el original grande no se sirve nunca, y no se genera el tamaño «2048x2048», que superaría ese máximo.
 *  - Los tamaños intermedios de JPEG y PNG se guardan en WebP (entre un 25 % y un 35 % menos de peso),
 *    solo si el servidor sabe generarlo (GD o Imagick con WebP). Si no, se quedan en su formato.
 *  - Calidad 82 en JPEG y WebP (la de WordPress por defecto es 82 en JPEG y 86 en WebP).
 *  - Se rechazan imágenes de más de 8 MB, con un mensaje que explica cómo reducirlas.
 * No se toca la carga diferida del contenido: WordPress ya la pone, salvo en las primeras imágenes, a las que
 * da fetchpriority="high" para no retrasar el primer pintado; forzarla ahí empeoraría el LCP.
 * Las imágenes propias del plugin ya van optimizadas en assets/ (scripts/imagenes/optimizar_imagenes.py): la galería en
 * WebP, el logotipo y los 25 escudos de las delegaciones en PNG con paleta (de 1,6 MB a 0,3 MB). Los escudos y el logotipo
 * se copian a la biblioteca de medios al instalar; en una web ya instalada, cadus_img_actualizar_semillas() cambia una sola
 * vez esas copias por las optimizadas y rehace sus tamaños (que pasan a WebP), sin tocar las imágenes subidas por el equipo.
 */

if (!defined('ABSPATH')) {
    exit;
}

const CADUS_IMG_MAX_PX = 1920;
const CADUS_IMG_MAX_MB = 8;
const CADUS_IMG_CALIDAD = 82;
define('CADUS_IMG_SEMILLAS_VERSION', '1');

add_filter('big_image_size_threshold', static fn(): int => CADUS_IMG_MAX_PX);
add_filter('wp_editor_set_quality', static fn(): int => CADUS_IMG_CALIDAD);
add_filter('image_editor_output_format', 'cadus_img_formato_salida');
add_filter('wp_image_editors', static function (array $editores): array {
    // GD con soporte de imágenes con paleta (escudos y logotipo): ver includes/imagenes-gd.php.
    if (class_exists('WP_Image_Editor_GD') && !class_exists('Cadus_Image_Editor_GD')) {
        require_once __DIR__ . '/imagenes-gd.php';
    }
    return array_map(static fn(string $e): string => $e === 'WP_Image_Editor_GD' ? 'Cadus_Image_Editor_GD' : $e, $editores);
});
add_filter('wp_handle_upload_prefilter', 'cadus_img_limite_subida');
add_action('admin_init', function () {
    if (get_option('cadus_portal_version') && get_option('cadus_img_semillas_version') !== CADUS_IMG_SEMILLAS_VERSION) {
        cadus_img_actualizar_semillas();
    }
});
add_filter('intermediate_image_sizes_advanced', static function (array $tamanos): array {
    unset($tamanos['2048x2048']);
    return $tamanos;
});

/** ¿Puede este servidor guardar WebP? (se calcula una vez por petición) */
function cadus_img_webp_disponible(): bool
{
    static $si = null;
    if ($si === null) {
        $si = function_exists('wp_image_editor_supports') && wp_image_editor_supports(['mime_type' => 'image/webp']);
    }
    return $si;
}

/** JPEG y PNG se guardan en WebP en los tamaños que genera WordPress. GIF (animaciones) y SVG no se tocan. */
function cadus_img_formato_salida(array $formatos): array
{
    if (cadus_img_webp_disponible()) {
        $formatos['image/jpeg'] = 'image/webp';
        $formatos['image/png'] = 'image/webp';
    }
    return $formatos;
}

/** Límite de peso solo para imágenes: los PDF de actas tienen su propio límite (el del servidor). */
function cadus_img_limite_subida(array $archivo): array
{
    $tipo = (string) ($archivo['type'] ?? '');
    if (strpos($tipo, 'image/') === 0 && (int) ($archivo['size'] ?? 0) > CADUS_IMG_MAX_MB * MB_IN_BYTES) {
        $archivo['error'] = sprintf(
            'La imagen pesa %s y el máximo es %d MB. Redúcela antes de subirla (por ejemplo, a 1920 px de ancho con squoosh.app) y vuelve a intentarlo.',
            size_format((int) $archivo['size'], 1),
            CADUS_IMG_MAX_MB
        );
    }
    return $archivo;
}

/**
 * Cambia por su versión optimizada las copias que el plugin hizo en la biblioteca de medios (escudos «Escudo de …» y
 * «Logotipo CADUS (oficial)») y regenera sus tamaños. Solo toca adjuntos creados por el plugin cuyo archivo se llama
 * igual que el del plugin: un escudo que una delegación haya subido después es otro adjunto y no se toca.
 * Devuelve cuántas imágenes se han actualizado.
 */
function cadus_img_actualizar_semillas(): int
{
    require_once ABSPATH . 'wp-admin/includes/image.php';
    global $wpdb;
    $ids = $wpdb->get_col($wpdb->prepare(
        "SELECT ID FROM {$wpdb->posts} WHERE post_type = 'attachment' AND (post_title LIKE %s OR post_title = %s)",
        $wpdb->esc_like('Escudo de ') . '%',
        'Logotipo CADUS (oficial)'
    ));
    $hechas = 0;
    foreach (array_map('intval', $ids) as $id) {
        $ruta = (string) get_attached_file($id);
        // wp_upload_bits añade «-1», «-2»… si el nombre ya existía: se quita para encontrar el archivo del plugin.
        $nombre = preg_replace('/-\d+(\.png)$/i', '$1', basename($ruta));
        $semilla = CADUS_PORTAL_DIR . 'assets/' . (strpos($nombre, 'logo-cadus') === 0 ? '' : 'escudos/') . $nombre;
        if (!is_file($ruta) || !is_readable($semilla) || md5_file($ruta) === md5_file($semilla)) {
            continue;
        }
        // Se borran los tamaños antiguos (PNG) antes de rehacerlos.
        $meta = wp_get_attachment_metadata($id);
        foreach ((array) ($meta['sizes'] ?? []) as $tam) {
            if (!empty($tam['file'])) {
                wp_delete_file(path_join(dirname($ruta), $tam['file']));
            }
        }
        if (copy($semilla, $ruta)) {
            wp_update_attachment_metadata($id, wp_generate_attachment_metadata($id, $ruta));
            ++$hechas;
        }
    }
    update_option('cadus_img_semillas_version', CADUS_IMG_SEMILLAS_VERSION);
    return $hechas;
}
