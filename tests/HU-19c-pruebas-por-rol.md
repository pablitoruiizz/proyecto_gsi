# Pruebas de HU-19c · Panel de administración con cada rol

**Requisitos:** RF-14, RF-15 · RN-01, RN-03, RN-04 · HU-19a (menús por rol) y HU-19b (panel de inicio)
**Código probado:** `cms-wordpress/wp-content/plugins/cadus-portal/includes/admin.php` y `roles.php`
**Quién prueba:** Álvaro Martínez Ocaña · **Fecha:** `[POR COMPLETAR]` · **Versión probada:** `main` en el commit `[POR COMPLETAR]`

Anotar el resultado **real** en la última columna (OK, o describir lo que ha pasado) y abrir una issue por cada fallo.

## Estado de la verificación

**Entorno:** WordPress local (XAMPP, base `bd_cadus`), plugin CADUS Portal 1.0.0 activo, con los usuarios `test-ejecutivo`, `test-delegado` y `test-estudiante` creados el 24/10/2026.

| Tipo de comprobación | Estado |
|---|---|
| Revisión del código (`roles.php`, `admin.php`): qué permisos concede cada rol | **Hecha** (ver tabla siguiente) |
| Ejecución de los casos E1–E5, D1–D8, X1–X7 y A1–A3 en el navegador | **Pendiente.** La columna «Resultado» de las tablas de abajo sigue vacía: no se ha rellenado nada sin ejecutar. |

### Resultado de la revisión del código (no sustituye a la ejecución)

| Rol | Capacidades concedidas en `roles.php` | Consecuencia |
|---|---|---|
| Estudiante US | Solo `read`. | Sin acceso a listados ni edición; coherente con E4 y E5. |
| Delegado de centro | `read`, `upload_files`, `edit_cadus_delegacions`, `edit_published_cadus_delegacions`. Sin `edit_others_`, `create_` ni `publish_`. | Edita solo las delegaciones de las que es autor (RN-04) y no puede crear ni publicar nuevas (D5). Sin permisos sobre actas, tickets ni mediaciones (RN-01, RN-03). |
| Ejecutiva del CADUS | Entradas, páginas, comentarios y todas las capacidades de actas, delegaciones, tickets y mediaciones, incluida `edit_others_cadus_delegacions`. | Aprueba actas y atiende buzón y mediaciones (RN-01, RN-03). |

**Hallazgo (caso X7):** la Ejecutiva tiene `edit_others_cadus_delegacions`, así que puede editar delegaciones de otros autores, algo que RN-04 reserva a su delegado o a un administrador. Hay que decidir con el Product Owner si se quita esa capacidad o se amplía RN-04.

## Puesta en marcha

1. Actualizar el repositorio (`git checkout main` y `git pull origin main`) y arrancar Apache y MySQL en XAMPP.
2. Entrar en el panel con un administrador y crear **tres usuarios de prueba** en *Usuarios › Añadir nuevo*, uno por rol, con contraseñas que no se reutilicen en ningún otro sitio:
   - `test-ejecutivo` con el rol **Ejecutiva del CADUS**
   - `test-delegado` con el rol **Delegado de centro**
   - `test-estudiante` con el rol **Estudiante US**
3. Para probar RN-04, crear (o usar) dos delegaciones: poner como **autor** de la primera a `test-delegado` (campo *Autor* de la ficha) y dejar la segunda con otro autor (por ejemplo, un administrador).
4. Tener a mano un acta en estado *Pendiente de revisión*, un ticket del buzón y una solicitud de mediación de prueba.
5. Usar una **ventana de incógnito distinta por rol** (o cerrar sesión entre pruebas) para no mezclar sesiones.

Al terminar, **borrar los tres usuarios de prueba y los datos de prueba**, para que no queden en el volcado final de la base de datos.

## Casos

### Estudiante (`test-estudiante`)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| E1 | Iniciar sesión en `wp-login.php`. | Redirige a la portada, no al escritorio. | |
| E2 | Revisar la barra superior de WordPress. | Solo cuenta, salir y ver el sitio; sin «Nuevo» ni Escritorio. | |
| E3 | Abrir `/wp-admin/profile.php`. | Puede ver y editar su perfil. El menú solo muestra «Perfil». | |
| E4 | Abrir por URL directa: `wp-admin/edit.php`, `edit.php?post_type=cadus_acta`, `edit.php?post_type=cadus_delegacion`, `edit.php?post_type=cadus_ticket`, `edit.php?post_type=cadus_mediacion`. | En todas: sin permisos. | |
| E5 | Abrir `wp-admin/plugins.php`, `users.php`, `options-general.php` y `edit-comments.php`. | Sin permisos; en comentarios, «No tienes permisos para gestionar comentarios». | |

