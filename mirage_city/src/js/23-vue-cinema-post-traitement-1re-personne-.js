/* =====================================================================
   VUE CINÉMA : post-traitement, 1re personne, GPS, téléphone, trams
   ===================================================================== */
const LIGHT_MAT = new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false });
let LIGHTS, SHOPWIN;
const POOLS = [];
const FILM_SHADER = {
  uniforms: { filt: { value: 0 }, tDiffuse: { value: null }, time: { value: 0 }, grain: { value: 0.03 }, vig: { value: 0.5 }, ab: { value: 0.0018 }, lift: { value: new THREE.Vector3() },
    px: { value: new THREE.Vector2(1 / 1280, 1 / 720) }, sharpen: { value: 0.35 }, speed: { value: 0 }, sat: { value: 1.08 }, contrast: { value: 1.06 },
    shadowTint: { value: new THREE.Vector3(0.94, 1.0, 1.08) }, highTint: { value: new THREE.Vector3(1.06, 1.0, 0.92) } },
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
  fragmentShader: `uniform sampler2D tDiffuse; uniform int filt; uniform float time, grain, vig, ab, sharpen, speed, sat, contrast; uniform vec2 px; uniform vec3 lift, shadowTint, highTint; varying vec2 vUv;
    float rnd(vec2 p){ return fract(sin(dot(p, vec2(12.9898,78.233))) * 43758.5453); }
    void main(){
      vec2 c = vUv - 0.5; float d = length(c); vec2 off = c * ab * (0.5 + d);
      vec3 col = vec3(texture2D(tDiffuse, vUv + off).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - off).b);
      vec3 nb = (texture2D(tDiffuse, vUv + vec2(px.x, 0.)).rgb + texture2D(tDiffuse, vUv - vec2(px.x, 0.)).rgb + texture2D(tDiffuse, vUv + vec2(0., px.y)).rgb + texture2D(tDiffuse, vUv - vec2(0., px.y)).rgb) * 0.25;
      col = max(col + (col - nb) * sharpen, 0.0);
      if (speed > 0.001) { vec3 acc = col; for (int i = 1; i < 8; i++) acc += texture2D(tDiffuse, vUv - c * speed * float(i) * 0.014).rgb; col = mix(col, acc / 8.0, smoothstep(0.12, 0.45, d)); }
      float l = dot(col, vec3(0.2126, 0.7152, 0.0722));
      col = mix(vec3(l), col, sat);
      col *= mix(shadowTint, highTint, smoothstep(0.02, 0.6, l));
      col = pow(max(col, 0.0), vec3(contrast)) * pow(0.18, 1.0 - contrast);
      col += lift;
      if (filt > 0) { float g = dot(col, vec3(0.2126, 0.7152, 0.0722));
        if (filt == 1) col = vec3(g) * 1.08;
        else if (filt == 2) col = vec3(g) * vec3(1.1, 0.9, 0.68);
        else if (filt == 3) col = mix(col, vec3(g), 0.35) * vec3(1.08, 0.97, 0.8) + vec3(0.025, 0.018, 0.0);
        else if (filt == 4) col = pow(col * vec3(1.18, 0.82, 1.3), vec3(0.88));
        else col *= vec3(0.84, 0.98, 1.2); }
      col *= 1.0 - vig * smoothstep(0.32, 0.86, d);
      col += (rnd(vUv * vec2(1733.0, 977.0) + fract(time)) - 0.5) * grain * (0.6 + 0.8 * (1.0 - min(l * 3.0, 1.0)));
      gl_FragColor = vec4(max(col, 0.0), 1.0);
    }`
};
let composer = null, bloomPass = null, filmPass = null, bokehPass = null;
function setupFX() {
  const pr = renderer.getPixelRatio();
  const rt = new THREE.WebGLRenderTarget(Math.floor(innerWidth * pr), Math.floor(innerHeight * pr), { type: THREE.HalfFloatType, samples: isTouch ? 0 : 4 });
  rt.depthTexture = new THREE.DepthTexture(rt.width, rt.height); rt.depthTexture.type = THREE.FloatType;
  composer = new EffectComposer(renderer, rt);
  composer.addPass(new RenderPass(scene, camera));
  gtaoPass = new GTAOPass(scene, camera, innerWidth, innerHeight);
  gtaoPass.blendIntensity = 0.9;
  gtaoPass.updateGtaoMaterial({ radius: 1.8, distanceExponent: 1.5, thickness: 1.5, scale: 1.1, samples: 12 });
  gtaoPass.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 5, rings: 2, samples: 10 });
  gtaoPass.enabled = S.gfx === 'ultra';
  composer.addPass(gtaoPass);
  bokehPass = new BokehPass(scene, camera, { focus: 6, aperture: 0.0035, maxblur: 0.014 }); bokehPass.enabled = false; composer.addPass(bokehPass);
  bloomPass = new UnrealBloomPass(new THREE.Vector2(innerWidth / 2, innerHeight / 2), 0.5, 0.6, 0.8);
  composer.addPass(bloomPass);
  filmPass = new ShaderPass(FILM_SHADER); composer.addPass(filmPass);
  composer.addPass(new OutputPass());
  composer.setPixelRatio(pr); composer.setSize(innerWidth, innerHeight);
}
function renderFrame(time, night) {
  if ((S.cinema || S.photo) && composer) {
    filmPass.uniforms.filt.value = S.photo ? PHOTO.filter : 0;
    bloomPass.strength = lerp(0.14, 0.9, night) + S.wet * 0.15; bloomPass.threshold = lerp(0.95, 0.72, night);
    const u = filmPass.uniforms;
    u.time.value = time; u.lift.value.set(0.003 * night, 0.005 * night, 0.014 * night);
    u.px.value.set(1 / innerWidth, 1 / innerHeight);
    const v = P.vehicle; u.speed.value = v && S.mode === 'play' ? clamp((Math.abs(v.speed) - 25) / 60, 0, 1) * (CAM.fp ? 0.6 : 1) : 0;
    u.sat.value = lerp(1.1, 0.92, S.wet) * (S.weather === 'brume' ? 0.85 : 1);
    composer.render();
  } else renderer.render(scene, camera);
  photoAfterRender();
}

