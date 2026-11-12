# Entrega del 08/11/2026 — CADUS (CMS + DMS)

Equipo: Pablo Ruiz Vidal, Joaquín Luna Canela, Miguel Ángel Camacho Martín, Álvaro Martínez Ocaña y Marcos-Paban Delgado Rodríguez.

## Entrevista con el cliente
- `Entrevista-CADUS.docx` / `.pdf`: entrevista con el CADUS (26/10/2026), de la que salen los requisitos del DMS y los cambios del CMS.

## CMS (portal WordPress)
El proyecto es el mismo que en la entrega anterior, así que se vuelve a adjuntar el documento de la entrega 2 (propuesta de temática, comparativas de hosting, comunicación, SCRUM, control de versiones y plugins, análisis, diseño, mockups y capturas) y se añade una adenda con lo que cambia:
- `Entrega2-CMS-CADUS.docx` / `.pdf`: documento de la entrega 2, sin cambios (sus gráficos de burndown son los de los sprints anteriores; el burndown de esta entrega es el del Sprint 3, en la adenda).
- `REM-CADUS-v2.1.pdf` y `CADUS.rem`: REM del CMS (versión 2.1), exportado desde REMUS, con las respuestas de la entrevista.
- `Adenda-CMS-Sprint3.docx` / `.pdf`: cambios de requisitos tras la entrevista, product backlog actualizado, sprint backlog y burndown del Sprint 3.
- `seguimiento/`: sprint backlog, burndown (csv) y product backlog en su formato original.

## DMS (SharePoint de la Universidad de Sevilla)
- `Entrega-DMS-CADUS.docx` / `.pdf`: documento principal (requisitos, análisis, diseño, casos de uso, implementación y seguimiento SCRUM).
- `1-Requisitos`: `DMS.rem` (proyecto REMUS) y `REM-DMS-v1.0.pdf` (su exportación), hoja `carga-remus.md` y `REM-DMS.md`.
- `2-Analisis`: UML de análisis y diagrama de casos de uso.
- `3-Diseno`: UML de diseño (del análisis a SharePoint).
- `4-Casos-de-uso`: 4 documentos de casos de uso (acta y expediente con 2 casos de uso cada uno).
- `5-Implementacion-SharePoint`: capturas del entorno real (`uses0.sharepoint.com`).
- `seguimiento`: product backlog, sprint backlog y burndown del DMS (independientes de los del CMS).

Sitios de SharePoint: `uses0.sharepoint.com/sites/cadus-documentacion-publica`, `cadus-organos-de-gobierno` y `cadus-atencion-al-estudiante`.

## Estado a 12/11/2026
- **CMS:** en el Sprint 3 se han cerrado 11 de los 36 SP (HU-22 relevo de la cuenta de la delegación; HU-17a, HU-16b y HU-15b del buzón) y las tareas E3-03, E3-05, E3-07 y E3-08. Quedan 25 SP; el hito del 08/11 no se alcanzó. El despliegue en el servidor de la US (E3-09) está bloqueado porque ofrece PHP 7.2/7.3 y WordPress 7.1 necesita 7.4 o superior. Detalle en `Adenda-CMS-Sprint3`.
- **DMS:** configurado y observado con la cuenta de Pablo; las pruebas cruzadas con cuentas de delegado y de estudiante siguen pendientes.
