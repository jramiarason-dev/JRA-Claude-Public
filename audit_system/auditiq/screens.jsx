// screens.jsx — AuditIQ screens
// Exposes: IntroSplash, Topbar, Sidebar, DashboardScreen, AgentScreen, AuditsScreen,
//          DocumentsScreen, HistoryScreen, SettingsScreen

var { useState, useEffect, useMemo, useRef } = React;

// ─── helpers ─────────────────────────────────────────────────────
const fmt = (s, vars) => Object.keys(vars || {}).reduce(
  (acc, k) => acc.replace(`{${k}}`, vars[k]), s);
const useT = (lang) => (key, vars) => fmt(window.AIQ.i18n[lang][key] || key, vars);

const Icon = ({ name, size = 16 }) => {
  const paths = {
    home:     "M3 12l9-9 9 9M5 10v10h14V10",
    grid:     "M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z",
    book:     "M4 4h12a4 4 0 0 1 4 4v12a4 4 0 0 0-4-4H4zM4 4v12h12",
    map:      "M9 20l-6 2V6l6-2 6 2 6-2v16l-6 2-6-2zM9 4v16M15 6v16",
    chart:    "M3 17l6-6 4 4 8-8M21 7h-5M21 7v5",
    docs:     "M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9zM14 3v6h6M8 13h8M8 17h5",
    history:  "M3 12a9 9 0 1 0 3-6.7M3 4v5h5",
    settings: "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06A2 2 0 1 1 4.27 16.96l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09a1.65 1.65 0 0 0 1.51-1A1.65 1.65 0 0 0 4.27 7.27l-.06-.06A2 2 0 1 1 7.04 4.38l.06.06a1.65 1.65 0 0 0 1.82.33h.05a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z",
    search:   "M11 19a8 8 0 1 1 5.3-14M21 21l-4.3-4.3",
    plus:     "M12 5v14M5 12h14",
    bell:     "M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0",
    burger:   "M4 6h16M4 12h16M4 18h16",
    arrow:    "M5 12h14M13 5l7 7-7 7",
    chevron:  "M9 18l6-6-6-6",
    sparkle:  "M12 3v6m0 6v6M3 12h6m6 0h6M5.6 5.6l4.2 4.2m4.4 4.4l4.2 4.2M5.6 18.4l4.2-4.2m4.4-4.4l4.2-4.2",
    download: "M12 4v12m-5-5l5 5 5-5M5 20h14",
    file:     "M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9zM14 3v6h6",
    check:    "M5 12l5 5 9-11",
    close:    "M6 6l12 12M18 6L6 18",
    pin:      "M12 22s7-7 7-12a7 7 0 1 0-14 0c0 5 7 12 7 12zM12 11a2 2 0 1 0 0-4 2 2 0 0 0 0 4z",
    play:     "M5 3l14 9-14 9V3z",
    pulse:    "M3 12h4l3-9 4 18 3-9h4",
  };
  return (
    <svg viewBox="0 0 24 24" width={size} height={size} fill="none"
         stroke="currentColor" strokeWidth="1.7"
         strokeLinecap="round" strokeLinejoin="round">
      <path d={paths[name] || paths.home} />
    </svg>
  );
};

// ─── COVER / SIGN-IN ─────────────────────────────────────────────
const SignIn = ({ lang, setLang, onEnter }) => {
  const t = useT(lang);
  const [fading, setFading] = useState(false);
  const [email, setEmail] = useState("lucas.brunner@helvetia-private.ch");
  const [pwd, setPwd] = useState("auditiq-demo");
  const [remember, setRemember] = useState(true);
  const [busy, setBusy] = useState(false);

  const L = (fr, en) => (lang === 'fr' ? fr : en);

  const handleEnter = () => {
    if (fading || busy) return;
    setBusy(true);
    // brief "authenticating" beat, then fade to the app
    setTimeout(() => {
      setFading(true);
      setTimeout(() => onEnter(), 750);
    }, 720);
  };

  const submit = (e) => { e.preventDefault(); handleEnter(); };

  return (
    <div className={`aiq-cover ${fading ? 'fading' : ''}`}>
      <div className="aiq-blob b1" />
      <div className="aiq-blob b2" />

      {/* ── Left: brand + rotating earth ── */}
      <div className="aiq-cover-hero">
        <div className="aiq-cover-brand">
          <div className="mark">A</div>
          <span className="nm">Audit<b>IQ</b></span>
          <span className="aiq-pill aiq-pill-indigo" style={{ marginLeft: 6 }}>Pro</span>
        </div>

        <div className="aiq-cover-globe">
          <window.AIQ_Globe size={340} />
        </div>

        <h1 className="aiq-cover-title" aria-label={t('brand')}>
          {L("Audit bancaire,", "Banking audit,")}<br />
          <span className="grad">{L("augmenté par l'IA.", "augmented by AI.")}</span>
        </h1>
        <p className="aiq-cover-tag">{t('intro_sub')}</p>

        <div className="aiq-cover-flags">
          {window.AIQ.jurisdictions.map(j => (
            <span key={j.id} className="fl" title={`${j[lang]} · ${j.regulator}`}>
              <span className="em">{j.flag}</span>{j.regulator}
            </span>
          ))}
        </div>
      </div>

      {/* ── Right: fake sign-in ── */}
      <div className="aiq-cover-auth">
        <div className="aiq-lang aiq-cover-lang">
          <button data-active={lang === 'fr'} onClick={() => setLang('fr')}>FR</button>
          <button data-active={lang === 'en'} onClick={() => setLang('en')}>EN</button>
        </div>

        <form className="aiq-signin" onSubmit={submit}>
          <div className="aiq-signin-head">
            <h2>{L("Connexion", "Sign in")}</h2>
            <p>{L("Accédez à votre espace d'audit sécurisé.",
                  "Access your secure audit workspace.")}</p>
          </div>

          <label className="aiq-signin-field">
            <span>{L("Adresse e-mail", "Email address")}</span>
            <div className="ip">
              <span className="ic">✉</span>
              <input type="email" value={email} autoComplete="username"
                     onChange={e => setEmail(e.target.value)} />
            </div>
          </label>

          <label className="aiq-signin-field">
            <span>{L("Mot de passe", "Password")}</span>
            <div className="ip">
              <span className="ic">🔒</span>
              <input type="password" value={pwd} autoComplete="current-password"
                     onChange={e => setPwd(e.target.value)} />
            </div>
          </label>

          <div className="aiq-signin-row">
            <label className="aiq-check" onClick={() => setRemember(!remember)}>
              <span className="box" data-on={remember}>{remember ? '✓' : ''}</span>
              {L("Se souvenir de moi", "Remember me")}
            </label>
            <a href="#" onClick={e => e.preventDefault()}>{L("Mot de passe oublié ?", "Forgot password?")}</a>
          </div>

          <button type="submit" className={`aiq-signin-btn ${busy ? 'busy' : ''}`} disabled={busy}>
            {busy ? (
              <React.Fragment>
                {L("Authentification", "Authenticating")}
                <span className="aiq-typing"><span /><span /><span /></span>
              </React.Fragment>
            ) : (
              <React.Fragment>{L("Se connecter", "Sign in")} <span className="arr">→</span></React.Fragment>
            )}
          </button>

          <div className="aiq-signin-or"><span>{L("ou", "or")}</span></div>

          <div className="aiq-signin-sso">
            <button type="button" onClick={handleEnter}>
              <span className="g">🔑</span> {L("SSO entreprise", "Enterprise SSO")}
            </button>
            <button type="button" onClick={handleEnter}>
              <span className="g">🪪</span> {L("Carte d'accès", "Access card")}
            </button>
          </div>

          <p className="aiq-signin-foot">
            <span className="aiq-pill aiq-pill-green" style={{ fontSize: 9 }}>
              <span className="dot" /> {L("Connexion chiffrée", "Encrypted session")}
            </span>
            {t('footer')}
          </p>
        </form>
      </div>
    </div>
  );
};

