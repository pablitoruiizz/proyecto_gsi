"""Convierte a PDF los documentos de requisitos que exporta REMUS (CADUS__CRS.html y DMS__CRS.html), con Chrome.
Uso: python scripts/dms/rem_a_pdf.py   (requiere playwright y pymupdf; usa el Chrome instalado)"""
import os
import re
import tempfile

import pymupdf
from playwright.sync_api import sync_playwright

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TRABAJOS = [
    (os.path.join(RAIZ, "docs", "requisitos", "rem-remus", "CADUS__CRS.html"), os.path.join(RAIZ, "docs", "requisitos", "rem-remus", "REM-CADUS-v2.3.pdf")),
    (os.path.join(RAIZ, "docs", "dms", "rem-remus", "DMS__CRS.html"), os.path.join(RAIZ, "docs", "dms", "rem-remus", "REM-DMS-v1.1.pdf")),
]
# un REM por sección (opcional): si REMUS exportó DMS-<Seccion>__CRS.html en docs/dms/rem-remus/secciones, también se pasa a PDF
for _sec in ("Acta", "Normativa", "Expediente", "Votacion"):
    _h = os.path.join(RAIZ, "docs", "dms", "rem-remus", "secciones", f"DMS-{_sec}__CRS.html")
    if os.path.exists(_h):
        TRABAJOS.append((_h, os.path.join(RAIZ, "docs", "dms", "rem-remus", "secciones", f"REM-DMS-{_sec}-v1.1.pdf")))

# REM de la red social (Lab 5): si REMUS exportó RSI__CRS.html en docs/redsocial/rem-remus, también se pasa a PDF
_rsi_html = os.path.join(RAIZ, "docs", "redsocial", "rem-remus", "RSI__CRS.html")
if os.path.exists(_rsi_html):
    TRABAJOS.append((_rsi_html, os.path.join(RAIZ, "docs", "redsocial", "rem-remus", "REM-RSI-v1.0.pdf")))

# El REM del CMS solo se convierte si el HTML exportado es de la versión actual (2.3): un HTML antiguo daría un PDF engañoso.
_cms_html = TRABAJOS[0][0]
if not os.path.exists(_cms_html) or not re.search(r"Versi.n\s*2\.3", open(_cms_html, encoding="latin-1").read()):
    print("AVISO: CADUS__CRS.html no es la versión 2.3 del REM del CMS: abre CADUS.rem en REMUS, expórtalo y vuelve a ejecutar. No se genera REM-CADUS-v2.3.pdf.")
    TRABAJOS.pop(0)

# la función que convierte los enlaces del índice en enlaces directos y añade marcadores es la de build_html.py
fuente = open(os.path.join(RAIZ, "scripts", "entrega", "build_html.py"), encoding="utf-8").read()
trozo = fuente[fuente.index("def enlazar_pdf"):fuente.index("def paginas_de_titulos")]
exec(trozo, globals())


def a_pdf(html, destino):
    h = open(html, encoding="latin-1").read().replace(" (<em>(null)</em>)", "")
    h = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    ruta = os.path.join(tempfile.mkdtemp(), "rem.html")
    open(ruta, "w", encoding="latin-1", errors="replace").write(h)
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="chrome")
        pg = nav.new_page()
        pg.goto("file:///" + ruta.replace(os.sep, "/"), wait_until="networkidle")
        pg.pdf(path=destino, format="A4", print_background=True, margin={"top": "18mm", "bottom": "18mm", "left": "18mm", "right": "18mm"})
        nav.close()


for html, pdf in TRABAJOS:
    a_pdf(html, pdf)
    n = enlazar_pdf(pdf)
    print("generado", os.path.relpath(pdf, RAIZ), "·", len(pymupdf.open(pdf)), "páginas ·", n, "enlaces y marcadores")
