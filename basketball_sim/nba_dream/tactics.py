"""Team tactical system, chosen in the offseason. Fit with your attributes decides the payoff."""

# `weights` is what the system asks of a player: the fit score compares your
# attributes against it. `stats` reshapes production, `team` nudges the roster's
# own strength — a system that suits you makes the whole team better.
TACTICS = {
    "Pace & Space": {
        "icon": "🏃",
        "desc": "Tempo élevé, tirs extérieurs, peu de jeu au poste.",
        "weights": {"shooting": 0.45, "athleticism": 0.35, "basketball_iq": 0.20},
        "stats": {"pts": 1.15, "reb": 0.88, "ast": 1.05},
        "best_for": ["PG", "SG", "SF"],
    },
    "Jeu Intérieur": {
        "icon": "🪨",
        "desc": "On passe par les grands, on domine la raquette et le rebond.",
        "weights": {"athleticism": 0.45, "mental": 0.25, "basketball_iq": 0.30},
        "stats": {"pts": 0.95, "reb": 1.30, "ast": 0.90},
        "best_for": ["PF", "C"],
    },
    "Motion Offense": {
        "icon": "🔄",
        "desc": "Ballon qui circule, écrans permanents, lecture collective.",
        "weights": {"basketball_iq": 0.50, "shooting": 0.30, "leadership": 0.20},
        "stats": {"pts": 1.00, "reb": 0.98, "ast": 1.35},
        "best_for": ["PG", "SF", "C"],
    },
    "Défense de Fer": {
        "icon": "🛡️",
        "desc": "Tout sur la défense. Peu de points marqués, peu encaissés.",
        "weights": {"athleticism": 0.35, "mental": 0.40, "basketball_iq": 0.25},
        "stats": {"pts": 0.82, "reb": 1.12, "ast": 0.95},
        "best_for": ["PF", "C", "SG"],
    },
    "Système Iso": {
        "icon": "🎯",
        "desc": "On dégage l'aile et on laisse le meilleur joueur créer seul.",
        "weights": {"shooting": 0.40, "mental": 0.35, "athleticism": 0.25},
        "stats": {"pts": 1.28, "reb": 0.92, "ast": 0.75},
        "best_for": ["SG", "SF"],
    },
}


ATTRS = ("athleticism", "shooting", "basketball_iq", "mental", "leadership")


def fit_score(player, tactic_name: str) -> float:
    """0-100: does this system lean on your strengths?

    Measured against the player's own average, not in absolute terms — a system
    suits a profile, and a beginner is not 'out of position' in every system.
    """
    t = TACTICS[tactic_name]
    weighted = sum(getattr(player, attr) * w for attr, w in t["weights"].items())
    baseline = sum(getattr(player, a) for a in ATTRS) / len(ATTRS)
    score = 55 + (weighted - baseline) * 2.2
    if player.position in t["best_for"]:
        score += 6
    return round(max(5.0, min(100.0, score)), 1)


def fit_label(score: float) -> tuple:
    if score >= 78: return "Taillé pour toi", "#2fa35c"
    if score >= 66: return "Bon compromis", "#8ac926"
    if score >= 54: return "Acceptable", "#e07a1e"
    return "À contre-emploi", "#e0492c"


def tactic_modifiers(player, tactic_name: str) -> dict:
    """Turn the fit into concrete multipliers. A bad fit really does cost you."""
    t = TACTICS[tactic_name]
    fit = fit_score(player, tactic_name)
    # Centred on 66: above it you gain, below it you lose.
    edge = (fit - 66) / 100.0
    return {
        "pts": t["stats"]["pts"] * (1 + edge * 0.8),
        "reb": t["stats"]["reb"] * (1 + edge * 0.5),
        "ast": t["stats"]["ast"] * (1 + edge * 0.5),
        "efficiency": 1 + edge * 0.55,
        "team_strength": edge * 0.18,
        "xp": 1 + max(0.0, edge) * 0.5,
        "fit": fit,
    }
