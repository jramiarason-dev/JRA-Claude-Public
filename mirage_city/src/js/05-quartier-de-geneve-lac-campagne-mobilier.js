/* =====================================================================
   QUARTIER DE GENÈVE, LAC, CAMPAGNE & MOBILIER URBAIN
   ===================================================================== */
const SHOP_NAMES = ['BOULANGERIE', 'PHARMACIE', 'CAFÉ', 'HORLOGERIE', 'CHOCOLATIER', 'FROMAGERIE', 'BANQUE', 'LIBRAIRIE', 'FLEURISTE', 'BOUCHERIE', 'PIZZERIA', 'KEBAB', 'COIFFEUR', 'OPTICIEN', 'TABAC', 'BOUTIQUE', 'BIJOUTERIE', 'SUPERMARCHÉ', 'BRASSERIE', 'PÂTISSERIE', 'FONDUE', 'RESTAURANT', 'CINÉMA', 'HÔTEL', 'SHAWARMA', 'PARFUMS', 'ÉLECTRONIQUE', 'SOUK', 'HÔPITAL', 'POLICE', 'POMPIERS', 'MAIRIE', 'POSTE', 'PARKING', 'GARE ROUTIÈRE', 'ARRÊT BUS', 'FERME', 'ÉPICERIE', 'GLACIER', 'SPORT', 'DUBAI MALL', 'DOUANE · CUSTOMS', 'ARENA', 'STADE', 'TERMINAL 1', 'AÉROPORT', 'GRAND HÔTEL DU LAC', 'HÔTEL BELLEVUE', 'PALAIS DES NATIONS', 'ATLANTIS', 'MUSÉE DU FUTUR', 'BIENVENUE À GENÈVE', 'WELCOME TO DUBAI', 'HORLOGERIE DE LUXE'];
const SIGN_H = Math.ceil(SHOP_NAMES.length / 4) * 64;
const SIGN_BG = ['#7a1f2b', '#0f5e3a', '#1f3a6b', '#5b3a1e', '#2b2b2b', '#8a5a00', '#4b2a6b', '#0b5563'];
const SIGN_SPECIAL = { 'DOUANE · CUSTOMS': '#1f3a6b', 'DUBAI MALL': '#1b1b1b', 'ARENA': '#c8102e', 'STADE': '#8a0d1f', 'AÉROPORT': '#1f3a6b', 'TERMINAL 1': '#2b2b2b', 'GRAND HÔTEL DU LAC': '#2b2b2b', 'HÔTEL BELLEVUE': '#1f3a2b', 'PALAIS DES NATIONS': '#1f5fbf', 'ATLANTIS': '#0b5563', 'MUSÉE DU FUTUR': '#2b2b2b', 'BIENVENUE À GENÈVE': '#0a7d3b', 'WELCOME TO DUBAI': '#0a7d3b', 'HORLOGERIE DE LUXE': '#1b1b1b', 'HÔPITAL': '#c8102e', 'POLICE': '#1f4fa0', 'POMPIERS': '#b3261e', 'MAIRIE': '#3d4a5c', 'POSTE': '#f2c230', 'PARKING': '#1f5fbf', 'GARE ROUTIÈRE': '#2b7a3d', 'ARRÊT BUS': '#1f5fbf', 'PHARMACIE': '#0a8a3a' };
const signAtlas = canvasTex(1024, SIGN_H, (g) => {
  SHOP_NAMES.forEach((n, i) => {
    const x = (i % 4) * 256, y = Math.floor(i / 4) * 64;
    g.fillStyle = SIGN_SPECIAL[n] || SIGN_BG[i % SIGN_BG.length]; g.fillRect(x, y, 256, 64);
    g.strokeStyle = 'rgba(255,255,255,.55)'; g.lineWidth = 3; g.strokeRect(x + 4, y + 4, 248, 56);
    g.fillStyle = n === 'POSTE' ? '#1b1b1b' : '#fff8e8'; g.textAlign = 'center'; g.textBaseline = 'middle';
    let fs = 34; g.font = `bold ${fs}px Outfit, Arial, sans-serif`; while (g.measureText(n).width > 228 && fs > 14) { fs -= 2; g.font = `bold ${fs}px Outfit, Arial, sans-serif`; }
    g.fillText(n, x + 128, y + 34);
  });
}, false);
const SIGN_MAT = new THREE.MeshStandardMaterial({ map: signAtlas, emissiveMap: signAtlas, emissive: 0xffffff, emissiveIntensity: 0, roughness: 0.55 });
function signGeo(name, w, h) {
  const i = Math.max(0, SHOP_NAMES.indexOf(name)), col = i % 4, row = Math.floor(i / 4);
  const g = new THREE.PlaneGeometry(w, h), uv = g.attributes.uv;
  const u0 = col / 4 + 0.002, u1 = (col + 1) / 4 - 0.002, vt = 1 - row * 64 / SIGN_H - 0.002, vb = 1 - (row + 1) * 64 / SIGN_H + 0.002;
  for (let k = 0; k < uv.count; k++) uv.setXY(k, lerp(u0, u1, uv.getX(k)), lerp(vb, vt, uv.getY(k)));
  return g;
}
let DECO, SIGNS, ROOFS, CLOCKS;
function addLocal(bag, geo, color, lx, ly, lz, ry, wx, wz, wy = 0) { geo.translate(lx, ly, lz); bag.add(geo, color, wx, wy, wz, 0, ry, 0); }
function shopFront(wx, wz, ry, width, name, color) {
  addLocal(DECO, new THREE.BoxGeometry(width * 0.94, 2.9, 0.12), '#2a2f36', 0, 1.6, 0.06, ry, wx, wz);
  addLocal(SHOPWIN, uvCell(new THREE.PlaneGeometry(width * 0.84, 2.45), Math.floor(Math.random() * 4), 2, 2), '#ffffff', -width * 0.05, 1.55, 0.13, ry, wx, wz);
  addLocal(DECO, new THREE.BoxGeometry(width * 0.96, 0.28, 0.22), '#eee6d6', 0, 3.1, 0.11, ry, wx, wz);
  addLocal(DECO, new THREE.BoxGeometry(1.1, 2.4, 0.16), '#5a3a22', width * 0.38, 1.2, 0.15, ry, wx, wz);
  if (Math.random() < 0.55) for (const t of [-0.22, 0.22]) { const sb = new THREE.BoxGeometry(0.7, 1.05, 0.05); sb.rotateX(t); addLocal(DECO, sb, t < 0 ? '#1e1e22' : '#2a2a30', -width * 0.25, 0.5, 2.4 + t * 0.8, ry, wx, wz); }
  POOLS.push({ x: wx + Math.sin(ry) * 2.4, z: wz + Math.cos(ry) * 2.4, r: width * 0.42 });
  const aw = new THREE.BoxGeometry(width * 0.92, 0.08, 1.7); aw.rotateX(0.38); addLocal(DECO, aw, color, 0, 3.55, 0.8, ry, wx, wz);
  addLocal(SIGNS, signGeo(name, Math.min(width * 0.8, 6.5), 1.15), '#ffffff', 0, 4.55, 0.16, ry, wx, wz);
}
function signOnly(wx, wz, ry, y, name, w = 9, h = 1.8) { addLocal(SIGNS, signGeo(name, w, h), '#ffffff', 0, y, 0.2, ry, wx, wz); }

