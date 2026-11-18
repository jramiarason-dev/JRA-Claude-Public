/* =====================================================================
   CARTES (mini-carte & grande carte)
   ===================================================================== */
const MAP = { x0: -1100, x1: 1500, z0: -1000, z1: 1300, s: 0.5 };
let mapCanvas;
const LANDMARKS = [
  { n: 'Burj Khalifa', x: 8, z: 76, i: '🏙️' },
  { n: 'Sommet du Burj Khalifa', x: 0, z: 5.5, y: 470.2, i: '🗼' },
  { n: 'Dubai Mall', x: 120, z: -70, i: '🛍️' },
  { n: 'Fontaine de Dubaï', x: 0, z: 160, i: '⛲' },
  { n: 'Burj Al Arab', x: -462, z: -128, i: '⛵' },
  { n: 'Héliport du Burj Al Arab', x: -452, z: -160, y: 170.1, i: '🚁' },
  { n: 'Palm Jumeirah', x: -600, z: 261, i: '🌴' },
  { n: 'Atlantis', x: -857, z: 221, i: '🏨' },
  { n: 'Dubai Marina', x: -268, z: -300, i: '🛥️' },
  { n: 'Musée du Futur', x: -120, z: -70, i: '💍' },
  { n: 'Emirates Towers', x: -120, z: 52, i: '🔺' },
  { n: 'Coca-Cola Arena', x: 240, z: -190, i: '🎤' },
  { n: 'Dubai Frame', x: 360, z: 52, i: '🖼️' },
  { n: 'Sommet du Dubai Frame', x: 360, z: 0, y: 156.2, i: '🪂' },
  { n: 'Plage de Jumeirah', x: -322, z: 120, i: '🏖️' },
  { n: 'Héliport', x: 120, z: 120, i: '🚁' },
  { n: 'Aéroport international', x: 1010, z: -395, i: '✈️' },
  { n: 'Désert', x: 760, z: 75, i: '🏜️' },
  { n: 'Oasis', x: 900, z: -170, i: '🌴' },
  { n: 'Douane Dubaï ↔ Genève', x: 60, z: 530, i: '🛂' },
  { n: 'Genève — Mairie', x: 120, z: 575, i: '🏛️' },
  { n: "Jet d'eau", x: 60, z: 930, i: '⛲' },
  { n: 'Quai du Mont-Blanc', x: -100, z: 928, i: '🌊' },
  { n: 'Grand Hôtel du Lac', x: 0, z: 905, i: '🏨' },
  { n: 'Rue des horlogers', x: 120, z: 905, i: '⌚' },
  { n: 'Vieille ville — Cathédrale', x: 0, z: 682, i: '⛪' },
  { n: 'Palais des Nations', x: -120, z: 668, i: '🇺🇳' },
  { n: 'Stade de Genève', x: 360, z: 670, i: '🏟️' },
  { n: 'Horloge fleurie', x: -240, z: 805, i: '🌼' },
  { n: 'Hôpital', x: 240, z: 575, i: '🏥' },
  { n: 'Police', x: 360, z: 575, i: '👮' },
  { n: 'Caserne des pompiers', x: 480, z: 575, i: '🚒' },
  { n: 'Poste', x: 0, z: 575, i: '📮' },
  { n: 'Gare routière', x: -240, z: 590, i: '🚌' },
  { n: 'Fermes', x: 700, z: 790, i: '🐄' },
  { n: 'Vignobles', x: 1285, z: 785, i: '🍇' },
];
const toMap = (x, z) => [(x - MAP.x0) * MAP.s, (z - MAP.z0) * MAP.s];
function buildMapCanvas() {
  const W = (MAP.x1 - MAP.x0) * MAP.s, H = (MAP.z1 - MAP.z0) * MAP.s, c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d'), s = MAP.s;
  g.fillStyle = '#e4cd99'; g.fillRect(0, 0, W, H);
  g.fillStyle = '#2b9fc4'; g.fillRect(0, 0, (SHORE - MAP.x0) * s, H);
  // îles (échantillonnage)
  g.fillStyle = '#ecdcb0';
  for (let x = MAP.x0; x < SHORE; x += 4) for (let z = MAP.z0; z < MAP.z1; z += 4) if (onIsland(x, z)) { const [px, pz] = toMap(x, z); g.fillRect(px, pz, 2.2, 2.2); }
  g.fillStyle = '#f0dcae'; { const [a, b] = toMap(SHORE, MAP.z0); g.fillRect(a, b, 31 * s, H); }
  g.fillStyle = '#2b9fc4'; { const [a, b] = toMap(SHORE, LAKE_Z); g.fillRect(a, b, W, H); }
  g.fillStyle = '#9cc77a'; { const [a, b] = toMap(556, GVA_Z); g.fillRect(a, b, (MAP.x1 - 556) * s, (LAKE_Z - GVA_Z) * s); }
  for (const f of mapFeatures.rects) { g.fillStyle = f.c; const [a, b] = toMap(f.x0, f.z0); g.fillRect(a, b, (f.x1 - f.x0) * s, (f.z1 - f.z0) * s); }
  for (const f of mapFeatures.fields) { g.fillStyle = f.c; const [a, b] = toMap(f.x0, f.z0); g.fillRect(a, b, (f.x1 - f.x0) * s, (f.z1 - f.z0) * s); }
  g.fillStyle = '#d2cabd'; { const [a, b] = toMap(-310, 552); g.fillRect(a, b, 865 * s, (LAKE_Z - 552) * s); }
  g.fillStyle = '#d6cfc2'; { const [a, b] = toMap(-310, -555); g.fillRect(a, b, 865 * s, 1110 * s); }
  g.fillStyle = '#6bab55'; for (const p of mapFeatures.parks) { const [a, b] = toMap(p.x - 44, p.z - 44); g.fillRect(a, b, 88 * s, 88 * s); }
  { const [a, b] = toMap(316, -44); g.fillRect(a, b, 88 * s, 88 * s); }
  g.fillStyle = '#2bb3c8'; for (const p of mapFeatures.ponds) { const [a, b] = toMap(p.x, p.z); g.beginPath(); g.arc(a, b, p.r * s, 0, 7); g.fill(); }
  g.strokeStyle = '#45454b'; g.lineWidth = ROAD_W * s; g.lineCap = 'square';
  for (const x of ROADS_X) { g.beginPath(); g.moveTo(...toMap(x, -549)); g.lineTo(...toMap(x, 909)); g.stroke(); }
  g.beginPath(); g.moveTo(...toMap(549, 780)); g.lineTo(...toMap(1460, 780)); g.stroke();
  for (const z of ROADS_Z) { g.beginPath(); g.moveTo(...toMap(-309, z)); g.lineTo(...toMap(549, z)); g.stroke(); }
  g.beginPath(); g.moveTo(...toMap(540, HWY_Z)); g.lineTo(...toMap(1500, HWY_Z)); g.stroke();
  g.lineWidth = 12 * s; g.beginPath(); g.moveTo(...toMap(-340, -160)); g.lineTo(...toMap(-440, -160)); g.stroke();
  g.beginPath(); g.moveTo(...toMap(-340, 261)); g.lineTo(...toMap(-580, 261)); g.stroke();
  for (const b of mapFeatures.buildings) {
    const t = clamp(b.h / 300, 0, 1); g.fillStyle = `rgb(${150 - t * 70},${158 - t * 70},${172 - t * 60})`;
    if (b.t === 'cyl') { const [a, bb] = toMap(b.x, b.z); g.beginPath(); g.arc(a, bb, b.r * s, 0, 7); g.fill(); }
    else { const [a, bb] = toMap(b.x - b.w / 2, b.z - b.d / 2); g.fillRect(a, bb, b.w * s, b.d * s); }
  }
  mapCanvas = c;
}
const mm = $('minimap').getContext('2d');
function drawArrow(g, x, y, ang, size, col) {
  g.save(); g.translate(x, y); g.rotate(ang); g.fillStyle = col; g.strokeStyle = '#000'; g.lineWidth = size * 0.18;
  g.beginPath(); g.moveTo(0, -size); g.lineTo(size * 0.7, size * 0.8); g.lineTo(0, size * 0.4); g.lineTo(-size * 0.7, size * 0.8); g.closePath(); g.fill(); g.stroke(); g.restore();
}
function drawMinimap() {
  const W = 360, k = 1.5, pp = P.vehicle ? P.vehicle.pos : P.pos, yaw = P.vehicle ? P.vehicle.yaw : P.yaw;
  const [px, pz] = toMap(pp.x, pp.z);
  mm.save(); mm.clearRect(0, 0, W, W); mm.beginPath(); mm.arc(W / 2, W / 2, W / 2, 0, 7); mm.clip();
  mm.fillStyle = '#2b9fc4'; mm.fillRect(0, 0, W, W);
  mm.translate(W / 2, W / 2); mm.rotate(CAM.yaw - Math.PI); mm.scale(k, k);
  mm.drawImage(mapCanvas, -px, -pz);
  for (const v of vehicles) { if (v === P.vehicle) continue; const [a, b] = toMap(v.pos.x, v.pos.z); mm.fillStyle = v.driver === 'ai' ? 'rgba(255,255,255,.75)' : '#f0bf62'; mm.fillRect(a - px - 1.5, b - pz - 1.5, 3, 3); }
  mm.font = '14px sans-serif'; mm.textAlign = 'center'; mm.textBaseline = 'middle';
  for (const l of LANDMARKS) { if (l.y) continue; const [a, b] = toMap(l.x, l.z); if (Math.abs(a - px) < 140 && Math.abs(b - pz) < 140) { mm.save(); mm.translate(a - px, b - pz); mm.rotate(-(CAM.yaw - Math.PI)); mm.fillText(l.i, 0, 0); mm.restore(); } }
  drawRoute(mm, px, pz, 1, 3.5);
  drawArrow(mm, 0, 0, Math.PI - yaw, 8, '#f0bf62');
  mm.restore();
  // Nord
  const na = CAM.yaw - Math.PI, nx = W / 2 + Math.sin(-na) * -0 , r = W / 2 - 18;
  const nv = { x: 0, y: -1 }; const ca = Math.cos(na), sa = Math.sin(na);
  const tx = W / 2 + (nv.x * ca - nv.y * sa) * r, ty = W / 2 + (nv.x * sa + nv.y * ca) * r;
  mm.fillStyle = '#000a'; mm.beginPath(); mm.arc(tx, ty, 14, 0, 7); mm.fill(); mm.fillStyle = '#fff'; mm.font = 'bold 16px sans-serif'; mm.textAlign = 'center'; mm.textBaseline = 'middle'; mm.fillText('N', tx, ty + 1);
}
function drawBigMap() {
  const c = $('bigCanvas'), r = c.getBoundingClientRect(), dpr = Math.min(devicePixelRatio, 2);
  c.width = r.width * dpr; c.height = r.height * dpr; const g = c.getContext('2d'); g.scale(dpr, dpr);
  const sc = Math.min(r.width / mapCanvas.width, r.height / mapCanvas.height), ox = (r.width - mapCanvas.width * sc) / 2, oy = (r.height - mapCanvas.height * sc) / 2;
  c._xf = { sc, ox, oy };
  g.fillStyle = '#e4cd99'; g.fillRect(0, 0, r.width, r.height); g.fillStyle = '#2b9fc4'; g.fillRect(0, 0, ox + (SHORE - MAP.x0) * MAP.s * sc, r.height); g.fillRect(0, oy + (LAKE_Z - MAP.z0) * MAP.s * sc, r.width, r.height);
  g.drawImage(mapCanvas, ox, oy, mapCanvas.width * sc, mapCanvas.height * sc);
  g.font = '600 12px Outfit, sans-serif'; g.textAlign = 'center';
  for (const l of LANDMARKS) { if (l.y) continue; const [a, b] = toMap(l.x, l.z); const x = ox + a * sc, y = oy + b * sc; g.font = '18px sans-serif'; g.fillText(l.i, x, y); g.font = '600 10px Outfit, sans-serif'; g.fillStyle = '#000'; g.fillText(l.n, x + 1, y + 17); g.fillStyle = '#fff'; g.fillText(l.n, x, y + 16); }
  const pp = P.vehicle ? P.vehicle.pos : P.pos, [a, b] = toMap(pp.x, pp.z);
  g.save(); g.translate(ox, oy); drawRoute(g, 0, 0, sc, 3); g.restore();
  drawArrow(g, ox + a * sc, oy + b * sc, Math.PI - (P.vehicle ? P.vehicle.yaw : P.yaw), 10, '#f0bf62');
}
$('bigCanvas').addEventListener('click', e => {
  const c = $('bigCanvas'), r = c.getBoundingClientRect(), { sc, ox, oy } = c._xf;
  const mx = (e.clientX - r.left - ox) / sc, mz = (e.clientY - r.top - oy) / sc;
  const x = mx / MAP.s + MAP.x0, z = mz / MAP.s + MAP.z0;
  if (x < BOUNDS.x0 || x > BOUNDS.x1 || z < BOUNDS.z0 || z > BOUNDS.z1) return;
  setWaypoint(x, z, 'Point de la carte'); drawBigMap();
});
