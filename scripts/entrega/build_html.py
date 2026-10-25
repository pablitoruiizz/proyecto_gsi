"""Genera el PDF de la entrega con el aspecto de los documentos de REMUS (mismo CSS, portada, índice y tablas).

El capítulo 3 es el documento de requisitos que exporta REMUS (docs/requisitos/rem-remus/CADUS__CRS.html), incrustado tal cual;
el resto de capítulos reutiliza el contenido de build_doc.py con un «doc» que escribe HTML en lugar de Word.
Requiere: pip install playwright pillow numpy pymupdf python-docx (usa el Chrome del sistema).
Uso: python scripts/entrega/build_html.py   → docs/entrega/Entrega2-CMS-CADUS-REMUS.pdf
"""
import ast
import html
import json
import os
import re
import tempfile

import numpy as np
import pymupdf
from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENTREGA = os.path.join(RAIZ, "docs", "entrega")
IMG = os.path.join(ENTREGA, "img")
CAP = os.path.join(IMG, "capturas")
FECHA_DATOS = "24/10/2026"
SALIDA_PDF = os.path.join(ENTREGA, "Entrega2-CMS-CADUS-REMUS.pdf")
HTML_REM = os.path.join(RAIZ, "docs", "requisitos", "rem-remus", "CADUS__CRS.html")
CSS_DIR = os.path.join(os.path.dirname(__file__), "estilo_remus")
TMP = tempfile.mkdtemp(prefix="entrega_html_")

datos = json.load(open(os.path.join(RAIZ, "scripts", "remus", "cadus_data.json"), encoding="utf-8"))
plugins = {p["slug"]: p for p in json.load(open(os.path.join(ENTREGA, "datos", "plugins.json"), encoding="utf-8"))}
temas = {t["slug"]: t for t in json.load(open(os.path.join(ENTREGA, "datos", "themes.json"), encoding="utf-8"))}

out = []          # fragmentos HTML en orden
lista = [False]   # ¿hay un <ul> abierto?
figura_n, tabla_n = [0], [0]
titulos = []      # (nivel, id, texto) para el índice


# ------------------------------------------------------------------ «doc» y utilidades que escriben HTML
def cerrar_lista():
    if lista[0]:
        out.append("</ul>")
        lista[0] = False


def emitir(trozo):
    cerrar_lista()
    out.append(trozo)


