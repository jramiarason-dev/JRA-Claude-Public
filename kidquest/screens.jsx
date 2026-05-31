// screens.jsx — All KidQuest screens
// Exposes: OnboardScreen, WorldMapScreen, QuestMapScreen, QuizScreen,
//          RewardOverlay, ProfileScreen, ParentScreen, BottomTabs, Topbar

var { useState, useEffect, useMemo } = React;

// ── helpers ──
const fmt = (s, vars) => Object.keys(vars || {}).reduce(
  (acc, k) => acc.replace(`{${k}}`, vars[k]), s);

const useT = (lang) => (key, vars) => fmt(window.KQ.i18n[lang][key] || key, vars);

const ConfettiBurst = () => (
  <div className="kq-confetti" aria-hidden="true">
    {[...Array(24)].map((_, i) => {
      const colors = ["#FF6B35","#FFD93D","#4ECDC4","#A78BFA","#FF99B6","#6BCB77"];
      const left = (i * 4.2) % 100;
      const delay = (i * 0.13).toFixed(2);
      const dur = 1.2 + (i % 4) * 0.4;
      const c = colors[i % colors.length];
      return <span key={i} style={{ left: `${left}%`, top: 0, animationDelay: `${delay}s`, "--c": c, "--d": `${dur}s` }} />;
    })}
  </div>
);

const Stars = ({ n, max = 3, size = 16 }) => (
  <span style={{ display: 'inline-flex', gap: 1, fontSize: size }}>
    {[...Array(max)].map((_, i) => (
      <span key={i} style={{ opacity: i < n ? 1 : 0.25 }}>⭐</span>
    ))}
  </span>
);

// ── TOPBAR ──
const Topbar = ({ lang, setLang, t, profile, stars, streak, onProfile, hideHud }) => (
  <div className="kq-topbar">
    <div className="kq-brand">
      <div className="logo">🎓</div>
      <div className="name"><b>Kid</b>Quest</div>
    </div>
    <div className="kq-topbar-spacer" />
    {!hideHud && (
      <div className="kq-hud">
        <div className="kq-chip gold"><span className="emoji">⭐</span><strong>{stars}</strong></div>
        <div className="kq-chip fire"><span className="emoji">🔥</span><strong>{streak}</strong></div>
        <div className="kq-lang" role="tablist">
          <button data-active={lang === 'fr'} onClick={() => setLang('fr')}>🇫🇷 FR</button>
          <button data-active={lang === 'en'} onClick={() => setLang('en')}>🇬🇧 EN</button>
        </div>
        {profile && (
          <button className="kq-profile-pill" onClick={onProfile} title={t('profile')}>
            <div className="av">{profile.avatar}</div>
            <span>{profile.name}</span>
          </button>
        )}
      </div>
    )}
    {hideHud && (
      <div className="kq-lang" role="tablist">
        <button data-active={lang === 'fr'} onClick={() => setLang('fr')}>🇫🇷 FR</button>
        <button data-active={lang === 'en'} onClick={() => setLang('en')}>🇬🇧 EN</button>
      </div>
    )}
  </div>
);

// ── BOTTOM TABS ──
const BottomTabs = ({ active, onPick, t }) => (
  <nav className="kq-tabs">
    {[
      { id: "world",    emoji: "🗺️", label: t('world_map') },
      { id: "trophies", emoji: "🏆", label: t('trophies') },
      { id: "profile",  emoji: "👤", label: t('profile') },
      { id: "parent",   emoji: "🔒", label: t('parent_zone') },
    ].map(tab => (
      <button key={tab.id} data-active={active === tab.id} onClick={() => onPick(tab.id)}>
        <span className="emoji">{tab.emoji}</span>
        <span>{tab.label}</span>
      </button>
    ))}
  </nav>
);

