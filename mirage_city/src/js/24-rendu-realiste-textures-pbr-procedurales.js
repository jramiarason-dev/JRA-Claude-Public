/* =====================================================================
   RENDU RÉALISTE : textures PBR procédurales, peinture vernie, pluie,
   chaussée mouillée, reflets d'objectif, occlusion ambiante, étalonnage
   ===================================================================== */
function hash2(x, y, s) { let h = (x * 374761393 + y * 668265263 + s * 1442695041) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967295; }
function vnoise(x, y, g, s) {
  const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi, u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  const w = a => ((a % g) + g) % g;
  const a = hash2(w(xi), w(yi), s), b = hash2(w(xi + 1), w(yi), s), c = hash2(w(xi), w(yi + 1), s), d = hash2(w(xi + 1), w(yi + 1), s);
  return lerp(lerp(a, b, u), lerp(c, d, u), v);
}
function fbm(px, py, N, base, oct, s) { let v = 0, amp = 0.5, g = base; for (let o = 0; o < oct; o++) { v += amp * vnoise(px / N * g, py / N * g, g, s + o * 17); g *= 2; amp *= 0.5; } return v; }
/* Cuit une carte de normales + une carte ORM (G = rugosité, B = métal) à partir d'une fonction de relief */
function bakeMaps(N, fn, strength) {
  const H = new Float32Array(N * N), Rg = new Float32Array(N * N), Mt = new Float32Array(N * N);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const o = fn(x, y), i = y * N + x; H[i] = o.h; Rg[i] = o.r; Mt[i] = o.m || 0; }
  const mk = () => { const c = document.createElement('canvas'); c.width = c.height = N; const g = c.getContext('2d'); return [c, g, g.createImageData(N, N)]; };
  const [nc, ng, ni] = mk(), [oc, og, oi] = mk();
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const i = y * N + x, xl = y * N + (x + N - 1) % N, xr = y * N + (x + 1) % N, yu = ((y + N - 1) % N) * N + x, yd = ((y + 1) % N) * N + x;
    let nx = -(H[xr] - H[xl]) * strength, ny = (H[yd] - H[yu]) * strength, nz = 1; const l = Math.hypot(nx, ny, nz); nx /= l; ny /= l; nz /= l;
    const o = i * 4;
    ni.data[o] = (nx * 0.5 + 0.5) * 255; ni.data[o + 1] = (ny * 0.5 + 0.5) * 255; ni.data[o + 2] = (nz * 0.5 + 0.5) * 255; ni.data[o + 3] = 255;
    oi.data[o] = 255; oi.data[o + 1] = clamp(Rg[i], 0.02, 1) * 255; oi.data[o + 2] = clamp(Mt[i], 0, 1) * 255; oi.data[o + 3] = 255;
  }
  ng.putImageData(ni, 0, 0); og.putImageData(oi, 0, 0);
  const tex = c => { const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 8; return t; };
  return { normal: tex(nc), orm: tex(oc) };
}
const inRect = (x, y, rx, ry, rw, rh) => x >= rx && x < rx + rw && y >= ry && y < ry + rh;
const edge = (x, y, rx, ry, rw, rh) => Math.min(x - rx, rx + rw - 1 - x, y - ry, ry + rh - 1 - y);
let PBR = null;
function bakeAllPBR() {
  const t0 = performance.now();
  PBR = {
    asphalt: bakeMaps(256, (x, y) => { const n = fbm(x, y, 256, 8, 4, 1), a = hash2(x, y, 7) > 0.9 ? hash2(x, y, 9) * 0.8 : 0, p = fbm(x, y, 256, 3, 2, 5); return { h: n * 0.6 + a, r: 0.72 + p * 0.28 - a * 0.25 }; }, 2.2),
    paving: bakeMaps(256, (x, y) => { const T = 64, gx = x % T, gy = y % T, grout = Math.min(gx, gy) < 3; const tile = hash2(Math.floor(x / T), Math.floor(y / T), 3); return { h: grout ? 0 : 0.7 + tile * 0.15 + fbm(x, y, 256, 16, 2, 4) * 0.12 + (gx / T - 0.5) * tile * 0.1, r: grout ? 0.97 : 0.74 + tile * 0.15 }; }, 3),
    cobble: bakeMaps(256, (x, y) => { const T = 32, cx = Math.floor(x / T), cy = Math.floor(y / T); let best = 9; for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) { const px = (cx + i + hash2((cx + i + 8) % 8, (cy + j + 8) % 8, 11) * 0.5 + 0.25) * T, py = (cy + j + hash2((cx + i + 8) % 8, (cy + j + 8) % 8, 12) * 0.5 + 0.25) * T; best = Math.min(best, Math.hypot(x - px, y - py) / (T * 0.55)); } const h = Math.sqrt(Math.max(0, 1 - best * best)); return { h: h * 0.9 + fbm(x, y, 256, 32, 2, 6) * 0.1, r: h > 0.05 ? 0.6 + fbm(x, y, 256, 8, 2, 2) * 0.25 : 0.95 }; }, 3.5),
    grass: bakeMaps(128, (x, y) => ({ h: fbm(x, y, 128, 32, 3, 21), r: 0.9 }), 3),
    sand: bakeMaps(256, (x, y) => { const w = fbm(x, y, 256, 4, 3, 31); return { h: 0.5 + 0.5 * Math.sin((y + w * 60) / 256 * Math.PI * 2 * 14), r: 0.96 }; }, 1.6),
    roof: bakeMaps(128, (x, y) => { const row = Math.floor(y / 16), off = row % 2 ? 8 : 0, gx = (x + off) % 16; return { h: ((y % 16) / 16) * 0.8 + (gx < 1 ? -0.3 : 0) + fbm(x, y, 128, 16, 2, 41) * 0.15, r: 0.8 }; }, 2.5),
    facades: [0, 1, 2].map(s => bakeMaps(256, (X, Y) => {
      const x = X / 2, y = Y / 2; let win = null;
      for (let i = 0; i < 4 && !win; i++) for (let j = 0; j < 4 && !win; j++) {
        let r = [i * 32 + 4, j * 32 + 5, 24, 20]; if (s === 1) r = [i * 32 + 3, j * 32 + 1, 26, 30]; if (s === 2) r = [i * 32, j * 32 + 8, 32, 18];
        if (inRect(x, y, ...r)) win = r;
      }
      const n = fbm(X, Y, 256, 16, 2, 50 + s);
      if (win) { const e = edge(x, y, ...win); return { h: 0.15 + Math.min(e, 1.5) * 0.08, r: 0.06 + n * 0.06, m: 0.55 }; }
      return { h: 0.9 + n * 0.08, r: 0.45 + n * 0.25, m: 0.15 };
    }, 4)),
    gva: bakeMaps(256, (X, Y) => {
      const x = X / 2, y = Y / 2;
      for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
        const wx = i * 32 + 10, wy = j * 32 + 6;
        if (inRect(x, y, wx, wy, 12, 22)) return { h: 0.1 + (Math.abs(x - wx - 6) < 1 ? 0.25 : 0), r: 0.08, m: 0.5 };
        if (inRect(x, y, wx - 6, wy, 5, 22) || inRect(x, y, wx + 13, wy, 5, 22)) return { h: 0.75 + 0.15 * Math.sin(y * 2.4), r: 0.6 };
        if (inRect(x, y, wx - 2, wy + 23, 16, 3)) return { h: 1, r: 0.7 };
      }
      const course = (y % 8) < 0.7 || ((x + (Math.floor(y / 8) % 2) * 9) % 18) < 0.7;
      return { h: course ? 0.45 : 0.7 + fbm(X, Y, 256, 32, 3, 61) * 0.18, r: 0.88 };
    }, 3.2),
  };
  console.info(`PBR : textures générées en ${Math.round(performance.now() - t0)} ms`);
}
function withRepeat(t, rx, ry) { const c = t.clone(); c.needsUpdate = true; c.repeat.set(rx, ry); return c; }
function setPBR(m, set, rx, ry, normalScale = 1) {
  m.normalMap = withRepeat(set.normal, rx, ry); m.normalScale = new THREE.Vector2(normalScale, normalScale);
  m.roughnessMap = withRepeat(set.orm, rx, ry); m.roughness = 1;
  m.needsUpdate = true;
}
const WET = [];
function applyPBR() {
  bakeAllPBR();
  const done = new Set();
  scene.traverse(o => {
    const m = o.material; if (!m || !m.isMeshStandardMaterial || done.has(m)) return;
    const tag = m.userData.pbr; if (!tag) return; done.add(m);
    const p = o.geometry.parameters || {}, W = p.width || 88, H = p.height || 88;
    if (tag === 'road') { setPBR(m, PBR.asphalt, W / 7, H / 7, 0.8); WET.push(m); }
    else if (tag === 'asphalt') { setPBR(m, PBR.asphalt, W / 7, H / 7, 0.8); WET.push(m); }
    else if (tag === 'paving') { setPBR(m, PBR.paving, W / 4, H / 4, 0.7); WET.push(m); }
    else if (tag === 'cobble') { setPBR(m, PBR.cobble, W / 1.6, H / 1.6, 0.55); WET.push(m); }
    else if (tag === 'grass') setPBR(m, PBR.grass, W / 3, H / 3, 0.8);
    else if (tag === 'sand') setPBR(m, PBR.sand, W / 9, H / 9, 0.7);
  });
  for (const w of WET) w.userData.baseColor = w.color.clone();
  // façades : mêmes coordonnées de texture que la couleur (une tuile = 15 m x 13 m)
  const fac = m => { for (let s = 0; s < 3; s++) if (m.map === FACADES[s].map) return PBR.facades[s]; return m.map === GVA_FAC.map ? PBR.gva : null; };
  for (const m of BMATS) {
    const set = fac(m); if (!set) continue;
    m.normalMap = set.normal; m.normalScale = new THREE.Vector2(1, 1); m.roughnessMap = set.orm; m.metalnessMap = set.orm; m.roughness = 1; m.metalness = set === PBR.gva ? 0.6 : 1; m.needsUpdate = true;
  }
  const roofMat = ROOFS_MESH && ROOFS_MESH.material; if (roofMat) { roofMat.normalMap = withRepeat(PBR.roof.normal, 6, 6); roofMat.roughnessMap = withRepeat(PBR.roof.orm, 6, 6); roofMat.needsUpdate = true; }
}
let ROOFS_MESH = null;

