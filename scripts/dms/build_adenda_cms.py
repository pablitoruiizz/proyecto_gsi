"""Genera la adenda del CMS para la entrega del 08/11 (docs/dms/entrega/cms/Adenda-CMS-Sprint3.docx).
El documento del CMS de la entrega 2 se reutiliza tal cual; esta adenda recoge lo que cambia: requisitos tras la entrevista,
product backlog actualizado, sprint backlog del Sprint 3 y burndown del Sprint 3.
Uso: python scripts/dms/build_adenda_cms.py"""
import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
import build_doc_dms as B  # noqa: E402

RAIZ = B.RAIZ
SAL = os.path.join(B.DMS, "entrega", "cms")
os.makedirs(SAL, exist_ok=True)


def burndown_cms():
    ruta = os.path.join(RAIZ, "docs", "scrum", "burndown", "sprint-03.csv")
    filas = list(csv.DictReader(open(ruta, encoding="utf-8")))
    x = [f["fecha"][5:] for f in filas]
    ideal = [float(f["ideal_sp"]) for f in filas]
    real = [(i, float(f["real_sp"])) for i, f in enumerate(filas) if f["real_sp"] != ""]
    hitos = [(i, float(f["hito_sp"])) for i, f in enumerate(filas) if f.get("hito_sp", "") != ""]
    fig, ax = plt.subplots(figsize=(9.5, 4.3), dpi=130)
    ax.plot(range(len(x)), ideal, "--", color="#888", label="Ideal")
    ax.plot([i for i, _ in hitos], [v for _, v in hitos], "s", color="#e08a00", label="Hito semanal (compromiso)")
    ax.plot([i for i, _ in real], [v for _, v in real], "-o", color="#8d0739", lw=2, label="Real")
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=45, fontsize=8)
    ax.set_ylabel("Puntos de historia pendientes")
    ax.set_title("Burndown del Sprint 3 del CMS (26/10 – 15/11/2026, 36 SP)", fontsize=11, color="#1f3a5f", fontweight="bold")
    ax.grid(alpha=.3)
    ax.legend()
    sal = os.path.join(B.IMG, "burndown-cms-sprint3.png")
    fig.savefig(sal, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return sal


def historias():
    filas = []
    for l in open(os.path.join(RAIZ, "docs", "scrum", "backlog", "product-backlog.md"), encoding="utf-8"):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) == 8 and c[0].startswith(("HU-", "PB-")):
            filas.append([c[0], c[1], c[2], c[3], c[4], c[5], c[6]])
    return filas


