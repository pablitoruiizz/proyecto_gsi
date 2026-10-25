# Entrega 2 · Portal web del CADUS (CMS en WordPress)

| Fichero | Contenido |
|---|---|
| `Entrega2-CMS-CADUS.pdf` | Documento de la entrega (estilo REMUS): planificación, REM 2.0, análisis, diseño, implementación, trazabilidad y calidad |
| `CADUS-REM-v2.pdf` | Documento de requisitos tal como lo genera REMUS (versión 2.0) |
| `CADUS.rem` | Proyecto REMUS con los requisitos (versión 2.0) |
| `bd_cadus_v1_sprint2.sql` | Volcado de la base de datos del Sprint 2 (contiene las contraseñas cifradas de los usuarios: no se publica) |
| `wp-content-uploads.zip` | Medios del sitio (carpeta `wp-content/uploads`): el volcado referencia estos archivos |
| `plugin-cadus-portal.zip` | Plugin propio del portal (CADUS Portal) |
| `burndown-sprint-02.png` / `.csv` | Burndown chart del Sprint 2 y sus datos |

Mockups en Figma: https://www.figma.com/design/IZ4OfXGSS6T8WLToDq8f8s/CADUS---Mockups-entrega-2

Seguimiento SCRUM: https://github.com/users/pablitoruiizz/projects/1 (público). Repositorio: https://github.com/pablitoruiizz/proyecto_gsi

## Restaurar el portal en otro equipo
1. Instalar WordPress 7.1 (Wamp o XAMPP, PHP 8.x y MySQL 8.x), crear la base `bd_cadus` y restaurar `bd_cadus_v1_sprint2.sql` (si el sitio cambia de dirección, actualizar `siteurl` y `home` en `wp_options`).
2. Copiar el contenido del repositorio `cms-wordpress/` a la carpeta del servidor y ajustar `wp-config.php` (base de datos).
3. Descomprimir `wp-content-uploads.zip` dentro de `wp-content/` (el zip ya contiene la carpeta `uploads/`) y `plugin-cadus-portal.zip` dentro de `wp-content/plugins/` (contiene la carpeta `cadus-portal/`; el plugin también está en el repositorio).
4. Activar el plugin **CADUS Portal**, entrar con la cuenta `cadus` (`¿Has olvidado tu contraseña?` envía el enlace a dcadus@us.es) y comprobar los menús, la portada y el calendario.