/* ---------- peinture automobile vernie (vernis + flocons métalliques) */
function carPaint(type) {
  return new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: type === 'tractor' ? 0.6 : 0.34, metalness: type === 'hyper' ? 0.85 : 0.5, clearcoat: type === 'tractor' ? 0.2 : 1, clearcoatRoughness: 0.05, envMapIntensity: envLevel });
}

/* ---------- pluie, flaques et chaussée mouillée */
const RAIN_N = isTouch ? 700 : 1800;
const rainMesh = new THREE.InstancedMesh(new THREE.BoxGeometry(0.025, 0.9, 0.025), new THREE.MeshBasicMaterial({ color: 0xb8c6d8, transparent: true, opacity: 0.32, depthWrite: false }), RAIN_N);
rainMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage); rainMesh.frustumCulled = false; rainMesh.visible = false; scene.add(rainMesh);
const rainP = new Float32Array(RAIN_N * 3); for (let i = 0; i < RAIN_N; i++) { rainP[i * 3] = rand(-35, 35); rainP[i * 3 + 1] = rand(0, 30); rainP[i * 3 + 2] = rand(-35, 35); }
const puddleMat = new THREE.MeshStandardMaterial({ color: 0x1a1c20, roughness: 0.03, metalness: 0.95, transparent: true, opacity: 0, depthWrite: false });
let puddles = null;
function buildPuddles() {
  const g = new THREE.CircleGeometry(1, 20); g.rotateX(-Math.PI / 2);
  const list = [];
  for (let i = 0; i < 260; i++) { const onX = Math.random() < 0.5, line = onX ? pick(ROADS_X) : pick(ROADS_Z), off = rand(-11, 11), along = onX ? rand(-540, 900) : rand(-300, 540); list.push(onX ? { x: line + off, z: along } : { x: along, z: line + off }); }
  puddles = new THREE.InstancedMesh(g, puddleMat, list.length); const d = new THREE.Object3D();
  list.forEach((p, i) => { d.position.set(p.x, 0.075, p.z); d.scale.set(rand(1, 3.2), 1, rand(0.8, 2.4)); d.rotation.y = rand(0, 3); d.updateMatrix(); puddles.setMatrixAt(i, d.matrix); });
  puddles.renderOrder = 1; scene.add(puddles); ENV_MATS.add(puddleMat);
}
let lightningT = 12;
function updateWeatherFX(dt) {
  const target = S.weather === 'pluie' ? 1 : 0;
  S.wet = clamp(S.wet + (target - S.wet) * dt * (target ? 0.35 : 0.04), 0, 1);
  for (const m of WET) { m.roughness = lerp(1, 0.22, S.wet); m.color.copy(m.userData.baseColor).multiplyScalar(lerp(1, 0.58, S.wet)); }
  puddleMat.opacity = S.wet * 0.9; POOL_MAT.opacity *= 1 + S.wet * 1.2;
  const raining = S.weather === 'pluie';
  rainMesh.visible = raining && S.mode !== 'creator' && !P.inside;
  if (raining) {
    const a = rainMesh.instanceMatrix.array, cp = camera.position;
    for (let i = 0; i < RAIN_N; i++) {
      let x = rainP[i * 3], y = rainP[i * 3 + 1], z = rainP[i * 3 + 2];
      y -= 32 * dt; x += 3 * dt;
      if (y < -2) { y = 30; x = rand(-35, 35); z = rand(-35, 35); if (Math.random() < 0.08) emit(cp.x + x, Math.max(0.1, heightAt(cp.x + x, cp.z + z, cp.y)) + 0.05, cp.z + z, rand(-0.6, 0.6), rand(1, 2), rand(-0.6, 0.6), 0.25, 0.06, '#cfd8e6', 0.6); }
      if (x > 35) x -= 70;
      rainP[i * 3] = x; rainP[i * 3 + 1] = y; rainP[i * 3 + 2] = z;
      const o = i * 16; a.fill(0, o, o + 16); a[o] = a[o + 5] = a[o + 10] = a[o + 15] = 1; a[o + 4] = 0.08;
      a[o + 12] = cp.x + x; a[o + 13] = cp.y - 6 + y; a[o + 14] = cp.z + z;
    }
    rainMesh.instanceMatrix.needsUpdate = true;
    lightningT -= dt;
    if (lightningT <= 0 && S.hour > 18 || lightningT <= 0 && S.hour < 6) { lightningT = rand(14, 32); hemi.intensity += 3; setTimeout(() => SFX.burst(2.2, 160, 0.7), rand(400, 1600)); }
  }
}

