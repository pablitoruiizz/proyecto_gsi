"""Genera los UML de la Red Social Interna del CADUS (Lab 5, MS Teams) en docs/redsocial/img:
  uml-rsi-analisis.png   conceptos del Lab 5: <<Role>>, <<Group>>, <<Subgroups>>, <<Tool>> y <<Permission>>
  uml-rsi-diseno.png     el mismo diagrama transformado a conceptos de Microsoft Teams
Los códigos rojos son los del REM (scripts/remus/rsi_data.json). Uso: python scripts/redsocial/diagramas_rsi.py"""
import os
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "scripts", "entrega"))
import diagramas as D  # noqa: E402

D.IMG = os.path.join(RAIZ, "docs", "redsocial", "img")
os.makedirs(D.IMG, exist_ok=True)
lienzo, clase, rel, caja, guardar = D.lienzo, D.clase, D.rel, D.caja, D.guardar
AZUL, VERDE, NARANJA, ROJO = D.AZUL, D.VERDE, D.NARANJA, D.ROJO


def analisis():
    fig, ax = lienzo(1800, 965)
    ax.text(900, 24, "UML de análisis de la Red Social Interna del CADUS — etiquetas de trazabilidad en rojo", ha="center", fontsize=13, fontweight="bold", color=AZUL)
    rol = clase(ax, 40, 80, 480, "Rol", "<<Role>> · RF-R06 · ACT-R01 a ACT-R03 · RN-R04",
                ["nombre (Ejecutiva | Delegación | Administrador)", "cuenta (CADUS | delegación | equipo)"])
    grupo = clase(ax, 720, 80, 450, "Grupo", "<<Group>> · IR-R01 · RF-R01 · RF-R02 · RF-R04 · OBJ-R01",
                  ["nombre (Ejecutiva | Delegaciones | Asamblea)", "privado (sí)", "propietarios y miembros"], VERDE)
    sub = clase(ax, 1400, 80, 380, "Subgrupo", "<<Subgroups>> · IR-R01 · IR-R02 · RF-R03 · RN-R02 · CU-R05",
                ["nombre (la delegación de un centro)", "privado (sí)", "27 en el grupo Delegaciones"], VERDE)
    perm = clase(ax, 40, 430, 480, "Permiso", "<<Permission>> · IR-R04 · RF-R06 · RN-R01 · RN-R02 · RN-R05",
                 ["acción (leer | publicar | gestionar canales |", "   administrar miembros)", "sobre un grupo o un subgrupo"], NARANJA)
    herr = clase(ax, 720, 430, 450, "Herramienta", "<<Tool>> · IR-R03 · RF-R07 a RF-R12 · OBJ-R02 · OBJ-R03",
                 ["nombre (Archivos | Calendario | Planner |", "   Forms | Flujo | Aplicación)", "uso y quién la gestiona"], ROJO)
    doc = clase(ax, 1400, 430, 380, "DocumentoDMS", "<<Document>> externo · RF-R07 · RN-R03 · OBJ-R04",
                ["vive en el DMS (SharePoint)", "la red social solo lo enlaza"])
    plan = clase(ax, 1400, 740, 380, "Plan", "<<Plan>> · RF-R09 · RF-R13 · IR-R05 · OBJ-R02",
                 ["equipo · patrón (ciclo de vida | proceso)", "cubos: estados o etapas en orden"], ROJO)
    tarea = clase(ax, 720, 740, 450, "Tarea", "IR-R05 · RF-R09 · CU-R02 · OBJ-R02",
                  ["plan, cubo, responsable", "fechaLimite, estado"])
    rel(ax, rol, "der", grupo, "izq", "es miembro de", "*", "*", dy=-12)
    rel(ax, grupo, "der", sub, "izq", "se divide en", "1", "*", dy=-12)
    rel(ax, perm, "arr", rol, "abj", "se concede a", "*", "1", dx=40, dy=0)
    rel(ax, perm, "der", herr, "izq", "se aplica a", "*", "*", dy=-12)
    rel(ax, grupo, "abj", herr, "arr", "usa", "1", "*", dx=36, dy=0)
    rel(ax, herr, "der", doc, "izq", "enlaza", "*", "*", dy=-12)
    rel(ax, herr, "abj", tarea, "arr", "Planner reparte", "1", "*", dx=44, dy=0)
    rel(ax, plan, "izq", tarea, "der", "contiene", "1", "*", dy=-12)
    pie = ["Casos de uso sobre este modelo: CU-R01 publicar un aviso (Rol, Permiso, Grupo) · CU-R02 preparar una asamblea (Plan, Tarea) · CU-R03 compartir un documento (Herramienta, DocumentoDMS, Subgrupo)",
           "CU-R04 consultar avisos, calendario y tareas (Rol, Grupo, Herramienta) · CU-R05 alta o baja de una delegación (Subgrupo, Permiso). Reglas y casos de uso completos: REM (RSI.rem).",
           "Una delegación es un subgrupo (canal privado) del grupo Delegaciones; la Ejecutiva es propietaria de los tres grupos."]
    for k, t in enumerate(pie):
        ax.text(40, 895 + 20 * k, t, fontsize=8.6, color="#333")
    guardar(fig, "uml-rsi-analisis.png")


