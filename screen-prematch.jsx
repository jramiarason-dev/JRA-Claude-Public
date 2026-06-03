// screen-prematch.jsx — Pre-match analysis: formation, key matchups, prediction

const Pitch = ({ lineup, color }) => {
  if (!lineup) return null;
  return (
    <div className="pitch">
      {/* Field markings */}
      <div className="pitch-line" style={{ left: '50%', top: 0, bottom: 0, width: 1 }} />
      <div className="pitch-circle" style={{ left: '50%', top: '50%', width: 80, height: 80, transform: 'translate(-50%, -50%)' }} />
      <div className="pitch-line" style={{ left: '50%', top: '50%', width: 4, height: 4, borderRadius: '50%', transform: 'translate(-50%,-50%)', background: 'rgba(255,255,255,.3)' }} />
      {/* Penalty boxes */}
      <div style={{ position: 'absolute', left: '20%', right: '20%', top: 0, height: '14%', border: '1px solid rgba(255,255,255,.18)', borderTop: 0 }} />
      <div style={{ position: 'absolute', left: '30%', right: '30%', top: 0, height: '6%', border: '1px solid rgba(255,255,255,.18)', borderTop: 0 }} />
      <div style={{ position: 'absolute', left: '20%', right: '20%', bottom: 0, height: '14%', border: '1px solid rgba(255,255,255,.18)', borderBottom: 0 }} />
      <div style={{ position: 'absolute', left: '30%', right: '30%', bottom: 0, height: '6%', border: '1px solid rgba(255,255,255,.18)', borderBottom: 0 }} />

      {lineup.players.map((p, i) => (
        <div key={i} className="pitch-player" style={{ left: `${p.x}%`, top: `${p.y}%` }}>
          <div className="ball" style={{ background: color }}>{p.num}</div>
          <div className="pname">{p.name}</div>
        </div>
      ))}
    </div>
  );
};

