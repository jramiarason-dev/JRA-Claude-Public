/* =====================================================================
   PARTICULES
   ===================================================================== */
const PMAX = 4200;
const pMesh = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({ toneMapped: false }), PMAX);
pMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage); pMesh.frustumCulled = false;
pMesh.setColorAt(0, new THREE.Color(1, 1, 1));
const PA = { x: new Float32Array(PMAX), y: new Float32Array(PMAX), z: new Float32Array(PMAX), vx: new Float32Array(PMAX), vy: new Float32Array(PMAX), vz: new Float32Array(PMAX), life: new Float32Array(PMAX), max: new Float32Array(PMAX), size: new Float32Array(PMAX), grav: new Float32Array(PMAX), drag: new Float32Array(PMAX) };
{ const a = pMesh.instanceMatrix.array; for (let i = 0; i < PMAX; i++) { a.fill(0, i * 16, i * 16 + 16); a[i * 16 + 15] = 1; } }
scene.add(pMesh);
let pNext = 0;
const _c = new THREE.Color();
function emit(x, y, z, vx, vy, vz, life, size, color, grav = 1, drag = 0) {
  const i = pNext; pNext = (pNext + 1) % PMAX;
  PA.x[i] = x; PA.y[i] = y; PA.z[i] = z; PA.vx[i] = vx; PA.vy[i] = vy; PA.vz[i] = vz; PA.life[i] = PA.max[i] = life; PA.size[i] = size; PA.grav[i] = grav; PA.drag[i] = drag;
  _c.set(color); pMesh.setColorAt(i, _c); pMesh.instanceColor.needsUpdate = true;
}
function updateParticles(dt) {
  const a = pMesh.instanceMatrix.array;
  for (let i = 0; i < PMAX; i++) {
    if (PA.life[i] <= 0) { if (a[i * 16] !== 0) { a[i * 16] = a[i * 16 + 5] = a[i * 16 + 10] = 0; } continue; }
    PA.life[i] -= dt;
    PA.vy[i] -= G * PA.grav[i] * dt;
    if (PA.drag[i]) { const k = 1 - PA.drag[i] * dt; PA.vx[i] *= k; PA.vy[i] *= k; PA.vz[i] *= k; }
    PA.x[i] += PA.vx[i] * dt; PA.y[i] += PA.vy[i] * dt; PA.z[i] += PA.vz[i] * dt;
    const s = PA.life[i] > 0 ? PA.size[i] * (0.3 + 0.7 * PA.life[i] / PA.max[i]) : 0, o = i * 16;
    a[o] = a[o + 5] = a[o + 10] = s; a[o + 12] = PA.x[i]; a[o + 13] = PA.y[i]; a[o + 14] = PA.z[i];
  }
  pMesh.instanceMatrix.needsUpdate = true;
}