// ─── SIDEBAR ─────────────────────────────────────────────────────
const Sidebar = ({ route, setRoute, lang, open, onClose }) => {
  const t = useT(lang);
  const navItem = (id, icon, badge) => (
    <button className="aiq-nav-item"
            data-active={route === id}
            onClick={() => { setRoute(id); onClose && onClose(); }}>
      <span className="ic"><Icon name={icon} size={14} /></span>
      <span className="lbl">{t(id)}</span>
      {badge && <span className="aiq-pill aiq-pill-indigo" style={{padding:'2px 7px', fontSize: 10}}>{badge}</span>}
    </button>
  );
  const agentItem = (id, color) => {
    const agent = window.AIQ.agents.find(a => a.id === id);
    return (
      <button className="aiq-nav-item"
              data-active={route === id}
              onClick={() => { setRoute(id); onClose && onClose(); }}
              style={{ "--agent-color": color }}>
        <span className="ic agent">{agent.icon}</span>
        <span className="lbl">{t(id === 'agent1' ? 'regulatory'
                                : id === 'agent2' ? 'audit_plan'
                                : 'audit_report')}</span>
        {route === id && <span className="dot" style={{background: color}} />}
      </button>
    );
  };
  return (
    <aside className={`aiq-sidebar ${open ? 'open' : ''}`}>
      <div className="aiq-brand">
        <div className="mark">A</div>
        <div className="name">Audit<b>IQ</b></div>
        <span className="badge">Pro</span>
      </div>

      <div className="aiq-nav-title">{lang === 'fr' ? 'Menu' : 'Menu'}</div>
      {navItem('dashboard', 'grid')}
      {navItem('audits', 'book', '4')}

      <div className="aiq-nav-title">{t('agents_label')}</div>
      {agentItem('agent1', '#22d3a5')}
      {agentItem('agent2', '#4f7ef8')}
      {agentItem('agent3', '#a78bfa')}

      <div className="aiq-nav-title">{t('tools_label')}</div>
      {navItem('documents', 'docs')}
      {navItem('history', 'history')}
      {navItem('settings', 'settings')}

      <div className="aiq-sidebar-foot">
        <div className="aiq-user">
          <div className="av">LB</div>
          <div className="meta">
            <div className="nm">L. Brunner</div>
            <div className="ro">{lang === 'fr' ? 'Auditeur senior' : 'Senior auditor'}</div>
          </div>
          <button className="aiq-icon-btn" style={{position:'relative'}}>
            <Icon name="bell" size={14} />
            <span className="badge-dot" />
          </button>
        </div>
      </div>
    </aside>
  );
};

// ─── TOPBAR ──────────────────────────────────────────────────────
const Topbar = ({ route, lang, setLang, onMenu }) => {
  const t = useT(lang);
  return (
    <header className="aiq-topbar">
      <button className="aiq-menu-btn" onClick={onMenu}><Icon name="burger" size={16} /></button>
      <div className="crumbs">
        <span>AuditIQ</span>
        <span className="sep">/</span>
        <span className="here">{
          t(route === 'agent1' ? 'regulatory'
            : route === 'agent2' ? 'audit_plan'
            : route === 'agent3' ? 'audit_report'
            : route)
        }</span>
      </div>
      <div className="spacer" />
      <div className="aiq-search">
        <span className="ic"><Icon name="search" size={14} /></span>
        <input placeholder={t('search')} />
      </div>
      <div className="aiq-lang">
        <button data-active={lang === 'fr'} onClick={() => setLang('fr')}>FR</button>
        <button data-active={lang === 'en'} onClick={() => setLang('en')}>EN</button>
      </div>
      <button className="aiq-icon-btn" style={{position:'relative'}}>
        <Icon name="bell" size={15} />
        <span className="badge-dot" />
      </button>
      <button className="aiq-btn aiq-btn-primary aiq-btn-sm">
        <Icon name="plus" size={13} /> {t('new_audit')}
      </button>
    </header>
  );
};

