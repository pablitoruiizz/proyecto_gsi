"""Monta el zip de la versión definitiva del DMS en docs/dms/entrega/paquete/.
Uso: python scripts/dms/empaquetar_dms.py            (solo el DMS)
     python scripts/dms/empaquetar_dms.py --con-cms  (añade la parte del CMS, como en la entrega del 08/11)
Antes: python scripts/dms/build_doc_dms.py y scripts/dms/exportar_pdf.ps1. Comprueba el contenido frente a la lista del profesor."""
import json
import os
import shutil
import sys
import zipfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DMS = os.path.join(RAIZ, "docs", "dms")
ENT = os.path.join(DMS, "entrega")
PAQ = os.path.join(ENT, "paquete")
FINAL = "--final" in sys.argv  # entrega final del 29/11/2026: implica CMS + DMS + red social v2
CON_RSI = "--con-rsi" in sys.argv or FINAL
CON_CMS = "--con-cms" in sys.argv or CON_RSI
D = json.load(open(os.path.join(RAIZ, "scripts", "remus", "dms_data.json"), encoding="utf-8-sig"))
VERSION = ".".join(str(n) for n in D["version"])
FECHA = "29-11" if FINAL else ("22-11" if CON_RSI else "15-11")  # fecha de entrega de la versión definitiva, pendiente de confirmar con el profesor (D-09)
NOMBRE = f"Entrega-{FECHA}-CADUS-CMS-DMS-RSI" + ("-v2" if FINAL else "") if CON_RSI else f"Entrega-{FECHA}-CADUS-DMS-definitiva" + ("-con-CMS" if CON_CMS else "")
RAIZ_ZIP = os.path.join(PAQ, NOMBRE)
TIPOS = ("CU-Acta", "CU-Normativa", "CU-Expediente", "CU-Votacion")

# (origen relativo a RAIZ, destino dentro del paquete)
CMS = [
    ("docs/entrega/Entrega2-CMS-CADUS.docx", "CMS/Entrega2-CMS-CADUS.docx"),
    ("docs/entrega/entrega2/Entrega2-CMS-CADUS.pdf", "CMS/Entrega2-CMS-CADUS.pdf"),
    ("docs/requisitos/rem-remus/REM-CADUS-v2.3.pdf", "CMS/REM-CADUS-v2.3.pdf"),
    ("docs/requisitos/rem-remus/CADUS.rem", "CMS/CADUS.rem"),
    ("docs/dms/entrega/cms/Adenda-CMS-Sprint3.docx", "CMS/Adenda-CMS-Sprint3.docx"),
    ("docs/dms/entrega/cms/Adenda-CMS-Sprint3.pdf", "CMS/Adenda-CMS-Sprint3.pdf"),
    ("docs/scrum/sprints/sprint-03.md", "CMS/seguimiento/sprint-03.md"),
    ("docs/scrum/burndown/sprint-03.csv", "CMS/seguimiento/burndown-sprint-03.csv"),
    ("docs/scrum/backlog/product-backlog.md", "CMS/seguimiento/product-backlog.md"),
    ("docs/entrega/capturas-sprint3-miguel.md", "CMS/capturas-sprint3/capturas-sprint3.md"),
    ("docs/entrega/actualizacion-cms-22-11.md", "CMS/ACTUALIZACION-22-11-estado-del-cms.md"),
    ("tests/E3-04-pruebas-de-aceptacion.md", "CMS/seguimiento/E3-04-pruebas-de-aceptacion.md"),
]
for _f in sorted(os.listdir(os.path.join(DMS, "..", "entrega", "img", "capturas3"))):
    CMS.append((f"docs/entrega/img/capturas3/{_f}", f"CMS/capturas-sprint3/{_f}"))
