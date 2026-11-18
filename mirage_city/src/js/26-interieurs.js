/* =====================================================================
   INTÉRIEURS VISITABLES : Dubai Mall, Grand Hôtel du Lac, horlogerie, aéroport
   (salles construites sous la campagne, à -300 m, reliées aux portes de la ville)
   ===================================================================== */
const INT_Y = -300;
const INTERIORS = [], INTERACTS = [], INT_NPCS = [];
const MARBLE_TEX = canvasTex(256, 256, (g) => {
  g.fillStyle = '#efeae2'; g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 40; i++) { g.strokeStyle = `rgba(150,140,130,${rand(0.05, 0.2)})`; g.lineWidth = rand(0.5, 2); g.beginPath(); let x = rand(0, 256), y = rand(0, 256); g.moveTo(x, y); for (let k = 0; k < 6; k++) { x += rand(-40, 40); y += rand(-40, 40); g.lineTo(x, y); } g.stroke(); }
  g.strokeStyle = 'rgba(120,110,100,.35)'; g.lineWidth = 2; g.strokeRect(0, 0, 256, 256);
});
const CHECK_TEX = canvasTex(128, 128, (g) => { for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) { g.fillStyle = (i + j) % 2 ? '#1b1b1d' : '#f2efe8'; g.fillRect(i * 64, j * 64, 64, 64); } });
function iwall(x, z, w, d, h, color) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshStandardMaterial({ color, roughness: 0.8 }));
  m.position.set(x, INT_Y + h / 2, z); m.receiveShadow = true; scene.add(m);
  addCollider({ t: 'box', x0: x - w / 2, x1: x + w / 2, z0: z - d / 2, z1: z + d / 2, y0: INT_Y - 5, y1: INT_Y + h });
}
function room(def) {
  const { x, z, w, d, h } = def, it = { ...def, lights: [] };
  addCollider({ t: 'box', floor: true, x0: x - w / 2, x1: x + w / 2, z0: z - d / 2, z1: z + d / 2, y0: INT_Y - 5, y1: INT_Y });
  const ft = (def.floorTex || MARBLE_TEX).clone(); ft.needsUpdate = true; ft.repeat.set(w / 4, d / 4);
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(w, d), new THREE.MeshStandardMaterial({ map: ft, roughness: 0.12, metalness: 0.1 }));
  fl.rotation.x = -Math.PI / 2; fl.position.set(x, INT_Y + 0.01, z); fl.receiveShadow = true; scene.add(fl);
  const wc = def.wall || 0xe9e2d6;
  iwall(x, z - d / 2 - 0.25, w + 1, 0.5, h, wc); iwall(x, z + d / 2 + 0.25, w + 1, 0.5, h, wc);
  iwall(x - w / 2 - 0.25, z, 0.5, d, h, wc); iwall(x + w / 2 + 0.25, z, 0.5, d, h, wc);
  const ceil = new THREE.Mesh(new THREE.BoxGeometry(w + 1, 0.5, d + 1), new THREE.MeshStandardMaterial({ color: def.ceil || 0xf4f1ea, roughness: 0.9 }));
  ceil.position.set(x, INT_Y + h + 0.25, z); ceil.castShadow = true; scene.add(ceil);
  for (const [lx, lz, i, c] of def.lightsAt || [[0, 0, 40, 0xfff1dc]]) {
    const l = new THREE.PointLight(c, 0, Math.max(w, d) * 1.2, 1.2); l.position.set(x + lx, INT_Y + h - 1, z + lz); l.userData.i = i; scene.add(l); it.lights.push(l);
  }
  // porte de sortie
  DECO.box(3.2, 3.6, 0.2, '#3a2a1e', x + def.exit.x, INT_Y + 1.8, z + def.exit.z);
  INTERIORS.push(it); return it;
}
function ishop(x, z, ry, width, name, color) {
  addLocal(DECO, new THREE.BoxGeometry(width * 0.94, 2.9, 0.12), '#2a2f36', 0, 1.6, 0.06, ry, x, z, INT_Y);
  addLocal(SHOPWIN, uvCell(new THREE.PlaneGeometry(width * 0.84, 2.45), Math.floor(Math.random() * 4), 2, 2), '#ffffff', 0, 1.55, 0.13, ry, x, z, INT_Y);
  addLocal(SIGNS, signGeo(name, Math.min(width * 0.8, 6), 1), '#fff', 0, 3.6, 0.14, ry, x, z, INT_Y);
  addLocal(DECO, new THREE.BoxGeometry(width * 0.96, 0.25, 0.4), color, 0, 3.05, 0.2, ry, x, z, INT_Y);
}
function intNPC(it, n, region) {
  for (let i = 0; i < n; i++) {
    const m = buildCharacter(randomChar(region)); scene.add(m);
    const npc = { m, it, pos: new V3(it.x + rand(-it.w / 3, it.w / 3), INT_Y, it.z + rand(-it.d / 3, it.d / 3)), yaw: rand(0, 6.28), t: 0, phase: rand(0, 6), still: Math.random() < 0.35 };
    npc.target = npc.pos.clone(); INT_NPCS.push(npc);
  }
}
function buildInteriors() {
  // ---------- Dubai Mall
  const mall = room({ name: 'Dubai Mall', x: 760, z: 660, w: 64, d: 44, h: 14, wall: 0xe8e2d6, door: { x: 120, z: -75.5 }, out: { x: 120, z: -70, yaw: 0 }, spawn: { x: 760, z: 677, yaw: Math.PI }, exit: { x: 0, z: 21.8 },
    lightsAt: [[-16, 0, 38, 0xfff4e0], [16, 0, 38, 0xfff4e0], [0, -14, 26, 0xbfe4ff]] });
  const names = ['PARFUMS', 'BIJOUTERIE', 'ÉLECTRONIQUE', 'SPORT', 'CAFÉ', 'BOUTIQUE', 'HORLOGERIE DE LUXE', 'GLACIER', 'OPTICIEN', 'SUPERMARCHÉ'];
  for (let i = 0; i < 5; i++) { ishop(mall.x - 25 + i * 12.5, mall.z - 21.7, 0, 10.5, names[i], pick(AWN)); ishop(mall.x - 31.7, mall.z - 14 + i * 7, Math.PI / 2, 6.5, names[i + 5], pick(AWN)); }
  for (let i = 0; i < 4; i++) ishop(mall.x + 31.7, mall.z - 14 + i * 8, -Math.PI / 2, 7, pick(names), pick(AWN));
  DECO.add(new THREE.CylinderGeometry(6, 6.3, 0.8, 32), '#d9d2c4', mall.x, INT_Y + 0.4, mall.z); DECO.add(new THREE.CylinderGeometry(5.5, 5.5, 0.1, 32), '#3aa6c8', mall.x, INT_Y + 0.82, mall.z);
  for (let i = 0; i < 6; i++) { const a = i / 6 * 6.28; DECO.add(new THREE.CylinderGeometry(0.6, 0.7, 1.2, 12), '#b8a88a', mall.x + Math.cos(a) * 12, INT_Y + 0.6, mall.z + Math.sin(a) * 12); }
  for (let i = 0; i < 8; i++) DECO.box(4, 0.4, 0.8, '#c9ccd1', mall.x + 18 + i * 0.1, INT_Y + 0.6 + i * 0.9, mall.z + 8 - i * 1.6);
  DECO.box(20, 0.5, 6, '#e9e4da', mall.x + 18, INT_Y + 7, mall.z - 6); DECO.box(20, 1.1, 0.1, '#9fd0e6', mall.x + 18, INT_Y + 7.8, mall.z - 3);
  for (let i = -2; i <= 2; i++) LIGHTS.box(7, 0.1, 3, '#fffaf0', mall.x + i * 12, INT_Y + 13.9, mall.z);
  intNPC(mall, 8, 'dxb');
  INTERACTS.push({ x: mall.x, z: mall.z, label: '⛲ Fontaine du Dubai Mall', act: () => { for (let i = 0; i < 40; i++) emit(mall.x + rand(-2, 2), INT_Y + 1, mall.z + rand(-2, 2), rand(-2, 2), rand(6, 10), rand(-2, 2), 1.5, 0.3, '#dff4ff', 0.6); toast('✨ Tu as jeté une pièce dans la fontaine'); } });
  // ---------- Grand Hôtel du Lac (hall)
  const hotel = room({ name: 'Grand Hôtel du Lac', x: 900, z: 660, w: 40, d: 30, h: 10, wall: 0xe7dcc6, ceil: 0xf2e8d4, floorTex: CHECK_TEX, door: { x: 0, z: 886.5 }, out: { x: 0, z: 893, yaw: 0 }, spawn: { x: 900, z: 672, yaw: Math.PI }, exit: { x: 0, z: 14.8 },
    lightsAt: [[-8, 0, 45, 0xffe2b0], [8, 0, 45, 0xffe2b0]] });
  for (const sx of [-1, 1]) for (let i = -1; i <= 1; i++) { DECO.add(new THREE.CylinderGeometry(0.7, 0.8, 10, 16), '#f4efe4', hotel.x + sx * 10, INT_Y + 5, hotel.z + i * 8); DECO.box(2, 0.5, 2, '#c9a24a', hotel.x + sx * 10, INT_Y + 9.7, hotel.z + i * 8); }
  for (const sx of [-1, 1]) { const cx = hotel.x + sx * 8; DECO.add(new THREE.CylinderGeometry(0.05, 0.05, 1.5, 6), '#c9a24a', cx, INT_Y + 9.2, hotel.z); for (let k = 0; k < 10; k++) { const a = k / 10 * 6.28; LIGHTS.add(new THREE.SphereGeometry(0.16, 8, 6), '#ffe9b8', cx + Math.cos(a) * 1.2, INT_Y + 8.1, hotel.z + Math.sin(a) * 1.2); } DECO.add(new THREE.TorusGeometry(1.25, 0.06, 6, 24), '#c9a24a', cx, INT_Y + 8.2, hotel.z, Math.PI / 2); }
  DECO.box(12, 1.2, 2, '#5a3a22', hotel.x, INT_Y + 0.6, hotel.z - 11); DECO.box(12.4, 0.12, 2.4, '#e9e2d6', hotel.x, INT_Y + 1.26, hotel.z - 11);
  addLocal(SIGNS, signGeo('GRAND HÔTEL DU LAC', 12, 1.8), '#fff', 0, 4.5, 0.27, 0, hotel.x, hotel.z - 15, INT_Y);
  DECO.box(4, 0.02, 26, '#8a1c2b', hotel.x, INT_Y + 0.03, hotel.z + 2);
  for (const sx of [-1, 1]) { DECO.box(5, 0.9, 2, '#6b2a32', hotel.x + sx * 14, INT_Y + 0.45, hotel.z + 6); DECO.box(5, 1.4, 0.5, '#6b2a32', hotel.x + sx * 14, INT_Y + 1.1, hotel.z + 6.9); DECO.box(2.2, 0.5, 2.2, '#3a2a1e', hotel.x + sx * 14, INT_Y + 0.25, hotel.z + 3.5); }
  for (let i = 0; i < 2; i++) DECO.box(2.6, 4, 0.2, '#b8bcc4', hotel.x - 15 + i * 30, INT_Y + 2, hotel.z - 14.7);
  intNPC(hotel, 4, 'gva');
  // ---------- Horlogerie de luxe
  const shop = room({ name: 'Horlogerie de luxe', x: 1000, z: 660, w: 18, d: 14, h: 5, wall: 0x3a2a1e, ceil: 0x2a1f16, door: { x: 149.3, z: 886.5 }, out: { x: 149.3, z: 893, yaw: 0 }, spawn: { x: 1000, z: 664, yaw: Math.PI }, exit: { x: 0, z: 6.8 },
    lightsAt: [[-4, -2, 18, 0xfff0d8], [4, -2, 18, 0xfff0d8]] });
  addLocal(SIGNS, signGeo('HORLOGERIE DE LUXE', 6.5, 1.1), '#fff', 0, 6.2, 0.3, 0, 149.3, 884.4);
  const styles = [['or', 'Montre en or', '#d6a63c'], ['acier', 'Montre en acier', '#c9ccd1'], ['noir', 'Montre noire', '#1b1b1b']];
  styles.forEach(([k, n, c], i) => {
    const x = shop.x - 5 + i * 5, z = shop.z - 3;
    DECO.box(3, 1, 1.4, '#2a1f16', x, INT_Y + 0.5, z);
    const glass = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.6, 1.2), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.18, roughness: 0.02, clearcoat: 1 })); glass.position.set(x, INT_Y + 1.3, z); scene.add(glass);
    for (let j = 0; j < 3; j++) { DECO.add(new THREE.TorusGeometry(0.11, 0.025, 8, 18), c, x - 0.8 + j * 0.8, INT_Y + 1.06, z, Math.PI / 2); DECO.add(new THREE.CylinderGeometry(0.09, 0.09, 0.02, 16), j === 1 ? '#0f1a24' : '#f6f1e2', x - 0.8 + j * 0.8, INT_Y + 1.08, z); }
    LIGHTS.box(2.6, 0.04, 1, '#fff6e0', x, INT_Y + 1.58, z);
    INTERACTS.push({ x, z: z + 1.2, label: `⌚ Essayer : ${n}`, act: () => { CHAR.watch = true; CHAR.watchStyle = k; saveChar(); rebuildPlayer(); toast(`⌚ ${n} au poignet`); } });
  });
  for (let i = 0; i < 3; i++) { const cx = shop.x - 5 + i * 5; const cl = new THREE.Mesh(new THREE.CircleGeometry(0.6, 24), new THREE.MeshStandardMaterial({ map: CLOCK_TEX })); cl.position.set(cx, INT_Y + 3.2, shop.z - 6.74); scene.add(cl); clockHand(cx, INT_Y + 3.2, shop.z - 6.72, 0, 0.55); }
  DECO.box(6, 1.1, 1.2, '#1b1410', shop.x + 4, INT_Y + 0.55, shop.z + 3);
  intNPC(shop, 1, 'gva'); INT_NPCS[INT_NPCS.length - 1].still = true; INT_NPCS[INT_NPCS.length - 1].pos.set(shop.x + 4, INT_Y, shop.z + 1.8);
  // ---------- Hall de l'aéroport
  const air = room({ name: 'Aéroport — hall des départs', x: 1150, z: 680, w: 70, d: 32, h: 12, wall: 0xdfe4ea, door: { x: 1010, z: -467.5 }, out: { x: 1010, z: -473, yaw: Math.PI }, spawn: { x: 1150, z: 690, yaw: Math.PI }, exit: { x: 0, z: 15.8 },
    lightsAt: [[-20, 0, 36, 0xf2f6ff], [20, 0, 36, 0xf2f6ff], [0, 0, 22, 0xf2f6ff]] });
  for (let i = 0; i < 6; i++) { const x = air.x - 25 + i * 10; DECO.box(6, 1.1, 1.2, '#c9ccd1', x, INT_Y + 0.55, air.z - 10); DECO.box(5, 1.6, 0.1, '#1d2836', x, INT_Y + 3, air.z - 12.5); LIGHTS.box(4.6, 1.2, 0.05, '#2a6fdb', x, INT_Y + 3, air.z - 12.42); }
  const board = canvasTex(512, 256, (g) => {
    g.fillStyle = '#0b0f17'; g.fillRect(0, 0, 512, 256); g.fillStyle = '#f0bf62'; g.font = 'bold 26px monospace'; g.fillText('DÉPARTS  DEPARTURES', 16, 34);
    const rows = [['08:15', 'GENÈVE', 'A12', 'À L\'HEURE'], ['09:40', 'LONDRES', 'B04', 'EMBARQUEMENT'], ['10:05', 'PARIS', 'A07', 'À L\'HEURE'], ['11:30', 'NEW YORK', 'C21', 'RETARDÉ'], ['12:10', 'TOKYO', 'C02', 'À L\'HEURE'], ['13:45', 'ZURICH', 'A15', 'À L\'HEURE']];
    g.font = '20px monospace'; rows.forEach((r, i) => { g.fillStyle = i === 3 ? '#ff6b6b' : '#e9edf2'; g.fillText(r.join('   '), 16, 74 + i * 30); });
  }, false);
  const bm = new THREE.Mesh(new THREE.PlaneGeometry(12, 6), new THREE.MeshBasicMaterial({ map: board, toneMapped: false })); bm.position.set(air.x, INT_Y + 7, air.z - 15.7); scene.add(bm);
  for (let r = 0; r < 3; r++) for (let i = 0; i < 8; i++) { const x = air.x - 20 + i * 1.2 + (i > 3 ? 4 : 0), z = air.z + 2 + r * 4; DECO.box(1, 0.5, 1, '#2a2f36', x, INT_Y + 0.45, z); DECO.box(1, 0.8, 0.15, '#2a2f36', x, INT_Y + 0.95, z + 0.45); }
  for (let i = -3; i <= 3; i++) LIGHTS.box(8, 6, 0.05, '#cfe6ff', air.x + i * 9.5, INT_Y + 6.5, air.z + 15.9);
  intNPC(air, 8, Math.random() < 0.5 ? 'gva' : 'dxb');
  // portes extérieures signalées
  for (const it of INTERIORS) { LIGHTS.box(1.8, 0.12, 0.12, '#f0bf62', it.door.x, 3.6, it.door.z); }
}
let interiorT = 0;
function updateInteriors(dt) {
  if (!P.inside) return;
  for (const n of INT_NPCS) {
    if (n.it !== P.inside) { n.m.visible = false; continue; }
    n.m.visible = true; n.t -= dt;
    if (n.still) { pose(n.m, n.it.name.startsWith('Horlogerie') ? 'walk' : 'phone', 0, 0); }
    else {
      if (n.t <= 0) { n.t = rand(3, 7); n.target.set(n.it.x + rand(-n.it.w / 2.6, n.it.w / 2.6), INT_Y, n.it.z + rand(-n.it.d / 2.6, n.it.d / 2.6)); }
      const dx = n.target.x - n.pos.x, dz = n.target.z - n.pos.z, d = Math.hypot(dx, dz);
      if (d > 0.4) { n.pos.x += dx / d * 1.2 * dt; n.pos.z += dz / d * 1.2 * dt; n.yaw = angleLerp(n.yaw, Math.atan2(dx, dz), 5 * dt); n.phase += dt * 3; pose(n.m, 'walk', n.phase, 0.8); }
      else pose(n.m, 'walk', 0, 0);
    }
    n.m.position.copy(n.pos); n.m.rotation.set(0, n.yaw, 0);
  }
}
function enterInterior(it) {
  if (P.vehicle) exitVehicle();
  P.inside = it; it.lights.forEach(l => l.intensity = l.userData.i);
  P.pos.set(it.spawn.x, INT_Y + 0.05, it.spawn.z); P.vel.set(0, 0, 0); P.yaw = it.spawn.yaw; CAM.yaw = it.spawn.yaw; CAM.pitch = 0.15;
  toast(`🚪 ${it.name}`);
}
function exitInterior() {
  const it = P.inside; if (!it) return;
  it.lights.forEach(l => l.intensity = 0); P.inside = null;
  P.pos.set(it.out.x, heightAt(it.out.x, it.out.z, 3) + 0.05, it.out.z); P.vel.set(0, 0, 0); P.yaw = it.out.yaw; CAM.yaw = it.out.yaw;
  for (const n of INT_NPCS) n.m.visible = false;
}
function nearInteract() {
  if (P.vehicle) return null;
  if (P.inside) {
    const it = P.inside;
    if (Math.hypot(P.pos.x - (it.x + it.exit.x), P.pos.z - (it.z + it.exit.z)) < 3) return { label: '🚪 Sortir', act: exitInterior };
    for (const a of INTERACTS) if (Math.hypot(P.pos.x - a.x, P.pos.z - a.z) < 2.2) return a;
    return null;
  }
  if (P.pos.y > 4) return null;
  for (const it of INTERIORS) if (Math.hypot(P.pos.x - it.door.x, P.pos.z - it.door.z) < 3.5) return { label: `🚪 Entrer : ${it.name}`, act: () => enterInterior(it) };
  return null;
}
