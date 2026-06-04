// screen-tactics.jsx — Tactics catalog with hand-drawn-style SVG diagrams

// ── Hand-drawn-style schematic for each tactic type ──────────────────────────
const TacticDiagram = ({ diagram, color }) => {
  const ACC = color || '#CAFF33';
  const OPP = '#7a7a7a';
  const LINE = '#2c2c2c';
  const BG = '#0d0d0d';
  const aid = 'th-arr-' + (diagram || 'def');
  const oid = 'th-arro-' + (diagram || 'def');

  const Markers = () => (
    <defs>
      <marker id={aid} markerWidth="9" markerHeight="9" refX="6.5" refY="4"
              orient="auto" markerUnits="userSpaceOnUse">
        <path d="M0 0 L8 4 L0 8 z" fill={ACC} />
      </marker>
      <marker id={oid} markerWidth="9" markerHeight="9" refX="6.5" refY="4"
              orient="auto" markerUnits="userSpaceOnUse">
        <path d="M0 0 L8 4 L0 8 z" fill={OPP} />
      </marker>
    </defs>
  );

  const dot = (x, y, fill, key) => (
    <circle key={key} cx={x} cy={y} r="6" fill={fill} stroke="#000" strokeWidth="0.8" />
  );
  const arr = (x1, y1, x2, y2, key, c) => (
    <line key={key} x1={x1} y1={y1} x2={x2} y2={y2}
          stroke={c || ACC} strokeWidth="2" strokeLinecap="round"
          markerEnd={'url(#' + (c === OPP ? oid : aid) + ')'} />
  );

  // ── pitch backgrounds ──
  const footballBg = (
    <g>
      <rect x="0" y="0" width="320" height="200" fill="#0f2417" />
      <rect x="6" y="6" width="308" height="188" fill="none" stroke="#2e5d40" strokeWidth="1.5" />
      <line x1="160" y1="6" x2="160" y2="194" stroke="#2e5d40" strokeWidth="1.5" />
      <circle cx="160" cy="100" r="26" fill="none" stroke="#2e5d40" strokeWidth="1.5" />
    </g>
  );
  const basketBg = (
    <g>
      <rect x="0" y="0" width="320" height="200" fill="#1a1206" />
      <rect x="6" y="6" width="308" height="188" fill="none" stroke="#5a4420" strokeWidth="1.5" />
      <rect x="110" y="6" width="100" height="78" fill="none" stroke="#5a4420" strokeWidth="1.5" />
      <path d="M120 84 A 40 40 0 0 0 200 84" fill="none" stroke="#5a4420" strokeWidth="1.5" />
      <path d="M40 6 A 130 130 0 0 0 280 6" fill="none" stroke="#5a4420" strokeWidth="1.5" />
      <circle cx="160" cy="20" r="4" fill="none" stroke="#5a4420" strokeWidth="1.5" />
    </g>
  );
  const rugbyBg = (
    <g>
      <rect x="0" y="0" width="320" height="200" fill="#0f2417" />
      <rect x="6" y="6" width="308" height="188" fill="none" stroke="#2e5d40" strokeWidth="1.5" />
      <line x1="6" y1="40" x2="314" y2="40" stroke="#2e5d40" strokeWidth="2" />
      <line x1="6" y1="160" x2="314" y2="160" stroke="#2e5d40" strokeWidth="1.5" strokeDasharray="5 5" />
    </g>
  );

  let body = null;
  switch (diagram) {
    // ── FOOTBALL ──
    case 'fb_press':
      body = (<g>{footballBg}
        {[[60,150],[120,160],[180,158],[240,150]].map((p,i)=>dot(p[0],p[1],ACC,'p'+i))}
        {dot(160,70,OPP,'ball')}
        {arr(60,150,120,95,'a0')}{arr(120,160,150,90,'a1')}{arr(180,158,168,90,'a2')}{arr(240,150,200,95,'a3')}
      </g>); break;
    case 'fb_block':
      body = (<g>{footballBg}
        {[60,110,160,210,260].map((x,i)=>dot(x,80,ACC,'b'+i))}
        {[90,160,230].map((x,i)=>dot(x,120,ACC,'c'+i))}
        <line x1="40" y1="80" x2="280" y2="80" stroke={ACC} strokeWidth="1" strokeDasharray="3 3" />
        <line x1="60" y1="120" x2="250" y2="120" stroke={ACC} strokeWidth="1" strokeDasharray="3 3" />
      </g>); break;
    case 'fb_buildup':
      body = (<g>{footballBg}
        {dot(40,100,ACC,'gk')}{dot(110,55,ACC,'cb1')}{dot(110,145,ACC,'cb2')}{dot(180,100,ACC,'mid')}
        {arr(40,100,108,57,'a0')}{arr(110,55,178,98,'a1')}{arr(180,100,112,143,'a2')}
      </g>); break;
    case 'fb_counter':
      body = (<g>{footballBg}
        {dot(50,150,ACC,'d')}{dot(120,120,ACC,'m')}{dot(250,60,ACC,'f')}
        {arr(50,150,118,122,'a0')}{arr(120,120,245,62,'a1')}
        <path d="M250 60 q 30 -20 55 10" fill="none" stroke={ACC} strokeWidth="2" markerEnd={'url(#'+aid+')'} />
      </g>); break;
    case 'fb_setpiece':
      body = (<g>{footballBg}
        <rect x="200" y="40" width="114" height="120" fill="none" stroke="#2e5d40" strokeWidth="1.5" />
        {dot(20,180,ACC,'corner')}
        {[[150,90],[160,130],[150,60]].map((p,i)=>dot(p[0],p[1],ACC,'r'+i))}
        <path d="M28 178 Q 130 60 235 70" fill="none" stroke={ACC} strokeWidth="2" markerEnd={'url(#'+aid+')'} />
        {arr(150,90,250,90,'a1')}{arr(150,130,250,120,'a2')}
      </g>); break;
    case 'fb_width':
      body = (<g>{footballBg}
        {dot(40,40,ACC,'w1')}{dot(40,160,ACC,'w2')}{dot(120,40,ACC,'fb1')}{dot(120,160,ACC,'fb2')}{dot(200,100,ACC,'st')}
        {arr(120,40,180,40,'a0')}{arr(40,40,90,90,'a1')}{arr(120,160,180,160,'a2')}{arr(40,160,90,110,'a3')}
      </g>); break;

    // ── BASKET ──
    case 'bk_pnr':
      body = (<g>{basketBg}
        {dot(160,150,ACC,'bh')}{dot(190,110,ACC,'scr')}
        <path d="M160 150 q 40 -10 50 -60" fill="none" stroke={ACC} strokeWidth="2" markerEnd={'url(#'+aid+')'} />
        {arr(190,110,150,60,'roll')}
        {dot(60,90,ACC,'s1')}{dot(260,90,ACC,'s2')}{dot(60,40,ACC,'s3')}
      </g>); break;
    case 'bk_iso':
      body = (<g>{basketBg}
        {dot(40,140,ACC,'s1')}{dot(280,140,ACC,'s2')}{dot(40,60,ACC,'s3')}{dot(280,60,ACC,'s4')}
        {dot(160,160,ACC,'drv')}
        {arr(160,160,160,60,'a0')}
      </g>); break;
    case 'bk_post':
      body = (<g>{basketBg}
        {dot(190,55,ACC,'post')}{dot(110,140,ACC,'wing')}
        {arr(110,140,184,60,'a0')}
        {dot(50,90,ACC,'s1')}{dot(270,90,ACC,'s2')}{dot(160,170,ACC,'s3')}
      </g>); break;
    case 'bk_motion':
      body = (<g>{basketBg}
        {[[100,80],[220,80],[160,150],[60,140],[260,140]].map((p,i)=>dot(p[0],p[1],ACC,'m'+i))}
        <path d="M100 80 Q 160 40 220 80" fill="none" stroke={ACC} strokeWidth="2" markerEnd={'url(#'+aid+')'} />
        <path d="M220 80 Q 240 120 160 150" fill="none" stroke={ACC} strokeWidth="2" markerEnd={'url(#'+aid+')'} />
        <path d="M160 150 Q 90 160 60 140" fill="none" stroke={ACC} strokeWidth="2" markerEnd={'url(#'+aid+')'} />
      </g>); break;
    case 'bk_defense':
      body = (<g>{basketBg}
        {[[130,55],[190,55],[110,110],[210,110],[160,140]].map((p,i)=>dot(p[0],p[1],ACC,'z'+i))}
        <path d="M130 55 L190 55 L210 110 L160 140 L110 110 Z" fill="none" stroke={ACC} strokeWidth="1.5" strokeDasharray="4 3" />
      </g>); break;
    case 'bk_transition':
      body = (<g>{basketBg}
        {dot(60,170,ACC,'g')}{dot(40,120,ACC,'w1')}{dot(280,120,ACC,'w2')}
        {arr(60,170,60,60,'a0')}{arr(40,120,90,50,'a1')}{arr(280,120,230,50,'a2')}
      </g>); break;

    // ── RUGBY ──
    case 'rg_lineout':
      body = (<g>{rugbyBg}
        {[150,110,70].map((y,i)=>dot(200,y,ACC,'j'+i))}
        {[180,140,100].map((y,i)=>dot(230,y,OPP,'o'+i))}
        {dot(60,150,ACC,'thrower')}
        <path d="M66 148 Q 130 70 196 78" fill="none" stroke={ACC} strokeWidth="2" markerEnd={'url(#'+aid+')'} />
      </g>); break;
    case 'rg_scrum':
      body = (<g>{rugbyBg}
        {[[140,80],[160,70],[180,80],[135,105],[160,100],[185,105],[150,128],[170,128]].map((p,i)=>dot(p[0],p[1],ACC,'a'+i))}
        {[[140,150],[160,160],[180,150]].map((p,i)=>dot(p[0],p[1],OPP,'o'+i))}
        <line x1="120" y1="115" x2="200" y2="115" stroke={LINE} strokeWidth="2" />
      </g>); break;
    case 'rg_kick':
      body = (<g>{rugbyBg}
        {dot(60,160,ACC,'kicker')}{dot(230,60,ACC,'chase')}
        <path d="M66 158 Q 160 -10 250 60" fill="none" stroke={ACC} strokeWidth="2" strokeDasharray="5 4" markerEnd={'url(#'+aid+')'} />
        {arr(200,150,225,75,'chasearr')}{dot(200,150,ACC,'c2')}
      </g>); break;
    case 'rg_defense':
      body = (<g>{rugbyBg}
        {[50,100,150,200,260].map((x,i)=>dot(x,140,ACC,'d'+i))}
        <line x1="40" y1="140" x2="280" y2="140" stroke={ACC} strokeWidth="1" strokeDasharray="3 3" />
        {[50,100,150,200,260].map((x,i)=>arr(x,140,x,95,'u'+i))}
      </g>); break;
    case 'rg_ruck':
      body = (<g>{rugbyBg}
        {[[150,100],[165,90],[178,100],[160,115]].map((p,i)=>dot(p[0],p[1],ACC,'r'+i))}
        {[[145,80],[170,75]].map((p,i)=>dot(p[0],p[1],OPP,'o'+i))}
        {dot(120,130,ACC,'sh')}{dot(70,130,ACC,'fly')}
        {arr(120,130,75,130,'a0')}
        <path d="M160 110 q -25 25 -38 18" fill="none" stroke={ACC} strokeWidth="1.5" markerEnd={'url(#'+aid+')'} />
      </g>); break;
    case 'rg_backline':
      body = (<g>{rugbyBg}
        {[[60,160],[110,135],[160,115],[210,95],[260,75]].map((p,i)=>dot(p[0],p[1],ACC,'b'+i))}
        {arr(60,160,106,137,'a0')}{arr(110,135,156,117,'a1')}{arr(160,115,206,97,'a2')}{arr(210,95,256,77,'a3')}
      </g>); break;

    default:
      body = (<g>
        <rect x="0" y="0" width="320" height="200" fill="#101010" />
        <rect x="6" y="6" width="308" height="188" fill="none" stroke={LINE} strokeWidth="1.5" />
        {[[100,80],[220,80],[160,140]].map((p,i)=>dot(p[0],p[1],ACC,'x'+i))}
        {arr(100,80,160,140,'a0')}{arr(220,80,160,140,'a1')}
      </g>); break;
  }

  return (
    <svg viewBox="0 0 320 200" width="100%" preserveAspectRatio="xMidYMid meet"
         style={{ display: 'block', borderRadius: 8, background: BG }}>
      <Markers />
      {body}
    </svg>
  );
};

