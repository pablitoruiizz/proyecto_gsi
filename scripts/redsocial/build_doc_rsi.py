"""Genera los documentos Word de la entrega de la Red Social Interna del CADUS (Lab 5, MS Teams) en docs/redsocial/entrega:
  Entrega-RSI-CADUS.docx     documento principal (Business Case, REM, análisis, diseño, implementación, trazabilidad y SCRUM)
  Business-Case-RSI.docx     el Business Case solo (sale de docs/redsocial/business-case.md)
Reutiliza las utilidades de scripts/dms/build_doc_dms.py. Las capturas se leen de docs/redsocial/capturas; las que falten se
avisan y se marcan como pendientes en el documento (no se inventan).
Uso: python scripts/redsocial/build_doc_rsi.py"""
import csv
import json
import os
import re
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "scripts", "dms"))
import build_doc_dms as B  # noqa: E402

RSI = os.path.join(RAIZ, "docs", "redsocial")
ENT = os.path.join(RSI, "entrega")
IMG = os.path.join(RSI, "img")
CAP = os.path.join(RSI, "capturas")
D = json.load(open(os.path.join(RAIZ, "scripts", "remus", "rsi_data.json"), encoding="utf-8-sig"))
VERSION = ".".join(str(n) for n in D["version"])
FECHA_ENTREGA = "22/11/2026"
FECHA = "20/11/2026"  # fecha del estado que se describe; actualizar al regenerar
AVISOS = B.AVISOS

# capturas previstas: archivo -> (pie, explicación, requisitos). Solo se incluyen las que existen en docs/redsocial/capturas.
CAPS = {
    "01-equipos.jpg": ("Los tres equipos privados del CADUS en Teams.", "Se crearon «CADUS · Ejecutiva», «CADUS · Delegaciones» y «CADUS · Asamblea» como equipos privados, con la plantilla «Equipo básico», en el tenant de la Universidad de Sevilla.", "RF-R01 · RC-R01"),
    "02-ejecutiva-miembros.jpg": ("Propietarios del equipo CADUS · Ejecutiva.", "Los cuatro integrantes del equipo del proyecto (Pablo, Álvaro, Joaquín y Marcos) son propietarios, con rol de propietario en Teams; el equipo no tiene más miembros.", "RF-R02 · RF-R06"),
    "03-delegaciones-avisos.jpg": ("Canal de avisos con moderación.", "En el canal General de CADUS · Delegaciones solo los propietarios publican; las delegaciones leen.", "RF-R05 · RN-R01"),
    "04-delegaciones-canales-privados.jpg": ("Canales privados de las delegaciones.", "Un canal privado por delegación dentro del equipo CADUS · Delegaciones (tres de ejemplo; el patrón se repite para las 27).", "RF-R03 · CU-R05"),
    "05-vista-miembro.jpg": ("Lo que ve una delegación.", "Un miembro solo ve su propio canal privado y el canal de avisos, no los de las demás delegaciones.", "RN-R02 · CU-R04"),
    "06-asamblea-calendario.jpg": ("Equipo de la asamblea con su calendario.", "El equipo CADUS · Asamblea con el canal Cursos y un calendario con un evento de ejemplo.", "RF-R04 · RF-R08 · CU-R02"),
    "07-archivos-dms.jpg": ("Pestaña de archivos enlazada al DMS.", "La pestaña de archivos apunta al sitio de SharePoint del DMS: el documento oficial no se copia a Teams.", "RF-R07 · RN-R03 · CU-R03"),
    "08-planner.jpg": ("Plan de tareas en Planner.", "Plan «Preparación de la asamblea» con cubos y tareas asignadas a distintas personas.", "RF-R09 · CU-R02"),
    "09-forms.jpg": ("Formulario de confirmación de asistencia.", "Formulario de Forms para recoger la asistencia de las delegaciones.", "RF-R10"),
}
# capturas que necesita cada caso de uso para considerarse observado
CAP_CU = {"CU-R01": ["03-delegaciones-avisos.jpg"], "CU-R02": ["06-asamblea-calendario.jpg", "08-planner.jpg"],
          "CU-R03": ["07-archivos-dms.jpg", "04-delegaciones-canales-privados.jpg"], "CU-R04": ["05-vista-miembro.jpg"],
          "CU-R05": ["04-delegaciones-canales-privados.jpg"]}