### Delegado (`test-delegado`)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| D1 | Iniciar sesión en `wp-login.php`. | Redirige a la lista de Delegaciones (`edit.php?post_type=cadus_delegacion`). | |
| D2 | Revisar el menú lateral. | Solo Escritorio, Medios y Delegaciones (y lo que añadan los módulos de HU-10 y HU-19b). Sin Entradas, Páginas, Actas, Tickets, Mediaciones, Comentarios, Plugins, Usuarios, Apariencia ni Ajustes. | |
| D3 | Editar y guardar la delegación de la que es **autor**. | Se guarda; el cambio se ve en la ficha pública (RN-04). | |
| D4 | Abrir por URL directa la edición de la delegación **de otro autor** (`post.php?post=ID&action=edit`). | Sin permiso (RN-04). | |
| D5 | Intentar crear o publicar una delegación nueva. | No puede: no aparece «Añadir» o falla al guardar. | |
| D6 | Abrir por URL directa `edit.php?post_type=cadus_acta`, `cadus_ticket`, `cadus_mediacion` y `edit-comments.php`. | Sin permisos (RN-01, RN-03). | |
| D7 | Abrir `wp-admin/plugins.php`, `users.php` y `options-general.php`. | Sin permisos. | |
| D8 | Revisar la barra superior, apartado «Nuevo». | Solo Medios y Delegación (más lo que añadan los módulos). | |

### Ejecutivo (`test-ejecutivo`)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| X1 | Iniciar sesión en `wp-login.php`. | Entra en el Escritorio (panel de inicio de HU-19b). | |
| X2 | Revisar el menú lateral. | Escritorio, Medios, Entradas (con categorías y etiquetas), Páginas, Actas y normativas, Delegaciones, Tickets del buzón, Mediaciones, y los menús de calendario y votaciones. Sin Plugins, Usuarios, Apariencia, Ajustes, Herramientas, Comentarios, Fluent Forms ni Yoast. | |
| X3 | Aprobar y publicar un acta en estado *Pendiente de revisión*. | Se publica y aparece en la web (RN-01). | |
| X4 | Abrir un ticket del buzón, cambiar el estado y añadir una respuesta. | Se guarda y se ve en el seguimiento (RN-03). | |
| X5 | Abrir una solicitud de mediación y cambiar su estado. | Se guarda y se mantiene al recargar (RN-03). | |
| X6 | Abrir por URL directa `plugins.php`, `users.php`, `options-general.php` y `edit-comments.php`. | Sin permisos; en comentarios, «No tienes permisos para gestionar comentarios». | |
| X7 | Editar la delegación de otro autor. | **A decidir:** RN-04 dice que solo la edita su delegado o un administrador; el código actual (`roles.php`) da `edit_others_cadus_delegacions` a la Ejecutiva. Anotar qué ocurre y plantearlo al Product Owner. | |

### Anónimo y administrador

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| A1 | Sin sesión, abrir `/wp-admin/`. | Redirige a la pantalla de acceso. | |
| A2 | Sin sesión, pedir `/wp-json/wp/v2/cadus_ticket` y `/wp-json/wp/v2/cadus_mediacion`. | La ruta no existe (404). | |
| A3 | Con un administrador, revisar el menú (control). | Ve todos los menús, sin filtrar. | |

## Fallos encontrados y correcciones

| # | Caso | Qué ocurre | Corrección / issue |
|---|---|---|---|
| | | | |

## Comprobaciones finales

- Sin avisos de PHP en `wp-content/debug.log` (con `WP_DEBUG_LOG` activo) tras recorrer los tres roles.
- Usuarios y datos de prueba borrados.

## Capturas para la implementación (1920×1080, con pie y códigos RF-14 · RF-15 · RN-04 · HU-19c)

A. Menú lateral del Delegado. · B. Menú lateral del Ejecutivo. · C. «Sin permisos» al abrir por URL directa un tipo que no le corresponde a un rol. · D. El Delegado editando su propia delegación. · E. Pantalla de Usuarios con los roles del CADUS.
