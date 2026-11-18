/* =====================================================================
   GARDE-ROBE (tenues enregistrées) & GARAGE PERSONNEL (peinture, néons)
   ===================================================================== */
const WARDROBE_KEY = 'mirage_wardrobe';
function loadWardrobe() { try { return JSON.parse(localStorage.getItem(WARDROBE_KEY) || '[]'); } catch (e) { return []; } }
function saveWardrobe(list) { try { localStorage.setItem(WARDROBE_KEY, JSON.stringify(list.slice(0, 8))); } catch (e) { } }
function wardrobeHTML() {
  const list = loadWardrobe();
  return `<div class="cr-sec">Garde-robe</div>
    <div class="cr-row"><label>Enregistre jusqu'à 8 tenues et change-en à tout moment (aussi depuis le téléphone).</label>
    <div class="seg"><button id="wdSave">💾 Enregistrer cette tenue</button></div>
    <div class="seg" style="margin-top:8px">${list.map((o, i) => `<button data-wd="${i}">👕 ${o._label || 'Tenue ' + (i + 1)}</button><button data-wdx="${i}" aria-label="Supprimer">✕</button>`).join('') || '<span style="color:var(--muted);font-size:13px">Aucune tenue enregistrée.</span>'}</div></div>`;
}
function bindWardrobe(box) {
  const sv = box.querySelector('#wdSave');
  if (sv) sv.onclick = () => { const list = loadWardrobe(); const o = { ...CHAR, _label: `${OPTS.top.find(t => t[0] === CHAR.top)?.[1] || 'Tenue'} ${list.length + 1}` }; list.push(o); saveWardrobe(list); toast('💾 Tenue enregistrée'); renderCreator(); };
  box.querySelectorAll('[data-wd]').forEach(b => b.onclick = () => applyOutfit(loadWardrobe()[+b.dataset.wd]));
  box.querySelectorAll('[data-wdx]').forEach(b => b.onclick = () => { const l = loadWardrobe(); l.splice(+b.dataset.wdx, 1); saveWardrobe(l); renderCreator(); });
}
function applyOutfit(o) {
  if (!o) return;
  const keep = { name: CHAR.name, body: CHAR.body, height: CHAR.height, build: CHAR.build, skin: CHAR.skin, eyes: CHAR.eyes, hair: CHAR.hair, hairColor: CHAR.hairColor, beard: CHAR.beard };
  CHAR = { ...DEFAULT_CHAR, ...o, ...keep }; delete CHAR._label;
  saveChar(); rebuildPlayer();
  if (S.mode === 'creator') { P.model.position.copy(P.pos); renderCreator(); }
  toast(`👕 ${o._label || 'Tenue'} enfilée`);
}

/* ---------- garage personnel */
const PAINTS = ['#f5f5f2', '#1c1c1e', '#c8102e', '#2a6fdb', '#ff7a1a', '#14b8c4', '#e2b13c', '#6d3fc0', '#0a7d3b', '#9aa1ab', '#e05aa8', '#7a1f2b'];
const NEONS = [null, '#ff2fa0', '#2ec5ff', '#5ad45a', '#f0bf62', '#b18cff'];
function addNeon(v, color) {
  if (v.neon) { v.group.remove(v.neon); v.neon.geometry.dispose(); v.neon = null; }
  v.neonColor = color; if (!color) return;
  const g = new THREE.PlaneGeometry(1, 1); g.rotateX(-Math.PI / 2);
  const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ map: POOL_TEX, color, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false }));
  const s = v.def.r * 1.6; m.scale.set(s * 0.75, 1, s * 1.3); m.position.y = 0.08; v.group.add(m); v.neon = m;
}
function recolorVehicle(v, color) {
  const old = v.group, b = buildVehicleMesh(v.type, color);
  b.group.position.copy(old.position); b.group.rotation.copy(old.rotation);
  if (P.model && P.model.parent === old) { old.remove(P.model); b.group.add(P.model); }
  scene.remove(old); old.traverse(o => { if (o.geometry && o.geometry !== WHEEL_GEO) o.geometry.dispose(); });
  Object.assign(v, b); v.color = color; ENV_MATS.add(v.mat); v.mat.envMapIntensity = envLevel; scene.add(v.group);
  const nc = v.neonColor; v.neon = null; if (nc) addNeon(v, nc);
}
function rememberGarage(v) { S.garage[v.type] = { color: v.color, neon: v.neonColor || null }; }
