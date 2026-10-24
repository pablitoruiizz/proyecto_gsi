"""Genera el documento Word de la entrega. Uso: python scripts/entrega/build_doc.py
Requiere: python-docx. Antes, ejecutar diagramas.py para crear las imágenes."""
import json
import os
import re

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENTREGA = os.path.join(RAIZ, "docs", "entrega")
IMG = os.path.join(ENTREGA, "img")
CAP = os.path.join(IMG, "capturas")
SALIDA = os.path.join(ENTREGA, "Entrega1-CMS-CADUS.docx")
FECHA_DATOS = "18/10/2026"

datos = json.load(open(os.path.join(RAIZ, "scripts", "remus", "cadus_data.json"), encoding="utf-8"))
plugins = {p["slug"]: p for p in json.load(open(os.path.join(ENTREGA, "datos", "plugins.json"), encoding="utf-8"))}
temas = {t["slug"]: t for t in json.load(open(os.path.join(ENTREGA, "datos", "themes.json"), encoding="utf-8"))}
AZUL = RGBColor(0x1F, 0x3A, 0x5F)
ROJO = RGBColor(0xB3, 0x26, 0x1E)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2)
sec.top_margin = sec.bottom_margin = Cm(2)

st = doc.styles["Normal"]
st.font.name = "Calibri"
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
st.font.size = Pt(10.5)
st.paragraph_format.space_after = Pt(6)
for nombre, tam in (("Heading 1", 18), ("Heading 2", 14), ("Heading 3", 12)):
    h = doc.styles[nombre]
    h.font.name = "Calibri"
    h.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    h.font.size = Pt(tam)
    h.font.bold = True
    h.font.color.rgb = AZUL
    h.paragraph_format.space_before = Pt(14 if nombre != "Heading 1" else 18)
    h.paragraph_format.space_after = Pt(6)
cap = doc.styles["Caption"]
cap.font.size = Pt(9)
cap.font.italic = True
cap.font.bold = False
cap.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

figura_n = [0]
tabla_n = [0]


# ------------------------------------------------------------------ utilidades
def campo(par, codigo, texto_previo=""):
    for tipo in ("begin", None, "separate", "texto", "end"):
        r = par.add_run()
        if tipo in ("begin", "separate", "end"):
            f = OxmlElement("w:fldChar")
            f.set(qn("w:fldCharType"), tipo)
            r._r.append(f)
        elif tipo is None:
            i = OxmlElement("w:instrText")
            i.set(qn("xml:space"), "preserve")
            i.text = codigo
            r._r.append(i)
        else:
            r.text = texto_previo


def sombrear(celda, color):
    tcPr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def par(texto="", negrita=False, cursiva=False, color=None, tam=None, alin=None, estilo=None, despues=None):
    p = doc.add_paragraph(style=estilo)
    if texto:
        r = p.add_run(texto)
        r.bold, r.italic = negrita, cursiva
        if color:
            r.font.color.rgb = color
        if tam:
            r.font.size = Pt(tam)
    if alin:
        p.alignment = alin
    if despues is not None:
        p.paragraph_format.space_after = Pt(despues)
    return p


def rico(texto, estilo=None):
    """Párrafo con **negrita** y `código` en línea."""
    p = doc.add_paragraph(style=estilo)
    for trozo in re.split(r"(\*\*.+?\*\*|`.+?`)", texto):
        if not trozo:
            continue
        if trozo.startswith("**"):
            p.add_run(trozo[2:-2]).bold = True
        elif trozo.startswith("`"):
            r = p.add_run(trozo[1:-1])
            r.font.name = "Consolas"
            r.font.size = Pt(9.5)
        else:
            p.add_run(trozo)
    return p


def vineta(texto):
    return rico(texto, "List Bullet")


def tabla(cabecera, filas, anchos, tam=8.5, titulo=None, resaltar=None):
    if titulo:
        tabla_n[0] += 1
        c = doc.add_paragraph(style="Caption")
        c.add_run(f"Tabla {tabla_n[0]}. {titulo}")
        c.paragraph_format.keep_with_next = True
    t = doc.add_table(rows=1, cols=len(cabecera))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, h in enumerate(cabecera):
        c = t.rows[0].cells[i]
        c.text = ""
        r = c.paragraphs[0].add_run(h)
        r.bold, r.font.size = True, Pt(tam)
        r.font.color.rgb = RGBColor(255, 255, 255)
        sombrear(c, "1F3A5F")
    trPr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trPr.append(th)
    for n, fila in enumerate(filas):
        cells = t.add_row().cells
        for i, v in enumerate(fila):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(str(v))
            r.font.size = Pt(tam)
            if resaltar and resaltar(fila):
                r.bold = True
            if n % 2 == 1:
                sombrear(cells[i], "F2F5F9")
    for row in t.rows:
        for i, w in enumerate(anchos):
            row.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return t


def figura(archivo, texto, ancho=16.5, carpeta=IMG):
    ruta = os.path.join(carpeta, archivo)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(ruta, width=Cm(ancho))
    figura_n[0] += 1
    c = doc.add_paragraph(style="Caption")
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.add_run(f"Figura {figura_n[0]}. {texto}")
    return figura_n[0]


def salto():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def millar(n):
    if not n:
        return "—"
    if n >= 1_000_000:
        return f"{n // 1_000_000} M+"
    return f"{n // 1000} k+"


def fecha(iso):
    a, m, d = iso.split("-")
    return f"{d}/{m}/{a}"


def estrellas(r):
    return f"{r / 20:.1f}/5".replace(".", ",")


def comparar(titulo, slugs, elegido, motivo, tema=False):
    fuente = temas if tema else plugins
    filas = []
    for s in slugs:
        p = fuente[s]
        nombre = re.sub(r"\s+[–—-]\s+.*$", "", p["nombre"]).strip()[:34]
        filas.append([nombre, p.get("version", ""), fecha(p["actualizado"]), millar(p.get("instal")), estrellas(p["rating"]), f'{p["votos"]:,}'.replace(",", "."),
                      "Seleccionado" if s == elegido else ""])
    tabla(["Plugin" if not tema else "Tema", "Versión", "Última actualización", "Instalaciones activas", "Valoración", "Nº valoraciones", "Decisión"], filas,
          [4.0, 1.7, 2.5, 2.4, 1.9, 2.0, 2.5], titulo=titulo, resaltar=lambda f: f[-1] == "Seleccionado")
    rico("**Justificación.** " + motivo)


def parsear_tablas(ruta):
    tablas, actual = [], None
    for linea in open(ruta, encoding="utf-8"):
        linea = linea.rstrip("\n")
        if linea.startswith("|"):
            celdas = [c.strip().strip("`") for c in linea.strip().strip("|").split("|")]
            if re.match(r"^:?-+:?$", celdas[0]):
                continue
            if actual is None:
                actual = []
                tablas.append(actual)
            actual.append(celdas)
        else:
            actual = None
    return tablas


