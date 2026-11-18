/* =====================================================================
   MONUMENTS RECONNAISSABLES, FRONTIÈRE & AÉROPORT
   ===================================================================== */
const FLAGS = [];
function flagTex(draw) { return canvasTex(96, 64, draw, false); }
const FLAG_UAE = flagTex(g => { g.fillStyle = '#00732f'; g.fillRect(0, 0, 96, 22); g.fillStyle = '#fff'; g.fillRect(0, 21, 96, 22); g.fillStyle = '#000'; g.fillRect(0, 43, 96, 21); g.fillStyle = '#ff0000'; g.fillRect(0, 0, 26, 64); });
const FLAG_CH = flagTex(g => { g.fillStyle = '#e8112d'; g.fillRect(0, 0, 96, 64); g.fillStyle = '#fff'; g.fillRect(41, 12, 14, 40); g.fillRect(28, 25, 40, 14); });
const FLAG_MISC = [['#0055a4', '#fff', '#ef4135'], ['#000', '#dd0000', '#ffce00'], ['#009246', '#fff', '#ce2b37'], ['#00247d', '#fff', '#cf142b'], ['#ffcd00', '#003893', '#cf0921'], ['#006847', '#fff', '#ce1126'], ['#0038a8', '#fff', '#0038a8'], ['#5b92e5', '#fff', '#5b92e5']]
  .map(([a, b, c], i) => flagTex(g => { if (i % 2) { g.fillStyle = a; g.fillRect(0, 0, 96, 22); g.fillStyle = b; g.fillRect(0, 21, 96, 22); g.fillStyle = c; g.fillRect(0, 43, 96, 21); } else { g.fillStyle = a; g.fillRect(0, 0, 32, 64); g.fillStyle = b; g.fillRect(32, 0, 32, 64); g.fillStyle = c; g.fillRect(64, 0, 32, 64); } }));
const FLAG_MATS = new Map();
function flag(x, z, tex, h = 10, ry = 0) {
  DECO.add(new THREE.CylinderGeometry(0.08, 0.1, h, 6), '#d8dde3', x, h / 2, z);
  if (!FLAG_MATS.has(tex)) FLAG_MATS.set(tex, new THREE.MeshStandardMaterial({ map: tex, side: THREE.DoubleSide, roughness: 0.8 }));
  const g = new THREE.PlaneGeometry(2.4, 1.6, 8, 1); g.translate(1.2, 0, 0);
  const m = new THREE.Mesh(g, FLAG_MATS.get(tex)); m.position.set(x + 0.1, h - 0.9, z); m.rotation.y = ry; m.castShadow = true; scene.add(m);
  FLAGS.push({ m, base: g.attributes.position.array.slice(), ph: rand(0, 6) });
}
function updateFlags(time) {
  const cp = camera.position;
  for (const f of FLAGS) {
    if (Math.abs(f.m.position.x - cp.x) + Math.abs(f.m.position.z - cp.z) > 300) continue;
    const a = f.m.geometry.attributes.position;
    for (let i = 0; i < a.count; i++) { const x = f.base[i * 3]; a.setZ(i, Math.sin(time * 4 + x * 2.2 + f.ph) * 0.18 * (x / 2.4)); }
    a.needsUpdate = true;
  }
}
const SILVER_GLASS = new THREE.MeshStandardMaterial({ color: 0xc9d6e2, map: FACADES[1].map, emissiveMap: FACADES[1].em, emissive: 0xbfe0ff, emissiveIntensity: 0, roughness: 0.2, metalness: 0.5 });
BMATS.push(SILVER_GLASS);

