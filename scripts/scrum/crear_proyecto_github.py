"""Crea el GitHub Project «CADUS · Scrum» a partir del product backlog de docs/scrum/backlog/product-backlog.md.

Requiere la CLI `gh` con sesión iniciada y permisos repo y project (gh auth login --web --scopes "repo,project").
Qué hace, en este orden (se puede relanzar: salta lo que ya existe):
  1. etiquetas del repositorio (tipo de ítem y sprint),
  2. proyecto vinculado al repositorio, con los campos SP, Requisitos, Prioridad, Responsable y la iteración Sprint,
  3. una issue por cada ítem del backlog (cerrada si ya está hecha), añadida al proyecto con sus campos rellenos.
Uso: python scripts/scrum/crear_proyecto_github.py [--dry-run]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

DUENO, REPO = "pablitoruiizz", "proyecto_gsi"
TITULO = "CADUS · Scrum"
GH = r"C:\Program Files\GitHub CLI\gh.exe"
RAIZ = Path(__file__).resolve().parents[2]
BACKLOG = RAIZ / "docs/scrum/backlog/product-backlog.md"

# Reparto del Sprint 1 (sprint-01.md) y del Sprint 2 (sprint-02.md); Sprint 3 y 4 sin asignar todavía.
RESPONSABLE = {
    "PB-001": "Pablo", "PB-002": "Pablo", "PB-005": "Pablo", "PB-006": "Pablo", "PB-007": "Pablo", "PB-008": "Pablo",
    "HU-13": "Pablo", "HU-18": "Pablo", "HU-01": "Joaquín", "HU-02": "Joaquín", "HU-03": "Miguel Ángel", "HU-04": "Miguel Ángel",
    "HU-05": "Álvaro", "HU-06": "Álvaro", "HU-07": "Marcos", "HU-08": "Marcos",
    "HU-09": "Marcos y Pablo", "HU-10": "Miguel Ángel", "HU-11": "Joaquín", "HU-12": "Álvaro", "HU-19": "Pablo, Miguel Ángel y Álvaro",
    "HU-22": "Miguel Ángel", "HU-23": "Álvaro",
}
# Solo se asigna la issue a una cuenta cuando está claro quién es.
ASIGNADO = {"Pablo": "pablitoruiizz", "Joaquín": "joaquinluna2005-jpg", "Álvaro": "Alvaromartinez07"}
ITERACIONES = [("Sprint 1", "2026-09-28", 21), ("Sprint 2", "2026-10-19", 7), ("Sprint 3", "2026-10-26", 21)]
ESTADO = {"Hecho": "Done", "Pendiente": "Todo", "Cancelada": "Todo"}  # una historia cancelada se cierra aparte como «not planned»
# Fechas reales de cierre del Sprint 1 (las issues se cerraron de golpe al crearlas, así que la gráfica nativa de GitHub no las refleja).
CIERRE = {"PB-002": "2026-09-28", "PB-005": "2026-10-05", **{i: "2026-10-18" for i in
          ["PB-006", "PB-007", "PB-008", "HU-01", "HU-02", "HU-03", "HU-04", "HU-05", "HU-06", "HU-07", "HU-08", "HU-13", "HU-18"]}}

seco = "--dry-run" in sys.argv
sys.stdout.reconfigure(encoding="utf-8")


def gh(*args, entrada=None, json_salida=False):
    r = subprocess.run([GH, *args], capture_output=True, text=True, encoding="utf-8", input=entrada)
    if r.returncode != 0:
        raise SystemExit(f"gh {' '.join(args[:3])}… falló: {r.stderr.strip()}")
    return json.loads(r.stdout) if json_salida else r.stdout.strip()


def leer_backlog():
    """Devuelve los ítems del backlog como diccionarios; las dos tablas tienen columnas distintas."""
    items = []
    for linea in BACKLOG.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if not re.match(r"^(PB|HU)-\d+$", c[0] if c else ""):
            continue
        if c[0].startswith("PB"):
            items.append(dict(id=c[0], texto=c[1], sistema=c[2], prioridad=c[3], sp=int(c[4]), estado=c[5], sprint=c[6], req="—", tipo="tarea técnica"))
        else:
            items.append(dict(id=c[0], texto=c[1], sistema="", req=c[2], prioridad=c[3], sp=int(c[4]), estado=c[5], sprint=c[6], tipo="historia de usuario"))
    return items


def etiqueta_sprint(s):
    m = re.search(r"(\d+)", s)
    return f"sprint-{int(m.group(1))}" if m else "sprint-pendiente"


def main():
    items = leer_backlog()
    print(f"{len(items)} ítems en el backlog; SP totales {sum(i['sp'] for i in items)}")
    if seco:
        for i in items:
            print(f"  {i['id']:6} {i['sp']:>2} SP  {i['estado']:9} {i['sprint']:12} {RESPONSABLE.get(i['id'], 'Sin asignar')}")
        return

    repo = f"{DUENO}/{REPO}"
    # 1. etiquetas
    existentes = {x["name"] for x in gh("label", "list", "-R", repo, "--json", "name", "--limit", "100", json_salida=True)}
    nuevas = {"historia de usuario": "1d76db", "tarea técnica": "5319e7", "sprint-0": "cccccc", "sprint-1": "8d0739",
              "sprint-2": "faba09", "sprint-3": "6b052b", "sprint-4": "212529", "sprint-pendiente": "ededed"}
    for n, color in nuevas.items():
        if n not in existentes:
            gh("label", "create", n, "-R", repo, "--color", color)

    # 2. proyecto
    lista = gh("project", "list", "--owner", DUENO, "--format", "json", json_salida=True)["projects"]
    proyecto = next((p for p in lista if p["title"] == TITULO), None)
    if not proyecto:
        proyecto = gh("project", "create", "--owner", DUENO, "--title", TITULO, "--format", "json", json_salida=True)
        gh("project", "link", str(proyecto["number"]), "--owner", DUENO, "--repo", repo)
        print("proyecto creado:", proyecto["url"])
    num, pid = str(proyecto["number"]), proyecto["id"]

    campos = {f["name"]: f for f in gh("project", "field-list", num, "--owner", DUENO, "--format", "json", json_salida=True)["fields"]}
    for nombre, tipo, extra in [("SP", "NUMBER", []), ("Requisitos", "TEXT", []), ("Responsable", "TEXT", []),
                                ("Prioridad", "SINGLE_SELECT", ["--single-select-options", "Alta,Media,Baja"])]:
        if nombre not in campos:
            gh("project", "field-create", num, "--owner", DUENO, "--name", nombre, "--data-type", tipo, *extra)
    if "Sprint" not in campos:
        iters = ",".join(f'{{title:"{t}",startDate:"{d}",duration:{n}}}' for t, d, n in ITERACIONES)
        q = ('mutation($p:ID!){createProjectV2Field(input:{projectId:$p,dataType:ITERATION,name:"Sprint",'
             f'iterationConfiguration:{{startDate:"{ITERACIONES[0][1]}",duration:{ITERACIONES[0][2]},iterations:[{iters}]}}}})'
             '{projectV2Field{... on ProjectV2IterationField{id}}}}')
        gh("api", "graphql", "-f", f"query={q}", "-f", f"p={pid}")
    campos = {f["name"]: f for f in gh("project", "field-list", num, "--owner", DUENO, "--format", "json", json_salida=True)["fields"]}

    q = ('query($p:ID!){node(id:$p){... on ProjectV2{field(name:"Sprint"){... on ProjectV2IterationField{configuration{iterations{id title} completedIterations{id title}}}}}}}')
    cfg = gh("api", "graphql", "-f", f"query={q}", "-f", f"p={pid}", json_salida=True)
    conf = cfg["data"]["node"]["field"]["configuration"]
    # las iteraciones ya terminadas (Sprint 1) salen en completedIterations, no en iterations
    iteracion = {i["title"]: i["id"] for i in conf["iterations"] + conf["completedIterations"]}
    estado_opc = {o["name"]: o["id"] for o in campos["Status"]["options"]}
    prio_opc = {o["name"]: o["id"] for o in campos["Prioridad"]["options"]}

    # 3. issues + elementos del proyecto
    ya = {x["title"]: x for x in gh("issue", "list", "-R", repo, "--state", "all", "--limit", "200", "--json", "title,url,state", json_salida=True)}
    # url → elemento del proyecto (con sus campos), para completar los que quedaron a medias en una ejecución anterior
    en_proyecto = {x["content"]["url"]: x for x in gh("project", "item-list", num, "--owner", DUENO, "--format", "json", "--limit", "200", json_salida=True)["items"] if x.get("content", {}).get("url")}
    for it in items:
        corto = it["texto"] if len(it["texto"]) < 90 else it["texto"][:87] + "…"
        titulo = f"{it['id']} · {corto}"
        resp = RESPONSABLE.get(it["id"], "Sin asignar")
        cuerpo = (f"**{it['texto']}**\n\n- Requisito(s): {it['req']}\n- Story points: {it['sp']}\n- Estado: {it['estado']}\n"
                  f"- Sprint: {it['sprint']}\n- Responsable: {resp}\n\n"
                  "Trazabilidad con los requisitos: [REM-CADUS.md](../blob/main/docs/requisitos/rem-remus/REM-CADUS.md). "
                  "Backlog de origen: [product-backlog.md](../blob/main/docs/scrum/backlog/product-backlog.md).")
        if titulo in ya:
            url = ya[titulo]["url"]
        else:
            args = ["issue", "create", "-R", repo, "--title", titulo, "--body", cuerpo,
                    "--label", f"{it['tipo']},{etiqueta_sprint(it['sprint'])}"]
            if resp in ASIGNADO:
                args += ["--assignee", ASIGNADO[resp]]
            url = gh(*args).splitlines()[-1]
            if it["estado"] == "Hecho":
                gh("issue", "close", url, "--reason", "completed")
        existente = en_proyecto.get(url) or {}
        if existente:
            item = {"id": existente["id"]}
        else:
            item = gh("project", "item-add", num, "--owner", DUENO, "--url", url, "--format", "json", json_salida=True)
        base = ["project", "item-edit", "--id", item["id"], "--project-id", pid]
        # solo se rellenan los campos vacíos: así relanzar el script no pisa lo que el equipo haya cambiado después
        if existente.get("sP") is None and existente.get("sp") is None:
            gh(*base, "--field-id", campos["SP"]["id"], "--number", str(it["sp"]))
        if not existente.get("requisitos"):
            gh(*base, "--field-id", campos["Requisitos"]["id"], "--text", it["req"])
        if not existente.get("responsable"):
            gh(*base, "--field-id", campos["Responsable"]["id"], "--text", resp)
        if it["prioridad"] in prio_opc and not existente.get("prioridad"):
            gh(*base, "--field-id", campos["Prioridad"]["id"], "--single-select-option-id", prio_opc[it["prioridad"]])
        if not existente.get("status"):
            gh(*base, "--field-id", campos["Status"]["id"], "--single-select-option-id", estado_opc[ESTADO.get(it["estado"], "Todo")])
        m = re.search(r"Sprint-0?(\d+)", it["sprint"])
        if m and not existente.get("sprint") and f"Sprint {int(m.group(1))}" in iteracion:
            gh(*base, "--field-id", campos["Sprint"]["id"], "--iteration-id", iteracion[f"Sprint {int(m.group(1))}"])
        print("  ok", it["id"])

    # reparación: elementos que quedaron sin iteración (p. ej. si la iteración aún no estaba disponible al crearlos)
    por_titulo = {f"{i['id']} · {i['texto'] if len(i['texto']) < 90 else i['texto'][:87] + '…'}": i for i in items}
    for el in gh("project", "item-list", num, "--owner", DUENO, "--format", "json", "--limit", "200", json_salida=True)["items"]:
        it = por_titulo.get(el["title"])
        m = re.search(r"Sprint-0?(\d+)", it["sprint"]) if it else None
        if m and not el.get("sprint") and f"Sprint {int(m.group(1))}" in iteracion:
            gh("project", "item-edit", "--id", el["id"], "--project-id", pid, "--field-id", campos["Sprint"]["id"],
               "--iteration-id", iteracion[f"Sprint {int(m.group(1))}"])
            print("  iteración reparada", it["id"])

    # fechas de cierre reales (campo «Cierre») para calcular el burndown
    campos = {f["name"]: f for f in gh("project", "field-list", num, "--owner", DUENO, "--format", "json", json_salida=True)["fields"]}
    if "Cierre" not in campos:
        gh("project", "field-create", num, "--owner", DUENO, "--name", "Cierre", "--data-type", "DATE")
        campos = {f["name"]: f for f in gh("project", "field-list", num, "--owner", DUENO, "--format", "json", json_salida=True)["fields"]}
    for el in gh("project", "item-list", num, "--owner", DUENO, "--format", "json", "--limit", "200", json_salida=True)["items"]:
        clave = el["title"].split(" ")[0]
        if clave in CIERRE and el.get("cierre") != CIERRE[clave]:
            gh("project", "item-edit", "--id", el["id"], "--project-id", pid, "--field-id", campos["Cierre"]["id"], "--date", CIERRE[clave])
            print("  cierre", clave, CIERRE[clave])
    print("terminado:", proyecto["url"])


main()
