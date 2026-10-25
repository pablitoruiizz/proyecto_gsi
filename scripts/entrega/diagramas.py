"""Genera los diagramas, mockups y el burndown de la entrega. Uso: python scripts/entrega/diagramas.py"""
import csv
import datetime as dt
import json
import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IMG = os.path.join(RAIZ, "docs", "entrega", "img")
BURN = os.path.join(RAIZ, "docs", "scrum", "burndown")
os.makedirs(IMG, exist_ok=True)

AZUL, AZUL_CLARO, GRIS, VERDE, NARANJA, ROJO = "#1f3a5f", "#dbe6f4", "#f4f5f7", "#2e7d32", "#e08a00", "#b3261e"


def lienzo(w, h, dpi=110):
    fig, ax = plt.subplots(figsize=(w / dpi, h / dpi), dpi=dpi)
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax


def guardar(fig, nombre):
    fig.savefig(os.path.join(IMG, nombre), bbox_inches="tight", facecolor="white")
    if nombre.startswith(("mockup-0", "tematica-")):
        # copia vectorial con el texto como texto, para importarla en Figma (docs/entrega/figma/)
        carpeta = os.path.join(RAIZ, "docs", "entrega", "figma")
        os.makedirs(carpeta, exist_ok=True)
        with matplotlib.rc_context({"svg.fonttype": "none"}):
            fig.savefig(os.path.join(carpeta, nombre.replace(".png", ".svg")), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("generado", nombre)


# ---------------------------------------------------------------- clases (análisis)
def clase(ax, x, y, w, nombre, tag, attrs, color=AZUL):
    lineas = textwrap.wrap(tag, 36, break_long_words=False)
    cab = 34 + 17 * len(lineas) + 6
    h = cab + 22 * len(attrs) + 10
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=color, lw=1.6, zorder=2))
    ax.add_patch(Rectangle((x, y), w, 34, fc=color, ec=color, zorder=3))
    ax.text(x + w / 2, y + 17, nombre, ha="center", va="center", color="white", fontsize=11, fontweight="bold", zorder=4)
    for i, l in enumerate(lineas):
        ax.text(x + 8, y + 34 + 12 + 17 * i, l, ha="left", va="center", color=ROJO, fontsize=8.5, fontstyle="italic", zorder=4)
    ax.plot([x, x + w], [y + cab, y + cab], color=color, lw=0.8, zorder=3)
    for i, a in enumerate(attrs):
        ax.text(x + 10, y + cab + 14 + 22 * i, a, ha="left", va="center", fontsize=9, zorder=4)
    return (x, y, w, h)


def centro(c, lado):
    x, y, w, h = c
    return {"izq": (x, y + h / 2), "der": (x + w, y + h / 2), "arr": (x + w / 2, y), "abj": (x + w / 2, y + h)}[lado]


def rel(ax, a, la, b, lb, txt, ma="", mb="", dx=0, dy=-9):
    p, q = centro(a, la), centro(b, lb)
    ax.plot([p[0], q[0]], [p[1], q[1]], color="#444", lw=1.3, zorder=1)
    ax.text((p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, txt, ha="center", va="center", fontsize=8.5, color="#222",
            bbox=dict(fc="white", ec="none", pad=1.2), zorder=5)
    for pt, m, o in ((p, ma, q), (q, mb, p)):
        if m:
            vx, vy = o[0] - pt[0], o[1] - pt[1]
            n = max((vx ** 2 + vy ** 2) ** 0.5, 1)
            ax.text(pt[0] + vx / n * 20, pt[1] + vy / n * 20 - 7, m, ha="center", va="center", fontsize=8.5, fontweight="bold", zorder=5,
                    bbox=dict(fc="white", ec="none", pad=0.8))


def diagrama_clases():
    fig, ax = lienzo(1820, 1090)
    ax.text(910, 22, "Diagrama de clases del portal CADUS (análisis) — etiquetas de trazabilidad en rojo", ha="center", fontsize=13, fontweight="bold", color=AZUL)
    W = 300
    cx = [30, 520, 1010, 1490]
    ry = [70, 410, 760]
    cat = clase(ax, cx[0], ry[0], W, "Categoria", "IR-03 · RF-01", ["nombre", "tipoContenido (noticia|documento)"])
    noticia = clase(ax, cx[1], ry[0], W, "Noticia", "IR-03 · RF-01 · RF-02 · UI-02", ["titulo", "cuerpo", "fechaPublicacion", "estado (borrador | publicada)"])
    evento = clase(ax, cx[2], ry[0], W, "EventoCalendario", "IR-07 · RF-11 · RF-12 · RN-05 · UI-06", ["titulo", "tipo (asamblea|evento|votacion)", "fechaHora", "lugar", "asambleaVinculada (0..1)", "apertura / cierre (votacion)"], VERDE)
    doc = clase(ax, cx[0], ry[1], W, "DocumentoInstitucional", "IR-04 · RF-03 · RF-04 · RF-05 · RN-01 · UI-05", ["tipo (acta | normativa)", "fecha", "archivoPDF", "estadoAprobacion", "plenoAsociado"])
    usuario = clase(ax, cx[1], ry[1], W, "Usuario", "IR-09 · RF-14 · RF-15 · UI-08", ["cuenta (del CADUS o de un delegado)", "correoAcceso", "rol: anonimo, estudiante, delegado,", "      ejecutiva o administrador"])
    deleg = clase(ax, cx[2], ry[1], W, "Delegacion", "IR-05 · RF-06 · RF-07 · RN-04 · UI-03", ["contacto", "horarioAtencion", "enlaces"])
    fac = clase(ax, cx[3], ry[1], W, "FacultadEscuela", "IR-05 · RF-06", ["nombre"], VERDE)
    solic = clase(ax, cx[0], ry[2], W, "SolicitudMediacion", "IR-08 · RF-13 · RN-02 · RN-03 · UI-07", ["referencia", "descripcionConflicto", "fechaSolicitud", "estado (pendiente|en_proceso|", "          cerrada)"], VERDE)
    ticket = clase(ax, cx[1], ry[2], W, "Ticket", "IR-06 · RF-08 · RF-09 · RF-10 · RN-02 · RN-03 · UI-04", ["codigoSeguimiento", "asunto", "estado (abierto|en_proceso|cerrado)", "fechaUltimoAviso", "confidencial"])
    resp = clase(ax, cx[2], ry[2], W, "RespuestaTicket", "RF-10", ["mensaje", "fecha"], VERDE)
    rel(ax, cat, "der", noticia, "izq", "clasifica", "1", "*", dy=-22)
    rel(ax, usuario, "arr", noticia, "abj", "redacta", "1", "*", dx=38)
    rel(ax, usuario, "arr", evento, "abj", "convoca", "1", "*", dx=-8, dy=-18)
    rel(ax, usuario, "izq", doc, "der", "aprueba", "0..1", "*", dy=-22)
    rel(ax, usuario, "der", deleg, "izq", "es delegado de", "0..1", "1", dy=-22)
    rel(ax, deleg, "der", fac, "izq", "pertenece a", "*", "1", dy=-22)
    rel(ax, usuario, "abj", ticket, "arr", "envía", "1", "*", dx=30)
    rel(ax, usuario, "abj", solic, "arr", "solicita", "1", "*", dx=-70, dy=6)
    rel(ax, ticket, "der", resp, "izq", "tiene", "1", "*", dy=-22)
    ax.text(30, 1060, "Azul: entidades con requisito de información propio · Verde: entidades de apoyo derivadas de los requisitos funcionales.", fontsize=8.5, color="#555")
    guardar(fig, "uml-analisis-clases.png")


# ---------------------------------------------------------------- estructura web (análisis)
def caja(ax, x, y, w, h, titulo, sub="", fc=AZUL_CLARO, ec=AZUL, bold=True, subcolor=None, titcolor="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=7", fc=fc, ec=ec, lw=1.3, zorder=2))
    ax.text(x + w / 2, y + (h / 2 - (7 if sub else 0)), titulo, ha="center", va="center", fontsize=9.5, fontweight="bold" if bold else "normal", zorder=3, color=titcolor)
    if sub:
        ax.text(x + w / 2, y + h / 2 + 11, sub, ha="center", va="center", fontsize=8, color=subcolor or ROJO, fontstyle="italic", zorder=3)


