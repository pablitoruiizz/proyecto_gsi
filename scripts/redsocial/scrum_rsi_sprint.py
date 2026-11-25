"""Burndown de un sprint de la red social: anota lo cerrado cada día, actualiza el CSV y dibuja la gráfica.

Complementa a scrum_rsi.py (que solo dibuja el Sprint 1) y sirve para cualquier sprint de la red social.
Los puntos de cada historia salen de docs/redsocial/scrum/product-backlog-rsi.md (columnas SP y Sprint).

Uso (desde la raíz del repositorio):
  python scripts/redsocial/scrum_rsi_sprint.py                       # Sprint 2, día de hoy, sin cierres
  python scripts/redsocial/scrum_rsi_sprint.py --hecho RSI-HU-09     # hoy se cierra RSI-HU-09
  python scripts/redsocial/scrum_rsi_sprint.py --fecha 2026-11-25 --hecho RSI-HU-07 --nota "Flujos probados por Marcos"
  python scripts/redsocial/scrum_rsi_sprint.py --regenerar           # solo redibuja la gráfica

Reglas (las de la definición de hecho de la red social):
  - Una historia solo se cierra cuando está en main, tiene su captura explicada y la ha probado otra persona.
  - El pendiente baja únicamente con los SP de las historias marcadas con --hecho; no se inventan datos.
  - Cada día se anota aunque no se cierre nada: los días sin registro arrastran el valor anterior.
  - Una historia no se puede cerrar dos veces. Para corregir un error se edita el CSV a mano y se usa --regenerar.
"""
import argparse
import csv
import datetime as dt
import os
import re
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CARPETA = os.path.join(RAIZ, "docs", "redsocial", "scrum")
BACKLOG = os.path.join(CARPETA, "product-backlog-rsi.md")
SPRINTS = {  # sprint: (inicio, fin)
    1: (dt.date(2026, 11, 16), dt.date(2026, 11, 22)),
    2: (dt.date(2026, 11, 23), dt.date(2026, 11, 29)),
}
CABECERA = ["fecha", "ideal_sp", "real_sp", "hito_sp", "tareas_completadas"]


def historias(sprint):
    """SP por historia del sprint, leídos del product backlog de la red social."""
    resultado = {}
    for linea in open(BACKLOG, encoding="utf-8-sig"):
        if not linea.startswith("| RSI-HU-"):
            continue
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if len(celdas) >= 7 and celdas[5] == f"Sprint {sprint}" and celdas[3].isdigit():
            resultado[celdas[0]] = int(celdas[3])
    return resultado


