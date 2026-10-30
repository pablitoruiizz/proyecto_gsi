# Revisión pedida a Codex: entrega del DMS y adenda del CMS (30/10/2026)

Revisión de SOLO LECTURA (no edites archivos ni hagas commit). Responde en español, con hallazgos ordenados por gravedad (alta, media, baja), citando archivo y línea, y al final qué cambiarías.

## Contexto
Proyecto GSI (Universidad de Sevilla): portal del CADUS en WordPress (CMS) y un DMS nuevo en SharePoint de la US (Lab 4). La próxima entrega (zip) debe contener, según el profesor:

CMS: propuesta de temática, comparativas (hosting, comunicación, SCRUM, control de versiones; si no cambian se adjunta el mismo documento), product backlog (el mismo), sprint backlog del sprint de estas semanas, burndown solo del sprint actual, REM, análisis (UML estructura web), diseño (UML de plugins, tabla comparativa con métricas, mockups con 3 temáticas), implementación (capturas).
DMS: Requisitos (REM), nuevos documentos de análisis (UML), nuevos documentos de diseño (UML), documentos de casos de uso (3-4 documentos distintos y mínimo 1 con más de 1 CU), nuevos documentos de implementación (SharePoint).

## Qué revisar
1. `docs/dms/entrega/Entrega-DMS-CADUS.docx` (y su `.pdf`), generado por `scripts/dms/build_doc_dms.py`, y los 4 documentos de `docs/dms/entrega/casos-de-uso/`: ¿cubren lo pedido? ¿hay errores, incoherencias entre secciones o requisitos sin trazabilidad?
2. `docs/dms/REM-DMS.md`, `scripts/remus/dms_data.json` y `docs/dms/rem-remus/carga-remus.md` (hoja generada para `DMS.rem`): coherencia entre los tres, códigos, trazas (OBJ, CU, RF, RN, IR, UI).
3. `docs/dms/img/uml-dms-analisis.png`, `uml-dms-diseno.png`, `casos-de-uso-dms.png` (generados por `scripts/dms/diagramas_dms.py`): ¿el análisis y el diseño son coherentes con el Lab 4 (`docs/Lab 4 - DMS - v2.pptx`: documento, carpeta, rol, permiso, búsqueda, metadato; sitio/carpeta, grupos propietario/integrante/visitante, vista plana)?
4. `docs/dms/entrega/cms/Adenda-CMS-Sprint3.docx` (`scripts/dms/build_adenda_cms.py`): ¿refleja bien los cambios del CMS (HU-21 cancelada, HU-22 y HU-23, 36 SP), el sprint backlog y el burndown de solo el Sprint 3?
5. Estado real: las capturas de `docs/dms/capturas/` son de SharePoint real (`uses0.sharepoint.com`, tres sitios creados con bibliotecas, columnas, vistas y permisos por la API REST). Comprueba si el texto del documento afirma algo que las capturas o el estado declarado no sostienen (por ejemplo, que un delegado no ve borradores: no se ha probado con una cuenta de delegado).
6. El paquete `docs/dms/entrega/paquete/Entrega-08-11-CADUS-CMS-DMS.zip` (`scripts/dms/empaquetar_dms.py`): ¿falta o sobra algo respecto a la lista del profesor?
7. Burndown del DMS (`docs/dms/burndown/sprint-01.csv`): ¿se presenta de forma honesta?

No toques `cms-wordpress/.htaccess` ni los `.sql`.
