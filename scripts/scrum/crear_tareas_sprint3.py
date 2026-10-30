"""Prepara el Sprint 3 en el GitHub Project «CADUS · Scrum»: asigna HU-14, HU-15, HU-16, HU-17, HU-20, HU-22 y HU-23 al Sprint 3
(con su responsable y la etiqueta sprint-3) y da de alta las tareas E3-xx de docs/scrum/sprints/sprint-03.md, que no llevan puntos.
Se puede relanzar: no duplica issues ni elementos, y solo rellena los campos vacíos.
Uso: python scripts/scrum/crear_tareas_sprint3.py [--dry-run]"""
import json
import subprocess
import sys

DUENO, REPO, NUM = "pablitoruiizz", "proyecto_gsi", "1"
GH = r"C:\Program Files\GitHub CLI\gh.exe"
ASIGNADO = {"Pablo": "pablitoruiizz", "Joaquín": "joaquinluna2005-jpg", "Álvaro": "Alvaromartinez07", "Miguel Ángel": "migcammar"}
ENLACE = "[sprint-03.md](../blob/main/docs/scrum/sprints/sprint-03.md)"
# historia -> responsables (como en el Sprint 2: «Marcos y Pablo»)
HISTORIAS = {
    "HU-14": "Joaquín, Álvaro y Pablo", "HU-15": "Joaquín, Marcos y Miguel Ángel", "HU-16": "Álvaro y Marcos",
    "HU-17": "Marcos y Pablo", "HU-20": "Miguel Ángel y Pablo", "HU-22": "Miguel Ángel", "HU-23": "Álvaro",
}
# (id, título, responsable, prioridad, estado, requisitos)
TAREAS = [
    ("E3-01", "Facilitar el Sprint 3: planning, daily, puntos de control del 01/11 y el 08/11, review y burndown diario", "Joaquín", "Alta", "In Progress", "—"),
    ("E3-02", "Cuentas de los delegados, comprobar el correo del buzón y volcado bd_cadus_v1_sprint3.sql", "Pablo", "Alta", "Todo", "RF-14, RN-04"),
    ("E3-03", "Preguntar a la US qué ofrece el servidor SFTP (PHP, MySQL, límites) y cómo se despliega, antes del 30/10", "Miguel Ángel", "Alta", "Todo", "RNF-05, RNF-07"),
    ("E3-04", "Pruebas de aceptación: guion por historia y por rol (HU-14 a HU-23) y ejecución en la semana 3", "Álvaro", "Alta", "Todo", "Todos"),
    ("E3-05", "Revisar el REM y la trazabilidad con los cambios del sprint y regenerar CADUS.rem", "Marcos", "Media", "Todo", "Todos"),
    ("E3-06", "Montar el documento final (Word y PDF) con el Sprint 3, el burndown y la trazabilidad completa", "Pablo", "Alta", "Todo", "—"),
    ("E3-07", "Añadir la categoría «Cursos» al calendario (asambleas y cursos)", "Miguel Ángel", "Media", "Todo", "RF-11"),
    ("E3-09", "Desplegar en el servidor de la US: migración, correo, tarea programada de HU-23, pruebas en destino y copia de seguridad", "Pablo", "Alta", "Todo", "RNF-05, RNF-06, RNF-07"),
    ("E3-08", "Tickets: aviso al correo de dcadus y datos mínimos (nombre y apellidos, facultad y correo US); plazo de respuesta pendiente de aclarar", "Marcos", "Alta", "Todo", "RF-09, RF-10, RNF-08"),
]
seco = "--dry-run" in sys.argv
sys.stdout.reconfigure(encoding="utf-8")