def diagrama_estructura():
    fig, ax = lienzo(1560, 990)
    ax.text(780, 22, "Estructura del sitio web (análisis): menús y páginas con sus etiquetas de trazabilidad", ha="center", fontsize=13, fontweight="bold", color=AZUL)
    caja(ax, 40, 435, 190, 70, "Inicio", "UI-02 · IR-01", fc=AZUL, ec=AZUL, subcolor="#ffd2cf", titcolor="white")
    secciones = [
        ("Qué es el CADUS", "IR-02", ["Gobierno", "Estatutos"]),
        ("Noticias y comunicados", "RF-01 · RF-02 · IR-03", ["Becas", "Movilidad", "Normativa", "Eventos"]),
        ("Actas y normativa", "RF-03 · RF-04 · RF-05 · UI-05", ["Ficha de acta / normativa (PDF)"]),
        ("Delegaciones", "RF-06 · RF-07 · UI-03", ["Facultad / Escuela", "Ficha de delegación"]),
        ("Calendario", "RF-11 · RF-12 · IR-07 · UI-06", ["Asambleas", "Eventos", "Votaciones"]),
        ("Atención al estudiante", "RF-08 · RF-09 · RF-13 · UI-04 · UI-07", ["Buzón de consultas", "Seguimiento de ticket", "Mediación estudiantil", "Preguntas frecuentes"]),
        ("Contacto y legal", "RNF-08 · UI-04", ["Contacto", "Aviso de privacidad"]),
    ]
    y = 62
    for nombre, tag, hijos in secciones:
        alto = max(1, len(hijos)) * 36 + 20
        cy = y + alto / 2
        caja(ax, 330, cy - 32, 300, 64, nombre, tag)
        ax.plot([230, 280, 280, 330], [470, 470, cy, cy], color="#555", lw=1.2, zorder=1)
        for i, h in enumerate(hijos):
            hy = y + 10 + i * 36
            caja(ax, 800, hy, 330, 28, h, fc="white", bold=False)
            ax.plot([630, 715, 715, 800], [cy, cy, hy + 14, hy + 14], color="#888", lw=1, zorder=1)
        y += alto + 14
    ax.text(40, 965, "Acceso para usuarios con rol: la gestión de contenidos (RF-15, UI-08) y los roles (RF-14, IR-09) se realizan desde el panel de administración de WordPress.", fontsize=8.5, color="#555")
    guardar(fig, "uml-analisis-estructura-web.png")


# ---------------------------------------------------------------- diseño: plugins
def diagrama_plugins():
    fig, ax = lienzo(1560, 860)
    ax.text(780, 22, "Arquitectura de diseño: plugins por funcionalidad y su trazabilidad", ha="center", fontsize=13, fontweight="bold", color=AZUL)
    ax.add_patch(FancyBboxPatch((470, 315), 620, 160, boxstyle="round,pad=0,rounding_size=10", fc=AZUL, ec=AZUL, zorder=2))
    ax.text(780, 350, "WordPress 7.1 · PHP 8.x · MySQL 8.x", ha="center", va="center", color="white", fontsize=12.5, fontweight="bold", zorder=3)
    ax.text(780, 380, "Servidor local WampServer, compartido por Tailscale", ha="center", va="center", color="white", fontsize=9.5, zorder=3)
    ax.text(780, 412, "Tema: Blocksy (instalado y activo)", ha="center", va="center", color="white", fontsize=9.5, zorder=3)
    ax.text(780, 444, "UI-01 · RNF-02 · RNF-03", ha="center", va="center", color="#ffd2cf", fontsize=9, fontstyle="italic", zorder=3)

    def plugin(x, y, nombre, funcion, tags, estado="instalado"):
        ec, fc, ls = (VERDE, "#eef7ee", "-") if estado == "instalado" else (NARANJA, "#fff6e5", "--")
        ax.add_patch(FancyBboxPatch((x, y), 380, 82, boxstyle="round,pad=0,rounding_size=7", fc=fc, ec=ec, lw=1.6, ls=ls, zorder=2))
        ax.text(x + 12, y + 20, nombre, fontsize=10.5, fontweight="bold", va="center", zorder=3)
        ax.text(x + 12, y + 44, funcion, fontsize=8.8, va="center", color="#333", zorder=3)
        ax.text(x + 12, y + 66, tags, fontsize=8.6, va="center", color=ROJO, fontstyle="italic", zorder=3)
        return (x, y)

    ax.text(40, 70, "Plugins obligatorios del curso (instalados)", fontsize=11, fontweight="bold", color=VERDE)
    obl = [("Wordfence Security", "Seguridad: cortafuegos y escáner de malware", "RNF-04 · RNF-08"),
           ("WP Fastest Cache", "Caché de páginas, Gzip y de navegador", "RNF-01 · RNF-06"),
           ("WP Statistics", "Analítica sin cookies y conforme al RGPD", "RNF-08 · RNF-01"),
           ("Yoast SEO", "SEO: metadatos, sitemap y contenido", "RF-01 · RF-02 · IR-03 · UI-02 · OBJ-02")]
    for i, (n, f, t) in enumerate(obl):
        _, y = plugin(40, 95 + i * 98, n, f, t)
        ax.plot([420, 470], [y + 41, 395], color="#888", lw=1.1, zorder=1)

    ax.text(1140, 70, "Plugins funcionales (instalados)", fontsize=11, fontweight="bold", color=VERDE)
    fun = [("Advanced Custom Fields", "Campos de actas y delegaciones", "RF-03 · RF-04 · RF-06 · RF-07 · IR-04 · IR-05"),
           ("Fluent Forms", "Formularios: buzón y mediación", "RF-08 · RF-09 · RF-13 · IR-06 · IR-08 · RN-02"),
           ("Members", "Roles y permisos (Ejecutiva, Delegado, Estudiante)", "RF-05 · RF-14 · IR-09 · RN-01 · RN-03 · RN-04"),
           ("The Events Calendar", "Calendario de asambleas y eventos (HU-10)", "RF-11 · RF-12 · IR-07 · RN-05 · UI-06")]
    for i, (n, f, t) in enumerate(fun):
        _, y = plugin(1140, 95 + i * 98, n, f, t)
        ax.plot([1140, 1090], [y + 41, 395], color="#888", lw=1.1, zorder=1)

    ax.text(590, 505, "Plugin propio del equipo (instalado)", fontsize=11, fontweight="bold", color=AZUL)
    plugin(590, 520, "CADUS Portal", "Roles, buzón, mediación, votaciones", "RF-01 a RF-15 · IR-01 a IR-09 · RN-01 a RN-05 · UI-01 a UI-08")
    ax.plot([780, 780], [475, 520], color="#888", lw=1.1, zorder=1)
    ax.text(40, 625, "Decisiones del Sprint 2: plugins previstos que no se han instalado", fontsize=11, fontweight="bold", color=NARANJA)
    prev = [("SupportCandy (descartado)", "Tickets: módulo propio (HU-09a)", "RF-10 · RN-03"),
            ("YOP Poll (opcional, pendiente)", "Papeleta de votaciones (opcional)", "RF-12 · RN-05")]
    for i, (n, f, t) in enumerate(prev):
        plugin(40 + i * 430, 650, n, f, t, "previsto")
    ax.add_patch(Rectangle((40, 775), 12, 12, fc=VERDE, ec=VERDE)); ax.text(60, 782, "Instalado y activo", fontsize=9, va="center")
    ax.add_patch(Rectangle((260, 775), 12, 12, fc="#fff6e5", ec=NARANJA, ls="--")); ax.text(280, 782, "No instalado (decisión del Sprint 2)", fontsize=9, va="center")
    ax.text(40, 820, "Las etiquetas en rojo son los códigos de requisito del documento REM (CADUS.rem) a los que da respuesta cada plugin.", fontsize=9, color="#555")
    guardar(fig, "uml-diseno-plugins.png")


