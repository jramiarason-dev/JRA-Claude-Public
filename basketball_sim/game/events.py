import random
from typing import Optional

POSITIVE_EVENTS = [
    {"id": "breakout_game", "title": "🔥 Match Référence", "description": "Tu réalises le meilleur match de ta carrière. 42 points, la salle explose.", "reputation_bonus": 8, "morale_bonus": 15, "stat_boost": {"shooting": 2}, "scout_notice": True},
    {"id": "mvp_season", "title": "🏆 MVP de la ligue", "description": "Tu remportes le titre de MVP de ta ligue. Ta cote monte en flèche.", "reputation_bonus": 15, "morale_bonus": 20, "stat_boost": {"basketball_iq": 2, "leadership": 3}, "scout_notice": True},
    {"id": "scout_workout", "title": "👁️ Workout NBA", "description": "Un scout des Warriors t'invite à un workout privé à San Francisco. Tu l'impressionnes.", "reputation_bonus": 12, "morale_bonus": 10, "stat_boost": {}, "scout_notice": True},
    {"id": "media_coverage", "title": "📺 Couverture Médias", "description": "ESPN International te consacre un reportage. Le monde entier parle de toi.", "reputation_bonus": 10, "morale_bonus": 8, "stat_boost": {"mental": 2}, "scout_notice": True},
    {"id": "playoff_hero", "title": "🎯 Héros des Playoffs", "description": "Tu marques le panier de la victoire en finale. Ton équipe est championne.", "reputation_bonus": 12, "morale_bonus": 20, "stat_boost": {"mental": 3, "leadership": 2}, "scout_notice": True},
    {"id": "training_breakthrough", "title": "💪 Percée à l'Entraînement", "description": "Tu trouves un nouveau mouvement signature. Ton coach est bluffé.", "reputation_bonus": 5, "morale_bonus": 12, "stat_boost": {"athleticism": 3, "shooting": 2}, "scout_notice": False},
    {"id": "team_captain", "title": "📣 Capitaine de l'Équipe", "description": "Ton équipe te nomme capitaine. Tu portes le brassard avec fierté.", "reputation_bonus": 6, "morale_bonus": 15, "stat_boost": {"leadership": 4, "mental": 2}, "scout_notice": False},
    {"id": "national_team", "title": "🏳️ Sélection Nationale", "description": "Tu es appelé en équipe nationale pour la première fois. Histoire familiale.", "reputation_bonus": 14, "morale_bonus": 20, "stat_boost": {"mental": 3, "basketball_iq": 2}, "scout_notice": True},
    {"id": "mentor", "title": "🎓 Mentor Légendaire", "description": "Tony Parker te contacte pour des sessions d'entraînement privées. Révélateur.", "reputation_bonus": 8, "morale_bonus": 10, "stat_boost": {"shooting": 3, "basketball_iq": 3, "mental": 2}, "scout_notice": False},
]

NEGATIVE_EVENTS = [
    {"id": "minor_injury", "title": "🤕 Blessure Légère", "description": "Une entorse à la cheville te met à l'écart 3 semaines. Coup dur.", "reputation_bonus": -3, "morale_bonus": -10, "games_missed": 5, "stat_boost": {"athleticism": -1}, "fitness_penalty": 15},
    {"id": "major_injury", "title": "💔 Blessure Grave", "description": "Rupture du ligament croisé. Saison terminée. Long chemin de croix.", "reputation_bonus": -10, "morale_bonus": -25, "games_missed": 30, "stat_boost": {"athleticism": -3}, "fitness_penalty": 35},
    {"id": "slump", "title": "📉 Passage à Vide", "description": "Tu traverses une période de doute. 8 matchs sans marquer plus de 10 points.", "reputation_bonus": -5, "morale_bonus": -15, "games_missed": 0, "stat_boost": {"mental": -2}, "fitness_penalty": 0},
    {"id": "coach_conflict", "title": "😤 Conflit avec le Coach", "description": "Désaccord tactique avec le coach. Tu te retrouves sur le banc.", "reputation_bonus": -4, "morale_bonus": -20, "games_missed": 6, "stat_boost": {}, "fitness_penalty": 0},
    {"id": "family_issue", "title": "🏠 Problème Personnel", "description": "Des difficultés familiales t'affectent. Tu n'arrives pas à te concentrer.", "reputation_bonus": -2, "morale_bonus": -15, "games_missed": 2, "stat_boost": {"mental": -1}, "fitness_penalty": 5},
]

NEUTRAL_EVENTS = [
    {"id": "transfer_offer", "title": "📋 Offre de Transfert", "description": "Une équipe de la ligue supérieure t'approche pour un transfert.", "reputation_bonus": 5, "morale_bonus": 10, "offers_promotion": True},
    {"id": "contract_renewal", "title": "✍️ Prolongation de Contrat", "description": "Ton club te propose de prolonger. Signe de confiance.", "reputation_bonus": 3, "morale_bonus": 8, "offers_promotion": False},
    {"id": "documentary", "title": "🎬 Documentaire", "description": "Une chaîne suit ta saison pour un documentaire. Exposition médiatique.", "reputation_bonus": 7, "morale_bonus": 5, "offers_promotion": False},
]

def get_random_event(reputation: int, morale: int, season_number: int) -> dict:
    roll = random.random()
    positive_chance = 0.35 + (reputation / 200) + (morale / 400)
    negative_chance = 0.25 - (morale / 400)
    if roll < negative_chance:
        event = random.choice(NEGATIVE_EVENTS).copy()
        event["type"] = "negative"
    elif roll < positive_chance + negative_chance:
        event = random.choice(POSITIVE_EVENTS).copy()
        event["type"] = "positive"
    else:
        event = random.choice(NEUTRAL_EVENTS).copy()
        event["type"] = "neutral"
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