/* ---------- Burj Khalifa : plan en Y, retraits en spirale, flèche */
function buildMegaTower() {
  const parts = [], LV = 10;
  const core = new THREE.CylinderGeometry(8.5, 13, 470, 6, 1); scaleCylUV(core, 12, 470, 6); core.translate(0, 235, 0); parts.push(core);
  for (let w = 0; w < 3; w++) {
    const ang = w * Math.PI * 2 / 3 + Math.PI / 2;
    for (let k = 0; k < LV; k++) {
      const L = 38 - k * 3.6, y0 = k === 0 ? 0 : k * 44 + w * 14, y1 = Math.min(468, (k + 1) * 44 + w * 14);
      if (L < 4 || y1 <= y0) continue;
      const g = new THREE.BoxGeometry(15 - k * 0.5, y1 - y0, L); scaleBoxUV(g, 15, y1 - y0, L);
      g.translate(0, (y0 + y1) / 2, L / 2 + 5); g.rotateY(Math.PI / 2 - ang); parts.push(g);
      const cap = new THREE.CylinderGeometry((15 - k * 0.5) / 2, (15 - k * 0.5) / 2, y1 - y0, 10, 1, false, 0, Math.PI); scaleCylUV(cap, 7, y1 - y0, 10);
      cap.translate(0, (y0 + y1) / 2, L + 5); cap.rotateY(Math.PI / 2 - ang); parts.push(cap);
    }
  }
  const m = new THREE.Mesh(mergeGeometries(parts), SILVER_GLASS); m.castShadow = m.receiveShadow = true; scene.add(m);
  for (let k = 0; k < LV; k++) addCollider({ t: 'cyl', x: 0, z: 0, r: Math.max(10, 38 - k * 3.6 + 5), y0: k * 44 - 5, y1: k * 44 + 44 + 28 > 470 ? 470 : k * 44 + 30 });
  TOWER_TOP = 470;
  const sp = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 4.5, 140, 10), new THREE.MeshStandardMaterial({ color: 0xe2e8ee, metalness: 0.6, roughness: 0.25 }));
  sp.position.set(0, 540, 0); scene.add(sp);
  const beacon = new THREE.Mesh(new THREE.SphereGeometry(1.4, 8, 6), new THREE.MeshBasicMaterial({ color: 0xff3030, toneMapped: false }));
  beacon.position.set(0, 611, 0); scene.add(beacon);
  plane(96, 96, STONE_MAT, 0, 0.06, 0);
  for (let a = 0; a < 6.28; a += 0.4) addPalm(Math.cos(a) * 42, Math.sin(a) * 42);
  mapFeatures.buildings.push({ t: 'cyl', x: 0, z: 0, r: 40, h: 470 });
}

/* ---------- Dubai Mall */
function buildMall(cx, cz) {
  addBoxBuilding(cx, cz, 84, 84, 24, BMATS[3]);
  const dome = new THREE.Mesh(new THREE.SphereGeometry(20, 24, 12, 0, 6.28, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0x9fd0e6, roughness: 0.05, metalness: 0.6, transparent: true, opacity: 0.85 }));
  dome.position.set(cx, 24, cz); scene.add(dome);
  for (const [x, z, ry] of [[cx, cz + 42.1, 0], [cx - 42.1, cz, -Math.PI / 2], [cx, cz - 42.1, Math.PI]]) {
    addLocal(DECO, new THREE.BoxGeometry(40, 14, 0.4), '#1d2836', 0, 9, 0.2, ry, x, z);
    addLocal(DECO, new THREE.BoxGeometry(46, 0.6, 9), '#e8e2d4', 0, 6.5, 4.5, ry, x, z);
    for (const s of [-1, 1]) addLocal(DECO, new THREE.CylinderGeometry(0.4, 0.4, 6.5, 10), '#c9a24a', s * 20, 3.25, 8.5, ry, x, z);
    signOnly(x, z, ry, 19, 'DUBAI MALL', 22, 3.4);
  }
}

/* ---------- Burj Al Arab : exosquelette, mât, restaurant suspendu */
function buildBurjAlArabDetails() {
  const B = new GeoBag();
  const P = t => { const u = 1 - t; return [u * u * 0 + 2 * u * t * 78 + t * t * 62, u * u * 200 + 2 * u * t * 120 + t * t * 0]; };
  for (const zs of [-19, 19]) {
    let prev = P(0);
    for (let i = 1; i <= 14; i++) {
      const cur = P(i / 14), a = new V3(-470 - prev[0] - 2, prev[1], -160 + zs), b = new V3(-470 - cur[0] - 2, cur[1], -160 + zs);
      const d = b.clone().sub(a), g = new THREE.CylinderGeometry(1.4, 1.4, d.length() + 1, 8);
      g.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(new V3(0, 1, 0), d.normalize()));
      B.add(g, '#f4f4f2', (a.x + b.x) / 2, (a.y + b.y) / 2, (a.z + b.z) / 2);
      if (i % 2 === 0) B.add(new THREE.CylinderGeometry(0.6, 0.6, 38, 6), '#f4f4f2', b.x, b.y, -160, Math.PI / 2);
      prev = cur;
    }
  }
  for (let y = 20; y < 200; y += 20) B.box(4, 1.2, 40, '#e8e8e6', -466, y, -160);
  B.box(26, 6, 14, '#f4f4f2', -545, 190, -160); B.box(26.4, 2, 14.4, '#3aa6c8', -545, 189, -160);
  B.add(new THREE.CylinderGeometry(2.5, 2.5, 30, 10), '#e8e8e6', -470, 230, -160);
  const m = B.mesh(VC_MAT); scene.add(m);
  addCollider({ t: 'box', x0: -558, x1: -532, z0: -167, z1: -153, y0: 186, y1: 193 });
}