// ─── DASHBOARD ──────────────────────────────────────────────────
const StatTile = ({ label, value, delta, deltaKind = "up", meta }) => (
  <div className="aiq-stat">
    <div className="lbl">{label}</div>
    <div className="val">{value}</div>
    {delta && (
      <div className={`delta ${deltaKind}`}>
        {deltaKind === "up" ? "▲" : deltaKind === "down" ? "▼" : "—"} {delta}
      </div>
    )}
    {meta && <div className="meta">{meta}</div>}
  </div>
);

const AuditCard = ({ a, lang, t, onOpen }) => {
  const jurs = a.jurisdictions.map(j => window.AIQ.jurisdictions.find(x => x.id === j));
  const sev = a.severity;
  const statusPill = a.status === 'active'
    ? <span className="aiq-pill aiq-pill-indigo"><span className="dot" /> {t('status_active')}</span>
    : a.status === 'review'
      ? <span className="aiq-pill aiq-pill-orange"><span className="dot" /> {t('status_review')}</span>
      : <span className="aiq-pill aiq-pill-green"><span className="dot" /> {t('status_closed')}</span>;
  return (
    <div className="aiq-audit-card" onClick={onOpen}>
      <div className="id">{a.id}</div>
      <div className="subj">
        <span className={`aiq-sev-bar ${sev}`} />
        {a[`subject_${lang}`]}
      </div>
      <div className="jur-row">
        {jurs.map(j => <span key={j.id} title={j[lang]}>{j.flag}</span>)}
      </div>
      <div className="meta-row">
        {statusPill}
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
          <Icon name="pin" size={12} /> {a.owner}
        </span>
      </div>
      <div className="prog-row">
        <div className="aiq-progress"><span style={{ width: `${a.progress}%` }} /></div>
        <span>{a.progress}%</span>
      </div>
    </div>
  );
};

