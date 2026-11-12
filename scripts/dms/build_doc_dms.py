"""Genera los documentos de la entrega del DMS en docs/dms/entrega:
  - Entrega-DMS-CADUS.docx (REM, análisis, diseño, casos de uso, implementación en SharePoint, trazabilidad y SCRUM)
  - casos-de-uso/CU-*.docx (versión definitiva: un documento por sección con 2 casos de uso cada uno, 8 en total)
Cada documento de casos de uso sale de docs/dms/casos-de-uso/<nombre>.md, que escribe su autor (reparto de la versión
definitiva). Si el .md aún no existe, se genera con los datos de este script. Los pasos de cada caso deben coincidir con
scripts/remus/dms_data.json: el script avisa de cada diferencia, de cada caso que falte en el JSON y de cada captura que falte.
Uso: python scripts/dms/build_doc_dms.py   (después, scripts/dms/exportar_pdf.ps1 para los PDF)
     python scripts/dms/build_doc_dms.py --comprobar   (solo comprueba, sin generar nada)"""
import csv
import json
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DMS = os.path.join(RAIZ, "docs", "dms")
IMG = os.path.join(DMS, "img")
CAP = os.path.join(DMS, "capturas")
SAL = os.path.join(DMS, "entrega")
os.makedirs(os.path.join(SAL, "casos-de-uso"), exist_ok=True)
D = json.load(open(os.path.join(RAIZ, "scripts", "remus", "dms_data.json"), encoding="utf-8"))
AZUL = RGBColor(0x1F, 0x3A, 0x5F)
VERSION = ".".join(str(n) for n in D["version"])  # versión del REM del DMS (1.1 en la versión definitiva)
FECHA_ENTREGA = "15/11/2026"  # pendiente de confirmar con el profesor (tarea D-09)
CU_MD = os.path.join(DMS, "casos-de-uso")
AVISOS = []


def aviso(texto):
    AVISOS.append(texto)


# ------------------------------------------------------------------ utilidades de Word
def nuevo():
    Num.fig = 0
    Num.tab = 0
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2)
    sec.top_margin = sec.bottom_margin = Cm(2)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    for n, tam in (("Heading 1", 17), ("Heading 2", 13.5), ("Heading 3", 11.5)):
        h = doc.styles[n]
        h.font.name = "Calibri"
        h.font.size = Pt(tam)
        h.font.bold = True
        h.font.color.rgb = AZUL
        h.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    return doc


def sombrear(celda, color):
    tcPr = celda._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), color)
    tcPr.append(sh)


class Num:
    fig = 0
    tab = 0


def par(doc, texto, negrita=False, cursiva=False, tam=None, alinear=None):
    p = doc.add_paragraph()
    texto = texto.replace("`", "")
    partes = re.split(r"(\*\*.+?\*\*)", texto)
    for x in partes:
        if x.startswith("**") and x.endswith("**"):
            r = p.add_run(x[2:-2]); r.bold = True
        else:
            r = p.add_run(x); r.bold = negrita
        r.italic = cursiva
        if tam:
            r.font.size = Pt(tam)
    if alinear:
        p.alignment = alinear
    p.paragraph_format.space_after = Pt(6)
    return p


def vineta(doc, texto):
    p = doc.add_paragraph(style="List Bullet")
    partes = re.split(r"(\*\*.+?\*\*)", texto)
    for x in partes:
        if x.startswith("**") and x.endswith("**"):
            p.add_run(x[2:-2]).bold = True
        else:
            p.add_run(x)
    return p


def tabla(doc, cabecera, filas, anchos=None, titulo=None, tam=9):
    if titulo:
        Num.tab += 1
        p = doc.add_paragraph()
        r = p.add_run(f"Tabla {Num.tab}. {titulo}"); r.bold = True; r.font.size = Pt(9.5)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_after = Pt(3)
    t = doc.add_table(rows=1, cols=len(cabecera))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(cabecera):
        celda = t.rows[0].cells[i]
        celda.text = ""
        r = celda.paragraphs[0].add_run(c); r.bold = True; r.font.size = Pt(tam); r.font.color.rgb = RGBColor(255, 255, 255)
        sombrear(celda, "1F3A5F")
    for f in filas:
        cel = t.add_row().cells
        for i, v in enumerate(f):
            cel[i].text = ""
            r = cel[i].paragraphs[0].add_run(str(v).replace("`", "").replace("**", "")); r.font.size = Pt(tam)
    if anchos:
        for fila in t.rows:
            for i, a in enumerate(anchos):
                fila.cells[i].width = Cm(a)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def figura(doc, ruta, pie, ancho=16.5):
    Num.fig += 1
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(ruta, width=Cm(ancho))
    p.paragraph_format.keep_with_next = True
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = c.add_run(f"Figura {Num.fig}. {pie}"); r.italic = True; r.font.size = Pt(9)


