// app.jsx — Root app: routing, tweaks, language, sport state

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "palette": ["#4f7ef8", "#2d54d4", "#070b14"],
  "density": "regular",
  "showNoise": true,
  "rounded": "medium"
}/*EDITMODE-END*/;

// Accent palettes — each is [accent, accent-deep, bg-tone]
const PALETTES = [
  ["#4f7ef8", "#2d54d4", "#070b14"], // AuditIQ indigo (default)
  ["#CAFF33", "#90ee2a", "#080808"], // CoachIQ lime
  ["#FF6B35", "#FF8E53", "#0e0805"], // Sunset orange
  ["#22d3a5", "#16a085", "#06100c"], // Teal
];

const RADII = {
  sharp:  { sm: 4,  md: 6,  lg: 8 },
  medium: { sm: 8,  md: 12, lg: 14 },
  soft:   { sm: 12, md: 16, lg: 20 },
};

function App() {
  const [t, setTweak] = window.useTweaks(TWEAK_DEFAULTS);

  const [lang, setLang] = React.useState('fr');
  const [sport, setSport] = React.useState('football');
  const [route, setRoute] = React.useState('dashboard');
  const [openMatchId, setOpenMatchId] = React.useState(null);
  const [openMatchView, setOpenMatchView] = React.useState('pre'); // pre | post
  const [sidebarOpen, setSidebarOpen] = React.useState(false);

  const openMatch = (id, view) => {
    setOpenMatchId(id);
    setOpenMatchView(view);
    setRoute(view === 'post' ? 'post-match' : 'pre-match');
  };

  // Apply tweaks: accent palette → CSS vars
  React.useEffect(() => {
    const root = document.documentElement;
    const [accent, deep, bg] = t.palette || PALETTES[0];
    root.style.setProperty('--accent', accent);
    root.style.setProperty('--accent-deep', deep);
    root.style.setProperty('--accent-hot', accent);
    const ink = isLight(accent) ? '#080808' : '#fff';
    root.style.setProperty('--accent-ink', ink);
    // glow color from accent
    const glow = hexToRgba(accent, 0.18);
    const glowStrong = hexToRgba(accent, 0.45);
    root.style.setProperty('--accent-glow', glow);
    root.style.setProperty('--accent-glow-strong', glowStrong);
    root.style.setProperty('--glow-lime', `0 0 12px ${glow}`);
    root.style.setProperty('--glow-lime-2', `0 0 18px ${glowStrong}`);
    root.style.setProperty('--glow-lime-3', `0 0 24px ${glow}`);
    root.style.setProperty('--accent-bg', bg);
    document.body.dataset.density = t.density;
    const r = RADII[t.rounded] || RADII.medium;
    root.style.setProperty('--r-sm', r.sm + 'px');
    root.style.setProperty('--r-md', r.md + 'px');
    root.style.setProperty('--r-lg', r.lg + 'px');
  }, [t.palette, t.density, t.rounded]);

  const props = { lang, setLang, sport, setSport, setRoute, openMatch };

  let screen;
  switch (route) {
    case 'dashboard': screen = <DashboardScreen {...props} />; break;
    case 'matches':   screen = <MatchesScreen {...props} />; break;
    case 'pre-match': screen = <PreMatchScreen {...props} matchId={openMatchId} />; break;
    case 'post-match':screen = <PostMatchScreen {...props} matchId={openMatchId} />; break;
    case 'analysis':  screen = <AnalysisScreen {...props} />; break;
    case 'tactics':   screen = <TacticsScreen {...props} />; break;
    case 'compare':   screen = <CompareScreen {...props} />; break;
    case 'simulator': screen = <SimulatorScreen {...props} />; break;
    case 'trends':    screen = <TrendsScreen {...props} />; break;
    case 'history':   screen = <HistoryScreen {...props} />; break;
    case 'settings':  screen = <SettingsScreen {...props} />; break;
    default:          screen = <DashboardScreen {...props} />;
  }

  // Deep screens that highlight a parent nav entry
  const _analysisChildren = ['compare', 'simulator', 'trends'];
  const _matchChildren = ['pre-match', 'post-match'];
  // Crumb route id for header
  const headerRoute = _matchChildren.includes(route) ? 'matches'
    : _analysisChildren.includes(route) ? 'analysis' : route;
  // navigation highlight maps deep screens to their parent
  const navRoute = headerRoute;

  return (
    <React.Fragment>
      {t.showNoise && <div className="noise" />}
      <div className={`scrim ${sidebarOpen ? 'open' : ''}`} onClick={() => setSidebarOpen(false)} />
      <div className="shell">
        <Sidebar sport={sport} setSport={setSport}
                 route={navRoute} setRoute={setRoute}
                 lang={lang}
                 open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <main className="main">
          <Topbar route={headerRoute} lang={lang} setLang={setLang} sport={sport}
                  onMenu={() => setSidebarOpen(true)} />
          {screen}
        </main>
      </div>

      <window.TweaksPanel title="Tweaks">
        <window.TweakSection label={lang==='fr'?'Couleur d\'accent':'Accent color'} />
        <window.TweakColor label={lang==='fr'?'Palette':'Palette'}
                           value={t.palette}
                           options={PALETTES}
                           onChange={(v) => setTweak('palette', v)} />
        <window.TweakSection label={lang==='fr'?'Disposition':'Layout'} />
        <window.TweakRadio label={lang==='fr'?'Densité':'Density'}
                           value={t.density}
                           options={['compact', 'regular', 'comfy']}
                           onChange={(v) => setTweak('density', v)} />
        <window.TweakRadio label={lang==='fr'?'Coins':'Corners'}
                           value={t.rounded}
                           options={['sharp', 'medium', 'soft']}
                           onChange={(v) => setTweak('rounded', v)} />
        <window.TweakToggle label={lang==='fr'?'Grain de bruit':'Noise grain'}
                            value={t.showNoise}
                            onChange={(v) => setTweak('showNoise', v)} />
      </window.TweaksPanel>
    </React.Fragment>
  );
}

function isLight(hex) {
  const c = hex.replace('#','');
  const r = parseInt(c.slice(0,2), 16);
  const g = parseInt(c.slice(2,4), 16);
  const b = parseInt(c.slice(4,6), 16);
  return (r * 299 + g * 587 + b * 114) / 1000 > 165;
}
function hexToRgba(hex, a) {
  const c = hex.replace('#','');
  const r = parseInt(c.slice(0,2), 16);
  const g = parseInt(c.slice(2,4), 16);
  const b = parseInt(c.slice(4,6), 16);
  return `rgba(${r},${g},${b},${a})`;
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
