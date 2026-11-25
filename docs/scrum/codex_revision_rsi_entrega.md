# Revisión pedida a Codex: entrega del 22/11/2026 (red social interna, SCRUM y proyecto de GitHub)

Revisión de SOLO LECTURA (no edites archivos, no hagas commit ni push, no cambies nada en GitHub ni en Teams). Responde en español, con hallazgos ordenados por gravedad (alta, media, baja), citando archivo y línea, y al final qué cambiarías. Si no puedes comprobar algo, dilo en vez de suponerlo.

## Contexto
Proyecto GSI (Universidad de Sevilla): portal del CADUS en WordPress (CMS), un DMS en SharePoint y, desde el Lab 5, una **red social interna en Microsoft Teams**. Hoy es la entrega (domingo 22/11/2026, 23:59): un solo zip con CMS, DMS y red social. Equipo de 4 personas (Pablo, Joaquín, Álvaro y Marcos; Miguel Ángel dejó el trabajo el 16/11).

Lista de entrega del profesor para la red social: Requisitos (REM) siguiendo el índice del Lab 5; Caso de negocio; Requisitos del sistema software; Glosario de términos; nuevo UML de análisis; nuevo UML de diseño; implementación explicada de Teams con capturas. El enunciado está en `docs/Lab 5 - Red Social Interna - MS Teams.pdf` (diapositivas: Business Case, grupos principales y piloto, REM con caso de negocio y requisitos de grupos y herramientas, análisis con `<<Role>>`, `<<Group>>`/`<<Subgroups>>`, `<<Tool>>` y `<<Permission>>`, diseño transformado a conceptos de Teams, capturas explicadas y SCRUM).

Parte del trabajo está en ramas remotas sin fusionar en `main`; léelas con `git show origin/<rama>:<ruta>` o `git diff main...origin/<rama>`:
- `origin/feature/marcos-teams-capturas`: configuración de Teams de Marcos (capturas 03 a 06, 10 y 11, `docs/redsocial/pruebas.md`).
- `origin/docs/rsi-uml-revision`: revisión de los UML de Álvaro y `docs/redsocial/powerapps-especificacion.md`.

## Qué revisar
1. **REM de la red social** (`scripts/remus/rsi_data.json`, `scripts/remus/rsi_generar.py`, `docs/redsocial/rem-remus/carga-remus.md`, `docs/redsocial/glosario.md`): coherencia entre objetivos, actores, información, funcionales, casos de uso, reglas y trazas; códigos con trazas rotas o requisitos sin caso de uso; si cubre lo que pide el Lab 5 (caso de negocio, requisitos de grupos y herramientas, glosario).
2. **Caso de negocio** (`docs/redsocial/business-case.md`): ¿se sostiene la justificación de Teams frente a Discord y mensajería personal? ¿Afirma hechos sobre el CADUS que no constan en `docs/cliente/entrevista-cliente.md`?
3. **UML** (`docs/redsocial/img/uml-rsi-analisis.png`, `uml-rsi-diseno.png`, generados por `scripts/redsocial/diagramas_rsi.py`, y la versión de la rama de Álvaro): estereotipos del Lab 5, correspondencia análisis→diseño, decisión de tres equipos por el límite de canales privados (¿es correcta y está bien explicada?).
4. **Implementación y capturas** (`docs/redsocial/capturas/`, `docs/redsocial/configuracion-teams.md`, `configuracion-planner.md`, `pruebas.md` de la rama de Marcos, `colaboracion-microsoft365/planner/README.md`): ¿cada pie de foto y cada afirmación del documento está sostenida por su captura? ¿Hay datos personales que no deban ir en una entrega? Mira los pies en `scripts/redsocial/build_doc_rsi.py` (diccionario `CAPS`).
5. **Documento principal y empaquetado** (`scripts/redsocial/build_doc_rsi.py`, `docs/redsocial/entrega/*.docx`, `scripts/dms/empaquetar_dms.py` con `--con-rsi`): ¿falta o sobra algo respecto a la lista del profesor? ¿Hay estados o afirmaciones inflados (por ejemplo, tareas «hechas» sin evidencia)?
6. **SCRUM de la red social** (`docs/redsocial/scrum/*`): backlog con puntos estimados a posteriori, sprint backlog, burndown (`burndown-sprint-01-rsi.csv`) y review. ¿Son honestos frente al historial de git (`git log --since=2026-11-16`)? ¿Está bien dicho que los puntos se estimaron después?
7. **Proyecto de GitHub** (`scripts/scrum/crear_rsi.py`, `scripts/scrum/cerrar_pendientes.py`): hoy se dieron de alta las ocho historias RSI-HU-01 a 08 y se cerraron como hechas HU-14, HU-15, PB-003, PB-004, E2-02, E2-03, E2-04, E2-09, E2-12 y E3-01, y se cancelaron E2-08, E2-11 y E2-19 por depender del cliente. Contrasta cada cierre con la evidencia que cita (repositorio, `docs/scrum/`) y dime cuáles no se sostienen. Los comentarios de GitHub se pueden leer con `gh issue view <n> --comments` (solo lectura).
8. **Sprint 3 del CMS**: `docs/scrum/sprints/sprint-03.md` (secciones «Estado a 15/11», «Resultado» y «Sprint Review y retrospectiva», escritas a partir de los datos del sprint, no de una reunión) y su coherencia con `docs/scrum/burndown/sprint-03.csv` y el product backlog.

No toques `cms-wordpress/.htaccess` ni los `.sql`.
