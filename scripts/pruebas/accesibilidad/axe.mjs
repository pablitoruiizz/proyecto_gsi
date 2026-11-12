// Auditoría axe-core (WCAG 2.1 A/AA) de las 19 páginas públicas, en escritorio y móvil.
import { chromium } from 'playwright';
const BASE = (process.env.CADUS_URL || '').replace(/\/$/, '');
if (!BASE) { console.error('Indica la web: CADUS_URL=http://servidor/ruta node ' + process.argv[1].split(/[\\/]/).pop() + ' salida'); process.exit(1); }
import { readFileSync, writeFileSync } from 'fs';
const AXE = readFileSync(new URL('./node_modules/axe-core/axe.min.js', import.meta.url), 'utf8');
const RUTAS = ['/', '/que-es-el-cadus/', '/que-es-el-cadus/gobierno-y-estatutos/', '/noticias/', '/comunicado-de-ejemplo-sobre-becas/',
  '/actas-y-normativa/', '/acta/acta-del-pleno-ordinario-ejemplo/', '/delegaciones/', '/delegacion/delegacion-de-facultad-de-ciencias-de-la-educacion/',
  '/atencion-al-estudiante/', '/atencion-al-estudiante/buzon-de-consultas/', '/atencion-al-estudiante/seguimiento-de-ticket/',
  '/atencion-al-estudiante/preguntas-frecuentes/', '/aviso-de-privacidad/', '/votaciones/', '/contacto/', '/eventos/',
  '/delegacion/delegacion-de-facultad-de-fisica/', '/acceso/'];
const OUT = process.argv[2];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const resumen = {};
for (const [disp, vp] of [['escritorio', { width: 1280, height: 900 }], ['movil', { width: 390, height: 844 }]]) {
  const ctx = await b.newContext({ viewport: vp, reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  for (const r of RUTAS) {
    await p.goto(BASE + r, { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(600);
    await p.addScriptTag({ content: AXE });
    const res = await p.evaluate(async () => (await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] } })).violations
      .map(v => ({ id: v.id, impacto: v.impact, ayuda: v.help, nodos: v.nodes.map(n => ({ sel: n.target.join(' '), html: n.html.slice(0, 160), msg: n.failureSummary.slice(0, 220) })) })));
    for (const v of res) {
      const k = v.id;
      resumen[k] ??= { ayuda: v.ayuda, impacto: v.impacto, paginas: {} };
      resumen[k].paginas[`${disp} ${r}`] = v.nodos;
    }
    console.log(`${disp} ${r}: ${res.length ? res.map(v => `${v.id}(${v.nodos.length})`).join(' ') : 'sin fallos'}`);
  }
  await ctx.close();
}
writeFileSync(OUT, JSON.stringify(resumen, null, 1));
await b.close();