# estado de las tareas del plan a la fecha del documento (actualizar al regenerar)
ESTADO = {"R-01": "Borrador hecho; falta la revisión de otra persona", "R-02": "Hecho (REM en REMUS); falta la exportación a PDF",
          "R-03": "Borrador hecho; falta la revisión de Álvaro", "R-04": "Borrador hecho; falta la revisión de Álvaro",
          "R-05": "Equipos creados el 16/11; configuración pendiente (Marcos)", "R-06": "Pendiente (Joaquín)", "R-07": "Pendiente (Marcos)",
          "R-08": "Pendiente (Joaquín)", "R-09": "En curso (Pablo)", "R-10": "Pendiente (todos)"}


def existe(nombre):
    return os.path.exists(os.path.join(CAP, nombre))


def md_en_doc(doc, ruta, prefijo="", omitir_titulo=True):
    """Pinta un .md (títulos, párrafos, tablas y listas) dentro de un documento ya abierto; los títulos ## pasan a nivel 2."""
    lineas = open(ruta, encoding="utf-8-sig").read().splitlines()
    i = 0
    while i < len(lineas):
        l = lineas[i].rstrip()
        if not l.strip():
            pass
        elif l.startswith("# "):
            if not omitir_titulo:
                doc.add_heading(l[2:].strip(), 1)
        elif l.startswith("## "):
            t = re.sub(r"^\d+\.\s*", "", l[3:].strip())
            n = re.match(r"^## (\d+)\.", l)
            doc.add_heading((f"{prefijo}{n.group(1)} " if n and prefijo else "") + t, 2)
        elif l.startswith(">"):
            B.par(doc, l.lstrip("> ").replace("`", ""), cursiva=True, tam=9.5)
        elif l.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                if not re.match(r"^\|[\s:|-]+\|$", lineas[i].strip()):
                    filas.append(B.celdas(lineas[i]))
                i += 1
            n = len(filas[0])
            anchos = {2: [5, 12], 3: [4, 5, 8], 4: [3, 4, 5, 5]}.get(n)
            B.tabla(doc, filas[0], filas[1:], anchos, tam=9)
            continue
        elif re.match(r"^[-*] ", l):
            B.vineta(doc, l[2:].replace("`", ""))
        elif re.match(r"^\d+\.\s", l):
            B.vineta(doc, re.sub(r"^\d+\.\s*", "", l).replace("`", ""))
        else:
            B.par(doc, l.replace("`", ""))
        i += 1


def business_case_docx():
    doc = B.nuevo()
    doc.add_heading("Business Case — Red Social Interna del CADUS (MS Teams)", 0)
    md_en_doc(doc, os.path.join(RSI, "business-case.md"))
    sal = os.path.join(ENT, "Business-Case-RSI.docx")
    doc.save(sal)
    return sal


def tareas_plan():
    """Filas de la tabla de la entrega del 22/11 de plan-lab5.md: (id, tarea, quién)."""
    filas = []
    on = False
    for l in open(os.path.join(RSI, "plan-lab5.md"), encoding="utf-8").read().splitlines():
        if l.startswith("## Entrega del 22/11"):
            on = True
        elif l.startswith("## ") and on:
            break
        m = re.match(r"^\| (R-\d+) \| (.*?) \| (.*?) \| (.*?) \|$", l)
        if on and m:
            tarea = re.sub(r"\s*\*\*.*", "", m.group(2))
            tarea = re.split(r"\. (?=\*\*|Creados|Borrador)", tarea)[0].rstrip(".")
            filas.append((m.group(1), tarea, m.group(3)))
    return filas


