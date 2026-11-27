# Red Social Interna (Lab 5, MS Teams) · plan de trabajo

> **Nota del 22/11/2026:** este es el plan inicial del 16/11 y está superado en varios puntos: el caso de negocio sí tiene estructura en el Lab 5 (diapositiva 11) y se rehízo con ella; la separación en tres equipos ya no se justifica por un límite de canales (no comprobado) sino por separación de miembros, permisos y herramientas; y los UML están revisados. El estado vigente está en `scrum/` y en `entrega/Entrega-RSI-CADUS.docx`.

Equipo de 4 desde el 16/11/2026: Pablo (Product Owner), Joaquín (Scrum Master), Álvaro y Marcos. Miguel Ángel ya no participa y no se cuenta en el reparto.

## Fechas (calendario de la asignatura; las entregas son el domingo a las 23:59)

| Fecha | Clase | Entrega |
|---|---|---|
| 16/11 | Laboratorio 7: configuración de cada grupo (I), estructura de Teams y Planner | 22/11: Red Social Interna + REM + SCRUM review |
| 23/11 | Laboratorio 8: configuración (II), Power Automate y PowerApps | 29/11: Red Social Interna + REM + SCRUM review |
| 30/11 | Laboratorio 9: repaso de trabajos | — |
| 07/12 → **29/11** | — | Entrega FINAL de todos los sistemas (cambiada el 23/11: pasa al domingo 29/11, junto con la versión 2 de la red social) |
| 14/12 | Examen de prácticas | — |

## Qué pide el Lab 5

Business Case (con la estructura vista en clase) · grupos principales y piloto · REM (Business Case, grupos y herramientas) · análisis: clases con `<<Role>>`, `<<Group>>`/`<<Subgroups>>`, `<<Tool>>` y `<<Permission>>` · diseño: el mismo diagrama pasado a conceptos de Microsoft Teams · implementación: capturas explicadas · SCRUM.

## Entrega del 22/11 (Teams + Planner)

| ID | Tarea | Quién | Depende de |
|---|---|---|---|
| R-01 | Business Case (borrador hecho el 16/11 en `business-case.md`; falta revisión de otra persona) | Pablo | — |
| R-02 | REM en REMUS: actores, roles, grupos y subgrupos, herramientas y permisos. **Hecho el 16/11** (scripts/remus/rsi_data.json, docs/redsocial/rem-remus/RSI.rem: 12 RF, 5 CU, 5 RN) | Pablo | R-01 |
| R-03 | UML de análisis con los estereotipos de la diapositiva 13. **Borrador hecho el 16/11** (docs/redsocial/img/uml-rsi-analisis.png); falta que Álvaro lo revise | Álvaro | R-02 |
| R-04 | UML de diseño: del análisis a equipos, canales, roles de Teams y planes de Planner. **Borrador hecho el 16/11** (uml-rsi-diseno.png): tres equipos, no uno, por el límite de canales privados; falta que Álvaro lo revise | Álvaro | R-03 |
| R-05 | Crear y configurar los equipos y los grupos en Teams (el piloto). **Creados el 16/11** los tres equipos privados (Ejecutiva, Delegaciones y Asamblea) con Pablo, Marcos, Joaquín y Álvaro como propietarios (invitados como miembros el 16/11 y pasados a propietarios el 20/11). Falta la configuración de canales, moderación y canales privados: guía en `configuracion-teams.md` | Pablo (crea) y Marcos (configura y prueba) | R-04 |
| R-06 | Planner: un plan por grupo con sus buckets y tareas | Joaquín | R-05 |
| R-07 | Capturas explicadas de Teams y Planner | Marcos | R-05, R-06 |
| R-08 | Seguimiento SCRUM: backlog, sprint y burndown de la red social | Joaquín | — |
| R-09 | Documento principal, empaquetado y zip (se reutilizan `build_doc_dms.py` y `empaquetar_dms.py`) | Pablo | R-01 a R-08 |
| R-10 | Prueba cruzada: cada uno prueba lo que no escribió, y revisión con Codex | Todos | R-09 |

## Entrega del 29/11 (Power Automate y PowerApps)

| ID | Tarea | Quién |
|---|---|---|
| R-11 | Requisitos de automatización (REM actualizado) | Pablo |
| R-12 | Flujos de Power Automate (por ejemplo, avisos de tareas y de nuevos documentos) | Joaquín y Marcos |
| R-13 | Aplicación de PowerApps, si el tenant la ofrece | Álvaro |
| R-14 | UML, capturas y documento actualizados; SCRUM del sprint | Álvaro y Joaquín |

## Reglas del equipo

- Un único editor por archivo compartido; el resto pide los cambios.
- Nadie prueba lo que escribió.
- Lo que no esté probado por otra persona se dice en el documento.
- Lo que cambia permisos o miembros en el tenant de la Universidad lo hace cada persona con su cuenta, y la creación de equipos la hace Pablo.

## Pendiente de aclarar

1. ~~La estructura del Business Case de clase~~: en clase solo se dio el esquema de la pizarra (SCRUM review; REM con Business Case y requisitos de herramienta; UML de análisis y de diseño; implementación). No hay estructura de Business Case: se usa una estándar de siete apartados en `business-case.md`, que se reordenará si el profesor indica otra.
2. Qué grupos son «los principales» para el piloto. Propuesta de partida: Ejecutiva, Delegaciones (con un subgrupo por centro) y Asamblea; herramientas: archivos, calendario, Planner y Forms.
3. ~~Si el tenant ofrece Power Automate y PowerApps (se comprueba antes del Lab 8).~~ Respondido el 25/11/2026: sí. Joaquín creó dos flujos de Power Automate y Álvaro una aplicación de Power Apps, y Marcos los probó con su cuenta (`pruebas.md`); la aplicación no está publicada y la ejecución programada del segundo flujo no se ha observado.