# ------------------------------------------------------------------ portada
for _ in range(3):
    par()
par("Universidad de Sevilla · Gestión de Sistemas de Información (GSI)", color=RGBColor(0x55, 0x55, 0x55), alin=WD_ALIGN_PARAGRAPH.CENTER, tam=12)
par("Portal web del CADUS", negrita=True, color=AZUL, tam=30, alin=WD_ALIGN_PARAGRAPH.CENTER, despues=2)
par("Sistema 1 · CMS en WordPress", color=AZUL, tam=16, alin=WD_ALIGN_PARAGRAPH.CENTER)
par("Entrega 1 · Versión 1 · 18 de octubre de 2026", negrita=True, tam=13, alin=WD_ALIGN_PARAGRAPH.CENTER, despues=24)
tabla(["Integrante", "Rol SCRUM / Área"], [[s["name"], s["role"]] for s in datos["stakeholders"][1:]], [7.0, 10.0], tam=10, titulo="Equipo del proyecto")
par("Cliente: CADUS – Consejo de Alumnos de la Universidad de Sevilla · Pabellón de Uruguay, Av. de Chile, s/n, 41013 Sevilla · cadus@us.es", cursiva=True, tam=9.5, alin=WD_ALIGN_PARAGRAPH.CENTER)
salto()

par("Índice", negrita=True, color=AZUL, tam=18)
campo(par(), 'TOC \\o "1-2" \\h \\z \\u', "Haz clic derecho sobre el índice y elige «Actualizar campo» para generarlo.")
salto()

# ------------------------------------------------------------------ resumen
doc.add_heading("Resumen del estado de la entrega", 1)
par("Esta entrega recoge los apartados pedidos para la primera entrega del CMS (versión 1, 18 de octubre). Quedan fuera, por pertenecer a la entrega 2 (25 de octubre), la comparativa de temas, el portal final y el burndown final del segundo sprint. El detalle de cada apartado está en la sección indicada.")
n = lambda k: len(datos[k])
tabla(["Apartado solicitado", "Estado", "Sección"], [
    ["Propuesta de temática y empresa (versión definitiva)", "Completo", "1"],
    ["Comparativas: hosting WordPress, comunicación, gestión SCRUM, control de versiones", "Completo", "2.2"],
    ["Product backlog, sprint backlog y burndown chart", "Completo: sprint cerrado con 70 de 70 SP", "2.3 – 2.5"],
    [f"Requisitos (REM): {n('objectives')} objetivos, {n('information')} de información, {n('ui')} de interfaz, {n('functional')} funcionales, {n('nonfunctional')} no funcionales, {len(datos['rules'])} reglas de negocio", "Completo (fichero CADUS.rem)", "3"],
    ["Análisis: UML de la estructura web y mockups", "Completo", "4"],
    ["Diseño: UML de plugins, tabla comparativa de plugins (con los obligatorios) y mockups", "Completo", "4.3 · 5"],
    ["Implementación: capturas de WordPress", "Completa para el alcance del Sprint 1: portal con tema, roles, noticias, actas, directorio y buzón", "6"],
    ["Trazabilidad entre REM, análisis, diseño e implementación", "Completo", "7"],
], [9.5, 5.5, 2.0], titulo="Estado de cada apartado de la entrega")
par("Nota sobre el sprint: se han completado los 70 SP comprometidos, pero el trabajo de contenido se concentró en el último día (ver el burndown y la retrospectiva de la sección 2.5). Los contenidos del portal son de ejemplo y deben sustituirse por los reales validados con el cliente.", cursiva=True)

# ------------------------------------------------------------------ 1. propuesta
doc.add_heading("1. Propuesta de temática y empresa (versión definitiva)", 1)
tabla(["Campo", "Valor"], [
    ["Organización cliente", "CADUS – Consejo de Alumnos de la Universidad de Sevilla"],
    ["Sector", "Educación superior / representación estudiantil"],
    ["Persona de contacto", "Delegación General del CADUS (cadus@us.es)"],
    ["Ubicación", "Pabellón de Uruguay, Av. de Chile, s/n, 41013 Sevilla"],
    ["Sistema", "CMS en WordPress (Sistema 1 del proyecto en grupo)"],
], [4.5, 12.5], titulo="Datos del cliente")
rico(datos["paragraphs"]["intro"])
doc.add_heading("Objetivos del sistema", 2)
for o in datos["objectives"]:
    vineta(f"**{o['id']} · {o['name']}:** {o['description']}.")

# ------------------------------------------------------------------ 2. planificación
doc.add_heading("2. Planificación", 1)
doc.add_heading("2.1 Equipo y organización", 2)
par("El equipo lo forman cinco integrantes con roles SCRUM y áreas funcionales diferenciadas. Cada miembro debe poder operar y explicar los tres sistemas, por lo que el reparto por áreas no implica aislamiento de conocimiento.")
tabla(["Integrante", "Rol SCRUM y área funcional"], [[s["name"], s["role"]] for s in datos["stakeholders"][1:]], [6.5, 10.5], titulo="Roles del equipo")

doc.add_heading("2.2 Comparativa y justificación de herramientas", 2)
doc.add_heading("2.2.1 Hosting de WordPress", 3)
par("Se comparan cuatro alternativas para alojar el CMS. La valoración es cualitativa; no se han contratado ni probado los servicios de pago.")
tabla(["Criterio", "Servidor local WampServer + Tailscale", "Hosting gratuito compartido", "Hosting compartido de pago", "WordPress.com"], [
    ["Coste", "0 €", "0 €", "Cuota periódica", "Plan gratuito limitado; los planes con plugins son de pago"],
    ["Control sobre PHP, MySQL y archivos", "Total", "Limitado", "Alto", "Bajo"],
    ["Instalación de plugins propios", "Sí", "Sí", "Sí", "Solo en planes de pago"],
    ["Disponibilidad", "Solo con el equipo anfitrión encendido", "Variable", "24 h / 7 d", "24 h / 7 d"],
    ["Acceso simultáneo del equipo", "Sí, por red privada Tailscale", "Sí, por internet", "Sí, por internet", "Sí, por internet"],
    ["Cumple lo que pide la guía del proyecto", "Sí: exige servidor local (XAMPP, WAMP o MAMP)", "Opcional", "Opcional", "Opcional"],
    ["Riesgo principal", "Dependencia de un solo PC", "Límites y rendimiento", "Coste", "Falta de control"],
], [3.4, 3.7, 3.0, 3.3, 3.6], tam=8, titulo="Comparativa de alojamiento para WordPress")
rico("**Elección: servidor local WampServer compartido mediante Tailscale.** La guía del proyecto exige un servidor local verificado con PHP y MySQL; Wamp cumple ese requisito sin coste, permite instalar cualquier plugin y deja que los cinco integrantes trabajen a la vez sobre la misma instancia de WordPress y la misma base de datos `bd_cadus`. La VPN privada de Tailscale evita abrir puertos del router y limita el acceso a los miembros invitados. El inconveniente asumido es la disponibilidad, que se mitiga avisando en Discord (#avisos-servidor) y manteniendo copias de la base de datos en el repositorio.")