/* ---------- façades genevoises (pierre, fenêtres hautes, volets) */
function gvaFacadeTex(emissive) {
  return canvasTex(128, 128, (g, w, h) => {
    g.fillStyle = emissive ? '#000' : '#f4f1ea'; g.fillRect(0, 0, w, h);
    if (!emissive) { g.fillStyle = 'rgba(0,0,0,.07)'; for (let y = 0; y < h; y += 8) g.fillRect(0, y, w, 1); }
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
      const x = i * 32 + 10, y = j * 32 + 6;
      if (emissive) { g.fillStyle = Math.random() < 0.45 ? '#ffcf86' : '#000'; g.fillRect(x, y, 12, 22); continue; }
      g.fillStyle = '#6f8f6a'; g.fillRect(x - 6, y, 5, 22); g.fillRect(x + 13, y, 5, 22);
      g.fillStyle = '#3c4a5a'; g.fillRect(x, y, 12, 22);
      g.fillStyle = '#e8e2d6'; g.fillRect(x + 5, y, 2, 22); g.fillRect(x - 2, y + 23, 16, 3);
    }
  });
}
const GVA_FAC = { map: gvaFacadeTex(false), em: gvaFacadeTex(true) };
const GVA_COLORS = [0xefe4cf, 0xe2cfaa, 0xf3ece0, 0xd4bc96, 0xe8d6c6, 0xdcd6ca, 0xf0d9b5, 0xc9c3b8];
const GVA_MATS = GVA_COLORS.map(c => new THREE.MeshStandardMaterial({ color: c, map: GVA_FAC.map, emissiveMap: GVA_FAC.em, emissive: 0xffd9a0, emissiveIntensity: 0, roughness: 0.85 }));
const mkFacMat = (color, style = 0, rough = 0.5) => new THREE.MeshStandardMaterial({ color, map: FACADES[style].map, emissiveMap: FACADES[style].em, emissive: 0xffe0b0, emissiveIntensity: 0, roughness: rough, metalness: 0.15 });
const HOSP_MAT = mkFacMat(0xf6f7f9, 2), POLICE_MAT = mkFacMat(0x9db3d4, 0), FIRE_MAT = mkFacMat(0xc2553f, 0, 0.8), POSTE_MAT = mkFacMat(0xf2c94c, 2, 0.7);
const STONE_GVA = new THREE.MeshStandardMaterial({ color: 0xd8ccb4, map: GVA_FAC.map, emissiveMap: GVA_FAC.em, emissive: 0xffd9a0, emissiveIntensity: 0, roughness: 0.9 });
const CHALET_MAT = new THREE.MeshStandardMaterial({ color: 0xf7f2e8, map: GVA_FAC.map, emissiveMap: GVA_FAC.em, emissive: 0xffd9a0, emissiveIntensity: 0, roughness: 0.9 });
const WOOD_MAT = new THREE.MeshStandardMaterial({ color: 0x8a5a34, roughness: 0.9 });
const BARN_MAT = new THREE.MeshStandardMaterial({ color: 0xa8322a, roughness: 0.9 });
for (const m of [...GVA_MATS, HOSP_MAT, POLICE_MAT, FIRE_MAT, POSTE_MAT, STONE_GVA, CHALET_MAT]) BMATS.push(m);
const ROOF_COLORS = ['#6b7480', '#8a6a58', '#5f6873', '#a3543f', '#7a848f', '#b0624a'];
function prismRoof(cx, cz, w, d, y, color, pitch = 0.38, over = 0.8) {
  const alongX = w >= d, span = (alongX ? d : w) + over * 2, len = (alongX ? w : d) + over * 2;
  const r = span / 1.732, geo = new THREE.CylinderGeometry(r, r, len, 3);
  geo.rotateX(-Math.PI / 2); geo.translate(0, 0.5 * r, 0);
  const rh = span * pitch; geo.scale(1, rh / (1.5 * r), 1);
  if (alongX) geo.rotateY(Math.PI / 2);
  ROOFS.add(geo, color, cx, y, cz);
  return rh;
}
function gvaBuilding(cx, cz, w, d, h, mat) {
  addBoxBuilding(cx, cz, w, d, h, mat || pick(GVA_MATS));
  const rh = prismRoof(cx, cz, w, d, h, pick(ROOF_COLORS));
  ROOFS.box(1.1, 2.4, 1.1, '#8a7d70', cx + rand(-w / 3, w / 3), h + rh * 0.45, cz + rand(-d / 5, d / 5));
  // corniche
  DECO.box(w + 0.5, 0.45, d + 0.5, '#efe9dc', cx, h - 0.2, cz);
  DECO.box(w + 0.3, 0.35, d + 0.3, '#cfc6b4', cx, 4.6, cz);
}
const AWN = ['#7a1f2b', '#1f5e3a', '#c8a24a', '#2b4a7a', '#d9d2c4', '#b33a2e', '#3a3a3a'];
const GVA_SHOPS = ['BOULANGERIE', 'PHARMACIE', 'CAFÉ', 'HORLOGERIE', 'CHOCOLATIER', 'FROMAGERIE', 'BANQUE', 'LIBRAIRIE', 'FLEURISTE', 'BOUCHERIE', 'PIZZERIA', 'KEBAB', 'COIFFEUR', 'OPTICIEN', 'TABAC', 'BOUTIQUE', 'BIJOUTERIE', 'SUPERMARCHÉ', 'BRASSERIE', 'PÂTISSERIE', 'FONDUE', 'RESTAURANT', 'CINÉMA', 'HÔTEL', 'ÉPICERIE', 'GLACIER', 'SPORT'];
const DXB_SHOPS = ['SHAWARMA', 'PARFUMS', 'ÉLECTRONIQUE', 'SOUK', 'CAFÉ', 'PHARMACIE', 'SUPERMARCHÉ', 'BIJOUTERIE', 'RESTAURANT', 'SPORT', 'GLACIER', 'HÔTEL', 'BANQUE', 'BOUTIQUE', 'OPTICIEN'];

