# Pruebas de accesibilidad (HU-15c)

Auditoría automática del portal con **axe-core** (WCAG 2.1 A y AA), **Lighthouse** y una **simulación de daltonismo**. El informe con los resultados está en [`docs/accesibilidad/HU-15c-auditoria.md`](../../../docs/accesibilidad/HU-15c-auditoria.md).

Necesita Node 18 o superior. Desde esta carpeta:

```bash
npm install
npx playwright install chromium     # solo la primera vez
```

## axe-core: 17 páginas públicas, en escritorio (1280 px) y móvil (390 px)

```bash
CADUS_URL=http://servidor/ruta-de-la-web node axe.mjs resultados-axe.json
```

En Windows (PowerShell): `$env:CADUS_URL="http://servidor/ruta"; node axe.mjs resultados-axe.json`.
Escribe cada página con sus fallos (o «sin fallos») y deja el detalle en el JSON.

## Lighthouse

```bash
npx lighthouse http://servidor/ruta/ --only-categories=accessibility,performance,best-practices,seo --view
npx lighthouse http://servidor/ruta/ --preset=desktop --only-categories=accessibility,performance,best-practices,seo --view
```

## Daltonismo

```bash
CADUS_URL=http://servidor/ruta node daltonismo.mjs capturas
```

Hace una captura de la portada, las actas y las delegaciones tal como las ve una persona con protanopia, deuteranopia, tritanopia y acromatopsia (matrices de Machado, Oliveira y Fernandes, 2009, con severidad máxima). Hay que comprobar a ojo que nada se entienda solo por el color: estado activo de filtros y menús, enlaces y avisos.

`CHROMIUM=/ruta/al/navegador` permite usar un Chromium ya instalado en lugar del de Playwright.
