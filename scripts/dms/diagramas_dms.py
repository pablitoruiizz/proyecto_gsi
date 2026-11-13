"""Genera los diagramas del DMS (análisis, diseño y casos de uso) en docs/dms/img.
Reutiliza los dibujos de scripts/entrega/diagramas.py. Uso: python scripts/dms/diagramas_dms.py"""
import os
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "scripts", "entrega"))
import diagramas as D  # noqa: E402

D.IMG = os.path.join(RAIZ, "docs", "dms", "img")
os.makedirs(D.IMG, exist_ok=True)
lienzo, clase, rel, caja, guardar = D.lienzo, D.clase, D.rel, D.caja, D.guardar
AZUL, VERDE, NARANJA, ROJO, AZUL_CLARO = D.AZUL, D.VERDE, D.NARANJA, D.ROJO, D.AZUL_CLARO


def analisis():
    fig, ax = lienzo(1900, 900)
    ax.text(950, 24, "UML de análisis del DMS del CADUS — etiquetas de trazabilidad en rojo", ha="center", fontsize=13, fontweight="bold", color=AZUL)
    W = 340
    carp = clase(ax, 30, 70, W, "Carpeta", "<<Folder>> · RF-D01 · RF-D06", ["nombre (Actas, Normativa,", "   Expedientes, Votaciones)"], VERDE)
    perm = clase(ax, 30, 390, W, "Permiso", "<<Permission>> · RF-D06 · RF-D03 · RN-D01 · RN-D02", ["nivel (leer | leer y escribir)", "sobre una carpeta"], VERDE)
    rol = clase(ax, 30, 700, W, "Rol", "<<Role>> · RF-D06 · ACT-D01 a ACT-D03", ["nombre (Ejecutiva|Delegado|Estudiante)", "cuenta (CADUS|delegación|@alum.us.es)"])
    doc = clase(ax, 900, 70, W, "Documento", "<<Document>> · IR-D01 · IR-D06 · RF-D02 · RN-D06", ["tipoDocumento", "fecha", "cursoAcademico", "estado"])
    busq = clase(ax, 1500, 70, 360, "Busqueda", "<<Search>> · RF-D04 · RF-D05 · UI-D02", ["texto (nombre y contenido)", "filtros por metadatos (vista plana)"], VERDE)
    acta = clase(ax, 420, 390, W, "Acta", "<<Document>> · IR-D02 · CU-D01 · CU-D02 · RN-D01", ["asamblea", "estadoAprobacion (borrador|aprobada)", "resumen (deseable, RF-D10)"])
    norm = clase(ax, 780, 390, W, "Normativa", "<<Document>> · IR-D03 · CU-D03 · CU-D07 · RN-D07", ["titulo", "norma (identifica la misma norma)", "version, anio", "estado (vigente|derogada)"])
    exp = clase(ax, 1140, 390, W, "Expediente", "<<Document>> · IR-D04 · CU-D04 · CU-D05 · RF-D07 · RN-D02 · RN-D03", ["codigo (CAD-… | MED-…)", "facultad", "fechaResolucion", "fechaCaducidad (calculada)"])
    vot = clase(ax, 1500, 390, W + 20, "RegistroVotacion", "<<Document>> · IR-D05 · CU-D06 · CU-D08 · RN-D04 · RN-D05", ["asamblea, numeroVotacion (obligatorios)", "tipoVoto (nominal|secreto)", "resultado", "27 filas: presente, identidad", "voto (solo si es nominal)"])
    for sub in (acta, norm, exp, vot):
        rel(ax, sub, "arr", doc, "abj", "")
    ax.text(1070, 300, "es un tipo de", ha="center", fontsize=8.5, bbox=dict(fc="white", ec="none", pad=1.2), zorder=6)
    rel(ax, carp, "der", doc, "izq", "contiene", "1", "*", dy=-18)
    rel(ax, perm, "arr", carp, "abj", "se concede sobre", "*", "1", dx=64, dy=0)
    rel(ax, rol, "arr", perm, "abj", "tiene", "1", "*", dx=40, dy=0)
    rel(ax, busq, "izq", doc, "der", "encuentra", "*", "*", dy=-18)
    ax.text(30, 880, "Los casos de uso CU-D01 a CU-D08 y las reglas RN-D01 a RN-D07 están en REM-DMS.md. Los metadatos (IR-D06) son las columnas de Documento; la vista plana (RF-D05) es la forma de aplicar los filtros.", fontsize=8.5, color="#555")
    guardar(fig, "uml-dms-analisis.png")


