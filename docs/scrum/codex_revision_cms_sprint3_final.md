# Revisión pedida a Codex: CMS en el cierre del Sprint 3 (13/11/2026)

Revisión de SOLO LECTURA (no edites archivos, no hagas commit ni push). Responde en español, con hallazgos ordenados por gravedad (alta, media, baja), citando archivo y línea, y al final qué cambiarías. Si no puedes comprobar algo, dilo en vez de suponerlo.

## Contexto
Portal del CADUS (Consejo de Alumnos de la Universidad de Sevilla) en WordPress, en `cms-wordpress/` (tema y plugin propio en `wp-content`), sprint único del 26/10 al 15/11/2026. Este sprint se añadieron: HU-24 (acceso y gestión desde el portal, `scripts/pruebas/gestion.php`), 27 delegaciones con escudos y buscador (`includes/delegaciones.php`), pie nuevo, HU-17b (revisión de formularios en `docs/seguridad/`), HU-20b (caché, minificado y Gzip; informe en `docs/rendimiento/`), HU-14c (móvil, `scripts/pruebas/movil.py`), X7 (la Ejecutiva edita cualquier ficha) y HU-22/HU-23 (relevo de delegados y borrado a los 2 años). Requisitos en `docs/requisitos/rem-remus/REM-CADUS.md` y backlog en `docs/scrum/`.

## Qué revisar
1. Seguridad del código propio (PHP del tema y del plugin): XSS, CSRF/nonces, comprobación de capacidades y roles (Anónimo, Estudiante, Delegado, Ejecutiva, Administrador), inyección SQL, subida de archivos, privacidad del buzón (RN-03) y de las mediaciones, y que un delegado solo pueda editar su propia ficha salvo la Ejecutiva (RN-04, X7).
2. HU-24: flujo de acceso y gestión desde el portal; casos límite de permisos y redirecciones; ¿cubre `scripts/pruebas/gestion.php` lo que afirma?
3. HU-23: borrado o anonimización a los 2 años (RNF-08, RN-03); ¿se puede borrar algo que no toca o dejar datos personales?
4. Coherencia entre `docs/requisitos/rem-remus/REM-CADUS.md`, `docs/scrum/backlog/product-backlog.md`, `docs/scrum/sprints/sprint-03.md` y el código: historias marcadas como hechas que no lo estén, o requisitos sin implementar.
5. Los informes `docs/seguridad/HU-17b-revision-formularios.md`, `docs/rendimiento/HU-20b-informe.md` y `docs/pruebas/HU-14c-movil-tablet.md`: ¿afirman más de lo que prueban?
6. Riesgos para la entrega del 15/11 que no estén contemplados.

No toques `cms-wordpress/.htaccess` ni los `.sql`.
