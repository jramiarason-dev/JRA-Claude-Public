/* =====================================================================
   NIVEAUX DE DÉTAIL, RÉSOLUTION DYNAMIQUE & SAUVEGARDE
   ===================================================================== */
const LOD = { t: 0, frames: 0, acc: 0, basePR: 1, pr: 1 };
function updateLOD(dt, realDt) {
  LOD.t -= dt;
  if (LOD.t <= 0) {
    LOD.t = 0.5;
    const cp = camera.position;
    for (const v of vehicles) {
      const far = v !== P.vehicle && (Math.abs(v.pos.x - cp.x) + Math.abs(v.pos.z - cp.z)) > 160;
      if (v._far !== far) { v._far = far; v.group.traverse(o => { if (o.isMesh) o.castShadow = !far; }); for (const w of v.wheels) w.visible = !far; }
    }
  }
  // résolution dynamique : vise 50 à 60 images/s
  if (S.mode !== 'play' || !S.dynres) return;
  LOD.frames++; LOD.acc += realDt;
  if (LOD.acc < 2) return;
  const fps = LOD.frames / LOD.acc; LOD.frames = 0; LOD.acc = 0;
  let pr = LOD.pr;
  if (fps < 44) pr = Math.max(LOD.basePR * 0.6, pr - 0.1); else if (fps > 58) pr = Math.min(LOD.basePR, pr + 0.1);
  if (Math.abs(pr - LOD.pr) > 0.01) {
    LOD.pr = pr; renderer.setPixelRatio(pr); renderer.setSize(innerWidth, innerHeight);
    if (composer) { composer.setPixelRatio(pr); composer.setSize(innerWidth, innerHeight); }
  }
}
/* ---------- sauvegarde automatique (navigateur) */
const SAVE_KEY = 'mirage_save';
function saveGame() {
  if (S.mode !== 'play' && S.mode !== 'photo') return;
  const v = P.vehicle;
  const data = {
    v: 1, at: Date.now(), pos: [P.pos.x, P.pos.y, P.pos.z], yaw: P.yaw, hour: S.hour, weather: S.weather, weapon: S.weapon, fp: CAM.fp,
    vehicle: v ? { type: v.type, color: v.color, neon: v.neonColor || null } : null, waypoint: S.waypoint, garage: S.garage,
    inside: P.inside ? INTERIORS.indexOf(P.inside) : -1, powers: S.powers,
  };
  try { localStorage.setItem(SAVE_KEY, JSON.stringify(data)); } catch (e) { }
}
function loadSave() { try { const d = JSON.parse(localStorage.getItem(SAVE_KEY) || 'null'); return d && d.v === 1 ? d : null; } catch (e) { return null; } }
let saveT = 8;
function autoSave(dt) { saveT -= dt; if (saveT <= 0) { saveT = 8; saveGame(); } }
addEventListener('pagehide', saveGame);
addEventListener('beforeunload', saveGame);
function continueGame() {
  const d = loadSave(); if (!d) return;
  $('crPlay').click();
  S.hour = d.hour; S.weather = d.weather || 'clair'; setWeapon(d.weapon ?? 1); CAM.fp = !!d.fp; S.garage = d.garage || {}; Object.assign(S.powers, d.powers || {});
  if (d.inside >= 0 && INTERIORS[d.inside]) { enterInterior(INTERIORS[d.inside]); }
  else {
    P.pos.set(d.pos[0], d.pos[1], d.pos[2]); P.yaw = d.yaw; CAM.yaw = d.yaw; P.vel.set(0, 0, 0);
    if (d.vehicle) { spawnVehicleForPlayer(d.vehicle.type); if (P.vehicle) { if (d.vehicle.color && d.vehicle.color !== P.vehicle.color) recolorVehicle(P.vehicle, d.vehicle.color); if (d.vehicle.neon) addNeon(P.vehicle, d.vehicle.neon); P.vehicle.pos.set(d.pos[0], d.pos[1], d.pos[2]); P.vehicle.yaw = d.yaw; } }
  }
  if (d.waypoint) setWaypoint(d.waypoint.x, d.waypoint.z, d.waypoint.name);
  toast('⏯ Partie reprise');
}