def diseno():
    """UML de diseño con los estereotipos de la diapositiva 3 del Lab 4: <<Site>>, <<Folder>>, <<Document>>, <<Role>>, <<Permission>>
    y <<Filter>> (la búsqueda del análisis pasa a ser un filtro de metadatos sobre una vista plana)."""
    fig, ax = lienzo(1900, 1290)
    ax.text(950, 24, "UML de diseño del DMS en SharePoint — del análisis al diseño", ha="center", fontsize=13, fontweight="bold", color=AZUL)
    # sitios
    sitios = [(40, "Documentación pública", "cadus-documentacion-publica · RF-D01"),
              (700, "Órganos de gobierno", "cadus-organos-de-gobierno"),
              (1070, "Votaciones", "cadus-votaciones · RN-D04"),
              (1440, "Atención al estudiante", "cadus-atencion-al-estudiante · RN-D02")]
    anchos = [560, 330, 330, 430]
    for (x, n, t), w in zip(sitios, anchos):
        caja(ax, x - 10, 70, w + 20, 70, "<<Site>> " + n, t, fc=AZUL, ec=AZUL, subcolor="#ffd2cf", titcolor="white")
    cols_comunes = ["<<Document>> con estas columnas:", "Tipo de documento (elección)", "Fecha (fecha)", "Curso académico (elección)"]
    norm = clase(ax, 40, 230, 560, "<<Folder>> Normativa", "IR-D03 · CU-D03 · CU-D07 · RF-D05", cols_comunes + ["Norma (texto: identifica la norma)", "Versión (número)", "Estado (vigente|derogada)", "Una versión vigente por norma (RN-D07)"])
    actas = clase(ax, 700, 230, 330, "<<Folder>> Actas", "IR-D02 · CU-D01 · CU-D02 · RF-D03", cols_comunes + ["Asamblea (texto)", "Estado de aprobación (nativo)", "Resumen (generado, deseable)", "Aprobación de contenido: activada"])
    votac = clase(ax, 1070, 230, 330, "<<Folder>> Votaciones", "IR-D05 · CU-D06 · CU-D08 · RN-D04 · RN-D05", cols_comunes + ["Asamblea (texto, obligatoria)", "Número de votación (obligatorio)", "Tipo de voto (nominal|secreto)", "Resultado (aprobada|rechazada)", "Plantilla: 27 filas por delegación"])
    exp = clase(ax, 1440, 230, 430, "<<Folder>> Expedientes", "IR-D04 · CU-D04 · CU-D05 · RF-D07 · RF-D08", cols_comunes + ["Código (texto: CAD-… | MED-…)", "Facultad (elección)", "Fecha de resolución (obligatoria)", "Fecha de caducidad (calculada: +2 años)"], NARANJA)
    for x in (320, 865, 1235, 1655):
        ax.plot([x, x], [140, 230], color="#555", lw=1.3, zorder=1)
    # filtros: la búsqueda por metadatos son vistas planas con filtros (diapositivas 2 y 4 del Lab 4)
    ax.text(40, 545, "Búsqueda por metadatos: vista plana de la carpeta con filtros (tipo de documento y otro metadato)", fontsize=11.5, fontweight="bold", color=AZUL)
    filtros = [(40, 560, "<<Filter>> Vigente", "Normativa · Estado = Vigente · RF-D05 · UI-D02", norm),
               (700, 330, "<<Filter>> Aprobadas", "Acta · Aprobación = Aprobado · RF-D05", actas),
               (1070, 330, "<<Filter>> Asamblea y voto", "Votación · CU-D08", votac),
               (1440, 430, "<<Filter>> Caducados", "Expediente · Fecha de caducidad < hoy · RF-D08", exp)]
    for x, w, tit, sub, carpeta in filtros:
        caja(ax, x, 580, w, 62, tit, sub, fc="#eef7ee", ec=VERDE, subcolor="#333")
        rel(ax, carpeta, "abj", (x, 580, w, 62), "arr", "", dy=0)
    ax.text(40, 668, "Búsqueda genérica (RF-D04): la de SharePoint, por nombre y por contenido del archivo, sobre todo el sitio.", fontsize=9.5, color="#333")
    # roles y permisos: grupos predefinidos de SharePoint
    ax.text(40, 715, "Roles y permisos (RF-D06): grupos predefinidos de SharePoint, concedidos sobre el sitio", fontsize=11.5, fontweight="bold", color=AZUL)
    roles = [("<<Role>> Propietario", "Cuenta única del CADUS (dcadus@us.es) y Pablo", AZUL),
             ("<<Role>> Integrante", "Equipo del proyecto (4 integrantes), solo con datos de ejemplo", VERDE),
             ("<<Role>> Visitante", "Delegados (cuenta de su delegación) y estudiantes (@alum.us.es)", NARANJA)]
    for i, (n, quien, c) in enumerate(roles):
        caja(ax, 40 + i * 610, 740, 570, 70, n, quien, fc="white", ec=c, subcolor="#333")
    caja(ax, 160, 880, 700, 64, "<<Permission>> Read/write", "leer y escribir · Propietario e Integrante · concedido sobre cada <<Site>>", fc="#fff7ea", ec=NARANJA, subcolor="#333")
    caja(ax, 1010, 880, 700, 64, "<<Permission>> Read", "solo lectura · Visitante · concedido sobre el <<Site>> (Votaciones y Atención: sin visitantes)", fc="#fff7ea", ec=NARANJA, subcolor="#333")
    ax.plot([325, 510], [810, 880], color="#555", lw=1.3, zorder=1)
    ax.plot([935, 510], [810, 880], color="#555", lw=1.3, zorder=1)
    ax.plot([1545, 1360], [810, 880], color="#555", lw=1.3, zorder=1)
    ax.text(40, 975, "Visitantes por sitio:", fontsize=10, fontweight="bold")
    visit = ["Documentación pública: estudiantes y delegados (lectura de la normativa vigente)",
             "Órganos de gobierno: delegados (solo actas aprobadas)",
             "Votaciones: nadie (solo la Ejecutiva, RN-D04); sitio propio para no romper la herencia de permisos de una biblioteca",
             "Atención al estudiante: nadie (solo la Ejecutiva, RN-D02); la biblioteca Expedientes conserva además permisos propios"]
    for i, t in enumerate(visit):
        ax.text(60, 1000 + 22 * i, "• " + t, fontsize=9.5)
    # tabla análisis -> diseño (diapositiva 2 del Lab 4)
    ax.text(40, 1112, "Del análisis al diseño", fontsize=11.5, fontweight="bold", color=AZUL)
    mapa = ["<<Document>> → <<Document>> (con columnas de metadatos)", "<<Folder>> → <<Site>> / <<Folder>> (los sitios asignan permisos de golpe)", "<<Role>> → <<Role>> (Propietario, Integrante, Visitante)",
            "<<Search>> → búsqueda genérica + <<Filter>> por metadatos en una vista plana", "Metadato → columna de la biblioteca (el Lab 4 las asocia al Site; en SharePoint viven en cada biblioteca)", "<<Permission>> → Read/write o Read sobre el sitio, por grupo"]
    for i in range(3):
        ax.text(60, 1140 + 24 * i, "   ·   ".join(mapa[2 * i:2 * i + 2]), fontsize=9.5)
    guardar(fig, "uml-dms-diseno.png")


