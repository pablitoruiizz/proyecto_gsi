<?php
/**
 * Editor de imágenes GD que puede guardar en WebP las imágenes con paleta (HU-20a).
 *
 * GD no admite pasar a WebP una imagen indexada (PNG de 256 colores, como los escudos o el logotipo optimizados):
 * imagewebp() avisa «Palette image not supported by webp» y deja un archivo vacío. Antes de guardar en WebP o AVIF,
 * la imagen se pasa a color verdadero, conservando la transparencia. El resto es el editor GD de WordPress.
 * Se carga desde includes/imagenes.php, en el filtro «wp_image_editors» (cuando WordPress ya ha cargado sus clases).
 */

if (!defined('ABSPATH')) {
    exit;
}

class Cadus_Image_Editor_GD extends WP_Image_Editor_GD
{
    protected function _save($image, $filename = null, $mime_type = null)
    {
        [, , $salida] = $this->get_output_format($filename, $mime_type);
        if (in_array($salida, ['image/webp', 'image/avif'], true) && function_exists('imageistruecolor') && !imageistruecolor($image)) {
            imagepalettetotruecolor($image);
            imagealphablending($image, false);
            imagesavealpha($image, true);
        }
        return parent::_save($image, $filename, $mime_type);
    }
}
