"""Monta el zip de la entrega del 08/11 (CMS + DMS) en docs/dms/entrega/paquete/. Uso: python scripts/dms/empaquetar_dms.py"""
import os
import shutil
import sys
import zipfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DMS = os.path.join(RAIZ, "docs", "dms")
ENT = os.path.join(DMS, "entrega")
PAQ = os.path.join(ENT, "paquete")
NOMBRE = "Entrega-08-11-CADUS-CMS-DMS"
RAIZ_ZIP = os.path.join(PAQ, NOMBRE)

# (origen relativo a RAIZ, destino dentro del paquete)
ARCHIVOS = [
    ("docs/entrega/Entrega2-CMS-CADUS.docx", "CMS/Entrega2-CMS-CADUS.docx"),
    ("docs/entrega/entrega2/Entrega2-CMS-CADUS.pdf", "CMS/Entrega2-CMS-CADUS.pdf"),
    ("docs/entrega/paquete/CADUS-REM-v2.pdf", "CMS/REM-CADUS-v2.pdf"),
    ("docs/entrega/paquete/CADUS.rem", "CMS/CADUS.rem"),
    ("docs/dms/entrega/cms/Adenda-CMS-Sprint3.docx", "CMS/Adenda-CMS-Sprint3.docx"),
    ("docs/dms/entrega/cms/Adenda-CMS-Sprint3.pdf", "CMS/Adenda-CMS-Sprint3.pdf"),
    ("docs/scrum/sprints/sprint-03.md", "CMS/seguimiento/sprint-03.md"),
    ("docs/scrum/burndown/sprint-03.csv", "CMS/seguimiento/burndown-sprint-03.csv"),
    ("docs/scrum/backlog/product-backlog.md", "CMS/seguimiento/product-backlog.md"),
    ("docs/dms/entrega/Entrevista-CADUS.docx", "Entrevista-CADUS.docx"),
    ("docs/dms/entrega/Entrevista-CADUS.pdf", "Entrevista-CADUS.pdf"),
    ("docs/dms/entrega/Entrega-DMS-CADUS.docx", "DMS/Entrega-DMS-CADUS.docx"),
    ("docs/dms/entrega/Entrega-DMS-CADUS.pdf", "DMS/Entrega-DMS-CADUS.pdf"),
    ("docs/dms/rem-remus/DMS.rem", "DMS/1-Requisitos/DMS.rem"),
    ("docs/dms/rem-remus/carga-remus.md", "DMS/1-Requisitos/carga-remus.md"),
    ("docs/dms/REM-DMS.md", "DMS/1-Requisitos/REM-DMS.md"),
    ("docs/dms/img/uml-dms-analisis.png", "DMS/2-Analisis/uml-dms-analisis.png"),
    ("docs/dms/img/casos-de-uso-dms.png", "DMS/2-Analisis/casos-de-uso-dms.png"),
    ("docs/dms/img/uml-dms-diseno.png", "DMS/3-Diseno/uml-dms-diseno.png"),
    ("docs/dms/backlog/product-backlog.md", "DMS/seguimiento/product-backlog-dms.md"),
    ("docs/dms/sprints/sprint-01.md", "DMS/seguimiento/sprint-01-dms.md"),
    ("docs/dms/burndown/sprint-01.csv", "DMS/seguimiento/burndown-sprint-01-dms.csv"),
    ("docs/dms/img/burndown-dms.png", "DMS/seguimiento/burndown-dms.png"),
]
for t in ("CU-Acta", "CU-Normativa", "CU-Expediente", "CU-Votacion"):
    ARCHIVOS += [(f"docs/dms/entrega/casos-de-uso/{t}.docx", f"DMS/4-Casos-de-uso/{t}.docx"), (f"docs/dms/entrega/casos-de-uso/{t}.pdf", f"DMS/4-Casos-de-uso/{t}.pdf")]
for f in sorted(os.listdir(os.path.join(DMS, "capturas"))):
    ARCHIVOS.append((f"docs/dms/capturas/{f}", f"DMS/5-Implementacion-SharePoint/{f}"))

LEEME = """# Entrega del 08/11/2026 — CADUS (CMS + DMS)

Equipo: Pablo Ruiz Vidal, Joaquín Luna Canela, Miguel Ángel Camacho Martín, Álvaro Martínez Ocaña y Marcos-Paban Delgado Rodríguez.

## Entrevista con el cliente
- `Entrevista-CADUS.docx` / `.pdf`: entrevista con el CADUS (26/10/2026), de la que salen los requisitos del DMS y los cambios del CMS.

## CMS (portal WordPress)
El proyecto es el mismo que en la entrega anterior, así que se vuelve a adjuntar el documento de la entrega 2 (propuesta de temática, comparativas de hosting, comunicación, SCRUM, control de versiones y plugins, análisis, diseño, mockups y capturas) y se añade una adenda con lo que cambia:
- `Entrega2-CMS-CADUS.docx` / `.pdf`: documento de la entrega 2, sin cambios (sus gráficos de burndown son los de los sprints anteriores; el burndown de esta entrega es el del Sprint 3, en la adenda).
- `REM-CADUS-v2.pdf` y `CADUS.rem`: REM del CMS actualizado a la versión 2.1 con las respuestas de la entrevista (el PDF se regenera al exportar de nuevo desde REMUS).
- `Adenda-CMS-Sprint3.docx` / `.pdf`: cambios de requisitos tras la entrevista, product backlog actualizado, sprint backlog y burndown del Sprint 3.
- `seguimiento/`: sprint backlog, burndown (csv) y product backlog en su formato original.

## DMS (SharePoint de la Universidad de Sevilla)
- `Entrega-DMS-CADUS.docx` / `.pdf`: documento principal (requisitos, análisis, diseño, casos de uso, implementación y seguimiento SCRUM).
- `1-Requisitos`: `DMS.rem` (proyecto REMUS), hoja `carga-remus.md` y `REM-DMS.md`.
- `2-Analisis`: UML de análisis y diagrama de casos de uso.
- `3-Diseno`: UML de diseño (del análisis a SharePoint).
- `4-Casos-de-uso`: 4 documentos de casos de uso (acta y expediente con 2 casos de uso cada uno).
- `5-Implementacion-SharePoint`: capturas del entorno real (`uses0.sharepoint.com`).
- `seguimiento`: product backlog, sprint backlog y burndown del DMS (independientes de los del CMS).

Sitios de SharePoint: `uses0.sharepoint.com/sites/cadus-documentacion-publica`, `cadus-organos-de-gobierno` y `cadus-atencion-al-estudiante`.
"""


def main():
    if os.path.isdir(PAQ):
        shutil.rmtree(PAQ)
    faltan = []
    for o, d in ARCHIVOS:
        src = os.path.join(RAIZ, o)
        if not os.path.exists(src):
            faltan.append(o)
            continue
        dst = os.path.join(RAIZ_ZIP, d)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    if faltan:
        sys.exit("faltan archivos: " + ", ".join(faltan))
    open(os.path.join(RAIZ_ZIP, "LEEME.md"), "w", encoding="utf-8").write(LEEME)
    zip_ruta = os.path.join(PAQ, NOMBRE + ".zip")
    with zipfile.ZipFile(zip_ruta, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, fs in os.walk(RAIZ_ZIP):
            for f in fs:
                p = os.path.join(base, f)
                z.write(p, os.path.relpath(p, PAQ))
    print("zip:", zip_ruta, round(os.path.getsize(zip_ruta) / 1e6, 1), "MB,", len(ARCHIVOS) + 1, "archivos")


main()
