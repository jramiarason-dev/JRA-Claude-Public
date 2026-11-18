/* =====================================================================
   ENTREES
   ===================================================================== */
const keys = {};
const inp = { fwd: 0, side: 0, jump: false, down: false, sprint: false, fire: false, firePressed: false };
let mouseDown = false, mouseClicked = false;
const joy = { x: 0, y: 0, id: null };
const tbtn = { jump: false, down: false, fire: false, sprint: false };
addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT') return;
  keys[e.code] = true; const k = e.key.toLowerCase();
  if (S.mode === 'photo') { if (e.code === 'Escape') closePhotoMode(); return; }
  if (S.mode !== 'play') { if (e.code === 'Escape' && S.mode === 'menu') closeMenu(); if (S.mode === 'map' && (e.code === 'Escape' || k === 'm')) closeMap(); return; }
  if (S.photo) { setPhoto(false); return; }
  if (e.code === 'Escape' && S.phone) { closePhone(); return; }
  if (e.code === 'Escape' || e.code === 'Tab' || e.code === 'KeyP') { e.preventDefault(); closePhone(); openMenu(); }
  if (e.code === 'KeyT') togglePhone();
  if (e.code === 'KeyV') toggleFP();
  if (e.code === 'KeyG' && S.waypoint) clearWaypoint();
  if (e.code === 'KeyF' || e.code === 'Enter') toggleVehicle();
  if (k === 'm' || e.code === 'Semicolon') openMap();
  if (e.code === 'KeyJ') togglePower('jetpack');
  if (e.code === 'KeyH') { SFX.horn(true); if (P.vehicle && P.vehicle.siren) P.vehicle.sirenOn = !P.vehicle.sirenOn; }
  if (e.code.startsWith('Digit')) { const n = +e.code.slice(5) - 1; if (n >= 0 && n < WEAPONS.length) setWeapon(n); }
  if (e.code === 'KeyQ' && e.shiftKey) setWeapon((S.weapon + WEAPONS.length - 1) % WEAPONS.length);
  if (e.code === 'KeyR') setWeapon((S.weapon + 1) % WEAPONS.length);
  if (e.code === 'Space') e.preventDefault();
});
addEventListener('keyup', e => { keys[e.code] = false; if (e.code === 'KeyH') SFX.horn(false); });
addEventListener('blur', () => { for (const k in keys) keys[k] = false; mouseDown = false; });
const cv = renderer.domElement;
cv.addEventListener('mousedown', e => {
  SFX.init();
  if (S.mode === 'creator') { drag.on = true; drag.x = e.clientX; return; }
  if (S.photo) { setPhoto(false); return; }
  if (S.phone) { closePhone(); return; }
  if (S.mode !== 'play') return;
  if (!isTouch && document.pointerLockElement !== cv && !lockFailed) {
    try { const r = cv.requestPointerLock?.(); if (r && r.catch) r.catch(() => { lockFailed = true; }); else if (!cv.requestPointerLock) lockFailed = true; } catch (err) { lockFailed = true; }
    return;
  }
  if (e.button === 0) { mouseDown = true; mouseClicked = true; }
});
addEventListener('mouseup', e => { if (e.button === 0) mouseDown = false; drag.on = false; });
addEventListener('mousemove', e => {
  if (S.mode === 'creator' && drag.on) { P.yaw += (e.clientX - drag.x) * 0.01; drag.x = e.clientX; return; }
  const dragLook = lockFailed && document.pointerLockElement !== cv && e.buttons;
  if (S.mode === 'photo' && e.buttons) { CAM.yaw -= e.movementX * 0.005; CAM.pitch = clamp(CAM.pitch + e.movementY * 0.004, -1.1, 1.3); return; }
  if (S.mode === 'play' && (document.pointerLockElement === cv || dragLook)) { CAM.yaw -= e.movementX * 0.0025; CAM.pitch = clamp(CAM.pitch + e.movementY * 0.0022, -1.1, 1.3); CAM.lastMouse = performance.now(); }
});
cv.addEventListener('wheel', e => { if (S.mode === 'creator') { CAM.crZoom = clamp((CAM.crZoom ?? 0.3) - Math.sign(e.deltaY) * 0.15, 0, 1); return; } CAM.dist = clamp(CAM.dist + Math.sign(e.deltaY) * 0.12, 0.45, 2.6); }, { passive: true });
cv.addEventListener('contextmenu', e => e.preventDefault());
const drag = { on: false, x: 0 };
let lockFailed = false;
document.addEventListener('pointerlockerror', () => { lockFailed = true; });
cv.addEventListener('touchstart', e => { SFX.init(); if (S.mode === 'creator') { drag.on = true; drag.x = e.touches[0].clientX; } }, { passive: true });
cv.addEventListener('touchmove', e => { if (S.mode === 'photo') { const x = e.touches[0].clientX, y = e.touches[0].clientY; if (drag.px !== undefined) { CAM.yaw -= (x - drag.px) * 0.008; CAM.pitch = clamp(CAM.pitch + (y - drag.py) * 0.006, -1.1, 1.3); } drag.px = x; drag.py = y; return; } if (S.mode === 'creator' && drag.on) { P.yaw += (e.touches[0].clientX - drag.x) * 0.012; drag.x = e.touches[0].clientX; } }, { passive: true });
cv.addEventListener('touchend', () => { drag.on = false; drag.px = undefined; });

