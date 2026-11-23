"""Añade las historias de la red social interna (RSI-HU-01 a RSI-HU-09, docs/redsocial/scrum/product-backlog-rsi.md) al GitHub Project
«CADUS · Scrum»: una issue por historia con sus campos (SP, Requisitos, Responsable, Prioridad, Estado y Cierre).
El campo Sprint (iteración) no se toca: sus iteraciones son las del CMS (Sprint 1 a 3) y reescribirlas podría soltar la asignación de
las demás tareas; el sprint de la red social va en la etiqueta y en el cuerpo de cada issue.
Uso: python scripts/scrum/crear_rsi.py [--dry-run]   (idempotente: no duplica issues ni elementos y vuelve a escribir los campos)"""
import json
import subprocess
import sys

GH = r"C:\Program Files\GitHub CLI\gh.exe"
DUENO, REPO, NUM = "pablitoruiizz", "proyecto_gsi", "1"
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--dry-run" in sys.argv
ASIGNADO = {"Pablo": "pablitoruiizz", "Joaquín": "joaquinluna2005-jpg", "Álvaro": "Alvaromartinez07", "Marcos": "Federomai"}
ENLACE = "[product-backlog-rsi.md](../blob/main/docs/redsocial/scrum/product-backlog-rsi.md)"
# id, historia, requisitos, SP, responsable, estado (Todo | In Progress | Done), cierre, sprint, nota de estado
H = [
    ("RSI-HU-01", "Como equipo, queremos un caso de negocio y un REM de la red social para saber qué se construye y por qué Teams.", "OBJ-R01 a OBJ-R05, RC-R01 a RC-R03", 3, "Pablo", "Done", "2026-11-20", "Sprint 1 de la red social (16/11 – 22/11)", "Hecho en main el 20/11; falta la revisión de otra persona."),
    ("RSI-HU-02", "Como equipo, queremos un UML de análisis y otro de diseño para pasar de los conceptos del Lab 5 a Teams.", "RF-R01, RF-R06, IR-R01 a IR-R05", 3, "Álvaro", "Done", "2026-11-22", "Sprint 1 de la red social (16/11 – 22/11)", "Borrador de Pablo (20/11) y revisión de Álvaro en main el 22/11 (PR #89)."),
    ("RSI-HU-03", "Como Ejecutiva, quiero un equipo privado por grupo principal (Ejecutiva, Delegaciones y Asamblea) con propietarios y miembros.", "RF-R01, RF-R02, RF-R04, RF-R06, RN-R05", 3, "Pablo", "Done", "2026-11-20", "Sprint 1 de la red social (16/11 – 22/11)", "Equipos creados el 16/11 y cuatro propietarios el 20/11; capturas 01 y 02."),
    ("RSI-HU-04", "Como Ejecutiva, quiero un canal de avisos donde solo yo publique y un canal privado por delegación para que cada una vea solo lo suyo.", "RF-R03, RF-R05, RN-R01, RN-R02, CU-R01, CU-R04, CU-R05", 5, "Marcos", "Done", "2026-11-22", "Sprint 1 de la red social (16/11 – 22/11)", "Configurado por Marcos el 21/11 y en main el 22/11; comprobado en Teams por Pablo (Avisos y tres canales privados). Aislamiento probado el 22/11 con una cuenta Miembro (Álvaro): no publica en «Avisos» y no ve los canales ajenos."),
    ("RSI-HU-05", "Como Ejecutiva y delegación, queremos calendario, tareas, formularios y enlace al DMS dentro de Teams.", "RF-R07 a RF-R10, RN-R03, CU-R02, CU-R03", 5, "Joaquín", "Done", "2026-11-22", "Sprint 1 de la red social (16/11 – 22/11)", "Planner, Forms y pestaña del DMS (Joaquín, capturas 07 a 09) y calendario (Marcos, captura 06), en main el 22/11; solo el plan de la Asamblea tiene captura."),
    ("RSI-HU-06", "Como equipo, queremos el documento de la entrega, el REM exportado y el zip con la lista del profesor.", "Todos", 3, "Pablo", "Done", "2026-11-22", "Sprint 1 de la red social (16/11 – 22/11)", "Hecho en main el 22/11 con el commit de cierre: documento, PDF del REM y zip; el envío se hace esa noche."),
    ("RSI-HU-07", "Como Ejecutiva, quiero avisos automáticos cuando se asigna una tarea o vence su fecha.", "RF-R11, RC-R02", 3, "Joaquín", "Todo", "", "Sprint 2 de la red social (23/11 – 29/11)", "Pendiente (Lab 8)."),
    ("RSI-HU-08", "Como Ejecutiva, quiero una aplicación sencilla con la lista de delegaciones y su estado, si el tenant lo permite.", "RF-R12, RC-R02", 3, "Álvaro", "Todo", "", "Sprint 2 de la red social (23/11 – 29/11)", "Borrador de especificación de Álvaro (powerapps-especificacion.md); no se ha comprobado que se pueda crear y guardar una aplicación."),
    ("RSI-HU-09", "Como Ejecutiva y delegación, queremos que cada tablero de Planner siga un patrón de diseño explícito, para entender cada plan sin explicación (Lab 6).", "RF-R09, RNF-R02", 2, "Joaquín", "Todo", "", "Sprint 2 de la red social (23/11 – 29/11)", "Análisis redactado en docs/redsocial/diseno-tableros-planner.md; falta decidir si el plan de la asamblea pasa a «Proceso de tareas», rehacerlo en Planner con su captura y reflejarlo en el UML."),
]


