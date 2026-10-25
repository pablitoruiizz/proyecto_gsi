"""Captura a página completa las páginas públicas del portal (sin sesión) con el Chrome instalado.
Requiere: pip install playwright pillow (no descarga navegadores: usa el Chrome del sistema) y el servidor Wamp encendido.
Uso: python scripts/entrega/capturas_publicas.py"""
import os

from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SALIDA = os.path.join(RAIZ, "docs", "entrega", "img", "capturas2")
BASE = "http://localhost/proyecto_gsi/cms-wordpress"
PAGINAS = {
    "p01-portada": "/", "p02-que-es-el-cadus": "/que-es-el-cadus/", "p03-noticias": "/noticias/",
    "p04-actas-y-normativa": "/actas-y-normativa/", "p05-delegaciones": "/delegaciones/",
    "p06-atencion-al-estudiante": "/atencion-al-estudiante/", "p07-buzon": "/atencion-al-estudiante/buzon-de-consultas/",
    "p08-seguimiento": "/atencion-al-estudiante/seguimiento-de-ticket/", "p09-faq": "/atencion-al-estudiante/preguntas-frecuentes/",
    "p10-privacidad": "/aviso-de-privacidad/", "p11-votaciones": "/votaciones/",
    "p12-mediacion": "/atencion-al-estudiante/mediacion-estudiantil/", "p13-calendario": "/events/", "p14-contacto": "/contacto/",
}
os.makedirs(SALIDA, exist_ok=True)
with sync_playwright() as p:
    navegador = p.chromium.launch(channel="chrome")
    pagina = navegador.new_page(viewport={"width": 1366, "height": 900}, reduced_motion="reduce")
    for nombre, ruta in PAGINAS.items():
        pagina.goto(BASE + ruta, wait_until="networkidle")
        # fuerza la carga de imágenes diferidas y de las secciones que aparecen al hacer scroll
        alto = pagina.evaluate("document.documentElement.scrollHeight")
        for y in range(0, alto, 600):
            pagina.evaluate(f"window.scrollTo(0, {y})")
            pagina.wait_for_timeout(120)
        pagina.evaluate("window.scrollTo(0, 0)")
        pagina.wait_for_timeout(400)
        destino = os.path.join(SALIDA, nombre + ".jpg")
        pagina.screenshot(path=destino, full_page=True, type="jpeg", quality=82)
        im = Image.open(destino)
        if nombre != "p01-portada":  # el pie (granate) es igual en todas las páginas: solo se deja en la portada
            y = im.height
            while y > 0 and im.getpixel((2, y - 1)) == (141, 7, 57):
                y -= 1
            im.crop((0, 0, im.width, y)).convert("RGB").save(destino, quality=82)
        print(nombre, Image.open(destino).size)
    navegador.close()