def gh(*args, json_salida=False):
    r = subprocess.run([GH, *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise SystemExit(f"gh {' '.join(args[:3])}… falló: {r.stderr.strip()}")
    return json.loads(r.stdout) if json_salida else r.stdout.strip()


def main():
    if seco:
        for k, v in HISTORIAS.items():
            print(f"{k:6} historia     {v}")
        for t in TAREAS:
            print(f"{t[0]:6} {t[4]:11} {t[2]:13} {t[1]}")
        return
    repo = f"{DUENO}/{REPO}"
    etiquetas = {x["name"] for x in gh("label", "list", "-R", repo, "--json", "name", "--limit", "100", json_salida=True)}
    if "sprint-3" not in etiquetas:
        gh("label", "create", "sprint-3", "-R", repo, "--color", "1d76db")
    pid = gh("project", "view", NUM, "--owner", DUENO, "--format", "json", json_salida=True)["id"]
    campos = {f["name"]: f for f in gh("project", "field-list", NUM, "--owner", DUENO, "--format", "json", json_salida=True)["fields"]}
    estado = {o["name"]: o["id"] for o in campos["Status"]["options"]}
    prio = {o["name"]: o["id"] for o in campos["Prioridad"]["options"]}
    q = ('query($p:ID!){node(id:$p){... on ProjectV2{field(name:"Sprint"){... on ProjectV2IterationField{configuration{iterations{id title} completedIterations{id title}}}}}}}')
    conf = gh("api", "graphql", "-f", f"query={q}", "-f", f"p={pid}", json_salida=True)["data"]["node"]["field"]["configuration"]
    sprint3 = next((i["id"] for i in conf["iterations"] + conf["completedIterations"] if i["title"] == "Sprint 3"), None)
    if not sprint3:
        raise SystemExit("Falta la iteración «Sprint 3» en el campo Sprint del proyecto")

    items = {i["title"].split(" ")[0]: i for i in gh("project", "item-list", NUM, "--owner", DUENO, "--format", "json", "--limit", "300", json_salida=True)["items"]}
    for hu, resp in HISTORIAS.items():
        it = items.get(hu)
        if not it:
            raise SystemExit(f"{hu} no está en el proyecto: ejecuta antes crear_proyecto_github.py")
        base = ["project", "item-edit", "--id", it["id"], "--project-id", pid]
        if it.get("responsable") in (None, "", "Sin asignar"):
            gh(*base, "--field-id", campos["Responsable"]["id"], "--text", resp)
        if not it.get("sprint"):
            gh(*base, "--field-id", campos["Sprint"]["id"], "--iteration-id", sprint3)
        gh("issue", "edit", str(it["content"]["number"]), "-R", repo, "--add-label", "sprint-3")
        print("  historia", hu, "→ Sprint 3,", resp)

    issues = {x["title"]: x for x in gh("issue", "list", "-R", repo, "--state", "all", "--limit", "300", "--json", "title,url,state", json_salida=True)}
    en_proyecto = {x["content"]["url"]: x for x in items.values() if x.get("content", {}).get("url")}
    en_proyecto.update({x["content"]["url"]: x for x in gh("project", "item-list", NUM, "--owner", DUENO, "--format", "json", "--limit", "300", json_salida=True)["items"] if x.get("content", {}).get("url")})
    for id_, texto, resp, pri, est, req in TAREAS:
        titulo = f"{id_} · {texto}"
        cuerpo = (f"**{texto}**\n\n- Tipo: tarea del Sprint 3 (sin puntos de historia)\n- Requisito(s): {req}\n- Responsable: {resp}\n"
                  f"- Sprint: Sprint-03 (26/10 – 15/11/2026)\n\nDetalle en {ENLACE}.")
        previa = next((x for t, x in issues.items() if t.startswith(f"{id_} ·")), None)
        if previa:
            url = previa["url"]
            if previa["title"] != titulo:  # el título cambió tras la entrevista: se renombra en lugar de duplicar
                gh("issue", "edit", url, "--title", titulo, "--body", cuerpo)
        else:
            asignar = ["--assignee", ASIGNADO[resp]] if resp in ASIGNADO else []  # Marcos: sin cuenta de GitHub confirmada
            url = gh("issue", "create", "-R", repo, "--title", titulo, "--body", cuerpo, "--label", "tarea de entrega,sprint-3", *asignar).splitlines()[-1]
        el = en_proyecto.get(url) or {}
        item = {"id": el["id"]} if el else gh("project", "item-add", NUM, "--owner", DUENO, "--url", url, "--format", "json", json_salida=True)
        base = ["project", "item-edit", "--id", item["id"], "--project-id", pid]
        if not el.get("responsable"):
            gh(*base, "--field-id", campos["Responsable"]["id"], "--text", resp)
        if el.get("requisitos") != req:
            gh(*base, "--field-id", campos["Requisitos"]["id"], "--text", req)
        if not el.get("prioridad"):
            gh(*base, "--field-id", campos["Prioridad"]["id"], "--single-select-option-id", prio[pri])
        if not el.get("status"):
            gh(*base, "--field-id", campos["Status"]["id"], "--single-select-option-id", estado[est])
        if not el.get("sprint"):
            gh(*base, "--field-id", campos["Sprint"]["id"], "--iteration-id", sprint3)
        print("  ok", id_)


main()
