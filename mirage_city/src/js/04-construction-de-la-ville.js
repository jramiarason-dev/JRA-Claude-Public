/* =====================================================================
   CONSTRUCTION DE LA VILLE
   ===================================================================== */
const mapFeatures = { parks: [], ponds: [], buildings: [], fields: [], rects: [] };
const landmarksPos = {};
let TOWER_TOP = 450;

function plane(w, d, mat, x, y, z) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d), mat); m.rotation.x = -Math.PI / 2; m.position.set(x, y, z); m.receiveShadow = true; scene.add(m); return m;
}
function addBoxBuilding(cx, cz, w, d, h, mat, y0 = 0) {
  const g = new THREE.BoxGeometry(w, h, d); scaleBoxUV(g, w, h, d);
  const m = new THREE.Mesh(g, mat); m.position.set(cx, y0 + h / 2, cz); m.castShadow = m.receiveShadow = true; scene.add(m);
  addCollider({ t: 'box', x0: cx - w / 2, x1: cx + w / 2, z0: cz - d / 2, z1: cz + d / 2, y0: y0 - 5, y1: y0 + h });
  mapFeatures.buildings.push({ t: 'box', x: cx, z: cz, w, d, h });
  return m;
}
function addCylBuilding(cx, cz, r, h, mat, y0 = 0, seg = 16) {
  const g = new THREE.CylinderGeometry(r, r, h, seg, 1); scaleCylUV(g, r, h, seg);
  const m = new THREE.Mesh(g, mat); m.position.set(cx, y0 + h / 2, cz); m.castShadow = m.receiveShadow = true; scene.add(m);
  addCollider({ t: 'cyl', x: cx, z: cz, r, y0: y0 - 5, y1: y0 + h });
  if (y0 === 0) mapFeatures.buildings.push({ t: 'cyl', x: cx, z: cz, r, h });
  return m;
}

function buildGround() {
  const sand = new THREE.MeshStandardMaterial({ color: 0xe0c28c, roughness: 1, userData: { pbr: 'sand' } });
  // grand sol de sable (côté terre)
  plane(BOUNDS.x1 - SHORE + 200, LAKE_Z + 1200, sand, (BOUNDS.x1 + 200 + SHORE) / 2, -0.05, (LAKE_Z - 1200) / 2);
  // dunes
  const dg = new THREE.PlaneGeometry(1000, 1660, 150, 230); dg.rotateX(-Math.PI / 2); dg.translate(1060, 0, -270);
  const p = dg.attributes.position;
  for (let i = 0; i < p.count; i++) p.setY(i, duneH(p.getX(i), p.getZ(i)));
  dg.computeVertexNormals();
  const dm = new THREE.Mesh(dg, new THREE.MeshStandardMaterial({ color: 0xe3b877, roughness: 1, userData: { pbr: 'sand' } })); dm.receiveShadow = true; scene.add(dm);
  // dalle urbaine
  plane(870, 1110, new THREE.MeshStandardMaterial({ color: 0xd3cbbb, roughness: 0.95, userData: { pbr: 'paving' } }), 122.5, 0.01, 0);
  // plage
  plane(31, 1300, new THREE.MeshStandardMaterial({ color: 0xf0dcae, roughness: 1 }), -324.5, 0.0, 0);
  // mer
  const sea = plane(4000, 4000, WATER_MAT, SHORE - 2000, WATER_Y, 0);
  plane(40, 2400, new THREE.MeshStandardMaterial({ color: 0x4fc6cf, roughness: 0.2, transparent: true, opacity: 0.85 }), SHORE - 20, WATER_Y + 0.02, 0);
  sea.receiveShadow = false;
}

