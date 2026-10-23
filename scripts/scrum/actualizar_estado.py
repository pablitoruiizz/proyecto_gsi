"""Cambia el estado (y la fecha de cierre) de ítems del GitHub Project «CADUS · Scrum».
Uso: python scripts/scrum/actualizar_estado.py HU-10=Done@2026-10-23 HU-19="In Progress" ...
Estados: Todo, "In Progress", Done. La fecha de cierre (tras @) es opcional y solo para Done."""
import json, subprocess, sys
GH = r"C:\Program Files\GitHub CLI\gh.exe"
DUENO, NUM = "pablitoruiizz", "1"
sys.stdout.reconfigure(encoding="utf-8")

def gh(*a):
    r = subprocess.run([GH, *a], capture_output=True, text=True, encoding="utf-8")
    if r.returncode: raise SystemExit(r.stderr)
    return r.stdout

proyecto = json.loads(gh("project", "view", NUM, "--owner", DUENO, "--format", "json"))
campos = {f["name"]: f for f in json.loads(gh("project", "field-list", NUM, "--owner", DUENO, "--format", "json"))["fields"]}
estados = {o["name"]: o["id"] for o in campos["Status"]["options"]}
items = {i["title"].split(" ")[0]: i for i in json.loads(gh("project", "item-list", NUM, "--owner", DUENO, "--format", "json", "--limit", "200"))["items"]}
for arg in sys.argv[1:]:
    clave, resto = arg.split("=", 1)
    estado, _, fecha = resto.partition("@")
    it = items[clave]
    gh("project", "item-edit", "--id", it["id"], "--project-id", proyecto["id"], "--field-id", campos["Status"]["id"], "--single-select-option-id", estados[estado])
    if fecha:
        gh("project", "item-edit", "--id", it["id"], "--project-id", proyecto["id"], "--field-id", campos["Cierre"]["id"], "--date", fecha)
    if estado == "Done":
        num = it["content"]["number"]
        gh("issue", "close", str(num), "-R", f"{DUENO}/proyecto_gsi", "--reason", "completed")
    print(clave, "→", estado, fecha)
