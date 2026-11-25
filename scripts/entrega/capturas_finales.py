"""Capturas de la entrega final (29/11/2026): el portal con el contenido real del CADUS (noticias, actas, normativa y calendario).
Escribe en docs/entrega/img/capturas4; no toca las capturas de la entrega 2 (capturas2).
Requiere: pip install playwright pillow (usa el Chrome del sistema) y el servidor Wamp encendido.
Uso: python scripts/entrega/capturas_finales.py"""
import os
import subprocess

from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SALIDA = os.path.join(RAIZ, "docs", "entrega", "img", "capturas4")
BASE = "http://localhost/proyecto_gsi/cms-wordpress"
MYSQL = os.path.join(RAIZ, "..", "..", "bin", "mysql", "mysql8.4.7", "bin", "mysql.exe")


def articulo():
    """Dirección de la noticia sobre el Pabellón libre de humo. Falla si no la encuentra: no se sustituye por otra página."""
    r = subprocess.run([MYSQL, "-uroot", "bd_cadus", "-N", "-e",
                        "select ID from wp_posts where post_type='post' and post_status='publish' and post_title like 'El Pabell%' limit 1"],
                       capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip().isdigit():
        raise SystemExit("No se encontró la noticia «El Pabellón de Uruguay será espacio libre de humo»: ¿está cargado el contenido real y WampServer encendido?")
    return f"/?p={r.stdout.strip()}"


# el parámetro cap evita la caché de WP Fastest Cache
PAGINAS = {
    "f01-portada": "/?cap=1",
    "f02-noticias": "/noticias/?cap=1",
    "f03-noticia": articulo(),
    "f04-actas-y-normativa": "/actas-y-normativa/?cap=1",
    "f05-calendario-septiembre": "/events/month/2026-09/?cap=1",
    "f06-calendario-proximos": "/events/list/?cap=1",
}
os.makedirs(SALIDA, exist_ok=True)
with sync_playwright() as p:
    navegador = p.chromium.launch(channel="chrome")
    pagina = navegador.new_page(viewport={"width": 1366, "height": 900}, reduced_motion="reduce")
    for nombre, ruta in PAGINAS.items():
        respuesta = pagina.goto(BASE + ruta, wait_until="networkidle", timeout=120000)
        if respuesta is None or respuesta.status >= 400:
            raise SystemExit(f"{nombre}: la página {ruta} respondió {respuesta.status if respuesta else 'sin respuesta'}: no se hace la captura")
        alto = pagina.evaluate("document.documentElement.scrollHeight")
        for y in range(0, alto, 600):
            pagina.evaluate(f"window.scrollTo(0, {y})")
            pagina.wait_for_timeout(120)
        pagina.evaluate("window.scrollTo(0, 0)")
        pagina.wait_for_timeout(400)
        destino = os.path.join(SALIDA, nombre + ".jpg")
        pagina.screenshot(path=destino, full_page=True, type="jpeg", quality=82)
        im = Image.open(destino)
        if nombre != "f01-portada":  # el pie granate es igual en todas: solo se deja en la portada
            y = im.height
            while y > 0 and im.getpixel((2, y - 1)) == (141, 7, 57):
                y -= 1
            im.crop((0, 0, im.width, y)).convert("RGB").save(destino, quality=82)
        print(nombre, pagina.title()[:60], Image.open(destino).size)
    navegador.close()
