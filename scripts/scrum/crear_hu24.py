"""Añade HU-24 (acceso y gestión desde el portal, cambio de alcance del 12/11) al GitHub Project «CADUS · Scrum».
Uso: python scripts/scrum/crear_hu24.py   (idempotente: si la issue ya existe, solo completa los campos que falten)"""
import json, subprocess, sys

GH = r"C:\Program Files\GitHub CLI\gh.exe"
DUENO, REPO, NUM = "pablitoruiizz", "proyecto_gsi", "1"
sys.stdout.reconfigure(encoding="utf-8")
TITULO = "HU-24 · Como miembro de la Ejecutiva o delegado, quiero iniciar sesión en el portal y gestionar sin entrar en el panel de administración"
CUERPO = ("**Como miembro de la Ejecutiva o delegado, quiero iniciar sesión en el portal y encontrar un apartado de gestión sencillo "
          "(nueva noticia, nuevo evento, nueva acta y delegaciones) sin entrar en el panel de administración.**\n\n"
          "- Requisito(s): RF-14, RF-15, UI-09, UI-10\n- Story points: 8\n- Estado: Hecho (falta prueba cruzada de una persona del equipo)\n"
          "- Sprint: Sprint-03 (cambio de alcance del 12/11/2026: 36 → 44 SP)\n- Responsable: Pablo\n\n"
          "Código: `cms-wordpress/wp-content/plugins/cadus-portal/includes/gestion.php`. Pruebas: `scripts/pruebas/gestion.php` (93 correctas). "
          "Revisión cruzada con Codex hecha (docs/scrum/codex_revision_gestion_portal.md y codex_revision_delegaciones_pie.md).\n\n"
          "Trazabilidad con los requisitos: [REM-CADUS.md](../blob/main/docs/requisitos/rem-remus/REM-CADUS.md). "
          "Backlog de origen: [product-backlog.md](../blob/main/docs/scrum/backlog/product-backlog.md).")


def gh(*a, js=False):
    r = subprocess.run([GH, *a], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise SystemExit(f"gh {' '.join(a[:3])}… falló: {r.stderr.strip()}")
    return json.loads(r.stdout) if js else r.stdout.strip()


repo = f"{DUENO}/{REPO}"
pid = gh("project", "view", NUM, "--owner", DUENO, "--format", "json", js=True)["id"]
campos = {f["name"]: f for f in gh("project", "field-list", NUM, "--owner", DUENO, "--format", "json", js=True)["fields"]}
estado = {o["name"]: o["id"] for o in campos["Status"]["options"]}
prio = {o["name"]: o["id"] for o in campos["Prioridad"]["options"]}
q = 'query($p:ID!){node(id:$p){... on ProjectV2{field(name:"Sprint"){... on ProjectV2IterationField{configuration{iterations{id title} completedIterations{id title}}}}}}}'
conf = gh("api", "graphql", "-f", f"query={q}", "-f", f"p={pid}", js=True)["data"]["node"]["field"]["configuration"]
sprint3 = next(i["id"] for i in conf["iterations"] + conf["completedIterations"] if i["title"] == "Sprint 3")

previa = next((x for x in gh("issue", "list", "-R", repo, "--state", "all", "--limit", "300", "--json", "title,url", js=True) if x["title"].startswith("HU-24")), None)
url = previa["url"] if previa else gh("issue", "create", "-R", repo, "--title", TITULO, "--body", CUERPO, "--label", "historia de usuario,sprint-3", "--assignee", DUENO).splitlines()[-1]
items = gh("project", "item-list", NUM, "--owner", DUENO, "--format", "json", "--limit", "300", js=True)["items"]
el = next((i for i in items if i.get("content", {}).get("url") == url), None)
item_id = el["id"] if el else gh("project", "item-add", NUM, "--owner", DUENO, "--url", url, "--format", "json", js=True)["id"]
base = ["project", "item-edit", "--id", item_id, "--project-id", pid]
gh(*base, "--field-id", campos["Responsable"]["id"], "--text", "Pablo")
gh(*base, "--field-id", campos["Requisitos"]["id"], "--text", "RF-14, RF-15, UI-09, UI-10")
gh(*base, "--field-id", campos["Prioridad"]["id"], "--single-select-option-id", prio["Alta"])
gh(*base, "--field-id", campos["Sprint"]["id"], "--iteration-id", sprint3)
gh(*base, "--field-id", campos["Status"]["id"], "--single-select-option-id", estado["Done"])
gh(*base, "--field-id", campos["Cierre"]["id"], "--date", "2026-11-12")
num = url.rsplit("/", 1)[-1]
gh("issue", "close", num, "-R", repo, "--reason", "completed")
print("HU-24 en el proyecto:", url)