/* ---------- Atlantis sur le croissant de Palm Jumeirah */
function buildAtlantis() {
  const cx = PALM_C.x - 221, cz = PALM_C.z, mat = mkFacMat(0xeaa98c, 0, 0.6);
  BMATS.push(mat);
  for (const s of [-1, 1]) { addBoxBuilding(cx, cz + s * 26, 16, 22, 62, mat); DECO.add(new THREE.CylinderGeometry(4, 4, 8, 12), '#e0b25a', cx, 66, cz + s * 26); DECO.add(new THREE.SphereGeometry(4, 12, 6, 0, 6.28, 0, Math.PI / 2), '#e0b25a', cx, 70, cz + s * 26); }
  addBoxBuilding(cx, cz, 16, 30, 14, mat); addBoxBuilding(cx, cz, 16, 30, 16, mat, 46);
  const arch = new THREE.Mesh(new THREE.TorusGeometry(13, 2.4, 8, 24, Math.PI), new THREE.MeshStandardMaterial({ color: 0xe0b25a, metalness: 0.4, roughness: 0.4 }));
  arch.position.set(cx, 32, cz); arch.rotation.y = Math.PI / 2; scene.add(arch);
  for (const s of [-1, 1]) for (let i = 0; i < 6; i++) addPalm(cx + rand(-10, 10), cz + s * (45 + i * 6));
  signOnly(cx - 8.1, cz, -Math.PI / 2, 10, 'ATLANTIS', 12, 2.4);
}

/* ---------- Musée du Futur (anneau calligraphié) */
const CALLI_TEX = canvasTex(256, 128, (g) => {
  g.fillStyle = '#000'; g.fillRect(0, 0, 256, 128); g.strokeStyle = '#ffffff'; g.lineCap = 'round';
  for (let i = 0; i < 60; i++) { g.lineWidth = rand(1.5, 4); g.beginPath(); let x = rand(0, 256), y = rand(10, 118); g.moveTo(x, y); for (let k = 0; k < 4; k++) { x += rand(-20, 20); y += rand(-10, 10); g.quadraticCurveTo(x + rand(-10, 10), y + rand(-10, 10), x, y); } g.stroke(); }
});
function buildMuseumFuture(cx, cz) {
  const hill = new THREE.Mesh(new THREE.SphereGeometry(36, 24, 12, 0, 6.28, 0, Math.PI / 2), GRASS_MAT); hill.scale.set(1.15, 0.25, 0.7); hill.position.set(cx, 0, cz); hill.receiveShadow = true; scene.add(hill);
  const g = new THREE.TorusGeometry(24, 10, 28, 56); g.scale(1.3, 1, 1);
  const map = canvasTex(256, 128, (gg) => { gg.drawImage(CALLI_TEX.image, 0, 0); const d = gg.getImageData(0, 0, 256, 128); for (let i = 0; i < d.data.length; i += 4) { const v = d.data[i]; d.data[i] = d.data[i + 1] = d.data[i + 2] = 235 - v * 0.75; } gg.putImageData(d, 0, 0); });
  map.repeat.set(4, 1); const em = CALLI_TEX.clone(); em.needsUpdate = true; em.repeat.set(4, 1);
  const m = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: 0xe6eaee, metalness: 0.55, roughness: 0.22, map, emissiveMap: em, emissive: 0xffe3b0, emissiveIntensity: 0 }));
  m.position.set(cx, 36, cz); m.castShadow = true; scene.add(m); BMATS.push(m.material);
  for (const s of [-1, 1]) addCollider({ t: 'box', x0: cx + s * 26 - 9, x1: cx + s * 26 + 9, z0: cz - 10, z1: cz + 10, y0: -5, y1: 60 });
  addCollider({ t: 'box', x0: cx - 30, x1: cx + 30, z0: cz - 10, z1: cz + 10, y0: 56, y1: 70 });
  mapFeatures.buildings.push({ t: 'box', x: cx, z: cz, w: 80, d: 20, h: 70 });
  signOnly(cx, cz + 10.5, 0, 3, 'MUSÉE DU FUTUR', 12, 1.8);
}