function setupTouch() {
  $('touch').hidden = false;
  const jz = $('joy'), jk = $('joyK');
  const jmove = e => { const r = jz.getBoundingClientRect(); let x = (e.clientX - r.left - r.width / 2) / (r.width / 2), y = (e.clientY - r.top - r.height / 2) / (r.height / 2); const l = Math.hypot(x, y); if (l > 1) { x /= l; y /= l; } joy.x = x; joy.y = y; jk.style.transform = `translate(${x * 40}px,${y * 40}px)`; };
  jz.addEventListener('pointerdown', e => { joy.id = e.pointerId; jz.setPointerCapture(e.pointerId); jmove(e); });
  jz.addEventListener('pointermove', e => { if (e.pointerId === joy.id) jmove(e); });
  const jend = () => { joy.id = null; joy.x = joy.y = 0; jk.style.transform = ''; };
  jz.addEventListener('pointerup', jend); jz.addEventListener('pointercancel', jend);
  const look = $('look'); let lid = null, lx = 0, ly = 0;
  look.addEventListener('pointerdown', e => { lid = e.pointerId; lx = e.clientX; ly = e.clientY; look.setPointerCapture(e.pointerId); });
  look.addEventListener('pointermove', e => { if (e.pointerId !== lid) return; CAM.yaw -= (e.clientX - lx) * 0.006; CAM.pitch = clamp(CAM.pitch + (e.clientY - ly) * 0.005, -1.1, 1.3); lx = e.clientX; ly = e.clientY; CAM.lastMouse = performance.now(); });
  look.addEventListener('pointerup', () => lid = null);
  const hold = (id, key) => { const b = $(id); b.addEventListener('pointerdown', e => { e.preventDefault(); SFX.init(); tbtn[key] = true; if (key === 'fire') mouseClicked = true; b.classList.add('on'); }); const up = () => { tbtn[key] = false; b.classList.remove('on'); }; b.addEventListener('pointerup', up); b.addEventListener('pointerleave', up); b.addEventListener('pointercancel', up); };
  hold('tJump', 'jump'); hold('tDown', 'down'); hold('tFire', 'fire'); hold('tSprint', 'sprint');
  $('tEnter').addEventListener('pointerdown', e => { e.preventDefault(); toggleVehicle(); });
  $('tWeap').addEventListener('pointerdown', e => { e.preventDefault(); setWeapon((S.weapon + 1) % WEAPONS.length); });
}
function readInput() {
  const k = keys;
  inp.fwd = clamp(((k.KeyW || k.ArrowUp) ? 1 : 0) - ((k.KeyS || k.ArrowDown) ? 1 : 0) - joy.y, -1, 1);
  inp.side = clamp(((k.KeyD || k.ArrowRight) ? 1 : 0) - ((k.KeyA || k.ArrowLeft) ? 1 : 0) + joy.x, -1, 1);
  inp.jump = !!(k.Space || tbtn.jump);
  inp.down = !!(k.KeyC || k.ControlLeft || k.ControlRight || tbtn.down);
  inp.sprint = !!(k.ShiftLeft || k.ShiftRight || tbtn.sprint);
  inp.fire = mouseDown || tbtn.fire; inp.firePressed = mouseClicked; mouseClicked = false;
}
