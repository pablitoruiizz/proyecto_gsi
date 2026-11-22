"""Deja al día el GitHub Project «CADUS · Scrum» antes de la entrega final (22/11/2026):
  1. Asigna en GitHub a las personas del campo «Responsable» de las issues que no tenían asignado (Marcos es Federomai).
  2. Cierra como hechas las tareas que tienen evidencia en el repositorio, con un comentario que la cita.
  3. Cancela (etiqueta «cancelada», cerrada como no planificada) las que dependían de que el CADUS entregase contenido.
Lo que depende del cliente o de la entrega del 07/12 (E2-01, E3-02, E3-06 y E3-09) se deja abierto a propósito.
Uso: python scripts/scrum/cerrar_pendientes.py [--dry-run]   (se puede relanzar: no repite comentarios ni cierres)"""
import json
import subprocess
import sys

GH = r"C:\Program Files\GitHub CLI\gh.exe"
DUENO, REPO, NUM = "pablitoruiizz", "proyecto_gsi", "1"
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--dry-run" in sys.argv
USUARIO = {"Pablo": "pablitoruiizz", "Joaquín": "joaquinluna2005-jpg", "Álvaro": "Alvaromartinez07", "Miguel Ángel": "migcammar", "Marcos": "Federomai"}
# número de issue -> (Responsable a escribir o None, fecha de cierre, comentario con la evidencia)
HECHAS = {
    4: ("Pablo", "2026-10-30", "Hecha: los cuatro sitios de SharePoint del DMS están creados y configurados (docs/dms/entorno-sharepoint.md)."),
    5: ("Pablo y Marcos", "2026-11-21", "Hecha: tres equipos privados en Teams (Ejecutiva, Delegaciones y Asamblea) con propietarios, canales, canal de avisos con moderación, canales privados y calendario. Evidencia: capturas 01 a 11 y docs/redsocial/pruebas.md; las de Marcos (03 a 06, 10 y 11 y pruebas.md) están en la rama feature/marcos-teams-capturas, todavía sin fusionar en main."),
    23: (None, "2026-11-15", "Hecha: HU-14a (13/11), HU-14b (15/11, PR #77) y HU-14c (12/11). Solo en emulación y sin prueba cruzada: ver docs/pruebas/HU-14c-movil-tablet.md y tests/."),
    24: (None, "2026-11-13", "Hecha: HU-15a (13/11), HU-15b (12/11) y HU-15c (12/11). Sin prueba cruzada ni lector de pantalla real: ver tests/HU-14a-HU-15a-portada.md."),
    37: (None, "2026-10-25", "Hecha: volcado docs/entrega/entrega2/bd_cadus_v1_sprint2.sql en la entrega 2; la revisión de Wordfence se hizo después (HU-17b, 12/11)."),
    38: (None, "2026-10-25", "Hecha: docs/entrega/Entrega2-CMS-CADUS.docx y .pdf, con la trazabilidad."),
    39: (None, "2026-10-26", "Hecha: las prioridades se recogieron en la entrevista con el CADUS del 26/10/2026 (docs/cliente/entrevista-cliente.md, sección 6)."),
    44: (None, "2026-10-26", "Hecha: entrevista con el CADUS del 26/10/2026 (docs/cliente/entrevista-cliente.md)."),
    47: (None, "2026-11-12", "Hecha: las 27 delegaciones con ficha (cadus-portal/data/delegaciones.json; 25 con escudo, salvo Doctorado y Odontología) y edición restringida por RN-04 (HU-24 y decisión X7)."),
    57: (None, "2026-11-15", "Hecha: burndown actualizado hasta el cierre (docs/scrum/burndown/sprint-03.csv) y Sprint Review y retrospectiva escritas en docs/scrum/sprints/sprint-03.md (a partir de los datos del sprint, no de una reunión)."),
}
CANCELADAS = {
    43: "Cancelada: el CADUS indicó en la entrevista (pregunta 14) que la web es de prueba y que ellos subirán el contenido que quieran; el equipo no inventa comunicados. Si el CADUS se queda con el portal, la tarea pasa a ser suya.",
    46: "Cancelada: mismo motivo (entrevista, pregunta 14). Los documentos de ejemplo del portal y del DMS son ficticios y los reales los aporta el CADUS.",
    54: "Cancelada: mismo motivo (entrevista, pregunta 14). El portal tiene eventos de ejemplo y el CADUS creará los reales.",
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


def nombres(texto):
    return [u for n, u in USUARIO.items() if n in (texto or "")]


def comentado(num, inicio):
    cs = gh("issue", "view", str(num), "-R", repo, "--json", "comments", js=True)["comments"]
    return any(c["body"].startswith(inicio) for c in cs)


# 1) asignados
for num, it in sorted(por_num.items()):
    if not it.get("assignees"):
        resp = HECHAS.get(num, (None,))[0] or it.get("responsable")
        quienes = nombres(resp)
        if quienes:
            print(f"asignar #{num} -> {', '.join(quienes)}")
            if not SECO:
                gh("issue", "edit", str(num), "-R", repo, *sum((["--add-assignee", q] for q in quienes), []))
# 2) hechas
for num, (resp, cierre, texto) in HECHAS.items():
    it = por_num[num]
    print(f"hecha #{num} {it['title'][:60]}")
    if SECO:
        continue
    base = ["project", "item-edit", "--id", it["id"], "--project-id", pid]
    if resp:
        gh(*base, "--field-id", campos["Responsable"]["id"], "--text", resp)
        quienes = nombres(resp)
        gh("issue", "edit", str(num), "-R", repo, *sum((["--add-assignee", q] for q in quienes), []))
    gh(*base, "--field-id", campos["Status"]["id"], "--single-select-option-id", estado["Done"])
    gh(*base, "--field-id", campos["Cierre"]["id"], "--date", cierre)
    if not comentado(num, "Hecha:"):
        gh("issue", "comment", str(num), "-R", repo, "--body", texto)
    gh("issue", "close", str(num), "-R", repo, "--reason", "completed")
# 3) canceladas
for num, texto in CANCELADAS.items():
    it = por_num[num]
    print(f"cancelada #{num} {it['title'][:60]}")
    if SECO:
        continue
    gh("issue", "edit", str(num), "-R", repo, "--add-label", "cancelada")
    gh("project", "item-edit", "--id", it["id"], "--project-id", pid, "--field-id", campos["Status"]["id"], "--single-select-option-id", estado["Done"])
    if not comentado(num, "Cancelada:"):
        gh("issue", "comment", str(num), "-R", repo, "--body", texto)
    gh("issue", "close", str(num), "-R", repo, "--reason", "not planned")
print("listo")