/* ---------- Emirates Towers (deux tours triangulaires) */
function buildEmiratesTowers(cx, cz) {
  plane(88, 88, STONE_MAT, cx, 0.05, cz);
  for (const [x, z, r, h] of [[cx - 16, cz - 12, 17, 300], [cx + 18, cz + 16, 14, 255]]) {
    const g = new THREE.CylinderGeometry(r, r, h, 3, 1); scaleCylUV(g, r, h, 3); g.rotateY(0.5);
    const m = new THREE.Mesh(g, SILVER_GLASS); m.position.set(x, h / 2, z); m.castShadow = m.receiveShadow = true; scene.add(m);
    const top = new THREE.Mesh(new THREE.ConeGeometry(r, 40, 3), SILVER_GLASS); top.rotation.y = 0.5; top.position.set(x, h + 20, z); scene.add(top);
    DECO.add(new THREE.CylinderGeometry(0.3, 0.8, 30, 6), '#d8dde3', x, h + 52, z);
    addCollider({ t: 'cyl', x, z, r: r * 0.8, y0: -5, y1: h });
    mapFeatures.buildings.push({ t: 'cyl', x, z, r: r * 0.8, h });
  }
  addBoxBuilding(cx, cz + 30, 40, 18, 14, BMATS[3]);
}

/* ---------- Arène (Coca-Cola Arena) */
const LED_TEX = canvasTex(256, 64, (g) => { for (let x = 0; x < 256; x += 4) { const h = (x / 256 * 360 + 200) % 360; g.fillStyle = `hsl(${h},90%,${50 + 20 * Math.sin(x / 9)}%)`; g.fillRect(x, 0, 4, 64); } }, true);
function buildArena(cx, cz) {
  plane(88, 88, ASPHALT_MAT, cx, 0.045, cz);
  addBoxBuilding(cx, cz, 80, 66, 30, mkFacMat(0x3a3f48, 2, 0.4));
  const led = new THREE.MeshStandardMaterial({ color: 0x111111, emissiveMap: LED_TEX, emissive: 0xffffff, emissiveIntensity: 1.2, roughness: 0.3 });
  const band = new THREE.Mesh(new THREE.BoxGeometry(80.6, 6, 66.6), led); band.position.set(cx, 22, cz); scene.add(band); ARENA_LED.push(LED_TEX);
  for (const [x, z, ry] of [[cx, cz - 33.2, Math.PI], [cx, cz + 33.2, 0]]) { signOnly(x, z, ry, 12, 'ARENA', 18, 3.6); addLocal(DECO, new THREE.BoxGeometry(30, 0.6, 8), '#d9dde2', 0, 7, 4, ry, x, z); }
}
const ARENA_LED = [];

/* ---------- Stade de Genève */
const PITCH_TEX = canvasTex(256, 160, (g) => {
  for (let i = 0; i < 10; i++) { g.fillStyle = i % 2 ? '#3f8f3a' : '#4a9e43'; g.fillRect(i * 25.6, 0, 25.6, 160); }
  g.strokeStyle = '#f4f4f4'; g.lineWidth = 2; g.strokeRect(8, 8, 240, 144); g.beginPath(); g.moveTo(128, 8); g.lineTo(128, 152); g.stroke(); g.beginPath(); g.arc(128, 80, 22, 0, 7); g.stroke();
  g.strokeRect(8, 46, 34, 68); g.strokeRect(214, 46, 34, 68); g.strokeRect(8, 64, 12, 32); g.strokeRect(236, 64, 12, 32);
}, false);
function buildStadium(cx, cz) {
  plane(88, 88, ASPHALT_MAT, cx, 0.045, cz);
  const p = plane(60, 38, new THREE.MeshStandardMaterial({ map: PITCH_TEX, roughness: 0.9 }), cx, 0.07, cz);
  const st = mkFacMat(0x9aa3ad, 2, 0.7);
  for (const [x, z, w, d, ry] of [[cx, cz - 31, 74, 12, 0], [cx, cz + 31, 74, 12, Math.PI], [cx - 39, cz, 12, 50, Math.PI / 2], [cx + 39, cz, 12, 50, -Math.PI / 2]]) {
    const len = Math.max(w, d), g = new GeoBag();
    for (let r = 0; r < 8; r++) g.box(len, 1.4, 1.5, r % 2 ? '#c8102e' : '#9b0d24', 0, 1 + r * 1.5, -r * 1.4);
    g.box(len, 13, 1, '#5a6068', 0, 6.5, -11.5); g.box(len + 2, 0.5, 13, '#d8dde3', 0, 15.5, -5.5);
    const m = g.mesh(VC_MAT); m.position.set(x, 0, z); m.rotation.y = ry; scene.add(m);
    addCollider({ t: 'box', x0: x - w / 2, x1: x + w / 2, z0: z - d / 2, z1: z + d / 2, y0: -5, y1: 13 });
  }
  for (const [sx, sz] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) {
    const x = cx + sx * 42, z = cz + sz * 40; DECO.add(new THREE.CylinderGeometry(0.4, 0.6, 30, 8), '#c9ccd1', x, 15, z);
    DECO.box(5, 3, 0.6, '#3a3f46', x, 30, z); LIGHTS.box(4.6, 2.6, 0.3, '#fff6d8', x, 30, z - sz * 0.4);
  }
  for (const s of [-1, 1]) { DECO.box(0.15, 2.4, 7.3, '#ffffff', cx + s * 29.6, 1.2, cz); }
  signOnly(cx, cz - 43.8, Math.PI, 17, 'STADE', 12, 2.4);
  mapFeatures.parks.push({ x: cx, z: cz });
}

