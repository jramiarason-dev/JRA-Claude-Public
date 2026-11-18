/* =====================================================================
   VÉGÉTATION : palmiers et arbres détaillés, herbe, vent
   ===================================================================== */
const WIND = { time: { value: 0 } };
function windMaterial(minY, scale, amp) {
  const m = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.75, side: THREE.DoubleSide });
  m.onBeforeCompile = (sh) => {
    sh.uniforms.uTime = WIND.time;
    sh.vertexShader = 'uniform float uTime;\n' + sh.vertexShader.replace('#include <begin_vertex>', `#include <begin_vertex>
      #ifdef USE_INSTANCING
        vec3 ip = vec3(instanceMatrix[3][0], instanceMatrix[3][1], instanceMatrix[3][2]);
      #else
        vec3 ip = vec3(0.0);
      #endif
      float sw = max(0.0, position.y - ${minY.toFixed(2)}) / ${scale.toFixed(2)};
      transformed.x += sin(uTime * 1.3 + ip.x * 0.07 + ip.z * 0.05) * ${amp.toFixed(3)} * sw * sw;
      transformed.z += cos(uTime * 1.05 + ip.z * 0.06 - ip.x * 0.03) * ${(amp * 0.7).toFixed(3)} * sw * sw;`);
  };
  return m;
}
const VEG_MAT = windMaterial(3.5, 6, 0.28), GRASS_BLADE_MAT = windMaterial(0.02, 0.5, 0.09);
function palmGeometry2() {
  const b = new GeoBag();
  const trunk = new THREE.CylinderGeometry(0.2, 0.36, 9.2, 9, 18);
  const p = trunk.attributes.position, col = [];
  for (let i = 0; i < p.count; i++) {
    const y = p.getY(i) + 4.6, ring = 1 + 0.08 * Math.max(0, Math.sin(y * 5.5)), x = p.getX(i) * ring, z = p.getZ(i) * ring;
    p.setXYZ(i, x + y * y * 0.008, y, z);
    const k = 0.75 + 0.25 * Math.max(0, Math.sin(y * 5.5)); col.push(0.52 * k, 0.4 * k, 0.27 * k);
  }
  trunk.computeVertexNormals(); trunk.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); trunk.setIndex(trunk.index); b.g.push(trunk);
  const top = [0.65, 9.2, 0];
  for (let k = 0; k < 12; k++) {
    const f = new THREE.PlaneGeometry(1.1, 4.8, 2, 8), fp = f.attributes.position, fc = [];
    for (let i = 0; i < fp.count; i++) {
      const w = fp.getX(i), t = fp.getY(i) / 4.8 + 0.5, width = Math.sin(Math.PI * Math.min(1, t * 1.15)) * 0.55 + 0.05;
      fp.setXYZ(i, t * 4.8, -t * t * (1.6 + (k % 3) * 0.4) - Math.abs(w) * 0.45, w * width * 2);
      const g = 0.55 + t * 0.35; fc.push(0.18 * g, 0.48 * g + 0.08, 0.16 * g);
    }
    f.computeVertexNormals(); f.setAttribute('color', new THREE.Float32BufferAttribute(fc, 3));
    f.rotateZ(0.35 - (k % 2) * 0.25); f.rotateY(k / 12 * Math.PI * 2 + (k % 2) * 0.2); f.translate(...top); b.g.push(f);
  }
  for (let i = 0; i < 5; i++) b.add(new THREE.SphereGeometry(0.2, 6, 4), 0x5b3a1e, top[0] + Math.cos(i * 1.3) * 0.28, 8.75, Math.sin(i * 1.3) * 0.28);
  return b.geo();
}
function treeGeometry2() {
  const b = new GeoBag();
  b.add(new THREE.CylinderGeometry(0.22, 0.42, 5.2, 8), 0x5e4029, 0, 2.6, 0);
  for (const [x, y, z, l] of [[0.9, 4.2, 0.2, 2.2], [-0.8, 4.4, -0.4, 2], [0.1, 4.6, 0.9, 1.8]]) b.add(new THREE.CylinderGeometry(0.08, 0.14, l, 6), 0x5e4029, x / 2, y, z / 2, z * 0.5, 0, -x * 0.5);
  const greens = [0x3c7a35, 0x4a8f40, 0x356d2e, 0x55993f, 0x2f6328];
  for (const [x, y, z, r] of [[0, 6.4, 0, 2.5], [1.5, 6.9, 0.4, 1.8], [-1.4, 6.6, -0.6, 1.9], [0.3, 7.8, -0.4, 1.7], [-0.4, 6.1, 1.4, 1.7], [0.6, 5.6, -1.3, 1.5]]) {
    const ico = new THREE.IcosahedronGeometry(r, 1), ip = ico.attributes.position;
    for (let i = 0; i < ip.count; i++) { const s = 1 + (hash2(Math.round(ip.getX(i) * 40), Math.round(ip.getY(i) * 40 + ip.getZ(i) * 13), 9) - 0.5) * 0.25; ip.setXYZ(i, ip.getX(i) * s, ip.getY(i) * s * 0.9, ip.getZ(i) * s); }
    ico.computeVertexNormals(); b.add(ico, pick(greens), x, y, z);
  }
  return b.geo();
}
let PALM_GEO2, TREE_GEO2;
const GRASS_CHUNKS = [];
function buildGrass() {
  const tuft = new GeoBag();
  for (let k = 0; k < 3; k++) { const g = new THREE.PlaneGeometry(0.12, 0.55, 1, 2), p = g.attributes.position; for (let i = 0; i < p.count; i++) { const y = p.getY(i) + 0.275; p.setXYZ(i, p.getX(i) * (1 - y / 0.6), y, (y * y) * 0.4); } g.computeVertexNormals(); tuft.add(g, k % 2 ? 0x5b9a3f : 0x4e8a37, 0, 0, 0, 0, k / 3 * Math.PI * 2 + 0.3); }
  const geo = tuft.geo(), CH = 70, cells = new Map();
  const put = (x, z) => { const k = Math.floor(x / CH) + ',' + Math.floor(z / CH); if (!cells.has(k)) cells.set(k, []); cells.get(k).push({ x, z, ry: rand(0, 6.28), s: rand(0.7, 1.4) }); };
  const N = isTouch ? 0.35 : 1;
  for (const pk of mapFeatures.parks) for (let i = 0; i < 700 * N; i++) put(pk.x + rand(-43, 43), pk.z + rand(-43, 43));
  for (let i = 0; i < 9000 * N; i++) { const x = rand(565, 1480), z = rand(565, 940); if (mapFeatures.fields.some(f => x > f.x0 && x < f.x1 && z > f.z0 && z < f.z1) || Math.abs(z - 780) < 8) continue; put(x, z); }
  for (const [k, list] of cells) {
    const im = instanced(geo, GRASS_BLADE_MAT, list, false); im.receiveShadow = true;
    const [cx, cz] = k.split(',').map(Number); GRASS_CHUNKS.push({ im, x: (cx + 0.5) * CH, z: (cz + 0.5) * CH });
  }
}
function updateVegetation(time) {
  WIND.time.value = time;
  const cp = camera.position;
  for (const c of GRASS_CHUNKS) c.im.visible = Math.abs(c.x - cp.x) < 260 && Math.abs(c.z - cp.z) < 260 && cp.y > -50;
}