# ------------------------------------------------------------------ burndown
def burndown(n=1, titulo="Burndown del Sprint 1 del DMS (26/10 – 08/11/2026)"):
    ruta = os.path.join(DMS, "burndown", f"sprint-0{n}.csv")
    filas = list(csv.DictReader(open(ruta, encoding="utf-8")))
    x = [f["fecha"][5:] for f in filas]
    ideal = [float(f["ideal_sp"]) for f in filas]
    real = [(i, float(f["real_sp"])) for i, f in enumerate(filas) if f["real_sp"] != ""]
    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=130)
    ax.plot(range(len(x)), ideal, "--", color="#888", label="Ideal")
    ax.plot([i for i, _ in real], [v for _, v in real], "-o", color="#1f3a5f", lw=2, label="Real")
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=45, fontsize=8)
    ax.set_ylabel("Puntos de historia pendientes")
    ax.set_title(titulo, fontsize=11, color="#1f3a5f", fontweight="bold")
    ax.grid(alpha=.3)
    ax.legend()
    sal = os.path.join(IMG, "burndown-dms.png" if n == 1 else f"burndown-dms-sprint-0{n}.png")
    fig.savefig(sal, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return sal


# ------------------------------------------------------------------ datos de los 4 tipos de documento
CAPS = {
    "01": ("01-sitios-y-bibliotecas.jpg", "Los tres sitios de grupo del DMS y sus bibliotecas en SharePoint de la US (sección «Compilar», «De su propiedad»).",
           "Se crearon los sitios «CADUS Documentación pública», «CADUS Órganos de gobierno» y «CADUS Atención al estudiante», cada uno con su biblioteca de documentos (Normativa, Actas y Votaciones, Expedientes). Cada sitio de grupo trae los grupos Propietarios, Integrantes y Visitantes que pide el Lab 4 y tiene 5 miembros: Pablo como propietario y los otros cuatro integrantes del equipo. Responde a RF-D01 y RF-D06 (DMS-HU-01)."),
    "02": ("02-normativa.jpg", "Biblioteca Normativa con sus columnas de metadatos.",
           "La biblioteca guarda la normativa del CADUS. Además del nombre, cada documento tiene las columnas Tipo de documento (obligatoria, con valor Normativa por defecto), Fecha, Curso académico y Estado (Vigente o Derogada). En la captura se ve un reglamento derogado junto a dos vigentes. Responde a RF-D02 y RN-D06 (DMS-HU-02)."),
    "03": ("03-normativa-vigente.jpg", "Vista plana «Vigente» de la biblioteca Normativa.",
           "La vista «Vigente» recorre la biblioteca sin carpetas y filtra por Estado = Vigente, así que el reglamento derogado desaparece. Es el filtro por metadatos de CU-D03 y de RF-D05 (DMS-HU-03 y DMS-HU-05)."),
    "04": ("04-actas.jpg", "Biblioteca Actas vista por la Ejecutiva (propietario): borrador y acta aprobada.",
           "La biblioteca Actas tiene activada la aprobación de contenido y la visibilidad de borradores solo para autor y aprobadores. La Ejecutiva ve a la vez el acta aprobada del pleno del 12/10 y el borrador de la asamblea del 26/10, con sus columnas Tipo de documento, Fecha, Curso académico y Asamblea. Responde a RF-D03 y RN-D01 (DMS-HU-04)."),
    "05": ("05-actas-aprobadas.jpg", "Vista plana «Aprobadas» de la biblioteca Actas.",
           "La vista «Aprobadas» filtra por estado de aprobación y solo muestra el acta aprobada, que es lo que debe ver un delegado en CU-D02. El borrador de la asamblea del 26/10 no aparece. Responde a RF-D03, RF-D05 y RN-D01."),
    "06": ("06-votaciones.jpg", "Biblioteca Votaciones con las columnas propias del registro de votación.",
           "La biblioteca Votaciones añade las columnas Número de votación, Tipo de voto (Nominal o Secreto) y Resultado. Los dos registros de ejemplo son de la misma asamblea: la votación 1 nominal y la 2 secreta. Los documentos no contienen números de DNI y, en la secreta, solo el recuento total. Responde a CU-D06, RN-D04 y RN-D05 (DMS-HU-07). En la biblioteca «Plantillas» del mismo sitio hay una plantilla de acta y otra de registro de votación con una fila por cada una de las 27 delegaciones (RF-D09)."),
    "07": ("07-permisos-votaciones.jpg", "Permisos exclusivos de la biblioteca Votaciones.",
           "La biblioteca Votaciones rompe la herencia de permisos del sitio: «Esta biblioteca tiene permisos exclusivos». Solo conserva Propietarios (control total) e Integrantes (editar); se ha quitado el grupo Visitantes, en el que irán los delegados, para que no vean los registros de votación. Responde a RF-D06 y RN-D04."),
    "08": ("08-expedientes.jpg", "Biblioteca Expedientes del sitio Atención al estudiante.",
           "La biblioteca guarda los expedientes de reclamaciones y mediaciones resueltos, con las columnas Tipo de documento, Fecha, Curso académico, Código (CAD-… o MED-…), Facultad, Estado y Fecha de resolución, más la fecha de caducidad calculada. Tiene también permisos exclusivos, sin el grupo Visitantes (RN-D02). Responde a CU-D04 y RF-D01 (DMS-HU-06)."),
    "09": ("09-expedientes-caducados.jpg", "Vista plana «Caducados» de la biblioteca Expedientes.",
           "La columna Fecha de caducidad es calculada (fecha de resolución más 2 años). La vista «Caducados» filtra los expedientes cuya caducidad es anterior a hoy: aparece el MED-2024-0002, resuelto el 10/05/2024 y caducado desde el 10/05/2026. Es lo que la Ejecutiva revisa cada mes para retirar los expedientes (CU-D05, RF-D07, RF-D08, RN-D03)."),
    # Versión definitiva (Sprint 2 del DMS). Cada autor puede cambiar el texto en su .md de casos de uso.
    "10": ("10-cu-d05-eliminar.jpg", "CU-D05: eliminación del expediente caducado desde la vista «Caducados».",
           "La Ejecutiva elimina el expediente MED-2024-0002 desde la vista «Caducados». Al eliminar el documento se eliminan también todas sus versiones. Paso 3 de CU-D05 (RN-D03)."),
    "11": ("11-cu-d05-papelera.jpg", "CU-D05: papelera de reciclaje del sitio Atención al estudiante.",
           "El expediente eliminado pasa a la papelera del sitio y se elimina también de ella. Paso 3 de CU-D05 (RN-D03)."),
    "12": ("12-cu-d05-papelera-segunda-fase.jpg", "CU-D05: papelera de segunda fase sin el expediente.",
           "SharePoint guarda lo que se borra de la papelera del sitio en la papelera de segunda fase. Se vacía también, y la vista «Caducados» queda sin expedientes: ya no se conserva ninguna copia (paso 4 y postcondición de CU-D05, RN-D03 y RNF-D04)."),
    "13": ("13-cu-d07-nueva-version.jpg", "CU-D07: nueva versión de una norma y la anterior derogada.",
           "La biblioteca Normativa con las columnas Norma y Versión: la versión nueva está vigente y la anterior ha pasado a derogada; la vista «Vigente» solo muestra la nueva (CU-D07, RN-D07)."),
    "14": ("14-cu-d08-votaciones-filtradas.jpg", "CU-D08: registros de votación filtrados por asamblea y tipo de voto.",
           "La Ejecutiva filtra los registros de la biblioteca Votaciones por asamblea y tipo de voto; Asamblea y Número de votación son obligatorias para poder distinguirlos (CU-D08, RN-D04, RN-D05)."),
}

TIPOS = [
    {"archivo": "CU-Acta", "nombre": "Acta de pleno o asamblea", "cus": ["CU-D01", "CU-D02"], "sitio": "CADUS Órganos de gobierno", "biblioteca": "Actas",
     "desc": "Documento que recoge lo tratado y acordado en un pleno o una asamblea. Se redacta a partir de una plantilla, queda en borrador hasta que la Ejecutiva la aprueba y solo entonces la ven los delegados.",
     "meta": [["Tipo de documento", "Elección (Acta)", "Sí"], ["Fecha", "Fecha", "Sí"], ["Curso académico", "Elección", "No"], ["Asamblea", "Texto", "No"], ["Estado de aprobación", "Nativo de SharePoint (borrador, aprobada)", "Automático"], ["Resumen", "Generado automáticamente (RF-D10, deseable)", "No"]],
     "permisos": "Propietarios (cuenta del CADUS): leer y escribir. Visitantes (delegados, con la cuenta de su delegación): leer, solo las actas aprobadas. Los borradores solo los ven el autor y los aprobadores.",
     "caps": ["04", "05"], "reglas": ["RN-D01"], "ejemplo": "Acta del pleno del 12-10-2026 (ejemplo).docx (aprobada) y Acta de la asamblea del 26-10-2026 (ejemplo, borrador).docx"},
    {"archivo": "CU-Normativa", "nombre": "Normativa y estatutos", "cus": ["CU-D03", "CU-D07"], "sitio": "CADUS Documentación pública", "biblioteca": "Normativa",
     "desc": "Normas, reglamentos y estatutos del CADUS. De cada norma solo hay una versión vigente; al publicar una nueva, la anterior pasa a derogada y se conserva como referencia.",
     "meta": [["Tipo de documento", "Elección (Normativa)", "Sí"], ["Fecha", "Fecha", "Sí"], ["Curso académico", "Elección", "No"], ["Norma", "Texto (identifica la misma norma entre versiones)", "Sí"], ["Versión", "Número", "Sí"], ["Estado", "Elección (Vigente, Derogada)", "Sí"]],
     "permisos": "Propietarios: leer y escribir. Visitantes (estudiantes con su correo @alum.us.es y delegados con la cuenta de su delegación): solo lectura.",
     "caps": ["02", "03", "13"], "reglas": ["RN-D06", "RN-D07"], "ejemplo": "Estatutos del CADUS (ejemplo).docx, Reglamento de votaciones (ejemplo).docx y un reglamento derogado"},
    {"archivo": "CU-Expediente", "nombre": "Expediente de reclamación o mediación", "cus": ["CU-D04", "CU-D05"], "sitio": "CADUS Atención al estudiante", "biblioteca": "Expedientes",
     "desc": "Expediente de una reclamación o mediación ya resuelta. Se conserva 2 años desde su resolución como prueba y luego se retira. Solo lo ve la Ejecutiva.",
     "meta": [["Tipo de documento", "Elección (Expediente)", "Sí"], ["Fecha", "Fecha", "Sí"], ["Curso académico", "Elección", "No"], ["Código", "Texto (CAD-… o MED-…)", "No"], ["Facultad", "Elección", "No"], ["Estado", "Elección (Resuelto)", "Sí"], ["Fecha de resolución", "Fecha (obligatoria: de ella depende la caducidad)", "Sí"], ["Fecha de caducidad", "Calculada: resolución + 2 años", "Automático"]],
     "permisos": "Permisos exclusivos: Propietarios (control total) e Integrantes (editar, solo el equipo con datos de ejemplo). Sin el grupo Visitantes.",
     "caps": ["08", "09", "10", "11", "12"], "reglas": ["RN-D02", "RN-D03"], "ejemplo": "CAD-2026-0001 (ejemplo).docx y MED-2024-0002 (ejemplo, caducado).docx"},
    {"archivo": "CU-Votacion", "nombre": "Registro de votación", "cus": ["CU-D06", "CU-D08"], "sitio": "CADUS Órganos de gobierno", "biblioteca": "Votaciones",
     "desc": "Resultado de una votación presencial de asamblea, con un voto por delegación (27 delegaciones). No guarda el DNI y, si la votación es secreta, solo el recuento total.",
     "meta": [["Tipo de documento", "Elección (Votación)", "Sí"], ["Fecha", "Fecha", "Sí"], ["Curso académico", "Elección", "No"], ["Asamblea", "Texto", "Sí"], ["Número de votación", "Número", "Sí"], ["Tipo de voto", "Elección (Nominal, Secreto)", "Sí"], ["Resultado", "Elección (Aprobada, Rechazada)", "No"]],
     "permisos": "Permisos exclusivos: Propietarios (control total) e Integrantes (editar, el equipo del proyecto). Sin el grupo Visitantes: los delegados no ven los registros.",
     "caps": ["06", "07", "14"], "reglas": ["RN-D04", "RN-D05"], "ejemplo": "Votación 1 (nominal, ejemplo).docx y Votación 2 (secreta, ejemplo).docx"},
]
CU = {u["id"]: u for u in D["usecases"]}
DOC_DE = {c: t for t in TIPOS for c in t["cus"]}
# Trazabilidad: historia, elemento de SharePoint, capturas y estado de cada caso. Actualizar tras cada prueba cruzada.
TRAZA = {
    "CU-D01": ("DMS-HU-01, 02, 04", "Biblioteca Actas con aprobación de contenido; plantilla de acta", "4", "Configurado y observado"),
    "CU-D02": ("DMS-HU-03, 04", "Vista plana Aprobadas", "5", "Configurado; falta probar con un visitante"),
    "CU-D03": ("DMS-HU-03, 05", "Vista plana Vigente de Normativa", "3", "Configurado y observado"),
    "CU-D04": ("DMS-HU-06", "Biblioteca Expedientes (permisos exclusivos)", "8", "Configurado y observado"),
    "CU-D05": ("DMS-HU-06", "Vista plana Caducados, columna calculada y papeleras", "9-12", "Configurado; pendiente la ejecución del 13/11"),
    "CU-D06": ("DMS-HU-07", "Biblioteca Votaciones (permisos exclusivos) y plantilla de votación", "6, 7", "Configurado y observado"),
    "CU-D07": ("DMS-HU-08", "Columnas Norma y Versión en Normativa y vista Vigente", "13", "Pendiente (Sprint 2 del DMS)"),
    "CU-D08": ("DMS-HU-09", "Votaciones con Asamblea y Número de votación obligatorias; filtros", "14", "Pendiente (Sprint 2 del DMS)"),
}
ACT = {a["id"]: a["name"] for a in D["actors"]}
RF = {r["id"]: r for r in D["functional"]}


def actores_de(cu):
    if cu["id"] == "CU-D03":
        return ["Delegado", "Estudiante"]
    return sorted({ACT[s["actor"]] for s in cu["steps"] if s["who"] == "actor"})


def pasos_de(cu):
    return [f"{ACT[s['actor']] if s['who'] == 'actor' else 'El sistema'} {s['text']}." for s in cu["steps"]]


def bloque_cu(doc, cu, nivel=2):
    if isinstance(cu, str):  # el caso aún no está en dms_data.json (lo añade Pablo en la versión 1.1)
        doc.add_heading(cu, nivel)
        par(doc, f"[Pendiente: {cu} todavía no está en scripts/remus/dms_data.json.]", cursiva=True)
        aviso(f"{cu} no está en dms_data.json")
        return
    doc.add_heading(f"{cu['id']} {cu['name']}", nivel)
    actores = actores_de(cu)
    tabla(doc, ["Campo", "Contenido"], [["Actor", ", ".join(actores)], ["Cuándo", cu["trigger"][0].upper() + cu["trigger"][1:]], ["Precondición", cu["pre"]], ["Postcondición", cu["post"]]], [3.5, 13.5], tam=9)
    par(doc, "**Pasos**")
    for i, paso in enumerate(pasos_de(cu), 1):
        par(doc, f"{i}. {paso}")
    trazas = next((t[1] for t in D["traces"] if t[0] == cu["id"]), [])
    par(doc, "**Requisitos relacionados:** " + ", ".join(trazas))


def celdas(l):
    return [c.strip() for c in l.strip().strip("|").split("|")]


def md_a_docx(ruta):
    """Convierte el documento de casos de uso escrito en Markdown: títulos, párrafos, tablas, listas e imágenes."""
    doc = nuevo()
    base = os.path.dirname(ruta)
    lineas = open(ruta, encoding="utf-8-sig").read().splitlines()
    i = 0
    while i < len(lineas):
        l = lineas[i].rstrip()
        img = re.match(r"!\[(.*)\]\((.+)\)$", l.strip())
        if not l.strip():
            pass
        elif l.startswith("#"):
            nivel = len(l) - len(l.lstrip("#"))
            doc.add_heading(l.lstrip("#").strip(), 0 if nivel == 1 else nivel - 1)
        elif img:
            pie, archivo = img.group(1), os.path.normpath(os.path.join(base, img.group(2)))
            if os.path.exists(archivo):
                figura(doc, archivo, pie, 16)
            else:
                par(doc, f"[Falta la captura {os.path.basename(archivo)}: {pie}]", cursiva=True)
                aviso(f"{os.path.basename(ruta)}: falta la captura {os.path.relpath(archivo, RAIZ)}")
        elif l.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                if not re.match(r"^\|[\s:|-]+\|$", lineas[i].strip()):
                    filas.append(celdas(lineas[i]))
                i += 1
            n = len(filas[0])
            anchos = {2: [4, 13], 3: [5, 9, 3], 4: [2.5, 2.5, 7, 5]}.get(n)
            tabla(doc, filas[0], filas[1:], anchos, tam=9)
            continue
        elif re.match(r"^[-*] ", l):
            vineta(doc, l[2:].replace("`", ""))
        else:
            if l.startswith("PENDIENTE"):
                aviso(f"{os.path.basename(ruta)}: {l[:90]}")
            primera = i == 1 or (i == 2 and not lineas[1].strip())
            par(doc, l, cursiva=primera, tam=9.5 if primera else None)
        i += 1
    return doc


def normal(paso):
    """Compara pasos sin tener en cuenta el artículo inicial, las mayúsculas ni el punto final."""
    paso = re.sub(r"^(la|el|los|las)\s+", "", paso.strip().lower())
    return paso.rstrip(".")


def comprobar_md(tipo):
    """Avisa si los casos o sus pasos del .md no coinciden con dms_data.json."""
    ruta = os.path.join(CU_MD, tipo["archivo"] + ".md")
    if not os.path.exists(ruta):
        aviso(f"{tipo['archivo']}.md no existe todavía: se genera con los datos del script")
        return
    texto = open(ruta, encoding="utf-8-sig").read()
    secciones = re.split(r"^### ", texto, flags=re.M)[1:]
    vistos = []
    for sec in secciones:
        m = re.match(r"(CU-D\d+)", sec)
        if not m:
            continue
        cid = m.group(1)
        vistos.append(cid)
        if cid not in CU:
            aviso(f"{tipo['archivo']}.md: {cid} no está en dms_data.json")
            continue
        pasos_md = [re.sub(r"^\d+\.\s*", "", x.strip()) for x in sec.splitlines() if re.match(r"^\d+\.\s", x.strip())]
        pasos_json = pasos_de(CU[cid])
        if [normal(x) for x in pasos_md] != [normal(x) for x in pasos_json]:
            aviso(f"{tipo['archivo']}.md: los pasos de {cid} no coinciden con dms_data.json ({len(pasos_md)} en el .md, {len(pasos_json)} en el JSON)")
    if vistos != tipo["cus"]:
        aviso(f"{tipo['archivo']}.md: tiene {', '.join(vistos) or 'ningún caso'} y debería tener {', '.join(tipo['cus'])}")


def doc_cu(tipo):
    ruta_md = os.path.join(CU_MD, tipo["archivo"] + ".md")
    if os.path.exists(ruta_md):
        doc = md_a_docx(ruta_md)
        sal = os.path.join(SAL, "casos-de-uso", tipo["archivo"] + ".docx")
        doc.save(sal)
        return sal
    doc = nuevo()
    t = doc.add_heading(f"Casos de uso — {tipo['nombre']}", 0)
    par(doc, f"DMS del CADUS · Lab 4 · Universidad de Sevilla (GSI) · versión {VERSION}", cursiva=True, tam=9.5)
    doc.add_heading("1. Documento", 1)
    par(doc, tipo["desc"])
    tabla(doc, ["Dato", "Valor"], [["Sitio de SharePoint", tipo["sitio"]], ["Biblioteca", tipo["biblioteca"]], ["Casos de uso", ", ".join(tipo["cus"])], ["Reglas de negocio", ", ".join(tipo["reglas"]) or "—"], ["Documentos de ejemplo", tipo["ejemplo"]]], [4, 13], tam=9)
    doc.add_heading("2. Metadatos", 1)
    tabla(doc, ["Metadato", "Tipo de columna", "Obligatorio"], tipo["meta"], [5, 9, 3], tam=9)
    doc.add_heading("3. Permisos", 1)
    par(doc, tipo["permisos"])
    doc.add_heading("4. Casos de uso", 1)
    for c in tipo["cus"]:
        bloque_cu(doc, CU.get(c, c), 2)
    doc.add_heading("5. Implementación en SharePoint", 1)
    for k in tipo["caps"]:
        captura(doc, k)
    sal = os.path.join(SAL, "casos-de-uso", tipo["archivo"] + ".docx")
    doc.save(sal)
    return sal


def captura(doc, k, titulo=False):
    arch, pie, texto = CAPS[k]
    if titulo:
        doc.add_heading(f"{int(k)}. {pie.rstrip('.')}", 3)
    par(doc, texto)
    ruta = os.path.join(CAP, arch)
    if os.path.exists(ruta):
        figura(doc, ruta, pie, 16)
    else:
        par(doc, f"[Falta la captura {arch}]", cursiva=True)
        aviso(f"falta la captura docs/dms/capturas/{arch}")


# ------------------------------------------------------------------ documento de la entrega
def backlog():
    filas = []
    for l in open(os.path.join(DMS, "backlog", "product-backlog.md"), encoding="utf-8"):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) == 8 and c[0].startswith("DMS-HU"):
            filas.append([c[0], c[1], c[2], c[4], c[5], c[7]])
    return filas


