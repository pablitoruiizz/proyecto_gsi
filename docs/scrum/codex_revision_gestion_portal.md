# Revisión pedida a Codex: acceso y gestión desde el portal (HU-24, 12/11/2026)

Revisión de SOLO LECTURA (no edites archivos ni hagas commit). Responde en español, con hallazgos ordenados por gravedad (alta, media, baja), citando archivo y línea, y al final qué cambiarías.

## Contexto
Portal del CADUS en WordPress 7.1.4 con el plugin propio `cadus-portal`. El cliente pidió que la Ejecutiva (cuenta única `cadus`) y las delegaciones (una cuenta por delegación) puedan gestionar contenidos **sin entrar en el panel de administración de WordPress**, y que el portal tenga un inicio de sesión visible. Se ha añadido `cms-wordpress/wp-content/plugins/cadus-portal/includes/gestion.php`: páginas `/acceso/` y `/gestion/`, elemento «Acceder» / «Gestión» / «Salir» en el menú, formularios (nueva noticia, nuevo evento con The Events Calendar, nueva acta o normativa con PDF, datos de cada delegación y alta de delegaciones) procesados por `admin-post.php`. Las pruebas están en `scripts/pruebas/gestion.php` (84 correctas). Los permisos son los de WordPress (roles de `includes/roles.php`).

## Qué revisar
1. **Seguridad** de `includes/gestion.php`: nonces, comprobación de permisos en el servidor (¿se puede saltar con otra tarea o con otro `ficha`?), saneado y escape de entradas y salidas, subida del PDF (extensión, tipo real, tamaño, ruta, `is_uploaded_file`), redirección tras el inicio de sesión (`redirect_to`, `wp_login_failed`: ¿redirección abierta o enumeración de usuarios?), mensajes guardados en transients (¿se pueden manipular?), XSS en el mensaje que contiene una URL, inyección en el HTML generado. ¿Algún permiso queda ampliado respecto al panel?
2. **Privacidad (RN-03)**: ¿la página de gestión o los mensajes pueden mostrar datos de tickets o mediaciones? ¿Se cachean o indexan las páginas `/acceso/` y `/gestion/`?
3. **Corrección funcional**: validaciones de fecha y hora, evento sin categoría, evento que debe aparecer en el calendario (The Events Calendar 6 sincroniza sus tablas personalizadas al terminar la petición), actas pendientes de revisión frente a publicadas (RN-01), una cuenta por delegación (RN-04, `includes/relevo.php`), ficha de delegación editada por quien no es su autor.
4. **Accesibilidad (HU-15, DUA, personas ciegas y daltónicas)**: etiquetas, mensajes con `role`, foco, contraste (colores en `cadus_gestion_estilos`), tamaño de los objetivos táctiles, orden de encabezados, uso de color como única señal.
5. **Pruebas**: `scripts/pruebas/gestion.php`: ¿qué casos faltan (por ejemplo, el procesado de los formularios de `cadus_gestion_procesar`, nonce incorrecto, tarea inválida, fichero subido que no es una subida real)?
6. **Documentación y trazabilidad**: HU-24 en `docs/scrum/backlog/product-backlog.md`, `docs/scrum/sprints/sprint-03.md` (cambio de alcance 36 → 44 SP), UI-09 y UI-10 en `scripts/remus/cadus_data.json` y `docs/requisitos/rem-remus/REM-CADUS.md`, README del plugin.

No toques `cms-wordpress/.htaccess` ni los `.sql`.
