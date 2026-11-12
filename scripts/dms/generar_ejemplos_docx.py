"""Genera los documentos Word de ejemplo del DMS (ficticios, sin datos personales ni DNI) como .docx válidos y mínimos.

Los de la carga del 30/10/2026 se subieron mal por la API de SharePoint: pesaban 2 bytes (el contenido era literalmente «{}») y no se
abrían ni en Word en línea ni en la vista previa. Este script crea los archivos correctos, los valida abriéndolos con python-docx y
escribe un JSON con su contenido en base64 para subirlos de nuevo (ver docs/dms/entorno-sharepoint.md).
Uso:  python scripts/dms/generar_ejemplos_docx.py <carpeta de salida>
"""
import base64, io, json, os, random, sys, zipfile
from xml.sax.saxutils import escape

import docx  # python-docx, solo para comprobar que los archivos se abren

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DELEGACIONES = [d["centro"] for d in json.load(open(os.path.join(RAIZ, "cms-wordpress", "wp-content", "plugins", "cadus-portal", "data", "delegaciones.json"), encoding="utf-8"))]
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def p(texto, negrita=False, tam=None, centrado=False, color=None):
    ppr = '<w:pPr><w:jc w:val="center"/></w:pPr>' if centrado else ""
    rpr = ("<w:b/>" if negrita else "") + (f'<w:color w:val="{color}"/>' if color else "") + (f'<w:sz w:val="{tam}"/>' if tam else "")
    return f'<w:p>{ppr}<w:r>{"<w:rPr>" + rpr + "</w:rPr>" if rpr else ""}<w:t xml:space="preserve">{escape(texto)}</w:t></w:r></w:p>'


def tabla(cabecera, filas, anchos):
    borde = '<w:tblBorders>' + "".join(f'<w:{l} w:val="single" w:sz="4" w:space="0" w:color="808080"/>' for l in ("top", "left", "bottom", "right", "insideH", "insideV")) + '</w:tblBorders>'
    def celda(t, w, neg=False, sombra=False):
        sh = '<w:shd w:val="clear" w:color="auto" w:fill="E7E6E6"/>' if sombra else ""
        return f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{sh}</w:tcPr>{p(t, negrita=neg, tam=20)}</w:tc>'
    xml = f'<w:tbl><w:tblPr><w:tblW w:w="{sum(anchos)}" w:type="dxa"/>{borde}</w:tblPr><w:tblGrid>' + "".join(f'<w:gridCol w:w="{w}"/>' for w in anchos) + "</w:tblGrid>"
    xml += "<w:tr>" + "".join(celda(c, w, True, True) for c, w in zip(cabecera, anchos)) + "</w:tr>"
    for f in filas:
        xml += "<w:tr>" + "".join(celda(c, w) for c, w in zip(f, anchos)) + "</w:tr>"
    return xml + "</w:tbl>" + p("")


def docx_bytes(cuerpo_xml, titulo):
    doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="{W}"><w:body>{cuerpo_xml}'
           '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>')
    tipos = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
             '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
             '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
             '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>')
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{escape(titulo)}</dc:title><dc:creator>CADUS (documento de ejemplo)</dc:creator></cp:coreProperties>')
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("[Content_Types].xml", tipos)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc)
        z.writestr("docProps/core.xml", core)
    return b.getvalue()


AVISO = p("Documento ficticio de ejemplo para probar el DMS del CADUS. No contiene datos reales ni personales.", tam=18, color="7F7F7F")


def votacion(num, asamblea, fecha, tipo, resultado, semilla):
    rnd = random.Random(semilla)
    presentes = [rnd.random() > 0.15 for _ in DELEGACIONES]
    votos = [rnd.choice(["Sí", "Sí", "No", "Abstención"]) if pr else "" for pr in presentes]
    cuerpo = p(f"Registro de votación n.º {num}", True, 32) + p(f"Asamblea: {asamblea}") + p(f"Fecha: {fecha}") + p(f"Tipo de voto: {tipo}") + p(f"Resultado: {resultado}") + AVISO
    if tipo == "Nominal":
        filas = [[d, "Presente" if pr else "Ausente", "Sí" if pr else "—", v or "—"] for d, pr, v in zip(DELEGACIONES, presentes, votos)]
        cuerpo += p("Voto de cada delegación (una delegación, un voto)", True) + tabla(["Delegación", "Asistencia", "Identidad comprobada", "Voto"], filas, [4200, 1500, 2100, 1500])
    else:
        filas = [[d, "Presente" if pr else "Ausente", "Sí" if pr else "—"] for d, pr in zip(DELEGACIONES, presentes)]
        si, no, ab = votos.count("Sí"), votos.count("No"), votos.count("Abstención")
        cuerpo += p("Participación (votación secreta: el voto no se vincula a ninguna delegación)", True) + tabla(["Delegación", "Asistencia", "Identidad comprobada"], filas, [5200, 2000, 2100])
        cuerpo += p("Recuento total", True) + tabla(["Sí", "No", "Abstención"], [[str(si), str(no), str(ab)]], [3000, 3000, 3000])
    cuerpo += p("No se guarda el número de DNI de ninguna persona: solo si se comprobó su identidad.", tam=18, color="7F7F7F")
    return cuerpo


