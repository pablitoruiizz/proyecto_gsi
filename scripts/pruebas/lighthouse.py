"""Mide el portal con Lighthouse (HU-20b) y guarda un resumen en JSON.
Uso:  python scripts/pruebas/lighthouse.py antes|despues [--veces 3] [--paginas Inicio,Noticias]
Necesita Node y Chrome; descarga Lighthouse con npx la primera vez. Mide en móvil (emulación y limitación de red por defecto de Lighthouse)
las páginas de PAGINAS con el sitio local arrancado, y deja docs/rendimiento/lighthouse-<etiqueta>.json con la mediana de cada métrica."""
import json, os, statistics, subprocess, sys, tempfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE = "http://localhost/proyecto_gsi/cms-wordpress"
PAGINAS = {"Inicio": "/", "Noticias": "/noticias/", "Delegaciones": "/delegaciones/", "Actas y normativa": "/actas-y-normativa/", "Buzón": "/atencion-al-estudiante/buzon-de-consultas/"}
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
etiqueta = sys.argv[1] if len(sys.argv) > 1 else "antes"
veces = int(sys.argv[sys.argv.index("--veces") + 1]) if "--veces" in sys.argv else 3
solo = sys.argv[sys.argv.index("--paginas") + 1].split(",") if "--paginas" in sys.argv else list(PAGINAS)
sys.stdout.reconfigure(encoding="utf-8")
os.environ["CHROME_PATH"] = CHROME

METRICAS = {"first-contentful-paint": "FCP (ms)", "largest-contentful-paint": "LCP (ms)", "total-blocking-time": "TBT (ms)",
            "cumulative-layout-shift": "CLS", "speed-index": "Speed Index (ms)", "server-response-time": "Respuesta del servidor (ms)",
            "total-byte-weight": "Peso total (bytes)"}


def medir(url):
    with tempfile.TemporaryDirectory() as t:
        salida = os.path.join(t, "lh.json")
        r = subprocess.run(["npx", "--yes", "lighthouse@12.6.1", url, "--output=json", f"--output-path={salida}", "--quiet",
                            "--only-categories=performance,accessibility,best-practices,seo",
                            "--chrome-flags=--headless=new --no-sandbox --disable-gpu"], capture_output=True, text=True, shell=True, timeout=300)
        if not os.path.exists(salida):
            raise SystemExit(f"Lighthouse falló en {url}: {r.stderr[-400:]}")
        d = json.load(open(salida, encoding="utf-8"))
    a = d["audits"]
    res = {n: a[k]["numericValue"] for k, n in METRICAS.items() if k in a and a[k].get("numericValue") is not None}
    res["Rendimiento (0-100)"] = round(d["categories"]["performance"]["score"] * 100)
    res["Accesibilidad (0-100)"] = round(d["categories"]["accessibility"]["score"] * 100)
    res["Buenas prácticas (0-100)"] = round(d["categories"]["best-practices"]["score"] * 100)
    res["SEO (0-100)"] = round(d["categories"]["seo"]["score"] * 100)
    res["Peticiones"] = len(a["network-requests"]["details"]["items"])
    return res


salida = {"etiqueta": etiqueta, "veces": veces, "paginas": {}}
for nombre, ruta in ((n, r) for n, r in PAGINAS.items() if n in solo):
    medidas = [medir(BASE + ruta) for _ in range(veces)]
    mediana = {k: round(statistics.median(m[k] for m in medidas), 3) for k in medidas[0]}
    salida["paginas"][nombre] = mediana
    print(nombre, {k: mediana[k] for k in ("Rendimiento (0-100)", "LCP (ms)", "TBT (ms)", "Peso total (bytes)", "Peticiones")})
os.makedirs(os.path.join(RAIZ, "docs", "rendimiento"), exist_ok=True)
json.dump(salida, open(os.path.join(RAIZ, "docs", "rendimiento", f"lighthouse-{etiqueta}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("guardado docs/rendimiento/lighthouse-%s.json" % etiqueta)