/* ---------- vitrines éclairées (atlas 2x2) */
const SHOPWIN_TEX = canvasTex(512, 256, (g) => {
  const pal = [['#ff4fa3', '#3a7bff'], ['#ffd23a', '#e63946'], ['#2ec5d3', '#6d3fc0'], ['#5ad45a', '#ff7a1a']];
  for (let k = 0; k < 4; k++) {
    const x0 = (k % 2) * 256, y0 = Math.floor(k / 2) * 128;
    const gr = g.createLinearGradient(0, y0, 0, y0 + 128); gr.addColorStop(0, '#fff4dc'); gr.addColorStop(1, '#f2c48a');
    g.fillStyle = gr; g.fillRect(x0, y0, 256, 128);
    g.fillStyle = 'rgba(80,50,30,.55)'; for (let s = 0; s < 3; s++) g.fillRect(x0 + 120, y0 + 30 + s * 32, 130, 4);
    for (let s = 0; s < 3; s++) for (let i = 0; i < 9; i++) { g.fillStyle = pick(['#c8102e', '#2a6fdb', '#f2c230', '#0a7d3b', '#fff', '#6d3fc0']); g.fillRect(x0 + 124 + i * 14, y0 + 14 + s * 32, 10, 15); }
    g.fillStyle = pal[k][0]; g.fillRect(x0 + 10, y0 + 10, 92, 108);
    g.fillStyle = pal[k][1]; g.fillRect(x0 + 16, y0 + 18, 80, 30);
    g.fillStyle = 'rgba(255,255,255,.85)'; for (let i = 0; i < 4; i++) g.fillRect(x0 + 20, y0 + 58 + i * 13, 70 - i * 8, 6);
    g.fillStyle = 'rgba(30,20,10,.75)'; g.fillRect(x0 + 108, y0, 4, 128); g.fillRect(x0, y0 + 124, 256, 4); g.fillRect(x0, y0, 256, 3);
  }
}, false);
const SHOPWIN_MAT = new THREE.MeshStandardMaterial({ map: SHOPWIN_TEX, emissiveMap: SHOPWIN_TEX, emissive: 0xffffff, emissiveIntensity: 0.3, roughness: 0.15, metalness: 0.1 });
function uvCell(geo, i, cols, rows) {
  const uv = geo.attributes.uv, c = i % cols, r = Math.floor(i / cols);
  const u0 = c / cols + 0.003, u1 = (c + 1) / cols - 0.003, vt = 1 - r / rows - 0.003, vb = 1 - (r + 1) / rows + 0.003;
  for (let k = 0; k < uv.count; k++) uv.setXY(k, lerp(u0, u1, uv.getX(k)), lerp(vb, vt, uv.getY(k)));
  return geo;
}
const POOL_TEX = canvasTex(64, 64, (g) => { const r = g.createRadialGradient(32, 32, 0, 32, 32, 32); r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(0.45, 'rgba(255,255,255,.45)'); r.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = r; g.fillRect(0, 0, 64, 64); }, false);
const POOL_MAT = new THREE.MeshBasicMaterial({ map: POOL_TEX, color: 0xffc98a, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false });
function buildPools() {
  const g = new THREE.PlaneGeometry(1, 1); g.rotateX(-Math.PI / 2);
  const im = new THREE.InstancedMesh(g, POOL_MAT, POOLS.length), d = new THREE.Object3D();
  POOLS.forEach((p, i) => { d.position.set(p.x, 0.09, p.z); d.scale.set(p.r * 2, 1, p.r * 2); d.updateMatrix(); im.setMatrixAt(i, d.matrix); });
  im.renderOrder = 2; scene.add(im);
}

