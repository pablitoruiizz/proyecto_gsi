"""Corrige en el GitHub Project «CADUS · Scrum» los cierres de scripts/scrum/cerrar_pendientes.py que la revisión con Codex del 22/11/2026
no consideró sostenidos del todo por su evidencia:
  - E3-01 (#57) y E2-12 (#47): se reabren y vuelven a «In Progress», porque lo que acreditan no cubre todo su alcance.
  - HU-14 (#23), HU-15 (#24), PB-003 (#4), E2-02 (#37), E2-03 (#38), E2-04 (#39), E2-09 (#44) y E2-11 (#46): se mantienen como están y se añade un
    comentario «Corrección:» con lo que la evidencia sí y no demuestra.
Uso: python scripts/scrum/corregir_cierres.py [--dry-run]   (idempotente: no repite comentarios)"""
import json
import subprocess
import sys

GH = r"C:\Program Files\GitHub CLI\gh.exe"
DUENO, REPO, NUM = "pablitoruiizz", "proyecto_gsi", "1"
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--dry-run" in sys.argv
REABRIR = {
    57: "Corrección: reabierta. Una Sprint Review escrita después y un CSV no demuestran el planning, las dailies, los puntos de control ni una retrospectiva hecha por el equipo. Se da por hecha cuando el equipo haga la retrospectiva en grupo y la anote en docs/scrum/sprints/sprint-03.md.",
    47: "Corrección: reabierta. Las 27 fichas existen (cadus-portal/data/delegaciones.json), pero faltan datos reales del CADUS (no hay horarios, hay siete teléfonos vacíos y un correo vacío). Depende de que el CADUS los aporte.",
}
CORREGIR = {
    23: "Corrección: los informes tests/HU-14a-HU-15a-portada.md y docs/pruebas/HU-14c-movil-tablet.md dejan casos manuales sin ejecutar (réplica estática sin la cabecera real de Blocksy, emulación sin dispositivos reales). Se cierra con el criterio del Sprint 3 («integrada en main», falta prueba cruzada); la historia no está probada por completo.",
    24: "Corrección: los informes dejan sin ejecutar la validación manual de teclado y lector de pantalla y el formulario real del buzón (docs/accesibilidad/HU-15c-auditoria.md, tests/HU-14a-HU-15a-portada.md). Se cierra con el criterio del Sprint 3 («integrada en main», falta prueba cruzada); la historia no está probada por completo.",
    4: "Corrección: los tres sitios iniciales (Documentación pública, Órganos de gobierno y Atención al estudiante) se crearon y configuraron el 26/10 y el 30/10; el cuarto, CADUS Votaciones, se creó el 13/11/2026 (docs/dms/entorno-sharepoint.md).",
    37: "Corrección: el volcado docs/entrega/entrega2/bd_cadus_v1_sprint2.sql es de la entrega 2 (25/10). La revisión de Wordfence se hizo después (HU-17b, 12/11/2026), así que esa parte no estaba hecha el 25/10.",
    38: "Corrección: el PDF de la entrega 2 está en docs/entrega/entrega2/Entrega2-CMS-CADUS.pdf (el Word, en docs/entrega/Entrega2-CMS-CADUS.docx).",
    39: "Corrección: la entrevista del 26/10 recoge prioridades generales; no hay un visto bueno del cliente historia a historia, que era lo que pedía la tarea (docs/scrum/sprints/sprint-02.md).",
    44: "Corrección: la entrevista existe; la parte «cuentas reales» del alcance sigue abierta en E2-01 y E3-02.",
    46: "Corrección: la cancelación vale para las actas y los documentos reales que debe aportar el CADUS; el contenido institucional real que sí se pudo hacer (páginas «Qué es el CADUS» y «Gobierno y estatutos») ya está hecho (docs/entrega/capturas-sprint3-miguel.md).",
}


def gh(*a, js=False):
    r = subprocess.run([GH, *a], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise SystemExit(f"gh {' '.join(a[:3])}… falló: {r.stderr.strip()}")
    return json.loads(r.stdout) if js else r.stdout.strip()


repo = f"{DUENO}/{REPO}"
pid = gh("project", "view", NUM, "--owner", DUENO, "--format", "json", js=True)["id"]
campos = {f["name"]: f for f in gh("project", "field-list", NUM, "--owner", DUENO, "--format", "json", js=True)["fields"]}
estado = {o["name"]: o["id"] for o in campos["Status"]["options"]}
items = gh("project", "item-list", NUM, "--owner", DUENO, "--format", "json", "--limit", "400", js=True)["items"]
por_num = {i["content"].get("number"): i for i in items if i.get("content")}


def comentado(num):
    cs = gh("issue", "view", str(num), "-R", repo, "--json", "comments", js=True)["comments"]
    return any(c["body"].startswith("Corrección:") for c in cs)


for num, texto in REABRIR.items():
    print(f"reabrir #{num} {por_num[num]['title'][:60]}")
    if SECO:
        continue
    gh("issue", "reopen", str(num), "-R", repo)
    gh("project", "item-edit", "--id", por_num[num]["id"], "--project-id", pid, "--field-id", campos["Status"]["id"], "--single-select-option-id", estado["In Progress"])
    if not comentado(num):
        gh("issue", "comment", str(num), "-R", repo, "--body", texto)
for num, texto in CORREGIR.items():
    print(f"corregir #{num} {por_num[num]['title'][:60]}")
    if not SECO and not comentado(num):
        gh("issue", "comment", str(num), "-R", repo, "--body", texto)
print("listo")
