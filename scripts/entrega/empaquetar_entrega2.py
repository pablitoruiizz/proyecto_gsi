"""Monta la carpeta docs/entrega/entrega2/ con lo que se sube a la plataforma. Se puede repetir.
Uso: python scripts/entrega/empaquetar_entrega2.py
Si falta cualquier pieza obligatoria (o no se puede copiar) termina con código 1 y borra la copia anterior de esa pieza,
para no entregar por error una versión antigua. Antes: generar el volcado con `php scripts/entrega/volcado_bd.php`."""
import os
import shutil
import sys
import zipfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
E = os.path.join(RAIZ, "docs", "entrega")
DESTINO = os.path.join(E, "entrega2")
PLUGIN = os.path.join(RAIZ, "cms-wordpress", "wp-content", "plugins", "cadus-portal")
UPLOADS = os.path.join(RAIZ, "cms-wordpress", "wp-content", "uploads")
os.makedirs(DESTINO, exist_ok=True)

obligatorias = [
    (os.path.join(E, "Entrega2-CMS-CADUS-REMUS.pdf"), "Entrega2-CMS-CADUS.pdf"),
    (os.path.join(E, "paquete", "CADUS-REM-v2.pdf"), "CADUS-REM-v2.pdf"),
    (os.path.join(RAIZ, "docs", "requisitos", "rem-remus", "CADUS.rem"), "CADUS.rem"),
    (os.path.join(RAIZ, "cms-wordpress", "backup-db", "bd_cadus_v1_sprint2.sql"), "bd_cadus_v1_sprint2.sql"),
    (os.path.join(RAIZ, "docs", "scrum", "burndown", "sprint-02.csv"), "burndown-sprint-02.csv"),
    (os.path.join(E, "img", "burndown-sprint2.png"), "burndown-sprint-02.png"),
]
fallos = []
for origen, nombre in obligatorias:
    destino = os.path.join(DESTINO, nombre)
    if os.path.exists(destino):
        os.remove(destino)  # nunca queda una copia antigua si la nueva falla
    try:
        shutil.copyfile(origen, destino)
        print("ok      ", nombre)
    except (FileNotFoundError, PermissionError) as e:
        fallos.append(nombre)
        print("FALTA   ", nombre, "-", type(e).__name__, "-", origen)


def comprimir(carpeta, nombre_zip, raiz_zip):
    ruta = os.path.join(DESTINO, nombre_zip)
    if os.path.exists(ruta):
        os.remove(ruta)
    n = 0
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, ficheros in os.walk(carpeta):
            for f in ficheros:
                p = os.path.join(base, f)
                z.write(p, os.path.join(raiz_zip, os.path.relpath(p, carpeta)))
                n += 1
    print("ok      ", nombre_zip, f"({n} ficheros)")
    return n


comprimir(PLUGIN, "plugin-cadus-portal.zip", "cadus-portal")
if comprimir(UPLOADS, "wp-content-uploads.zip", "uploads") == 0:
    fallos.append("wp-content-uploads.zip (sin ficheros)")

open(os.path.join(DESTINO, "LEEME.md"), "w", encoding="utf-8").write("""# Entrega 2 · Portal web del CADUS (CMS en WordPress)

| Fichero | Contenido |
|---|---|
| `Entrega2-CMS-CADUS.pdf` | Documento de la entrega (estilo REMUS): planificación, REM 2.0, análisis, diseño, implementación, trazabilidad y calidad |
| `CADUS-REM-v2.pdf` | Documento de requisitos tal como lo genera REMUS (versión 2.0) |
| `CADUS.rem` | Proyecto REMUS con los requisitos (versión 2.0) |
| `bd_cadus_v1_sprint2.sql` | Volcado de la base de datos del Sprint 2 (contiene las contraseñas cifradas de los usuarios: no se publica) |
| `wp-content-uploads.zip` | Medios del sitio (carpeta `wp-content/uploads`): el volcado referencia estos archivos |
| `plugin-cadus-portal.zip` | Plugin propio del portal (CADUS Portal) |
| `burndown-sprint-02.png` / `.csv` | Burndown chart del Sprint 2 y sus datos |

Seguimiento SCRUM: https://github.com/users/pablitoruiizz/projects/1 (público). Repositorio: https://github.com/pablitoruiizz/proyecto_gsi

## Restaurar el portal en otro equipo
1. Instalar WordPress 7.1 (Wamp o XAMPP, PHP 8.x y MySQL 8.x), crear la base `bd_cadus` y restaurar `bd_cadus_v1_sprint2.sql` (si el sitio cambia de dirección, actualizar `siteurl` y `home` en `wp_options`).
2. Copiar el contenido del repositorio `cms-wordpress/` a la carpeta del servidor y ajustar `wp-config.php` (base de datos).
3. Descomprimir `wp-content-uploads.zip` en `wp-content/uploads/` y `plugin-cadus-portal.zip` en `wp-content/plugins/` (el plugin también está en el repositorio).
4. Activar el plugin **CADUS Portal**, entrar con la cuenta `cadus` (`¿Has olvidado tu contraseña?` envía el enlace a dcadus@us.es) y comprobar los menús, la portada y el calendario.
""")
print("ok       LEEME.md")
if fallos:
    print("\nENTREGA INCOMPLETA, falta:", ", ".join(fallos))
    sys.exit(1)
print("\nPaquete completo.")
