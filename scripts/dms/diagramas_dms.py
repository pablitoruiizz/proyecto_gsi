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
    rol = clase(ax, 30, 700, W, "Rol", "<<Role>> · RF-D06 · ACT-D01 a ACT-D03", ["nombre (Ejecutiva|Delegado|Estudiante)"])
    doc = clase(ax, 900, 70, W, "Documento", "<<Document>> · IR-D01 · IR-D06 · RF-D02 · RN-D06", ["tipoDocumento", "fecha", "cursoAcademico", "estado"])
    busq = clase(ax, 1500, 70, 360, "Busqueda", "<<Search>> · RF-D04 · RF-D05 · UI-D02", ["texto (nombre y contenido)", "filtros por metadatos (vista plana)"], VERDE)
    acta = clase(ax, 420, 390, W, "Acta", "<<Document>> · IR-D02 · CU-D01 · CU-D02 · RN-D01", ["asamblea", "estadoAprobacion (borrador|aprobada)", "resumen (deseable, RF-D10)"])
    norm = clase(ax, 780, 390, W, "Normativa", "<<Document>> · IR-D03 · CU-D03", ["titulo", "anio", "estado (vigente|derogada)"])
    exp = clase(ax, 1140, 390, W, "Expediente", "<<Document>> · IR-D04 · CU-D04 · CU-D05 · RF-D07 · RN-D02 · RN-D03", ["codigo (CAD-… | MED-…)", "facultad", "fechaResolucion", "fechaCaducidad (calculada)"])
    vot = clase(ax, 1500, 390, W + 20, "RegistroVotacion", "<<Document>> · IR-D05 · CU-D06 · RN-D04 · RN-D05", ["asamblea, numeroVotacion", "tipoVoto (nominal|secreto)", "resultado", "27 filas: presente, identidad", "voto (solo si es nominal)"])
    for sub in (acta, norm, exp, vot):
        rel(ax, sub, "arr", doc, "abj", "")
    ax.text(1070, 300, "es un tipo de", ha="center", fontsize=8.5, bbox=dict(fc="white", ec="none", pad=1.2), zorder=6)
    rel(ax, carp, "der", doc, "izq", "contiene", "1", "*", dy=-18)
    rel(ax, perm, "arr", carp, "abj", "se concede sobre", "*", "1", dx=64, dy=0)
    rel(ax, rol, "arr", perm, "abj", "tiene", "1", "*", dx=40, dy=0)
    rel(ax, busq, "izq", doc, "der", "encuentra", "*", "*", dy=-18)
    ax.text(30, 880, "Los casos de uso CU-D01 a CU-D06 y las reglas RN-D01 a RN-D06 están en REM-DMS.md. Los metadatos (IR-D06) son las columnas de Documento; la vista plana (RF-D05) es la forma de aplicar los filtros.", fontsize=8.5, color="#555")
    guardar(fig, "uml-dms-analisis.png")


