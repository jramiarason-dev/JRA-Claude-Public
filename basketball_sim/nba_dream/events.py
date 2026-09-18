import random
from typing import Optional

# Events are drawn BEFORE the season is simulated, so none of them may claim a
# sporting outcome (a title, an MVP trophy). Those are produced by the playoff and
# award systems and shown in their own sections — otherwise the bilan contradicts
# itself. `min_rep` / `min_minutes` keep each event plausible for the player's status.
POSITIVE_EVENTS = [
    {"id": "breakout_game", "title": "🔥 Match Référence", "description": "Tu réalises le meilleur match de ta carrière. La salle explose.", "reputation_bonus": 8, "morale_bonus": 15, "stat_boost": {"shooting": 2}, "min_minutes": 18},
    {"id": "scout_workout", "title": "👁️ Workout NBA", "description": "Un scout NBA t'invite à un workout privé. Tu l'impressionnes.", "reputation_bonus": 12, "morale_bonus": 10, "stat_boost": {}, "min_rep": 30},
    {"id": "media_coverage", "title": "📺 Couverture Médias", "description": "Une chaîne internationale te consacre un reportage.", "reputation_bonus": 10, "morale_bonus": 8, "stat_boost": {"mental": 2}, "min_rep": 35},
    {"id": "training_breakthrough", "title": "💪 Percée à l'Entraînement", "description": "Tu trouves un nouveau mouvement signature. Ton coach est bluffé.", "reputation_bonus": 5, "morale_bonus": 12, "stat_boost": {"athleticism": 3, "shooting": 2}},
    {"id": "team_captain", "title": "📣 Capitaine de l'Équipe", "description": "Ton équipe te nomme capitaine. Tu portes le brassard avec fierté.", "reputation_bonus": 6, "morale_bonus": 15, "stat_boost": {"leadership": 4, "mental": 2}, "min_minutes": 24},
    {"id": "national_team", "title": "🏳️ Sélection Nationale", "description": "Tu es appelé en équipe nationale pour la première fois.", "reputation_bonus": 14, "morale_bonus": 20, "stat_boost": {"mental": 3, "basketball_iq": 2}, "min_rep": 45},
    {"id": "mentor", "title": "🎓 Mentor Légendaire", "description": "Un ancien international te prend sous son aile pour des sessions privées.", "reputation_bonus": 8, "morale_bonus": 10, "stat_boost": {"shooting": 3, "basketball_iq": 3, "mental": 2}},
    {"id": "gym_rat", "title": "🌙 Séances de Nuit", "description": "Tu restes au gymnase bien après les autres, tous les soirs de la saison.", "reputation_bonus": 2, "morale_bonus": 6, "stat_boost": {"shooting": 2, "mental": 2}},
]

NEGATIVE_EVENTS = [
    {"id": "minor_injury", "title": "🤕 Blessure Légère", "description": "Une entorse à la cheville te met à l'écart 3 semaines. Coup dur.", "reputation_bonus": -3, "morale_bonus": -10, "games_missed": 5, "stat_boost": {"athleticism": -1}, "fitness_penalty": 15},
    {"id": "major_injury", "title": "💔 Blessure Grave", "description": "Rupture du ligament croisé. Saison terminée. Long chemin de croix.", "reputation_bonus": -10, "morale_bonus": -25, "games_missed": 30, "stat_boost": {"athleticism": -3}, "fitness_penalty": 35},
    {"id": "slump", "title": "📉 Passage à Vide", "description": "Tu traverses une période de doute. 8 matchs sans marquer plus de 10 points.", "reputation_bonus": -5, "morale_bonus": -15, "games_missed": 0, "stat_boost": {"mental": -2}, "fitness_penalty": 0},
    {"id": "coach_conflict", "title": "😤 Conflit avec le Coach", "description": "Désaccord tactique avec le coach. Tu te retrouves sur le banc.", "reputation_bonus": -4, "morale_bonus": -20, "games_missed": 6, "stat_boost": {}, "fitness_penalty": 0},
    {"id": "family_issue", "title": "🏠 Problème Personnel", "description": "Des difficultés familiales t'affectent. Tu n'arrives pas à te concentrer.", "reputation_bonus": -2, "morale_bonus": -15, "games_missed": 2, "stat_boost": {"mental": -1}, "fitness_penalty": 5},
]

NEUTRAL_EVENTS = [
    {"id": "transfer_offer", "title": "📋 Offre de Transfert", "description": "Une équipe de la ligue supérieure se renseigne sur toi.", "reputation_bonus": 5, "morale_bonus": 10},
    {"id": "contract_renewal", "title": "✍️ Marque de Confiance", "description": "Ton club affiche publiquement sa confiance en toi.", "reputation_bonus": 3, "morale_bonus": 8},
    {"id": "documentary", "title": "🎬 Documentaire", "description": "Une chaîne suit ta saison pour un documentaire.", "reputation_bonus": 7, "morale_bonus": 5, "min_rep": 25},
    {"id": "quiet_season", "title": "🔁 Saison sans Relief", "description": "Rien de marquant. Du travail, des matchs, de la routine.", "reputation_bonus": 0, "morale_bonus": 0},
]


def _eligible(pool: list, reputation: int, minutes: float) -> list:
    return [e for e in pool
            if reputation >= e.get("min_rep", 0) and minutes >= e.get("min_minutes", 0)]


def get_random_event(reputation: int, morale: int, season_number: int,
                     minutes: float = 30.0) -> dict:
    """Pick a season event that stays plausible for the player's current standing."""
    roll = random.random()
    positive_chance = 0.35 + (reputation / 200) + (morale / 400)
    negative_chance = 0.25 - (morale / 400)

    if roll < negative_chance:
        pool, kind = NEGATIVE_EVENTS, "negative"
    elif roll < positive_chance + negative_chance:
        pool, kind = POSITIVE_EVENTS, "positive"
    else:
        pool, kind = NEUTRAL_EVENTS, "neutral"

    candidates = _eligible(pool, reputation, minutes)
    if not candidates:
        candidates, kind = _eligible(NEUTRAL_EVENTS, reputation, minutes), "neutral"
    event = random.choice(candidates).copy()
    event["type"] = kind
    return event

def get_draft_event(prospect_score: int, age: int) -> Optional[dict]:
    if age > 25:
        return None
    if prospect_score >= 85:
        return {"round": 1, "pick": random.choice(list(range(1, 6))), "team": random.choice(["Los Angeles Lakers", "Golden State Warriors", "Boston Celtics", "Miami Heat", "Oklahoma City Thunder"])}
    elif prospect_score >= 75:
        return {"round": 1, "pick": random.choice(list(range(6, 16))), "team": random.choice(["Dallas Mavericks", "Phoenix Suns", "Denver Nuggets", "Milwaukee Bucks", "Toronto Raptors"])}
    elif prospect_score >= 65:
        return {"round": 1, "pick": random.choice(list(range(16, 31))), "team": random.choice(["Chicago Bulls", "New York Knicks", "Washington Wizards", "Orlando Magic", "Charlotte Hornets"])}
    elif prospect_score >= 55:
        return {"round": 2, "pick": random.choice(list(range(31, 51))), "team": random.choice(["Sacramento Kings", "Detroit Pistons", "Indiana Pacers", "Cleveland Cavaliers", "San Antonio Spurs"])}
    elif prospect_score >= 48:
        return {"round": 0, "pick": 0, "team": random.choice(["Memphis Grizzlies", "Minnesota Timberwolves", "Portland Trail Blazers"])}
    return None