doc.add_heading("2.2.2 Software de comunicación del equipo", 3)
tabla(["Criterio", "Discord", "Microsoft Teams", "WhatsApp", "Slack"], [
    ["Coste", "Gratuito", "Gratuito con cuenta universitaria o personal", "Gratuito", "Gratuito con límites"],
    ["Canales por tema", "Sí (categorías y canales)", "Sí (equipos y canales)", "No (grupos planos)", "Sí"],
    ["Voz y pantalla compartida para trabajar desde casa", "Sí, canales de voz permanentes", "Sí, reuniones", "Llamadas básicas", "Llamadas (limitadas en gratis)"],
    ["Integración con GitHub", "Sí, webhook de commits", "Sí, mediante aplicación", "No", "Sí"],
    ["Historial y búsqueda", "Ilimitado y buscable", "Sí", "Limitado a búsqueda simple", "Limitado en el plan gratuito"],
    ["Encaje en el proyecto", "Comunicación diaria del equipo", "Se usará como Sistema 3 del proyecto (Teams, Planner, Power Platform)", "Avisos urgentes", "—"],
], [3.4, 3.4, 3.8, 3.0, 3.4], tam=8, titulo="Comparativa de software de comunicación")
rico("**Elección: Discord.** Permite estructurar la comunicación en categorías (INFO, SCRUM, DESARROLLO y VOZ), mantiene salas de voz siempre abiertas para el trabajo a distancia y recibe los commits de GitHub. Teams se reserva para el Sistema 3 de la asignatura, en el que será objeto de implantación y no herramienta de trabajo. La estructura creada está descrita en `docs/arquitectura/entorno-de-trabajo.md`.")

doc.add_heading("2.2.3 Software para la gestión de SCRUM", 3)
tabla(["Criterio", "GitHub Projects", "Jira", "Trello", "Microsoft Planner", "Taiga"], [
    ["Coste", "Gratuito", "Gratuito para equipos pequeños", "Gratuito con límites", "Incluido en Microsoft 365", "Gratuito para proyectos pequeños"],
    ["Integración con el repositorio", "Nativa: incidencias y pull requests", "Mediante integración", "Mediante extensión", "No", "Mediante integración"],
    ["Puntos de historia y sprints", "Campos personalizados e iteraciones", "Sí", "Con extensiones", "No", "Sí"],
    ["Burndown", "No nativo: se calcula desde el backlog", "Nativo", "Con extensiones", "No", "Nativo"],
    ["Plantillas SCRUM", "Plantillas de incidencias y de tablero", "Sí", "Sí", "Básicas", "Sí"],
    ["Curva de aprendizaje", "Baja (ya se usa GitHub)", "Media-alta", "Baja", "Baja", "Media"],
], [3.0, 3.0, 2.6, 2.6, 3.0, 2.8], tam=8, titulo="Comparativa de herramientas de gestión SCRUM")
rico("**Recomendación: GitHub Projects**, con tablero, incidencias etiquetadas como historia de usuario (existen plantillas en `.github/ISSUE_TEMPLATE`) y los artefactos SCRUM versionados en el repositorio. Es la opción de menor fricción: el equipo ya trabaja en GitHub, que la guía define como fuente de la verdad, y cada historia puede enlazarse con sus commits y pull requests. Su carencia es el burndown nativo; se compensa generando el gráfico a partir de los puntos de historia del backlog (`docs/scrum/burndown/sprint-01.csv`, generado por `scripts/entrega/diagramas.py`). Si el equipo prefiere un burndown automático, Taiga sería la alternativa SCRUM puro.")

doc.add_heading("2.2.4 Sistema de control de versiones", 3)
tabla(["Criterio", "Git + GitHub", "Git + GitLab", "Git + Bitbucket", "Subversion"], [
    ["Modelo", "Distribuido", "Distribuido", "Distribuido", "Centralizado"],
    ["Coste para el equipo", "Gratuito", "Gratuito", "Gratuito", "Gratuito (requiere servidor)"],
    ["Revisión de cambios (pull / merge request)", "Sí", "Sí", "Sí", "No nativa"],
    ["Incidencias y tableros", "Sí (Projects)", "Sí", "Sí (con Jira)", "No"],
    ["Exigido por la guía del proyecto", "Sí: «fuente de la verdad»", "No", "No", "No"],
], [4.5, 3.5, 3.0, 3.0, 3.0], tam=8, titulo="Comparativa de control de versiones")
rico("**Elección: Git con GitHub.** La guía exige un repositorio GitHub con la estructura `docs/`, `scrum/`, `cms-wordpress/`, `dms-sharepoint/` y la carpeta del sistema 3, un `README.md` detallado y plantillas SCRUM. El flujo de ramas (`main`, `develop`, `feature/*`) y las plantillas de pull request están documentados en el README del repositorio.")

doc.add_heading("2.3 Product backlog", 2)
par("El product backlog es el mismo de todo el proyecto CMS. Se ordena por prioridad y agrupa tareas técnicas (PB) e historias de usuario (HU), cada una enlazada con los requisitos del REM. Estimación en puntos de historia (Fibonacci).")
tb = parsear_tablas(os.path.join(RAIZ, "docs", "scrum", "backlog", "product-backlog.md"))
infra = [[c[0], c[1], c[4], c[5], c[6]] for c in tb[0][1:]]
tabla(["ID", "Tarea técnica", "SP", "Estado", "Sprint"], infra, [1.6, 10.0, 1.1, 2.0, 2.3], titulo="Product backlog: tareas técnicas y de infraestructura")
hu = [[c[0], c[1], c[2], c[4], c[6]] for c in tb[1][1:]]
tabla(["ID", "Historia de usuario", "Requisitos", "SP", "Sprint"], hu, [1.5, 9.1, 3.0, 1.0, 2.4], tam=8, titulo="Product backlog: historias de usuario")
par(f"Total del product backlog: {sum(int(c[4]) for c in tb[0][1:]) + sum(int(c[4]) for c in tb[1][1:])} puntos de historia.", cursiva=True)

