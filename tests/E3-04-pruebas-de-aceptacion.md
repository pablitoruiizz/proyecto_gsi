# E3-04 · Pruebas de aceptación del CMS (Sprint 3)

**Historias:** HU-14 a HU-23 (menos HU-21, cancelada) · **Reglas:** RN-01, RN-03, RN-04 · **Requisitos:** RF-02, RF-04, RF-14, RNF-02, RNF-04, RNF-08
**22/11/2026: se repitieron H16-1 a H16-6 con clics reales y se ejecutaron T1, T2, H14-2 a H14-4, H15-1 y H15-3 (estas dos, parciales) en el WordPress de WampServer (Apache, PHP 8.3, MySQL 8.4, base `bd_cadus`, con Fluent Forms y The Events Calendar), con el navegador integrado; los datos de ese sitio difieren de los del 15/11 (4 noticias del 14 al 17/10, 2 documentos en actas). No se han probado dispositivos reales, lector de pantalla ni las cuentas por rol.** **Pruebas H16-1 a H16-6 ejecutadas el 15/11/2026 en el WordPress local (peticiones anónimas desde el navegador integrado, datos de ejemplo; no se usó el formulario con clics, no se probó el panel de la Ejecutiva).** **Quién prueba:** el guion es de Álvaro; las ejecuciones son parciales: el 15/11 por peticiones anónimas y el 22/11 por Claude con Pablo (H14-5 la hizo Pablo con su móvil; H16-7 y H17-3 las ejecutó Claude en nombre de Pablo). **No hay prueba cruzada completa.** · **Fecha:** 15/11/2026 y 22/11/2026 · **Versión probada:** `main` con los cambios locales del 22/11
**Estado del guion:** en ejecución. Los casos con la columna «Resultado» vacía **no se han ejecutado**; un caso que no se haya podido ejecutar se anota como «Pendiente» con el motivo.

## Cómo se usa este guion

1. Haz `git pull` de `main` y comprueba en la sección «Historias integradas» qué historias están ya en `main`; las que no lo estén se dejan como «No integrada» y no se ejecutan.
2. Cada rol se prueba en una sesión distinta del navegador (o en una ventana privada): anónimo, `test-estudiante`, `test-delegado` y `test_ejecutivo` (mismos usuarios que en HU-19c; se borran al terminar).
3. Anota el resultado real en cada fila: `OK`, `FALLO` (con el número de la tabla de fallos) o `Pendiente` (con el motivo).
4. Los dispositivos: ordenador (1920×1080), tablet (768×1024) y móvil (390×844), con el modo dispositivo del navegador salvo donde se pida un dispositivo real.

## Historias integradas

| Historia | Responsable | ¿En `main`? |
|---|---|---|
| HU-14a Menús y portada en móvil y tablet | Joaquín | Sí (14/11) |
| HU-14b Directorio, tablas y fichas en móvil y tablet | Álvaro | No: en la rama `feature/hu-14b-directorio-movil`, sin PR a 14/11 |
| HU-14c Buzón, calendario y mediación en móvil y tablet | Pablo | Sí (14/11) |
| HU-15a/b/c Accesibilidad | Joaquín, Marcos, Miguel Ángel | Sí (14/11) |
| HU-16a Filtros por palabra clave y fecha (noticias y actas) | Álvaro | Sí (14/11) |
| HU-16b Búsqueda en tickets sin exponer datos | Marcos | Sí (14/11) |
| HU-17a/b Spam e inyección | Marcos, Pablo | Sí (14/11) |
| HU-20a/b Rendimiento | Miguel Ángel, Pablo | Sí (14/11) |
| HU-22 Relevo de la cuenta de la delegación | Miguel Ángel | Sí (14/11) |
| HU-23 Anonimización a los 2 años | Álvaro | Sí (14/11) |

## 1. Las tres operaciones en menos de un minuto (criterio del cliente)

Se cronometra con una persona que no conoce el portal, desde la portada y en el móvil (390×844). El tiempo cuenta desde que carga la portada hasta que ve el resultado.

