# Revisión de la guía de defensa (25/11/2026)

Revisión de SOLO LECTURA: no edites archivos, no hagas commit ni push, no cambies nada en GitHub, Teams ni en el WordPress, y no toques `cms-wordpress/.htaccess` ni los `.sql`. No leas ni cites `tests/cuentas-de-prueba-local.md`. No ejecutes generadores ni scripts que cambien datos. Responde en español, con hallazgos por gravedad (alta, media, baja), cada uno con el texto exacto de la guía que está mal, la evidencia del repositorio y cómo corregirlo. Al final di si se puede usar tal cual para estudiar.

`docs/defensa/guia-defensa-uml.html` es una infografía de estudio para la defensa del proyecto (CMS WordPress del CADUS, DMS en SharePoint y red social interna en Teams). Quien la use la va a estudiar y a repetir en voz alta ante el profesor, así que **cualquier afirmación falsa, exagerada o desactualizada es un problema grave**. La guía explica cómo se plantearon los UML, de dónde salen y cómo se aplicaron a cada parte.

Revisa, comprobando contra el repositorio (REM en `scripts/remus/*_data.json`, UML en `scripts/entrega/diagramas.py`, `scripts/dms/diagramas_dms.py` y `scripts/redsocial/diagramas_rsi.py`, documentos en `scripts/entrega/build_doc.py`, `scripts/dms/build_doc_dms.py` y `scripts/redsocial/build_doc_rsi.py`, seguimiento en `docs/scrum/`, `docs/dms/` y `docs/redsocial/`, y los PDF de los laboratorios `docs/Lab 4 - DMS - v2.pptx`, `docs/Lab 5 - Red Social Interna - MS Teams.pdf` y `Lab 6 - Red Social Interna - Planner Patterns.pdf`):

1. **Cifras de cada REM** (las tarjetas de CMS, DMS y red social): requisitos de información, de interfaz, funcionales, no funcionales, reglas de negocio, casos de uso y actores, y las versiones 2.3, 1.1 y 1.1.
2. **Cada afirmación sobre los UML:** qué clases hay en cada diagrama de análisis, qué dicen las leyendas de las figuras, qué significan las clases azules y verdes del CMS, las asignaciones «concepto del análisis → elemento del diseño» de las tres tablas, y que la clase Plan y el requisito RF-R13 existen donde la guía dice.
3. **Origen de los conceptos:** qué aportan realmente el Lab 4, el Lab 5 y el Lab 6 (la guía dice, por ejemplo, que el Lab 4 da los conceptos documento, carpeta, rol, permiso, búsqueda y metadato, y que el Lab 5 da los estereotipos Role, Group/Subgroups, Tool y Permission).
4. **Las 14 preguntas y sus respuestas:** que todas sean ciertas con lo que hay en el repositorio (por ejemplo, las razones de Teams frente a Discord, de tres equipos frente a uno, de SharePoint, lo que cambió entre entregas, quién hizo qué, cómo encajan los UML con SCRUM, y la respuesta a «¿cómo sabéis que no falta ningún requisito?»).
5. **Los datos clave y la sección «Lo que no está terminado»:** fechas, herramientas, hosting, número de delegaciones y personas, y que cada pendiente declarado sea cierto y que no falte alguno importante.
6. **Las dos cadenas de trazabilidad** (red social: OBJ-R02, RF-R09, RF-R13, IR-R05 y CU-R02; CMS: RN-03, Ticket y Mediación, H16-7 y P5): que cada eslabón exista.
7. **Redacción que pueda inducir a error** a alguien que la repita ante el profesor, y cualquier cosa importante de los UML que la guía no cubra y que el profesor podría preguntar.

Las imágenes del HTML se publican junto a la página desde las carpetas `docs/entrega/img`, `docs/dms/img` y `docs/redsocial/img`; no hace falta que valores el diseño visual.
