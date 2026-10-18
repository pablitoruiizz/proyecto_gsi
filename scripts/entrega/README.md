# Generador del documento de entrega

Genera `docs/entrega/Entrega1-CMS-CADUS.docx` a partir de los datos del repositorio, para poder regenerarlo en cada entrega.

## Piezas
- `diagramas.py`: dibuja los UML (clases, estructura web, plugins), los 4 mockups y el burndown, y escribe `docs/scrum/burndown/sprint-01.csv`.
- `build_doc.py`: monta el Word con los requisitos (`scripts/remus/cadus_data.json`), los backlogs (`docs/scrum`), las comparativas de plugins y temas (`docs/entrega/datos/*.json`) y las capturas (`docs/entrega/img/capturas`).
- `actualizar_indice.ps1`: abre el Word con Microsoft Word, actualiza el índice y los campos y, opcionalmente, exporta un PDF.

## Uso
Requiere Python 3 con `python-docx`, `matplotlib` y `pillow` (`pip install python-docx matplotlib pillow`).

```powershell
python scripts/entrega/diagramas.py
python scripts/entrega/build_doc.py
powershell -File scripts/entrega/actualizar_indice.ps1 -Pdf docs/entrega/Entrega1-CMS-CADUS.pdf
```

## Qué editar para la siguiente entrega
- Requisitos: `scripts/remus/cadus_data.json` (y regenerar el `.rem`, ver `scripts/remus/README.md`).
- Backlogs: `docs/scrum/backlog/product-backlog.md` y `docs/scrum/sprints/sprint-01.md`.
- Burndown: los hitos del diccionario `hechos` de `diagramas.py` (fecha, SP completados e IDs).
- Capturas: sustituir los archivos de `docs/entrega/img/capturas` y revisar la lista `imp_items` de `build_doc.py`.
- Datos de plugins y temas: `docs/entrega/datos/` (procedentes de la API de wordpress.org).
