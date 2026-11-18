/* =====================================================================
   CAMERA
   ===================================================================== */
const _t = new V3();
function updateCamera(dt) {
  if (S.mode === 'creator') {
    P.model.visible = true;
    const z = CAM.crZoom ?? 0.3, H = P.model.userData.H || 1;
    rimLight.intensity = 2.4; keyLight.intensity = 1.1;
    rimLight.position.set(P.pos.x - 2.5, P.pos.y + 3, P.pos.z - 3); rimLight.target.position.set(P.pos.x, P.pos.y + 1.4, P.pos.z);
    keyLight.position.set(P.pos.x + 2.5, P.pos.y + 2.2, P.pos.z + 3); keyLight.target.position.copy(rimLight.target.position);
    const ty = lerp(1.0, 1.7, z) * H, cd = lerp(innerWidth > 720 ? 3.0 : 3.8, 0.85, z);
    camera.position.set(P.pos.x + lerp(0.4, 0.12, z), P.pos.y + ty + lerp(0.25, 0.04, z), P.pos.z + cd);
    camera.lookAt(P.pos.x + lerp(0.12, 0.02, z), P.pos.y + ty, P.pos.z);
    return;
  }
  rimLight.intensity = 0; keyLight.intensity = 0;
  const v = P.vehicle;
  if (CAM.fp) {
    let eye;
    if (v) {
      const f = v.fwd, side = v.def.open || v.def.kind === 'heli' ? 0 : 0.42;
      const h = v.def.kind === 'heli' ? 2.0 : v.def.open ? 1.95 : ['bus', 'firetruck', 'tram'].includes(v.type) ? 2.7 : ['suv', 'van', 'ambulance', 'tractor'].includes(v.type) ? 1.9 : v.type === 'yacht' ? 3.4 : 1.25;
      const fo = v.def.kind === 'heli' ? 1.7 : ['bus', 'tram'].includes(v.type) ? (v.type === 'tram' ? 7.6 : 4.6) : v.type === 'firetruck' ? 3.6 : 0.05;
      eye = v.pos.clone().add(new V3(f.z * side, h, -f.x * side)).addScaledVector(f, fo);
      if (performance.now() - CAM.lastMouse > 1500) { CAM.yaw = angleLerp(CAM.yaw, v.yaw, 1 - Math.exp(-4 * dt)); CAM.pitch = lerp(CAM.pitch, 0.04, 1 - Math.exp(-3 * dt)); }
    } else {
      const hs = Math.hypot(P.vel.x, P.vel.z);
      eye = P.pos.clone().add(new V3(0, (P.swim ? 0.45 : 1.68) * P.model.userData.H + (P.onGround ? Math.sin(P.phase * 2) * 0.035 * clamp(hs / 5, 0, 1.4) : 0), 0)).addScaledVector(new V3(Math.sin(CAM.yaw), 0, Math.cos(CAM.yaw)), 0.2);
    }
    camera.position.copy(eye);
    const cp = Math.cos(CAM.pitch);
    camera.lookAt(eye.x + Math.sin(CAM.yaw) * cp, eye.y - Math.sin(CAM.pitch), eye.z + Math.cos(CAM.yaw) * cp);
    CAM.curDist = 0;
    if (CAM.shake > 0) { camera.position.x += rand(-1, 1) * CAM.shake * 0.4; camera.position.y += rand(-1, 1) * CAM.shake * 0.4; CAM.shake = Math.max(0, CAM.shake - dt * 1.8); }
    const fovT = 72 + (v && inp.sprint ? 8 : 0);
    if (Math.abs(camera.fov - fovT) > 0.1) { camera.fov = lerp(camera.fov, fovT, 4 * dt); camera.updateProjectionMatrix(); }
    P.model.visible = false;
    return;
  }
  P.model.visible = !v || !!v.def.open;
  let target, dist;
  if (v) {
    const k = v.def.kind;
    target = v.pos.clone().add(new V3(0, k === 'heli' ? 2.5 : v.type === 'yacht' ? 4 : 1.6, 0));
    dist = (k === 'plane' ? 26 : k === 'heli' ? 17 : v.type === 'yacht' ? 22 : v.type === 'limo' ? 12 : 8.5) + Math.abs(v.speed) * 0.04;
    if (performance.now() - CAM.lastMouse > 1800 && Math.abs(v.speed) > 3) { CAM.yaw = angleLerp(CAM.yaw, v.speed >= 0 ? v.yaw : v.yaw, 1 - Math.exp(-2.2 * dt)); CAM.pitch = lerp(CAM.pitch, k === 'heli' ? 0.3 : 0.18, 1 - Math.exp(-1.5 * dt)); }
  } else {
    target = P.pos.clone().add(new V3(0, P.swim ? 0.8 : 1.55, 0));
    dist = 5.2;
    if (S.weapon > 0 && P.aimT > 0) { dist = 3.4; const r = new V3(-Math.cos(CAM.yaw), 0, Math.sin(CAM.yaw)); target.addScaledVector(r, 0.75); }
  }
  dist *= CAM.dist;
  const cp = Math.cos(CAM.pitch), sp = Math.sin(CAM.pitch);
  const want = _t.set(target.x - Math.sin(CAM.yaw) * cp * dist, target.y + sp * dist, target.z - Math.cos(CAM.yaw) * cp * dist);
  const gy = P.inside ? INT_Y + 0.4 : surfaceY(want.x, want.z) + 0.4; if (want.y < gy) want.y = gy;
  if (P.inside) { const it = P.inside; want.x = clamp(want.x, it.x - it.w / 2 + 0.6, it.x + it.w / 2 - 0.6); want.z = clamp(want.z, it.z - it.d / 2 + 0.6, it.z + it.d / 2 - 0.6); want.y = Math.min(want.y, INT_Y + it.h - 0.6); }
  camera.position.copy(want);
  CAM.curDist = camera.position.distanceTo(target);
  camera.lookAt(target);
  if (CAM.shake > 0) { camera.position.x += rand(-1, 1) * CAM.shake; camera.position.y += rand(-1, 1) * CAM.shake; CAM.shake = Math.max(0, CAM.shake - dt * 1.8); }
  const fovT = S.photo ? PHOTO.fov : 65 + (v && inp.sprint && v.def.kind !== 'heli' ? 12 : 0) + (v ? clamp(Math.abs(v.speed) / 10, 0, 6) : 0);
  if (Math.abs(camera.fov - fovT) > 0.1) { camera.fov = lerp(camera.fov, fovT, 4 * dt); camera.updateProjectionMatrix(); }
}
