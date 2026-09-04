import random
from dataclasses import dataclass, field
from typing import Optional

# XP thresholds to reach each level
LEVEL_THRESHOLDS = [0, 100, 250, 450, 700, 1000, 1350, 1750, 2200, 2700, 3250]

def xp_for_level(level: int) -> int:
    if level >= len(LEVEL_THRESHOLDS):
        return LEVEL_THRESHOLDS[-1] + (level - len(LEVEL_THRESHOLDS) + 1) * 600
    return LEVEL_THRESHOLDS[level]

@dataclass
class PlayoffResult:
    reached_final: bool
    champion: bool
    rounds_won: int
    opponent: str
    title: Optional[str] = None

@dataclass
class SeasonRecord:
    season: int
    age: int
    league: str
    team: str
    games: int
    ppg: float
    rpg: float
    apg: float
    spg: float
    bpg: float
    fg_pct: float
    reputation_gained: int
    xp_gained: int = 0
    level_before: int = 1
    level_after: int = 1
    award: Optional[str] = None
    event: Optional[str] = None
    training_focus: Optional[str] = None
    playoff: Optional[PlayoffResult] = None

@dataclass
class Player:
    name: str
    country: str
    position: str
    age: int = 17

    # Core attributes (1-99)
    athleticism: int = 50
    shooting: int = 50
    basketball_iq: int = 50
    mental: int = 50
    leadership: int = 50

    # Career state
    current_league: str = ""
    current_team: str = ""
    reputation: int = 0
    morale: int = 75
    fitness: int = 100

    # Level & XP system
    level: int = 1
    xp: int = 0
    total_xp_earned: int = 0

    # Financials
    total_earnings: int = 0

    # Draft
    draft_round: Optional[int] = None
    draft_pick: Optional[int] = None

    # History
    season_number: int = 0
    career_history: list = field(default_factory=list)

    # NBA status
    in_nba: bool = False
    nba_seasons: int = 0
    championships: int = 0  # total across all leagues

    def overall_rating(self) -> int:
        weights = {"athleticism": 0.2, "shooting": 0.25, "basketball_iq": 0.25, "mental": 0.2, "leadership": 0.1}
        return int(
            self.athleticism * weights["athleticism"] +
            self.shooting * weights["shooting"] +
            self.basketball_iq * weights["basketball_iq"] +
            self.mental * weights["mental"] +
            self.leadership * weights["leadership"]
        )

    def nba_prospect_score(self) -> int:
        return int(self.athleticism * 0.3 + self.shooting * 0.2 + self.basketball_iq * 0.2 +
                   self.mental * 0.15 + self.reputation * 0.15)

    def position_label(self) -> str:
        labels = {"PG": "Meneur", "SG": "Arrière", "SF": "Ailier", "PF": "Ailier Fort", "C": "Pivot"}
        return labels.get(self.position, self.position)

    def gain_xp(self, amount: int) -> bool:
        """Add XP and level up if threshold crossed. Returns True if leveled up."""
        self.xp += amount
        self.total_xp_earned += amount
        leveled_up = False
        while True:
            next_threshold = xp_for_level(self.level + 1)
            if self.xp >= next_threshold:
                self.xp -= next_threshold
                self.level += 1
                self._apply_level_bonus()
                leveled_up = True
            else:
                break
        return leveled_up

    def _apply_level_bonus(self):
        """Each level-up grants a small attribute bonus based on position."""
        position_bonuses = {
            "PG": {"shooting": 1, "basketball_iq": 1, "mental": 1},
            "SG": {"shooting": 2, "athleticism": 1},
            "SF": {"athleticism": 1, "shooting": 1, "basketball_iq": 1},
            "PF": {"athleticism": 1, "leadership": 1, "mental": 1},
            "C":  {"athleticism": 2, "leadership": 1},
        }
        bonuses = position_bonuses.get(self.position, {"basketball_iq": 1, "mental": 1})
        for attr, val in bonuses.items():
            if hasattr(self, attr):
                setattr(self, attr, min(99, getattr(self, attr) + val))
        # Always gain 1 in a random attribute
        random_attr = random.choice(["athleticism", "shooting", "basketball_iq", "mental", "leadership"])
        setattr(self, random_attr, min(99, getattr(self, random_attr) + 1))

    def xp_to_next_level(self) -> int:
        return xp_for_level(self.level + 1)

    def xp_progress_pct(self) -> float:
        needed = xp_for_level(self.level + 1)
        return min(100.0, (self.xp / needed) * 100) if needed > 0 else 100.0

    def train(self, focus: str) -> dict:
        """Apply offseason training gains. Returns the gains dict."""
        gains = {
            "Tir":           {"shooting": random.randint(2, 5), "mental": random.randint(0, 2)},
            "Athletisme":    {"athleticism": random.randint(2, 5), "fitness": random.randint(0, 3)},
            "QI Basketball": {"basketball_iq": random.randint(2, 5), "leadership": random.randint(0, 2)},
            "Mental":        {"mental": random.randint(2, 5), "leadership": random.randint(1, 3)},
            "Physique Complet": {
                "athleticism": random.randint(1, 3), "shooting": random.randint(1, 2),
                "basketball_iq": random.randint(1, 2), "mental": random.randint(1, 2),
            },
        }
        applied = gains.get(focus, {})
        for attr, val in applied.items():
            if hasattr(self, attr):
                setattr(self, attr, min(99, getattr(self, attr) + val))
        return applied

    def apply_age_regression(self):
        if self.age > 30:
            penalty = (self.age - 30) * 0.5
            self.athleticism = max(30, int(self.athleticism - penalty))

    def add_season(self, record: SeasonRecord):
        self.career_history.append(record)

    def career_ppg(self) -> float:
        if not self.career_history: return 0.0
        return round(sum(s.ppg for s in self.career_history) / len(self.career_history), 1)

    def career_rpg(self) -> float:
        if not self.career_history: return 0.0
        return round(sum(s.rpg for s in self.career_history) / len(self.career_history), 1)

    def career_apg(self) -> float:
        if not self.career_history: return 0.0
        return round(sum(s.apg for s in self.career_history) / len(self.career_history), 1)

    def total_championships(self) -> int:
        return sum(1 for s in self.career_history if s.playoff and s.playoff.champion)
