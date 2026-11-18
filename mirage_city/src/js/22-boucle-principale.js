/* =====================================================================
   BOUCLE PRINCIPALE
   ===================================================================== */
let last = performance.now(), time = 0, fwTimer = 8, hudT = 0;
function frame(now) {
  requestAnimationFrame(frame);
  const realDt = Math.min((now - last) / 1000, 0.25); let dt = Math.min(realDt, 0.05); last = now;
  if (S.mode === 'loading') return;
  if (S.powers.slowmo && S.mode === 'play') dt *= 0.35;
  time += dt;
  if (S.mode === 'play') {
    readInput();
    if (!S.freezeTime) S.hour = (S.hour + dt / 50) % 24;
    if (P.vehicle) updatePlayerVehicle(dt); else updatePlayerFoot(dt);
    if (S.weapon >= 0) { P.fireCd -= dt; const w = WEAPONS[S.weapon]; if ((w.auto ? inp.fire : inp.firePressed) && P.fireCd <= 0) { P.fireCd = w.rate; fireWeapon(); } }
    for (const v of vehicles) {
      if (v === P.vehicle) continue;
      if (v.loose) looseVehicle(v, dt);
      else if (v.driver === 'ai') driveVehicle(v, aiControl(v, dt), dt);
      else if (v.driver === 'tram') updateTram(v, dt);
      else if (v.come && !v.come.heli) { const c = comeControl(v, dt); driveVehicle(v, c || { thr: 0, steer: 0, brake: true }, dt); }
      else if (v.come && v.come.heli) { comeControl(v, dt); driveHeli(v, { thr: 0, steer: 0 }, dt); }
      else if (v.def.kind === 'heli') driveHeli(v, { thr: 0, steer: 0 }, dt);
      else if (Math.abs(v.speed) > 0.05 || v.air) driveVehicle(v, { thr: 0, steer: 0, brake: true }, dt);
      if (v.burn > 0) { v.burn -= dt; if (Math.random() < 0.3) emit(v.pos.x + rand(-1, 1), v.pos.y + 1.5, v.pos.z + rand(-1, 1), rand(-0.5, 0.5), rand(2, 4), rand(-0.5, 0.5), 2, rand(0.8, 1.6), pick(['#333', '#555', '#ff7a1a']), -0.05, 0.5); if (v.burn <= 0) { v.mat.color.set(0xffffff); v.hp = 10; } }
      v.sync();
    }
    if (P.vehicle) P.vehicle.sync();
    updatePeds(dt);
    updateRockets(dt);
    managePopulation(dt);
    const night = applyTime();
    if (S.fwAuto && night > 0.7) { fwTimer -= dt; if (fwTimer <= 0) { fwTimer = rand(25, 45); launchFireworks(10); } }
    hudT -= dt; if (hudT <= 0) { hudT = 0.1; updateHUD(); }
  } else if (S.mode === 'creator') {
    P.model.position.copy(P.pos); P.model.rotation.set(0, P.yaw, 0);
    pose(P.model, 'walk', 0, 0);
    applyTime();
  } else applyTime();
  const nightNow = 1 - smooth(-0.06, 0.2, Math.sin((S.hour - 6) / 12 * Math.PI));
  if (S.mode === 'play') { updateTrafficLights(dt, nightNow); updateInteriors(dt); autoSave(dt); }
  if (S.mode === 'photo') applyPhotoPose();
  for (const v of vehicles) vehicleExtras(v, time, nightNow);
  updateHeadlights(nightNow); updateVegetation(time); updateLOD(dt, realDt);
  updateWeatherFX(dt); autoTune(realDt);
  updateFireworks(dt); updateFountain(dt, time); if (S.mode !== 'loading') updateGeneva(dt, time); updateParticles(dt);
  updateBarriers(dt); updateFlags(time); for (const t of ARENA_LED) t.offset.x += dt * 0.08;
  WATER_NORMALS.offset.x += dt * 0.012; WATER_NORMALS.offset.y += dt * 0.007;
  for (const v of vehicles) v.group.visible = v === P.vehicle || Math.abs(v.pos.x - camera.position.x) + Math.abs(v.pos.z - camera.position.z) < 750;
  updateCamera(dt);
  sky.position.copy(camera.position); stars.position.copy(camera.position);
  if (S.mode === 'play' || S.mode === 'creator') drawMinimap();
  if (S.mode === 'photo' && bokehPass) { bokehPass.enabled = PHOTO.dof; bokehPass.uniforms.focus.value = camera.position.distanceTo(P.pos) + 0.5; }
  updateWaypoint(time);
  $('crosshair').classList.toggle('fp', CAM.fp);
  if (S.phone && Math.floor(time) !== frame._ps) { frame._ps = Math.floor(time); const h = S.hour; $('phClock').textContent = `${String(Math.floor(h)).padStart(2, '0')}:${String(Math.floor((h % 1) * 60)).padStart(2, '0')}`; }
  renderFrame(time, 1 - smooth(-0.06, 0.2, Math.sin((S.hour - 6) / 12 * Math.PI)));
}

addEventListener('resize', () => { renderer.setSize(innerWidth, innerHeight); if (composer) { composer.setSize(innerWidth, innerHeight); bloomPass.resolution.set(innerWidth / 2, innerHeight / 2); } camera.aspect = innerWidth / innerHeight; layoutCreatorCam(); });