def diseno():
    fig, ax = lienzo(1900, 950)
    ax.text(950, 24, "UML de diseño del DMS en SharePoint — del análisis al diseño", ha="center", fontsize=13, fontweight="bold", color=AZUL)
    # sitios
    sitios = [(40, "CADUS Documentación pública", "cadus-documentacion-publica · RF-D01"),
              (700, "CADUS Órganos de gobierno", "cadus-organos-de-gobierno · RF-D01"),
              (1440, "CADUS Atención al estudiante", "cadus-atencion-al-estudiante · RF-D01 · RN-D02")]
    anchos = [560, 700, 430]
    for (x, n, t), w in zip(sitios, anchos):
        caja(ax, x, 70, w, 70, "<<Site>> " + n, t, fc=AZUL, ec=AZUL, subcolor="#ffd2cf", titcolor="white")
    cols_comunes = ["Tipo de documento (elección)", "Fecha (fecha)", "Curso académico (elección)"]
    norm = clase(ax, 40, 230, 560, "<<Library>> Normativa", "IR-D03 · CU-D03 · RF-D05", cols_comunes + ["Estado (vigente|derogada)", "Vista plana «Vigente»: Estado = vigente"])
    actas = clase(ax, 700, 230, 330, "<<Library>> Actas", "IR-D02 · CU-D01 · CU-D02 · RF-D03", cols_comunes + ["Asamblea (texto)", "Estado de aprobación (nativo)", "Resumen (generado, deseable)", "Vista plana «Aprobadas»", "Aprobación de contenido: activada"])
    votac = clase(ax, 1070, 230, 330, "<<Library>> Votaciones", "IR-D05 · CU-D06 · RN-D04 · RN-D05", cols_comunes + ["Asamblea (texto)", "Número de votación (número)", "Tipo de voto (nominal|secreto)", "Resultado (aprobada|rechazada)", "Plantilla: 27 filas por delegación", "Permisos propios: sin visitantes"])
    exp = clase(ax, 1440, 230, 430, "<<Library>> Expedientes", "IR-D04 · CU-D04 · CU-D05 · RF-D07 · RF-D08", cols_comunes + ["Código (texto: CAD-… | MED-…)", "Facultad (elección)", "Fecha de resolución (obligatoria)", "Fecha de caducidad (calculada: +2 años)", "Vista plana «Caducados»: caducidad < hoy", "Sin acceso para visitantes"], NARANJA)
    for (x, _, _), (lib, w) in zip(sitios, ((norm, 0), (actas, 0), (exp, 0))):
        pass
    ax.plot([320, 320], [140, 230], color="#555", lw=1.3, zorder=1)
    ax.plot([865, 865], [140, 230], color="#555", lw=1.3, zorder=1)
    ax.plot([1235, 1235], [140, 150], color="#555", lw=1.3, zorder=1)
    ax.plot([1235, 1235], [150, 230], color="#555", lw=1.3, zorder=1)
    ax.plot([865, 1235], [150, 150], color="#555", lw=1.3, zorder=1)
    ax.plot([1655, 1655], [140, 230], color="#555", lw=1.3, zorder=1)
    # grupos de permisos
    ax.text(40, 525, "Grupos de permisos de cada sitio (RF-D06) y a quién se asignan", fontsize=11.5, fontweight="bold", color=AZUL)
    grupos = [("<<Group>> Propietarios", "control total (r/w)", "Cuenta única del CADUS (dcadus@us.es) y Pablo", AZUL),
              ("<<Group>> Integrantes", "leer y escribir (r/w)", "Equipo del proyecto (4 integrantes), solo con datos de ejemplo", VERDE),
              ("<<Group>> Visitantes", "solo lectura (r)", "Delegados y estudiantes con correo @alum.us.es, según el sitio", NARANJA)]
    for i, (n, nivel, quien, c) in enumerate(grupos):
        x = 40 + i * 610
        caja(ax, x, 555, 570, 110, n + " — " + nivel, quien, fc="white", ec=c, subcolor="#333")
    ax.text(40, 705, "Visitantes por sitio:", fontsize=10, fontweight="bold")
    visit = ["Documentación pública: estudiantes y delegados (lectura de la normativa vigente)",
             "Órganos de gobierno: delegados (solo actas aprobadas; la biblioteca Votaciones tiene permisos propios y no la ven)",
             "Atención al estudiante: nadie (solo la Ejecutiva, RN-D02)"]
    for i, t in enumerate(visit):
        ax.text(60, 730 + 22 * i, "• " + t, fontsize=9.5)
    # tabla análisis -> diseño
    ax.text(40, 830, "Del análisis al diseño", fontsize=11.5, fontweight="bold", color=AZUL)
    mapa = ["Documento → documento con columnas", "Carpeta → sitio o biblioteca", "Rol → grupo de permisos", "Búsqueda y metadatos → búsqueda + vista plana con filtros", "Permiso → permiso del grupo sobre el sitio o la biblioteca"]
    ax.text(60, 857, "   ·   ".join(mapa[:3]), fontsize=9.5)
    ax.text(60, 881, "   ·   ".join(mapa[3:]), fontsize=9.5)
    guardar(fig, "uml-dms-diseno.png")


def casos_de_uso():
    fig, ax = lienzo(1500, 860)
    ax.text(750, 24, "Casos de uso del DMS del CADUS", ha="center", fontsize=13, fontweight="bold", color=AZUL)
    actores = [("Ejecutiva del CADUS", "ACT-D01 · propietario (r/w)", 250), ("Delegado", "ACT-D02 · visitante (r)", 450), ("Estudiante", "ACT-D03 · visitante (r)", 690)]
    pos = {}
    for n, t, y in actores:
        caja(ax, 40, y - 35, 260, 70, n, t)
        pos[n] = (300, y)
    casos = [("CU-D01 Redactar, aprobar y archivar un acta", "Acta · RF-D01, D02, D03, D09", 110, "Ejecutiva del CADUS"),
             ("CU-D02 Consultar las actas aprobadas", "Acta · RF-D03 a D06, D10", 230, "Delegado"),
             ("CU-D03 Consultar la normativa vigente", "Normativa · RF-D04 a D06", 350, "Estudiante"),
             ("CU-D04 Archivar un expediente resuelto", "Expediente · RF-D01, D02, D07", 470, "Ejecutiva del CADUS"),
             ("CU-D05 Retirar los expedientes caducados", "Expediente · RF-D07, D08", 590, "Ejecutiva del CADUS"),
             ("CU-D06 Registrar el resultado de una votación", "Registro de votación · RF-D01, D02, D09", 710, "Ejecutiva del CADUS")]
    for n, t, y, a in casos:
        caja(ax, 760, y - 32, 640, 64, n, t, fc="#eef7ee", ec=VERDE)
        px, py = pos[a]
        ax.plot([px, 760], [py, y], color="#666", lw=1.2, zorder=1)
    # el delegado también consulta la normativa
    px, py = pos["Delegado"]
    ax.plot([px, 760], [py, 350], color="#666", lw=1.2, zorder=1)
    ax.text(40, 830, "Cada tipo de documento tiene al menos un caso de uso; el acta y el expediente tienen dos. El delegado también consulta la normativa (CU-D03).", fontsize=9, color="#555")
    guardar(fig, "casos-de-uso-dms.png")


if __name__ == "__main__":
    analisis()
    diseno()
    casos_de_uso()
