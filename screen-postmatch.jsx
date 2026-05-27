// screen-postmatch.jsx — Post-match analysis: stats, top performers, verdict

const PostMatchScreen = ({ lang, matchId, setRoute, sport }) => {
  const t = window.I18N[lang];
  const match = (window.MATCHES[sport] || []).find(m => m.id === matchId);
  if (!match) return <div className="page"><div className="card">{t.no_data}</div></div>;

  // Synthetic per-sport stats
  const sportType = sport;
  const stats = sportType === 'football' ? [
    { label: t.possession, l: 58, r: 42, suffix: '%' },
    { label: t.shots, l: 16, r: 9 },
    { label: t.shots_on_target, l: 7, r: 3 },
    { label: t.xg, l: 2.4, r: 1.1, fixed: 1 },
    { label: t.passes, l: 614, r: 412 },
    { label: t.pass_accuracy, l: 89, r: 81, suffix: '%' },
    { label: t.corners, l: 8, r: 3 },
    { label: t.fouls, l: 10, r: 14 },
  ] : sportType === 'basket' ? [
    { label: lang==='fr'?'Points':'Points', l: match.score?.home || 118, r: match.score?.away || 109 },
    { label: lang==='fr'?'Rebonds':'Rebounds', l: 44, r: 38 },
    { label: lang==='fr'?'Passes décisives':'Assists', l: 28, r: 22 },
    { label: lang==='fr'?'% tir':'FG%', l: 51, r: 44, suffix: '%' },
    { label: lang==='fr'?'% à 3 pts':'3P%', l: 42, r: 33, suffix: '%' },
    { label: lang==='fr'?'Pertes de balle':'Turnovers', l: 11, r: 16 },
  ] : [
    { label: lang==='fr'?'Points':'Points', l: match.score?.home || 31, r: match.score?.away || 28 },
    { label: lang==='fr'?'Essais':'Tries', l: 4, r: 3 },
    { label: lang==='fr'?'Possession':'Possession', l: 54, r: 46, suffix: '%' },
    { label: lang==='fr'?'Territoire':'Territory', l: 58, r: 42, suffix: '%' },
    { label: lang==='fr'?'Mêlées gagnées':'Scrums won', l: 8, r: 6 },
    { label: lang==='fr'?'Pénalités':'Penalties', l: 9, r: 13 },
    { label: lang==='fr'?'Plaquages réussis':'Tackles made', l: 142, r: 168 },
    { label: lang==='fr'?'% conservation ruck':'Ruck retention', l: 94, r: 88, suffix: '%' },
  ];

  const performers = sportType === 'football' ? [
    { num: 25, name: 'Alexander-Arnold', team: 'LIV', pos: 'Latéral D.', rating: 9.2, stat: '1 but · 2 passes déc.' },
    { num: 11, name: 'Salah', team: 'LIV', pos: 'Ailier D.', rating: 8.7, stat: '2 buts · xG 1.4' },
    { num: 7,  name: 'Son',  team: 'TOT', pos: 'Ailier G.', rating: 7.4, stat: '1 but · 4 tirs' },
    { num: 10, name: 'Maddison', team: 'TOT', pos: 'MOC', rating: 6.1, stat: '32 passes · 75%' },
  ] : sportType === 'basket' ? [
    { num: 15, name: 'N. Jokic', team: 'DEN', pos: 'C',  rating: 9.6, stat: '32 PTS · 14 AST · 11 REB' },
    { num: 27, name: 'J. Murray', team: 'DEN', pos: 'PG', rating: 8.8, stat: '28 PTS · 9 AST' },
    { num: 34, name: 'G. Antetokounmpo', team: 'MIL', pos: 'PF', rating: 8.4, stat: '34 PTS · 12 REB' },
    { num: 22, name: 'K. Middleton', team: 'MIL', pos: 'SF', rating: 6.7, stat: '14 PTS · 5 AST' },
  ] : [
    { num: 10, name: 'A. Dupont', team: 'FRA', pos: 'Demi de mêlée', rating: 9.5, stat: '2 essais · 8 plaquages' },
    { num: 15, name: 'T. Ramos', team: 'FRA', pos: 'Arrière', rating: 8.9, stat: '13 pts au pied' },
    { num: 8,  name: 'A. Savea', team: 'NZL', pos: '3e ligne', rating: 8.6, stat: '1 essai · 18 plaquages' },
    { num: 11, name: 'R. Ioane', team: 'NZL', pos: 'Ailier', rating: 7.5, stat: '142 m parcourus' },
  ];

  const timeline = sportType === 'football' ? [
    { min: "12'", event: lang==='fr'?'⚽ Salah (LIV) — passe d\'Alexander-Arnold':'⚽ Salah (LIV) — Alexander-Arnold assist', accent: true },
    { min: "28'", event: lang==='fr'?'🟨 Bissouma (TOT) — faute tactique':'🟨 Bissouma (TOT) — tactical foul' },
    { min: "41'", event: lang==='fr'?'⚽ Son (TOT) — contre rapide, égalisation':'⚽ Son (TOT) — quick counter, equaliser', accent: true },
    { min: "58'", event: lang==='fr'?'🔁 Salah → Diaz · changement offensif':'🔁 Salah → Diaz · attacking switch' },
    { min: "67'", event: lang==='fr'?'⚽ Diaz (LIV) — tête sur corner':'⚽ Diaz (LIV) — header on corner', accent: true },
    { min: "82'", event: lang==='fr'?'⚽ Salah (LIV) — penalty':'⚽ Salah (LIV) — penalty', accent: true },
    { min: "90+3'", event: lang==='fr'?'Fin de match · victoire LIV 3-1':'Final whistle · LIV win 3-1' },
  ] : sportType === 'basket' ? [
    { min: 'Q1', event: lang==='fr'?'Nuggets prennent les commandes 32-24':'Nuggets take the lead 32-24', accent: true },
    { min: 'Q2', event: lang==='fr'?'Run 14-2 mené par Jokic':'14-2 run led by Jokic', accent: true },
    { min: 'Q3', event: lang==='fr'?'Antetokounmpo revient à 7 pts':'Antetokounmpo cuts deficit to 7' },
    { min: 'Q4', event: lang==='fr'?'Murray + Jokic ferment le match':'Murray + Jokic close the game', accent: true },
  ] : [
    { min: "8'",  event: lang==='fr'?'🏉 Essai Dupont (FRA), transformation Ramos':'🏉 Try Dupont (FRA), Ramos conversion', accent: true },
    { min: "24'", event: lang==='fr'?'🏉 Essai Ioane (NZL), pénalité réussie':'🏉 Try Ioane (NZL), penalty successful', accent: true },
    { min: "48'", event: lang==='fr'?'Carton jaune Savea (NZL) — plaquage haut':'Yellow card Savea (NZL) — high tackle' },
    { min: "67'", event: lang==='fr'?'🏉 Essai Penaud (FRA) — action collective':'🏉 Try Penaud (FRA) — team move', accent: true },
    { min: "80'", event: lang==='fr'?'Coup de sifflet final · FRA 31-28 NZL':'Final whistle · FRA 31-28 NZL' },
  ];

  return (
    <div className="page">
      <div className="page-head">
        <div>
          <button className="btn btn-ghost btn-sm" onClick={() => setRoute('history')} style={{ marginBottom: 8 }}>
            ← {lang === 'fr' ? 'Retour' : 'Back'}
          </button>
          <h1 className="page-title">{t.post_match}</h1>
          <p className="page-sub">
            <span style={{color:'var(--accent)'}}>{match.competition}</span> · {match.venue} · {match.date}
          </p>
        </div>
        <div className="row" style={{gap: 10}}>
          <button className="btn btn-ghost"><Icon name="share" size={14} /> {t.share}</button>
          <button className="btn btn-ghost"><Icon name="download" size={14} /> {t.export_pdf}</button>
        </div>
      </div>

      {/* Score banner */}
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
              <div style={{fontSize: 12, color: '#888'}}>#{match.home.rank}</div>
            </div>
          </div>

          <div className="match-vs">
            <div style={{ fontFamily: 'var(--font-display)', fontSize: 11, color: '#888', letterSpacing: '.12em' }}>
              {t.full_time}
            </div>
            <div style={{
              fontFamily: 'var(--font-display)', fontSize: 56,
              color: '#fff', letterSpacing: '.06em', lineHeight: 1,
              display: 'flex', alignItems: 'center', gap: 14,
            }}>
              <span style={{
                color: match.score.home > match.score.away ? 'var(--accent)' : '#fff',
              }}>{match.score.home}</span>
              <span style={{color:'#444', fontSize: 32}}>—</span>
              <span style={{
                color: match.score.away > match.score.home ? 'var(--accent)' : '#fff',
              }}>{match.score.away}</span>
            </div>
            <Pill kind="finished">✓ {t.finished}</Pill>
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
              <div style={{fontSize: 12, color: '#888'}}>#{match.away.rank}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Verdict */}
      <div className="verdict fade-in" style={{ marginBottom: 20 }}>
        <p className="verdict-quote">
          {lang === 'fr' ? match.verdict_fr : match.verdict_en}
        </p>
        <div className="verdict-attr">
          {t.verdict} · {lang === 'fr' ? 'Généré par CoachIQ' : 'Generated by CoachIQ'}
        </div>
      </div>

      <div className="grid" style={{ gridTemplateColumns: 'minmax(0, 1.4fr) minmax(0, 1fr)', gap: 18 }}>
        <div className="col">
          {/* Stats */}
          <div className="card">
            <div className="card-head">
              <div>
                <h3 className="card-title">{t.key_stats}</h3>
                <p className="card-sub">{match.home.name} <span style={{color: '#444'}}>vs</span> {match.away.name}</p>
              </div>
              <Pill>Opta · live</Pill>
            </div>
            <div className="col" style={{ gap: 4 }}>
              {stats.map((s, i) => (
                <BarCompare key={i}
                  label={s.label}
                  left={s.fixed ? s.l.toFixed(s.fixed) : s.l}
                  right={s.fixed ? s.r.toFixed(s.fixed) : s.r}
                  leftLabel={s.suffix || ''} rightLabel={s.suffix || ''} />
              ))}
            </div>
          </div>

          {/* Top performers */}
          <div className="card">
            <div className="card-head">
              <h3 className="card-title">{t.top_performers}</h3>
              <span style={{ fontSize: 11, color: '#666' }}>{t.rating} / 10</span>
            </div>
            <div className="col" style={{ gap: 0 }}>
              {performers.map((p, i) => (
                <div key={i} className="player-row">
                  <div className="player-num">{p.num}</div>
                  <div className="player-photo">{p.name.split(' ').map(x => x[0]).join('').slice(0,2)}</div>
                  <div>
                    <div className="player-name">{p.name}</div>
                    <div className="player-meta">{p.team} · {p.pos} · {p.stat}</div>
                  </div>
                  <div></div>
                  <div className={`rating-badge ${p.rating >= 8.5 ? 'high' : p.rating >= 7 ? 'mid' : ''}`}>
                    {p.rating.toFixed(1)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="col">
          {/* Timeline */}
          <div className="card">
            <div className="card-head">
              <h3 className="card-title">{t.timeline}</h3>
            </div>
            <div className="timeline">
              {timeline.map((ev, i) => (
                <div key={i} className={`timeline-item ${ev.accent ? 'accent' : ''}`}>
                  <div className="timeline-min">{ev.min}</div>
                  <div className="timeline-event">{ev.event}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Win deltas */}
          <div className="card">
            <div className="card-head">
              <h3 className="card-title">{lang==='fr'?'Différentiel attendu':'Expected delta'}</h3>
            </div>
            <div className="col" style={{ gap: 12 }}>
              <div className="tile">
                <div style={{fontSize: 11, color: '#888', letterSpacing: '.1em', textTransform: 'uppercase', marginBottom: 6, fontWeight: 700}}>
                  {lang==='fr'?'Score prédit':'Predicted score'}
                </div>
                <div style={{fontFamily: 'var(--font-display)', fontSize: 24, color: '#fff', letterSpacing: '.04em'}}>
                  2 – 1
                </div>
                <div style={{fontSize: 12, color: 'var(--accent)', marginTop: 4}}>
                  ✓ {lang==='fr'?'Vainqueur correct':'Winner correct'}
                </div>
              </div>
              <div className="tile">
                <div style={{fontSize: 11, color: '#888', letterSpacing: '.1em', textTransform: 'uppercase', marginBottom: 6, fontWeight: 700}}>
                  {lang==='fr'?'xG total':'Total xG'}
                </div>
                <div style={{fontFamily: 'var(--font-display)', fontSize: 24, color: '#fff', letterSpacing: '.04em'}}>
                  3.50
                </div>
                <div style={{fontSize: 12, color: '#888', marginTop: 4}}>
                  {lang==='fr'?'pour 4 buts marqués':'for 4 goals scored'}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="footer">{t.footer}</div>
    </div>
  );
};

Object.assign(window, { PostMatchScreen });
