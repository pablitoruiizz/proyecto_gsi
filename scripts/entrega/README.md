# Generador de los documentos de entrega

Genera, a partir de los datos del repositorio, el documento de la entrega (Word y PDF en estilo REMUS), los diagramas, las capturas y el paquete que se sube. Todo se puede regenerar en cada entrega.

## Piezas
- `diagramas.py`: dibuja los UML (clases, estructura web, plugins), los 7 mockups, las 3 temáticas visuales con sus métricas de contraste, las comparativas con los mockups de la entrega 1 y los burndown; también escribe `docs/scrum/burndown/sprint-0N.csv` y las copias SVG de los mockups (`docs/entrega/figma/`) para importarlas en Figma.
- `build_doc.py`: contenido del documento (requisitos de `scripts/remus/cadus_data.json`, backlogs de `docs/scrum`, comparativas de `docs/entrega/datos/*.json`, capturas) y versión Word (`Entrega2-CMS-CADUS.docx`).
- `build_html.py`: **PDF final en estilo REMUS** (`Entrega2-CMS-CADUS-REMUS.pdf`): mismo CSS que REMUS (`estilo_remus/`), con el documento que exporta REMUS (`docs/requisitos/rem-remus/CADUS__CRS.html`) incrustado como capítulo 3. También genera `docs/entrega/paquete/CADUS-REM-v2.pdf`.
- `capturas_publicas.py` y `capturas_admin.py`: capturas del portal (páginas públicas a página completa y pantallas de administración por rol con cuentas temporales de prueba; `PHP_EXE` indica la ruta de `php.exe` si no es la de Wamp).
- `cargar_eventos_ejemplo.php`: dos eventos y una convocatoria de votación de ejemplo para la demostración (`--quitar` los retira).
- `volcado_bd.php`: volcado de la base de datos con PHP (`mysqldump` no conecta con `caching_sha2_password`); el fichero no se sube a GitHub.
- `empaquetar_entrega2.py`: monta `docs/entrega/entrega2/` y termina con error si falta algo.
- `actualizar_indice.ps1`: abre el Word con Microsoft Word, actualiza el índice y exporta un PDF (alternativa al PDF de `build_html.py`).

## Orden para regenerar la entrega
Requiere Python 3 con `python-docx`, `matplotlib`, `pillow`, `numpy`, `pymupdf` y `playwright` (usa el Chrome instalado; no descarga navegadores), y el servidor Wamp encendido.

```powershell
python scripts/entrega/capturas_publicas.py     # capturas públicas
python scripts/entrega/capturas_admin.py        # capturas de administración
python scripts/entrega/diagramas.py             # UML, mockups, temáticas y burndown
python scripts/entrega/build_doc.py             # Word
python scripts/entrega/build_html.py            # PDF en estilo REMUS (necesita CADUS__CRS.html: abrir CADUS.rem en REMUS)
php scripts/entrega/volcado_bd.php              # volcado de la base de datos
python scripts/entrega/empaquetar_entrega2.py   # docs/entrega/entrega2/
```

## Qué editar para la siguiente entrega
- Requisitos: `scripts/remus/cadus_data.json` y regenerar el `.rem` (ver `scripts/remus/README.md`); después abrirlo en REMUS para que exporte el HTML.
- Backlogs y sprint: `docs/scrum/backlog/product-backlog.md` y `docs/scrum/sprints/sprint-0N.md`.
- Burndown: los hitos del diccionario de `burndowns()` en `diagramas.py` (fecha, SP completados e IDs).
- Capturas: la lista `publicas` y `admin` de `build_doc.py` (sección 6).
- Datos de plugins y temas: `docs/entrega/datos/` (procedentes de la API de wordpress.org).
