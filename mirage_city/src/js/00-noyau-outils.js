import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { BokehPass } from 'three/addons/postprocessing/BokehPass.js';
import { Sky } from 'three/addons/objects/Sky.js';
import { Lensflare, LensflareElement } from 'three/addons/objects/Lensflare.js';

/* =====================================================================
   OUTILS
   ===================================================================== */
const V3 = THREE.Vector3;
const rand = (a, b) => a + Math.random() * (b - a);
const pick = a => a[Math.floor(Math.random() * a.length)];
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const smooth = (a, b, x) => { const t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
const wrapA = a => { while (a > Math.PI) a -= 2 * Math.PI; while (a < -Math.PI) a += 2 * Math.PI; return a; };
const angleLerp = (a, b, t) => a + wrapA(b - a) * t;
const $ = id => document.getElementById(id);
const isTouch = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;

function coloredGeo(geo, color) {
  const c = new THREE.Color(color), n = geo.attributes.position.count, arr = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) { arr[i * 3] = c.r; arr[i * 3 + 1] = c.g; arr[i * 3 + 2] = c.b; }
  geo.setAttribute('color', new THREE.BufferAttribute(arr, 3));
  return geo;
}
/* Sac de géométries colorées fusionnées en un seul mesh (peu d'appels de dessin) */
class GeoBag {
  constructor() { this.g = []; }
  add(geo, color, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0) {
    if (!geo.index) geo.setIndex([...Array(geo.attributes.position.count).keys()]);
    if (rx) geo.rotateX(rx); if (ry) geo.rotateY(ry); if (rz) geo.rotateZ(rz);
    geo.translate(x, y, z); this.g.push(coloredGeo(geo, color)); return this;
  }
  box(w, h, d, c, x, y, z, rx, ry, rz) { return this.add(new THREE.BoxGeometry(w, h, d), c, x, y, z, rx, ry, rz); }
  geo() { return mergeGeometries(this.g); }
  mesh(mat) { const m = new THREE.Mesh(this.geo(), mat); m.castShadow = true; m.receiveShadow = true; return m; }
}
