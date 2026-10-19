# HU-09b / RN-03 — auditoría y correcciones

Fecha: 19/10/2026. WordPress 7.1, PHP HTTP 8.3.28, formulario Fluent Forms 3. Sitio: `http://localhost/proyecto_gsi/cms-wordpress/`. Sin navegador, instalación de plugins, cambios de ajustes, commit ni push.

## Hallazgos priorizados

| Prioridad | Evidencia observada | Corrección / resultado |
|---|---|---|
| Bloqueante de aceptación RN-03 | Un adjunto sintético cuyo padre era un ticket devolvía su título en `GET /wp-json/wp/v2/media/61` con sesión administradora: HTTP 200. La historia prohíbe exponer estos datos por API incluso a usuarios autorizados. Anónimo recibió 401; no se observó fuga anónima. | Se bloquea el endpoint individual y se excluyen tickets/hijos de consultas públicas/REST. Reprueba con ID 64: 404 para administrador, ambas Ejecutivas, delegado, estudiante y anónimo. `includes/privacidad.php:31`, `:103`. |
| Importante | El código original enviaba los campos completos al almacenamiento de FF; el servicio instalado escribe tanto `fluentform_submissions.response` como `fluentform_entry_details`. La instalación tenía cero entradas del buzón: no se identificaron reclamaciones históricas afectadas. | Campos solo en memoria; INSERT vacío sin datos del dispositivo/usuario; purga por ID de entrada en las tres tablas. Prueba del servicio real, observando INSERT/UPDATE, sin texto/correo sensible y cero filas residuales. `privacidad.php:114`, `:129`, `:147`; `buzon.php:314`. |
| Importante | `curl -I` del seguimiento llegó a devolver 200 sin `Cache-Control`, con `Last-Modified`; existía su `cache/all/.../seguimiento-de-ticket/index.html`. El código de WP Fastest Cache respeta `DONOTCACHEPAGE` solo en casos específicos con Wordfence/Divi. No se encontró un resultado privado cacheado; sí el formulario. | Exclusión explícita y filtro de escritura de caché; cabeceras no-store. Retirado solo ese HTML antiguo. GET/POST/GET correctos y el fichero no reaparece. `buzon.php:558`, `privacidad.php:167`. |
| Importante | Códigos originales derivados exclusivamente del ID; comparación de correo dentro de SQL, no en tiempo constante. | Se añaden 128 bits aleatorios; se aceptan códigos anteriores. Comparación de hashes fijos mediante `hash_equals`, respuesta genérica y límite existente 10/15 min probado hasta el undécimo intento. `buzon.php:344`, `:583`. |
| Importante | Listado original con asunto y correo; tras retirar columnas, WordPress 7.1 todavía insertaba el asunto en el `aria-label` de la columna primaria. | Código/estado/fecha, copia de presentación sin texto sensible y sin edición rápida/masiva. Reprueba HTTP de las tres cuentas autorizadas sin asunto/correo/descripción en el HTML. `buzon.php:503`, `privacidad.php:71`, `:78`, `:86`. |
| Importante, prevención | No había notificaciones FF configuradas ni `wp_mail` en el buzón, pero añadir un feed permitiría usar plantillas sensibles. | Feeds del buzón anulados por código. Prueba de feed configurado en memoria queda vacío; otros formularios conservan sus feeds; contador de `wp_mail` = 0. No se añadió aviso nuevo. `privacidad.php:142`. |
| Menor | `?post_type=cadus_ticket` y `?cadus_ticket=ID` devolvían portada 200, sin datos del ticket. | Respuesta 404 también para esos selectores y búsqueda manipulada. `privacidad.php:48`. |

Las capacidades actuales de `roles.php` ya eran correctas. Se añade una lista cerrada en `privacidad.php:13` para que una concesión accidental a otro rol no abra tickets. No se modificaron roles ni menús. Un miembro distinto de Ejecutiva sí tiene acceso al panel de todos los tickets; en el sitio público también recibe 404.

