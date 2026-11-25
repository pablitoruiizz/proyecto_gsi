# Product backlog · Red Social Interna del CADUS (Teams)

> **Herramienta de seguimiento:** este archivo y los de la misma carpeta (`docs/redsocial/scrum/`), independientes del CMS y del DMS. Escala Fibonacci (1, 2, 3, 5, 8).
> **Cómo se estimó:** los puntos los estimó Pablo, con Claude, el 22/11/2026 al cerrar el sprint, **a posteriori**: el sprint no se planificó con puntos el 16/11. Sirven para el burndown y para repartir el sprint siguiente, no como estimación previa del equipo.
> **Equipo:** cuatro personas desde el 16/11/2026 (Pablo, Joaquín, Álvaro y Marcos).

| ID | Historia | Requisitos | SP | Estado a 22/11 | Sprint | Responsable |
|---|---|---|---:|---|---|---|
| RSI-HU-01 | Como equipo, queremos un caso de negocio y un REM de la red social para saber qué se construye y por qué Teams. | OBJ-R01 a OBJ-R05, RC-R01 a RC-R03 | 3 | Hecho en `main` (20/11); falta la revisión de otra persona | Sprint 1 | Pablo |
| RSI-HU-02 | Como equipo, queremos un UML de análisis y otro de diseño para pasar de los conceptos del Lab 5 a Teams. | RF-R01, RF-R06, IR-R01 a IR-R05 | 3 | Hecho: borrador de Pablo (20/11) y revisión de Álvaro en `main` (22/11, PR #89) | Sprint 1 | Álvaro (borrador de Pablo) |
| RSI-HU-03 | Como Ejecutiva, quiero un equipo privado por grupo principal (Ejecutiva, Delegaciones y Asamblea) con propietarios y miembros. | RF-R01, RF-R02, RF-R04, RF-R06, RN-R05 | 3 | Hecho (equipos creados el 16/11; cuatro propietarios el 20/11); capturas 01 y 02 | Sprint 1 | Pablo |
| RSI-HU-04 | Como Ejecutiva, quiero un canal de avisos donde solo yo publique y un canal privado por delegación para que cada una vea solo lo suyo. | RF-R03, RF-R05, RN-R01, RN-R02, CU-R01, CU-R04, CU-R05 | 5 | Hecho en `main` el 22/11 (configuración de Marcos del 21/11, capturas 03 a 05, 05b, 05c, 10 y 11); aislamiento probado con una cuenta Miembro (Álvaro, 22/11) | Sprint 1 | Marcos |
| RSI-HU-05 | Como Ejecutiva y delegación, queremos calendario, tareas, formularios y enlace al DMS dentro de Teams. | RF-R07 a RF-R10, RN-R03, CU-R02, CU-R03 | 5 | Hecho en `main` el 22/11: Planner, Forms y pestaña del DMS (Joaquín, capturas 07 a 09) y calendario (Marcos, captura 06); solo el plan de la Asamblea tiene captura | Sprint 1 | Joaquín (calendario: Marcos) |
| RSI-HU-06 | Como equipo, queremos el documento de la entrega, el REM exportado y el zip con la lista del profesor. | Todos | 3 | Hecho en `main` el 22/11 con el commit de cierre (documento con el índice del Lab 5, PDF del REM y zip con la lista del profesor); el envío del zip se hace esa noche | Sprint 1 | Pablo |
| RSI-HU-07 | Como Ejecutiva, quiero avisos automáticos cuando se asigna una tarea o vence su fecha. | RF-R11, RC-R02 | 3 | Pendiente (Lab 8) | Sprint 2 | Joaquín |
| RSI-HU-08 | Como Ejecutiva, quiero una aplicación sencilla con la lista de delegaciones y su estado, si el tenant lo permite. | RF-R12, RC-R02 | 3 | Pendiente (Lab 8); no se ha comprobado que el tenant ofrezca PowerApps | Sprint 2 | Álvaro |
| RSI-HU-09 | Como Ejecutiva y delegación, queremos que cada tablero de Planner siga un patrón de diseño explícito, para entender cada plan sin explicación (Lab 6). | RF-R09, RNF-R02 | 2 | Pendiente: análisis redactado (`docs/redsocial/diseno-tableros-planner.md`); falta decidir si el plan de la asamblea pasa a «Proceso de tareas», rehacerlo en Planner con su captura y reflejarlo en el UML | Sprint 2 | Joaquín |

**Total del Sprint 1: 22 SP.** Sprint 2 (23/11 a 29/11): 8 SP más lo que quede del Sprint 1.

## Definición de hecho (red social)

1. El entregable está en `main`.
2. Si es de Teams, tiene captura explicada en `docs/redsocial/capturas/` con los requisitos que demuestra.
3. Lo ha revisado o probado otra persona y queda anotado. Solo se cumple del todo en RSI-HU-02 (revisión de Álvaro) y en RSI-HU-04 (Joaquín probó que solo ve su canal y Álvaro, con una cuenta Miembro, que no publica en «Avisos» ni ve los canales ajenos; `docs/redsocial/pruebas.md`); en el resto, no. Se dice en el documento de la entrega.

## Reglas mínimas

- Priorizar por valor para la entrega y por dependencia entre historias.
- Cada historia con su responsable y su estado actualizado en la review.
- Nadie da por hecho lo que escribió: lo prueba otra persona.
