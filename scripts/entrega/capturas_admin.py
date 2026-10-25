"""Capturas de las pantallas de administración, una por rol, con cuentas temporales de prueba (sin contraseñas).
Reutiliza el ayudante de las pruebas de privacidad: crea un usuario temporal por rol con una sesión de 30 minutos y los borra al terminar.
Requiere: pip install playwright (usa el Chrome del sistema) y el servidor Wamp encendido.
Uso: python scripts/entrega/capturas_admin.py"""
import json
import os
import subprocess
import sys

from playwright.sync_api import sync_playwright

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PHP = os.path.join(RAIZ, "..", "..", "apps proyecto", "php", "php.exe")
HELPER = os.path.join(RAIZ, "scripts", "pruebas", "rn03_auditoria.php")
BASE = "http://localhost/proyecto_gsi/cms-wordpress"
SALIDA = os.path.join(RAIZ, "docs", "entrega", "img", "capturas2")
# (archivo, rol, ruta de wp-admin, alto de la captura)
PANTALLAS = [
    ("a01-plugins.jpg", "administrator", "/wp-admin/plugins.php?plugin_status=active", 1500),
    ("a02-roles.jpg", "administrator", "/wp-admin/admin.php?page=roles", 1000),
    ("a03-escritorio-ejecutivo.jpg", "cadus_ejecutiva", "/wp-admin/index.php", 1000),
    ("a04-escritorio-delegado.jpg", "cadus_delegado", "/wp-admin/index.php", 1000),
    ("a06-eventos.jpg", "cadus_ejecutiva", "/wp-admin/post-new.php?post_type=tribe_events", 1000),
    ("a07-votaciones.jpg", "cadus_ejecutiva", "/wp-admin/post-new.php?post_type=cadus_votacion", 1100),
]


def php(accion, datos=None):
    r = subprocess.run([PHP, HELPER, accion], input=json.dumps(datos or {}), capture_output=True, encoding="utf-8", cwd=RAIZ)
    if r.returncode:
        raise SystemExit(r.stdout + r.stderr)
    return json.loads(r.stdout)


estado = php("fixture")
try:
    with sync_playwright() as p:
        navegador = p.chromium.launch(channel="chrome")
        contextos = {}
        for archivo, rol, ruta, alto in PANTALLAS:
            if rol not in contextos:
                ctx = navegador.new_context(viewport={"width": 1920, "height": 1080})
                ctx.add_cookies([{"name": c.split("=", 1)[0], "value": c.split("=", 1)[1], "url": BASE + "/"}
                                 for c in estado["auth"][rol]["cookie"].split("; ")])
                contextos[rol] = ctx
            pagina = contextos[rol].new_page()
            pagina.set_viewport_size({"width": 1920, "height": alto})
            pagina.goto(BASE + ruta, wait_until="networkidle")
            pagina.wait_for_timeout(1200)
            for texto in ("Cerrar", "Dismiss"):  # avisos y ventanas de bienvenida de los plugins
                for boton in pagina.get_by_role("button", name=texto).all():
                    try:
                        boton.click(timeout=500)
                    except Exception:
                        pass
            if archivo.startswith("a07"):  # el panel de Yoast empuja los datos de la votación fuera de la captura
                pagina.add_style_tag(content="#wpseo_meta{display:none}")
            pagina.screenshot(path=os.path.join(SALIDA, archivo), type="jpeg", quality=85)
            print("ok", archivo, pagina.title())
            pagina.close()
        navegador.close()
finally:
    print("limpieza:", php("cleanup", estado))
