"""Optimiza las imágenes propias del plugin cadus-portal (HU-20a).

Genera, a partir de los originales de docs/recursos/imagenes-originales/ (fuera del plugin, para no subirlos al servidor):
  - Fotos de la galería recortadas a 3:4 (el formato en que se muestran) en dos anchos, 360 y 720 px,
    en WebP (calidad 80) y en JPEG progresivo (calidad 80) como alternativa para navegadores antiguos.
  - El logotipo a 760 px de ancho (el doble del tamaño máximo en pantalla), en PNG de 128 colores: tiene menos de
    100 colores, así que el PNG con paleta ocupa menos que un WebP (17 KB frente a 40 KB).
  - Los escudos de las delegaciones (assets/escudos/, 320 px) en PNG de 256 colores con transparencia: pasan de 1,6 MB
    a 0,3 MB sin diferencia visible. Se optimizan en el mismo archivo (el nombre lo usa data/delegaciones.json); volver a
    ejecutarlo no los degrada: un escudo que ya tiene paleta se deja como está.

Uso (desde la raíz del repositorio):
    python scripts/imagenes/optimizar_imagenes.py
Necesita Pillow (pip install pillow). Se puede volver a ejecutar: sobrescribe los archivos generados.
Si el CADUS entrega fotos nuevas, se copian en docs/recursos/imagenes-originales/ y se añaden en includes/galeria.php.
"""
from pathlib import Path

from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parents[2]
ASSETS = RAIZ / "cms-wordpress" / "wp-content" / "plugins" / "cadus-portal" / "assets"
FOTOS = ASSETS / "fotos"
ORIGINALES = RAIZ / "docs" / "recursos" / "imagenes-originales"
ANCHOS = (360, 720)  # 4 columnas en escritorio (~300 px) y 2 en móvil (~180 px), con pantallas de alta densidad
CALIDAD = 80


def recortar_3x4(imagen: Image.Image) -> Image.Image:
    """Recorte centrado a 3:4, igual que object-fit: cover en la galería."""
    ancho, alto = imagen.size
    objetivo = 3 / 4
    if ancho / alto > objetivo:
        nuevo = round(alto * objetivo)
        izq = (ancho - nuevo) // 2
        return imagen.crop((izq, 0, izq + nuevo, alto))
    nuevo = round(ancho / objetivo)
    arriba = (alto - nuevo) // 2
    return imagen.crop((0, arriba, ancho, arriba + nuevo))


def fotos() -> None:
    for original in sorted(ORIGINALES.glob("*.jpg")):  # el logotipo es PNG y va aparte
        # exif_transpose respeta la orientación; al guardar sin exif se quitan los metadatos (GPS, cámara).
        imagen = recortar_3x4(ImageOps.exif_transpose(Image.open(original)).convert("RGB"))
        for ancho in ANCHOS:
            alto = round(ancho * 4 / 3)
            copia = imagen.resize((ancho, alto), Image.LANCZOS)
            copia.save(FOTOS / f"{original.stem}-{ancho}.webp", "WEBP", quality=CALIDAD, method=6)
            copia.save(FOTOS / f"{original.stem}-{ancho}.jpg", "JPEG", quality=CALIDAD, optimize=True, progressive=True)
        print(f"{original.name}: {', '.join(f'{a} px' for a in ANCHOS)} en WebP y JPEG")


def logo() -> None:
    original = ORIGINALES / "logo-cadus.png"
    imagen = Image.open(original).convert("RGBA")
    ancho = 760
    imagen = imagen.resize((ancho, round(imagen.height * ancho / imagen.width)), Image.LANCZOS)
    imagen.quantize(128, method=Image.FASTOCTREE).save(ASSETS / "logo-cadus.png", "PNG", optimize=True)
    print(f"logo-cadus: {imagen.width}x{imagen.height} en PNG con paleta")


def escudos() -> None:
    antes = despues = 0
    for archivo in sorted((ASSETS / "escudos").glob("*.png")):
        tamano = archivo.stat().st_size
        original = Image.open(archivo)
        if original.mode == "P":  # ya optimizado
            antes += tamano
            despues += tamano
            continue
        imagen = original.convert("RGBA")
        temporal = archivo.with_suffix(".tmp.png")
        imagen.quantize(256, method=Image.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG).save(temporal, "PNG", optimize=True)
        if temporal.stat().st_size < tamano:
            temporal.replace(archivo)
        else:
            temporal.unlink()
        antes += tamano
        despues += archivo.stat().st_size
    print(f"escudos: {antes // 1024} KB -> {despues // 1024} KB")


if __name__ == "__main__":
    fotos()
    logo()
    escudos()
