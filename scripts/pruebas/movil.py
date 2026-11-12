"""Comprueba el portal en móvil (375×812) y tablet (768×1024) emulados con Chrome (HU-14c).
Uso:  python scripts/pruebas/movil.py        (con el sitio local arrancado)
Mide en cada página: desborde horizontal, elementos que se salen, objetivos táctiles menores de 40 px, campos con letra menor de 16 px
(iOS amplía la página al enfocarlos) y texto menor de 14 px. No sustituye a probar en dispositivos reales: la emulación no reproduce
el teclado del móvil, el rendimiento del procesador ni los gestos del navegador del sistema."""
import json, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost/proyecto_gsi/cms-wordpress"
PAGINAS = ["/", "/noticias/", "/delegaciones/", "/delegacion/delegacion-de-facultad-de-derecho/", "/actas-y-normativa/", "/events/",
           "/atencion-al-estudiante/", "/atencion-al-estudiante/buzon-de-consultas/", "/atencion-al-estudiante/seguimiento-de-ticket/",
           "/atencion-al-estudiante/mediacion-estudiantil/", "/atencion-al-estudiante/preguntas-frecuentes/", "/votaciones/", "/acceso/", "/contacto/"]
TAMANOS = {"móvil 375": (375, 812, True), "tablet 768": (768, 1024, True)}
JS = """() => {
  const vw = document.documentElement.clientWidth, out = {};
  out.desborde = document.documentElement.scrollWidth > vw + 1;
  const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && !e.closest('.screen-reader-text, [hidden], .ct-drawer-canvas, .ct-panel, .tribe-common-a11y-visual-hide, .ff-el-form-check-input[hidden]') && !e.classList.contains('tribe-common-a11y-visual-hide'); };
  // los carruseles con scroll propio (overflow-x auto) pueden ser más anchos que la pantalla
  out.se_salen = [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); if (!(r.width > 0 && r.right > vw + 1 && s.position !== 'fixed' && s.visibility !== 'hidden')) return false; for (let p = e.parentElement; p; p = p.parentElement) { const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden' || o === 'clip') return false; } return true; }).slice(0, 4).map(e => e.tagName.toLowerCase() + '.' + String(e.className).split(' ')[0]);
  const dianas = [...document.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, summary')].filter(vis);
  out.pequenas = dianas.filter(e => { const r = e.getBoundingClientRect(); return (r.height < 40 || r.width < 40) && !(e.tagName === 'A' && e.closest('p, li') && e.textContent.trim().length > 12 && r.height >= 24) && !(e.type === 'checkbox' && r.width >= 24); })
    .slice(0, 6).map(e => e.tagName.toLowerCase() + ' "' + (e.innerText || e.value || e.name || e.getAttribute('aria-label') || '').trim().slice(0, 24) + '" ' + Math.round(e.getBoundingClientRect().width) + 'x' + Math.round(e.getBoundingClientRect().height));
  out.letra_campo = [...document.querySelectorAll('input:not([type=hidden]):not([type=checkbox]):not([type=radio]), select, textarea')].filter(vis).filter(e => parseFloat(getComputedStyle(e).fontSize) < 16).map(e => e.name || e.id);
  out.texto_pequeno = [...document.querySelectorAll('p, li, a, span, label, td, small')].filter(vis).filter(e => e.children.length === 0 && e.textContent.trim().length > 3 && parseFloat(getComputedStyle(e).fontSize) < 14).length;
  return out;
}"""

fallos = 0
with sync_playwright() as p:
    nav = p.chromium.launch(channel="chrome", headless=True)
    for nombre, (w, h, movil) in TAMANOS.items():
        ctx = nav.new_context(viewport={"width": w, "height": h}, is_mobile=movil, has_touch=True, device_scale_factor=2)
        pag = ctx.new_page()
        print(f"== {nombre}")
        for ruta in PAGINAS:
            r = pag.goto(BASE + ruta, wait_until="networkidle", timeout=90000)
            pag.wait_for_timeout(500)
            m = pag.evaluate(JS)
            ok = r.status == 200 and not m["desborde"] and not m["se_salen"] and not m["pequenas"] and not m["letra_campo"]
            fallos += 0 if ok else 1
            print(("OK    " if ok else "REVISAR ") + ruta, "" if ok else json.dumps({k: v for k, v in m.items() if v and k != "texto_pequeno"} | {"http": r.status}, ensure_ascii=False))
        ctx.close()
    nav.close()
print(f"\n{fallos} páginas con algo que revisar")
sys.exit(1 if fallos else 0)