def gh(*a, js=False):
    r = subprocess.run([GH, *a], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise SystemExit(f"gh {' '.join(a[:3])}… falló: {r.stderr.strip()}")
    return json.loads(r.stdout) if js else r.stdout.strip()


repo = f"{DUENO}/{REPO}"
if SECO:
    for i, t, req, sp, quien, est, cierre, sprint, nota in H:
        print(f"[seco] {i} · {sp} SP · {quien} · {est}")
    raise SystemExit(0)
pid = gh("project", "view", NUM, "--owner", DUENO, "--format", "json", js=True)["id"]
campos = {f["name"]: f for f in gh("project", "field-list", NUM, "--owner", DUENO, "--format", "json", js=True)["fields"]}
estado = {o["name"]: o["id"] for o in campos["Status"]["options"]}
prio = {o["name"]: o["id"] for o in campos["Prioridad"]["options"]}
etiquetas = {l["name"] for l in gh("label", "list", "-R", repo, "--limit", "100", "--json", "name", js=True)}
if "red social" not in etiquetas:
    gh("label", "create", "red social", "-R", repo, "--color", "6f42c1", "--description", "Red social interna del CADUS (Lab 5, MS Teams)")
previas = gh("issue", "list", "-R", repo, "--state", "all", "--limit", "400", "--json", "title,url,number", js=True)
items = gh("project", "item-list", NUM, "--owner", DUENO, "--format", "json", "--limit", "400", js=True)["items"]

for i, texto, req, sp, quien, est, cierre, sprint, nota in H:
    titulo = f"{i} · {texto}"
    cuerpo = (f"**{texto}**\n\n- Requisito(s): {req}\n- Story points: {sp} (estimados a posteriori el 22/11/2026)\n- Estado: {est}. {nota}\n- Sprint: {sprint}\n"
              f"- Responsable: {quien}\n\nDefinición de hecho: entregable en main, captura explicada si es de Teams y revisión de otra persona anotada "
              f"(esta última aún no se ha cumplido en el Sprint 1).\n\nBacklog de origen: {ENLACE}. Trazabilidad: [REM de la red social](../blob/main/docs/redsocial/rem-remus/carga-remus.md).")
    previa = next((x for x in previas if x["title"].startswith(i)), None)
    if previa:
        url, num = previa["url"], str(previa["number"])
        gh("issue", "edit", num, "-R", repo, "--body", cuerpo)
    else:
        url = gh("issue", "create", "-R", repo, "--title", titulo, "--body", cuerpo, "--label", "historia de usuario,red social",
                 "--assignee", ASIGNADO[quien]).splitlines()[-1]
        num = url.rsplit("/", 1)[-1]
    el = next((x for x in items if x.get("content", {}).get("url") == url), None)
    item_id = el["id"] if el else gh("project", "item-add", NUM, "--owner", DUENO, "--url", url, "--format", "json", js=True)["id"]
    base = ["project", "item-edit", "--id", item_id, "--project-id", pid]
    gh(*base, "--field-id", campos["SP"]["id"], "--number", str(sp))
    gh(*base, "--field-id", campos["Responsable"]["id"], "--text", quien)
    gh(*base, "--field-id", campos["Requisitos"]["id"], "--text", req)
    gh(*base, "--field-id", campos["Prioridad"]["id"], "--single-select-option-id", prio["Alta" if sp >= 5 or i <= "RSI-HU-06" else "Media"])
    gh(*base, "--field-id", campos["Status"]["id"], "--single-select-option-id", estado[est])
    if cierre:
        gh(*base, "--field-id", campos["Cierre"]["id"], "--date", cierre)
        gh("issue", "close", num, "-R", repo, "--reason", "completed")
    print(f"ok {i} ({est}) {url}")