/* ---------- Palais des Nations + chaise cassée */
function buildPalaisNations(cx, cz) {
  plane(88, 88, GRASS_MAT, cx, 0.05, cz);
  const wm = mkFacMat(0xf2efe8, 0, 0.7); BMATS.push(wm);
  addBoxBuilding(cx, cz + 30, 84, 22, 22, wm);
  for (const s of [-1, 1]) addBoxBuilding(cx + s * 34, cz + 4, 16, 34, 18, wm);
  for (let i = -6; i <= 6; i++) DECO.add(new THREE.CylinderGeometry(0.7, 0.8, 16, 12), '#f6f4ee', cx + i * 5.5, 8, cz + 18.6);
  DECO.box(84, 1.2, 4, '#e8e4da', cx, 16.6, cz + 18.6);
  plane(14, 60, COBBLE_MAT, cx, 0.06, cz - 14);
  for (let i = 0; i < 10; i++) for (const s of [-1, 1]) flag(cx + s * 8, cz - 40 + i * 6, FLAG_MISC[(i * 2 + (s > 0 ? 1 : 0)) % FLAG_MISC.length], 9);
  // chaise cassée (sculpture monumentale)
  const c = new GeoBag(), x = cx - 30, z = cz - 32;
  c.box(6, 1, 6, '#8a5a34', x, 9, z); c.box(6, 9, 0.8, '#8a5a34', x, 13.5, z - 2.6);
  for (const [lx, lz, h] of [[-2.6, -2.6, 9], [2.6, -2.6, 9], [-2.6, 2.6, 9], [2.6, 2.6, 4]]) c.box(0.8, h, 0.8, '#8a5a34', x + lx, h / 2 + (h < 9 ? 5 : 0), z + lz);
  scene.add(c.mesh(VC_MAT));
  addCollider({ t: 'box', x0: x - 3, x1: x + 3, z0: z - 3, z1: z + 3, y0: -5, y1: 9.5 });
  signOnly(cx, cz + 18.7 - 0.1, Math.PI, 18.5, 'PALAIS DES NATIONS', 22, 2.4);
}

/* ---------- Grands hôtels du quai & rue des horlogers */
function buildGrandHotel(cx, cz, name) {
  genevaBlock(cx, cz, true);
  const fz = cz + 44.3;
  signOnly(cx, fz, 0, 24, name, 26, 3.2);
  addLocal(DECO, new THREE.BoxGeometry(18, 0.5, 6), '#7a1f2b', 0, 4.2, 3, 0, cx, fz);
  for (const s of [-1, 1]) addLocal(DECO, new THREE.CylinderGeometry(0.25, 0.25, 4.2, 8), '#c9a24a', s * 8.5, 2.1, 5.8, 0, cx, fz);
  plane(6, 8, new THREE.MeshStandardMaterial({ color: 0x9b1b2a, roughness: 1 }), cx, 0.07, fz + 4);
  for (const s of [-2, -1, 0, 1, 2]) flag(cx + s * 9, fz - 7.5, s % 2 ? FLAG_CH : FLAG_MISC[(s + 5) % FLAG_MISC.length], 6, 0);
}
function watchStreet(cx, cz) {
  genevaBlock(cx, cz, true);
  for (const s of [-1, 1]) {
    const x = cx + s * 30, z = cz + 49;
    DECO.add(new THREE.CylinderGeometry(0.18, 0.22, 4.2, 10), '#1f3a2b', x, 2.1, z); DECO.add(new THREE.CylinderGeometry(0.75, 0.75, 0.3, 20), '#1f3a2b', x, 4.6, z, Math.PI / 2);
    const cl = new THREE.Mesh(new THREE.CircleGeometry(0.66, 20), new THREE.MeshStandardMaterial({ map: CLOCK_TEX })); cl.position.set(x, 4.6, z + 0.16); scene.add(cl);
    clockHand(x, 4.6, z + 0.18, 0, 0.6);
  }
}

