/* =====================================================================
   DEMARRAGE
   ===================================================================== */
function placeStartVehicles() {
  const add = (t, x, z, yaw, col) => { const v = new Vehicle(t, x, z, yaw, col); v.spawned = false; return v; };
  add('supercar', 22, 64.5, Math.PI / 2, '#ff7a1a');
  add('hyper', -14, 64.5, Math.PI / 2);
  add('moto', 18, 74, 0, '#c8102e');
  add('heli', 120, 120, Math.PI, '#1c1c1e');
  add('heli', -452, -160, Math.PI / 2, '#f5f5f2').pos.y = 170;
  add('police', 66, 40, 0);
  add('limo', -455, -132, 0.3, '#f5f5f2'); add('taxi', -480, -128, 2.6);
  add('suv', 585, 66, Math.PI / 2, '#d9c7a1'); add('quad', 585, 50, Math.PI / 2, '#ff7a1a');
  add('jetski', -365, 110, -Math.PI / 2, '#f0bf62'); add('jetski', -365, 100, -Math.PI / 2, '#14b8c4');
  add('yacht', -395, -300, 0, '#0f2a4a');
  add('supercar', -268, -292, 0, '#14b8c4');
  const park = (spots, n) => { if (!spots) return; for (const sp of [...spots].sort(() => Math.random() - 0.5).slice(0, n)) add(pick(['sedan', 'sedan', 'suv', 'taxi', 'supercar', 'sedan']), sp.x, sp.z, Math.random() < 0.5 ? 0 : Math.PI); };
  park(publicSpots.parkDxb, 9); park(publicSpots.parkGva, 9); park(publicSpots.parkLac, 7);
  for (const sp of publicSpots.hospital || []) if (Math.random() < 0.25) add('ambulance', sp.x, sp.z, Math.PI);
  for (const sp of (publicSpots.police || []).slice(0, 6)) add('police', sp.x, sp.z, Math.PI);
  for (const sp of publicSpots.fire || []) add('firetruck', sp.x, sp.z, Math.PI);
  for (const sp of (publicSpots.poste || []).slice(0, 3)) add('van', sp.x, sp.z, Math.PI);
  for (const sp of publicSpots.bus || []) add('bus', sp.x, sp.z, 0);
  for (const sp of publicSpots.jets || []) add('jet', sp.x, sp.z, Math.PI / 2, pick(['#f4f4f4', '#1c1c1e', '#e2b13c']));
  for (const k in publicSpots) if (k.startsWith('farm')) add('tractor', publicSpots[k].x, publicSpots[k].z, Math.PI / 2);
  add('jetski', 75, LAKE_Z + 15, 0, '#c8102e'); add('heli', 260, 614, 0, '#c8102e').pos.y = 30;
  for (const v of vehicles) v.sync();
}
async function start() {
  await new Promise(r => setTimeout(r, 30));
  buildWorld(); buildMapCanvas();
  rebuildPlayer();
  $('loadTxt').textContent = 'Génération des matériaux PBR…'; await new Promise(r => setTimeout(r, 20));
  applyPBR(); buildPuddles();
  { const T = charTextures(), w = nm(T.weave, [8, 6]); CHAR_MAT.normalMap = w.normalMap; CHAR_MAT.normalScale = new THREE.Vector2(0.3, 0.3); CHAR_MAT.needsUpdate = true; }
  scene.traverse(o => { const m = o.material; if (m && m.isMeshStandardMaterial) ENV_MATS.add(m); }); ENV_MATS.add(CHAR_MAT);
  placeStartVehicles(); spawnTrams();
  setGfx(S.gfx, true); LOD.basePR = LOD.pr = renderer.getPixelRatio();
  $('crContinue').onclick = continueGame;
  $('btnPhone').onclick = () => togglePhone(); $('btnView').onclick = () => toggleFP();
  $('mapTp').onclick = () => { if (!S.waypoint) { toast('Place d\'abord un point sur la carte'); return; } teleport(S.waypoint.x, S.waypoint.z); closeMap(); clearWaypoint(); toast('✨ Téléporté'); };
  $('mapClr').onclick = () => { clearWaypoint(); drawBigMap(); };
  if (isTouch) $('tView').addEventListener('pointerdown', e => { e.preventDefault(); toggleFP(); });
  for (let i = 0; i < S.trafficN; i++) spawnTraffic(false);
  for (const v of vehicles) if (v.driver === 'ai' && Math.hypot(v.pos.x - P.pos.x, v.pos.z - P.pos.z) > 360) v.remove();
  for (let i = 0; i < S.pedN; i++) { const p = makePed(); respawnPedNear(p, P.pos); }
  setWeapon(1);
  if (isTouch) setupTouch(), $('touch').hidden = true;
  $('loading').hidden = true;
  openCreator(false);
  last = performance.now();
  requestAnimationFrame(frame);
  applyTime();
}
window.__THREE = THREE; window.__mirage = { camera, scene, cquery, heightAt, enterInterior, exitInterior, INTERIORS, openPhotoMode, closePhotoMode, PHOTO, saveGame, loadSave, continueGame, lightState, applyOutfit, recolorVehicle, addNeon, knock: knockPed, setGfx, setWaypoint, togglePhone, toggleFP, renderPhone, setCinema, renderer, S, P, vehicles, peds, teleport, spawnVehicleForPlayer, keys, CAM, setWeapon, togglePower, launchFireworks };
S.mode = 'loading';
start().catch(e => { $('loadTxt').textContent = 'Erreur : ' + e.message; console.error(e); });