# ---------------------------------------------------------------- mockups
def marco(titulo, ui, menu_activo):
    fig, ax = lienzo(1000, 700, 100)
    ax.add_patch(Rectangle((0, 0), 1000, 700, fc="white", ec="#888", lw=1.5))
    ax.add_patch(Rectangle((0, 0), 1000, 34, fc="#e6e8eb", ec="#888"))
    for i, c in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        ax.add_patch(plt.Circle((20 + i * 20, 17), 6, fc=c, ec="none"))
    ax.add_patch(FancyBboxPatch((100, 7), 800, 20, boxstyle="round,pad=0,rounding_size=8", fc="white", ec="#bbb"))
    ax.text(116, 17, titulo, fontsize=8.5, va="center", color="#555")
    ax.add_patch(Rectangle((0, 34), 1000, 70, fc=AZUL))
    ax.add_patch(Rectangle((30, 50), 44, 38, fc="white", ec="none"))
    ax.text(52, 69, "LOGO", ha="center", va="center", fontsize=7.5, color=AZUL, fontweight="bold")
    ax.text(88, 69, "CADUS", fontsize=15, fontweight="bold", color="white", va="center")
    menus = ["Inicio", "Qué es", "Noticias", "Actas", "Delegaciones", "Calendario", "Atención"]
    x = 300
    for m in menus:
        ax.text(x, 69, m, fontsize=9.5, color="white" if m != menu_activo else "#ffd54f", va="center", fontweight="bold" if m == menu_activo else "normal")
        if m == menu_activo:
            ax.plot([x, x + len(m) * 8.8], [86, 86], color="#ffd54f", lw=2)
        x += len(m) * 8.8 + 24
    ax.text(985, 118, ui, ha="right", fontsize=9, color=ROJO, fontstyle="italic", fontweight="bold")
    return fig, ax


def bloque(ax, x, y, w, h, texto, fc="#eceff3", fs=9.5, color="#444"):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec="#c5cad1"))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs, color=color)


def mockup_portada():
    fig, ax = marco("localhost/proyecto_gsi/cms-wordpress/", "UI-01 · UI-02 · IR-01", "Inicio")
    bloque(ax, 30, 135, 940, 150, "BANNER INSTITUCIONAL DEL CADUS\n(imagen + lema)", "#cfd8e6", 12)
    ax.text(30, 310, "Comunicados recientes", fontsize=12, fontweight="bold", color=AZUL)
    for i, cat in enumerate(("Becas", "Movilidad", "Normativa")):
        bloque(ax, 30 + i * 320, 330, 300, 150, f"[{cat}]\nTitular del comunicado\nResumen de dos líneas…", "white", 9)
    bloque(ax, 30, 505, 460, 150, "Acceso al directorio de delegaciones\n(RF-06)", "#e3efe3", 10.5)
    bloque(ax, 510, 505, 460, 150, "Acceso al buzón de consultas\n(RF-08)", "#fdeed6", 10.5)
    bloque(ax, 30, 665, 940, 28, "Próximas asambleas, eventos y votaciones (RF-11) · Pie: contacto cadus@us.es · Pabellón de Uruguay", "#f4f5f7", 8.5)
    guardar(fig, "mockup-01-portada.png")


def mockup_directorio():
    fig, ax = marco("localhost/proyecto_gsi/cms-wordpress/delegaciones/", "UI-03 · RF-06 · RF-07", "Delegaciones")
    ax.text(30, 150, "Directorio de Delegaciones de Alumnos", fontsize=14, fontweight="bold", color=AZUL)
    bloque(ax, 30, 170, 300, 28, "Filtrar por Facultad o Escuela  ▾", "white", 9)
    for i, f in enumerate(("Escuela Técnica Superior de Ingeniería Informática", "Facultad de Derecho", "Facultad de Ciencias de la Educación")):
        y = 215 + i * 105
        ax.text(30, y, f, fontsize=10.5, fontweight="bold", color="#333")
        for j in range(3):
            bloque(ax, 30 + j * 320, y + 12, 300, 62, f"Delegación {j + 1}\nDelegado/a · contacto", "white", 8.8)
    ax.add_patch(Rectangle((610, 560), 360, 125, fc="#fffbe6", ec=NARANJA, ls="--"))
    ax.text(625, 580, "Ficha de delegación (al pulsar)", fontsize=9.5, fontweight="bold")
    ax.text(625, 603, "· Delegado/a responsable\n· Correo y teléfono\n· Horario de atención\n· Enlaces de interés", fontsize=8.8, va="top")
    guardar(fig, "mockup-02-directorio.png")


