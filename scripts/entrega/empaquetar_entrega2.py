"""Monta la carpeta docs/entrega/entrega2/ con lo que se sube a la plataforma. Se puede repetir.
Uso: python scripts/entrega/empaquetar_entrega2.py
No incluye el volcado de la base de datos si no existe: se genera al final (ver README de la carpeta)."""
import os
import shutil
import zipfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
E = os.path.join(RAIZ, "docs", "entrega")
DESTINO = os.path.join(E, "entrega2")
PLUGIN = os.path.join(RAIZ, "cms-wordpress", "wp-content", "plugins", "cadus-portal")
os.makedirs(DESTINO, exist_ok=True)

copias = [
    (os.path.join(E, "Entrega2-CMS-CADUS-REMUS.pdf"), "Entrega2-CMS-CADUS.pdf"),
    (os.path.join(E, "paquete", "CADUS-REM-v2.pdf"), "CADUS-REM-v2.pdf"),
    (os.path.join(RAIZ, "docs", "requisitos", "rem-remus", "CADUS.rem"), "CADUS.rem"),
    (os.path.join(RAIZ, "cms-wordpress", "backup-db", "bd_cadus_v1_sprint2.sql"), "bd_cadus_v1_sprint2.sql"),
    (os.path.join(RAIZ, "docs", "scrum", "burndown", "sprint-02.csv"), "burndown-sprint-02.csv"),
    (os.path.join(E, "img", "burndown-sprint2.png"), "burndown-sprint-02.png"),
]
for origen, nombre in copias:
    try:
        shutil.copyfile(origen, os.path.join(DESTINO, nombre))
        print("ok      ", nombre)
    except (FileNotFoundError, PermissionError) as e:
        print("FALTA   ", nombre, "-", type(e).__name__)

zip_ruta = os.path.join(DESTINO, "plugin-cadus-portal.zip")
with zipfile.ZipFile(zip_ruta, "w", zipfile.ZIP_DEFLATED) as z:
    for base, _, ficheros in os.walk(PLUGIN):
        for f in ficheros:
            ruta = os.path.join(base, f)
            z.write(ruta, os.path.join("cadus-portal", os.path.relpath(ruta, PLUGIN)))
print("ok       plugin-cadus-portal.zip")

open(os.path.join(DESTINO, "LEEME.md"), "w", encoding="utf-8").write("""# Entrega 2 · Portal web del CADUS (CMS en WordPress)

| Fichero | Contenido |
|---|---|
| `Entrega2-CMS-CADUS.pdf` | Documento de la entrega (estilo REMUS): planificación, REM 2.0, análisis, diseño, implementación, trazabilidad y calidad |
| `CADUS-REM-v2.pdf` | Documento de requisitos tal como lo genera REMUS (versión 2.0) |
| `CADUS.rem` | Proyecto REMUS con los requisitos (versión 2.0) |
| `bd_cadus_v1_sprint2.sql` | Volcado de la base de datos del Sprint 2 (se genera al cerrar la entrega) |
| `burndown-sprint-02.png` / `.csv` | Burndown chart del Sprint 2 y sus datos |
| `plugin-cadus-portal.zip` | Plugin propio del portal (CADUS Portal) |

Seguimiento SCRUM: https://github.com/users/pablitoruiizz/projects/1 (público). Repositorio: https://github.com/pablitoruiizz/proyecto_gsi

Para instalar el portal desde cero: restaurar el volcado `.sql` en MySQL (base `bd_cadus`), copiar `cms-wordpress/` a Wamp y activar el plugin; el README del plugin explica la configuración.
""")
print("ok       LEEME.md")
