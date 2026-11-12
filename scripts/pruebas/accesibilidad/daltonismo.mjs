// Simulación de daltonismo (Machado et al., 2009, severidad máxima) sobre páginas de la web: una captura por tipo.
import { chromium } from 'playwright';
const BASE = (process.env.CADUS_URL || '').replace(/\/$/, '');
if (!BASE) { console.error('Indica la web: CADUS_URL=http://servidor/ruta node ' + process.argv[1].split(/[\\/]/).pop() + ' salida'); process.exit(1); }
const OUT = process.argv[2];
const M = {
  normal: null,
  protanopia: '0.152286 1.052583 -0.204868 0 0  0.114503 0.786281 0.099216 0 0  -0.003882 -0.048116 1.051998 0 0  0 0 0 1 0',
  deuteranopia: '0.367322 0.860646 -0.227968 0 0  0.280085 0.672501 0.047413 0 0  -0.011820 0.042940 0.968881 0 0  0 0 0 1 0',
  tritanopia: '1.255528 -0.076749 -0.178779 0 0  -0.078411 0.930809 0.147602 0 0  0.004733 0.691367 0.303900 0 0  0 0 0 1 0',
  acromatopsia: '0.299 0.587 0.114 0 0  0.299 0.587 0.114 0 0  0.299 0.587 0.114 0 0  0 0 0 1 0',
};
const PAGINAS = [['portada', '/'], ['actas', '/actas-y-normativa/'], ['delegaciones', '/delegaciones/']];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const p = await (await b.newContext({ viewport: { width: 1280, height: 800 }, reducedMotion: 'reduce' })).newPage();
for (const [nombre, ruta] of PAGINAS) {
  for (const [tipo, matriz] of Object.entries(M)) {
    await p.goto(BASE + ruta, { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(500);
    if (matriz) await p.evaluate(m => {
      const ns = 'http://www.w3.org/2000/svg';
      const svg = document.createElementNS(ns, 'svg'); svg.setAttribute('width', 0); svg.setAttribute('height', 0); svg.style.position = 'absolute';
      svg.innerHTML = `<filter id="cb" color-interpolation-filters="linearRGB"><feColorMatrix type="matrix" values="${m}"/></filter>`;
      document.body.appendChild(svg);
      document.documentElement.style.filter = 'url(#cb)';
    }, matriz);
    await p.waitForTimeout(200);
    await p.screenshot({ path: `${OUT}/${nombre}-${tipo}.png` });
  }
  console.log('capturas:', nombre);
}
await b.close();
