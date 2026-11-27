"""Genera los seis manuales (usuario y administrador de CMS, DMS y red social) en docs/manuales/entrega:
Word (.docx) a partir de docs/manuales/NN-*.md. El PDF se exporta con scripts/entrega/exportar_manuales_pdf.ps1 (Microsoft Word).
Reutiliza las utilidades de scripts/dms/build_doc_dms.py. Una captura que falte se avisa y se marca en el documento.
Uso: python scripts/entrega/build_manuales.py"""
import glob
import os
import re
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "scripts", "dms"))
import build_doc_dms as B  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402
from PIL import Image  # noqa: E402

ORIGEN = os.path.join(RAIZ, "docs", "manuales")
SALIDA = os.path.join(ORIGEN, "entrega")
NOMBRES = {"01": "Manual-usuario-CMS-CADUS", "02": "Manual-administrador-CMS-CADUS", "03": "Manual-usuario-DMS-CADUS",
           "04": "Manual-administrador-DMS-CADUS", "05": "Manual-usuario-RSI-CADUS", "06": "Manual-administrador-RSI-CADUS"}
ANCHO_MAX, ALTO_MAX = 15.5, 10.5  # cm: las capturas de página completa son muy altas y se limitan por la altura


def campo(par, instruccion):
    """Inserta un campo de Word (PAGE, TOC...) que Word actualiza al abrir o al exportar."""
    for tipo, texto in (("begin", None), (None, instruccion), ("separate", None), (None, "1"), ("end", None)):
        r = par.add_run()
        if tipo:
            f = OxmlElement("w:fldChar")
            f.set(qn("w:fldCharType"), tipo)
            r._r.append(f)
        else:
            if texto == instruccion:
                t = OxmlElement("w:instrText")
                t.set(qn("xml:space"), "preserve")
            else:
                t = OxmlElement("w:t")
            t.text = texto
            r._r.append(t)


def figura(doc, ruta, pie):
    B.Num.fig += 1
    ancho, alto = Image.open(ruta).size
    w = min(ANCHO_MAX, ALTO_MAX * ancho / alto)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(ruta, width=Cm(w))
    p.paragraph_format.keep_with_next = True
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = c.add_run(f"Figura {B.Num.fig}. {pie}")
    r.italic = True
    r.font.size = Pt(9)


def numerada(doc, n, texto):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.9)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    p.paragraph_format.space_after = Pt(3)
    p.add_run(f"{n}. ")
    for x in re.split(r"(\*\*.+?\*\*)", texto.replace("`", "")):
        if x.startswith("**") and x.endswith("**"):
            p.add_run(x[2:-2]).bold = True
        else:
            p.add_run(x)


def pie_pagina(doc, titulo):
    sec = doc.sections[0]
    p = sec.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"{titulo} · página ")
    r.font.size = Pt(8.5)
    campo(p, "PAGE")


def construir(ruta):
    doc = B.nuevo()
    B.Num.fig = 0
    B.Num.tab = 0
    lineas = open(ruta, encoding="utf-8").read().splitlines()
    titulo = lineas[0].lstrip("# ").strip()
    pie_pagina(doc, titulo)
    i = 1
    portada = False
    while i < len(lineas):
        l = lineas[i].rstrip()
        img = re.match(r"!\[(.*)\]\((.+)\)$", l.strip())
        if not portada and not l.startswith("## "):
            i += 1  # lo anterior a la primera sección es el subtítulo, que va en la portada
            continue
        if not l.strip():
            pass
        elif l.startswith("## ") and not portada:
            # primera sección: antes se pone la portada con el índice
            doc.add_heading(titulo, 0)
            sub = next((x for x in lineas[1:i] if x.strip()), "")
            B.par(doc, sub, cursiva=True, tam=10)
            B.par(doc, "Contenido", negrita=True, tam=12)
            toc = doc.add_paragraph()
            campo(toc, 'TOC \\o "1-2" \\h \\z \\u')
            doc.add_page_break()
            portada = True
            continue
        elif l.startswith("#### "):
            doc.add_heading(l[5:].strip(), 4)
        elif l.startswith("### "):
            doc.add_heading(l[4:].strip(), 3)
        elif l.startswith("## "):
            doc.add_heading(l[3:].strip(), 1)
        elif img:
            pie, archivo = img.group(1), os.path.normpath(os.path.join(os.path.dirname(ruta), img.group(2)))
            if os.path.exists(archivo):
                figura(doc, archivo, pie)
            else:
                B.par(doc, f"[Falta la captura {os.path.basename(archivo)}: {pie}]", cursiva=True)
                B.aviso(f"{os.path.basename(ruta)}: falta la captura {os.path.relpath(archivo, RAIZ)}")
        elif l.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                if not re.match(r"^\|[\s:|-]+\|$", lineas[i].strip()):
                    filas.append(B.celdas(lineas[i]))
                i += 1
            B.tabla(doc, filas[0], filas[1:], tam=9)
            continue
        elif re.match(r"^\d+\. ", l):
            n, texto = l.split(". ", 1)
            numerada(doc, n, texto)
        elif re.match(r"^[-*] ", l):
            B.vineta(doc, l[2:].replace("`", ""))
        elif l.startswith("   ") and not l.strip():
            pass
        else:
            B.par(doc, l)
        i += 1
    return doc


def main():
    os.makedirs(SALIDA, exist_ok=True)
    for ruta in sorted(glob.glob(os.path.join(ORIGEN, "0*.md"))):
        nombre = os.path.splitext(os.path.basename(ruta))[0]
        doc = construir(ruta)
        destino = os.path.join(SALIDA, NOMBRES[nombre[:2]] + ".docx")
        doc.save(destino)
        print("docx:", os.path.relpath(destino, RAIZ))
    for a in B.AVISOS:
        print("AVISO:", a)


if __name__ == "__main__":
    main()