// ── ONBOARDING ──
const OnboardScreen = ({ lang, setLang, onDone }) => {
  const t = useT(lang);
  const [step, setStep] = useState(0);
  const [avatar, setAvatar] = useState(null);
  const [name, setName] = useState("");

  const next = () => setStep(s => s + 1);
  const back = () => setStep(s => Math.max(0, s - 1));

  // 0 = welcome, 1 = avatar, 2 = name
  return (
    <div className="kq-onboard">
      <div className="step-dots">
        {[0,1,2].map(i => <span key={i} className="dot" data-active={step === i} />)}
      </div>

      {step === 0 && (
        <React.Fragment>
          <div className="kq-onboard-mascot">
            <window.OwlMascot size={150} accent="#4ECDC4" />
          </div>
          <h1 className="kq-h1 rainbow">{t('welcome')}</h1>
          <p className="kq-sub">{t('welcome_sub')}</p>
          <div className="kq-lang-row">
            <button className="kq-btn kq-btn-teal kq-btn-big"
                    data-active={lang === 'fr'}
                    onClick={() => { setLang('fr'); }}>
              <span className="flag">🇫🇷</span> Français
            </button>
            <button className="kq-btn kq-btn-purple kq-btn-big"
                    data-active={lang === 'en'}
                    onClick={() => { setLang('en'); }}>
              <span className="flag">🇬🇧</span> English
            </button>
          </div>
          <button className="kq-btn kq-btn-primary kq-btn-big" onClick={next}>
            {t('next')} →
          </button>
        </React.Fragment>
      )}

      {step === 1 && (
        <React.Fragment>
          <h1 className="kq-h1">{t('choose_avatar')}</h1>
          <p className="kq-sub">{t('choose_avatar_sub')}</p>
          <div className="kq-avatar-grid">
            {window.KQ.avatars.map(a => (
              <button key={a.id}
                      data-active={avatar?.id === a.id}
                      onClick={() => setAvatar(a)}>
                {a.emoji}
              </button>
            ))}
          </div>
          <div style={{ display: 'flex', gap: 12 }}>
            <button className="kq-btn kq-btn-ghost" onClick={back}>← {t('back')}</button>
            <button className="kq-btn kq-btn-primary kq-btn-big"
                    disabled={!avatar}
                    onClick={next}>
              {t('next')} →
            </button>
          </div>
        </React.Fragment>
      )}

      {step === 2 && (
        <React.Fragment>
          <div className="kq-onboard-mascot">
            <window.FoxMascot size={130} accent={avatar?.color || "#A78BFA"} />
          </div>
          <h1 className="kq-h1">{t('whats_your_name')}</h1>
          <input className="kq-input"
                 maxLength={12}
                 value={name}
                 onChange={e => setName(e.target.value)}
                 placeholder={t('name_placeholder')}
                 autoFocus />
          <div style={{ display: 'flex', gap: 12 }}>
            <button className="kq-btn kq-btn-ghost" onClick={back}>← {t('back')}</button>
            <button className="kq-btn kq-btn-primary kq-btn-big"
                    disabled={!name.trim()}
                    onClick={() => onDone({ name: name.trim(), avatar })}>
              {t('lets_go')} 🚀
            </button>
          </div>
        </React.Fragment>
      )}
    </div>
  );
};