/* ---------- rails de tram, caténaires, feux sur potence, panneaux */
const TRAM_LINES = [{ axis: 'z', line: 60, a: 562, b: 898 }, { axis: 'x', line: 780, a: -292, b: 532 }];
function buildTramInfra() {
  for (const L of TRAM_LINES) {
    const { axis, line, a, b } = L;
    for (const dir of [1, -1]) {
      const c = axis === 'z' ? line - LANE * dir : line + LANE * dir;
      for (const o of [-0.72, 0.72]) { if (axis === 'z') DECO.box(0.12, 0.05, b - a, '#a7aab0', c + o, 0.055, (a + b) / 2); else DECO.box(b - a, 0.05, 0.12, '#a7aab0', (a + b) / 2, 0.055, c + o); }
      if (axis === 'z') DECO.box(0.05, 0.05, b - a, '#1b1b1b', c, 6.6, (a + b) / 2); else DECO.box(b - a, 0.05, 0.05, '#1b1b1b', (a + b) / 2, 6.6, c);
    }
    for (let t = a; t <= b; t += 30) {
      if (axis === 'z') { DECO.add(new THREE.CylinderGeometry(0.12, 0.16, 7.2, 6), '#4a4f57', line + 10.2, 3.6, t); DECO.box(15, 0.1, 0.1, '#4a4f57', line + 2.7, 6.9, t); }
      else { DECO.add(new THREE.CylinderGeometry(0.12, 0.16, 7.2, 6), '#4a4f57', t, 3.6, line - 10.2); DECO.box(0.1, 0.1, 15, '#4a4f57', t, 6.9, line - 2.7); }
    }
  }
  // feux sur potence et panneaux bleus aux carrefours genevois
  for (const x of ROADS_X) for (const z of ROADS_Z) {
    if (z < GVA_Z) continue;
    DECO.add(new THREE.CylinderGeometry(0.14, 0.18, 6.8, 8), '#3a3f46', x + 11.2, 3.4, z - 11.2);
    DECO.box(9, 0.16, 0.16, '#3a3f46', x + 6.8, 6.5, z - 11.2);
    DECO.box(0.5, 1.4, 0.4, '#1d1f22', x + 3, 5.7, z - 11.2);
    tlBag('z', 'r').box(0.24, 0.24, 0.06, '#ff2a1a', x + 3, 6.15, z - 11.42); tlBag('z', 'y').box(0.24, 0.24, 0.06, '#ffb300', x + 3, 5.72, z - 11.42); tlBag('z', 'g').box(0.24, 0.24, 0.06, '#2cff6a', x + 3, 5.3, z - 11.42);
    DECO.add(new THREE.CylinderGeometry(0.06, 0.06, 2.6, 6), '#9aa1ab', x - 11.2, 1.3, z + 11.2);
    DECO.add(new THREE.CylinderGeometry(0.45, 0.45, 0.05, 16), '#1f5fbf', x - 11.2, 2.7, z + 11.2, Math.PI / 2);
    DECO.box(0.08, 0.5, 0.06, '#ffffff', x - 11.2, 2.7, z + 11.18);
  }
}
function spawnTrams() {
  for (const L of TRAM_LINES) for (const dir of [1, -1]) {
    const along = rand(L.a + 60, L.b - 60);
    const x = L.axis === 'z' ? L.line - LANE * dir : along, z = L.axis === 'z' ? along : L.line + LANE * dir;
    const yaw = L.axis === 'z' ? (dir > 0 ? 0 : Math.PI) : (dir > 0 ? Math.PI / 2 : -Math.PI / 2);
    const v = new Vehicle('tram', x, z, yaw, '#1f5fbf'); v.driver = 'tram'; v.tram = { L, dir }; v.speed = 6;
  }
}
function updateTram(v, dt) {
  const { L } = v.tram; let dir = v.tram.dir;
  const along = L.axis === 'z' ? v.pos.z : v.pos.x;
  if ((along >= L.b && dir > 0) || (along <= L.a && dir < 0)) {
    dir = -dir; v.tram.dir = dir; v.yaw += Math.PI; v.speed = 0;
    if (L.axis === 'z') v.pos.x = L.line - LANE * dir; else v.pos.z = L.line + LANE * dir;
  }
  const f = v.fwd; let target = 11;
  const blocked = (px, pz, rad) => { const dx = px - v.pos.x, dz = pz - v.pos.z, fd = dx * f.x + dz * f.z; return fd > 2 && fd < 16 && Math.abs(dx * f.z - dz * f.x) < rad; };
  const pp = P.vehicle ? P.vehicle.pos : P.pos;
  if (blocked(pp.x, pp.z, 2.6)) target = 0;
  for (const o of vehicles) if (o !== v && Math.abs(o.pos.x - v.pos.x) < 22 && Math.abs(o.pos.z - v.pos.z) < 22 && blocked(o.pos.x, o.pos.z, 2.4)) { target = 0; break; }
  for (const p of peds) if (Math.abs(p.pos.x - v.pos.x) < 18 && Math.abs(p.pos.z - v.pos.z) < 18 && blocked(p.pos.x, p.pos.z, 1.8)) { target = 0; break; }
  v.speed = lerp(v.speed, target, 1 - Math.exp(-(target > v.speed ? 0.6 : 2.5) * dt));
  v.pos.x += f.x * v.speed * dt; v.pos.z += f.z * v.speed * dt; v.pos.y = 0;
  for (const w of v.wheels) w.rotation.x += v.speed * dt / w.scale.y;
  if (Math.random() < 0.002 && v.speed > 6) SFX.burst(0.25, 3000, 0.04);
}

