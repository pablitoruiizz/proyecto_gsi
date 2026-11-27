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
FECHA_ENTREGA = "29/11/2026"
FECHA = "26/11/2026"  # fecha del estado que se describe; actualizar al regenerar
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
    "08-planner.jpg": ("Plan de la asamblea rehecho como proceso de tareas.", "Plan «Preparación de la Asamblea» en el equipo CADUS · Asamblea, rehecho el 25/11/2026 con el patrón «Proceso de tareas»: cuatro cubos numerados que son las etapas (1 · Convocatoria, 2 · Preparación, 3 · Día de la asamblea y 4 · Después del acta) y seis tareas de ejemplo con responsable y fecha. La captura es de la cuenta de Joaquín. Antes de este cambio el plan usaba los cubos Por hacer, En curso y Hecho (ciclo de vida de tareas).", "RF-R09 · RF-R13 · CU-R02"),
    "09-forms.jpg": ("Formulario de confirmación de asistencia.", "Formulario de Forms «Confirmación de asistencia», anclado como pestaña del canal General de CADUS · Asamblea, con dos preguntas: si asistirá la delegación y de qué delegación se trata. La captura es de la cuenta de Joaquín.", "RF-R10"),
    "R09-01a-panel-cubos-1-a-3.jpg": ("Prueba del plan rehecho: cubos 1 a 3.", "Marcos abre el plan con su cuenta el 26/11/2026 y ve los cubos 1 · Convocatoria (2 tareas), 2 · Preparación (2) y 3 · Día de la asamblea (1), en orden.", "RF-R13 · RNF-R02"),
    "R09-01b-panel-cubo-4.jpg": ("Prueba del plan rehecho: cubo 4.", "El cuarto cubo, 4 · Después (acta), con la tarea de subir el acta aprobada al DMS.", "RF-R13"),
    "R09-02b-tarea-completada.jpg": ("Una tarea completada se queda en su etapa.", "Marcos pasa «Reservar la sala (ejemplo)» a completada: la tarjeta sale tachada y sigue en 2 · Preparación, en «Tareas completadas». Al terminar se devolvió a «En curso».", "RF-R13 · RF-R09"),
    "R09-02d-graficos-despues.jpg": ("Gráficos de Planner tras completar la tarea.", "En la vista Gráficos, las tareas restantes pasan de 6 a 5 y aparece «Completado»: el avance se ve en la vista, no en una columna «Hecho».", "RF-R13 · RF-R09"),
    "R09-03-calendario.jpg": ("Vista de programación del plan.", "En la vista Calendario cada tarea sale en su fecha: las de las etapas 1 y 2 entre el 21 y el 25/11, la de la etapa 3 el 26/11 y la de la etapa 4 el 28/11, después de la asamblea.", "RF-R13 · RNF-R02"),
    "12a-power-automate-flujo-tarea.jpg": ("Flujo «Aviso de tarea nueva».", "Flujo de Power Automate creado por Joaquín el 25/11/2026 desde una plantilla del tenant: cuando se crea una tarea en el plan «Preparación de la Asamblea», publica un mensaje en el canal General del equipo.", "RF-R11 · RC-R02"),
    "12b-power-automate-aviso-tarea.jpg": ("Aviso de tarea nueva en el canal.", "El mensaje que publica el flujo en el canal General de CADUS · Asamblea, con el título de la tarea, su fecha límite y quién la creó.", "RF-R11"),
    "12c-power-automate-flujo-vencimiento.jpg": ("Flujo «Aviso de tareas que vencen».", "Segundo flujo, programado cada día porque Planner no tiene un disparador «vence la fecha»: lista las tareas sin completar que vencen hoy o mañana.", "RF-R11 · RC-R02"),
    "12d-power-automate-aviso-vencimiento.jpg": ("Aviso de tareas que vencen en el canal.", "El mensaje del segundo flujo en el canal General, con una tabla de las tareas pendientes y su fecha.", "RF-R11"),
    "12e-r12c-tarea-creada.jpg": ("Prueba de Marcos: tarea creada.", "Marcos crea con su cuenta la tarea «Prueba de Marcos del flujo (ejemplo)» con responsable y fecha límite el 26/11/2026 (25/11, 22:34).", "RF-R11"),
    "12f-r12c-aviso-en-general.jpg": ("Prueba de Marcos: aviso recibido.", "Cinco minutos después (22:39) sale en General el aviso con el título y la fecha de esa tarea.", "RF-R11"),
    "12i-r12c-tabla-con-tarea.jpg": ("Prueba de Marcos: tabla de vencimientos con la tarea.", "Ejecutado a mano el segundo flujo, el mensaje «Tareas que vencen hoy o mañana» incluye la tarea de prueba.", "RF-R11"),
    "12j-r12c-tabla-sin-tarea.jpg": ("Prueba de Marcos: tabla tras completar la tarea.", "Con la tarea completada, el mensaje nuevo lista solo las otras cinco tareas pendientes.", "RF-R11"),
    "12l-r12c-copropietarios-flujo2.jpg": ("Flujo compartido con Marcos.", "En la página del segundo flujo figuran como propietarios Joaquín y Marcos. Los flujos usan las conexiones de la cuenta que los creó: si esa cuenta se desactiva dejan de ejecutarse, y al traspasar la red social hay que reconstruirlos con la cuenta de la Ejecutiva.", "RF-R11 · RC-R02"),
    "R13-01-lista-delegaciones-sharepoint.jpg": ("Lista de SharePoint «Delegaciones CADUS».", "Lista con las columnas Título, Centro y Estado y tres delegaciones de ejemplo (ETSII, Derecho y Biología), sin datos personales.", "RF-R12 · RNF-R01"),
    "R13-02-app-guardada-power-apps-studio.jpg": ("Aplicación «Estado de las delegaciones» guardada.", "Aplicación de lienzo generada desde la lista en Power Apps Studio con la cuenta de Álvaro y guardada el 25/11/2026.", "RF-R12 · RC-R02"),
    "R13-03-app-ejecutada-vista-previa.jpg": ("Aplicación en ejecución (vista previa).", "La aplicación lee la lista y muestra las tres delegaciones con su centro y su estado.", "RF-R12"),
    "R13-06-app-ejecutada-marcos.jpg": ("Aplicación abierta por Marcos.", "Marcos abre la aplicación compartida con su cuenta, fuera de Power Apps Studio (apps.powerapps.com): lee la lista y muestra las tres delegaciones.", "RF-R12"),
    "R13-07-detalle-derecho-marcos.jpg": ("Ficha de una delegación en la aplicación.", "Al elegir una delegación, la aplicación muestra su ficha con título, centro y estado.", "RF-R12"),
}
CAPS.update({
    "08c-planner-ejecutiva.jpg": ("Plan «Coordinación de la Ejecutiva».", "Plan del equipo CADUS · Ejecutiva con el patrón «Ciclo de vida de tareas»: tres cubos (Por hacer, En curso y Hecho) y tres tareas de ejemplo con responsable y fecha, una de ellas completada. Captura del 27/11/2026 con la cuenta de Pablo, propietario del equipo.", "RF-R09 · RF-R02"),
    "08d-planner-delegaciones.jpg": ("Plan «Seguimiento de las delegaciones».", "Plan del equipo CADUS · Delegaciones con el patrón «Ciclo de vida de tareas»: dos tareas por hacer, una en curso y una completada («Leer el aviso de la convocatoria»), tres de ellas de «Confirmar la asistencia» de una delegación de ejemplo (ETSII, Derecho y Biología). Captura del 27/11/2026 con la cuenta de Pablo.", "RF-R09 · RF-R03"),
    "12m-power-automate-ejecucion-programada-27-11.jpg": ("Ejecución programada del segundo flujo (27/11, 08:00).", "En el canal General de CADUS · Asamblea aparece el mensaje «Tareas que vencen hoy o mañana…» publicado por el flujo a las 8:00 del 27/11/2026, con la tabla de tareas pendientes. Es la hora programada; las ejecuciones manuales de prueba fueron el 25/11 por la noche. Captura del 27/11/2026 con la cuenta de Pablo.", "RF-R11"),
    "12n-power-automate-ejecucion-programada-26-11.jpg": ("Ejecución programada del segundo flujo (26/11, 08:00).", "El mismo mensaje de la víspera, publicado a las 8:00 del 26/11/2026: el flujo programado se ejecutó solo dos mañanas seguidas. Captura del 27/11/2026 con la cuenta de Pablo.", "RF-R11"),
})
CAP_GRUPOS = [  # (título de la sección, introducción, capturas)
    ("6.1 Estructura de Teams", "Los tres equipos, sus canales, roles, moderación y pestañas.",
     ["01-equipos.jpg", "02-ejecutiva-miembros.jpg", "10-ejecutiva-canales.jpg", "03-delegaciones-avisos.jpg", "11-delegaciones-avisos-renombrado.jpg", "04-delegaciones-canales-privados.jpg", "05-vista-miembro.jpg", "05b-avisos-solo-miembro.jpg", "05c-canales-solo-miembro.jpg", "06-asamblea-calendario.jpg", "07-archivos-dms.jpg", "07b-archivos-dms-marcos.jpg", "09-forms.jpg"]),
    ("6.2 Los planes de Planner y el patrón del Lab 6", "Capturas del plan de la asamblea rehecho como proceso de tareas y de la prueba de otra persona (Marcos, 26/11/2026), y de los planes de la Ejecutiva y de las delegaciones (27/11/2026, cuenta de Pablo, sin prueba de otra persona). El patrón y su justificación están en la sección 5.1.",
     ["08-planner.jpg", "R09-01a-panel-cubos-1-a-3.jpg", "R09-01b-panel-cubo-4.jpg", "R09-02b-tarea-completada.jpg", "R09-02d-graficos-despues.jpg", "R09-03-calendario.jpg", "08c-planner-ejecutiva.jpg", "08d-planner-delegaciones.jpg"]),
    ("6.3 Power Automate: avisos automáticos (Lab 8, RF-R11)", "Dos flujos creados por Joaquín en el tenant de la US y probados por Marcos con su cuenta (25/11/2026); la ejecución programada del segundo se observó el 26 y el 27/11/2026.",
     ["12a-power-automate-flujo-tarea.jpg", "12b-power-automate-aviso-tarea.jpg", "12c-power-automate-flujo-vencimiento.jpg", "12d-power-automate-aviso-vencimiento.jpg", "12e-r12c-tarea-creada.jpg", "12f-r12c-aviso-en-general.jpg", "12i-r12c-tabla-con-tarea.jpg", "12j-r12c-tabla-sin-tarea.jpg", "12l-r12c-copropietarios-flujo2.jpg", "12n-power-automate-ejecucion-programada-26-11.jpg", "12m-power-automate-ejecucion-programada-27-11.jpg"]),
    ("6.4 PowerApps: estado de las delegaciones (Lab 8, RF-R12)", "Aplicación de prueba con datos de ejemplo, en el espacio personal de Álvaro; Álvaro dice que ya está publicada (27/11, de palabra, sin captura). Lo que no se comprobó está en la sección 10.",
     ["R13-01-lista-delegaciones-sharepoint.jpg", "R13-02-app-guardada-power-apps-studio.jpg", "R13-03-app-ejecutada-vista-previa.jpg", "R13-06-app-ejecutada-marcos.jpg", "R13-07-detalle-derecho-marcos.jpg"]),
]
# capturas que necesita cada caso de uso para considerarse observado
CAP_CU = {"CU-R01": ["03-delegaciones-avisos.jpg", "11-delegaciones-avisos-renombrado.jpg", "05b-avisos-solo-miembro.jpg"], "CU-R02": ["06-asamblea-calendario.jpg", "08-planner.jpg", "12b-power-automate-aviso-tarea.jpg"],
          "CU-R03": ["07-archivos-dms.jpg", "04-delegaciones-canales-privados.jpg"], "CU-R04": ["05-vista-miembro.jpg", "05c-canales-solo-miembro.jpg"],
          "CU-R05": ["04-delegaciones-canales-privados.jpg"]}
