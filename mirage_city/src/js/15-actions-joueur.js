/* =====================================================================
   ACTIONS JOUEUR
   ===================================================================== */
function nearestVehicle() {
  let best = null, bd = 1e9;
  for (const v of vehicles) { const d = Math.hypot(v.pos.x - P.pos.x, v.pos.z - P.pos.z) - v.def.r; if (d < 3 && Math.abs(v.pos.y - P.pos.y) < 4 && d < bd) { bd = d; best = v; } }
  return best;
}
function enterVehicle(v) {
  if (v.driver === 'ai') ejectAIDriver(v);
  v.ai = null; v.tram = null; v.come = null; v.driver = 'player'; v.loose = false; v.vel.set(0, 0, 0);
  if (v.burn > 0) { v.burn = 0; v.mat.color.set(0xffffff); v.hp = 10; }
  P.vehicle = v; P.para = false;
  const d = v.def;
  if (d.open) { scene.remove(P.model); v.group.add(P.model); const H = P.model.userData.H; P.model.position.set(d.seat[0], d.seat[1] - 0.95 * H + 0.05, d.seat[2]); P.model.rotation.set(0, 0, 0); pose(P.model, 'sit', 0); }
  else P.model.visible = false;
  P.jetMesh.visible = false; P.chute.visible = false;
  CAM.yaw = v.yaw; toast(`${d.icon} ${d.name}`);
}
function exitVehicle(fly = false) {
  const v = P.vehicle; if (!v) return;
  v.driver = null; P.vehicle = null;
  if (P.model.parent !== scene) { v.group.remove(P.model); scene.add(P.model); }
  P.model.visible = true; P.model.rotation.set(0, v.yaw, 0);
  const f = v.fwd; P.pos.set(v.pos.x + f.z * (v.def.r * 0.75 + 0.6), v.pos.y + 0.5, v.pos.z - f.x * (v.def.r * 0.75 + 0.6));
  collide(P.pos, 0.4, 1.8);
  P.vel.set(0, fly ? 14 : 0, 0); P.onGround = false; P.yaw = v.yaw;
  SFX.engine(false, 0, '');
}
function toggleVehicle() {
  if (P.vehicle) { exitVehicle(); return; }
  const it = nearInteract(); if (it) { it.act(); return; }
  const v = nearestVehicle(); if (v) enterVehicle(v);
}
function setWeapon(n) { S.weapon = n; updateGunMesh(); const w = WEAPONS[n]; $('wIcon').textContent = w.icon; $('wName').textContent = w.name; }
function togglePower(k) {
  S.powers[k] = !S.powers[k];
  const names = { superJump: 'Super saut', superSpeed: 'Super vitesse', slowmo: 'Ralenti', jetpack: 'Jetpack' };
  toast(`${names[k]} : ${S.powers[k] ? 'activé' : 'désactivé'}`);
}
function spawnVehicleForPlayer(type) {
  const d = VDEF[type];
  let x, z, yaw = P.vehicle ? P.vehicle.yaw : P.yaw;
  const base = P.vehicle ? P.vehicle.pos : P.pos;
  const f = new V3(Math.sin(yaw), 0, Math.cos(yaw));
  x = base.x + f.x * (d.r + 4); z = base.z + f.z * (d.r + 4);
  if (d.kind === 'boat' && !isWater(x, z) && base.z > 650) { x = clamp(base.x, -300, 1400); z = LAKE_Z + 25; yaw = 0; toast('⛵ Bateau placé sur le lac'); }
  else if (d.kind === 'boat' && !isWater(x, z)) { x = -380; z = clamp(base.z, -500, 500); if (!isWater(x, z)) z = 0; yaw = -Math.PI / 2; toast('🌊 Bateau placé sur la mer, près de la plage'); }
  let y = heightAt(x, z, base.y + 2);
  if (d.kind === 'heli' && base.y > y) y = base.y;
  if (P.vehicle) exitVehicle();
  const gs = S.garage[type]; const v = new Vehicle(type, x, z, yaw, gs?.color, y); v.spawned = true; if (gs?.neon) addNeon(v, gs.neon);
  collide(v.pos, d.r * 0.75, 1.5);
  const mine = vehicles.filter(o => o.spawned); if (mine.length > 12) mine[0].remove();
  enterVehicle(v);
}
function teleport(x, z, y) {
  const gy = y ?? heightAt(x, z, 2000);
  if (P.vehicle) {
    const v = P.vehicle;
    if (v.def.kind === 'boat' && !isWater(x, z)) exitVehicle();
    else { v.pos.set(x, y ?? Math.max(gy, surfaceY(x, z)), z); v.speed = 0; v.vy = 0; v.air = false; collide(v.pos, v.def.r * 0.75, 1.5); return; }
  }
  P.pos.set(x, gy, z); P.vel.set(0, 0, 0); collide(P.pos, 0.4, 1.8); P.onGround = false;
}

