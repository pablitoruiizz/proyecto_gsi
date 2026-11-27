# Volcado de demostración de la base de datos del portal CADUS

`bd_cadus_v1_sprint3.sql` es una **copia saneada** de la base `bd_cadus` para evaluar el portal: conserva la estructura, los roles, las páginas, las noticias, las actas, las 27 fichas de delegaciones, el calendario y la configuración del plugin.

## Qué se quitó
- Las cuentas reales del equipo y sus correos personales, contraseñas cifradas, sesiones y datos de perfil.
- Los registros de inicio de sesión, de actividad y de diagnóstico de Wordfence, y su clave de instalación.
- Los visitantes y las cifras de visitas de WP Statistics, el estado y los avisos internos de Wordfence, las cachés temporales y las sales.
- No hay tickets, solicitudes de mediación ni cuentas de prueba.

## Cuentas de demostración
| Usuario | Rol | Correo (ficticio) |
|---|---|---|
| `demo-admin` | Administrador | demo-admin@example.org |
| `demo-ejecutiva` | Ejecutivo del CADUS | demo-ejecutiva@example.org |
| `demo-delegado` | Delegado de centro (edita solo la ficha de la delegación de la ETSII) | demo-delegado@example.org |

Contraseña de las tres: `0z3qeIQZ5Xiw9d`. Son cuentas de demostración: cambia la contraseña si el portal se publica.

## Cómo restaurarlo
1. Crear la base `bd_cadus` con cotejamiento `utf8mb4_unicode_ci` e importar el `.sql` (phpMyAdmin › Importar, o `mysql`).
2. Copiar WordPress y `wp-content` y crear `wp-config.php` con los datos de esa base y claves propias.
3. El volcado se generó con la dirección `http://localhost/proyecto_gsi/cms-wordpress` (`siteurl` y `home`), y esa dirección también está en el contenido y en la caché de Yoast. Lo más simple es restaurarlo en una instalación con esa misma dirección. Para otra dirección, fija `WP_HOME` y `WP_SITEURL` en `wp-config.php` antes del primer acceso y migra las direcciones del contenido con una herramienta que respete los datos serializados (por ejemplo, `wp search-replace` de WP-CLI); no basta con cambiar *Ajustes › Generales*.
4. Entrar con una de las cuentas anteriores y vaciar la caché de WP Fastest Cache.

Wordfence no tiene su clave de instalación: al abrirlo pedirá registrarse de nuevo (es opcional para evaluar el portal).
