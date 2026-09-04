import random
from .player import Player, SeasonRecord
from .leagues import LEAGUES, get_next_league

POSITION_STAT_WEIGHTS = {
    "PG": {"pts": 0.8, "reb": 0.3, "ast": 1.0, "stl": 0.7, "blk": 0.2},
    "SG": {"pts": 1.0, "reb": 0.4, "ast": 0.5, "stl": 0.6, "blk": 0.2},
    "SF": {"pts": 0.9, "reb": 0.6, "ast": 0.4, "stl": 0.5, "blk": 0.3},
    "PF": {"pts": 0.8, "reb": 0.9, "ast": 0.3, "stl": 0.3, "blk": 0.6},
    "C":  {"pts": 0.7, "reb": 1.0, "ast": 0.2, "stl": 0.2, "blk": 1.0},
}

def simulate_season(player: Player) -> dict:
    league_data = LEAGUES.get(player.current_league, {})
    if not league_data:
        return {}
    difficulty = league_data["difficulty"]
    games_in_season = league_data["games"]
    weights = POSITION_STAT_WEIGHTS.get(player.position, POSITION_STAT_WEIGHTS["SF"])
    overall = player.overall_rating()
    performance_factor = max(0.3, min(1.8, (overall / 100) / (difficulty + 0.1)))
    morale_mod = (player.morale / 100) * 0.3 + 0.7
    fitness_mod = (player.fitness / 100) * 0.2 + 0.8
    base_factor = performance_factor * morale_mod * fitness_mod

    def stat_with_noise(base, weight, noise_range=2.5):
        return max(0, round(base * weight * base_factor + random.uniform(-noise_range, noise_range), 1))

    ppg = stat_with_noise(22, weights["pts"])
    rpg = stat_with_noise(10, weights["reb"])
    apg = stat_with_noise(8, weights["ast"])
    spg = stat_with_noise(2.5, weights["stl"])
    bpg = stat_with_noise(2.0, weights["blk"])
    fg_base = 0.3 + (player.shooting / 100) * 0.2 - difficulty * 0.05
    fg_pct = round(max(0.25, min(0.65, fg_base + random.uniform(-0.04, 0.04))), 3)
    games_played = random.randint(max(10, int(games_in_season * 0.7)), games_in_season)

    rep_base = league_data["reputation_gain"]
    if ppg > 18: rep_base = int(rep_base * 1.4)
    elif ppg > 12: rep_base = int(rep_base * 1.1)
    elif ppg < 6: rep_base = int(rep_base * 0.6)
    reputation_gained = max(0, rep_base + random.randint(-3, 5))

    award = None
    if ppg > 22 and rpg + apg > 10:
        award = "MVP de la Ligue"; reputation_gained += 8
    elif ppg > 18:
        award = "All-Star de la Ligue"; reputation_gained += 4
    elif games_played == games_in_season and ppg > 10:
        award = "Most Improved Player"; reputation_gained += 3

    return {"ppg": ppg, "rpg": rpg, "apg": apg, "spg": spg, "bpg": bpg, "fg_pct": fg_pct,
            "games": games_played, "reputation_gained": reputation_gained, "award": award,
            "salary": league_data.get("salary", 0)}

def apply_season_results(player: Player, sim: dict, event: dict) -> SeasonRecord:
    rep_gain = sim["reputation_gained"] + event.get("reputation_bonus", 0)
    player.reputation = min(100, max(0, player.reputation + rep_gain))
    player.morale = min(100, max(10, player.morale + event.get("morale_bonus", 0)))
    for attr, delta in event.get("stat_boost", {}).items():
        if hasattr(player, attr):
            setattr(player, attr, min(99, max(1, getattr(player, attr) + delta)))
    player.fitness = max(30, player.fitness - event.get("fitness_penalty", 0))
    if player.age < 26:
        for attr in ["athleticism", "shooting", "basketball_iq"]:
            setattr(player, attr, min(99, getattr(player, attr) + random.randint(0, 2)))
    player.apply_age_regression()
    player.total_earnings += sim.get("salary", 0)
    player.season_number += 1
    player.age += 1
    player.fitness = min(100, player.fitness + random.randint(5, 15))
    record = SeasonRecord(
        season=player.season_number, age=player.age - 1, league=player.current_league,
        team=player.current_team, games=sim["games"], ppg=sim["ppg"], rpg=sim["rpg"],
        apg=sim["apg"], spg=sim["spg"], bpg=sim["bpg"], fg_pct=sim["fg_pct"],
        reputation_gained=sim["reputation_gained"], award=sim.get("award"), event=event.get("title"),
    )
    player.add_season(record)
    return record

def check_promotion_eligibility(player: Player) -> bool:
    league_data = LEAGUES.get(player.current_league, {})
    next_league = get_next_league(player.current_league, player.country)
    if not next_league:
        return False
    next_level = LEAGUES.get(next_league, {}).get("level", 99)
    current_level = league_data.get("level", 0)
    overall = player.overall_rating()
    if next_level - current_level == 1:
        return overall >= 45 + (current_level * 5) and player.reputation >= 10
    return overall >= 60 and player.reputation >= 25

def get_draft_eligibility_age(country: str) -> int:
    return 19 if country == "USA (NCAA)" else 18

def is_draft_eligible(player: Player) -> bool:
    return player.age >= get_draft_eligibility_age(player.country) and player.reputation >= 20