def inline(texto):
    t = html.escape(str(texto), quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", t)


class Doc:
    def add_heading(self, texto, nivel):
        ident = f"H{len(titulos) + 1}"
        titulos.append((nivel, ident, texto))
        if nivel == 1 and len(titulos) > 1:
            emitir('<div class="pagebreak"></div>')
        emitir(f'<h{nivel} id="{ident}" class="section">{html.escape(texto, quote=False)}</h{nivel}>')


doc = Doc()


def par(texto="", negrita=False, cursiva=False, color=None, tam=None, alin=None, estilo=None, despues=None):
    if not texto:
        return
    t = inline(texto)
    if negrita:
        t = f"<b>{t}</b>"
    if cursiva:
        t = f"<i>{t}</i>"
    emitir(f"<p>{t}</p>")


def rico(texto, estilo=None):
    emitir(f"<p>{inline(texto)}</p>")


def vineta(texto):
    if not lista[0]:
        out.append("<ul>")
        lista[0] = True
    out.append(f"<li>{inline(texto)}</li>")


def tabla(cabecera, filas, anchos, tam=8.5, titulo=None, resaltar=None):
    clase = "plan matriz" if titulo and titulo.startswith("Trazabilidad") else "plan"
    if titulo:
        tabla_n[0] += 1
        emitir(f'<p class="matrix_caption"><span class="matrix_caption_label">Tabla {tabla_n[0]}.</span> {inline(titulo)}</p>')
    total = sum(anchos)
    cols = "".join(f'<col style="width:{a * 100 / total:.1f}%">' for a in anchos)
    cab = "".join(f"<th>{inline(h)}</th>" for h in cabecera)
    cuerpo = []
    for fila in filas:
        negro = " class=\"resaltada\"" if resaltar and resaltar(fila) else ""
        cuerpo.append(f"<tr{negro}>" + "".join(f"<td>{inline(v)}</td>" for v in fila) + "</tr>")
    emitir(f'<table class="remus_table {clase}" style="font-size:{tam + 2:.1f}pt"><colgroup>{cols}</colgroup>'
           f"<thead><tr>{cab}</tr></thead><tbody>{''.join(cuerpo)}</tbody></table>")


def figura(archivo, texto, ancho=16.5, carpeta=IMG, max_h=22.0, caja=None):
    ruta = os.path.join(carpeta, archivo)
    if caja:
        base = Image.open(ruta)
        ruta = os.path.join(TMP, f"trozo_{caja[0]}_{archivo}")
        base.crop((0, caja[0], base.width, caja[1])).convert("RGB").save(ruta, quality=90)
    w, h = Image.open(ruta).size
    ancho = min(ancho, max_h * w / h)
    figura_n[0] += 1
    emitir(f'<div class="figure"><img class="figure_image" src="file:///{ruta.replace(os.sep, "/")}" style="width:{ancho:.1f}cm">'
           f'<p class="figure_caption"><span class="figure_caption_label">Figura {figura_n[0]}.</span> {inline(texto)}</p></div>')
    return figura_n[0]


def salto():
    emitir('<div class="pagebreak"></div>')


# ------------------------------------------------------------------ funciones auxiliares de build_doc.py (se copian tal cual)
FUENTE = open(os.path.join(os.path.dirname(__file__), "build_doc.py"), encoding="utf-8").read()
arbol = ast.parse(FUENTE)
ns = dict(os=os, re=re, json=json, np=np, Image=Image, RAIZ=RAIZ, ENTREGA=ENTREGA, IMG=IMG, CAP=CAP, FECHA_DATOS=FECHA_DATOS,
          datos=datos, plugins=plugins, temas=temas, doc=doc, par=par, rico=rico, vineta=vineta, tabla=tabla, figura=figura,
          salto=salto, figura_n=figura_n, tabla_n=tabla_n)
for nodo in arbol.body:
    if isinstance(nodo, ast.FunctionDef) and nodo.name in {"cortes", "leer_seccion", "md_linea", "millar", "fecha", "estrellas", "comparar", "parsear_tablas"}:
        exec(compile(ast.get_source_segment(FUENTE, nodo), f"build_doc:{nodo.name}", "exec"), ns)


def marca(sufijo):
    m = re.search(r"^# -{20,} " + re.escape(sufijo) + r"$", FUENTE, re.M)
    assert m, sufijo
    return m.start()


bloque_a = FUENTE[marca("resumen"):marca("3. REM")]
bloque_b = FUENTE[marca("4. análisis"):marca("pie de página")]


# ------------------------------------------------------------------ capítulo 3: el documento de REMUS, incrustado
def capitulo_rem():
    h = open(HTML_REM, encoding="latin-1").read()
    h = h[h.index('<h1 id="SEC-0001"'):h.index("</body>")]
    h = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    h = re.sub(r'<div class="pagebreak"></div>', "", h)
    # REMUS escribe «(null)» tras los pasos de los casos de uso cuando no tienen comentario (build_rem.ps1 ya lo rellena con «Ninguno»)
    h = h.replace(" (<em>(null)</em>)", "")
    # los capítulos de REMUS pasan a ser subapartados 3.x: un nivel más de encabezado y número con prefijo
    titulos.append((1, "H_REM", "3. Requisitos (REM)"))  # antes que sus subapartados, para que el índice salga en orden
    def sube(m):
        nivel = int(m.group(1)) + 1
        numero, resto = m.group(4), m.group(5)
        ident = m.group(2)
        titulos.append((nivel, ident, f"3.{numero} {resto}"))
        return f'<h{nivel} id="{ident}" class="{m.group(3)}">3.{numero} {resto}</h{nivel}>'
    h = re.sub(r'<h([1-4]) id="([^"]+)" class="([^"]*)">(\d+(?:\.\d+)*)\s+(.*?)</h\1>', sube, h, flags=re.S)
    nivel_max = 5
    emitir('<div class="pagebreak"></div>')
    emitir('<h1 id="H_REM" class="section">3. Requisitos (REM)</h1>')
    rico("Este capítulo reproduce, sin cambios, el documento de requisitos que genera REMUS a partir de CADUS.rem (versión 2.0, 24/10/2026), "
         "con su estructura de cinco dimensiones (información, interfaz, funcionales, no funcionales y reglas de negocio), los actores, los casos de uso, "
         "las restricciones del entorno y el glosario. Su numeración interna (1 a 7) pasa a ser 3.1 a 3.7. El documento completo de REMUS se entrega además aparte (CADUS-REM-v2.pdf).")
    rico("Una diferencia conocida: el código de ticket (CAD-AAAA-NNNNN) y la referencia de mediación (MED-AAAA-NNNNN) llevan en el portal un sufijo aleatorio de 32 caracteres hexadecimales que el REM aún no recoge; se incorporará al validarlo con el cliente. "
         "La entrevista con el CADUS prevista para confirmar los requisitos no se ha realizado: el REM queda marcado como pendiente de validar con el cliente, lo que incluye el plazo de conservación de los datos, la lista de cuentas reales y el logotipo oficial.")
    emitir(h)


# ------------------------------------------------------------------ ensamblado
def portada():
    equipo = "".join(f"<tr><td>{html.escape(s['name'])}</td><td>{html.escape(s['role'])}</td></tr>" for s in datos["stakeholders"][1:])
    return f"""<div id="document_cover">
<div id="project_name">Proyecto CADUS</div>
<div id="document_logo"><img alt="Universidad de Sevilla" src="https://cdn.jsdelivr.net/gh/amador-duran-toro/rem/assets/images/logo_us.gif"></div>
<div id="document_name">Portal web del CADUS<br><span style="font-size:large;font-weight:normal">Sistema 1 · CMS en WordPress · Gestión de Sistemas de Información</span></div>
<div id="document_version">Entrega 2 · Versión final</div>
<div id="document_date">Fecha 25/10/2026</div>
<div id="document_prepared_for">Preparado para:<p>CADUS - Consejo de Alumnos de la Universidad de Sevilla</p></div>
<div id="document_prepared_by" style="margin-bottom:30pt">Preparado por:<p>Equipo de proyecto GSI</p></div>
<table class="remus_table stakeholder" style="width:80%;margin:0 auto;font-size:10pt;text-align:left"><thead><tr><th>Integrante</th><th>Rol SCRUM / Área</th></tr></thead><tbody>{equipo}</tbody></table>
</div>"""


def indice(paginas):
    items = []
    n1, n2 = 0, 0
    for nivel, ident, texto in titulos:
        if nivel > 2:
            continue
        pag = paginas.get(ident, "")
        sangria = "" if nivel == 1 else ' style="margin-left:2em"'
        items.append(f'<li{sangria}><a href="#{ident}">{html.escape(texto, quote=False)}</a> <span class="pag">{pag}</span></li>')
    return '<nav id="toc" role="navigation"><h1>Índice</h1><ul class="toc_list toc_list_level_1">' + "".join(items) + "</ul></nav>"


ESTILO_EXTRA = """
body { font-size: 11pt; }
div.pagebreak { page-break-after: always; }
h1.section, h2.section, h3.section, h4.section { page-break-after: avoid; break-after: avoid; }
table.plan td { text-align: left; }
nav#toc li { list-style: none; line-height: 135%; font-weight: normal; }
nav#toc ul.toc_list_level_1 > li:not([style]) { font-weight: bold; margin-top: 4pt; }
nav#toc .pag { float: right; }
table.plan > thead > tr { background-color: lightcyan; }
table.plan.matriz > thead > tr { background-color: lightgoldenrodyellow; }
table.remus_table { page-break-inside: auto; margin-bottom: 12pt; }
table.remus_table tr { page-break-inside: avoid; }
table.remus_table thead { display: table-header-group; }
table.remus_table th { text-align: left; }
table.remus_table tr.resaltada td { font-weight: bold; }
p.matrix_caption, p.figure_caption { font-size: 10pt; text-align: center; margin-bottom: 6pt; }
div.figure { page-break-inside: avoid; margin: 8pt 0; }
img.figure_image { max-width: 100%; height: auto; }
code { font-size: 9.5pt; }
body > div { margin-top: 0; margin-bottom: 0; }
"""


def construir(paginas):
    out.clear()
    titulos.clear()
    lista[0] = False
    figura_n[0] = tabla_n[0] = 0
    exec(compile(bloque_a, "build_doc:2-secciones", "exec"), ns)
    capitulo_rem()
    exec(compile(bloque_b, "build_doc:4-8-secciones", "exec"), ns)
    cerrar_lista()
    cuerpo = "".join(out)
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Portal web del CADUS — Entrega 2</title>'
            f'<link rel="stylesheet" href="file:///{CSS_DIR.replace(os.sep, "/")}/remus.css"><link rel="stylesheet" href="file:///{CSS_DIR.replace(os.sep, "/")}/madeja.css">'
            f"<style>{ESTILO_EXTRA}</style></head><body>{portada()}<div class=\"pagebreak\"></div>{indice(paginas)}<div class=\"pagebreak\"></div>{cuerpo}</body></html>")


