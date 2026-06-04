// screen-compare.jsx — Head-to-head team comparator
// Compares two teams of the current sport across season KPIs + direct H2H.

const CompareScreen = ({ lang, sport, setRoute }) => {
  const t = window.I18N[lang];
  const TS = window.TEAMSTATS || {};

  const teams = Object.entries(TS)
    .filter(([, v]) => v && v.sport === sport)
    .map(([k]) => k)
    .sort();

  const [a, setA] = React.useState(teams[0] || '');
  const [b, setB] = React.useState(teams.find(x => x !== teams[0]) || teams[1] || teams[0] || '');

  // Keep selections valid if the sport (and thus team list) changes.
  React.useEffect(() => {
    if (!teams.includes(a)) setA(teams[0] || '');
    if (!teams.includes(b)) setB(teams.find(x => x !== (teams.includes(a) ? a : teams[0])) || teams[0] || '');
  }, [sport]); // eslint-disable-line

  const code = (name) => (name || '').replace(/[^A-Za-z]/g, '').slice(0, 3).toUpperCase() || '???';

  const colorOf = (name) => {
    const list = (window.MATCHES && window.MATCHES[sport]) || [];
    for (const m of list) {
      if (m.home && m.home.name === name && m.home.color) return m.home.color;
      if (m.away && m.away.name === name && m.away.color) return m.away.color;
    }
    return '#888';
  };

  const ACCENT = 'var(--accent)';
  const RIGHT = '#3b82f6';

  const sa = TS[a];
  const sb = TS[b];

  const formPoints = (form) => (form || []).reduce((acc, r) => acc + (r === 'V' ? 3 : r === 'N' ? 1 : 0), 0);
  const r2 = (n) => Math.round(n * 100) / 100;

  const metrics = (s) => {
    if (!s) return null;
    const p = s.played || 0;
    return {
      played: p,
      w: s.w || 0, d: s.d || 0, l: s.l || 0,
      pf: s.pf || 0, pa: s.pa || 0,
      winPct: p ? Math.round(((s.w || 0) / p) * 100) : 0,
      avgFor: p ? r2((s.pf || 0) / p) : 0,
      avgAgainst: p ? r2((s.pa || 0) / p) : 0,
      formPts: formPoints(s.form),
    };
  };

  const ma = metrics(sa);
  const mb = metrics(sb);

  const TwoSidedBar = ({ label, left, right, leftFmt, rightFmt }) => {
    const lv = Number(left) || 0;
    const rv = Number(right) || 0;
    const tot = lv + rv;
    const lPct = tot > 0 ? (lv / tot) * 100 : 50;
    const rPct = 100 - lPct;
    return (
      <div style={{ marginBottom: 14 }}>
        <div style={{
          textAlign: 'center', fontSize: 10, letterSpacing: '.12em',
          color: '#777', textTransform: 'uppercase', fontWeight: 700, marginBottom: 6,
        }}>{label}</div>
        <div className="row" style={{ alignItems: 'center', gap: 10 }}>
          <span style={{
            width: 56, textAlign: 'right', fontFamily: 'var(--font-display)',
            fontSize: 16, color: '#fff', fontVariantNumeric: 'tabular-nums',
          }}>{leftFmt != null ? leftFmt : lv}</span>
          <div style={{ flex: 1, display: 'flex', height: 8, borderRadius: 4, overflow: 'hidden', background: '#1a1a1a' }}>
            <div style={{ width: `${lPct}%`, background: ACCENT, transition: 'width .6s' }} />
            <div style={{ width: `${rPct}%`, background: RIGHT, transition: 'width .6s' }} />
          </div>
          <span style={{
            width: 56, textAlign: 'left', fontFamily: 'var(--font-display)',
            fontSize: 16, color: '#fff', fontVariantNumeric: 'tabular-nums',
          }}>{rightFmt != null ? rightFmt : rv}</span>
        </div>
      </div>
    );
  };

  const FormChips = ({ form }) => (
    <div className="row" style={{ gap: 5 }}>
      {(form || []).length === 0
        ? <span style={{ color: '#666', fontSize: 12 }}>—</span>
        : form.map((r, i) => (
          <span key={i} title={r} style={{
            display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
            width: 22, height: 22, borderRadius: 6, fontSize: 11, fontWeight: 700,
            color: r === 'N' ? '#ccc' : '#0a0a0a',
            background: r === 'V' ? 'var(--accent)' : r === 'N' ? '#3a3a3a' : '#ef4444',
          }}>{r}</span>
        ))}
    </div>
  );

  // Head-to-head finished matches between the two teams.
  const h2h = (() => {
    const list = (window.MATCHES && window.MATCHES[sport]) || [];
    return list.filter(m => {
      if (!m || m.status !== 'finished' || !m.score) return false;
      const names = [m.home && m.home.name, m.away && m.away.name];
      return names.includes(a) && names.includes(b);
    });
  })();

  const TeamHead = ({ name, align }) => (
    <div className="col" style={{ alignItems: 'center', gap: 8 }}>
      <Crest code={code(name)} color={colorOf(name)} />
      <div style={{
        fontFamily: 'var(--font-display)', fontSize: 15, color: '#fff',
        letterSpacing: '.03em', textAlign: 'center',
      }}>{name || '—'}</div>
    </div>
  );

  return (
    <div className="page fade-in">
      <div className="page-head">
        <div>
          <h1 className="page-title">{lang === 'fr' ? "Comparateur d'équipes" : 'Team comparator'}</h1>
          <p className="page-sub">
            {lang === 'fr'
              ? 'Confrontez deux équipes sur leurs indicateurs de saison.'
              : 'Compare two teams across their season indicators.'}
          </p>
        </div>
      </div>

      {teams.length < 2 ? (
        <div className="card">{t.no_data}</div>
      ) : (
        <>
          <div className="card" style={{ marginBottom: 18 }}>
            <div className="grid" style={{ gridTemplateColumns: '1fr 1fr', gap: 16 }}>
              <div>
                <div className="kv-key" style={{ marginBottom: 6 }}>{lang === 'fr' ? 'Équipe A' : 'Team A'}</div>
                <select className="field" value={a} onChange={e => setA(e.target.value)}>
                  {teams.map(tm => <option key={tm} value={tm}>{tm}</option>)}
                </select>
              </div>
              <div>
                <div className="kv-key" style={{ marginBottom: 6 }}>{lang === 'fr' ? 'Équipe B' : 'Team B'}</div>
                <select className="field" value={b} onChange={e => setB(e.target.value)}>
                  {teams.map(tm => <option key={tm} value={tm}>{tm}</option>)}
                </select>
              </div>
            </div>
          </div>

          {(!sa || !sb) ? (
            <div className="card">{t.no_data}</div>
          ) : (
            <>
              <div className="card" style={{
                marginBottom: 18,
                background: `linear-gradient(135deg, ${colorOf(a)}22, transparent 45%, transparent 55%, ${colorOf(b)}22)`,
              }}>
                <div className="grid" style={{ gridTemplateColumns: '1fr auto 1fr', gap: 16, alignItems: 'center' }}>
                  <TeamHead name={a} />
                  <div style={{ fontFamily: 'var(--font-display)', fontSize: 22, color: '#666', letterSpacing: '.12em' }}>VS</div>
                  <TeamHead name={b} />
                </div>
              </div>

              <div className="card" style={{ marginBottom: 18 }}>
                <div className="card-head">
                  <h3 className="card-title">{lang === 'fr' ? 'Indicateurs comparés' : 'Compared indicators'}</h3>
                  <div className="row" style={{ gap: 14, fontSize: 11, color: '#888' }}>
                    <span><span style={{ display: 'inline-block', width: 8, height: 8, borderRadius: 2, background: ACCENT, marginRight: 5 }} />{code(a)}</span>
                    <span><span style={{ display: 'inline-block', width: 8, height: 8, borderRadius: 2, background: RIGHT, marginRight: 5 }} />{code(b)}</span>
                  </div>
                </div>
                <TwoSidedBar label={lang === 'fr' ? 'Matchs joués' : 'Played'} left={ma.played} right={mb.played} />
                <TwoSidedBar label={lang === 'fr' ? 'Victoires' : 'Wins'} left={ma.w} right={mb.w} />
                <TwoSidedBar label={lang === 'fr' ? 'Nuls' : 'Draws'} left={ma.d} right={mb.d} />
                <TwoSidedBar label={lang === 'fr' ? 'Défaites' : 'Losses'} left={ma.l} right={mb.l} />
                <TwoSidedBar label={lang === 'fr' ? 'Pour' : 'For'} left={ma.pf} right={mb.pf} />
                <TwoSidedBar label={lang === 'fr' ? 'Contre' : 'Against'} left={ma.pa} right={mb.pa} />
                <TwoSidedBar label={lang === 'fr' ? '% Victoires' : 'Win %'} left={ma.winPct} right={mb.winPct} leftFmt={ma.winPct + '%'} rightFmt={mb.winPct + '%'} />
                <TwoSidedBar label={lang === 'fr' ? 'Moy. marqués' : 'Avg scored'} left={ma.avgFor} right={mb.avgFor} />
                <TwoSidedBar label={lang === 'fr' ? 'Moy. encaissés' : 'Avg conceded'} left={ma.avgAgainst} right={mb.avgAgainst} />
                <TwoSidedBar label={lang === 'fr' ? 'Points de forme' : 'Form points'} left={ma.formPts} right={mb.formPts} />
              </div>

              <div className="card" style={{ marginBottom: 18 }}>
                <div className="card-head">
                  <h3 className="card-title">{lang === 'fr' ? 'Forme récente' : 'Recent form'}</h3>
                </div>
                <div className="col" style={{ gap: 12 }}>
                  <div className="row" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: 13, color: '#fff', fontWeight: 600 }}>{a}</span>
                    <FormChips form={sa.form} />
                  </div>
                  <div className="row" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: 13, color: '#fff', fontWeight: 600 }}>{b}</span>
                    <FormChips form={sb.form} />
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="card-head">
                  <h3 className="card-title">{lang === 'fr' ? 'Confrontations directes' : 'Head-to-head'}</h3>
                  {h2h.length > 0 && <Pill kind="accent">{h2h.length}</Pill>}
                </div>
                {h2h.length === 0 ? (
                  <div style={{ color: '#666', fontSize: 13 }}>
                    {lang === 'fr' ? 'Aucune confrontation directe enregistrée' : 'No direct head-to-head on record'}
                  </div>
                ) : (
                  <div className="col" style={{ gap: 8 }}>
                    {h2h.map((m, i) => (
                      <div key={i} className="tile" style={{ display: 'grid', gridTemplateColumns: 'auto 1fr auto', gap: 12, alignItems: 'center' }}>
                        <span className="kv-key" style={{ whiteSpace: 'nowrap' }}>{m.date}</span>
                        <div style={{ textAlign: 'center' }}>
                          <span style={{ fontSize: 13, color: '#bbb' }}>{m.home.name}</span>
                          <span style={{ fontFamily: 'var(--font-display)', fontSize: 18, color: '#fff', margin: '0 12px', letterSpacing: '.04em' }}>
                            {m.score.home} <span style={{ color: '#444' }}>–</span> {m.score.away}
                          </span>
                          <span style={{ fontSize: 13, color: '#bbb' }}>{m.away.name}</span>
                        </div>
                        <span className="kv-key" style={{ whiteSpace: 'nowrap', color: 'var(--accent)' }}>{m.competition}</span>
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

Object.assign(window, { CompareScreen });
