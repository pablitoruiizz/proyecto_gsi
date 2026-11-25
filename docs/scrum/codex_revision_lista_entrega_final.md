# Revisión del análisis de la lista de la entrega final (25/11/2026)

Revisión de SOLO LECTURA: no edites archivos, no hagas commit ni push, no cambies nada en GitHub, Teams ni en el WordPress, y no toques `cms-wordpress/.htaccess` ni los `.sql`. No leas ni cites `tests/cuentas-de-prueba-local.md`. Responde en español, con hallazgos por gravedad (alta, media, baja), cada uno con archivo y línea, y al final di qué falta o no tiene dueño.

## Qué se pide

El profesor pide un único zip con tres bloques (lista literal resumida):

- **CMS:** propuesta de temática o empresa (versión definitiva); comparativa y justificación de hosting de WordPress, software de comunicación, software de SCRUM y control de versiones (se vuelve a adjuntar lo mismo si no ha cambiado); product backlog; sprint backlog del sprint de estas semanas; burndown chart solo de ese sprint; REM; análisis (UML de la estructura web); diseño (UML de plugins, tabla comparativa de plugins con métricas incluyendo los obligatorios, mockups con mínimo 3 temáticas); implementación (capturas).
- **DMS:** REM; nuevos UML de análisis y de diseño; documentos de casos de uso (3 o 4 documentos distintos y mínimo uno con más de un caso de uso); nuevos documentos de implementación (SharePoint).
- **RSI:** REM (revisar el índice del Lab 5); caso de negocio; requisitos del sistema software; glosario de términos; nuevo UML de análisis; nuevo UML de diseño; implementación explicada de Teams con capturas; **«añadir las modificaciones del Planner en todos los puntos del RSI (revisar Lab 6)»**.

Entrega: domingo 29/11/2026 a las 23:59. El Lab 6 (`Lab 6 - Red Social Interna - Planner Patterns.pdf`, en la raíz del repositorio) explica los patrones de diseño de tableros: cinco preguntas (qué gestionar, nivel, criterio de clasificación, precedencia semántica y flujo de tarjetas) y un catálogo de patrones, entre ellos «Ciclo de vida de tareas» y «Proceso de tareas».

## Mi análisis (compruébalo contra el repositorio y contra `docs/dms/entrega/paquete/Entrega-22-11-CADUS-CMS-DMS-RSI.zip`)

### CMS: cubierto

El zip del 22/11 lleva `CMS/Entrega2-CMS-CADUS.docx` y `.pdf` (propuesta, comparativas 2.2.1 a 2.2.4, product backlog, sprint backlog y burndown del Sprint 2, REM, estructura del sitio, UML de plugins, comparativa de plugins con métricas, mockups y tres temáticas, capturas), la adenda `Adenda-CMS-Sprint3` (product backlog, sprint backlog y burndown del Sprint 3, con la gráfica incrustada como imagen), `REM-CADUS-v2.3.pdf`, `CADUS.rem` y `seguimiento/`. El documento de la entrega 2 todavía dice «Planificado» para el Sprint 3 y «Pendiente» para HU-14 a HU-17; `ACTUALIZACION-22-11-estado-del-cms.md` lo corrige. Lo que falta o puede mejorarse: E3-06 (documento final del CMS, de Pablo) y capturas del portal con el contenido real nuevo (noticias, actas, normativa, calendario), que nadie tiene asignadas.

### DMS: cubierto sin cambios previstos

4 documentos de casos de uso con 8 casos (`DMS/4-Casos-de-uso`), REM 1.1 con 8 casos, UML de análisis y de diseño, 19 archivos de implementación. Pendiente sin dueño: solo CU-D01 tiene prueba hecha por otra persona.

### RSI: el hueco principal es el Planner

Todos los puntos del RSI deben reflejar el cambio de Planner (Lab 6). Cuántas veces aparecen hoy «patrón», «Proceso de tareas», «Ciclo de vida» o «Task Process» en cada artefacto: `scripts/remus/rsi_data.json` (REM), 0; `docs/redsocial/business-case.md`, 0; `docs/redsocial/glosario.md`, 0; `scripts/redsocial/diagramas_rsi.py` (UML), 0; `scripts/redsocial/build_doc_rsi.py` (documento), 0; `docs/redsocial/pruebas.md`, 0 y ni siquiera nombra Planner. Solo `docs/redsocial/configuracion-planner.md` y `docs/redsocial/diseno-tableros-planner.md` lo recogen. La decisión (Joaquín, 24/11): el plan «Preparación de la asamblea» pasa a «Proceso de tareas»; aún no se ha rehecho en Planner ni capturado.

| Punto de la lista RSI | Qué hay que cambiar por Planner | Dueño actual |
|---|---|---|
| REM (índice Lab 5) y requisitos del sistema software | Actualizar RF-R09 (planes de tareas) con el patrón de cada plan y, si procede, un requisito nuevo; subir la versión y exportar el PDF desde REMUS | R-11 de Pablo, pero su descripción solo habla de requisitos de automatización |
| Caso de negocio | Mencionar que cada tablero sigue un patrón | Nadie |
| Glosario de términos | Términos nuevos: tablero, cubo, patrón de diseño, Ciclo de vida de tareas, Proceso de tareas | Nadie |
| UML de análisis | Reflejar el patrón del plan | Nadie (R-14a de Álvaro es solo de diseño) |
| UML de diseño | Cubos nuevos del plan de la asamblea | Álvaro (R-14a), depende de R-06c |
| Implementación de Teams con capturas | Rehacer el plan de la asamblea con sus cubos nuevos y repetir `08-planner.jpg`; capturas de los planes de Ejecutiva y Delegaciones | Joaquín (R-06c) y Pablo (R-14b) |
| Pruebas | Probar el plan nuevo (otra persona) | Marcos (R-12c) |

### Otros huecos sin dueño que he visto

- Capturas del portal con contenido real (CMS).
- Revisión por otra persona del caso de negocio (RSI-HU-01, «por asignar» en `docs/redsocial/scrum/sprint-02-rsi.md`).
- Pruebas cruzadas de los casos de uso del DMS distintos de CU-D01.
- Revisión con Codex del zip final y comprobación final del zip (R-10b figura como «Todos»).
- `LEEME.md` del zip y la lista `CMS` de `scripts/dms/empaquetar_dms.py`, que no incluyen aún el documento final del CMS ni el volcado.

## Qué te pido

1. Comprueba cada afirmación de arriba contra el repositorio y el zip (por ejemplo, los recuentos de «patrón» y el contenido del zip). Dime las que sean falsas.
2. Recorre la lista del profesor punto por punto y dime si he pasado por alto algún entregable que falte o esté mal cubierto, en CMS, DMS o RSI.
3. Mira `docs/scrum/plan-23-11.md` y `docs/redsocial/scrum/sprint-02-rsi.md`: ¿hay algún punto de la lista que no figure asignado a nadie y que yo no haya listado?
4. Mira si hay contradicciones entre la lista del profesor y lo que prevé el empaquetador (`scripts/dms/empaquetar_dms.py` con `--con-rsi --final`).