doc.add_heading("2.4 Sprint backlog (Sprint 1: 28/09 – 18/10/2026)", 2)
rico("**Objetivo del Sprint 1:** desplegar la plataforma base en WordPress, definir la identidad visual corporativa del CADUS y maquetar las secciones principales de información, delegaciones y buzón de consultas. **Alcance comprometido: 70 SP.**")
hechas = {"PB-002", "PB-005", "PB-006", "PB-007", "PB-008"}
ts = parsear_tablas(os.path.join(RAIZ, "docs", "scrum", "sprints", "sprint-01.md"))
miembros = [s["name"] + " — " + s["role"] for s in datos["stakeholders"][1:]]
filas_sp = []
for i, t in enumerate(ts[:5]):
    for c in t[1:]:
        if c[0].startswith("**"):
            continue
        filas_sp.append([miembros[i].split(" — ")[0], c[0], c[1], c[2], "Hecho"])
tabla(["Responsable", "ID", "Tarea", "SP", "Estado"], filas_sp, [3.2, 1.5, 8.2, 1.0, 3.1], tam=8, titulo="Sprint backlog del Sprint 1")
hecho_sp = sum(int(f[3]) for f in filas_sp if f[4] == "Hecho")
tot_sp = sum(int(f[3]) for f in filas_sp)
par(f"Resultado: {hecho_sp} de {tot_sp} SP completados ({hecho_sp / tot_sp:.0%}). Las historias HU-09 a HU-12 y HU-19 (tickets avanzados, calendario, votaciones, mediación y panel de administración) corresponden al Sprint 2.", cursiva=True)

doc.add_heading("2.5 Burndown chart del sprint", 2)
figura("burndown-sprint1.png", "Burndown chart del Sprint 1 (alcance 70 SP). Ideal frente a real.", 14.5)
rico("**Lectura.** El sprint arrancó con 70 SP pendientes. PB-002 (entorno WordPress) se completó el 28/09 y PB-005 (servidor compartido con Tailscale) el 05/10. El 18/10 se cerraron PB-006, PB-007 y PB-008 y se implementaron y probaron las diez historias de contenido (HU-01 a HU-08, HU-13 y HU-18), quedando 0 SP pendientes. **Lección aprendida:** la curva real queda por encima de la ideal durante casi todo el sprint y cae de golpe al final; el trabajo de contenido se aplazó en lugar de repartirse. En el Sprint 2 las historias se repartirán a lo largo de las dos semanas y el burndown se actualizará cada día. Los datos están en `docs/scrum/burndown/sprint-01.csv`.")

# ------------------------------------------------------------------ 3. REM
doc.add_heading("3. Requisitos (REM)", 1)
par("Los requisitos se han elicitado a partir del encargo del cliente y se han registrado en REMUS (fichero CADUS.rem, versión 1.0) con la estructura de cinco dimensiones: información, interfaz, funcionales, no funcionales y reglas de negocio. Cada requisito lleva su código de trazabilidad, que se repite en el análisis, el diseño y las capturas. La importancia indicada es la asignada en REMUS.")
imp = {2: "Vital", 3: "Importante", 4: "Quedaría bien"}
doc.add_heading("3.1 Requisitos de información", 2)
tabla(["Código", "Nombre", "Se almacenará información correspondiente a…", "Datos específicos"],
      [[r["id"], r["name"], r["concept"], "; ".join(r["data"])] for r in datos["information"]], [1.5, 3.0, 5.0, 7.5], tam=8, titulo="Requisitos de información")
doc.add_heading("3.2 Actores", 2)
tabla(["Actor", "Representa a…"], [[a["name"], a["role"]] for a in datos["actors"]], [4.0, 13.0], titulo="Actores del sistema")
doc.add_heading("3.3 Requisitos de interfaz de usuario", 2)
tabla(["Código", "Nombre", "El sistema deberá…", "Historias"], [[r["id"], r["name"], r["description"].replace("\n\n- ", "; ").replace("\n", " "), r["comments"]] for r in datos["ui"]],
      [1.5, 3.3, 10.2, 2.0], tam=8, titulo="Requisitos de interfaz de usuario")
doc.add_heading("3.4 Requisitos funcionales", 2)
tabla(["Código", "Nombre", "El sistema deberá…", "Historias", "Importancia"], [[r["id"], r["name"], r["description"], r["comments"], imp[r["importance"]]] for r in datos["functional"]],
      [1.4, 3.5, 7.2, 2.0, 2.2], tam=8, titulo="Requisitos funcionales")
doc.add_heading("Casos de uso", 3)
for u in datos["usecases"]:
    rico(f"**{u['id']} · {u['name']}** — Evento disparador: {u['trigger']}. Precondición: {u['pre']}. Postcondición: {u['post']}.")
    for i, s in enumerate(u["steps"], 1):
        quien = next(a["name"] for a in datos["actors"] if a["id"] == s["actor"]) if s["who"] == "actor" else "El sistema"
        par(f"{i}. {quien} {s['text']}.", despues=1)
    par()
doc.add_heading("3.5 Requisitos no funcionales", 2)
tabla(["Código", "Nombre", "El sistema deberá…", "Importancia"], [[r["id"], r["name"], r["description"], imp[r["importance"]]] for r in datos["nonfunctional"]], [1.6, 3.6, 9.8, 2.0], tam=8.5, titulo="Requisitos no funcionales")
doc.add_heading("3.6 Reglas de negocio", 2)
tabla(["Código", "Nombre", "Regla"], [[r["id"], r["name"], r["description"]] for r in datos["rules"]], [1.6, 4.0, 11.4], titulo="Reglas de negocio")
doc.add_heading("3.7 Restricciones del entorno de trabajo", 2)
tabla(["Código", "Nombre", "Descripción"], [[r["id"], r["name"], r["description"]] for r in datos["environment"]], [1.6, 3.8, 11.6], tam=8, titulo="Restricciones del proyecto (Tailscale, GitHub y Discord)")

# ------------------------------------------------------------------ 4. análisis
doc.add_heading("4. Análisis", 1)
doc.add_heading("4.1 Estructura del sitio web", 2)
par("El portal se organiza en seis secciones de primer nivel colgando de la portada. Cada rama indica los requisitos que implementa.")
figura("uml-analisis-estructura-web.png", "Estructura de menús y páginas del portal, con las etiquetas de trazabilidad (IR, RF, UI).", 16)
doc.add_heading("4.2 Diagrama de clases", 2)
par("El modelo de información se deriva de los requisitos de información IR-03 a IR-09. Las entidades en azul tienen requisito propio; las verdes se han deducido de los requisitos funcionales.")
figura("uml-analisis-clases.png", "Diagrama de clases del análisis con las etiquetas de trazabilidad de cada entidad.", 17)
doc.add_heading("4.3 Mockups", 2)
par("Se muestran los cuatro prototipos esenciales y visuales de la web (portada, directorio de delegaciones, buzón de consultas y ficha de acta). Son bocetos de baja fidelidad; la identidad visual definitiva (HU-18) queda para el Sprint 2.")
figura("mockup-01-portada.png", "Mockup de la portada. UI-01 · UI-02 · IR-01.", 13.5)
figura("mockup-02-directorio.png", "Mockup del directorio de delegaciones y su ficha. UI-03 · RF-06 · RF-07.", 13.5)
figura("mockup-03-buzon.png", "Mockup del buzón de consultas y del seguimiento de ticket. UI-04 · RF-08 · RF-09 · RN-02 · RN-03.", 13.5)
figura("mockup-04-acta.png", "Mockup de la ficha de acta o normativa. UI-05 · RF-03 · RF-04 · RF-05 · RN-01.", 13.5)