// ── WORLD MAP ──
const WorldMapScreen = ({ lang, profile, progress, onPickHub }) => {
  const t = useT(lang);
  const totalStars = Object.values(progress).reduce((s, h) =>
    s + h.reduce((ss, l) => ss + l.stars, 0), 0);

  return (
    <section className="kq-world">
      <div className="kq-world-bg" />
      <h1 className="kq-h1 rainbow">{t('hello_name', { name: profile?.name || '' })}</h1>
      <p className="kq-sub sub">{t('choose_world')}</p>

      <div className="kq-islands" style={{ marginTop: 24 }}>
        {window.KQ.hubs.map((hub, i) => {
          const levels = progress[hub.id] || window.KQ.levels[hub.id];
          const done = levels.filter(l => l.status === 'done').length;
          const total = levels.length;
          const hubStars = levels.reduce((s, l) => s + l.stars, 0);
          const bgGrad = `linear-gradient(180deg, ${hub.colorSoft}, ${hub.color})`;
          return (
            <button key={hub.id}
                    className="kq-island"
                    style={{ "--hub-bg": bgGrad, "--hub-color": hub.color, animationDelay: `${i*.1}s` }}
                    onClick={() => onPickHub(hub.id)}>
              <div className="kq-island-mascot">
                <window.HubMascot hubId={hub.id} size={130} accent={hub.color} />
              </div>
              <h2 className="kq-island-title">{t(hub.title_key)}</h2>
              <p className="kq-island-sub">{t(hub.sub_key)}</p>

              <div className="kq-island-meta">
                <span className="kq-chip"><span className="emoji">⭐</span><strong>{hubStars}</strong></span>
                <span className="kq-chip"><span className="emoji">📍</span><strong>{done}/{total}</strong></span>
              </div>

              <div className="kq-island-progress">
                <span style={{ width: `${(done/total) * 100}%` }} />
              </div>

              <div className="kq-island-cta">
                <span className="kq-btn kq-btn-primary">
                  {done === total ? t('replay') : t('play')} →
                </span>
              </div>
            </button>
          );
        })}
      </div>
    </section>
  );
};

