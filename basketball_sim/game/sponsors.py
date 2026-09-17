"""Endorsement deals: unlocked by reputation, they pay every season and boost visibility."""
import random

MAX_ACTIVE_SPONSORS = 3

SPONSOR_POOL = [
    {"name": "Décathlon Local",     "tier": "Local",         "icon": "🏪", "min_rep": 5,  "base": 3_000,     "morale": 3, "xp": 3},
    {"name": "Spalding",            "tier": "Équipementier", "icon": "🏀", "min_rep": 15, "base": 12_000,    "morale": 4, "xp": 5},
    {"name": "Peak Sport",          "tier": "Régional",      "icon": "⛰️", "min_rep": 22, "base": 25_000,    "morale": 5, "xp": 6},
    {"name": "Panini Cards",        "tier": "National",      "icon": "🃏", "min_rep": 30, "base": 45_000,    "morale": 5, "xp": 8},
    {"name": "Under Armour",        "tier": "National",      "icon": "🛡️", "min_rep": 40, "base": 110_000,   "morale": 7, "xp": 10},
    {"name": "Gatorade",            "tier": "National",      "icon": "🥤", "min_rep": 48, "base": 180_000,   "morale": 7, "xp": 11},
    {"name": "Puma Hoops",          "tier": "International", "icon": "🐆", "min_rep": 55, "base": 320_000,   "morale": 9, "xp": 13},
    {"name": "Adidas Basketball",   "tier": "International", "icon": "👟", "min_rep": 62, "base": 550_000,   "morale": 10, "xp": 15},
    {"name": "Red Bull Athletes",   "tier": "International", "icon": "🐂", "min_rep": 68, "base": 700_000,   "morale": 10, "xp": 16},
    {"name": "EA Sports NBA",       "tier": "Élite",         "icon": "🎮", "min_rep": 75, "base": 1_200_000, "morale": 12, "xp": 18},
    {"name": "Beats by Dre",        "tier": "Élite",         "icon": "🎧", "min_rep": 80, "base": 1_800_000, "morale": 12, "xp": 20},
    {"name": "Nike Signature",      "tier": "Élite",         "icon": "✔️", "min_rep": 86, "base": 4_000_000, "morale": 15, "xp": 24},
    {"name": "Jordan Brand",        "tier": "Légende",       "icon": "🐐", "min_rep": 93, "base": 9_000_000, "morale": 18, "xp": 30},
]

TIER_COLORS = {
    "Local": "#6b7280", "Équipementier": "#0ea5e9", "Régional": "#0ea5e9",
    "National": "#22c55e", "International": "#a855f7", "Élite": "#f59e0b", "Légende": "#ef4444",
}


def deal_value(sponsor: dict, player) -> int:
    """Scale the headline figure with reputation and level — stars get paid more."""
    factor = 0.6 + (player.reputation / 100) * 0.9 + (player.level / 40)
    value = int(sponsor["base"] * factor * random.uniform(0.85, 1.2))
    return int(round(value / 500.0)) * 500


def generate_sponsor_offers(player, n: int = 2) -> list:
    signed = {s["name"] for s in player.sponsors}
    eligible = [s for s in SPONSOR_POOL if s["min_rep"] <= player.reputation and s["name"] not in signed]
    if not eligible:
        return []
    # Favour the best brands the player currently qualifies for.
    eligible.sort(key=lambda s: s["min_rep"], reverse=True)
    pool = eligible[:5]
    chosen = random.sample(pool, min(n, len(pool)))
    return [{
        "name": s["name"], "tier": s["tier"], "icon": s["icon"],
        "annual_value": deal_value(s, player),
        "years": random.choice([1, 2, 2, 3]),
        "morale_bonus": s["morale"], "xp_bonus": s["xp"],
    } for s in chosen]


def sponsor_income(player) -> int:
    return sum(s["annual_value"] for s in player.sponsors)


def sponsor_xp(player) -> int:
    return sum(s["xp_bonus"] for s in player.sponsors)


def tick_sponsors(player) -> list:
    """Advance one season. Returns the deals that just expired."""
    expired = []
    for s in list(player.sponsors):
        s["years"] -= 1
        if s["years"] <= 0:
            player.sponsors.remove(s)
            expired.append(s)
    return expired
