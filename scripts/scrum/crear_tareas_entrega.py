"""Da de alta en el GitHub Project «CADUS · Scrum» las tareas de documentación y entrega del Sprint 2 (E2-xx de
docs/scrum/sprints/sprint-02.md). Estas tareas no llevan puntos de historia, así que no cambian el burndown.
Se puede relanzar: no duplica issues ni elementos, y solo rellena los campos vacíos.
Uso: python scripts/scrum/crear_tareas_entrega.py [--dry-run]"""
import json
import subprocess
import sys

DUENO, REPO, NUM = "pablitoruiizz", "proyecto_gsi", "1"
GH = r"C:\Program Files\GitHub CLI\gh.exe"
ASIGNADO = {"Pablo": "pablitoruiizz", "Joaquín": "joaquinluna2005-jpg", "Álvaro": "Alvaromartinez07", "Miguel Ángel": "migcammar"}
ENLACE = "[sprint-02.md](../blob/main/docs/scrum/sprints/sprint-02.md)"
# (id, título, responsable, prioridad, estado, fecha de cierre, requisitos)
TAREAS = [
    ("E2-01", "Cuentas institucionales: la del CADUS y una por delegación (script scripts/roles/aplicar_usuarios.php)", "Pablo", "Alta", "In Progress", "", "RF-14, RN-04"),
    ("E2-02", "Volcado bd_cadus_v1_sprint2.sql, push de la versión final y revisión de Wordfence", "Pablo", "Alta", "Todo", "", "RNF-04"),
    ("E2-03", "Montar el documento de la entrega 2 (Word y PDF) con la trazabilidad completa", "Pablo", "Alta", "In Progress", "", "—"),
    ("E2-04", "Priorizar el backlog con el cliente a través de Miguel Ángel", "Pablo", "Media", "Todo", "", "—"),
    ("E2-05", "Facilitar el Sprint 2: planning, daily, review y burndown", "Joaquín", "Alta", "Done", "2026-10-24", "—"),
    ("E2-06", "Retrospectiva del Sprint 1 y del Sprint 2 en el documento", "Joaquín", "Media", "Done", "2026-10-24", "—"),
    ("E2-07", "Comparativa razonada de al menos tres temas de WordPress", "Joaquín", "Alta", "Done", "2026-10-24", "UI-01, RNF-03"),
    ("E2-08", "Sustituir los comunicados de ejemplo por noticias reales del CADUS", "Joaquín", "Media", "Todo", "", "RF-01"),
    ("E2-09", "Entrevista con el CADUS: requisitos, prioridades, identidad visual y cuentas reales", "Miguel Ángel", "Alta", "Todo", "", "RF-14, UI-01"),
    ("E2-10", "Mockups finales en Figma con descripción y etiquetas de trazabilidad", "Miguel Ángel", "Alta", "Todo", "", "UI-01 a UI-08"),
    ("E2-11", "Sustituir actas, estatutos y páginas institucionales por los documentos reales", "Miguel Ángel", "Media", "Todo", "", "RF-03, RF-04"),
    ("E2-12", "Fichas reales de delegaciones (faltan Química, Física, Biología y ETSI) y edición restringida", "Álvaro", "Alta", "Todo", "", "RF-06, RF-07, RN-04"),
    ("E2-13", "Actualizar los diagramas UML (clases, estructura web y plugins) con las entidades nuevas", "Álvaro", "Alta", "Todo", "", "IR-01 a IR-09"),
    ("E2-14", "Comparativa de plugins: tres alternativas por tipo, con los obligatorios", "Marcos", "Alta", "Done", "2026-10-24", "RNF-01, RNF-04, RNF-08"),
    ("E2-15", "Revisar el REM (versión 2.0) y regenerar CADUS.rem", "Marcos", "Alta", "Done", "2026-10-25", "Todos"),
    ("E2-16", "Preguntas frecuentes y aviso de privacidad (consentimiento RGPD)", "Marcos", "Media", "Done", "2026-10-24", "RNF-08, UI-04"),
    ("E2-17", "Exportar el REM a PDF desde REMUS (la vista previa de REMUS sale en blanco; hay PDF provisional)", "Pablo", "Alta", "In Progress", "", "Todos"),
    ("E2-18", "Fusionar las pull requests #32 y #33 de Álvaro (pruebas por rol y su documentación)", "Pablo", "Media", "Todo", "", "RF-15"),
    ("E2-19", "Crear 2 o 3 eventos reales en el calendario para la demostración", "Miguel Ángel", "Media", "Todo", "", "RF-11"),
    ("E2-20", "Revisión cruzada final con Codex y corrección de los hallazgos", "Pablo", "Alta", "Done", "2026-10-25", "RN-03, RNF-03, RNF-04"),
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
        for t in TAREAS:
            print(f"{t[0]:6} {t[4]:11} {t[2]:13} {t[1]}")
        return
    repo = f"{DUENO}/{REPO}"
    if "tarea de entrega" not in {x["name"] for x in gh("label", "list", "-R", repo, "--json", "name", "--limit", "100", json_salida=True)}:
        gh("label", "create", "tarea de entrega", "-R", repo, "--color", "0e8a16")
    pid = gh("project", "view", NUM, "--owner", DUENO, "--format", "json", json_salida=True)["id"]
    campos = {f["name"]: f for f in gh("project", "field-list", NUM, "--owner", DUENO, "--format", "json", json_salida=True)["fields"]}
    estado = {o["name"]: o["id"] for o in campos["Status"]["options"]}
    prio = {o["name"]: o["id"] for o in campos["Prioridad"]["options"]}
    q = ('query($p:ID!){node(id:$p){... on ProjectV2{field(name:"Sprint"){... on ProjectV2IterationField{configuration{iterations{id title} completedIterations{id title}}}}}}}')
    conf = gh("api", "graphql", "-f", f"query={q}", "-f", f"p={pid}", json_salida=True)["data"]["node"]["field"]["configuration"]
    sprint2 = next(i["id"] for i in conf["iterations"] + conf["completedIterations"] if i["title"] == "Sprint 2")

    issues = {x["title"]: x for x in gh("issue", "list", "-R", repo, "--state", "all", "--limit", "300", "--json", "title,url,state", json_salida=True)}
    en_proyecto = {x["content"]["url"]: x for x in gh("project", "item-list", NUM, "--owner", DUENO, "--format", "json", "--limit", "300", json_salida=True)["items"] if x.get("content", {}).get("url")}
    for id_, texto, resp, pri, est, cierre, req in TAREAS:
        titulo = f"{id_} · {texto}"
        if titulo in issues:
            url = issues[titulo]["url"]
        else:
            cuerpo = (f"**{texto}**\n\n- Tipo: tarea de la entrega 2 (sin puntos de historia)\n- Requisito(s): {req}\n- Responsable: {resp}\n"
                      f"- Sprint: Sprint-02\n\nDetalle en {ENLACE}.")
            asignar = ["--assignee", ASIGNADO[resp]] if resp in ASIGNADO else []  # Marcos: sin cuenta de GitHub confirmada
            url = gh("issue", "create", "-R", repo, "--title", titulo, "--body", cuerpo, "--label", "tarea de entrega,sprint-2", *asignar).splitlines()[-1]
            if est == "Done":
                gh("issue", "close", url, "--reason", "completed")
        el = en_proyecto.get(url) or {}
        item = {"id": el["id"]} if el else gh("project", "item-add", NUM, "--owner", DUENO, "--url", url, "--format", "json", json_salida=True)
        base = ["project", "item-edit", "--id", item["id"], "--project-id", pid]
        if not el.get("responsable"):
            gh(*base, "--field-id", campos["Responsable"]["id"], "--text", resp)
        if not el.get("requisitos"):
            gh(*base, "--field-id", campos["Requisitos"]["id"], "--text", req)
        if not el.get("prioridad"):
            gh(*base, "--field-id", campos["Prioridad"]["id"], "--single-select-option-id", prio[pri])
        if not el.get("status"):
            gh(*base, "--field-id", campos["Status"]["id"], "--single-select-option-id", estado[est])
        if not el.get("sprint"):
            gh(*base, "--field-id", campos["Sprint"]["id"], "--iteration-id", sprint2)
        if cierre and not el.get("cierre"):
            gh(*base, "--field-id", campos["Cierre"]["id"], "--date", cierre)
        print("  ok", id_)


main()
