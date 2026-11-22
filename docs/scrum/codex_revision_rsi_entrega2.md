# Segunda revisión pedida a Codex: entrega del 22/11/2026 (tras corregir la primera)

Revisión de SOLO LECTURA (no edites archivos, no hagas commit ni push, no cambies nada en GitHub ni en Teams). Responde en español, con hallazgos ordenados por gravedad (alta, media, baja), citando archivo y línea, y al final qué falta antes de entregar. Si no puedes comprobar algo, dilo.

## Contexto
La primera revisión (`docs/scrum/codex_revision_rsi_entrega.md`) encontró 12 problemas. Se han corregido así (compruébalo, no te fíes de este resumen):
1. El caso de negocio se reescribió con el índice del Lab 5 (diapositiva 11: resumen ejecutivo con misión y visión, situación actual con DAFO, descripción del proyecto, drivers, objetivos, riesgos y participantes con personas y organizaciones), y el documento principal pasó a ese orden: 1 caso de negocio, 2 requisitos del sistema software, 3 glosario.
2. Los PDF se regeneraron; las capturas 03 a 06, 10 y 11 de la rama de Marcos están ya en `main` (la 07 quedó duplicada como `07b`); el paquete incluye `pruebas.md`, la guía de Planner y la especificación de PowerApps.
3. El burndown de la red social se corrigió (22, 16 y 3 SP) y se escribió `docs/redsocial/scrum/review-sprint-01-rsi.md`.
4. Se quitó la justificación de los tres equipos por un límite de 30 canales privados.
5. Se añadieron relaciones y multiplicidades en texto al UML de diseño; se completaron trazas del REM (RF-R01, RF-R02, RF-R10, RNF-R02, RNF-R04, RC-R03) y el caso de uso CU-R02 con un paso de Forms.
6. En GitHub se reabrieron E3-01 y E2-12 y se añadieron comentarios «Corrección:» a HU-14, HU-15, PB-003, E2-02, E2-03, E2-04, E2-09 y E2-11 (scripts `scripts/scrum/corregir_cierres.py` y `crear_rsi.py`).

## Qué revisar
1. **Resolución de los 12 hallazgos anteriores:** dime cuáles siguen sin resolverse del todo y por qué.
2. **Caso de negocio frente a la diapositiva 11 del Lab 5** (`docs/Lab 5 - Red Social Interna - MS Teams.pdf`, páginas 11 y 12): ¿están todos los apartados del índice, con el mismo orden y nombre? ¿Afirma hechos del CADUS que no consten en `docs/cliente/entrevista-cliente.md`?
3. **Documento principal** (`docs/redsocial/entrega/Entrega-RSI-CADUS.docx`, generado por `scripts/redsocial/build_doc_rsi.py`): estructura, coherencia entre secciones, pies de captura frente a las imágenes de `docs/redsocial/capturas/`, estados y limitaciones honestos.
4. **REM** (`scripts/remus/rsi_data.json`, `docs/redsocial/rem-remus/carga-remus.md`, `REM-RSI-v1.0.pdf`): trazas rotas, requisitos sin caso de uso, coherencia con el UML y el caso de negocio.
5. **SCRUM** (`docs/redsocial/scrum/*`): ¿burndown, estados y review concuerdan con `git log` y con las capturas?
6. **Paquete final** (`docs/dms/entrega/paquete/Entrega-22-11-CADUS-CMS-DMS-RSI.zip`, que genera `scripts/dms/empaquetar_dms.py --con-rsi`): ¿cumple la lista del profesor para CMS, DMS y red social? La lista es:
   - CMS: propuesta de temática; comparativas (hosting, comunicación, SCRUM, control de versiones); product backlog; sprint backlog; burndown del sprint; REM; UML de estructura web; UML de plugins; tabla comparativa de plugins con métricas; mockups de 3 temáticas; capturas de implementación.
   - DMS: REM; UML de análisis; UML de diseño; 3 o 4 documentos de casos de uso (mínimo uno con más de un CU); documentos de implementación en SharePoint.
   - RSI: REM (índice del Lab 5); caso de negocio; requisitos del sistema software; glosario de términos; nuevo UML de análisis; nuevo UML de diseño; implementación explicada de Teams con capturas.
   Comprueba el contenido real del zip (puedes abrirlo con Python en solo lectura) y dime qué falta o sobra, y si algún documento incluido contradice a otro.
7. **Datos personales** en capturas y documentos del paquete que no deban ir en una entrega.

No toques `cms-wordpress/.htaccess` ni los `.sql`.
