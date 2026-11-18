/* =====================================================================
   HUD
   ===================================================================== */
function updateHUD() {
  const v = P.vehicle;
  $('vehCard').hidden = !v;
  if (v) { const sp = v.def.kind === 'heli' ? Math.hypot(v.speed, v.vy) : v.loose ? v.vel.length() : Math.abs(v.speed); $('speed').textContent = Math.round(sp * 3.6); $('vehName').textContent = `${v.def.icon} ${v.def.name}${v.def.kind === 'heli' ? ` · alt ${Math.round(v.pos.y)} m` : ''}`; }
  let hint = '';
  const ia = !v && nearInteract();
  if (ia) hint = `<b>F</b> : ${ia.label}`;
  else if (!v) { const n = nearestVehicle(); if (n) hint = `<b>F</b> : monter dans ${n.def.icon} ${n.def.name}`; else if (!P.onGround && !P.para && !S.powers.jetpack && P.vel.y < -8) hint = '<b>Espace</b> : ouvrir le parachute'; else if (P.swim) hint = 'Tu nages — <b>Espace</b> pour sortir de l\'eau'; }
  else if (v.def.kind === 'heli' && v.pos.y < heightAt(v.pos.x, v.pos.z, v.pos.y) + 1) hint = '<b>Espace</b> : décoller · <b>F</b> : descendre';
  if (isTouch) hint = hint.replace('<b>F</b>', '<b>🚗</b>').replace(/<b>Espace<\/b>/g, '<b>Saut</b>');
  const h = $('hint'); if (h._v !== hint) { h.innerHTML = hint; h._v = hint; }
  $('crosshair').style.opacity = S.weapon > 0 ? 1 : 0.35;
}
