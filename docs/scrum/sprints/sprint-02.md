# Sprint 2 — Participación estudiantil, gestión avanzada y Entrega 2 (CMS final)

**Equipo:** 5 integrantes
**Cliente:** CADUS (Consejo de Alumnos de la Universidad de Sevilla). **Contacto con el cliente:** Miguel Ángel Camacho Martín, que forma parte del CADUS.
**Periodo:** 19/10/2026 – 25/10/2026 (entrega 2 del CMS, versión final)
**Estado:** Cerrado. Alcance completado (29 de 29 SP) el 24/10/2026; la entrega 2 es el 25/10/2026

## Objetivo del Sprint

Completar el portal con las historias de participación (tickets avanzados, calendario, votaciones, mediación y panel de administración), sustituir el contenido de ejemplo por contenido real validado con el cliente y entregar la documentación final del CMS.

## Qué exige la entrega 2

Según el enunciado (Lab 2-3, «1st and 2nd deliverables»), la versión final debe incluir, además de lo ya entregado:

- REM revisado con todos los requisitos elicitados tras una entrevista con el cliente.
- Análisis: **mockups** de las páginas (con una herramienta como Figma) con su descripción, diagrama de clases y capturas de menús y página principal.
- Diseño: comparativa de **al menos tres plugins de cada tipo** (con los obligatorios: seguridad, caché, analítica y SEO) y comparativa de **al menos tres temas**, con la razón de la elección.
- Implementación: capturas de la web **explicadas una a una**.
- Planificación: herramienta colaborativa, control de versiones, y en cada entrega **product backlog, sprint backlog y burndown** (este último del Sprint 2).
- Trazabilidad entre REM, análisis, diseño e implementación.

## Reparto de puntos

Para que la carga sea parecida, HU-09 (8 SP) y HU-19 (8 SP) se dividen en subtareas. En el Product Backlog siguen siendo una sola historia; la historia se da por hecha cuando se cierran todas sus partes.

| Subtarea | Qué incluye | SP |
|---|---|---:|
| HU-09a | Panel de tickets: listado, filtros, cambio de estado y respuesta al estudiante | 5 |
| HU-09b | Privacidad de las reclamaciones (RN-03): permisos, sin datos sensibles en avisos ni en búsquedas | 3 |
| HU-19a | Ocultar los menús de administración que no usa cada rol (Ejecutiva y Delegado) | 3 |
| HU-19b | Panel de inicio con accesos directos a noticias, actas, delegaciones y tickets | 3 |
| HU-19c | Pruebas del panel con cada rol y corrección de fallos | 2 |
| HU-10 | Calendario de asambleas y eventos | 3 |
| HU-11 | Convocatorias de votación vinculadas a una asamblea | 5 |
| HU-12 | Solicitud de mediación estudiantil | 5 |
| **Total** | | **29** |

| Integrante | Rol | SP |
|---|---|---:|
| Pablo | Product Owner e infraestructura | 6 |
| Joaquín | Scrum Master y portada | 5 |
| Miguel Ángel | Institucional y normativa; contacto con CADUS | 6 |
| Álvaro | Directorio de delegaciones | 7 |
| Marcos | Buzón y atención al estudiante | 5 |

La diferencia entre el que más y el que menos es de 2 SP. Las tareas `E2-xx` (documentación de la entrega) no llevan SP y se reparten de forma que quien tiene menos puntos tenga más documentación.

## Reparto de tareas por integrante

> Historias tomadas del [Product Backlog](../backlog/product-backlog.md). Las tareas `E2-xx` son de la entrega y no llevan SP.

### Pablo Ruiz Vidal — Product Owner y Dev Infraestructura (6 SP)

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-19a | Ocultar los menús de administración que no usa cada rol (Ejecutiva y Delegado). | 3 |
| HU-09b | Privacidad de las reclamaciones (RN-03): solo la Ejecutiva ve los tickets, sin datos sensibles en avisos, búsquedas ni API. | 3 |
| E2-01 | Asignar los roles Ejecutiva y Delegado a los usuarios reales (la lista la facilita Miguel Ángel) y retirar cuentas de administrador innecesarias. | — |
| E2-02 | Volcado `bd_cadus_v1_sprint2.sql`, push de la versión final y revisión de Wordfence antes de entregar. | — |
| E2-03 | Montar el documento de la entrega 2 (actualizar `scripts/entrega/build_doc.py`), generar Word y PDF y revisar la trazabilidad completa. | — |
| E2-04 | Priorizar el backlog con el cliente a través de Miguel Ángel y dar el visto bueno a cada historia. | — |

