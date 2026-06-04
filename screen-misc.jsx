// screen-misc.jsx — History, Analysis, Settings screens

const HistoryScreen = ({ lang, sport, openMatch }) => {
  const t = window.I18N[lang];
  const all = window.MATCHES[sport] || [];
  const finished = all.filter(m => m.status === 'finished');

  return (
    <div className="page">
      <div className="page-head">
        <div>
          <h1 className="page-title">{t.history}</h1>
          <p className="page-sub">{lang === 'fr' ? 'Vos analyses post-match archivées' : 'Your archived post-match analyses'}</p>
        </div>
        <div className="row" style={{ gap: 10 }}>
          <button className="btn btn-ghost"><Icon name="download" size={14} /> {lang==='fr'?'Tout exporter':'Export all'}</button>
        </div>
      </div>

      <div className="card" style={{padding: 0}}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border)' }}>
              {[t.matches, lang==='fr'?'Compétition':'Competition', lang==='fr'?'Date':'Date', lang==='fr'?'Résultat':'Result', t.verdict, ''].map(h => (
                <th key={h} style={{
                  textAlign: 'left', padding: '14px 16px',
                  fontSize: 10, letterSpacing: '.1em',
                  color: '#666', fontWeight: 700, textTransform: 'uppercase',
                }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {finished.map((m, i) => (
              <tr key={m.id} style={{ borderBottom: '1px solid var(--border)' }}
                  className="card-hover" onClick={() => openMatch(m.id, 'post')}>
                <td style={{ padding: '14px 16px' }}>
                  <div className="row" style={{gap: 10, alignItems: 'center'}}>
                    <Crest code={m.home.code} color={m.home.color} />
                    <span style={{fontSize: 13, color: '#888'}}>vs</span>
                    <Crest code={m.away.code} color={m.away.color} />
                    <span style={{ fontWeight: 600, color: '#fff', marginLeft: 4 }}>
                      {m.home.name} – {m.away.name}
                    </span>
                  </div>
                </td>
                <td style={{ padding: '14px 16px', fontSize: 12, color: 'var(--accent)' }}>{m.competition}</td>
                <td style={{ padding: '14px 16px', fontSize: 12, color: '#aaa' }}>{m.date}</td>
                <td style={{ padding: '14px 16px' }}>
                  <span style={{ fontFamily: 'var(--font-display)', fontSize: 18, letterSpacing: '.04em', color: '#fff' }}>
                    {m.score.home} – {m.score.away}
                  </span>
                </td>
                <td style={{ padding: '14px 16px', fontSize: 12, color: '#bbb', maxWidth: 320 }}>
                  <span style={{
                    display: 'inline-block',
                    maxWidth: 340,
                    whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
                  }}>
                    {(lang === 'fr' ? m.verdict_fr : m.verdict_en)}
                  </span>
                </td>
                <td style={{ padding: '14px 16px', textAlign: 'right' }}>
                  <button className="btn btn-ghost btn-sm">
                    {t.review} <Icon name="chevron" size={12} />
                  </button>
                </td>
              </tr>
            ))}
            {finished.length === 0 && (
              <tr><td colSpan="6" style={{ padding: 60, textAlign: 'center', color: '#666' }}>{t.no_data}</td></tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="footer">{t.footer}</div>
    </div>
  );
};

const AnalysisScreen = ({ lang, sport, setRoute }) => {
  const t = window.I18N[lang];
  return (
    <div className="page">
      <div className="page-head">
        <div>
          <h1 className="page-title">{t.analysis}</h1>
          <p className="page-sub">{lang==='fr'?'Lancez une analyse tactique personnalisée':'Run a custom tactical analysis'}</p>
        </div>
      </div>

      <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 16 }}>
        {[
          { icon: 'matches', title: lang==='fr'?'Analyser un match':'Analyse a match', desc: lang==='fr'?'Choisissez un match passé ou à venir':'Pick a past or upcoming match', cta: setRoute.bind(null, 'matches') },
          { icon: 'target',  title: lang==='fr'?'Comparer deux équipes':'Compare two teams', desc: lang==='fr'?'Forme, stats, head-to-head':'Form, stats, head-to-head', cta: setRoute.bind(null, 'compare') },
          { icon: 'sparkle', title: lang==='fr'?'Simulateur tactique':'Tactical simulator', desc: lang==='fr'?'Testez un onze, une formation':'Test a lineup, a formation', cta: setRoute.bind(null, 'simulator') },
          { icon: 'trend',   title: lang==='fr'?'Tendances saisonnières':'Season trends', desc: lang==='fr'?'Analyse longitudinale des KPIs':'Longitudinal KPI analysis', cta: setRoute.bind(null, 'trends') },
        ].map((c, i) => (
          <div key={i} className="card card-hover fade-in" style={{ animationDelay: `${i*.06}s` }} onClick={c.cta}>
            <div className="brand-mark" style={{ background: '#1a1a1a', color: 'var(--accent)', marginBottom: 16 }}>
              <Icon name={c.icon} size={18} />
            </div>
            <h3 className="card-title" style={{ marginBottom: 6 }}>{c.title}</h3>
            <p style={{ fontSize: 13, color: '#888', margin: 0, lineHeight: 1.6 }}>{c.desc}</p>
            <div style={{ marginTop: 18, fontSize: 12, color: 'var(--accent)', fontWeight: 700, letterSpacing: '.06em', textTransform: 'uppercase' }}>
              {lang==='fr'?'Démarrer':'Start'} →
            </div>
          </div>
        ))}
      </div>

      <div className="footer">{t.footer}</div>
    </div>
  );
};

const SettingsScreen = ({ lang, setLang, sport, setSport }) => {
  const t = window.I18N[lang];
  const [apiKey, setApiKey] = React.useState('sk-ant-•••••••••••••••••••••••••••2f4');
  const [notifPre, setNotifPre] = React.useState(true);
  const [notifPost, setNotifPost] = React.useState(true);
  const [theme, setTheme] = React.useState('lime');

  return (
    <div className="page" style={{maxWidth: 900}}>
      <div className="page-head">
        <div>
          <h1 className="page-title">{t.settings}</h1>
          <p className="page-sub">{lang==='fr'?'Préférences globales de CoachIQ':'Global CoachIQ preferences'}</p>
        </div>
        <button className="btn btn-primary">{t.save}</button>
      </div>

      <div className="col" style={{ gap: 16 }}>
        {/* API */}
        <div className="card">
          <div className="card-head">
            <h3 className="card-title">{t.api_key}</h3>
            <Pill kind="finished">✓ {t.api_key_set}</Pill>
          </div>
          <div className="row" style={{ gap: 10 }}>
            <input className="field" style={{
              background: '#0e0e0e', flex: 1, padding: '10px 12px',
              border: '1px solid var(--border)', borderRadius: 8, color: '#fff',
              fontFamily: 'ui-monospace, Menlo, monospace', fontSize: 13,
            }} type="text" value={apiKey} onChange={e => setApiKey(e.target.value)} />
            <button className="btn btn-ghost">{lang==='fr'?'Régénérer':'Regenerate'}</button>
          </div>
          <p style={{ fontSize: 11, color: '#666', marginTop: 10 }}>
            {lang==='fr'?'Votre clé Anthropic est stockée chiffrée et n\'est jamais partagée.':'Your Anthropic key is encrypted at rest and never shared.'}
          </p>
        </div>

        {/* Preferences */}
        <div className="card">
          <div className="card-head">
            <h3 className="card-title">{lang === 'fr' ? 'Préférences' : 'Preferences'}</h3>
          </div>
          <div className="col" style={{ gap: 16 }}>
            <div className="row" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div className="kv-val">{t.language}</div>
                <div className="kv-key">{lang === 'fr' ? 'Langue de l\'interface' : 'Interface language'}</div>
              </div>
              <div className="lang-toggle">
                <button data-active={lang === 'fr'} onClick={() => setLang('fr')}>Français</button>
                <button data-active={lang === 'en'} onClick={() => setLang('en')}>English</button>
              </div>
            </div>

            <div style={{height: 1, background: 'var(--border)'}} />

            <div className="row" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div className="kv-val">{t.preferred_sport}</div>
                <div className="kv-key">{lang==='fr'?'Sport affiché par défaut':'Default sport shown'}</div>
              </div>
              <div className="sport-tabs" style={{ width: 'auto' }}>
                {window.SPORTS.map(s => (
                  <button key={s.id}
                          className="sport-tab"
                          data-active={sport === s.id}
                          onClick={() => setSport(s.id)}
                          style={{ minWidth: 80 }}>
                    <span className="emoji">{s.emoji}</span>
                    <span>{lang === 'fr' ? s.label_fr : s.label_en}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Notifications */}
        <div className="card">
          <div className="card-head">
            <h3 className="card-title">{t.notifications}</h3>
          </div>
          <div className="col" style={{ gap: 14 }}>
            <div className="row" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div className="kv-val">{t.notif_pre}</div>
                <div className="kv-key">{lang==='fr'?'Push + email':'Push + email'}</div>
              </div>
              <Switch on={notifPre} onClick={() => setNotifPre(!notifPre)} />
            </div>
            <div style={{height: 1, background: 'var(--border)'}} />
            <div className="row" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div className="kv-val">{t.notif_post}</div>
                <div className="kv-key">{lang==='fr'?'Email seulement':'Email only'}</div>
              </div>
              <Switch on={notifPost} onClick={() => setNotifPost(!notifPost)} />
            </div>
          </div>
        </div>
      </div>

      <div className="footer">{t.footer}</div>
    </div>
  );
};

Object.assign(window, { HistoryScreen, AnalysisScreen, SettingsScreen });
