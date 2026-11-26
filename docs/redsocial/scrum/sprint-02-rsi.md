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

| Tarea | Historia | Qué incluye | Quién | Estado a 26/11 |
|---|---|---|---|---|
| R-11 | — | REM actualizado con los requisitos de automatización | Pablo | Hecho: REM 1.1 con RF-R13 (Planner) y glosario; falta exportar el PDF desde REMUS |
| R-12a | RSI-HU-07 | Flujo «Aviso de tarea nueva» (Planner a Teams) con capturas | Joaquín | Hecho el 25/11: flujo creado y capturas 12a y 12b |
| R-12b | RSI-HU-07 | Flujo «Aviso de tareas que vencen» (programado cada día) con capturas | Joaquín | Hecho el 25/11: flujo creado y capturas 12c y 12d |
| R-12c | RSI-HU-07 | Prueba de los flujos por otra persona (Lab 8) | Marcos | Hecho el 25/11: los dos flujos probados con su cuenta (capturas 12e a 12l, `pruebas.md`) |
| R-13 | RSI-HU-08 | Aplicación de PowerApps «Estado de las delegaciones», o la alternativa documentada si el tenant no la permite | Álvaro | Hecho: aplicación guardada, ejecutada y compartida; probada por Marcos el 25/11 (capturas R13-01 a R13-07) |
| R-06c | RSI-HU-09 | Decidir el patrón del plan de la asamblea y rehacerlo en Planner con su captura | Joaquín | Hecho el 25/11: plan rehecho con cuatro cubos, captura `08-planner.jpg` repetida y prueba de Marcos el 26/11 |
| R-14a | RSI-HU-09 | UML de diseño con los cubos nuevos del plan de la asamblea | Álvaro | Hecho el 26/11: `uml-rsi-diseno.png` con el patrón de cada plan (PR #100) |
| R-14b | — | Capturas explicadas y documento de la entrega | Pablo | En curso: documento y zip final del sábado 28/11 |
| R-14c | — | SCRUM del sprint: planning, burndown diario y review | Joaquín | Hecho salvo la retrospectiva en grupo: planning, burndown al día y review (borrador del 26/11) |
| R-10b | — | Pruebas cruzadas y revisión con Codex | Todos | En curso: pruebas de Marcos hechas; falta la revisión final con Codex |

## Heredado del Sprint 1

| Pendiente | Quién |
|---|---|
| Revisión de otra persona del caso de negocio (RSI-HU-01) | Hecha por Álvaro el 26/11 (`pruebas.md`) |
| Solo el plan de la Asamblea tiene captura (`08-planner.jpg`); los de Ejecutiva y Delegaciones no | Joaquín: sin capturar; se entrega con la captura del plan de la asamblea y se dice en el documento |
| Prueba cruzada humana de las historias de Teams: solo se probó el aislamiento de canales | Marcos probó los flujos, la aplicación y el plan nuevo; las historias de Teams del Sprint 1 siguen sin prueba cruzada |

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
| 25/11 | Capturas de los dos flujos (Joaquín) y plan de la asamblea rehecho con su captura; Marcos prueba los flujos y la aplicación de Álvaro. Pendiente: 8 SP (aún no estaban en `main`) |
| 26/11 | Pruebas de Marcos y UML de diseño de Álvaro en `main`: RSI-HU-07, 08 y 09 cerradas según la DoD. Pendiente: 0 SP |

## Sprint Review y retrospectiva (borrador del 26/11/2026)

> Redactada por Pablo, con Claude, a partir de los datos del sprint (commits, burndown y pruebas). No sale de una reunión del equipo: si el equipo la hace el 28 o el 29/11, se añaden aquí sus conclusiones.

### Review

- **Entregado (8 SP, el 26/11):** RSI-HU-07 (dos flujos de Power Automate, con los avisos de tarea nueva y de tareas que vencen), RSI-HU-08 (aplicación de PowerApps «Estado de las delegaciones», probada con otra cuenta) y RSI-HU-09 (plan de la asamblea como Proceso de tareas, con UML de diseño). Las tres, en `main`, con capturas explicadas y probadas por Marcos.
- **Lo que no cubre:** la aplicación solo se probó con lectura (no se creó, editó ni borró nada) y no desde la pestaña de Teams; los planes de la Ejecutiva y de las delegaciones no tienen captura; las historias de Teams del Sprint 1 siguen sin prueba cruzada humana.
- **Calidad:** primera vez en el proyecto que cada historia tiene una prueba de otra persona antes de cerrarse (Marcos).

### Retrospectiva

| Qué fue bien | Qué no | Qué cambiamos |
|---|---|---|
| Se cerró cada historia con la prueba de otra persona y las capturas en `main` | Las pruebas de Marcos llegaron a `main` el 26/11 y las historias no se cerraron hasta ese día, pese a estar hechas el 25/11 | Subir las pruebas a `main` el mismo día en que se hacen |
| El burndown se actualizó con el script desde el primer día | Pablo y Marcos no tenían puntos y trabajaron en la integración y las pruebas, que el backlog no refleja | Dar puntos a las pruebas cruzadas y al documento en el próximo sprint |
| Los cubos del plan de la asamblea se rehicieron sobre el mismo plan y los flujos siguieron funcionando | Dos tareas del plan quedaron con un error de escritura y los planes de la Ejecutiva y las delegaciones, sin captura | Capturar los tres planes cuando se rehaga uno |
