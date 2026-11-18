/* =====================================================================
   VEHICULES
   ===================================================================== */
const VDEF = {
  supercar: { name: 'Falcon GT', icon: '🏎️', desc: 'Supercar ultra-rapide', kind: 'car', max: 74, acc: 26, turn: 2.0, r: 2.4 },
  hyper: { name: 'Aurum X (or)', icon: '✨', desc: "Hypercar plaquée or", kind: 'car', max: 96, acc: 34, turn: 2.0, r: 2.4 },
  sedan: { name: 'Berline', icon: '🚗', desc: 'Voiture de ville', kind: 'car', max: 48, acc: 15, turn: 1.8, r: 2.3 },
  taxi: { name: 'Taxi Mirage', icon: '🚕', desc: 'Le taxi de la ville', kind: 'car', max: 50, acc: 16, turn: 1.8, r: 2.3 },
  police: { name: 'Patrouille', icon: '🚓', desc: 'Sirène incluse (H)', kind: 'car', max: 70, acc: 25, turn: 1.95, r: 2.4 },
  suv: { name: 'Dune Patrol 4x4', icon: '🚙', desc: 'Tout-terrain pour les dunes', kind: 'car', max: 56, acc: 20, turn: 1.7, r: 2.6, offroad: true },
  limo: { name: 'Limousine', icon: '🎩', desc: 'Grand luxe', kind: 'car', max: 42, acc: 11, turn: 1.2, r: 3.6 },
  quad: { name: 'Quad Sable', icon: '🏜️', desc: 'Parfait pour le désert', kind: 'car', max: 42, acc: 22, turn: 2.4, r: 1.6, offroad: true, open: true, seat: [0, 1.05, -0.25] },
  moto: { name: 'Viper 1000', icon: '🏍️', desc: 'Moto sportive', kind: 'bike', max: 84, acc: 32, turn: 2.3, r: 1.4, open: true, seat: [0, 1.02, -0.3] },
  heli: { name: 'Skyhawk', icon: '🚁', desc: 'Hélicoptère (Espace / C)', kind: 'heli', max: 60, acc: 18, turn: 1.4, r: 4.5 },
  jetski: { name: 'Jet-ski', icon: '🌊', desc: 'Sur la mer', kind: 'boat', max: 44, acc: 22, turn: 2.4, r: 1.6, open: true, seat: [0, 0.65, -0.35] },
  yacht: { name: 'Yacht Al Bahr', icon: '🛥️', desc: 'Yacht de luxe', kind: 'boat', max: 28, acc: 7, turn: 0.7, r: 7 },
  bus: { name: 'Bus urbain', icon: '🚌', desc: 'Transports publics', kind: 'car', max: 38, acc: 9, turn: 1.1, r: 3.4 },
  ambulance: { name: 'Ambulance', icon: '🚑', desc: 'Sirène incluse (H)', kind: 'car', max: 60, acc: 18, turn: 1.6, r: 2.8 },
  firetruck: { name: 'Camion de pompiers', icon: '🚒', desc: 'Grande échelle, sirène (H)', kind: 'car', max: 48, acc: 12, turn: 1.25, r: 3.6 },
  van: { name: 'Fourgon postal', icon: '📮', desc: 'Livraison du courrier', kind: 'car', max: 46, acc: 13, turn: 1.5, r: 2.7 },
  jet: { name: 'Jet privé', icon: '✈️', desc: 'Décolle vers 130 km/h · Espace monter, C descendre', kind: 'plane', max: 110, acc: 16, turn: 0.9, r: 7 },
  tram: { name: 'Tram', icon: '🚋', desc: 'Sur les rails de Genève', kind: 'car', max: 22, acc: 6, turn: 0.8, r: 4.5 },
  tractor: { name: 'Tracteur', icon: '🚜', desc: 'Pour les champs', kind: 'car', max: 24, acc: 10, turn: 1.6, r: 2.3, offroad: true },
};
const CAR_COLORS = ['#f5f5f2', '#1c1c1e', '#c8102e', '#2a6fdb', '#ff7a1a', '#14b8c4', '#f0bf62', '#6d3fc0', '#0a7d3b', '#9aa1ab', '#e05aa8'];
const WHEEL_GEO = (() => {
  const b = new GeoBag();
  b.add(new THREE.CylinderGeometry(1, 1, 1, 22), '#141414', 0, 0, 0, 0, 0, Math.PI / 2);
  b.add(new THREE.TorusGeometry(0.86, 0.14, 6, 22), '#1b1b1b', 0.5, 0, 0, 0, Math.PI / 2);
  b.add(new THREE.TorusGeometry(0.86, 0.14, 6, 22), '#1b1b1b', -0.5, 0, 0, 0, Math.PI / 2);
  for (const s of [-1, 1]) { b.add(new THREE.CylinderGeometry(0.62, 0.62, 0.06, 20), '#c4c9d0', s * 0.51, 0, 0, 0, 0, Math.PI / 2); b.add(new THREE.CylinderGeometry(0.16, 0.16, 0.08, 10), '#8a9099', s * 0.53, 0, 0, 0, 0, Math.PI / 2); for (let k = 0; k < 5; k++) b.add(new THREE.BoxGeometry(0.06, 0.5, 0.11), '#d8dde3', s * 0.55, Math.cos(k / 5 * Math.PI * 2) * 0.32, Math.sin(k / 5 * Math.PI * 2) * 0.32, k / 5 * Math.PI * 2); }
  return b.geo();
})();
const BRAKE_MAT = new THREE.MeshBasicMaterial({ color: new THREE.Color(3.5, 0.2, 0.2), toneMapped: false });
const REV_MAT = new THREE.MeshBasicMaterial({ color: new THREE.Color(2.5, 2.5, 2.4), toneMapped: false });
const BLINK_MAT = new THREE.MeshBasicMaterial({ color: new THREE.Color(3, 1.6, 0.1), toneMapped: false });
const DASH_MAT = new THREE.MeshBasicMaterial({ color: new THREE.Color(0.4, 1.6, 2.4), toneMapped: false });
const ROCKET_GEO = (() => { const b = new GeoBag(); b.add(new THREE.CylinderGeometry(0.12, 0.12, 0.9, 6), '#5d6b52', 0, 0, 0, Math.PI / 2); b.add(new THREE.ConeGeometry(0.12, 0.3, 6), '#c8102e', 0, 0, 0.6, Math.PI / 2); return b.geo(); })();