def leer(ruta):
    filas = {}
    if os.path.exists(ruta):
        with open(ruta, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                filas[dt.date.fromisoformat(r["fecha"])] = r
    return filas


def escribir(ruta, sprint, total, filas):
    inicio, fin = SPRINTS[sprint]
    n = (fin - inicio).days
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(CABECERA)
        for i in range(n + 1):
            d = inicio + dt.timedelta(i)
            r = filas.get(d, {})
            w.writerow([d.isoformat(), f"{total * (1 - i / n):.1f}", r.get("real_sp", ""),
                        "0" if i == n else "", r.get("tareas_completadas", "")])


def dibujar(ruta_png, sprint, total, filas):
    inicio, fin = SPRINTS[sprint]
    n = (fin - inicio).days
    dias = [inicio + dt.timedelta(i) for i in range(n + 1)]
    ideal = [total * (1 - i / n) for i in range(n + 1)]
    real = [(i, float(filas[d]["real_sp"])) for i, d in enumerate(dias) if d in filas and filas[d].get("real_sp", "") != ""]
    fig, ax = plt.subplots(figsize=(9, 4), dpi=130)
    ax.plot(range(n + 1), ideal, "--", color="#888", label="Ideal")
    if real:
        ax.plot([i for i, _ in real], [v for _, v in real], "-o", color="#8d0739", lw=2, label="Real")
    ax.set_xticks(range(n + 1))
    ax.set_xticklabels([d.strftime("%d/%m") for d in dias], rotation=45, fontsize=8)
    ax.set_ylabel("Puntos de historia pendientes")
    ax.set_ylim(0, total + 1)
    ax.set_title(f"Burndown del Sprint {sprint} de la red social ({inicio:%d/%m} - {fin:%d/%m/%Y}, {total} SP)",
                 fontsize=11, color="#1f3a5f", fontweight="bold")
    ax.grid(alpha=.3)
    ax.legend()
    fig.savefig(ruta_png, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sprint", type=int, default=2, choices=sorted(SPRINTS), help="número de sprint (por defecto, 2)")
    ap.add_argument("--fecha", help="día a anotar (AAAA-MM-DD); por defecto, hoy")
    ap.add_argument("--hecho", nargs="*", default=[], help="historias cerradas ese día (RSI-HU-07 ...)")
    ap.add_argument("--nota", default="", help="texto para la columna tareas_completadas")
    ap.add_argument("--regenerar", action="store_true", help="solo redibuja la gráfica a partir del CSV")
    a = ap.parse_args()

    hist = historias(a.sprint)
    if not hist:
        sys.exit(f"No hay historias del Sprint {a.sprint} en {BACKLOG}")
    total = sum(hist.values())
    nombre = f"burndown-sprint-{a.sprint:02d}-rsi"
    csv_ruta, png_ruta = os.path.join(CARPETA, nombre + ".csv"), os.path.join(CARPETA, nombre + ".png")
    inicio, fin = SPRINTS[a.sprint]
    filas = leer(csv_ruta)

    if a.regenerar:
        dibujar(png_ruta, a.sprint, total, filas)
        print(f"generado {nombre}.png")
        return

    dia = dt.date.fromisoformat(a.fecha) if a.fecha else dt.date.today()
    if not inicio <= dia <= fin:
        sys.exit(f"{dia} queda fuera del Sprint {a.sprint} ({inicio} a {fin}). Usa --fecha o --regenerar.")
    desconocidas = [h for h in a.hecho if h not in hist]
    if desconocidas:
        sys.exit(f"Historias que no son del Sprint {a.sprint}: {desconocidas}. Las del sprint: {', '.join(hist)}")
    cerradas = {h for r in filas.values() for h in re.findall(r"RSI-HU-\d+", r.get("tareas_completadas", ""))
                if re.search(r"(?i)cerrad", r.get("tareas_completadas", ""))}
    repetidas = [h for h in a.hecho if h in cerradas]
    if repetidas:
        sys.exit(f"Ya estaban cerradas: {repetidas}. Para corregirlo edita el CSV y usa --regenerar.")

    # Arrastra el valor anterior en los días sin registro hasta la fecha indicada.
    previo = total
    d = inicio
    while d <= dia:
        if d not in filas or filas[d].get("real_sp", "") == "":
            filas[d] = {"real_sp": str(previo), "tareas_completadas": filas.get(d, {}).get("tareas_completadas", "")}
        previo = int(float(filas[d]["real_sp"]))
        d += dt.timedelta(1)
    bajada = sum(hist[h] for h in a.hecho)
    filas[dia]["real_sp"] = str(int(float(filas[dia]["real_sp"])) - bajada)
    notas = [n for n in (filas[dia].get("tareas_completadas", ""),
                         (f"Cerradas: {', '.join(a.hecho)}. " if a.hecho else "") + a.nota) if n]
    filas[dia]["tareas_completadas"] = " | ".join(notas).strip()
    for futuro in [x for x in filas if x > dia and filas[x].get("real_sp", "") != ""]:
        filas[futuro]["real_sp"] = str(int(float(filas[futuro]["real_sp"])) - bajada)
    escribir(csv_ruta, a.sprint, total, filas)
    dibujar(png_ruta, a.sprint, total, filas)
    print(f"{dia}: pendiente {filas[dia]['real_sp']} SP de {total}" + (f" (cerradas: {', '.join(a.hecho)})" if a.hecho else ""))
    print(f"generados {nombre}.csv y {nombre}.png")


if __name__ == "__main__":
    main()
