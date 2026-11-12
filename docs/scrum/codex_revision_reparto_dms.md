# Revisión pedida a Codex: reparto de la versión definitiva del DMS (12/11/2026)

Revisión de SOLO LECTURA (no edites archivos ni hagas commit). Responde en español, con hallazgos ordenados por gravedad (alta, media, baja), citando archivo y línea, y al final qué cambiarías.

## Contexto
Proyecto GSI (Universidad de Sevilla): portal del CADUS en WordPress (CMS) y un DMS en SharePoint (Lab 4, enunciado en `docs/Lab 4 - DMS - v2.pptx`). El profesor dijo sobre lo entregado del DMS: **«dividir los casos de uso por roles o secciones y añadir en ellos dos casos»**. La lista de lo que hay que entregar es: Requisitos (REM), nuevos documentos de análisis (UML), nuevos documentos de diseño (UML), documentos de casos de uso (3-4 documentos distintos y mínimo 1 con más de 1 CU) y documentos de implementación (SharePoint). Hoy es 12/11/2026 y el equipo (5 personas) también cierra el Sprint 3 del CMS el 15/11.

## Qué revisar
1. `docs/dms/reparto-version-definitiva.md`:
   - ¿Interpreta bien lo que pidió el profesor (dividir por roles o secciones y 2 casos en cada documento)? ¿Hay una lectura mejor?
   - ¿Los dos casos nuevos (CU-D07 y CU-D08) son coherentes con `docs/dms/REM-DMS.md` y `scripts/remus/dms_data.json` (actores, permisos, reglas RN-D01 a RN-D06)? ¿Falta alguna regla o requisito que deban llevar?
   - ¿El reparto entre los 5 es equilibrado y realista en 3 días (13, 14 y 15/11), teniendo en cuenta lo que cada uno tiene pendiente del CMS en `docs/scrum/sprints/sprint-03.md`?
   - ¿Hay dependencias o cuellos de botella (por ejemplo, Pablo con REM, REMUS, zip y SharePoint) y conflictos de archivos entre personas?
   - Pruebas cruzadas: ¿nadie prueba lo suyo y está todo cubierto?
2. `docs/dms/backlog/product-backlog.md`: ¿DMS-HU-08 y DMS-HU-09, los SP (28 en total) y la tarea D-07 son coherentes con el reparto y con `docs/dms/sprints/sprint-01.md`?
3. La decisión del cliente del 09/11 (una cuenta por delegación, con el correo institucional de la delegación), recogida en `docs/scrum/sprints/sprint-03.md` y `scripts/remus/cadus_data.json`: ¿qué partes del DMS (`REM-DMS.md`, `dms_data.json`, `scripts/dms/build_doc_dms.py`, `scripts/dms/diagramas_dms.py`) siguen diciendo que el delegado entra con su correo `@alum.us.es` y habría que cambiar?
4. Riesgos que falten: fecha de entrega sin confirmar, pruebas con cuentas de delegado, el servidor de la US (PHP 7.2/7.3) y la carga conjunta CMS + DMS.

No toques `cms-wordpress/.htaccess` ni los `.sql`.