function buildRoads() {
  const mk = (len, horiz, x, z) => {
    const t = roadTex.clone(); t.needsUpdate = true; t.repeat.set(1, len / 22);
    const m = plane(ROAD_W, len, new THREE.MeshStandardMaterial({ map: t, roughness: 0.9 }), x, 0.03, z); m.material.userData.pbr = 'road';
    if (horiz) m.rotation.z = Math.PI / 2;
  };
  for (const x of ROADS_X) mk(1458, false, x, 180);
  for (const z of ROADS_Z) mk(858, true, 120, z);
  mk(960, true, 1020, HWY_Z); // autoroute du désert
  const inter = new THREE.MeshStandardMaterial({ color: 0x44454b, roughness: 0.9 }); inter.userData.pbr = 'asphalt';
  const ig = new THREE.PlaneGeometry(ROAD_W, ROAD_W); ig.rotateX(-Math.PI / 2);
  const im = new THREE.InstancedMesh(ig, inter, ROADS_X.length * ROADS_Z.length); let k = 0;
  const d = new THREE.Object3D();
  for (const x of ROADS_X) for (const z of ROADS_Z) { d.position.set(x, 0.04, z); d.updateMatrix(); im.setMatrixAt(k++, d.matrix); }
  im.receiveShadow = true; scene.add(im);
  // passages piétons
  const zb = new GeoBag();
  for (const x of ROADS_X) for (const z of ROADS_Z) for (const s of [-1, 1]) for (let i = -3; i <= 3; i++) {
    const zc = z > GVA_Z ? '#f2c230' : '#eeeeee';
    zb.box(1.2, 0.02, 3, zc, x + i * 2.2, 0.05, z + s * (ROAD_W / 2 + 1.8));
    zb.box(3, 0.02, 1.2, zc, x + s * (ROAD_W / 2 + 1.8), 0.05, z + i * 2.2);
  }
  const zm = zb.mesh(VC_MAT); zm.castShadow = false; scene.add(zm);
}

/* ---------- Mobilier : palmiers & lampadaires (instanciés) */
function palmGeometry() {
  const b = new GeoBag();
  const trunk = new THREE.CylinderGeometry(0.22, 0.38, 9, 6, 5);
  const p = trunk.attributes.position;
  for (let i = 0; i < p.count; i++) { const y = p.getY(i) + 4.5; p.setY(i, y); p.setX(i, p.getX(i) + y * y * 0.008); }
  trunk.computeVertexNormals(); b.add(trunk, 0x8a6a45);
  for (let k = 0; k < 8; k++) {
    const f = new THREE.BoxGeometry(4.4, 0.06, 0.95); f.translate(2.2, 0, 0); f.rotateZ(-0.3 - (k % 2) * 0.22); f.rotateY(k / 8 * Math.PI * 2);
    b.add(f, k % 2 ? 0x2f7d32 : 0x46a043, 0.65, 9, 0);
  }
  b.add(new THREE.SphereGeometry(0.35, 6, 4), 0x5b3a1e, 0.65, 8.7, 0);
  return b.geo();
}
const PALM_GEO = palmGeometry();
const palmSpots = [];
function addPalm(x, z, s = 1) { palmSpots.push({ x, y: duneH(x, z), z, ry: rand(0, 6.28), s: s * rand(0.85, 1.25) }); }
function instanced(geo, mat, list, shadow = true) {
  const im = new THREE.InstancedMesh(geo, mat, list.length), d = new THREE.Object3D();
  list.forEach((p, i) => { d.position.set(p.x, p.y || 0, p.z); d.rotation.set(0, p.ry || 0, 0); d.scale.setScalar(p.s || 1); d.updateMatrix(); im.setMatrixAt(i, d.matrix); });
  im.castShadow = shadow; im.receiveShadow = true; scene.add(im); return im;
}
const LAMP_MAT = new THREE.MeshStandardMaterial({ color: 0xfff1d0, emissive: 0xffc870, emissiveIntensity: 0 });
function buildStreetFurniture() {
  const lamps = [];
  const nearNode = (v, list) => list.some(n => Math.abs(v - n) < 17);
  for (const x of ROADS_X) for (let z = -555; z <= 905; z += 30) {
    if (nearNode(z, ROADS_Z)) continue;
    for (const s of [-1, 1]) { if (x === -300 && s < 0) continue; if (z > GVA_Z) addTree(x + s * 13.5, z, 0.9); else addPalm(x + s * 13.5, z); }
    if ((z / 30) % 2 === 0) lamps.push({ x: x + 9.6, z: z + 15, ry: Math.PI }, { x: x - 9.6, z: z + 15, ry: 0 });
  }
  for (const z of ROADS_Z) for (let x = -300; x <= 545; x += 30) {
    if (nearNode(x, ROADS_X)) continue;
    for (const s of [-1, 1]) { if (z > GVA_Z) addTree(x, z + s * 13.5, 0.9); else addPalm(x, z + s * 13.5); }
  }
  for (let x = 560; x < 1480; x += 40) { addPalm(x, HWY_Z - 13, 0.9); lamps.push({ x: x + 20, z: HWY_Z + 9.6, ry: -Math.PI / 2 }); }
  // lampadaires
  const pole = new GeoBag();
  pole.add(new THREE.CylinderGeometry(0.1, 0.15, 7, 6), 0x55595f, 0, 3.5, 0);
  pole.box(1.7, 0.1, 0.12, 0x55595f, 0.8, 7, 0);
  const pg = pole.geo(); const hg = new THREE.BoxGeometry(0.7, 0.16, 0.38); hg.translate(1.55, 6.9, 0);
  const dl = lamps.map(l => ({ x: l.x, z: l.z, ry: l.ry }));
  for (const l of dl) POOLS.push({ x: l.x + 1.55 * Math.cos(l.ry), z: l.z - 1.55 * Math.sin(l.ry), r: 7 });
  instanced(pg, VC_MAT, dl);
  instanced(hg, LAMP_MAT, dl, false);
}

