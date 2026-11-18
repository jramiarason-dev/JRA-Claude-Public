/* =====================================================================
   PERSONNAGES
   ===================================================================== */
const SKINS = ['#f7dcc8', '#eac0a0', '#dba67f', '#c68b59', '#a8693f', '#8d5524', '#6b3e1f', '#45260f'];
const HAIR_COLORS = ['#16100b', '#3b2416', '#6a4327', '#a8743e', '#dcb76e', '#e9e4d6', '#b23a2a', '#2d5bd6', '#e05aa8', '#7a7a7a'];
const CLOTH = ['#f5f5f2', '#1c1c1e', '#2a6fdb', '#c8102e', '#0a7d3b', '#f0bf62', '#6d3fc0', '#ff7a1a', '#14b8c4', '#e05aa8', '#8a5a33', '#4b5563', '#0f2a4a', '#d9c7a1'];
const DEFAULT_CHAR = { name: 'Joueur', body: 'homme', height: 1, build: 1, skin: '#c68b59', hair: 'court', hairColor: '#16100b', beard: 'courte', head: 'aucun', top: 'tshirt', topColor: '#f5f5f2', pants: 'pantalon', pantsColor: '#0f2a4a', shoes: '#f5f5f2', glasses: true, watch: true, chain: false, eyes: '#4a3220', motif: 'uni', hatColor: '#1c1c1e', shoeStyle: 'baskets', sole: '#f2f2f2', shoeAccent: '#c8102e', gloves: false };
const OPTS = {
  body: [['homme', 'Homme'], ['femme', 'Femme']],
  hair: [['court', 'Court'], ['long', 'Long'], ['queue', 'Queue'], ['chignon', 'Chignon'], ['afro', 'Afro'], ['crete', 'Crête'], ['chauve', 'Rasé']],
  beard: [['aucune', 'Aucune'], ['courte', 'Courte'], ['longue', 'Longue'], ['moustache', 'Moustache'], ['bouc', 'Bouc']],
  head: [['aucun', 'Aucun'], ['ghutra', 'Ghutra'], ['foulard', 'Foulard'], ['casquette', 'Casquette'], ['casquette_inv', 'Casquette à l\'envers'], ['cagoule', 'Cagoule'], ['chapeau', 'Chapeau'], ['bonnet', 'Bonnet']],
  motif: [['uni', 'Uni'], ['carreaux', 'Carreaux'], ['rayures', 'Rayures'], ['fleurs', 'Fleurs']],
  shoeStyle: [['baskets', 'Baskets'], ['montantes', 'Baskets montantes'], ['cuir', 'Chaussures en cuir']],
  top: [['tshirt', 'T-shirt'], ['chemise', 'Chemise'], ['costume', 'Costume'], ['hoodie', 'Sweat'], ['debardeur', 'Débardeur'], ['manteau', 'Manteau'], ['kandura', 'Kandura'], ['abaya', 'Abaya']],
  pants: [['pantalon', 'Pantalon'], ['jean', 'Jean'], ['short', 'Short']],
};
const CHAR_MAT = new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.62, metalness: 0, sheen: 0.35, sheenRoughness: 0.8 });

function randomChar(region = 'dxb') {
  const fem = Math.random() < 0.45, o = { ...DEFAULT_CHAR, name: '' };
  o.body = fem ? 'femme' : 'homme'; o.height = rand(0.92, 1.08); o.build = rand(0.88, 1.15);
  o.skin = pick(SKINS); o.hairColor = Math.random() < 0.8 ? pick(HAIR_COLORS.slice(0, 5)) : pick(HAIR_COLORS);
  o.hair = fem ? pick(['long', 'queue', 'chignon', 'afro', 'court']) : pick(['court', 'court', 'crete', 'chauve', 'afro', 'long']);
  o.beard = fem ? 'aucune' : pick(['aucune', 'courte', 'longue', 'moustache', 'bouc', 'courte']);
  const style = Math.random();
  if (style < 0.25) { o.top = fem ? 'abaya' : 'kandura'; o.topColor = fem ? '#1c1c1e' : '#f5f5f2'; o.head = fem ? 'foulard' : 'ghutra'; }
  else if (style < 0.4) { o.top = 'costume'; o.topColor = pick(['#1c1c1e', '#0f2a4a', '#4b5563', '#d9c7a1']); o.head = 'aucun'; }
  else { o.top = pick(['tshirt', 'chemise', 'hoodie', 'debardeur']); o.topColor = pick(CLOTH); o.head = pick(['aucun', 'aucun', 'casquette', 'chapeau']); }
  if (o.top === 'abaya') o.topColor = pick(['#1c1c1e', '#1c1c1e', '#0f2a4a', '#8a5a33']);
  o.pants = Math.random() < 0.3 ? 'short' : 'pantalon'; o.pantsColor = pick(CLOTH); o.shoes = pick(CLOTH);
  o.glasses = Math.random() < 0.4; o.watch = Math.random() < 0.5; o.chain = Math.random() < 0.15; o.eyes = Math.random() < 0.7 ? pick(['#4a3220', '#6b4f2a', '#1b1b1b']) : pick(['#4a3220', '#2b6cb0', '#3c7a4a', '#6b4f2a', '#8a8f99', '#1b1b1b']);
  o.hatColor = pick(CLOTH); o.shoeStyle = pick(['baskets', 'baskets', 'montantes', 'cuir']); o.sole = Math.random() < 0.7 ? '#f2f2f2' : pick(['#1c1c1e', '#d9c7a1']); o.shoeAccent = pick(CLOTH); o.gloves = Math.random() < 0.03;
  if (o.head === 'casquette' && Math.random() < 0.3) o.head = 'casquette_inv';
  if (o.pants === 'pantalon' && Math.random() < 0.45) o.pants = 'jean';
  if (o.top === 'costume') o.shoeStyle = 'cuir';
  if (region === 'gva') {
    const st = Math.random();
    if (st < 0.4) { o.top = 'manteau'; o.topColor = pick(['#1c1c1e', '#4b5563', '#8a5a33', '#0f2a4a', '#7a1f2b', '#d9c7a1', '#2f5d3a']); o.head = pick(['aucun', 'aucun', 'bonnet', 'chapeau']); }
    else if (st < 0.55) { o.top = 'costume'; o.topColor = pick(['#1c1c1e', '#0f2a4a', '#4b5563']); o.head = 'aucun'; }
    else { o.top = pick(['tshirt', 'chemise', 'hoodie']); o.topColor = pick(CLOTH); o.head = pick(['aucun', 'aucun', 'casquette', 'bonnet']); }
    o.pants = 'pantalon'; o.glasses = Math.random() < 0.2; o.chain = false;
  }
  return o;
}