function buildVehicleMesh(type, color) {
  const g = new THREE.Group(), bag = new GeoBag(), wheels = [];
  const mat = carPaint(type);
  const mkSiren = (y, z, w = 0.3) => { siren = [new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.15, w), new THREE.MeshBasicMaterial({ color: 0xff2020 })), new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.15, w), new THREE.MeshBasicMaterial({ color: 0x2050ff }))]; siren[0].position.set(0.3, y, z); siren[1].position.set(-0.3, y, z); g.add(...siren); };
  const GL = '#121a26', HL = '#fff7da', TL = '#ff2424';
  let rotor = null, tail = null, siren = null, blink = null, brakeMesh = null, revMesh = null, cabin = null, wheelSteer = null; const lbag = new GeoBag();
  if (type === 'jet') { const pm = planeMesh(color, '#1f3a6b'); g.add(pm); g.rotation.order = 'YXZ'; return { group: g, mat: pm.material, wheels: [], rotor, tail, siren }; }
  const wheel = (x, y, z, r, w) => { const m = new THREE.Mesh(WHEEL_GEO, VC_MAT); m.scale.set(w, r, r); m.position.set(x, y, z); m.castShadow = true; g.add(m); wheels.push(m); };
  const car = (L, W, H, wr, ch, cl, co, col) => {
    const y0 = wr + 0.05;
    bag.box(W, H, L, col, 0, y0 + H / 2, 0);
    const sh = new THREE.Shape(), b0 = -cl / 2, b1 = cl / 2, t0 = -cl / 2 + cl * 0.2, t1 = cl / 2 - cl * 0.32;
    sh.moveTo(b0, 0); sh.lineTo(b1, 0); sh.lineTo(t1, ch); sh.lineTo(t0, ch); sh.closePath();
    const cg = new THREE.ExtrudeGeometry(sh, { depth: W * 0.86, bevelEnabled: false }); cg.translate(0, 0, -W * 0.43); cg.rotateY(-Math.PI / 2);
    bag.add(cg, GL, 0, y0 + H, co);
    bag.box(W * 0.8, 0.06, (t1 - t0) * 0.98, col, 0, y0 + H + ch + 0.02, co + (t0 + t1) / 2);
    bag.box(W * 1.005, 0.16, L * 0.5, '#1e2024', 0, y0 + 0.1, 0);
    bag.box(W * 0.5, H * 0.35, 0.05, '#15171a', 0, y0 + H * 0.45, L / 2 + 0.01);
    for (const f of [-1, 1]) bag.box(0.55, 0.13, 0.03, '#f4f4f4', 0, y0 + 0.3, f * (L / 2 + 0.03));
    for (const s2 of [-1, 1]) bag.box(0.08, 0.12, 0.22, col, s2 * (W / 2 + 0.06), y0 + H + 0.12, co + cl * 0.3);
    bag.box(W * 1.01, 0.18, 0.3, '#202226', 0, y0 + 0.12, L / 2 - 0.1); bag.box(W * 1.01, 0.18, 0.3, '#202226', 0, y0 + 0.12, -L / 2 + 0.1);
    for (const s of [-1, 1]) { lbag.box(0.42, 0.14, 0.06, HL, s * W * 0.32, y0 + H * 0.7, L / 2); lbag.box(0.42, 0.12, 0.06, TL, s * W * 0.32, y0 + H * 0.7, -L / 2); }
    for (const s of [-1, 1]) for (const f of [-1, 1]) wheel(s * (W / 2 - 0.06), wr, f * L * 0.32, wr, 0.32);
    // feux stop, recul, clignotants
    const bm = new GeoBag(); for (const s of [-1, 1]) bm.box(0.44, 0.14, 0.04, '#ffffff', s * W * 0.32, y0 + H * 0.7, -L / 2 - 0.035);
    brakeMesh = new THREE.Mesh(bm.geo(), BRAKE_MAT); brakeMesh.visible = false; g.add(brakeMesh);
    const rv = new GeoBag(); for (const s of [-1, 1]) rv.box(0.12, 0.09, 0.04, '#ffffff', s * W * 0.15, y0 + H * 0.7, -L / 2 - 0.035);
    revMesh = new THREE.Mesh(rv.geo(), REV_MAT); revMesh.visible = false; g.add(revMesh);
    blink = { L: [], R: [] };
    for (const [side, sx] of [['L', 1], ['R', -1]]) for (const fz of [1, -1]) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.1, 0.05), BLINK_MAT); m.position.set(sx * (W / 2 - 0.08), y0 + H * 0.72, fz * (L / 2 + 0.03)); m.visible = false; g.add(m); blink[side].push(m); }
    // habitacle (visible en vue 1re personne)
    const ib = new GeoBag();
    ib.box(W * 0.84, 0.28, 0.5, '#1d1f22', 0, y0 + H + 0.06, co + cl * 0.26);
    for (const s of [-1, 1]) { ib.box(0.5, 0.12, 0.55, '#3a2a22', s * W * 0.21, y0 + H * 0.55, co - cl * 0.05); ib.box(0.5, 0.65, 0.12, '#3a2a22', s * W * 0.21, y0 + H * 0.85, co - cl * 0.05 - 0.3); }
    ib.box(0.22, 0.25, 0.9, '#1d1f22', 0, y0 + H * 0.6, co + 0.05);
    cabin = ib.mesh(VC_MAT); cabin.visible = false; cabin.castShadow = false; g.add(cabin);
    const dial = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 0.1), DASH_MAT); dial.position.set(W * 0.21, y0 + H + 0.21, co + cl * 0.26 - 0.26); dial.rotation.x = -0.4; cabin.add(dial);
    wheelSteer = new THREE.Mesh(new THREE.TorusGeometry(0.17, 0.022, 6, 18), new THREE.MeshStandardMaterial({ color: 0x1b1b1b, roughness: 0.6 }));
    wheelSteer.position.set(W * 0.21, y0 + H + 0.12, co + cl * 0.14); wheelSteer.rotation.set(-1.15, 0, 0); wheelSteer.rotation.order = 'XYZ'; cabin.add(wheelSteer);
    return y0 + H + ch;
  };
  switch (type) {
    case 'supercar': car(4.6, 2.05, 0.55, 0.36, 0.46, 1.9, -0.2, color); bag.box(1.9, 0.06, 0.35, '#111', 0, 1.3, -2.15); for (const s of [-1, 1]) { bag.box(0.08, 0.3, 0.2, '#111', s * 0.7, 1.12, -2.15); bag.box(0.06, 0.25, 1.2, '#111', s * 1.03, 0.75, -0.6); } break;
    case 'hyper': car(4.8, 2.1, 0.5, 0.37, 0.42, 1.8, -0.3, color); bag.box(0.08, 0.55, 1.4, color, 0, 1.45, -1.6); bag.box(2.0, 0.06, 0.4, '#111', 0, 1.35, -2.25); break;
    case 'sedan': car(4.5, 1.9, 0.65, 0.35, 0.6, 2.3, -0.2, color); break;
    case 'taxi': { const t = car(4.5, 1.9, 0.65, 0.35, 0.6, 2.3, -0.2, '#efe3c4'); bag.box(1.53, 0.06, 2.08, '#c8102e', 0, t + 0.04, -0.2); bag.box(0.7, 0.24, 0.3, '#ffd23a', 0, t + 0.18, -0.2); break; }
    case 'police': { const t = car(4.6, 1.95, 0.65, 0.36, 0.6, 2.3, -0.2, '#f4f6f8'); for (const s of [-1, 1]) bag.box(0.02, 0.2, 4.0, '#0a7d3b', s * 0.985, 0.75, 0);
      siren = [new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.15, 0.3), new THREE.MeshBasicMaterial({ color: 0xff2020 })), new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.15, 0.3), new THREE.MeshBasicMaterial({ color: 0x2050ff }))];
      siren[0].position.set(0.3, t + 0.1, -0.2); siren[1].position.set(-0.3, t + 0.1, -0.2); g.add(...siren); break; }
    case 'suv': { const t = car(4.9, 2.15, 1.0, 0.48, 0.8, 3.0, -0.45, color); bag.box(1.7, 0.08, 2.4, '#222', 0, t + 0.15, -0.45); bag.add(new THREE.CylinderGeometry(0.42, 0.42, 0.28, 12), '#151515', 0, 1.3, -2.6, Math.PI / 2); break; }
    case 'limo': car(7.6, 2.0, 0.66, 0.36, 0.56, 5.0, -0.3, color); break;
    case 'quad':
      bag.box(1.0, 0.4, 1.7, color, 0, 0.75, 0); bag.box(0.55, 0.15, 0.8, '#111', 0, 1.0, -0.25); bag.box(0.9, 0.06, 0.06, '#222', 0, 1.3, 0.6); bag.box(0.08, 0.4, 0.08, '#222', 0, 1.1, 0.55);
      bag.box(1.3, 0.08, 0.5, color, 0, 1.0, 0.8); bag.box(1.3, 0.08, 0.5, color, 0, 1.0, -0.85);
      for (const s of [-1, 1]) for (const f of [-1, 1]) wheel(s * 0.78, 0.42, f * 0.72, 0.42, 0.42); break;
    case 'moto':
      bag.box(0.32, 0.42, 1.4, color, 0, 0.72, 0.05); bag.box(0.46, 0.3, 0.6, color, 0, 1.0, 0.32); bag.box(0.32, 0.1, 0.72, '#111', 0, 1.0, -0.38);
      bag.box(0.8, 0.05, 0.05, '#222', 0, 1.25, 0.72); bag.box(0.06, 0.6, 0.06, '#888', 0, 0.85, 0.78); lbag.box(0.25, 0.18, 0.08, HL, 0, 1.05, 0.9); lbag.box(0.2, 0.08, 0.05, TL, 0, 0.98, -0.75);
      wheel(0, 0.38, 0.8, 0.38, 0.18); wheel(0, 0.38, -0.78, 0.38, 0.2); break;
    case 'heli':
      bag.box(2.2, 1.9, 3.6, color, 0, 1.55, 0.3); bag.box(2.0, 1.3, 1.4, GL, 0, 1.85, 1.95); bag.box(0.5, 0.5, 5.5, color, 0, 2.0, -4.0); bag.box(0.12, 1.4, 0.9, color, 0, 2.6, -6.5);
      bag.box(2.2, 0.08, 0.7, color, 0, 2.0, -6.0);
      for (const s of [-1, 1]) { bag.box(0.12, 0.12, 4.2, '#222', s * 1.0, 0.12, 0.3); bag.box(0.08, 0.5, 0.08, '#222', s * 0.95, 0.4, 1.2); bag.box(0.08, 0.5, 0.08, '#222', s * 0.95, 0.4, -0.7); }
      bag.box(0.2, 0.5, 0.2, '#333', 0, 2.7, 0.3);
      rotor = new THREE.Mesh(new GeoBag().box(11, 0.06, 0.4, '#1d1d1d', 0, 0, 0).box(0.4, 0.06, 11, '#1d1d1d', 0, 0, 0).geo(), VC_MAT); rotor.position.set(0, 2.98, 0.3); g.add(rotor);
      tail = new THREE.Mesh(new GeoBag().box(0.05, 1.7, 0.2, '#1d1d1d', 0, 0, 0).geo(), VC_MAT); tail.position.set(0.15, 2.6, -6.6); g.add(tail); break;
    case 'jetski':
      bag.box(1.1, 0.5, 2.8, color, 0, -0.05, 0); bag.box(0.9, 0.35, 0.7, color, 0, 0.05, 1.6); bag.box(0.5, 0.18, 1.1, '#111', 0, 0.3, -0.35); bag.box(0.8, 0.06, 0.06, '#222', 0, 0.75, 0.55); bag.box(0.12, 0.45, 0.12, '#333', 0, 0.45, 0.6); break;
    case 'yacht':
      bag.box(4.2, 1.8, 14, '#f6f6f6', 0, 0.1, 0); bag.box(3.0, 1.6, 3, '#f6f6f6', 0, 0.2, 8.0); bag.box(4.25, 0.3, 14.05, color, 0, -0.4, 0);
      bag.box(3.2, 1.6, 6, '#f2f2f2', 0, 1.8, -1); bag.box(3.25, 0.5, 5.5, GL, 0, 2.0, -1); bag.box(2.6, 1.0, 3, '#e8e8e8', 0, 3.1, -1.5); bag.box(2.65, 0.35, 2.6, GL, 0, 3.2, -1.3);
      bag.box(0.1, 2.5, 0.1, '#ccc', 0, 4.8, -1.5); break;
    case 'bus': {
      const wr = 0.5, L = 11, W = 2.5, c = color;
      bag.box(W, 2.7, L, c, 0, wr + 0.2 + 1.35, 0); bag.box(W + 0.02, 1.05, L - 1.8, GL, 0, wr + 2.05, -0.4);
      bag.box(W - 0.2, 1.5, 0.06, GL, 0, wr + 1.95, L / 2 + 0.01); bag.box(1.7, 0.32, 0.06, '#ffb000', 0, wr + 2.9, L / 2 + 0.02);
      bag.box(W * 0.7, 0.35, 3, '#d8d8d8', 0, wr + 3.2, -1.5); bag.box(W + 0.03, 0.3, L, '#f4f4f4', 0, wr + 0.65, 0);
      for (const z of [3.6, -0.6]) bag.box(0.04, 2.3, 1.3, GL, -(W / 2 + 0.01), wr + 1.4, z);
      for (const s of [-1, 1]) { lbag.box(0.42, 0.18, 0.06, HL, s * W * 0.36, wr + 0.65, L / 2); lbag.box(0.3, 0.3, 0.06, TL, s * W * 0.4, wr + 0.8, -L / 2); }
      for (const s of [-1, 1]) for (const z of [3.7, -3.5]) wheel(s * (W / 2 - 0.15), wr, z, wr, 0.42);
      break; }
    case 'ambulance': case 'van': {
      const wr = 0.42, c = type === 'van' ? '#f2c230' : '#f6f7f9';
      bag.box(2.2, 2.4, 3.6, c, 0, wr + 0.15 + 1.2, -0.9); bag.box(2.1, 1.3, 1.6, c, 0, wr + 0.15 + 0.65, 1.7);
      bag.box(2.0, 0.85, 0.9, GL, 0, wr + 1.75, 1.35); bag.box(1.95, 0.2, 1.0, c, 0, wr + 2.25, 1.35);
      if (type === 'ambulance') { bag.box(2.22, 0.3, 3.62, '#d01c2b', 0, wr + 1.15, -0.9); bag.box(2.22, 0.15, 5.0, '#ffd23a', 0, wr + 0.75, -0.2); for (const s of [-1, 1]) { bag.box(0.03, 0.9, 0.3, '#d01c2b', s * 1.115, wr + 2.0, -1.2); bag.box(0.03, 0.3, 0.9, '#d01c2b', s * 1.115, wr + 2.0, -1.2); } mkSiren(wr + 2.45, 1.3); }
      else { bag.box(2.22, 0.35, 3.62, '#1b1b1b', 0, wr + 1.0, -0.9); bag.box(0.03, 0.6, 0.6, '#d01c2b', 1.115, wr + 1.9, -1.2); }
      for (const s of [-1, 1]) { lbag.box(0.36, 0.16, 0.06, HL, s * 0.75, wr + 0.65, 2.51); lbag.box(0.25, 0.3, 0.06, TL, s * 0.9, wr + 0.9, -2.71); }
      for (const s of [-1, 1]) for (const z of [1.65, -1.9]) wheel(s * 0.98, wr, z, wr, 0.3);
      break; }
    case 'firetruck': {
      const wr = 0.55, L = 9, W = 2.5;
      bag.box(W, 2.1, 2.4, '#c8102e', 0, wr + 0.2 + 1.05, L / 2 - 1.2); bag.box(W * 0.95, 0.9, 0.06, GL, 0, wr + 1.85, L / 2 + 0.01);
      for (const s of [-1, 1]) bag.box(0.04, 0.8, 1.6, GL, s * (W / 2 + 0.01), wr + 1.85, L / 2 - 1.1);
      bag.box(W, 1.9, L - 2.6, '#c8102e', 0, wr + 0.2 + 0.95, -1.3); bag.box(W + 0.02, 1.1, L - 3.4, '#c9ccd1', 0, wr + 1.1, -1.3);
      bag.box(W + 0.04, 0.16, L, '#f4f4f4', 0, wr + 0.45, 0);
      for (const s of [-1, 1]) bag.box(0.12, 0.12, L - 1.2, '#d8d8d8', s * 0.45, wr + 2.35, -0.8);
      for (let i = 0; i < 12; i++) bag.box(0.9, 0.06, 0.08, '#d8d8d8', 0, wr + 2.35, -L / 2 + 1 + i * 0.62);
      for (const s of [-1, 1]) { lbag.box(0.4, 0.18, 0.06, HL, s * W * 0.34, wr + 0.75, L / 2); lbag.box(0.3, 0.3, 0.06, TL, s * W * 0.4, wr + 0.8, -L / 2 - 0.0); }
      for (const s of [-1, 1]) for (const z of [L / 2 - 1.5, -2.2, -3.5]) wheel(s * (W / 2 - 0.15), wr, z, wr, 0.4);
      mkSiren(wr + 2.45, L / 2 - 1.2, 0.4); break; }
    case 'tram': {
      const wr = 0.45, W = 2.4;
      for (const [z0, L] of [[4.3, 8.4], [-4.3, 8.4]]) {
        bag.box(W, 1.5, L, color, 0, wr + 0.2 + 0.75, z0); bag.box(W, 1.3, L, '#f4f4f4', 0, wr + 0.95 + 1.3, z0);
        bag.box(W + 0.02, 0.95, L - 0.8, GL, 0, wr + 2.25, z0); bag.box(W - 0.1, 0.12, L, '#cfd3d8', 0, wr + 2.98, z0);
        for (const s of [-1, 1]) for (const z of [z0 - 2.6, z0 + 2.6]) wheel(s * 0.9, wr, z, wr, 0.25);
      }
      bag.box(W - 0.4, 2.4, 0.3, '#2a2f36', 0, wr + 1.6, 0);
      bag.box(W * 0.9, 1.0, 0.06, GL, 0, wr + 2.2, 8.51); bag.box(W * 0.9, 1.0, 0.06, GL, 0, wr + 2.2, -8.51);
      bag.box(1.2, 0.25, 0.06, '#ffb000', 0, wr + 2.8, 8.52);
      bag.box(0.08, 0.9, 0.08, '#333', 0, wr + 3.4, 2.5); bag.box(1.4, 0.06, 0.12, '#333', 0, wr + 3.85, 2.5);
      for (const s of [-1, 1]) { lbag.box(0.35, 0.18, 0.06, HL, s * 0.8, wr + 0.8, 8.52); lbag.box(0.3, 0.25, 0.06, TL, s * 0.85, wr + 0.85, -8.52); }
      break; }
    case 'tractor':
      bag.box(1.1, 1.0, 2.2, color, 0, 1.25, 0.6); bag.box(1.0, 0.25, 0.1, '#222', 0, 1.2, 1.72);
      for (const [x, z] of [[-0.75, -0.05], [0.75, -0.05], [-0.75, -1.45], [0.75, -1.45]]) bag.box(0.08, 1.6, 0.08, '#222', x, 2.3, z);
      bag.box(1.7, 0.1, 1.7, color, 0, 3.15, -0.75); bag.box(1.4, 0.9, 0.04, '#9fc5d4', 0, 2.4, -0.05);
      bag.box(0.6, 0.15, 0.6, '#111', 0, 1.7, -0.8); bag.add(new THREE.CylinderGeometry(0.07, 0.07, 1.3, 6), '#333', 0.35, 2.3, 1.2);
      bag.box(1.9, 0.12, 0.9, color, 0, 1.75, -1.0);
      for (const s of [-1, 1]) { wheel(s * 0.98, 0.85, -0.9, 0.85, 0.5); wheel(s * 0.75, 0.45, 1.3, 0.45, 0.3); }
      break;
  }
  const body = bag.mesh(mat); g.add(body);
  if (lbag.g.length) { const lm = lbag.mesh(LIGHT_MAT); lm.castShadow = false; g.add(lm); }
  g.rotation.order = 'YXZ';
  return { group: g, mat, wheels, rotor, tail, siren, blink, brakeMesh, revMesh, cabin, wheelSteer };
}

