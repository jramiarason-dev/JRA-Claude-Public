// app.jsx — AuditIQ root: sign-in cover → app shell with routing.
const { useState: useStateApp, useEffect: useEffectApp } = React;

function AuditIQApp() {
  const [lang, setLang] = useStateApp(() => localStorage.getItem('aiq-lang') || 'fr');
  const [authed, setAuthed] = useStateApp(false);
  const [route, setRoute] = useStateApp('dashboard');
  const [navOpen, setNavOpen] = useStateApp(false);

  useEffectApp(() => { localStorage.setItem('aiq-lang', lang); }, [lang]);
  // reset scroll on route change
  useEffectApp(() => { const m = document.querySelector('.aiq-main'); if (m) m.scrollTop = 0; window.scrollTo(0, 0); }, [route]);

  const screen = () => {
    switch (route) {
      case 'dashboard': return <window.AIQ_DashboardScreen lang={lang} setRoute={setRoute} />;
      case 'audits':    return <window.AIQ_AuditsScreen lang={lang} setRoute={setRoute} />;
      case 'agent1':
      case 'agent2':
      case 'agent3':    return <window.AIQ_AgentScreen lang={lang} agentId={route} setRoute={setRoute} />;
      case 'documents': return <window.AIQ_DocumentsScreen lang={lang} />;
      case 'history':   return <window.AIQ_HistoryScreen lang={lang} />;
      case 'settings':  return <window.AIQ_SettingsScreen lang={lang} setLang={setLang} />;
      default:          return <window.AIQ_DashboardScreen lang={lang} setRoute={setRoute} />;
    }
  };

  if (!authed) {
    return <window.AIQ_SignIn lang={lang} setLang={setLang} onEnter={() => setAuthed(true)} />;
  }

  return (
    <React.Fragment>
      <div className="aiq-blob b1" />
      <div className="aiq-blob b2" />
      <div className="aiq-app">
        <div className={`aiq-scrim ${navOpen ? 'open' : ''}`} onClick={() => setNavOpen(false)} />
        <window.AIQ_Sidebar route={route} setRoute={setRoute} lang={lang}
                            open={navOpen} onClose={() => setNavOpen(false)} />
        <div className="aiq-main">
          <window.AIQ_Topbar route={route} lang={lang} setLang={setLang}
                             onMenu={() => setNavOpen(true)} />
          {screen()}
        </div>
      </div>
    </React.Fragment>
  );
}

const aiqRoot = ReactDOM.createRoot(document.getElementById('root'));
aiqRoot.render(<AuditIQApp />);