/* ---------- Grande tour (la plus haute de la ville) */
/* ---------- Tours torsadées (marina) */
function buildTwisted(cx, cz, w, h, mat) {
  const parts = []; const n = Math.floor(h / 6);
  for (let i = 0; i < n; i++) {
    const g = new THREE.BoxGeometry(w, 6, w * 0.8); scaleBoxUV(g, w, 6, w * 0.8);
    g.rotateY(i * 0.05); g.translate(0, i * 6 + 3, 0); parts.push(g);
  }
  const m = new THREE.Mesh(mergeGeometries(parts), mat); m.position.set(cx, 0, cz); m.castShadow = m.receiveShadow = true; scene.add(m);
  addCollider({ t: 'cyl', x: cx, z: cz, r: w * 0.62, y0: -5, y1: n * 6 });
  mapFeatures.buildings.push({ t: 'cyl', x: cx, z: cz, r: w * 0.62, h: n * 6 });
}

/* ---------- Hôtel en forme de voile sur son île */
function buildSailHotel() {
  const isl = new THREE.Mesh(new THREE.CylinderGeometry(38, 41, 1.4, 40), new THREE.MeshStandardMaterial({ color: 0xead6a6, roughness: 1 }));
  isl.position.set(-470, -0.7, -160); isl.receiveShadow = true; scene.add(isl);
  const br = new THREE.Mesh(new THREE.BoxGeometry(104, 1, 14), new THREE.MeshStandardMaterial({ color: 0x3a3b40, roughness: 0.9 }));
  br.position.set(-391, -0.5, -160); br.receiveShadow = true; scene.add(br);
  const s = new THREE.Shape(); s.moveTo(0, 0); s.lineTo(0, 200); s.quadraticCurveTo(78, 120, 62, 0); s.lineTo(0, 0);
  const g = new THREE.ExtrudeGeometry(s, { depth: 34, bevelEnabled: false }); g.translate(0, 0, -17);
  const m = new THREE.Mesh(g, WHITE_MAT); m.position.set(-470, 0, -160); m.rotation.y = Math.PI; m.castShadow = true; scene.add(m);
  const mast = new THREE.Mesh(new THREE.BoxGeometry(5, 222, 5), STONE_MAT); mast.position.set(-468, 111, -160); mast.castShadow = true; scene.add(mast);
  for (const [w, a, b] of [[60, 0, 80], [46, 80, 150], [24, 150, 200]]) addCollider({ t: 'box', x0: -470 - w, x1: -466, z0: -177, z1: -143, y0: -5, y1: b });
  // héliport en porte-à-faux
  const hp = new THREE.Mesh(new THREE.CylinderGeometry(11, 11, 1, 24), new THREE.MeshStandardMaterial({ map: helipadTex(), roughness: 0.8 }));
  hp.position.set(-452, 169.5, -160); hp.castShadow = true; scene.add(hp);
  addCollider({ t: 'cyl', x: -452, z: -160, r: 11, y0: 168, y1: 170 });
  for (let a = 0; a < 6.28; a += 0.5) addPalm(-470 + Math.cos(a) * 32, -160 + Math.sin(a) * 32);
  mapFeatures.buildings.push({ t: 'box', x: -500, z: -160, w: 62, d: 34, h: 200 });
}
function helipadTex() {
  return canvasTex(128, 128, (g, w, h) => {
    g.fillStyle = '#3b3e45'; g.fillRect(0, 0, w, h); g.strokeStyle = '#f2c94c'; g.lineWidth = 6; g.beginPath(); g.arc(64, 64, 52, 0, 7); g.stroke();
    g.fillStyle = '#fff'; g.font = 'bold 70px sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('H', 64, 68);
  }, false);
}