def mockup_buzon():
    fig, ax = marco("localhost/proyecto_gsi/cms-wordpress/atencion/buzon/", "UI-04 · RF-08 · RF-09 · RN-02", "Atención")
    ax.text(30, 150, "Buzón de consultas y reclamaciones", fontsize=14, fontweight="bold", color=AZUL)
    campos = [("Correo institucional (@alum.us.es) *", 38), ("Asunto *", 38), ("Tipo: consulta · reclamación académica", 38), ("Descripción detallada *", 110)]
    y = 185
    for txt, h in campos:
        ax.text(30, y, txt, fontsize=9.5, fontweight="bold", color="#333")
        bloque(ax, 30, y + 10, 560, h, "", "white")
        y += 22 + h + 20
    bloque(ax, 30, y + 6, 180, 36, "Enviar consulta", AZUL, 10.5, "white")
    ax.add_patch(Rectangle((630, 185), 340, 190, fc="#f4f5f7", ec="#c5cad1"))
    ax.text(645, 208, "Seguimiento de ticket", fontsize=11, fontweight="bold", color=AZUL)
    ax.text(645, 235, "Introduce tu código de seguimiento:", fontsize=9)
    bloque(ax, 645, 250, 310, 34, "CAD-2026-00042", "white", 9.5)
    bloque(ax, 645, 296, 150, 32, "Consultar estado", "#cfd8e6", 9.5)
    ax.text(645, 352, "Estado: abierto · en proceso · cerrado", fontsize=8.8, color="#555")
    ax.add_patch(Rectangle((630, 395), 340, 150, fc="#fdeaea", ec=ROJO, ls="--"))
    ax.text(645, 418, "Privacidad (RN-03)", fontsize=10, fontweight="bold", color=ROJO)
    ax.text(645, 440, "Las reclamaciones solo son visibles para\nquien las envía y para la Ejecutiva.\nSe tratan conforme al RGPD (RNF-08).", fontsize=8.8, va="top")
    guardar(fig, "mockup-03-buzon.png")


def mockup_acta():
    fig, ax = marco("localhost/proyecto_gsi/cms-wordpress/actas/pleno-2026-10/", "UI-05 · RF-03 · RF-04 · RF-05", "Actas")
    ax.text(30, 150, "Acta del Pleno · octubre de 2026", fontsize=14, fontweight="bold", color=AZUL)
    ax.text(30, 175, "Inicio  ›  Actas y normativa  ›  Acta del Pleno", fontsize=8.8, color="#777")
    ax.add_patch(Rectangle((30, 200), 600, 440, fc="#fafafa", ec="#c5cad1"))
    ax.text(330, 420, "Vista previa del documento PDF", ha="center", fontsize=12, color="#999")
    ax.add_patch(Rectangle((660, 200), 310, 190, fc="white", ec="#c5cad1"))
    ax.text(675, 222, "Datos del documento", fontsize=11, fontweight="bold", color=AZUL)
    ax.text(675, 248, "Tipo:  acta\nFecha:  15/10/2026\nPleno asociado:  Pleno ordinario\nEstado:  aprobada por la Ejecutiva\nCategoría:  Normativa", fontsize=9.2, va="top", linespacing=1.7)
    bloque(ax, 660, 410, 310, 44, "Descargar PDF", AZUL, 11, "white")
    ax.add_patch(Rectangle((660, 475), 310, 120, fc="#fffbe6", ec=NARANJA, ls="--"))
    ax.text(675, 495, "Flujo de aprobación (RN-01, RF-05)", fontsize=9.5, fontweight="bold")
    ax.text(675, 517, "borrador → pendiente → aprobada\nSolo un miembro de la Ejecutiva\npuede publicar el documento.", fontsize=8.8, va="top", linespacing=1.5)
    guardar(fig, "mockup-04-acta.png")