/* Îlot genevois : immeubles en périmètre avec cour intérieure et commerces au rez-de-chaussée */
function genevaBlock(cx, cz, luxury = false) {
  const half = 44, dep = 15, segs = [];
  for (const sz of [-1, 1]) { const n = 3, ws = 88 / n; for (let i = 0; i < n; i++) segs.push({ x: cx - half + ws / 2 + i * ws, z: cz + sz * (half - dep / 2), w: ws - 0.5, d: dep, ry: sz > 0 ? 0 : Math.PI }); }
  for (const sx of [-1, 1]) { const inner = 88 - 2 * dep, n = 2, ds = inner / n; for (let i = 0; i < n; i++) segs.push({ x: cx + sx * (half - dep / 2), z: cz - inner / 2 + ds / 2 + i * ds, w: dep, d: ds - 0.5, ry: sx > 0 ? Math.PI / 2 : -Math.PI / 2 }); }
  for (const s of segs) {
    gvaBuilding(s.x, s.z, s.w, s.d, rand(15, 25));
    const nz = Math.abs(Math.cos(s.ry)) > 0.5, hd = nz ? s.d / 2 : s.w / 2, len = nz ? s.w : s.d;
    const fx = s.x + Math.sin(s.ry) * (hd + 0.02), fz = s.z + Math.cos(s.ry) * (hd + 0.02);
    if (Math.random() < 0.85) shopFront(fx, fz, s.ry, Math.min(len * 0.7, 13), luxury ? pick(['HORLOGERIE DE LUXE', 'HORLOGERIE', 'HORLOGERIE DE LUXE', 'BIJOUTERIE', 'CHOCOLATIER', 'BANQUE', 'BOUTIQUE']) : pick(GVA_SHOPS), pick(AWN));
  }
  plane(56, 56, GRASS_MAT, cx, 0.05, cz);
  for (let i = 0; i < 3; i++) addTree(cx + rand(-20, 20), cz + rand(-20, 20));
}

/* ---------- arbres feuillus (instanciés) */
function treeGeometry() {
  const b = new GeoBag();
  b.add(new THREE.CylinderGeometry(0.25, 0.4, 5, 6), 0x6b4a2f, 0, 2.5, 0);
  b.add(new THREE.IcosahedronGeometry(2.6, 0), 0x3f7d3a, 0, 6.2, 0);
  b.add(new THREE.IcosahedronGeometry(1.9, 0), 0x4f9447, 1.3, 7.2, 0.6);
  b.add(new THREE.IcosahedronGeometry(1.8, 0), 0x36702f, -1.2, 6.9, -0.8);
  return b.geo();
}
const TREE_GEO = treeGeometry();
const treeSpots = [];
function addTree(x, z, s = 1) { treeSpots.push({ x, y: 0, z, ry: rand(0, 6.28), s: s * rand(0.8, 1.25) }); }

/* ---------- horloges animées */
const clockHands = [];
function clockHand(x, y, z, ry, r, color = '#1b1b1b', flat = false) {
  const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry;
  const mkH = (len, w) => { const p = new THREE.Group(); const m = new THREE.Mesh(new THREE.BoxGeometry(w, len, 0.08), new THREE.MeshStandardMaterial({ color })); m.position.y = len / 2; p.add(m); g.add(p); return p; };
  const hh = mkH(r * 0.55, r * 0.09), mh = mkH(r * 0.85, r * 0.06);
  if (flat) g.rotation.x = -Math.PI / 2;
  scene.add(g); clockHands.push({ hh, mh });
}
const CLOCK_TEX = canvasTex(128, 128, (g) => {
  g.fillStyle = '#f6f1e2'; g.beginPath(); g.arc(64, 64, 60, 0, 7); g.fill(); g.strokeStyle = '#1b1b1b'; g.lineWidth = 5; g.stroke();
  g.fillStyle = '#1b1b1b'; for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; g.fillRect(64 + Math.sin(a) * 48 - 3, 64 - Math.cos(a) * 48 - 3, 6, 6); }
}, false);
function updateClocks() {
  const h = S.hour % 12, m = (S.hour % 1) * 60;
  for (const c of clockHands) { c.hh.rotation.z = -h / 12 * Math.PI * 2; c.mh.rotation.z = -m / 60 * Math.PI * 2; }
}

