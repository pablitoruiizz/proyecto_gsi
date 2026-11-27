# Entrega final del proyecto GSI — CADUS (CMS + DMS + red social v2)

Entrega del domingo 29/11/2026. Los documentos describen el estado a 26/11/2026. Quedan **pendientes**, y así constan en ellos: la retrospectiva en grupo del Sprint 3, algunas pruebas cruzadas (HU-14b y HU-16a de Joaquín, HU-22 de Álvaro), los casos T1 a T3 y P5 de las pruebas de aceptación (parciales) y la prueba con NVDA.

Equipo de la entrega: Pablo Ruiz Vidal (Product Owner), Joaquín Luna Canela (Scrum Master), Álvaro Martínez Ocaña y Marcos-Paban Delgado Rodríguez. Miguel Ángel Camacho Martín, miembro del CADUS, colaboró en el DMS y en el contacto con el cliente hasta el 16/11/2026.


Cambio pedido por el profesor sobre la entrega del 08/11: dividir los casos de uso por roles o secciones y añadir dos casos en cada documento. Ahora hay 4 documentos de casos de uso, uno por sección, con 2 casos cada uno (8 en total, con los nuevos CU-D07 y CU-D08), y el REM pasa a la versión 1.1.

## Entrevista con el cliente
- `Entrevista-CADUS.docx` / `.pdf`: entrevista con el CADUS (26/10/2026), de la que salen los requisitos del DMS.

## DMS (SharePoint de la Universidad de Sevilla)
- `Entrega-DMS-CADUS.docx` / `.pdf`: documento principal (requisitos, análisis, diseño, casos de uso, implementación, trazabilidad y seguimiento SCRUM).
- `1-Requisitos`: `DMS.rem` (proyecto REMUS completo, con los 8 casos), `REM-DMS-v1.1.pdf` (su exportación), hoja `carga-remus.md` y `REM-DMS.md`; en `secciones/`, un `.rem` por sección (Acta, Normativa, Expediente y Votación, con sus dos casos de uso cada uno) y su hoja legible.
- `2-Analisis`: UML de análisis y diagrama de casos de uso con los 8 casos y los roles.
- `3-Diseno`: UML de diseño (del análisis a SharePoint).
- `4-Casos-de-uso`: CU-Acta (CU-D01, CU-D02), CU-Normativa (CU-D03, CU-D07), CU-Expediente (CU-D04, CU-D05) y CU-Votacion (CU-D06, CU-D08).
- `5-Implementacion-SharePoint`: capturas del entorno real (`uses0.sharepoint.com`), explicadas en cada documento de casos de uso.
- `seguimiento`: product backlog, sprint backlog y burndown de los dos sprints del DMS.

Sitios de SharePoint: `uses0.sharepoint.com/sites/cadus-documentacion-publica`, `cadus-organos-de-gobierno`, `cadus-votaciones` y `cadus-atencion-al-estudiante`.

## CMS (portal WordPress)
- `Entrega2-CMS-CADUS.docx` / `.pdf`: documento de la entrega 2, sin cambios.
- `REM-CADUS-v2.3.pdf` y `CADUS.rem`: REM del CMS (versión 2.3) exportado desde REMUS.
- `capturas-sprint3`: capturas del Sprint 3 (relevo de la cuenta, calendario, páginas institucionales y accesibilidad) con su tabla explicativa.
- `Adenda-CMS-Sprint3.docx` / `.pdf`: cambios de requisitos tras la entrevista, backlog, sprint backlog y burndown del Sprint 3.
- `seguimiento/`: sprint backlog, burndown (csv) y product backlog en su formato original.
- `Entrega-final-CMS-CADUS.docx` / `.pdf`: **documento con el estado vigente del CMS a 26/11/2026** (backlog, Sprint 3, burndown, implementación con contenido real, pruebas y pendientes), para la entrega del 29/11/2026. Prevalece sobre `ACTUALIZACION-22-11-estado-del-cms.md` y sobre la adenda del Sprint 3 donde se contradigan.
- `capturas-final`: capturas del portal con el contenido real (noticias, actas, normativa y calendario).
- `bd_cadus_v1_sprint3.sql` y `LEEME-volcado.md`: **copia saneada** de la base de datos del portal, con tres cuentas de demostración (administración, Ejecutiva y delegación) y sin cuentas reales, sesiones, registros de Wordfence ni de estadísticas, tickets ni cuentas de prueba. El `LEEME-volcado.md` explica qué conserva, las cuentas de demostración y cómo restaurarla.
- `seguimiento/E2-12-fichas-y-edicion.md` y `revisiones/`: pruebas de las fichas de delegaciones y encargos de las revisiones con Codex del 23 y 25/11 citadas en el documento final.
- Los `.md` de seguimiento conservan algunos enlaces al repositorio de GitHub; los que no apuntan a un archivo del zip aparecen como texto con la ruta del repositorio.

## Red social interna (Microsoft Teams, Lab 5)
- `Entrega-RSI-CADUS.docx` / `.pdf`: documento principal (caso de negocio, requisitos, glosario, análisis, diseño, implementación, trazabilidad y SCRUM).
- `1-Requisitos-REM`: `RSI.rem` (proyecto REMUS), `REM-RSI-v1.1.pdf` (su exportación, con el índice propio de REMUS), hoja `carga-remus.md` y `glosario-de-terminos.md`. El índice del Lab 5 (caso de negocio, requisitos del sistema software y glosario) está en `Entrega-RSI-CADUS` y en `2-Caso-de-negocio`.
- `2-Caso-de-negocio`: `Business-Case-RSI` (Word y PDF).
- `3-Analisis-UML` y `4-Diseno-UML`: UML de análisis (Role, Group, Subgroups, Tool y Permission) y UML de diseño en Teams.
- `5-Implementacion-Teams`: capturas de Teams (tenant de la Universidad de Sevilla) y guía de configuración.
- `seguimiento`: plan y seguimiento SCRUM de la red social.
