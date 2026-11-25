# Revisión cruzada final pedida a Codex: entrega del 22/11/2026 (CMS + DMS + red social)

Revisión de SOLO LECTURA: no edites archivos, no hagas commit ni push, no cambies nada en GitHub, Teams ni en el WordPress. Responde en español, con hallazgos ordenados por gravedad (alta, media, baja), citando archivo y línea, y al final qué falta antes de entregar. Si no puedes comprobar algo, dilo. No toques `cms-wordpress/.htaccess` ni los `.sql`. No leas ni cites `tests/cuentas-de-prueba-local.md` (está fuera de git y no va en la entrega).

## Contexto
Es la última revisión antes de enviar el zip `docs/dms/entrega/paquete/Entrega-22-11-CADUS-CMS-DMS-RSI.zip` (lo genera `scripts/dms/empaquetar_dms.py --con-cms --con-rsi`). Las dos revisiones anteriores están en `docs/scrum/codex_revision_rsi_entrega.md` y `docs/scrum/codex_revision_rsi_entrega2.md`. Cambios desde la segunda:
1. Prueba de aislamiento con una cuenta «solo miembro» (Álvaro, 22/11): capturas `docs/redsocial/capturas/05b-avisos-solo-miembro.jpg` y `05c-canales-solo-miembro.jpg`, fila nueva en `docs/redsocial/pruebas.md`, y textos actualizados en el generador `scripts/redsocial/build_doc_rsi.py`, el SCRUM de la red social, `business-case.md` y `configuracion-teams.md`.
2. Pruebas del CMS en el WordPress local el 22/11 (`tests/E3-04-pruebas-de-aceptacion.md`: H16-1 a H16-7, T1, T2, H14-2 a H14-4, H15-1 y H15-3 parciales, H17-3 parcial). HU-14 y HU-15 se reabrieron en GitHub (siguen «En curso»); E3-09 (despliegue en la US) queda como «hablar con la US», fuera de la cuenta de los sprints. Cambios en `docs/scrum/backlog/product-backlog.md` y `docs/scrum/sprints/sprint-03.md`.
3. La tarea de Planner «Preparar la plantilla del acta» pasó del 27/11 al 25/11 (`colaboracion-microsoft365/planner/README.md`).

## Qué revisar
1. **Coherencia de la prueba de aislamiento**: ¿afirma algo que las capturas 05b y 05c no muestren? (Las capturas no enseñan el rol; el pie lo dice.) ¿Quedó algún texto que aún diga que esa prueba está pendiente o que «los cuatro son propietarios» sin matizar? Busca en `docs/redsocial`, `scripts/redsocial`, `scripts/scrum`, `docs/dms` y el contenido real del zip (ábrelo con Python en solo lectura, incluido el docx y el PDF de la entrega).
2. **Resultados del CMS** (`tests/E3-04-pruebas-de-aceptacion.md`, backlog, `sprint-03.md`): ¿hay algún «OK» que la descripción del propio caso no sostenga (por ejemplo, pruebas hechas en emulación presentadas como en dispositivo real, o por la misma persona que programó)? ¿Se declara con honestidad quién ejecutó H16-7 y H17-3 (Claude en nombre de Pablo, no prueba cruzada)? ¿Contradice el backlog a `sprint-03.md` o a lo anotado en GitHub (HU-14, HU-15, HU-16, E3-09)?
3. **Paquete final**: ¿cumple la lista del profesor para CMS, DMS y RSI? La lista es:
   - CMS: propuesta de temática; comparativas (hosting, comunicación, SCRUM, control de versiones); product backlog; sprint backlog; burndown del sprint; REM; UML de estructura web; UML de plugins; tabla comparativa de plugins con métricas; mockups de 3 temáticas; capturas de implementación.
   - DMS: REM; UML de análisis; UML de diseño; 3 o 4 documentos de casos de uso (mínimo uno con más de un CU); documentos de implementación en SharePoint.
   - RSI: REM (índice del Lab 5); caso de negocio; requisitos del sistema software; glosario de términos; nuevo UML de análisis; nuevo UML de diseño; implementación explicada de Teams con capturas.
   Dime qué falta, qué sobra y si algún documento contradice a otro (fechas, nombres, cifras, estados).
4. **Datos personales y secretos** en capturas, documentos y zip: contraseñas, tokens, correos personales, claves, rutas locales con nombre de usuario. Las capturas 05b y 05c muestran las iniciales «ÁO» y la barra del navegador: ¿es un problema?
5. **Seguimiento SCRUM de la red social** (`docs/redsocial/scrum/*`): ¿concuerdan burndown, estados y review con `git log` y con las capturas? ¿Los puntos y fechas son honestos?
6. Cualquier otra cosa que impida entregar hoy.
