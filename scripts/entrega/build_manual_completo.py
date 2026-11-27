"""Junta los seis manuales (docs/manuales/0N-*.md) en un único documento Word con partes, índice, enlaces internos y anexos de
referencias cruzadas: docs/manuales/entrega/Manuales-CADUS-completo.docx (el PDF se exporta con Microsoft Word).
Uso: python scripts/entrega/build_manual_completo.py"""
import os
import re
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "scripts", "dms"))
sys.path.insert(0, os.path.dirname(__file__))
import build_doc_dms as B  # noqa: E402
import build_manuales as M  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402

TITULO = "Manuales de usuario y de administrador del CADUS"
SUBTITULO = ("Portal web (CMS), gestión documental (DMS) y red social interna (Microsoft Teams) · versión 1.0 · 27/11/2026 · "
             "Grupo de proyecto de GSI, Universidad de Sevilla")
SALIDA = os.path.join(M.ORIGEN, "entrega", "Manuales-CADUS-completo.docx")

# (parte, ancla de la parte, título, [(archivo, ancla del manual, título del manual)])
PARTES = [
    ("Parte I", "parte1", "Portal web del CADUS (CMS)", [
        ("01-manual-usuario-cms.md", "m1u", "Manual de usuario del portal web"),
        ("02-manual-administrador-cms.md", "m1a", "Manual de administrador del portal web")]),
    ("Parte II", "parte2", "Gestión documental del CADUS (DMS, SharePoint)", [
        ("03-manual-usuario-dms.md", "m2u", "Manual de usuario del DMS"),
        ("04-manual-administrador-dms.md", "m2a", "Manual de administrador del DMS")]),
    ("Parte III", "parte3", "Red social interna del CADUS (Microsoft Teams)", [
        ("05-manual-usuario-red-social.md", "m3u", "Manual de usuario de la red social"),
        ("06-manual-administrador-red-social.md", "m3a", "Manual de administrador de la red social")]),
]
NOMBRE = {"m1u": "Parte I, Manual de usuario del portal web", "m1a": "Parte I, Manual de administrador del portal web",
          "m2u": "Parte II, Manual de usuario del DMS", "m2a": "Parte II, Manual de administrador del DMS",
          "m3u": "Parte III, Manual de usuario de la red social", "m3a": "Parte III, Manual de administrador de la red social"}

# referencias entre manuales: (texto de origen, ancla, texto que se muestra). Van de más específica a más general.
REFS = [
    ("(véase el manual de administrador, apartado 4)", "m3a", "(véase la Parte III, Manual de administrador de la red social, apartado 4)"),
    ("(véase el manual de administrador del DMS)", "m2a", "(véase la Parte II, Manual de administrador del DMS)"),
    ("(véase el manual de administrador)", "m2a", "(véase la Parte II, Manual de administrador del DMS, apartado 7)"),
    ("(véase el manual de la red social)", "m3a", "(véase la Parte III, Manual de administrador de la red social)"),
    ("(véase el manual de usuario, CU-D07)", "m2u", "(véase la Parte II, Manual de usuario del DMS, apartado 6)"),
    ("Véase el manual de usuario", "m2u", "Véase la Parte II, Manual de usuario del DMS, apartados 5 y 7"),
    ("(Manual de administrador)", "m1a", "(Parte I, Manual de administrador del portal web)"),
    ("«Manual de administrador del portal»", "m1a", "Parte I, Manual de administrador del portal web"),
    ("«Manual de usuario del portal»", "m1u", "Parte I, Manual de usuario del portal web"),
    ("«Manual de administrador del DMS»", "m2a", "Parte II, Manual de administrador del DMS"),
    ("«Manual de usuario del DMS»", "m2u", "Parte II, Manual de usuario del DMS"),
    ("«Manual de administrador de la red social»", "m3a", "Parte III, Manual de administrador de la red social"),
    ("«Manual de usuario de la red social»", "m3u", "Parte III, Manual de usuario de la red social"),
    ("que tienen sus propios manuales", None, "que tienen sus propios manuales (Partes II y III)"),
]