/* ---------- Île Palmier */
function buildPalmIsland() {
  const mat = new THREE.MeshStandardMaterial({ color: 0xead6a6, roughness: 1 });
  const add = (geo, x, z, ry = 0) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, -0.6, z); m.rotation.y = ry; m.receiveShadow = true; scene.add(m); };
  add(new THREE.BoxGeometry(245, 1.2, 22), -462.5, 261);
  add(new THREE.CylinderGeometry(55, 57, 1.2, 40), PALM_C.x, PALM_C.z);
  const villas = new GeoBag();
  for (const a of FRONDS) {
    const g = new THREE.BoxGeometry(175, 1.2, 16); g.translate(87.5, 0, 0); add(g, PALM_C.x, PALM_C.z, -a);
    for (let d = 70; d <= 165; d += 24) for (const s of [-1, 1]) {
      const px = PALM_C.x + Math.cos(a) * d - Math.sin(a) * s * 4, pz = PALM_C.z + Math.sin(a) * d + Math.cos(a) * s * 4;
      const vx = PALM_C.x + Math.cos(a) * (d + 10) - Math.sin(a) * s * 2, vz = PALM_C.z + Math.sin(a) * (d + 10) + Math.cos(a) * s * 2;
      addPalm(px, pz);
      if (s > 0) { villas.box(7, 5, 7, 0xf6f1e7, vx, 2.5, vz); villas.box(7.4, 0.4, 7.4, 0xc9763d, vx, 5.2, vz); villas.box(3, 0.2, 4, 0x3fc4dd, vx + 0.1, 0.05, vz + 0.1); }
    }
  }
  const ring = new THREE.RingGeometry(212, 230, 64, 1, -(Math.PI + 1.9), 3.8); ring.rotateX(-Math.PI / 2);
  const rm = new THREE.Mesh(ring, mat); rm.position.set(PALM_C.x, 0, PALM_C.z); rm.receiveShadow = true; scene.add(rm);
  for (let a = Math.PI - 1.8; a < Math.PI + 1.8; a += 0.12) addPalm(PALM_C.x + Math.cos(a) * 221, PALM_C.z + Math.sin(a) * 221);
  // hôtel central
  addBoxBuilding(PALM_C.x - 15, PALM_C.z, 30, 60, 38, BMATS[4]);
  const vm = villas.mesh(VC_MAT); scene.add(vm);
  // route sur le tronc
  const t = roadTex.clone(); t.needsUpdate = true; t.repeat.set(1, 10);
  const r = plane(12, 240, new THREE.MeshStandardMaterial({ map: t, roughness: 0.9 }), -460, 0.03, 261); r.rotation.z = Math.PI / 2;
}

/* ---------- Cadre d'or */
function buildFrame(cx, cz) {
  for (const s of [-1, 1]) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(14, 150, 14), GOLD_MAT); m.position.set(cx + s * 38, 75, cz); m.castShadow = true; scene.add(m);
    addCollider({ t: 'box', x0: cx + s * 38 - 7, x1: cx + s * 38 + 7, z0: cz - 7, z1: cz + 7, y0: -5, y1: 150 });
    mapFeatures.buildings.push({ t: 'box', x: cx + s * 38, z: cz, w: 14, d: 14, h: 150 });
  }
  const top = new THREE.Mesh(new THREE.BoxGeometry(90, 16, 14), new THREE.MeshStandardMaterial({ color: 0xe8b84a, metalness: 0.3, roughness: 0.35, map: FACADES[2].map }));
  top.position.set(cx, 148, cz); top.castShadow = true; scene.add(top);
  addCollider({ t: 'box', x0: cx - 45, x1: cx + 45, z0: cz - 7, z1: cz + 7, y0: 140, y1: 156 });
  plane(88, 88, new THREE.MeshStandardMaterial({ color: 0x5c9a4a, roughness: 1 }), cx, 0.05, cz);
}

