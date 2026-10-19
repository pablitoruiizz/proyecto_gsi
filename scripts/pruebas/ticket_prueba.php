<?php
/**
 * Ticket de prueba para las comprobaciones de privacidad (RN-03).
 * Uso (CLI): php ticket_prueba.php crear | borrar | roles
 *   crear  → inserta un ticket privado con el texto «TEXTO-SECRETO-RN03» y escribe su ID.
 *   borrar → elimina TODOS los tickets de prueba (código CAD-2026-99999).
 *   roles  → matriz de capacidades sobre tickets por rol (JSON).
 */
$_SERVER['HTTP_HOST'] = 'localhost';
define('WP_USE_THEMES', false);
require dirname(__DIR__, 2) . '/cms-wordpress/wp-load.php';

const CODIGO = 'CAD-2026-99999';
$accion = $argv[1] ?? '';

function tickets_de_prueba(): array
{
    return get_posts(['post_type' => 'cadus_ticket', 'post_status' => 'any', 'numberposts' => -1, 'fields' => 'ids',
        'meta_key' => '_cadus_codigo', 'meta_value' => CODIGO]);
}

if ($accion === 'crear') {
    $id = wp_insert_post(['post_type' => 'cadus_ticket', 'post_status' => 'private', 'post_title' => '[' . CODIGO . '] Asunto de prueba',
        'post_content' => 'TEXTO-SECRETO-RN03 detalle de la reclamación de prueba'], true);
    if (is_wp_error($id)) {
        fwrite(STDERR, $id->get_error_message() . "\n");
        exit(1);
    }
    update_post_meta($id, '_cadus_codigo', CODIGO);
    update_post_meta($id, '_cadus_email', 'prueba@alum.us.es');
    update_post_meta($id, '_cadus_tipo', 'Reclamación');
    update_post_meta($id, '_cadus_estado', 'abierto');
    echo $id, "\n";
} elseif ($accion === 'borrar') {
    foreach (tickets_de_prueba() as $id) {
        wp_delete_post($id, true);
    }
    echo count(tickets_de_prueba()) === 0 ? "borrados\n" : "QUEDAN tickets de prueba\n";
} elseif ($accion === 'roles') {
    $salida = [];
    foreach (['administrator', 'cadus_ejecutiva', 'cadus_delegado', 'cadus_estudiante', 'subscriber'] as $rol) {
        $u = new WP_User();
        $u->ID = 999999;
        $u->roles = [$rol];
        $u->caps = [$rol => true];
        $u->get_role_caps();
        $ids = tickets_de_prueba();
        $id = $ids[0] ?? 0;
        $salida[$rol] = [
            'ver_listado' => user_can($u, 'edit_cadus_tickets'),
            'leer_ticket' => $id ? user_can($u, 'read_post', $id) : null,
            'editar_ticket' => $id ? user_can($u, 'edit_post', $id) : null,
            'borrar_ticket' => $id ? user_can($u, 'delete_post', $id) : null,
            'leer_privados' => user_can($u, 'read_private_cadus_tickets'),
        ];
    }
    echo json_encode($salida, JSON_PRETTY_PRINT), "\n";
}
