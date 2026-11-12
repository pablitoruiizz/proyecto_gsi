# HU-17b · Revisión de saneado, nonces y escape de salida (12/11/2026)

Revisión del plugin propio `cadus-portal` (`cms-wordpress/wp-content/plugins/cadus-portal`) hecha por Pablo con Claude y con dos revisiones cruzadas de Codex (`docs/scrum/codex_revision_gestion_portal.md` y `codex_revision_delegaciones_pie.md`). Pruebas automáticas de lo revisado en `scripts/pruebas/` (gestión: 93 correctas, 0 fallos; privacidad RN-03 y buzón de Marcos en sus propios scripts).

## Entradas de usuario del plugin

| Archivo | Entrada | Nonce | Permiso | Saneado / validación | Salida |
|---|---|---|---|---|---|
| `gestion.php` | formularios del panel (noticia, evento, acta, delegación) por `admin-post.php` | uno por tarea (`cadus_gestion_<tarea>`) | capacidades de WordPress repetidas en el servidor en cada función | texto, términos por id, fechas, correo, enlaces `https`, Instagram solo `instagram.com`, PDF (extensión, tipo real con `finfo`, tamaño, `is_uploaded_file`) | `esc_html`, `esc_attr`, `esc_url`, `esc_textarea` |
| `buzon.php` | formulario del buzón (Fluent Forms), seguimiento de ticket, respuesta de la Ejecutiva | `cadus_seguimiento`, `cadus_ticket_guardar_<id>` | `edit_post` | `cadus_buzon_input` (cadena, `wp_unslash`, `sanitize_text_field`), límite de intentos y campo trampa | escapado al pintar |
| `mediacion.php` | solicitud y estado de la mediación | `cadus_mediacion_guardar_<id>` | `edit_post` | igual que el buzón | escapado al pintar |
| `votaciones.php` | metadatos de la votación | `cadus_votacion_guardar` | `edit_post` | `sanitize_text_field`, `absint`, `esc_url_raw`, fechas por expresión regular | escapado al pintar |
| `relevo.php` | relevo de la cuenta de una delegación | `check_admin_referer('cadus_relevo')` | `cadus_relevo_puede` (delegado de su cuenta o Ejecutiva) | contraseña sin sanear (solo `wp_unslash`) y con longitud mínima | mensaje por transient del propio usuario |
| `setup.php`, `contenidos.php` | filtros GET del listado de noticias y de actas (`q`, `cat`, `anio`, `pag`, `tipo`) | no aplica (lectura) | no aplica | `sanitize_text_field`, `absint`, `sanitize_title` | escapado al pintar |
| `delegaciones.php`, directorio | buscador del directorio | no aplica | no aplica | se filtra en el navegador con `textContent`; `data-buscar` escapado con `esc_attr` | sin HTML insertado |
| `privacidad.php` | filtros REST/AJAX de RN-03 | no aplica | corta las rutas de tickets y mediaciones | `absint` | respuesta 404 |

## Comprobaciones generales
- **SQL:** las 13 consultas directas con `$wpdb` usan `prepare()`; el resto va por `WP_Query` o las API de WordPress.
- **Salida:** no hay `echo` de variables sin escapar (la única, `escritorio.php:180`, se escapa al montar el HTML y lo dice en el comentario).
- **Subida de archivos:** solo existe en el panel de gestión (PDF de actas) y pasa por `media_handle_sideload`; se rechaza si el servidor no puede comprobar el tipo real.
- **Datos privados (RN-03):** tickets y mediaciones no salen por REST, búsqueda, feeds ni mediateca; tienen prueba automática. `/acceso/` y `/gestion/` llevan `noindex` y cabeceras sin caché.

## Hallazgos y correcciones de hoy
| Gravedad | Hallazgo | Estado |
|---|---|---|
| Alta | Un delegado podía cambiar título, centro o estado de su ficha por la API REST `/wp/v2/cadus_delegacion` sin pasar por el panel. | **Corregido** (`wp_insert_post_data`, `rest_pre_insert_cadus_delegacion` y capacidad `assign_terms`); prueba HTTP real. |
| Media | Crear actas o delegaciones no comprobaba `upload_files`, `publish_*` ni `edit_others_*`. | **Corregido.** |
| Media | Sin `finfo` el PDF se daba por válido. | **Corregido:** se rechaza. |
| Media | Un error al reasignar la cuenta de una ficha dejaba datos guardados a medias. | **Corregido:** se valida todo antes de escribir. |
| Media | Los avisos de la cuenta única `cadus` se podían leer desde otra sesión. | **Corregido:** el aviso va por usuario y sesión. |
| Media | La carga de delegaciones podía reponer lo que alguien había vaciado y tratar un error de inserción como el id 1. | **Corregido.** |
| Media | El campo Instagram admitía cualquier dominio. | **Corregido:** solo `https://` y `instagram.com`. |
| Baja | Ficha editada desde el portal no avisaba a WP Fastest Cache. | **Corregido.** |

## Pendiente
1. **Escaneo de Wordfence** (cuenta de administración): ejecutar «Scan» desde Wordfence ▸ Scan, anotar el resultado y las alertas. No se puede hacer sin iniciar sesión.
2. **Cambiar la contraseña de `root` de MySQL** del equipo local (aparece en listas filtradas) y la de la cuenta `cadus` antes de publicar.
3. **Plugins de terceros** (Fluent Forms, The Events Calendar, ACF, Wordfence, WP Fastest Cache…): actualizados hoy; repetir el escaneo tras cada actualización.
4. Pruebas de gestión que aún no existen: ausencia de `finfo`, tamaño límite del PDF e invalidación real de la caché pública.
