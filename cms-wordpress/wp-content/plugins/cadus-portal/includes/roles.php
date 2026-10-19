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

/** Crea el rol si no existe o le añade las capacidades que falten, sin borrar las que el equipo haya personalizado. */
function cadus_asegurar_rol(string $slug, string $nombre, array $caps): void
{
    $rol = get_role($slug);
    if (!$rol) {
        add_role($slug, $nombre, $caps);
        return;
    }
    foreach ($caps as $cap => $permitida) {
        $rol->add_cap($cap, (bool) $permitida);
    }
}

/** Crea o actualiza los roles. Idempotente: se puede llamar en cada activación. */
function cadus_registrar_roles(): void
{
    $tipos = [['cadus_acta', 'cadus_actas'], ['cadus_delegacion', 'cadus_delegacions'], ['cadus_ticket', 'cadus_tickets'], ['cadus_mediacion', 'cadus_mediaciones']];

    // Ejecutiva: gestiona contenidos, aprueba y publica actas (RN-01) y atiende el buzón (RN-03).
    $ejecutiva = ['read' => true, 'upload_files' => true, 'edit_posts' => true, 'edit_others_posts' => true,
        'edit_published_posts' => true, 'publish_posts' => true, 'delete_posts' => true, 'delete_published_posts' => true,
        'edit_pages' => true, 'edit_published_pages' => true, 'publish_pages' => true, 'manage_categories' => true,
        'moderate_comments' => true];
    foreach ($tipos as [$s, $p]) {
        foreach (cadus_caps_cpt($s, $p) as $cap) {
            $ejecutiva[$cap] = true;
        }
    }
    cadus_asegurar_rol('cadus_ejecutiva', 'Ejecutiva del CADUS', $ejecutiva);

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
}