# ------------------------------------------------------------------ 5. diseño
doc.add_heading("5. Diseño", 1)
doc.add_heading("5.1 Arquitectura de plugins", 2)
par("La figura muestra qué plugin da respuesta a cada requisito. En verde, los ya instalados; en naranja, los previstos para el Sprint 2.")
figura("uml-diseno-plugins.png", "Diagrama de diseño: plugins de WordPress y requisitos a los que responden.", 16.5)

doc.add_heading("5.2 Comparativa y elección de plugins", 2)
par(f"Para cada tipo de plugin se comparan al menos tres alternativas con los criterios de la guía: fecha de la última actualización, número de instalaciones activas, valoración de los usuarios y número de valoraciones. Los datos proceden de la API pública de wordpress.org consultada el {FECHA_DATOS}; la valoración está en una escala de 5. Además se ha tenido en cuenta la compatibilidad con la versión instalada (WordPress 7.1, PHP 8.x) y el encaje con los requisitos del REM.")
doc.add_heading("Plugins obligatorios: seguridad, caché, analítica y SEO", 3)
comparar("Seguridad", ["wordfence", "all-in-one-wp-security-and-firewall", "better-wp-security", "sucuri-scanner"], "wordfence",
         "Wordfence es el más instalado (más de 5 M), con 4,7/5 en más de 5.000 valoraciones y actualización reciente. Combina cortafuegos, escáner de malware y protección del inicio de sesión, lo que cubre RNF-04 y RNF-08. All-In-One Security (4,7/5) es una alternativa más ligera; Kadence Security (antes Solid Security) y Sucuri están más centrados en endurecimiento y auditoría. La licencia gratuita ya está registrada.")
comparar("Caché", ["wp-fastest-cache", "wp-super-cache", "w3-total-cache", "litespeed-cache"], "wp-fastest-cache",
         "WP Fastest Cache tiene la mejor valoración del grupo (4,9/5 en más de 4.000 valoraciones), se configura con casillas sencillas y funciona sobre Apache con .htaccess, que es nuestro servidor. LiteSpeed Cache es el más instalado, pero su rendimiento depende de un servidor LiteSpeed. W3 Total Cache ofrece más opciones a costa de más complejidad. Responde a RNF-01 (carga inferior a 3 s) y RNF-06.")
comparar("Analítica", ["wp-statistics", "google-site-kit", "google-analytics-for-wordpress", "koko-analytics"], "wp-statistics",
         "WP Statistics guarda los datos en la propia base de datos, sin cookies de terceros ni cuenta de Google, lo que encaja con RNF-08 (RGPD) y funciona desde el servidor local. Site Kit y MonsterInsights tienen más instalaciones pero dependen de Google Analytics y de un sitio público. Koko Analytics es muy ligero pero con menos informes. Para la publicación final se podrá añadir Site Kit.")
comparar("SEO", ["wordpress-seo", "seo-by-rank-math", "all-in-one-seo-pack", "wp-seopress"], "wordpress-seo",
         "Yoast SEO es el estándar del mercado (más de 10 M de instalaciones, 4,8/5 en casi 28.000 valoraciones), con análisis de contenido, metadatos, sitemap XML y migas de pan. Apoya OBJ-02 y UI-02 al mejorar la visibilidad de los comunicados. Rank Math y All in One SEO son alternativas equivalentes; SEOPress es más ligero.")
doc.add_heading("Plugins funcionales", 3)
comparar("Formularios (buzón y mediación)", ["fluentform", "wpforms-lite", "contact-form-7", "ninja-forms"], "fluentform",
         "Fluent Forms guarda las entradas en la base de datos en la versión gratuita (necesario para los tickets del buzón), incluye lógica condicional y validación por expresión regular, con 4,8/5. WPForms Lite solo guarda entradas en la versión de pago y Contact Form 7 solo envía correos. Cubre RF-08, RF-09 y RF-13; la restricción de correo @alum.us.es (RN-02) se aplica en el servidor desde el plugin propio, y se ha comprobado que rechaza un correo ajeno.")
comparar("Tipos de contenido y campos personalizados", ["advanced-custom-fields", "custom-post-type-ui", "pods"], "advanced-custom-fields",
         "ACF aporta los campos de las actas (fecha, pleno y archivo PDF) y de las delegaciones (contacto y horario), con más de 2 M de instalaciones; los campos se definen por código en el plugin propio para que viajen con el repositorio. Los tipos de contenido se registran con la función nativa de WordPress desde ese mismo plugin, de modo que no hace falta Custom Post Type UI, que solo registra tipos y taxonomías. Pods ofrece lo mismo que ACF con una comunidad menor. Cubre RF-03, RF-04, RF-06 y RF-07.")
comparar("Roles y permisos", ["members", "user-role-editor", "wpfront-user-role-editor"], "members",
         "Members tiene la mejor valoración (4,9/5) y permite crear los roles Ejecutiva, Delegado y Estudiante con capacidades a medida, y restringir contenido por rol. Los roles Ejecutiva, Delegado y Estudiante los crea el plugin propio y se gestionan con Members. Son la base de RF-14 y del flujo de aprobación RF-05 / RN-01, que usa el estado nativo «Pendiente de revisión». User Role Editor tiene más instalaciones pero menos funciones de control de contenido.")
comparar("Calendario de eventos (Sprint 2)", ["the-events-calendar", "my-calendar", "sugar-calendar-lite", "event-organiser"], "the-events-calendar",
         "The Events Calendar es el más instalado (600 k) y tiene vistas de calendario, lista y mes listas para usar; responde a RF-11 y RF-12. My Calendar y Event Organiser son alternativas válidas con menos uso.")