| # | Operación | Resultado esperado | Tiempo | Resultado |
|---|---|---|---|---|
| T1 | Crear un ticket en el buzón con un correo `@alum.us.es`. | Aparece el código de seguimiento en menos de 60 s. | | Parcial (22/11, Claude con Pablo). Funcional: con el formulario real de Fluent Forms en WampServer (PHP 8.3), en ordenador, se rellenaron los 7 campos obligatorios y «Enviar al CADUS» devolvió en unos 5 s el código `CAD-2026-00479-…` con el texto «guarda este código» y el plazo de 4 días hábiles. **No cumple el criterio completo**: no se cronometró ni en móvil ni con una persona que no conozca el portal. Queda un ticket de prueba («Prueba E3-04 (borrar)») en la base local. |
| T2 | Consultar el calendario. | Se ve el mes con las asambleas y los cursos en menos de 60 s. | | Parcial (22/11). Funcional: el WordPress de WampServer sí tiene The Events Calendar y la vista Mes de noviembre 2026 muestra la asamblea del 12/11 y la jornada del 19/11 (eventos de ejemplo, ya pasados: la vista «Próximos» dice «No hay eventos programados»). **No cumple el criterio completo**: no se cronometró ni se probó con una persona externa ni en móvil. |
| T3 | Ver asambleas, eventos y noticias. | Se llega a las tres secciones en menos de 60 s. | | Parcial (22/11). Noticias, Actas y normativa y Calendario son accesibles desde el menú de la portada en un clic cada uno; las asambleas son los eventos del mismo calendario. No se cronometró con una persona externa. |

## 2. Por historia y por rol

### HU-14 · Móvil, tablet y ordenador (RNF-02)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| H14-1 | Portada y menú en móvil y tablet (anónimo). | Menú plegable, tarjetas en una columna, sin scroll horizontal. | Parcial (15/11, emulación a 390 y 768 px; en el móvil real de Pablo la portada se ve bien el 22/11, ver H14-5). La página no hace scroll horizontal; a 390 px el botón «Menú» abre el menú a pantalla completa. A 768 px 20 elementos de la portada se salen por la derecha pero quedan recortados (no hay scroll); no se identificaron cuáles. Las tarjetas en una columna no se comprobaron una a una. |
| H14-2 | Directorio de delegaciones en móvil y tablet. | Tarjetas legibles, buscador usable, sin textos cortados. | OK (22/11, navegador integrado a 390 px y 768 px). Sin scroll horizontal; 27 delegaciones (una columna a 390 px, dos a 768 px); el buscador filtra al escribir (`ETSII` deja 1 delegación). |
| H14-3 | Ficha de una delegación en móvil y tablet. | Datos y enlaces visibles, el botón «Volver al listado» funciona. | Parcial (22/11, 390 px). Ficha de la ETSII: correo, teléfono, Instagram y lista de miembros visibles, sin scroll horizontal; el enlace «Volver al listado» apunta a `/delegaciones/` (se comprobó su destino, no se pulsó). Falta la parte de tablet. |
| H14-4 | Tabla de actas y normativa en móvil. | Cada fila se muestra como tarjeta con sus etiquetas (Fecha, Documento, Tipo, PDF). | OK (22/11, 390 px). Cada fila de la tabla es una tarjeta con las etiquetas Fecha, Documento, Tipo y PDF, sin scroll horizontal; a 768 px vuelve la tabla con cabecera. |
| H14-5 | Buzón, calendario y mediación en un móvil y una tablet reales. | Se pueden completar y enviar sin perder funciones (lo prueba Pablo; se anota aquí). | OK en móvil (22/11, según Pablo, con su móvil real por Tailscale: ha probado todo, incluidos buzón, calendario, mediación y menú). La primera vez la portada salió sin estilos ni imágenes por la caché de WP Fastest Cache del WordPress local (servía páginas generadas por `localhost`), no por un fallo del portal; tras vaciar la caché se ve bien. Lo probó Pablo, que programó HU-14c: no es prueba cruzada. Una tablet real no se ha probado (solo emulación a 768 px). |

