import random
from dataclasses import dataclass, field
from typing import Optional

# XP thresholds to reach each level
LEVEL_THRESHOLDS = [0, 100, 250, 450, 700, 1000, 1350, 1750, 2200, 2700, 3250]

RETIREMENT_AGE = 40


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
    role: str
    games: int
    mpg: float
    ppg: float
    rpg: float
    apg: float
    spg: float
    bpg: float
    fg_pct: float
    reputation_gained: int
    salary_earned: int = 0
    sponsor_earned: int = 0
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
    jersey: int = 23

    # Core attributes (1-99)
    athleticism: int = 50
    shooting: int = 50
    basketball_iq: int = 50
    mental: int = 50
    leadership: int = 50

    # Career state
    current_league: str = ""
    current_team: str = ""
    current_role: str = "Titulaire"
    team_strength: float = 0.5
    contract_salary: int = 0
    contract_years_left: int = 0
    reputation: int = 0
    morale: int = 75
    fitness: int = 100

    # Level & XP
    level: int = 1
    xp: int = 0
    total_xp_earned: int = 0

    # Money
    total_earnings: int = 0
    sponsors: list = field(default_factory=list)

    # Draft
    drafted: bool = False
    draft_round: Optional[int] = None
    draft_pick: Optional[int] = None
    draft_team: Optional[str] = None

    # History
    season_number: int = 0
    career_history: list = field(default_factory=list)

    in_nba: bool = False
    nba_seasons: int = 0
    retired: bool = False

    # ── Ratings ────────────────────────────────────────────────────────────────
    def overall_rating(self) -> int:
        return int(self.athleticism * 0.20 + self.shooting * 0.25 + self.basketball_iq * 0.25
                   + self.mental * 0.20 + self.leadership * 0.10)

    def nba_prospect_score(self) -> int:
        return int(self.athleticism * 0.28 + self.shooting * 0.20 + self.basketball_iq * 0.20
                   + self.mental * 0.12 + self.reputation * 0.20)

    def position_label(self) -> str:
        return {"PG": "Meneur", "SG": "Arrière", "SF": "Ailier",
                "PF": "Ailier Fort", "C": "Pivot"}.get(self.position, self.position)

    # ── Level & XP ─────────────────────────────────────────────────────────────
    def gain_xp(self, amount: int) -> int:
        """Add XP, level up as many times as earned. Returns the number of levels gained."""
        self.xp += amount
        self.total_xp_earned += amount
        gained = 0
        while self.xp >= xp_for_level(self.level + 1):
            self.xp -= xp_for_level(self.level + 1)
            self.level += 1
            self._apply_level_bonus()
            gained += 1
        return gained

    def _apply_level_bonus(self):
        bonuses = {
            "PG": {"shooting": 1, "basketball_iq": 1, "mental": 1},
            "SG": {"shooting": 2, "athleticism": 1},
            "SF": {"athleticism": 1, "shooting": 1, "basketball_iq": 1},
            "PF": {"athleticism": 1, "leadership": 1, "mental": 1},
            "C":  {"athleticism": 2, "leadership": 1},
        }.get(self.position, {"basketball_iq": 1, "mental": 1})
        for attr, val in bonuses.items():
            setattr(self, attr, min(99, getattr(self, attr) + val))
        rnd = random.choice(["athleticism", "shooting", "basketball_iq", "mental", "leadership"])
        setattr(self, rnd, min(99, getattr(self, rnd) + 1))

    def xp_to_next_level(self) -> int:
        return xp_for_level(self.level + 1)

    def xp_progress_pct(self) -> float:
        needed = xp_for_level(self.level + 1)
        return min(100.0, (self.xp / needed) * 100) if needed > 0 else 100.0

    # ── Training & ageing ──────────────────────────────────────────────────────
    def train(self, focus: str) -> dict:
        """Offseason work. Young bodies respond more than veterans'."""
        scale = 1.3 if self.age <= 21 else 1.0 if self.age <= 27 else 0.6 if self.age <= 32 else 0.35

        def r(a, b):
            return max(0, int(round(random.randint(a, b) * scale)))

        gains = {
            "Tir":              {"shooting": r(2, 5), "mental": r(0, 2)},
            "Athletisme":       {"athleticism": r(2, 5)},
            "QI Basketball":    {"basketball_iq": r(2, 5), "leadership": r(0, 2)},
            "Mental":           {"mental": r(2, 5), "leadership": r(1, 3)},
            "Physique Complet": {"athleticism": r(1, 3), "shooting": r(1, 2),
                                 "basketball_iq": r(1, 2), "mental": r(1, 2)},
        }.get(focus, {})
        for attr, val in gains.items():
            setattr(self, attr, min(99, getattr(self, attr) + val))
        return gains

    def apply_ageing(self):
        """Growth until the mid-twenties, a plateau, then a real decline."""
        if self.age <= 23:
            for attr in ("athleticism", "shooting", "basketball_iq"):
                setattr(self, attr, min(99, getattr(self, attr) + random.randint(0, 2)))
            self.basketball_iq = min(99, self.basketball_iq + 1)
        elif self.age <= 27:
            for attr in ("shooting", "basketball_iq", "mental"):
                setattr(self, attr, min(99, getattr(self, attr) + random.randint(0, 1)))
        elif self.age <= 30:
            self.basketball_iq = min(99, self.basketball_iq + random.randint(0, 1))
            self.athleticism = max(25, self.athleticism - random.randint(0, 1))
        else:
            decline = 1 + (self.age - 30) // 3
            self.athleticism = max(20, self.athleticism - random.randint(decline, decline + 2))
            if self.age >= 34:
                self.shooting = max(25, self.shooting - random.randint(0, 1))
            # Experience keeps accumulating even as the body goes.
            self.basketball_iq = min(99, self.basketball_iq + random.randint(0, 1))
            self.leadership = min(99, self.leadership + random.randint(0, 1))

    def should_consider_retirement(self) -> bool:
        return self.age >= 33 or (self.age >= 30 and self.overall_rating() < 45)

    def must_retire(self) -> bool:
        return self.age >= RETIREMENT_AGE

    # ── Career ─────────────────────────────────────────────────────────────────
    def sign_contract(self, offer: dict):
        self.current_league = offer["league"]
        self.current_team = offer["team"]
        self.current_role = offer["role"]
        self.team_strength = offer["strength"]
        self.contract_salary = offer["salary"]
        self.contract_years_left = offer["years"]
        if offer["league"] == "NBA":
            self.in_nba = True

    def add_season(self, record: SeasonRecord):
        self.career_history.append(record)

    def _avg(self, attr: str) -> float:
        if not self.career_history:
            return 0.0
        return round(sum(getattr(s, attr) for s in self.career_history) / len(self.career_history), 1)

    def career_ppg(self) -> float: return self._avg("ppg")
    def career_rpg(self) -> float: return self._avg("rpg")
    def career_apg(self) -> float: return self._avg("apg")
    def career_mpg(self) -> float: return self._avg("mpg")

    def total_championships(self) -> int:
        return sum(1 for s in self.career_history if s.playoff and s.playoff.champion)

    def total_awards(self) -> int:
        return sum(1 for s in self.career_history if s.award)