comparar("Gestión de tickets (Sprint 2)", ["supportcandy", "awesome-support", "fluent-support"], "",
         "En la Entrega 1 se seleccionó SupportCandy por su valoración (4,9/5) y su panel por rol. En el Sprint 2 (HU-09) se decidió no instalar ninguno y ampliar el módulo propio del buzón: SupportCandy guarda los tickets en sus propias tablas, así que habría que rehacer la integración con Fluent Forms, el código de seguimiento CAD-AAAA-NNNNN (RF-09) y la página de seguimiento (HU-08), o mantener dos sistemas a la vez. El módulo propio ya cumplía la privacidad de RN-03 (tickets privados, sin API REST ni búsqueda) y solo le faltaban los filtros y el aviso al estudiante, que se han añadido en HU-09a. Así se reduce el riesgo antes de la congelación y no se añade un plugin más que mantener. Awesome Support (3,5/5) y Fluent Support tienen el mismo problema de integración.")
comparar("Votaciones (Sprint 2)", ["yop-poll", "wp-polls", "poll-maker"], "yop-poll",
         "YOP Poll admite votaciones programadas, control de votos únicos y resultados, necesarios para RF-12 y RN-05; tiene actualización reciente y 4,4/5.")
comparar("Gestión de documentos descargables", ["download-monitor", "document-library-lite", "wp-document-revisions"], "",
         "Por ahora no se instala ninguno: un campo de archivo de ACF sobre un tipo «Acta» cubre RF-03 y RF-04 sin plugin adicional. Download Monitor (80 k, 4,5/5) se incorporará solo si se necesitan estadísticas de descarga.")

doc.add_heading("5.3 Tema de WordPress", 2)
rico("**Tema elegido: Blocksy**, instalado y activo (versión 2.1.60). Se eligió por su valoración (5/5 en más de 800 valoraciones), su actualización reciente (15/10/2026), la etiqueta «Accessibility ready» (RNF-03), un generador de cabeceras gratuito y una paleta de colores editable, que permitió aplicar la identidad del CADUS (UI-01) sin escribir CSS. Se configuró con una paleta azul marino y dorado y un logotipo provisional.")
par("La comparativa razonada de al menos tres temas corresponde a la documentación de la versión final y se entregará en la entrega 2 (25/10); los datos de partida están recogidos en docs/entrega/datos/themes.json. El logotipo y los colores son provisionales hasta que el cliente facilite su identidad visual.")

# ------------------------------------------------------------------ 6. implementación
doc.add_heading("6. Implementación", 1)
par("Capturas del WordPress del equipo (servidor local WampServer, WordPress 7.1, tema Blocksy) con todo lo implementado en el Sprint 1. Cada captura indica los requisitos y las historias a las que corresponde. Los textos de noticias, actas y delegaciones son de ejemplo; se sustituirán por contenido real.")
imp_items = [
    ("09-portada-final.jpg", "Portada del portal con tema Blocksy, logotipo y banner. UI-01 · UI-02 · IR-01 · HU-18.",
     "La portada muestra el banner institucional con accesos al directorio y al buzón, y debajo los comunicados recientes. El tema Blocksy se configuró con la paleta del CADUS (azul marino y dorado) y un logotipo provisional."),
    ("10-noticias.jpg", "Listado de noticias con filtro por palabra clave, categoría y año. RF-01 · RF-02 · IR-03 · HU-01 · HU-02.",
     "Los comunicados se clasifican en las categorías Becas, Movilidad, Normativa y Eventos. El formulario filtra por palabra clave, categoría y año, y el listado se pagina."),
    ("11-actas-y-normativa.jpg", "Repositorio de actas y normativas con filtro por tipo y descarga en PDF. RF-03 · RF-04 · UI-05 · HU-04.",
     "La tabla se ordena por fecha y filtra por tipo (acta o normativa). Cada documento tiene su ficha con los datos y un botón de descarga del PDF. Solo se listan los documentos publicados."),
    ("16-admin-actas.jpg", "Panel de administración de actas: dos publicadas y una «Pendiente». RF-05 · RN-01 · HU-03.",
     "El acta «pendiente de aprobación» solo es visible aquí y no aparece en la web pública. Solo la Ejecutiva y el administrador tienen la capacidad de publicarla; un delegado solo puede dejarla pendiente."),
    ("12-delegaciones.jpg", "Directorio de delegaciones agrupado por facultad o escuela. RF-06 · UI-03 · HU-05.",
     "Cada centro lista sus delegaciones, con enlace a su ficha (delegado, correo, teléfono, horario y enlaces). Hay una delegación de ejemplo por cada uno de los seis centros cargados; los datos de contacto están por completar por cada delegado (HU-06)."),
    ("13-buzon-codigo-ticket.jpg", "Buzón de consultas: confirmación con el código de seguimiento. RF-08 · RF-09 · RN-02 · UI-04 · HU-07.",
     "Al enviar el formulario con un correo @alum.us.es se crea un ticket privado y se muestra el código CAD-AAAA-NNNNN. Con un correo de otro dominio el envío se rechaza con un mensaje de error (RN-02)."),
    ("14-seguimiento-ticket.jpg", "Seguimiento de ticket con código y correo. RF-09 · RN-03 · HU-08.",
     "La consulta exige código y correo a la vez. Muestra tipo, asunto, estado y respuestas. Si los datos no coinciden devuelve un mensaje genérico, sin revelar si el código existe (RN-03)."),
    ("15-admin-tickets.jpg", "Tickets del buzón en el panel de administración, visibles solo para la Ejecutiva. RF-10 · RN-03.",
     "Los tickets son un tipo de contenido privado: no son públicos ni accesibles por la API REST. La Ejecutiva ve código, correo, tipo y estado, y puede cambiar el estado y añadir respuestas. En el Sprint 2 (HU-09a) se amplía este módulo con filtros por estado y tipo y aviso por correo al estudiante."),
    ("19-fluent-forms-buzon.jpg", "Formulario «Buzón de consultas y reclamaciones» en Fluent Forms. RF-08 · RN-02 · RNF-04.",
     "El formulario lo crea el plugin propio al activarse e incluye consentimiento RGPD obligatorio. La validación del dominio y de los campos se repite en el servidor."),
    ("17-roles-members.jpg", "Listado de roles en Members con los roles del CADUS. RF-14 · RN-04 · HU-13.",
     "Además de los roles estándar de WordPress existen Ejecutiva del CADUS, Delegado de centro y Estudiante US, con los permisos descritos en la sección de pruebas."),
    ("18-tema-blocksy.jpg", "Pantalla de temas con Blocksy instalado y activo. UI-01 · RNF-02 · RNF-03 · HU-18.",
     "Blocksy es el tema activo. El aviso del tema sobre su plugin complementario es opcional y no se ha instalado."),
    ("01-plugins-instalados.jpg", "Listado de plugins activos. RF-15 · RNF-01 · RNF-04 · RNF-08.",
     "Plugins obligatorios del curso (Wordfence, WP Fastest Cache, WP Statistics y Yoast SEO), plugins funcionales (Advanced Custom Fields, Fluent Forms y Members) y el plugin propio CADUS Portal."),
    ("08-yoast-seo-editor.jpg", "Editor de bloques con el panel de Yoast SEO. RF-01 · RF-02 · UI-02 · OBJ-02.",
     "Yoast SEO se integra en el editor de cada entrada y página para definir frase clave, título y descripción."),
    ("02-wp-fastest-cache-ajustes.jpg", "Ajustes de WP Fastest Cache guardados. RNF-01 · RNF-06.",
     "Caché de páginas con compresión Gzip, excluyendo a los usuarios conectados para que el equipo vea sus cambios al instante."),
    ("06-wordfence.jpg", "Panel de Wordfence con la protección activada. RNF-04 · RNF-08.",
     "Cortafuegos de aplicaciones en modo de aprendizaje y licencia gratuita registrada."),
    ("03-wp-statistics.jpg", "Resumen de WP Statistics, analítica sin cookies de terceros. RNF-08 · RNF-01.",
     "Registra visitas y páginas más vistas en la propia base de datos, conforme al RGPD."),
]
nfig = {}
for archivo, pie, texto in imp_items:
    nfig[archivo] = figura(archivo, pie, 15.5, CAP)
    par(texto)

