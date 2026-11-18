/* =====================================================================
   TEXTURES
   ===================================================================== */
function canvasTex(w, h, draw, rep = true) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; }
  t.anisotropy = 4; return t;
}
/* Façades : 3 styles (grille, bandes verticales, bandes horizontales) */
function facadeTex(style, emissive) {
  return canvasTex(128, 128, (g, w, h) => {
    g.fillStyle = emissive ? '#000' : '#f2f2f2'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
      let x = i * 32 + 4, y = j * 32 + 5, ww = 24, hh = 20;
      if (style === 1) { y = j * 32 + 1; hh = 30; ww = 26; x = i * 32 + 3; }
      if (style === 2) { x = i * 32; ww = 32; y = j * 32 + 8; hh = 18; }
      if (emissive) {
        const r = Math.random(); g.fillStyle = r < 0.45 ? '#000' : r < 0.85 ? '#ffd38a' : r < 0.95 ? '#fff4d6' : '#9fd6ff';
      } else g.fillStyle = `rgb(${70 + Math.random() * 25},${90 + Math.random() * 25},${115 + Math.random() * 30})`;
      g.fillRect(x, y, ww, hh);
    }
  });
}
const FACADES = [0, 1, 2].map(s => ({ map: facadeTex(s, false), em: facadeTex(s, true) }));
const BCOLORS = [0xe9eef3, 0xbcd6e6, 0x8fb6cf, 0xd8c7a8, 0xf0e6d2, 0x9fb7c4, 0xcfd8dc, 0xe2c08a, 0x7fa3b8, 0xc0c8d4];
const BMATS = [];
for (let i = 0; i < 12; i++) {
  const f = FACADES[i % 3];
  BMATS.push(new THREE.MeshStandardMaterial({ color: BCOLORS[i % BCOLORS.length], map: f.map, emissiveMap: f.em, emissive: 0xffe0b0, emissiveIntensity: 0, roughness: 0.22, metalness: 0.45 }));
}
const GOLD_MAT = new THREE.MeshStandardMaterial({ color: 0xe8b84a, metalness: 0.3, roughness: 0.35, emissive: 0x3a2500, emissiveIntensity: 0 });
const WHITE_MAT = new THREE.MeshStandardMaterial({ color: 0xf4f4f2, roughness: 0.5, emissive: 0x6a4cff, emissiveIntensity: 0 });
const STONE_MAT = new THREE.MeshStandardMaterial({ color: 0xe6dcc8, roughness: 0.8 });
const VC_MAT = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.8 });
const WATER_NORMALS = (() => {
  const N = 128, c = document.createElement('canvas'); c.width = c.height = N; const g = c.getContext('2d'), img = g.createImageData(N, N);
  const W = [[3, 1, 0.5], [1, 4, 0.35], [5, -2, 0.25], [-2, 7, 0.15]];
  const h = (x, y) => W.reduce((a, [kx, ky, amp]) => a + amp * Math.sin(2 * Math.PI * (kx * x + ky * y) / N), 0);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const dx = h(x + 1, y) - h(x - 1, y), dy = h(x, y + 1) - h(x, y - 1), n = new THREE.Vector3(-dx * 3, -dy * 3, 1).normalize(), o = (y * N + x) * 4;
    img.data[o] = (n.x * 0.5 + 0.5) * 255; img.data[o + 1] = (n.y * 0.5 + 0.5) * 255; img.data[o + 2] = (n.z * 0.5 + 0.5) * 255; img.data[o + 3] = 255;
  }
  g.putImageData(img, 0, 0); const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(120, 120); return t;
})();
const WATER_MAT = new THREE.MeshStandardMaterial({ color: 0x1b8fb3, roughness: 0.08, metalness: 0.35, transparent: true, opacity: 0.93, normalMap: WATER_NORMALS, normalScale: new THREE.Vector2(0.5, 0.5) });

const roadTex = canvasTex(64, 128, (g, w, h) => {
  g.fillStyle = '#44454b'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 400; i++) { g.fillStyle = `rgba(255,255,255,${Math.random() * 0.05})`; g.fillRect(Math.random() * w, Math.random() * h, 1, 1); }
  g.fillStyle = '#e8b23a'; g.fillRect(2, 0, 2, h); g.fillRect(w - 4, 0, 2, h);
  g.fillStyle = '#f2f2f2'; g.fillRect(w / 2 - 1.5, 0, 3, h * 0.55);
});
function scaleBoxUV(g, w, h, d, tw = 15, th = 13) {
  const uv = g.attributes.uv, sx = [d, d, 0, 0, w, w];
  for (let f = 0; f < 6; f++) for (let k = 0; k < 4; k++) {
    const i = f * 4 + k;
    if (f === 2 || f === 3) uv.setXY(i, 0.01, 0.01); else uv.setXY(i, uv.getX(i) * sx[f] / tw, uv.getY(i) * h / th);
  }
}
function scaleCylUV(g, r, h, rs, tw = 15, th = 13) {
  const uv = g.attributes.uv, torso = (1 + 1) * (rs + 1);
  for (let i = 0; i < uv.count; i++) {
    if (i < torso) uv.setXY(i, uv.getX(i) * 2 * Math.PI * r / tw, uv.getY(i) * h / th); else uv.setXY(i, 0.01, 0.01);
  }
}