/* ---------- bâtiments publics */
const COBBLE_MAT = new THREE.MeshStandardMaterial({ color: 0xbdb3a3, roughness: 1, userData: { pbr: 'cobble' } });
const ASPHALT_MAT = new THREE.MeshStandardMaterial({ color: 0x4a4b51, roughness: 0.95, userData: { pbr: 'asphalt' } });
const publicSpots = {};
function parkingLot(cx, cz, w, d, rows) {
  plane(w, d, ASPHALT_MAT, cx, 0.045, cz);
  for (const r of rows) for (let x = cx - w / 2 + 4; x <= cx + w / 2 - 4; x += 4.2) DECO.box(0.15, 0.02, 5.4, '#f4f4f4', x, 0.06, r);
  const spots = [];
  for (const r of rows) for (let x = cx - w / 2 + 6.1; x < cx + w / 2 - 4; x += 4.2) spots.push({ x, z: r });
  return spots;
}
function buildMairie(cx, cz) {
  plane(88, 88, COBBLE_MAT, cx, 0.05, cz);
  addBoxBuilding(cx, cz + 10, 70, 34, 20, STONE_GVA); prismRoof(cx, cz + 10, 70, 34, 20, '#6b7480', 0.32);
  DECO.box(71, 1, 35, '#efe9dc', cx, 19.6, cz + 10);
  addBoxBuilding(cx, cz - 11, 11, 11, 44, STONE_GVA);
  ROOFS.add(new THREE.ConeGeometry(8.2, 12, 4), '#3a4048', cx, 50, cz - 11, 0, Math.PI / 4);
  const cg = new GeoBag();
  for (const [ox, oz, ry] of [[0, -5.6, Math.PI], [0, 5.6, 0], [5.6, 0, Math.PI / 2], [-5.6, 0, -Math.PI / 2]]) {
    const p = new THREE.PlaneGeometry(6, 6); p.rotateY(ry); cg.add(p, '#ffffff', cx + ox * 1.002, 37, cz - 11 + oz * 1.002);
    clockHand(cx + ox * 1.03, 37, cz - 11 + oz * 1.03, ry, 3);
  }
  const cm = cg.mesh(new THREE.MeshStandardMaterial({ map: CLOCK_TEX, roughness: 0.6 })); scene.add(cm);
  // drapeau, escalier, colonnes
  DECO.add(new THREE.CylinderGeometry(0.12, 0.12, 12, 6), '#dddddd', cx, 62, cz - 11);
  DECO.box(0.1, 3, 4.5, '#c8102e', cx, 66, cz - 8.7);
  for (let i = 0; i < 4; i++) DECO.box(20, 0.3, 1.2, '#e3dccd', cx, 0.15 + i * 0.3, cz - 22 - i * 1.2 + 4);
  for (let i = -3; i <= 3; i++) DECO.add(new THREE.CylinderGeometry(0.6, 0.7, 9, 10), '#efe9dc', cx + i * 7, 4.5, cz - 7.4);
  signOnly(cx, cz - 16.6, Math.PI, 14, 'MAIRIE', 12, 2.2);
  for (const s of [-1, 1]) for (let i = 0; i < 4; i++) addTree(cx + s * 38, cz - 38 + i * 24);
}
function buildHospital(cx, cz) {
  plane(88, 88, COBBLE_MAT, cx, 0.05, cz);
  addBoxBuilding(cx, cz + 10, 74, 50, 30, HOSP_MAT);
  for (const [x, z, ry] of [[cx, cz - 15.1, Math.PI], [cx + 37.1, cz + 10, Math.PI / 2]]) {
    addLocal(DECO, new THREE.BoxGeometry(6, 1.8, 0.2), '#d01c2b', 0, 25, 0.1, ry, x, z);
    addLocal(DECO, new THREE.BoxGeometry(1.8, 6, 0.2), '#d01c2b', 0, 25, 0.1, ry, x, z);
  }
  signOnly(cx - 18, cz - 15.1, Math.PI, 19, 'HÔPITAL', 14, 2.6);
  DECO.box(20, 0.5, 8, '#e8eef4', cx, 4.5, cz - 19); for (const s of [-1, 1]) DECO.box(0.5, 4.5, 0.5, '#cfd6de', cx + s * 9.5, 2.25, cz - 22.5);
  const hp = plane(22, 22, new THREE.MeshStandardMaterial({ map: helipadTex(), roughness: 0.8 }), cx + 20, 30.06, cz + 14);
  publicSpots.hospital = parkingLot(cx, cz - 34, 80, 16, [cz - 34]);
}
function buildPolice(cx, cz) {
  plane(88, 88, COBBLE_MAT, cx, 0.05, cz);
  addBoxBuilding(cx, cz + 12, 70, 40, 20, POLICE_MAT);
  DECO.box(70.4, 1.2, 40.4, '#1f4fa0', cx, 6, cz + 12);
  signOnly(cx, cz - 8.1, Math.PI, 15, 'POLICE', 12, 2.4);
  DECO.add(new THREE.CylinderGeometry(0.15, 0.25, 14, 6), '#9aa1ab', cx + 28, 27, cz + 24);
  for (let i = 0; i < 3; i++) DECO.add(new THREE.CylinderGeometry(0.06, 0.06, 2.2, 6), '#cfd6de', cx + 28, 30 + i * 1.5, cz + 24, 0, 0, Math.PI / 2);
  publicSpots.police = parkingLot(cx, cz - 26, 80, 22, [cz - 30, cz - 21]);
}
function buildFireStation(cx, cz) {
  plane(88, 88, ASPHALT_MAT, cx, 0.045, cz);
  addBoxBuilding(cx - 6, cz + 14, 64, 34, 15, FIRE_MAT);
  for (let i = 0; i < 4; i++) {
    const x = cx - 30 + i * 14.5; DECO.box(10, 8.5, 0.25, '#e8e2d6', x, 4.25, cz - 3.1);
    for (let k = 0; k < 6; k++) DECO.box(9.6, 0.12, 0.3, '#b9b2a4', x, 1 + k * 1.3, cz - 3.0);
  }
  addBoxBuilding(cx + 33, cz + 22, 10, 10, 30, FIRE_MAT); prismRoof(cx + 33, cz + 22, 10, 10, 30, '#3f454d', 0.5);
  signOnly(cx - 6, cz - 3.2, Math.PI, 12.4, 'POMPIERS', 13, 2.4);
  for (let i = 0; i < 6; i++) DECO.add(new THREE.CylinderGeometry(0.25, 0.3, 0.9, 8), '#d01c2b', cx - 40 + i * 2, 0.45, cz - 40);
  publicSpots.fire = [{ x: cx - 30, z: cz - 14 }, { x: cx - 15.5, z: cz - 14 }, { x: cx - 1, z: cz - 14 }];
}
function buildPoste(cx, cz) {
  plane(88, 88, COBBLE_MAT, cx, 0.05, cz);
  addBoxBuilding(cx, cz + 8, 60, 40, 16, POSTE_MAT); prismRoof(cx, cz + 8, 60, 40, 16, '#4a4f57', 0.25);
  signOnly(cx, cz - 12.1, Math.PI, 11.5, 'POSTE', 10, 2.2);
  for (let i = 0; i < 4; i++) { DECO.box(0.9, 1.2, 0.6, '#f2c230', cx - 6 + i * 4, 1.4, cz - 16); DECO.box(0.15, 0.8, 0.15, '#333', cx - 6 + i * 4, 0.4, cz - 16); }
  publicSpots.poste = parkingLot(cx, cz - 30, 70, 14, [cz - 30]);
}
function buildParking(cx, cz, name = 'PARKING') {
  const spots = parkingLot(cx, cz, 88, 88, [cz - 34, cz - 22, cz - 4, cz + 8, cz + 26, cz + 38]);
  DECO.box(3, 3, 3, '#e8e2d6', cx - 40, 1.5, cz - 44); DECO.box(6, 0.15, 0.15, '#d01c2b', cx - 36, 1.1, cz - 44);
  DECO.add(new THREE.CylinderGeometry(0.15, 0.15, 6, 6), '#888', cx - 44, 3, cz - 44.5);
  signOnly(cx - 44, cz - 44.5, Math.PI, 6.5, name, 6, 1.6);
  return spots;
}
function buildBusStation(cx, cz) {
  plane(88, 88, ASPHALT_MAT, cx, 0.045, cz);
  for (let i = 0; i < 4; i++) { const x = cx - 30 + i * 20; busShelter(x, cz + 18, Math.PI); DECO.box(3, 0.02, 14, '#f2c94c', x, 0.06, cz + 6); }
  addBoxBuilding(cx, cz + 36, 60, 12, 8, STONE_GVA); signOnly(cx, cz + 29.9, Math.PI, 6.5, 'GARE ROUTIÈRE', 12, 1.8);
  publicSpots.bus = [{ x: cx - 30, z: cz + 4 }, { x: cx - 10, z: cz + 4 }, { x: cx + 10, z: cz + 4 }];
}
function buildCathedral(cx, cz) {
  plane(88, 88, COBBLE_MAT, cx, 0.05, cz);
  addBoxBuilding(cx, cz + 8, 24, 52, 24, STONE_GVA); prismRoof(cx, cz + 8, 24, 52, 24, '#4c5a63', 0.55);
  addBoxBuilding(cx, cz + 8, 46, 12, 18, STONE_GVA); prismRoof(cx, cz + 8, 46, 12, 18, '#4c5a63', 0.5);
  for (const s of [-1, 1]) { addBoxBuilding(cx + s * 8, cz - 22, 10, 10, 40, STONE_GVA); ROOFS.add(new THREE.ConeGeometry(7.4, 9, 4), '#4c5a63', cx + s * 8, 44.5, cz - 22, 0, Math.PI / 4); }
  ROOFS.add(new THREE.ConeGeometry(2.4, 20, 8), '#6f9f8a', cx, 46, cz + 6);
  const rose = new THREE.Mesh(new THREE.CircleGeometry(3.4, 24), new THREE.MeshStandardMaterial({ color: 0x6a3fb0, emissive: 0x6a3fb0, emissiveIntensity: 0.3 }));
  rose.position.set(cx, 16, cz - 18.1); rose.rotation.y = Math.PI; scene.add(rose);
  DECO.box(6, 9, 0.4, '#5a3a22', cx, 4.5, cz - 18);
  for (let i = 0; i < 6; i++) addTree(cx + rand(-38, 38), cz + 38 - rand(0, 6));
}
function busShelter(x, z, ry) {
  BUS_STOPS.push({ x, z });
  addLocal(DECO, new THREE.BoxGeometry(5, 0.15, 2), '#3a3f46', 0, 2.7, 0, ry, x, z);
  addLocal(DECO, new THREE.BoxGeometry(5, 2.5, 0.08), '#a9d4e6', 0, 1.4, -0.9, ry, x, z);
  for (const s of [-1, 1]) addLocal(DECO, new THREE.BoxGeometry(0.12, 2.7, 0.12), '#3a3f46', s * 2.4, 1.35, -0.9, ry, x, z);
  addLocal(DECO, new THREE.BoxGeometry(3.4, 0.12, 0.5), '#8a5a34', 0, 0.55, -0.55, ry, x, z);
  addLocal(DECO, new THREE.CylinderGeometry(0.06, 0.06, 3.4, 6), '#888', 3, 1.7, 0.6, ry, x, z);
  addLocal(SIGNS, signGeo('ARRÊT BUS', 1.8, 0.5), '#fff', 3, 3.2, 0.67, ry, x, z);
}
function buildFlowerClock(cx, cz) {
  plane(88, 88, GRASS_MAT, cx, 0.05, cz);
  const cols = ['#e63946', '#ffd166', '#f4f1de', '#ef476f', '#ffb703', '#8338ec'];
  for (let i = 0; i < 24; i++) { const a0 = i / 24 * Math.PI * 2, g = new THREE.RingGeometry(4, 13, 6, 1, a0, Math.PI * 2 / 24); g.rotateX(-Math.PI / 2); DECO.add(g, cols[i % cols.length], cx, 0.12, cz); }
  DECO.add(new THREE.CircleGeometry(4, 20), '#2f7d32', cx, 0.13, cz, -Math.PI / 2);
  clockHand(cx, 0.3, cz, 0, 12, '#1b1b1b', true);
  for (let i = 0; i < 10; i++) addTree(cx + rand(-38, 38), cz + (Math.random() < 0.5 ? -1 : 1) * rand(22, 38));
  for (let i = 0; i < 6; i++) bench(cx - 25 + i * 10, cz - 18, 0);
}
function bench(x, z, ry) {
  addLocal(DECO, new THREE.BoxGeometry(2.2, 0.1, 0.6), '#8a5a34', 0, 0.55, 0, ry, x, z);
  addLocal(DECO, new THREE.BoxGeometry(2.2, 0.5, 0.08), '#8a5a34', 0, 0.85, -0.28, ry, x, z);
  for (const s of [-1, 1]) addLocal(DECO, new THREE.BoxGeometry(0.08, 0.55, 0.5), '#333', s * 0.95, 0.28, 0, ry, x, z);
}
function buildGvaPark(cx, cz) {
  plane(88, 88, GRASS_MAT, cx, 0.05, cz);
  for (let i = 0; i < 18; i++) addTree(cx + rand(-40, 40), cz + rand(-40, 40));
  DECO.add(new THREE.CylinderGeometry(6, 6.4, 0.8, 24), '#d8ccb4', cx, 0.4, cz); DECO.add(new THREE.CylinderGeometry(5.4, 5.4, 0.1, 24), '#3aa6c8', cx, 0.82, cz);
  DECO.add(new THREE.CylinderGeometry(0.5, 0.8, 3, 10), '#d8ccb4', cx, 2, cz);
  for (let i = 0; i < 8; i++) { const a = i / 8 * 6.28; bench(cx + Math.cos(a) * 12, cz + Math.sin(a) * 12, -a - Math.PI / 2); }
  mapFeatures.parks.push({ x: cx, z: cz });
}