ARCHIVOS = [
    ("docs/dms/entrega/Entrevista-CADUS.docx", "Entrevista-CADUS.docx"),
    ("docs/dms/entrega/Entrevista-CADUS.pdf", "Entrevista-CADUS.pdf"),
    ("docs/dms/entrega/Entrega-DMS-CADUS.docx", "DMS/Entrega-DMS-CADUS.docx"),
    ("docs/dms/entrega/Entrega-DMS-CADUS.pdf", "DMS/Entrega-DMS-CADUS.pdf"),
    ("docs/dms/rem-remus/DMS.rem", "DMS/1-Requisitos/DMS.rem"),
    (f"docs/dms/rem-remus/REM-DMS-v{VERSION}.pdf", f"DMS/1-Requisitos/REM-DMS-v{VERSION}.pdf"),
    ("docs/dms/rem-remus/carga-remus.md", "DMS/1-Requisitos/carga-remus.md"),
    ("docs/dms/REM-DMS.md", "DMS/1-Requisitos/REM-DMS.md"),
    ("docs/dms/img/uml-dms-analisis.png", "DMS/2-Analisis/uml-dms-analisis.png"),
    ("docs/dms/img/casos-de-uso-dms.png", "DMS/2-Analisis/casos-de-uso-dms.png"),
    ("docs/dms/img/uml-dms-diseno.png", "DMS/3-Diseno/uml-dms-diseno.png"),
    ("docs/dms/backlog/product-backlog.md", "DMS/seguimiento/product-backlog-dms.md"),
    ("docs/dms/sprints/sprint-01.md", "DMS/seguimiento/sprint-01-dms.md"),
    ("docs/dms/burndown/sprint-01.csv", "DMS/seguimiento/burndown-sprint-01-dms.csv"),
    ("docs/dms/img/burndown-dms.png", "DMS/seguimiento/burndown-dms.png"),
    ("docs/dms/sprints/sprint-02.md", "DMS/seguimiento/sprint-02-dms.md"),
    ("docs/dms/burndown/sprint-02.csv", "DMS/seguimiento/burndown-sprint-02-dms.csv"),
    ("docs/dms/img/burndown-dms-sprint-02.png", "DMS/seguimiento/burndown-dms-sprint-02.png"),
]
for sec in ("Acta", "Normativa", "Expediente", "Votacion"):
    ARCHIVOS += [(f"docs/dms/rem-remus/secciones/DMS-{sec}.rem", f"DMS/1-Requisitos/secciones/DMS-{sec}.rem"),
                 (f"docs/dms/rem-remus/secciones/carga-remus-{sec.lower()}.md", f"DMS/1-Requisitos/secciones/carga-remus-{sec.lower()}.md")]
for t in TIPOS:
    ARCHIVOS += [(f"docs/dms/entrega/casos-de-uso/{t}.docx", f"DMS/4-Casos-de-uso/{t}.docx"), (f"docs/dms/entrega/casos-de-uso/{t}.pdf", f"DMS/4-Casos-de-uso/{t}.pdf")]
for f in sorted(os.listdir(os.path.join(DMS, "capturas"))):
    ARCHIVOS.append((f"docs/dms/capturas/{f}", f"DMS/5-Implementacion-SharePoint/{f}"))
if CON_CMS:
    ARCHIVOS = CMS + ARCHIVOS

# Red social interna (Lab 5): lo que falte (capturas, seguimiento de Joaquín) se avisa, pero no impide generar el zip
RSI_FILES = [
    ("docs/redsocial/entrega/Entrega-RSI-CADUS.docx", "RSI/Entrega-RSI-CADUS.docx"),
    ("docs/redsocial/entrega/Entrega-RSI-CADUS.pdf", "RSI/Entrega-RSI-CADUS.pdf"),
    ("docs/redsocial/rem-remus/RSI.rem", "RSI/1-Requisitos-REM/RSI.rem"),
    ("docs/redsocial/rem-remus/REM-RSI-v1.0.pdf", "RSI/1-Requisitos-REM/REM-RSI-v1.0.pdf"),
    ("docs/redsocial/rem-remus/carga-remus.md", "RSI/1-Requisitos-REM/carga-remus.md"),
    ("docs/redsocial/glosario.md", "RSI/1-Requisitos-REM/glosario-de-terminos.md"),
    ("docs/redsocial/entrega/Business-Case-RSI.docx", "RSI/2-Caso-de-negocio/Business-Case-RSI.docx"),
    ("docs/redsocial/entrega/Business-Case-RSI.pdf", "RSI/2-Caso-de-negocio/Business-Case-RSI.pdf"),
    ("docs/redsocial/img/uml-rsi-analisis.png", "RSI/3-Analisis-UML/uml-rsi-analisis.png"),
    ("docs/redsocial/img/uml-rsi-diseno.png", "RSI/4-Diseno-UML/uml-rsi-diseno.png"),
    ("docs/redsocial/configuracion-teams.md", "RSI/5-Implementacion-Teams/configuracion-teams.md"),
    ("docs/redsocial/configuracion-planner.md", "RSI/5-Implementacion-Teams/configuracion-planner.md"),
    ("docs/redsocial/pruebas.md", "RSI/5-Implementacion-Teams/pruebas.md"),
    ("docs/redsocial/powerapps-especificacion.md", "RSI/5-Implementacion-Teams/powerapps-especificacion.md"),
    ("docs/redsocial/diseno-tableros-planner.md", "RSI/5-Implementacion-Teams/diseno-tableros-planner.md"),  # Lab 6
    ("colaboracion-microsoft365/planner/README.md", "RSI/5-Implementacion-Teams/planner-diseno.md"),
    ("docs/redsocial/plan-lab5.md", "RSI/seguimiento/plan-lab5.md"),
]
_cap = os.path.join(RAIZ, "docs", "redsocial", "capturas")
if os.path.isdir(_cap):
    RSI_FILES += [(f"docs/redsocial/capturas/{f}", f"RSI/5-Implementacion-Teams/{f}") for f in sorted(os.listdir(_cap))]
