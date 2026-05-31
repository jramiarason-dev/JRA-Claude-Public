// components-ui.jsx — Small UI primitives shared across screens
// Exports: Icon, Pill, Stat, Crest, MatchCard, ProgressBar, BarCompare, Gauge

const Icon = ({ name, size = 18, stroke = 1.6 }) => {
  const paths = {
    home: "M3 12l9-9 9 9M5 10v10h14V10",
    matches: "M4 6h16M4 12h16M4 18h10",
    analysis: "M3 17l6-6 4 4 8-8M21 7h-5M21 7v5",
    history: "M3 12a9 9 0 1 0 3-6.7M3 4v5h5",
    settings: "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06A2 2 0 1 1 4.27 16.96l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09a1.65 1.65 0 0 0 1.51-1A1.65 1.65 0 0 0 4.27 7.27l-.06-.06A2 2 0 1 1 7.04 4.38l.06.06a1.65 1.65 0 0 0 1.82.33h.05a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z",
    search: "M11 19a8 8 0 1 1 5.3-14M21 21l-4.3-4.3",
    plus: "M12 5v14M5 12h14",
    chevron: "M9 18l6-6-6-6",
    arrow: "M5 12h14M13 5l7 7-7 7",
    download: "M12 4v12m-5-5l5 5 5-5M5 20h14",
    share: "M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13",
    burger: "M4 6h16M4 12h16M4 18h16",
    close: "M6 6l12 12M18 6L6 18",
    star: "M12 2l2.9 6.5 7.1.7-5.4 4.8 1.7 7-6.3-3.8-6.3 3.8 1.7-7L2 9.2l7.1-.7L12 2z",
    bell: "M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0",
    check: "M5 12l5 5 9-11",
    sparkle: "M12 3v6m0 6v6M3 12h6m6 0h6M5.6 5.6l4.2 4.2m4.4 4.4l4.2 4.2M5.6 18.4l4.2-4.2m4.4-4.4l4.2-4.2",
    trend: "M3 17l6-6 4 4 8-8M21 7h-5M21 7v5",
    target: "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 18a6 6 0 1 0 0-12 6 6 0 0 0 0 12zM12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4z",
    play: "M5 3l14 9-14 9V3z",
    clock: "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 6v6l4 2",
    pin: "M12 22s7-7 7-12a7 7 0 1 0-14 0c0 5 7 12 7 12zM12 11a2 2 0 1 0 0-4 2 2 0 0 0 0 4z",
  };
  return (
    <svg viewBox="0 0 24 24" width={size} height={size} fill="none"
         stroke="currentColor" strokeWidth={stroke}
         strokeLinecap="round" strokeLinejoin="round">
      <path d={paths[name] || paths.home} />
    </svg>
  );
};

const Pill = ({ kind = "default", children }) => {
  const cls = { default: "pill",
    accent: "pill pill-accent",
    live: "pill pill-live",
    finished: "pill pill-finished",
    upcoming: "pill pill-upcoming" }[kind] || "pill";
  return <span className={cls}>{children}</span>;
};

const Stat = ({ label, value, delta, deltaKind = "up", suffix }) => (
  <div className="stat">
    <div className="stat-label">{label}</div>
    <div className="stat-value">{value}{suffix && <span style={{fontSize: 18, color: '#888', marginLeft: 4, letterSpacing: 0}}>{suffix}</span>}</div>
    {delta && (
      <div className={`stat-delta ${deltaKind}`}>
        {deltaKind === "up" ? "▲" : "▼"} {delta}
      </div>
    )}
  </div>
);

const Crest = ({ code, color }) => (
  <div className="team-crest" style={{ background: `linear-gradient(135deg, ${color}, ${color}cc)` }}>
    {code}
  </div>
);

const FormBar = ({ form = [] }) => (
  <div className="form-bar">
    {form.map((r, i) => (
      <span key={i} className={`dot ${r==='V'?'dot-w': r==='N'?'dot-n':'dot-d'}`} title={r} />
    ))}
  </div>
);