/* ---------- lac, quai, jet d'eau, montagnes */
function buildLake() {
  plane(2000, 1200, WATER_MAT, 600, WATER_Y, LAKE_Z + 600);
  plane(864, 36, COBBLE_MAT, 123, 0.02, (909 + LAKE_Z) / 2);
  DECO.box(BOUNDS.x1 - SHORE + 40, 1.0, 1.2, '#cfc6b4', (BOUNDS.x1 + SHORE) / 2, -0.4, LAKE_Z + 0.6);
  for (let x = -300; x <= 540; x += 18) { addTree(x, 920); if (Math.round(x / 18) % 2 === 0) bench(x + 9, 938, Math.PI); }
  // jetée vers le jet d'eau
  plane(6, 70, COBBLE_MAT, 60, 0.03, LAKE_Z + 35); addCollider({ t: 'box', x0: 57, x1: 63, z0: LAKE_Z, z1: LAKE_Z + 70, y0: -5, y1: 0.05 });
  DECO.box(4, 0.6, 4, '#d8ccb4', 60, 0.3, LAKE_Z + 72);
  // voiliers décoratifs
  for (let i = 0; i < 8; i++) {
    const b = new GeoBag(), x = rand(-250, 900), z = rand(LAKE_Z + 80, LAKE_Z + 330), c = pick(['#f4f4f4', '#1f3a6b', '#c8102e']);
    b.box(2.2, 0.8, 7, c, 0, 0.1, 0); b.add(new THREE.CylinderGeometry(0.08, 0.08, 9, 5), '#ddd', 0, 5, 0.5);
    const sail = new THREE.BufferGeometry(); sail.setAttribute('position', new THREE.Float32BufferAttribute([0, 1.2, 0.6, 0, 9, 0.6, 0, 1.2, -2.6, 0, 1.2, 0.6, 0, 1.2, -2.6, 0, 9, 0.6], 3)); sail.computeVertexNormals();
    sail.setAttribute('uv', new THREE.Float32BufferAttribute(new Array(12).fill(0), 2));
    b.add(sail, '#fbfbf6');
    const m = b.mesh(new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, roughness: 0.6 }));
    m.position.set(x, WATER_Y, z); m.rotation.y = rand(0, 6.28); scene.add(m); lakeBoats.push({ m, t: rand(0, 9) });
  }
  // Alpes à l'horizon
  const mb = new GeoBag();
  for (let i = 0; i < 26; i++) {
    const x = -1600 + i * 140 + rand(-50, 50), z = LAKE_Z + rand(750, 1100), h = rand(140, 330), r = h * rand(1.1, 1.6);
    mb.add(new THREE.ConeGeometry(r, h, 7), '#7b8a9c', x, h / 2 - 5, z, 0, rand(0, 6));
    mb.add(new THREE.ConeGeometry(r * 0.32, h * 0.32, 7), '#f7f9fb', x, h - h * 0.16 - 4.5, z, 0, rand(0, 6));
  }
  const mm = mb.mesh(new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 1, flatShading: true })); mm.castShadow = false; scene.add(mm);
}
const lakeBoats = [];
let jetT = 0;
function updateGeneva(dt, time) {
  const cp = camera.position;
  if (Math.hypot(cp.x - 60, cp.z - (LAKE_Z + 72)) < 1400) {
    jetT += dt;
    while (jetT > 0.012) { jetT -= 0.012; emit(60 + rand(-0.4, 0.4), 0.6, LAKE_Z + 72 + rand(-0.4, 0.4), rand(-1.2, 1.2) + 2.2, rand(60, 64), rand(-1.2, 1.2), 4.4, rand(0.8, 1.5), pick(['#ffffff', '#eaf6ff', '#d6eefc']), 0.45, 0.15); }
  }
  for (const b of lakeBoats) { b.t += dt; b.m.position.y = WATER_Y + Math.sin(b.t * 1.3) * 0.15; b.m.rotation.z = Math.sin(b.t * 0.9) * 0.05; b.m.position.x += Math.sin(b.m.rotation.y) * dt * 1.5; b.m.position.z += Math.cos(b.m.rotation.y) * dt * 1.5; if (b.m.position.z < LAKE_Z + 40 || b.m.position.z > LAKE_Z + 380 || Math.abs(b.m.position.x - 300) > 700) b.m.rotation.y += Math.PI; }
  updateClocks();
  updateAnimals(dt);
}