/* ---------- reflets d'objectif du soleil */
const flareTex = (draw) => { const c = document.createElement('canvas'); c.width = c.height = 128; draw(c.getContext('2d')); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
const FLARE0 = flareTex(g => { const r = g.createRadialGradient(64, 64, 0, 64, 64, 64); r.addColorStop(0, 'rgba(255,250,235,1)'); r.addColorStop(0.15, 'rgba(255,230,190,.8)'); r.addColorStop(1, 'rgba(255,200,140,0)'); g.fillStyle = r; g.fillRect(0, 0, 128, 128); });
const FLARE1 = flareTex(g => { g.strokeStyle = 'rgba(180,220,255,.35)'; g.lineWidth = 6; g.beginPath(); for (let i = 0; i <= 6; i++) { const a = i / 6 * Math.PI * 2; g[i ? 'lineTo' : 'moveTo'](64 + Math.cos(a) * 50, 64 + Math.sin(a) * 50); } g.stroke(); });
const lensflare = new Lensflare();
lensflare.addElement(new LensflareElement(FLARE0, 420, 0, new THREE.Color(1, 0.95, 0.85)));
lensflare.addElement(new LensflareElement(FLARE1, 70, 0.35));
lensflare.addElement(new LensflareElement(FLARE0, 50, 0.55, new THREE.Color(0.6, 0.8, 1)));
lensflare.addElement(new LensflareElement(FLARE1, 120, 0.8));
lensflare.addElement(new LensflareElement(FLARE0, 35, 1.0, new THREE.Color(1, 0.7, 0.5)));
sun.add(lensflare);

/* ---------- niveaux de qualité : Standard / Cinéma / Ultra */
let gtaoPass = null;
const GFX_NAMES = { standard: 'Standard', cinema: 'Cinéma', ultra: 'Ultra (réaliste)' };
function setGfx(level, silent) {
  S.gfx = level; S.cinema = level !== 'standard';
  if (S.cinema && !composer) setupFX();
  if (gtaoPass) gtaoPass.enabled = level === 'ultra';
  const ms = level === 'ultra' ? 4096 : isTouch ? 1024 : 2048, half = level === 'ultra' ? 100 : 70;
  if (sun.shadow.mapSize.x !== ms) { sun.shadow.mapSize.set(ms, ms); if (sun.shadow.map) { sun.shadow.map.dispose(); sun.shadow.map = null; } }
  Object.assign(sun.shadow.camera, { left: -half, right: half, top: half, bottom: -half }); sun.shadow.camera.updateProjectionMatrix();
  if (!silent) { try { localStorage.setItem('mirage_gfx', level); } catch (e) { } toast(`🎨 Graphismes : ${GFX_NAMES[level]}`); }
}
const perf = { t: 0, n: 0 };
function autoTune(realDt) {
  if (S.autoTuned || S.mode !== 'play') return;
  perf.t += realDt; perf.n++;
  if (perf.t < 6) return;
  S.autoTuned = true; const fps = perf.n / perf.t;
  let chosen = null; try { chosen = localStorage.getItem('mirage_gfx'); } catch (e) { }
  if (chosen) return;
  if (S.gfx === 'ultra' && fps < 32) { setGfx('cinema', true); toast(`🎨 Qualité ajustée : Cinéma (${Math.round(fps)} img/s)`); }
  else if (S.gfx === 'cinema' && fps < 24) { setGfx('standard', true); toast(`🎨 Qualité ajustée : Standard (${Math.round(fps)} img/s)`); }
}
