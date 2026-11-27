# Sprint 3 — Móvil, accesibilidad, seguridad, rendimiento y cierre del CMS

**Equipo:** 5 integrantes
**Cliente:** CADUS (Consejo de Alumnos de la Universidad de Sevilla). **Contacto con el cliente:** Miguel Ángel Camacho Martín, que forma parte del CADUS.
**Periodo:** 26/10/2026 – 15/11/2026 (un único sprint de tres semanas, como acordó el equipo con el profesor)
**Estado:** Cerrado el 15/11/2026 (con pendientes: ver «Resultado del Sprint 3»). Compromiso: 36 SP (HU-14, HU-15, HU-16, HU-17, HU-20, HU-22 y HU-23) más 8 SP de HU-24 añadidos el 12/11 (44 SP; ver «Cambio de alcance»)

## Objetivo del Sprint

Dejar el portal terminado e implementado para el 15/11, como pidió el cliente en la entrevista del 26/10: que se use sin pérdida de funcionalidad desde móvil, tablet y ordenador, que sea accesible (WCAG 2.1 AA, personas ciegas o daltónicas y pautas DUA), que los formularios estén protegidos frente a spam e inyección, que el panel permita buscar y filtrar, que cargue rápido y que cumpla los plazos de conservación de datos.

> Este sprint reúne el Sprint 3 y el Sprint 4 que figuraban en el plan anterior. El **DMS** (Lab 4) es un sistema distinto con su propia documentación y su propio seguimiento SCRUM; se planifica en [`docs/dms/`](../../dms/README.md) y se entrega el 08/11.

## Cambios por la entrevista con el CADUS (26/10)

La entrevista completa está en [`docs/cliente/entrevista-cliente.md`](../../cliente/entrevista-cliente.md). Lo que cambia en este sprint:

| Respuesta del cliente | Cambio |
|---|---|
| Las votaciones son presenciales, solo votan los delegados (un voto por delegación, con DNI) y no se publican resultados | **HU-21 (papeleta online) cancelada.** El portal solo anuncia la votación, como ya hace HU-11. El registro de la votación pasa al DMS |
| El delegado puede dar de alta a su sucesor cuando se da de baja | **Nueva HU-22** |
| Tickets y mediaciones se conservan 2 años desde que se resuelven | **Nueva HU-23** (borrado o anonimización) |
| Aviso de ticket al correo de `dcadus`, plazo de respuesta (máximo 4 días hábiles desde que la Ejecutiva revisa el ticket) y datos mínimos (nombre y apellidos, facultad y correo US) | Tarea E3-08 |
| Calendario con asambleas y cursos | Tarea E3-07 |
| Móvil, tablet y ordenador | HU-14 incluye la tablet |
| Accesibilidad para personas ciegas o daltónicas y pautas DUA | HU-15 añade esos criterios |
| El servidor será un SFTP de la US y se busca poco mantenimiento | Tarea E3-03: confirmar qué ofrece el servidor (PHP y MySQL) |

## Cómo se organizan las tres semanas

Aunque es un solo sprint, hay un punto de control cada domingo para que el burndown no se concentre al final (la lección de los dos sprints anteriores). La línea ideal de `sprint-03.csv` es lineal; los puntos de control son el compromiso real: 18 SP pendientes el 01/11 y 10 el 08/11.

| Semana | Fechas | Historias | SP | Pendiente al cerrar la semana |
|---|---|---|---:|---:|
| 1 | 26/10 – 01/11 | HU-14 móvil y tablet, HU-17 spam e inyección, HU-22 alta del sucesor, HU-23 borrado a los 2 años | 18 | 18 |
| 2 | 02/11 – 08/11 | HU-15 accesibilidad (y la entrega del DMS) | 8 | 10 |
| 3 | 09/11 – 15/11 | HU-16 buscar y filtrar en el panel, HU-20 rendimiento, despliegue en la US, pruebas de aceptación, documentación final y Sprint Review | 10 | 0 |

Por qué este orden:

- **HU-14 antes que HU-15:** las dos tocan `cadus-interior.css`; así no se editan a la vez y la accesibilidad se comprueba sobre el diseño móvil ya definitivo.
- **HU-20 al final:** el rendimiento se mide con el sitio ya terminado.
- **HU-16 pasa a la semana 3:** el cliente no la mencionó entre sus prioridades y así la semana 2 queda libre para HU-15 y la entrega del DMS (el 08/11 hay 55 SP comprometidos entre CMS y DMS si no se mueve). Es la primera candidata a recortarse si hay retraso.

## Reparto de puntos

HU-14, HU-15, HU-16, HU-17 y HU-20 se dividen en subtareas para repartir la carga. En el Product Backlog siguen siendo una sola historia; se da por hecha cuando se cierran todas sus partes.