const vehicles = [];
class Vehicle {
  constructor(type, x, z, yaw = 0, color, y) {
    this.type = type; this.def = VDEF[type];
    this.color = color || (type === 'hyper' ? '#e2b13c' : type === 'bus' ? pick(['#d6262f', '#f2c230', '#1f5fbf']) : type === 'tractor' ? pick(['#2e7d32', '#c8102e']) : type === 'heli' ? pick(['#1c1c1e', '#f5f5f2', '#c8102e', '#0f2a4a']) : pick(CAR_COLORS));
    const b = buildVehicleMesh(type, this.color); Object.assign(this, b);
    this.pos = new V3(x, y ?? surfaceY(x, z), z); this.yaw = yaw; this.speed = 0; this.vy = 0; this.air = false;
    this.vel = new V3(); this.loose = false; this.spin = 0; this.rollV = 0;
    this.pitch = 0; this.roll = 0; this.driver = null; this.ai = null; this.hp = 10; this.burn = 0;
    this.rotorSpd = 0; this.fromTraffic = false; this.spawned = false; this.sirenOn = false; this.t = Math.random() * 10;
    ENV_MATS.add(this.mat); this.mat.envMapIntensity = envLevel;
    scene.add(this.group); vehicles.push(this); this.sync();
  }
  get fwd() { return new V3(Math.sin(this.yaw), 0, Math.cos(this.yaw)); }
  sync() { this.group.position.copy(this.pos); this.group.rotation.set(this.pitch, this.yaw, this.roll); }
  remove() { scene.remove(this.group); this.group.traverse(o => { if (o.geometry && o.geometry !== WHEEL_GEO) o.geometry.dispose(); }); const i = vehicles.indexOf(this); if (i >= 0) vehicles.splice(i, 1); }
}

