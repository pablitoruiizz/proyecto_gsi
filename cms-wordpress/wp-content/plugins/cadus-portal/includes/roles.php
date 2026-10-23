<?php
/**
 * Roles y capacidades del portal (HU-13, RF-14, RN-01, RN-03, RN-04).
 *
 * Contrato con el resto de módulos:
 *  - cadus_caps_cpt($singular, $plural): lista de capacidades de un tipo de contenido.
 *  - Roles: cadus_ejecutiva, cadus_delegado, cadus_estudiante (+ administrator).
 *  - Tipos con capacidades propias: cadus_acta, cadus_delegacion, cadus_ticket.
 *    Se registran con 'capability_type' => ['cadus_acta', 'cadus_actas'] y 'map_meta_cap' => true.
 */

if (!defined('ABSPATH')) {
    exit;
}

define('CADUS_ROLES_VERSION', '3'); // 3: capacidades de las solicitudes de mediación (HU-12)
add_action('init', 'cadus_actualizar_roles', 5);

/** Aplica las migraciones de roles una sola vez por versión, sin reactivar el plugin. */
function cadus_actualizar_roles(): void
{
    if (get_option('cadus_roles_version') !== CADUS_ROLES_VERSION) {
        cadus_registrar_roles();
    }
}

/** Capacidades primitivas de un tipo de contenido con capability_type [singular, plural]. */
function cadus_caps_cpt(string $singular, string $plural): array
{
    return [
        "edit_{$singular}", "read_{$singular}", "delete_{$singular}",
        "edit_{$plural}", "edit_others_{$plural}", "publish_{$plural}",
        "read_private_{$plural}", "delete_{$plural}", "delete_private_{$plural}",
        "delete_published_{$plural}", "delete_others_{$plural}",
        "edit_private_{$plural}", "edit_published_{$plural}", "create_{$plural}",
    ];
}

/** Actualiza nombre y capacidades; solo retira las indicadas, conservando las personalizadas. */
function cadus_asegurar_rol(string $slug, string $nombre, array $caps, array $retirar = []): void
{
    $rol = get_role($slug);
    if (!$rol) {
        $rol = add_role($slug, $nombre, $caps);
    }
    foreach ($caps as $cap => $permitida) {
        $rol->add_cap($cap, (bool) $permitida);
    }
    foreach ($retirar as $cap) {
        $rol->remove_cap($cap);
    }

    $roles = wp_roles();
    if ($roles->roles[$slug]['name'] !== $nombre) {
        $roles->roles[$slug]['name'] = $nombre;
        $roles->role_names[$slug] = $nombre;
        update_option($roles->role_key, $roles->roles);
    }
}

/** Crea o actualiza los roles. Idempotente: se puede llamar en cada activación. */
function cadus_registrar_roles(): void
{
    $tipos = [['cadus_acta', 'cadus_actas'], ['cadus_delegacion', 'cadus_delegacions'], ['cadus_ticket', 'cadus_tickets'], ['cadus_mediacion', 'cadus_mediaciones']];

    // Ejecutivo: gestiona contenidos, aprueba y publica actas (RN-01) y atiende el buzón (RN-03).
    $ejecutiva = ['read' => true, 'upload_files' => true, 'edit_posts' => true, 'edit_others_posts' => true,
        'edit_published_posts' => true, 'publish_posts' => true, 'delete_posts' => true, 'delete_published_posts' => true,
        'edit_pages' => true, 'edit_published_pages' => true, 'publish_pages' => true, 'manage_categories' => true];
    foreach ($tipos as [$s, $p]) {
        foreach (cadus_caps_cpt($s, $p) as $cap) {
            $ejecutiva[$cap] = true;
        }
    }
    cadus_asegurar_rol('cadus_ejecutiva', 'Ejecutivo del CADUS', $ejecutiva, ['moderate_comments']);

    // Delegado: solo edita su propia delegación (RN-04); no publica actas ni ve tickets.
    cadus_asegurar_rol('cadus_delegado', 'Delegado de centro', [
        'read' => true, 'upload_files' => true,
        'edit_cadus_delegacions' => true, 'edit_published_cadus_delegacions' => true,
    ]);

    // Estudiante: solo lectura y uso de formularios.
    cadus_asegurar_rol('cadus_estudiante', 'Estudiante US', ['read' => true]);

    // El administrador conserva todas las capacidades de los tipos propios.
    $admin = get_role('administrator');
    if ($admin) {
        foreach ($tipos as [$s, $p]) {
            foreach (cadus_caps_cpt($s, $p) as $cap) {
                $admin->add_cap($cap);
            }
        }
    }

    // La activación también deja registrada la versión para no repetir la migración en init.
    update_option('cadus_roles_version', CADUS_ROLES_VERSION);
}
