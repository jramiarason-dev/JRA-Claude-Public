// screen-trends.jsx — Season longitudinal KPIs for a single team.
// Plots scored vs conceded over time + a results timeline.

const TrendsScreen = ({ lang, sport, setRoute }) => {
  const t = window.I18N[lang];
  const TS = window.TEAMSTATS || {};

  const teams = Object.entries(TS)
    .filter(([, v]) => v && v.sport === sport)
    .map(([k]) => k)
    .sort();

  const [team, setTeam] = React.useState(teams[0] || '');

  React.useEffect(() => {
    if (!teams.includes(team)) setTeam(teams[0] || '');
  }, [sport]); // eslint-disable-line

  const s = TS[team];
  const results = (s && Array.isArray(s.results)) ? s.results : [];

  const ACCENT = 'var(--accent)';
  const CONCEDED = '#3b82f6';

  const played = s ? (s.played || 0) : 0;
  const winPct = played ? Math.round(((s.w || 0) / played) * 100) : 0;
  const diff = s ? ((s.pf || 0) - (s.pa || 0)) : 0;

  // ── Standings row (football / Ligue 1 only) ────────────────
  const standRow = (() => {
    if (sport !== 'football') return null;
    const table = (window.STANDINGS && window.STANDINGS['Ligue 1']) || [];
    return table.find(r => r.team === team) || null;
  })();

  // ── Chart geometry ─────────────────────────────────────────
  const W = 480, H = 160, PAD_L = 28, PAD_R = 12, PAD_T = 14, PAD_B = 22;
  const innerW = W - PAD_L - PAD_R;
  const innerH = H - PAD_T - PAD_B;

  const n = results.length;
  const maxVal = Math.max(1, ...results.map(r => Math.max(r.gf || 0, r.ga || 0)));

  const xAt = (i) => n <= 1 ? PAD_L + innerW / 2 : PAD_L + (i / (n - 1)) * innerW;
  const yAt = (v) => PAD_T + innerH - (v / maxVal) * innerH;

  const lineFor = (key) => results.map((r, i) => `${xAt(i)},${yAt(r[key] || 0)}`).join(' ');
  const areaFor = (key) => {
    if (n === 0) return '';
    const pts = results.map((r, i) => `${xAt(i)},${yAt(r[key] || 0)}`).join(' ');
    return `${PAD_L + (n <= 1 ? innerW / 2 : 0)},${PAD_T + innerH} ${pts} ${xAt(n - 1)},${PAD_T + innerH}`;
  };

  const resColor = (r) => r === 'V' ? 'var(--accent)' : r === 'N' ? '#3a3a3a' : '#ef4444';
  const resTextColor = (r) => r === 'N' ? '#ccc' : '#0a0a0a';

  const Chip = ({ r }) => (
    <span style={{
      display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
      width: 22, height: 22, borderRadius: 6, fontSize: 11, fontWeight: 700,
      color: resTextColor(r), background: resColor(r),
    }}>{r}</span>
  );

  return (
    <div className="page fade-in">
      <div className="page-head">
        <div>
          <h1 className="page-title">{lang === 'fr' ? 'Tendances saisonnières' : 'Season trends'}</h1>
          <p className="page-sub">
            {lang === 'fr'
              ? "Évolution des performances d'une équipe sur la saison."
              : "A team's performance evolution across the season."}
          </p>
        </div>
      </div>

      {teams.length === 0 ? (
        <div className="card">{t.no_data}</div>
      ) : (
        <>
          <div className="card" style={{ marginBottom: 18 }}>
            <div className="kv-key" style={{ marginBottom: 6 }}>{lang === 'fr' ? 'Équipe' : 'Team'}</div>
            <select className="field" value={team} onChange={e => setTeam(e.target.value)}>
              {teams.map(tm => <option key={tm} value={tm}>{tm}</option>)}
            </select>
          </div>

          {!s ? (
            <div className="card">{t.no_data}</div>
          ) : (
            <>
              <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: 12, marginBottom: 18 }}>
                <div className="card card-tight"><Stat label={lang === 'fr' ? 'Joués' : 'Played'} value={played} /></div>
                <div className="card card-tight"><Stat label={lang === 'fr' ? 'Bilan (V-N-D)' : 'Record (W-D-L)'} value={`${s.w || 0}-${s.d || 0}-${s.l || 0}`} /></div>
                <div className="card card-tight"><Stat label={lang === 'fr' ? 'Pour' : 'For'} value={s.pf || 0} /></div>
                <div className="card card-tight"><Stat label={lang === 'fr' ? 'Contre' : 'Against'} value={s.pa || 0} /></div>
                <div className="card card-tight"><Stat label={lang === 'fr' ? 'Différence' : 'Diff'} value={`${diff > 0 ? '+' : ''}${diff}`} /></div>
                <div className="card card-tight"><Stat label={lang === 'fr' ? '% Victoires' : 'Win %'} value={winPct} suffix="%" /></div>
              </div>

              <div className="card" style={{ marginBottom: 18 }}>
                <div className="card-head">
                  <div>
                    <h3 className="card-title">{lang === 'fr' ? 'Marqués vs encaissés' : 'Scored vs conceded'}</h3>
                    <p className="card-sub">{lang === 'fr' ? 'Par match, dans l\'ordre chronologique' : 'Per match, chronological'}</p>
                  </div>
                  <div className="row" style={{ gap: 14, fontSize: 11, color: '#888' }}>
                    <span><span style={{ display: 'inline-block', width: 8, height: 8, borderRadius: 2, background: ACCENT, marginRight: 5 }} />{lang === 'fr' ? 'Marqués' : 'Scored'}</span>
                    <span><span style={{ display: 'inline-block', width: 8, height: 8, borderRadius: 2, background: CONCEDED, marginRight: 5 }} />{lang === 'fr' ? 'Encaissés' : 'Conceded'}</span>
                  </div>
                </div>

                {n === 0 ? (
                  <div style={{ color: '#666', fontSize: 13 }}>{t.no_data}</div>
                ) : (
                  <>
                    <svg viewBox={`0 0 ${W} ${H}`} width="100%" style={{ display: 'block' }} preserveAspectRatio="xMidYMid meet">
                      {/* baseline + max gridline */}
                      <line x1={PAD_L} y1={PAD_T + innerH} x2={W - PAD_R} y2={PAD_T + innerH} stroke="#2a2a2a" strokeWidth="1" />
                      <line x1={PAD_L} y1={PAD_T} x2={W - PAD_R} y2={PAD_T} stroke="#1a1a1a" strokeWidth="1" />
                      <text x={PAD_L - 6} y={PAD_T + innerH + 4} textAnchor="end" fontSize="9" fill="#666">0</text>
                      <text x={PAD_L - 6} y={PAD_T + 4} textAnchor="end" fontSize="9" fill="#666">{maxVal}</text>

                      {/* conceded area + line */}
                      <polygon points={areaFor('ga')} fill={CONCEDED} fillOpacity="0.08" />
                      <polyline points={lineFor('ga')} fill="none" stroke={CONCEDED} strokeWidth="2" strokeLinejoin="round" strokeLinecap="round" />
                      {/* scored area + line */}
                      <polygon points={areaFor('gf')} fill={ACCENT === 'var(--accent)' ? 'rgba(190,242,100,1)' : ACCENT} fillOpacity="0.10" />
                      <polyline points={lineFor('gf')} fill="none" stroke="var(--accent)" strokeWidth="2" strokeLinejoin="round" strokeLinecap="round" />

                      {/* dots */}
                      {results.map((r, i) => (
                        <g key={i}>
                          <circle cx={xAt(i)} cy={yAt(r.ga || 0)} r="2.5" fill={CONCEDED} />
                          <circle cx={xAt(i)} cy={yAt(r.gf || 0)} r="2.5" fill="var(--accent)" />
                        </g>
                      ))}

                      {/* start / end labels */}
                      <text x={PAD_L} y={H - 6} textAnchor="start" fontSize="9" fill="#777">{results[0].date || (lang === 'fr' ? 'Début' : 'Start')}</text>
                      {n > 1 && (
                        <text x={W - PAD_R} y={H - 6} textAnchor="end" fontSize="9" fill="#777">{results[n - 1].date || (lang === 'fr' ? 'Fin' : 'End')}</text>
                      )}
                    </svg>
                  </>
                )}
              </div>

              {standRow && (
                <div className="card" style={{ marginBottom: 18 }}>
                  <div className="card-head">
                    <h3 className="card-title">{lang === 'fr' ? 'Classement · Ligue 1' : 'Standings · Ligue 1'}</h3>
                  </div>
                  <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(110px, 1fr))', gap: 12 }}>
                    <div className="tile"><div className="kv-key">{lang === 'fr' ? 'Position' : 'Position'}</div><div className="kv-val" style={{ fontFamily: 'var(--font-display)', fontSize: 22, color: 'var(--accent)' }}>#{standRow.pos}</div></div>
                    <div className="tile"><div className="kv-key">{lang === 'fr' ? 'Points' : 'Points'}</div><div className="kv-val" style={{ fontFamily: 'var(--font-display)', fontSize: 22, color: '#fff' }}>{standRow.pts}</div></div>
                    <div className="tile"><div className="kv-key">{lang === 'fr' ? 'Différence' : 'Diff'}</div><div className="kv-val" style={{ fontFamily: 'var(--font-display)', fontSize: 22, color: '#fff' }}>{standRow.diff > 0 ? '+' : ''}{standRow.diff}</div></div>
                  </div>
                </div>
              )}

              <div className="card">
                <div className="card-head">
                  <h3 className="card-title">{lang === 'fr' ? 'Chronologie des résultats' : 'Results timeline'}</h3>
                  <div className="row" style={{ gap: 5 }}>
                    {(s.form || []).map((r, i) => <Chip key={i} r={r} />)}
                  </div>
                </div>
                {n === 0 ? (
                  <div style={{ color: '#666', fontSize: 13 }}>{t.no_data}</div>
                ) : (
                  <div className="col" style={{ gap: 8 }}>
                    {results.slice().reverse().map((r, i) => (
                      <div key={i} className="tile" style={{ display: 'grid', gridTemplateColumns: 'auto 1fr auto auto', gap: 12, alignItems: 'center' }}>
                        <span className="kv-key" style={{ whiteSpace: 'nowrap' }}>{r.date}</span>
                        <span style={{ fontSize: 13, color: '#bbb', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {lang === 'fr' ? 'vs' : 'vs'} {r.opp}
                        </span>
                        <span style={{ fontFamily: 'var(--font-display)', fontSize: 16, color: '#fff', letterSpacing: '.04em', fontVariantNumeric: 'tabular-nums' }}>
                          {r.gf} <span style={{ color: '#444' }}>–</span> {r.ga}
                        </span>
                        <Chip r={r.res} />
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </>
          )}
        </>
      )}

      <div className="footer">{t.footer}</div>
    </div>
  );
};

Object.assign(window, { TrendsScreen });
