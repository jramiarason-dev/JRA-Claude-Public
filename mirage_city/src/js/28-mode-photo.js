/* =====================================================================
   MODE PHOTO : caméra libre, filtres, profondeur de champ, poses, capture
   ===================================================================== */
const PHOTO = { filter: 0, dof: false, fov: 55, pose: 'auto', capture: false };
const PHOTO_FILTERS = ['Aucun', 'Noir & blanc', 'Sépia', 'Vintage', 'Néon', 'Froid'];
const PHOTO_POSES = [['auto', 'Naturel'], ['handsup', 'Mains en l\'air'], ['dance', 'Danse'], ['phone', 'Au téléphone'], ['hero', 'Héroïque'], ['wave', 'Salut']];
(() => {
  const st = document.createElement('style');
  st.textContent = `#photoUI{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:24;width:min(760px,calc(100% - 24px));background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:12px 14px;display:flex;flex-direction:column;gap:8px;backdrop-filter:blur(10px)}
  #photoUI .row{display:flex;gap:6px;flex-wrap:wrap;align-items:center}#photoUI .row b{font-size:12px;color:var(--muted);min-width:78px}
  #photoUI button{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:6px 10px;font-size:13px}#photoUI button.on{background:var(--gold);color:#1b1206;border-color:var(--gold)}
  #photoUI input[type=range]{width:160px}#photoShot{position:fixed;inset:0;z-index:40;background:rgba(5,8,14,.8);display:grid;place-items:center;padding:16px}
  #photoShot .box{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:14px;max-width:min(960px,100%);display:flex;flex-direction:column;gap:10px}#photoShot img{max-width:100%;max-height:70vh;border-radius:10px}`;
  document.head.appendChild(st);
  const ui = document.createElement('div'); ui.id = 'photoUI'; ui.hidden = true; document.body.appendChild(ui);
  const shot = document.createElement('div'); shot.id = 'photoShot'; shot.hidden = true; document.body.appendChild(shot);
})();
function renderPhotoUI() {
  const ui = $('photoUI');
  ui.innerHTML = `<div class="row"><b>📷 Mode photo</b><span style="color:var(--muted);font-size:12px">Glisse pour tourner autour, molette pour zoomer · Échap pour quitter</span></div>
    <div class="row"><b>Filtre</b>${PHOTO_FILTERS.map((n, i) => `<button data-f="${i}" class="${PHOTO.filter === i ? 'on' : ''}">${n}</button>`).join('')}</div>
    <div class="row"><b>Pose</b>${PHOTO_POSES.map(([k, n]) => `<button data-p="${k}" class="${PHOTO.pose === k ? 'on' : ''}">${n}</button>`).join('')}</div>
    <div class="row"><b>Objectif</b><button id="phDof" class="${PHOTO.dof ? 'on' : ''}">Profondeur de champ</button><span style="font-size:12px">Focale</span><input type="range" id="phFov" min="20" max="90" value="${PHOTO.fov}"></div>
    <div class="row"><button id="phCap" style="background:var(--gold);color:#1b1206;font-weight:700">📸 Capturer</button><button id="phQuit">Quitter</button></div>`;
  ui.querySelectorAll('[data-f]').forEach(b => b.onclick = () => { PHOTO.filter = +b.dataset.f; renderPhotoUI(); });
  ui.querySelectorAll('[data-p]').forEach(b => b.onclick = () => { PHOTO.pose = b.dataset.p; renderPhotoUI(); });
  $('phDof').onclick = () => { PHOTO.dof = !PHOTO.dof; renderPhotoUI(); };
  $('phFov').oninput = e => { PHOTO.fov = +e.target.value; };
  $('phCap').onclick = () => { PHOTO.capture = true; };
  $('phQuit').onclick = closePhotoMode;
}
function openPhotoMode() {
  if (S.mode !== 'play') return;
  closePhone(); S.mode = 'photo'; S.photo = true; document.exitPointerLock?.();
  $('hud').hidden = true; $('touch').hidden = true; $('photoUI').hidden = false;
  if (!composer) setupFX();
  PHOTO.fov = Math.round(camera.fov); renderPhotoUI();
}
function closePhotoMode() {
  S.mode = 'play'; S.photo = false; PHOTO.filter = 0; PHOTO.dof = false; if (bokehPass) bokehPass.enabled = false;
  $('photoUI').hidden = true; $('photoShot').hidden = true; $('hud').hidden = false; if (isTouch) $('touch').hidden = false;
}
function applyPhotoPose() {
  if (P.vehicle && !P.vehicle.def.open) return;
  const m = P.model, u = m.userData, t = performance.now() / 1000;
  switch (PHOTO.pose) {
    case 'handsup': pose(m, 'handsup', 0, 0); break;
    case 'dance': pose(m, 'dance', t * 5, 1); break;
    case 'phone': pose(m, 'phone', 0, 0); break;
    case 'hero': pose(m, 'walk', 0, 0); u.armL.rotation.set(0.1, 0, 0.75); u.armR.rotation.set(0.1, 0, -0.75); u.foreL.rotation.x = u.foreR.rotation.x = -1.7; u.legL.rotation.z = 0.12; u.legR.rotation.z = -0.12; u.chest.rotation.x = -0.06; u.head.rotation.x = -0.12; break;
    case 'wave': pose(m, 'walk', 0, 0); u.armR.rotation.set(-0.3, 0, -2.5); u.foreR.rotation.x = -0.5 - Math.abs(Math.sin(t * 6)) * 0.6; u.head.rotation.z = -0.1; break;
    default: if (!P.vehicle) pose(m, 'walk', 0, 0);
  }
}
function photoAfterRender() {
  if (!PHOTO.capture) return;
  PHOTO.capture = false;
  const url = renderer.domElement.toDataURL('image/jpeg', 0.92), name = `mirage-city-${new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-')}.jpg`;
  const box = $('photoShot');
  box.innerHTML = `<div class="box"><b>📸 Photo prise</b><img src="${url}" alt="Capture du jeu"><div style="display:flex;gap:8px;flex-wrap:wrap"><a class="btn primary" href="${url}" download="${name}" style="text-decoration:none;flex:none">⬇️ Télécharger</a><button class="btn" id="shotClose">Fermer</button></div><small style="color:var(--muted)">Si le téléchargement ne démarre pas, fais un clic droit (ou un appui long) sur l'image puis « Enregistrer l'image ».</small></div>`;
  box.hidden = false; $('shotClose').onclick = () => box.hidden = true;
  SFX.burst(0.12, 5000, 0.12);
}