// ── Main screen ──────────────────────────────────────────────────────────────
function TacticsScreen({ lang, sport, setRoute }) {
  const t = (window.I18N && window.I18N[lang]) || {};
  const fr = lang === 'fr';
  const accent = 'var(--accent)';

  const propToKey = { football: 'football', basket: 'basket', rugby: 'rugby' };
  const sportTabs = [
    { key: 'football', label: 'Football' },
    { key: 'basket', label: 'Basket' },
    { key: 'rugby', label: 'Rugby' },
  ];

  const [activeSport, setActiveSport] = React.useState(propToKey[sport] || 'football');
  const [cat, setCat] = React.useState('__all__');
  const [query, setQuery] = React.useState('');
  const [selected, setSelected] = React.useState(null);

  const PB = (window.PLAYBOOKS && window.PLAYBOOKS[activeSport]) || [];

  // distinct categories
  const cats = React.useMemo(() => {
    const seen = [];
    PB.forEach(p => { if (p.categorie && seen.indexOf(p.categorie) === -1) seen.push(p.categorie); });
    return seen;
  }, [activeSport]);

  const filtered = React.useMemo(() => {
    const q = query.trim().toLowerCase();
    return PB.filter(p => {
      if (cat !== '__all__' && p.categorie !== cat) return false;
      if (q) {
        const hay = ((p.name || '') + ' ' + (p.objectif || '')).toLowerCase();
        if (hay.indexOf(q) === -1) return false;
      }
      return true;
    });
  }, [activeSport, cat, query]);

  const switchSport = (k) => { setActiveSport(k); setCat('__all__'); setQuery(''); setSelected(null); };

  const truncate = (s, n) => (s && s.length > n ? s.slice(0, n - 1) + '…' : (s || ''));

  // ── Detail view ──
  const Detail = ({ tac }) => {
    const sections = [
      ['objectif', fr ? 'Objectif' : 'Objective'],
      ['principe', fr ? 'Principe' : 'Principle'],
      ['avantages', fr ? 'Avantages' : 'Strengths'],
      ['limites', fr ? 'Limites' : 'Weaknesses'],
      ['reconnaitre', fr ? 'Reconnaître' : 'How to spot it'],
      ['contre_mesures', fr ? 'Contre-mesures' : 'Counter-measures'],
    ];
    return (
      <div className="fade-in">
        <button className="btn btn-ghost btn-sm" onClick={() => setSelected(null)}
                style={{ marginBottom: 14 }}>
          <Icon name="arrow" size={14} /> {fr ? 'Retour' : 'Back'}
        </button>

        <div className="card" style={{ marginBottom: 16 }}>
          <div className="card-head" style={{ alignItems: 'center' }}>
            <div>
              <div className="card-title" style={{ fontFamily: 'var(--font-display, inherit)', fontSize: 22 }}>
                {tac.name}
              </div>
              <div style={{ marginTop: 6 }}><Pill kind="accent">{tac.categorie}</Pill></div>
            </div>
            <Icon name="target" size={22} />
          </div>
          <div style={{ maxWidth: 460, margin: '12px auto 0' }}>
            <TacticDiagram diagram={tac.diagram} color="#CAFF33" />
          </div>
        </div>

        <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))' }}>
          {sections.map(([k, label]) => (
            <div className="card card-tight" key={k}>
              <div className="kv-key" style={{ marginBottom: 6, color: accent, textTransform: 'uppercase', fontSize: 11, letterSpacing: 0.5 }}>
                {label}
              </div>
              <div className="kv-val" style={{ lineHeight: 1.5 }}>{tac[k] || '—'}</div>
            </div>
          ))}
        </div>

        <div className="card card-tight" style={{ marginTop: 16 }}>
          <div className="kv-key" style={{ marginBottom: 8, color: accent, textTransform: 'uppercase', fontSize: 11, letterSpacing: 0.5 }}>
            {fr ? "Équipes qui l'utilisent" : 'Teams that use it'}
          </div>
          {(tac.teams && tac.teams.length) ? (
            <div className="row" style={{ flexWrap: 'wrap', gap: 6 }}>
              {tac.teams.map((tm, i) => (
                <span className="pill" key={i}>{tm}</span>
              ))}
            </div>
          ) : <div className="kv-val">—</div>}
        </div>
      </div>
    );
  };

  // ── Card ──
  const Card = ({ tac }) => {
    const teams = tac.teams || [];
    const shown = teams.slice(0, 3);
    const extra = teams.length - shown.length;
    return (
      <div className="card card-hover fade-in" style={{ cursor: 'pointer', display: 'flex', flexDirection: 'column' }}
           onClick={() => setSelected(tac)}>
        <div className="card-head" style={{ alignItems: 'flex-start' }}>
          <div className="card-title" style={{ fontFamily: 'var(--font-display, inherit)', fontSize: 17 }}>
            {tac.name}
          </div>
          <Pill kind="accent">{tac.categorie}</Pill>
        </div>
        <div style={{ margin: '10px 0' }}>
          <TacticDiagram diagram={tac.diagram} color="#CAFF33" />
        </div>
        <div className="card-sub" style={{ lineHeight: 1.45, minHeight: 38 }}>
          {truncate(tac.objectif, 110)}
        </div>
        <div className="row" style={{ flexWrap: 'wrap', gap: 5, marginTop: 10 }}>
          {shown.map((tm, i) => <span className="pill" key={i} style={{ fontSize: 11 }}>{tm}</span>)}
          {extra > 0 && <span className="pill" style={{ fontSize: 11 }}>+{extra}</span>}
          {teams.length === 0 && <span className="card-sub" style={{ fontSize: 11 }}>—</span>}
        </div>
      </div>
    );
  };

  return (
    <div className="page">
      <div className="page-head">
        <h1 className="page-title">{fr ? 'Tactiques' : 'Tactics'}</h1>
        <div className="page-sub">
          {fr ? 'Catalogue de concepts tactiques et qui les emploie.'
              : 'A catalog of tactical concepts and who uses them.'}
        </div>
      </div>

      {!selected && (
        <React.Fragment>
          <div className="tab-strip" style={{ marginBottom: 14 }}>
            {sportTabs.map(s => (
              <button key={s.key}
                      className={'btn btn-sm ' + (activeSport === s.key ? 'btn-primary' : 'btn-ghost')}
                      onClick={() => switchSport(s.key)}>
                {s.label}
              </button>
            ))}
          </div>

          <div className="row" style={{ flexWrap: 'wrap', gap: 6, marginBottom: 12 }}>
            <button className={'pill ' + (cat === '__all__' ? 'pill-accent' : '')}
                    onClick={() => setCat('__all__')} style={{ cursor: 'pointer' }}>
              {fr ? 'Toutes' : 'All'}
            </button>
            {cats.map(c => (
              <button key={c} className={'pill ' + (cat === c ? 'pill-accent' : '')}
                      onClick={() => setCat(c)} style={{ cursor: 'pointer' }}>
                {c}
              </button>
            ))}
          </div>

          <div className="row" style={{ marginBottom: 16, alignItems: 'center', gap: 8 }}>
            <Icon name="search" size={16} />
            <input className="field" value={query}
                   onChange={e => setQuery(e.target.value)}
                   placeholder={fr ? 'Rechercher une tactique…' : 'Search a tactic…'}
                   style={{ maxWidth: 360 }} />
          </div>

          {filtered.length === 0 ? (
            <div className="card card-tight" style={{ textAlign: 'center', color: '#888' }}>
              {t.no_data || (fr ? 'Aucune tactique.' : 'No tactic.')}
            </div>
          ) : (
            <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))' }}>
              {filtered.map(tac => <Card key={tac.id} tac={tac} />)}
            </div>
          )}
        </React.Fragment>
      )}

      {selected && <Detail tac={selected} />}

      <div className="footer">{t.footer}</div>
    </div>
  );
}

Object.assign(window, { TacticsScreen });