def casos_de_uso():
    fig, ax = lienzo(1500, 880)
    ax.text(750, 24, "Casos de uso del DMS del CADUS", ha="center", fontsize=13, fontweight="bold", color=AZUL)
    actores = [("Ejecutiva del CADUS", "ACT-D01 · propietario (r/w)", 330), ("Delegado", "ACT-D02 · visitante (r) · de la delegación", 520), ("Estudiante", "ACT-D03 · visitante (r) · @alum.us.es", 700)]
    pos = {}
    for n, t, y in actores:
        caja(ax, 20, y - 35, 340, 70, n, t)
        pos[n] = (360, y)
    casos = [("CU-D01 Redactar, aprobar y archivar un acta", "Acta · RF-D01, D02, D03, D09", 100, "Ejecutiva del CADUS"),
             ("CU-D02 Consultar las actas aprobadas", "Acta · RF-D03 a D06, D10", 190, "Delegado"),
             ("CU-D03 Consultar la normativa vigente", "Normativa · RF-D04 a D06", 280, "Estudiante"),
             ("CU-D04 Archivar un expediente resuelto", "Expediente · RF-D01, D02, D07", 370, "Ejecutiva del CADUS"),
             ("CU-D05 Retirar los expedientes caducados", "Expediente · RF-D07, D08", 460, "Ejecutiva del CADUS"),
             ("CU-D06 Registrar el resultado de una votación", "Registro de votación · RF-D01, D02, D09", 550, "Ejecutiva del CADUS"),
             ("CU-D07 Publicar una versión nueva de una norma", "Normativa · RF-D02, D05, D06, RN-D07", 640, "Ejecutiva del CADUS"),
             ("CU-D08 Consultar los registros de votaciones", "Registro de votación · RF-D05, D06, RN-D04, D05", 730, "Ejecutiva del CADUS")]
    for n, t, y, a in casos:
        caja(ax, 760, y - 32, 640, 64, n, t, fc="#eef7ee", ec=VERDE)
        px, py = pos[a]
        ax.plot([px, 760], [py, y], color="#666", lw=1.2, zorder=1)
    # el delegado también consulta la normativa
    px, py = pos["Delegado"]
    ax.plot([px, 760], [py, 280], color="#666", lw=1.2, zorder=1)
    ax.text(40, 850, "Cada tipo de documento tiene dos casos de uso (ocho en total). El delegado también consulta la normativa (CU-D03).", fontsize=9, color="#555")
    guardar(fig, "casos-de-uso-dms.png")


if __name__ == "__main__":
    analisis()
    diseno()
    casos_de_uso()
