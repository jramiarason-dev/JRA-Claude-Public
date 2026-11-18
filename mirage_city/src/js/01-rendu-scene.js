/* =====================================================================
   RENDU & SCENE
   ===================================================================== */
const renderer = new THREE.WebGLRenderer({ antialias: !isTouch, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(devicePixelRatio, isTouch ? 1.25 : 1.6));
renderer.setSize(innerWidth, innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
$('game').appendChild(renderer.domElement);

const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
const ENV_MATS = new Set(); let envLevel = 0.6;
scene.fog = new THREE.Fog(0xf0c89a, 300, 1900);
const camera = new THREE.PerspectiveCamera(65, innerWidth / innerHeight, 0.3, 5000);

const hemi = new THREE.HemisphereLight(0xcfe6ff, 0xc9a77a, 0.7);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xffe2b8, 2.6);
sun.castShadow = true;
sun.shadow.mapSize.set(isTouch ? 1024 : 2048, isTouch ? 1024 : 2048);
const SH = 70;
Object.assign(sun.shadow.camera, { left: -SH, right: SH, top: SH, bottom: -SH, near: 10, far: 900 });
sun.shadow.bias = -0.0005; sun.shadow.normalBias = 0.4;
scene.add(sun, sun.target);
const flash = new THREE.PointLight(0xffa040, 0, 80, 1.6);
const rimLight = new THREE.DirectionalLight(0xcfe0ff, 0), keyLight = new THREE.DirectionalLight(0xfff2e0, 0);
scene.add(rimLight, rimLight.target, keyLight, keyLight.target);
scene.add(flash);

/* Ciel en dégradé + soleil */
const skyMat = new THREE.ShaderMaterial({
  side: THREE.BackSide, depthWrite: false, fog: false,
  uniforms: { top: { value: new THREE.Color() }, bottom: { value: new THREE.Color() }, sunDir: { value: new V3(0, 1, 0) }, sunCol: { value: new THREE.Color(1, .8, .5) } },
  vertexShader: `varying vec3 vW; void main(){ vW = position; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
  fragmentShader: `varying vec3 vW; uniform vec3 top,bottom,sunDir,sunCol;
    void main(){ vec3 d=normalize(vW); float h=max(d.y,0.); vec3 c=mix(bottom,top,pow(h,.55));
      float s=max(dot(d,sunDir),0.); c+=sunCol*(pow(s,600.)*4.+pow(s,10.)*.25);
      if(d.y<0.) c=bottom; gl_FragColor=vec4(c,1.); }`
});
const sky = new THREE.Mesh(new THREE.SphereGeometry(3000, 24, 16), skyMat);
sky.renderOrder = -1; scene.add(sky);
const starGeo = new THREE.BufferGeometry(); {
  const a = []; for (let i = 0; i < 900; i++) { const v = new V3(rand(-1, 1), rand(0.05, 1), rand(-1, 1)).normalize().multiplyScalar(2800); a.push(v.x, v.y, v.z); }
  starGeo.setAttribute('position', new THREE.Float32BufferAttribute(a, 3));
}
const stars = new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xffffff, size: 3, sizeAttenuation: false, transparent: true, opacity: 0, fog: false, depthWrite: false }));
scene.add(stars);
