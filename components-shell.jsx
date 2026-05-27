// components-shell.jsx — Sidebar, Topbar, Layout shell

const NAV = [
  { id: "dashboard", icon: "home" },
  { id: "matches",   icon: "matches", count: "12" },
  { id: "analysis",  icon: "analysis" },
  { id: "history",   icon: "history" },
  { id: "settings",  icon: "settings" },
];

const Sidebar = ({ sport, setSport, route, setRoute, lang, open, onClose }) => {
  const t = window.I18N[lang];
  return (
    <aside className={`sidebar ${open ? 'open' : ''}`}>
      <div className="brand">
        <div className="brand-mark">C</div>
        <div className="brand-name">COACH<span className="brand-suffix">IQ</span></div>
      </div>

      <div className="sport-tabs" role="tablist">
        {window.SPORTS.map(s => (
          <button key={s.id}
                  className="sport-tab"
                  data-active={sport === s.id}
                  onClick={() => setSport(s.id)}>
            <span className="emoji">{s.emoji}</span>
            <span>{lang === 'fr' ? s.label_fr : s.label_en}</span>
          </button>
        ))}
      </div>

      <nav className="nav">
        <div className="nav-title">Menu</div>
        {NAV.map(item => (
          <button key={item.id}
                  className="nav-item"
                  data-active={route === item.id}
                  onClick={() => { setRoute(item.id); onClose && onClose(); }}>
            <span className="nav-icon"><Icon name={item.icon} size={17} /></span>
            <span>{t[item.id]}</span>
            {item.count && <span className="count">{item.count}</span>}
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="avatar">JR</div>
        <div className="user-meta">
          <span className="name">J. Ramiarason</span>
          <span className="role">{lang === 'fr' ? 'Analyste tactique' : 'Tactical analyst'}</span>
        </div>
        <button className="btn btn-ghost btn-sm" style={{padding: 6}} title="Notifications">
          <Icon name="bell" size={14} />
        </button>
      </div>
    </aside>
  );
};

const Topbar = ({ route, lang, setLang, sport, onMenu }) => {
  const t = window.I18N[lang];
  const sportLabel = window.SPORTS.find(s => s.id === sport);
  return (
    <header className="topbar">
      <button className="mobile-menu-btn" onClick={onMenu}>
        <Icon name="burger" size={18} />
      </button>
      <div className="crumbs">
        <span className="ghost">{sportLabel?.emoji}</span>
        <span className="sep">/</span>
        <span>{t[route]}</span>
      </div>
      <div className="spacer" />
      <div className="search">
        <span className="icon"><Icon name="search" size={14} /></span>
        <input placeholder={t.search} />
      </div>
      <div className="lang-toggle">
        <button data-active={lang === 'fr'} onClick={() => setLang('fr')}>FR</button>
        <button data-active={lang === 'en'} onClick={() => setLang('en')}>EN</button>
      </div>
      <button className="btn btn-primary btn-sm" style={{display: 'inline-flex'}}>
        <Icon name="plus" size={14} /> {t.new_analysis}
      </button>
    </header>
  );
};

Object.assign(window, { Sidebar, Topbar });
