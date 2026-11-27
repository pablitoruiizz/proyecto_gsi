# Volcado de demostración de la base de datos del portal CADUS

`bd_cadus_v1_sprint3.sql` es una **copia saneada** de la base `bd_cadus` para evaluar el portal: conserva la estructura, los roles, las páginas, las noticias, las actas, las 27 fichas de delegaciones, el calendario y la configuración del plugin.

## Qué se quitó
- Las cuentas reales del equipo y sus correos personales, contraseñas cifradas, sesiones y datos de perfil.
- Los registros de inicio de sesión, de actividad y de diagnóstico de Wordfence, y su clave de instalación.
- Los visitantes de las estadísticas, las cachés temporales y las sales.
- No hay tickets, solicitudes de mediación ni cuentas de prueba.

## Cuentas de demostración
| Usuario | Rol | Correo (ficticio) |
|---|---|---|
| `demo-admin` | Administrador | demo-admin@example.org |
| `demo-ejecutiva` | Ejecutivo del CADUS | demo-ejecutiva@example.org |
| `demo-delegado` | Delegado de centro (edita solo la ficha de la delegación de la ETSII) | demo-delegado@example.org |

Contraseña de las tres: `croGTZH5oRVFx3`. Son cuentas de demostración: cambia la contraseña si el portal se publica.

## Cómo restaurarlo
1. Crear la base `bd_cadus` con cotejamiento `utf8mb4_unicode_ci` e importar el `.sql` (phpMyAdmin › Importar, o `mysql`).
2. Copiar WordPress y `wp-content` y crear `wp-config.php` con los datos de esa base y claves propias.
3. Si la dirección web no es `http://localhost/proyecto_gsi/cms-wordpress`, cambiar `siteurl` y `home` en *Ajustes › Generales*.
4. Entrar con una de las cuentas anteriores y vaciar la caché de WP Fastest Cache.

Wordfence no tiene su clave de instalación: al abrirlo pedirá registrarse de nuevo (es opcional para evaluar el portal).