_scrum = os.path.join(RAIZ, "docs", "redsocial", "scrum")
if os.path.isdir(_scrum):
    RSI_FILES += [(f"docs/redsocial/scrum/{f}", f"RSI/seguimiento/{f}") for f in sorted(os.listdir(_scrum))]
if CON_RSI:
    ARCHIVOS = ARCHIVOS + RSI_FILES

# Lista del profesor (Lab 4): carpeta del zip y mínimo de archivos que debe tener.
LISTA = [
    ("Requisitos (REM y proyectos REMUS: DMS.rem y un .rem por sección)", "DMS/1-Requisitos", 5),
    ("Documentos de análisis (UML)", "DMS/2-Analisis", 2),
    ("Documentos de diseño (UML)", "DMS/3-Diseno", 1),
    ("Documentos de casos de uso: 4, por secciones, con 2 casos cada uno (docx y pdf)", "DMS/4-Casos-de-uso", 8),
    ("Documentos de implementación (capturas de SharePoint)", "DMS/5-Implementacion-SharePoint", 14),
    ("Seguimiento SCRUM del DMS", "DMS/seguimiento", 5),
]
if CON_RSI:
    LISTA += [
        ("RSI · Requisitos (REM), requisitos del sistema software y glosario de términos", "RSI/1-Requisitos-REM", 4),
        ("RSI · Caso de negocio (Word y PDF)", "RSI/2-Caso-de-negocio", 2),
        ("RSI · Nuevo UML de análisis", "RSI/3-Analisis-UML", 1),
        ("RSI · Nuevo UML de diseño", "RSI/4-Diseno-UML", 1),
        ("RSI · Implementación explicada de Teams con capturas (guía y al menos 6 capturas)", "RSI/5-Implementacion-Teams", 7),
        ("RSI · Seguimiento SCRUM de la red social", "RSI/seguimiento", 3),
    ]

LEEME_RSI = """
## Red social interna (Microsoft Teams, Lab 5)
- `Entrega-RSI-CADUS.docx` / `.pdf`: documento principal (caso de negocio, requisitos, glosario, análisis, diseño, implementación, trazabilidad y SCRUM).
- `1-Requisitos-REM`: `RSI.rem` (proyecto REMUS), `REM-RSI-v1.0.pdf` (su exportación, con el índice propio de REMUS), hoja `carga-remus.md` y `glosario-de-terminos.md`. El índice del Lab 5 (caso de negocio, requisitos del sistema software y glosario) está en `Entrega-RSI-CADUS` y en `2-Caso-de-negocio`.
- `2-Caso-de-negocio`: `Business-Case-RSI` (Word y PDF).
- `3-Analisis-UML` y `4-Diseno-UML`: UML de análisis (Role, Group, Subgroups, Tool y Permission) y UML de diseño en Teams.
- `5-Implementacion-Teams`: capturas de Teams (tenant de la Universidad de Sevilla) y guía de configuración.
- `seguimiento`: plan y seguimiento SCRUM de la red social.
"""

LEEME_CMS = """
## CMS (portal WordPress)
- `Entrega2-CMS-CADUS.docx` / `.pdf`: documento de la entrega 2, sin cambios.
- `REM-CADUS-v2.3.pdf` y `CADUS.rem`: REM del CMS (versión 2.3) exportado desde REMUS.
- `capturas-sprint3`: capturas del Sprint 3 (relevo de la cuenta, calendario, páginas institucionales y accesibilidad) con su tabla explicativa.
- `Adenda-CMS-Sprint3.docx` / `.pdf`: cambios de requisitos tras la entrevista, backlog, sprint backlog y burndown del Sprint 3.
- `seguimiento/`: sprint backlog, burndown (csv) y product backlog en su formato original.
"""