/* ---------- Frontière Dubaï ↔ Genève : mur, postes de douane, barrières */
const BARRIERS = [];
function buildBorder() {
  const zW = 552;
  // mur entre les routes
  for (let i = 0; i < ROADS_X.length - 1; i++) {
    const a = ROADS_X[i] + 14, b = ROADS_X[i + 1] - 14, x = (a + b) / 2;
    DECO.box(b - a, 3.2, 0.7, '#cfc6b4', x, 1.6, zW); DECO.box(b - a, 1.4, 0.15, '#6b7078', x, 3.9, zW);
    for (let t = a; t <= b; t += 4) DECO.box(0.12, 1.5, 0.12, '#6b7078', t, 3.9, zW);
    addCollider({ t: 'box', x0: a, x1: b, z0: zW - 0.4, z1: zW + 0.4, y0: -5, y1: 3.2 });
  }
  addCollider({ t: 'box', x0: -345, x1: -312, z0: zW - 0.4, z1: zW + 0.4, y0: -5, y1: 3.2 }); DECO.box(33, 3.2, 0.7, '#cfc6b4', -328.5, 1.6, zW);
  // postes de douane sur chaque route nord-sud
  for (const x of ROADS_X) {
    DECO.box(24, 0.6, 12, '#e9edf2', x, 6.4, zW); DECO.box(24.2, 1.2, 12.2, '#1f3a6b', x, 7.2, zW);
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) DECO.add(new THREE.CylinderGeometry(0.3, 0.3, 6.4, 8), '#9aa1ab', x + sx * 11, 3.2, zW + sz * 5.5);
    DECO.box(2.6, 2.8, 3.4, '#f4f4f4', x, 1.4, zW); DECO.box(2.7, 0.8, 3.5, '#1f3a6b', x, 2.6, zW); DECO.box(2.62, 1, 0.05, '#7fb8d8', x, 1.8, zW + 1.71);
    addCollider({ t: 'box', x0: x - 1.4, x1: x + 1.4, z0: zW - 1.8, z1: zW + 1.8, y0: -5, y1: 2.8 });
    signOnly(x, zW - 6.1, Math.PI, 7.2, 'DOUANE · CUSTOMS', 14, 1.1); signOnly(x, zW + 6.1, 0, 7.2, 'DOUANE · CUSTOMS', 14, 1.1);
    for (const dir of [-1, 1]) { // une barrière par voie
      const piv = new THREE.Group(); piv.position.set(x + dir * 1.4, 1.1, zW + dir * 1.3);
      const arm = new THREE.Mesh(new THREE.BoxGeometry(7.4, 0.18, 0.18), new THREE.MeshStandardMaterial({ map: canvasTex(64, 8, (g) => { for (let i = 0; i < 8; i++) { g.fillStyle = i % 2 ? '#d01c2b' : '#ffffff'; g.fillRect(i * 8, 0, 8, 8); } }, false) }));
      arm.position.x = dir * 3.7; piv.add(arm); scene.add(piv);
      BARRIERS.push({ piv, x: x + dir * 4.5, z: zW, dir, open: 0 });
    }
    flag(x - 13, zW - 6, FLAG_UAE, 10); flag(x + 13, zW + 6, FLAG_CH, 10);
  }
  signOnly(60, 540 - 9.6, Math.PI, 9, 'BIENVENUE À GENÈVE', 20, 2.4);
  signOnly(60, 660 + 9.6, 0, 9, 'WELCOME TO DUBAI', 20, 2.4);
  for (const [x, z, ry, n] of [[60, 530.4, Math.PI, 'BIENVENUE À GENÈVE'], [60, 669.6, 0, 'WELCOME TO DUBAI']]) { for (const s of [-1, 1]) DECO.add(new THREE.CylinderGeometry(0.25, 0.25, 9, 8), '#5a6068', x + s * 10, 4.5, z); }
  mapFeatures.rects.push({ x0: -345, z0: zW - 1.5, x1: 549, z1: zW + 1.5, c: '#8a2b2b' });
}
function updateBarriers(dt) {
  for (const b of BARRIERS) {
    let near = false;
    const pp = P.vehicle ? P.vehicle.pos : P.pos;
    if (Math.abs(pp.x - b.x) < 6 && Math.abs(pp.z - b.z) < 22) near = true;
    if (!near) for (const v of vehicles) if (Math.abs(v.pos.x - b.x) < 5 && Math.abs(v.pos.z - b.z) < 20) { near = true; break; }
    b.open = clamp(b.open + (near ? 2.2 : -0.8) * dt, 0, 1);
    b.piv.rotation.z = b.dir * smooth(0, 1, b.open) * 1.45;
  }
}

