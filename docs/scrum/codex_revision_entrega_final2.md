# Segunda pasada de Codex sobre la entrega del 22/11/2026 (tras corregir la revisión final)

Revisión de SOLO LECTURA: no edites archivos, no hagas commit ni push, no cambies nada en GitHub, Teams ni en el WordPress. Responde en español, hallazgos por gravedad (alta, media, baja), con archivo y línea, y al final di si el zip se puede entregar. No leas ni cites `tests/cuentas-de-prueba-local.md`. No toques `cms-wordpress/.htaccess` ni los `.sql`.

Tu informe anterior (`docs/scrum/codex_revision_entrega_final.md` es el encargo) tenía 10 hallazgos. Comprueba, abriendo el zip `docs/dms/entrega/paquete/Entrega-22-11-CADUS-CMS-DMS-RSI.zip` (113 archivos) y no solo las fuentes, cuáles siguen sin resolverse:
1. Contraseñas visibles en `CMS/capturas-sprint3/m01`, `m02` y `m03` (ahora tapadas). Mira también si alguna otra imagen o PDF del zip enseña una contraseña, token o clave (revisa todas las imágenes del zip, no solo las de RSI y DMS).
2. «OK» del CMS que no sostenían su criterio (T1, T2, H14-1, H14-3 → ahora «Parcial»), cabecera del guion `E3-04` y estados de H16-7 entre `E3-04`, backlog y `sprint-03.md`.
3. Adenda CMS desactualizada: se añadió `CMS/ACTUALIZACION-22-11-estado-del-cms.md` y `CMS/seguimiento/E3-04-pruebas-de-aceptacion.md` al zip. ¿Es suficiente o contradice a la adenda sin aclararlo?
4. `CU-Acta.docx/pdf` (DMS) con la prueba de CU-D01 de Marcos y el texto de la sección 8.4 del documento principal del DMS.
5. Estados RSI (R-02, RSI-HU-06) y trazabilidad de las capturas 05b/05c en el documento (el generador usaba `c[:2]`).
6. `plan-lab5.md` (nota histórica), pie de la captura 08 (fecha del acta), correos individuales en `configuracion-teams.md`, número de capturas en la review.

Después, busca contradicciones nuevas que las correcciones hayan podido introducir y confirma que el zip pasa la lista del profesor (CMS, DMS, RSI).