/* ---------- Mise à jour joueur à pied */
function updatePlayerFoot(dt) {
  const pw = S.powers;
  const fx = Math.sin(CAM.yaw), fz = Math.cos(CAM.yaw);
  let mx = fx * inp.fwd - fz * inp.side, mz = fz * inp.fwd + fx * inp.side;
  const ml = Math.hypot(mx, mz); if (ml > 1) { mx /= ml; mz /= ml; }
  const inWater = isWater(P.pos.x, P.pos.z) && P.pos.y < WATER_Y + 0.2;
  P.swim = inWater && !pw.jetpack;
  let spd = inp.sprint ? 9.5 : 4.8; if (pw.superSpeed) spd *= 3.2;
  if (P.swim) spd = inp.sprint ? 5 : 3;
  const jetting = pw.jetpack && inp.jump;
  if (pw.jetpack && !P.onGround) spd = pw.superSpeed ? 45 : 18;
  if (P.para) spd = 9;
  const acc = P.onGround || P.swim ? 12 : (pw.jetpack || P.para ? 3 : 2.5);
  const k = 1 - Math.exp(-acc * dt);
  P.vel.x = lerp(P.vel.x, mx * spd, k); P.vel.z = lerp(P.vel.z, mz * spd, k);
  const jumpEdge = inp.jump && !P.prevJump; P.prevJump = inp.jump;
  if (P.swim) {
    P.vel.y = 0; P.pos.y = lerp(P.pos.y, WATER_Y - 1.15, 6 * dt);
    if (jumpEdge) { P.vel.y = 7; P.pos.y = WATER_Y + 0.25; P.swim = false; }
  } else {
    if (jetting) { P.vel.y = Math.min(P.vel.y + 42 * dt, 16); P.para = false; if (Math.random() < 0.9) for (const s of [-1, 1]) { const f = new V3(Math.sin(P.yaw), 0, Math.cos(P.yaw)); emit(P.pos.x - f.x * 0.3 + f.z * s * 0.12, P.pos.y + 0.8, P.pos.z - f.z * 0.3 - f.x * s * 0.12, rand(-0.5, 0.5), -12, rand(-0.5, 0.5), 0.25, 0.3, pick(['#ffd36b', '#ff7a1a', '#fff2c0']), 0); } }
    else if (pw.jetpack && inp.down) P.vel.y = Math.max(P.vel.y - 30 * dt, -14);
    else if (pw.jetpack && !P.onGround) P.vel.y = lerp(P.vel.y, 0, 2.5 * dt);
    else P.vel.y -= G * dt;
    if (P.para) P.vel.y = Math.max(P.vel.y, -4.5);
    if (jumpEdge && P.onGround && !pw.jetpack) { P.vel.y = pw.superJump ? 32 : 8.5; P.onGround = false; }
    else if (jumpEdge && !P.onGround && !pw.jetpack && P.vel.y < -6) { P.para = !P.para; if (P.para) toast('🪂 Parachute ouvert'); }
  }
  P.pos.addScaledVector(P.vel, dt);
  collide(P.pos, 0.4, 1.8);
  const g = heightAt(P.pos.x, P.pos.z, P.pos.y);
  if (!P.swim) {
    if (P.pos.y <= g) { P.pos.y = g; P.vel.y = Math.max(0, P.vel.y); if (!P.onGround) { P.para = false; } P.onGround = true; }
    else if (P.onGround && P.pos.y - g < 0.6 && P.vel.y <= 0) { P.pos.y = g; }
    else P.onGround = false;
  } else P.onGround = false;
  P.pos.x = clamp(P.pos.x, BOUNDS.x0, BOUNDS.x1); P.pos.z = clamp(P.pos.z, BOUNDS.z0, BOUNDS.z1);
  // orientation & animation
  if (CAM.fp) P.yaw = CAM.yaw;
  const aiming = S.weapon > 0 && (inp.fire || P.aimT > 0);
  if (inp.fire && S.weapon > 0) P.aimT = 1.2; P.aimT -= dt;
  const hs = Math.hypot(P.vel.x, P.vel.z);
  if (aiming) P.yaw = angleLerp(P.yaw, CAM.yaw, 1 - Math.exp(-20 * dt));
  else if (ml > 0.1) P.yaw = angleLerp(P.yaw, Math.atan2(mx, mz), 1 - Math.exp(-12 * dt));
  const m = P.model; m.position.copy(P.pos); m.rotation.set(0, P.yaw, 0);
  let mode = 'walk';
  if (P.swim) { mode = 'swim'; m.rotation.x = 1.2; P.phase += dt * 5; }
  else if (P.para) mode = 'para';
  else if (pw.jetpack && !P.onGround) mode = 'jet';
  else if (!P.onGround && P.vel.y < -10) mode = 'fall';
  else P.phase += dt * Math.min(hs, 14) * 1.7;
  pose(m, mode, P.phase, P.onGround ? clamp(hs / 5, 0, 1.3) : 0.3);
  if (S.weapon > 0 && !P.swim) m.userData.fingR.rotation.z = 1.25;
  if (aiming && !P.swim) { const u = m.userData; u.armR.rotation.set(-Math.PI / 2 + CAM.pitch * 0.8, 0, 0); if (S.weapon >= 2) { u.armL.rotation.set(-1.15 + CAM.pitch * 0.6, 0, -0.5); u.foreL.rotation.x = -0.55; } u.spine.rotation.y = 0.12; u.head.rotation.x = CAM.pitch * 0.5; }
  if (P.punchT > 0) { P.punchT -= dt; const u = m.userData, k = Math.sin((0.25 - P.punchT) / 0.25 * Math.PI); u.armR.rotation.set(-1.5 * k - 0.2, 0, 0); u.foreR.rotation.x = -1.4 * (1 - k); u.chest.rotation.y = -0.35 * k; u.armL.rotation.set(-1.0, 0, 0.3); u.foreL.rotation.x = -1.8; }
  P.jetMesh.visible = pw.jetpack; P.chute.visible = P.para;
}

