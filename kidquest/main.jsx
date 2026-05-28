// main.jsx — root app: routing + tweaks + persistence

// useState/useEffect/useMemo are already destructured at the top of screens.jsx (loaded before main).

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "palette": ["#FF6B35", "#FF8E53", "#FFD93D"],
  "dark": false,
  "mascotStyle": "default",
  "difficulty": "easy",
  "voice": false,
  "dailyLimit": 30
}/*EDITMODE-END*/;

// Accent palette options: [primary, primaryDeep, soft]
const PALETTES = [
  ["#FF6B35", "#FF8E53", "#FFD93D"], // KidQuest orange (default)
  ["#4ECDC4", "#44A9C6", "#A8E6CF"], // teal
  ["#A78BFA", "#7c6ef5", "#f093fb"], // purple
  ["#FFD93D", "#FF8E53", "#4ECDC4"], // yellow
];

function App() {
  const [t, setTweak] = window.useTweaks(TWEAK_DEFAULTS);

  const [lang, setLangRaw] = useState('fr');
  const [profile, setProfile] = useState(null);
  const [mode, setMode] = useState('onboard'); // onboard | world | quest | quiz | trophies | profile | parent
  const [activeHub, setActiveHub] = useState(null);
  const [activeLevel, setActiveLevel] = useState(null);
  const [reward, setReward] = useState(null);

  // Progress is a copy of the data levels per hub, mutable
  const [progress, setProgress] = useState(() => ({
    english: JSON.parse(JSON.stringify(window.KQ.levels.english)),
    geo:     JSON.parse(JSON.stringify(window.KQ.levels.geo)),
    math:    JSON.parse(JSON.stringify(window.KQ.levels.math)),
  }));

  // ─── Persistence
  useEffect(() => {
    try {
      const saved = localStorage.getItem('kq_state');
      if (saved) {
        const s = JSON.parse(saved);
        if (s.lang) setLangRaw(s.lang);
        if (s.profile) setProfile(s.profile);
        if (s.progress) setProgress(s.progress);
        if (s.profile) setMode('world');
      }
    } catch (e) {}
  }, []);
  useEffect(() => {
    try {
      localStorage.setItem('kq_state', JSON.stringify({ lang, profile, progress }));
    } catch (e) {}
  }, [lang, profile, progress]);

  const setLang = (l) => setLangRaw(l);

  // ─── Apply palette + dark via CSS vars
  useEffect(() => {
    const root = document.documentElement;
    const [p, pd, soft] = t.palette || PALETTES[0];
    root.style.setProperty('--kq-primary', p);
    root.style.setProperty('--kq-primary-deep', pd);
    root.style.setProperty('--kq-soft', soft);
    root.dataset.dark = String(!!t.dark);
  }, [t.palette, t.dark]);

  // ─── Stats for HUD
  const totalStars = Object.values(progress).reduce((s, h) =>
    s + h.reduce((ss, l) => ss + l.stars, 0), 0);

  const T = window.KQ_useT(lang);

  // ─── Handlers
  const handleOnboardDone = ({ name, avatar }) => {
    setProfile({ name, avatar });
    setMode('world');
  };
  const handlePickHub = (hubId) => {
    setActiveHub(hubId);
    setMode('quest');
  };
  const handleBackToWorld = () => {
    setActiveHub(null);
    setMode('world');
  };
  const handlePickLevel = (lv) => {
    setActiveLevel(lv);
    setMode('quiz');
  };
  const handleQuizComplete = ({ stars, correctCount, total }) => {
    // Update progress
    setProgress(prev => {
      const next = { ...prev };
      const list = [...next[activeHub]];
      const i = list.findIndex(l => l.n === activeLevel.n);
      if (i >= 0) {
        list[i] = { ...list[i], status: 'done', stars: Math.max(list[i].stars || 0, stars) };
        // Unlock next
        if (i + 1 < list.length && list[i+1].status === 'locked') {
          list[i+1] = { ...list[i+1], status: 'current' };
        }
      }
      next[activeHub] = list;
      return next;
    });
    // Reward overlay
    setReward({
      stars,
      newBadge: stars === 3
        ? { emoji: '💎', title_fr: 'Score parfait', title_en: 'Perfect score' }
        : null,
    });
    setMode('quest');
  };
  const handleExitQuiz = () => { setActiveLevel(null); setMode('quest'); };
  const handleCloseReward = () => setReward(null);

  const handleTab = (id) => {
    if (id === 'world') { setActiveHub(null); setMode('world'); }
    else setMode(id);
  };

  const handleChangeAvatar = (a) => {
    setProfile(p => ({ ...p, avatar: a }));
  };

  const hideHud = mode === 'onboard' || mode === 'quiz';
  const showTabs = profile && mode !== 'onboard' && mode !== 'quiz';
  const activeTab = ['world','trophies','profile','parent'].includes(mode) ? mode : 'world';

  let screen;
  if (mode === 'onboard' || !profile) {
    screen = <window.OnboardScreen lang={lang} setLang={setLang} onDone={handleOnboardDone} />;
  } else if (mode === 'world') {
    screen = <window.WorldMapScreen lang={lang} profile={profile} progress={progress} onPickHub={handlePickHub} />;
  } else if (mode === 'quest' && activeHub) {
    screen = <window.QuestMapScreen lang={lang} hubId={activeHub} levels={progress[activeHub]}
                                    profile={profile}
                                    onBack={handleBackToWorld}
                                    onPickLevel={handlePickLevel} />;
  } else if (mode === 'quiz' && activeLevel) {
    screen = <window.QuizScreen lang={lang} hubId={activeHub} level={activeLevel}
                                onExit={handleExitQuiz}
                                onComplete={handleQuizComplete} />;
  } else if (mode === 'trophies') {
    screen = <window.TrophiesScreen lang={lang} />;
  } else if (mode === 'profile') {
    screen = <window.ProfileScreen lang={lang} profile={profile} progress={progress}
                                   onChangeAvatar={handleChangeAvatar} />;
  } else if (mode === 'parent') {
    screen = <window.ParentScreen lang={lang} progress={progress}
                                  tweaks={t} setTweak={setTweak} />;
  }

  return (
    <React.Fragment>
      <div className="kq-app" data-mode={mode}>
        <window.Topbar lang={lang} setLang={setLang}
                       t={T}
                       profile={profile}
                       stars={totalStars} streak={5}
                       onProfile={() => setMode('profile')}
                       hideHud={hideHud || !profile} />
        {screen}
        {showTabs && <window.BottomTabs active={activeTab} onPick={handleTab} t={T} />}
      </div>

      {reward && (
        <window.RewardOverlay lang={lang}
                              stars={reward.stars}
                              newBadge={reward.newBadge}
                              onClose={handleCloseReward} />
      )}

      <window.TweaksPanel title="Tweaks">
        <window.TweakSection label={lang === 'fr' ? 'Palette' : 'Palette'} />
        <window.TweakColor label={lang === 'fr' ? 'Couleurs' : 'Colors'}
                           value={t.palette}
                           options={PALETTES}
                           onChange={(v) => setTweak('palette', v)} />
        <window.TweakSection label={lang === 'fr' ? 'Apparence' : 'Appearance'} />
        <window.TweakToggle label={lang === 'fr' ? 'Mode sombre' : 'Dark mode'}
                            value={t.dark}
                            onChange={(v) => setTweak('dark', v)} />
        <window.TweakSection label={lang === 'fr' ? 'Difficulté' : 'Difficulty'} />
        <window.TweakRadio label={lang === 'fr' ? 'Niveau' : 'Level'}
                           value={t.difficulty}
                           options={['easy', 'medium', 'hard']}
                           onChange={(v) => setTweak('difficulty', v)} />
        <window.TweakSection label={lang === 'fr' ? 'Confort' : 'Comfort'} />
        <window.TweakToggle label={lang === 'fr' ? 'Lecture vocale' : 'Voice reader'}
                            value={t.voice}
                            onChange={(v) => setTweak('voice', v)} />
        <window.TweakSlider label={lang === 'fr' ? 'Temps quotidien' : 'Daily time'}
                            value={t.dailyLimit}
                            min={10} max={60} step={5} unit=" min"
                            onChange={(v) => setTweak('dailyLimit', v)} />
        <window.TweakButton label={lang === 'fr' ? 'Réinitialiser' : 'Reset'}
                            onClick={() => {
                              try { localStorage.removeItem('kq_state'); } catch {}
                              location.reload();
                            }} />
      </window.TweaksPanel>
    </React.Fragment>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
