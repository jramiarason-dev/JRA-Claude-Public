// Test de fumée de Mirage City : charge le jeu dans Chromium (rendu logiciel),
// joue, entre dans un intérieur, ouvre le mode photo, capture, sauvegarde et reprend.
// Usage : node mirage_city/tests/smoke.mjs   (THREE_DIR=chemin/three pour servir Three.js en local)
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const server = createServer(async (req, res) => {
  try { res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }); res.end(await readFile(path.join(ROOT, 'index.html'))); }
  catch (e) { res.writeHead(500); res.end(String(e)); }
}).listen(0);
const url = `http://127.0.0.1:${server.address().port}/`;

const fails = [];
const check = (ok, msg) => { console.log(`${ok ? '✓' : '✗'} ${msg}`); if (!ok) fails.push(msg); };

const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await browser.newPage({ viewport: { width: 800, height: 450 } });
page.setDefaultTimeout(300000);
const errors = [];
page.on('pageerror', e => errors.push(e.message));
if (process.env.THREE_DIR) await page.route('https://cdn.jsdelivr.net/npm/three@0.160.0/**', r => r.fulfill({ path: path.join(process.env.THREE_DIR, r.request().url().split('three@0.160.0/')[1]), contentType: 'application/javascript' }));
await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
await page.addInitScript(() => { localStorage.setItem('mirage_gfx', 'standard'); localStorage.removeItem('mirage_save'); });

try {
  await page.goto(url);
  await page.waitForFunction(() => window.__mirage && window.__mirage.S.mode === 'creator', null, { timeout: 240000 });
  check(true, 'le monde se construit et le créateur de personnage s’affiche');

  await page.evaluate(() => document.getElementById('crPlay').click());
  await page.waitForFunction(() => window.__mirage.S.mode === 'play');
  check(true, 'la partie démarre');

  const inside = await page.evaluate(async () => {
    const m = window.__mirage; m.enterInterior(m.INTERIORS[0]);
    await new Promise(r => setTimeout(r, 2500));
    const it = m.P.inside, p = m.P.pos;
    return !!it && Math.abs(p.x - it.x) < it.w / 2 && Math.abs(p.z - it.z) < it.d / 2 && Math.abs(p.y + 300) < 0.5;
  });
  check(inside, 'le joueur entre dans le Dubai Mall et reste dans la salle');
  await page.evaluate(() => window.__mirage.exitInterior());

  const light = await page.evaluate(() => ['x', 'z'].map(a => window.__mirage.lightState(a)));
  check(light.every(s => ['r', 'y', 'g'].includes(s)) && !(light[0] === 'g' && light[1] === 'g'), `feux tricolores cohérents (${light})`);

  const photo = await page.evaluate(async () => {
    const m = window.__mirage; m.openPhotoMode(); m.PHOTO.filter = 2; m.PHOTO.capture = true;
    for (let i = 0; i < 100 && !document.querySelector('#photoShot img'); i++) await new Promise(r => setTimeout(r, 200));
    const img = document.querySelector('#photoShot img'); m.closePhotoMode();
    return img ? img.src.length : 0;
  });
  check(photo > 5000, `le mode photo produit une image (${photo} octets)`);

  const saved = await page.evaluate(() => { const m = window.__mirage; m.teleport(30, 60); m.saveGame(); const d = m.loadSave(); return d && Math.abs(d.pos[0] - 30) < 2 && Math.abs(d.pos[2] - 60) < 2; });
  check(saved, 'la sauvegarde enregistre la position');
} catch (e) {
  check(false, 'exception : ' + e.message);
}
check(errors.length === 0, `aucune erreur JavaScript${errors.length ? ' : ' + errors.slice(0, 3).join(' | ') : ''}`);
await browser.close(); server.close();
if (fails.length) { console.error(`\n${fails.length} échec(s)`); process.exit(1); }
console.log('\nTest de fumée réussi');