## Cobertura de los siete vectores

1. **URL:** `?p`, `?post_type=...&p`, `?page_id`, preview, attachment, feed de ticket, trackback (`tb=1`) y selector de tipo: 404, sin marcadores sensibles, para seis identidades (anónimo, administrador, dos Ejecutivas, delegado, estudiante). El tipo usa permalink sin rewrite, equivalente a la URL por tipo/ID probada. No se subió ningún fichero binario.
2. **REST:** tipos, búsqueda genérica y subtipo manipulado, posts, ruta de tickets inexistente, medios listados/individuales y Fluent Forms (`submissions`, `report/form-stats`, `global-search`). Sin tickets ni datos sensibles. FF: 401 anónimo, 403 roles CADUS, 200 administrador con cero entradas de prueba. `/wp/v2/users`: 401 anónimo; solo observado, no modificado.
3. **Descubrimiento:** búsquedas normales/manipuladas, feeds, autor, fecha, sitemap Yoast 200 sin tickets, sitemap específico de tickets 404 y nativo 404 (Yoast activo). El buscador de la portada solo genera una búsqueda nativa y ahora su manipulación queda bloqueada desde privacidad sin editar `inicio.php`. Los widgets recientes usan `WP_Query` y reciben la exclusión; por código, los widgets del Escritorio consultan `post`/`page`. Índices Yoast de tickets tras limpiar: 0.
4. **Avisos/logs:** cero feeds configurados y cero correos en prueba; no existe aviso propio a Ejecutiva. Se bloquean futuras notificaciones/integraciones del buzón. Búsqueda de marcadores de prueba en `apache/logs/error.log`: cero coincidencias. El `error_log` indicado por PHP CLI y `wp-content/debug.log` no existían; `WP_DEBUG`/`WP_DEBUG_LOG` estaban desactivados. No se auditaron logs externos/rotados, backups ni fallos forzados de BD.
5. **Almacenamiento:** envío a través del servicio real de Fluent Forms, con validación; ticket conserva el texto, FF no lo inserta y queda sin entrada/detalles/metadatos. No se soportan revisiones, `wp_revisions_to_keep` devuelve 0. Metadatos privados, sin esquema REST público. Seguimiento sin código+correo devuelve error genérico y nunca imprime el correo. No hubo datos históricos que migrar.
6. **Panel:** listado/editor 403 delegado y estudiante, 200 ambas Ejecutivas y administrador; cuenta distinta de Ejecutiva puede gestionar el mismo ticket. Lista minimizada incluso en HTML/ARIA; `can_export=false` y código del exportador WXR confirma exclusión también en `content=all`. Sin edición rápida o masiva; borrado masivo mantiene los permisos WordPress. El Escritorio autenticado no incluyó los marcadores.
7. **Seguimiento:** prueba del código nuevo y del formato antiguo; correo en mayúsculas aceptado; correo incorrecto y código inexistente producen exactamente el mismo resultado; undécimo intento rechazado. Hashes de longitud fija (no una garantía de tiempo constante del SQL completo). POST correcto y GET posterior no filtraron texto original ni correo, y mantuvieron `no-store`. La caché HTML no reapareció.

## Evidencia reproducible

Ejecutar desde la raíz. PHP = `C:\Users\ruizv\OneDrive\Escritorio\UNI\GSI\apps proyecto\php\php.exe`.