_id = [100]


def marcar(par, nombre):
    _id[0] += 1
    s = OxmlElement("w:bookmarkStart")
    s.set(qn("w:id"), str(_id[0]))
    s.set(qn("w:name"), nombre)
    e = OxmlElement("w:bookmarkEnd")
    e.set(qn("w:id"), str(_id[0]))
    par._p.insert(1 if par._p.pPr is not None else 0, s)
    par._p.append(e)


def enlace(par, ancla, texto, tam=None):
    h = OxmlElement("w:hyperlink")
    h.set(qn("w:anchor"), ancla)
    h.set(qn("w:history"), "1")
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    c = OxmlElement("w:color")
    c.set(qn("w:val"), "0563C1")
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rpr.append(c)
    rpr.append(u)
    if tam:
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), str(int(tam * 2)))
        rpr.append(sz)
    r.append(rpr)
    t = OxmlElement("w:t")
    t.text = texto
    t.set(qn("xml:space"), "preserve")
    r.append(t)
    h.append(r)
    par._p.append(h)


def con_enlaces(par, texto, enlazar=True):
    """Añade a un párrafo texto con **negrita** y referencias [[ancla|texto]] que son enlaces internos."""
    for x in re.split(r"(\*\*.+?\*\*|\[\[[^|\]]+\|[^\]]+\]\])", texto.replace("`", "")):
        if x.startswith("**") and x.endswith("**"):
            par.add_run(x[2:-2]).bold = True
        elif x.startswith("[["):
            ancla, txt = x[2:-2].split("|", 1)
            enlace(par, ancla, txt) if enlazar else par.add_run(txt)
        elif x:
            par.add_run(x)


def referenciar(texto, enlazar=True):
    """Sustituye las menciones a otros manuales por una referencia concreta (con enlace si se pide)."""
    for origen, ancla, nuevo in REFS:
        if origen in texto:
            texto = texto.replace(origen, f"[[{ancla}|{nuevo}]]" if (ancla and enlazar) else nuevo)
    return texto


def parrafo(doc, texto, cursiva=False, tam=None):
    p = doc.add_paragraph()
    con_enlaces(p, texto)
    for r in p.runs:
        r.italic = cursiva or None
        if tam:
            r.font.size = Pt(tam)
    p.paragraph_format.space_after = Pt(6)
    return p


def vineta(doc, texto):
    p = doc.add_paragraph(style="List Bullet")
    con_enlaces(p, texto)


def numerada(doc, n, texto):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.9)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    p.paragraph_format.space_after = Pt(3)
    p.add_run(f"{n}. ")
    con_enlaces(p, texto)


def tabla_con_enlaces(doc, cabecera, filas, enlaces, anchos=None, titulo=None):
    """enlaces: {(fila, columna): ancla}; la celda mantiene su texto, que pasa a ser un enlace interno."""
    t = B.tabla(doc, cabecera, filas, anchos, titulo=titulo, tam=9)
    for (i, j), ancla in enlaces.items():
        celda = t.rows[i + 1].cells[j]
        txt = celda.text
        for p in celda.paragraphs[1:]:
            p._p.getparent().remove(p._p)
        par = celda.paragraphs[0]
        for r in list(par.runs):
            r._r.getparent().remove(r._r)
        enlace(par, ancla, txt, 9)
    return t