ARCHIVOS = {
    "Normativa/Estatutos del CADUS (ejemplo).docx": p("Estatutos del CADUS", True, 36) + AVISO
        + p("Artículo 1. Naturaleza", True) + p("El Consejo de Alumnos de la Universidad de Sevilla (CADUS) es el órgano de representación de los estudiantes de la Universidad de Sevilla.")
        + p("Artículo 2. Fines", True) + p("Representar a los estudiantes, coordinar a las delegaciones de centro y defender sus derechos ante la Universidad.")
        + p("Artículo 3. Órganos", True) + p("Son órganos del CADUS el Pleno, la Ejecutiva y la Delegación General."),
    "Normativa/Reglamento de votaciones (ejemplo).docx": p("Reglamento de votaciones", True, 36) + AVISO
        + p("Artículo 1. Un voto por delegación", True) + p("En cada votación cuenta un voto por delegación, que representa a sus estudiantes. Solo votan los delegados.")
        + p("Artículo 2. Tipos de voto", True) + p("La votación puede ser nominal o secreta. En la secreta solo se recoge el recuento total, sin relacionar el voto con la delegación.")
        + p("Artículo 3. Constancia", True) + p("Se registra la asistencia y si se comprobó la identidad del delegado, sin guardar su DNI."),
    "Normativa/Reglamento de régimen interno 2019 (ejemplo, derogado).docx": p("Reglamento de régimen interno (2019)", True, 36) + p("DEROGADO", True, 28, color="C00000") + AVISO
        + p("Este reglamento fue sustituido por una versión posterior y se conserva solo como histórico. Su estado en el DMS es Derogada y no aparece en la vista de normativa vigente."),
    "Actas/Acta del pleno del 12-10-2026 (ejemplo).docx": p("Acta del pleno del 12 de octubre de 2026", True, 36) + AVISO
        + p("Orden del día", True) + p("1. Aprobación del acta anterior. 2. Calendario de asambleas. 3. Ruegos y preguntas.")
        + p("Acuerdos", True) + p("Se aprueba el acta anterior por asentimiento. Se fija la asamblea ordinaria para el 26 de octubre de 2026.")
        + p("Estado: aprobada por la Ejecutiva.", True),
    "Actas/Acta de la asamblea del 26-10-2026 (ejemplo, borrador).docx": p("Acta de la asamblea del 26 de octubre de 2026", True, 36) + p("BORRADOR", True, 28, color="C00000") + AVISO
        + p("Orden del día", True) + p("1. Votación de los presupuestos. 2. Votación de la reforma del reglamento.")
        + p("Este borrador solo lo ven su autor y la Ejecutiva hasta que se apruebe."),
    "Votaciones/Votación 1 de la asamblea del 26-10-2026 (nominal, ejemplo).docx": votacion(1, "Asamblea del 26-10-2026", "26/10/2026", "Nominal", "Aprobada", 261001),
    "Votaciones/Votación 2 de la asamblea del 26-10-2026 (secreta, ejemplo).docx": votacion(2, "Asamblea del 26-10-2026", "26/10/2026", "Secreto", "Rechazada", 261002),
    "Expedientes/CAD-2026-0001 (ejemplo).docx": p("Expediente CAD-2026-0001", True, 36) + AVISO
        + p("Tipo: reclamación académica (ejemplo).") + p("Facultad: Escuela Técnica Superior de Ingeniería Informática.") + p("Fecha de resolución: 20/10/2026. Caducidad: 20/10/2028 (resolución más 2 años).")
        + p("Resumen", True) + p("Reclamación ficticia sobre el calendario de una convocatoria de examen, resuelta a favor del estudiante. Sin datos personales."),
}

if __name__ == "__main__":
    salida = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(salida, exist_ok=True)
    paquete = {}
    for ruta, cuerpo in ARCHIVOS.items():
        datos = docx_bytes(cuerpo, os.path.basename(ruta)[:-5])
        d = docx.Document(io.BytesIO(datos))  # si no se abre, esto falla
        assert len(d.paragraphs) > 0
        paquete[ruta] = base64.b64encode(datos).decode("ascii")
        open(os.path.join(salida, os.path.basename(ruta)), "wb").write(datos)
        print(f"{ruta}: {len(datos)} bytes, {len(d.paragraphs)} párrafos, {len(d.tables)} tablas")
    json.dump(paquete, open(os.path.join(salida, "ejemplos_docx.json"), "w", encoding="utf-8"))
