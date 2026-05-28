// globe.jsx — Real rotating Earth.
// A genuine 3-D globe: a coarse world land-mask is sampled into lat/long
// points, rotated around the polar axis each frame, projected onto a sphere
// (front hemisphere only) and drawn as shaded dots over an ocean gradient.

const Globe = ({ size = 360 }) => {
  const ref = React.useRef(null);

  React.useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = size * dpr;
    canvas.height = size * dpr;
    ctx.scale(dpr, dpr);

    const cx = size / 2, cy = size / 2, R = size * 0.43;

    // Coarse equirectangular land mask. Each row = a 5° latitude band from
    // +90° (top) to −90°; entries are inclusive [col0, col1] longitude spans
    // on a 72-column grid (col 0 = −180°, 5° per col).
    const MASK = {
      2:  [[8,14],[26,30],[50,69]],
      3:  [[2,5],[7,22],[25,31],[46,70]],
      4:  [[1,24],[26,31],[35,40],[42,71]],
      5:  [[1,14],[17,25],[27,30],[33,44],[45,71]],
      6:  [[2,15],[19,26],[35,42],[43,71]],
      7:  [[3,16],[19,27],[32,33],[35,71]],
      8:  [[4,28],[33,71]],
      9:  [[5,27],[33,52],[54,71]],
      10: [[6,26],[32,37],[40,71]],
      11: [[7,25],[31,46],[47,70]],
      12: [[9,22],[30,53],[55,70]],
      13: [[11,20],[29,53],[55,70]],
      14: [[13,20],[30,52],[54,69]],
      15: [[15,21],[31,51],[55,68]],
      16: [[20,27],[32,50],[60,68]],
      17: [[21,30],[33,49],[60,69]],
      18: [[21,31],[34,48],[60,70]],
      19: [[21,32],[35,47],[61,69]],
      20: [[22,33],[36,46],[57,68]],
      21: [[23,33],[37,45],[57,68]],
      22: [[24,33],[38,45],[56,67]],
      23: [[25,32],[39,44],[57,66]],
      24: [[26,31],[40,43],[58,65]],
      25: [[27,30],[41,43],[60,63]],
      26: [[27,29],[68,70]],
      27: [[27,29]],
      28: [[27,28]],
      29: [[27,28]],
      32: [[4,67]],
      33: [[0,71]],
      34: [[0,71]],
    };

    const pts = [];
    for (const r in MASK) {
      const row = +r;
      for (const [c0, c1] of MASK[r]) {
        for (let c = c0; c <= c1; c += 0.5) {
          const lon = (-180 + c * 5 + 2.5) * Math.PI / 180;
          for (const sub of [-1.25, 1.25]) {
            const lat = (90 - row * 5 - 2.5 + sub) * Math.PI / 180;
            pts.push([lon, lat]);
          }
        }
      }
    }

    const tilt = 21 * Math.PI / 180;
    const ct = Math.cos(tilt), st = Math.sin(tilt);
    // light direction (top-left, toward viewer)
    const lx = -0.42, ly = 0.5, lz = 0.62;

    let raf, rot = -1.2, last = performance.now();

    const draw = (now) => {
      const dt = Math.min((now - last) / 1000, 0.05);
      last = now;
      rot += dt * 0.32;
      ctx.clearRect(0, 0, size, size);

      // ocean sphere
      const og = ctx.createRadialGradient(cx - R * 0.34, cy - R * 0.4, R * 0.08, cx, cy, R);
      og.addColorStop(0, '#26336f');
      og.addColorStop(0.5, '#141f47');
      og.addColorStop(1, '#070b1c');
      ctx.beginPath();
      ctx.arc(cx, cy, R, 0, Math.PI * 2);
      ctx.fillStyle = og;
      ctx.fill();
      ctx.lineWidth = 1.2;
      ctx.strokeStyle = 'rgba(129,140,248,0.42)';
      ctx.stroke();

      // land dots
      for (let i = 0; i < pts.length; i++) {
        const lon = pts[i][0], lat = pts[i][1];
        const lam = lon + rot;
        const clat = Math.cos(lat);
        let x = clat * Math.sin(lam);
        let y = Math.sin(lat);
        let z = clat * Math.cos(lam);
        // axial tilt around X
        const y2 = y * ct - z * st;
        const z2 = y * st + z * ct;
        y = y2; z = z2;
        if (z <= 0.02) continue;            // front hemisphere only

        const sx = cx + R * x, sy = cy - R * y;
        const lf = Math.max(0, x * lx + y * ly + z * lz);   // diffuse light
        const shade = 0.32 + 0.68 * lf;
        const rr = Math.round(70 + 90 * shade);
        const gg = Math.round(95 + 110 * shade);
        const bb = Math.round(180 + 75 * shade);
        const alpha = (0.55 + 0.45 * z) * (z < 0.12 ? z / 0.12 : 1);
        ctx.beginPath();
        ctx.arc(sx, sy, 1.5 * (0.55 + 0.55 * z), 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${rr},${gg},${bb},${alpha})`;
        ctx.fill();
      }

      // specular sheen
      const sg = ctx.createRadialGradient(cx - R * 0.3, cy - R * 0.34, 0, cx - R * 0.3, cy - R * 0.34, R * 0.85);
      sg.addColorStop(0, 'rgba(175,186,255,0.26)');
      sg.addColorStop(0.45, 'rgba(175,186,255,0)');
      ctx.fillStyle = sg;
      ctx.beginPath();
      ctx.arc(cx, cy, R, 0, Math.PI * 2);
      ctx.fill();

      // limb darkening at the edge for roundness
      const lg = ctx.createRadialGradient(cx, cy, R * 0.7, cx, cy, R);
      lg.addColorStop(0, 'rgba(0,0,0,0)');
      lg.addColorStop(1, 'rgba(2,4,12,0.5)');
      ctx.fillStyle = lg;
      ctx.beginPath();
      ctx.arc(cx, cy, R, 0, Math.PI * 2);
      ctx.fill();

      raf = requestAnimationFrame(draw);
    };

    const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) { rot = -0.6; draw(performance.now()); }
    else raf = requestAnimationFrame(draw);

    return () => raf && cancelAnimationFrame(raf);
  }, [size]);

  return (
    <div className="aiq-globe" style={{ width: size, height: size }}>
      <canvas ref={ref} style={{ width: size, height: size, display: 'block' }} />
    </div>
  );
};

window.AIQ_Globe = Globe;