const PreMatchScreen = ({ lang, matchId, setRoute, sport }) => {
  const t = window.I18N[lang];
  const match = (window.MATCHES[sport] || []).find(m => m.id === matchId);
  const [view, setView] = React.useState('home'); // 'home' | 'away' | 'both'

  if (!match) return <div className="page"><div className="card">{t.no_data}</div></div>;
  const lineup = window.LINEUPS[matchId];
  const matchups = (window.MATCHUPS && window.MATCHUPS[matchId]) || [];
  const odds = match.odds || { home: 2.0, draw: 3.5, away: 3.0 };
  const total = (1/odds.home) + (odds.draw ? 1/odds.draw : 0) + (1/odds.away);
  const probs = {
    home: Math.round(((1/odds.home) / total) * 100),
    draw: odds.draw ? Math.round(((1/odds.draw) / total) * 100) : 0,
    away: Math.round(((1/odds.away) / total) * 100),
  };

  return (
    <div className="page">
      <div className="page-head">
        <div>
          <button className="btn btn-ghost btn-sm" onClick={() => setRoute('matches')} style={{ marginBottom: 8 }}>
            ← {lang === 'fr' ? 'Retour aux matchs' : 'Back to matches'}
          </button>
          <h1 className="page-title">{t.pre_match}</h1>
          <p className="page-sub">
            <span style={{color:'var(--accent)'}}>{match.competition}</span> · {match.venue} · {match.date}
          </p>
        </div>
        <div className="row" style={{gap: 10}}>
          <button className="btn btn-ghost"><Icon name="share" size={14} /> {t.share}</button>
          <button className="btn btn-primary"><Icon name="sparkle" size={14} /> {t.generate}</button>
        </div>
      </div>

      {/* Match banner */}
      <div className="card" style={{
        marginBottom: 20,
        background: `linear-gradient(135deg, ${match.home.color}26, transparent 40%, transparent 60%, ${match.away.color}26)`,
      }}>
        <div className="match-teams" style={{ gap: 24 }}>
          <div className="team" style={{ gap: 16 }}>
            <div className="team-crest" style={{
              width: 64, height: 64, fontSize: 20,
              background: `linear-gradient(135deg, ${match.home.color}, ${match.home.color}cc)`
            }}>{match.home.code}</div>
            <div>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: 26, color: '#fff', letterSpacing: '0.04em' }}>
                {match.home.name}
              </div>
              <div style={{fontSize: 12, color: '#888'}}>#{match.home.rank} · <FormBar form={match.home.form} /></div>
            </div>
          </div>

          <div className="match-vs">
            <div style={{ fontFamily: 'var(--font-display)', fontSize: 12, color: '#888', letterSpacing: '.12em' }}>
              {t.predicted_score}
            </div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: 44, color: 'var(--accent)', letterSpacing: '.04em', lineHeight: 1 }}>
              {match.predicted || '–'}
            </div>
            <div className="match-time">{match.date}</div>
          </div>

          <div className="team away" style={{ gap: 16 }}>
            <div className="team-crest" style={{
              width: 64, height: 64, fontSize: 20,
              background: `linear-gradient(135deg, ${match.away.color}, ${match.away.color}cc)`
            }}>{match.away.code}</div>
            <div style={{textAlign: 'right'}}>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: 26, color: '#fff', letterSpacing: '0.04em' }}>
                {match.away.name}
              </div>
              <div style={{fontSize: 12, color: '#888'}}><FormBar form={match.away.form} /> · #{match.away.rank}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid" style={{ gridTemplateColumns: 'minmax(0, 1.4fr) minmax(0, 1fr)', gap: 18 }}>
        {/* Left col — Formation */}
        <div className="col">
          <div className="card">
            <div className="card-head">
              <div>
                <h3 className="card-title">{t.formation}</h3>
                <p className="card-sub">{t.expected_lineups}</p>
              </div>
              <div className="tab-strip">
                <button data-active={view === 'home'} onClick={() => setView('home')}>{match.home.code}</button>
                <button data-active={view === 'away'} onClick={() => setView('away')}>{match.away.code}</button>
              </div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 16 }}>
              <div>
                <div className="row" style={{justifyContent: 'space-between', marginBottom: 10, alignItems: 'baseline'}}>
                  <div style={{fontFamily: 'var(--font-display)', fontSize: 14, color: '#fff', letterSpacing: '.06em'}}>
                    {view === 'home' ? match.home.name : match.away.name}
                  </div>
                  <Pill kind="accent">
                    {view === 'home' ? (lineup?.home.formation || '4-3-3') : (lineup?.away.formation || '3-4-2-1')}
                  </Pill>
                </div>
                <Pitch
                  lineup={view === 'home' ? lineup?.home : lineup?.away}
                  color={view === 'home' ? match.home.color : match.away.color}
                />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-head">
              <h3 className="card-title">{t.key_matchups}</h3>
            </div>
            <div className="col" style={{ gap: 10 }}>
              {matchups.length === 0 && (
                <div style={{ color: '#666', fontSize: 13 }}>{t.no_data}</div>
              )}
              {matchups.map((d, i) => (
                <div key={i} className="tile" style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', gap: 14, alignItems: 'center' }}>
                  <div>
                    <div className="kv-val">{d.home.name}</div>
                    <div className="kv-key">{d.home.pos}</div>
                  </div>
                  <div style={{
                    fontFamily: 'var(--font-display)', fontSize: 16,
                    letterSpacing: '.06em',
                    color: d.edge === 'home' ? 'var(--accent)' : d.edge === 'away' ? '#fde047' : '#666',
                  }}>
                    {d.edge === 'home' ? '◄' : d.edge === 'away' ? '►' : '◆'}
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div className="kv-val">{d.away.name}</div>
                    <div className="kv-key">{d.away.pos}</div>
                  </div>
                  <div style={{ gridColumn: '1 / -1', fontSize: 12, color: '#999' }}>{d.note}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right col */}
        <div className="col">
          <div className="card">
            <div className="card-head">
              <h3 className="card-title">{t.win_probability}</h3>
            </div>
            <div className="col" style={{ gap: 14 }}>
              {[
                { label: match.home.name, code: match.home.code, value: probs.home, color: match.home.color, side: 'home' },
                ...(odds.draw ? [{ label: t.draw, code: '=', value: probs.draw, color: '#444', side: 'draw' }] : []),
                { label: match.away.name, code: match.away.code, value: probs.away, color: match.away.color, side: 'away' },
              ].map((p) => (
                <div key={p.side}>
                  <div className="row" style={{ justifyContent: 'space-between', marginBottom: 6 }}>
                    <span style={{ fontSize: 13, fontWeight: 600, color: '#fff' }}>
                      <span style={{
                        display: 'inline-block', width: 8, height: 8, borderRadius: 2,
                        background: p.color, marginRight: 8,
                      }}/>
                      {p.label}
                    </span>
                    <span style={{ fontFamily: 'var(--font-display)', fontSize: 20, color: '#fff', letterSpacing: '.04em' }}>
                      {p.value}%
                    </span>
                  </div>
                  <div className="progress">
                    <span style={{ width: `${p.value}%`, background: p.side === 'home' ? 'var(--accent)' : p.color }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="card-head">
              <h3 className="card-title">{t.tactical_brief}</h3>
              <Pill kind="accent">AI</Pill>
            </div>
            <div className="col" style={{ gap: 14 }}>
              <div>
                <div style={{ fontSize: 11, color: 'var(--accent)', letterSpacing: '.1em', fontWeight: 700, textTransform: 'uppercase', marginBottom: 8 }}>
                  {t.home_strengths}
                </div>
                <ul style={{ margin: 0, paddingLeft: 18, fontSize: 13, color: '#d0d0d0', lineHeight: 1.7 }}>
                  <li>{lang==='fr'?'Pressing haut (PPDA 8.2 — top 3 Ligue 1)':'High press (PPDA 8.2 — top 3 Ligue 1)'}</li>
                  <li>{lang==='fr'?'Conversion xG : 1.34 par match':'xG conversion: 1.34 per game'}</li>
                  <li>{lang==='fr'?'Domination sur coups de pied arrêtés':'Set-piece dominance'}</li>
                </ul>
              </div>
              <div>
                <div style={{ fontSize: 11, color: '#fde047', letterSpacing: '.1em', fontWeight: 700, textTransform: 'uppercase', marginBottom: 8 }}>
                  {t.away_strengths}
                </div>
                <ul style={{ margin: 0, paddingLeft: 18, fontSize: 13, color: '#d0d0d0', lineHeight: 1.7 }}>
                  <li>{lang==='fr'?'Bloc bas étanche (0.78 buts/match)':'Tight low block (0.78 goals/game)'}</li>
                  <li>{lang==='fr'?'Transitions rapides — 4 buts en contre':'Quick transitions — 4 counter goals'}</li>
                </ul>
              </div>
              <div>
                <div style={{ fontSize: 11, color: '#f97316', letterSpacing: '.1em', fontWeight: 700, textTransform: 'uppercase', marginBottom: 8 }}>
                  {t.watch_for}
                </div>
                <p style={{ margin: 0, fontSize: 13, color: '#d0d0d0', lineHeight: 1.6 }}>
                  {(() => {
                    const duel = matchups[2] || matchups[0];
                    const def = duel ? duel.home.name : match.home.name;
                    const att = duel ? duel.away.name : match.away.name;
                    return lang === 'fr'
                      ? `Vulnérabilité possible dans l'axe : ${def} (${match.home.code}) devra contenir les appels de ${att} (${match.away.code}) dans le dos de la défense.`
                      : `Possible central vulnerability: ${def} (${match.home.code}) must contain ${att}'s (${match.away.code}) runs in behind.`;
                  })()}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-head">
              <h3 className="card-title">{lang==='fr'?'Cotes':'Odds'}</h3>
              <span style={{ fontSize: 11, color: '#666' }}>Bookmakers · {lang==='fr'?'moyenne':'avg'}</span>
            </div>
            <div className="grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)', gap: 10 }}>
              {[
                { code: '1', label: match.home.code, val: odds.home },
                ...(odds.draw ? [{ code: 'X', label: t.draw, val: odds.draw }] : []),
                { code: '2', label: match.away.code, val: odds.away },
              ].map(c => (
                <div key={c.code} className="tile" style={{ textAlign: 'center' }}>
                  <div className="kv-key" style={{textTransform: 'uppercase'}}>{c.code} · {c.label}</div>
                  <div style={{ fontFamily: 'var(--font-display)', fontSize: 26, color: '#fff', letterSpacing: '.04em', marginTop: 4 }}>
                    {c.val.toFixed(2)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="footer">{t.footer}</div>
    </div>
  );
};

Object.assign(window, { PreMatchScreen });
