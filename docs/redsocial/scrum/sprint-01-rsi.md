# Sprint 1 de la red social · estructura de Teams y Planner

**Periodo:** 16/11/2026 – 22/11/2026 (entrega el domingo 22/11 a las 23:59)
**Compromiso:** RSI-HU-01 a RSI-HU-06 (22 SP). Sprint Review y retrospectiva: [`review-sprint-01-rsi.md`](review-sprint-01-rsi.md). Burndown: [`burndown-sprint-01-rsi.csv`](burndown-sprint-01-rsi.csv).

## Objetivo

Entregar el caso de negocio, el REM, el UML de análisis y de diseño y la estructura de la red social en Teams (equipos, canales, roles, Planner y formularios), con capturas explicadas y el documento de la entrega.

## Reparto de puntos

| Integrante | Rol | Historias | SP |
|---|---|---|---:|
| Pablo | Product Owner | RSI-HU-01, RSI-HU-03, RSI-HU-06 | 9 |
| Joaquín | Scrum Master | RSI-HU-05 | 5 |
| Álvaro | Desarrollo | RSI-HU-02 | 3 |
| Marcos | Desarrollo | RSI-HU-04 | 5 |
| **Total** | | | **22** |

El reparto no es equilibrado (9 frente a 3): Pablo concentra el caso de negocio, el REM, la creación de los equipos y el documento. Es un punto de la retrospectiva.

## Sprint backlog

| Tarea | Historia | Qué incluye | Quién | Estado a 22/11 |
|---|---|---|---|---|
| R-01 | RSI-HU-01 | Caso de negocio (`docs/redsocial/business-case.md`) | Pablo | Hecho con el índice del Lab 5; falta revisión de otra persona |
| R-02 | RSI-HU-01 | REM en REMUS (`RSI.rem`, 12 RF, 5 CU, 5 RN) y glosario | Pablo | Hecho; falta exportarlo a PDF |
| R-03 | RSI-HU-02 | UML de análisis | Álvaro | Hecho: borrador de Pablo y revisión de Álvaro (22/11) |
| R-04 | RSI-HU-02 | UML de diseño a Teams (tres equipos) | Álvaro | Hecho: revisado por Álvaro, con los tres planes de Planner |
| R-05a | RSI-HU-03 | Crear los tres equipos privados y pasar a los cuatro a propietarios | Pablo | Hecho (16/11 y 20/11) |
| R-05b | RSI-HU-04 | Moderación del canal de avisos y tres canales privados de ejemplo | Marcos | Hecho el 21/11 (en `main` el 22/11) |
| R-06 | RSI-HU-05 | Planes de Planner, formulario de Forms y pestaña del DMS | Joaquín | Hecho (pestañas de Planner de los tres equipos; Forms y DMS en la Asamblea) |
| R-06b | RSI-HU-05 | Calendario del canal con el evento de ejemplo (captura 06) | Marcos | Hecho (evento «Asamblea Noviembre», 26/11) |
| R-07 | RSI-HU-03 a 05 | Capturas explicadas | Pablo, Joaquín, Marcos | Hecho: 01 a 11 |
| R-08 | — | Seguimiento SCRUM de la red social | Pablo (con Claude) | Hecho el 22/11 |
| R-09 | RSI-HU-06 | Documento principal, REM en PDF y zip | Pablo | En curso |
| R-10 | — | Prueba cruzada y revisión con Codex | Todos | Revisión con Codex hecha y corregida el 22/11; prueba cruzada humana parcial (Álvaro revisó los UML, Joaquín probó el aislamiento de canales) |

## Definición de hecho

Ver [`product-backlog-rsi.md`](product-backlog-rsi.md): entregable en `main`, captura explicada y revisión de otra persona anotada. El tercer punto solo se cumple del todo en RSI-HU-02.

## Riesgos

| Riesgo | Medida |
|---|---|
| Se trabajó a ráfagas (commits el 20/11 y el 22/11) y los puntos quedaron concentrados al final | Daily en Discord y actualizar el burndown cada día en el Sprint 2 |
| Miguel Ángel dejó el trabajo el 16/11 y era el contacto con el CADUS | Las decisiones sobre el CADUS se marcan «por confirmar» |
| Los cuatro integrantes son propietarios de los tres equipos: no hay una cuenta «solo miembro» para probar el aislamiento entre delegaciones | Usar una cuenta de ejemplo o bajar temporalmente a un integrante a miembro durante la prueba |
| El tenant puede no ofrecer Power Automate o PowerApps (Lab 8) | Comprobarlo el 23/11 y documentar el mensaje del tenant |
| El límite de canales privados por equipo no está comprobado en el tenant | Comprobarlo al crear el tercer canal privado |