/* ---------- GPS : point de destination + itinéraire par les routes */
const wpMarker = new THREE.Group();
{
  const dia = new THREE.Mesh(new THREE.OctahedronGeometry(1.1, 0), new THREE.MeshBasicMaterial({ color: new THREE.Color(1.6, 0.15, 0.7), toneMapped: false }));
  dia.scale.set(0.8, 1.3, 0.8); wpMarker.add(dia);
  const beam = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 160, 8, 1, true), new THREE.MeshBasicMaterial({ color: 0xff2fa0, transparent: true, opacity: 0.18, depthWrite: false, toneMapped: false }));
  beam.position.y = 80; wpMarker.add(beam);
  wpMarker.visible = false; scene.add(wpMarker);
}
function setWaypoint(x, z, name) {
  S.waypoint = { x, z, name: name || 'Destination' };
  wpMarker.visible = true; toast(`📍 Itinéraire vers ${S.waypoint.name}`);
}
function clearWaypoint() { S.waypoint = null; wpMarker.visible = false; $('wpLabel').hidden = true; }
const nearestOf = (list, v) => list.reduce((a, b) => Math.abs(b - v) < Math.abs(a - v) ? b : a);
function routePoints(from, to) {
  const inGrid = p => p.x >= -312 && p.x <= 552 && p.z >= -552 && p.z <= 912;
  const pts = [{ x: from.x, z: from.z }];
  if (!inGrid(from) || !inGrid(to)) { pts.push({ x: to.x, z: to.z }); return pts; }
  const snap = p => { const nx = nearestOf(ROADS_X, p.x), nz = nearestOf(ROADS_Z, p.z); return Math.abs(nx - p.x) < Math.abs(nz - p.z) ? { x: nx, z: p.z, ax: 'x' } : { x: p.x, z: nz, ax: 'z' }; };
  const A = snap(from), B = snap(to);
  pts.push(A);
  if (A.ax === 'x') { const zr = B.ax === 'z' ? B.z : nearestOf(ROADS_Z, B.z); pts.push({ x: A.x, z: zr }); pts.push({ x: B.ax === 'x' ? B.x : B.x, z: zr }); }
  else { const xr = B.ax === 'x' ? B.x : nearestOf(ROADS_X, B.x); pts.push({ x: xr, z: A.z }); pts.push({ x: xr, z: B.ax === 'z' ? B.z : B.z }); }
  pts.push(B); pts.push({ x: to.x, z: to.z });
  return pts;
}
function drawRoute(g, offx, offz, scale = 1, lw = 3) {
  if (!S.waypoint) return;
  const pp = P.vehicle ? P.vehicle.pos : P.pos, pts = routePoints(pp, S.waypoint);
  g.save(); g.strokeStyle = '#ff2fa0'; g.lineWidth = lw; g.lineJoin = 'round'; g.lineCap = 'round'; g.shadowColor = '#ff2fa0'; g.shadowBlur = 4;
  g.beginPath(); pts.forEach((p, i) => { const [a, b] = toMap(p.x, p.z); const X = (a - offx) * scale, Y = (b - offz) * scale; i ? g.lineTo(X, Y) : g.moveTo(X, Y); }); g.stroke();
  const [a, b] = toMap(S.waypoint.x, S.waypoint.z); const X = (a - offx) * scale, Y = (b - offz) * scale;
  g.shadowBlur = 0; g.fillStyle = '#ff2fa0'; g.beginPath(); g.moveTo(X, Y - 7); g.lineTo(X + 6, Y); g.lineTo(X, Y + 7); g.lineTo(X - 6, Y); g.closePath(); g.fill();
  g.restore();
}
const _wp = new V3();
function updateWaypoint(time) {
  const lab = $('wpLabel');
  if (!S.waypoint || S.mode !== 'play' || S.photo) { lab.hidden = true; return; }
  const w = S.waypoint, pp = P.vehicle ? P.vehicle.pos : P.pos, d = Math.hypot(w.x - pp.x, w.z - pp.z);
  if (d < 9) { toast(`✅ Arrivé : ${w.name}`); clearWaypoint(); return; }
  const gy = heightAt(w.x, w.z, 2000);
  wpMarker.position.set(w.x, gy + 3 + Math.sin(time * 2) * 0.3, w.z); wpMarker.children[0].rotation.y = time * 1.5;
  const s = Math.max(1, d / 60); wpMarker.children[0].scale.set(0.8 * s, 1.3 * s, 0.8 * s);
  _wp.copy(wpMarker.position).project(camera);
  if (_wp.z > 1 || Math.abs(_wp.x) > 1.2 || Math.abs(_wp.y) > 1.2) { lab.hidden = true; return; }
  lab.hidden = false; lab.style.transform = `translate(${(_wp.x + 1) / 2 * innerWidth}px, ${(1 - _wp.y) / 2 * innerHeight + 28}px) translate(-50%, 0)`;
  lab.textContent = d > 1000 ? `${(d / 1000).toFixed(1)} km` : `${Math.round(d)} m`;
}

