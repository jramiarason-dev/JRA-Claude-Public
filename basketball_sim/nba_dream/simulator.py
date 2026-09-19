import random

from .player import Player, SeasonRecord, PlayoffResult
from .leagues import LEAGUES, get_next_league
from .teams import ROLES, market_value, starter_baseline
from .tactics import tactic_modifiers
from .sponsors import sponsor_income, sponsor_xp, tick_sponsors
from .events import get_random_event

# Per-36-minutes production ceilings by position.
PER36_CEILING = {
    "PG": {"pts": 24, "reb": 4.5, "ast": 9.5, "stl": 2.0, "blk": 0.5},
    "SG": {"pts": 27, "reb": 5.0, "ast": 5.0, "stl": 1.7, "blk": 0.6},
    "SF": {"pts": 25, "reb": 7.5, "ast": 4.5, "stl": 1.5, "blk": 0.9},
    "PF": {"pts": 23, "reb": 10.5, "ast": 3.0, "stl": 1.0, "blk": 1.6},
    "C":  {"pts": 21, "reb": 12.5, "ast": 2.5, "stl": 0.8, "blk": 2.6},
}

XP_TABLE = {
    "base_per_league_level": {1: 30, 2: 45, 3: 60, 4: 80, 5: 110, 6: 150},
    "training_bonus": {"Tir": 15, "Athletisme": 15, "QI Basketball": 15,
                       "Mental": 15, "Physique Complet": 10},
    "award_bonus": {"MVP de la Ligue": 40, "All-Star de la Ligue": 20, "Most Improved Player": 15},
    "playoff_bonus": {"champion": 50, "finalist": 25, "semifinal": 15, "quarterfinal": 8},
    "event_bonus": {"positive": 10, "neutral": 5, "negative": 0},
}


def _ppg_xp_bonus(ppg: float) -> int:
    for threshold, bonus in [(25, 30), (20, 20), (15, 12), (10, 5)]:
        if ppg >= threshold:
            return bonus
    return 0


def _age_curve(age: int) -> float:
    """Physical output peaks in the late twenties and tails off after."""
    if age <= 19: return 0.82
    if age <= 22: return 0.92
    if age <= 27: return 1.00
    if age <= 30: return 0.97
    if age <= 33: return 0.90
    if age <= 36: return 0.80
    return 0.68


def simulate_season(player: Player, games_missed: int = 0) -> dict:
    ld = LEAGUES.get(player.current_league, {})
    if not ld:
        return {}

    difficulty = ld["difficulty"]
    schedule = ld["games"]
    role = ROLES.get(player.current_role, ROLES["Titulaire"])
    ceiling = PER36_CEILING.get(player.position, PER36_CEILING["SF"])

    tac = tactic_modifiers(player, player.current_tactic)

    # How good you are for this level of competition.
    skill = (player.overall_rating() / 100.0) / (difficulty + 0.25)
    morale_mod = 0.80 + (player.morale / 100) * 0.25
    fitness_mod = 0.85 + (player.fitness / 100) * 0.18
    efficiency = max(0.30, min(1.35, skill * morale_mod * fitness_mod
                               * _age_curve(player.age) * tac["efficiency"]))

    # Minutes come from the role; stats come from minutes. Everything stays coherent.
    mpg = round(max(3.0, min(38.0, role["minutes"] * random.uniform(0.88, 1.12)
                             + (efficiency - 0.9) * 4)), 1)
    # Minutes already carry the role. Usage only adds shot volume on top of them,
    # so it applies to scoring alone — rebounds and assists scale with time on court.
    scale = (mpg / 36.0) * efficiency

    def stat(key, noise=0.10, mult=1.0):
        return round(max(0.0, ceiling[key] * scale * mult * random.uniform(1 - noise, 1 + noise)), 1)

    ppg = stat("pts", mult=role["usage"] * tac["pts"])
    rpg, apg = stat("reb", mult=tac["reb"]), stat("ast", mult=tac["ast"])
    spg, bpg = stat("stl", 0.2), stat("blk", 0.2)

    fg_pct = round(max(0.30, min(0.62,
                   0.36 + (player.shooting / 100) * 0.14 - difficulty * 0.06
                   + (efficiency - 0.9) * 0.05 + random.uniform(-0.02, 0.02))), 3)

    # Games missed are expressed on an 82-game scale; rescale to this league's calendar.
    missed = round(games_missed * schedule / 82.0)
    availability = 0.82 + (player.fitness / 100) * 0.18
    games = max(0, min(schedule, int(schedule * availability * random.uniform(0.93, 1.0)) - missed))
    if games == 0:
        ppg = rpg = apg = spg = bpg = mpg = 0.0

    # Reputation follows production, role visibility and league exposure.
    rep = ld["reputation_gain"] * role["rep_mult"] * (0.55 + min(1.6, ppg / 16.0))
    rep *= 0.6 + ld.get("scout_presence", 0.1) * 1.2
    reputation_gained = max(0, int(rep) + random.randint(-2, 3))

    award = None
    if mpg >= 28 and ppg >= 21 and (rpg + apg) >= 9 and games >= schedule * 0.75:
        award, reputation_gained = "MVP de la Ligue", reputation_gained + 10
    elif mpg >= 25 and ppg >= 17 and games >= schedule * 0.7:
        award, reputation_gained = "All-Star de la Ligue", reputation_gained + 5
    elif player.career_history and ppg >= player.career_history[-1].ppg + 5 and games >= schedule * 0.7:
        award, reputation_gained = "Most Improved Player", reputation_gained + 3

    # A strong roster makes the playoffs; your own level and the system nudge it.
    effective_strength = max(0.05, min(0.98, player.team_strength + tac["team_strength"]))
    playoff_odds = effective_strength * 0.9 + (efficiency - 0.9) * 0.25
    playoff_qualified = random.random() < max(0.05, min(0.96, playoff_odds))

    return {
        "ppg": ppg, "rpg": rpg, "apg": apg, "spg": spg, "bpg": bpg,
        "mpg": mpg, "fg_pct": fg_pct, "games": games,
        "reputation_gained": reputation_gained, "award": award,
        "salary": player.contract_salary,
        "playoff_qualified": playoff_qualified,
        "efficiency": efficiency,
        "effective_strength": effective_strength,
        "tactic_fit": tac["fit"], "tactic_xp": tac["xp"],
        "league_level": ld.get("level", 3),
    }