doc.add_heading("Estado de la implementación por historia de usuario", 2)
F = lambda a: f"figura {nfig[a]}"
tabla(["Historia", "Estado", "Evidencia"], [
    ["PB-002 · PB-005 · PB-006", "Hecho", "Servidor Wamp, acceso por Tailscale y servidor de Discord operativos."],
    ["PB-007", "Hecho", f"Siete plugins de terceros y el plugin propio activos ({F('01-plugins-instalados.jpg')})."],
    ["PB-008", "Hecho", "CADUS.rem (REMUS) generado y revisado."],
    ["HU-01 · HU-02", "Hecho", f"Portada con comunicados y listado filtrable ({F('09-portada-final.jpg')}, {F('10-noticias.jpg')})."],
    ["HU-03 · HU-04", "Hecho", f"Flujo de aprobación y repositorio con descarga ({F('16-admin-actas.jpg')}, {F('11-actas-y-normativa.jpg')})."],
    ["HU-05 · HU-06", "Hecho", f"Directorio y ficha de delegación ({F('12-delegaciones.jpg')}); edición restringida al delegado propietario."],
    ["HU-07 · HU-08", "Hecho", f"Buzón, código de ticket y seguimiento ({F('13-buzon-codigo-ticket.jpg')}, {F('14-seguimiento-ticket.jpg')})."],
    ["HU-13", "Hecho", f"Roles Ejecutiva, Delegado y Estudiante ({F('17-roles-members.jpg')})."],
    ["HU-18", "Hecho", f"Tema Blocksy con paleta y logotipo provisional ({F('18-tema-blocksy.jpg')})."],
], [4.0, 2.0, 11.0], titulo="Estado de la implementación")

doc.add_heading("Pruebas realizadas", 2)
par("Las pruebas se hicieron en el servidor compartido; los datos de prueba (un ticket con un correo ficticio) se eliminaron después.")
tabla(["Prueba", "Resultado esperado", "Resultado"], [
    ["Enviar el buzón con un correo de gmail.com", "Rechazo con mensaje (RN-02)", "Correcto: «Utiliza un correo universitario válido terminado en @alum.us.es»"],
    ["Enviar el buzón con un correo @alum.us.es", "Ticket creado y código mostrado (RF-09)", "Correcto: se mostró el código CAD-2026-00049"],
    ["Seguimiento con código correcto y correo equivocado", "Sin datos del ticket (RN-03)", "Correcto: mensaje genérico, no revela si el código existe"],
    ["Seguimiento con código y correo correctos, en mayúsculas y minúsculas", "Muestra tipo, asunto y estado", "Correcto"],
    ["Permisos de cada rol sobre actas, delegaciones y tickets", "Solo Ejecutiva y administrador publican actas y ven tickets; el delegado edita solo lo suyo (RN-01, RN-03, RN-04)", "Correcto en los cuatro roles"],
    ["Acta en estado pendiente en la web pública", "No aparece (RN-01)", "Correcto: solo se listan los publicados"],
    ["Parámetro manipulado ?tipo[]=acta en el listado de actas", "Sin error del servidor", "Corregido tras la revisión de código (antes devolvía error 500)"],
    ["Volver a ejecutar la configuración del plugin", "No duplica contenido", "Correcto: mismas entradas, páginas, actas, delegaciones y elementos de menú"],
], [5.5, 5.5, 6.0], tam=8, titulo="Pruebas funcionales y de seguridad")

