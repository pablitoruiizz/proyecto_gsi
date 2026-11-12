<?php
/**
 * Directorio de delegaciones con los datos publicados en www.cadus.us.es/delegaciones/ (HU-05, HU-06).
 *
 * - data/delegaciones.json: una entrada por centro (miembros, correo, teléfono, Instagram y escudo).
 * - assets/escudos/*.png: escudos reducidos a 320 px (los originales pesaban hasta 6,5 MB).
 * - cadus_delegaciones_cargar() es idempotente: crea la ficha si no existe, y en las existentes solo rellena
 *   los campos vacíos, de modo que nunca pisa lo que haya editado una delegación desde el portal.
 *   Se llama al activar el plugin y también se puede lanzar sola con scripts/entrega/cargar_delegaciones.php.
 */

if (!defined('ABSPATH')) {
    exit;
}

/** Escudo de una delegación (imagen decorativa: el nombre del centro va siempre al lado, en texto). */
function cadus_delegacion_escudo(int $id, string $clase = 'cadus-escudo'): string
{
    $adjunto = (int) cadus_campo('escudo', $id);
    if ($adjunto <= 0) {
        return '';
    }
    return wp_get_attachment_image($adjunto, 'medium', false, ['class' => $clase, 'alt' => '', 'loading' => 'lazy', 'decoding' => 'async']);
}

/** Miembros como lista (una línea por persona). */
function cadus_delegacion_miembros(int $id): array
{
    return array_values(array_filter(array_map('trim', preg_split('/\R/', (string) cadus_campo('miembros', $id)) ?: [])));
}

/** @return array{creadas:int,actualizadas:int,sin_escudo:int} */
function cadus_delegaciones_cargar(): array
{
    $res = ['creadas' => 0, 'actualizadas' => 0, 'sin_escudo' => 0];
    $ruta = CADUS_PORTAL_DIR . 'data/delegaciones.json';
    $datos = is_readable($ruta) ? json_decode((string) file_get_contents($ruta), true) : null;
    if (!is_array($datos)) {
        return $res;
    }
    foreach ($datos as $d) {
        $centro = trim((string) ($d['centro'] ?? ''));
        if ($centro === '') {
            continue;
        }
        if (!term_exists($centro, 'cadus_centro')) {
            wp_insert_term($centro, 'cadus_centro');
        }
        $titulo = 'Delegación de ' . $centro;
        $clave = 'delegacion:' . sanitize_title($centro);
        $ficha = cadus_buscar_semilla($clave, 'cadus_delegacion', $titulo);
        if ($ficha) {
            $id = (int) $ficha->ID;
            ++$res['actualizadas'];
            // La ficha sembrada antes llevaba un texto de relleno que ya no es cierto.
            if (str_contains((string) $ficha->post_content, 'Ficha pendiente de completar')) {
                wp_update_post(['ID' => $id, 'post_content' => '']);
            }
        } else {
            $nuevo = wp_insert_post(['post_type' => 'cadus_delegacion', 'post_status' => 'publish', 'post_title' => $titulo, 'post_author' => 1], true);
            if (is_wp_error($nuevo) || (int) $nuevo <= 0) {
                continue;
            }
            $id = (int) $nuevo;
            update_post_meta($id, '_cadus_semilla', $clave);
            ++$res['creadas'];
        }
        // Una ficha ya importada una vez no se vuelve a rellenar: lo que se vacíe a propósito (un miembro retirado, un centro
        // sin asignar) tiene que seguir vacío. Solo se repara el escudo si su archivo ha desaparecido.
        $importada = (bool) get_post_meta($id, '_cadus_importada', true);
        if (!$importada && !wp_get_post_terms($id, 'cadus_centro', ['fields' => 'ids'])) {
            wp_set_object_terms($id, $centro, 'cadus_centro');
        }
        $valores = $importada ? [] : [
            ['field_cadus_deleg_miembros', 'miembros', implode("\n", array_map('strval', $d['miembros'] ?? []))],
            ['field_cadus_deleg_correo', 'correo', (string) ($d['correo'] ?? '')],
            ['field_cadus_deleg_tel', 'telefono', (string) ($d['telefono'] ?? '')],
            ['field_cadus_deleg_instagram', 'instagram', (string) ($d['instagram'] ?? '')],
        ];
        foreach ($valores as [$clave_acf, $nombre, $valor]) {
            if ($valor !== '' && (string) cadus_campo($nombre, $id) === '') {
                cadus_gestion_campo($clave_acf, $nombre, $valor, $id);
            }
        }
        $escudo = (int) cadus_campo('escudo', $id);
        $roto = $escudo > 0 && (!get_post($escudo) || !is_file((string) get_attached_file($escudo)));
        if ($roto || (!$importada && $escudo <= 0)) {
            $archivo = (string) ($d['escudo'] ?? '');
            $adjunto = $archivo !== '' ? cadus_adjuntar('assets/escudos/' . basename($archivo), 'Escudo de ' . $centro) : 0;
            if ($adjunto > 0) {
                cadus_gestion_campo('field_cadus_deleg_escudo', 'escudo', $adjunto, $id);
            } else {
                ++$res['sin_escudo'];
            }
        }
        update_post_meta($id, '_cadus_importada', '1');
    }
    delete_transient('cadus_portada_datos');
    return $res;
}
