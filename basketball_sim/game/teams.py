"""Team offers: role within the roster drives minutes, stats, salary, XP and title odds."""
import random

from .leagues import LEAGUES

# A bigger role means more minutes, more stats, more money and more visibility.
# A smaller role on a stronger roster means less production but faster learning
# (you practice against better players) and much better title odds.
ROLES = {
    "Franchise Player": {
        "icon": "⭐", "minutes": 36, "usage": 1.30, "xp_mult": 1.00,
        "salary_mult": 2.40, "rep_mult": 1.45,
        "desc": "Le système tourne autour de toi. Ballon, pression, projecteurs.",
    },
    "Titulaire": {
        "icon": "🏀", "minutes": 30, "usage": 1.05, "xp_mult": 1.15,
        "salary_mult": 1.35, "rep_mult": 1.15,
        "desc": "Dans le cinq majeur, un rôle clair, de vraies responsabilités.",
    },
    "6ème Homme": {
        "icon": "🔥", "minutes": 23, "usage": 0.88, "xp_mult": 1.32,
        "salary_mult": 0.95, "rep_mult": 0.92,
        "desc": "Premier relanceur du banc. Moins de stats, plus d'apprentissage.",
    },
    "Rotation": {
        "icon": "🔄", "minutes": 15, "usage": 0.68, "xp_mult": 1.45,
        "salary_mult": 0.68, "rep_mult": 0.70,
        "desc": "Minutes limitées, mais tu t'entraînes tous les jours avec l'élite.",
    },
    "Bout de Banc": {
        "icon": "🪑", "minutes": 7, "usage": 0.45, "xp_mult": 1.60,
        "salary_mult": 0.45, "rep_mult": 0.45,
        "desc": "Tu joues peu. Tu apprends énormément. Tu gagnes peut-être un titre.",
    },
}

ROLE_ORDER = ["Bout de Banc", "Rotation", "6ème Homme", "Titulaire", "Franchise Player"]

# Overall rating expected of a solid starter at each league level. Role offers are
# graded against this, not against the raw difficulty coefficient.
STARTER_BASELINE = {1: 32, 2: 44, 3: 53, 4: 62, 5: 71, 6: 79}


def starter_baseline(league: str) -> int:
    return STARTER_BASELINE.get(LEAGUES.get(league, {}).get("level", 3), 55)


def strength_label(strength: float) -> str:
    if strength >= 0.85: return "Favori au titre"
    if strength >= 0.70: return "Contender"
    if strength >= 0.55: return "Playoffs probables"
    if strength >= 0.40: return "Milieu de tableau"
    return "Reconstruction"


def market_value(player, league: str) -> int:
    """What the player should reasonably earn in this league, for morale comparison."""
    base = LEAGUES.get(league, {}).get("salary", 0)
    return int(base * (0.4 + player.overall_rating() / 90))


def _contract_years(role: str, age: int) -> int:
    if role in ("Franchise Player", "Titulaire"):
        return 2 if age >= 31 else random.choice([2, 3, 3])
    if role == "6ème Homme":
        return random.choice([1, 2, 2])
    return random.choice([1, 1, 2])


def build_offer(player, league: str, team: str, strength: float, role: str) -> dict:
    ld = LEAGUES.get(league, {})
    r = ROLES[role]
    base = ld.get("salary", 0)
    # Stronger rosters pay better for the same role; so does a higher overall.
    salary = int(base * r["salary_mult"] * (0.75 + strength * 0.55)
                 * (0.65 + player.overall_rating() / 110))
    salary = int(round(salary / 500.0)) * 500 if salary else 0
    return {
        "league": league,
        "team": team,
        "role": role,
        "strength": round(strength, 2),
        "salary": salary,
        "years": _contract_years(role, player.age),
        "minutes": r["minutes"],
    }


def generate_team_offers(player, league: str, n_offers: int = 3) -> list:
    """Offers trade role against roster quality: star on a weak team vs bench on a contender."""
    ld = LEAGUES.get(league, {})
    teams = ld.get("teams", ["Équipe"])
    picked = random.sample(teams, min(n_offers, len(teams)))
    baseline = starter_baseline(league)

    offers = []
    for i, team in enumerate(picked):
        # Spread the field: one contender, one mid-table, one rebuilding project.
        lo, hi = [(0.72, 0.95), (0.45, 0.72), (0.20, 0.48)][i % 3]
        strength = random.uniform(lo, hi)

        # The better you are for this level, the bigger the role offered.
        # The stronger the roster, the smaller the role available to you.
        edge = (player.overall_rating() - baseline) / 6.0 - (strength - 0.5) * 4.0
        edge += random.uniform(-0.5, 0.5)
        idx = max(0, min(len(ROLE_ORDER) - 1, round(2 + edge)))
        offers.append(build_offer(player, league, team, strength, ROLE_ORDER[idx]))
    return offers


def generate_draft_offers(player, draft_round: int, draft_pick: int) -> list:
    """NBA offers shaped by where you were picked. Early picks land on rebuilding teams."""
    nba = LEAGUES["NBA"]
    teams = random.sample(nba["teams"], 3)

    if draft_round == 1 and draft_pick <= 5:
        bands, roles = [(0.15, 0.40), (0.30, 0.55), (0.20, 0.45)], ["Franchise Player", "Titulaire", "Franchise Player"]
    elif draft_round == 1 and draft_pick <= 14:
        bands, roles = [(0.25, 0.50), (0.55, 0.75), (0.40, 0.65)], ["Titulaire", "6ème Homme", "Titulaire"]
    elif draft_round == 1:
        bands, roles = [(0.60, 0.85), (0.45, 0.70), (0.70, 0.92)], ["6ème Homme", "Titulaire", "Rotation"]
    elif draft_round == 2:
        bands, roles = [(0.50, 0.80), (0.30, 0.60), (0.75, 0.95)], ["Rotation", "6ème Homme", "Bout de Banc"]
    else:  # undrafted / two-way
        bands, roles = [(0.35, 0.65), (0.70, 0.95), (0.25, 0.55)], ["Bout de Banc", "Bout de Banc", "Rotation"]

    return [build_offer(player, "NBA", t, random.uniform(*b), r)
            for t, b, r in zip(teams, bands, roles)]