/* ---------- Parcs, fontaine, mall, héliport */
const GRASS_MAT = new THREE.MeshStandardMaterial({ color: 0x5c9a4a, roughness: 1, userData: { pbr: 'grass' } });
function buildPark(cx, cz, withPad) {
  plane(88, 88, GRASS_MAT, cx, 0.05, cz);
  mapFeatures.parks.push({ x: cx, z: cz });
  for (let i = 0; i < 14; i++) addPalm(cx + rand(-40, 40), cz + rand(-40, 40));
  if (withPad) { const p = plane(26, 26, new THREE.MeshStandardMaterial({ map: helipadTex(), roughness: .8 }), cx, 0.07, cz); }
}
function buildFountain(cx, cz) {
  plane(88, 88, STONE_MAT, cx, 0.05, cz);
  const pond = new THREE.Mesh(new THREE.CircleGeometry(30, 48), new THREE.MeshStandardMaterial({ color: 0x25a9c9, roughness: 0.1, metalness: 0.3 }));
  pond.rotation.x = -Math.PI / 2; pond.position.set(cx, WATER_Y + 0.15, cz); scene.add(pond);
  const rim = new THREE.Mesh(new THREE.TorusGeometry(30.5, 0.6, 6, 64), STONE_MAT); rim.rotation.x = Math.PI / 2; rim.position.set(cx, 0.2, cz); scene.add(rim);
  mapFeatures.ponds.push({ x: cx, z: cz, r: 30 });
  for (let a = 0; a < 6.28; a += 0.45) addPalm(cx + Math.cos(a) * 38, cz + Math.sin(a) * 38);
}
function buildBlocks() {
  const special = {
    '0,0': () => buildMegaTower(),
    '0,120': () => buildFountain(0, 120),
    '120,-120': () => buildMall(120, -120),
    '360,0': () => buildFrame(360, 0),
    '120,120': () => buildPark(120, 120, true),
    '-120,240': () => buildPark(-120, 240),
    '240,360': () => buildPark(240, 360),
    '480,-240': () => buildPark(480, -240),
    '-240,-360': () => { buildTwisted(-240, -380, 30, 300, BMATS[1]); addBoxBuilding(-225, -330, 26, 26, 140, BMATS[8]); },
    '-240,-240': () => { buildTwisted(-250, -240, 28, 250, BMATS[6]); addCylBuilding(-215, -205, 12, 170, BMATS[2]); },
    '-240,-480': () => { addCylBuilding(-240, -480, 22, 260, BMATS[9]); },
    '-120,-360': () => { publicSpots.parkDxb = buildParking(-120, -360); },
    '-120,-120': () => buildMuseumFuture(-120, -120),
    '-120,0': () => buildEmiratesTowers(-120, 0),
    '240,-240': () => buildArena(240, -240),
    '-120,720': () => buildPalaisNations(-120, 720),
    '0,840': () => buildGrandHotel(0, 840, 'GRAND HÔTEL DU LAC'),
    '240,840': () => buildGrandHotel(240, 840, 'HÔTEL BELLEVUE'),
    '-120,840': () => watchStreet(-120, 840),
    '120,840': () => watchStreet(120, 840),
    '360,840': () => watchStreet(360, 840),
    '-240,600': () => buildBusStation(-240, 600),
    '-120,600': () => { publicSpots.parkGva = buildParking(-120, 600); },
    '0,600': () => buildPoste(0, 600),
    '120,600': () => buildMairie(120, 600),
    '240,600': () => buildHospital(240, 600),
    '360,600': () => buildPolice(360, 600),
    '480,600': () => buildFireStation(480, 600),
    '0,720': () => buildCathedral(0, 720),
    '360,720': () => buildStadium(360, 720),
    '-240,840': () => buildFlowerClock(-240, 840),
    '480,840': () => { publicSpots.parkLac = buildParking(480, 840); },
  };
  for (const cx of BLOCKS_X) for (const cz of BLOCKS_Z) {
    const key = cx + ',' + cz;
    if (special[key]) { special[key](); continue; }
    if (cz > GVA_Z) { genevaBlock(cx, cz, cz === 840); continue; }
    const dist = Math.hypot(cx, cz);
    const centrality = 1 - clamp(dist / 650, 0, 1);
    const lots = Math.random() < 0.35 ? [[0, 0, 80]] : [[-22, -22, 38], [22, -22, 38], [-22, 22, 38], [22, 22, 38]];
    for (const [ox, oz, size] of lots) {
      if (lots.length > 1 && Math.random() < 0.18) { for (let i = 0; i < 2; i++) addPalm(cx + ox + rand(-10, 10), cz + oz + rand(-10, 10)); continue; }
      const w = size * rand(0.6, 0.95), d = size * rand(0.6, 0.95);
      const h = 14 + rand(0, 30) + centrality * rand(30, 200) * (cx < -150 ? 1.3 : 1);
      const mat = pick(BMATS.slice(0, 12));
      if (Math.random() < 0.2) {
        const r = Math.min(w, d) / 2; addCylBuilding(cx + ox, cz + oz, r, h, mat);
        if (Math.random() < 0.5) addCylBuilding(cx + ox, cz + oz, r * 0.6, h * 0.15, mat, h);
      } else {
        addBoxBuilding(cx + ox, cz + oz, w, d, h, mat);
        DECO.box(w + 0.6, 4.2, d + 0.6, '#2a3340', cx + ox, 2.1, cz + oz);
        if (h > 40 && Math.random() < 0.7) { ROOFS.box(3, 2, 3, '#9aa1ab', cx + ox + rand(-w / 4, w / 4), h + 1, cz + oz + rand(-d / 4, d / 4)); ROOFS.add(new THREE.CylinderGeometry(1.4, 1.4, 3, 10), '#c9ccd1', cx + ox - w / 4, h + 1.5, cz + oz - d / 4); }
        if (Math.random() < 0.65) {
          const ry = lots.length > 1 ? (ox > 0 ? Math.PI / 2 : -Math.PI / 2) : 0, hd = lots.length > 1 ? w / 2 : d / 2, len = lots.length > 1 ? d : w;
          shopFront(cx + ox + Math.sin(ry) * (hd + 0.32), cz + oz + Math.cos(ry) * (hd + 0.32), ry, Math.min(len * 0.6, 12), pick(DXB_SHOPS), pick(AWN));
        }
        if (h > 80 && Math.random() < 0.6) { // couronne / flèche
          addBoxBuilding(cx + ox, cz + oz, w * 0.6, d * 0.6, h * 0.12, mat, h);
          const sp = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 1.2, h * 0.25, 6), GOLD_MAT); sp.position.set(cx + ox, h * 1.12 + h * 0.125, cz + oz); scene.add(sp);
        }
      }
    }
  }
}
function buildBeachAndDesert() {
  const b = new GeoBag();
  for (let z = -520; z <= 520; z += 26) {
    const x = -326 + rand(-3, 3), c = pick([0xe94f37, 0xf6f6f6, 0x2e86de, 0xf5b700]);
    b.add(new THREE.CylinderGeometry(0.06, 0.06, 3, 5), 0xdddddd, x, 1.5, z);
    b.add(new THREE.ConeGeometry(2.2, 0.8, 10), c, x, 3.1, z);
    b.box(0.8, 0.25, 2, 0xffffff, x + 1.6, 0.35, z + 0.5); b.box(0.8, 0.25, 2, 0xffffff, x - 1.6, 0.35, z + 0.5);
  }
  for (let i = 0; i < 70; i++) { const x = rand(620, 1450), z = rand(-950, 950); if (Math.abs(z - HWY_Z) < 20 || airportMask(x, z) < 1) continue; const s = rand(1, 4); b.add(new THREE.DodecahedronGeometry(s, 0), 0xb98a55, x, duneH(x, z) + s * 0.4, z); }
  // oasis
  const oasis = new THREE.Mesh(new THREE.CircleGeometry(28, 40), new THREE.MeshStandardMaterial({ color: 0x2bb3b8, roughness: 0.1 }));
  oasis.rotation.x = -Math.PI / 2; oasis.position.set(900, WATER_Y + 0.1, -220); scene.add(oasis);
  mapFeatures.ponds.push({ x: 900, z: -220, r: 28 });
  for (let a = 0; a < 6.28; a += 0.35) addPalm(900 + Math.cos(a) * rand(31, 40), -220 + Math.sin(a) * rand(31, 40));
  // campement bédouin
  for (let i = 0; i < 4; i++) { const a = i * 1.5; b.add(new THREE.ConeGeometry(5, 5, 4), 0x8b5a2b, 950 + Math.cos(a) * 60, 2.5, -200 + Math.sin(a) * 60, 0, 0.78); }
  const m = b.mesh(VC_MAT); scene.add(m);
}
