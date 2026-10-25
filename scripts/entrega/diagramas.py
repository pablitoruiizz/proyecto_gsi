"""Genera los diagramas, mockups y el burndown de la entrega. Uso: python scripts/entrega/diagramas.py"""
import csv
import datetime as dt
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
    solic = clase(ax, cx[0], ry[2], W, "SolicitudMediacion", "IR-08 · RF-13 · RN-02 · RN-03 · UI-07", ["referencia", "descripcionConflicto", "fechaSolicitud", "estado (pendiente|cerrada)"], VERDE)
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
           ("Yoast SEO", "SEO: metadatos, sitemap y contenido", "RF-01 · RF-02 · UI-02 · OBJ-02")]
    for i, (n, f, t) in enumerate(obl):
        _, y = plugin(40, 95 + i * 98, n, f, t)
        ax.plot([420, 470], [y + 41, 395], color="#888", lw=1.1, zorder=1)

    ax.text(1140, 70, "Plugins funcionales (instalados)", fontsize=11, fontweight="bold", color=VERDE)
    fun = [("Advanced Custom Fields", "Campos de actas y delegaciones", "RF-03 · RF-04 · RF-06 · RF-07 · RF-15"),
           ("Fluent Forms", "Formularios: buzón y mediación", "RF-08 · RF-09 · RF-13 · RN-02 · RNF-04"),
           ("Members", "Roles y permisos (Ejecutiva, Delegado, Estudiante)", "RF-05 · RF-14 · RN-01 · RN-03 · RN-04"),
           ("The Events Calendar", "Calendario de asambleas y eventos (HU-10)", "RF-11 · RF-12 · RN-05 · UI-06")]
    for i, (n, f, t) in enumerate(fun):
        _, y = plugin(1140, 95 + i * 98, n, f, t)
        ax.plot([1140, 1090], [y + 41, 395], color="#888", lw=1.1, zorder=1)

    ax.text(590, 505, "Plugin propio del equipo (instalado)", fontsize=11, fontweight="bold", color=AZUL)
    plugin(590, 520, "CADUS Portal", "Roles, buzón, mediación, votaciones", "RF-01 a RF-15 · RN-01 a RN-05 · UI-01 a UI-08")
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
    burndowns()
