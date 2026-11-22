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
FECHA = "22/11/2026"  # fecha del estado que se describe; actualizar al regenerar
AVISOS = B.AVISOS

# capturas previstas: archivo -> (pie, explicación, requisitos). Solo se incluyen las que existen en docs/redsocial/capturas.
CAPS = {
    "01-equipos.jpg": ("Los tres equipos privados del CADUS en Teams.", "Se crearon «CADUS · Ejecutiva», «CADUS · Delegaciones» y «CADUS · Asamblea» como equipos privados, con la plantilla «Equipo básico», en el tenant de la Universidad de Sevilla (junto al equipo de la asignatura).", "RF-R01 · RC-R01"),
    "02-ejecutiva-miembros.jpg": ("Propietarios del equipo CADUS · Ejecutiva.", "Los cuatro integrantes del equipo del proyecto (Pablo, Álvaro, Joaquín y Marcos) son propietarios, con rol de propietario en Teams; el equipo no tiene más miembros.", "RF-R02 · RF-R06"),
    "10-ejecutiva-canales.jpg": ("Canales del equipo CADUS · Ejecutiva.", "El equipo de la Ejecutiva tiene el canal General y el canal estándar «Preparación de avisos», donde se prepara lo que luego se publica. La captura es de la cuenta de Marcos.", "RF-R02"),
    "03-delegaciones-avisos.jpg": ("Moderación del canal de avisos.", "En «Configuración» del canal General de CADUS · Delegaciones, la moderación está en «Solo los propietarios pueden publicar mensajes»: las delegaciones leen y no inician conversaciones. La captura es de la cuenta de Marcos.", "RF-R05 · RN-R01"),
    "11-delegaciones-avisos-renombrado.jpg": ("Canal de avisos renombrado.", "Teams permite renombrar el canal General como «Avisos», que es el nombre que usa el diseño. La captura es de la cuenta de Marcos.", "RF-R05"),
    "04-delegaciones-canales-privados.jpg": ("Canales privados de las delegaciones.", "Lista de canales de CADUS · Delegaciones: «Avisos» y tres canales privados con candado, «Delegación · Biología», «Delegación · Derecho» y «Delegación · ETSII» (tres de ejemplo; el patrón se repite para las 27). La captura es de la cuenta de Marcos.", "RF-R03 · CU-R05"),
    "05-vista-miembro.jpg": ("Lo que ve una delegación.", "Con la cuenta de Joaquín, que representa a la delegación de Biología, la lista del equipo solo muestra «Avisos» y «Delegación · Biología»: no aparecen los canales de ETSII ni de Derecho. Joaquín es propietario del equipo, pero un canal privado solo lo ven sus miembros, así que la prueba vale para el aislamiento entre delegaciones.", "RN-R02 · CU-R04"),
    "05b-avisos-solo-miembro.jpg": ("«Avisos» visto por un miembro.", "Con la cuenta de Álvaro como Miembro (no propietario; se le bajó de Propietario para la prueba el 22/11, por orden de Pablo, y se le volvió a subir), el canal «Avisos» no deja publicar: Teams muestra «Solo los moderadores del canal pueden publicar en este canal.» La captura no muestra el rol.", "RF-R05 · RN-R01"),
    "05c-canales-solo-miembro.jpg": ("Canales que ve un miembro.", "La misma cuenta, como Miembro de CADUS · Delegaciones, solo ve «Avisos» y «Delegación · ETSII» (del que es miembro): no ve los canales privados de Derecho ni de Biología. La captura no muestra el rol.", "RF-R03 · RN-R02"),
    "06-asamblea-calendario.jpg": ("Equipo de la asamblea con su calendario.", "En el canal General de CADUS · Asamblea, la pestaña «Calendario del canal» muestra el evento «Asamblea Noviembre» el jueves 26/11/2026 de 17:00 a 18:00; el equipo tiene además el canal Cursos. La captura es de la cuenta de Marcos.", "RF-R04 · RF-R08 · CU-R02"),
    "07-archivos-dms.jpg": ("Pestaña del canal que muestra el DMS.", "El canal General de CADUS · Asamblea tiene una pestaña «DMS · Órganos de gobierno» que enseña el sitio de SharePoint del DMS, con las actas y la plantilla de acta: los documentos oficiales se leen desde su sitio y no se copian a Teams. La captura es de la cuenta de Joaquín.", "RF-R07 · RN-R03 · CU-R03"),
    "07b-archivos-dms-marcos.jpg": ("La misma pestaña del DMS, vista por Marcos.", "La misma pestaña, antes de renombrarla, con la cuenta de Marcos: los documentos del DMS se abren desde su sitio.", "RF-R07 · RN-R03"),
    "08-planner.jpg": ("Plan de tareas en Planner.", "Plan «Preparación de la Asamblea» en el equipo CADUS · Asamblea, con los cubos Por hacer (2), En curso (1) y Hecho (1) y cuatro tareas de ejemplo asignadas a distintas personas y con fecha límite. La captura es de la cuenta de Joaquín y es anterior a un ajuste: la tarea «Preparar la plantilla del acta» vence ahí el 27/11 y el 22/11 se cambió al 25/11, porque la asamblea es el 26/11.", "RF-R09 · CU-R02"),
    "09-forms.jpg": ("Formulario de confirmación de asistencia.", "Formulario de Forms «Confirmación de asistencia», anclado como pestaña del canal General de CADUS · Asamblea, con dos preguntas: si asistirá la delegación y de qué delegación se trata. La captura es de la cuenta de Joaquín.", "RF-R10"),
}
# capturas que necesita cada caso de uso para considerarse observado
CAP_CU = {"CU-R01": ["03-delegaciones-avisos.jpg", "11-delegaciones-avisos-renombrado.jpg", "05b-avisos-solo-miembro.jpg"], "CU-R02": ["06-asamblea-calendario.jpg", "08-planner.jpg"],
          "CU-R03": ["07-archivos-dms.jpg", "04-delegaciones-canales-privados.jpg"], "CU-R04": ["05-vista-miembro.jpg", "05c-canales-solo-miembro.jpg"],
          "CU-R05": ["04-delegaciones-canales-privados.jpg"]}