# estado de las tareas del plan a la fecha del documento (actualizar al regenerar)
ESTADO = {"R-01": "Hecho con el índice del Lab 5; revisado por Álvaro el 26/11", "R-02": "Hecho: REM en REMUS (versión 1.1, con el patrón de los tableros, RF-R13)",
          "R-03": "Hecho y revisado por Álvaro (UML en main)", "R-04": "Hecho y revisado por Álvaro (UML de diseño con los planes de Planner)",
          "R-05": "Hecho: tres equipos, cuatro propietarios, Avisos con moderación, canal Cursos, tres canales privados y calendario (capturas 01 a 06, 10 y 11)",
          "R-06": "Hecho: pestañas de Planner de los tres equipos (Coordinación de la Ejecutiva, Seguimiento de las delegaciones y Preparación de la Asamblea), Forms y pestaña del DMS; solo el plan de la Asamblea tiene captura (08), rehecho el 25/11",
          "R-07": "Hecho: 14 capturas (01 a 11, 05b, 05c y 07b); la prueba con una cuenta solo miembro se hizo el 22/11 (capturas 05b y 05c)",
          "R-08": "Hecho el 22/11 por Pablo con Claude (puntos estimados a posteriori)", "R-09": "Hecho el 22/11 con el commit de cierre", "R-10": "Revisión con Codex hecha el 22/11 y corregida; prueba cruzada humana parcial (Joaquín y Álvaro probaron el aislamiento de canales; Álvaro revisó los UML)"}