def entrega():
    doc = nuevo()
    doc.add_heading("DMS del CADUS — Entrega del sistema de gestión documental", 0)
    par(doc, "Gestión de Sistemas de Información (GSI) · Universidad de Sevilla · Lab 4 (DMS)", cursiva=True)
    par(doc, "Equipo: Pablo Ruiz Vidal (Product Owner), Joaquín Luna Canela (Scrum Master), Miguel Ángel Camacho Martín, Álvaro Martínez Ocaña y Marcos-Paban Delgado Rodríguez. Cliente: CADUS (contacto: Miguel Ángel Camacho Martín).")
    par(doc, f"Versión definitiva · REM del DMS versión {VERSION} · fecha de entrega: {FECHA_ENTREGA}")

    doc.add_heading("1. Resumen", 1)
    par(doc, "El DMS guarda y organiza los documentos internos del CADUS —actas, normativa, expedientes de reclamaciones y registros de votación— en **SharePoint de Microsoft 365 de la Universidad de Sevilla**. Es independiente del portal web (CMS): tiene su propio REM, análisis, diseño, implementación y seguimiento SCRUM. Los requisitos salen de la entrevista con el CADUS del 26/10/2026.")
    tabla(doc, ["Contenido pedido para el DMS", "Dónde está"], [
        ["Requisitos (REM)", "Sección 2 y proyecto REMUS `DMS.rem` (más la hoja `carga-remus.md`)"],
        ["Documentos de análisis (UML)", "Sección 3 (UML de análisis y casos de uso)"],
        ["Documentos de diseño (UML)", "Sección 4 (UML de diseño y del análisis al diseño)"],
        ["Documentos de casos de uso, divididos por secciones", f"Sección 5 y carpeta `casos-de-uso`: {len(TIPOS)} documentos con 2 casos de uso cada uno ({sum(len(t['cus']) for t in TIPOS)} en total)"],
        ["Documentos de implementación (SharePoint)", f"Sección 6: {len(CAPS)} capturas explicadas una a una"],
        ["Seguimiento SCRUM del DMS", "Sección 8: product backlog, sprint backlog y burndown"],
        ["Entrevista con el cliente", "Sección 2.9 y anexo (sección 10); también como documento aparte"]], [7, 10])

    doc.add_heading("2. Requisitos (REM)", 1)
    par(doc, f"El REM se mantiene en REMUS (`DMS.rem`, versión {VERSION}) a partir de `scripts/remus/dms_data.json`. Cada requisito lleva un código que se repite en el UML, en los casos de uso, en las capturas y en la trazabilidad.")
    doc.add_heading("2.1 Objetivos", 2)
    tabla(doc, ["Código", "Objetivo", "El sistema deberá"], [[o["id"], o["name"], o["description"]] for o in D["objectives"]], [2, 4, 11], tam=9)
    doc.add_heading("2.2 Actores", 2)
    tabla(doc, ["Código", "Actor", "Representa a"], [[a["id"], a["name"], a["role"]] for a in D["actors"]], [2, 4, 11], tam=9)
    doc.add_heading("2.3 Requisitos de información", 2)
    tabla(doc, ["Código", "Concepto", "Datos"], [[r["id"], r["name"], "; ".join(r["data"])] for r in D["information"]], [2, 3.5, 11.5], tam=8.5)
    doc.add_heading("2.4 Requisitos de interfaz y funcionales", 2)
    tabla(doc, ["Código", "Nombre", "El sistema deberá", "Historia"], [[r["id"], r["name"], r["description"], r["comments"]] for r in D["ui"] + D["functional"]], [1.8, 3.4, 9.2, 2.6], tam=8.5)
    doc.add_heading("2.5 Requisitos no funcionales", 2)
    tabla(doc, ["Código", "Nombre", "El sistema deberá"], [[r["id"], r["name"], r["description"]] for r in D["nonfunctional"]], [2, 3.5, 11.5], tam=9)
    doc.add_heading("2.6 Reglas de negocio", 2)
    tabla(doc, ["Código", "Nombre", "Regla"], [[r["id"], r["name"], r["description"]] for r in D["rules"]], [2, 3.5, 11.5], tam=9)
    doc.add_heading("2.7 Restricciones del entorno", 2)
    tabla(doc, ["Código", "Nombre", "Descripción"], [[r["id"], r["name"], r["description"]] for r in D["environment"]], [2, 4, 11], tam=9)
    doc.add_heading("2.8 Casos de uso", 2)
    filas_cu = []
    for c in sorted(DOC_DE):
        if c in CU:
            u = CU[c]
            filas_cu.append([f"{c} {u['name']}", " o ".join(actores_de(u)), u["trigger"][0].upper() + u["trigger"][1:], DOC_DE[c]["nombre"]])
        else:
            filas_cu.append([c, "Pendiente del REM " + VERSION, "", DOC_DE[c]["nombre"]])
            aviso(f"{c} no está en dms_data.json")
    tabla(doc, ["Caso de uso", "Quién", "Cuándo", "Documento"], filas_cu, [6.5, 3, 4.5, 3], tam=9)
    doc.add_heading("2.9 Origen de los requisitos: la entrevista", 2)
    par(doc, "Las respuestas del cliente que moldean el DMS (entrevista del 26/10/2026): las votaciones son presenciales, solo votan los delegados con un voto por delegación y se comprueba la identidad con el DNI; no se publican resultados en el portal; los tickets y mediaciones se conservan 2 años desde que se resuelven; todas las consultas deben tratarse con total privacidad; y todo pasa por la Ejecutiva, que usa la cuenta única del CADUS. El texto completo está en `docs/cliente/entrevista-cliente.md`.")

    doc.add_heading("3. Análisis", 1)
    par(doc, "El UML de análisis recoge los conceptos del Lab 4: documento (con sus cuatro tipos), carpeta, rol, permiso, búsqueda y metadato. Las etiquetas en rojo son los códigos de requisito.")
    figura(doc, os.path.join(IMG, "uml-dms-analisis.png"), "UML de análisis del DMS con etiquetas de trazabilidad.", 17)
    par(doc, "El diagrama de casos de uso relaciona cada actor con los casos de uso que ejecuta. Los casos se dividen por secciones, una por tipo de documento, y cada una tiene dos casos de uso.")
    figura(doc, os.path.join(IMG, "casos-de-uso-dms.png"), "Casos de uso del DMS.", 16)

    doc.add_heading("4. Diseño", 1)
    par(doc, "En el diseño cada concepto del análisis pasa a un elemento de SharePoint: los documentos tienen columnas de metadatos, las carpetas son sitios y bibliotecas, los roles son grupos de permisos y la búsqueda es una búsqueda genérica más vistas planas con filtros.")
    figura(doc, os.path.join(IMG, "uml-dms-diseno.png"), "UML de diseño del DMS en SharePoint.", 17)
    tabla(doc, ["Concepto del análisis", "Elemento del diseño en SharePoint"], [
        ["Documento", "Documento de una biblioteca, con columnas de metadatos"],
        ["Carpeta", "Sitio de grupo y biblioteca de documentos"],
        ["Rol (Ejecutiva, Delegado, Estudiante)", "Grupo de permisos: Propietarios, Integrantes y Visitantes"],
        ["Permiso", "Permiso del grupo sobre el sitio o la biblioteca (permisos exclusivos en Votaciones y Expedientes)"],
        ["Búsqueda", "Búsqueda de SharePoint por nombre y contenido"],
        ["Metadato", "Columna de la biblioteca (elección, fecha, texto, número o calculada)"],
        ["Filtro", "Vista plana de la biblioteca con filtro por metadatos (Vigente, Aprobadas, Caducados)"]], [6.5, 10.5], tam=9, titulo="Del análisis al diseño")
    doc.add_heading("4.1 Metadatos y vistas por biblioteca", 2)
    tabla(doc, ["Sitio", "Biblioteca", "Columnas propias", "Vista plana"], [
        ["Documentación pública", "Normativa", "Tipo de documento, Fecha, Curso académico, Estado", "Vigente (Estado = Vigente)"],
        ["Órganos de gobierno", "Actas", "Tipo de documento, Fecha, Curso académico, Asamblea; aprobación de contenido", "Aprobadas (estado de aprobación = Aprobado)"],
        ["Órganos de gobierno", "Votaciones", "Tipo de documento, Fecha, Curso académico, Asamblea, Número de votación, Tipo de voto, Resultado", "Todas las votaciones"],
        ["Atención al estudiante", "Expedientes", "Tipo de documento, Fecha, Curso académico, Código, Facultad, Estado, Fecha de resolución, Fecha de caducidad (calculada)", "Caducados (caducidad anterior a hoy)"]], [3.3, 2.7, 7.3, 3.7], tam=8.5, titulo="Bibliotecas, columnas y vistas")

    doc.add_heading("5. Documentos de casos de uso", 1)
    par(doc, f"Se entregan **{len(TIPOS)} documentos de casos de uso**, uno por sección (tipo de documento), con **dos casos de uso cada uno**. Cada documento describe el tipo de documento, sus metadatos, sus permisos por rol, sus casos de uso paso a paso con su actor y su escenario, y las capturas de SharePoint donde se ven.")
    tabla(doc, ["Documento de casos de uso", "Casos de uso", "Biblioteca"], [[f"{t['archivo']}.docx — {t['nombre']}", ", ".join(t["cus"]), f"{t['sitio']} · {t['biblioteca']}"] for t in TIPOS], [7.5, 3.5, 6], tam=9)
    for t in TIPOS:
        doc.add_heading(t["nombre"], 2)
        par(doc, t["desc"])
        for c in t["cus"]:
            if c not in CU:
                par(doc, f"**{c}.** [Pendiente: todavía no está en dms_data.json.]")
                continue
            u = CU[c]
            par(doc, f"**{c} {u['name']}.** " + " ".join(f"{i}. {(ACT[s['actor']] if s['who'] == 'actor' else 'El sistema')} {s['text']}." for i, s in enumerate(u["steps"], 1)))

    doc.add_heading("6. Implementación en SharePoint", 1)
    par(doc, "Capturas del entorno real (`uses0.sharepoint.com`), con documentos de ejemplo ficticios. Cada una indica los requisitos y la historia a la que responde.")
    for k in sorted(CAPS):
        captura(doc, k, titulo=True)

    doc.add_heading("7. Trazabilidad", 1)
    filas_t = []
    for c in sorted(TRAZA):
        req = next((t[1] for t in D["traces"] if t[0] == c), [])
        req = [r for r in req if r.startswith(("RF-", "RN-", "RNF-"))]
        hu, elem, cap, estado = TRAZA[c]
        filas_t.append([c, ", ".join(req) or "Pendiente del REM " + VERSION, hu, elem, cap, estado])
    tabla(doc, ["Caso de uso", "Requisitos", "Historia", "Elemento de SharePoint", "Captura", "Estado"], filas_t, [1.6, 3.8, 2.4, 4.6, 1.2, 3.4], tam=8.5, titulo="Casos de uso, requisitos, historias y SharePoint")
    n_trazas = sum(len(t[1]) for t in D["traces"])
    par(doc, f"Los objetivos y los requisitos de información están enlazados con los requisitos y casos de uso en las trazas de `DMS.rem` ({n_trazas} trazas).")

    doc.add_heading("8. Seguimiento SCRUM del DMS", 1)
    par(doc, "El DMS tiene su propio product backlog, sprint backlog y burndown, independientes de los del CMS. Sprint 1 del DMS: 26/10 – 08/11/2026 (24 SP). Sprint 2 del DMS, la versión definitiva: 13/11 – 15/11/2026 (4 SP y las tareas D-07 a D-09).")
    doc.add_heading("8.1 Product backlog", 2)
    tabla(doc, ["ID", "Historia", "Requisitos", "SP", "Estado", "Responsable"], backlog(), [2, 6.5, 3, 1, 2.5, 2], tam=8)
    doc.add_heading("8.2 Sprint backlog", 2)
    tabla(doc, ["Integrante", "Historias del DMS", "SP"], [["Pablo", "DMS-HU-01", 5], ["Joaquín", "DMS-HU-02, DMS-HU-05", 7], ["Miguel Ángel", "DMS-HU-04, DMS-HU-07", 6], ["Álvaro", "DMS-HU-03", 3], ["Marcos", "DMS-HU-06", 3]], [4, 10, 2], tam=9)
    par(doc, "Tareas sin puntos: D-01 REM en REMUS (Pablo), D-02 y D-03 UML de análisis y diseño (Álvaro), D-04 capturas (todos), D-05 seguimiento SCRUM (Joaquín) y D-06 este documento (Pablo).")
    doc.add_heading("8.3 Burndown del sprint", 2)
    figura(doc, burndown(), "Burndown chart del Sprint 1 del DMS: puntos pendientes por día frente a la línea ideal.", 14)
    doc.add_heading("8.4 Sprint 2 del DMS: versión definitiva", 2)
    par(doc, "Lo que pidió el profesor sobre lo entregado: dividir los casos de uso por roles o secciones y añadir dos casos en cada documento. Se añaden CU-D07 (nueva versión de una norma) y CU-D08 (consultar votaciones anteriores) y cada documento queda con dos casos. Nadie prueba lo que escribió.")
    tabla(doc, ["Integrante", "Trabajo del Sprint 2 del DMS"], [
        ["Pablo", "D-09 (fecha y alcance con el profesor), REM 1.1 y DMS.rem, prueba de CU-Normativa"],
        ["Joaquín", "CU-Normativa con CU-D07 (DMS-HU-08, 2 SP), backlog y burndown, prueba de CU-Votacion"],
        ["Miguel Ángel", "CU-Acta, validación de CU-D07 y CU-D08 con el CADUS, prueba con un visitante"],
        ["Álvaro", "CU-Votacion con CU-D08 (DMS-HU-09, 2 SP), UML y diagrama de casos de uso, prueba de CU-Expediente y del rol estudiante"],
        ["Marcos", "CU-Expediente y ejecución de CU-D05, generador y zip (D-08), prueba de CU-Acta, revisión del REM"]], [3.5, 13.5], tam=9)
    if os.path.exists(os.path.join(DMS, "burndown", "sprint-02.csv")):
        figura(doc, burndown(2, "Burndown del Sprint 2 del DMS (13/11 – 15/11/2026)"), "Burndown chart del Sprint 2 del DMS.", 12)
    par(doc, "La configuración de las siete historias se hizo en bloque el 30/10 y el burndown no se actualizó los días anteriores: repite la lección de los sprints del CMS. Según la definición de hecho del sprint (caso de uso ejecutado por otra persona y permisos comprobados con cada rol), ninguna historia está todavía cerrada: seis están configuradas a la espera de la prueba cruzada y DMS-HU-04 espera además una cuenta de delegado. Por eso el burndown sigue en 24 SP; bajará cuando el equipo cierre las pruebas.")

    doc.add_heading("9. Pendiente y limitaciones", 1)
    for t in ("Probar los permisos con una cuenta real de delegación: sin ella, la prueba se hace con un integrante pasado a Visitantes y se anota que no es una cuenta de delegación real.",
              "Añadir la cuenta del CADUS (dcadus@us.es) como propietaria de los tres sitios.",
              "Anotar el resultado de cada prueba cruzada (fecha, persona y resultado) en el documento de casos de uso correspondiente.",
              "RF-D10 (resumen automático del acta) es deseable y no se ha implementado.",
              "Los documentos de ejemplo son ficticios; los datos reales los aporta el CADUS.",
              "Estado de verificación: lo que está **configurado** (sitios, columnas, vistas y permisos), **observado** (capturas) y **probado** (por otra persona o con otra cuenta) no es lo mismo; la tabla de trazabilidad indica el estado de cada caso."):
        vineta(doc, t)
    anexo_entrevista(doc)
    sal = os.path.join(SAL, "Entrega-DMS-CADUS.docx")
    doc.save(sal)
    return sal


