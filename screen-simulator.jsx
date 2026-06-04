// screen-simulator.jsx — "Simulateur tactique": lineup editor + matchup simulation

// ── tiny deterministic helpers ───────────────────────────────────────────────
const simHash = (str) => {
  let h = 2166136261 >>> 0;
  const s = String(str || '');
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619) >>> 0;
  }
  return h >>> 0;
};
// seeded PRNG (mulberry32) — deterministic stream from a seed
const simRng = (seed) => {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

// ── static config per sport ──────────────────────────────────────────────────
const SIM_FORMATIONS = {
  football: ['4-3-3', '4-2-3-1', '4-4-2', '3-5-2', '4-1-4-1'],
  basket: ['Twin Towers', 'Small Ball', 'Three-Guard', 'Standard'],
  rugby: ['Standard XV'],
};
const SIM_STYLES = {
  football: ['Possession', 'Contre-attaque', 'Pressing haut', 'Bloc bas', 'Jeu direct'],
  basket: ['Pace & Space', 'Iso-ball', 'Motion', 'Défense agressive'],
  rugby: ['Jeu déployé', 'Jeu au pied', 'Jeu au près'],
};
const SIM_TARGET = { football: 11, basket: 5, rugby: 15 };

// football pitch coordinate templates (vertical 100x100, GK at bottom)
// each formation lists [x,y] from the goalkeeper up to the strikers
const SIM_PITCH_TPL = {
  '4-3-3': [
    [50, 92],
    [16, 74], [38, 78], [62, 78], [84, 74],
    [30, 54], [50, 50], [70, 54],
    [22, 26], [50, 20], [78, 26],
  ],
  '4-2-3-1': [
    [50, 92],
    [16, 74], [38, 78], [62, 78], [84, 74],
    [38, 58], [62, 58],
    [22, 38], [50, 34], [78, 38],
    [50, 16],
  ],
  '4-4-2': [
    [50, 92],
    [16, 74], [38, 78], [62, 78], [84, 74],
    [16, 50], [38, 52], [62, 52], [84, 50],
    [38, 22], [62, 22],
  ],
  '3-5-2': [
    [50, 92],
    [28, 76], [50, 78], [72, 76],
    [12, 54], [36, 56], [50, 50], [64, 56], [88, 54],
    [38, 22], [62, 22],
  ],
  '4-1-4-1': [
    [50, 92],
    [16, 74], [38, 78], [62, 78], [84, 74],
    [50, 62],
    [18, 44], [40, 46], [60, 46], [82, 44],
    [50, 18],
  ],
};

// style match-up: how rowStyle (attacker) fares vs colStyle — additive modifier
const SIM_STYLE_MATRIX = {
  football: {
    'Pressing haut': { 'Possession': 6, 'Jeu direct': -3, 'Bloc bas': -4 },
    'Contre-attaque': { 'Pressing haut': 7, 'Possession': 4, 'Bloc bas': -5 },
    'Possession': { 'Bloc bas': -2, 'Jeu direct': 3, 'Contre-attaque': -4 },
    'Bloc bas': { 'Possession': 5, 'Pressing haut': 3, 'Contre-attaque': 5 },
    'Jeu direct': { 'Pressing haut': 3, 'Possession': -3 },
  },
  basket: {
    'Défense agressive': { 'Iso-ball': 6, 'Motion': 3, 'Pace & Space': -2 },
    'Pace & Space': { 'Iso-ball': 5, 'Défense agressive': 4, 'Motion': 1 },
    'Motion': { 'Iso-ball': 3, 'Défense agressive': -3 },
    'Iso-ball': { 'Motion': 2, 'Pace & Space': -4 },
  },
  rugby: {
    'Jeu déployé': { 'Jeu au près': 5, 'Jeu au pied': 2 },
    'Jeu au pied': { 'Jeu déployé': 4, 'Jeu au près': 2 },
    'Jeu au près': { 'Jeu au pied': 4, 'Jeu déployé': -2 },
  },
};

// position → line classification (football)
const SIM_LINE = (pos) => {
  const p = String(pos || '').toUpperCase();
  if (/GK|G\b|GARD/.test(p)) return 'gk';
  if (/^(D|CB|LB|RB|DEF|DC|DD|DG|LWB|RWB|ARR)/.test(p)) return 'def';
  if (/^(M|CM|DM|AM|MIL|MD|MDC|MO|MC)/.test(p)) return 'mid';
  if (/^(F|FW|ST|CF|W|LW|RW|ATT|AIL|BU|AT)/.test(p)) return 'att';
  return 'mid';
};

// ── main screen ──────────────────────────────────────────────────────────────
const SimulatorScreen = ({ lang, sport, setRoute }) => {
  const fr = lang === 'fr';
  const t = (window.I18N && window.I18N[lang]) || {};
  const ACC = '#CAFF33';
  const SEC = '#3b82f6';

  const SQUADS = window.SQUADS || {};
  const TEAMSTATS = window.TEAMSTATS || {};
  const MATCHES = window.MATCHES || {};
  const PLAYBOOKS = window.PLAYBOOKS || {};

  const teams = Object.entries(SQUADS)
    .filter(([, v]) => v && v.sport === sport)
    .map(([k]) => k)
    .sort();

  const formations = SIM_FORMATIONS[sport] || ['Standard'];
  const styles = SIM_STYLES[sport] || ['Standard'];
  const target = SIM_TARGET[sport] || 5;

  const [mode, setMode] = React.useState('editor');

  // ── team colour lookup from MATCHES by name ──
  const colorFor = React.useCallback((name) => {
    if (!name) return '#888';
    const list = MATCHES[sport] || [];
    for (let i = 0; i < list.length; i++) {
      const m = list[i];
      if (m && m.home && m.home.name === name && m.home.color) return m.home.color;
      if (m && m.away && m.away.name === name && m.away.color) return m.away.color;
    }
    return '#888';
  }, [MATCHES, sport]);

  const crestCode = (name) => String(name || '???').slice(0, 3).toUpperCase();

  const playersOf = (name) => {
    const sq = SQUADS[name];
    if (!sq || !Array.isArray(sq.players)) return [];
    return sq.players;
  };

  // strength 0..100 from team stats (win% + scoring), neutral 50 fallback
  const baseStrength = React.useCallback((name) => {
    const s = TEAMSTATS[name];
    if (!s) return 50;
    const played = (s.w || 0) + (s.d || 0) + (s.l || 0) || s.played || 0;
    const winPct = played ? ((s.w || 0) + 0.5 * (s.d || 0)) / played : 0.5;
    const avgFor = played ? (s.pf || 0) / played : 0;
    const avgAgainst = played ? (s.pa || 0) / played : 0;
    const diff = avgFor - avgAgainst;
    // normalise scoring diff into a small +/- band per sport
    const band = sport === 'basket' ? 20 : sport === 'rugby' ? 15 : 1.2;
    const scoreComp = clamp(diff / band, -1, 1);
    return clamp(50 + (winPct - 0.5) * 80 + scoreComp * 12, 20, 95);
  }, [TEAMSTATS, sport]);

  // ── balance heuristic for football lineup ──
  const computeBalance = (sel, style) => {
    let att = 0, mid = 0, def = 0, gk = 0;
    sel.forEach(([, pos]) => {
      const l = SIM_LINE(pos);
      if (l === 'att') att++; else if (l === 'mid') mid++; else if (l === 'def') def++; else gk++;
    });
    const outfield = Math.max(1, att + mid + def);
    let A = (att / outfield) * 100 * 1.6;
    let M = (mid / outfield) * 100 * 1.4;
    let D = ((def + gk) / outfield) * 100 * 1.3;
    // style modifiers
    const mod = {
      'Possession': [4, 12, 2],
      'Contre-attaque': [12, -2, 6],
      'Pressing haut': [8, 8, -4],
      'Bloc bas': [-6, 0, 14],
      'Jeu direct': [10, -4, 2],
      'Pace & Space': [12, 4, -2],
      'Iso-ball': [10, -2, 0],
      'Motion': [4, 12, 0],
      'Défense agressive': [-2, 2, 14],
      'Jeu déployé': [12, 6, -2],
      'Jeu au pied': [4, 2, 6],
      'Jeu au près': [2, 4, 10],
    }[style] || [0, 0, 0];
    A = clamp(A + mod[0], 0, 100);
    M = clamp(M + mod[1], 0, 100);
    D = clamp(D + mod[2], 0, 100);
    const balance = clamp(100 - (Math.abs(A - M) + Math.abs(M - D) + Math.abs(A - D)) / 3, 0, 100);
    return { att: Math.round(A), mid: Math.round(M), def: Math.round(D), eq: Math.round(balance) };
  };

  // ────────────────────────────────────────────────────────────────
  // EDITOR state
  // ────────────────────────────────────────────────────────────────
  const [edTeam, setEdTeam] = React.useState(teams[0] || '');
  const [edForm, setEdForm] = React.useState(formations[0]);
  const [edStyle, setEdStyle] = React.useState(styles[0]);
  const [edSel, setEdSel] = React.useState(() => {
    const ps = playersOf(teams[0] || '');
    return ps.slice(0, target).map((p) => p[0]);
  });

  React.useEffect(() => {
    // reset selection when team changes
    const ps = playersOf(edTeam);
    setEdSel(ps.slice(0, target).map((p) => p[0]));
  // eslint-disable-next-line
  }, [edTeam]);

  React.useEffect(() => {
    // when sport switches, reset form/style and team
    setEdForm(formations[0]);
    setEdStyle(styles[0]);
    setEdTeam(teams[0] || '');
  // eslint-disable-next-line
  }, [sport]);

  const toggleStarter = (name) => {
    setEdSel((cur) => {
      if (cur.indexOf(name) !== -1) return cur.filter((n) => n !== name);
      if (cur.length >= target) return cur; // cap at target
      return cur.concat([name]);
    });
  };

  const edPlayers = playersOf(edTeam);
  const edSelected = edPlayers.filter((p) => edSel.indexOf(p[0]) !== -1);
  const balance = computeBalance(edSelected, edStyle);

  // ── football pitch render ──
  const renderPitch = (selected, form, accent) => {
    const tpl = SIM_PITCH_TPL[form] || SIM_PITCH_TPL['4-3-3'];
    const W = 320, H = 440;
    const spots = tpl.slice(0, Math.min(selected.length, tpl.length));
    return (
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" preserveAspectRatio="xMidYMid meet"
           style={{ display: 'block', background: '#0c1f15', borderRadius: 12 }}>
        <rect x="6" y="6" width={W - 12} height={H - 12} fill="none" stroke="#1f4636" strokeWidth="1.5" />
        <line x1="6" y1={H / 2} x2={W - 6} y2={H / 2} stroke="#1f4636" strokeWidth="1.2" />
        <circle cx={W / 2} cy={H / 2} r="40" fill="none" stroke="#1f4636" strokeWidth="1.2" />
        <rect x={W / 2 - 55} y={H - 60} width="110" height="54" fill="none" stroke="#1f4636" strokeWidth="1.2" />
        <rect x={W / 2 - 55} y="6" width="110" height="54" fill="none" stroke="#1f4636" strokeWidth="1.2" />
        {spots.map((s, i) => {
          const cx = (s[0] / 100) * W;
          const cy = (s[1] / 100) * H;
          const name = selected[i] ? selected[i][0] : '';
          const last = name.split(' ').slice(-1)[0];
          return (
            <g key={i}>
              <circle cx={cx} cy={cy} r="12" fill={accent} stroke="#000" strokeWidth="1.2" />
              <text x={cx} y={cy + 4} textAnchor="middle" fontSize="11" fontWeight="700"
                    fill="#0a0a0a" fontFamily="sans-serif">{i === 0 ? 'GK' : i + 1}</text>
              <text x={cx} y={cy + 25} textAnchor="middle" fontSize="10"
                    fill="#dfe7e2" fontFamily="sans-serif">{last}</text>
            </g>
          );
        })}
      </svg>
    );
  };

  // ────────────────────────────────────────────────────────────────
  // SIM state
  // ────────────────────────────────────────────────────────────────
  const [aTeam, setATeam] = React.useState(teams[0] || '');
  const [aForm, setAForm] = React.useState(formations[0]);
  const [aStyle, setAStyle] = React.useState(styles[0]);
  const [bTeam, setBTeam] = React.useState(teams[1] || teams[0] || '');
  const [bForm, setBForm] = React.useState(formations[0]);
  const [bStyle, setBStyle] = React.useState(styles[1] || styles[0]);
  const [result, setResult] = React.useState(null);

  React.useEffect(() => {
    setATeam(teams[0] || '');
    setBTeam(teams[1] || teams[0] || '');
    setAForm(formations[0]); setBForm(formations[0]);
    setAStyle(styles[0]); setBStyle(styles[1] || styles[0]);
    setResult(null);
  // eslint-disable-next-line
  }, [sport]);

  const styleMod = (mine, theirs) => {
    const tbl = SIM_STYLE_MATRIX[sport] || {};
    return (tbl[mine] && typeof tbl[mine][theirs] === 'number') ? tbl[mine][theirs] : 0;
  };

  const runSim = () => {
    const seed = simHash([aTeam, aForm, aStyle, bTeam, bForm, bStyle, sport].join('|'));
    const rng = simRng(seed);

    const HOME_ADV = 4;
    let sA = baseStrength(aTeam) + HOME_ADV + styleMod(aStyle, bStyle);
    let sB = baseStrength(bTeam) + styleMod(bStyle, aStyle);
    // small deterministic jitter
    sA += (rng() - 0.5) * 8;
    sB += (rng() - 0.5) * 8;
    sA = clamp(sA, 10, 100);
    sB = clamp(sB, 10, 100);

    const total = sA + sB;
    let pA = sA / total;
    let pB = sB / total;
    // draw probability shrinks the closer the gap is filled; sport dependent
    const drawBase = sport === 'football' ? 0.26 : sport === 'rugby' ? 0.06 : 0.02;
    const gap = Math.abs(pA - pB);
    let pDraw = clamp(drawBase * (1 - gap), 0, 0.4);
    pA = pA * (1 - pDraw);
    pB = pB * (1 - pDraw);
    const norm = pA + pB + pDraw;
    pA /= norm; pB /= norm; pDraw /= norm;

    // scoreline scale per sport
    let scoreA, scoreB;
    if (sport === 'basket') {
      const baseline = 98;
      scoreA = Math.round(baseline + (sA - 50) * 0.5 + (rng() - 0.5) * 8);
      scoreB = Math.round(baseline + (sB - 50) * 0.5 + (rng() - 0.5) * 8);
    } else if (sport === 'rugby') {
      const baseline = 22;
      scoreA = Math.round(clamp(baseline + (sA - 50) * 0.35 + (rng() - 0.5) * 6, 3, 55));
      scoreB = Math.round(clamp(baseline + (sB - 50) * 0.35 + (rng() - 0.5) * 6, 3, 55));
    } else {
      scoreA = Math.round(clamp((sA / 35) + (rng() - 0.3) * 1.4, 0, 6));
      scoreB = Math.round(clamp((sB / 35) + (rng() - 0.3) * 1.4, 0, 6));
    }

    // tactical keys
    const aP = playersOf(aTeam);
    const bP = playersOf(bTeam);
    const aNames = aP.slice(0, 2).map((p) => p[0]);
    const bNames = bP.slice(0, 2).map((p) => p[0]);
    const keys = [];
    const smAB = styleMod(aStyle, bStyle);
    const smBA = styleMod(bStyle, aStyle);
    if (smAB > smBA && smAB > 0) {
      keys.push(fr
        ? `Le ${aStyle} de ${aTeam} prend l'ascendant sur le ${bStyle} adverse.`
        : `${aTeam}'s ${aStyle} gains the upper hand over the opposing ${bStyle}.`);
    } else if (smBA > smAB && smBA > 0) {
      keys.push(fr
        ? `Le ${bStyle} de ${bTeam} neutralise le ${aStyle} de ${aTeam}.`
        : `${bTeam}'s ${bStyle} neutralises ${aTeam}'s ${aStyle}.`);
    } else {
      keys.push(fr
        ? `Duel de styles équilibré (${aStyle} vs ${bStyle}) : la décision se fera sur les individualités.`
        : `Balanced style duel (${aStyle} vs ${bStyle}): individuals will make the difference.`);
    }
    keys.push(fr
      ? `Disposition ${aForm} contre ${bForm} : l'occupation des espaces sera déterminante.`
      : `${aForm} against ${bForm}: spacing control will be key.`);
    if (aNames.length) {
      keys.push(fr
        ? `Côté ${aTeam}, ${aNames.join(' et ')} devront porter le projet de jeu.`
        : `For ${aTeam}, ${aNames.join(' and ')} must carry the game plan.`);
    }
    if (bNames.length) {
      keys.push(fr
        ? `${bTeam} s'appuiera sur ${bNames.join(' et ')} pour répondre.`
        : `${bTeam} will rely on ${bNames.join(' and ')} to respond.`);
    }

    setResult({
      scoreA, scoreB,
      pA: Math.round(pA * 100), pDraw: Math.round(pDraw * 100), pB: Math.round(pB * 100),
      keys: keys.slice(0, 4),
      sA: Math.round(sA), sB: Math.round(sB),
    });
  };

  // ── small reusable controls ──
  const Field = ({ label, value, onChange, options }) => (
    <label style={{ display: 'block', flex: '1 1 140px', minWidth: 120 }}>
      <div className="kv-key" style={{ marginBottom: 4, textTransform: 'uppercase', letterSpacing: '.06em', fontSize: 11 }}>{label}</div>
      <select className="field" value={value} onChange={(e) => onChange(e.target.value)} style={{ width: '100%' }}>
        {options.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    </label>
  );

  const Bar = ({ label, value, color }) => (
    <div style={{ marginBottom: 10 }}>
      <div className="row" style={{ justifyContent: 'space-between', marginBottom: 4 }}>
        <span className="kv-key" style={{ fontSize: 12 }}>{label}</span>
        <span className="kv-val" style={{ fontSize: 13, color: color || '#ddd' }}>{value}%</span>
      </div>
      <div className="progress" style={{ background: '#1a1a1a', borderRadius: 6, overflow: 'hidden', height: 8 }}>
        <div style={{ width: `${clamp(value, 0, 100)}%`, height: '100%', background: color || ACC, borderRadius: 6, transition: 'width .4s' }} />
      </div>
    </div>
  );

  const noData = teams.length === 0;

  // related playbook tactic suggestion (link style → a tactic name)
  const linkedTactic = React.useMemo(() => {
    const pb = PLAYBOOKS[sport] || [];
    if (!pb.length) return null;
    const idx = simHash(edStyle + sport) % pb.length;
    return pb[idx] && pb[idx].name;
  }, [PLAYBOOKS, sport, edStyle]);

  return (
    <div className="page">
      <div className="page-head">
        <div>
          <h1 className="page-title">{fr ? 'Simulateur tactique' : 'Tactical simulator'}</h1>
          <p className="page-sub">
            {fr
              ? 'Composez un onze, choisissez une formation et un style, puis simulez la confrontation.'
              : 'Build a lineup, pick a formation and style, then simulate the matchup.'}
          </p>
        </div>
      </div>

      <div className="tab-strip" style={{ marginBottom: 18 }}>
        <button data-active={mode === 'editor'} onClick={() => setMode('editor')}>
          {fr ? 'Éditeur de onze' : 'Lineup editor'}
        </button>
        <button data-active={mode === 'sim'} onClick={() => setMode('sim')}>
          {fr ? 'Simulation de confrontation' : 'Matchup simulation'}
        </button>
      </div>

      {noData && (
        <div className="card" style={{ textAlign: 'center', padding: 50, color: '#666' }}>
          {t.no_data || (fr ? 'Aucune donnée' : 'No data')}
        </div>
      )}

      {/* ─────────────── EDITOR ─────────────── */}
      {!noData && mode === 'editor' && (
        <div className="grid fade-in" style={{ gridTemplateColumns: 'minmax(280px, 1fr) minmax(280px, 360px)', gap: 16, alignItems: 'start' }}>
          <div>
            <div className="card" style={{ marginBottom: 16 }}>
              <div className="card-head"><h3 className="card-title" style={{ margin: 0, fontSize: 18 }}>{fr ? 'Configuration' : 'Setup'}</h3></div>
              <div className="row" style={{ flexWrap: 'wrap', gap: 10, marginTop: 12 }}>
                <Field label={fr ? 'Équipe' : 'Team'} value={edTeam} onChange={setEdTeam} options={teams} />
                <Field label="Formation" value={edForm} onChange={setEdForm} options={formations} />
                <Field label={fr ? 'Style' : 'Style'} value={edStyle} onChange={setEdStyle} options={styles} />
              </div>
              {linkedTactic && (
                <div className="row" style={{ marginTop: 12, alignItems: 'center', gap: 8 }}>
                  <Pill kind="accent">{fr ? 'Tactique liée' : 'Linked tactic'}</Pill>
                  <span style={{ color: '#bbb', fontSize: 13 }}>{linkedTactic}</span>
                </div>
              )}
            </div>

            <div className="card">
              <div className="card-head" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3 className="card-title" style={{ margin: 0, fontSize: 18 }}>{fr ? 'Effectif' : 'Squad'}</h3>
                <Pill kind={edSelected.length === target ? 'accent' : 'default'}>
                  {edSelected.length} / {target} {fr ? 'titulaires' : 'starters'}
                </Pill>
              </div>
              <div style={{ marginTop: 12, display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: 8 }}>
                {edPlayers.map((p, i) => {
                  const on = edSel.indexOf(p[0]) !== -1;
                  return (
                    <button key={p[0] + i} className="player-row" onClick={() => toggleStarter(p[0])}
                            style={{
                              display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', textAlign: 'left',
                              background: on ? 'rgba(202,255,51,0.10)' : '#131313',
                              border: `1px solid ${on ? ACC : 'var(--border-strong, #2a2a2a)'}`,
                              borderRadius: 8, padding: '8px 10px', width: '100%',
                            }}>
                      <span style={{
                        width: 18, height: 18, borderRadius: 5, flex: '0 0 auto',
                        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                        background: on ? ACC : 'transparent', border: `1px solid ${on ? ACC : '#555'}`,
                      }}>
                        {on && <Icon name="check" size={12} stroke={2.4} />}
                      </span>
                      <span style={{ overflow: 'hidden' }}>
                        <span className="player-name" style={{ display: 'block', fontSize: 13, color: '#e6e6e6', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>{p[0]}</span>
                        <span className="player-meta" style={{ fontSize: 11, color: '#888' }}>{p[1]}</span>
                      </span>
                    </button>
                  );
                })}
                {edPlayers.length === 0 && <div style={{ color: '#666', fontSize: 13 }}>{t.no_data || (fr ? 'Aucun joueur' : 'No players')}</div>}
              </div>
            </div>
          </div>

          <div>
            {sport === 'football' && (
              <div className="card" style={{ marginBottom: 16 }}>
                <div className="card-head"><h3 className="card-title" style={{ margin: 0, fontSize: 18 }}>{fr ? 'Le terrain' : 'On the pitch'} · {edForm}</h3></div>
                <div style={{ marginTop: 12 }}>{renderPitch(edSelected, edForm, ACC)}</div>
              </div>
            )}

            <div className="card">
              <div className="card-head"><h3 className="card-title" style={{ margin: 0, fontSize: 18 }}>{fr ? 'Équilibre de l\'équipe' : 'Team balance'}</h3></div>
              <div style={{ marginTop: 14 }}>
                <Bar label={fr ? 'Attaque' : 'Attack'} value={balance.att} color={ACC} />
                <Bar label={fr ? 'Milieu' : 'Midfield'} value={balance.mid} color={SEC} />
                <Bar label={fr ? 'Défense' : 'Defense'} value={balance.def} color="#f59e0b" />
              </div>
              <div className="row" style={{ justifyContent: 'center', marginTop: 14 }}>
                <div style={{ textAlign: 'center' }}>
                  <Gauge value={balance.eq} />
                  <div className="kv-key" style={{ marginTop: 6, fontSize: 11, textTransform: 'uppercase', letterSpacing: '.06em' }}>{fr ? 'Équilibre global' : 'Overall balance'}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ─────────────── SIM ─────────────── */}
      {!noData && mode === 'sim' && (
        <div className="fade-in">
          <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 16 }}>
            {/* Team A */}
            <div className="card">
              <div className="row" style={{ alignItems: 'center', gap: 10 }}>
                <Crest code={crestCode(aTeam)} color={colorFor(aTeam)} />
                <div>
                  <div className="card-title" style={{ fontSize: 17 }}>{aTeam || '—'}</div>
                  <div className="card-sub" style={{ fontSize: 12 }}>{fr ? 'Équipe A (domicile)' : 'Team A (home)'}</div>
                </div>
              </div>
              <div className="row" style={{ flexWrap: 'wrap', gap: 10, marginTop: 12 }}>
                <Field label={fr ? 'Équipe' : 'Team'} value={aTeam} onChange={setATeam} options={teams} />
                <Field label="Formation" value={aForm} onChange={setAForm} options={formations} />
                <Field label={fr ? 'Style' : 'Style'} value={aStyle} onChange={setAStyle} options={styles} />
              </div>
            </div>
            {/* Team B */}
            <div className="card">
              <div className="row" style={{ alignItems: 'center', gap: 10 }}>
                <Crest code={crestCode(bTeam)} color={colorFor(bTeam)} />
                <div>
                  <div className="card-title" style={{ fontSize: 17 }}>{bTeam || '—'}</div>
                  <div className="card-sub" style={{ fontSize: 12 }}>{fr ? 'Équipe B (extérieur)' : 'Team B (away)'}</div>
                </div>
              </div>
              <div className="row" style={{ flexWrap: 'wrap', gap: 10, marginTop: 12 }}>
                <Field label={fr ? 'Équipe' : 'Team'} value={bTeam} onChange={setBTeam} options={teams} />
                <Field label="Formation" value={bForm} onChange={setBForm} options={formations} />
                <Field label={fr ? 'Style' : 'Style'} value={bStyle} onChange={setBStyle} options={styles} />
              </div>
            </div>
          </div>

          <div className="row" style={{ justifyContent: 'center', margin: '18px 0' }}>
            <button className="btn btn-primary" onClick={runSim}>
              <Icon name="play" size={16} />
              {fr ? 'Simuler' : 'Simulate'}
            </button>
          </div>

          {result && (
            <div className="grid fade-in" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 16 }}>
              <div className="card">
                <div className="card-sub" style={{ textAlign: 'center', textTransform: 'uppercase', letterSpacing: '.07em', fontSize: 11 }}>
                  {t.predicted_score || (fr ? 'Score prédit' : 'Predicted score')}
                </div>
                <div className="row" style={{ justifyContent: 'center', alignItems: 'center', gap: 18, margin: '14px 0' }}>
                  <div style={{ textAlign: 'center' }}>
                    <Crest code={crestCode(aTeam)} color={colorFor(aTeam)} />
                    <div style={{ fontSize: 12, color: '#aaa', marginTop: 6, maxWidth: 90 }}>{aTeam}</div>
                  </div>
                  <div style={{ fontSize: 40, fontWeight: 800, color: '#fff' }}>
                    {result.scoreA}<span style={{ color: '#555', margin: '0 8px' }}>-</span>{result.scoreB}
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <Crest code={crestCode(bTeam)} color={colorFor(bTeam)} />
                    <div style={{ fontSize: 12, color: '#aaa', marginTop: 6, maxWidth: 90 }}>{bTeam}</div>
                  </div>
                </div>
                <div className="row" style={{ justifyContent: 'center', gap: 16, fontSize: 11, color: '#777' }}>
                  <span>{fr ? 'Force A' : 'Strength A'}: {result.sA}</span>
                  <span>{fr ? 'Force B' : 'Strength B'}: {result.sB}</span>
                </div>
              </div>

              <div className="card">
                <div className="card-head"><h3 className="card-title" style={{ margin: 0, fontSize: 16 }}>{t.win_probability || (fr ? 'Probabilités' : 'Win probability')}</h3></div>
                <div style={{ marginTop: 12 }}>
                  <Bar label={`${aTeam} (${fr ? 'dom.' : 'home'})`} value={result.pA} color={ACC} />
                  <Bar label={fr ? 'Nul' : 'Draw'} value={result.pDraw} color="#888" />
                  <Bar label={`${bTeam} (${fr ? 'ext.' : 'away'})`} value={result.pB} color={SEC} />
                </div>
              </div>

              <div className="card" style={{ gridColumn: '1 / -1' }}>
                <div className="card-head"><h3 className="card-title" style={{ margin: 0, fontSize: 16 }}>{fr ? 'Clés tactiques' : 'Tactical keys'}</h3></div>
                <ul style={{ margin: '12px 0 0', paddingLeft: 0, listStyle: 'none' }}>
                  {result.keys.map((k, i) => (
                    <li key={i} style={{ display: 'flex', gap: 8, alignItems: 'flex-start', marginBottom: 8, color: '#d2d2d2', fontSize: 13, lineHeight: 1.5 }}>
                      <span style={{ color: ACC, flex: '0 0 auto', marginTop: 2 }}><Icon name="target" size={14} /></span>
                      <span>{k}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}

      <div className="footer">{(window.I18N && window.I18N[lang] && window.I18N[lang].footer) || ''}</div>
    </div>
  );
};

Object.assign(window, { SimulatorScreen });