def volcar(doc, ruta, base):
    """Vuelca un manual (sin título ni subtítulo) con sus apartados como títulos de nivel 3 y 4."""
    lineas = open(ruta, encoding="utf-8").read().splitlines()
    i = 1
    empezado = False
    while i < len(lineas):
        l = lineas[i].rstrip()
        img = re.match(r"!\[(.*)\]\((.+)\)$", l.strip())
        if not empezado and not l.startswith("## "):
            i += 1
            continue
        empezado = True
        if not l.strip():
            pass
        elif l.startswith("#### "):
            doc.add_heading(l[5:].strip(), 5)
        elif l.startswith("### "):
            doc.add_heading(l[4:].strip(), 4)
        elif l.startswith("## "):
            doc.add_heading(l[3:].strip(), 3)
        elif img:
            pie, archivo = img.group(1), os.path.normpath(os.path.join(base, img.group(2)))
            if os.path.exists(archivo):
                M.figura(doc, archivo, pie)
            else:
                parrafo(doc, f"[Falta la captura {os.path.basename(archivo)}: {pie}]", cursiva=True)
                B.aviso(f"{os.path.basename(ruta)}: falta la captura {os.path.relpath(archivo, RAIZ)}")
        elif l.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                if not re.match(r"^\|[\s:|-]+\|$", lineas[i].strip()):
                    filas.append(B.celdas(referenciar(lineas[i], enlazar=False)))
                i += 1
            B.tabla(doc, filas[0], filas[1:], tam=9)
            continue
        elif re.match(r"^\d+\. ", l):
            n, texto = l.split(". ", 1)
            numerada(doc, n, referenciar(texto))
        elif re.match(r"^[-*] ", l):
            vineta(doc, referenciar(l[2:]))
        else:
            parrafo(doc, referenciar(l))
        i += 1


def titulo_con_ancla(doc, texto, nivel, ancla):
    h = doc.add_heading(texto, nivel)
    marcar(h, ancla)
    return h


def introduccion(doc):
    titulo_con_ancla(doc, "Cómo usar este documento", 1, "intro")
    parrafo(doc, "El CADUS (Consejo de Alumnos y Estudiantes de la Universidad de Sevilla) trabaja con tres sistemas independientes, "
                 "cada uno con su manual de usuario y su manual de administrador. Este documento los reúne en uno solo: cada parte es un sistema, "
                 "cada sistema tiene sus dos manuales y los anexos finales enlazan unos con otros. Los enlaces azules llevan directamente al apartado; "
                 "el índice también es navegable.")
    doc.add_heading("Qué es cada sistema", 2)
    filas = [
        ["Portal web (CMS)", "Web pública del CADUS en WordPress: noticias, actas, normativa, delegaciones, calendario, votaciones y buzón de consultas y reclamaciones", "Parte I", "Estudiantes, delegaciones, Ejecutiva y administradores"],
        ["Gestión documental (DMS)", "Cuatro sitios de SharePoint con los documentos oficiales: normativa, actas, votaciones y expedientes", "Parte II", "Ejecutiva, delegados y estudiantes (lectura) y administradores"],
        ["Red social interna", "Tres equipos de Microsoft Teams con avisos, calendario, tareas (Planner), formularios y avisos automáticos (Power Automate)", "Parte III", "Ejecutiva, delegaciones y propietarios de los equipos"]]
    tabla_con_enlaces(doc, ["Sistema", "Para qué sirve", "Dónde", "Quién lo usa"], filas,
                      {(0, 2): "parte1", (1, 2): "parte2", (2, 2): "parte3"}, [3.2, 7.2, 1.8, 4.8])
    doc.add_heading("Qué manual te toca", 2)
    filas = [
        ["Soy estudiante y quiero consultar algo o enviar una consulta al CADUS", "Parte I, Manual de usuario del portal web"],
        ["Soy una delegación de centro", "Parte I (portal), Parte II (documentos) y Parte III (Teams), manuales de usuario"],
        ["Soy de la Ejecutiva del CADUS", "Manuales de usuario de las tres partes"],
        ["Instalo, mantengo o recupero el portal", "Parte I, Manual de administrador del portal web"],
        ["Administro los sitios de SharePoint", "Parte II, Manual de administrador del DMS"],
        ["Administro los equipos de Teams, Planner, Power Automate o Power Apps", "Parte III, Manual de administrador de la red social"]]
    enl = {(0, 1): "m1u", (3, 1): "m1a", (4, 1): "m2a", (5, 1): "m3a"}
    tabla_con_enlaces(doc, ["Si…", "Lee"], filas, enl, [8, 9])
    parrafo(doc, "La Ejecutiva y las delegaciones usan los tres manuales de usuario: [[m1u|portal web]], [[m2u|DMS]] y [[m3u|red social]].")
    doc.add_heading("Convenciones", 2)
    for t in ("Los nombres de botones, menús y campos van en **negrita**; las rutas de menús usan «›» (por ejemplo, **Delegaciones › Relevo de la cuenta**).",
              "Las referencias a otro manual indican la parte y el manual (por ejemplo, «Parte II, Manual de usuario del DMS, apartado 6»); el número de apartado es el del manual citado.",
              "Las capturas son del entorno real del equipo con datos de ejemplo y cuentas del equipo que representan a una delegación o a la Ejecutiva.",
              "Estado: documento a 27/11/2026. Lo que no se ha podido comprobar está dicho en cada manual y recogido en el [[anexoD|anexo D]]."):
        vineta(doc, t)
    doc.add_page_break()