def simulate_playoffs(player: Player, efficiency: float, strength: float = None) -> PlayoffResult:
    """Three rounds: quarter-final, semi-final, final. Roster quality does most of the work."""
    ld = LEAGUES.get(player.current_league, {})
    teams = [t for t in ld.get("teams", ["Adversaire"]) if t != player.current_team] or ["Adversaire"]
    strength = player.team_strength if strength is None else strength
    base = min(0.84, max(0.20, strength * 0.70 + (efficiency - 0.9) * 0.30))

    rounds_won = 0
    for i in range(3):
        opponent = random.choice(teams)
        if random.random() >= max(0.12, base - i * 0.06):
            return PlayoffResult(reached_final=(i == 2), champion=False,
                                 rounds_won=rounds_won, opponent=opponent)
        rounds_won += 1

    return PlayoffResult(reached_final=True, champion=True, rounds_won=3,
                         opponent=random.choice(teams),
                         title=f"Champion {ld.get('name', player.current_league)} 🏆")


def compute_season_xp(player: Player, sim: dict, event: dict, training_focus: str,
                      playoff) -> int:
    xp = XP_TABLE["base_per_league_level"].get(sim["league_level"], 50)
    xp += XP_TABLE["training_bonus"].get(training_focus, 10)
    xp += _ppg_xp_bonus(sim["ppg"])
    xp += XP_TABLE["award_bonus"].get(sim.get("award"), 0)
    xp += XP_TABLE["event_bonus"].get(event.get("type", "neutral"), 0)
    xp += sponsor_xp(player)

    if playoff:
        if playoff.champion:          xp += XP_TABLE["playoff_bonus"]["champion"]
        elif playoff.reached_final:   xp += XP_TABLE["playoff_bonus"]["finalist"]
        elif playoff.rounds_won >= 1: xp += XP_TABLE["playoff_bonus"]["semifinal"]
        else:                         xp += XP_TABLE["playoff_bonus"]["quarterfinal"]

    # A smaller role on a better roster teaches you more per minute played.
    xp = int(xp * ROLES.get(player.current_role, ROLES["Titulaire"])["xp_mult"])
    xp = int(xp * (0.85 + player.team_strength * 0.35))
    xp = int(xp * sim.get("tactic_xp", 1.0))
    return max(10, xp + random.randint(-5, 10))


