"""Prueba HU-22 (relevo de la cuenta de la delegación) con sesiones HTTP reales (casos H22-1 a H22-4).

Uso:  CADUS_PRUEBA_CLAVE=<clave de las cuentas de prueba> python scripts/pruebas/hu22_relevo.py [url_base]
Necesita las cuentas test-delegado y test-ejecutivo (ver tests/cuentas-de-prueba-local.md, solo local) y que la ficha 32
sea de test-delegado. Cambia la clave de test-delegado dos veces; al acabar, la deja con CLAVE + "-final".
La clave no se escribe aquí ni se imprime.
"""
import os
import re
import sys

import requests

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost/proyecto_gsi/cms-wordpress").rstrip("/")
CLAVE = os.environ["CADUS_PRUEBA_CLAVE"]
NUEVA1 = CLAVE + "-uno"
NUEVA2 = CLAVE + "-final"
PAGINA = BASE + "/wp-admin/edit.php?post_type=cadus_delegacion&page=cadus-relevo"
POST = BASE + "/wp-admin/admin-post.php"
res = []


def login(usuario, clave):
    s = requests.Session()
    s.cookies.set("wordpress_test_cookie", "WP Cookie check")
    r = s.post(BASE + "/wp-login.php", data={"log": usuario, "pwd": clave, "wp-submit": "Acceder", "redirect_to": PAGINA,
                                             "testcookie": "1"}, allow_redirects=False)
    ok = r.status_code == 302 and any(c.name.startswith("wordpress_logged_in") for c in s.cookies)
    return s if ok else None


def pagina(s):
    return s.get(PAGINA, allow_redirects=False)


def nonce(html):
    return re.search(r'name="cadus_relevo_nonce" value="([^"]+)"', html).group(1)


def relevo(s, cuenta, clave, html):
    return s.post(POST, data={"action": "cadus_relevo", "cadus_relevo_nonce": nonce(html), "cuenta": cuenta, "modo": "contrasena",
                              "clave": clave, "confirmo": "1"}, allow_redirects=False)


def anota(caso, ok, detalle):
    res.append((caso, ok))
    print(f"{caso}: {'OK' if ok else 'FALLO'} - {detalle}")


d1 = login("test-delegado", CLAVE)
d2 = login("test-delegado", CLAVE)  # segunda sesión del mismo equipo, «otro navegador»
e = login("test-ejecutivo", CLAVE)
assert d1 and d2 and e, "no se pudo entrar con las cuentas de prueba (¿existen y tienen esa clave?)"
pg = pagina(d1)
assert pg.status_code == 200
ficha = lambda: os.popen('"C:/Users/ruizv/OneDrive/Escritorio/UNI/GSI/bin/mysql/mysql8.4.7/bin/mysql.exe" -uroot bd_cadus -N -e '
                         '"select post_author from wp_posts where ID=32"').read().strip()
autor_antes = ficha()
ide = re.search(r'name="cuenta" value="(\d+)"', pg.text).group(1)  # la cuenta propia del delegado

# H22-3 antes de nada: el delegado intenta hacer el relevo de otras cuentas (la Ejecutiva y root)
ide_ejec = os.popen('"C:/Users/ruizv/OneDrive/Escritorio/UNI/GSI/bin/mysql/mysql8.4.7/bin/mysql.exe" -uroot bd_cadus -N -e '
                    '"select ID from wp_users where user_login=\'test-ejecutivo\'"').read().strip()
codigos = [relevo(d1, c, "otraClave-12345", pg.text).status_code for c in (ide_ejec, "1")]
anota("H22-3", codigos == [403, 403], f"el delegado, al cambiar `cuenta` por la de la Ejecutiva y por la de root, recibe {codigos}")

# H22-1: el delegado hace su relevo con contraseña nueva
r = relevo(d1, ide, NUEVA1, pg.text)
destino = r.headers.get("Location", "")
anota("H22-1a", r.status_code == 302 and "wp-login.php" in destino, f"redirección a {destino.split('?')[0].split('/')[-1]} con parámetros {sorted(re.findall(r'[?&]([a-z_]+)=', destino))}")
anota("H22-1b", login("test-delegado", CLAVE) is None, "la contraseña antigua ya no entra")
n1 = login("test-delegado", NUEVA1)
anota("H22-1c", n1 is not None, "la contraseña nueva sí entra")
anota("H22-1d", ficha() == autor_antes, f"la ficha 32 sigue en la misma cuenta (autor {autor_antes})")

# H22-2: la otra sesión y la que hizo el relevo quedan cerradas
c2 = pagina(d2)
c1 = pagina(d1)
anota("H22-2", c2.status_code in (301, 302) and "wp-login" in c2.headers.get("Location", "") and
      c1.status_code in (301, 302) and "wp-login" in c1.headers.get("Location", ""),
      f"la segunda sesión ({c2.status_code}) y la que hizo el relevo ({c1.status_code}) se mandan al acceso")

# H22-4: la Ejecutiva hace el relevo de la delegación y ve la tabla
pe = pagina(e)
opciones = re.findall(r'<option value="(\d+)">([^<]*)</option>', pe.text)
solo_delegacion = all("test-" in t or "(" in t for _, t in opciones) and len(opciones) == 1
r = relevo(e, ide, NUEVA2, pe.text)
pe2 = pagina(e)
anota("H22-4a", r.status_code == 302 and "relevo" in r.headers.get("Location", ""), "la Ejecutiva hace el relevo y vuelve a la pantalla con el aviso")
anota("H22-4b", "por test-ejecutivo" in pe2.text, "la tabla muestra el último relevo «por test-ejecutivo»")
anota("H22-4c", len(opciones) == 1, f"la lista ofrece {len(opciones)} cuenta(s), solo de delegación")
ra = relevo(e, "1", "otraClave-12345", pe2.text)
anota("H22-4d", ra.status_code == 403, f"el relevo de root por la Ejecutiva devuelve {ra.status_code}")
anota("H22-4e", pagina(n1).status_code in (301, 302), "la sesión abierta del delegado con la clave de antes queda cerrada")
anota("H22-4f", login("test-delegado", NUEVA1) is None and login("test-delegado", NUEVA2) is not None, "la clave del relevo anterior deja de valer y la nueva entra")

# H22-5 (una sola cuenta por ficha en la tabla)
filas = len(re.findall(r"<td[^>]*>\s*test-delegado\s*</td>|>test-delegado<", pe2.text))
anota("H22-5a", filas >= 1 and "test-estudiante" not in pe2.text, "la tabla de la Ejecutiva muestra una sola cuenta de delegación para la ficha 32")
print("\nTotal:", sum(1 for _, o in res if o), "OK de", len(res))
sys.exit(0 if all(o for _, o in res) else 1)