# ---------------------------------------------------------------- burndown
def burndown(sprint, inicio, fin, total, hechos):
    """Genera el CSV y la gráfica de un sprint. hechos = {fecha: (SP cerrados ese día, texto)}."""
    dias = [(inicio + dt.timedelta(d)) for d in range((fin - inicio).days + 1)]
    n = len(dias) - 1
    filas, restante = [], total
    for i, d in enumerate(dias):
        if d in hechos:
            restante -= hechos[d][0]
        filas.append((d.isoformat(), round(total * (1 - i / n), 1), restante, hechos.get(d, (0, ""))[1]))
    with open(os.path.join(BURN, f"sprint-0{sprint}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["fecha", "ideal_sp", "real_sp", "tareas_completadas"])
        w.writerows(filas)
    print(f"generado docs/scrum/burndown/sprint-0{sprint}.csv")
    fig, ax = plt.subplots(figsize=(10, 5), dpi=110)
    x = list(range(len(dias)))
    ax.plot(x, [r[1] for r in filas], "--", color="#888", label="Ideal")
    ax.step(x, [r[2] for r in filas], where="post", color=AZUL, lw=2.4, label="Real")
    ax.scatter([i for i, r in enumerate(filas) if r[3]], [r[2] for r in filas if r[3]], color=ROJO, zorder=5)
    for i, r in enumerate(filas):
        if r[3]:
            ax.annotate(r[3], (i, r[2]), textcoords="offset points", xytext=(6, 8), fontsize=8, color=ROJO)
    paso = 3 if len(x) > 10 else 1
    ax.set_xticks(x[::paso])
    ax.set_xticklabels([dias[i].strftime("%d/%m") for i in x[::paso]])
    ax.set_xlabel(f"Días del Sprint {sprint} ({inicio:%d/%m} – {fin:%d/%m/%Y})")
    ax.set_ylabel("Puntos de historia pendientes")
    ax.set_title(f"Burndown chart — Sprint {sprint} (alcance: {total} SP)", fontweight="bold", color=AZUL)
    ax.set_ylim(0, total + 5)
    ax.grid(alpha=0.25)
    ax.legend()
    fig.savefig(os.path.join(IMG, f"burndown-sprint{sprint}.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"generado burndown-sprint{sprint}.png")


def burndowns():
    burndown(1, dt.date(2026, 9, 28), dt.date(2026, 10, 18), 70, {
        dt.date(2026, 9, 28): (5, "PB-002"), dt.date(2026, 10, 5): (5, "PB-005"),
        dt.date(2026, 10, 18): (60, "PB-006, PB-007, PB-008 y HU-01 a HU-08, HU-13, HU-18")})
    # Sprint 2: fechas reales según el historial de Git y las pull requests (19/10: HU-19a y HU-09b;
    # 23/10: HU-19b, HU-10 y HU-12 integradas en main; 24/10: HU-09a, HU-11 y HU-19c).
    burndown(2, dt.date(2026, 10, 19), dt.date(2026, 10, 25), 29, {
        dt.date(2026, 10, 19): (6, "HU-19a, HU-09b"),
        dt.date(2026, 10, 23): (11, "HU-19b, HU-10, HU-12"),
        dt.date(2026, 10, 24): (12, "HU-09a, HU-11, HU-19c")})


def mockup_calendario():
    fig, ax = marco("localhost/proyecto_gsi/cms-wordpress/events/", "UI-06 · RF-11 · RF-12 · RN-05", "Calendario")
    ax.text(30, 150, "Calendario de asambleas y eventos", fontsize=14, fontweight="bold", color=AZUL)
    bloque(ax, 30, 170, 420, 30, "Buscar por eventos…", "white", 9)
    for i, v in enumerate(("Lista", "Mes", "Día")):
        bloque(ax, 480 + i * 70, 170, 62, 30, v, AZUL if i == 0 else "white", 9, "white" if i == 0 else "#444")
    for i, (fecha, titulo, tipo) in enumerate((("12 NOV", "Asamblea general ordinaria", "Asamblea"), ("19 NOV", "Jornada de bienvenida", "Evento"), ("26 NOV", "Votación de los estatutos", "Votación"))):
        y = 225 + i * 82
        bloque(ax, 30, y, 70, 68, fecha, "#cfd8e6", 10, AZUL)
        bloque(ax, 100, y, 520, 68, f"{titulo}\n{tipo} · Pabellón de Uruguay", "white", 9.5)
    ax.add_patch(Rectangle((650, 225), 320, 200, fc="#fffbe6", ec=NARANJA, ls="--"))
    ax.text(665, 247, "Convocatoria de votación (RF-12)", fontsize=9, fontweight="bold")
    ax.text(665, 272, "· Vinculada a una asamblea\n· Apertura: 24 NOV 10:00\n· Cierre: 26 NOV 20:00\n· Solo se vota con la votación\n  abierta (RN-05)", fontsize=8.8, va="top", linespacing=1.6)
    bloque(ax, 650, 445, 320, 44, "Suscribirse al calendario", "white", 10)
    guardar(fig, "mockup-05-calendario.png")


def mockup_mediacion():
    fig, ax = marco("localhost/proyecto_gsi/cms-wordpress/atencion-al-estudiante/mediacion-estudiantil/", "UI-07 · RF-13 · RN-02 · RN-03", "Atención")
    ax.text(30, 150, "Solicitud de mediación estudiantil", fontsize=14, fontweight="bold", color=AZUL)
    campos = [("Nombre y apellidos *", 36), ("Correo universitario (@alum.us.es) *", 36), ("Facultad o Escuela *", 36), ("Descripción del conflicto *", 100)]
    y = 185
    for txt, h in campos:
        ax.text(30, y, txt, fontsize=9.5, fontweight="bold", color="#333")
        bloque(ax, 30, y + 10, 560, h, "", "white")
        y += 22 + h + 18
    ax.text(30, y + 4, "☐  Consiento el tratamiento de mis datos (RGPD) · Aviso de privacidad", fontsize=8.8, color="#333")
    bloque(ax, 30, y + 24, 180, 34, "Solicitar mediación", AZUL, 10.5, "white")
    ax.add_patch(Rectangle((630, 185), 340, 170, fc="#eef7ee", ec=VERDE))
    ax.text(645, 208, "Confirmación", fontsize=11, fontweight="bold", color=VERDE)
    ax.text(645, 234, "Solicitud registrada.\nTu referencia:  MED-2026-00017\nNo se repiten los datos enviados.", fontsize=9.2, va="top", linespacing=1.7)
    ax.add_patch(Rectangle((630, 375), 340, 150, fc="#fdeaea", ec=ROJO, ls="--"))
    ax.text(645, 398, "Privacidad (RN-03)", fontsize=10, fontweight="bold", color=ROJO)
    ax.text(645, 420, "Solo la Ejecutiva ve las solicitudes.\nNo aparecen en la web pública, el buscador\nni la API, ni en los avisos por correo.", fontsize=8.8, va="top", linespacing=1.6)
    guardar(fig, "mockup-06-mediacion.png")


# ---------------------------------------------------------------- tres temáticas visuales para la comparativa
def luminancia(hexa):
    r, g, b = [int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contraste(a, b):
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 1)


# nombre, tema de WordPress candidato, colores y pares (texto, fondo) que se miden
TEMATICAS = [
    dict(clave="A", nombre="Institucional CADUS", tema="blocksy", fondo="#f1f1f1", cab="#ffffff", hero="#8d0739", hero_txt="#ffffff", acento="#faba09",
         tarjetas=["#8d0739", "#faba09", "#212529"], tarjeta_txt=["#ffffff", "#6b052b", "#ffffff"], texto="#212529", boton="#faba09", boton_txt="#6b052b",
         fidelidad="Alta: paleta, logotipo y tipografía de cadus.us.es"),
    dict(clave="B", nombre="Claro y sobrio", tema="astra", fondo="#ffffff", cab="#ffffff", hero="#e8eef7", hero_txt="#1f3a5f", acento="#2b6cb0",
         tarjetas=["#f4f6f9", "#f4f6f9", "#f4f6f9"], tarjeta_txt=["#1f3a5f"] * 3, texto="#1f3a5f", boton="#2b6cb0", boton_txt="#ffffff",
         fidelidad="Baja: azul genérico, sin los colores del CADUS"),
    dict(clave="C", nombre="Oscuro contemporáneo", tema="kadence", fondo="#14161a", cab="#0d0f12", hero="#1d2026", hero_txt="#ffffff", acento="#faba09",
         tarjetas=["#1d2026", "#1d2026", "#1d2026"], tarjeta_txt=["#e8eaed"] * 3, texto="#e8eaed", boton="#faba09", boton_txt="#14161a",
         fidelidad="Media: conserva el dorado, pierde el granate"),
]


def dibujo_tematica(t):
    fig, ax = lienzo(1000, 700, 100)
    ax.add_patch(Rectangle((0, 0), 1000, 700, fc=t["fondo"], ec="#888", lw=1.5, zorder=0))
    ax.add_patch(Rectangle((0, 0), 1000, 34, fc="#e6e8eb", ec="#888", zorder=1))
    for i, c in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        ax.add_patch(plt.Circle((20 + i * 20, 17), 6, fc=c, ec="none", zorder=2))
    ax.add_patch(FancyBboxPatch((100, 7), 800, 20, boxstyle="round,pad=0,rounding_size=8", fc="white", ec="#bbb", zorder=2))
    ax.text(116, 17, f"Temática {t['clave']} · {t['nombre']}", fontsize=8.5, va="center", color="#555", zorder=3)
    ax.text(985, 118, f"UI-01 · UI-02 · tema candidato: {t['tema'].capitalize()}", ha="right", fontsize=9, color="#b3261e" if t["clave"] != "C" else "#faba09", fontstyle="italic", fontweight="bold", zorder=3)
    ax.add_patch(Rectangle((0, 34), 1000, 70, fc=t["cab"], ec="#bbbbbb", zorder=1))
    ax.add_patch(Rectangle((30, 50), 44, 38, fc=t["hero"] if t["clave"] != "B" else t["acento"], ec="none", zorder=2))
    ax.text(52, 69, "LOGO", ha="center", va="center", fontsize=7.5, color="white" if t["clave"] != "C" else "#14161a", fontweight="bold", zorder=3)
    ax.text(88, 69, "CADUS", fontsize=15, fontweight="bold", color=t["texto"], va="center", zorder=3)
    x = 330
    for m in ("Inicio", "Qué es", "Noticias", "Actas", "Delegaciones", "Calendario", "Atención"):
        ax.text(x, 69, m, fontsize=9.5, color=t["texto"], va="center", zorder=3)
        x += len(m) * 8.8 + 24
    # banner
    ax.add_patch(Rectangle((30, 125), 940, 190, fc=t["hero"], ec="none", zorder=1))
    if t["clave"] == "A":
        ax.add_patch(FancyBboxPatch((780, 150), 150, 165, boxstyle="round,pad=0,rounding_size=70", fc="white", ec="none", zorder=2))
        ax.add_patch(FancyBboxPatch((700, 205), 70, 110, boxstyle="round,pad=0,rounding_size=30", fc=t["acento"], ec="none", zorder=2))
        ax.text(855, 240, "logotipo", ha="center", va="center", fontsize=10, color=t["hero"], fontweight="bold", zorder=3)
        ax.text(60, 180, "LA VOZ DEL\nALUMNADO", fontsize=26, fontweight="bold", color=t["hero_txt"], va="center", linespacing=1.0, zorder=3)
    elif t["clave"] == "B":
        ax.add_patch(Rectangle((600, 140, ), 350, 160, fc="#c5d3e6", ec="none", zorder=2))
        ax.text(775, 220, "imagen", ha="center", va="center", fontsize=11, color="#6b7f99", zorder=3)
        ax.text(60, 180, "La voz del alumnado\nde la Universidad de Sevilla", fontsize=19, fontweight="bold", color=t["hero_txt"], va="center", zorder=3)
    else:
        ax.add_patch(Rectangle((60, 150), 8, 70, fc=t["acento"], ec="none", zorder=3))
        ax.text(85, 185, "LA VOZ DEL ALUMNADO", fontsize=22, fontweight="bold", color=t["hero_txt"], va="center", zorder=3)
        ax.text(85, 225, "Consejo de Alumnos · Universidad de Sevilla", fontsize=11, color=t["acento"], va="center", zorder=3)
    ax.add_patch(FancyBboxPatch((60, 262), 220, 36, boxstyle="round,pad=0,rounding_size=6", fc=t["boton"], ec="none", zorder=3))
    ax.text(170, 280, "Enviar una consulta", ha="center", va="center", fontsize=10, fontweight="bold", color=t["boton_txt"], zorder=4)
    # tarjetas de acceso
    for i, (nombre, desc) in enumerate((("Comunicados", "Novedades del CADUS"), ("Actas y normativa", "Consulta y descarga"), ("Buzón de consultas", "Envía tu duda"))):
        x0 = 30 + i * 320
        ax.add_patch(FancyBboxPatch((x0, 340), 300, 130, boxstyle="round,pad=0,rounding_size=8", fc=t["tarjetas"][i],
                                    ec=t["acento"] if t["clave"] == "C" else ("#d6dce5" if t["clave"] == "B" else "none"), lw=1.2, zorder=1))
        ax.text(x0 + 20, 380, nombre, fontsize=14, fontweight="bold", color=t["tarjeta_txt"][i], zorder=3)
        ax.text(x0 + 20, 410, desc, fontsize=9.5, color=t["tarjeta_txt"][i], zorder=3)
    ax.text(30, 505, "Últimas noticias", fontsize=13, fontweight="bold", color=t["texto"], zorder=3)
    for i in range(3):
        ax.add_patch(Rectangle((30 + i * 320, 525), 300, 90, fc="white" if t["clave"] != "C" else "#1d2026", ec="#c5cad1" if t["clave"] != "C" else "#3a3f48", zorder=1))
        ax.text(45 + i * 320, 550, "Titular del comunicado", fontsize=10, fontweight="bold", color="#212529" if t["clave"] != "C" else "#e8eaed", zorder=3)
        ax.text(45 + i * 320, 575, "Resumen de dos líneas…", fontsize=9, color="#555" if t["clave"] != "C" else "#aab0b9", zorder=3)
    ax.add_patch(Rectangle((0, 650), 1000, 50, fc=t["hero"] if t["clave"] != "B" else "#1f3a5f", ec="none", zorder=1))
    ax.text(30, 675, "Pie · cadus@us.es · Pabellón de Uruguay", fontsize=9, color="white", va="center", zorder=3)
    guardar(fig, f"tematica-{t['clave'].lower()}.png")


def tematicas():
    resultado = []
    for t in TEMATICAS:
        dibujo_tematica(t)
        resultado.append(dict(clave=t["clave"], nombre=t["nombre"], tema=t["tema"], fidelidad=t["fidelidad"],
                              contraste_texto=contraste(t["texto"], t["fondo"]),
                              contraste_banner=contraste(t["hero_txt"], t["hero"]),
                              contraste_boton=contraste(t["boton_txt"], t["boton"]),
                              contraste_tarjetas=min(contraste(a, b) for a, b in zip(t["tarjeta_txt"], t["tarjetas"]))))
    with open(os.path.join(RAIZ, "docs", "entrega", "datos", "tematicas.json"), "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=1)
    print("generado datos/tematicas.json")



# ---------------------------------------------------------------- mockups de la entrega 1 frente al portal implementado
def comparativas_mockups():
    """Une cada mockup de la entrega 1 con la captura de la pantalla implementada (necesita las capturas de capturas_publicas.py)."""
    from PIL import Image, ImageDraw, ImageFont
    pares = [("mockup-01-portada.png", "p01-portada.jpg", (0, 1500), "comparativa-1-portada.png"),
             ("mockup-02-directorio.png", "p05-delegaciones.jpg", None, "comparativa-2-directorio.png"),
             ("mockup-03-buzon.png", "p07-buzon.jpg", None, "comparativa-3-buzon.png"),
             ("mockup-04-acta.png", "p04-actas-y-normativa.jpg", None, "comparativa-4-acta.png")]
    try:
        fuente = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        fuente = ImageFont.load_default()
    for mockup, captura, recorte, salida in pares:
        a = Image.open(os.path.join(IMG, mockup)).convert("RGB")
        b = Image.open(os.path.join(IMG, "capturas2", captura)).convert("RGB")
        if recorte:
            b = b.crop((0, recorte[0], b.width, min(recorte[1], b.height)))
        alto = 720
        a = a.resize((int(a.width * alto / a.height), alto))
        b = b.resize((int(b.width * alto / b.height), alto))
        hoja = Image.new("RGB", (a.width + b.width + 30, alto + 46), "white")
        d = ImageDraw.Draw(hoja)
        d.text((10, 10), "Entrega 1 · mockup de baja fidelidad", fill="#1f3a5f", font=fuente)
        d.text((a.width + 30, 10), "Entrega 2 · portal implementado", fill="#8d0739", font=fuente)
        hoja.paste(a, (0, 46))
        hoja.paste(b, (a.width + 30, 46))
        d.line([(a.width + 15, 46), (a.width + 15, alto + 46)], fill="#888", width=2)
        hoja.save(os.path.join(IMG, salida), quality=92)
        print("generado", salida)



def evolucion_portada():
    """La portada en tres etapas: mockup (entrega 1), primera implementación (Sprint 1) y portal final (Sprint 2)."""
    from PIL import Image, ImageDraw, ImageFont
    try:
        fuente = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        fuente = ImageFont.load_default()
    etapas = [("1 · Mockup (entrega 1)", os.path.join(IMG, "mockup-01-portada.png"), None, "#1f3a5f"),
              ("2 · Primera implementación (Sprint 1)", os.path.join(IMG, "capturas", "09-portada-final.jpg"), None, "#1f3a5f"),
              ("3 · Portal final (Sprint 2)", os.path.join(IMG, "capturas2", "p01-portada.jpg"), (0, 1500), "#8d0739")]
    alto = 640
    ims = []
    for titulo, ruta, recorte, color in etapas:
        im = Image.open(ruta).convert("RGB")
        if recorte:
            im = im.crop((0, recorte[0], im.width, min(recorte[1], im.height)))
        ims.append((titulo, color, im.resize((int(im.width * alto / im.height), alto))))
    ancho = sum(i.width for _, _, i in ims) + 20 * (len(ims) - 1)
    hoja = Image.new("RGB", (ancho, alto + 46), "white")
    d = ImageDraw.Draw(hoja)
    x = 0
    for k, (titulo, color, im) in enumerate(ims):
        d.text((x + 6, 10), titulo, fill=color, font=fuente)
        hoja.paste(im, (x, 46))
        x += im.width + 20
        if k < len(ims) - 1:
            d.text((x - 17, alto // 2 + 30), "›", fill="#888", font=fuente)
    hoja.save(os.path.join(IMG, "evolucion-portada.png"), quality=92)
    print("generado evolucion-portada.png")



# ---------------------------------------------------------------- anexo: evolución del proyecto
def avance_backlog():
    """SP del product backlog por estado y sprint, leídos de docs/scrum/backlog/product-backlog.md."""
    import re
    tot = {"Sprint-00": 0, "Sprint-01": 0, "Sprint-02": 0, "Sprint-03": 0, "Sprint-04": 0, "otros": 0}
    hecho = {k: 0 for k in tot}
    for linea in open(os.path.join(RAIZ, "docs", "scrum", "backlog", "product-backlog.md"), encoding="utf-8"):
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if not re.match(r"^(PB|HU)-\d+$", c[0] if c else ""):
            continue
        if c[0].startswith("PB"):
            sp, estado, sprint = int(c[4]), c[5], c[6]
        else:
            sp, estado, sprint = int(c[4]), c[5], c[6]
        clave = sprint if sprint in tot else "otros"
        tot[clave] += sp
        if estado == "Hecho":
            hecho[clave] += sp
    return tot, hecho


def evolucion_backlog():
    tot, hecho = avance_backlog()
    total = sum(tot.values())
    hechos_s0 = hecho["Sprint-00"]
    hechos_s1 = hecho["Sprint-01"]
    hechos_s2 = hecho["Sprint-02"]
    pendiente = total - hechos_s0 - hechos_s1 - hechos_s2
    fig, ax = plt.subplots(figsize=(10, 3.2), dpi=110)
    partes = [(f"S0 ({hechos_s0} SP)", hechos_s0, "#7a8aa3"), ("Sprint 1 (hecho)", hechos_s1, AZUL), ("Sprint 2 (hecho)", hechos_s2, VERDE), ("Pendiente (Sprints 3 y 4)", pendiente, "#c9ced6")]
    izq = 0
    for nombre, v, color in partes:
        ax.barh(0, v, left=izq, color=color, edgecolor="white", height=0.55)
        if v > 10:
            ax.text(izq + v / 2, 0, f"{v} SP\n{v / total:.0%}", ha="center", va="center", color="white" if color != "#c9ced6" else "#333", fontsize=11, fontweight="bold")
        ax.text(izq + v / 2, 0.52, nombre, ha="center", va="bottom", fontsize=9.5, color="#333")
        izq += v
    ax.set_xlim(0, total)
    ax.set_ylim(-0.6, 1.0)
    ax.set_yticks([])
    ax.set_xlabel(f"Puntos de historia del product backlog (total: {total} SP)")
    ax.set_title("Avance del product backlog al cierre de la entrega 2", fontweight="bold", color=AZUL)
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    fig.savefig(os.path.join(IMG, "evolucion-backlog.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("generado evolucion-backlog.png")


def linea_tiempo():
    hitos = [(dt.date(2026, 9, 28), "Inicio del\nSprint 1", "up"), (dt.date(2026, 10, 5), "Servidor compartido\ncon Tailscale", "down"),
             (dt.date(2026, 10, 18), "Entrega 1\n70 SP", "up"), (dt.date(2026, 10, 19), "Inicio del\nSprint 2", "down"),
             (dt.date(2026, 10, 23), "Calendario,\nmediación y panel", "up"), (dt.date(2026, 10, 24), "Sprint Review\ny votaciones", "down"),
             (dt.date(2026, 10, 25), "Entrega 2\n(Sprints 1 y 2: 99 SP)", "up"), (dt.date(2026, 10, 26), "Sprint 3\n(hasta el 15/11)", "down")]
    fig, ax = plt.subplots(figsize=(11, 5.2), dpi=110)
    inicio = dt.date(2026, 9, 26)
    ax.axhline(0, color=AZUL, lw=3, zorder=1)
    ax.axvspan((dt.date(2026, 9, 28) - inicio).days, (dt.date(2026, 10, 18) - inicio).days + 0.5, ymin=0.46, ymax=0.54, color=AZUL, alpha=0.25)
    ax.axvspan((dt.date(2026, 10, 19) - inicio).days, (dt.date(2026, 10, 25) - inicio).days + 0.5, ymin=0.46, ymax=0.54, color=VERDE, alpha=0.35)
    contador = {"up": 0, "down": 0}
    for k, (fecha, texto, lado) in enumerate(hitos):
        x = (fecha - inicio).days
        contador[lado] += 1
        nivel = 1.0 if contador[lado] % 2 == 1 else 2.15  # etiquetas escalonadas para que no se pisen
        y = nivel if lado == "up" else -nivel
        ax.plot([x, x], [0, y * 0.9], color="#888", lw=1, zorder=1)
        ax.scatter([x], [0], s=60, color=ROJO if "Entrega" in texto else AZUL, zorder=3)
        ax.text(x, y * 0.95, f"{fecha:%d/%m}\n{texto}", ha="center", va="bottom" if lado == "up" else "top", fontsize=8.4)
    ax.set_xlim(-1, (dt.date(2026, 10, 28) - inicio).days)
    ax.set_ylim(-3.6, 3.6)
    ax.axis("off")
    ax.set_title("Línea de tiempo del proyecto (Sprint 1 en azul, Sprint 2 en verde)", fontweight="bold", color=AZUL)
    fig.savefig(os.path.join(IMG, "evolucion-tiempo.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("generado evolucion-tiempo.png")


def comparativas_evolucion():
    """Cada pantalla del Sprint 1 (captura de la entrega 1) junto a la de la entrega 2."""
    from PIL import Image, ImageDraw, ImageFont
    pares = [("10-noticias.jpg", "p03-noticias.jpg", "noticias"), ("11-actas-y-normativa.jpg", "p04-actas-y-normativa.jpg", "actas"),
             ("12-delegaciones.jpg", "p05-delegaciones.jpg", "delegaciones"), ("13-buzon-codigo-ticket.jpg", "p07-buzon.jpg", "buzon"),
             ("14-seguimiento-ticket.jpg", "p08-seguimiento.jpg", "seguimiento"), ("15-admin-tickets.jpg", "20-admin-tickets-filtros.jpg", "tickets"),
             ("17-roles-members.jpg", "a02-roles.jpg", "roles")]
    try:
        fuente = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        fuente = ImageFont.load_default()
    for antes, despues, nombre in pares:
        a = Image.open(os.path.join(IMG, "capturas", antes)).convert("RGB")
        carpeta = "capturas" if despues.startswith("20-") else "capturas2"
        b = Image.open(os.path.join(IMG, carpeta, despues)).convert("RGB")
        b = b.crop((0, 0, b.width, min(b.height, 1150 if despues.startswith("p") else int(b.width * 9 / 16))))  # banner y primer contenido de la página
        a = a.crop((0, 0, a.width, min(a.height, int(a.width * 9 / 16))))
        alto = 620
        a = a.resize((int(a.width * alto / a.height), alto))
        b = b.resize((int(b.width * alto / b.height), alto))
        hoja = Image.new("RGB", (a.width + b.width + 30, alto + 46), "white")
        d = ImageDraw.Draw(hoja)
        d.text((10, 10), "Entrega 1 · Sprint 1", fill="#1f3a5f", font=fuente)
        d.text((a.width + 30, 10), "Entrega 2 · Sprint 2", fill="#8d0739", font=fuente)
        hoja.paste(a, (0, 46))
        hoja.paste(b, (a.width + 30, 46))
        d.line([(a.width + 15, 46), (a.width + 15, alto + 46)], fill="#888", width=2)
        hoja.save(os.path.join(IMG, f"evolucion-{nombre}.png"), quality=92)
        print("generado", f"evolucion-{nombre}.png")



def comparativas_uml():
    """Los UML de la entrega 1 (sacados del historial de Git) junto a los actuales."""
    import io
    import subprocess
    from PIL import Image, ImageDraw, ImageFont
    try:
        fuente = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        fuente = ImageFont.load_default()
    for fichero, salida in (("uml-analisis-estructura-web.png", "evolucion-uml-estructura.png"), ("uml-analisis-clases.png", "evolucion-uml-clases.png"),
                            ("uml-diseno-plugins.png", "evolucion-uml-plugins.png")):
        try:
            primera = subprocess.run(["git", "-C", RAIZ, "log", "--format=%h", "--diff-filter=A", "--", f"docs/entrega/img/{fichero}"], capture_output=True, text=True, check=True).stdout.split()[-1]
            viejo = subprocess.run(["git", "-C", RAIZ, "show", f"{primera}:docs/entrega/img/{fichero}"], capture_output=True, check=True).stdout
            a = Image.open(io.BytesIO(viejo)).convert("RGB")
        except Exception as e:
            print("sin historial para", fichero, e)
            continue
        b = Image.open(os.path.join(IMG, fichero)).convert("RGB")
        ancho = 900
        a = a.resize((ancho, int(a.height * ancho / a.width)))
        b = b.resize((ancho, int(b.height * ancho / b.width)))
        alto = max(a.height, b.height)
        hoja = Image.new("RGB", (2 * ancho + 30, alto + 46), "white")
        d = ImageDraw.Draw(hoja)
        d.text((10, 10), "Entrega 1", fill="#1f3a5f", font=fuente)
        d.text((ancho + 40, 10), "Entrega 2", fill="#8d0739", font=fuente)
        hoja.paste(a, (0, 46))
        hoja.paste(b, (ancho + 30, 46))
        d.line([(ancho + 15, 46), (ancho + 15, alto + 46)], fill="#888", width=2)
        hoja.save(os.path.join(IMG, salida), quality=92)
        print("generado", salida)



def mockup_panel():
    fig, ax = marco("localhost/proyecto_gsi/cms-wordpress/wp-admin/", "UI-08 · RF-14 · RF-15", "Inicio")
    ax.text(30, 150, "Escritorio del CADUS (según el rol)", fontsize=14, fontweight="bold", color=AZUL)
    ax.add_patch(Rectangle((30, 175), 200, 480, fc="#23282d", ec="#23282d"))
    for i, m in enumerate(("Escritorio", "Noticias", "Actas y normativa", "Delegaciones", "Tickets del buzón", "Mediaciones", "Eventos", "Votaciones")):
        ax.text(45, 200 + i * 34, m, fontsize=9.5, color="white" if i else "#ffd54f", va="center", fontweight="bold" if not i else "normal")
    for i, (t, d) in enumerate((("Tickets", "3 pendientes"), ("Mediaciones", "1 pendiente"), ("Actas", "1 por aprobar"), ("Delegaciones", "6 fichas"))):
        bloque(ax, 260 + (i % 2) * 235, 175 + (i // 2) * 120, 220, 105, f"{t}\n{d}", "white", 10.5)
    ax.add_patch(Rectangle((260, 425), 455, 230, fc="#fffbe6", ec=NARANJA, ls="--"))
    ax.text(275, 447, "Menús visibles según el rol (RF-14 · RF-15)", fontsize=10, fontweight="bold")
    ax.text(275, 472, "· Ejecutiva / CADUS: todos los menús del portal\n· Delegado: solo su ficha de delegación (RN-04)\n· Estudiante: sin acceso al panel de administración\n· Las reclamaciones y mediaciones solo las ve la Ejecutiva (RN-03)", fontsize=9, va="top", linespacing=1.8)
    guardar(fig, "mockup-07-panel.png")


if __name__ == "__main__":
    diagrama_clases()
    diagrama_estructura()
    diagrama_plugins()
    mockup_portada()
    mockup_directorio()
    mockup_buzon()
    mockup_acta()
    mockup_calendario()
    mockup_mediacion()
    mockup_panel()
    tematicas()
    comparativas_mockups()
    evolucion_portada()
    evolucion_backlog()
    linea_tiempo()
    comparativas_evolucion()
    comparativas_uml()
    burndowns()