/* ---------- campagne : champs, fermes, vignes, animaux */
const FIELD_TEX = [['#d9b44a', '#c9a23c'], ['#5e9e3a', '#4f8a30'], ['#8a6240', '#76533a'], ['#b7c95a', '#a3b84e']].map(([a, b]) => canvasTex(64, 64, (g, w, h) => { g.fillStyle = a; g.fillRect(0, 0, w, h); g.fillStyle = b; for (let x = 0; x < w; x += 8) g.fillRect(x, 0, 4, h); }));
function field(x0, z0, x1, z1, k) {
  const t = FIELD_TEX[k].clone(); t.needsUpdate = true; t.repeat.set((x1 - x0) / 10, 1);
  const m = plane(x1 - x0, z1 - z0, new THREE.MeshStandardMaterial({ map: t, roughness: 1 }), (x0 + x1) / 2, 0.03, (z0 + z1) / 2);
  mapFeatures.fields.push({ x0, z0, x1, z1, c: ['#d9b44a', '#5e9e3a', '#8a6240', '#b7c95a'][k] });
  return m;
}
function fence(x0, z0, x1, z1) {
  for (const [ax, az, bx, bz] of [[x0, z0, x1, z0], [x1, z0, x1, z1], [x1, z1, x0, z1], [x0, z1, x0, z0]]) {
    const L = Math.hypot(bx - ax, bz - az), n = Math.floor(L / 3), ry = Math.atan2(bx - ax, bz - az);
    for (let i = 0; i <= n; i++) DECO.box(0.18, 1.3, 0.18, '#7a5233', lerp(ax, bx, i / n), 0.65, lerp(az, bz, i / n));
    for (const y of [0.55, 1.05]) addLocal(DECO, new THREE.BoxGeometry(0.08, 0.12, L), '#8a5a34', 0, y, L / 2, ry, ax, az);
  }
}
function farm(cx, cz, rot = 0) {
  // ferme (chalet), grange, silo, foin
  addBoxBuilding(cx, cz, 18, 12, 4.5, CHALET_MAT); addBoxBuilding(cx, cz, 18, 12, 4, WOOD_MAT, 4.5);
  prismRoof(cx, cz, 18, 12, 8.5, '#5a4a42', 0.42, 2.2);
  DECO.box(18.6, 0.25, 1.4, '#6b4a2f', cx, 4.6, cz - 6.6);
  for (let i = 0; i < 5; i++) DECO.box(1.2, 0.5, 0.4, pick(['#e63946', '#ffd166', '#ef476f']), cx - 7 + i * 3.4, 5.1, cz - 7);
  addBoxBuilding(cx + 28, cz + 4, 22, 16, 9, BARN_MAT); prismRoof(cx + 28, cz + 4, 22, 16, 9, '#4a4f57', 0.5, 0.6);
  DECO.box(7, 6.5, 0.2, '#f4efe6', cx + 28, 3.25, cz - 4.1); DECO.box(6.4, 0.3, 0.25, '#a8322a', cx + 28, 3.25, cz - 4.0);
  addCylBuilding(cx + 44, cz + 16, 4, 20, new THREE.MeshStandardMaterial({ color: 0xc9ccd1, metalness: 0.4, roughness: 0.4 }));
  ROOFS.add(new THREE.SphereGeometry(4, 12, 6, 0, 6.28, 0, Math.PI / 2), '#9aa1ab', cx + 44, 20, cz + 16);
  for (let i = 0; i < 6; i++) DECO.add(new THREE.CylinderGeometry(1.3, 1.3, 1.6, 12), '#e0c068', cx - 6 + (i % 3) * 3.2, 0.8, cz + 14 + Math.floor(i / 3) * 3.2, 0, 0, Math.PI / 2);
  plane(60, 40, new THREE.MeshStandardMaterial({ color: 0x9c8a6a, roughness: 1 }), cx + 14, 0.025, cz + 2);
  for (let i = 0; i < 6; i++) addTree(cx + rand(-30, 60), cz + (i % 2 ? -22 : 30));
}
const animals = [];
function makeAnimal(kind, area) {
  const b = new GeoBag();
  if (kind === 'vache') {
    b.box(1.0, 0.9, 2.0, '#f3f1ea', 0, 1.15, 0); b.box(1.02, 0.5, 0.7, '#1e1e1e', 0, 1.3, 0.3); b.box(0.6, 0.45, 0.5, '#1e1e1e', 0.25, 1.0, -0.6);
    b.box(0.5, 0.5, 0.7, '#f3f1ea', 0, 1.45, 1.2); b.box(0.42, 0.25, 0.2, '#e8a6a6', 0, 1.3, 1.6);
    for (const s of [-1, 1]) { b.box(0.08, 0.2, 0.08, '#d8d0c0', s * 0.22, 1.78, 1.15); for (const f of [-1, 1]) b.box(0.18, 0.75, 0.18, '#f3f1ea', s * 0.35, 0.37, f * 0.7); }
  } else {
    b.add(new THREE.DodecahedronGeometry(0.6, 0), '#f1ece0', 0, 0.85, 0); b.box(0.35, 0.4, 0.5, '#2a2a2a', 0, 1.0, 0.65);
    for (const s of [-1, 1]) for (const f of [-1, 1]) b.box(0.12, 0.5, 0.12, '#2a2a2a', s * 0.25, 0.25, f * 0.35);
  }
  const m = b.mesh(VC_MAT); m.scale.setScalar(kind === 'vache' ? 1.3 : 1); m.rotation.order = 'YXZ'; scene.add(m);
  const a = { kind, m, area, pos: new V3(rand(area[0], area[2]), 0, rand(area[1], area[3])), yaw: rand(0, 6.28), t: rand(0, 5), state: 'idle', vel: new V3(), spin: 0 };
  a.target = { x: a.pos.x, z: a.pos.z }; animals.push(a); return a;
}
function updateAnimals(dt) {
  const pp = P.vehicle ? P.vehicle.pos : P.pos;
  for (const a of animals) {
    const far = Math.abs(a.pos.x - pp.x) > 450 || Math.abs(a.pos.z - pp.z) > 450;
    a.m.visible = !far; if (far) continue;
    if (a.state === 'fly') {
      a.vel.y -= G * dt; a.pos.addScaledVector(a.vel, dt); a.yaw += a.spin * dt; a.m.rotation.z = lerp(a.m.rotation.z, Math.PI / 2, 3 * dt);
      if (a.pos.y <= 0) { a.pos.y = 0; if (a.vel.y < -5) { a.vel.y *= -0.3; a.vel.x *= 0.5; a.vel.z *= 0.5; } else { a.state = 'down'; a.t = 3; } }
    } else if (a.state === 'down') { a.t -= dt; if (a.t <= 0) { a.state = 'idle'; a.m.rotation.z = 0; a.pos.x = clamp(a.pos.x, a.area[0], a.area[2]); a.pos.z = clamp(a.pos.z, a.area[1], a.area[3]); } }
    else {
      a.t -= dt;
      if (a.t <= 0) { a.t = rand(3, 9); a.target = { x: rand(a.area[0], a.area[2]), z: rand(a.area[1], a.area[3]) }; }
      const dx = a.target.x - a.pos.x, dz = a.target.z - a.pos.z, d = Math.hypot(dx, dz);
      if (d > 0.5) { const sp = a.kind === 'vache' ? 0.7 : 1.0; a.pos.x += dx / d * sp * dt; a.pos.z += dz / d * sp * dt; a.yaw = angleLerp(a.yaw, Math.atan2(dx, dz), 3 * dt); }
      // percuté par le véhicule du joueur
      if (P.vehicle && Math.abs(P.vehicle.speed) > 5) { const v = P.vehicle, ex = a.pos.x - v.pos.x, ez = a.pos.z - v.pos.z; if (ex * ex + ez * ez < (v.def.r * 0.7 + 1) ** 2) knockAnimal(a, v.fwd.x * Math.abs(v.speed) * 0.8, Math.abs(v.speed) * 0.35 + 3, v.fwd.z * Math.abs(v.speed) * 0.8); }
    }
    a.m.position.set(a.pos.x, a.pos.y + (a.state === 'idle' ? Math.abs(Math.sin(performance.now() / 300 + a.area[0])) * 0.03 : 0), a.pos.z); a.m.rotation.y = a.yaw;
  }
}
function knockAnimal(a, vx, vy, vz) { a.state = 'fly'; a.vel.set(vx, vy, vz); a.spin = rand(-4, 4); SFX.burst(0.2, 700, 0.2); }