# ------------------------------------------------------------------ 7. trazabilidad
doc.add_heading("7. Matriz de trazabilidad", 1)
par("Cada requisito del REM aparece con el mismo código en el análisis (entidad o pantalla), en el diseño (plugin) y en la implementación (figura).")
tabla(["Requisito (REM)", "Análisis (UML / mockup)", "Diseño (plugin)", "Implementación"], [
    ["RF-01 Publicación de noticias", "Clases Noticia, Categoria · UI-02", "Plugin propio + Yoast SEO", f"{F('10-noticias.jpg')}, {F('08-yoast-seo-editor.jpg')}"],
    ["RF-02 Búsqueda de noticias", "Clase Noticia · UI-02", "Plugin propio (filtro)", F("10-noticias.jpg")],
    ["RF-03 Repositorio de actas", "Clase DocumentoInstitucional · UI-05", "Plugin propio + ACF", F("11-actas-y-normativa.jpg")],
    ["RF-04 Repositorio de normativas", "Clase DocumentoInstitucional · UI-05", "Plugin propio + ACF", F("11-actas-y-normativa.jpg")],
    ["RF-05 Aprobación previa", "DocumentoInstitucional.estadoAprobacion", "Plugin propio + Members", F("16-admin-actas.jpg")],
    ["RF-06 Directorio de delegaciones", "Clases Delegacion, FacultadEscuela · UI-03", "Plugin propio + ACF", F("12-delegaciones.jpg")],
    ["RF-07 Ficha de delegación", "Clase Delegacion · UI-03", "Plugin propio + ACF + Members", F("12-delegaciones.jpg")],
    ["RF-08 Buzón de consultas", "Clase Ticket · UI-04", "Fluent Forms + plugin propio", f"{F('13-buzon-codigo-ticket.jpg')}, {F('19-fluent-forms-buzon.jpg')}"],
    ["RF-09 Código de seguimiento", "Ticket.codigoSeguimiento · UI-04", "Plugin propio", f"{F('13-buzon-codigo-ticket.jpg')}, {F('14-seguimiento-ticket.jpg')}"],
    ["RF-10 Gestión de tickets", "Clases Ticket, RespuestaTicket", "Plugin propio (módulo buzón)", f"{F('15-admin-tickets.jpg')}; HU-09a: filtros y aviso al estudiante"],
    ["RF-11 Calendario", "Clase EventoCalendario", "The Events Calendar (previsto)", "Sprint 2"],
    ["RF-12 Convocatorias de votación", "EventoCalendario.asambleaVinculada", "The Events Calendar + YOP Poll (previstos)", "Sprint 2"],
    ["RF-13 Solicitud de mediación", "Clase SolicitudMediacion", "Fluent Forms", "Sprint 2 (HU-12)"],
    ["RF-14 Roles y permisos", "Clase Usuario (rol)", "Plugin propio + Members", F("17-roles-members.jpg")],
    ["RF-15 Panel de administración", "Todas las clases", "Panel de WordPress + ACF + Members", f"{F('01-plugins-instalados.jpg')}, {F('16-admin-actas.jpg')}"],
    ["RNF-01 Rendimiento", "—", "WP Fastest Cache", F("02-wp-fastest-cache-ajustes.jpg")],
    ["RNF-03 Accesibilidad", "Mockups", "Tema Blocksy", F("18-tema-blocksy.jpg")],
    ["RNF-04 Seguridad en formularios", "—", "Wordfence + Fluent Forms", f"{F('06-wordfence.jpg')}, {F('13-buzon-codigo-ticket.jpg')}"],
    ["RNF-08 Privacidad", "Ticket.confidencial · UI-04", "WP Statistics + Wordfence + plugin propio", f"{F('03-wp-statistics.jpg')}, {F('14-seguimiento-ticket.jpg')}"],
    ["UI-01 Diseño gráfico", "Mockup de portada", "Tema Blocksy", f"{F('09-portada-final.jpg')}, {F('18-tema-blocksy.jpg')}"],
    ["UI-02 Página principal", "Mockup 1 · estructura web", "Tema + Yoast SEO", F("09-portada-final.jpg")],
    ["UI-03 Directorio", "Mockup 2", "Plugin propio", F("12-delegaciones.jpg")],
    ["UI-04 Buzón de consultas", "Mockup 3", "Fluent Forms + plugin propio", F("13-buzon-codigo-ticket.jpg")],
    ["UI-05 Ficha de acta o normativa", "Mockup 4", "Plugin propio + ACF", F("11-actas-y-normativa.jpg")],
], [4.3, 4.7, 4.3, 3.7], tam=8, titulo="Trazabilidad requisito → análisis → diseño → implementación")
par("Los números de figura corresponden a la numeración de este documento; se recalculan automáticamente al regenerarlo.", cursiva=True, tam=9)

# ------------------------------------------------------------------ 8. calidad e incidencias
doc.add_heading("8. Calidad, incidencias y próximos pasos", 1)
doc.add_heading("Revisión cruzada del código", 2)
par("El plugin propio se repartió entre dos asistentes de programación: Claude escribió los roles, las actas, las delegaciones y la configuración del sitio, y Codex escribió el módulo del buzón. Después cada uno revisó el código del otro, y el resultado se probó en el servidor. El código se revisó y comprendió antes de integrarlo; el desglose está en el README del plugin (cms-wordpress/wp-content/plugins/cadus-portal/README.md).")
tabla(["Revisor", "Hallazgos", "Resolución"], [
    ["Codex sobre el código de Claude", "9: error 500 con ?tipo[]=; borrado de contenido por defecto en cada activación; ajustes del equipo sobrescritos al reactivar; ejemplos recreados al renombrarlos; la búsqueda de noticias incluía páginas y actas; actas sin fecha omitidas y sin paginación; enlace al PDF perdido sin ACF; orden de enlaces y tipos; roles borrados y recreados", "Los 9 corregidos y verificados (sección 6, pruebas)"],
    ["Claude sobre el código de Codex", "Sin fallos bloqueantes. Observaciones: el código del ticket no es correlativo (deriva del ID); el seguimiento no acredita la propiedad del correo, solo la coincidencia", "Aceptado y documentado; se mitigó con límite de intentos y exigiendo código y correo"],
], [4.0, 8.5, 4.5], tam=8, titulo="Revisión cruzada")
doc.add_heading("Incidencias resueltas durante el sprint", 2)
tabla(["Incidencia", "Causa", "Solución"], [
    ["WordPress no podía descargar plugins (cURL error 77)", "Faltaba wp-includes/certificates/ca-bundle.crt: el .gitignore excluye *.crt", "Restaurado el archivo desde el repositorio oficial de WordPress"],
    ["Pantallas de Yoast y Fluent Forms en blanco; editor de bloques sin cargar", "Faltaban wp-includes/js/dist, css/dist y build: el .gitignore excluye dist/ y build/", "Restauradas desde el paquete oficial de WordPress 7.1 (404 archivos)"],
    ["WP Fastest Cache no guardaba sus ajustes", "No existía el archivo .htaccess", "Creado el .htaccess estándar de WordPress"],
    ["Un clon nuevo del repositorio no reproducía el entorno", "Los patrones del .gitignore dejaban fuera esos archivos del núcleo", "Excepciones en cms-wordpress/.gitignore; los plugins de terceros dejan de versionarse y se documentan aquí"],
    ["Enlaces de las páginas sin index.php daban error 404", "El sitio usaba la estructura de enlaces antigua", "Enlaces permanentes por nombre fijados desde el plugin propio"],
], [4.8, 6.0, 6.2], tam=8, titulo="Incidencias técnicas y su resolución")
doc.add_heading("Próximos pasos (Sprint 2, entrega del 25/10)", 2)
for t in ("Sustituir los textos de ejemplo por contenido real validado con la Delegación General del CADUS y completar las fichas de las delegaciones.",
          "Asignar los roles Ejecutiva y Delegado a los usuarios reales del cliente (hoy el equipo usa cuentas de administrador).",
          "Instalar y configurar The Events Calendar, SupportCandy y YOP Poll (HU-09 a HU-12) y el panel de administración (HU-19).",
          "Reemplazar el logotipo provisional por la identidad visual real del cliente.",
          "Repartir el trabajo a lo largo del sprint y actualizar el burndown cada día.",
          "Para la entrega 2: comparativa razonada de al menos tres temas y versión final del portal."):
    vineta(t)

# ------------------------------------------------------------------ pie de página
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run("Portal CADUS · Entrega 1 (CMS) · Página ")
r.font.size = Pt(8.5)
campo(fp, "PAGE", "1")

# actualizar campos (índice) al abrir
settings = doc.settings.element
u = OxmlElement("w:updateFields")
u.set(qn("w:val"), "true")
settings.append(u)

doc.core_properties.title = "Portal web del CADUS — Entrega 1 (CMS)"
doc.core_properties.author = "Equipo GSI — CADUS"
doc.save(SALIDA)
print("documento generado:", SALIDA, "·", figura_n[0], "figuras ·", tabla_n[0], "tablas")