def anexos(doc):
    titulo_con_ancla(doc, "Anexo A. Dónde está cada tarea", 1, "anexoA")
    parrafo(doc, "Tarea habitual, quién la hace y el manual donde se explica (el enlace lleva al manual; el apartado se indica en la tercera columna).")
    T = [
        ("Enviar una consulta o reclamación al CADUS", "Estudiante", "m1u", "Apartado 4"),
        ("Consultar el estado de un ticket o pedir una mediación", "Estudiante", "m1u", "Apartado 5"),
        ("Editar la ficha de mi delegación", "Delegación", "m1u", "Apartado 6.2"),
        ("Pasar la cuenta de la delegación al equipo nuevo (relevo)", "Delegación o Ejecutiva", "m1u", "Apartado 6.3; técnico: Manual de administrador del portal, 4.4"),
        ("Publicar una noticia, un evento o un acta en el portal", "Ejecutiva", "m1u", "Apartados 7.2 a 7.4"),
        ("Atender los tickets y las mediaciones", "Ejecutiva", "m1u", "Apartado 7.6"),
        ("Convocar una votación en el portal", "Ejecutiva", "m1u", "Apartado 7.5; técnico: Manual de administrador del portal, 5.3"),
        ("Instalar, restaurar o actualizar el portal", "Administrador", "m1a", "Apartados 3, 6.3 y 6.5"),
        ("Dar de alta las cuentas de las delegaciones por lotes", "Administrador", "m1a", "Apartado 4.3"),
        ("Consultar la normativa vigente y las actas aprobadas", "Estudiante o delegado", "m2u", "Apartados 3 y 4"),
        ("Redactar y aprobar un acta", "Ejecutiva", "m2u", "Apartado 5"),
        ("Publicar una nueva versión de una norma", "Ejecutiva", "m2u", "Apartado 6"),
        ("Registrar una votación presencial", "Ejecutiva", "m2u", "Apartado 7"),
        ("Archivar y retirar expedientes", "Ejecutiva", "m2u", "Apartado 8; técnico: Manual de administrador del DMS, 5"),
        ("Dar permisos a alguien en SharePoint", "Administrador", "m2a", "Apartado 3.3"),
        ("Leer avisos, ver el calendario y mis tareas", "Delegación", "m3u", "Apartado 3"),
        ("Publicar un aviso y preparar una asamblea", "Ejecutiva", "m3u", "Apartados 4.1 y 4.2"),
        ("Dar de alta o de baja una delegación en Teams", "Propietario del equipo", "m3a", "Apartado 4"),
        ("Crear planes de Planner, flujos de Power Automate y la aplicación de Power Apps", "Propietario del equipo", "m3a", "Apartados 6, 7 y 8"),
        ("Traspasar la red social a la Ejecutiva", "Propietario del equipo", "m3a", "Apartado 9"),
    ]
    filas = [[a, q, NOMBRE[ancla], d] for a, q, ancla, d in T]
    tabla_con_enlaces(doc, ["Tarea", "Quién", "Manual", "Dónde"], filas, {(i, 2): t[2] for i, t in enumerate(T)}, [6, 2.8, 4.8, 3.4])

    titulo_con_ancla(doc, "Anexo B. Cómo se relacionan los tres sistemas", 1, "anexoB")
    filas = [
        ["Tickets y expedientes", "Cuando la Ejecutiva resuelve un ticket del portal (`CAD-…`) o una mediación (`MED-…`), archiva el expediente en el DMS, que lo conserva dos años y lo retira. El portal anonimiza el ticket a los dos años por su cuenta.", "Parte I, 7.6 y 6.4 · Parte II, 8"],
        ["Actas", "El portal publica las actas con su PDF para el público; el DMS guarda el acta con su aprobación y la ven los delegados solo cuando está aprobada. Es la misma regla de negocio en los dos sistemas.", "Parte I, 7.4 · Parte II, 5"],
        ["Documentos en Teams", "Los canales enlazan los sitios del DMS con una pestaña; los documentos no se copian a Teams y los permisos los siguen dando los sitios de SharePoint.", "Parte III, 3.3 y 5 · Parte II, 3"],
        ["Cuentas", "El portal usa una cuenta por delegación (correo institucional de la delegación) y la cuenta única de la Ejecutiva. Teams y SharePoint usan cuentas de la Universidad de Sevilla.", "Parte I, 4.1 · Parte II, 3.1 · Parte III, 3.2"],
        ["Privacidad", "Los tickets y las mediaciones son privados en el portal; los expedientes y las votaciones solo los ve la Ejecutiva en el DMS; nada de eso se escribe en Teams.", "Parte I, 7 · Parte II, 3.2 · Parte III, 5"]]
    enl = {(0, 2): "m1u", (1, 2): "m1u", (2, 2): "m3u", (3, 2): "m1a", (4, 2): "m2a"}
    tabla_con_enlaces(doc, ["Relación", "Qué ocurre", "Dónde"], filas, enl, [3, 10, 4])

    titulo_con_ancla(doc, "Anexo C. Cuentas y accesos", 1, "anexoC")
    filas = [
        ["Portal web", "Estudiante", "No necesita cuenta", "Manual de usuario, 1"],
        ["Portal web", "Delegación", "Cuenta de la delegación (correo institucional); entra por **Acceder**", "Manual de usuario, 6.1"],
        ["Portal web", "Ejecutiva", "Cuenta única `cadus` (correo del CADUS)", "Manual de usuario, 7.1 · Manual de administrador, 4.1"],
        ["Portal web", "Administración", "Cuentas de administrador del equipo", "Manual de administrador, 4"],
        ["DMS", "Estudiante y delegado", "Correo `@alum.us.es` (estudiante) o cuenta de la delegación (delegado), como visitantes; aún sin crear", "Manual de usuario, 1 · Manual de administrador, 7"],
        ["DMS", "Ejecutiva y administración", "Propietarios de los sitios (hoy, el equipo del proyecto; la cuenta del CADUS está pendiente de añadir)", "Manual de administrador, 3.1 y 7"],
        ["Red social", "Delegación", "Cuenta de la Universidad, como miembro del equipo y de su canal privado", "Manual de usuario, 3 · Manual de administrador, 3.2"],
        ["Red social", "Ejecutiva y propietarios", "Cuenta de la Universidad, como propietaria de los tres equipos", "Manual de administrador, 3.2 y 9"]]
    tabla_con_enlaces(doc, ["Sistema", "Quién", "Cómo accede", "Dónde se explica"], filas, {}, [2.4, 3, 7.2, 4.4])

    titulo_con_ancla(doc, "Anexo D. Estado, pendientes y límites a 27/11/2026", 1, "anexoD")
    parrafo(doc, "Resumen de lo que **no** se ha podido comprobar o queda por hacer. El detalle está en el apartado de pendientes y límites de cada manual de administrador.")
    filas = [
        ["Portal web", "Despliegue en la Universidad de Sevilla", "Sin hacer: el servidor estudiado tenía PHP 7.2/7.3. Pendiente de la respuesta de la Universidad"],
        ["Portal web", "Correo saliente real", "Los avisos salen por SMTP y un correo de prueba llegó a una bandeja de Gmail; los cuatro avisos enviados a una dirección @alum.us.es llegaron con 65 a 70 minutos de retraso, por el filtro de la Universidad"],
        ["Portal web", "Anonimización a los dos años", "Probada con datos de ejemplo; no comprobada en el servidor del equipo"],
        ["Portal web", "Accesibilidad con lector de pantalla", "Probado con el Narrador de Windows; NVDA probado el 27/11 según Pablo, sin registro paso a paso"],
        ["DMS", "Cuenta del CADUS como propietaria", "Pendiente en los cuatro sitios"],
        ["DMS", "Cuentas de delegado y de estudiante", "No existen; los permisos no se han probado con cuentas reales de esos roles. Pendiente de la respuesta de la Universidad de Sevilla"],
        ["Red social", "Aplicación de Power Apps", "Publicada según Álvaro (27/11), sin captura ni comprobación de otra persona; no consta que esté integrada en Teams"],
        ["Red social", "Planes de la Ejecutiva y de las delegaciones", "Capturados el 27/11/2026; sin prueba de otra persona"],
        ["Red social", "Cuentas de delegación reales", "No existen en Teams: es un piloto con datos de ejemplo"]]
    enl = {(0, 0): "m1a", (1, 0): "m1a", (2, 0): "m1a", (3, 0): "m1a", (4, 0): "m2a", (5, 0): "m2a", (6, 0): "m3a", (7, 0): "m3a", (8, 0): "m3a"}
    tabla_con_enlaces(doc, ["Sistema", "Asunto", "Estado"], filas, enl, [3, 5.5, 8.5])

    titulo_con_ancla(doc, "Anexo E. Glosario", 1, "anexoE")
    filas = [
        ["CADUS", "Consejo de Alumnos y Estudiantes de la Universidad de Sevilla"],
        ["Ejecutiva", "Órgano de gobierno del CADUS; entra en el portal con su cuenta única"],
        ["Delegación de centro", "Representación de los estudiantes de una facultad o escuela; hay 27, cada una con una cuenta"],
        ["Ticket", "Consulta o reclamación enviada por un estudiante al buzón del portal; tiene un código `CAD-…`"],
        ["Mediación", "Solicitud de un estudiante para que el CADUS medie en un conflicto; tiene una referencia `MED-…`"],
        ["Expediente", "Documento que queda en el DMS de un ticket o una mediación resueltos"],
        ["CMS", "Sistema de gestión de contenidos; aquí, el portal web en WordPress"],
        ["DMS", "Sistema de gestión documental; aquí, los sitios de SharePoint"],
        ["Plan, cubo, tarea", "En Planner, un plan agrupa tareas en cubos (en Teams, depósitos); cada tarea tiene responsable y fecha límite"],
        ["Propietario y miembro", "Roles de un equipo de Teams: el propietario administra el equipo; el miembro participa"],
        ["Tenant", "Entorno de Microsoft 365 de la Universidad de Sevilla donde están Teams y SharePoint"]]
    B.tabla(doc, ["Término", "Significado"], filas, [4, 13], tam=9)


def main():
    B.AVISOS.clear()
    doc = B.nuevo()
    B.Num.fig = 0
    B.Num.tab = 0
    M.pie_pagina(doc, TITULO)
    doc.add_heading(TITULO, 0)
    parrafo(doc, SUBTITULO, cursiva=True, tam=10)
    parrafo(doc, "**Contenido**", tam=12)
    toc = doc.add_paragraph()
    M.campo(toc, 'TOC \\o "1-3" \\h \\z \\u')
    doc.add_page_break()
    introduccion(doc)
    for parte, ancla_p, titulo_p, manuales in PARTES:
        titulo_con_ancla(doc, f"{parte}. {titulo_p}", 1, ancla_p)
        for archivo, ancla_m, titulo_m in manuales:
            titulo_con_ancla(doc, titulo_m, 2, ancla_m)
            volcar(doc, os.path.join(M.ORIGEN, archivo), M.ORIGEN)
        doc.add_page_break()
    anexos(doc)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    doc.save(SALIDA)
    print("docx:", os.path.relpath(SALIDA, RAIZ))
    for a in B.AVISOS:
        print("AVISO:", a)


if __name__ == "__main__":
    main()
