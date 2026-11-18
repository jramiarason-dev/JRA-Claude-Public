/* =====================================================================
   MONDE : constantes & terrain
   ===================================================================== */
const ROADS_X = [-300, -180, -60, 60, 180, 300, 420, 540];
const ROADS_Z = [-540, -420, -300, -180, -60, 60, 180, 300, 420, 540, 660, 780, 900];
const BLOCKS_X = [-240, -120, 0, 120, 240, 360, 480];
const BLOCKS_Z = [-480, -360, -240, -120, 0, 120, 240, 360, 480, 600, 720, 840];
const GVA_Z = 552, LAKE_Z = 945;
const ROAD_W = 18, LANE = 4.5, SIDEW = 12;
const SHORE = -340, WATER_Y = -0.45, G = 28;
const HWY_Z = 60;
const PALM_C = { x: -640, z: 261 };
const FRONDS = [-3, -2, -1, 0, 1, 2, 3].map(k => Math.PI + k * 0.38);
const BOUNDS = { x0: -1300, x1: 1500, z0: -1000, z1: 1300 };

function inORect(x, z, sx, sz, ang, len, w) {
  const dx = x - sx, dz = z - sz, c = Math.cos(ang), s = Math.sin(ang);
  const lx = dx * c + dz * s, lz = -dx * s + dz * c;
  return lx >= 0 && lx <= len && Math.abs(lz) <= w / 2;
}
function onIsland(x, z) {
  if (Math.hypot(x + 470, z + 160) < 38) return true;                    // île de l'hôtel Voile
  if (x > -442 && x < -340 && z > -167 && z < -153) return true;          // pont
  if (x > -585 && x < -340 && z > 250 && z < 272) return true;            // tronc de l'île Palmier
  const dx = x - PALM_C.x, dz = z - PALM_C.z, d = Math.hypot(dx, dz);
  if (d < 55) return true;
  if (d > 212 && d < 230) { const a = Math.atan2(dz, dx); if (Math.abs(wrapA(a - Math.PI)) < 1.9) return true; }
  for (const a of FRONDS) if (inORect(x, z, PALM_C.x, PALM_C.z, a, 175, 16)) return true;
  return false;
}
function isWater(x, z) {
  if (x >= SHORE) return z > LAKE_Z || Math.hypot(x, z - 120) < 30 || Math.hypot(x - 900, z + 220) < 28;
  return !onIsland(x, z);
}
function duneH(x, z) {
  if (x < 560) return 0;
  const t = airportMask(x, z) * smooth(560, 720, x) * (1 - smooth(470, 552, z)) * smooth(14, 46, Math.abs(z - HWY_Z)) * smooth(40, 95, Math.hypot(x - 900, z + 220));
  if (t <= 0) return 0;
  const h = 7 + 5 * Math.sin(x * 0.019 + 0.5) * Math.cos(z * 0.016) + 3 * Math.sin(x * 0.047 + z * 0.031) + 2 * Math.cos(z * 0.06 - x * 0.012);
  return Math.max(0, h) * t;
}
const surfaceY = (x, z) => isWater(x, z) ? WATER_Y : duneH(x, z);

/* ---------- Collisions (grille spatiale) */
const colliders = [], cgrid = new Map(), CELL = 50, EMPTY = [];
const ckey = (i, j) => i * 100003 + j;
function addCollider(c) {
  if (c.t === 'cyl') { c.x0 = c.x - c.r; c.x1 = c.x + c.r; c.z0 = c.z - c.r; c.z1 = c.z + c.r; }
  colliders.push(c);
  const m = 6;
  for (let i = Math.floor((c.x0 - m) / CELL); i <= Math.floor((c.x1 + m) / CELL); i++)
    for (let j = Math.floor((c.z0 - m) / CELL); j <= Math.floor((c.z1 + m) / CELL); j++) {
      const k = ckey(i, j); if (!cgrid.has(k)) cgrid.set(k, []); cgrid.get(k).push(c);
    }
}
const cquery = (x, z) => cgrid.get(ckey(Math.floor(x / CELL), Math.floor(z / CELL))) || EMPTY;
function insideXZ(c, x, z) {
  if (c.t === 'cyl') { const dx = x - c.x, dz = z - c.z; return dx * dx + dz * dz <= c.r * c.r; }
  return x >= c.x0 && x <= c.x1 && z >= c.z0 && z <= c.z1;
}
function heightAt(x, z, y) {
  let h = y < -50 ? -1e9 : surfaceY(x, z);
  for (const c of cquery(x, z)) if (c.y1 <= y + 0.8 && c.y1 > h && insideXZ(c, x, z)) h = c.y1;
  return h;
}
function collide(p, r, hgt) {
  let hit = null;
  for (const c of cquery(p.x, p.z)) {
    if (c.floor || p.y + hgt <= c.y0 || p.y >= c.y1 - 0.05) continue;
    if (c.t === 'cyl') {
      const dx = p.x - c.x, dz = p.z - c.z, d = Math.hypot(dx, dz), m = c.r + r;
      if (d < m && d > 1e-4) { p.x = c.x + dx / d * m; p.z = c.z + dz / d * m; hit = { x: dx / d, z: dz / d }; }
    } else {
      const cx = clamp(p.x, c.x0, c.x1), cz = clamp(p.z, c.z0, c.z1), dx = p.x - cx, dz = p.z - cz, d = Math.hypot(dx, dz);
      if (d < r) {
        if (d > 1e-4) { p.x = cx + dx / d * r; p.z = cz + dz / d * r; hit = { x: dx / d, z: dz / d }; }
        else {
          const l = p.x - c.x0, rr = c.x1 - p.x, b = p.z - c.z0, f = c.z1 - p.z, mn = Math.min(l, rr, b, f);
          if (mn === l) { p.x = c.x0 - r; hit = { x: -1, z: 0 }; } else if (mn === rr) { p.x = c.x1 + r; hit = { x: 1, z: 0 }; }
          else if (mn === b) { p.z = c.z0 - r; hit = { x: 0, z: -1 }; } else { p.z = c.z1 + r; hit = { x: 0, z: 1 }; }
        }
      }
    }
  }
  return hit;
}