def principal():
    doc = B.nuevo()
    doc.add_heading("Red Social Interna del CADUS — Entrega en Microsoft Teams", 0)
    B.par(doc, "Gestión de Sistemas de Información (GSI) · Universidad de Sevilla · Lab 5 (Red Social Interna, MS Teams)", cursiva=True)
    B.par(doc, "Equipo: Pablo Ruiz Vidal (Product Owner), Joaquín Luna Canela (Scrum Master), Álvaro Martínez Ocaña y Marcos-Paban Delgado Rodríguez. Cliente: CADUS.")
    B.par(doc, f"REM de la red social versión {VERSION} · estado a {FECHA} · fecha de entrega: {FECHA_ENTREGA}")

    doc.add_heading("1. Resumen", 1)
    B.par(doc, "La red social interna reúne la comunicación, las tareas, el calendario y los archivos de la Ejecutiva, las delegaciones de centro y las asambleas del CADUS en **Microsoft Teams**, dentro de la cuenta de la Universidad de Sevilla. Es independiente del portal (CMS) y del gestor documental (DMS), con los que se relaciona: los documentos oficiales siguen en el DMS y la red social los enlaza. Esta es la entrega de la estructura de Teams y Planner (Lab 7); las automatizaciones con Power Automate y PowerApps llegan en la entrega del 29/11.")
    n_cap = sum(1 for k in CAPS if existe(k))
    B.tabla(doc, ["Contenido pedido en el Lab 5", "Dónde está"], [
        ["Caso de negocio (Business Case)", "Sección 2 y documento aparte `Business-Case-RSI`"],
        ["Grupos principales y piloto", "Secciones 5 y 6: tres equipos privados creados en Teams"],
        ["Requisitos (REM): caso de negocio, requisitos del sistema software y glosario", "Sección 3 y proyecto REMUS `RSI.rem` (más la hoja `carga-remus.md`)"],
        ["Glosario de términos", "Sección 3.9 y glosario del REM"],
        ["Análisis: diagrama de clases con Role, Group, Subgroups, Tool y Permission", "Sección 4"],
        ["Diseño: el diagrama pasado a conceptos de Microsoft Teams", "Sección 5"],
        ["Implementación: capturas explicadas", f"Sección 6: {n_cap} de {len(CAPS)} capturas previstas"],
        ["Seguimiento SCRUM", "Sección 8"]], [7, 10], tam=9)

    doc.add_heading("2. Caso de negocio (Business Case)", 1)
    md_en_doc(doc, os.path.join(RSI, "business-case.md"), prefijo="2.")

    doc.add_heading("3. Requisitos (REM): requisitos del sistema software", 1)
    B.par(doc, f"El REM se mantiene en REMUS (`RSI.rem`, versión {VERSION}) a partir de `scripts/remus/rsi_data.json`. Cada requisito lleva un código que se repite en el UML, en las capturas y en la trazabilidad.")
    doc.add_heading("3.1 Objetivos", 2)
    B.tabla(doc, ["Código", "Objetivo", "El sistema deberá"], [[o["id"], o["name"], o["description"]] for o in D["objectives"]], [2, 4, 11], tam=9)
    doc.add_heading("3.2 Actores", 2)
    B.tabla(doc, ["Código", "Actor", "Representa a"], [[a["id"], a["name"], a["role"]] for a in D["actors"]], [2, 4, 11], tam=9)
    doc.add_heading("3.3 Requisitos de información", 2)
    B.tabla(doc, ["Código", "Concepto", "Datos"], [[r["id"], r["name"], "; ".join(r["data"])] for r in D["information"]], [2, 3.5, 11.5], tam=8.5)
    doc.add_heading("3.4 Requisitos de interfaz y funcionales (grupos y herramientas)", 2)
    B.tabla(doc, ["Código", "Nombre", "El sistema deberá", "Entrega"], [[r["id"], r["name"], r["description"], r["comments"]] for r in D["ui"] + D["functional"]], [1.8, 3.4, 9.2, 2.6], tam=8.5)
    doc.add_heading("3.5 Requisitos no funcionales", 2)
    B.tabla(doc, ["Código", "Nombre", "El sistema deberá"], [[r["id"], r["name"], r["description"]] for r in D["nonfunctional"]], [2, 3.5, 11.5], tam=9)
    doc.add_heading("3.6 Reglas de negocio", 2)
    B.tabla(doc, ["Código", "Nombre", "Regla"], [[r["id"], r["name"], r["description"]] for r in D["rules"]], [2, 3.5, 11.5], tam=9)
    doc.add_heading("3.7 Restricciones del entorno", 2)
    B.tabla(doc, ["Código", "Nombre", "Descripción"], [[r["id"], r["name"], r["description"]] for r in D["environment"]], [2, 4, 11], tam=9)
    doc.add_heading("3.8 Casos de uso", 2)
    actores = {a["id"]: a["name"] for a in D["actors"]}
    for u in D["usecases"]:
        pasos = " ".join(f"{i}. {(actores[s['actor']] if s['who'] == 'actor' else 'El sistema')} {s['text']}." for i, s in enumerate(u["steps"], 1))
        B.par(doc, f"**{u['id']} {u['name']}.** Cuándo: {u['trigger']}. Precondición: {u['pre']}. {pasos} Postcondición: {u['post']}.")

    doc.add_heading("3.9 Glosario de términos", 2)
    B.tabla(doc, ["Término", "Significado"], [[g["name"], g["text"]] for g in D["paragraphs"]["glossary"]], [4, 13], tam=9)

    doc.add_heading("4. Análisis", 1)
    B.par(doc, "El UML de análisis recoge los conceptos del Lab 5: rol, grupo y subgrupos, herramienta y permiso. Las etiquetas en rojo son los códigos de requisito.")
    B.figura(doc, os.path.join(IMG, "uml-rsi-analisis.png"), "UML de análisis de la red social interna con etiquetas de trazabilidad.", 17)

    doc.add_heading("5. Diseño", 1)
    B.par(doc, "En el diseño cada concepto del análisis pasa a un elemento de Microsoft Teams: los grupos son equipos, los subgrupos son canales privados, los roles son los de Teams y las herramientas son pestañas o aplicaciones de cada canal. Se usan tres equipos y no uno porque Teams limita los canales privados por equipo y las 27 delegaciones más la Ejecutiva casi lo agotarían.")
    B.figura(doc, os.path.join(IMG, "uml-rsi-diseno.png"), "UML de diseño de la red social interna en Microsoft Teams.", 17)
    B.tabla(doc, ["Concepto del análisis", "Elemento del diseño en Teams"], [
        ["Grupo", "Equipo privado de Teams: CADUS · Ejecutiva, CADUS · Delegaciones y CADUS · Asamblea"],
        ["Subgrupo", "Canal privado del equipo Delegaciones, uno por centro (27)"],
        ["Rol", "Propietario, miembro o invitado; cuentas de grupo (la del CADUS y una por delegación)"],
        ["Permiso", "Quién publica (avisos solo para propietarios) y quién ve cada canal (los privados, solo sus miembros)"],
        ["Herramienta", "Pestañas del canal: Archivos (enlace al DMS), Calendario, Planner, Forms; después Power Automate y PowerApps"]], [5, 12], tam=9, titulo="Del análisis al diseño")

    doc.add_heading("6. Implementación en Teams", 1)
    B.par(doc, "Capturas del tenant de la Universidad de Sevilla, con datos de ejemplo. Cada una indica el requisito al que responde. Las que todavía no se han hecho aparecen como pendientes: no se muestra ninguna captura que no exista.")
    hechas = [k for k in CAPS if existe(k)]
    for k in CAPS:
        pie, expl, req = CAPS[k]
        if k in hechas:
            doc.add_heading(pie.rstrip("."), 3)
            B.figura(doc, os.path.join(CAP, k), pie, 15)
            B.par(doc, f"{expl} Responde a {req.replace(' · ', ', ')}.")
        else:
            AVISOS.append(f"falta la captura docs/redsocial/capturas/{k}")
    pend = [k for k in CAPS if k not in hechas]
    if pend:
        B.tabla(doc, ["Captura pendiente", "Qué debe demostrar", "Requisitos"], [[k, CAPS[k][1], CAPS[k][2]] for k in pend], [4.5, 9, 3.5], tam=8.5, titulo="Capturas pendientes a " + FECHA)

    doc.add_heading("7. Trazabilidad", 1)
    filas_t = []
    for u in D["usecases"]:
        req = next((t[1] for t in D["traces"] if t[0] == u["id"]), [])
        req = [r for r in req if r.startswith(("RF-", "RN-", "RNF-"))]
        caps = CAP_CU.get(u["id"], [])
        ok = caps and all(existe(c) for c in caps)
        filas_t.append([u["id"], ", ".join(req), ", ".join(c[:2] for c in caps) or "—", "Observado en capturas" if ok else "Pendiente de configurar o capturar"])
    B.tabla(doc, ["Caso de uso", "Requisitos", "Capturas", "Estado"], filas_t, [2, 7, 2.5, 5.5], tam=8.5, titulo="Casos de uso, requisitos y capturas")
    n_trazas = sum(len(t[1]) for t in D["traces"])
    B.par(doc, f"Los objetivos, los requisitos de información y las reglas están enlazados con los requisitos y los casos de uso en las trazas de `RSI.rem` ({n_trazas} trazas declaradas; REMUS añade las inversas).")

    doc.add_heading("8. Seguimiento SCRUM", 1)
    B.par(doc, "La red social tiene su propio seguimiento, independiente del CMS y del DMS. Equipo de cuatro personas desde el 16/11/2026. Entrega del 22/11: estructura de Teams y Planner; entrega del 29/11: Power Automate y PowerApps; entrega final: 07/12/2026.")
    B.tabla(doc, ["ID", "Tarea", "Quién", f"Estado a {FECHA}"], [[i, t, q, ESTADO.get(i, "—")] for i, t, q in tareas_plan()], [1.3, 8.2, 3.2, 4.3], tam=8.5, titulo="Backlog de la entrega del 22/11")
    carpeta = os.path.join(RSI, "scrum")
    csvs = sorted(f for f in os.listdir(carpeta)) if os.path.isdir(carpeta) else []
    if any(f.endswith(".csv") for f in csvs):
        filas = list(csv.DictReader(open(os.path.join(carpeta, next(f for f in csvs if f.endswith('.csv'))), encoding="utf-8")))
        B.par(doc, "Burndown de la red social: ver `scrum/` (se mantiene cada día).")
        B.tabla(doc, ["Fecha", "Pendiente", "Ideal"], [[f["fecha"], f.get("real_sp") or "—", f.get("ideal_sp", "")] for f in filas], [4, 4, 4], tam=8.5)
    else:
        B.par(doc, "El burndown, el sprint backlog con puntos y la Sprint Review los mantiene Joaquín en `docs/redsocial/scrum/` y todavía no están: se añaden al documento al subirlos.")
        AVISOS.append("falta docs/redsocial/scrum (backlog con puntos, burndown y review de Joaquín)")

    doc.add_heading("9. Pendiente y limitaciones", 1)
    for t in ("Configurar los canales, la moderación del canal de avisos y los canales privados de ejemplo (Marcos) y hacer las capturas.",
              "Los planes de Planner y los formularios (Joaquín) dependen de lo que permita el tenant de la Universidad.",
              "Probar con una cuenta distinta que cada delegación solo ve su canal (RN-R02): lo hace otra persona, no quien lo configuró. Como los cuatro integrantes son propietarios de los tres equipos, hace falta una cuenta que sea solo miembro.",
              "Power Automate y PowerApps (RF-R11 y RF-R12) son de la entrega del 29/11 y dependen de que el tenant los ofrezca; no se ha comprobado.",
              "No hay contacto con el CADUS en el equipo desde el 16/11: las decisiones que dependen del CADUS son suposiciones del caso de negocio.",
              "El límite de canales privados por equipo (30 según la documentación de Microsoft) no se ha comprobado en el tenant.",
              "Los datos del piloto son de ejemplo; las cuentas de delegación reales no existen en Teams todavía."):
        B.vineta(doc, t)
    sal = os.path.join(ENT, "Entrega-RSI-CADUS.docx")
    doc.save(sal)
    return sal


def main():
    os.makedirs(ENT, exist_ok=True)
    for f in (principal, business_case_docx):
        print("generado", f())
    if AVISOS:
        print(f"\nAVISOS ({len(AVISOS)}):")
        for a in AVISOS:
            print("  -", a)
    else:
        print("\nSin avisos.")


if __name__ == "__main__":
    main()