// ── QUEST MAP ──
const QuestMapScreen = ({ lang, hubId, levels, profile, onBack, onPickLevel }) => {
  const t = useT(lang);
  const hub = window.KQ.hubs.find(h => h.id === hubId);
  const hubStars = levels.reduce((s, l) => s + l.stars, 0);
  const done = levels.filter(l => l.status === 'done').length;
  const bgGrad = `linear-gradient(135deg, ${hub.colorSoft}, ${hub.color})`;

  return (
    <section className="kq-quest">
      <div className="kq-quest-header">
        <button className="kq-back-btn" onClick={onBack} aria-label={t('back')}>←</button>
        <div style={{ flex: 1 }}>
          <h1 className="kq-h2">{t(hub.hub_title_key)}</h1>
          <p className="kq-sub" style={{ margin: 0 }}>
            ⭐ {hubStars} · 📍 {done}/{levels.length}
          </p>
        </div>
      </div>

      <div className="kq-quest-hero" style={{ "--hub-bg": bgGrad }}>
        <div className="mascot">
          <window.HubMascot hubId={hubId} size={120} accent={hub.color} />
        </div>
        <div className="who">
          <h1>{hub.mascotName[lang]}</h1>
          <p>
            {lang === 'fr'
              ? `Coucou ${profile?.name || ''} ! Aujourd'hui on apprend ensemble.`
              : `Hi ${profile?.name || ''}! Let's learn together today.`}
          </p>
          <div style={{ display: 'flex', gap: 8 }}>
            <span className="kq-chip gold"><span className="emoji">⭐</span><strong>{hubStars}</strong></span>
            <span className="kq-chip"><span className="emoji">📍</span><strong>{done}/{levels.length}</strong></span>
          </div>
        </div>
        <div className="stats">
          <span className="kq-chip teal">{t('level')} {done + 1}</span>
        </div>
      </div>

      <div className="kq-path" style={{ "--hub-color": hub.color }}>
        {levels.map((lv, i) => {
          const side = i % 2 === 0 ? "left" : "right";
          const offset = side === "left" ? -60 : 60;
          return (
            <div key={lv.n} className={`kq-level ${side === 'right' ? 'right' : ''}`}
                 style={{ marginLeft: side === 'left' ? 0 : 'auto',
                          marginRight: side === 'right' ? 0 : 'auto',
                          paddingLeft: side === 'left' ? 8 : 0,
                          paddingRight: side === 'right' ? 8 : 0,
                          transform: `translateX(${offset}px)` }}>
              <button className="kq-level-node"
                      data-status={lv.status}
                      onClick={() => lv.status !== 'locked' && onPickLevel(lv)}
                      title={lv[`title_${lang}`]}>
                {lv.status === 'locked' ? <span className="lock">🔒</span>
                  : lv.boss ? <span className="boss-emoji">👑</span>
                  : <span>{lv.n}</span>}
                {lv.status === 'done' && lv.stars > 0 && (
                  <div className="kq-level-stars">
                    <Stars n={lv.stars} max={3} size={11} />
                  </div>
                )}
                {lv.status === 'current' && (
                  <div className="kq-level-stars" style={{ background: '#FFD93D' }}>
                    {t('current')} 📍
                  </div>
                )}
              </button>
              <div className="kq-level-info">
                <div className="num">{t('lesson')} {lv.n}</div>
                <div className="ttl">{lv[`title_${lang}`]}</div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

// ── QUIZ ──
const QuizScreen = ({ lang, hubId, level, onExit, onComplete }) => {
  const t = useT(lang);
  const hub = window.KQ.hubs.find(h => h.id === hubId);
  // Fallback: if no question bank, generate placeholders matching the topic count
  const bank = window.KQ.questions[level.topic] || [
    { q_fr: `Question d'exemple — ${level.title_fr}`,
      q_en: `Example question — ${level.title_en}`,
      opts: [
        { fr: "Option A", en: "Option A", emoji: "🅰️" },
        { fr: "Option B", en: "Option B", emoji: "🅱️" },
        { fr: "Option C", en: "Option C", emoji: "🆎" },
      ], correct: 0 },
    { q_fr: "Une autre question d'exemple", q_en: "Another example question",
      opts: [
        { fr: "Bonne", en: "Right", emoji: "✅" },
        { fr: "Pas bonne", en: "Wrong", emoji: "❌" },
        { fr: "Peut-être", en: "Maybe", emoji: "🤔" },
      ], correct: 0 },
    { q_fr: "Dernière question", q_en: "Last question",
      opts: [
        { fr: "Un", en: "One", emoji: "1️⃣" },
        { fr: "Deux", en: "Two", emoji: "2️⃣" },
        { fr: "Trois", en: "Three", emoji: "3️⃣" },
      ], correct: 1 },
  ];

  const [qi, setQi] = useState(0);
  const [picked, setPicked] = useState(null);
  const [state, setState] = useState("idle"); // idle | correct | wrong
  const [hearts, setHearts] = useState(3);
  const [correctCount, setCorrectCount] = useState(0);

  const q = bank[qi];
  const total = bank.length;

  const choose = (i) => {
    if (state !== 'idle') return;
    setPicked(i);
  };
  const check = () => {
    if (picked == null) return;
    const right = picked === q.correct;
    setState(right ? 'correct' : 'wrong');
    if (right) setCorrectCount(c => c + 1);
    else setHearts(h => Math.max(0, h - 1));
  };
  const cont = () => {
    if (qi + 1 >= total) {
      // Compute stars: 3 if perfect, 2 if 1 mistake, 1 if 2+ mistakes
      const stars = correctCount + (state === 'correct' ? 0 : 0) === total
        ? 3 : correctCount >= total - 1 ? 2 : 1;
      onComplete({ stars, correctCount: correctCount + (state === 'correct' ? 0 : 0), total });
      return;
    }
    setQi(qi + 1);
    setPicked(null);
    setState('idle');
  };

  return (
    <section className="kq-quiz">
      <div className="kq-quiz-bar">
        <button className="kq-back-btn" onClick={onExit} aria-label="Quit">✕</button>
        <div className="kq-progress">
          <span style={{ width: `${((qi + (state !== 'idle' ? 1 : 0))/total) * 100}%`, background: hub.color }} />
        </div>
        <div className="kq-hearts">
          {[0,1,2].map(i => <span key={i} className={i < hearts ? '' : 'empty'}>❤️</span>)}
        </div>
      </div>

      <div className="kq-question-card">
        <div className="kq-mascot-bubble">
          <div className="speech">
            {state === 'idle' && t('pick_answer')}
            {state === 'correct' && t('correct') + " 🎉"}
            {state === 'wrong' && t('wrong')}
          </div>
          <window.HubMascot hubId={hubId} size={88} mood={state === 'wrong' ? 'wow' : 'happy'} accent={hub.color} />
        </div>

        <p style={{ fontSize: 12, color: 'var(--kq-ink-soft)', letterSpacing: '.1em',
                    textTransform: 'uppercase', fontWeight: 700, margin: '0 0 8px' }}>
          {t('question_of', { a: qi + 1, b: total })}
        </p>
        <h2 className="kq-question">{q[`q_${lang}`]}</h2>

        <div className="kq-options">
          {q.opts.map((opt, i) => {
            const selected = picked === i;
            let stateAttr;
            if (state !== 'idle') {
              if (i === q.correct) stateAttr = 'correct';
              else if (selected && state === 'wrong') stateAttr = 'wrong';
            }
            return (
              <button key={i}
                      className="kq-option"
                      data-selected={selected}
                      data-state={stateAttr}
                      onClick={() => choose(i)}
                      disabled={state !== 'idle'}>
                <span className="emoji">{opt.emoji}</span>
                <span>{opt[lang]}</span>
              </button>
            );
          })}
        </div>

        {state === 'idle' ? (
          <button className="kq-btn kq-btn-primary kq-btn-big"
                  disabled={picked == null}
                  onClick={check}>
            {t('check')} ✓
          </button>
        ) : (
          <React.Fragment>
            <div className={`kq-feedback ${state === 'correct' ? 'good' : 'bad'}`}>
              {state === 'correct' ? t('correct') + ' 🌟' : t('wrong') + ' 💪'}
            </div>
            <button className="kq-btn kq-btn-primary kq-btn-big" onClick={cont}>
              {qi + 1 >= total ? t('continue') + ' 🏁' : t('continue') + ' →'}
            </button>
          </React.Fragment>
        )}
      </div>
    </section>
  );
};

// ── REWARD OVERLAY ──
const RewardOverlay = ({ lang, stars, newBadge, onClose }) => {
  const t = useT(lang);
  return (
    <div className="kq-reward" onClick={onClose}>
      <div className="kq-reward-card" onClick={e => e.stopPropagation()}>
        <ConfettiBurst />
        <div style={{ fontSize: 70, lineHeight: 1 }}>🎉</div>
        <h2 className="kq-h1">{t('well_done')}</h2>
        <div className="kq-reward-stars">
          {[0,1,2].map(i => (
            <span key={i} className="pop" style={{ opacity: i < stars ? 1 : 0.18 }}>⭐</span>
          ))}
        </div>
        <p className="kq-sub">{t('stars_earned', { n: stars })}</p>
        {newBadge && (
          <div className="kq-reward-badge">
            <span style={{ fontSize: 22 }}>{newBadge.emoji}</span>
            <span>{t('new_badge')} — {newBadge[`title_${lang}`]}</span>
          </div>
        )}
        <button className="kq-btn kq-btn-primary kq-btn-big" onClick={onClose} style={{ marginTop: 14 }}>
          {t('back_to_map')} 🗺️
        </button>
      </div>
    </div>
  );
};

// ── TROPHIES / COLLECTION ──
const TrophiesScreen = ({ lang }) => {
  const t = useT(lang);
  const owned = window.KQ.trophies.filter(tr => tr.owned).length;
  return (
    <section style={{ paddingBottom: 40 }}>
      <h1 className="kq-h1 rainbow" style={{ textAlign: 'center' }}>{t('trophies')}</h1>
      <p className="kq-sub" style={{ textAlign: 'center', marginBottom: 18 }}>
        {owned} / {window.KQ.trophies.length} 🏆
      </p>
      <div className="kq-trophies">
        {window.KQ.trophies.map(tr => (
          <div key={tr.id} className={`kq-trophy ${tr.owned ? '' : 'locked'}`}>
            <div className="emoji">{tr.emoji}</div>
            <h4>{tr[`title_${lang}`]}</h4>
            <p>{tr[`desc_${lang}`]}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

// ── PROFILE ──
const ProfileScreen = ({ lang, profile, progress, onChangeAvatar }) => {
  const t = useT(lang);
  const totalStars = Object.values(progress).reduce((s, h) =>
    s + h.reduce((ss, l) => ss + l.stars, 0), 0);
  const levelsDone = Object.values(progress).reduce((s, h) =>
    s + h.filter(l => l.status === 'done').length, 0);
  const trophies = window.KQ.trophies.filter(tr => tr.owned).length;

  return (
    <section style={{ paddingBottom: 40 }}>
      <div className="kq-profile-hero">
        <div className="kq-big-avatar">{profile?.avatar?.emoji || '🦊'}</div>
        <div>
          <h1>{profile?.name || 'Aventurier'}</h1>
          <p className="sub">{t('hello_name', { name: '' }).replace(/[!\s]+$/, '')} 👋</p>
          <div className="chips">
            <span className="kq-chip gold"><span className="emoji">⭐</span><strong>{totalStars}</strong> {t('total_stars')}</span>
            <span className="kq-chip fire"><span className="emoji">🔥</span><strong>5</strong> {t('streak')}</span>
          </div>
        </div>
      </div>

      <div className="kq-stat-row">
        <div className="kq-stat"><div className="v">{totalStars}</div><div className="l">⭐ {t('total_stars')}</div></div>
        <div className="kq-stat"><div className="v">{levelsDone}</div><div className="l">📍 {t('levels_done')}</div></div>
        <div className="kq-stat"><div className="v">{trophies}</div><div className="l">🏆 {t('trophies')}</div></div>
        <div className="kq-stat"><div className="v">5</div><div className="l">🔥 {t('streak')}</div></div>
      </div>

      <div className="kq-card">
        <h2 className="kq-h2">{t('progress')}</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14, marginTop: 14 }}>
          {window.KQ.hubs.map(hub => {
            const levels = progress[hub.id];
            const done = levels.filter(l => l.status === 'done').length;
            const pct = (done / levels.length) * 100;
            return (
              <div key={hub.id}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                  <strong>{t(hub.title_key)}</strong>
                  <span style={{ color: 'var(--kq-ink-soft)' }}>{done}/{levels.length}</span>
                </div>
                <div style={{
                  height: 14,
                  background: 'rgba(42,31,31,.1)',
                  border: '2px solid var(--kq-line)',
                  borderRadius: 999,
                  overflow: 'hidden',
                }}>
                  <div style={{
                    height: '100%', width: `${pct}%`,
                    background: hub.color, borderRight: '2px solid var(--kq-line)',
                    transition: 'width .6s var(--ease)',
                  }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="kq-card" style={{ marginTop: 16 }}>
        <h2 className="kq-h2">{t('choose_avatar')}</h2>
        <p className="kq-sub" style={{ marginBottom: 12 }}>{t('choose_avatar_sub')}</p>
        <div className="kq-avatar-grid" style={{ maxWidth: 'none' }}>
          {window.KQ.avatars.map(a => (
            <button key={a.id}
                    data-active={profile?.avatar?.id === a.id}
                    onClick={() => onChangeAvatar(a)}>
              {a.emoji}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
};

// ── PIN CHANGE ──
const PinChangeCard = ({ lang }) => {
  const [current, setCurrent] = React.useState('');
  const [next1, setNext1]     = React.useState('');
  const [next2, setNext2]     = React.useState('');
  const [msg, setMsg]         = React.useState(null);

  const save = () => {
    const stored = localStorage.getItem('kq_parent_pin') || '1234';
    if (current !== stored)       { setMsg({ ok: false, text: lang === 'fr' ? 'Code actuel incorrect' : 'Wrong current PIN' }); return; }
    if (!/^\d{4}$/.test(next1))   { setMsg({ ok: false, text: lang === 'fr' ? 'Le nouveau code doit être 4 chiffres' : 'New PIN must be 4 digits' }); return; }
    if (next1 !== next2)          { setMsg({ ok: false, text: lang === 'fr' ? 'Les codes ne correspondent pas' : 'PINs do not match' }); return; }
    localStorage.setItem('kq_parent_pin', next1);
    setCurrent(''); setNext1(''); setNext2('');
    setMsg({ ok: true, text: lang === 'fr' ? 'Code mis à jour ✓' : 'PIN updated ✓' });
  };

  return (
    <div className="kq-card" style={{ marginTop: 16 }}>
      <h2 className="kq-h2" style={{ marginBottom: 12 }}>
        {lang === 'fr' ? '🔑 Changer le code parental' : '🔑 Change parent PIN'}
      </h2>
      {[
        [lang === 'fr' ? 'Code actuel' : 'Current PIN', current, setCurrent],
        [lang === 'fr' ? 'Nouveau code' : 'New PIN',    next1,   setNext1],
        [lang === 'fr' ? 'Confirmer'   : 'Confirm',     next2,   setNext2],
      ].map(([label, val, set]) => (
        <div key={label} className="kq-setting" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: 4 }}>
          <div className="label">{label}</div>
          <input type="password" inputMode="numeric" maxLength={4}
                 value={val} onChange={e => { set(e.target.value.replace(/[^\d]/g, '')); setMsg(null); }}
                 style={{ fontSize: 20, letterSpacing: 8, width: 100, textAlign: 'center', borderRadius: 8, border: '1.5px solid #6366f1', padding: '4px 8px' }} />
        </div>
      ))}
      <button onClick={save}
              style={{ marginTop: 12, background: '#6366f1', color: '#fff', border: 'none', borderRadius: 10, padding: '8px 20px', fontSize: 15, cursor: 'pointer' }}>
        {lang === 'fr' ? 'Enregistrer' : 'Save'}
      </button>
      {msg && <p style={{ marginTop: 8, fontSize: 13, color: msg.ok ? '#16a34a' : '#dc2626' }}>{msg.text}</p>}
    </div>
  );
};

// ── PARENT ZONE ──
const ParentScreen = ({ lang, tweaks, setTweak, progress }) => {
  const t = useT(lang);
  const [unlocked, setUnlocked] = useState(false);
  const [pin, setPin] = useState(['','','','']);

  const tryUnlock = (digits) => {
    const stored = localStorage.getItem('kq_parent_pin') || '1234';
    if (digits.every(d => d !== '') && digits.join('') === stored) {
      setUnlocked(true);
    }
  };

  if (!unlocked) {
    return (
      <section className="kq-parent">
        <div className="kq-card lock-screen">
          <div style={{ fontSize: 72 }}>🔒</div>
          <h1 className="kq-h1">{t('parent_zone')}</h1>
          <p className="kq-sub">{t('parent_lock')}</p>
          <div className="pin-row">
            {[0,1,2,3].map(i => (
              <input key={i}
                     type="text" inputMode="numeric"
                     maxLength={1}
                     value={pin[i]}
                     onChange={(e) => {
                       const v = e.target.value.replace(/[^\d]/g, '');
                       const next = [...pin]; next[i] = v;
                       setPin(next);
                       if (v && i < 3) document.querySelectorAll('.pin-row input')[i+1].focus();
                       tryUnlock(next);
                     }}
                     onKeyDown={(e) => {
                       if (e.key === 'Backspace' && !pin[i] && i > 0) {
                         document.querySelectorAll('.pin-row input')[i-1].focus();
                       }
                     }} />
            ))}
          </div>
          <p className="kq-sub" style={{ fontSize: 13 }}>
            {lang === 'fr' ? 'Réservé aux parents' : 'Parents only'}
          </p>
        </div>
      </section>
    );
  }

  const totalLevels = Object.values(progress).reduce((s, h) => s + h.length, 0);
  const doneLevels = Object.values(progress).reduce((s, h) => s + h.filter(l => l.status === 'done').length, 0);
  const totalStars = Object.values(progress).reduce((s, h) => s + h.reduce((ss, l) => ss + l.stars, 0), 0);

  return (
    <section className="kq-parent" style={{ paddingBottom: 40 }}>
      <h1 className="kq-h1">{t('parent_zone')}</h1>
      <p className="kq-sub" style={{ marginBottom: 18 }}>
        {lang === 'fr' ? 'Suivi de la progression et réglages.' : 'Progress tracking and settings.'}
      </p>

      <div className="kq-stat-row">
        <div className="kq-stat"><div className="v">{doneLevels}</div><div className="l">{t('levels_done')}</div></div>
        <div className="kq-stat"><div className="v">{totalStars}</div><div className="l">⭐ {t('total_stars')}</div></div>
        <div className="kq-stat"><div className="v">—</div><div className="l">{t('time_today')} ({t('minutes')})</div></div>
        <div className="kq-stat"><div className="v">—</div><div className="l">🔥 {t('streak')}</div></div>
      </div>

      <div className="kq-card">
        <h2 className="kq-h2">{t('parent_settings')}</h2>

        <div className="kq-setting">
          <div>
            <div className="label">{t('difficulty')}</div>
            <div className="desc">{lang === 'fr' ? 'Ajuste la difficulté des questions' : 'Adjusts question difficulty'}</div>
          </div>
          <div className="kq-seg">
            {['easy','medium','hard'].map(d => (
              <button key={d}
                      data-active={tweaks.difficulty === d}
                      onClick={() => setTweak('difficulty', d)}>
                {t(d)}
              </button>
            ))}
          </div>
        </div>

        <div className="kq-setting">
          <div>
            <div className="label">{lang === 'fr' ? 'Mode sombre' : 'Dark mode'}</div>
            <div className="desc">{lang === 'fr' ? 'Repos pour les yeux le soir' : 'Easier on the eyes at night'}</div>
          </div>
          <div className="kq-switch" data-on={tweaks.dark}
               onClick={() => setTweak('dark', !tweaks.dark)} />
        </div>

        <div className="kq-setting">
          <div>
            <div className="label">{lang === 'fr' ? 'Lecture vocale' : 'Voice reader'}</div>
            <div className="desc">{lang === 'fr' ? 'Lit les questions à voix haute' : 'Reads questions aloud'}</div>
          </div>
          <div className="kq-switch" data-on={tweaks.voice}
               onClick={() => setTweak('voice', !tweaks.voice)} />
        </div>

        <div className="kq-setting">
          <div>
            <div className="label">{lang === 'fr' ? 'Temps quotidien max' : 'Daily time limit'}</div>
            <div className="desc">{tweaks.dailyLimit} {t('minutes')}</div>
          </div>
          <input type="range" min="10" max="60" step="5"
                 value={tweaks.dailyLimit}
                 onChange={e => setTweak('dailyLimit', parseInt(e.target.value, 10))} />
        </div>
      </div>

      <PinChangeCard lang={lang} />

      <div className="kq-card" style={{ marginTop: 16 }}>
        <h2 className="kq-h2">{t('progress')}</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginTop: 12 }}>
          {window.KQ.hubs.map(hub => {
            const levels = progress[hub.id];
            const done = levels.filter(l => l.status === 'done').length;
            return (
              <div key={hub.id} className="kq-setting">
                <div>
                  <div className="label">{t(hub.title_key)}</div>
                  <div className="desc">{done} / {levels.length} {lang==='fr'?'leçons':'lessons'}</div>
                </div>
                <strong style={{ color: hub.color, fontSize: 22 }}>
                  {Math.round((done/levels.length)*100)}%
                </strong>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

Object.assign(window, {
  KQ_useT: useT,
  Topbar, BottomTabs,
  OnboardScreen, WorldMapScreen, QuestMapScreen, QuizScreen,
  RewardOverlay, TrophiesScreen, ProfileScreen, ParentScreen,
});
