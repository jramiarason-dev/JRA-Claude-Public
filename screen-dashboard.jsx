// screen-dashboard.jsx — Welcome dashboard with KPIs and recent/upcoming matches

const DashboardScreen = ({ lang, sport, setRoute, openMatch }) => {
  const t = window.I18N[lang];
  const matches = window.MATCHES[sport] || [];
  const upcoming = matches.filter(m => m.status === 'upcoming' || m.status === 'live').slice(0, 2);
  const recent = matches.filter(m => m.status === 'finished').slice(0, 2);

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

      {/* KPI row */}
      <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', marginBottom: 24 }}>
        <div className="card card-tight fade-in" style={{ animationDelay: '0s' }}>
          <Stat label={t.matches_analyzed} value="247" delta="+18 " deltaKind="up" />
          <div className="progress" style={{ marginTop: 12 }}>
            <span style={{ width: '72%' }} />
          </div>
          <div style={{ fontSize: 11, color: '#666', marginTop: 6 }}>{t.this_month}</div>
        </div>
        <div className="card card-tight fade-in" style={{ animationDelay: '.08s' }}>
          <Stat label={t.avg_accuracy} value="78" suffix="%" delta="+4.2 " deltaKind="up" />
          <div className="progress" style={{ marginTop: 12 }}>
            <span style={{ width: '78%' }} />
          </div>
          <div style={{ fontSize: 11, color: '#666', marginTop: 6 }}>{t.vs_last}</div>
        </div>
        <div className="card card-tight fade-in" style={{ animationDelay: '.16s' }}>
          <Stat label={t.competitions} value="14" delta="3 actives" deltaKind="up" />
          <div className="row" style={{ marginTop: 12, flexWrap: 'wrap', gap: 4 }}>
            {['L1','PL','UCL','LaLiga','Bun','T14','NBA'].map(c => (
              <span key={c} className="pill" style={{padding: '2px 7px'}}>{c}</span>
            ))}
          </div>
        </div>
        <div className="card card-tight fade-in" style={{ animationDelay: '.24s' }}>
          <Stat label={t.saved_reports} value="42" delta="+6 " deltaKind="up" />
          <div className="row" style={{ marginTop: 12, alignItems: 'center', gap: 6 }}>
            <Icon name="download" size={14} />
            <span style={{fontSize: 11, color: '#888'}}>3 {lang==='fr'?'téléchargés':'downloaded'}</span>
          </div>
        </div>
      </div>

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
                { icon: 'sparkle', label: t.new_analysis },
                { icon: 'matches', label: lang==='fr'?'Comparer 2 équipes':'Compare 2 teams' },
                { icon: 'target', label: lang==='fr'?'Simuler un onze':'Simulate a lineup' },
                { icon: 'trend', label: lang==='fr'?'Tendances de la saison':'Season trends' },
              ].map((q, i) => (
                <button key={i} className="btn btn-ghost" style={{ width: '100%', justifyContent: 'flex-start' }}>
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
