# Pruebas de HU-19c · Panel de administración con cada rol

**Requisitos:** RF-14, RF-15 · RN-01, RN-03, RN-04 · HU-19a (menús por rol) y HU-19b (panel de inicio)
**Código probado:** `cms-wordpress/wp-content/plugins/cadus-portal/includes/admin.php` y `roles.php`
**Quién prueba:** Álvaro Martínez Ocaña · **Fecha:** 24/10/2026 · **Versión probada:** rama `main` tras `git pull` del 24/10/2026, WordPress 7.1 local (XAMPP, base `bd_cadus`), plugin CADUS Portal 1.0.0

## Entorno y usuarios de prueba

| Usuario | Rol en WordPress |
|---|---|
| `test-estudiante` | Estudiante US |
| `test-delegado` | Delegado de centro |
| `test_ejecutivo` | Ejecutivo del CADUS (rol `cadus_ejecutiva`) |
| `root` | Administrador (control) |

Cada rol se probó en una sesión distinta del navegador. Los usuarios de prueba se borran al terminar para que no queden en el volcado de la base de datos.

## Revisión del código (`roles.php`)

| Rol | Capacidades concedidas | Consecuencia |
|---|---|---|
| Estudiante US | Solo `read`. | Sin acceso a listados ni edición. |
| Delegado de centro | `read`, `upload_files`, `edit_cadus_delegacions`, `edit_published_cadus_delegacions`. Sin `edit_others_`, `create_` ni `publish_`. | Edita solo las delegaciones de las que es autor (RN-04). Sin permisos sobre actas, tickets ni mediaciones (RN-01, RN-03). |
| Ejecutivo del CADUS | Entradas, páginas, comentarios y todas las capacidades de actas, delegaciones, tickets y mediaciones, incluida `edit_others_cadus_delegacions`. | Aprueba actas y atiende buzón y mediaciones (RN-01, RN-03). |

## Casos y resultados

### Estudiante (`test-estudiante`)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| E1 | Iniciar sesión en `wp-login.php`. | Redirige a la portada, no al escritorio. | OK. Entra en la portada con la barra «Hola, test-estudiante». |
| E2 | Revisar la barra superior de WordPress. | Sin «Nuevo» ni Escritorio. | OK. |
| E3 | Abrir `/wp-admin/profile.php`. | Puede ver y editar su perfil. | OK. |
| E4 | Abrir por URL directa `edit.php`, `edit.php?post_type=cadus_acta`, `cadus_delegacion`, `cadus_ticket` y `cadus_mediacion`. | Sin permisos en todas. | OK. «Lo siento, no tienes permisos para acceder a esta página» (captura C). |
| E5 | Abrir `plugins.php`, `users.php`, `options-general.php` y `edit-comments.php`. | Sin permisos. | OK. |

### Delegado (`test-delegado`)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| D1 | Iniciar sesión en `wp-login.php`. | Redirige a la lista de Delegaciones. | OK. |
| D2 | Revisar el menú lateral. | Solo Escritorio, Medios y Delegaciones (más Perfil). | OK. Menú: Escritorio, Medios, Delegaciones y Perfil (captura A). |
| D3 | Editar y guardar la delegación de la que es **autor**. | Se guarda y se ve en la ficha pública (RN-04). | **Pendiente.** En la lista del Delegado las seis delegaciones tienen como autor a `root`, así que no se probó con una delegación propia. |
| D4 | Abrir por URL directa la edición de la delegación **de otro autor**. | Sin permiso (RN-04). | OK. |
| D5 | Intentar crear o publicar una delegación nueva. | No puede. | **A confirmar.** La interfaz muestra «Añadir delegación de centro» en el menú y en la lista; falta comprobar si el guardado falla. |
| D6 | Abrir por URL directa `edit.php?post_type=cadus_acta`, `cadus_ticket`, `cadus_mediacion` y `edit-comments.php`. | Sin permisos (RN-01, RN-03). | OK. |
| D7 | Abrir `plugins.php`, `users.php` y `options-general.php`. | Sin permisos. | OK. |
| D8 | Revisar la barra superior, apartado «Nuevo». | Solo lo permitido al rol. | OK. |

### Ejecutivo (`test_ejecutivo`)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| X1 | Iniciar sesión en `wp-login.php`. | Entra en el Escritorio (panel de HU-19b). | OK. Escritorio con «Accesos rápidos del CADUS» (captura B). |
| X2 | Revisar el menú lateral. | Entradas, Páginas, Actas, Delegaciones, Tickets, Mediaciones, Votaciones. Sin Plugins, Usuarios, Apariencia, Ajustes ni Comentarios. | OK (captura B). |
| X3 | Aprobar y publicar un acta pendiente de revisión. | Se publica (RN-01). | OK. |
| X4 | Abrir un ticket, cambiar el estado y responder. | Se guarda (RN-03). | OK. |
| X5 | Abrir una mediación y cambiar su estado. | Se guarda al recargar (RN-03). | OK. |
| X6 | Abrir por URL directa `plugins.php`, `users.php`, `options-general.php` y `edit-comments.php`. | Sin permisos. | OK. |
| X7 | Editar la delegación de otro autor. | A decidir: RN-04 solo lo permite a su delegado o a un administrador. | **Hallazgo por código:** la Ejecutiva tiene `edit_others_cadus_delegacions`, así que puede editarla. Pendiente de decisión del Product Owner. |

### Anónimo y administrador

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| A1 | Sin sesión, abrir `/wp-admin/`. | Redirige al acceso. | OK. |
| A2 | Sin sesión, pedir `/wp-json/wp/v2/cadus_ticket` y `cadus_mediacion`. | 404. | OK. |
| A3 | Con `root`, revisar el menú. | Ve todos los menús. | OK (captura E). |

## Fallos y puntos abiertos

| # | Caso | Qué ocurre | Corrección / issue |
|---|---|---|---|
| 1 | X7 | La Ejecutiva puede editar delegaciones de otros autores; contradice RN-04. | Decidir con el PO: quitar `edit_others_cadus_delegacions` o ampliar RN-04. |
| 2 | D5 | Se muestra «Añadir delegación de centro» al Delegado. | Comprobar si el guardado falla; si no, restringir `create_cadus_delegacions`. |
| 3 | D3 | No probada con una delegación propia. | Asignar autor `test-delegado` y repetir. |
| 4 | Roles | El rol de la Ejecutiva se ve como «Ejecutivo del CADUS» en la base de datos, aunque `roles.php` lo define como «Ejecutiva del CADUS»: `cadus_asegurar_rol` no renombra roles ya creados. | Opcional: actualizar el nombre visible. |

## Comprobaciones finales

- Usuarios de prueba borrados al terminar.
- Sin avisos de PHP revisados en `debug.log`: no comprobado.

## Capturas (carpeta `tests/capturas/`)

- **A.** Menú lateral del Delegado (lista de Delegaciones). RF-14, RN-04, HU-19c.
- **B.** Escritorio y menú de la Ejecutiva. RF-14, HU-19b, HU-19c.
- **C.** «Sin permisos» al abrir `edit.php?post_type=cadus_ticket` con el Estudiante. RF-14, RN-03, HU-19c.
- **E.** Pantalla de Usuarios con los roles del CADUS. RF-14, HU-19c.

No se incluye captura D (el Delegado editando su propia delegación): D3 sigue pendiente.
