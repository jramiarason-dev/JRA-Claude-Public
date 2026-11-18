/* =====================================================================
   HEURE, METEO
   ===================================================================== */
const C = (h) => new THREE.Color(h);
const SKY = { dayT: C(0x3f8fe0), dayB: C(0xf3dcb4), setT: C(0x2c3d78), setB: C(0xff9a52), nightT: C(0x070c1c), nightB: C(0x1d2a4f) };
const _top = new THREE.Color(), _bot = new THREE.Color();
function applyTime() {
  const h = S.hour, ang = (h - 6) / 12 * Math.PI, elev = Math.sin(ang);
  const dir = new V3(Math.cos(ang) * 0.85, elev, -0.42).normalize();
  const day = smooth(-0.12, 0.3, elev);
  const set = clamp(1 - Math.abs(elev) / 0.38, 0, 1) * (elev > -0.25 ? 1 : 0);
  _top.copy(SKY.nightT).lerp(SKY.dayT, day).lerp(SKY.setT, set * 0.55);
  _bot.copy(SKY.nightB).lerp(SKY.dayB, day).lerp(SKY.setB, set * 0.8);
  const nf = 1 - smooth(-0.06, 0.2, elev);
  let fogC = _bot.clone(), near = lerp(350, 40, nf * 0.85), far = lerp(2600, 1100, nf * 0.85);
  if (nf > 0) fogC.lerp(new THREE.Color(0x1c2233), nf * 0.6);
  if (S.weather === 'sable') { fogC = new THREE.Color(0xc9a46a).multiplyScalar(0.35 + 0.65 * day); _top.copy(fogC); _bot.copy(fogC); near = 4; far = 150; }
  else if (S.weather === 'pluie') { fogC.lerp(new THREE.Color(0x7d848e).multiplyScalar(0.18 + 0.82 * day), 0.75); _top.lerp(fogC, 0.8); _bot.copy(fogC); near = 15; far = 700; }
  else if (S.weather === 'brume') { fogC.lerp(new THREE.Color(0xd9d4c8).multiplyScalar(0.3 + 0.7 * day), 0.6); _top.lerp(fogC, 0.6); _bot.copy(fogC); near = 40; far = 520; }
  skyMat.uniforms.top.value.copy(_top); skyMat.uniforms.bottom.value.copy(_bot);
  updatePhysSky(dir, elev); updateClouds(performance.now() / 1000, day, set);
  skyMat.uniforms.sunDir.value.copy(elev > -0.1 ? dir : dir.clone().negate());
  skyMat.uniforms.sunCol.value.set(elev > -0.1 ? 0xffd7a0 : 0x8899cc).multiplyScalar(S.weather === 'clair' ? 1 : 0.2);
  scene.fog.color.copy(fogC); scene.fog.near = near; scene.fog.far = far;
  const pp = P.vehicle ? P.vehicle.pos : P.pos;
  const ldir = elev > -0.05 ? dir : new V3(-dir.x, Math.max(0.35, -elev), -dir.z).normalize();
  sun.position.copy(pp).addScaledVector(ldir, 400); sun.target.position.copy(pp);
  sun.color.set(elev > -0.05 ? 0xffe2b8 : 0x9fb3ff).lerp(new THREE.Color(0xff9a52), set * 0.6);
  sun.intensity = (elev > -0.05 ? 0.4 + 2.6 * day : 0.3) * (S.weather === 'pluie' ? 0.35 : 1);
  lensflare.visible = S.weather === 'clair' && elev > 0.02;
  hemi.intensity = 0.22 + 0.43 * day;
  const envI = 0.18 + 0.62 * day; if (Math.abs(envI - envLevel) > 0.02) { envLevel = envI; for (const m of ENV_MATS) m.envMapIntensity = envI; } hemi.color.set(0x8193cc).lerp(new THREE.Color(0xe4f0ff), day); hemi.groundColor.set(0x3a3428).lerp(new THREE.Color(0xc9a77a), day);
  const night = 1 - smooth(-0.06, 0.2, elev);
  for (const m of BMATS) m.emissiveIntensity = night * 1.1;
  SIGN_MAT.emissiveIntensity = night * 0.9;
  WHITE_MAT.emissiveIntensity = night * 0.35; GOLD_MAT.emissiveIntensity = night * 0.8;
  LAMP_MAT.emissiveIntensity = night > 0.4 ? 2.4 : 0;
  LIGHT_MAT.color.setScalar(1 + night * 2.2); SHOPWIN_MAT.emissiveIntensity = 0.25 + night * 1.25; POOL_MAT.opacity = night > 0.35 ? night * 0.5 : 0;
  stars.material.opacity = S.weather === 'clair' ? clamp(night * 1.3 - 0.3, 0, 1) : 0;
  renderer.toneMappingExposure = 0.85 + 0.25 * day;
  const hh = Math.floor(h), mm = Math.floor((h - hh) * 60);
  $('clock').textContent = `${S.weather === 'sable' ? '🌪️' : S.weather === 'pluie' ? '🌧️' : S.weather === 'brume' ? '🌫️' : elev > 0 ? '☀️' : '🌙'} ${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}`;
  return night;
}
