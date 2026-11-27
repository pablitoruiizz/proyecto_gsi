"""Genera el documento final del CMS para la entrega del 29/11/2026 (docs/dms/entrega/cms/Entrega-final-CMS-CADUS.docx).
El documento de la entrega 2 (Entrega2-CMS-CADUS) se reutiliza para la propuesta, las comparativas, el REM, el análisis, el diseño
y las capturas de esa entrega; este documento recoge el estado final: backlog, Sprint 3, burndown, requisitos que cambian,
implementación con el contenido real, pruebas de aceptación y lo que queda pendiente. Reutiliza las tablas del Sprint 3 de
build_adenda_cms.py.
Uso: python scripts/dms/build_final_cms.py   (después, exportar a PDF con Word)"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_adenda_cms as A  # noqa: E402
import build_doc_dms as B  # noqa: E402

RAIZ = B.RAIZ
SAL = os.path.join(B.DMS, "entrega", "cms")
CAP = os.path.join(RAIZ, "docs", "entrega", "img", "capturas4")


def estado_vigente(res):
    """Estado actual de un caso: primera palabra de estado del texto vigente, sin el historial («Antes: ...», «Prueba anterior: ...»)."""
    if not res:
        return "Sin ejecutar"
    vigente = re.split(r"\bAntes(?:, con [^:]*)?:|Prueba anterior:", res)[0]
    pos = {k: vigente.find(k) for k in ("OK", "Parcial", "Pendiente", "FALLO") if vigente.find(k) >= 0}
    return min(pos, key=pos.get) if pos else "Sin clasificar"


def pruebas():
    """Resumen de tests/E3-04-pruebas-de-aceptacion.md: (id, caso, estado). La columna «Resultado» es la última de cada tabla."""
    filas = []
    for l in open(os.path.join(RAIZ, "tests", "E3-04-pruebas-de-aceptacion.md"), encoding="utf-8"):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) >= 4 and re.fullmatch(r"[THPA]\d+(-\d+)?", c[0]):
            filas.append((c[0], c[1], estado_vigente(c[-1])))
    return filas


def main():
    doc = B.nuevo()
    doc.add_heading("CMS del CADUS — Documento final de la entrega del 29/11/2026", 0)
    B.par(doc, "Gestión de Sistemas de Información (GSI) · Universidad de Sevilla · estado a 26/11/2026", cursiva=True)

    doc.add_heading("1. Qué se adjunta", 1)
    B.par(doc, "El proyecto del CMS es el mismo desde la entrega 2, así que se **vuelve a adjuntar el documento de la entrega 2** (`Entrega2-CMS-CADUS`) para lo que no ha cambiado y este documento recoge el estado final. No hubo un Sprint 4 del CMS: el trabajo posterior al cierre del Sprint 3 (15/11) son tareas de cierre y la reapertura de HU-14 y HU-15, que constan en las secciones 2 y 9; por eso el sprint backlog y el burndown de referencia son los del Sprint 3, el último sprint del CMS.")
    B.tabla(doc, ["Contenido pedido para el CMS", "Dónde está"], [
        ["Propuesta de temática o empresa (versión definitiva)", "Documento de la entrega 2, sección 1"],
        ["Comparativa y justificación de hosting, comunicación, gestión de SCRUM y control de versiones", "Documento de la entrega 2, sección 2.2; la comparativa de hosting se amplía con el servidor SFTP de la US (adenda del Sprint 3, sección 8)"],
        ["Product backlog", "Sección 4 de este documento (estados finales)"],
        ["Sprint backlog del sprint de estas semanas", "Sección 5 (Sprint 3, el último sprint del CMS)"],
        ["Burndown chart del sprint de esta semana", "Sección 6 (Sprint 3)"],
        ["Requisitos (REM)", "`CADUS.rem` y `REM-CADUS-v2.3.pdf`; cambios en la sección 3"],
        ["Análisis: UML con la estructura de la página web", "Documento de la entrega 2, sección 4.1"],
        ["Diseño: UML de plugins, comparativa de plugins con métricas (incluidos los obligatorios) y mockups con 3 temáticas", "Documento de la entrega 2, secciones 4.3, 4.4, 5.1 y 5.2"],
        ["Implementación: capturas", "Sección 8 de este documento (portal con el contenido real), carpeta `capturas-sprint3` y capturas de la entrega 2"],
        ["Pruebas, calidad y pendientes", "Secciones 9 y 10"]], [7, 10], tam=9)

    doc.add_heading("2. Estado final del portal (a 26/11/2026)", 1)
    B.tabla(doc, ["Área", "Estado"], [
        ["Contenido", "Las noticias, las actas y la normativa de ejemplo se han sustituido por contenido real de www.cadus.us.es y el calendario lleva actividades reales ya celebradas (sección 8). Se conservan, identificados como ejemplo, dos eventos futuros inventados, su votación vinculada y un acta pendiente de aprobación. Las 27 delegaciones se cargaron de esa web con sus miembros; falta el correo en 1, el teléfono en 7 y el horario en las 27, que esa web no publica (`seguimiento/E2-12-fichas-y-edicion.md`)"],
        ["HU-14 móvil y tablet", "Hecho. Móvil real el 22/11 (Pablo: portada, buzón, calendario, mediación y menú) y tablet el 23/11, comprobados según Pablo. Emulación a 390 y 768 px el 15/11, repetida por Marcos el 23/11"],
        ["HU-15 accesibilidad", "Hecha. Marcos (23/11): teclado completo y daltonismo correctos, y el Narrador lee los campos y los errores del buzón (también antes del arreglo). Lighthouse de accesibilidad: 97 / 96 / 96 el 23/11 (con una copia anterior del plugin) y **100 / 100 / 100** repetido por Marcos el 25/11 con el código actual (portada, buzón y directorio, PR #98). El PR #96 (errores de los formularios enlazados con su campo y foco al primer error) se fusionó el 25/11 y se comprobó con una ejecución en el navegador, no con un lector de pantalla. Queda sin probar NVDA"],
        ["HU-16 buscar y filtrar", "H16-1 a H16-6 probados con clics el 22/11 y repetidos el 25/11 con los datos reales mediante peticiones al servidor construidas desde los formularios (no con clics); búsqueda del panel (H16-7) probada en tickets y en mediaciones: solo encuentra por referencia, asunto o centro, nunca por datos del estudiante"],
        ["HU-17 seguridad de formularios", "Campo trampa, nonce y límite de envíos comprobados con peticiones al servidor; texto con etiquetas HTML y con SQL se guarda como texto. Wordfence bloquea `<script>` antes de llegar al portal"],
        ["HU-20 rendimiento", "Lighthouse de rendimiento de la portada en móvil, mediana de 3 ejecuciones el 26/11: **98** con el contenido real (el informe de HU-20b da 91 antes de la caché, el minificado y el Gzip y 99 después, el 12/11); LCP de 2,9 s antes y 1,98 s hoy. Fotos de la galería en WebP de 720 px como máximo y escudos en WebP de 300 px, con carga diferida; una imagen de 3000 px se reduce a 1920. Al probarlo se encontró que el límite de 8 MB no se aplicaba a las subidas del editor de bloques (API REST); se corrigió el 26/11 y se repitió (`tests/E3-04-pruebas-de-aceptacion.md`, observación 4). Medido en el servidor local, no en el de la US"],
        ["HU-22 y HU-23", "HU-22 (relevo de la cuenta de la delegación): H22-1 a H22-5 ejecutados el 26/11 con sesiones reales de las cuentas de prueba y todos OK (el delegado hace el relevo y pierde la sesión, la contraseña antigua no sirve, no puede hacer el de otra cuenta, la Ejecutiva lo hace y solo ve cuentas de delegación, y el script rechaza una segunda cuenta para la misma ficha). Los ejecutó Claude en nombre de Pablo, no otra persona del equipo. HU-23 (conservación a los 2 años): el script se repitió en otro equipo (Marcos, 23/11) sin errores"],
        ["Volcado de la base de datos", "`bd_cadus_v1_sprint3.sql` es una **copia saneada** para evaluar el portal: conserva la estructura, los roles, el contenido y las 27 fichas, y sustituye las cuentas reales del equipo por tres cuentas de demostración (administración, Ejecutiva y delegación) con correos ficticios. No incluye contraseñas ni correos reales, sesiones, registros de Wordfence ni de estadísticas, claves de instalación, tickets ni cuentas de prueba. Cuentas, contraseña de demostración y forma de restaurarlo: `LEEME-volcado.md`, en la misma carpeta"],
        ["Cuentas y contraseñas", "Según Pablo, las contraseñas de `root` y `cadus` se cambiaron el 23/11 (aviso crítico de Wordfence); no queda constancia en el repositorio, por seguridad"],
        ["Despliegue en la US (E3-09)", "No se ha hecho: el servidor ofrecido tenía PHP 7.2/7.3 y queda pendiente de la respuesta de la US sobre el despliegue. El portal se entrega con su volcado de base de datos y funciona en el servidor local del equipo"]], [4, 13], tam=8.5)

    doc.add_heading("3. Cambios en los requisitos tras la entrevista con el CADUS (26/10/2026)", 1)
    B.par(doc, "El REM del CMS está en la versión 2.3 desde la tarea E3-05 del Sprint 3. Estos son los cambios acordados con el cliente:")
    A.cambios_requisitos(doc)

    doc.add_heading("4. Product backlog", 1)
    B.par(doc, "Mismo product backlog (mismo proyecto), con el estado a 26/11. HU-20 pasó al Sprint 3, el antiguo Sprint 4 desapareció (un único sprint de tres semanas), HU-21 quedó cancelada y se añadieron HU-22, HU-23 y, el 12/11, HU-24.")
    B.tabla(doc, ["ID", "Historia", "Requisitos", "Prioridad", "SP", "Estado", "Sprint"], A.historias(), [1.4, 6.3, 2.2, 1.5, 0.8, 2.2, 2.0], tam=7.5)

    doc.add_heading("5. Sprint backlog del Sprint 3", 1)
    A.sprint_backlog(doc)
    doc.add_heading("6. Burndown chart del Sprint 3", 1)
    A.burndown(doc)

    doc.add_heading("7. Calidad y revisión cruzada", 1)
    for t in ("Revisión con Codex de HU-23 el 13/11, con cuatro fallos corregidos (título y dirección del ticket anonimizado, ticket reabierto durante el borrado, limpieza dada por buena aunque fallase un borrado y edición de tickets anonimizados).",
              "Revisión con Codex de la entrega del 22/11 y, el 23/11, de la programación de la carga del contenido real y del calendario: siete hallazgos, todos corregidos y comprobados (encargo de la revisión en `revisiones/codex_revision_programacion_23_11.md`). El 25/11 hubo otra revisión del cierre (`revisiones/codex_revision_cierre_25_11.md`). El 26/11 y el 27/11 (sobre el zip de la entrega) hubo otras dos revisiones con Codex y sus hallazgos se corrigieron antes de entregar.",
              "Pruebas cruzadas hechas por otra persona: Marcos probó HU-14a, HU-17b y HU-23 (23/11) y repitió Lighthouse de accesibilidad (25/11). Joaquín y Álvaro tenían asignadas HU-14b, HU-16a y HU-22, que no han registrado como propias. Las pruebas que ejecutó Claude en nombre de Pablo (HU-16a, HU-16b, HU-17a, HU-17b, HU-20, HU-22, HU-23 y el panel de tickets) constan así en el registro y no se cuentan como prueba de otra persona."):
        B.vineta(doc, t)

    doc.add_heading("8. Implementación: el portal con el contenido real", 1)
    B.par(doc, "Estas capturas, hechas el 25/11/2026 en el servidor local del equipo, enseñan el portal con contenido real de www.cadus.us.es en lugar del texto de ejemplo. Los artículos, las actas y la normativa llevan al pie un enlace a su fuente. Los dos eventos futuros del calendario son inventados y están marcados «(ejemplo)» para ver cómo se muestran los próximos eventos y una votación vinculada a una asamblea.")
    figuras = [
        ("f01-portada.jpg", "Portada con las últimas noticias reales, los accesos y la agenda."),
        ("f02-noticias.jpg", "Noticias y comunicados: ocho artículos reales (2022 y 2023) con filtro por palabra clave, categoría y fechas."),
        ("f03-noticia.jpg", "Una noticia real, con su categoría, su fecha original y el enlace a la fuente."),
        ("f04-actas-y-normativa.jpg", "Actas y normativa: ocho actas de pleno (octubre de 2025 a junio de 2026) y dos normativas, con su PDF."),
        ("f05-calendario-septiembre.jpg", "Calendario de septiembre de 2026 con actividades reales: plazo de candidaturas de los IV Premios CADUS, su resolución y el pleno ordinario."),
        ("f06-calendario-proximos.jpg", "Próximos eventos: los dos eventos inventados, marcados «(ejemplo)»."),
    ]
    for nombre, pie in figuras:
        ruta = os.path.join(CAP, nombre)
        if os.path.exists(ruta):
            B.figura(doc, ruta, pie, 13)
        else:
            B.par(doc, f"(falta la captura {nombre})", cursiva=True)
    B.par(doc, "El resto de las capturas del portal están en el documento de la entrega 2 y en la carpeta `capturas-sprint3` (relevo de la cuenta, calendario, páginas institucionales y accesibilidad).")

    doc.add_heading("9. Pruebas de aceptación (E3-04)", 1)
    filas = pruebas()
    cuenta = {}
    for _, _, est in filas:
        cuenta[est] = cuenta.get(est, 0) + 1
    B.par(doc, "Registro completo en `seguimiento/E3-04-pruebas-de-aceptacion.md`, con el método, quién y cuándo de cada caso (el resumen cuenta solo el estado vigente de cada caso, no su historial). Resumen de " + str(len(filas)) + " casos: " + ", ".join(f"{n} {k}" for k, n in sorted(cuenta.items(), key=lambda x: -x[1])) + ". «Parcial» significa que se comprobó lo funcional pero no el criterio completo (por ejemplo, el cronometraje con una persona externa o la prueba en un servidor con correo real).")
    abiertos = [(i, c[:90], e) for i, c, e in filas if e != "OK"]
    if abiertos:
        B.tabla(doc, ["Caso", "Qué se prueba", "Estado"], abiertos, [2, 12, 3], tam=8, titulo="Casos que no están completos")

    doc.add_heading("10. Pendientes y limitaciones", 1)
    for t in ("**Despliegue en la US (E3-09):** queda pendiente de la respuesta de la US sobre el despliegue web; sin ello el portal sigue en el servidor local del equipo.",
              "**Correo del buzón:** el contenido de los avisos cumple RN-03 (solo código, tipo, fecha y enlace), y se comprobó el envío por SMTP a un servidor de pruebas local (Mailpit, 27/11), pero no la entrega a una bandeja real: el equipo local no tiene servidor de correo ni un SMTP con credenciales. Hallazgo: con el remitente por defecto de WordPress en local (`wordpress@localhost`) PHPMailer rechaza el envío; hay que fijar un remitente válido.",
              "**Cuentas y fichas reales:** E2-01 (cuentas reales de la Ejecutiva y las delegaciones) se descartó el 25/11 porque depende del CADUS; E2-12 se cerró el 25/11 con las limitaciones de datos de la sección 2 (horario, 7 teléfonos y 1 correo), que solo puede dar el CADUS. Mientras tanto se usan las cuentas actuales y los datos de su web.",
              "**Pruebas cruzadas y casos abiertos:** no todas las pruebas las ha repetido otra persona (sección 7) y la sección 9 lista los casos que no están completos (los cronometrados con una persona externa y el envío real del correo). Falta, por ejemplo, la prueba cruzada de HU-14b y HU-16a de Joaquín y la de HU-22 de Álvaro: sus casos los ejecutó Claude en nombre de Pablo.",
              "**Dispositivos reales:** móvil y tablet constan como comprobados según Pablo; no hay un registro de pruebas por dispositivo.",
              "**Accesibilidad:** se probó con el Narrador de Windows; NVDA no."):
        B.vineta(doc, t)

    sal = os.path.join(SAL, "Entrega-final-CMS-CADUS.docx")
    doc.save(sal)
    print("generado", sal)


if __name__ == "__main__":
    main()