def run_season(player: Player, training_focus: str, tactic: str = None) -> dict:
    """Play one full season and commit it to the player. Call exactly once per season."""
    if tactic:
        player.current_tactic = tactic
    player.train(training_focus)

    # A season at the same club starts before it is played, so the standing it earns
    # (cadre, capitaine, légende) applies to the season about to begin.
    player.seasons_with_team += 1
    loyalty = player.apply_loyalty_growth()

    role_minutes = ROLES.get(player.current_role, ROLES["Titulaire"])["minutes"]
    event = get_random_event(player.reputation, player.morale, player.season_number, role_minutes)
    sim = simulate_season(player, games_missed=event.get("games_missed", 0))
    # A season wiped out by injury cannot end with a playoff run.
    playoff = (simulate_playoffs(player, sim["efficiency"], sim["effective_strength"])
               if sim["playoff_qualified"] and sim["games"] > 0 else None)

    level_before = player.level

    # Reputation
    player.reputation = min(100, max(0, player.reputation
                                     + sim["reputation_gained"] + event.get("reputation_bonus", 0)))

    # Morale: event, playoff run, and how the pay compares to what you are worth.
    morale = event.get("morale_bonus", 0)
    if playoff:
        morale += 20 if playoff.champion else 10 if playoff.reached_final else 5 if playoff.rounds_won else -5
    else:
        morale -= 3
    value = market_value(player, player.current_league)
    if value > 0:
        ratio = player.contract_salary / value
        morale += 8 if ratio >= 1.4 else 4 if ratio >= 1.05 else -6 if ratio < 0.6 else 0
    morale += sum(s["morale_bonus"] for s in player.sponsors) // 2
    player.morale = min(100, max(10, player.morale + morale))

    # Event attribute effects and fitness
    for attr, delta in event.get("stat_boost", {}).items():
        if hasattr(player, attr):
            setattr(player, attr, min(99, max(1, getattr(player, attr) + delta)))
    player.fitness = max(30, player.fitness - event.get("fitness_penalty", 0))

    # Money
    salary_earned = player.contract_salary
    sponsor_earned = sponsor_income(player)
    player.total_earnings += salary_earned + sponsor_earned

    if player.current_league == "NBA":
        player.nba_seasons += 1

    xp_gained = compute_season_xp(player, sim, event, training_focus, playoff)
    levels_gained = player.gain_xp(xp_gained)

    record = SeasonRecord(
        season=player.season_number + 1, age=player.age,
        league=player.current_league, team=player.current_team, role=player.current_role,
        games=sim["games"], mpg=sim["mpg"],
        ppg=sim["ppg"], rpg=sim["rpg"], apg=sim["apg"], spg=sim["spg"], bpg=sim["bpg"],
        fg_pct=sim["fg_pct"], reputation_gained=sim["reputation_gained"],
        salary_earned=salary_earned, sponsor_earned=sponsor_earned,
        xp_gained=xp_gained, level_before=level_before, level_after=player.level,
        award=sim.get("award"), event=event.get("title"),
        training_focus=training_focus, playoff=playoff,
        tactic=player.current_tactic, tactic_fit=sim["tactic_fit"],
        club_status=player.club_status(),
    )
    player.add_season(record)

    # Advance the calendar exactly one year.
    player.season_number += 1
    player.age += 1
    player.apply_ageing()
    player.fitness = min(100, player.fitness + random.randint(6, 15))
    player.contract_years_left = max(0, player.contract_years_left - 1)
    expired_sponsors = tick_sponsors(player)

    return {
        "record": record, "sim": sim, "event": event, "playoff": playoff,
        "levels_gained": levels_gained, "expired_sponsors": expired_sponsors,
        "contract_expired": player.contract_years_left == 0,
        "loyalty": loyalty,
    }


# ── Progression gates ──────────────────────────────────────────────────────────
DRAFT_MAX_AGE = 22


def draft_eligibility_age(country: str) -> int:
    return 19 if country == "USA (NCAA)" else 18


def check_promotion_eligibility(player: Player) -> bool:
    nxt = get_next_league(player.current_league, player.country)
    if not nxt:
        return False
    if nxt == "NBA":
        return is_nba_ready(player)
    current = LEAGUES.get(player.current_league, {}).get("level", 0)
    # You move up once you're close to being a starter at the next level.
    return (player.overall_rating() >= starter_baseline(nxt) - 7
            and player.reputation >= 10 + current * 4)


def can_enter_draft(player: Player) -> bool:
    """The draft is for prospects: past DRAFT_MAX_AGE you are no longer draft-eligible.

    Declaring does not require climbing every rung of your country's ladder first —
    prospects come out of Pro B or the NCAA, not only out of the EuroLeague.
    """
    return (not player.in_nba
            and draft_eligibility_age(player.country) <= player.age <= DRAFT_MAX_AGE
            and player.nba_prospect_score() >= 52
            and player.reputation >= 32
            and player.season_number >= 1)


def can_sign_nba_contract(player: Player) -> bool:
    """Too old for the draft, so franchises sign you on your record instead — a higher bar."""
    return (not player.in_nba
            and player.age > DRAFT_MAX_AGE
            and player.overall_rating() >= starter_baseline("NBA") - 9
            and player.reputation >= 55)


def is_nba_ready(player: Player) -> bool:
    return can_enter_draft(player) or can_sign_nba_contract(player)


def run_draft(player: Player) -> dict:
    """Draft night. Where you land depends on your prospect score, with real variance."""
    score = player.nba_prospect_score() + random.randint(-6, 6)

    if score >= 88:   rnd, pick = 1, random.randint(1, 5)
    elif score >= 80: rnd, pick = 1, random.randint(4, 14)
    elif score >= 72: rnd, pick = 1, random.randint(12, 30)
    elif score >= 63: rnd, pick = 2, random.randint(31, 50)
    elif score >= 55: rnd, pick = 2, random.randint(45, 60)
    else:             rnd, pick = 0, 0

    player.drafted = rnd > 0
    player.draft_round = rnd or None
    player.draft_pick = pick or None
    return {"round": rnd, "pick": pick, "score": score}