def plan_caja(ax, x, w, titulo, linea1, linea2, y=842, h=80):
    """Caja de un plan de Planner con dos líneas de detalle (patrón y cubos)."""
    caja(ax, x, y, w, h, "", fc="#eef2fb", ec=AZUL)
    ax.text(x + w / 2, y + 20, titulo, ha="center", va="center", fontsize=9.5, fontweight="bold", zorder=3)
    ax.text(x + w / 2, y + 43, linea1, ha="center", va="center", fontsize=8, color="#333", fontstyle="italic", zorder=3)
    ax.text(x + w / 2, y + 62, linea2, ha="center", va="center", fontsize=8, color="#333", fontstyle="italic", zorder=3)


def diseno():
    fig, ax = lienzo(1700, 1420)
    ax.text(850, 24, "UML de diseño de la Red Social Interna en Microsoft Teams — del análisis al diseño", ha="center", fontsize=13, fontweight="bold", color=AZUL)
    caja(ax, 40, 60, 1620, 60, "<<Tenant>> Microsoft 365 de la Universidad de Sevilla (uses0)", "Teams, SharePoint, Planner, Forms, Power Automate y PowerApps · RC-R01 · RC-R02", fc=AZUL, ec=AZUL, subcolor="#ffd2cf", titcolor="white")
    eje = clase(ax, 40, 190, 520, "<<Team>> CADUS · Ejecutiva", "privado · RF-R01 · RF-R02 · OBJ-R01",
                ["canal General: coordinación de la Ejecutiva", "canal «Preparación de avisos»", "Propietarios: la Ejecutiva (cuenta del CADUS)", "Miembros: nadie más"])
    dele = clase(ax, 590, 190, 540, "<<Team>> CADUS · Delegaciones", "privado · RF-R01 · RF-R03 · RF-R05 · RN-R01 · RN-R02",
                 ["General → «Avisos»: solo publican los propietarios", "27 canales privados «Delegación · <centro>»", "   (piloto: ETSII, Derecho y Biología)", "Propietarios: la Ejecutiva", "Miembros: las 27 cuentas de delegación"], VERDE)
    asa = clase(ax, 1160, 190, 500, "<<Team>> CADUS · Asamblea", "privado · RF-R01 · RF-R04 · RF-R08 · RF-R09",
                ["canal General: convocatorias y seguimiento", "   pestañas Calendario y SharePoint (DMS)", "canal «Cursos»", "Propietarios: la Ejecutiva", "Miembros: las 27 cuentas de delegación"])
    ax.text(40, 440, "Roles y permisos de Teams (IR-R04 · RF-R06 · RN-R04 · RN-R05)", fontsize=11.5, fontweight="bold", color=AZUL)
    caja(ax, 40, 465, 520, 66, "<<Role>> Propietario (Owner)", "Ejecutiva y administrador: gestionan miembros y canales", fc="white", ec=AZUL, subcolor="#333")
    caja(ax, 590, 465, 540, 66, "<<Role>> Miembro (Member)", "una cuenta por delegación: lee y participa en su canal", fc="white", ec=VERDE, subcolor="#333")
    caja(ax, 1160, 465, 500, 66, "<<Role>> Invitado (Guest)", "solo el equipo del proyecto en pruebas; nunca estudiantes", fc="white", ec=NARANJA, subcolor="#333")
    caja(ax, 40, 575, 780, 70, "<<Permission>> Quién publica", "avisos: solo propietarios · canales de delegación: la delegación y la Ejecutiva · RN-R01", fc="#fff7ea", ec=NARANJA, subcolor="#333")
    caja(ax, 880, 575, 780, 70, "<<Permission>> Quién ve el canal", "canal privado: solo sus miembros; el resto del equipo no lo ve ni lo busca · RN-R02", fc="#fff7ea", ec=NARANJA, subcolor="#333")
    ax.text(40, 695, "Herramientas ancladas como pestañas de cada canal (IR-R03 · RF-R07 a RF-R12 · UI-R02)", fontsize=11.5, fontweight="bold", color=AZUL)
    herr = [("<<Tool>> SharePoint", "pestaña que abre el DMS · RN-R03", 40),
            ("<<Tool>> Calendario", "asambleas y cursos · RF-R08", 340),
            ("<<Tool>> Planner", "tareas por equipo · RF-R09", 640),
            ("<<Tool>> Forms", "asistencia y encuestas · RF-R10", 940),
            ("<<Tool>> PowerApps y flujos", "RF-R12 en vista previa · RF-R11 ejecutado", 1240)]
    for t, s, x in herr:
        caja(ax, x, 720, 280 if x < 1240 else 420, 66, t, s, fc="#eef7ee", ec=VERDE, subcolor="#333")
    ax.text(40, 800, "PowerApps (R-13): lista «Delegaciones CADUS» y app «Estado de las delegaciones», ejecutada en vista previa el 25/11. Power Automate (R-12): dos flujos que avisan en Asamblea (capturas 12a a 12d).", fontsize=9, color="#333")
    ax.text(40, 832, "Planes de Planner (IR-R05 · RF-R09 · CU-R02) — pestaña Planner de cada equipo", fontsize=11.5, fontweight="bold", color=AZUL)
    plan_caja(ax, 40, 440, "<<Plan>> «Coordinación de la Ejecutiva»", "equipo Ejecutiva · patrón Ciclo de vida de tareas", "cubos: Por hacer · En curso · Hecho")
    plan_caja(ax, 500, 460, "<<Plan>> «Seguimiento de las delegaciones»", "equipo Delegaciones · patrón Ciclo de vida de tareas", "cubos: Por hacer · En curso · Hecho")
    plan_caja(ax, 980, 680, "<<Plan>> «Preparación de la asamblea»", "equipo Asamblea · patrón Proceso de tareas (RSI-HU-09)", "cubos: 1 Convocatoria · 2 Preparación · 3 Día de la asamblea · 4 Después (acta)")
    caja(ax, 40, 934, 1620, 58, "<<Task>> Tarea del plan (IR-R05)", "título · cubo · responsable (persona) · fecha límite · estado · la Ejecutiva reparte, la delegación actualiza · datos de ejemplo", fc="#eef2fb", ec=AZUL, subcolor="#333")
    ax.text(40, 1012, "Diseño de Joaquín (R-06 y RSI-HU-09, Lab 6): un plan por equipo. La Asamblea sigue Proceso de tareas (etapas en orden); los otros dos, Ciclo de vida. Planner no tiene permisos por tarea.", fontsize=9.5, color="#333")
    ax.text(40, 1050, "Del análisis al diseño", fontsize=11.5, fontweight="bold", color=AZUL)
    filas = [("<<Group>> Grupo", "→", "<<Team>> equipo privado de Teams (tres: Ejecutiva, Delegaciones y Asamblea)"),
             ("<<Subgroups>> Subgrupo", "→", "canal privado del equipo Delegaciones, uno por centro (27; el piloto crea tres)"),
             ("<<Role>> Rol", "→", "rol de Teams: propietario, miembro o invitado (cuentas de grupo, no personales)"),
             ("<<Permission>> Permiso", "→", "ajuste del canal: quién publica y quién ve; permisos de miembros y propietarios"),
             ("<<Tool>> Herramienta", "→", "pestaña o aplicación del canal (SharePoint, Calendario, Planner, Forms, Power Automate, PowerApps)"),
             ("Tarea", "→", "tarea de Planner dentro de un cubo del plan del equipo"),
             ("DocumentoDMS", "→", "no se copia: es un enlace al sitio de SharePoint del DMS")]
    for i, (a, f, b) in enumerate(filas):
        ax.text(60, 1083 + 30 * i, f"{a}   {f}   {b}", fontsize=10)
    ax.text(40, 1307, "Por qué tres equipos y no uno: cada grupo tiene miembros, permisos y herramientas distintos, y los canales privados de las 27 delegaciones quedan en un solo equipo.", fontsize=9.5, color="#333")
    ax.text(40, 1332, "Cada delegación usa una sola cuenta a nombre de la delegación (RN-R04), como en el portal y en el DMS.", fontsize=9.5, color="#333")
    ax.text(40, 1362, "Relaciones: Tenant 1—* Equipo · Equipo 1—* Canal (los canales privados son los subgrupos) · Equipo *—* Rol (propietario o miembro) · Canal 1—* Pestaña (herramienta)", fontsize=9.5, color="#333")
    ax.text(40, 1387, "Permiso: «quién publica» y «quién ve» se aplican a un Canal; Plan de Planner 1—1 Equipo, con muchas Tareas · Pestaña Archivos → sitio de SharePoint del DMS (enlace, sin copia).", fontsize=9.5, color="#333")
    guardar(fig, "uml-rsi-diseno.png")


if __name__ == "__main__":
    analisis()
    diseno()
