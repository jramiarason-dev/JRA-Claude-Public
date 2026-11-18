/* =====================================================================
   UI : toasts, menu, créateur
   ===================================================================== */
function toast(t) { const d = document.createElement('div'); d.className = 'toast'; d.textContent = t; $('toasts').appendChild(d); setTimeout(() => d.remove(), 2200); while ($('toasts').children.length > 3) $('toasts').firstChild.remove(); }
function openMenu(tab) { if (S.mode !== 'play') return; S.mode = 'menu'; document.exitPointerLock?.(); $('menu').hidden = false; SFX.engine(false, 0, ''); renderMenu(tab || menuTab); }
function closeMenu() { $('menu').hidden = true; S.mode = 'play'; }
function openMap() { if (S.mode !== 'play') return; S.mode = 'map'; document.exitPointerLock?.(); $('bigmap').hidden = false; drawBigMap(); }
function closeMap() { $('bigmap').hidden = true; S.mode = 'play'; }
$('btnMenu').onclick = () => openMenu(); $('menuClose').onclick = closeMenu; $('btnMap').onclick = () => openMap(); $('mapClose').onclick = closeMap;
$('helpX').onclick = () => $('help').hidden = true;
$('menu').addEventListener('click', e => { if (e.target.id === 'menu') closeMenu(); });