/* ---------- Physique véhicule */
function driveVehicle(v, c, dt) {
  const d = v.def;
  if (d.kind === 'heli') return driveHeli(v, c, dt);
  if (d.kind === 'plane') return drivePlane(v, c, dt);
  const water = isWater(v.pos.x, v.pos.z);
  let max = d.max * (c.nitro ? 1.45 : 1) * (S.powers.superSpeed && v.driver === 'player' ? 1.35 : 1), acc = d.acc * (c.nitro ? 1.9 : 1);
  if (d.kind === 'boat') { if (!water) max *= 0.08; }
  else {
    if (water) max *= 0.35;
    if (v.pos.x > 580 && Math.abs(v.pos.z - HWY_Z) > 12 && !d.offroad) max *= 0.7;
  }
  if (c.thr > 0) v.speed += (v.speed < 0 ? acc * 2.5 : acc) * c.thr * dt;
  else if (c.thr < 0) v.speed += (v.speed > 0 ? -acc * 2.4 : -acc * 0.6) * -c.thr * dt;
  else v.speed *= 1 - 0.5 * dt;
  if (c.brake) v.speed *= 1 - 2.2 * dt;
  v.braking = c.brake || (c.thr < 0 && v.speed > 0.5);
  if (v.air) v.speed *= 1 - 0.05 * dt;
  v.speed = clamp(v.speed, -max * 0.35, Math.max(max, v.speed * (1 - 1.5 * dt)));
  if (!v.air || d.kind === 'boat') {
    const k = d.kind === 'boat' ? 1 : clamp(v.speed / 8, -1, 1);
    v.yaw += c.steer * d.turn * dt * k * (c.brake ? 1.5 : 1);
  }
  const f = v.fwd, ox = v.pos.x, oz = v.pos.z;
  v.pos.x += f.x * v.speed * dt; v.pos.z += f.z * v.speed * dt;
  // collisions avec les bâtiments
  const hit = collide(v.pos, d.r * 0.75, 1.5);
  if (hit) { if (Math.abs(v.speed) > 20 && v.driver === 'player') { shake(0.4); SFX.burst(0.2, 400, 0.4); } v.speed *= -0.25; }
  vehicleGround(v, dt, d.kind === 'boat' ? 1 : 0);
  // inclinaisons
  if (d.kind === 'boat') { v.t += dt; v.pitch = Math.sin(v.t * 2) * 0.03 - clamp(v.speed / d.max, 0, 1) * 0.08; v.roll = Math.sin(v.t * 1.6) * 0.04 - c.steer * 0.15 * clamp(v.speed / d.max, 0, 1); }
  else if (d.kind === 'bike') { v.roll = lerp(v.roll, -c.steer * clamp(v.speed / d.max, 0, 1) * 0.6, 6 * dt); if (!v.air) v.pitch = lerp(v.pitch, terrainPitch(v, 1.6), 8 * dt); }
  else if (!v.air) { v.pitch = lerp(v.pitch, terrainPitch(v, 2.2), 8 * dt); v.roll = lerp(v.roll, terrainRoll(v, 1), 8 * dt); }
  for (const w of v.wheels) w.rotation.x += v.speed * dt / w.scale.y;
  if (v.siren) { v.t += dt; const on = v.sirenOn && Math.floor(v.t * 6) % 2 === 0; v.siren[0].visible = !v.sirenOn || on; v.siren[1].visible = !v.sirenOn || !on; }
  v.pos.x = clamp(v.pos.x, BOUNDS.x0, BOUNDS.x1); v.pos.z = clamp(v.pos.z, BOUNDS.z0, BOUNDS.z1);
}
function terrainPitch(v, L) { const f = v.fwd, a = heightAt(v.pos.x + f.x * L, v.pos.z + f.z * L, v.pos.y), b = heightAt(v.pos.x - f.x * L, v.pos.z - f.z * L, v.pos.y); return Math.atan2(b - a, 2 * L); }
function terrainRoll(v, W) { const f = v.fwd, lx = f.z, lz = -f.x, a = heightAt(v.pos.x + lx * W, v.pos.z + lz * W, v.pos.y), b = heightAt(v.pos.x - lx * W, v.pos.z - lz * W, v.pos.y); return Math.atan2(a - b, 2 * W); }
function vehicleGround(v, dt, isBoat) {
  let gH = heightAt(v.pos.x, v.pos.z, v.pos.y);
  if (isBoat && isWater(v.pos.x, v.pos.z)) gH = Math.max(gH, WATER_Y + 0.05);
  if (v.air) {
    v.vy -= G * dt; v.pos.y += v.vy * dt;
    if (v.pos.y <= gH) { if (v.vy < -12 && v.driver === 'player') { shake(0.35); SFX.burst(0.25, 300, 0.4); } v.pos.y = gH; v.air = false; v.vy = 0; }
  } else {
    const dy = gH - v.pos.y;
    if (dy < -0.35) { v.air = true; v.vy = Math.max(v.vy, 0); }
    else { v.vy = lerp(v.vy, dy / Math.max(dt, 1e-3), 0.5); v.vy = clamp(v.vy, -20, 30); v.pos.y = gH; }
  }
}
function drivePlane(v, c, dt) {
  const d = v.def, piloted = v.driver === 'player', max = d.max * (c.nitro ? 1.35 : 1);
  if (piloted && c.thr) v.speed += (c.thr > 0 ? d.acc : -d.acc * 1.5) * Math.abs(c.thr) * dt;
  v.speed *= 1 - (piloted ? 0.05 : 0.8) * dt; v.speed = clamp(v.speed, -4, max);
  const gH = heightAt(v.pos.x, v.pos.z, v.pos.y), grounded = v.pos.y <= gH + 0.1;
  const lift = smooth(34, 50, v.speed), climb = (c.up ? 1 : 0) - (c.down ? 1 : 0);
  let tv = climb * 20 * lift - (1 - lift) * 14; if (grounded && tv < 0) tv = 0;
  v.vy = lerp(v.vy, tv, 1 - Math.exp(-2 * dt));
  v.yaw += (c.steer || 0) * d.turn * dt * clamp(v.speed / 25, 0, 1) * (grounded ? 0.5 : 1);
  const f = v.fwd; v.pos.x += f.x * v.speed * dt; v.pos.z += f.z * v.speed * dt; v.pos.y = Math.min(v.pos.y + v.vy * dt, 1200);
  if (collide(v.pos, d.r * 0.6, 3)) { v.speed *= 0.3; if (piloted) shake(0.5); }
  const g2 = heightAt(v.pos.x, v.pos.z, v.pos.y); if (v.pos.y < g2) { if (v.vy < -10 && piloted) shake(0.6); v.pos.y = g2; v.vy = Math.max(0, v.vy); }
  v.pitch = lerp(v.pitch, -clamp(v.vy / 30, -0.45, 0.45), 3 * dt); v.roll = lerp(v.roll, grounded ? 0 : -(c.steer || 0) * 0.7, 2.5 * dt);
  v.pos.x = clamp(v.pos.x, BOUNDS.x0, BOUNDS.x1); v.pos.z = clamp(v.pos.z, BOUNDS.z0, BOUNDS.z1);
}
function driveHeli(v, c, dt) {
  const d = v.def, piloted = v.driver === 'player';
  v.rotorSpd = lerp(v.rotorSpd, piloted ? 1 : 0, dt * 0.8);
  v.rotor.rotation.y += v.rotorSpd * 30 * dt; v.tail.rotation.x += v.rotorSpd * 40 * dt;
  const gH = heightAt(v.pos.x, v.pos.z, v.pos.y);
  const grounded = v.pos.y <= gH + 0.05;
  if (piloted && v.rotorSpd > 0.6) {
    const max = d.max * (c.nitro ? 1.6 : 1) * (S.powers.superSpeed ? 1.5 : 1);
    v.speed += c.thr * d.acc * dt; v.speed *= 1 - 0.35 * dt; v.speed = clamp(v.speed, -max * 0.4, max);
    v.yaw += c.steer * d.turn * dt;
    const tv = (c.up ? 16 : 0) - (c.down ? 16 : 0);
    v.vy = lerp(v.vy, tv, 3 * dt);
    if (grounded && v.vy <= 0) { v.speed *= 1 - 4 * dt; }
  } else { v.vy -= G * 0.6 * dt; v.speed *= 1 - 1.5 * dt; }
  const f = v.fwd;
  v.pos.x += f.x * v.speed * dt; v.pos.z += f.z * v.speed * dt; v.pos.y += v.vy * dt;
  v.pos.y = Math.min(v.pos.y, 900);
  const hit = collide(v.pos, d.r * 0.8, 3); if (hit) v.speed *= -0.3;
  const g2 = heightAt(v.pos.x, v.pos.z, v.pos.y);
  if (v.pos.y < g2) { v.pos.y = g2; v.vy = Math.max(0, v.vy); }
  v.pitch = lerp(v.pitch, clamp(v.speed / d.max, -1, 1) * 0.22 * (v.pos.y > g2 + 0.5 ? 1 : 0), 3 * dt);
  v.roll = lerp(v.roll, -c.steer * 0.25 * (v.pos.y > g2 + 0.5 ? 1 : 0), 3 * dt);
  v.pos.x = clamp(v.pos.x, BOUNDS.x0, BOUNDS.x1); v.pos.z = clamp(v.pos.z, BOUNDS.z0, BOUNDS.z1);
}
function looseVehicle(v, dt) {
  v.vel.y -= G * dt; v.pos.addScaledVector(v.vel, dt);
  v.yaw += v.spin * dt; v.spin *= 1 - 1.2 * dt;
  const hit = collide(v.pos, v.def.r * 0.75, 1.5); if (hit) { v.vel.x *= -0.3; v.vel.z *= -0.3; }
  const gH = heightAt(v.pos.x, v.pos.z, v.pos.y) + (v.def.kind === 'boat' && isWater(v.pos.x, v.pos.z) ? 0.5 : 0);
  if (v.pos.y <= gH) {
    v.pos.y = gH;
    if (v.vel.y < -4) { v.vel.y *= -0.3; } else v.vel.y = 0;
    v.vel.x *= 1 - 3 * dt; v.vel.z *= 1 - 3 * dt;
    v.roll = lerp(v.roll, 0, 4 * dt); v.pitch = lerp(v.pitch, 0, 4 * dt);
    if (v.vel.lengthSq() < 0.5 && Math.abs(v.spin) < 0.3) { v.loose = false; v.speed = 0; v.roll = 0; v.pitch = 0; }
  } else { v.roll += v.rollV * dt; v.pitch += v.rollV * 0.4 * dt; }
}
function makeLoose(v, vx, vy, vz, spin = rand(-3, 3)) {
  if (v.driver === 'ai') { ejectAIDriver(v); }
  v.ai = null; v.driver = v.driver === 'player' ? 'player' : null;
  if (v.driver === 'player') { v.speed *= 0.4; v.vy += vy * 0.5; v.air = true; return; }
  v.loose = true; v.vel.set(vx + v.fwd.x * v.speed, vy, vz + v.fwd.z * v.speed); v.spin = spin; v.rollV = rand(-4, 4) * (vy > 8 ? 1 : 0.2); v.speed = 0;
}
function burnVehicle(v) { v.burn = 25; v.mat.color.set(0x2a2a2a); v.hp = 0; }