/* ---------- Mise à jour joueur en véhicule */
function updatePlayerVehicle(dt) {
  const v = P.vehicle;
  const c = { thr: inp.fwd, steer: -inp.side, brake: inp.jump && v.def.kind !== 'heli' && v.def.kind !== 'plane', up: inp.jump, down: inp.down, nitro: inp.sprint };
  if (v.loose) looseVehicle(v, dt); else driveVehicle(v, c, dt);
  if (c.nitro && v.def.kind !== 'heli' && c.thr > 0) { const f = v.fwd; for (const s of [-1, 1]) emit(v.pos.x - f.x * 2.4 + f.z * s * 0.5, v.pos.y + 0.6, v.pos.z - f.z * 2.4 - f.x * s * 0.5, -f.x * 8, 0.5, -f.z * 8, 0.18, 0.35, pick(['#7fd4ff', '#ffffff', '#3aa0ff']), 0); }
  if (v.def.kind === 'car' && c.brake && Math.abs(v.speed) > 15 && !v.air) { const f = v.fwd; emit(v.pos.x - f.x * 1.8, v.pos.y + 0.2, v.pos.z - f.z * 1.8, rand(-1, 1), rand(0.5, 1.5), rand(-1, 1), 0.8, 0.8, '#d8d2c4', -0.05, 1); }
  // collisions avec véhicules & piétons
  const sp = Math.abs(v.speed) + Math.hypot(v.vel.x, v.vel.z);
  for (const o of vehicles) {
    if (o === v) continue;
    const dx = o.pos.x - v.pos.x, dz = o.pos.z - v.pos.z, d = Math.hypot(dx, dz), m = (v.def.r + o.def.r) * 0.75;
    if (d < m && Math.abs(o.pos.y - v.pos.y) < 3) {
      const nx = dx / (d || 1), nz = dz / (d || 1);
      if (sp > 6) { makeLoose(o, nx * sp * 0.6 + v.fwd.x * sp * 0.3, sp * 0.15 + 2, nz * sp * 0.6 + v.fwd.z * sp * 0.3); SFX.burst(0.3, 500, 0.5); shake(0.3); for (let i = 0; i < 10; i++) emit(v.pos.x + nx * d / 2, v.pos.y + 1, v.pos.z + nz * d / 2, rand(-5, 5), rand(1, 5), rand(-5, 5), 0.4, 0.15, '#ffd36b', 1); }
      v.pos.x -= nx * (m - d) * 0.5; v.pos.z -= nz * (m - d) * 0.5; v.speed *= 0.6;
    }
  }
  if (sp > 4) for (const p of peds) {
    if (p.state === 'fly') continue;
    const dx = p.pos.x - v.pos.x, dz = p.pos.z - v.pos.z, d = Math.hypot(dx, dz);
    if (d < v.def.r * 0.7 + 0.5 && Math.abs(p.pos.y - v.pos.y) < 2.5) { const f = v.fwd, s = Math.abs(v.speed); knockPed(p, f.x * s * 0.9 + dx / (d || 1) * 3, s * 0.35 + 3, f.z * s * 0.9 + dz / (d || 1) * 3); }
  }
  if (v.burn > 0) { v.burn -= dt; if (v.burn <= 0) { v.mat.color.set(0xffffff); v.hp = 10; } }
  if (v.def.open) { pose(P.model, 'sit', 0); const u = P.model.userData; if (S.weapon > 0 && P.aimT > 0) { u.armR.rotation.x = -Math.PI / 2; u.foreR.rotation.x = 0; } u.chest.rotation.z = clamp(-inp.side * 0.15, -0.15, 0.15); }
  if (inp.fire && S.weapon > 0) P.aimT = 1; P.aimT -= dt;
  SFX.engine(true, v.def.kind === 'heli' ? 60 + v.speed : v.speed, v.def.kind);
}
