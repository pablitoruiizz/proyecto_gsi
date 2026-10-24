"""Batería externa de privacidad de tickets (RN-03 / HU-09b). Solo biblioteca estándar.

Pruebas HTTP como visitante anónimo (sin cookies) y de capacidades por rol sobre un ticket de prueba
(código CAD-2026-99999, texto «TEXTO-SECRETO-RN03») que se crea y se borra siempre al terminar.
Uso: python scripts/pruebas/privacidad_tickets.py   (con Wamp en marcha; ajusta PHP si no está en esta ruta)
Salida: una línea por prueba (OK / FALLO / SIN CONCLUIR) y código de salida 1 si algo falla.
"""
import http.cookiejar
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "http://localhost/proyecto_gsi/cms-wordpress"
PHP = r"C:\Users\ruizv\OneDrive\Escritorio\UNI\GSI\apps proyecto\php\php.exe"
AYUDA = str(Path(__file__).with_name("ticket_prueba.php"))
SECRETOS = ["TEXTO-SECRETO-RN03", "CAD-2026-99999", "prueba@alum.us.es", "Asunto de prueba"]
sys.stdout.reconfigure(encoding="utf-8")
resultados = []


def php(*args):
    r = subprocess.run([PHP, AYUDA, *args], capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip(), r.stderr.strip()


def pedir(ruta, datos=None, opener=None, cabeceras=None):
    """Devuelve (estado, cuerpo, cabeceras). No sigue errores como excepciones."""
    url = ruta if ruta.startswith("http") else BASE + ruta
    peticion = urllib.request.Request(url, data=urllib.parse.urlencode(datos).encode() if datos else None, headers=cabeceras or {})
    opener = opener or urllib.request.build_opener()
    try:
        with opener.open(peticion, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), dict(e.headers)


def comprobar(nombre, ok, detalle=""):
    resultados.append(ok)
    print(("OK      " if ok else "FALLO   ") + nombre + (f"  [{detalle}]" if detalle else ""))


def sin_fugas(nombre, ruta, secretos=None):
    """Falla si la respuesta contiene datos del ticket. En las búsquedas WordPress refleja el propio término buscado,
    así que ahí se comprueban solo los datos que NO forman parte de la consulta."""
    estado, cuerpo, _ = pedir(ruta)
    fugas = [s for s in (secretos or SECRETOS) if s.lower() in cuerpo.lower()]
    # Un error de servidor no prueba nada: un 500 sin los textos no cuenta como correcto.
    comprobar(nombre, estado < 500 and not fugas, f"HTTP {estado}" + (f", fuga: {fugas}" if fugas else ""))
    return estado, cuerpo


def main():
    out, err = php("crear")
    if not out.isdigit():
        print("No se pudo crear el ticket de prueba:", out, err)
        return 2
    tid = out
    try:
        print(f"Ticket de prueba ID {tid}\n-- Visitante anónimo: URLs directas, búsqueda, feeds, sitemaps")
        # datos del ticket que no coinciden con el término buscado (el término sí se refleja legítimamente)
        distintos = ["Asunto de prueba", "detalle de la reclamación de prueba"]
        for ruta in ["/?s=TEXTO-SECRETO-RN03", "/?s=TEXTO-SECRETO-RN03&post_type=cadus_ticket", "/?s=CAD-2026-99999",
                     "/?s=prueba%40alum.us.es", "/?s=reclamaci%C3%B3n+de+prueba&post_type=cadus_ticket"]:
            sin_fugas(f"búsqueda anónima {ruta}", ruta, secretos=distintos)
        for ruta in [f"/?p={tid}", f"/?post_type=cadus_ticket&p={tid}", "/?post_type=cadus_ticket",
                     f"/?cadus_ticket={tid}", f"/?p={tid}&preview=true", f"/?page_id={tid}",
                     "/feed/", "/?feed=rss2&post_type=cadus_ticket", "/comments/feed/",
                     "/wp-sitemap.xml", "/wp-sitemap-posts-cadus_ticket-1.xml", "/?author=1", "/?post_type=any&p=" + tid]:
            sin_fugas(f"anónimo {ruta}", ruta)
        estado, _ = sin_fugas("anónimo ticket por ID no es 200", f"/?post_type=cadus_ticket&p={tid}")
        comprobar("ticket por ID devuelve 403/404 (no 200 ni 500)", estado in (403, 404), f"HTTP {estado}")

        print("-- API REST")
        estado, cuerpo, _ = pedir("/wp-json/wp/v2/types")
        comprobar("REST /types no lista cadus_ticket", "cadus_ticket" not in cuerpo, f"HTTP {estado}")
        estado, cuerpo, _ = pedir("/wp-json/wp/v2/cadus_ticket")
        comprobar("REST /cadus_ticket no existe", estado in (401, 403, 404) and not any(s in cuerpo for s in SECRETOS), f"HTTP {estado}")
        estado, cuerpo, _ = pedir(f"/wp-json/wp/v2/cadus_ticket/{tid}")
        comprobar("REST /cadus_ticket/ID no existe", estado in (401, 403, 404), f"HTTP {estado}")
        for ruta in ["/wp-json/wp/v2/search?search=TEXTO-SECRETO-RN03", "/wp-json/wp/v2/posts?search=TEXTO-SECRETO-RN03&status=any",
                     "/wp-json/wp/v2/pages?search=TEXTO-SECRETO-RN03", "/wp-json/wp/v2/media?search=TEXTO-SECRETO-RN03",
                     "/wp-json/", "/wp-json/wp/v2/comments"]:
            sin_fugas(f"REST {ruta}", ruta)
        estado, cuerpo, _ = pedir("/wp-json/wp/v2/users")
        print(f"INFO    /wp-json/wp/v2/users responde HTTP {estado} ({'expone usuarios' if estado == 200 and 'slug' in cuerpo else 'sin listado'})")

        print("-- Seguimiento de ticket (máx. 3 intentos para no agotar el límite de 10 por 15 min)")
        pagina = "/atencion-al-estudiante/seguimiento-de-ticket/"
        jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        estado, cuerpo, cab = pedir(pagina, opener=opener)
        cc = (cab.get("Cache-Control") or cab.get("cache-control") or "").lower()
        comprobar("página de seguimiento no es cacheable", "no-store" in cc or "no-cache" in cc or "private" in cc, f"Cache-Control: {cc or '—'}")
        nonce = re.search(r'name="cadus_seguimiento_nonce"[^>]*value="([^"]+)"', cuerpo) or re.search(r'value="([^"]+)"[^>]*name="cadus_seguimiento_nonce"', cuerpo)
        if not nonce:
            print("SIN CONCLUIR  no se encontró el formulario de seguimiento (¿cambió la URL?)")
            resultados.append(False)
        else:
            def intentar(codigo, correo):
                return pedir(pagina, datos={"cadus_seguimiento_enviar": "1", "cadus_seguimiento_nonce": nonce.group(1),
                                            "cadus_codigo": codigo, "cadus_correo": correo}, opener=opener)
            e1, c1, h1 = intentar("CAD-2026-99999", "otra@alum.us.es")
            if "límite de consultas" in c1:
                print("SIN CONCLUIR  límite de intentos alcanzado: espera 15 minutos")
                resultados.append(False)
            else:
                comprobar("código correcto + correo equivocado no revela nada", "Asunto de prueba" not in c1 and "TEXTO-SECRETO" not in c1 and "No hemos encontrado" in c1)
                e2, c2, _ = intentar("CAD-2026-12345", "prueba@alum.us.es")
                comprobar("código inexistente da el mismo mensaje genérico", "No hemos encontrado" in c2)
                e3, c3, h3 = intentar("CAD-2026-99999", "PRUEBA@alum.us.es")
                comprobar("código + correo correctos muestran el ticket (sin el texto de la reclamación)", "Asunto de prueba" in c3 and "TEXTO-SECRETO-RN03" not in c3)
                cc3 = (h3.get("Cache-Control") or h3.get("cache-control") or "").lower()
                comprobar("respuesta con datos no es cacheable", "no-store" in cc3 or "no-cache" in cc3 or "private" in cc3, f"Cache-Control: {cc3 or '—'}")

        print("-- Capacidades por rol (CLI)")
        salida, _ = php("roles")
        try:
            roles = json.loads(salida)
        except ValueError:
            roles = {}
            comprobar("matriz de roles legible", False, salida[:80])
        permitido = {"administrator", "cadus_ejecutiva"}
        for rol, caps in roles.items():
            quiere = rol in permitido
            comprobar(f"rol {rol}: " + ("puede gestionar tickets" if quiere else "NO puede ver ni editar tickets"),
                      all(bool(caps[k]) == quiere for k in ("leer_ticket", "editar_ticket", "ver_listado")), json.dumps(caps))
        sub = roles.get("cadus_delegado", {})
        comprobar("delegado no puede borrar tickets", not sub.get("borrar_ticket"))
    finally:
        print("-- Limpieza:", php("borrar")[0])
    fallos = resultados.count(False)
    print(f"\n{resultados.count(True)} correctas, {fallos} fallos")
    return 1 if fallos else 0


sys.exit(main())
