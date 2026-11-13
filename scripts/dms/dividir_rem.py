"""Divide el REM del DMS en un .rem por sección (acta, normativa, expediente y votación).

El profesor pidió dividir los casos de uso por secciones o roles y dos casos en cada una; al dividir los casos de uso, el REM sale
también en varios .rem (uno por sección). Este script parte de scripts/remus/dms_data.json (única fuente de verdad) y, para cada
sección, deja solo sus dos casos de uso y lo que esos casos tocan (requisitos de información, funcionales, reglas, no funcionales,
interfaz, actores y objetivos relacionados), y genera con build_rem.ps1:
  docs/dms/rem-remus/secciones/DMS-<Seccion>.rem            proyecto de REMUS de la sección
  docs/dms/rem-remus/secciones/carga-remus-<seccion>.md     hoja legible del contenido
  scripts/remus/secciones/dms_<seccion>_data.json           datos de la sección (generado, no editar a mano)
El DMS.rem general (los 8 casos) se conserva.
Uso:  python scripts/dms/dividir_rem.py        (requiere Windows: build_rem.ps1 usa Jet 4.0 en PowerShell de 32 bits)
"""
import copy
import json
import os
import subprocess
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FUENTE = os.path.join(RAIZ, "scripts", "remus", "dms_data.json")
JSON_DIR = os.path.join(RAIZ, "scripts", "remus", "secciones")
REM_DIR = os.path.join(RAIZ, "docs", "dms", "rem-remus", "secciones")
PS32 = r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe"
SECCIONES = {
    "Acta": ("Acta", ["CU-D01", "CU-D02"]),
    "Normativa": ("Normativa", ["CU-D03", "CU-D07"]),
    "Expediente": ("Expediente", ["CU-D04", "CU-D05"]),
    "Votacion": ("Votación", ["CU-D06", "CU-D08"]),
}
LISTAS = ("actors", "objectives", "information", "ui", "functional", "nonfunctional", "rules")


def subconjunto(d, nombre, casos):
    s = copy.deepcopy(d)
    s["usecases"] = [c for c in d["usecases"] if c["id"] in casos]
    trazas = {t[0]: t[1] for t in d["traces"]}
    # todo lo que citan los casos de uso de la sección
    usados = set(casos)
    for c in casos:
        usados.update(trazas.get(c, []))
    # los objetivos se conservan si enlazan con algo de lo anterior
    objetivos = {o["id"] for o in d["objectives"] if any(x in usados for x in trazas.get(o["id"], []))}
    usados |= objetivos
    for lista in LISTAS:
        s[lista] = [x for x in d[lista] if x["id"] in usados]
    # trazas: solo entre elementos que siguen en el proyecto
    s["traces"] = []
    for origen, destinos in d["traces"]:
        if origen not in usados:
            continue
        ok = [x for x in destinos if x in usados]
        if ok:
            s["traces"].append([origen, ok])
    titulo = f"DMS del CADUS · {nombre}"
    s["cName"] = s["dName"] = titulo
    s["paragraphs"]["intro"] = (f"Este documento es la parte «{nombre}» del REM del DMS del CADUS: recoge los dos casos de uso de esa sección "
                                f"({', '.join(casos)}) y los requisitos, reglas y actores que los afectan. El REM completo, con los ocho casos de uso, está en "
                                f"DMS.rem. ") + s["paragraphs"]["intro"]
    return s


def main():
    d = json.load(open(FUENTE, encoding="utf-8"))
    os.makedirs(JSON_DIR, exist_ok=True)
    os.makedirs(REM_DIR, exist_ok=True)
    for clave, (nombre, casos) in SECCIONES.items():
        s = subconjunto(d, nombre, casos)
        ruta_json = os.path.join(JSON_DIR, f"dms_{clave.lower()}_data.json")
        json.dump(s, open(ruta_json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        destino = os.path.join(REM_DIR, f"DMS-{clave}.rem")
        md = os.path.join(REM_DIR, f"carga-remus-{clave.lower()}.md")
        r = subprocess.run([PS32, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", os.path.join(RAIZ, "scripts", "remus", "build_rem.ps1"),
                            "-src", os.path.join(RAIZ, "docs", "remus", "REM-CMS.rem"), "-dst", destino, "-data", ruta_json, "-md", md],
                           capture_output=True, text=True, cwd=RAIZ)
        print(f"== {clave}: {len(s['usecases'])} casos, {len(s['functional'])} RF, {len(s['rules'])} RN, {len(s['information'])} IR, "
              f"{len(s['actors'])} actores, {len(s['objectives'])} objetivos")
        print("  ", (r.stdout.strip().splitlines() or [r.stderr.strip()])[0])
        if r.returncode != 0:
            print(r.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
