# Revisión pedida a Codex: planificación del Sprint 3 del CMS y DMS (26/10/2026)

Revisa SOLO LECTURA (no edites ni hagas commit) y responde en español, con hallazgos concretos y citando archivo y línea.

## Contexto
Proyecto GSI (Universidad de Sevilla), portal del CADUS en WordPress (CMS) + un DMS nuevo (Lab 4, SharePoint de la US). El 26/10/2026 se hizo una entrevista con el cliente (`docs/cliente/entrevista-cliente.md`) y el profesor pidió un único sprint de 3 semanas para el CMS y entregar el DMS el 08/11 (CMS el 15/11).

## Qué hay que revisar
1. `docs/cliente/entrevista-cliente.md`: ¿las consecuencias que se derivan de cada respuesta (tabla final) son correctas y completas? ¿Falta algún cambio de requisitos?
2. `docs/scrum/sprints/sprint-03.md`, `docs/scrum/backlog/product-backlog.md` y `docs/scrum/burndown/sprint-03.csv`: suma de SP (36), reparto por persona, coherencia semana a semana (18 + 13 + 5), HU-21 cancelada, HU-22 y HU-23 nuevas, riesgos. ¿Hay incoherencias entre los tres archivos y el script `scripts/scrum/crear_tareas_sprint3.py`?
3. `docs/dms/` (REM-DMS.md, backlog, sprint 1, burndown) frente al enunciado del Lab 4 (`docs/Lab 4 - DMS - v2.pptx`, texto en sus diapositivas): 3-4 documentos distintos, mínimo 1 caso de uso por documento (CU, no RF), al menos 1 documento con más de 1 CU, documentación independiente de la del CMS, metadatos con la columna «tipo de documento», roles Propietario/Integrante/Visitante, valor calculado. ¿Falta algo que el profesor pida? ¿Hay errores de diseño (permisos, metadatos, RN-D04 sin DNI, RN-D05 un voto por delegación)?
4. Trazabilidad: casos de uso ↔ requisitos ↔ historias del DMS; ¿hay requisitos sin caso de uso o casos de uso sin historia?
5. Cualquier riesgo que no esté contemplado (carga del equipo con CMS + DMS, plazos del 08/11 y 15/11, servidor SFTP de la US para WordPress).

No toques `cms-wordpress/.htaccess` ni los `.sql`. Devuelve una lista ordenada por gravedad (alta, media, baja) y, al final, qué cambiarías.