/* ---------- Aéroport international (désert, au sud de l'autoroute) */
const AIRPORT = { x0: 640, x1: 1420, z0: -740, z1: -360 };
function airportMask(x, z) {
  const dx = Math.max(0, AIRPORT.x0 - x, x - AIRPORT.x1), dz = Math.max(0, AIRPORT.z0 - z, z - AIRPORT.z1);
  let m = smooth(0, 70, Math.hypot(dx, dz));
  if (z > AIRPORT.z1 - 10 && z < HWY_Z) m *= smooth(14, 40, Math.abs(x - 700));
  return m;
}
const RUNWAY_TEX = canvasTex(64, 512, (g) => {
  g.fillStyle = '#3a3b40'; g.fillRect(0, 0, 64, 512);
  g.fillStyle = '#f2f2f2'; for (let y = 40; y < 472; y += 36) g.fillRect(30, y, 4, 20);
  for (let i = 0; i < 6; i++) { g.fillRect(4 + i * 10, 6, 6, 26); g.fillRect(4 + i * 10, 480, 6, 26); }
  g.fillRect(1, 0, 2, 512); g.fillRect(61, 0, 2, 512);
}, false);
function buildAirport() {
  const cxA = (AIRPORT.x0 + AIRPORT.x1) / 2;
  plane(AIRPORT.x1 - AIRPORT.x0, AIRPORT.z1 - AIRPORT.z0, new THREE.MeshStandardMaterial({ color: 0xc9c3b4, roughness: 0.95, userData: { pbr: 'paving' } }), cxA, 0.02, (AIRPORT.z0 + AIRPORT.z1) / 2);
  const rw = plane(46, 720, new THREE.MeshStandardMaterial({ map: RUNWAY_TEX, roughness: 0.9 }), cxA, 0.05, -660); rw.rotation.z = Math.PI / 2;
  plane(600, 18, ASPHALT_MAT, cxA, 0.045, -600);
  plane(420, 70, ASPHALT_MAT, 1010, 0.045, -520);
  const t = roadTex.clone(); t.needsUpdate = true; t.repeat.set(1, 420 / 22);
  plane(14, 420, new THREE.MeshStandardMaterial({ map: t, roughness: 0.9 }), 700, 0.035, -150);
  mapFeatures.rects.push({ x0: AIRPORT.x0, z0: AIRPORT.z0, x1: AIRPORT.x1, z1: AIRPORT.z1, c: '#cfc8b8' }, { x0: cxA - 360, z0: -683, x1: cxA + 360, z1: -637, c: '#45454b' }, { x0: 693, z0: -360, x1: 707, z1: 60, c: '#45454b' });
  // terminal à toit ondulé
  const tm = mkFacMat(0xbfd3e0, 1, 0.15); BMATS.push(tm);
  addBoxBuilding(1010, -440, 280, 50, 20, tm);
  const roof = new THREE.Mesh(new THREE.CylinderGeometry(40, 40, 290, 24, 1, false, -0.7, 1.4), new THREE.MeshStandardMaterial({ color: 0xeef1f4, metalness: 0.4, roughness: 0.3, side: THREE.DoubleSide }));
  roof.rotation.z = Math.PI / 2; roof.scale.set(1, 1, 0.75); roof.position.set(1010, -10, -440); scene.add(roof);
  signOnly(1010, -465.2, Math.PI, 15, 'AÉROPORT', 24, 3.6); signOnly(1010, -414.8, 0, 15, 'TERMINAL 1', 20, 3);
  for (let i = 0; i < 5; i++) { const x = 900 + i * 55; DECO.box(4, 4, 30, '#d8dde3', x, 5, -480); DECO.box(5, 5, 5, '#b8bec6', x, 5, -497); }
  // tour de contrôle
  addCylBuilding(830, -470, 5, 52, mkFacMat(0xd8dde3, 2, 0.5));
  const cab = new THREE.Mesh(new THREE.CylinderGeometry(10, 8, 9, 12), new THREE.MeshStandardMaterial({ color: 0x1d2836, metalness: 0.6, roughness: 0.1 })); cab.position.set(830, 56.5, -470); scene.add(cab);
  DECO.add(new THREE.CylinderGeometry(11, 11, 1.2, 12), '#e9edf2', 830, 61.5, -470); addCollider({ t: 'cyl', x: 830, z: -470, r: 10, y0: 51, y1: 62 });
  LIGHTS.add(new THREE.SphereGeometry(0.6, 8, 6), '#ff2a1a', 830, 66, -470); DECO.add(new THREE.CylinderGeometry(0.2, 0.2, 4, 6), '#aaa', 830, 64, -470);
  // hangars
  for (let i = 0; i < 3; i++) { const x = 1250 + i * 55; const h = new THREE.Mesh(new THREE.CylinderGeometry(22, 22, 40, 20, 1, false, -Math.PI / 2, Math.PI), new THREE.MeshStandardMaterial({ color: 0xa8b0ba, metalness: 0.6, roughness: 0.4, side: THREE.DoubleSide })); h.rotation.x = Math.PI / 2; h.rotation.z = Math.PI / 2; h.position.set(x, 0, -430); scene.add(h); addCollider({ t: 'box', x0: x - 22, x1: x + 22, z0: -450, z1: -410, y0: -5, y1: 22 }); mapFeatures.buildings.push({ t: 'box', x, z: -430, w: 44, d: 40, h: 22 }); }
  // avions de ligne décoratifs aux portes
  for (const x of [930, 1040]) { const m = planeMesh('#f4f4f4', '#c8102e', 2.4); m.position.set(x, 0, -520); m.rotation.y = 0; scene.add(m); addCollider({ t: 'box', x0: x - 4, x1: x + 4, z0: -545, z1: -495, y0: -5, y1: 7 }); }
  for (let x = AIRPORT.x0 + 20; x < AIRPORT.x1; x += 40) LIGHTS.box(0.6, 0.3, 0.6, '#ffd36b', x, 0.2, -685), LIGHTS.box(0.6, 0.3, 0.6, '#ffd36b', x, 0.2, -635);
  publicSpots.jets = [{ x: 1150, z: -560 }, { x: 1200, z: -560 }];
}
function planeMesh(body, stripe, s = 1) {
  const b = new GeoBag();
  b.add(new THREE.CapsuleGeometry(1.3, 12, 6, 14), body, 0, 2.2, 0, Math.PI / 2);
  b.add(new THREE.ConeGeometry(1.25, 3, 14), body, 0, 2.4, -8.5, -Math.PI / 2);
  b.box(2.66, 0.35, 12, stripe, 0, 2.0, 0);
  b.box(2.2, 0.55, 1.6, '#121a26', 0, 2.95, 6.4);
  for (let i = -4; i <= 4; i++) b.box(2.64, 0.35, 0.45, '#1d2836', 0, 2.7, i * 1.2);
  const wing = new THREE.BoxGeometry(17, 0.3, 3.6); wing.translate(0, 0, 0); b.add(wing, body, 0, 1.6, 0.5);
  for (const sx of [-1, 1]) { b.add(new THREE.CylinderGeometry(0.55, 0.6, 2.8, 12), '#9aa1ab', sx * 2.3, 2.6, -4.8, Math.PI / 2); b.box(0.2, 1.6, 2, body, sx * 7.8, 2.4, 0.2); }
  b.box(0.3, 3.8, 3, stripe, 0, 4.2, -8.6, -0.3); b.box(6, 0.25, 1.8, body, 0, 3.2, -8.8);
  for (const [x, z] of [[0, 4.5], [-1.6, -0.5], [1.6, -0.5]]) { b.add(new THREE.CylinderGeometry(0.35, 0.35, 0.3, 10), '#151515', x, 0.35, z, 0, 0, Math.PI / 2); b.box(0.12, 1.2, 0.12, '#aaa', x, 0.9, z); }
  const m = b.mesh(new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.3, metalness: 0.4 })); m.scale.setScalar(s); return m;
}