| Comando | Resultado conservado |
|---|---|
| `python scripts/pruebas/privacidad_tickets.py` (antes de corregir) | 35 correctas, 4 falsos positivos por reflejo del término buscado. Revisión en `RN03_REVISION_PRUEBAS.md`; no se alteró la batería de Claude. |
| `python scripts/pruebas/rn03_http.py > scripts/pruebas/rn03_resultados.txt` | 248 correctas, 3 fallos restantes: asunto en ARIA del listado de las tres cuentas autorizadas. El informe conserva estos fallos intermedios, no los oculta. Se corrigió después con la copia de presentación. |
| `python scripts/pruebas/rn03_http.py --panel > scripts/pruebas/rn03_reprueba_panel.txt` | **65 correctas, 0 fallos**; vuelve a ejecutar el servicio FF, controles internos, panel de todos los roles, seguimiento, caché y limpieza. Resuelve los tres fallos anteriores sin repetir innecesariamente toda la matriz pública. |
| `& '...\php.exe' scripts/pruebas/rn03_inspeccion.php` | `rn03_inspeccion_final.json`: **tickets=0, ff_entries=0, ff_details_total=0, ff_meta_total=0, usuarios_prueba=0, yoast_tickets=0, ff_notifications=0**. |
| `& '...\php.exe' -l cms-wordpress/wp-content/plugins/cadus-portal/includes/buzon.php` | `No syntax errors detected`. |
| `& '...\php.exe' -l cms-wordpress/wp-content/plugins/cadus-portal/includes/privacidad.php` | `No syntax errors detected`. También pasan ambos helpers PHP nuevos. |
| `curl.exe -I http://localhost/proyecto_gsi/cms-wordpress/atencion-al-estudiante/seguimiento-de-ticket/` (dos veces) | 200 y `Cache-Control: no-store, no-cache, must-revalidate, private, max-age=0`, `Referrer-Policy: no-referrer`, `X-Robots-Tag: noindex, nofollow, noarchive`. |
| `rg -n --count-matches -e RN03-CODEX-SECRETO -e RN03-CODEX-ASUNTO -e prueba@alum.us.es -e TEXTO-SECRETO-RN03 '...\apache\logs\error.log'` | Sin coincidencias; salida 1 de rg significa no encontrado. |
| `git diff --check -- cms-wordpress/wp-content/plugins/cadus-portal/includes/buzon.php cms-wordpress/wp-content/plugins/cadus-portal/README.md` | Sin errores de espacios. Solo aviso habitual LF/CRLF. |

Los `.txt` y `.json` de evidencia se normalizaron a UTF-8 tras la redirección de PowerShell. No contienen cookies, tokens de sesión ni contraseñas. Las sesiones de prueba se destruyeron y las cuentas auxiliares se eliminaron. Solo se empleó el correo de prueba o correo vacío en cuentas auxiliares.

## Alcance y decisiones pendientes

- Archivos de producción: **solo `includes/buzon.php`, nuevo `includes/privacidad.php` y sección añadida al README (línea 95)**. Se añadieron helpers, pruebas y evidencia en `scripts/pruebas/` para hacer la auditoría reproducible. Se retiró una copia generada de caché del seguimiento; no se editaron ajustes, `.htaccess`, archivos reservados ni otros módulos. Los cambios preexistentes del equipo se conservaron.
- No se añadió correo: la opción más privada es mantenerlo desactivado. Si el equipo requiere aviso, definir destinatarios y limitarlo a código + URL autenticada del panel.
- Compatibilidad con códigos antiguos preservada. Decidir su eventual sustitución; no se puede añadir entropía a códigos ya entregados sin comunicarlos de nuevo.
- Código + correo identifica al remitente solo por conocimiento de ambos valores; no demuestra que controle el buzón. Valorar verificación del correo si se exige autenticación más fuerte.
- Definir retención y borrado de tickets/backups. No se inventó un plazo ni se borraron datos reales.
- El formulario no admite archivos. El bloqueo de páginas/REST de adjuntos **no protege ficheros estáticos en uploads**: si se incorporan, necesitan un almacén privado y descarga autorizada. No se verificó protección de binarios porque no existen en este flujo.
- Queda pendiente la revisión del código por Claude; la revisión de sus pruebas sí está entregada. No se afirma haber recibido una aprobación externa.
