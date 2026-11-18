/* =====================================================================
   GESTION DE LA POPULATION
   ===================================================================== */
let popT = 0;
function managePopulation(dt) {
  popT -= dt; if (popT > 0) return; popT = 0.4;
  const pp = P.vehicle ? P.vehicle.pos : P.pos;
  // retirer les voitures de circulation trop loin
  for (const v of [...vehicles]) {
    if (v === P.vehicle || !v.fromTraffic) continue;
    const d = Math.hypot(v.pos.x - pp.x, v.pos.z - pp.z);
    if (d > (v.driver === 'ai' ? 360 : 450)) v.remove();
  }
  const ai = vehicles.filter(v => v.driver === 'ai').length;
  if (ai < S.trafficN) for (let i = 0; i < Math.min(3, S.trafficN - ai); i++) spawnTraffic(true);
  else if (ai > S.trafficN) { const v = vehicles.find(v => v.driver === 'ai'); v?.remove(); }
  while (peds.length < S.pedN) { const p = makePed(); respawnPedNear(p, pp); }
  while (peds.length > S.pedN) { const p = peds.pop(); scene.remove(p.model); disposeChar(p.model); }
}