| Subtarea | Qué incluye | SP |
|---|---|---:|
| HU-14a | Menús y portada en móvil y tablet | 3 |
| HU-14b | Directorio, tablas y fichas de delegación en móvil y tablet | 3 |
| HU-14c | Buzón, calendario y mediación en móvil y tablet, probados en dispositivos reales | 2 |
| HU-15a | Contraste, foco visible, navegación por teclado y enlace «saltar al contenido» | 3 |
| HU-15b | Etiquetas de formularios, textos alternativos, jerarquía de encabezados, ARIA y lector de pantalla | 3 |
| HU-15c | Daltonismo, pautas DUA, auditoría con Lighthouse y axe y corrección de los fallos | 2 |
| HU-16a | Filtros por palabra clave y fecha en noticias, actas y delegaciones | 3 |
| HU-16b | Búsqueda en tickets sin exponer datos del estudiante (RN-03) | 2 |
| HU-17a | Honeypot y límite de envíos en el buzón y la mediación | 3 |
| HU-17b | Revisión de saneamiento, nonces y escape de salida; revisión de Wordfence | 2 |
| HU-20a | Optimización de imágenes (tamaño, formato y carga diferida) | 2 |
| HU-20b | Caché y minificación con WP Fastest Cache; medición antes y después | 3 |
| HU-22 | Relevo de la cuenta de la delegación por el delegado saliente o cualquier ejecutivo, con efecto inmediato (una cuenta por delegación, decidido el 09/11). Criterios: el delegado solo actúa sobre su propia cuenta; el relevo cierra todas las sesiones y el equipo anterior pierde el acceso; la ficha sigue en la misma cuenta; cada delegación tiene exactamente una cuenta activa; funciona sin correo saliente | 3 |
| HU-23 | Borrado o anonimización de tickets y mediaciones a los 2 años de resolverse | 2 |
| **Total** | | **36** |

| Integrante | Rol | SP |
|---|---|---:|
| Pablo | Product Owner e infraestructura | 7 |
| Joaquín | Scrum Master y portada | 6 |
| Miguel Ángel | Institucional y normativa; contacto con CADUS | 7 |
| Álvaro | Directorio de delegaciones | 8 |
| Marcos | Buzón y atención al estudiante | 8 |

La diferencia entre el que más y el que menos es de 2 SP, la misma que en el Sprint 2. Las tareas `E3-xx` (proceso, cliente y documentación) no llevan SP. A estos puntos se suman los del DMS (ver [`docs/dms/`](../../dms/README.md)).

## Reparto de tareas por integrante

> Historias tomadas del [Product Backlog](../backlog/product-backlog.md). Las tareas `E3-xx` no llevan SP.

### Pablo Ruiz Vidal — Product Owner y Dev Infraestructura (7 SP)

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-17b | Revisar el saneamiento de entradas, los nonces y el escape de salida en todos los formularios y revisar Wordfence. | 2 |
| HU-14c | Probar el buzón, el calendario y la mediación en móvil y tablet reales y corregir lo que falle. | 2 |
| HU-20b | Caché y minificación con WP Fastest Cache; medir con Lighthouse antes y después. | 3 |
| E3-02 | Crear las cuentas de los delegados cuando el CADUS facilite la lista (`scripts/roles`), comprobar que llega el correo del buzón y hacer el volcado `bd_cadus_v1_sprint3.sql`. | — |
| E3-06 | Montar el documento final (actualizar `scripts/entrega/build_doc.py` con el Sprint 3: backlog, burndown, capturas y trazabilidad) y generar Word y PDF. | — |

### Joaquín Luna Canela — Scrum Master y Dev Portada (6 SP)

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-14a | Menús y portada en móvil y tablet (menú plegable, tarjetas en una columna, galería y buscador). | 3 |
| HU-15a | Contraste, foco visible, navegación por teclado y enlace «saltar al contenido». Empieza al cerrar HU-14a. | 3 |
| E3-01 | Facilitar el Sprint: planning (26/10), daily en Discord, puntos de control del 01/11 y el 08/11, review y retrospectiva (15/11); **actualizar el burndown cada día** (`docs/scrum/burndown/sprint-03.csv`). | — |

