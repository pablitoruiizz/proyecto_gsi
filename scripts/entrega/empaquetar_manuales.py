"""Empaqueta la entrega EXTRA de manuales (hasta el 14/12/2026), aparte del zip del 29/11.

Uso: python scripts/entrega/empaquetar_manuales.py
Salida: docs/dms/entrega/paquete/Entrega-14-12-Manuales-CADUS.zip (carpeta ignorada por Git).
Antes: python scripts/entrega/build_manuales.py, build_manual_completo.py y exportar los PDF con Word.
"""
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ORIGEN = RAIZ / "docs" / "manuales" / "entrega"
SALIDA = RAIZ / "docs" / "dms" / "entrega" / "paquete" / "Entrega-14-12-Manuales-CADUS.zip"
SISTEMAS = ["CMS", "DMS", "RSI"]
LEEME = """# Manuales de usuario y de administrador — CADUS (CMS, DMS y red social)

Entrega extra del proyecto GSI (hasta el 14/12/2026), aparte del zip del 29/11/2026.

- `Manuales-CADUS-completo.pdf` / `.docx`: **un solo documento** con los seis manuales, con portada, índice, referencias cruzadas entre ellos y un anexo con los límites conocidos.
- `Manual-usuario-<sistema>-CADUS` y `Manual-administrador-<sistema>-CADUS` (`.pdf` y `.docx`), para el CMS (portal web), el DMS (SharePoint) y la RSI (red social en Teams).

Estado de lo que describen, a 27/11/2026: el portal se probó en un WordPress local; el DMS y la red social, en el tenant de la Universidad de Sevilla. Siguen sin comprobarse con cuentas reales de delegado y de estudiante, y el despliegue en la Universidad espera su respuesta. El anexo del documento completo lista todos los límites.
"""


def main():
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    archivos = [ORIGEN / "Manuales-CADUS-completo.pdf", ORIGEN / "Manuales-CADUS-completo.docx"]
    for tipo in ("usuario", "administrador"):
        for s in SISTEMAS:
            for ext in ("pdf", "docx"):
                archivos.append(ORIGEN / f"Manual-{tipo}-{s}-CADUS.{ext}")
    faltan = [a.name for a in archivos if not a.exists()]
    assert not faltan, f"faltan archivos: {faltan}"
    with zipfile.ZipFile(SALIDA, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("LEEME.md", LEEME)
        for a in archivos:
            z.write(a, a.name)
    print(f"zip: {SALIDA} {SALIDA.stat().st_size / 1e6:.1f} MB, {len(archivos) + 1} archivos")


main()