/* ---------- Personnages articulés : squelette + maillage lissé, matériaux réalistes */
const BONES = ['root', 'hips', 'spine', 'chest', 'neck', 'head', 'uArmL', 'fArmL', 'handL', 'uArmR', 'fArmR', 'handR', 'thighL', 'shinL', 'footL', 'thighR', 'shinR', 'footR', 'jaw', 'lidL', 'lidR', 'fingL', 'fingR'];
const BI = Object.fromEntries(BONES.map((n, i) => [n, i]));
function skeletonLayout(o) {
  const fem = o.body === 'femme', sh = fem ? 0.185 : 0.21;
  return {
    root: [null, 0, 0, 0], hips: ['root', 0, 0.95, 0], spine: ['hips', 0, 1.06, 0], chest: ['spine', 0, 1.3, 0], neck: ['chest', 0, 1.52, 0], head: ['neck', 0, 1.62, 0],
    uArmL: ['chest', sh, 1.465, 0], fArmL: ['uArmL', sh + 0.012, 1.19, 0], handL: ['fArmL', sh + 0.018, 0.945, 0.01],
    uArmR: ['chest', -sh, 1.465, 0], fArmR: ['uArmR', -sh - 0.012, 1.19, 0], handR: ['fArmR', -sh - 0.018, 0.945, 0.01],
    thighL: ['hips', 0.095, 0.92, 0], shinL: ['thighL', 0.1, 0.5, 0.012], footL: ['shinL', 0.1, 0.085, 0],
    thighR: ['hips', -0.095, 0.92, 0], shinR: ['thighR', -0.1, 0.5, 0.012], footR: ['shinR', -0.1, 0.085, 0],
    jaw: ['head', 0, 1.705, 0.03], lidL: ['head', 0.038, 1.753, 0.1], lidR: ['head', -0.038, 1.753, 0.1],
    fingL: ['handL', sh + 0.03, 0.87, 0.01], fingR: ['handR', -sh - 0.03, 0.87, 0.01],
  };
}
/* Catégories de matériau : chaque pièce sait si elle est peau, tissu, cuir, métal… */
const CATS = ['skin', 'hair', 'top', 'pants', 'cloth', 'knit', 'shoe', 'rubber', 'leather', 'metal', 'glass', 'eye'];
class SkinBag {
  constructor() { this.g = []; this.c = 'cloth'; }
  add(geo, color, bone, x = 0, y = 0, z = 0, o = {}) {
    if (!geo.index) geo.setIndex([...Array(geo.attributes.position.count).keys()]);
    if (o.s) geo.scale(...o.s); if (o.rx) geo.rotateX(o.rx); if (o.ry) geo.rotateY(o.ry); if (o.rz) geo.rotateZ(o.rz); if (o.q) geo.applyQuaternion(o.q);
    if (o.post) o.post(geo);
    geo.translate(x, y, z); coloredGeo(geo, color);
    const n = geo.attributes.position.count, si = new Uint16Array(n * 4), sw = new Float32Array(n * 4), b = BI[bone], pb = o.blend ? BI[o.blend] : b;
    for (let i = 0; i < n; i++) {
      let w = 1;
      if (o.blend) { const yy = geo.attributes.position.getY(i), t = o.bottom ? 1 - smooth(o.y0, o.y1, yy) : smooth(o.y0, o.y1, yy); w = 1 - (o.amt ?? 0.5) * t; }
      si[i * 4] = b; si[i * 4 + 1] = pb; sw[i * 4] = w; sw[i * 4 + 1] = 1 - w;
    }
    geo.setAttribute('skinIndex', new THREE.Uint16BufferAttribute(si, 4)); geo.setAttribute('skinWeight', new THREE.Float32BufferAttribute(sw, 4));
    geo.userData.cat = o.cat || (color === this.skin ? 'skin' : color === this.hair ? 'hair' : this.c);
    this.g.push(geo); return this;
  }
  limb(a, b, r, color, bone, o = {}, rs = 10) {
    const d = new V3(b[0] - a[0], b[1] - a[1], b[2] - a[2]), len = d.length();
    return this.add(new THREE.CapsuleGeometry(r, Math.max(0.001, len), 4, rs), color, bone, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2, { ...o, q: new THREE.Quaternion().setFromUnitVectors(new V3(0, 1, 0), d.normalize()) });
  }
  ell(r, color, bone, x, y, z, s, o = {}, ws = 14, hs = 10) { return this.add(new THREE.SphereGeometry(r, ws, hs), color, bone, x, y, z, { ...o, s }); }
  merge(hq) {
    if (!hq) return { geo: mergeGeometries(this.g), cats: null };
    const by = {}; for (const g of this.g) (by[g.userData.cat] ||= []).push(g);
    const cats = CATS.filter(c => by[c]);
    return { geo: mergeGeometries(cats.map(c => mergeGeometries(by[c])), true), cats };
  }
}
/* ---------- textures de détail (normales) et motifs de tissu */
let CHAR_TEX = null;
function charTextures() {
  if (CHAR_TEX) return CHAR_TEX;
  const t0 = performance.now();
  CHAR_TEX = {
    weave: bakeMaps(128, (x, y) => { const a = Math.sin(x / 128 * Math.PI * 2 * 24), b = Math.sin(y / 128 * Math.PI * 2 * 24); return { h: (Math.floor(x / 5.33) + Math.floor(y / 5.33)) % 2 ? a * 0.5 + 0.5 : b * 0.5 + 0.5, r: 0.85 }; }, 1.6),
    denim: bakeMaps(128, (x, y) => ({ h: 0.5 + 0.5 * Math.sin((x + y * 2) / 128 * Math.PI * 2 * 20) + fbm(x, y, 128, 32, 2, 71) * 0.3, r: 0.8 }), 1.8),
    knit: bakeMaps(128, (x, y) => { const cx = x % 8, row = y % 8; const v = 1 - Math.abs((cx - 4) / 4 - (row / 8 - 0.5) * (x % 16 < 8 ? 1 : -1)); return { h: v * 0.8 + fbm(x, y, 128, 32, 2, 72) * 0.2, r: 0.95 }; }, 2.2),
    skin: bakeMaps(256, (x, y) => ({ h: fbm(x, y, 256, 32, 4, 73) * 0.7 - (hash2(x, y, 74) > 0.985 ? 0.6 : 0), r: 0.5 + fbm(x, y, 256, 8, 3, 75) * 0.15 }), 0.9),
    leather: bakeMaps(128, (x, y) => { let best = 9; const T = 10; const cx = Math.floor(x / T), cy = Math.floor(y / T); for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) { const w = n => ((n % 13) + 13) % 13; const px = (cx + i + hash2(w(cx + i), w(cy + j), 76)) * T, py = (cy + j + hash2(w(cx + i), w(cy + j), 77)) * T; best = Math.min(best, Math.hypot(x - px, y - py) / T); } return { h: Math.min(best, 0.6), r: 0.4 }; }, 2),
    strands: bakeMaps(128, (x, y) => ({ h: 0.5 + 0.5 * Math.sin(x / 128 * Math.PI * 2 * 40 + fbm(x, y, 128, 4, 2, 78) * 6), r: 0.45 }), 2),
  };
  const pat = (draw) => { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, 128, 128); draw(g); const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; };
  CHAR_TEX.patterns = {
    carreaux: pat(g => { g.globalAlpha = 0.45; g.fillStyle = '#000'; for (let i = 0; i < 128; i += 32) { g.fillRect(i, 0, 14, 128); g.fillRect(0, i, 128, 14); } g.globalAlpha = 0.6; g.fillStyle = '#fff'; for (let i = 6; i < 128; i += 32) { g.fillRect(i + 18, 0, 2, 128); g.fillRect(0, i + 18, 128, 2); } }),
    rayures: pat(g => { g.fillStyle = 'rgba(0,0,0,.55)'; for (let i = 0; i < 128; i += 16) g.fillRect(i, 0, 6, 128); }),
    fleurs: pat(g => { for (let i = 0; i < 9; i++) { const x = (i % 3) * 43 + 20 + (Math.floor(i / 3) % 2) * 20, y = Math.floor(i / 3) * 43 + 20; g.fillStyle = 'rgba(255,255,255,.95)'; for (let k = 0; k < 5; k++) { const a = k / 5 * 6.28; g.beginPath(); g.ellipse(x + Math.cos(a) * 8, y + Math.sin(a) * 8, 7, 4, a, 0, 7); g.fill(); } g.fillStyle = '#f2c230'; g.beginPath(); g.arc(x, y, 4, 0, 7); g.fill(); g.fillStyle = 'rgba(0,80,40,.5)'; g.beginPath(); g.ellipse(x + 16, y + 12, 10, 4, 0.8, 0, 7); g.fill(); } }),
  };
  console.info(`Personnages : textures générées en ${Math.round(performance.now() - t0)} ms`);
  return CHAR_TEX;
}
const nm = (set, r) => { const n = set.normal.clone(), o = set.orm.clone(); n.needsUpdate = o.needsUpdate = true; n.repeat.set(r[0], r[1]); o.repeat.set(r[0], r[1]); return { normalMap: n, roughnessMap: o }; };
function charMaterials(o) {
  const T = charTextures(), V = { vertexColors: true, envMapIntensity: envLevel };
  const top = new THREE.MeshPhysicalMaterial({ ...V, roughness: 1, sheen: 0.6, sheenRoughness: 0.8, sheenColor: new THREE.Color(0.6, 0.6, 0.6), ...nm(o.top === 'hoodie' || o.top === 'manteau' ? T.knit : T.weave, [10, 6]), normalScale: new THREE.Vector2(0.6, 0.6) });
  if (o.motif && o.motif !== 'uni' && CHAR_TEX.patterns[o.motif]) { top.map = CHAR_TEX.patterns[o.motif].clone(); top.map.needsUpdate = true; top.map.repeat.set(5, 3); }
  return {
    skin: new THREE.MeshPhysicalMaterial({ ...V, roughness: 1, sheen: 0.35, sheenRoughness: 0.55, sheenColor: new THREE.Color(0.85, 0.32, 0.22), clearcoat: 0.06, clearcoatRoughness: 0.5, ...nm(T.skin, [6, 4]), normalScale: new THREE.Vector2(0.25, 0.25) }),
    hair: new THREE.MeshPhysicalMaterial({ ...V, roughness: 1, sheen: 0.5, sheenRoughness: 0.35, sheenColor: new THREE.Color(0.5, 0.45, 0.4), anisotropy: 0.8, ...nm(T.strands, [8, 2]), normalScale: new THREE.Vector2(0.9, 0.9) }),
    top,
    pants: new THREE.MeshPhysicalMaterial({ ...V, roughness: 1, sheen: 0.4, sheenRoughness: 0.8, ...nm(o.pants === 'jean' ? T.denim : T.weave, [6, 8]), normalScale: new THREE.Vector2(0.7, 0.7) }),
    cloth: new THREE.MeshPhysicalMaterial({ ...V, roughness: 1, sheen: 0.5, sheenRoughness: 0.8, ...nm(T.weave, [8, 6]), normalScale: new THREE.Vector2(0.5, 0.5) }),
    knit: new THREE.MeshPhysicalMaterial({ ...V, roughness: 1, sheen: 0.7, sheenRoughness: 0.9, ...nm(T.knit, [10, 8]), normalScale: new THREE.Vector2(1, 1) }),
    shoe: new THREE.MeshPhysicalMaterial({ ...V, roughness: 1, sheen: 0.3, clearcoat: 0.2, clearcoatRoughness: 0.4, ...nm(T.weave, [4, 4]), normalScale: new THREE.Vector2(0.4, 0.4) }),
    rubber: new THREE.MeshStandardMaterial({ ...V, roughness: 0.9 }),
    leather: new THREE.MeshPhysicalMaterial({ ...V, roughness: 1, clearcoat: 0.45, clearcoatRoughness: 0.35, ...nm(T.leather, [6, 6]), normalScale: new THREE.Vector2(0.5, 0.5) }),
    metal: new THREE.MeshPhysicalMaterial({ ...V, metalness: 1, roughness: 0.18, clearcoat: 0.5 }),
    glass: new THREE.MeshPhysicalMaterial({ ...V, metalness: 0.6, roughness: 0.04, clearcoat: 1, clearcoatRoughness: 0.02 }),
    eye: new THREE.MeshPhysicalMaterial({ ...V, roughness: 0.15, clearcoat: 1, clearcoatRoughness: 0.03 }),
  };
}
const EYE_COLORS = ['#4a3220', '#2b6cb0', '#3c7a4a', '#6b4f2a', '#8a8f99', '#1b1b1b'];
const shade = (hex, k) => '#' + new THREE.Color(hex).multiplyScalar(k).getHexString();
function buildCharacter(o, hq = false) {
  const fem = o.body === 'femme', L = skeletonLayout(o), Pt = n => L[n].slice(1);
  const SK = o.skin, TC = o.topColor, PC = o.pantsColor, HC = o.hairColor, EYE = o.eyes || EYE_COLORS[0];
  const SHc = o.shoes, SOLE = o.sole || '#f2f2f2', ACC = o.shoeAccent || '#1c1c1e', HAT = o.hatColor || TC;
  const robe = o.top === 'kandura' || o.top === 'abaya', coat = o.top === 'manteau', balaclava = o.head === 'cagoule';
  const longSleeve = ['chemise', 'costume', 'hoodie', 'kandura', 'abaya', 'manteau'].includes(o.top);
  const shortP = o.pants === 'short';
  const sleeve = o.top === 'debardeur' ? SK : TC, fore = longSleeve ? TC : SK, lowLeg = robe ? TC : shortP ? SK : PC, HAND = o.gloves ? '#121212' : SK;
  const B = new SkinBag(); B.skin = SK; B.hair = HC;
  // ---------- jambes
  for (const s of ['L', 'R']) {
    const hip = Pt('thigh' + s), knee = Pt('shin' + s), ank = Pt('foot' + s), sg = s === 'L' ? 1 : -1;
    B.c = robe ? 'top' : 'pants';
    B.limb(hip, knee, fem ? 0.066 : 0.072, robe ? TC : PC, 'thigh' + s, { blend: 'hips', y0: 0.8, y1: 0.93 });
    B.limb(knee, ank, 0.054, lowLeg, 'shin' + s, { blend: 'thigh' + s, y0: 0.44, y1: 0.55 });
    if (shortP && !robe) { B.add(new THREE.CylinderGeometry(0.079, 0.086, 0.09, 12, 1, true), PC, 'thigh' + s, knee[0] * 0.98, 0.585, 0.008); B.add(new THREE.TorusGeometry(0.084, 0.006, 4, 14), shade(PC, 0.8), 'thigh' + s, knee[0] * 0.98, 0.54, 0.008, { rx: Math.PI / 2 }); }
    if (o.pants === 'jean' && !robe) { B.c = 'pants'; B.add(new THREE.BoxGeometry(0.004, 0.36, 0.004), '#c8a04a', 'thigh' + s, hip[0] + sg * 0.072, 0.72, 0.0); B.add(new THREE.TorusGeometry(0.058, 0.01, 4, 14), shade(PC, 0.85), 'shin' + s, ank[0], 0.135, 0.012, { rx: Math.PI / 2 }); }
    // chaussures
    const st = o.shoeStyle || 'baskets';
    if (st === 'cuir') {
      B.c = 'leather'; B.add(new THREE.CapsuleGeometry(0.048, 0.16, 4, 10), SHc, 'foot' + s, ank[0], 0.05, 0.06, { rx: Math.PI / 2, s: [1.05, 1, 0.75] });
      B.c = 'rubber'; B.add(new THREE.BoxGeometry(0.1, 0.014, 0.27), shade(SHc, 0.6), 'foot' + s, ank[0], 0.007, 0.058);
    } else {
      B.c = 'rubber';
      B.add(new THREE.CapsuleGeometry(0.056, 0.17, 4, 12), SOLE, 'foot' + s, ank[0], 0.024, 0.058, { rx: Math.PI / 2, s: [1.05, 1, 0.38] });
      B.add(new THREE.BoxGeometry(0.104, 0.012, 0.27), shade(SOLE, 0.8), 'foot' + s, ank[0], 0.006, 0.058);
      B.c = 'shoe';
      B.add(new THREE.CapsuleGeometry(0.05, 0.15, 4, 12), SHc, 'foot' + s, ank[0], 0.06, 0.05, { rx: Math.PI / 2, s: [1, 1, 0.82] });
      B.ell(0.046, SOLE, 'foot' + s, ank[0], 0.045, 0.14, [1.05, 0.7, 0.9], { cat: 'rubber' });
      for (const side of [-1, 1]) B.add(new THREE.BoxGeometry(0.004, 0.025, 0.13), ACC, 'foot' + s, ank[0] + side * 0.051, 0.055, 0.04, { rz: 0, rx: -0.35 * side * 0 - 0.3 });
      for (let i = 0; i < 4; i++) B.add(new THREE.BoxGeometry(0.05, 0.006, 0.008), '#f6f6f6', 'foot' + s, ank[0], 0.1 - i * 0.008, 0.06 + i * 0.022, { rx: 0.5 });
      B.add(new THREE.BoxGeometry(0.03, 0.04, 0.012), ACC, 'foot' + s, ank[0], 0.1, -0.035);
      if (st === 'montantes') { B.add(new THREE.CylinderGeometry(0.062, 0.058, 0.11, 12), SHc, 'shin' + s, ank[0], 0.135, 0.01); B.add(new THREE.TorusGeometry(0.06, 0.008, 4, 14), ACC, 'shin' + s, ank[0], 0.19, 0.01, { rx: Math.PI / 2 }); }
    }
  }
  // ---------- bassin, torse
  B.c = robe ? 'top' : 'pants';
  B.ell(0.15, robe ? TC : PC, 'hips', 0, 0.94, 0, [fem ? 1.1 : 1.0, 0.6, 0.72]);
  if (!robe && !coat) { B.add(new THREE.TorusGeometry(0.135, 0.012, 4, 20), o.pants === 'jean' ? '#3a2a1a' : shade(PC, 0.7), 'hips', 0, 1.0, 0, { rx: Math.PI / 2, s: [1.04, 0.74, 1] }); B.add(new THREE.BoxGeometry(0.035, 0.026, 0.01), '#c9ccd1', 'hips', 0, 1.0, 0.102, { cat: 'metal' }); }
  B.c = 'top';
  const tp = fem ? [[0.001, 0], [0.135, 0.02], [0.125, 0.12], [0.15, 0.25], [0.16, 0.36], [0.15, 0.45], [0.07, 0.5], [0.001, 0.5]]
    : [[0.001, 0], [0.145, 0.02], [0.14, 0.12], [0.165, 0.26], [0.19, 0.38], [0.18, 0.46], [0.08, 0.51], [0.001, 0.51]];
  B.add(new THREE.LatheGeometry(tp.map(([x, y]) => new THREE.Vector2(x * o.build ** 0.3, y)), 20), TC, 'chest', 0, 0.99, 0, { s: [1, 1.04, 0.62], blend: 'spine', bottom: true, y0: 1.02, y1: 1.24, amt: 0.85 });
  if (fem) for (const s of [-1, 1]) B.ell(0.055, TC, 'chest', s * 0.068, 1.35, 0.06, [1, 0.9, 0.75]);
  if (o.top === 'debardeur') B.ell(0.09, SK, 'chest', 0, 1.49, 0.03, [1.4, 0.5, 0.6]);
  if (o.top === 'chemise') {
    for (const s of [-1, 1]) B.add(new THREE.BoxGeometry(0.06, 0.05, 0.012), shade(TC, 1.05), 'chest', s * 0.035, 1.505, 0.075, { rz: s * 0.6, rx: -0.4 });
    B.add(new THREE.BoxGeometry(0.014, 0.4, 0.008), shade(TC, 0.95), 'chest', 0, 1.29, 0.121);
    for (let i = 0; i < 5; i++) B.ell(0.005, '#efe9dc', 'chest', 0, 1.46 - i * 0.075, 0.127, [1, 1, 0.5], { cat: 'rubber' }, 6, 4);
    B.add(new THREE.BoxGeometry(0.06, 0.06, 0.006), shade(TC, 0.95), 'chest', 0.07, 1.39, 0.115);
  }
  if (o.top === 'costume') { B.add(new THREE.BoxGeometry(0.1, 0.26, 0.01), '#f4f4f4', 'chest', 0, 1.39, 0.118, { cat: 'cloth' }); B.add(new THREE.BoxGeometry(0.035, 0.24, 0.012), '#8a1020', 'chest', 0, 1.37, 0.124, { cat: 'cloth' }); for (const s of [-1, 1]) B.add(new THREE.BoxGeometry(0.05, 0.26, 0.012), shade(TC, 0.8), 'chest', s * 0.06, 1.38, 0.12, { rz: s * 0.25 }); for (let i = 0; i < 2; i++) B.ell(0.008, '#1b1b1b', 'chest', 0.01, 1.2 - i * 0.07, 0.123, [1, 1, 0.5], { cat: 'rubber' }, 6, 4); }
  if (o.top === 'hoodie') { B.c = 'knit'; B.ell(0.11, TC, 'chest', 0, 1.52, -0.09, [1, 0.8, 0.7]); B.add(new THREE.BoxGeometry(0.2, 0.1, 0.015), shade(TC, 0.9), 'chest', 0, 1.13, 0.1); for (const s of [-1, 1]) B.limb([s * 0.03, 1.5, 0.1], [s * 0.035, 1.38, 0.115], 0.005, '#f2f2f2', 'chest', { cat: 'cloth' }, 6); B.c = 'top'; }
  if (robe) B.add(new THREE.CylinderGeometry(0.17, 0.3, 0.86, 18), TC, 'hips', 0, 0.55, 0, { s: [1, 1, 0.85] });
  if (coat) { B.add(new THREE.CylinderGeometry(0.165, 0.22, 0.46, 16), TC, 'hips', 0, 0.73, 0, { s: [1, 1, 0.8] }); B.add(new THREE.TorusGeometry(0.07, 0.025, 6, 14), TC, 'chest', 0, 1.52, 0.0, { rx: Math.PI / 2 }); for (let i = 0; i < 4; i++) B.ell(0.009, '#1b1b1b', 'chest', 0.035, 1.42 - i * 0.12, 0.124, [1, 1, 0.5], { cat: 'rubber' }, 6, 4); }
  B.add(new THREE.CylinderGeometry(0.056, 0.062, 0.13, 12), balaclava ? HAT : SK, 'neck', 0, 1.575, 0.005, { cat: balaclava ? 'knit' : 'skin' });
  // ---------- bras & mains
  for (const s of ['L', 'R']) {
    const sh = Pt('uArm' + s), el = Pt('fArm' + s), wr = Pt('hand' + s), sg = s === 'L' ? 1 : -1;
    B.c = 'top';
    B.ell(0.055, sleeve, 'uArm' + s, sh[0] - sg * 0.008, sh[1] - 0.01, 0, [1, 0.95, 0.95]);
    B.limb(sh, el, 0.048, sleeve, 'uArm' + s, { blend: 'chest', y0: 1.38, y1: 1.47 });
    B.limb(el, wr, 0.04, fore, 'fArm' + s, { blend: 'uArm' + s, y0: 1.14, y1: 1.24 });
    if (!longSleeve && o.top !== 'debardeur') B.add(new THREE.CylinderGeometry(0.056, 0.054, 0.05, 12, 1, true), shade(TC, 0.95), 'uArm' + s, (sh[0] + el[0]) / 2, 1.3, 0);
    if (longSleeve) B.add(new THREE.CylinderGeometry(0.044, 0.046, 0.04, 12, 1, true), shade(TC, 0.9), 'fArm' + s, wr[0], wr[1] + 0.025, wr[2]);
    // main : paume, doigts, pouce (gants en cuir noir en option)
    B.c = o.gloves ? 'leather' : 'skin';
    B.ell(0.042, HAND, 'hand' + s, wr[0], wr[1] - 0.05, wr[2] + 0.004, [0.75, 1.0, 0.5]);
    for (let f = 0; f < 4; f++) B.limb([wr[0] + sg * (0.012 - f * 0.0) - sg * 0.0, wr[1] - 0.075, wr[2] - 0.015 + f * 0.011], [wr[0] + sg * 0.004, wr[1] - 0.115 + Math.abs(f - 1.5) * 0.006, wr[2] - 0.012 + f * 0.012], 0.0075, HAND, 'fing' + s, {}, 6);
    B.limb([wr[0] + sg * 0.006, wr[1] - 0.03, wr[2] + 0.028], [wr[0] + sg * 0.004, wr[1] - 0.075, wr[2] + 0.042], 0.011, HAND, 'hand' + s, {}, 6);
    if (o.gloves) B.add(new THREE.CylinderGeometry(0.046, 0.044, 0.04, 12, 1, true), '#0d0d0d', 'fArm' + s, wr[0], wr[1] + 0.005, wr[2]);
    if (o.watch && s === 'L') {
      const WS = { or: ['#d6a63c', '#2a1a12', 'leather'], acier: ['#c9ccd1', '#a7adb6', 'metal'], noir: ['#1b1b1b', '#111111', 'leather'] }[o.watchStyle || 'or'];
      B.c = WS[2]; B.add(new THREE.TorusGeometry(0.041, 0.011, 6, 18), WS[1], 'fArm' + s, wr[0], wr[1] + 0.035, wr[2], { rx: Math.PI / 2, s: [1, 1, 1.4] });
      B.c = 'metal'; B.add(new THREE.CylinderGeometry(0.022, 0.022, 0.012, 18), WS[0], 'fArm' + s, wr[0] + 0.043, wr[1] + 0.035, wr[2], { rz: Math.PI / 2 });
      B.c = 'glass'; B.add(new THREE.CylinderGeometry(0.018, 0.018, 0.004, 18), '#0f1a24', 'fArm' + s, wr[0] + 0.0505, wr[1] + 0.035, wr[2], { rz: Math.PI / 2 });
    }
  }
  // ---------- tête & visage
  const hy = 1.735, skD = shade(SK, 0.88), fz = balaclava ? 0.012 : 0;
  B.c = 'skin';
  B.ell(0.112, SK, 'head', 0, hy, 0.004, [0.92, 1.08, 1.0], {}, 22, 16);
  B.ell(0.088, SK, 'head', 0, hy - 0.058, 0.024, [0.96, 0.82, 0.98], {}, 18, 12);
  if (!balaclava) B.ell(0.021, skD, 'head', 0, hy - 0.012, 0.104, [0.82, 1.35, 1.05]);
  for (const s of [-1, 1]) {
    if (!balaclava) { B.ell(0.03, skD, 'head', s * 0.102, hy - 0.004, -0.004, [0.42, 1, 0.72]); B.ell(0.0085, shade(SK, 0.6), 'head', s * 0.011, hy - 0.03, 0.112, [1, 0.6, 0.6], {}, 6, 4); }
    if (balaclava) B.ell(0.03, SK, 'head', s * 0.038, hy + 0.02, 0.112, [1.5, 0.75, 0.5]);
    B.ell(0.019, '#f6f2ea', 'head', s * 0.038, hy + 0.017, 0.1 + fz, [1.1, 0.78, 0.6], { cat: 'eye' });
    B.ell(0.0105, EYE, 'head', s * 0.038, hy + 0.016, 0.109 + fz, [1, 1, 0.45], { cat: 'eye' }, 12, 8);
    B.ell(0.0048, '#0a0a0a', 'head', s * 0.038, hy + 0.016, 0.1135 + fz, [1, 1, 0.4], { cat: 'eye' }, 8, 6);
    B.add(new THREE.SphereGeometry(0.0205, 12, 6, 0, Math.PI * 2, 0, Math.PI * 0.42), shade(SK, 0.92), s > 0 ? 'lidL' : 'lidR', s * 0.038, hy + 0.018, 0.1 + fz, { s: [1.12, 0.8, 0.68], rx: 0.15 });
    B.add(new THREE.BoxGeometry(0.036, 0.003, 0.006), '#1a1410', 'head', s * 0.038, hy + 0.029, 0.112 + fz, { cat: 'hair' });
    B.add(new THREE.BoxGeometry(0.044, 0.01, 0.012), HC, 'head', s * 0.04, hy + 0.045, 0.104 + fz, { rz: s * 0.12, cat: 'hair' });
    if (!balaclava) B.ell(0.026, shade(SK, 0.95), 'head', s * 0.056, hy - 0.03, 0.088, [1, 0.8, 0.6]);
  }
  if (!balaclava) { B.ell(0.02, fem ? '#a8475a' : shade(SK, 0.72), 'head', 0, hy - 0.058, 0.106, [1.45, 0.32, 0.55]); B.ell(0.021, fem ? '#b9505f' : shade(SK, 0.78), 'jaw', 0, hy - 0.068, 0.104, [1.4, 0.42, 0.55]); }
  // ---------- cheveux
  const covered = o.head === 'ghutra' || o.head === 'foulard' || balaclava;
  B.c = 'hair';
  const cap = (scale = 1) => B.add(new THREE.SphereGeometry(0.121 * scale, 20, 12, 0, Math.PI * 2, 0, Math.PI * 0.58), HC, 'head', 0, hy + 0.01, -0.008, { s: [0.97, 1.04, 1.06], rx: -0.6 });
  if (!covered) switch (o.hair) {
    case 'court': cap(); break;
    case 'long': cap(); B.limb([0, hy - 0.02, -0.07], [0, hy - 0.26, -0.085], 0.085, HC, 'head', { s: [1.3, 1, 0.55] }); for (const s of [-1, 1]) B.limb([s * 0.095, hy, -0.01], [s * 0.1, hy - 0.2, -0.03], 0.028, HC, 'head'); break;
    case 'queue': cap(); B.limb([0, hy + 0.01, -0.12], [0, hy - 0.2, -0.17], 0.034, HC, 'head'); B.add(new THREE.TorusGeometry(0.03, 0.007, 4, 10), '#1b1b1b', 'head', 0, hy - 0.0, -0.13, { rx: 1.2, cat: 'rubber' }); break;
    case 'chignon': cap(); B.ell(0.055, HC, 'head', 0, hy + 0.06, -0.11, [1, 1, 1]); break;
    case 'afro': B.ell(0.15, HC, 'head', 0, hy + 0.07, -0.06, [1.05, 0.95, 0.9], {}, 18, 12); break;
    case 'crete': B.ell(0.12, HC, 'head', 0, hy + 0.07, -0.01, [0.22, 0.55, 1.1]); break;
  }
  if ((!fem || o.beard !== 'aucune') && !balaclava) {
    const shell = () => B.add(new THREE.SphereGeometry(0.098, 18, 10, 0, Math.PI * 2, Math.PI * 0.55, Math.PI * 0.42), HC, 'head', 0, hy - 0.03, 0.02, { s: [1.0, 1.05, 1.06] });
    const must = () => B.limb([-0.026, hy - 0.04, 0.112], [0.026, hy - 0.04, 0.112], 0.009, HC, 'head', {}, 6);
    switch (o.beard) {
      case 'courte': shell(); must(); break;
      case 'longue': shell(); must(); B.limb([0, hy - 0.1, 0.07], [0, hy - 0.2, 0.06], 0.045, HC, 'head', { s: [1.2, 1, 0.7] }); break;
      case 'moustache': must(); break;
      case 'bouc': must(); B.ell(0.03, HC, 'head', 0, hy - 0.1, 0.085, [1, 1.2, 0.8]); break;
    }
  }
  // ---------- couvre-chefs
  const capVisor = (back) => {
    B.c = 'cloth';
    B.add(new THREE.SphereGeometry(0.127, 6, 8, 0, Math.PI * 2, 0, Math.PI * 0.5), HAT, 'head', 0, hy + 0.025, -0.004, { s: [1, 0.88, 1.06] });
    B.ell(0.011, HAT, 'head', 0, hy + 0.137, -0.004, [1, 0.6, 1], {}, 8, 4);
    B.add(new THREE.TorusGeometry(0.124, 0.006, 4, 24), shade(HAT, 0.85), 'head', 0, hy + 0.026, -0.004, { rx: Math.PI / 2, s: [1, 1.06, 1] });
    B.add(new THREE.CylinderGeometry(0.12, 0.12, 0.01, 18, 1, false, -Math.PI / 2, Math.PI), shade(HAT, 0.9), 'head', 0, hy + 0.03, back ? -0.07 : 0.07, { rx: back ? -0.12 : 0.12, ry: back ? Math.PI : 0, s: [0.95, 1, 1.05] });
    if (back) B.add(new THREE.BoxGeometry(0.05, 0.03, 0.01), '#e8e8e8', 'head', 0, hy + 0.05, 0.126, { cat: 'rubber' });
    else B.add(new THREE.BoxGeometry(0.045, 0.025, 0.01), '#e8e8e8', 'head', 0, hy + 0.08, 0.116, { rx: -0.3, cat: 'rubber' });
  };
  switch (o.head) {
    case 'ghutra': case 'foulard': {
      const c = o.head === 'ghutra' ? '#f6f6f2' : TC; B.c = 'cloth';
      B.add(new THREE.SphereGeometry(0.133, 20, 12, 0, Math.PI * 2, 0, Math.PI * 0.6), c, 'head', 0, hy + 0.012, -0.008, { s: [1, 1.05, 1.06], rx: -0.55 });
      B.add(new THREE.CylinderGeometry(0.128, o.head === 'ghutra' ? 0.2 : 0.17, 0.34, 18, 1, true, Math.PI * 0.62, Math.PI * 0.76), c, 'head', 0, hy - 0.13, -0.005, { s: [1, 1, 0.95] });
      if (o.head === 'ghutra') { B.c = 'knit'; B.add(new THREE.TorusGeometry(0.112, 0.014, 8, 24), '#151515', 'head', 0, hy + 0.075, -0.01, { rx: Math.PI / 2 - 0.15 }); B.add(new THREE.TorusGeometry(0.105, 0.012, 8, 24), '#151515', 'head', 0, hy + 0.06, -0.012, { rx: Math.PI / 2 - 0.15 }); }
      else B.add(new THREE.CylinderGeometry(0.075, 0.1, 0.07, 16, 1, true), c, 'neck', 0, 1.585, 0.0);
      break;
    }
    case 'casquette': capVisor(false); break;
    case 'casquette_inv': capVisor(true); break;
    case 'cagoule':
      B.c = 'knit';
      B.ell(0.119, HAT, 'head', 0, hy + 0.004, 0.003, [0.95, 1.1, 1.02], {}, 22, 16);
      B.ell(0.093, HAT, 'head', 0, hy - 0.058, 0.026, [0.98, 0.84, 1.0], {}, 18, 12);
      B.add(new THREE.TorusGeometry(0.03, 0.006, 6, 16), shade(HAT, 1.3), 'head', -0.038, hy + 0.019, 0.117, { s: [1.5, 0.75, 1] }); B.add(new THREE.TorusGeometry(0.03, 0.006, 6, 16), shade(HAT, 1.3), 'head', 0.038, hy + 0.019, 0.117, { s: [1.5, 0.75, 1] });
      break;
    case 'chapeau': B.c = 'cloth'; B.add(new THREE.CylinderGeometry(0.2, 0.2, 0.012, 24), '#2a2a2a', 'head', 0, hy + 0.07, 0); B.add(new THREE.CylinderGeometry(0.105, 0.115, 0.11, 20), '#2a2a2a', 'head', 0, hy + 0.13, 0); B.add(new THREE.CylinderGeometry(0.118, 0.118, 0.025, 20), '#8a1c1c', 'head', 0, hy + 0.09, 0); break;
    case 'bonnet': B.c = 'knit'; B.add(new THREE.SphereGeometry(0.128, 18, 10, 0, Math.PI * 2, 0, Math.PI * 0.55), HAT, 'head', 0, hy + 0.02, -0.004, { rx: -0.15 }); B.add(new THREE.TorusGeometry(0.115, 0.018, 8, 24), shade(HAT, 1.2), 'head', 0, hy + 0.0, -0.01, { rx: Math.PI / 2 - 0.15 }); B.ell(0.035, '#f2f2f2', 'head', 0, hy + 0.15, -0.02, [1, 1, 1]); break;
  }
  // ---------- accessoires
  if (o.glasses) {
    for (const s of [-1, 1]) {
      B.add(new THREE.CylinderGeometry(0.024, 0.024, 0.004, 20), '#14181c', 'head', s * 0.04, hy + 0.017, 0.118 + fz, { rx: Math.PI / 2, cat: 'glass' });
      B.add(new THREE.TorusGeometry(0.025, 0.003, 6, 20), '#c9a24a', 'head', s * 0.04, hy + 0.017, 0.118 + fz, { cat: 'metal' });
      B.add(new THREE.BoxGeometry(0.003, 0.004, 0.11), '#c9a24a', 'head', s * 0.066, hy + 0.024, 0.065, { cat: 'metal' });
    }
    B.add(new THREE.TorusGeometry(0.009, 0.0025, 4, 10, Math.PI), '#c9a24a', 'head', 0, hy + 0.021, 0.12 + fz, { cat: 'metal' });
  }
  if (o.chain) { for (let i = 0; i < 26; i++) { const a = i / 26 * Math.PI * 2; B.add(new THREE.TorusGeometry(0.008, 0.0028, 4, 8), '#e8b830', 'chest', Math.sin(a) * 0.072, 1.5 - (Math.cos(a) > 0 ? Math.cos(a) * 0.04 : 0), Math.cos(a) * 0.055 + 0.02, { ry: a + (i % 2) * Math.PI / 2, cat: 'metal' }); } B.ell(0.016, '#e8b830', 'chest', 0, 1.44, 0.085, [1, 1.2, 0.4], { cat: 'metal' }); }
  // ---------- squelette & assemblage
  const bones = {}; for (const n of BONES) { const b = new THREE.Bone(); b.name = n; bones[n] = b; }
  for (const n of BONES) { const [par, x, y, z] = L[n]; if (par) { const pp = L[par]; bones[n].position.set(x - pp[1], y - pp[2], z - pp[3]); bones[par].add(bones[n]); } else bones[n].position.set(x, y, z); }
  const { geo, cats } = B.merge(hq);
  let mat = CHAR_MAT; if (hq) { const M = charMaterials(o); mat = cats.map(c => M[c]); for (const m of mat) ENV_MATS.add(m); }
  const mesh = new THREE.SkinnedMesh(geo, mat); mesh.castShadow = true; mesh.receiveShadow = true;
  const root = new THREE.Group(); root.add(bones.root); root.add(mesh); root.updateMatrixWorld(true);
  mesh.bind(new THREE.Skeleton(BONES.map(n => bones[n])));
  const H = (fem ? 0.95 : 1) * o.height, W = o.build * (fem ? 0.95 : 1);
  root.scale.set(W, H, W); root.rotation.order = 'YXZ';
  root.userData = {
    H, mesh, seed: Math.random() * 10, baseHipY: bones.hips.position.y, hq,
    legL: bones.thighL, legR: bones.thighR, armL: bones.uArmL, armR: bones.uArmR, shinL: bones.shinL, shinR: bones.shinR, foreL: bones.fArmL, foreR: bones.fArmR,
    footL: bones.footL, footR: bones.footR, handL: bones.handL, handR: bones.handR, hips: bones.hips, spine: bones.spine, chest: bones.chest, neck: bones.neck, head: bones.head,
    jaw: bones.jaw, lidL: bones.lidL, lidR: bones.lidR, fingL: bones.fingL, fingR: bones.fingR,
  };
  return root;
}
function disposeChar(m) { m.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.isSkinnedMesh) { o.skeleton.dispose(); if (o.userData.ownMats !== false && Array.isArray(o.material)) for (const mm of o.material) { ENV_MATS.delete(mm); mm.dispose(); } } }); }