/* ---------- Circulation (IA) */
function lanePointAhead(v) {
  const a = v.ai;
  if (a.axis === 'z') return { x: a.line - LANE * a.dir, z: v.pos.z + a.dir * 10 };
  return { x: v.pos.x + a.dir * 10, z: a.line + LANE * a.dir };
}
function nextNode(along, dir, list) { for (const n of (dir > 0 ? list : [...list].reverse())) if ((n - along) * dir > 3) return n; return null; }
function aiPlan(v) {
  const a = v.ai, along = a.axis === 'z' ? v.pos.z : v.pos.x, cross = a.axis === 'z' ? ROADS_Z : ROADS_X;
  a.next = nextNode(along, a.dir, cross);
  const opts = [];
  if (a.next !== null && nextNode(a.next, a.dir, cross) !== null) opts.push('straight', 'straight');
  const otherList = a.axis === 'z' ? ROADS_X : ROADS_Z;
  const rightDir = a.axis === 'z' ? -a.dir : a.dir, leftDir = -rightDir;
  if (a.next !== null) {
    if (nextNode(a.line, rightDir, otherList) !== null) opts.push('right');
    if (nextNode(a.line, leftDir, otherList) !== null) opts.push('left');
  }
  a.choice = opts.length ? pick(opts) : 'uturn';
  a.rightDir = rightDir; a.leftDir = leftDir;
}
function aiControl(v, dt) {
  const a = v.ai, along = a.axis === 'z' ? v.pos.z : v.pos.x;
  if (a.next === null || a.next === undefined) { aiPlan(v); }
  if (a.next === null) { a.dir = -a.dir; aiPlan(v); }
  const dist = (a.next - along) * a.dir;
  const turnAt = a.choice === 'right' ? 7.5 : a.choice === 'left' ? -1.5 : -2;
  if (dist < turnAt) {
    if (a.choice === 'straight' || a.choice === 'uturn') { aiPlan(v); }
    else { const nd = a.choice === 'right' ? a.rightDir : a.leftDir; const oldLine = a.line; a.axis = a.axis === 'z' ? 'x' : 'z'; a.line = a.next; a.dir = nd; a.next = null; aiPlan(v); }
  }
  const t = lanePointAhead(v);
  const want = Math.atan2(t.x - v.pos.x, t.z - v.pos.z);
  const diff = wrapA(want - v.yaw);
  let target = a.speed;
  if (a.choice !== 'straight' && dist < 18 && dist > -3) target = Math.min(target, 8);
  if (Math.abs(diff) > 0.6) target = Math.min(target, 7);
  // feu rouge ou orange : on s'arrête à la ligne
  if (lightState(a.axis) !== 'g' && dist > 9.5 && dist < 26) target = Math.min(target, Math.max(0, (dist - 11.5) * 0.8));
  // bus : arrêt de quelques secondes aux abribus
  if (v.type === 'bus') { v.busCool = (v.busCool || 0) - dt; if (v.busWait > 0) { v.busWait -= dt; target = 0; } else if (v.busCool <= 0) for (const s of BUS_STOPS) if (Math.abs(s.x - v.pos.x) < 9 && Math.abs(s.z - v.pos.z) < 9) { v.busWait = 5; v.busCool = 16; break; } }
  v.blinkSide = (a.choice === 'left' ? 'L' : a.choice === 'right' ? 'R' : null); if (dist > 38 || dist < -6) v.blinkSide = null;
  // obstacles devant (joueur, voitures, piétons)
  const f = v.fwd, look = 11 + Math.abs(v.speed) * 0.4;
  const blocked = (px, pz, rad) => { const dx = px - v.pos.x, dz = pz - v.pos.z, fd = dx * f.x + dz * f.z; if (fd < 1 || fd > look) return false; return Math.abs(dx * f.z - dz * f.x) < rad; };
  const pp = P.vehicle ? P.vehicle.pos : P.pos;
  if (blocked(pp.x, pp.z, 2.6)) target = 0;
  if (target > 0) for (const o of vehicles) if (o !== v && Math.abs(o.pos.x - v.pos.x) < 20 && Math.abs(o.pos.z - v.pos.z) < 20 && blocked(o.pos.x, o.pos.z, 2.4)) { target = 0; break; }
  if (target > 0) for (const p of peds) if (Math.abs(p.pos.x - v.pos.x) < 14 && Math.abs(p.pos.z - v.pos.z) < 14 && blocked(p.pos.x, p.pos.z, 1.8)) { target = 0; break; }
  v.honk = target === 0 && blocked(pp.x, pp.z, 2.6);
  return { thr: v.speed < target - 0.5 ? 1 : v.speed > target + 1 ? -1 : 0, steer: clamp(diff * 2.2, -1, 1), brake: false, nitro: false };
}
const TRAFFIC_TYPES = ['sedan', 'sedan', 'sedan', 'taxi', 'taxi', 'suv', 'supercar', 'limo', 'police', 'sedan', 'taxi', 'bus', 'van', 'sedan', 'bus'];
function spawnTraffic(near = true) {
  const pp = P.vehicle ? P.vehicle.pos : P.pos;
  for (let tries = 0; tries < 25; tries++) {
    const axis = Math.random() < 0.5 ? 'z' : 'x', dir = Math.random() < 0.5 ? 1 : -1;
    let x, z, line;
    if (axis === 'z') { line = pick(ROADS_X); z = rand(-530, 890); x = line - LANE * dir; }
    else { line = pick(ROADS_Z); x = rand(-290, 530); z = line + LANE * dir; }
    const d = Math.hypot(x - pp.x, z - pp.z);
    if (near && (d < 90 || d > 330)) continue;
    if (vehicles.some(o => Math.hypot(o.pos.x - x, o.pos.z - z) < 12)) continue;
    const yaw = axis === 'z' ? (dir > 0 ? 0 : Math.PI) : (dir > 0 ? Math.PI / 2 : -Math.PI / 2);
    const v = new Vehicle(pick(TRAFFIC_TYPES), x, z, yaw);
    v.driver = 'ai'; v.fromTraffic = true; v.ai = { axis, line, dir, speed: rand(11, 17), next: null }; v.speed = v.ai.speed * 0.7;
    return v;
  }
}
function ejectAIDriver(v) {
  const p = peds.length ? peds.reduce((a, b) => (dist2(a.pos, P.pos) > dist2(b.pos, P.pos) ? a : b)) : null;
  if (!p) return;
  const f = v.fwd; p.pos.set(v.pos.x + f.z * 2.2, 0, v.pos.z - f.x * 2.2); p.state = 'flee'; p.t = 6; p.model.rotation.x = 0;
}
const dist2 = (a, b) => (a.x - b.x) ** 2 + (a.z - b.z) ** 2;