### Miguel Ángel Camacho Martín — Dev Sección Institucional y Normativa; contacto con el CADUS (7 SP)

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-22 | Relevo de la cuenta de la delegación (decidido el 09/11: **una cuenta por delegación**, con el correo institucional de la delegación). Lo hace el delegado saliente o cualquier ejecutivo, con efecto inmediato: la cuenta no cambia, se pone una contraseña nueva y se cierran sus sesiones. Debe: limitar al delegado a su propia delegación, cortar el acceso del equipo anterior y mantener una sola cuenta activa por delegación. Actualizar RF-14 y RN-04. | 3 |
| HU-15c | Daltonismo, pautas DUA, auditoría de accesibilidad con Lighthouse y axe, y corrección de los fallos. **Hecho (12/11):** axe sin fallos en 17 páginas (escritorio y móvil) y Lighthouse 100 en accesibilidad; se corrigen seis fallos, dos de ellos de daltonismo (menú y filtros). Informe en [`docs/accesibilidad/HU-15c-auditoria.md`](../../accesibilidad/HU-15c-auditoria.md). | 2 |
| HU-20a | Optimizar las imágenes (tamaño, formato y carga diferida). **Hecho (12/11):** fotos de la galería en WebP de 360 y 720 px con `srcset` (de 1 MB a 0,15 MB en ordenador), logotipo de 47 a 17 KB, los 25 escudos de 1,6 a 0,3 MB, y para las imágenes que se suban: máximo 1920 px, tamaños intermedios en WebP y límite de 8 MB (`includes/imagenes.php`). | 2 |
| E3-03 | Preguntar a la US qué ofrece el servidor SFTP (PHP, MySQL, límites) y cómo se despliega, antes del 30/10. **Respondido por el CADUS (09/11), sin escribir a la US:** acceso por SFTP, HTTPS activo, PHP 7.2/7.3 con MySQL, sin correo saliente ni cron; acceso a la base de datos sin confirmar. | — |
| E3-07 | Añadir la categoría «Cursos» al calendario (asambleas y cursos). **Hecho (09/11):** `cadus-portal` crea una vez las categorías «Asambleas» y «Cursos» en The Events Calendar (reutiliza «asamblea» o «curso» si ya existen). Al crear un evento, la Ejecutiva marca su categoría; las votaciones solo ofrecen eventos de «Asambleas» (RN-05). | — |
| E3-09 | Desplegar en el servidor de la US cuando E3-03 confirme qué ofrece: migración, correo, tarea programada de HU-23, pruebas en destino y copia de seguridad. **Bloqueada (09/11) y movida al siguiente sprint:** WordPress 7.1 necesita PHP 7.4 o superior y `cadus-portal` y `cadus-eventos` piden PHP 8.0. Hace falta que la US suba PHP a 8.1 o superior (con `mysqli`, `mbstring` y `zip`) y diga cómo se accede a la base de datos. El correo se resolverá con SMTP a través de `dcadus@us.es` y la tarea de HU-23 con WP-Cron, que se lanza con las visitas. La entrega del Sprint 3 se hace en el servidor del equipo. **Decisión del 22/11/2026:** no se sabe si se va a desplegar en la US, así que no se persigue; queda anotado como pendiente «hablar con la US sobre el despliegue web» (qué ofrece, PHP y base de datos) y la tarea no cuenta para cerrar los sprints. | — |

### Álvaro Martínez Ocaña — Dev Directorio de Delegaciones (8 SP)

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-14b | Directorio, tablas y fichas de delegación en móvil y tablet. | 3 |
| HU-16a | Filtros por palabra clave y fecha en noticias, actas y delegaciones. | 3 |
| HU-23 | Borrado o anonimización de tickets y mediaciones a los 2 años de resolverse (tarea programada con pruebas). | 2 |
| E3-04 | Pruebas de aceptación: guion por historia y por rol (HU-14 a HU-23, con la privacidad de todas las consultas, las tres operaciones en menos de un minuto y la aprobación por la Ejecutiva de todo el contenido) y ejecución en la semana 3. | — |

### Marcos-Paban Delgado Rodríguez — Dev Atención al Estudiante y Buzón (8 SP)

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-17a | Honeypot y límite de envíos en el buzón y la mediación. | 3 |
| HU-15b | Etiquetas de formularios, textos alternativos, jerarquía de encabezados, ARIA y lector de pantalla. | 3 |
| HU-16b | Búsqueda en el panel de tickets sin exponer datos del estudiante (RN-03); ampliar la batería de pruebas de privacidad. | 2 |
| E3-05 | Revisar el REM y la trazabilidad con los cambios del sprint y regenerar `CADUS.rem` con `scripts/remus/build_rem.ps1`: ampliar RN-03 a todas las consultas y RN-01 a todo el contenido, cerrar el plazo de conservación (2 años), añadir RF-14 con el relevo de delegados y los criterios de accesibilidad (DUA) y la regla de las tres operaciones en menos de un minuto. | — |
| E3-08 | Tickets: aviso al correo de `dcadus` y datos mínimos del estudiante (nombre y apellidos, facultad y correo US). Plazo de respuesta aclarado con Miguel Ángel el 09/11: **máximo 4 días hábiles, contados desde que la Ejecutiva revisa el ticket**. Publicarlo en el buzón con el texto «Te responderemos en un máximo de 4 días hábiles desde que revisemos tu consulta». | — |

**Capacidad total comprometida del Sprint:** 36 SP iniciales (la línea ideal del burndown parte de 36), más 8 SP de HU-24 añadidos el 12/11 y las tareas `E3-xx`.

## Pendiente del Sprint 2