### HU-15 · Accesibilidad (WCAG 2.1 AA, DUA)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| H15-1 | Navegar solo con el teclado desde la portada hasta el buzón. | Foco visible siempre; el enlace «Saltar al contenido» funciona. | Parcial (22/11). En el buzón, el primer Tab muestra «Saltar al contenido» con foco visible; Intro lleva a `#main`; 7 Tab más llegan al campo Descripción con anillo de foco de 2,4 px. No se completó el envío solo con teclado ni se recorrió toda la portada. |
| H15-2 | Lighthouse de accesibilidad en portada, buzón y directorio. | Puntuación mínima acordada por el equipo (anotar valor). | |
| H15-3 | Revisar formularios con un lector de pantalla. | Cada campo tiene etiqueta; los errores se anuncian. | Parcial (22/11). Los 8 campos del buzón tienen etiqueta asociada, 7 son obligatorios y la página declara `lang=es`. No se ha probado con un lector de pantalla real (NVDA o Narrador): pendiente. |
| H15-4 | Simular daltonismo en el navegador. | Los estados no se distinguen solo por el color. | |

### HU-16 · Buscar y filtrar (RF-04)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| H16-1 | Noticias: buscar una palabra que esté solo en un comunicado. | Solo aparece ese comunicado. | OK (22/11, con clics en el formulario real). «becas» deja solo el comunicado sobre becas (de 4). |
| H16-2 | Noticias: filtrar con «Desde» y «Hasta». | Solo salen las noticias del rango, incluidos los dos días de los extremos. | OK (22/11, con clics). Desde 15/10 hasta 16/10 devuelve las noticias del 15 y del 16 (incluye los dos extremos). |
| H16-3 | Noticias: «Desde» posterior a «Hasta». | Se ordena el rango; no hay error. | OK (22/11, con clics). Desde 16/10 hasta 14/10 se ordena el rango y salen las 3 noticias del 14 al 16, sin error. |
| H16-4 | Actas: buscar una palabra del título y filtrar por fechas a la vez que por tipo. | Salen solo las actas que cumplen todo; el chip de tipo conserva los otros filtros. | OK (22/11, con clics). «pleno» + desde 01/10 deja el acta; el chip «Normativa» conserva palabra y fecha y muestra «No hay documentos publicados para este filtro». |
| H16-5 | Actas: rango sin ningún documento. | Mensaje «No hay documentos publicados para este filtro». | OK (22/11, con clics). Un rango de 2027 con tipo Acta muestra «No hay documentos publicados para este filtro». |
| H16-6 | Actas: «Quitar filtros». | Vuelve el listado completo (manteniendo el tipo si estaba elegido). | OK (22/11, con clics). «Quitar filtros» vuelve al listado y conserva el tipo (`?tipo=acta`). |
| H16-7 | Ejecutiva: buscar en el panel de Tickets. | Encuentra por referencia, **sin** mostrar datos del estudiante (RN-03). Pendiente de HU-16b. | OK en tickets (22/11; ejecutada por Claude en nombre de Pablo y a su petición, con la cuenta `test-ejecutivo`: no es prueba cruzada). En Tickets, buscar `00479` o `CAD-2026` (referencia) y `E3-04` (asunto) encuentra el ticket; buscar el nombre (`Zacarias`, `Quintanilla`), el correo (`prueba.e304`), el centro (`Informatica`) o una palabra de la descripción (`aceptación`) devuelve «No se han encontrado tickets». El listado solo enseña referencia, tipo, estado y fecha. Mediaciones: la base local no tiene solicitudes, así que no se probó ahí. |