const TABS = [['garage', '🚗 Garage'], ['armes', '🔫 Armes'], ['tp', '📍 Téléport'], ['monde', '🌅 Monde'], ['pouvoirs', '⚡ Pouvoirs'], ['perso', '🧍 Personnage'], ['aide', '⌨️ Commandes']];
let menuTab = 'garage';
function renderMenu(tab) {
  menuTab = tab;
  $('menuTabs').innerHTML = TABS.map(([k, n]) => `<button data-t="${k}" class="${k === tab ? 'on' : ''}">${n}</button>`).join('');
  $('menuTabs').querySelectorAll('button').forEach(b => b.onclick = () => renderMenu(b.dataset.t));
  const body = $('menuBody');
  if (tab === 'garage') {
    body.innerHTML = `<p style="margin:0 0 12px;color:var(--muted)">Tous les véhicules sont gratuits et illimités. Clique pour le faire apparaître et monter dedans.</p><div class="grid">${Object.entries(VDEF).map(([k, d]) => `<button class="tile" data-v="${k}"><div class="ic">${d.icon}</div><div class="nm">${d.name}</div><div class="ds">${d.desc} · ${Math.round(d.max * 3.6)} km/h</div></button>`).join('')}</div>`;
    body.querySelectorAll('[data-v]').forEach(b => b.onclick = () => { closeMenu(); spawnVehicleForPlayer(b.dataset.v); });
  } else if (tab === 'armes') {
    body.innerHTML = `<p style="margin:0 0 12px;color:var(--muted)">Munitions infinies. Touches 1 à 5 ou R pour changer.</p><div class="grid">${WEAPONS.map((w, i) => `<button class="tile ${i === S.weapon ? 'on' : ''}" data-w="${i}"><div class="ic">${w.icon}</div><div class="nm">${i + 1}. ${w.name}</div><div class="ds">${w.desc}</div></button>`).join('')}</div>`;
    body.querySelectorAll('[data-w]').forEach(b => b.onclick = () => { setWeapon(+b.dataset.w); renderMenu('armes'); });
  } else if (tab === 'tp') {
    body.innerHTML = `<div class="grid">${LANDMARKS.map((l, i) => `<button class="tile" data-l="${i}"><div class="ic">${l.i}</div><div class="nm">${l.n}</div></button>`).join('')}</div>`;
    body.querySelectorAll('[data-l]').forEach(b => b.onclick = () => { const l = LANDMARKS[+b.dataset.l]; if (l.y && P.vehicle && P.vehicle.def.kind !== 'heli') exitVehicle(); teleport(l.x, l.z, l.y); closeMenu(); toast(`${l.i} ${l.n}`); });
  } else if (tab === 'monde') {
    body.innerHTML = `
      <div class="opt"><div class="l"><b>Heure</b><small id="hLbl"></small></div><input type="range" id="hour" min="0" max="23.99" step="0.05" value="${S.hour}"></div>
      <div class="opt"><div class="l"><b>Figer l'heure</b><small>Arrête le cycle jour / nuit</small></div><button class="tgl ${S.freezeTime ? 'on' : ''}" id="frz"></button></div>
      <div class="opt"><div class="l"><b>Météo</b></div><div class="seg" id="wth">${[['clair', '☀️ Clair'], ['pluie', '🌧️ Pluie'], ['brume', '🌫️ Brume'], ['sable', '🌪️ Tempête de sable']].map(([k, n]) => `<button data-k="${k}" class="${S.weather === k ? 'on' : ''}">${n}</button>`).join('')}</div></div>
      <div class="opt"><div class="l"><b>Qualité graphique</b><small>Ultra : matériaux PBR, occlusion ambiante, ombres fines, anticrénelage</small></div><div class="seg" id="gfxSeg">${Object.entries(GFX_NAMES).map(([k, n]) => `<button data-g="${k}" class="${S.gfx === k ? 'on' : ''}">${n}</button>`).join('')}</div></div>
      <div class="opt"><div class="l"><b>Circulation</b><small id="trL">${S.trafficN} voitures</small></div><input type="range" id="trN" min="0" max="60" step="1" value="${S.trafficN}"></div>
      <div class="opt"><div class="l"><b>Piétons</b><small id="pdL">${S.pedN} passants</small></div><input type="range" id="pdN" min="0" max="120" step="1" value="${S.pedN}"></div>
      <div class="opt"><div class="l"><b>Feux d'artifice</b><small>Au-dessus du centre-ville</small></div><button class="btn" id="fw">🎆 Lancer</button></div>
      <div class="opt"><div class="l"><b>Feux d'artifice automatiques la nuit</b></div><button class="tgl ${S.fwAuto ? 'on' : ''}" id="fwa"></button></div>
      <div class="opt"><div class="l"><b>Son</b></div><button class="tgl ${!SFX.muted ? 'on' : ''}" id="snd"></button></div>`;
    const hl = () => { const h = S.hour; $('hLbl').textContent = `${String(Math.floor(h)).padStart(2, '0')}:${String(Math.floor((h % 1) * 60)).padStart(2, '0')}`; }; hl();
    $('hour').oninput = e => { S.hour = +e.target.value; hl(); applyTime(); };
    $('frz').onclick = e => { S.freezeTime = !S.freezeTime; e.target.classList.toggle('on', S.freezeTime); };
    $('wth').querySelectorAll('button').forEach(b => b.onclick = () => { S.weather = b.dataset.k; renderMenu('monde'); applyTime(); });
    $('gfxSeg').querySelectorAll('button').forEach(b => b.onclick = () => { setGfx(b.dataset.g); renderMenu('monde'); });
    $('trN').oninput = e => { S.trafficN = +e.target.value; $('trL').textContent = `${S.trafficN} voitures`; };
    $('pdN').oninput = e => { S.pedN = +e.target.value; $('pdL').textContent = `${S.pedN} passants`; };
    $('fw').onclick = () => { closeMenu(); launchFireworks(18); };
    $('fwa').onclick = e => { S.fwAuto = !S.fwAuto; e.target.classList.toggle('on', S.fwAuto); };
    $('snd').onclick = e => { SFX.muted = !SFX.muted; e.target.classList.toggle('on', !SFX.muted); };
  } else if (tab === 'pouvoirs') {
    const P_ = [['jetpack', '🎒 Jetpack', 'Espace pour monter, C pour descendre (touche J)'], ['superJump', '🦘 Super saut', 'Saute par-dessus les immeubles'], ['superSpeed', '⚡ Super vitesse', 'Course ×3, véhicules boostés, coups de poing surpuissants'], ['slowmo', '🐢 Ralenti', 'Le temps tourne au ralenti']];
    body.innerHTML = `<p style="margin:0 0 6px;color:var(--muted)">Invincibilité permanente · aucune étoile de recherche · argent illimité.</p>` + P_.map(([k, n, d]) => `<div class="opt"><div class="l"><b>${n}</b><small>${d}</small></div><button class="tgl ${S.powers[k] ? 'on' : ''}" data-p="${k}"></button></div>`).join('') +
      `<div class="opt"><div class="l"><b>🪂 Parachute</b><small>Appuie sur Espace pendant une chute (essaie depuis le sommet de la Tour !)</small></div><span>Toujours dispo</span></div>`;
    body.querySelectorAll('[data-p]').forEach(b => b.onclick = () => { togglePower(b.dataset.p); b.classList.toggle('on', S.powers[b.dataset.p]); });
  } else if (tab === 'perso') {
    body.innerHTML = `<p style="color:var(--muted)">Modifie ton apparence à tout moment.</p><button class="btn primary" id="edit" style="max-width:280px">🧍 Ouvrir l'éditeur de personnage</button>`;
    $('edit').onclick = () => { closeMenu(); openCreator(true); };
  } else if (tab === 'aide') {
    const K = [['ZQSD / WASD / flèches', 'Se déplacer / conduire'], ['Souris', 'Caméra (clique pour la capturer)'], ['Molette', 'Zoom caméra'], ['Maj', 'Sprint / Nitro'], ['Espace', 'Sauter · Frein à main · Monter (hélico/jetpack) · Parachute en chute'], ['C / Ctrl', 'Descendre (hélico / jetpack)'], ['F / Entrée', 'Monter ou descendre d\'un véhicule (même ceux de la circulation)'], ['Clic gauche', 'Tirer / frapper'], ['1 à 5 · R', 'Changer d\'arme'], ['J', 'Jetpack on/off'], ['H', 'Klaxon (sirène sur la Patrouille)'], ['M', 'Grande carte : itinéraire GPS et téléportation'], ['V', 'Vue à la 1re personne'], ['T', 'Téléphone : GPS, appels (taxi, police, pompiers…), garage, météo, photo'], ['G', 'Effacer l\'itinéraire'], ['Échap / Tab', 'Menu']];
    body.innerHTML = `<div class="keys">${K.map(([a, b]) => `<kbd>${a}</kbd><span>${b}</span>`).join('')}</div><p style="color:var(--muted);margin-top:14px">Sur mobile : joystick à gauche, glisse à droite pour la caméra, boutons d'action à droite.</p>`;
  }
}