LEEME = f"""# Versión definitiva del DMS — CADUS

Equipo: Pablo Ruiz Vidal, Joaquín Luna Canela, Miguel Ángel Camacho Martín, Álvaro Martínez Ocaña y Marcos-Paban Delgado Rodríguez.

Cambio pedido por el profesor sobre la entrega del 08/11: dividir los casos de uso por roles o secciones y añadir dos casos en cada documento. Ahora hay 4 documentos de casos de uso, uno por sección, con 2 casos cada uno (8 en total, con los nuevos CU-D07 y CU-D08), y el REM pasa a la versión {VERSION}.

## Entrevista con el cliente
- `Entrevista-CADUS.docx` / `.pdf`: entrevista con el CADUS (26/10/2026), de la que salen los requisitos del DMS.

## DMS (SharePoint de la Universidad de Sevilla)
- `Entrega-DMS-CADUS.docx` / `.pdf`: documento principal (requisitos, análisis, diseño, casos de uso, implementación, trazabilidad y seguimiento SCRUM).
- `1-Requisitos`: `DMS.rem` (proyecto REMUS completo, con los 8 casos), `REM-DMS-v{VERSION}.pdf` (su exportación), hoja `carga-remus.md` y `REM-DMS.md`; en `secciones/`, un `.rem` por sección (Acta, Normativa, Expediente y Votación, con sus dos casos de uso cada uno) y su hoja legible.
- `2-Analisis`: UML de análisis y diagrama de casos de uso con los 8 casos y los roles.
- `3-Diseno`: UML de diseño (del análisis a SharePoint).
- `4-Casos-de-uso`: CU-Acta (CU-D01, CU-D02), CU-Normativa (CU-D03, CU-D07), CU-Expediente (CU-D04, CU-D05) y CU-Votacion (CU-D06, CU-D08).
- `5-Implementacion-SharePoint`: capturas del entorno real (`uses0.sharepoint.com`), explicadas en cada documento de casos de uso.
- `seguimiento`: product backlog, sprint backlog y burndown de los dos sprints del DMS.

Sitios de SharePoint: `uses0.sharepoint.com/sites/cadus-documentacion-publica`, `cadus-organos-de-gobierno`, `cadus-votaciones` y `cadus-atencion-al-estudiante`.
"""


def main():
    # solo se borra lo de esta variante (el zip del DMS y el zip con CMS conviven en la misma carpeta)
    if os.path.isdir(RAIZ_ZIP):
        shutil.rmtree(RAIZ_ZIP)
    if os.path.exists(RAIZ_ZIP + ".zip"):
        os.remove(RAIZ_ZIP + ".zip")
    faltan = []
    for o, d in ARCHIVOS:
        src = os.path.join(RAIZ, o)
        if not os.path.exists(src):
            if o.startswith("docs/redsocial/"):
                print("AVISO (red social, no se aborta): falta", o)
                continue
            faltan.append(o)
            continue
        dst = os.path.join(RAIZ_ZIP, d)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    if faltan:
        sys.exit("faltan archivos:\n  - " + "\n  - ".join(faltan))
    open(os.path.join(RAIZ_ZIP, "LEEME.md"), "w", encoding="utf-8").write(LEEME + (LEEME_CMS if CON_CMS else "") + (LEEME_RSI if CON_RSI else ""))
    print("Comprobación frente a la lista del profesor:")
    mal = 0
    for que, carpeta, minimo in LISTA:
        ruta = os.path.join(RAIZ_ZIP, carpeta)
        n = len(os.listdir(ruta)) if os.path.isdir(ruta) else 0
        ok = n >= minimo
        mal += not ok
        print(f"  [{'ok' if ok else 'FALTA'}] {que}: {n} archivos (mínimo {minimo})")
    n_cu = len(D["usecases"])
    print(f"  [{'ok' if n_cu >= 8 else 'FALTA'}] REM {VERSION} con los 8 casos de uso: {n_cu} en dms_data.json")
    mal += n_cu < 8
    if mal:
        sys.exit(f"{mal} apartados de la lista no se cumplen: no se genera el zip")
    zip_ruta = os.path.join(PAQ, NOMBRE + ".zip")
    with zipfile.ZipFile(zip_ruta, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, fs in os.walk(RAIZ_ZIP):
            for f in fs:
                p = os.path.join(base, f)
                z.write(p, os.path.relpath(p, PAQ))
    print("zip:", zip_ruta, round(os.path.getsize(zip_ruta) / 1e6, 1), "MB,", len(ARCHIVOS) + 1, "archivos")


main()