### HU-17 · Spam e inyección (RNF-08)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| H17-1 | Enviar el buzón y la mediación con el campo trampa (honeypot) relleno. | No se crea ningún ticket ni solicitud. | |
| H17-2 | Enviar más de 10 solicitudes seguidas. | Aviso de límite de envíos; las siguientes no se crean. | |
| H17-3 | Escribir `<script>alert(1)</script>` y `' OR 1=1 --` en la descripción. | Se guarda como texto; no se ejecuta; en el panel aparece escapado. | Parcial (22/11; ejecutada por Claude en nombre de Pablo y a su petición: no es prueba cruzada). `<script>` e `<img onerror>` en el asunto y la descripción: el envío devolvió 403 (dos intentos), lo bloquea Wordfence antes de llegar al portal, así que **no se guardó** y no se pudo comprobar el escapado propio del portal con ese texto. Con `<b>`, `<i>`, comillas, `x' OR 1=1 --` y `DROP TABLE x; --`: el envío devolvió 200, las etiquetas se eliminaron al guardar, la inyección SQL se guardó como texto (las tablas siguen intactas y hay 2 tickets) y el panel lo muestra como texto sin interpretar HTML. |

### HU-20 · Rendimiento

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| H20-1 | Lighthouse de rendimiento en la portada (móvil). | Mejora respecto a la medición anterior (anotar antes y después). | |
| H20-2 | Imágenes con carga diferida y tamaño ajustado. | Ninguna imagen supera el tamaño acordado (HU-20a): fotos de la galería de 720 px como máximo y en WebP, escudos en WebP a su tamaño, y una imagen subida de más de 1920 px se reduce a 1920 px (una de más de 8 MB se rechaza). | Parcial (15/11). En la portada, 6 imágenes, la mayor de 46 KB; todas con carga diferida salvo el logotipo. No se comprobó el resto de páginas ni el tamaño acordado. |

### HU-22 · Relevo de la cuenta de la delegación (RN-04, RF-14)

Modelo decidido con el CADUS el 09/11: **una cuenta por delegación**, con el correo institucional de la delegación. En el relevo no se crea otra cuenta: la misma pasa al equipo entrante con una contraseña nueva (**Delegaciones › Relevo de la cuenta**). Se prueba con dos navegadores (o uno en privado) para ver que la sesión del equipo anterior se cierra.

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| H22-1 | Delegado: en «Relevo de la cuenta», elegir «Contraseña nueva», marcar la confirmación y hacer el relevo. | Sale a la pantalla de acceso con el aviso «Relevo hecho» y entra con la contraseña nueva; la ficha sigue en la misma cuenta. | |
| H22-2 | Tras el relevo, el equipo anterior intenta seguir: con la sesión abierta en otro navegador y con la contraseña antigua. | La otra sesión queda cerrada y la contraseña antigua no sirve. | |
| H22-3 | Delegado: cambiar en el formulario (herramientas del navegador) el campo `cuenta` por el número de otra delegación y enviarlo. | No puede: «Solo puedes hacer el relevo de la cuenta de tu propia delegación» (403). | |
| H22-4 | Ejecutiva: hacer el relevo de otra delegación. | Puede; la lista solo ofrece cuentas de delegación (ninguna de administrador) y la tabla muestra el último relevo. | |
| H22-5 | Comprobar que cada delegación queda con una sola cuenta activa: en la tabla de la Ejecutiva, y con `php scripts/roles/aplicar_usuarios.php` probando una segunda cuenta para la misma delegación. | Una sola cuenta por ficha; el script rechaza la segunda («para el relevo cambia su contraseña, no crees otra»). | |

### HU-23 · Anonimización a los 2 años (RN-03)

Se prueba con `scripts/pruebas/hu23_prueba_retencion.php` (ver `tests/HU-23-retencion.md` cuando esté escrito).

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| H23-1 | Ejecutar el script de prueba. | Los 9 casos y las dos comprobaciones finales salen `OK`. | |
| H23-2 | Con la Ejecutiva, abrir un elemento anonimizado en el panel. | Se ven referencia, tipo y estado; no hay correo, texto ni respuestas. | |
| H23-3 | Un ticket abierto muy antiguo. | No se toca. | |
| H23-4 | Comprobar la tarea programada en el servidor del equipo. | El evento `cadus_retencion_diaria` existe y se ejecuta una vez al día. | |
| H23-5 | Borrar los datos de ejemplo (`limpiar`). | No quedan elementos `PRUEBA-HU23-*`. | |