Siguen abiertas en el GitHub Project las tareas de contenido y cliente del Sprint 2: entrevista con el CADUS (E2-09, hecha el 26/10), actas e institucional reales (E2-11), fichas de delegaciones (E2-12, ahora con las 27 fichas sacadas de `cadus.us.es/delegaciones/`), noticias reales (E2-08), eventos reales del calendario (E2-19) y cuentas de los delegados (E2-01). No suman puntos. El cliente indicó que todo contenido pasa por la Ejecutiva y que el portal actual es una web de prueba.

**Avance del 12/11 (Miguel Ángel):** E2-11 tiene ya el contenido real de «Qué es el CADUS» y «Gobierno y estatutos», basado en el art. 21 de los Estatutos de la US (Decreto 98/2025) y en el REOREUS (`includes/institucional.php`). Las actas reales las sube la Ejecutiva desde **Actas y normativas**. Para E2-19 hay un cargador de eventos reales con su categoría (`scripts/eventos/`).

## Tareas de todo el equipo

| ID | Tarea | Cuándo |
|---|---|---|
| T-01 | Cada uno prueba la historia de otra persona (prueba cruzada) y anota los fallos como issues. | al cerrar cada historia |
| T-02 | Cada uno hace las capturas de lo suyo (ordenador, tablet y móvil) y escribe el pie y la explicación con los códigos RF/HU. | semana 3 |
| T-03 | Marcar su tarea en GitHub Projects al terminarla; el burndown se calcula de ahí. | cada día |
| T-04 | Una pull request pequeña por subtarea, partiendo de `git pull` de `main`. | siempre |

## Calendario

| Fecha | Hito |
|---|---|
| Lun 26/10 | Sprint Planning y entrevista con el CADUS |
| Vie 30/10 | Respuesta de la US sobre el servidor SFTP (E3-03) |
| Dom 01/11 | Punto de control 1: HU-14, HU-17, HU-22 y HU-23 terminadas (quedan 18 SP) |
| Dom 08/11 | Punto de control 2: HU-15 terminada (quedan 10 SP). **Entrega del DMS** |
| Lun 09/11 | HU-16, HU-20 y despliegue en el servidor de la US (E3-09) |
| Jue 12/11 | **Congelación de funcionalidad** y pruebas de aceptación |
| Vie 13/11 | Documento final del CMS montado y volcado de la BD |
| Dom 15/11 | **Entrega final del CMS** y Sprint Review |

## Definición de Hecho (DoD) — Sprint 3

- [ ] HU-14, HU-15, HU-16, HU-17, HU-20, HU-22 y HU-23 implementadas, probadas por otra persona e integradas en `main`.
- [ ] Portal probado en móvil y tablet sin pérdida de funcionalidad (HU-14). **Cambio de criterio decidido por el equipo el 12/11:** se prueba en emulación (`scripts/pruebas/movil.py`, 28 comprobaciones) y no en dispositivos reales; queda anotado como limitación y no cumple la redacción original («reales»).
- [ ] Informe de Lighthouse y axe sin fallos críticos de accesibilidad, revisado para daltonismo y lector de pantalla (HU-15).
- [ ] Batería de pruebas de privacidad y de seguridad sin fallos (RN-03, HU-17, HU-23).
- [ ] Medición de rendimiento antes y después de la caché y de las imágenes (HU-20).
- [ ] Pruebas de aceptación por historia y por rol ejecutadas y documentadas.
- [ ] Burndown actualizado **cada día**, sin saltos de última hora.
- [ ] Trazabilidad REM ↔ análisis ↔ diseño ↔ implementación actualizada en el documento final.
- [ ] Contenido real validado con el cliente (o marcado como pendiente) y cuentas de los delegados creadas.
- [ ] Volcado `bd_cadus_v1_sprint3.sql` revisado y subido (al cerrar la entrega).
- [ ] Sin secretos, credenciales ni datos personales reales en el repositorio.

## Riesgos