const MatchCard = ({ match, lang, onClick }) => {
  const t = window.I18N[lang];
  const status = match.status;
  const isLive = status === "live";
  const isFinished = status === "finished";

  return (
    <div className="card card-hover match-card fade-in" onClick={onClick}>
      <div className="match-meta">
        <span className="comp">{match.competition}</span>
        <span>
          {isLive
            ? <Pill kind="live">{t.live}</Pill>
            : isFinished
              ? <Pill kind="finished">{t.finished}</Pill>
              : <Pill kind="upcoming">{t.upcoming_pill}</Pill>}
        </span>
      </div>

      <div className="match-teams">
        <div className="team">
          <Crest code={match.home.code} color={match.home.color} />
          <div style={{ minWidth: 0 }}>
            <div className="team-name">{match.home.name}</div>
            <div className="team-rank">
              {match.home.rank != null ? <><span className="muted">#{match.home.rank}</span>{' · '}</> : null}
              <FormBar form={match.home.form} />
            </div>
          </div>
        </div>

        <div className="match-vs">
          {isLive || isFinished ? (
            <div className={`match-score ${isLive ? 'live' : ''}`}>
              {match.score.home} <span style={{color:'#444'}}>–</span> {match.score.away}
            </div>
          ) : (
            <div className="match-vs-sep">VS</div>
          )}
          <div className="match-time">{match.date}</div>
        </div>

        <div className="team away">
          <Crest code={match.away.code} color={match.away.color} />
          <div style={{ minWidth: 0 }}>
            <div className="team-name">{match.away.name}</div>
            <div className="team-rank">
              <FormBar form={match.away.form} />
              {match.away.rank != null ? <>{' · '}<span className="muted">#{match.away.rank}</span></> : null}
            </div>
          </div>
        </div>
      </div>

      <div className="match-actions">
        <span style={{ flex: 1, fontSize: 11, color: '#666', letterSpacing: '.06em', textTransform: 'uppercase', fontWeight: 600 }}>
          <Icon name="pin" size={12} /> {match.venue}
        </span>
        {isFinished ? (
          <button className="btn btn-ghost btn-sm">{t.review} <Icon name="chevron" size={14} /></button>
        ) : isLive ? (
          <button className="btn btn-primary btn-sm">{t.view} <Icon name="chevron" size={14} /></button>
        ) : (
          <button className="btn btn-primary btn-sm">{t.analyze} <Icon name="sparkle" size={14} /></button>
        )}
      </div>
    </div>
  );
};

const BarCompare = ({ label, left, right, leftMax, rightMax, leftLabel, rightLabel }) => {
  const lMax = leftMax || Math.max(left, right);
  const rMax = rightMax || Math.max(left, right);
  const lPct = Math.min(100, (left / (left + right)) * 100);
  const rPct = 100 - lPct;
  return (
    <div className="bar-compare">
      <div className="lbl">{label}</div>
      <div className="val">{left}{leftLabel}</div>
      <div className="bars">
        <div className="bar-l" style={{ width: `${lPct}%` }} />
        <div className="bar-r" style={{ width: `${rPct}%` }} />
      </div>
      <div className="val right">{right}{rightLabel}</div>
    </div>
  );
};

const Gauge = ({ value = 0, max = 100 }) => {
  const radius = 70;
  const circ = Math.PI * radius;
  const offset = circ - (Math.min(value, max) / max) * circ;
  return (
    <div className="gauge">
      <svg viewBox="0 0 160 90">
        <path className="gauge-track" d="M 10 80 A 70 70 0 0 1 150 80" />
        <path className="gauge-fill"  d="M 10 80 A 70 70 0 0 1 150 80"
              strokeDasharray={circ} strokeDashoffset={offset} />
      </svg>
      <div className="gauge-val">{value}%</div>
    </div>
  );
};

const Switch = ({ on, onClick }) => (
  <div className="switch" data-on={on} onClick={onClick} role="switch" aria-checked={on} />
);

Object.assign(window, { Icon, Pill, Stat, Crest, FormBar, MatchCard, BarCompare, Gauge, Switch });
