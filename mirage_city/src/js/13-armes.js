/* =====================================================================
   ARMES
   ===================================================================== */
const WEAPONS = [
  { name: 'Poings', icon: '👊', type: 'melee', rate: 0.35, desc: 'Coup de poing' },
  { name: 'Pistolet', icon: '🔫', type: 'hitscan', rate: 0.22, desc: 'Précis' },
  { name: "Fusil d'assaut", icon: '🪖', type: 'hitscan', rate: 0.08, auto: true, desc: 'Tir automatique' },
  { name: 'Lance-roquettes', icon: '🚀', type: 'rocket', rate: 0.75, desc: 'Explosions géantes' },
  { name: 'Canon à confettis', icon: '🎉', type: 'confetti', rate: 0.12, auto: true, desc: 'Fait danser la foule' },
];
const rockets = [];
const tracers = [];
const _ray = new THREE.Raycaster();
function raySphere(o, d, c, r) { const ox = o.x - c.x, oy = o.y - c.y, oz = o.z - c.z, b = ox * d.x + oy * d.y + oz * d.z, cc = ox * ox + oy * oy + oz * oz - r * r, disc = b * b - cc; if (disc < 0) return -1; return -b - Math.sqrt(disc); }
function rayBox(o, d, c) {
  let tmin = 0, tmax = 1e9;
  const lo = [c.x0, c.y0, c.z0], hi = [c.x1, c.y1, c.z1], oo = [o.x, o.y, o.z], dd = [d.x, d.y, d.z];
  for (let i = 0; i < 3; i++) {
    if (Math.abs(dd[i]) < 1e-8) { if (oo[i] < lo[i] || oo[i] > hi[i]) return -1; continue; }
    let t1 = (lo[i] - oo[i]) / dd[i], t2 = (hi[i] - oo[i]) / dd[i]; if (t1 > t2) [t1, t2] = [t2, t1];
    tmin = Math.max(tmin, t1); tmax = Math.min(tmax, t2); if (tmin > tmax) return -1;
  }
  return tmin;
}
function raycastWorld(o, d, max, skipV, minT = 0.5) {
  let best = { t: max, type: 'none' };
  if (d.y < -1e-4) { const t = (0 - o.y) / d.y; if (t > minT && t < best.t) best = { t, type: 'ground' }; }
  for (const p of peds) { const lying = p.state === 'down' || p.state === 'fly'; const t = raySphere(o, d, { x: p.pos.x, y: p.pos.y + (lying ? 0.3 : 1.0), z: p.pos.z }, lying ? 0.7 : 0.55); if (t > minT && t < best.t) best = { t, type: 'ped', obj: p }; }
  for (const v of vehicles) { if (v === skipV) continue; const t = raySphere(o, d, { x: v.pos.x, y: v.pos.y + 1, z: v.pos.z }, v.def.r * 0.6); if (t > minT && t < best.t) best = { t, type: 'veh', obj: v }; }
  for (const c of colliders) { const t = rayBox(o, d, c); if (t > minT && t < best.t) best = { t, type: 'wall' }; }
  best.point = o.clone().addScaledVector(d, best.t);
  return best;
}
function muzzlePos() {
  if (P.vehicle) { const v = P.vehicle; return v.pos.clone().add(new V3(0, v.def.kind === 'heli' ? 0.8 : 2.0, 0)).addScaledVector(v.fwd, v.def.kind === 'heli' ? 3 : 0.5); }
  const f = new V3(Math.sin(P.yaw), 0, Math.cos(P.yaw));
  return P.pos.clone().add(new V3(-f.z * 0.35, 1.45, f.x * 0.35)).addScaledVector(f, 0.7);
}
function fireWeapon() {
  const w = WEAPONS[S.weapon];
  const camDir = new V3(); camera.getWorldDirection(camDir);
  const skipV = P.vehicle;
  if (w.type === 'melee') {
    if (P.vehicle) return;
    P.punchT = 0.25; SFX.burst(0.08, 900, 0.2);
    const f = new V3(Math.sin(P.yaw), 0, Math.cos(P.yaw));
    for (const p of peds) { const dx = p.pos.x - P.pos.x, dz = p.pos.z - P.pos.z, d = Math.hypot(dx, dz); if (d < 2.4 && (dx * f.x + dz * f.z) / (d || 1) > 0.3 && p.state !== 'fly' && p.state !== 'down') { knockPed(p, f.x * (S.powers.superSpeed ? 30 : 9), S.powers.superSpeed ? 14 : 5, f.z * (S.powers.superSpeed ? 30 : 9)); } }
    for (const v of vehicles) { if (Math.hypot(v.pos.x - P.pos.x, v.pos.z - P.pos.z) < v.def.r + 1.2 && S.powers.superSpeed) makeLoose(v, f.x * 25, 10, f.z * 25); }
    return;
  }
  const minT = CAM.fp ? 0.6 : CAM.curDist + 0.5;
  const hit = raycastWorld(camera.position, camDir, 500, skipV, minT);
  const mz = muzzlePos();
  const aim = hit.point.clone().sub(mz).normalize();
  panicAround(P.pos.x, P.pos.z, 45);
  if (w.type === 'hitscan') {
    SFX.burst(S.weapon === 2 ? 0.09 : 0.14, 2200, 0.35);
    const h2 = raycastWorld(mz, aim, 500, skipV, 0.3);
    addTracer(mz, h2.point);
    for (let i = 0; i < 3; i++) emit(mz.x, mz.y, mz.z, aim.x * 6 + rand(-1, 1), aim.y * 6 + rand(0, 1), aim.z * 6 + rand(-1, 1), 0.08, 0.15, '#ffd36b', 0);
    applyHit(h2, aim, S.weapon === 2 ? 1 : 2);
  } else if (w.type === 'rocket') {
    SFX.burst(0.35, 600, 0.4);
    const m = new THREE.Mesh(ROCKET_GEO, VC_MAT); m.position.copy(mz); m.lookAt(mz.clone().add(aim)); scene.add(m);
    rockets.push({ mesh: m, pos: mz.clone(), vel: aim.clone().multiplyScalar(95), life: 5 });
  } else if (w.type === 'confetti') {
    SFX.burst(0.1, 3500, 0.15);
    for (let i = 0; i < 14; i++) emit(mz.x, mz.y, mz.z, aim.x * 34 + rand(-5, 5), aim.y * 34 + rand(-3, 6), aim.z * 34 + rand(-5, 5), rand(1.2, 2.2), 0.22, pick(['#ff4d6d', '#ffd23a', '#2ec5d3', '#6d3fc0', '#5ad45a', '#ff9f1c']), 0.25, 1.2);
    for (const p of peds) { const dx = p.pos.x - mz.x, dz = p.pos.z - mz.z, d = Math.hypot(dx, dz); if (d < 26 && (dx * aim.x + dz * aim.z) / (d * Math.hypot(aim.x, aim.z) || 1) > 0.9 && (p.state === 'walk' || p.state === 'flee')) { p.state = 'dance'; p.t = rand(4, 7); } }
  }
}
function applyHit(h, dir, power) {
  if (h.type === 'ped') knockPed(h.obj, dir.x * 10 * power, 4 + power * 2, dir.z * 10 * power);
  else if (h.type === 'veh') {
    const v = h.obj; for (let i = 0; i < 6; i++) emit(h.point.x, h.point.y, h.point.z, rand(-4, 4), rand(1, 5), rand(-4, 4), 0.35, 0.12, '#ffd36b', 1);
    if (v.burn <= 0) { v.hp -= power; if (v.hp <= 0) explode(v.pos.clone().add(new V3(0, 1, 0)), 1); }
  } else if (h.type !== 'none') for (let i = 0; i < 5; i++) emit(h.point.x, h.point.y + 0.1, h.point.z, rand(-2, 2), rand(1, 4), rand(-2, 2), 0.4, 0.15, '#cbbd9e', 1);
}
const tracerMat = new THREE.LineBasicMaterial({ color: 0xffe08a, transparent: true, opacity: 0.9 });
function addTracer(a, b) { const g = new THREE.BufferGeometry().setFromPoints([a, b]); const l = new THREE.Line(g, tracerMat); scene.add(l); tracers.push({ l, t: 0.05 }); }
function explode(pos, power = 1) {
  SFX.burst(1.1, 260, 0.9); shake(Math.max(0, 1.2 - pos.distanceTo(camera.position) / 150));
  flash.position.copy(pos).y += 2; flash.intensity = 60 * power;
  for (let i = 0; i < 70; i++) { const a = rand(0, 6.28), e = rand(-0.2, 1), s = rand(6, 22) * power; emit(pos.x, pos.y + 0.5, pos.z, Math.cos(a) * s * Math.cos(e), Math.abs(Math.sin(e)) * s + 3, Math.sin(a) * s * Math.cos(e), rand(0.5, 1.2), rand(0.4, 1.3) * power, pick(['#ffef9a', '#ffb43a', '#ff6a1a', '#ff3b1a']), 0.25, 2); }
  for (let i = 0; i < 26; i++) emit(pos.x + rand(-2, 2), pos.y + rand(0, 3), pos.z + rand(-2, 2), rand(-3, 3), rand(3, 8), rand(-3, 3), rand(1.5, 3), rand(1, 2.4), pick(['#3a3a3a', '#555', '#6b6b6b']), -0.05, 1);
  const R = 15 * power;
  for (const a of animals) { const d = a.pos.distanceTo(pos); if (d < R && a.state !== 'fly') { const k = (1 - d / R) * 20 + 5; knockAnimal(a, (a.pos.x - pos.x) / (d || 1) * k, k, (a.pos.z - pos.z) / (d || 1) * k); } }
  for (const p of peds) { const d = p.pos.distanceTo(pos); if (d < R) { const k = (1 - d / R) * 26 + 6, dx = (p.pos.x - pos.x) / (d || 1), dz = (p.pos.z - pos.z) / (d || 1); knockPed(p, dx * k, k * 0.8 + 4, dz * k); } }
  for (const v of vehicles) {
    const d = v.pos.distanceTo(pos); if (d < R) {
      const k = (1 - d / R) * 18 + 4, dx = (v.pos.x - pos.x) / (d || 1), dz = (v.pos.z - pos.z) / (d || 1);
      if (v === P.vehicle) { if (d < R * 0.6 && v.def.kind !== 'heli') { exitVehicle(true); makeLoose(v, dx * k, k * 0.9, dz * k, rand(-4, 4)); burnVehicle(v); } else { v.speed *= 0.5; } }
      else { makeLoose(v, dx * k, k * 0.9 + 5, dz * k, rand(-5, 5)); if (d < R * 0.6) burnVehicle(v); }
    }
  }
  if (!P.vehicle) { const d = P.pos.distanceTo(pos); if (d < R) { const k = (1 - d / R) * 16 + 4; P.vel.x += (P.pos.x - pos.x) / (d || 1) * k; P.vel.z += (P.pos.z - pos.z) / (d || 1) * k; P.vel.y = Math.max(P.vel.y, k * 0.8); P.onGround = false; } }
  panicAround(pos.x, pos.z, 70);
}
function updateRockets(dt) {
  for (let i = rockets.length - 1; i >= 0; i--) {
    const r = rockets[i]; r.life -= dt; r.pos.addScaledVector(r.vel, dt); r.mesh.position.copy(r.pos);
    emit(r.pos.x, r.pos.y, r.pos.z, rand(-1, 1), rand(-1, 1), rand(-1, 1), 0.6, 0.4, pick(['#cfcfcf', '#ffb43a']), -0.1, 1);
    let hit = r.life <= 0 || r.pos.y <= heightAt(r.pos.x, r.pos.z, r.pos.y) + 0.1;
    if (!hit) for (const c of cquery(r.pos.x, r.pos.z)) if (r.pos.y > c.y0 && r.pos.y < c.y1 && insideXZ(c, r.pos.x, r.pos.z)) { hit = true; break; }
    if (!hit) for (const p of peds) if (p.pos.distanceToSquared(r.pos) < 2.5 && Math.abs(p.pos.y + 1 - r.pos.y) < 1.5) { hit = true; break; }
    if (!hit) for (const v of vehicles) if (v !== P.vehicle && Math.hypot(v.pos.x - r.pos.x, v.pos.z - r.pos.z) < v.def.r * 0.8 && r.pos.y - v.pos.y < 3 && r.pos.y >= v.pos.y - 0.5) { hit = true; break; }
    if (hit) { explode(r.pos, 1); scene.remove(r.mesh); rockets.splice(i, 1); }
  }
  for (let i = tracers.length - 1; i >= 0; i--) { tracers[i].t -= dt; if (tracers[i].t <= 0) { scene.remove(tracers[i].l); tracers[i].l.geometry.dispose(); tracers.splice(i, 1); } }
  flash.intensity *= Math.pow(0.002, dt);
}

