# Sprint 2 de la red social · automatización y patrón del tablero (Power Automate, PowerApps y Planner)

**Periodo:** 23/11/2026 – 29/11/2026 (entrega el domingo 29/11 a las 23:59, el mismo día que el CMS y el DMS)
**Compromiso:** RSI-HU-07, RSI-HU-08 y RSI-HU-09 (8 SP), más lo que quedó abierto del Sprint 1 (tabla «Heredado»). Burndown: [`burndown-sprint-02-rsi.csv`](burndown-sprint-02-rsi.csv) y su gráfica [`burndown-sprint-02-rsi.png`](burndown-sprint-02-rsi.png). Sprint Review y retrospectiva: se escriben el 29/11 con los datos finales.
**Cómo se actualiza el burndown:** cada día, con `python scripts/redsocial/scrum_rsi_sprint.py` (admite `--hecho RSI-HU-0X` y `--nota "..."`). Lee los puntos de [`product-backlog-rsi.md`](product-backlog-rsi.md).

## Objetivo

Entregar la automatización de la red social (RF-R11: avisos en el canal cuando se asigna una tarea o vence su fecha; RF-R12: aplicación sencilla con la lista de delegaciones), que cada tablero de Planner siga un patrón de diseño explícito (Lab 6) y el documento final actualizado, con capturas explicadas y probado por otra persona.

## Reparto de puntos

| Integrante | Rol | Historias | SP |
|---|---|---|---:|
| Joaquín | Scrum Master | RSI-HU-07, RSI-HU-09 | 5 |
| Álvaro | Desarrollo | RSI-HU-08 | 3 |
| Pablo | Product Owner | — | 0 |
| Marcos | Desarrollo | — | 0 |
| **Total** | | | **8** |

Pablo y Marcos no tienen historias con puntos este sprint: Pablo actualiza el REM (R-11), el documento y el zip, y Marcos prueba los flujos y la aplicación (Lab 8). Es una carga que el backlog no refleja y un punto para la retrospectiva.

## Sprint backlog

| Tarea | Historia | Qué incluye | Quién | Estado a 24/11 |
|---|---|---|---|---|
| R-11 | — | REM actualizado con los requisitos de automatización | Pablo | Pendiente |
| R-12a | RSI-HU-07 | Flujo «Aviso de tarea nueva» (Planner a Teams) con capturas | Joaquín | Pendiente: diseño y guía listos (`docs/redsocial/configuracion-power-automate.md`) |
| R-12b | RSI-HU-07 | Flujo «Aviso de tareas que vencen» (programado cada día) con capturas | Joaquín | Pendiente: diseño y guía listos |
| R-12c | RSI-HU-07 | Prueba de los flujos por otra persona (Lab 8) | Marcos | Pendiente |
| R-13 | RSI-HU-08 | Aplicación de PowerApps «Estado de las delegaciones», o la alternativa documentada si el tenant no la permite | Álvaro | Pendiente: borrador de especificación del 21/11 |
| R-06c | RSI-HU-09 | Decidir el patrón del plan de la asamblea y rehacerlo en Planner con su captura | Joaquín | Decidido: «Proceso de tareas» (`diseno-tableros-planner.md`); falta rehacerlo y capturarlo |
| R-14a | RSI-HU-09 | UML de diseño con los cubos nuevos del plan de la asamblea | Álvaro | Pendiente (depende de R-06c) |
| R-14b | — | Capturas explicadas y documento de la entrega | Pablo | Pendiente |
| R-14c | — | SCRUM del sprint: planning, burndown diario y review | Joaquín | En curso: este documento y el burndown desde el 23/11 |
| R-10b | — | Pruebas cruzadas y revisión con Codex | Todos | Pendiente |

## Heredado del Sprint 1

| Pendiente | Quién |
|---|---|
| Revisión de otra persona del caso de negocio (RSI-HU-01) | Por asignar |
| Solo el plan de la Asamblea tiene captura (`08-planner.jpg`); los de Ejecutiva y Delegaciones no | Joaquín (se recoge con RSI-HU-09) |
| Prueba cruzada humana de las historias de Teams: solo se probó el aislamiento de canales | Todos (R-10b) |

## Calendario propuesto

Es una propuesta del Scrum Master para confirmar en el planning del Lab 8; las fechas de entrega son las del plan.

| Día | Qué |
|---|---|
| Lun 23/11 (Lab 8) | Comprobar en el tenant si se puede guardar y ejecutar un flujo y una aplicación (Joaquín y Álvaro) |
| Mar 24 y mié 25/11 | Flujos (R-12a y R-12b) y rediseño del plan de la asamblea (R-06c) con sus capturas; Álvaro, la aplicación |
| Jue 26/11 | Pruebas cruzadas: Marcos los flujos y el plan; otra persona la aplicación. El evento de ejemplo de la asamblea cae ese día |
| Vie 27/11 | UML y capturas finales (Álvaro, Pablo); revisión con Codex |
| Sáb 28/11 | Documento y zip (Pablo); margen para lo que falle |
| Dom 29/11 | Entrega a las 23:59 y Sprint Review |

## Definición de hecho

Igual que en el Sprint 1 ([`product-backlog-rsi.md`](product-backlog-rsi.md)): entregable en `main`, captura explicada y revisión de otra persona anotada en `pruebas.md`. Lo que el tenant no permita se documenta con su mensaje de error y captura (RC-R02), y cuenta como contenido de la entrega; lo que no pruebe otra persona se dice como «no probado».

## Riesgos

| Riesgo | Medida |
|---|---|
| El tenant puede no permitir guardar o ejecutar flujos o aplicaciones (solo se comprobó que las páginas de creación cargan) | Comprobarlo el 23/11 y documentar el mensaje con captura; las alternativas de cada artefacto están en sus guías |
| El CMS, el DMS y la red social se entregan el mismo día (29/11) y el documento de cada uno pasa por Pablo | Cerrar la red social el viernes 27/11 y dejar el sábado de margen |
| En el Sprint 1 los puntos se cerraron al final y no hubo prueba cruzada humana | Burndown cada día con el script, cierre de una historia solo con su prueba de otra persona y un día de pruebas cruzadas (jueves 26/11) |
| Los flujos de Power Automate pertenecen a la cuenta de quien los crea: si esa cuenta deja de existir, se paran | Compartir cada flujo con Marcos como copropietario y documentarlo en `colaboracion-microsoft365/power-automate/README.md` |
| Rehacer el plan de la asamblea podría romper los flujos que lo vigilan | Se renombran los cubos del mismo plan en lugar de crear otro: su identificador no cambia |
| Sin contacto con el CADUS desde el 16/11 | Las decisiones sobre el CADUS siguen marcadas «por confirmar» |

## Seguimiento

| Fecha | Qué consta en el repositorio |
|---|---|
| 23/11 | Inicio del sprint (Lab 8). Burndown: 8 SP pendientes |
| 24/11 | Guía y diseño de los flujos de Power Automate, decisión y guía del rediseño del plan de la asamblea (RSI-HU-09), planning y script del burndown. Ninguna historia cerrada según la DoD: 8 SP pendientes |