def main():
    doc = B.nuevo()
    doc.add_heading("CMS del CADUS — Adenda de la entrega del 08/11/2026", 0)
    B.par(doc, "Gestión de Sistemas de Información (GSI) · Universidad de Sevilla · Sprint 3 del CMS (26/10 – 15/11/2026) · estado a 12/11/2026", cursiva=True)
    doc.add_heading("1. Qué se adjunta y qué cambia", 1)
    B.par(doc, "El proyecto del CMS es el mismo, así que se **reutiliza el documento de la entrega 2** (`Entrega2-CMS-CADUS`) para la propuesta de temática, las comparativas (hosting, comunicación, SCRUM, control de versiones y plugins), el análisis, el diseño, los mockups y las capturas. Esta adenda recoge solo lo que cambia desde entonces.")
    B.tabla(doc, ["Contenido pedido para el CMS", "Qué se adjunta"], [
        ["Propuesta de temática y comparativas", "Sin cambios: documento de la entrega 2"],
        ["Product backlog", "Mismo proyecto; actualizado en la sección 3 de esta adenda"],
        ["Sprint backlog (sprint de estas semanas)", "Sprint 3: sección 4"],
        ["Burndown chart (solo el sprint actual)", "Sprint 3: sección 5"],
        ["Requisitos (REM)", "REM del CMS actualizado a la versión 2.1 con las respuestas de la entrevista (CADUS.rem y REM-CADUS-v2.pdf); cambios en la sección 2"],
        ["Entrevista con el cliente", "Documento «Entrevista-CADUS» (adjunto)"],
        ["Análisis, diseño y mockups", "Sin cambios: documento de la entrega 2"],
        ["Implementación", "Capturas de la entrega 2; sección 6 de esta adenda"]], [7, 10], tam=9)

    doc.add_heading("2. Cambios en los requisitos tras la entrevista con el CADUS (26/10/2026)", 1)
    B.par(doc, "La entrevista con el cliente (documento «Entrevista-CADUS», adjunto) cambia el alcance del portal. El REM se actualizará en la tarea E3-05 del Sprint 3; estos son los cambios acordados:")
    B.tabla(doc, ["Respuesta del cliente", "Cambio en el CMS", "Requisitos"], [
        ["Las votaciones son presenciales; solo votan los delegados (un voto por delegación, con DNI) y no se publican resultados", "HU-21 (papeleta online) cancelada. El portal solo anuncia la votación (HU-11); el registro de la votación pasa al DMS", "RF-12, RN-05"],
        ["El delegado puede dar de alta a su sucesor", "HU-22 (hecha el 09/11): una cuenta por delegación con el correo institucional de la delegación; el relevo lo hace el delegado saliente o un ejecutivo, con efecto inmediato (nueva contraseña y sesiones cerradas)", "RF-14, RN-04"],
        ["Tickets y mediaciones se conservan 2 años desde que se resuelven", "Nueva HU-23: borrado o anonimización a los 2 años. Cierra el plazo pendiente", "RNF-08, RN-03"],
        ["Todas las consultas deben tratarse con total privacidad", "RN-03 se amplía de reclamaciones y mediaciones a todas las consultas del buzón", "RN-03"],
        ["Todo contenido pasa por la Ejecutiva", "RN-01 se amplía de actas y normativa a todo el contenido publicado", "RN-01"],
        ["Aviso de ticket al correo de dcadus; datos mínimos: nombre y apellidos, facultad y correo US", "Tarea E3-08. El plazo de respuesta («al menos 4 días») se publica cuando se aclare si es mínimo o máximo", "RF-09, RF-10, RNF-08"],
        ["Calendario con asambleas y cursos", "Tarea E3-07: categoría «Cursos»", "RF-11"],
        ["Móvil, tablet y ordenador", "HU-14 incluye la tablet", "RNF-02"],
        ["Accesibilidad para personas ciegas o daltónicas y pautas DUA", "HU-15 añade daltonismo, lector de pantalla y DUA", "RNF-03"],
        ["Servidor SFTP de la US y poco mantenimiento", "E3-03 respondida el 09/11: SFTP con PHP 7.2/7.3 y MySQL, sin correo saliente ni cron. WordPress 7.1 necesita PHP 7.4 o superior, así que E3-09 (desplegar) queda bloqueada hasta que la US actualice PHP", "RNF-05, RNF-07"]], [5.7, 8.3, 3], tam=8.5, titulo="Cambios tras la entrevista")

    doc.add_heading("3. Product backlog", 1)
    B.par(doc, "El product backlog sigue siendo el mismo (mismo proyecto). Cambios: HU-20 pasa al Sprint 3, el antiguo Sprint 4 desaparece (un único sprint de tres semanas), HU-21 queda cancelada y se añaden HU-22 y HU-23.")
    B.tabla(doc, ["ID", "Historia", "Requisitos", "Prioridad", "SP", "Estado", "Sprint"], historias(), [1.4, 6.3, 2.2, 1.5, 0.8, 2.2, 2.0], tam=7.5)

    doc.add_heading("4. Sprint backlog del Sprint 3", 1)
    B.par(doc, "**Sprint 3 (26/10 – 15/11/2026): 36 SP.** Objetivo: dejar el portal terminado e implementado para el 15/11, como pidió el cliente: móvil y tablet, accesibilidad, formularios protegidos, buscar y filtrar en el panel, rendimiento, relevo de delegados y borrado a los 2 años.")
    B.tabla(doc, ["Subtarea", "Qué incluye", "SP", "Quién"], [
        ["HU-14a", "Menús y portada en móvil y tablet", 3, "Joaquín"],
        ["HU-14b", "Directorio, tablas y fichas de delegación en móvil y tablet", 3, "Álvaro"],
        ["HU-14c", "Buzón, calendario y mediación en móvil y tablet, probados en dispositivos reales", 2, "Pablo"],
        ["HU-15a", "Contraste, foco visible, teclado y enlace «saltar al contenido»", 3, "Joaquín"],
        ["HU-15b", "Etiquetas de formularios, textos alternativos, encabezados, ARIA y lector de pantalla", 3, "Marcos"],
        ["HU-15c", "Daltonismo, pautas DUA, auditoría con Lighthouse y axe", 2, "Miguel Ángel"],
        ["HU-16a", "Filtros por palabra clave y fecha en noticias, actas y delegaciones", 3, "Álvaro"],
        ["HU-16b", "Búsqueda en tickets sin exponer datos del estudiante (RN-03)", 2, "Marcos"],
        ["HU-17a", "Honeypot y límite de envíos en el buzón y la mediación", 3, "Marcos"],
        ["HU-17b", "Revisión de saneamiento, nonces y escape; revisión de Wordfence", 2, "Pablo"],
        ["HU-20a", "Optimización de imágenes", 2, "Miguel Ángel"],
        ["HU-20b", "Caché y minificación; medición antes y después", 3, "Pablo"],
        ["HU-22", "El delegado da de alta a su sucesor, con efecto inmediato", 3, "Miguel Ángel"],
        ["HU-23", "Borrado o anonimización de tickets y mediaciones a los 2 años", 2, "Álvaro"]], [1.8, 10.2, 1, 4], tam=8.5, titulo="Sprint backlog del Sprint 3")
    B.tabla(doc, ["Subtarea", "Estado a 12/11", "Quién y cuándo"], [
        ["HU-22", "Hecha", "Miguel Ángel, 09/11"],
        ["HU-17a", "Hecha (pruebas propias: 81 correctas, 0 fallos)", "Marcos, 11/11"],
        ["HU-16b", "Hecha", "Marcos, 11/11"],
        ["HU-15b", "Hecha (59 comprobaciones de accesibilidad correctas, 0 fallos)", "Marcos, 12/11"],
        ["E3-03, E3-05, E3-07, E3-08", "Hechas (sin puntos)", "Miguel Ángel y Marcos, 09–11/11"],
        ["E3-09 (despliegue en la US)", "Bloqueada: PHP 7.2/7.3 en el servidor", "Pasa al siguiente sprint"],
        ["Resto (HU-14a/b/c, HU-15a/c, HU-16a, HU-17b, HU-20a/b, HU-23)", "Sin empezar según el repositorio", "—"]], [5.5, 8, 3.5], tam=8.5, titulo="Estado de las subtareas del Sprint 3 a 12/11/2026")
    B.tabla(doc, ["Integrante", "SP"], [["Pablo", 7], ["Joaquín", 6], ["Miguel Ángel", 7], ["Álvaro", 8], ["Marcos", 8], ["Total", 36]], [5, 2], tam=9)
    B.tabla(doc, ["Semana", "Historias", "Pendiente al cerrar la semana"], [
        ["26/10 – 01/11", "HU-14, HU-17, HU-22, HU-23 (18 SP)", "18 SP"],
        ["02/11 – 08/11", "HU-15 (8 SP) y entrega del DMS", "10 SP"],
        ["09/11 – 15/11", "HU-16, HU-20, despliegue, pruebas de aceptación y documentación final (10 SP)", "0 SP"]], [3, 10, 4], tam=9, titulo="Puntos de control semanales")

    doc.add_heading("5. Burndown chart del Sprint 3", 1)
    B.figura(doc, burndown_cms(), "Burndown del Sprint 3 del CMS: línea ideal, hitos semanales y puntos pendientes reales.", 15)
    B.par(doc, "A 12/11 quedan 25 de los 36 SP: se han cerrado 11 (HU-22, el 09/11; HU-17a, HU-16b y HU-15b, el 11 y el 12/11). El hito del 08/11 (10 SP pendientes) no se alcanzó y a esta altura la línea ideal pide 5,4 SP, así que el equipo va por detrás y se recortará primero HU-16 si hace falta. La línea ideal es lineal; los hitos semanales (18 SP el 01/11 y 10 SP el 08/11) son el compromiso real del equipo, para no repetir el cierre de última hora de los sprints 1 y 2. El burndown se actualiza cada día en `docs/scrum/burndown/sprint-03.csv`.")

    doc.add_heading("6. Implementación", 1)
    B.par(doc, "Las capturas del portal son las de la entrega 2. Lo hecho en el Sprint 3 es el relevo de la cuenta de la delegación (HU-22), las categorías «Asambleas» y «Cursos» del calendario (E3-07), y en Atención al estudiante la protección del formulario con campo trampa y límite de envíos (HU-17a), la búsqueda de tickets sin exponer datos (HU-16b), los datos mínimos y el aviso a la cuenta del CADUS (E3-08), y la accesibilidad de las siete páginas, con un encabezado h2 que evita el salto de h1 a h3 (HU-15b). Las pruebas del equipo (ver `scripts/pruebas/SPRINT3_BUZON.md`) dan 59, 81, 43, 254 y 316 comprobaciones correctas y ningún fallo, y un feed de entradas privadas que confirmaba que existía un ticket ahora responde 404 (RN-03). Las capturas del Sprint 3 se añadirán al documento final del 15/11.")
    doc.add_heading("7. Riesgos", 1)
    for t in ("El trabajo se deja para el final, como en los sprints anteriores: puntos de control semanales y burndown diario.",
              "El servidor SFTP de la US ofrece PHP 7.2/7.3 y WordPress 7.1 necesita 7.4 o superior: el despliegue (E3-09) está bloqueado hasta que la US actualice PHP; si no lo hace, hay que buscar otro alojamiento o seguir con el servidor compartido por Tailscale.",
              "HU-14 y HU-15 tocan el mismo CSS: HU-15a empieza al cerrar HU-14a.",
              "El DMS y el CMS compiten por las mismas personas: el DMS se entrega el 08/11 con su propio reparto."):
        B.vineta(doc, t)
    sal = os.path.join(SAL, "Adenda-CMS-Sprint3.docx")
    doc.save(sal)
    print("generado", sal)


if __name__ == "__main__":
    main()