function buildCountryside() {
  plane(1000, LAKE_Z - 556, new THREE.MeshStandardMaterial({ color: 0x7fae5a, roughness: 1, userData: { pbr: 'grass' } }), 1060, 0.015, (556 + LAKE_Z) / 2);
  // route de campagne
  const t = roadTex.clone(); t.needsUpdate = true; t.repeat.set(1, 900 / 22);
  const r = plane(12, 910, new THREE.MeshStandardMaterial({ map: t, roughness: 0.9 }), 1004, 0.035, 780); r.rotation.z = Math.PI / 2;
  // champs
  const F = [[580, 580, 660, 760, 0], [580, 800, 680, 930, 1], [760, 600, 860, 760, 2], [880, 800, 1000, 930, 0], [1010, 590, 1100, 760, 3], [1120, 800, 1230, 930, 1], [1340, 590, 1460, 760, 0], [1380, 800, 1470, 930, 2]];
  for (const [a, b, c, d, k] of F) field(a, b, c, d, k);
  // vignes
  const rows = [];
  for (let z = 600; z < 760; z += 4) for (let x = 1240; x < 1330; x += 2.6) rows.push({ x, z, ry: 0, s: 1 });
  instanced(new GeoBag().box(0.9, 1.2, 1.4, '#3f7d32', 0, 0.8, 0).box(0.1, 1.4, 0.1, '#6b4a2f', 0, 0.7, 0).geo(), VC_MAT, rows, false);
  mapFeatures.fields.push({ x0: 1240, z0: 600, x1: 1330, z1: 760, c: '#3f7d32' });
  // fermes + enclos
  for (const [x, z] of [[700, 840], [960, 690], [1260, 860]]) {
    farm(x, z);
    const pen = [x - 30, z - 60 + (z > 800 ? 0 : 120), x + 30, z - 30 + (z > 800 ? 0 : 120)];
    fence(pen[0], pen[1], pen[2], pen[3]);
    for (let i = 0; i < 5; i++) makeAnimal('vache', [pen[0] + 2, pen[1] + 2, pen[2] - 2, pen[3] - 2]);
    for (let i = 0; i < 5; i++) makeAnimal('mouton', [pen[0] + 2, pen[1] + 2, pen[2] - 2, pen[3] - 2]);
    publicSpots['farm' + x] = { x: x + 10, z: z - 14 };
  }
  for (let i = 0; i < 50; i++) addTree(rand(570, 1480), pick([772, 788]) + rand(-3, 3) * 0 + (Math.random() < 0.5 ? -10 : 10), 1.1);
}

