<?php
// Carga (o completa) las delegaciones de data/delegaciones.json en el portal. Idempotente.
// Uso: php scripts/entrega/cargar_delegaciones.php
$_SERVER['HTTP_HOST'] = 'localhost';
require dirname(__DIR__, 2) . '/cms-wordpress/wp-load.php';
wp_set_current_user(1);
print_r(cadus_delegaciones_cargar());
echo wp_count_posts('cadus_delegacion')->publish, " delegaciones publicadas\n";
