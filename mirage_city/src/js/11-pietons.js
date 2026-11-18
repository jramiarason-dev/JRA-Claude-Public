/* =====================================================================
   PIETONS
   ===================================================================== */
const peds = [];
const blockIdx = (cx, cz) => BLOCKS_X.includes(cx) && BLOCKS_Z.includes(cz);
function cornerOf(cx, cz, k) { const sx = (k === 1 || k === 2) ? 1 : -1, sz = k >= 2 ? 1 : -1; return { x: cx + sx * 48, z: cz + sz * 48 }; }
function makePed(x, z) {
  const o = randomChar(); const m = buildCharacter(o); scene.add(m);
  const p = { region: 'dxb', model: m, pos: new V3(x, 0, z), yaw: 0, state: 'walk', t: 0, vel: new V3(), phase: Math.random() * 6, speed: rand(1.2, 1.7), cw: Math.random() < 0.5 ? 1 : 3 };
  placePedOnBlock(p, pick(BLOCKS_X), pick(BLOCKS_Z));
  if (x !== undefined) { const b = nearestBlock(x, z); placePedOnBlock(p, b.cx, b.cz); }
  peds.push(p); return p;
}
function nearestBlock(x, z) { let best = { cx: 0, cz: 0 }, bd = 1e9; for (const cx of BLOCKS_X) for (const cz of BLOCKS_Z) { const d = (cx - x) ** 2 + (cz - z) ** 2; if (d < bd) { bd = d; best = { cx, cz }; } } return best; }
function placePedOnBlock(p, cx, cz) {
  p.bx = cx; p.bz = cz; const k = Math.floor(Math.random() * 4), c = cornerOf(cx, cz, k), c2 = cornerOf(cx, cz, (k + p.cw) % 4);
  const t = Math.random(); p.pos.set(lerp(c.x, c2.x, t), 0, lerp(c.z, c2.z, t)); p.k = (k + p.cw) % 4; p.target = c2;
}
function pedNext(p) {
  const c = cornerOf(p.bx, p.bz, p.k);
  if (Math.random() < 0.22) { // traverser la rue
    const sx = Math.sign(c.x - p.bx), sz = Math.sign(c.z - p.bz);
    const opts = [];
    if (blockIdx(p.bx + sx * 120, p.bz)) opts.push([p.bx + sx * 120, p.bz]);
    if (blockIdx(p.bx, p.bz + sz * 120)) opts.push([p.bx, p.bz + sz * 120]);
    if (opts.length) {
      const [nx, nz] = pick(opts); p.crossAxis = nx !== p.bx ? 'z' : 'x'; p.bx = nx; p.bz = nz;
      const tx = c.x + (nx !== c.x - sx * 48 ? 0 : 0);
      const ncx = nx + Math.sign(c.x - nx) * 48, ncz = nz + Math.sign(c.z - nz) * 48;
      p.target = { x: ncx, z: ncz };
      p.k = [[-1, -1], [1, -1], [1, 1], [-1, 1]].findIndex(([a, b]) => a === Math.sign(ncx - nx) && b === Math.sign(ncz - nz));
      return;
    }
  }
  p.k = (p.k + p.cw) % 4; p.target = cornerOf(p.bx, p.bz, p.k);
}
function knockPed(p, ix, iy, iz) {
  const mag = Math.hypot(ix, iz) + Math.max(0, iy - 4) * 0.6;
  if (mag < 9 && p.state !== 'fly' && p.state !== 'down' && p.state !== 'getup') { // choc léger : il titube et rattrape son équilibre
    p.state = 'stagger'; p.t = rand(0.9, 1.4); p.vel.set(ix * 0.55, 0, iz * 0.55); p.lean = clamp(mag / 9, 0.35, 1); p.yaw = Math.atan2(-ix, -iz);
    return;
  }
  p.state = 'fly'; p.vel.set(ix, iy, iz); p.spin = rand(-5, 5); p.t = 0; p.tilt = rand(-0.5, 0.5);
  for (let i = 0; i < 6; i++) emit(p.pos.x, p.pos.y + 1, p.pos.z, rand(-3, 3), rand(1, 4), rand(-3, 3), 0.6, 0.25, '#ffe9a8', 0.5);
}
function panicAround(x, z, r) { for (const p of peds) if (p.state === 'walk' && Math.abs(p.pos.x - x) < r && Math.abs(p.pos.z - z) < r) { p.state = 'flee'; p.t = rand(4, 7); } }
function updatePeds(dt) {
  const pp = P.vehicle ? P.vehicle.pos : P.pos;
  for (const p of peds) {
    const m = p.model;
    { const dcx = p.pos.x - camera.position.x, dcz = p.pos.z - camera.position.z, dc2 = dcx * dcx + dcz * dcz; m.visible = dc2 < 170 * 170; p.tick = (p.tick || 0) + 1; m.userData.skip = !m.visible || (dc2 > 70 * 70 && p.tick % 3 !== 0); }
    if (Math.abs(p.pos.x - pp.x) > 240 || Math.abs(p.pos.z - pp.z) > 240) {
      if (p.state !== 'fly') respawnPedNear(p, pp);
      continue;
    }
    if (p.state === 'fly') {
      p.vel.y -= G * dt; p.pos.addScaledVector(p.vel, dt); p.yaw += p.spin * dt; p.spin *= 1 - 0.8 * dt;
      m.rotation.x = lerp(m.rotation.x, -Math.PI / 2, 3.2 * dt); m.rotation.z = lerp(m.rotation.z, p.tilt, 2 * dt);
      const g = surfaceY(p.pos.x, p.pos.z);
      pose(m, p.vel.y < 0 && p.pos.y - g < 1.4 ? 'protect' : 'flail', 0);
      if (p.pos.y <= g) { p.pos.y = g; if (p.vel.y < -5) { p.vel.y *= -0.28; p.vel.x *= 0.55; p.vel.z *= 0.55; p.spin *= 0.5; } else { p.state = 'down'; p.t = rand(2.5, 4.5); p.vel.set(0, 0, 0); } }
    } else if (p.state === 'down') {
      p.t -= dt; m.rotation.x = -Math.PI / 2; pose(m, 'rag', 0);
      if (p.t <= 0) { p.state = 'getup'; p.t = 1.3; }
    } else if (p.state === 'getup') {
      p.t -= dt; const k = clamp(1 - p.t / 1.3, 0, 1);
      m.rotation.x = -Math.PI / 2 * (1 - smooth(0.1, 0.75, k)); m.rotation.z = lerp(m.rotation.z, 0, 4 * dt); pose(m, 'getup', 0, 1, k);
      if (p.t <= 0) { m.rotation.x = 0; m.rotation.z = 0; p.state = 'flee'; p.t = rand(3, 5); }
    } else if (p.state === 'stagger') {
      p.t -= dt; p.pos.addScaledVector(p.vel, dt); p.vel.multiplyScalar(1 - 3 * dt); p.phase += dt * 11;
      pose(m, 'stagger', p.phase, 1, p.lean * clamp(p.t, 0, 1)); m.rotation.x = 0;
      if (p.t <= 0) { if (p.lean > 0.9 && Math.random() < 0.5) { p.state = 'down'; p.t = rand(1.5, 2.5); } else { p.state = 'flee'; p.t = rand(3, 5); } }
    } else if (p.state === 'idle' || p.state === 'handsup') {
      p.t -= dt; pose(m, p.state === 'handsup' ? 'handsup' : p.idle, 0, 0); m.rotation.x = 0;
      if (p.t <= 0) p.state = p.state === 'handsup' ? 'flee' : 'walk', p.t = rand(3, 5);
    } else if (p.state === 'dance') {
      p.t -= dt; p.phase += dt * 5; p.yaw += dt * 3; pose(m, 'dance', p.phase); m.rotation.x = 0;
      if (p.t <= 0) p.state = 'walk';
    } else {
      const fleeing = p.state === 'flee'; if (fleeing) { p.t -= dt; if (p.t <= 0) p.state = 'walk'; }
      const sp = fleeing ? 5 : p.speed;
      const dx = p.target.x - p.pos.x, dz = p.target.z - p.pos.z, d = Math.hypot(dx, dz);
      const waiting = p.crossAxis && !fleeing && lightState(p.crossAxis) !== 'r'; if (p.crossAxis && !waiting) p.crossAxis = null;
      if (waiting) { pose(m, 'walk', 0, 0); m.position.set(p.pos.x, p.pos.y, p.pos.z); m.rotation.y = p.yaw; continue; }
      if (d < 0.7) { pedNext(p); if (!fleeing && Math.random() < 0.18) { p.state = 'idle'; p.t = rand(3, 8); p.idle = pick(['walk', 'phone', 'phone', 'walk']); } }
      else { p.pos.x += dx / d * sp * dt; p.pos.z += dz / d * sp * dt; p.yaw = angleLerp(p.yaw, Math.atan2(dx, dz), 8 * dt); }
      p.pos.y = surfaceY(p.pos.x, p.pos.z) < 0 ? 0 : surfaceY(p.pos.x, p.pos.z);
      p.phase += dt * sp * (fleeing ? 2.1 : 2.6); pose(m, 'walk', p.phase, fleeing ? 1.45 : 0.9 + (p.speed - 1.2) * 0.4); m.rotation.x = 0; m.rotation.z = 0;
    }
    // conscience de l'environnement : regarde le joueur, lève les mains quand on le vise
    const ddx = pp.x - p.pos.x, ddz = pp.z - p.pos.z, dd = Math.hypot(ddx, ddz);
    if (dd < 14 && !P.vehicle && S.weapon > 0 && P.aimT > 0 && (p.state === 'walk' || p.state === 'idle')) { const ax = -Math.sin(P.yaw) * ddx - Math.cos(P.yaw) * ddz; if (ax / (dd || 1) > 0.85) { p.state = 'handsup'; p.t = rand(2, 3.5); p.yaw = Math.atan2(ddx, ddz); } }
    if (dd < 8 && (p.state === 'walk' || p.state === 'idle' || p.state === 'handsup')) { const rel = clamp(wrapA(Math.atan2(ddx, ddz) - p.yaw), -1.2, 1.2); m.userData.head.rotation.y = lerp(m.userData.head.rotation.y, rel * 0.85, 0.6); }
    m.position.set(p.pos.x, p.pos.y + (p.state === 'down' || p.state === 'fly' ? 0.1 : 0), p.pos.z); m.rotation.y = p.yaw;
  }
}
function respawnPedNear(p, pp) {
  const cands = [];
  for (const cx of BLOCKS_X) for (const cz of BLOCKS_Z) { const d = Math.hypot(cx - pp.x, cz - pp.z); if (d > 60 && d < 200) cands.push([cx, cz]); }
  if (!cands.length) return;
  const [cx, cz] = pick(cands); p.state = 'walk';
  const region = cz > GVA_Z ? 'gva' : 'dxb';
  if (p.region !== region) { scene.remove(p.model); disposeChar(p.model); p.model = buildCharacter(randomChar(region)); scene.add(p.model); p.region = region; }
  p.model.rotation.x = 0; p.model.rotation.z = 0; placePedOnBlock(p, cx, cz);
}
