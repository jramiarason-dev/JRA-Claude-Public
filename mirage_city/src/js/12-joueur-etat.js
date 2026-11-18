/* =====================================================================
   JOUEUR & ETAT
   ===================================================================== */
const S = {
  mode: 'loading', hour: 16.3, freezeTime: false, weather: 'clair', weapon: 1, slow: false, dynres: true, garage: {},
  powers: { superJump: false, superSpeed: false, slowmo: false, jetpack: false },
  trafficN: isTouch ? 18 : 32, pedN: isTouch ? 40 : 80, fwAuto: true,
  gfx: (() => { try { return localStorage.getItem('mirage_gfx') || (isTouch ? 'standard' : 'ultra'); } catch (e) { return isTouch ? 'standard' : 'ultra'; } })(), cinema: false, wet: 0, autoTuned: false, phone: false, photo: false, waypoint: null,
};
let CHAR = (() => { try { return { ...DEFAULT_CHAR, ...JSON.parse(localStorage.getItem('mirage_char') || '{}') }; } catch (e) { return { ...DEFAULT_CHAR }; } })();
const P = { pos: new V3(8, 0, 78), vel: new V3(), yaw: 0, onGround: true, vehicle: null, model: null, phase: 0, para: false, swim: false, fireCd: 0, aimT: 0, punchT: 0, prevJump: false, gun: null, jetMesh: null, chute: null };
const CAM = { yaw: Math.PI, pitch: 0.25, dist: 1, lastMouse: 0, shake: 0, fp: false, curDist: 5 };
function shake(a) { CAM.shake = Math.max(CAM.shake, a); }

function rebuildPlayer() {
  const parent = P.model ? P.model.parent : scene;
  if (P.model) { parent.remove(P.model); disposeChar(P.model); }
  P.model = buildCharacter(CHAR, true);
  // arme dans la main droite
  const gb = new GeoBag();
  P.gunGeos = {
    1: new GeoBag().box(0.04, 0.2, 0.05, '#222', 0, -0.15, 0.03).box(0.035, 0.05, 0.11, '#222', 0, -0.07, -0.01).geo(),
    2: new GeoBag().box(0.05, 0.55, 0.07, '#1d1f22', 0, -0.3, 0.04).box(0.05, 0.08, 0.16, '#1d1f22', 0, -0.07, -0.02).box(0.045, 0.2, 0.09, '#5a4632', 0, 0.05, 0.05).box(0.03, 0.12, 0.05, '#1d1f22', 0, -0.2, 0.09).geo(),
    3: new GeoBag().add(new THREE.CylinderGeometry(0.075, 0.075, 0.95, 10), '#4a5a3a', 0, -0.22, 0.09).add(new THREE.CylinderGeometry(0.095, 0.075, 0.14, 10), '#2d2d2d', 0, -0.7, 0.09).geo(),
    4: new GeoBag().add(new THREE.CylinderGeometry(0.06, 0.1, 0.45, 10), '#e05aa8', 0, -0.25, 0.04).box(0.05, 0.1, 0.08, '#f0bf62', 0, -0.05, 0).geo(),
  };
  P.gun = new THREE.Mesh(P.gunGeos[1], VC_MAT); P.gun.castShadow = true; P.model.userData.handR.add(P.gun);
  P.jetMesh = new GeoBag().box(0.42, 0.5, 0.18, '#7a828c', 0, 1.3, -0.24).add(new THREE.CylinderGeometry(0.08, 0.1, 0.3, 8), '#333', 0.12, 1.0, -0.26).add(new THREE.CylinderGeometry(0.08, 0.1, 0.3, 8), '#333', -0.12, 1.0, -0.26).mesh(VC_MAT);
  P.model.add(P.jetMesh);
  P.chute = new GeoBag().add(new THREE.SphereGeometry(3.2, 12, 6, 0, Math.PI * 2, 0, Math.PI / 2.6), '#ff7a1a', 0, 3.2, 0).geo();
  P.chute = new THREE.Mesh(P.chute, new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, roughness: 0.8 }));
  P.chute.position.y = 1.2; P.model.add(P.chute); P.jetMesh.visible = false; P.chute.visible = false;
  parent.add(P.model);
  updateGunMesh();
}
function updateGunMesh() {
  if (!P.gun) return; const w = S.weapon;
  P.gun.visible = w > 0; if (w > 0) P.gun.geometry = P.gunGeos[w];
}
