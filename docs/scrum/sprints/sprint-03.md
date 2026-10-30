# Sprint 3 — Móvil, accesibilidad, seguridad, rendimiento y cierre del CMS

**Equipo:** 5 integrantes
**Cliente:** CADUS (Consejo de Alumnos de la Universidad de Sevilla). **Contacto con el cliente:** Miguel Ángel Camacho Martín, que forma parte del CADUS.
**Periodo:** 26/10/2026 – 15/11/2026 (un único sprint de tres semanas, como acordó el equipo con el profesor)
**Estado:** En curso. Compromiso: 36 SP (HU-14, HU-15, HU-16, HU-17, HU-20, HU-22 y HU-23)

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
| Aviso de ticket al correo de `dcadus`, plazo de respuesta de 4 días y datos mínimos (nombre y apellidos, facultad y correo US) | Tarea E3-08 |
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
| HU-22 | El delegado da de alta a su sucesor (y cualquier ejecutivo puede hacerlo), con efecto inmediato. Criterios: el delegado solo crea a su propio sucesor; al darlo de alta se revoca el acceso del anterior; la ficha pasa a la cuenta nueva; cada delegación tiene exactamente una cuenta activa | 3 |
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
| HU-22 | Permitir que el delegado dé de alta a su sucesor (y que cualquier ejecutivo lo haga) con efecto inmediato. Debe: limitar al delegado a su propia delegación, revocar el acceso del anterior, traspasar la ficha y mantener una sola cuenta activa por delegación. Actualizar RF-14 y RN-04. | 3 |
| HU-15c | Daltonismo, pautas DUA, auditoría de accesibilidad con Lighthouse y axe, y corrección de los fallos. | 2 |
| HU-20a | Optimizar las imágenes (tamaño, formato y carga diferida). | 2 |
| E3-03 | Preguntar a la US qué ofrece el servidor SFTP (PHP, MySQL, límites) y cómo se despliega, antes del 30/10. | — |
| E3-07 | Añadir la categoría «Cursos» al calendario (asambleas y cursos). | — |
| E3-09 | Desplegar en el servidor de la US cuando E3-03 confirme qué ofrece: migración, correo, tarea programada de HU-23, pruebas en destino y copia de seguridad. | — |

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
| E3-08 | Tickets: aviso al correo de `dcadus` y datos mínimos del estudiante (nombre y apellidos, facultad y correo US). El plazo de respuesta (el cliente dijo «al menos 4 días») no se publica hasta aclarar con Miguel Ángel si es mínimo o máximo, en días naturales o hábiles y desde cuándo se cuenta. | — |

**Capacidad total comprometida del Sprint:** 36 SP, más las tareas `E3-xx`.

## Pendiente del Sprint 2

Siguen abiertas en el GitHub Project las tareas de contenido y cliente del Sprint 2: entrevista con el CADUS (E2-09, hecha el 26/10), actas e institucional reales (E2-11), fichas de delegaciones (E2-12, ahora con las 27 fichas sacadas de `cadus.us.es/delegaciones/`), noticias reales (E2-08), eventos reales del calendario (E2-19) y cuentas de los delegados (E2-01). No suman puntos. El cliente indicó que todo contenido pasa por la Ejecutiva y que el portal actual es una web de prueba.

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
- [ ] Portal probado en móvil y tablet reales, sin pérdida de funcionalidad (HU-14).
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

## Resultado del Sprint 3

*(se completará al cerrar el sprint)*

## Sprint Review y retrospectiva

*(15/11/2026)*