function buildWorld() {
  DECO = new GeoBag(); SIGNS = new GeoBag(); ROOFS = new GeoBag(); LIGHTS = new GeoBag(); SHOPWIN = new GeoBag();
  buildGround(); buildRoads(); buildGeneva(); buildBlocks(); buildCountryside(); buildSailHotel(); buildBurjAlArabDetails(); buildPalmIsland(); buildAtlantis(); buildBorder(); buildAirport(); buildBeachAndDesert(); buildStreetFurniture(); buildCityProps(); buildTramInfra(); buildInteriors(); buildPools(); buildTrafficLightMeshes();
  PALM_GEO2 = palmGeometry2(); TREE_GEO2 = treeGeometry2();
  instanced(PALM_GEO2, VEG_MAT, palmSpots); instanced(TREE_GEO2, VEG_MAT, treeSpots); buildGrass();
  const dm = DECO.mesh(VC_MAT); scene.add(dm);
  const sm = SIGNS.mesh(SIGN_MAT); sm.castShadow = false; scene.add(sm);
  const lm = LIGHTS.mesh(LIGHT_MAT); lm.castShadow = false; scene.add(lm);
  const wm = SHOPWIN.mesh(SHOPWIN_MAT); wm.castShadow = false; scene.add(wm);
  ROOFS_MESH = ROOFS.mesh(new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.9, metalness: 0 })); scene.add(ROOFS_MESH);
  BMATS.push(SIGN_MAT);
}
