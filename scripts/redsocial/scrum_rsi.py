"""Dibuja el burndown del Sprint 1 de la red social (docs/redsocial/scrum/burndown-sprint-01-rsi.csv -> .png).
Uso: python scripts/redsocial/scrum_rsi.py"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CARPETA = os.path.join(RAIZ, "docs", "redsocial", "scrum")
filas = list(csv.DictReader(open(os.path.join(CARPETA, "burndown-sprint-01-rsi.csv"), encoding="utf-8")))
x = [f["fecha"][5:] for f in filas]
ideal = [float(f["ideal_sp"]) for f in filas]
real = [(i, float(f["real_sp"])) for i, f in enumerate(filas) if f["real_sp"] != ""]
fig, ax = plt.subplots(figsize=(9, 4), dpi=130)
ax.plot(range(len(x)), ideal, "--", color="#888", label="Ideal")
ax.plot([i for i, _ in real], [v for _, v in real], "-o", color="#8d0739", lw=2, label="Real")
ax.set_xticks(range(len(x)))
ax.set_xticklabels(x, rotation=45, fontsize=8)
ax.set_ylabel("Puntos de historia pendientes")
ax.set_title("Burndown del Sprint 1 de la red social (16/11 - 22/11/2026, 22 SP)", fontsize=11, color="#1f3a5f", fontweight="bold")
ax.grid(alpha=.3)
ax.legend()
fig.savefig(os.path.join(CARPETA, "burndown-sprint-01-rsi.png"), bbox_inches="tight", facecolor="white")
print("generado burndown-sprint-01-rsi.png")