### Joaquín Luna Canela — Scrum Master y Dev Portada (5 SP)

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-11 | Convocatorias de votación vinculadas a una asamblea del calendario (RN-05), con YOP Poll. Depende de HU-10. | 5 |
| E2-05 | Facilitar el Sprint: planning (19/10), daily en Discord, review y retrospectiva; **actualizar el burndown cada día** (`docs/scrum/burndown/sprint-02.csv`) y regenerar la gráfica. | — |
| E2-06 | Retrospectiva del Sprint 1 y del Sprint 2 en el documento (lección: el trabajo se concentró en el último día). | — |
| E2-07 | Comparativa de **al menos tres temas** (Blocksy, Astra, Kadence u otros) con fecha de actualización, instalaciones, valoración y accesibilidad; justificar Blocksy. Datos de partida en `docs/entrega/datos/themes.json`. | — |
| E2-08 | Sustituir los comunicados de ejemplo de la portada por noticias reales y comprobar el banner. | — |

### Miguel Ángel Camacho Martín — Dev Sección Institucional y Normativa; contacto con el CADUS (6 SP)

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-10 | Calendario de asambleas y eventos con The Events Calendar, en el menú y en la portada. Hay que terminarlo antes del miércoles porque HU-11 depende de él. | 3 |
| HU-19b | Panel de inicio con accesos directos a noticias, actas, delegaciones y tickets. | 3 |
| E2-09 | Entrevista con el CADUS: confirmar requisitos y prioridades, conseguir el logotipo y la identidad visual, y la lista de usuarios reales con su rol (Ejecutiva y delegados). Anotar el resultado en el REM. | — |
| E2-10 | Mockups finales en Figma de portada, calendario, votación, mediación, directorio, buzón y ficha de acta; con descripción de cada pantalla y las etiquetas de trazabilidad. | — |
| E2-11 | Sustituir actas, estatutos y las páginas «Qué es el CADUS» y «Gobierno» por los documentos reales. | — |

### Álvaro Martínez Ocaña — Dev Directorio de Delegaciones (7 SP)

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-12 | Solicitud de mediación estudiantil con un formulario de Fluent Forms, validando `@alum.us.es` y con aviso de privacidad. Reutiliza la validación del buzón. | 5 |
| HU-19c | Probar el panel de administración con cada rol (Ejecutiva, Delegado, Estudiante) y corregir los fallos. | 2 |
| E2-12 | Rellenar las fichas reales de delegaciones (delegado, correo, teléfono, horario y enlaces) y comprobar la edición restringida al delegado propietario. | — |
| E2-13 | Actualizar los diagramas (`scripts/entrega/diagramas.py`): clases del análisis con las entidades nuevas, estructura web y UML de plugins final. | — |

### Marcos-Paban Delgado Rodríguez — Dev Atención al Estudiante y Buzón (5 SP)

| ID | Tarea concreta | SP |
|---|---|---:|
| HU-09a | Panel de tickets: listado, filtros, cambio de estado y respuesta al estudiante. Decidir el martes si se instala SupportCandy o se amplía el módulo propio `buzon.php`, y justificarlo en el documento. | 5 |
| E2-14 | Revisar la comparativa de plugins: tres alternativas por tipo, incluidos los obligatorios, y añadir las filas de los plugins nuevos. Datos en `docs/entrega/datos/plugins.json`. | — |
| E2-15 | Revisar el REM tras la entrevista y regenerar `CADUS.rem` con `scripts/remus/build_rem.ps1`. | — |
| E2-16 | Preguntas frecuentes y textos legales (consentimiento RGPD, aviso de privacidad) con el contenido real. | — |

**Capacidad total comprometida del Sprint:** 29 SP, más las tareas de documentación `E2-xx`.

## Tareas de todo el equipo

| ID | Tarea | Cuándo |
|---|---|---|
| T-01 | Cada uno prueba la historia de otra persona (prueba cruzada) y anota los fallos como issues. | 22–23/10 |
| T-02 | Cada uno hace las capturas de lo suyo en alta resolución (1920×1080) y escribe el pie y la explicación con los códigos RF/HU. | 22–23/10 |
| T-03 | Cada uno añade la fila del plugin que instala (versión, instalaciones, valoración, última actualización y decisión). | al instalarlo |
| T-04 | Marcar su tarea en GitHub Projects al terminarla; el burndown se calcula de ahí. | cada día |