def rem_pdf(destino):
    """El documento de REMUS tal cual (solo sin el «(null)» de los pasos), para entregarlo aparte."""
    h = open(HTML_REM, encoding="latin-1").read().replace(" (<em>(null)</em>)", "")
    h = re.sub(r"<script.*?</script>", "", h, flags=re.S).replace('charset="iso-8859-1"', 'charset="iso-8859-1"')
    ruta = os.path.join(TMP, "rem.html")
    open(ruta, "w", encoding="latin-1", errors="replace").write(h)
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="chrome")
        pg = nav.new_page()
        pg.goto("file:///" + ruta.replace(os.sep, "/"), wait_until="networkidle")
        pg.pdf(path=destino, format="A4", print_background=True, margin={"top": "18mm", "bottom": "18mm", "left": "18mm", "right": "18mm"})
        nav.close()


def a_pdf(contenido, destino):
    ruta = os.path.join(TMP, "entrega.html")
    open(ruta, "w", encoding="utf-8").write(contenido)
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="chrome")
        pg = nav.new_page()
        pg.goto("file:///" + ruta.replace(os.sep, "/"), wait_until="networkidle")
        pg.pdf(path=destino, format="A4", print_background=True, display_header_footer=True,
               margin={"top": "18mm", "bottom": "20mm", "left": "18mm", "right": "18mm"},
               header_template="<span></span>",
               footer_template='<div style="font-size:8pt;width:100%;text-align:center;color:#555">Portal CADUS · Entrega 2 (CMS) · Página <span class="pageNumber"></span> de <span class="totalPages"></span></div>')
        nav.close()


def paginas_de_titulos(pdf):
    """Página de cada encabezado: se busca su texto desde donde empieza el cuerpo (tras el índice), siempre hacia delante."""
    d = pymupdf.open(pdf)
    cursor = next(i for i in range(2, len(d)) if d[i].get_text().strip().startswith("Resumen del estado de la entrega"))
    paginas = {}
    for nivel, ident, texto in titulos:
        if nivel > 2:
            continue
        for i in range(cursor, len(d)):
            if d[i].search_for(texto[:60]):
                paginas[ident] = i + 1
                cursor = i
                break
    return paginas


if __name__ == "__main__":
    vacio = {}
    a_pdf(construir(vacio), SALIDA_PDF)
    # el índice ocupa lo mismo con o sin números: segunda pasada con las páginas reales
    paginas = paginas_de_titulos(SALIDA_PDF)
    a_pdf(construir(paginas), SALIDA_PDF)
    rem_pdf(os.path.join(ENTREGA, "paquete", "CADUS-REM-v2.pdf"))
    d = pymupdf.open(SALIDA_PDF)
    print("generado", SALIDA_PDF, "·", len(d), "páginas ·", figura_n[0], "figuras ·", tabla_n[0], "tablas")
