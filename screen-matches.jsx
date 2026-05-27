// screen-matches.jsx — Browse matches list with filters

const MatchesScreen = ({ lang, sport, openMatch }) => {
  const t = window.I18N[lang];
  const all = window.MATCHES[sport] || [];
  const [filter, setFilter] = React.useState('all');
  const [comp, setComp] = React.useState('all');

  const competitions = window.COMPETITIONS.filter(c => c.sports.includes(sport) || c.id === 'all');

  const filtered = all.filter(m => {
    if (filter !== 'all' && m.status !== filter) return false;
    return true;
  });

  return (
    <div className="page">
      <div className="page-head">
        <div>
          <h1 className="page-title">{t.matches}</h1>
          <p className="page-sub">
            {filtered.length} {filtered.length > 1
              ? (lang==='fr'?'matchs disponibles':'matches available')
              : (lang==='fr'?'match disponible':'match available')}
          </p>
        </div>
        <div className="row" style={{ gap: 10, alignItems: 'center' }}>
          <div className="tab-strip">
            {[
              {id:'all', label: lang==='fr'?'Tous':'All'},
              {id:'upcoming', label: t.upcoming},
              {id:'live', label: t.live},
              {id:'finished', label: t.finished},
            ].map(f => (
              <button key={f.id} data-active={filter === f.id} onClick={() => setFilter(f.id)}>
                {f.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Competition chips */}
      <div className="row" style={{ flexWrap: 'wrap', gap: 6, marginBottom: 22 }}>
        {competitions.map(c => (
          <button key={c.id}
                  className="pill"
                  onClick={() => setComp(c.id)}
                  style={{
                    cursor: 'pointer',
                    background: comp === c.id ? 'var(--accent)' : '#131313',
                    color: comp === c.id ? 'var(--accent-ink)' : '#aaa',
                    borderColor: comp === c.id ? 'transparent' : 'var(--border-strong)',
                  }}>
            {lang === 'fr' ? c.fr : c.en}
          </button>
        ))}
      </div>

      <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: 16 }}>
        {filtered.length === 0 && (
          <div className="card" style={{ gridColumn: '1 / -1', textAlign: 'center', padding: 60, color: '#666' }}>
            {t.no_data}
          </div>
        )}
        {filtered.map((m, i) => (
          <div key={m.id} className="fade-in" style={{ animationDelay: `${i*.06}s` }}>
            <MatchCard match={m} lang={lang}
                       onClick={() => openMatch(m.id, m.status === 'finished' ? 'post' : 'pre')} />
          </div>
        ))}
      </div>

      <div className="footer">{t.footer}</div>
    </div>
  );
};

Object.assign(window, { MatchesScreen });
