/* =====================================================================
   CIEL PHYSIQUE (diffusion atmosphérique) & NUAGES ANIMÉS
   ===================================================================== */
const physSky = new Sky();
physSky.scale.setScalar(4400);
physSky.material.uniforms.skyGain = { value: 0.55 };
physSky.material.fragmentShader = physSky.material.fragmentShader
  .replace('void main() {', 'uniform float skyGain;\nvoid main() {')
  .replace('#include <tonemapping_fragment>', 'gl_FragColor.rgb *= skyGain;\n#include <tonemapping_fragment>');
Object.assign(physSky.material.uniforms.turbidity, { value: 3.2 });
physSky.material.uniforms.rayleigh.value = 1.4; physSky.material.uniforms.mieCoefficient.value = 0.004; physSky.material.uniforms.mieDirectionalG.value = 0.86;
physSky.renderOrder = -2; physSky.frustumCulled = false; scene.add(physSky);
function updatePhysSky(dir, elev) {
  const use = (S.weather === 'clair' || S.weather === 'brume') && elev > -0.2;
  physSky.visible = use; sky.visible = !use;
  physSky.material.uniforms.sunPosition.value.copy(dir);
  physSky.material.uniforms.skyGain.value = S.weather === 'brume' ? 0.35 : 0.55;
  physSky.position.copy(camera.position);
}
const cloudMat = new THREE.ShaderMaterial({
  transparent: true, depthWrite: false, fog: false, side: THREE.DoubleSide,
  uniforms: { time: { value: 0 }, cover: { value: 0.42 }, alpha: { value: 0.85 }, lit: { value: new THREE.Color(1, 1, 1) }, shade: { value: new THREE.Color(0.6, 0.64, 0.7) }, camPos: { value: new V3() } },
  vertexShader: `varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position, 1.); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
  fragmentShader: `uniform float time, cover, alpha; uniform vec3 lit, shade, camPos; varying vec3 vW;
    float h(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
    float n(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f); return mix(mix(h(i), h(i + vec2(1, 0)), f.x), mix(h(i + vec2(0, 1)), h(i + vec2(1, 1)), f.x), f.y); }
    float fbm(vec2 p){ float v = 0., a = .5; for (int i = 0; i < 6; i++) { v += a * n(p); p = p * 2.03 + vec2(1.7, 9.2); a *= .5; } return v; }
    void main(){
      vec2 p = vW.xz * 0.0011 + vec2(time * 0.004, time * 0.0015);
      float d = fbm(p), c = smoothstep(1. - cover, 1. - cover + 0.22, d), thick = smoothstep(1. - cover + 0.05, 1.05, d);
      float fade = 1. - smoothstep(2200., 4200., length(vW.xz - camPos.xz));
      gl_FragColor = vec4(mix(lit, shade, thick * 0.85), c * alpha * fade);
    }`
});
const clouds = new THREE.Mesh(new THREE.PlaneGeometry(9000, 9000), cloudMat);
clouds.rotation.x = Math.PI / 2; clouds.position.y = 950; clouds.renderOrder = -1; clouds.frustumCulled = false; scene.add(clouds);
function updateClouds(time, day, set) {
  const u = cloudMat.uniforms, w = S.weather;
  u.time.value = time; u.camPos.value.copy(camera.position);
  clouds.position.x = camera.position.x; clouds.position.z = camera.position.z;
  clouds.visible = w !== 'sable';
  const cover = w === 'pluie' ? 0.9 : w === 'brume' ? 0.62 : 0.42;
  u.cover.value = lerp(u.cover.value, cover, 0.02);
  u.alpha.value = w === 'pluie' ? 0.95 : 0.85;
  u.lit.value.setRGB(1, 1, 1).lerp(new THREE.Color(1, 0.62, 0.42), set * 0.7).multiplyScalar(0.12 + 0.88 * day);
  u.shade.value.setRGB(0.55, 0.58, 0.64).multiplyScalar((w === 'pluie' ? 0.6 : 1) * (0.1 + 0.9 * day));
}