/* ---------- appels de services : un véhicule arrive vers toi */
function serviceCall(type, label) {
  const pp = P.vehicle ? P.vehicle.pos : P.pos, d = VDEF[type];
  let best = null;
  for (let tries = 0; tries < 30; tries++) {
    const ang = rand(0, 6.28), r = rand(45, 70), x = pp.x + Math.cos(ang) * r, z = pp.z + Math.sin(ang) * r;
    const nx = nearestOf(ROADS_X, x), nz = nearestOf(ROADS_Z, z);
    const p = Math.abs(nx - x) < Math.abs(nz - z) ? { x: nx, z } : { x, z: nz };
    if (isWater(p.x, p.z) || heightAt(p.x, p.z, 1) > 1) continue; best = p; break;
  }
  if (!best || d.kind === 'heli') best = { x: pp.x + 14, z: pp.z + 14 };
  const v = new Vehicle(type, best.x, best.z, Math.atan2(pp.x - best.x, pp.z - best.z)); v.spawned = true;
  if (d.kind === 'heli') { v.pos.y = Math.max(pp.y, 0) + 40; v.come = { t: 0, heli: true }; }
  else v.come = { t: 25 };
  if (v.siren) v.sirenOn = true;
  const mine = vehicles.filter(o => o.spawned); if (mine.length > 14) mine[0].remove();
  toast(`${d.icon} ${label || d.name} arrive…`);
}
function comeControl(v, dt) {
  const pp = P.vehicle ? P.vehicle.pos : P.pos;
  v.come.t -= dt;
  const dx = pp.x - v.pos.x, dz = pp.z - v.pos.z, dist = Math.hypot(dx, dz);
  if (v.come.heli) { v.vy = -6; v.rotorSpd = 1; if (v.pos.y <= heightAt(v.pos.x, v.pos.z, v.pos.y) + 0.1) { v.come = null; v.sirenOn = false; } return null; }
  if (dist < 9 || v.come.t <= 0) { v.come = null; return { thr: 0, steer: 0, brake: true }; }
  const diff = wrapA(Math.atan2(dx, dz) - v.yaw);
  return { thr: v.speed < Math.min(16, dist * 0.6) ? 1 : -0.3, steer: clamp(diff * 2, -1, 1), brake: false, nitro: false };
}