/* ---------- Feux d'artifice & fontaine */
const shells = [];
function launchFireworks(n = 14) {
  for (let i = 0; i < n; i++) setTimeout(() => {
    const x = rand(-140, 140), z = rand(-140, 140);
    shells.push({ pos: new V3(x, 20, z), vel: new V3(rand(-4, 4), rand(85, 120), rand(-4, 4)), t: rand(1.8, 2.8), color: pick(['#ff4d6d', '#ffd23a', '#2ec5d3', '#b18cff', '#5ad45a', '#ffffff', '#ff9f1c']) });
    SFX.burst(0.3, 1800, 0.1);
  }, i * 260);
}
function updateFireworks(dt) {
  for (let i = shells.length - 1; i >= 0; i--) {
    const s = shells[i]; s.t -= dt; s.vel.y -= G * 0.6 * dt; s.pos.addScaledVector(s.vel, dt);
    emit(s.pos.x, s.pos.y, s.pos.z, 0, -2, 0, 0.4, 0.6, '#ffd9a0', 0, 1);
    if (s.t <= 0) {
      for (let k = 0; k < 110; k++) { const u = new V3(rand(-1, 1), rand(-1, 1), rand(-1, 1)).normalize().multiplyScalar(rand(26, 34)); emit(s.pos.x, s.pos.y, s.pos.z, u.x, u.y, u.z, rand(1.6, 2.6), 1.3, k % 7 ? s.color : '#ffffff', 0.12, 1.4); }
      SFX.burst(0.6, 500, 0.25); shells.splice(i, 1);
    }
  }
}
let fountainT = 0;
function updateFountain(dt, time) {
  const pp = P.vehicle ? P.vehicle.pos : P.pos;
  if (Math.hypot(pp.x, pp.z - 120) > 380) return;
  fountainT += dt; if (fountainT < 0.03) return; fountainT = 0;
  const night = S.hour < 6.5 || S.hour > 18.5;
  for (let k = 0; k < 12; k++) {
    const a = k / 12 * 6.28 + time * 0.3, r = 18, h = 16 + Math.sin(time * 1.7 + k) * 9;
    emit(Math.cos(a) * r, WATER_Y + 0.3, 120 + Math.sin(a) * r, Math.cos(a) * -2, h, Math.sin(a) * -2, 1.6, 0.42, night ? pick(['#9fd6ff', '#ffd38a', '#e7b0ff']) : '#dff4ff', 0.6, 0);
  }
  emit(0, WATER_Y + 0.3, 120, rand(-1, 1), 30 + Math.sin(time) * 8, rand(-1, 1), 2.2, 0.55, night ? '#ffffff' : '#e8f8ff', 0.6, 0);
}