# estado de las tareas del plan a la fecha del documento (actualizar al regenerar)
ESTADO = {"R-01": "Hecho con el índice del Lab 5; falta la revisión de otra persona", "R-02": "Hecho (REM en REMUS y PDF exportado el 22/11)",
          "R-03": "Hecho y revisado por Álvaro (UML en main)", "R-04": "Hecho y revisado por Álvaro (UML de diseño con los planes de Planner)",
          "R-05": "Hecho: tres equipos, cuatro propietarios, Avisos con moderación, canal Cursos, tres canales privados y calendario (capturas 01 a 06, 10 y 11)",
          "R-06": "Hecho: pestañas de Planner de los tres equipos (Coordinación de la Ejecutiva, Seguimiento de las delegaciones y Preparación de la Asamblea), Forms y pestaña del DMS; solo el plan de la Asamblea tiene captura (08)",
          "R-07": "Hecho: 14 capturas (01 a 11, 05b, 05c y 07b); la prueba con una cuenta solo miembro se hizo el 22/11 (capturas 05b y 05c)",
          "R-08": "Hecho el 22/11 por Pablo con Claude (puntos estimados a posteriori)", "R-09": "Hecho el 22/11 con el commit de cierre; falta solo enviarlo (Pablo)", "R-10": "Revisión con Codex hecha el 22/11 y corregida; prueba cruzada humana parcial (Joaquín y Álvaro probaron el aislamiento de canales; Álvaro revisó los UML)"}


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
        elif l.startswith("### "):
            doc.add_heading(l[4:].strip(), 3)
        elif l.startswith("## "):
            doc.add_heading(l[3:].strip(), 2)
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

    doc.add_heading("Resumen", 1)
    B.par(doc, "La red social interna reúne la comunicación, las tareas, el calendario y los archivos de la Ejecutiva, las delegaciones de centro y las asambleas del CADUS en **Microsoft Teams**, dentro de la cuenta de la Universidad de Sevilla. Es independiente del portal (CMS) y del gestor documental (DMS), con los que se relaciona: los documentos oficiales siguen en el DMS y la red social los enlaza. Esta es la entrega de la estructura de Teams y Planner (Lab 7); las automatizaciones con Power Automate y PowerApps llegan en la entrega del 29/11.")
    n_cap = sum(1 for k in CAPS if existe(k))
    B.tabla(doc, ["Contenido pedido en el Lab 5", "Dónde está"], [
        ["Caso de negocio (Business Case), con el índice del Lab 5", "Sección 1 y documento aparte `Business-Case-RSI`"],
        ["Grupos principales y piloto", "Secciones 5 y 6: tres equipos privados creados en Teams, con canales, roles y herramientas"],
        ["Requisitos (REM): caso de negocio, requisitos del sistema software y glosario", "Sección 2 y proyecto REMUS `RSI.rem` (más la hoja `carga-remus.md`)"],
        ["Glosario de términos", "Sección 3 y glosario del REM"],
        ["Análisis: diagrama de clases con Role, Group, Subgroups, Tool y Permission", "Sección 4"],
        ["Diseño: el diagrama pasado a conceptos de Microsoft Teams", "Sección 5"],
        ["Implementación: capturas explicadas", f"Sección 6: {n_cap} de {len(CAPS)} capturas previstas"],
        ["Seguimiento SCRUM", "Sección 8"]], [7, 10], tam=9)

    doc.add_heading("1. Caso de negocio (Business Case)", 1)
    md_en_doc(doc, os.path.join(RSI, "business-case.md"))

    doc.add_heading("2. Requisitos del sistema software", 1)
    B.par(doc, f"El REM se mantiene en REMUS (`RSI.rem`, versión {VERSION}) a partir de `scripts/remus/rsi_data.json`; REMUS ordena su documento con su propio índice y este sigue el del Lab 5. Cada requisito lleva un código que se repite en el UML, en las capturas y en la trazabilidad. Los objetivos de negocio están en el apartado 1.5.")
    doc.add_heading("2.1 Requisitos de información", 2)
    B.tabla(doc, ["Código", "Concepto", "Datos"], [[r["id"], r["name"], "; ".join(r["data"])] for r in D["information"]], [2, 3.5, 11.5], tam=8.5)
    doc.add_heading("2.2 Requisitos funcionales (y de interfaz) de grupos y herramientas", 2)
    B.tabla(doc, ["Código", "Nombre", "El sistema deberá", "Entrega"], [[r["id"], r["name"], r["description"], r["comments"]] for r in D["ui"] + D["functional"]], [1.8, 3.4, 9.2, 2.6], tam=8.5)
    doc.add_heading("2.3 Reglas de negocio", 2)
    B.tabla(doc, ["Código", "Nombre", "Regla"], [[r["id"], r["name"], r["description"]] for r in D["rules"]], [2, 3.5, 11.5], tam=9)
    doc.add_heading("2.4 Actores", 2)
    B.tabla(doc, ["Código", "Actor", "Representa a"], [[a["id"], a["name"], a["role"]] for a in D["actors"]], [2, 4, 11], tam=9)
    doc.add_heading("2.5 Requisitos no funcionales", 2)
    B.tabla(doc, ["Código", "Nombre", "El sistema deberá"], [[r["id"], r["name"], r["description"]] for r in D["nonfunctional"]], [2, 3.5, 11.5], tam=9)
    doc.add_heading("2.6 Restricciones del entorno", 2)
    B.tabla(doc, ["Código", "Nombre", "Descripción"], [[r["id"], r["name"], r["description"]] for r in D["environment"]], [2, 4, 11], tam=9)
    doc.add_heading("2.7 Casos de uso", 2)
    actores = {a["id"]: a["name"] for a in D["actors"]}
    for u in D["usecases"]:
        pasos = " ".join(f"{i}. {(actores[s['actor']] if s['who'] == 'actor' else 'El sistema')} {s['text']}." for i, s in enumerate(u["steps"], 1))
        B.par(doc, f"**{u['id']} {u['name']}.** Cuándo: {u['trigger']}. Precondición: {u['pre']}. {pasos} Postcondición: {u['post']}.")

    doc.add_heading("3. Glosario de términos", 1)
    B.tabla(doc, ["Término", "Significado"], [[g["name"], g["text"]] for g in D["paragraphs"]["glossary"]], [4, 13], tam=9)

    doc.add_heading("4. Análisis (UML)", 1)
    B.par(doc, "El UML de análisis recoge los conceptos del Lab 5: rol, grupo y subgrupos, herramienta y permiso. Las etiquetas en rojo son los códigos de requisito.")
    B.figura(doc, os.path.join(IMG, "uml-rsi-analisis.png"), "UML de análisis de la red social interna con etiquetas de trazabilidad.", 17)

    doc.add_heading("5. Diseño (UML)", 1)
    B.par(doc, "En el diseño cada concepto del análisis pasa a un elemento de Microsoft Teams: los grupos son equipos, los subgrupos son canales privados, los roles son los de Teams y las herramientas son pestañas o aplicaciones de cada canal. Se usan tres equipos y no uno porque cada grupo tiene miembros, permisos y herramientas distintos, y así los canales privados de las 27 delegaciones quedan en un solo equipo.")
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
        filas_t.append([u["id"], ", ".join(req), ", ".join(c.split("-")[0] for c in caps) or "—", "Con capturas de apoyo (sección 6)" if ok else "Sin captura todavía"])
    B.tabla(doc, ["Caso de uso", "Requisitos", "Capturas", "Estado"], filas_t, [2, 7, 2.5, 5.5], tam=8.5, titulo="Casos de uso, requisitos y capturas")
    B.par(doc, "Las capturas apoyan algunos pasos de cada caso de uso, no todos: no muestran, por ejemplo, la baja de una delegación (CU-R05) ni una respuesta enviada al formulario. La prueba completa de cada caso la hace otra persona y se anota en `docs/redsocial/pruebas.md`.")
    n_trazas = sum(len(t[1]) for t in D["traces"])
    B.par(doc, f"Los objetivos, los requisitos de información y las reglas están enlazados con los requisitos y los casos de uso en las trazas de `RSI.rem` ({n_trazas} trazas declaradas; REMUS añade las inversas).")

    doc.add_heading("8. Seguimiento SCRUM", 1)
    B.par(doc, "La red social tiene su propio seguimiento, independiente del CMS y del DMS. Equipo de cuatro personas desde el 16/11/2026 (Sprint 1 de la red social: 16/11 – 22/11). Entrega del 22/11: estructura de Teams y Planner; entrega del 29/11: Power Automate y PowerApps; entrega final: 07/12/2026.")
    B.tabla(doc, ["ID", "Tarea", "Quién", f"Estado a {FECHA}"], [[i, t, q, ESTADO.get(i, "—")] for i, t, q in tareas_plan()], [1.3, 8.2, 3.2, 4.3], tam=8.5, titulo="Backlog de la entrega del 22/11")
    carpeta = os.path.join(RSI, "scrum")
    bl = os.path.join(carpeta, "product-backlog-rsi.md")
    if os.path.exists(bl):
        filas_bl = []
        for l in open(bl, encoding="utf-8").read().splitlines():
            m = re.match(r"^\| (RSI-HU-\d+) \| (.*?) \| (.*?) \| (\d+) \| (.*?) \| (.*?) \| (.*?) \|$", l)
            if m:
                filas_bl.append([m.group(1), m.group(2), m.group(4), m.group(5).replace("**", ""), m.group(7)])
        B.par(doc, "Los puntos de historia se estimaron el 22/11/2026 al cerrar el sprint, **a posteriori**: el sprint no se planificó con puntos el 16/11. Sirven para el burndown y para repartir el siguiente.")
        B.tabla(doc, ["ID", "Historia", "SP", f"Estado a {FECHA}", "Responsable"], filas_bl, [1.9, 6.4, 0.9, 5.5, 2.3], tam=8, titulo="Product backlog de la red social")
    png = os.path.join(carpeta, "burndown-sprint-01-rsi.png")
    if os.path.exists(png):
        B.figura(doc, png, "Burndown del Sprint 1 de la red social: línea ideal y puntos pendientes reales.", 14)
        B.par(doc, "El burndown cuenta como hecha una historia cuando está integrada en `main`: 22 SP hasta el 19/11, 16 desde el 20/11 (RSI-HU-01 y RSI-HU-03) 3 durante el 22/11 y 0 con el commit de cierre de ese día, que integra RSI-HU-06 (el documento y el zip); el zip se envía esa noche. La Sprint Review y la retrospectiva están en `scrum/review-sprint-01-rsi.md`, escritas a partir de los datos del sprint y no de una reunión.")
    else:
        AVISOS.append("falta docs/redsocial/scrum/burndown-sprint-01-rsi.png (python scripts/redsocial/scrum_rsi.py)")

    doc.add_heading("9. Pendiente y limitaciones", 1)
    for t in ("El aislamiento (RN-R01 y RN-R02) se probó con dos cuentas distintas: Joaquín el 21/11 (captura 05; propietario del equipo pero miembro de un solo canal privado) y Álvaro el 22/11 como Miembro del equipo (capturas 05b y 05c). Falta probarlo con una delegación real, que aún no existe en Teams.",
              "Las pestañas de Planner de los tres equipos existen; solo el plan de la Asamblea tiene captura (08), así que el contenido de los otros dos no está documentado con imagen.",
              "Power Automate y PowerApps (RF-R11 y RF-R12) son de la entrega del 29/11. Álvaro comprobó que las páginas de creación cargan en el tenant, pero no que se pueda guardar y ejecutar un flujo o una aplicación (`docs/redsocial/powerapps-especificacion.md`).",
              "No hay contacto con el CADUS en el equipo desde el 16/11: las decisiones que dependen del CADUS son suposiciones del caso de negocio.",
              "No se ha comprobado el límite de canales del tenant (la documentación de Microsoft lo sitúa por encima de lo que necesita el piloto): se crearon tres canales privados.",
              "Los datos del piloto son de ejemplo; las cuentas de delegación reales no existen en Teams todavía, y las capturas son de las cuentas de Pablo, Joaquín, Marcos y Álvaro."):
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