## 3. Privacidad en todos los roles (RN-03)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| P1 | Anónimo: abrir `/wp-json/wp/v2/cadus_ticket` y `cadus_mediacion`. | 404. | OK (15/11). `/wp-json/wp/v2/cadus_ticket`, `cadus_mediacion` y `cadus_ticket/1` devuelven 404 y `/wp-json/wp/v2/types` no lista esos tipos. |
| P2 | Anónimo: buscar la referencia de un ticket y de una mediación en el buscador. | Sin resultados. | Parcial (15/11). La búsqueda `?s=00061` (parte de la referencia de una mediación, que tiene la forma `MED-2026-00061-<código largo>`) no devuelve ninguna entrada. No se comprobó con la referencia completa ni con un ticket, porque no hay tickets en el entorno local. |
| P3 | Estudiante y Delegado: abrir por URL directa `edit.php?post_type=cadus_ticket` y `cadus_mediacion`. | Sin permisos. | |
| P4 | Estudiante con sesión: enviar un ticket y una mediación. | Solo recibe la referencia; no los ve en ninguna parte. | |
| P5 | El aviso por correo de un ticket. | No incluye el contenido, solo código y enlace. | |
| P6 | Las nuevas búsquedas y filtros (HU-16) con un texto presente solo en un ticket. | No aparece nada del ticket. | |

## 4. Aprobación de la Ejecutiva (RN-01)

| # | Prueba | Resultado esperado | Resultado |
|---|---|---|---|
| A1 | Delegado: crear o editar una delegación y guardarla. | Queda pendiente de revisión hasta que la Ejecutiva la aprueba. | |
| A2 | Ejecutiva: aprobar un acta pendiente. | Se publica y aparece en el listado y en los filtros de HU-16a. | |
| A3 | Anónimo: abrir un acta pendiente por URL. | No se muestra. | OK (15/11). El acta «Acta pendiente de aprobación (ejemplo)» (ID 31) devuelve 404 para un visitante anónimo, tanto por `?post_type=cadus_acta&p=31` como por `?p=31`, y no aparece en el listado público. |

## Fallos y observaciones

| # | Caso | Qué ocurre | Corrección / issue |
|---|---|---|---|
| 1 | Panel de la Ejecutiva (`test-ejecutivo`), delegaciones (15/11) | Ve las 6 delegaciones, todas del autor `root`, con las acciones «Editar», «Papelera» y «Ver». Es coherente con la decisión X7 (puede editar fichas ajenas), pero también puede **mandar a la papelera** delegaciones ajenas, y X7 solo habla de editar. | Confirmar con Pablo si la Ejecutiva debe poder eliminar delegaciones. La edición no se pudo probar: la pantalla usa el editor de bloques, que no carga en el navegador integrado. |
| 2 | Panel de la Ejecutiva, votaciones (15/11) | La lista de Votaciones se abre, está vacía (0) y permite «Añadir convocatoria de votación». | Sin incidencia. Probar el alta desde Chrome o Edge. |
| 3 | Editor de bloques en el navegador integrado (15/11) | Las pantallas con editor de bloques (actas, delegaciones) no cargan: errores de JavaScript del propio editor (React no disponible). Las mediaciones usan el editor clásico y sí funcionan. | Es una limitación de la herramienta de prueba, no del plugin. Probar esas pantallas en Chrome o Edge. |

## Comprobaciones finales

- Usuarios de prueba y datos de ejemplo borrados al terminar.
- Sin avisos de PHP en `wp-content/debug.log`: _por comprobar_.

## Trazabilidad

| Requisito o regla | Casos que lo cubren |
|---|---|
| RNF-02 (móvil, tablet y ordenador) | T1–T3, H14-1 a H14-5 |
| RF-04 (buscar y filtrar) | H16-1 a H16-7 |
| RNF-08 (seguridad) | H17-1 a H17-3 |
| RN-01 (la Ejecutiva aprueba el contenido) | A1–A3 |
| RN-03 (privacidad de tickets y mediaciones) | H16-7, H23-1 a H23-5, P1–P6 |
| RN-04 (cada delegado, su delegación) | H22-1 a H22-5 |