/* ---------- téléphone */
const PHONE_APPS = [
  { id: 'gps', n: 'GPS', i: '🧭', c: 'linear-gradient(135deg,#1fb58a,#0b6b52)' },
  { id: 'call', n: 'Appels', i: '📞', c: 'linear-gradient(135deg,#3ddc6c,#14893a)' },
  { id: 'garage', n: 'Garage', i: '🚗', c: 'linear-gradient(135deg,#ffa24a,#d8571d)' },
  { id: 'meteo', n: 'Météo', i: '⛅', c: 'linear-gradient(135deg,#5ab0ff,#1f5fbf)' },
  { id: 'photo', n: 'Photo', i: '📷', c: 'linear-gradient(135deg,#8a8f99,#3b3f46)' },
  { id: 'wardrobe', n: 'Garde-robe', i: '👕', c: 'linear-gradient(135deg,#e05aa8,#7a1f5a)' },
  { id: 'mycar', n: 'Mon véhicule', i: '🎨', c: 'linear-gradient(135deg,#f0bf62,#a8742a)' },
  { id: 'settings', n: 'Réglages', i: '⚙️', c: 'linear-gradient(135deg,#a3a8b2,#5a5f69)' },
];
const CONTACTS = [
  { n: 'Taxi Mirage', sub: 'Course immédiate', i: '🚕', c: '#f2c230', act: () => serviceCall('taxi') },
  { n: 'Police', sub: '117', i: '👮', c: '#1f4fa0', act: () => serviceCall('police', 'La patrouille') },
  { n: 'Pompiers', sub: '118', i: '🚒', c: '#c8102e', act: () => serviceCall('firetruck', 'Les pompiers') },
  { n: 'Ambulance', sub: '144', i: '🚑', c: '#d9dee5', act: () => serviceCall('ambulance', "L'ambulance") },
  { n: 'Karim, mécano', sub: 'Livre ta supercar', i: '🔧', c: '#8a5a33', act: () => serviceCall('supercar', 'Ta supercar') },
  { n: 'Léa, pilote', sub: 'Hélicoptère', i: '🚁', c: '#3b3f46', act: () => serviceCall('heli', "L'hélicoptère") },
  { n: 'Artificier', sub: 'Feux d\'artifice', i: '🎆', c: '#6d3fc0', act: () => launchFireworks(16) },
];
let phoneScreen = 'home', callTimer = null;
function openPhone() { if (S.mode !== 'play') return; S.phone = true; document.exitPointerLock?.(); $('phone').hidden = false; renderPhone('home'); SFX.burst(0.05, 4000, 0.05); }
function closePhone() { S.phone = false; $('phone').hidden = true; if (callTimer) { clearTimeout(callTimer); callTimer = null; } }
function togglePhone() { S.phone ? closePhone() : openPhone(); }
function renderPhone(screen, arg) {
  phoneScreen = screen; const el = $('phScreen');
  const back = `<button class="ph-back" data-go="home">‹ Accueil</button>`;
  if (screen === 'home') {
    const h = S.hour, hh = String(Math.floor(h)).padStart(2, '0'), mm = String(Math.floor((h % 1) * 60)).padStart(2, '0');
    el.innerHTML = `<div class="ph-big">${hh}:${mm}</div><div class="ph-date">${S.waypoint ? '📍 ' + S.waypoint.name : (P.pos.z > GVA_Z ? 'Genève' : 'Mirage City')}</div>
      <div class="ph-grid">${PHONE_APPS.map(a => `<button class="ph-app" data-app="${a.id}"><span style="background:${a.c}">${a.i}</span>${a.n}</button>`).join('')}</div>`;
  } else if (screen === 'call') {
    el.innerHTML = back + `<div class="ph-title">Contacts</div><div class="ph-list">${CONTACTS.map((c, i) => `<button class="ph-row" data-call="${i}"><span class="ph-av" style="background:${c.c}">${c.i}</span><span><b>${c.n}</b><small>${c.sub}</small></span><span class="ph-dial">📞</span></button>`).join('')}</div>`;
  } else if (screen === 'calling') {
    const c = CONTACTS[arg];
    el.innerHTML = `<div class="ph-calling"><div class="ph-avbig" style="background:${c.c}">${c.i}</div><div class="ph-cname">${c.n}</div><div class="ph-cstat" id="phStat">Appel en cours…</div><button class="ph-hang" data-go="call">✕</button></div>`;
    SFX.burst(0.15, 1500, 0.06);
    callTimer = setTimeout(() => { const st = $('phStat'); if (st) st.textContent = 'En ligne'; c.act(); callTimer = setTimeout(() => { if (phoneScreen === 'calling') renderPhone('call'); }, 1200); }, 1500);
  } else if (screen === 'gps') {
    el.innerHTML = back + `<div class="ph-title">GPS</div><div class="ph-list">${S.waypoint ? `<button class="ph-row" data-clear="1"><span class="ph-av" style="background:#ff2fa0">✕</span><span><b>Effacer l'itinéraire</b><small>${S.waypoint.name}</small></span></button>` : ''}${LANDMARKS.filter(l => !l.y).map((l, i) => `<button class="ph-row" data-wp="${LANDMARKS.indexOf(l)}"><span class="ph-av" style="background:#22272f">${l.i}</span><span><b>${l.n}</b><small>${Math.round(Math.hypot(l.x - P.pos.x, l.z - P.pos.z))} m</small></span></button>`).join('')}</div>`;
  } else if (screen === 'garage') {
    el.innerHTML = back + `<div class="ph-title">Garage</div><div class="ph-grid small">${Object.entries(VDEF).map(([k, d]) => `<button class="ph-app" data-veh="${k}"><span style="background:#22272f">${d.icon}</span>${d.name.split(' ')[0]}</button>`).join('')}</div>`;
  } else if (screen === 'meteo') {
    el.innerHTML = back + `<div class="ph-title">Météo</div><div class="ph-list">${[['clair', '☀️ Ciel clair'], ['pluie', '🌧️ Pluie (chaussée mouillée)'], ['brume', '🌫️ Brume'], ['sable', '🌪️ Tempête de sable']].map(([k, n]) => `<button class="ph-row" data-wx="${k}"><span><b>${n}</b></span>${S.weather === k ? '<span class="ph-dial">✓</span>' : ''}</button>`).join('')}
      ${[[8, '🌅 Matin'], [13, '🌞 Midi'], [18.6, '🌇 Coucher de soleil'], [22.5, '🌙 Nuit']].map(([h, n]) => `<button class="ph-row" data-hr="${h}"><span><b>${n}</b></span></button>`).join('')}</div>`;
  } else if (screen === 'wardrobe') {
    const list = loadWardrobe();
    el.innerHTML = back + `<div class="ph-title">Garde-robe</div><div class="ph-list">${list.length ? list.map((o, i) => `<button class="ph-row" data-wear="${i}"><span class="ph-av" style="background:${o.topColor}">👕</span><span><b>${o._label || 'Tenue ' + (i + 1)}</b><small>${o.top} · ${o.pants}</small></span></button>`).join('') : '<div style="opacity:.8;font-size:13px">Aucune tenue enregistrée. Ouvre le menu ☰ → Personnage pour en créer.</div>'}</div>`;
  } else if (screen === 'mycar') {
    const v = P.vehicle;
    el.innerHTML = back + `<div class="ph-title">Mon véhicule</div>` + (v ? `<div style="font-size:13px;opacity:.85;margin-bottom:8px">${v.def.icon} ${v.def.name}</div><div style="font-size:12px;opacity:.7">Peinture</div><div class="ph-grid small" style="grid-template-columns:repeat(6,1fr)">${PAINTS.map(c => `<button class="ph-app" data-paint="${c}"><span style="background:${c};width:30px;height:30px;border-radius:50%"></span></button>`).join('')}</div><div style="font-size:12px;opacity:.7;margin-top:10px">Néons sous la caisse</div><div class="ph-grid small" style="grid-template-columns:repeat(6,1fr)">${NEONS.map((c, i) => `<button class="ph-app" data-neon="${i}"><span style="background:${c || '#333'};width:30px;height:30px;border-radius:50%">${c ? '' : '✕'}</span></button>`).join('')}</div><div style="font-size:12px;opacity:.7;margin-top:10px">Les couleurs sont mémorisées pour ce modèle dans le garage.</div>` : '<div style="opacity:.8;font-size:13px">Monte dans un véhicule pour le personnaliser.</div>');
  } else if (screen === 'settings') {
    const row = (k, n, on) => `<button class="ph-row" data-set="${k}"><span><b>${n}</b></span><span class="tgl ${on ? 'on' : ''}"></span></button>`;
    el.innerHTML = back + `<div class="ph-title">Réglages</div><div class="ph-list"><button class="ph-row" data-set="gfx"><span><b>🎨 Graphismes</b><small>${GFX_NAMES[S.gfx]} — touche pour changer</small></span></button>${row('fp', '👁️ Vue 1re personne (V)', CAM.fp)}${row('sound', '🔊 Son', !SFX.muted)}</div>`;
  }
  el.querySelectorAll('[data-wear]').forEach(b => b.onclick = () => { applyOutfit(loadWardrobe()[+b.dataset.wear]); });
  el.querySelectorAll('[data-paint]').forEach(b => b.onclick = () => { if (!P.vehicle) return; recolorVehicle(P.vehicle, b.dataset.paint); rememberGarage(P.vehicle); toast('🎨 Nouvelle peinture'); });
  el.querySelectorAll('[data-neon]').forEach(b => b.onclick = () => { if (!P.vehicle) return; addNeon(P.vehicle, NEONS[+b.dataset.neon]); rememberGarage(P.vehicle); });
  el.querySelectorAll('[data-go]').forEach(b => b.onclick = () => { if (callTimer) { clearTimeout(callTimer); callTimer = null; } renderPhone(b.dataset.go); });
  el.querySelectorAll('[data-app]').forEach(b => b.onclick = () => { const id = b.dataset.app; if (id === 'photo') { openPhotoMode(); } else renderPhone(id); });
  el.querySelectorAll('[data-call]').forEach(b => b.onclick = () => renderPhone('calling', +b.dataset.call));
  el.querySelectorAll('[data-wp]').forEach(b => b.onclick = () => { const l = LANDMARKS[+b.dataset.wp]; setWaypoint(l.x, l.z, l.n); closePhone(); });
  el.querySelectorAll('[data-clear]').forEach(b => b.onclick = () => { clearWaypoint(); renderPhone('gps'); });
  el.querySelectorAll('[data-veh]').forEach(b => b.onclick = () => { closePhone(); spawnVehicleForPlayer(b.dataset.veh); });
  el.querySelectorAll('[data-wx]').forEach(b => b.onclick = () => { S.weather = b.dataset.wx; applyTime(); renderPhone('meteo'); });
  el.querySelectorAll('[data-hr]').forEach(b => b.onclick = () => { S.hour = +b.dataset.hr; applyTime(); toast('🕒 Heure changée'); });
  el.querySelectorAll('[data-set]').forEach(b => b.onclick = () => {
    const k = b.dataset.set;
    if (k === 'gfx') setGfx({ standard: 'cinema', cinema: 'ultra', ultra: 'standard' }[S.gfx]); else if (k === 'fp') toggleFP(); else SFX.muted = !SFX.muted;
    renderPhone('settings');
  });
}
function setCinema(on) { setGfx(on ? 'cinema' : 'standard'); }
function toggleFP() { CAM.fp = !CAM.fp; toast(CAM.fp ? '👁️ Vue à la première personne' : '🎥 Vue à la troisième personne'); }
function setPhoto(on) { S.photo = on; $('hud').hidden = on; if (isTouch) $('touch').hidden = on; if (on) setTimeout(() => toast('📷 Mode photo — appuie sur une touche pour revenir'), 50); }
$('phHome').onclick = () => renderPhone('home');