# ------------------------------------------------------------------ entrevista con el cliente
def leer_entrevista():
    """Lee docs/cliente/entrevista-cliente.md: cabecera, bloques de preguntas y tabla de consecuencias."""
    lineas = open(os.path.join(RAIZ, "docs", "cliente", "entrevista-cliente.md"), encoding="utf-8").read().splitlines()
    cab, bloques, tabla_c, cur, modo = [], [], [], None, "cab"
    i = 0
    while i < len(lineas):
        l = lineas[i].strip()
        if l.startswith("## Qué cambia"):
            modo = "tabla"
        elif l.startswith("## "):
            cur = {"titulo": re.sub(r"^## \d+\.\s*", "", l), "preguntas": []}
            bloques.append(cur)
            modo = "bloque"
        elif modo == "cab" and l and not l.startswith("#"):
            cab.append(l.replace("**", ""))
        elif modo == "bloque" and l.startswith("**") and l.endswith("**"):
            q = re.sub(r"^\*\*(\d+)\.\s*", r"\1. ", l)[:-2]
            resp = []
            i += 1
            while i < len(lineas) and lineas[i].strip() and not lineas[i].strip().startswith("**"):
                resp.append(lineas[i].strip())
                i += 1
            cur["preguntas"].append((q, " ".join(resp)))
            continue
        elif modo == "tabla" and l.startswith("|") and not l.startswith("|---"):
            tabla_c.append([c.strip().replace("`", "") for c in l.strip("|").split("|")])
        i += 1
    return cab, bloques, tabla_c