## Calendario

| Fecha | Hito |
|---|---|
| Lun 19/10 | Sprint Planning; Miguel Ángel contacta con el CADUS (entrevista y lista de usuarios) |
| Mar 20/10 | Decisión SupportCandy o módulo propio (HU-09); plugins instalados |
| Mié 21/10 | HU-10 terminada (calendario) y HU-11 en marcha |
| Jue 22/10 | **Congelación de funcionalidad**; empiezan las pruebas cruzadas y las capturas |
| Vie 23/10 | Contenido real cargado, comparativas y mockups terminados |
| Sáb 24/10 | Documento montado, revisión y volcado de la BD |
| Dom 25/10 | **Entrega 2** (Word y PDF, `CADUS.rem`, volcado) y Sprint Review |

## Definición de Hecho (DoD) — Sprint 2

- [x] HU-09 a HU-12 y HU-19 implementadas y probadas (las pruebas por rol de HU-19c y de la mediación, documentadas por Álvaro, están fusionadas en `main` con las PR #32 y #33).
- [ ] Contenido de ejemplo sustituido por contenido real validado con el cliente: pendiente de que el CADUS entregue los textos (ver `docs/cliente/noticias-reales.md`).
- [ ] Cuentas del portal: el cliente decidió una cuenta única del CADUS (`cadus`, dcadus@us.es, usada por toda la Ejecutiva, que da acceso a los delegados) y una cuenta por delegado con su correo de alumno. La cuenta del CADUS está creada; las de los delegados se crean con `scripts/roles/aplicar_usuarios.php` cuando el CADUS facilite la lista.
- [x] Comparativa de cinco temas (`docs/entrega/comparativa-temas.md`) y de plugins por tipo con los obligatorios (`docs/entrega/datos/plugins.json`).
- [ ] Mockups finales en Figma con descripción: pendientes (se entregan los mockups del Sprint 1 y capturas de la web final).
- [ ] Burndown del Sprint 2 actualizado **cada día** y sin saltos de última hora. **No se cumplió**: el burndown se reconstruyó al final con las fechas reales de Git (ver la retrospectiva).
- [x] Trazabilidad REM ↔ análisis ↔ diseño ↔ implementación en el documento de la entrega (sección 7).
- [ ] Volcado `bd_cadus_v1_sprint2.sql` revisado y subido (al cerrar la entrega).
- [ ] Sin secretos, credenciales ni datos personales reales en el repositorio.

## Fuera del alcance de este Sprint

HU-14 (móvil), HU-15 (accesibilidad WCAG), HU-16, HU-17 y HU-20 están planificadas para los Sprints 3 y 4 (ver el [Product Backlog](../backlog/product-backlog.md)).

## Riesgos

| Riesgo | Medida |
|---|---|
| El trabajo se deja para el último día, como en el Sprint 1. | Congelación el jueves y burndown diario. |
| HU-11 depende de HU-10. | Terminar el calendario el miércoles; si se retrasa, HU-11 se entrega con enlace manual a la asamblea. |
| El CADUS tarda en dar contenido real o validar. | Miguel Ángel lo pide el lunes; si no llega a tiempo, se entrega con contenido de ejemplo marcado y la validación como pendiente. |
| Todo el contacto con el cliente pasa por una sola persona. | Miguel Ángel resume cada reunión en Discord (#scrum) y Pablo, como Product Owner, valida las prioridades. |
| Dos personas editan el mismo archivo del plugin propio. | Pull antes de empezar, commits pequeños y cada uno trabaja en su archivo (`includes/`). |

## Resultado del Sprint 2

- **Completado:** 29 de 29 SP. Las cinco historias están integradas en `main` (la documentación de las pruebas de HU-19c y HU-12 entró con las PR #32 y #33 el 25/10) y pasan las pruebas automáticas (privacidad de tickets y mediaciones, 0 fallos).

| Historia | SP | Quién | Fecha de cierre | Qué se entregó |
|---|---:|---|---|---|
| HU-19a · HU-09b | 6 | Pablo (con Claude y Codex) | 19/10 | Menús de administración por rol, rol «Ejecutivo del CADUS» sin comentarios y privacidad de los tickets (RN-03) |
| HU-19b | 3 | Miguel Ángel | 23/10 | Panel de inicio con accesos rápidos según el rol |
| HU-10 | 3 | Miguel Ángel | 23/10 | Calendario de asambleas y eventos con The Events Calendar |
| HU-12 | 5 | Álvaro (integrada por Pablo) | 23/10 | Solicitud de mediación estudiantil, privada y con la protección RN-03 |
| HU-09a | 5 | Marcos | 24/10 | Filtros de tickets, aviso al estudiante por correo sin contenido, FAQ y aviso de privacidad |
| HU-11 | 5 | Joaquín | 24/10 | Convocatorias de votación vinculadas a una asamblea (RN-05) |
| HU-19c | 2 | Álvaro | 24/10 | Plan y ejecución de pruebas por rol (PR #32, fusionada el 25/10) |

- **Decisiones del sprint:** se amplió el módulo propio del buzón en lugar de instalar SupportCandy (HU-09); las votaciones publican convocatorias y la emisión del voto (papeleta con YOP Poll, no instalado) pasa a la historia HU-21 del Sprint 3, un cambio de alcance pendiente de validar con el CADUS; el cliente decidió una **cuenta única del CADUS** (dcadus@us.es, para toda la Ejecutiva, que da acceso a los delegados) y una cuenta por delegado con su correo de alumno.
- **Extras no planificados:** portada y páginas interiores rediseñadas con la identidad de cadus.us.es (logotipo y paleta oficiales), pie global de contacto, bateria de pruebas de privacidad, GitHub Project «CADUS · Scrum».

## Sprint Review (24/10/2026)

Se revisó el incremento sobre el servidor compartido:

1. **Portada:** presentación del 40 aniversario, accesos, noticias con filtros por categoría, eventos del calendario, «Nuestro trabajo», galería, buscador, pasos del buzón y cierre con los datos de contacto.
2. **Participación:** calendario de eventos, convocatorias de votación y solicitud de mediación.
3. **Atención al estudiante:** buzón con código de seguimiento largo y aleatorio, panel de tickets con filtros y aviso al estudiante, FAQ y aviso de privacidad.
4. **Administración:** menús por rol, panel de inicio y cuentas (la del CADUS creada; las de los delegados, con el script).

**Pendiente de validar con el cliente (a través de Miguel Ángel):** textos reales de noticias, actas y delegaciones; los objetivos de «Nuestro trabajo» (proceden de la web oficial y son de 2024); y la lista de cuentas de delegación.

## Retrospectiva

**Qué ha ido bien**
- La arquitectura por módulos del plugin permitió trabajar en paralelo: calendario, mediación, votaciones y buzón se integraron sin tocarse entre sí (filtros `cadus_menus_admin` y `cadus_barra_nuevos`).
- La **revisión cruzada** entre Claude y Codex encontró fallos reales antes de entregar (contrastes ilegibles, permisos que se perdían, el autor «root» visible en las fichas) y las baterías de pruebas de privacidad se ampliaron con cada módulo.
- GitHub Project como fuente única del backlog, con campos de SP, sprint y fecha de cierre.

**Qué ha ido mal**
- **Se repitió la lección del Sprint 1: el trabajo se concentró al final.** El 79 % de los puntos (23 de 29) se cerró el 23 y el 24 de octubre. El burndown no se actualizó cada día, como se había acordado, y hubo que reconstruirlo con el historial de Git.
- Una rama (la de mediación) se hizo sobre una copia antigua del plugin y habría eliminado la portada, los menús por rol y el diseño al fusionarse. Se evitó integrando solo su módulo.
- Varios entregables de documentación (mockups en Figma, entrevista con el cliente, contenido real) no estaban listos al cerrar el sprint.

**Acciones para el próximo sprint**
1. Actualizar el tablero y el burndown **cada día** (5 minutos en la daily); no cerrar historias «de golpe».
2. Trabajar siempre desde `git pull` de `main` y abrir una pull request pequeña por historia; nunca copiar carpetas de otro equipo.
3. Pedir al cliente los contenidos reales al **inicio** del sprint, no al final.
4. Mantener la batería de pruebas de privacidad como requisito de cierre de cualquier historia que toque datos de estudiantes.