/* ---------- Créateur de personnage */
const CR_SCHEMA = [
  { sec: 'Identité' },
  { k: 'name', label: 'Nom', type: 'text' },
  { k: 'body', label: 'Silhouette', type: 'seg', opts: OPTS.body },
  { k: 'height', label: 'Taille', type: 'range', min: 0.85, max: 1.15, step: 0.01 },
  { k: 'build', label: 'Corpulence', type: 'range', min: 0.8, max: 1.3, step: 0.01 },
  { k: 'skin', label: 'Teint', type: 'color', opts: SKINS },
  { sec: 'Visage & cheveux' },
  { k: 'eyes', label: 'Couleur des yeux', type: 'color', opts: ['#4a3220', '#2b6cb0', '#3c7a4a', '#6b4f2a', '#8a8f99', '#1b1b1b'] },
  { k: 'hair', label: 'Coiffure', type: 'seg', opts: OPTS.hair },
  { k: 'hairColor', label: 'Couleur des cheveux / barbe', type: 'color', opts: HAIR_COLORS },
  { k: 'beard', label: 'Barbe', type: 'seg', opts: OPTS.beard },
  { k: 'head', label: 'Couvre-chef', type: 'seg', opts: OPTS.head },
  { k: 'hatColor', label: 'Couleur de la casquette / cagoule / bonnet', type: 'color', opts: CLOTH },
  { sec: 'Tenue' },
  { k: 'top', label: 'Haut', type: 'seg', opts: OPTS.top },
  { k: 'topColor', label: 'Couleur du haut', type: 'color', opts: CLOTH },
  { k: 'motif', label: 'Motif du haut', type: 'seg', opts: OPTS.motif },
  { k: 'pants', label: 'Bas', type: 'seg', opts: OPTS.pants },
  { k: 'pantsColor', label: 'Couleur du bas', type: 'color', opts: CLOTH },
  { sec: 'Chaussures' },
  { k: 'shoeStyle', label: 'Modèle', type: 'seg', opts: OPTS.shoeStyle },
  { k: 'shoes', label: 'Couleur des baskets', type: 'color', opts: CLOTH },
  { k: 'sole', label: 'Semelle', type: 'color', opts: ['#f2f2f2', '#1c1c1e', '#d9c7a1', '#8a5a33', '#c8102e', '#2a6fdb'] },
  { k: 'shoeAccent', label: 'Bande latérale', type: 'color', opts: CLOTH },
  { sec: 'Accessoires' },
  { k: 'acc', label: '', type: 'toggles', opts: [['glasses', '🕶️ Lunettes de soleil'], ['watch', '⌚ Montre (bracelet cuir)'], ['chain', '📿 Chaîne en or'], ['gloves', '🧤 Gants noirs']] },
];
function renderCreator() {
  const box = $('crOptions');
  box.innerHTML = CR_SCHEMA.map(f => {
    if (f.sec) return `<div class="cr-sec">${f.sec}</div>`;
    let inner = '';
    if (f.type === 'text') inner = `<input type="text" data-k="${f.k}" maxlength="18" value="${(CHAR[f.k] || '').replace(/"/g, '&quot;')}" placeholder="Ton nom">`;
    if (f.type === 'seg') inner = `<div class="seg">${f.opts.map(([v, n]) => `<button data-k="${f.k}" data-v="${v}" class="${CHAR[f.k] === v ? 'on' : ''}">${n}</button>`).join('')}</div>`;
    if (f.type === 'color') inner = `<div class="sw">${f.opts.map(c => `<button data-k="${f.k}" data-v="${c}" style="background:${c}" class="${CHAR[f.k] === c ? 'on' : ''}" aria-label="${c}"></button>`).join('')}</div>`;
    if (f.type === 'range') inner = `<input type="range" data-k="${f.k}" min="${f.min}" max="${f.max}" step="${f.step}" value="${CHAR[f.k]}">`;
    if (f.type === 'toggles') inner = `<div class="seg">${f.opts.map(([k, n]) => `<button data-t="${k}" class="${CHAR[k] ? 'on' : ''}">${n}</button>`).join('')}</div>`;
    return `<div class="cr-row">${f.label ? `<label>${f.label}</label>` : ''}${inner}</div>`;
  }).join('');
  box.querySelectorAll('button[data-v]').forEach(b => b.onclick = () => { CHAR[b.dataset.k] = b.dataset.v; charChanged(); });
  box.querySelectorAll('button[data-t]').forEach(b => b.onclick = () => { CHAR[b.dataset.t] = !CHAR[b.dataset.t]; charChanged(); });
  box.querySelectorAll('input[type=range]').forEach(i => i.oninput = () => { CHAR[i.dataset.k] = +i.value; charChanged(false); });
  box.querySelector('input[type=text]').oninput = e => { CHAR.name = e.target.value; saveChar(); };
  box.insertAdjacentHTML('beforeend', wardrobeHTML()); bindWardrobe(box);
}
function saveChar() { try { localStorage.setItem('mirage_char', JSON.stringify(CHAR)); } catch (e) { } }
function charChanged(rerender = true) {
  if (CHAR.top === 'kandura' && CHAR.head === 'aucun' && rerender && !CHAR._kh) { CHAR.head = 'ghutra'; CHAR._kh = true; }
  saveChar(); rebuildPlayer(); P.model.position.copy(P.pos); P.model.rotation.set(0, P.yaw, 0);
  if (rerender) { const st = $('crOptions').scrollTop; renderCreator(); $('crOptions').scrollTop = st; }
}
$('crZoomFace').onclick = () => CAM.crZoom = 1; $('crZoomBody').onclick = () => CAM.crZoom = 0.3;
$('crRandom').onclick = () => { const n = CHAR.name; CHAR = { ...randomChar(), name: n }; charChanged(); };
let creatorEditing = false, savedPos = null;
function openCreator(editing) {
  creatorEditing = editing;
  if (P.vehicle) exitVehicle();
  savedPos = editing ? { pos: P.pos.clone(), yaw: P.yaw } : null;
  S.mode = 'creator'; document.exitPointerLock?.();
  $('creator').hidden = false; $('hud').hidden = true; $('touch').hidden = true;
  $('crSub').textContent = editing ? 'Modifie ton personnage' : 'Étape 1 — Crée et personnalise ton personnage';
  $('crPlay').textContent = editing ? 'Valider ✓' : 'Jouer ▶';
  P.yaw = 0; P.vel.set(0, 0, 0);
  pose(P.model, 'walk', 0, 0); P.model.rotation.set(0, 0, 0);
  renderCreator(); layoutCreatorCam();
  const cont = $('crContinue'); if (cont) cont.hidden = editing || !loadSave();
}
function layoutCreatorCam() {
  const W = innerWidth, H = innerHeight;
  if (S.mode === 'creator') {
    if (W > 720) camera.setViewOffset(W, H, -Math.min(210, W * 0.17), 0, W, H);
    else camera.setViewOffset(W, H, 0, H * 0.2, W, H);
  } else camera.clearViewOffset();
  camera.updateProjectionMatrix();
}
$('crPlay').onclick = () => {
  SFX.init();
  $('creator').hidden = true; $('hud').hidden = false; if (isTouch) $('touch').hidden = false;
  S.mode = 'play'; layoutCreatorCam();
  if (savedPos) { P.pos.copy(savedPos.pos); P.yaw = savedPos.yaw; }
  else { P.yaw = Math.PI; CAM.yaw = Math.PI; CAM.pitch = 0.18; toast(`Bienvenue à Mirage City${CHAR.name ? ', ' + CHAR.name : ''} ! 🌴`); setTimeout(() => toast('Tout est débloqué — ouvre le menu (☰ / Échap) pour le garage'), 1600); }
  if (!isTouch && !lockFailed) { try { const r = cv.requestPointerLock?.(); if (r && r.catch) r.catch(() => { lockFailed = true; }); } catch (err) { lockFailed = true; } }
};
