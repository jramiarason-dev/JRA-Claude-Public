/* =====================================================================
   VIE URBAINE : feux synchronisés, clignotants, feux stop, arrêts de bus
   ===================================================================== */
// Cycle des feux : la circulation sur l'axe nord-sud (z) et l'axe est-ouest (x) alternent.
const TL = { t: 0, cycle: 26 };
function lightState(axis) {
  const t = TL.t % TL.cycle;
  if (axis === 'z') return t < 11 ? 'g' : t < 13 ? 'y' : 'r';
  return t < 13 ? 'r' : t < 24 ? 'g' : 'y';
}
const TL_BAGS = {}, TL_MATS = {};
function tlBag(axis, col) { const k = axis + col; return TL_BAGS[k] || (TL_BAGS[k] = new GeoBag()); }
function buildTrafficLightMeshes() {
  for (const k in TL_BAGS) {
    const mat = TL_MATS[k] = new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false });
    const m = TL_BAGS[k].mesh(mat); m.castShadow = false; scene.add(m);
  }
}
function updateTrafficLights(dt, night) {
  TL.t += dt;
  const on = 1.3 + night * 2.4, off = 0.1;
  for (const axis of ['x', 'z']) { const st = lightState(axis); for (const c of ['r', 'y', 'g']) { const m = TL_MATS[axis + c]; if (m) m.color.setScalar(st === c ? on : off); } }
}
const BUS_STOPS = [];

/* ---------- détails dynamiques des véhicules : clignotants, feux stop, phares, habitacle */
const headL = new THREE.SpotLight(0xfff1d6, 0, 70, 0.55, 0.6, 1.2), headR = headL.clone();
const headTarget = new THREE.Object3D();
scene.add(headL, headR, headTarget); headL.target = headTarget; headR.target = headTarget;
function vehicleExtras(v, time, night) {
  if (v.blink) {
    const on = Math.floor(time * 3) % 2 === 0;
    for (const s of ['L', 'R']) for (const m of v.blink[s]) m.visible = on && v.blinkSide === s;
  }
  if (v.brakeMesh) v.brakeMesh.visible = !!v.braking;
  if (v.revMesh) v.revMesh.visible = v.speed < -0.5;
  if (v.cabin) { v.cabin.visible = v === P.vehicle && CAM.fp; if (v.wheelSteer && v === P.vehicle) v.wheelSteer.rotation.z = lerp(v.wheelSteer.rotation.z, -inp.side * 1.6, 0.25); }
}
function updateHeadlights(night) {
  const v = P.vehicle;
  const on = v && night > 0.35 && v.def.kind !== 'heli' && v.def.kind !== 'boat';
  headL.intensity = headR.intensity = on ? (CAM.fp ? 260 : 420) * night : 0;
  if (!on) return;
  const f = v.fwd, r = new V3(-f.z, 0, f.x);
  headL.position.copy(v.pos).addScaledVector(f, 2.2).addScaledVector(r, 0.7).setY(v.pos.y + 0.9);
  headR.position.copy(v.pos).addScaledVector(f, 2.2).addScaledVector(r, -0.7).setY(v.pos.y + 0.9);
  headTarget.position.copy(v.pos).addScaledVector(f, 22).setY(v.pos.y);
}
