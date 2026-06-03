// screen-dashboard.jsx — Welcome dashboard with KPIs and recent/upcoming matches

const DashboardScreen = ({ lang, sport, setRoute, openMatch }) => {
  const t = window.I18N[lang];
  const matches = window.MATCHES[sport] || [];
  const upcoming = matches.filter(m => m.status === 'upcoming' || m.status === 'live').slice(0, 2);
  const recent = matches.filter(m => m.status === 'finished').slice(0, 2);

  // KPI drill-down state + real breakdowns computed from injected data
  const [openKpi, setOpenKpi] = React.useState(null);

  const allMatches = [].concat(
    window.MATCHES.football || [], window.MATCHES.basket || [], window.MATCHES.rugby || []
  );
  const finishedAll = allMatches.filter(m => m.status === 'finished');

  // Matches analysed, broken down by competition
  const byComp = {};
  finishedAll.forEach(m => { byComp[m.competition] = (byComp[m.competition] || 0) + 1; });
  const compRows = Object.entries(byComp).sort((a, b) => b[1] - a[1]);
  const totalAnalysed = finishedAll.length;

  // Accuracy breakdown (illustrative model metrics, stable values)
  const accRows = [
    { k: lang==='fr'?'Verdict correct':'Correct verdict', n: 5, d: 7 },
    { k: lang==='fr'?'Vainqueur exact':'Exact winner', n: 6, d: 7 },
    { k: lang==='fr'?'Score exact':'Exact score', n: 2, d: 7 },
    { k: lang==='fr'?'Écart ±1 but':'Margin ±1', n: 5, d: 7 },
  ];

  // Competitions list with sport tag + counts
  const sportOfComp = {};
  ['football','basket','rugby'].forEach(sp => (window.MATCHES[sp]||[]).forEach(m => { sportOfComp[m.competition] = sp; }));
  const compList = Object.keys(byComp).sort();

  const fmtKpi = (key) => {
    if (key === 'matches') return {
      title: t.matches_analyzed,
      rows: compRows.map(([c, n]) => ({ label: c, val: n })),
      foot: lang==='fr' ? `${totalAnalysed} matchs terminés dans la base` : `${totalAnalysed} finished matches on record`,
    };
    if (key === 'accuracy') return {
      title: t.avg_accuracy,
      rows: accRows.map(r => ({ label: r.k, val: `${r.n}/${r.d}`, pct: Math.round(r.n/r.d*100) })),
      foot: lang==='fr' ? 'Sur les 7 dernières analyses post-match' : 'Over the last 7 post-match analyses',
    };
    if (key === 'comps') return {
      title: t.competitions,
      rows: compList.map(c => ({ label: c, val: ({football:'⚽',basket:'🏀',rugby:'🏉'})[sportOfComp[c]] || '' })),
      foot: lang==='fr' ? `${compList.length} compétitions suivies` : `${compList.length} competitions tracked`,
    };
    return {
      title: t.saved_reports,
      rows: finishedAll.slice(0, 8).map(m => ({ label: `${m.home.name} – ${m.away.name}`, val: m.score ? `${m.score.home}–${m.score.away}` : '' })),
      foot: lang==='fr' ? 'Rapports post-match exportables' : 'Exportable post-match reports',
    };
  };

  return (
    <div className="page">
      <div className="page-head">
        <div>
          <h1 className="page-title">{t.welcome}</h1>
          <p className="page-sub">{t.dashboard_sub}</p>
        </div>
        <div className="row" style={{ gap: 10 }}>
          <button className="btn btn-ghost">
            <Icon name="download" size={14} /> {t.export_pdf}
          </button>
          <button className="btn btn-primary">
            <Icon name="sparkle" size={14} /> {t.new_analysis}
          </button>
        </div>
      </div>

      {/* KPI row — cliquable pour le détail */}
      <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', marginBottom: 24 }}>
        <div className="card card-tight card-hover fade-in" style={{ animationDelay: '0s', cursor: 'pointer' }}
             onClick={() => setOpenKpi('matches')}>
          <Stat label={t.matches_analyzed} value="247" delta="+18 " deltaKind="up" />
          <div className="progress" style={{ marginTop: 12 }}>
            <span style={{ width: '72%' }} />
          </div>
          <div style={{ fontSize: 11, color: '#666', marginTop: 6, display: 'flex', justifyContent: 'space-between' }}>
            <span>{t.this_month}</span>
            <span style={{ color: 'var(--accent)' }}>{lang==='fr'?'détails':'details'} →</span>
          </div>
        </div>
        <div className="card card-tight card-hover fade-in" style={{ animationDelay: '.08s', cursor: 'pointer' }}
             onClick={() => setOpenKpi('accuracy')}>
          <Stat label={t.avg_accuracy} value="78" suffix="%" delta="+4.2 " deltaKind="up" />
          <div className="progress" style={{ marginTop: 12 }}>
            <span style={{ width: '78%' }} />
          </div>
          <div style={{ fontSize: 11, color: '#666', marginTop: 6, display: 'flex', justifyContent: 'space-between' }}>
            <span>{t.vs_last}</span>
            <span style={{ color: 'var(--accent)' }}>{lang==='fr'?'détails':'details'} →</span>
          </div>
        </div>
        <div className="card card-tight card-hover fade-in" style={{ animationDelay: '.16s', cursor: 'pointer' }}
             onClick={() => setOpenKpi('comps')}>
          <Stat label={t.competitions} value={String(compList.length)} delta={`${['football','basket','rugby'].filter(s=>(window.MATCHES[s]||[]).length).length} actifs`} deltaKind="up" />
          <div className="row" style={{ marginTop: 12, flexWrap: 'wrap', gap: 4 }}>
            {compList.slice(0, 7).map(c => (
              <span key={c} className="pill" style={{padding: '2px 7px'}}>{c.length > 10 ? c.slice(0,9)+'…' : c}</span>
            ))}
          </div>
        </div>
        <div className="card card-tight card-hover fade-in" style={{ animationDelay: '.24s', cursor: 'pointer' }}
             onClick={() => setOpenKpi('reports')}>
          <Stat label={t.saved_reports} value={String(finishedAll.length)} delta="+6 " deltaKind="up" />
          <div className="row" style={{ marginTop: 12, alignItems: 'center', gap: 6 }}>
            <Icon name="download" size={14} />
            <span style={{fontSize: 11, color: '#888'}}>{lang==='fr'?'cliquer pour la liste':'click for the list'}</span>
          </div>
        </div>
      </div>

      {/* KPI drill-down modal */}
      {openKpi && (() => {
        const info = fmtKpi(openKpi);
        return (
          <div onClick={() => setOpenKpi(null)}
               style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,.6)', zIndex: 60,
                        display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20 }}>
            <div className="card fade-in" onClick={e => e.stopPropagation()}
                 style={{ maxWidth: 560, width: '100%', maxHeight: '80vh', overflowY: 'auto' }}>
              <div className="card-head">
                <h3 className="card-title">{info.title}</h3>
                <button className="btn btn-ghost btn-sm" onClick={() => setOpenKpi(null)}>
                  <Icon name="close" size={14} />
                </button>
              </div>
              <div className="col" style={{ gap: 8 }}>
                {info.rows.length === 0 && <div style={{ color: '#666', fontSize: 13 }}>{t.no_data}</div>}
                {info.rows.map((r, i) => (
                  <div key={i} className="tile" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    <div className="row" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
                      <span className="kv-key" style={{ textTransform: 'none', fontSize: 13 }}>{r.label}</span>
                      <span className="kv-val" style={{ fontFamily: 'var(--font-display)', letterSpacing: '.04em' }}>{r.val}</span>
                    </div>
                    {typeof r.pct === 'number' && (
                      <div className="progress"><span style={{ width: `${r.pct}%` }} /></div>
                    )}
                  </div>
                ))}
              </div>
              <div style={{ fontSize: 11, color: '#666', marginTop: 12 }}>{info.foot}</div>
            </div>
          </div>
        );
      })()}

      <div className="grid" style={{ gridTemplateColumns: 'minmax(0, 2fr) minmax(0, 1fr)', gap: 18 }}>
        {/* Upcoming + Recent */}
        <div className="col">
          <div className="card">
            <div className="card-head">
              <div>
                <h3 className="card-title">{t.upcoming}</h3>
                <p className="card-sub">{t.upcoming_sub}</p>
              </div>
              <button className="btn btn-ghost btn-sm" onClick={() => setRoute('matches')}>
                {lang==='fr'?'Tout voir':'View all'} <Icon name="arrow" size={12} />
              </button>
            </div>
            <div className="col" style={{ gap: 12 }}>
              {upcoming.length === 0 && <div style={{color:'#666', fontSize: 13}}>{t.no_data}</div>}
              {upcoming.map((m, i) => (
                <div key={m.id} style={{ animationDelay: `${.1 + i*.06}s` }}>
                  <MatchCard match={m} lang={lang} onClick={() => openMatch(m.id, 'pre')} />
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="card-head">
              <div>
                <h3 className="card-title">{t.recent}</h3>
                <p className="card-sub">{t.recent_sub}</p>
              </div>
              <button className="btn btn-ghost btn-sm" onClick={() => setRoute('history')}>
                {lang==='fr'?'Tout voir':'View all'} <Icon name="arrow" size={12} />
              </button>
            </div>
            <div className="col" style={{ gap: 12 }}>
              {recent.length === 0 && <div style={{color:'#666', fontSize: 13}}>{t.no_data}</div>}
              {recent.map(m => (
                <MatchCard key={m.id} match={m} lang={lang} onClick={() => openMatch(m.id, 'post')} />
              ))}
            </div>
          </div>
        </div>

        {/* Right column */}
        <div className="col">
          <div className="card">
            <div className="card-head">
              <h3 className="card-title">{lang === 'fr' ? 'Précision IA' : 'AI Accuracy'}</h3>
              <Pill kind="accent">7 {lang==='fr'?'derniers':'last'}</Pill>
            </div>
            <Gauge value={78} />
            <div className="tile" style={{ marginTop: 16 }}>
              <div className="tile-row">
                <span className="kv-key">{lang==='fr'?'Verdict correct':'Correct verdict'}</span>
                <span className="kv-val">5 / 7</span>
              </div>
              <div className="tile-row">
                <span className="kv-key">{lang==='fr'?'Score exact':'Exact score'}</span>
                <span className="kv-val">2 / 7</span>
              </div>
              <div className="tile-row">
                <span className="kv-key">{lang==='fr'?'Vainqueur':'Winner'}</span>
                <span className="kv-val">6 / 7</span>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-head">
              <h3 className="card-title">{lang === 'fr' ? 'Action rapide' : 'Quick action'}</h3>
            </div>
            <div className="col" style={{ gap: 8 }}>
              {[
                { icon: 'sparkle', label: t.new_analysis, route: 'matches' },
                { icon: 'matches', label: lang==='fr'?'Comparer 2 équipes':'Compare 2 teams', route: 'compare' },
                { icon: 'target', label: lang==='fr'?'Simuler un onze':'Simulate a lineup', route: 'simulator' },
                { icon: 'trend', label: lang==='fr'?'Tendances de la saison':'Season trends', route: 'trends' },
              ].map((q, i) => (
                <button key={i} className="btn btn-ghost" style={{ width: '100%', justifyContent: 'flex-start' }}
                        onClick={() => setRoute(q.route)}>
                  <Icon name={q.icon} size={14} /> {q.label}
                  <Icon name="chevron" size={14} style={{ marginLeft: 'auto', color: '#555' }} />
                </button>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="card-head">
              <h3 className="card-title">{lang === 'fr' ? 'État de la connexion' : 'Connection status'}</h3>
            </div>
            <div className="tile">
              <div className="tile-row">
                <span className="kv-key">{lang==='fr'?'Clé API Claude':'Claude API key'}</span>
                <Pill kind="finished">✓ OK</Pill>
              </div>
              <div className="tile-row">
                <span className="kv-key">{lang==='fr'?'Source de données':'Data source'}</span>
                <span className="kv-val">Opta · v3.2</span>
              </div>
              <div className="tile-row">
                <span className="kv-key">{lang==='fr'?'Dernière synchro':'Last sync'}</span>
                <span className="kv-val">{lang==='fr'?'il y a 2 min':'2 min ago'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="footer">{t.footer}</div>
    </div>
  );
};

Object.assign(window, { DashboardScreen });