def cuerpo_entrevista(doc, nivel):
    cab, bloques, tabla_c = leer_entrevista()
    for c in cab:
        par(doc, c)
    for b in bloques:
        doc.add_heading(b["titulo"], nivel + 1)
        for q, r in b["preguntas"]:
            par(doc, "**" + q + "**")
            par(doc, r)
    if tabla_c:
        doc.add_heading("Qué cambia en el proyecto según las respuestas", nivel)
        tabla(doc, tabla_c[0], tabla_c[1:], [6.2, 8.3, 2.5], tam=8.5)


def entrevista_docx():
    doc = nuevo()
    doc.add_heading("Entrevista con el CADUS", 0)
    par(doc, "Gestión de Sistemas de Información (GSI) · Universidad de Sevilla · requisitos del CMS y del DMS", cursiva=True, tam=9.5)
    cuerpo_entrevista(doc, 1)
    sal = os.path.join(SAL, "Entrevista-CADUS.docx")
    doc.save(sal)
    return sal


def anexo_entrevista(doc):
    doc.add_heading("10. Anexo: entrevista con el CADUS", 1)
    par(doc, "Texto completo de la entrevista con el cliente en la que se basan los requisitos del DMS y los cambios del CMS. También se adjunta como documento aparte (Entrevista-CADUS).")
    cuerpo_entrevista(doc, 2)


def informe():
    vistos = []
    for a in AVISOS:
        if a not in vistos:
            vistos.append(a)
    print(f"\nREM del DMS versión {VERSION}: {len(CU)} casos en dms_data.json, {sum(len(t['cus']) for t in TIPOS)} en los documentos")
    if vistos:
        print(f"AVISOS ({len(vistos)}):")
        for a in vistos:
            print("  -", a)
    else:
        print("Sin avisos: los documentos están listos para el zip.")
    return len(vistos)


if __name__ == "__main__":
    import sys
    for t in TIPOS:
        comprobar_md(t)
    if "--comprobar" not in sys.argv:
        for t in TIPOS:
            print("generado", doc_cu(t))
        print("generado", entrevista_docx())
        print("generado", entrega())
    informe()