/* ---------- Animation procédurale (marche, course, respiration, réactions physiques) */
function poseFace(u, mode) {
  const t = performance.now() / 1000 + u.seed;
  const blink = (t * 0.29) % 1 < 0.035;
  u.lidL.rotation.x = u.lidR.rotation.x = mode === 'rag' || blink ? 1.05 : 0;
  const grip = mode === 'sit' ? 1.25 : mode === 'handsup' || mode === 'dance' ? 0.05 : mode === 'flail' ? 0.9 : 0.35;
  u.fingL.rotation.z = -grip; u.fingR.rotation.z = grip;
  u.jaw.rotation.x = mode === 'flail' ? 0.25 : 0;
}
const POSE_BONES = ['legL', 'legR', 'armL', 'armR', 'shinL', 'shinR', 'foreL', 'foreR', 'footL', 'footR', 'handL', 'handR', 'hips', 'spine', 'chest', 'neck', 'head', 'jaw', 'lidL', 'lidR', 'fingL', 'fingR'];
function pose(ch, mode, phase, amt = 1, ex = 0) {
  const u = ch.userData; if (u.skip) return;
  for (const k of POSE_BONES) u[k].rotation.set(0, 0, 0);
  poseFace(u, mode);
  u.hips.position.y = u.baseHipY; u.armL.rotation.z = 0.09; u.armR.rotation.z = -0.09;
  const t = performance.now() / 1000 + u.seed, s = Math.sin(phase), c = Math.cos(phase);
  switch (mode) {
    case 'walk': {
      if (amt < 0.05) { // repos : respiration, transfert de poids, regard
        const br = Math.sin(t * 1.7) * 0.5 + 0.5;
        u.chest.rotation.x = -0.025 * br; u.spine.rotation.z = Math.sin(t * 0.35) * 0.025; u.hips.rotation.z = -Math.sin(t * 0.35) * 0.035;
        u.armL.rotation.z = 0.1 + 0.015 * br; u.armR.rotation.z = -0.1 - 0.015 * br; u.foreL.rotation.x = u.foreR.rotation.x = -0.14;
        u.head.rotation.y = Math.sin(t * 0.43) * 0.35; u.head.rotation.x = Math.sin(t * 0.31) * 0.06;
        u.legL.rotation.z = 0.03; u.legR.rotation.z = -0.03; u.shinL.rotation.x = 0.04 + Math.max(0, Math.sin(t * 0.35)) * 0.08;
        break;
      }
      const a = Math.min(amt, 1.5), run = clamp((amt - 1.05) / 0.35, 0, 1);
      u.legL.rotation.x = -s * (0.5 + run * 0.25) * a - run * 0.1; u.legR.rotation.x = s * (0.5 + run * 0.25) * a - run * 0.1;
      u.shinL.rotation.x = (0.12 + Math.max(0, Math.sin(phase + 1.3)) * (0.75 + run * 0.9)) * Math.min(a, 1.2);
      u.shinR.rotation.x = (0.12 + Math.max(0, Math.sin(phase + 1.3 + Math.PI)) * (0.75 + run * 0.9)) * Math.min(a, 1.2);
      u.footL.rotation.x = -u.legL.rotation.x * 0.3 - u.shinL.rotation.x * 0.25; u.footR.rotation.x = -u.legR.rotation.x * 0.3 - u.shinR.rotation.x * 0.25;
      u.armL.rotation.x = s * 0.45 * a * (1 + run * 0.5); u.armR.rotation.x = -s * 0.45 * a * (1 + run * 0.5);
      u.foreL.rotation.x = -(0.22 + 0.2 * a + run * 1.0) - Math.max(0, -s) * 0.25 * a; u.foreR.rotation.x = -(0.22 + 0.2 * a + run * 1.0) - Math.max(0, s) * 0.25 * a;
      u.chest.rotation.y = s * 0.1 * a; u.hips.rotation.y = -s * 0.09 * a; u.hips.rotation.z = c * 0.035 * a;
      u.spine.rotation.x = 0.03 + run * 0.2; u.head.rotation.x = -run * 0.12;
      u.hips.position.y = u.baseHipY - (0.012 + Math.abs(c) * 0.03 + run * 0.035) * Math.min(a, 1.2);
      break;
    }
    case 'sit': u.legL.rotation.x = u.legR.rotation.x = -1.5; u.shinL.rotation.x = u.shinR.rotation.x = 1.45; u.legL.rotation.z = 0.12; u.legR.rotation.z = -0.12;
      u.armL.rotation.x = u.armR.rotation.x = -0.75; u.foreL.rotation.x = u.foreR.rotation.x = -0.75; u.spine.rotation.x = -0.05; break;
    case 'swim': u.armL.rotation.x = -phase; u.armR.rotation.x = -phase - Math.PI; u.foreL.rotation.x = u.foreR.rotation.x = -0.3;
      u.legL.rotation.x = Math.sin(phase * 2) * 0.35; u.legR.rotation.x = -u.legL.rotation.x; u.shinL.rotation.x = u.shinR.rotation.x = 0.25; u.head.rotation.x = -0.9; break;
    case 'fall': u.armL.rotation.z = 1.25 + Math.sin(phase * 3) * 0.25; u.armR.rotation.z = -1.25 - Math.sin(phase * 3) * 0.25; u.foreL.rotation.x = u.foreR.rotation.x = -0.4;
      u.legL.rotation.x = Math.sin(phase * 4) * 0.5 - 0.2; u.legR.rotation.x = -Math.sin(phase * 4) * 0.5 - 0.2; u.shinL.rotation.x = u.shinR.rotation.x = 0.7; break;
    case 'para': u.armL.rotation.x = u.armR.rotation.x = -2.75; u.armL.rotation.z = 0.25; u.armR.rotation.z = -0.25; u.foreL.rotation.x = u.foreR.rotation.x = -0.35;
      u.legL.rotation.x = 0.1 + Math.sin(t * 2) * 0.1; u.legR.rotation.x = -0.05 - Math.sin(t * 2) * 0.1; u.shinL.rotation.x = u.shinR.rotation.x = 0.25; break;
    case 'jet': u.legL.rotation.x = 0.15; u.legR.rotation.x = -0.05; u.shinL.rotation.x = 0.45; u.shinR.rotation.x = 0.3; u.armL.rotation.z = 0.4; u.armR.rotation.z = -0.4; u.foreL.rotation.x = u.foreR.rotation.x = -0.3; break;
    case 'flail': { // en l'air après un choc : moulinets
      const w = t * 13; u.armL.rotation.x = Math.sin(w) * 1.6; u.armR.rotation.x = Math.cos(w) * 1.6; u.armL.rotation.z = 0.9; u.armR.rotation.z = -0.9;
      u.foreL.rotation.x = u.foreR.rotation.x = -0.6; u.legL.rotation.x = Math.sin(w * 0.8) * 0.9; u.legR.rotation.x = -Math.sin(w * 0.8) * 0.9; u.shinL.rotation.x = u.shinR.rotation.x = 0.9;
      u.spine.rotation.x = -0.3; u.head.rotation.x = -0.3; break; }
    case 'protect': // juste avant l'impact : les bras se tendent pour amortir
      u.armL.rotation.x = u.armR.rotation.x = -1.35; u.armL.rotation.z = 0.35; u.armR.rotation.z = -0.35; u.foreL.rotation.x = u.foreR.rotation.x = -0.25;
      u.legL.rotation.x = -0.5; u.legR.rotation.x = -0.2; u.shinL.rotation.x = 0.9; u.shinR.rotation.x = 0.5; u.head.rotation.x = 0.4; u.spine.rotation.x = 0.25; break;
    case 'rag': { // au sol : pose désarticulée propre à chaque passant
      const k = (u.seed % 1);
      u.armL.rotation.z = 1.0 + k * 0.9; u.armR.rotation.z = -0.6 - (1 - k) * 1.1; u.armL.rotation.x = -0.4 + k; u.foreL.rotation.x = -0.3 - k * 0.8; u.foreR.rotation.x = -0.9 * (1 - k);
      u.legL.rotation.x = -0.6 * k; u.shinL.rotation.x = 1.2 * k; u.legR.rotation.z = -0.25 - 0.2 * k; u.legL.rotation.z = 0.2;
      u.head.rotation.y = (k - 0.5) * 1.2; u.head.rotation.x = -0.2; u.spine.rotation.z = (k - 0.5) * 0.3;
      u.chest.rotation.x = -0.03 * (Math.sin(t * 2.2) * 0.5 + 0.5); break; }
    case 'getup': { // ex : progression 0 → 1
      const k = ex;
      u.legL.rotation.x = u.legR.rotation.x = -1.5 * (1 - k); u.shinL.rotation.x = u.shinR.rotation.x = 2.0 * (1 - k) * Math.min(1, k * 3 + 0.3);
      u.armL.rotation.x = u.armR.rotation.x = 0.5 * (1 - k); u.foreL.rotation.x = u.foreR.rotation.x = -0.6 * (1 - k); u.spine.rotation.x = 0.6 * (1 - k) * k * 2;
      u.hips.position.y = u.baseHipY - 0.35 * (1 - k) * Math.min(1, k * 3); break; }
    case 'stagger': { // déséquilibre : le corps encaisse, recule et rattrape son équilibre
      const w = t * 9;
      u.spine.rotation.x = -0.35 * ex; u.chest.rotation.x = -0.15 * ex; u.head.rotation.x = -0.25 * ex;
      u.armL.rotation.z = 0.9 + Math.sin(w) * 0.5; u.armR.rotation.z = -0.9 - Math.cos(w) * 0.5; u.armL.rotation.x = Math.sin(w * 1.3) * 0.6; u.armR.rotation.x = Math.cos(w * 1.3) * 0.6;
      u.foreL.rotation.x = u.foreR.rotation.x = -0.5;
      u.legL.rotation.x = s * 0.7; u.legR.rotation.x = -s * 0.7; u.shinL.rotation.x = 0.4 + Math.max(0, s) * 0.6; u.shinR.rotation.x = 0.4 + Math.max(0, -s) * 0.6;
      u.hips.position.y = u.baseHipY - 0.06; break; }
    case 'phone': pose(ch, 'walk', 0, 0); u.jaw.rotation.x = Math.abs(Math.sin(t * 9)) * 0.14; u.armR.rotation.x = -0.25; u.armR.rotation.z = -0.35; u.foreR.rotation.x = -2.35; u.foreR.rotation.y = 0.3; u.head.rotation.z = -0.12; u.head.rotation.y = Math.sin(t * 0.6) * 0.2; break;
    case 'handsup': u.armL.rotation.x = u.armR.rotation.x = -2.9; u.armL.rotation.z = 0.5; u.armR.rotation.z = -0.5; u.foreL.rotation.x = u.foreR.rotation.x = -0.5;
      u.spine.rotation.x = -0.08; u.head.rotation.x = Math.sin(t * 7) * 0.04; u.legL.rotation.z = 0.06; u.legR.rotation.z = -0.06; break;
    case 'dance': u.armL.rotation.z = 2.5 + Math.sin(phase * 2) * 0.4; u.armR.rotation.z = -2.5 + Math.sin(phase * 2) * 0.4; u.foreL.rotation.x = u.foreR.rotation.x = -0.6;
      u.legL.rotation.x = -Math.max(0, Math.sin(phase * 2)) * 0.7; u.legR.rotation.x = -Math.max(0, -Math.sin(phase * 2)) * 0.7; u.shinL.rotation.x = -u.legL.rotation.x * 1.4; u.shinR.rotation.x = -u.legR.rotation.x * 1.4;
      u.hips.rotation.y = Math.sin(phase) * 0.4; u.chest.rotation.y = -Math.sin(phase) * 0.3; u.hips.position.y = u.baseHipY - Math.abs(Math.sin(phase * 2)) * 0.06; u.head.rotation.z = Math.sin(phase * 2) * 0.15; break;
  }
}