def existe(nombre):
    return os.path.exists(os.path.join(CAP, nombre))


def md_en_doc(doc, ruta, prefijo="", omitir_titulo=True, desde=None, hasta=None, bajar=0):
    """Pinta un .md (títulos, párrafos, tablas y listas) dentro de un documento ya abierto; los títulos ## pasan a nivel 2 (más `bajar`).
    `desde` y `hasta` son los títulos (línea exacta) que abren y cierran el tramo que se pinta."""
    lineas = [re.sub(r"\[([^\]]+)\]\([^)]*\)", lambda m: m.group(1), l) for l in open(ruta, encoding="utf-8-sig").read().splitlines()]  # enlaces: solo el texto
    if desde is not None:
        lineas = lineas[[l.rstrip() for l in lineas].index(desde):]
    if hasta is not None and hasta in [l.rstrip() for l in lineas]:
        lineas = lineas[:[l.rstrip() for l in lineas].index(hasta)]
    i = 0
    while i < len(lineas):
        l = lineas[i].rstrip()
        if not l.strip():
            pass
        elif l.startswith("# "):
            if not omitir_titulo:
                doc.add_heading(l[2:].strip(), 1)
        elif l.startswith("### "):
            doc.add_heading(l[4:].strip(), 3 + bajar)
        elif l.startswith("## "):
            doc.add_heading(l[3:].strip(), 2 + bajar)
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
    doc.add_heading("Red Social Interna del CADUS — Entrega final (versión 2) en Microsoft Teams", 0)
    B.par(doc, "Gestión de Sistemas de Información (GSI) · Universidad de Sevilla · Lab 5 (Red Social Interna, MS Teams), Lab 6 (patrones de diseño de Planner) y Lab 8 (Power Automate y PowerApps)", cursiva=True)
    B.par(doc, "Equipo: Pablo Ruiz Vidal (Product Owner), Joaquín Luna Canela (Scrum Master), Álvaro Martínez Ocaña y Marcos-Paban Delgado Rodríguez. Cliente: CADUS.")
    B.par(doc, f"REM de la red social versión {VERSION} · estado a {FECHA} · fecha de entrega: {FECHA_ENTREGA}")

    doc.add_heading("Resumen", 1)
    B.par(doc, "La red social interna reúne la comunicación, las tareas, el calendario y los archivos de la Ejecutiva, las delegaciones de centro y las asambleas del CADUS en **Microsoft Teams**, dentro de la cuenta de la Universidad de Sevilla. Es independiente del portal (CMS) y del gestor documental (DMS), con los que se relaciona: los documentos oficiales siguen en el DMS y la red social los enlaza. Esta es la entrega final (versión 2): a la estructura de Teams y Planner de la entrega del 22/11 se suman el diseño de cada tablero de Planner con un patrón explícito (Lab 6) y las automatizaciones con Power Automate y PowerApps (Lab 8), con las pruebas de otra persona que constan en la sección 8.")
    n_cap = sum(1 for k in CAPS if existe(k))
    B.tabla(doc, ["Contenido pedido en el Lab 5", "Dónde está"], [
        ["Caso de negocio (Business Case), con el índice del Lab 5", "Sección 1 y documento aparte `Business-Case-RSI`"],
        ["Grupos principales y piloto", "Secciones 5 y 6: tres equipos privados creados en Teams, con canales, roles y herramientas"],
        ["Requisitos (REM): caso de negocio, requisitos del sistema software y glosario", "Sección 2 y proyecto REMUS `RSI.rem` (más la hoja `carga-remus.md`)"],
        ["Glosario de términos", "Sección 3 y glosario del REM"],
        ["Análisis: diagrama de clases con Role, Group, Subgroups, Tool y Permission", "Sección 4"],
        ["Diseño: el diagrama pasado a conceptos de Microsoft Teams", "Sección 5"],
        ["Implementación: capturas explicadas", f"Sección 6: {n_cap} capturas"],
        ["Patrones de diseño de los tableros de Planner (Lab 6)", "Secciones 5.1 y 6.2"],
        ["Power Automate y PowerApps (Lab 8)", "Secciones 6.3 y 6.4"],
        ["Pruebas hechas por otra persona", "Sección 8 y `docs/redsocial/pruebas.md`"],
        ["Seguimiento SCRUM (Sprints 1 y 2)", "Sección 9"]], [7, 10], tam=9)

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
        ["Herramienta", "Pestañas del canal: Archivos (enlace al DMS), Calendario, Planner, Forms; flujos de Power Automate que avisan en el canal y una aplicación de PowerApps con la lista de delegaciones"]], [5, 12], tam=9, titulo="Del análisis al diseño")

    doc.add_heading("5.1 Patrones de diseño de los tableros de Planner (Lab 6)", 2)
    B.par(doc, "Cada tablero de Planner sigue un patrón explícito, elegido con las cinco preguntas del Lab 6 (qué representan las tarjetas, a qué nivel, con qué criterio se agrupan, si los cubos están ordenados y si una tarjeta cambia de cubo). Los planes de la Ejecutiva y de las delegaciones son un «Ciclo de vida de tareas»; el de la asamblea, que sigue un proceso con etapas en orden, se rehízo el 25/11/2026 como «Proceso de tareas». El UML de diseño de arriba recoge el patrón de cada plan.")
    md_en_doc(doc, os.path.join(RSI, "diseno-tableros-planner.md"), bajar=1)

    doc.add_heading("6. Implementación en Teams", 1)
    B.par(doc, "Capturas del tenant de la Universidad de Sevilla, con datos de ejemplo. Cada una indica el requisito al que responde. Las que todavía no se han hecho aparecen como pendientes: no se muestra ninguna captura que no exista.")
    hechas = [k for k in CAPS if existe(k)]
    for titulo, intro, claves in CAP_GRUPOS:
        doc.add_heading(titulo, 2)
        B.par(doc, intro)
        for k in claves:
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

    doc.add_heading("8. Pruebas hechas por otra persona", 1)
    B.par(doc, "Regla de la definición de hecho de la red social: una historia no se cierra hasta que otra persona la ha probado y lo ha anotado. Las pruebas de la entrega del 22/11 (aislamiento de canales), la revisión del caso de negocio y las de la versión 2 (Power Automate, PowerApps y plan de la asamblea) están en `docs/redsocial/pruebas.md`; se reproducen aquí.")
    md_en_doc(doc, os.path.join(RSI, "pruebas.md"), desde="## Pruebas con otra cuenta", bajar=1)

    doc.add_heading("9. Seguimiento SCRUM", 1)
    B.par(doc, "La red social tiene su propio seguimiento, independiente del CMS y del DMS. Equipo de cuatro personas desde el 16/11/2026 (Sprint 1 de la red social: 16/11 – 22/11; Sprint 2: 23/11 – 29/11). Entrega del 22/11: estructura de Teams y Planner; entrega final del 29/11: patrones de Planner, Power Automate y PowerApps (versión 2), junto con la entrega final de los demás sistemas, que el 23/11 se adelantó desde el 07/12 al domingo 29/11.")
    doc.add_heading("9.1 Sprint 1 (16/11 – 22/11)", 2)
    B.tabla(doc, ["ID", "Tarea", "Quién", "Estado a 26/11/2026"], [[i, t, q, ESTADO.get(i, "—")] for i, t, q in tareas_plan()], [1.3, 8.2, 3.2, 4.3], tam=8.5, titulo="Backlog de la entrega del 22/11 (Sprint 1)")
    carpeta = os.path.join(RSI, "scrum")
    bl = os.path.join(carpeta, "product-backlog-rsi.md")
    if os.path.exists(bl):
        filas_bl = []
        for l in open(bl, encoding="utf-8").read().splitlines():
            m = re.match(r"^\| (RSI-HU-\d+) \| (.*?) \| (.*?) \| (\d+) \| (.*?) \| (.*?) \| (.*?) \|$", l)
            if m:
                filas_bl.append([m.group(1), m.group(2), m.group(4), m.group(5).replace("**", ""), m.group(7)])
        B.par(doc, "Los puntos de las historias del Sprint 1 se estimaron el 22/11/2026 al cerrar el sprint, **a posteriori**: no se planificó con puntos el 16/11. Los del Sprint 2 (RSI-HU-07, 08 y 09, 8 SP) sí se fijaron al empezar, el 23/11.")
        B.tabla(doc, ["ID", "Historia", "SP", f"Estado a {FECHA}", "Responsable"], filas_bl, [1.9, 6.4, 0.9, 5.5, 2.3], tam=8, titulo="Product backlog de la red social")
    png = os.path.join(carpeta, "burndown-sprint-01-rsi.png")
    if os.path.exists(png):
        B.figura(doc, png, "Burndown del Sprint 1 de la red social: línea ideal y puntos pendientes reales.", 14)
        B.par(doc, "El burndown cuenta como hecha una historia cuando está integrada en `main`: 22 SP hasta el 19/11, 16 desde el 20/11 (RSI-HU-01 y RSI-HU-03) 3 durante el 22/11 y 0 con el commit de cierre de ese día, que integra RSI-HU-06 (el documento y el zip); el zip se envía esa noche. La Sprint Review y la retrospectiva están en `scrum/review-sprint-01-rsi.md`, escritas a partir de los datos del sprint y no de una reunión.")
    else:
        AVISOS.append("falta docs/redsocial/scrum/burndown-sprint-01-rsi.png (python scripts/redsocial/scrum_rsi.py)")

    doc.add_heading("9.2 Sprint 2 (23/11 – 29/11)", 2)
    s2 = os.path.join(carpeta, "sprint-02-rsi.md")
    md_en_doc(doc, s2, desde="## Objetivo", hasta="## Heredado del Sprint 1", bajar=1)
    png2 = os.path.join(carpeta, "burndown-sprint-02-rsi.png")
    if os.path.exists(png2):
        B.figura(doc, png2, "Burndown del Sprint 2 de la red social: línea ideal y puntos pendientes reales.", 14)
        B.par(doc, "El burndown se actualizó cada día con `scripts/redsocial/scrum_rsi_sprint.py`. Una historia solo se cerró con su captura explicada y la prueba de otra persona: 8 SP pendientes hasta el 25/11 y 0 el 26/11, cuando las pruebas de Marcos y el UML de diseño de Álvaro entraron en `main`. La Sprint Review y la retrospectiva están en `scrum/sprint-02-rsi.md`, escritas a partir de los datos del sprint y no de una reunión.")
    else:
        AVISOS.append("falta docs/redsocial/scrum/burndown-sprint-02-rsi.png (python scripts/redsocial/scrum_rsi_sprint.py --regenerar)")
    md_en_doc(doc, s2, desde="## Sprint Review y retrospectiva (borrador del 26/11/2026)", bajar=1)

    doc.add_heading("10. Pendiente y limitaciones", 1)
    for t in ("El aislamiento (RN-R01 y RN-R02) se probó con dos cuentas distintas: Joaquín el 21/11 (captura 05; propietario del equipo pero miembro de un solo canal privado) y Álvaro el 22/11 como Miembro del equipo (capturas 05b y 05c). Falta probarlo con una delegación real, que aún no existe en Teams.",
              "Los planes de la Ejecutiva y de las delegaciones siguen el patrón «Ciclo de vida de tareas» en su diseño, y se capturaron el 27/11/2026 con la cuenta de Pablo (sección 6.2); a diferencia del plan de la asamblea, no los ha probado otra persona.",
              "En Planner, a la tarea de la etapa 3 le falta un espacio y la tilde («Pasar lista y abrir la sesion(ejemplo)») y ninguna tarea del plan figura como completada; son datos de ejemplo y no cambian el patrón.",
              "Power Automate (RF-R11): los dos flujos se ejecutan con las conexiones de la cuenta de Joaquín, propietario junto con Marcos; si esa cuenta se desactiva, dejan de ejecutarse y hay que reconstruirlos con la cuenta de la Ejecutiva. «Se asigna una tarea» solo se cumple si la asignación se hace al crearla: una tarea que se asigna después no genera aviso. Se probó crear una tarea, el aviso a los cinco minutos y la ejecución manual del flujo programado; la ejecución programada del segundo flujo se observó sola a las 08:00 del 26 y del 27/11 (capturas 12n y 12m).",
              "PowerApps (RF-R12): es una prueba con datos de ejemplo, en el espacio personal de Álvaro; Álvaro dice que ya está publicada (27/11, de palabra, sin captura ni comprobación de otra persona). Marcos la abrió con su cuenta y comprobó la lectura de la lista; no se probó crear, editar ni borrar delegaciones, ni abrirla desde la pestaña de Teams, y no restringe por rol (la propuesta original, CU-R05 y RN-R01, queda como mejora).",
              "Las historias de Teams del Sprint 1 solo tienen prueba de otra persona para el aislamiento de canales, y la retrospectiva de los dos sprints de la red social la redactó Pablo con Claude a partir de los datos, sin reunión del equipo.",
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