const DashboardScreen = ({ lang, setRoute }) => {
  const t = useT(lang);
  const audits = window.AIQ.audits;
  const active = audits.filter(a => a.status !== 'closed').slice(0, 4);
  const recentActivity = window.AIQ.activity.slice(0, 5);
  const upcoming = audits.filter(a => a.due_in > 0 && a.due_in <= 40)
    .sort((a, b) => a.due_in - b.due_in).slice(0, 3);

  return (
    <div className="aiq-page">
      <div className="aiq-page-head">
        <div>
          <h1 className="aiq-h1">{t('welcome')}</h1>
          <p className="aiq-sub">{t('welcome_sub')}</p>
        </div>
        <div className="aiq-row">
          <button className="aiq-btn aiq-btn-ghost" onClick={() => setRoute('audits')}>
            {t('view_all')} {t('audits')}
          </button>
          <button className="aiq-btn aiq-btn-primary">
            <Icon name="plus" size={13} /> {t('new_audit')}
          </button>
        </div>
      </div>

      {/* KPI row */}
      <div className="aiq-stat-row">
        <StatTile label={t('kpi_audits')}        value="4"  delta="+1"   deltaKind="up"   meta={t('this_month')} />
        <StatTile label={t('kpi_completed')}     value="12" delta="+3"   deltaKind="up"   meta={t('vs_last_q')} />
        <StatTile label={t('kpi_pending')}       value="17" delta="-2"   deltaKind="down" meta={lang==='fr'?'cette semaine':'this week'} />
        <StatTile label={t('kpi_jurisdictions')} value="6"  delta=""     deltaKind="flat" meta={lang==='fr'?'CH · SG · HK · BS · EU · UK':'CH · SG · HK · BS · EU · UK'} />
      </div>

      <div className="aiq-grid" style={{ gridTemplateColumns: 'minmax(0, 2fr) minmax(0, 1fr)' }}>
        {/* Left */}
        <div className="aiq-col">
          <div className="aiq-card">
            <div className="aiq-card-head">
              <div>
                <h2 className="aiq-h2">{lang === 'fr' ? 'Audits en cours' : 'Active audits'}</h2>
                <p className="aiq-sub" style={{ marginTop: 4 }}>
                  {active.length} {lang === 'fr' ? 'audits en cours' : 'audits in progress'}
                </p>
              </div>
              <button className="aiq-btn aiq-btn-ghost aiq-btn-sm" onClick={() => setRoute('audits')}>
                {t('view_all')} →
              </button>
            </div>
            <div className="aiq-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))' }}>
              {active.map(a => (
                <AuditCard key={a.id} a={a} lang={lang} t={t}
                           onOpen={() => setRoute('agent2')} />
              ))}
            </div>
          </div>

          {/* Agents */}
          <div className="aiq-card">
            <div className="aiq-card-head">
              <h2 className="aiq-h2">{t('agents_label')}</h2>
              <span className="aiq-pill aiq-pill-indigo">Claude · Sonnet 4.5</span>
            </div>
            <div className="aiq-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))' }}>
              {window.AIQ.agents.map(ag => (
                <button key={ag.id} className="aiq-agent-tile"
                        style={{ "--agent-color": ag.color }}
                        onClick={() => setRoute(ag.id)}>
                  <div className="head">
                    <div className="ic">{ag.icon}</div>
                    <div>
                      <div className="num">{ag.id.toUpperCase()}</div>
                      <h3>{t(ag.title_key).replace(/^Agent \d+ — /, '')}</h3>
                    </div>
                  </div>
                  <p>{t(ag.desc_key)}</p>
                  <span className="aiq-pill aiq-pill-green">
                    <span className="dot" /> {lang === 'fr' ? 'Disponible' : 'Available'}
                  </span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right */}
        <div className="aiq-col">
          <div className="aiq-card">
            <div className="aiq-card-head">
              <h2 className="aiq-h2">{t('next_milestones')}</h2>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {upcoming.map(a => (
                <div key={a.id}
                     style={{ padding: 12, border: '1px solid var(--aiq-border)',
                              borderRadius: 10, background: 'rgba(255,255,255,.02)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <span className="aiq-pill aiq-pill-indigo" style={{ fontSize: 9 }}>{a.id}</span>
                    <span className={`aiq-pill ${a.due_in <= 5 ? 'aiq-pill-red' : a.due_in <= 15 ? 'aiq-pill-orange' : ''}`}>
                      {t('due_in_days', { n: a.due_in })}
                    </span>
                  </div>
                  <div style={{ fontSize: 13, fontWeight: 600, marginTop: 6, color: 'var(--aiq-text)' }}>
                    {a[`subject_${lang}`]}
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--aiq-muted)', marginTop: 4 }}>
                    {a.owner} · {a.due}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="aiq-card">
            <div className="aiq-card-head">
              <h2 className="aiq-h2">{t('recent_activity')}</h2>
            </div>
            <div>
              {recentActivity.map((a, i) => (
                <div key={i} className="aiq-activity-row">
                  <div className="ic">{a.icon}</div>
                  <div>
                    <div className="who">{a.who}</div>
                    <div className="what">{a[`what_${lang}`]}</div>
                  </div>
                  <div className="when">{a.ago}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="aiq-card">
            <div className="aiq-card-head">
              <h2 className="aiq-h2">{lang === 'fr' ? 'Couverture juridictions' : 'Jurisdiction coverage'}</h2>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {window.AIQ.jurisdictions.map(j => {
                const count = audits.filter(a => a.jurisdictions.includes(j.id)).length;
                const pct = (count / 4) * 100;
                return (
                  <div key={j.id}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                      <span style={{ fontSize: 13 }}>
                        {j.flag} {j[lang]} <span style={{ color: 'var(--aiq-faint)', fontSize: 11 }}>· {j.regulator}</span>
                      </span>
                      <span style={{ fontSize: 12, color: 'var(--aiq-muted)', fontVariantNumeric: 'tabular-nums' }}>{count}</span>
                    </div>
                    <div className="aiq-progress" style={{ height: 4 }}>
                      <span style={{ width: `${pct}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      <div className="aiq-footer">{t('footer')}</div>
    </div>
  );
};

// ─── AGENT SCREEN (generic, 3 agents differ by content) ─────────
const AgentScreen = ({ lang, agentId, setRoute }) => {
  const t = useT(lang);
  const agent = window.AIQ.agents.find(a => a.id === agentId);
  const [subject, setSubject] = useState(window.AIQ.topics[0].id);
  const [scope, setScope] = useState("");
  const [jurs, setJurs] = useState(["ch", "sg"]);
  const [gen, setGen] = useState({ state: 'idle', progress: 0 });

  // Generated content state
  const [output, setOutput] = useState(null);

  const subjectObj = window.AIQ.topics.find(x => x.id === subject);

  const toggleJur = (id) => {
    setJurs(prev => prev.includes(id) ? prev.filter(j => j !== id) : [...prev, id]);
  };

  const start = () => {
    setGen({ state: 'running', progress: 0 });
    setOutput(null);
    // Fake progressive generation
    let p = 0;
    const tick = setInterval(() => {
      p += 8 + Math.random() * 14;
      if (p >= 100) {
        clearInterval(tick);
        setGen({ state: 'done', progress: 100 });
        // Populate sample output by agent
        if (agentId === 'agent1') {
          setOutput({ kind: 'framework', regs: window.AIQ.regulations.aml.filter(r => jurs.includes(r.jur)) });
        } else if (agentId === 'agent2') {
          setOutput({ kind: 'plan', steps: buildPlan(lang, subject, jurs) });
        } else {
          setOutput({ kind: 'report', findings: window.AIQ.findings });
        }
      } else {
        setGen({ state: 'running', progress: Math.min(p, 95) });
      }
    }, 280);
  };

  return (
    <div className="aiq-page">
      <div className="aiq-page-head">
        <div>
          <p className="aiq-sub" style={{ marginBottom: 6, color: agent.color, letterSpacing: '.1em', textTransform: 'uppercase', fontWeight: 700, fontSize: 11 }}>
            {agent.icon} {agentId.toUpperCase()}
          </p>
          <h1 className="aiq-h1">{t(agent.title_key)}</h1>
          <p className="aiq-sub">{t(agent.desc_key)}</p>
        </div>
        <div className="aiq-row">
          <span className="aiq-pill aiq-pill-green">
            <span className="dot" /> {t('api_key_set')}
          </span>
          <span className="aiq-pill aiq-pill-indigo">Claude Sonnet 4.5</span>
        </div>
      </div>

      <div className="aiq-gen-split">
        {/* Left — Input form */}
        <div className="aiq-card">
          <div className="aiq-card-head">
            <h2 className="aiq-h2">{lang === 'fr' ? 'Paramètres' : 'Parameters'}</h2>
          </div>

          <div className="aiq-field">
            <label>{t('audit_subject')}</label>
            <select className="aiq-select" value={subject} onChange={e => setSubject(e.target.value)}>
              {window.AIQ.topics.map(top => (
                <option key={top.id} value={top.id}>{top[lang]}</option>
              ))}
            </select>
          </div>

          <div className="aiq-field">
            <label>{t('audit_scope_opt')}</label>
            <textarea className="aiq-textarea"
                      placeholder={t('audit_scope_ph')}
                      value={scope}
                      onChange={e => setScope(e.target.value)} />
            <span className="hint">{lang === 'fr' ? '(optionnel)' : '(optional)'}</span>
          </div>

          <div className="aiq-field">
            <label>{t('jurisdiction')}</label>
            <div className="aiq-chip-grid">
              {window.AIQ.jurisdictions.map(j => (
                <button key={j.id}
                        className="aiq-chip-check"
                        data-checked={jurs.includes(j.id)}
                        onClick={() => toggleJur(j.id)}
                        type="button">
                  <span style={{ fontSize: 14 }}>{j.flag}</span>
                  {j[lang]}
                  <span className="check">{jurs.includes(j.id) ? '✓' : ''}</span>
                </button>
              ))}
            </div>
          </div>

          {agentId !== 'agent1' && (
            <div className="aiq-field">
              <label style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span className="aiq-pill aiq-pill-green" style={{ padding: '2px 7px', fontSize: 9 }}>✓</span>
                {agentId === 'agent2' ? t('framework_ready') : t('plan_ready')}
              </label>
              <span className="hint" style={{fontSize: 12}}>
                {lang === 'fr' ? 'Sortie de l\'agent précédent disponible' : 'Previous agent output available'}
              </span>
            </div>
          )}

          <div style={{ display: 'flex', gap: 10, marginTop: 18 }}>
            <button className="aiq-btn aiq-btn-primary aiq-btn-lg"
                    style={{ flex: 1 }}
                    disabled={!jurs.length || gen.state === 'running'}
                    onClick={start}>
              {gen.state === 'running' ? (
                <React.Fragment>
                  {t('generating')}
                  <span className="aiq-typing">
                    <span /><span /><span />
                  </span>
                </React.Fragment>
              ) : (
                <React.Fragment>
                  <Icon name="sparkle" size={14} />
                  {agentId === 'agent1' ? t('generate_framework')
                    : agentId === 'agent2' ? t('generate_plan')
                    : t('generate_report')}
                </React.Fragment>
              )}
            </button>
          </div>
          {gen.state === 'running' && (
            <div style={{ marginTop: 14 }}>
              <div className="aiq-progress">
                <span style={{ width: `${gen.progress}%` }} />
              </div>
              <div style={{ fontSize: 11, color: 'var(--aiq-faint)', marginTop: 6, letterSpacing: '.08em', textTransform: 'uppercase', fontWeight: 600 }}>
                {Math.round(gen.progress)}% · {lang === 'fr' ? 'analyse multi-juridictions…' : 'multi-jurisdiction analysis…'}
              </div>
            </div>
          )}
        </div>

        {/* Right — Output */}
        <div className="aiq-card aiq-output-card">
          <div className="aiq-card-head">
            <h2 className="aiq-h2">{t('output')}</h2>
            {gen.state === 'done' && (
              <div className="aiq-row">
                {agentId === 'agent1' && <button className="aiq-btn aiq-btn-ghost aiq-btn-sm"><Icon name="download" size={12} /> {t('download_word')}</button>}
                {agentId === 'agent2' && <button className="aiq-btn aiq-btn-ghost aiq-btn-sm"><Icon name="download" size={12} /> {t('download_pptx')}</button>}
                {agentId === 'agent2' && <button className="aiq-btn aiq-btn-ghost aiq-btn-sm"><Icon name="download" size={12} /> {t('download_xlsx')}</button>}
                {agentId === 'agent3' && <button className="aiq-btn aiq-btn-ghost aiq-btn-sm"><Icon name="download" size={12} /> {t('download_word')}</button>}
                {agentId === 'agent3' && <button className="aiq-btn aiq-btn-ghost aiq-btn-sm"><Icon name="download" size={12} /> {t('download_pdf')}</button>}
              </div>
            )}
          </div>

          {gen.state === 'idle' && (
            <div className="aiq-output-empty">
              <div className="ic">{agent.icon}</div>
              <div style={{ fontSize: 14, color: 'var(--aiq-text-2)', fontWeight: 600, marginBottom: 6 }}>
                {lang === 'fr' ? 'Aucune génération' : 'No generation yet'}
              </div>
              <div style={{ fontSize: 12, color: 'var(--aiq-muted)' }}>
                {lang === 'fr' ? 'Configurez les paramètres puis lancez l\'analyse.'
                              : 'Set the parameters then run the analysis.'}
              </div>
            </div>
          )}

          {gen.state === 'running' && (
            <div className="aiq-output-empty">
              <div className="ic" style={{ animation: 'pulse 1.8s ease-in-out infinite' }}>{agent.icon}</div>
              <div style={{ fontSize: 14, color: 'var(--aiq-text)', fontWeight: 600 }}>
                {t('generating')}
              </div>
              <div style={{ fontSize: 12, color: 'var(--aiq-muted)', marginTop: 6 }}>
                {lang === 'fr' ? 'Claude analyse votre demande…' : 'Claude is analysing your request…'}
              </div>
            </div>
          )}

          {gen.state === 'done' && output && (
            <OutputView lang={lang} output={output} subject={subjectObj[lang]} jurs={jurs} t={t} />
          )}
        </div>
      </div>

      <div className="aiq-footer">{t('footer')}</div>
    </div>
  );
};

// Build a fake plan based on subject + jurisdictions
const buildPlan = (lang, subject, jurs) => {
  const STEPS_FR = [
    { h: "Cadrage du périmètre", p: "Délimiter les entités, processus et systèmes concernés." },
    { h: "Identification des risques", p: "Cartographier les risques inhérents au sujet d'audit." },
    { h: "Tests de conception des contrôles", p: "Évaluer l'adéquation des contrôles documentés." },
    { h: "Tests d'efficacité opérationnelle", p: "Échantillonnage de transactions et revue d'évidence." },
    { h: "Évaluation des écarts", p: "Quantifier les non-conformités et hiérarchiser." },
    { h: "Synthèse & recommandations", p: "Formaliser les constats et préparer le rapport exécutif." },
  ];
  const STEPS_EN = [
    { h: "Scope framing", p: "Define the entities, processes and systems in scope." },
    { h: "Risk identification", p: "Map inherent risks tied to the audit topic." },
    { h: "Control design testing", p: "Assess whether documented controls are adequate." },
    { h: "Operating effectiveness testing", p: "Transaction sampling and evidence review." },
    { h: "Gap assessment", p: "Quantify non-conformities and prioritise." },
    { h: "Synthesis & recommendations", p: "Formalise findings and prepare the executive report." },
  ];
  const list = lang === 'fr' ? STEPS_FR : STEPS_EN;
  return list.map((s, i) => ({
    n: i + 1, h: s.h, p: s.p,
    duration: lang === 'fr' ? `${2 + i} jours` : `${2 + i} days`,
    auditor: ['L. Brunner', 'M. Tanaka', 'A. Cheung'][i % 3],
  }));
};

const OutputView = ({ lang, output, subject, jurs, t }) => {
  if (output.kind === 'framework') {
    return (
      <div className="aiq-prev-list">
        <div style={{ fontSize: 12, color: 'var(--aiq-muted)', marginBottom: 8 }}>
          {output.regs.length} {lang === 'fr' ? 'textes applicables' : 'applicable texts'} · {subject}
        </div>
        {output.regs.map((r, i) => {
          const jur = window.AIQ.jurisdictions.find(x => x.id === r.jur);
          return (
            <div key={i} className="aiq-prev-item" style={{ animationDelay: `${i * 0.08}s` }}>
              <span className="jur-tag">{jur.flag} {jur.id.toUpperCase()}</span>
              <span className="code">{r.code}</span>
              <div className="ttl">{r[lang]}</div>
              <div className="meta">
                <span>{jur.regulator}</span>
                <span>{lang === 'fr' ? 'MàJ' : 'Updated'} : {r.updated}</span>
                <span className={`aiq-pill aiq-pill-${r.severity === 'critical' ? 'red' : r.severity === 'high' ? 'orange' : 'yellow'}`}
                      style={{padding: '1px 7px', fontSize: 9}}>
                  {t(r.severity)}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    );
  }
  if (output.kind === 'plan') {
    return (
      <div>
        <div style={{ fontSize: 12, color: 'var(--aiq-muted)', marginBottom: 10 }}>
          {output.steps.length} {lang === 'fr' ? 'étapes' : 'steps'} · {subject}
        </div>
        {output.steps.map((s, i) => (
          <div key={s.n} className="aiq-step" style={{ animationDelay: `${i * 0.08}s` }}>
            <div className="num">{s.n}</div>
            <div className="body">
              <h4>{s.h}</h4>
              <p>{s.p}</p>
              <div className="meta">
                <span>⏱ {s.duration}</span>
                <span>👤 {s.auditor}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }
  if (output.kind === 'report') {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        <div style={{ fontSize: 12, color: 'var(--aiq-muted)', marginBottom: 8 }}>
          {output.findings.length} {lang === 'fr' ? 'constats' : 'findings'} · {subject}
        </div>
        {output.findings.map((f, i) => (
          <div key={i} className="aiq-finding" data-sev={f.sev} style={{ animationDelay: `${i * 0.08}s` }}>
            <div className="ico">{f.sev[0].toUpperCase()}</div>
            <div className="body">
              <h4>{f[`title_${lang}`]}</h4>
              <p>{f[`desc_${lang}`]}</p>
              <div className="jurs">
                {f.jur.map(jid => window.AIQ.jurisdictions.find(x => x.id === jid).flag)}
              </div>
            </div>
            <span className={`aiq-pill aiq-pill-${f.sev === 'critical' ? 'red' : f.sev === 'high' ? 'orange' : f.sev === 'medium' ? 'yellow' : 'green'}`}>
              {t(f.sev)}
            </span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

// ─── AUDITS LIST ─────────────────────────────────────────────────
const AuditsScreen = ({ lang, setRoute }) => {
  const t = useT(lang);
  const [filter, setFilter] = useState('all');
  const all = window.AIQ.audits;
  const items = filter === 'all' ? all : all.filter(a => a.status === filter);
  return (
    <div className="aiq-page">
      <div className="aiq-page-head">
        <div>
          <h1 className="aiq-h1">{lang === 'fr' ? 'Tous les audits' : 'All audits'}</h1>
          <p className="aiq-sub">{items.length} {lang === 'fr' ? 'audits' : 'audits'}</p>
        </div>
        <div className="aiq-row">
          <div className="aiq-lang" style={{ padding: 3 }}>
            {['all','active','review','closed'].map(f => (
              <button key={f}
                      data-active={filter === f}
                      onClick={() => setFilter(f)}>
                {f === 'all' ? (lang==='fr'?'Tous':'All')
                  : f === 'active' ? t('status_active')
                  : f === 'review' ? t('status_review')
                  : t('status_closed')}
              </button>
            ))}
          </div>
          <button className="aiq-btn aiq-btn-primary aiq-btn-sm">
            <Icon name="plus" size={13} /> {t('new_audit')}
          </button>
        </div>
      </div>

      <div className="aiq-card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="aiq-table">
          <thead>
            <tr>
              <th>{lang === 'fr' ? 'Identifiant' : 'ID'}</th>
              <th>{t('audit_subject')}</th>
              <th>{t('jurisdiction')}</th>
              <th>{lang === 'fr' ? 'Responsable' : 'Owner'}</th>
              <th>{lang === 'fr' ? 'Échéance' : 'Due'}</th>
              <th>{lang === 'fr' ? 'Sévérité' : 'Severity'}</th>
              <th>{lang === 'fr' ? 'Progression' : 'Progress'}</th>
              <th>{t('status_label')}</th>
            </tr>
          </thead>
          <tbody>
            {items.map(a => {
              const jurs = a.jurisdictions.map(j => window.AIQ.jurisdictions.find(x => x.id === j));
              const statusPill = a.status === 'active'
                ? <span className="aiq-pill aiq-pill-indigo"><span className="dot" /> {t('status_active')}</span>
                : a.status === 'review'
                  ? <span className="aiq-pill aiq-pill-orange"><span className="dot" /> {t('status_review')}</span>
                  : <span className="aiq-pill aiq-pill-green"><span className="dot" /> {t('status_closed')}</span>;
              return (
                <tr key={a.id} onClick={() => setRoute('agent2')}>
                  <td><span className="id">{a.id}</span></td>
                  <td style={{ maxWidth: 320, color: 'var(--aiq-text)' }}>{a[`subject_${lang}`]}</td>
                  <td>{jurs.map(j => <span key={j.id} style={{ marginRight: 4, fontSize: 16 }}>{j.flag}</span>)}</td>
                  <td>{a.owner}</td>
                  <td style={{ whiteSpace: 'nowrap' }}>{a.due}</td>
                  <td>
                    <span style={{ display: 'inline-flex', alignItems: 'center' }}>
                      <span className={`aiq-sev-bar ${a.severity}`} />
                      {t(a.severity)}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, minWidth: 120 }}>
                      <div className="aiq-progress" style={{ flex: 1 }}>
                        <span style={{ width: `${a.progress}%` }} />
                      </div>
                      <span style={{ fontVariantNumeric: 'tabular-nums', fontSize: 12, color: 'var(--aiq-muted)' }}>{a.progress}%</span>
                    </div>
                  </td>
                  <td>{statusPill}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="aiq-footer">{t('footer')}</div>
    </div>
  );
};

// ─── DOCUMENTS ───────────────────────────────────────────────────
const DocumentsScreen = ({ lang }) => {
  const t = useT(lang);
  return (
    <div className="aiq-page">
      <div className="aiq-page-head">
        <div>
          <h1 className="aiq-h1">{t('documents')}</h1>
          <p className="aiq-sub">{t('docs_sub')}</p>
        </div>
      </div>

      <div className="aiq-card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="aiq-table">
          <thead>
            <tr>
              <th>{lang === 'fr' ? 'Fichier' : 'File'}</th>
              <th>{t('doc_type')}</th>
              <th>{t('doc_audit')}</th>
              <th>{t('doc_date')}</th>
              <th>{t('doc_size')}</th>
              <th>{t('doc_status')}</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {window.AIQ.documents.map(d => (
              <tr key={d.id}>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                    <span style={{ fontSize: 18 }}>
                      {d.type === 'Word' ? '📄' : d.type === 'PowerPoint' ? '📊' : '📈'}
                    </span>
                    <span style={{ color: 'var(--aiq-text)', fontWeight: 600 }}>{d.name}</span>
                  </div>
                </td>
                <td>{d.type}</td>
                <td><span className="id">{d.audit}</span></td>
                <td>{d.date}</td>
                <td style={{ fontVariantNumeric: 'tabular-nums' }}>{d.size}</td>
                <td>
                  {d.status === 'approved'
                    ? <span className="aiq-pill aiq-pill-green"><span className="dot" /> {t('approved')}</span>
                    : <span className="aiq-pill aiq-pill-orange"><span className="dot" /> {t('review')}</span>}
                </td>
                <td>
                  <button className="aiq-icon-btn">
                    <Icon name="download" size={14} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="aiq-footer">{t('footer')}</div>
    </div>
  );
};

// ─── HISTORY ─────────────────────────────────────────────────────
const HistoryScreen = ({ lang }) => {
  const t = useT(lang);
  const closed = window.AIQ.audits.filter(a => a.status === 'closed');
  return (
    <div className="aiq-page">
      <div className="aiq-page-head">
        <div>
          <h1 className="aiq-h1">{t('history')}</h1>
          <p className="aiq-sub">{lang === 'fr' ? 'Audits clôturés et archivés' : 'Closed and archived audits'}</p>
        </div>
      </div>

      <div className="aiq-card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="aiq-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>{t('audit_subject')}</th>
              <th>{t('jurisdiction')}</th>
              <th>{lang === 'fr' ? 'Clôturé le' : 'Closed on'}</th>
              <th>{lang === 'fr' ? 'Constats' : 'Findings'}</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {closed.map(a => {
              const jurs = a.jurisdictions.map(j => window.AIQ.jurisdictions.find(x => x.id === j));
              return (
                <tr key={a.id}>
                  <td><span className="id">{a.id}</span></td>
                  <td style={{ color: 'var(--aiq-text)' }}>{a[`subject_${lang}`]}</td>
                  <td>{jurs.map(j => <span key={j.id} style={{ marginRight: 4, fontSize: 16 }}>{j.flag}</span>)}</td>
                  <td>{a.due}</td>
                  <td>4 {lang === 'fr' ? 'constats' : 'findings'}</td>
                  <td>
                    <button className="aiq-btn aiq-btn-ghost aiq-btn-sm">
                      {lang === 'fr' ? 'Revoir' : 'Review'} <Icon name="chevron" size={12} />
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="aiq-footer">{t('footer')}</div>
    </div>
  );
};

// ─── SETTINGS ────────────────────────────────────────────────────
const SettingsScreen = ({ lang, setLang }) => {
  const t = useT(lang);
  const [apiKey, setApiKey] = useState('sk-ant-•••••••••••••••••••••••••••f4e2');
  const [thinking, setThinking] = useState(true);
  const [model, setModel] = useState('sonnet-4-5');
  const [notif, setNotif] = useState(true);

  return (
    <div className="aiq-page" style={{ maxWidth: 920 }}>
      <div className="aiq-page-head">
        <div>
          <h1 className="aiq-h1">{t('settings')}</h1>
          <p className="aiq-sub">{lang === 'fr' ? 'Configuration de l\'instance AuditIQ' : 'AuditIQ instance configuration'}</p>
        </div>
        <button className="aiq-btn aiq-btn-primary">{lang === 'fr' ? 'Enregistrer' : 'Save'}</button>
      </div>

      <div className="aiq-col">
        <div className="aiq-card">
          <div className="aiq-card-head">
            <h2 className="aiq-h2">{t('api_key')}</h2>
            <span className="aiq-pill aiq-pill-green">
              <span className="dot" /> {t('api_key_set')}
            </span>
          </div>
          <div style={{ display: 'flex', gap: 10 }}>
            <input className="aiq-input" type="text"
                   value={apiKey} onChange={e => setApiKey(e.target.value)}
                   style={{ fontFamily: 'ui-monospace, Menlo, monospace' }} />
            <button className="aiq-btn aiq-btn-ghost">{lang === 'fr' ? 'Régénérer' : 'Regenerate'}</button>
          </div>
          <p style={{ fontSize: 11, color: 'var(--aiq-faint)', marginTop: 10 }}>
            {lang === 'fr'
              ? 'Votre clé Anthropic est chiffrée au repos. Variable d\'environnement : ANTHROPIC_API_KEY'
              : 'Your Anthropic key is encrypted at rest. Environment variable: ANTHROPIC_API_KEY'}
          </p>
        </div>

        <div className="aiq-card">
          <div className="aiq-card-head">
            <h2 className="aiq-h2">{lang === 'fr' ? 'Modèle & raisonnement' : 'Model & reasoning'}</h2>
          </div>

          <div className="aiq-setting">
            <div className="meta-l">
              <div className="nm">{t('model')}</div>
              <div className="ds">{lang === 'fr' ? 'Modèle Claude utilisé par les 3 agents' : 'Claude model used by all 3 agents'}</div>
            </div>
            <select className="aiq-select" value={model} onChange={e => setModel(e.target.value)} style={{ maxWidth: 240 }}>
              <option value="sonnet-4-5">Claude Sonnet 4.5 (recommandé)</option>
              <option value="opus-4">Claude Opus 4</option>
              <option value="haiku-4">Claude Haiku 4</option>
            </select>
          </div>

          <div className="aiq-setting">
            <div className="meta-l">
              <div className="nm">{t('thinking')}</div>
              <div className="ds">{t('thinking_desc')}</div>
            </div>
            <div className="aiq-switch" data-on={thinking} onClick={() => setThinking(!thinking)} />
          </div>
        </div>

        <div className="aiq-card">
          <div className="aiq-card-head">
            <h2 className="aiq-h2">{lang === 'fr' ? 'Apparence & langue' : 'Appearance & language'}</h2>
          </div>

          <div className="aiq-setting">
            <div className="meta-l">
              <div className="nm">{t('language')}</div>
              <div className="ds">{lang === 'fr' ? 'Langue de l\'interface et des livrables' : 'UI and document language'}</div>
            </div>
            <div className="aiq-lang">
              <button data-active={lang === 'fr'} onClick={() => setLang('fr')}>Français</button>
              <button data-active={lang === 'en'} onClick={() => setLang('en')}>English</button>
            </div>
          </div>

          <div className="aiq-setting">
            <div className="meta-l">
              <div className="nm">{lang === 'fr' ? 'Notifications email' : 'Email notifications'}</div>
              <div className="ds">{lang === 'fr' ? 'Rapports prêts, échéances proches' : 'Reports ready, due dates approaching'}</div>
            </div>
            <div className="aiq-switch" data-on={notif} onClick={() => setNotif(!notif)} />
          </div>
        </div>

        <div className="aiq-card">
          <div className="aiq-card-head">
            <h2 className="aiq-h2">{t('agent_status')}</h2>
          </div>
          <div className="aiq-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))' }}>
            {window.AIQ.agents.map(ag => (
              <div key={ag.id} className="aiq-status-tile">
                <div className="icb" style={{ background: `${ag.color}22`, color: ag.color }}>{ag.icon}</div>
                <div style={{ flex: 1 }}>
                  <div className="nm">{ag.id.toUpperCase()}</div>
                  <div className="st"><span className="live-dot" /> {lang === 'fr' ? 'Opérationnel' : 'Operational'}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="aiq-footer">{t('footer')}</div>
    </div>
  );
};

Object.assign(window, {
  AIQ_useT: useT,
  AIQ_SignIn: SignIn,
  AIQ_Sidebar: Sidebar,
  AIQ_Topbar: Topbar,
  AIQ_DashboardScreen: DashboardScreen,
  AIQ_AgentScreen: AgentScreen,
  AIQ_AuditsScreen: AuditsScreen,
  AIQ_DocumentsScreen: DocumentsScreen,
  AIQ_HistoryScreen: HistoryScreen,
  AIQ_SettingsScreen: SettingsScreen,
});