/* ---------- mobilier urbain partout : feux, bancs, poubelles, bornes, arrêts de bus, trottoirs */
function buildCityProps() {
  // feux tricolores aux carrefours
  for (const x of ROADS_X) for (const z of ROADS_Z) {
    for (const [sx, sz, ry] of [[1, 1, 0], [-1, -1, Math.PI], [1, -1, Math.PI / 2], [-1, 1, -Math.PI / 2]]) {
      const px = x + sx * 10.6, pz = z + sz * 10.6;
      DECO.add(new THREE.CylinderGeometry(0.1, 0.12, 4.2, 6), '#2f3237', px, 2.1, pz);
      addLocal(DECO, new THREE.BoxGeometry(0.45, 1.3, 0.35), '#1d1f22', 0, 3.9, 0, ry, px, pz);
      const ax = Math.abs(Math.sin(ry)) < 0.5 ? 'z' : 'x';
      addLocal(tlBag(ax, 'r'), new THREE.BoxGeometry(0.22, 0.22, 0.05), '#ff2a1a', 0, 4.3, -0.19, ry, px, pz);
      addLocal(tlBag(ax, 'y'), new THREE.BoxGeometry(0.22, 0.22, 0.05), '#ffb300', 0, 3.9, -0.19, ry, px, pz);
      addLocal(tlBag(ax, 'g'), new THREE.BoxGeometry(0.22, 0.22, 0.05), '#2cff6a', 0, 3.5, -0.19, ry, px, pz);
    }
  }
  // bordures de trottoir
  for (const x of ROADS_X) for (let i = 0; i < ROADS_Z.length - 1; i++) { const a = ROADS_Z[i] + 10, b = ROADS_Z[i + 1] - 10; for (const s of [-1, 1]) DECO.box(0.35, 0.16, b - a, '#bdb8ad', x + s * 9.2, 0.08, (a + b) / 2); }
  for (const z of ROADS_Z) for (let i = 0; i < ROADS_X.length - 1; i++) { const a = ROADS_X[i] + 10, b = ROADS_X[i + 1] - 10; for (const s of [-1, 1]) DECO.box(b - a, 0.16, 0.35, '#bdb8ad', (a + b) / 2, 0.08, z + s * 9.2); }
  // bancs, poubelles, bornes à incendie, arrêts de bus, kiosques
  let k = 0;
  for (const cx of BLOCKS_X) for (const cz of BLOCKS_Z) {
    k++;
    const gva = cz > GVA_Z;
    bench(cx - 20, cz - 46.5, 0); bench(cx + 20, cz + 46.5, Math.PI);
    for (const [x, z] of [[cx - 46, cz - 30], [cx + 46, cz + 30]]) { DECO.add(new THREE.CylinderGeometry(0.35, 0.3, 1, 10), gva ? '#2f5d3a' : '#6b6f75', x, 0.5, z); }
    DECO.add(new THREE.CylinderGeometry(0.22, 0.25, 0.8, 8), '#d01c2b', cx + 46.5, 0.4, cz - 8); DECO.add(new THREE.SphereGeometry(0.22, 8, 4), '#d01c2b', cx + 46.5, 0.85, cz - 8);
    if (k % 3 === 0) busShelter(cx - 47.5, cz + 6, -Math.PI / 2);
    if (k % 5 === 1) { DECO.box(2.6, 2.6, 2.2, gva ? '#2f5d3a' : '#d9a93f', cx + 47, 1.3, cz + 22); DECO.box(3.2, 0.2, 2.8, '#fafafa', cx + 47, 2.7, cz + 22); }
    if (gva && k % 2 === 0) { for (let i = 0; i < 5; i++) DECO.box(0.08, 0.9, 1.6, '#3b3f46', cx - 10 + i * 1, 0.45, cz + 47); }
  }
  // fontaines genevoises
  for (const [x, z] of [[60, 720], [-180, 840], [300, 840]]) { DECO.add(new THREE.CylinderGeometry(1.4, 1.5, 0.9, 12), '#d8ccb4', x + 12, 0.45, z); DECO.add(new THREE.CylinderGeometry(0.25, 0.25, 2.2, 8), '#6f9f8a', x + 12, 1.5, z); }
}

function buildGeneva() {
  plane(864, LAKE_Z - 552, new THREE.MeshStandardMaterial({ color: 0xcbc4b7, roughness: 0.95, userData: { pbr: 'cobble' } }), 122.5, 0.012, (552 + LAKE_Z) / 2);
  buildLake();
}