| Riesgo | Medida |
|---|---|
| El trabajo se deja para el final, como en los sprints 1 y 2. | Puntos de control los domingos 01/11 y 08/11 y burndown diario. |
| El servidor SFTP de la US puede no ofrecer PHP y MySQL, necesarios para WordPress. Una versión estática no cubriría tickets, cuentas ni administración. | E3-03 antes del 30/10; si no los ofrece, se busca un hosting alternativo y se avisa al cliente. E3-09 reserva la semana 3 para desplegar y probar en destino. |
| HU-14 y HU-15 tocan el mismo CSS. | HU-15a empieza al cerrar HU-14a; pull request pequeña por subtarea. |
| El DMS compite por las mismas personas y la entrega es el 08/11. | El DMS se planifica aparte con reparto propio (ver `docs/dms/`); el DMS es sobre todo documentación y configuración. |
| El borrado a los 2 años (HU-23) podría eliminar datos que aún se necesiten. | Probarlo con datos de ejemplo y anonimizar en lugar de borrar cuando haya dudas. |
| Todo el contacto con el cliente pasa por una sola persona. | Miguel Ángel resume cada reunión en Discord (#scrum) y Pablo, como Product Owner, valida las prioridades. |

## Estado a 12/11/2026

Según los commits de GitHub (ramas fusionadas en `main` el 12/11) y los resultados de pruebas del propio equipo.

| Subtarea | Quién | Fecha | Evidencia |
|---|---|---|---|
| HU-22 relevo de la cuenta de la delegación (3 SP) | Miguel Ángel | 09/11 | `includes/relevo.php`; `scripts/roles` |
| HU-17a honeypot y límite de envíos (3 SP) | Marcos | 11/11 | baterías `sprint3_buzon.py` (81 correctas, 0 fallos) y de privacidad |
| HU-16b búsqueda de tickets sin exponer datos (2 SP) | Marcos | 11/11 | `sprint3_buzon.py` |
| HU-15b etiquetas, encabezados y ARIA en Atención al estudiante (3 SP) | Marcos | 12/11 | `hu15b_accesibilidad.py` (59 correctas, 0 fallos) |
| E3-03, E3-05, E3-07 y E3-08 (sin puntos) | Miguel Ángel y Marcos | 09–11/11 | `scripts/pruebas/SPRINT3_BUZON.md`, calendario con «Asambleas» y «Cursos», REM v2.2 |

**Cambio de alcance (12/11): HU-24, acceso y gestión desde el portal (8 SP, Pablo).** Pedida por el cliente en la entrevista (portal fácil de usar para personas con pocos conocimientos informáticos) y por Pablo al probar la cuenta del CADUS: apartado «Acceder» en el menú, página de acceso dentro del portal y página «Gestión» donde cada rol ve solo lo que puede hacer (la Ejecutiva crea noticias, eventos del calendario, actas y normativas con su PDF y gestiona las delegaciones; cada delegación edita solo su ficha). Módulo `includes/gestion.php`; pruebas en `scripts/pruebas/gestion.php` (93 correctas, 0 fallos, con peticiones HTTP reales a los formularios y a la API REST). El compromiso del sprint pasa de 36 a 44 SP.

**Cierre del 12/11 por la noche: 9 SP pendientes de 44** (35 hechos). Se han fusionado en `main` los PR #69, #70 (Marcos) y #72, #73, #74 y #75 (Álvaro). Sin empezar según el repositorio: HU-14a (Joaquín), HU-14b (Álvaro) y HU-15a (Joaquín), 9 SP en total. El hito del 08/11 (10 SP pendientes) no se alcanzó.

| Subtarea | Quién | Fecha | Evidencia |
|---|---|---|---|
| HU-17b revisión de saneado, nonces y escape; Wordfence (2 SP) | Pablo | 12/11 | `docs/seguridad/HU-17b-revision-formularios.md`; escaneo de Wordfence sin malware ni vulnerabilidades. **Pendiente de Pablo (cambiadas según él el 23/11; ver la actualización del 25/11):** cambiar la contraseña de `root` (hallazgo crítico) y confirmar con Miguel Ángel su cuenta (aviso «creada fuera de WordPress») |
| HU-20b caché y minificación con Lighthouse (3 SP) | Pablo | 12/11 | `docs/rendimiento/HU-20b-informe.md`: Rendimiento 91 → 99 (Inicio), 90 → 99 (Noticias), 79 → 97 (Delegaciones) y 83 → 99 (Actas); peso −40 % con Gzip |
| HU-14c móvil y tablet (2 SP) | Pablo | 12/11 | `docs/pruebas/HU-14c-movil-tablet.md`, `scripts/pruebas/movil.py` (28 de 28 comprobaciones). En emulación el 12/11; el 22/11 Pablo probó su móvil real y el 23/11 da por comprobada y buena la tablet |
| HU-16a filtros por palabra clave y fecha (3 SP) | Álvaro | 12/11 | PR #72. Comprobada por HTTP el 12/11 por Pablo: en noticias, «becas» deja 2 de 5 y un texto inexistente muestra el aviso de vacío; en actas, «pleno» y los filtros «desde» y «hasta» filtran bien y los valores se escapan. La prueba en navegador de H16-1 a H16-6 se hizo con clics el 22/11/2026 (todos OK, `tests/E3-04-pruebas-de-aceptacion.md`); H16-7 (búsqueda en el panel de tickets) se ejecutó también el 22/11 con la cuenta `test-ejecutivo`, por Claude en nombre de Pablo: no es prueba cruzada |
| HU-23 anonimización de tickets y mediaciones a los 2 años (2 SP) | Álvaro | 12/11 | PR #73; `scripts/pruebas/hu23_prueba_retencion.php` correcta (simulación y ejecución, segunda ejecución idempotente). **Revisión cruzada con Codex el 13/11:** corregidos el título y la dirección (slug) que conservaban el asunto del estudiante, la anonimización de un ticket reabierto entre la selección y el borrado (ahora se revalida bajo el mismo bloqueo del buzón), la limpieza dada por buena aunque fallase un borrado y la edición de tickets ya anonimizados |
| E3-08 plazo de respuesta publicado (sin puntos) | Marcos | 12/11 | PR #69; REM del CMS 2.3 |

**Decisión X7 (12/11):** la Ejecutiva puede editar las delegaciones de otros autores. RN-04 queda como «la cuenta de la delegación o la cuenta del CADUS (Ejecutiva y administrador)»; la delegación solo cambia los datos de contacto, el horario, las redes, los enlaces y los miembros de su propia ficha, y un delegado no puede cambiar el título, el centro ni el estado de la ficha ni por la API REST.

**Actualización del 12/11 por la tarde (Miguel Ángel):** HU-15c y HU-20a están hechas (4 SP), con lo que Miguel Ángel termina sus 7 SP. HU-20a atiende además la recomendación del informe de HU-20b: los 25 escudos pasan de 1,6 MB a 0,3 MB y se sirven en WebP a su tamaño.

**Bloqueada (09/11):** E3-09, el despliegue en el servidor de la US. El servidor ofrece PHP 7.2/7.3 y WordPress 7.1 necesita 7.4 o superior (el plugin propio, 8.0). Pasa al siguiente sprint hasta que la US actualice PHP. El 22/11/2026 se decidió no perseguirlo: queda pendiente hablar con la US sobre el despliegue web, sin saber si se hará.

**Sin prueba cruzada:** las pruebas anteriores las ejecutó quien hizo cada subtarea; falta que otra persona las repita (T-01).

## Estado a 15/11/2026 (cierre)

| Subtarea | Quién | Fecha | Evidencia |
|---|---|---|---|
| HU-14a menús y portada en móvil y tablet (3 SP) y HU-15a contraste, foco, teclado y «saltar al contenido» (3 SP) | Joaquín | 13/11 | `tests/HU-14a-HU-15a-portada.md`, commit `788f1fb`. **Medidas sobre una réplica estática** de la portada y las interiores (Chromium) con los mismos CSS y JS del plugin: no incluyen la cabecera real del tema, ni dispositivos reales, ni lector de pantalla |
| HU-14b directorio, tablas y fichas en móvil y tablet (3 SP) | Álvaro | 14–15/11 | `tests/HU-14b-movil-tablet.md`, PR #77 fusionado el 15/11. Medido en una maqueta y en el WordPress local en emulación (390 y 768 px); la ficha de Derecho está «pendiente de completar», así que no se probaron filas con textos largos |
| E3-04 pruebas de aceptación | Álvaro | 15/11 | `tests/E3-04-pruebas-de-aceptacion.md`: guion con resultados parciales (H16-1 a H16-6 por peticiones anónimas); T1, T2 y T3 quedan pendientes porque el WordPress local no tiene Fluent Forms con el formulario ni The Events Calendar |
| Revisión cruzada con Codex (CMS y DMS) | Pablo | 13/11 | `docs/scrum/codex_revision_cms_sprint3_final.md`; correcciones de HU-23, RN-04, HU-21 y HU-22 en el commit `763353e` |

**Resultado: 0 SP pendientes de 44 el 15/11**, contando como hecha una subtarea cuando está integrada en `main`.

## Resultado del Sprint 3

- **Puntos:** 36 SP planificados y 8 SP de HU-24 añadidos el 12/11: 44 SP, todos integrados en `main` el 15/11. HU-21 (votar desde el portal) se canceló tras la entrevista del 26/10.
- **Cómo se llegó:** no se cerró ningún punto hasta el 08/11 (hitos de 18 y 10 SP no alcanzados); 33 SP pendientes el 09/11, 25 el 11/11, 9 el 12/11, 3 el 13/11 y 0 el 15/11. Se repite el cierre de última hora de los sprints anteriores.
- **Lo que «hecho» no significa todavía:** casi todas las pruebas las ejecutó quien implementó la subtarea; la prueba cruzada (T-01), la prueba en dispositivos reales (cambio de criterio de la DoD, decidido el 12/11) y la prueba con cuentas reales de cada rol siguen pendientes, y E3-04 está a medias.
- **Pruebas del 22/11/2026 en WampServer:** H16-1 a H16-6, T1 (buzón: ticket creado) y T2 (calendario con eventos) pasan; H14-2 a H14-4 pasan en emulación a 390 y 768 px; H15-1 y H15-3 solo parciales. Siguen sin hacerse: dispositivos reales (H14-5), lector de pantalla, cuentas por rol y la prueba cruzada por otra persona.
- **Reapertura del 22/11/2026:** el equipo reabrió HU-14 (#23) y HU-15 (#24) en GitHub (estado «In Progress») para terminarlas: faltan los casos manuales (tablet y móvil reales, menús, buzón, calendario y `/gestion/`; teclado, lector de pantalla y formulario real del buzón). El 22/11 Pablo probó HU-14 entera en su móvil real (se ve bien tras vaciar la caché del WordPress local): HU-14 vuelve a «Hecha», con una tablet real y la prueba cruzada pendientes (Pablo programó HU-14c). HU-15 sigue en curso: faltan el lector de pantalla real y el recorrido completo con teclado.
- **Pruebas del 23/11/2026 (Marcos, con Claude; `tests/pruebas-marcos-23-11.md`):** HU-15 con teclado (H15-1), Lighthouse 97 / 96 / 96 (H15-2) y daltonismo (H15-4) correctos; H15-3 parcial (falta Narrador o NVDA). Pruebas cruzadas: H14-1 (HU-14a, emulación), H17-3 (HU-17b, con el panel visto después) y H23-1, H23-4 y H23-5 (HU-23). Quedan dos arreglos menores: el contraste de `p.cadus-contacto__marca` en el pie y enlazar con `aria-describedby` los errores del formulario con su campo, llevando el foco al primer error.
- **Sin cerrar:** E3-09 (despliegue en el servidor de la US, bloqueado por PHP 7.2/7.3), E3-06 (documento final del CMS) y E3-02 (volcado de la base de datos y cuentas de los delegados), que dependen de que el CADUS decida quedarse con el portal.
- **Pendiente de Pablo:** cambiar las contraseñas de `root` y `cadus` (Wordfence, crítica) y confirmar la cuenta de Miguel Ángel.

## Sprint Review y retrospectiva

> Redactada el 22/11/2026 por Pablo, con Claude, a partir de los datos del sprint (commits, burndown, pruebas y revisiones). No sale de una reunión del equipo: si el equipo hace la retrospectiva en grupo, se añaden aquí sus conclusiones.

### Review (15/11/2026)

- **Entregado:** 44 SP integrados en `main` (36 planificados y 8 de HU-24): móvil y tablet (HU-14), accesibilidad (HU-15), búsqueda y filtros (HU-16), protección de formularios (HU-17), rendimiento (HU-20), relevo de delegados (HU-22), conservación a los 2 años (HU-23) y acceso y gestión desde el portal (HU-24). HU-21 se canceló tras la entrevista.
- **Calidad:** 96 comprobaciones propias en la gestión del portal, baterías de privacidad del buzón y la mediación en verde, y una revisión cruzada con Codex el 13/11 que encontró fallos reales en HU-23, RN-04 y el relevo, ya corregidos.
- **Sin cerrar:** E3-09 (despliegue en la US, bloqueado por PHP 7.2/7.3), E3-02 (volcado de la base de datos y cuentas de los delegados, que dependen del CADUS) y E3-06 (documento final del CMS, para la entrega final del domingo 29/11, adelantada el 23/11 desde el 07/12).

### Retrospectiva

| Qué fue bien | Qué no | Qué cambiamos |
|---|---|---|
| Las baterías automáticas y la revisión con Codex encontraron fallos antes de entregar | El burndown estuvo plano hasta el 08/11 (los hitos de 18 y 10 SP no se alcanzaron) y el trabajo se cerró entre el 09 y el 15/11 | Actualizar el burndown cada día y fijar hitos intermedios con alguien que los vigile |
| La decisión X7 y los cambios de alcance (HU-24) se documentaron en el momento | Casi todas las pruebas las hizo quien implementó cada subtarea; la prueba cruzada humana no se hizo | Reservar un día antes de cada entrega para pruebas cruzadas, con registro de fecha, persona y resultado |
| Los informes (HU-14c, HU-17b, HU-20b) dicen lo que miden y lo que no | Móvil y tablet solo en emulación, sin dispositivos reales | Hecho: móvil real el 22/11 y tablet el 23/11, comprobados según Pablo |
| El CMS, el DMS y la red social llevan documentación separada | Se perdió el contacto con el CADUS (Miguel Ángel dejó el trabajo el 16/11) y las tareas que dependían del cliente quedaron abiertas | Marcar «por confirmar» lo que dependa del CADUS y no planificar tareas que dependan de un contacto que ya no está |

### Retrospectiva en grupo (27/11/2026)

> **Celebrada el 27/11/2026, según Pablo** (Product Owner), que comunicó lo acordado; **no se registraron los asistentes ni las intervenciones**, y este apartado lo ha redactado Claude a partir de la propuesta del Scrum Master y de lo que Pablo comunicó. Se hizo en 30 minutos, con el formato previsto: datos, qué fue bien y qué no, acciones y responsables.

**Datos que se vieron** (`burndown-sprint-03.csv` y Sprints 1 y 2 del CMS)

| Indicador | Sprint 1 | Sprint 2 | Sprint 3 |
|---|---|---|---|
| Puntos comprometidos | 70 | 29 | 36 (44 con los 8 de HU-24) |
| Cuándo se cerraron | 60 SP (86 %) el último día | 23 SP (79 %) los dos últimos días | 0 SP en las dos primeras semanas (26/10 a 08/11); 24 SP (55 %) el 12/11 y 33 SP (75 %) del 12 al 15/11 |

El patrón se repitió tres sprints seguidos aunque en cada retrospectiva se acordó actualizar el burndown cada día. La red social ya usa un script que lo hace en un comando (`scrum_rsi_sprint.py`, en el repositorio).

**Qué fue bien, qué no y qué cambiamos:** la tabla del apartado «Retrospectiva» anterior es el punto de partida; lo concreto que se acordó son las tres acciones siguientes.

**Acciones acordadas**

| Acción | Responsable | Cómo se comprueba |
|---|---|---|
| A. Un día reservado antes de cada entrega para pruebas cruzadas humanas, con fecha, persona y resultado | Todos; lo vigila Joaquín | Cada prueba está firmada por alguien distinto de quien la implementó |
| B. Burndown actualizado cada día y un hito intermedio que alguien vigile | Pablo | El CSV del sprint tiene una fila por día, sin saltos de más de un tercio del alcance |
| C. Marcar «por confirmar» lo que dependa del CADUS y no planificar tareas que dependan de un contacto que ya no está | Pablo | Ninguna tarea del sprint depende de un contacto sin confirmar |

## Actualización del 25/11/2026 (cierre de las tareas abiertas)

Este apartado prevalece sobre los estados anteriores de este documento, que se conservan como historial de lo ocurrido hasta el 15/11.

| Tarea | Estado a 25/11/2026 |
|---|---|
| E2-01 cuentas reales del CADUS (#36) | **Descartada y cerrada:** depende del CADUS y el contacto se perdió el 16/11; se entrega con las cuentas actuales |
| E2-12 fichas reales de delegaciones (#47) | **Cerrada:** 27 fichas con los datos de la web del CADUS y edición restringida comprobada (`tests/E2-12-fichas-y-edicion.md`). Faltan el correo en 1 ficha, el teléfono en 7 y el horario en las 27: la web no los publica |
| E3-09 despliegue en la US (#67) | **Descartada y cerrada:** queda pendiente hablar con la US sobre el despliegue web |
| Contraseñas de `root` y `cadus` | Cambiadas el 23/11 según Pablo (sin constancia en el repositorio, por seguridad) |
| HU-14 móvil y tablet | Hecha: móvil real el 22/11 y tablet el 23/11, comprobados según Pablo |
| HU-15 accesibilidad | En curso: teclado, Lighthouse de accesibilidad, daltonismo y Narrador hechos (Marcos, 23/11) y arreglo de los errores de los formularios fusionado (PR #96, 25/11); falta repetir Lighthouse con el código actual |
| E3-01 retrospectiva en grupo (#57), E3-02 volcado y limpieza (#58), E3-06 documento final (#62) | Abiertas, con dueño y límite jueves 26/11 22:00 (`docs/scrum/plan-23-11.md`) |

## Actualización del 26/11/2026 (cierre de las pruebas)

Este apartado prevalece sobre el del 25/11 donde se contradigan.

| Tarea | Estado a 26/11/2026 |
|---|---|
| HU-15 accesibilidad (#24) | **Cerrada:** Lighthouse de accesibilidad repetido con el código actual, 100 / 100 / 100 (Marcos, PR #98); queda sin probar NVDA |
| HU-20 rendimiento | Lighthouse de la portada en móvil, 98 con el contenido real (91 antes de optimizar y 99 después, 12/11) (H20-1); el límite de 8 MB de imágenes no se aplicaba a las subidas por la API REST del editor de bloques, corregido y repetido (H20-2) |
| HU-22 relevo de la cuenta | H22-1 a H22-5 ejecutados el 26/11 por Pablo con Claude, con sesiones reales de las cuentas de prueba; todos OK. No son prueba de otra persona |
| E3-04 pruebas de aceptación | 43 casos: 39 OK y 4 parciales (T1 a T3 y P5) |
| E3-01 retrospectiva en grupo (#57) | **Hecha el 27/11/2026, según Pablo** (asistentes no registrados): tres acciones acordadas (pruebas cruzadas antes de cada entrega, burndown diario y «por confirmar» lo que dependa del CADUS), en el apartado «Retrospectiva en grupo» |
| E3-02 volcado y limpieza (#58) | **Cerrada el 26/11:** ficha 32 devuelta a su autor, cuentas y tickets de prueba borrados y volcado `bd_cadus_v1_sprint3.sql` generado |
| E3-06 documento final (#62) | **Cerrada el 26/11:** REM de la red social exportado desde REMUS (`REM-RSI-v1.1.pdf`) y zip final `Entrega-29-11-CADUS-CMS-DMS-RSI-v2.zip` generado con todos los controles en verde; falta solo enviarlo |
