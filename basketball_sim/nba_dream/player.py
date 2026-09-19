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
    tactic: Optional[str] = None
    tactic_fit: float = 0.0
    club_status: Optional[str] = None
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
    seasons_with_team: int = 0
    current_tactic: str = "Motion Offense"
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
        # Loyalty is measured in seasons at one club, so re-signing keeps the count.
        if offer["team"] != self.current_team:
            self.seasons_with_team = 0
        self.current_league = offer["league"]
        self.current_team = offer["team"]
        self.current_role = offer["role"]
        self.team_strength = offer["strength"]
        self.contract_salary = offer["salary"]
        self.contract_years_left = offer["years"]
        if offer["league"] == "NBA":
            self.in_nba = True

    def club_status(self) -> Optional[str]:
        """Standing earned by staying: captains lead, legends are part of the club."""
        if self.seasons_with_team >= 6:
            return "Légende du club"
        if self.seasons_with_team >= 4:
            return "Capitaine"
        if self.seasons_with_team >= 2:
            return "Cadre du vestiaire"
        return None

    def apply_loyalty_growth(self) -> dict:
        """Leading the same dressing room year after year builds mental and leadership."""
        status = self.club_status()
        gains = {"Cadre du vestiaire": (0, 1), "Capitaine": (1, 2), "Légende du club": (2, 3)}
        if status not in gains:
            return {}
        mental, leadership = gains[status]
        self.mental = min(99, self.mental + mental)
        self.leadership = min(99, self.leadership + leadership)
        return {"status": status, "mental": mental, "leadership": leadership}

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

    def career_tier(self) -> tuple:
        """Where this career stands right now. Returns (tier, icon, colour)."""
        score = (self.overall_rating() * 0.9 + self.reputation * 0.5
                 + self.nba_seasons * 3 + self.total_championships() * 12
                 + self.total_awards() * 5 + self.level * 2)
        if score >= 190: return "Légende", "🐐", "#ef4444"
        if score >= 155: return "Superstar", "⭐", "#f59e0b"
        if score >= 125: return "All-Star", "🌟", "#a855f7"
        if score >= 100: return "Titulaire confirmé", "🏀", "#22c55e"
        if score >= 75:  return "Joueur de rotation", "🔄", "#0ea5e9"
        if score >= 50:  return "Espoir", "🌱", "#8a8a96"
        return "Débutant", "👶", "#6b7280"

    def career_verdict(self) -> str:
        """An adaptive read on the career as it stands at this exact moment."""
        if not self.career_history:
            return "La carrière n'a pas encore commencé."

        tier, _, _ = self.career_tier()
        n = len(self.career_history)
        champs, awards = self.total_championships(), self.total_awards()
        parts = [f"Après {n} saison{'s' if n > 1 else ''}, {self.name} est un profil de "
                 f"**{tier.lower()}** ({self.overall_rating()} d'overall, niveau {self.level})."]

        # Trajectory: compare the last three seasons with the three before them.
        if n >= 4:
            recent = self.career_history[-3:]
            earlier = self.career_history[-6:-3] or self.career_history[:-3]
            r = sum(s.ppg for s in recent) / len(recent)
            e = sum(s.ppg for s in earlier) / len(earlier)
            if r > e + 2.5:
                parts.append("La progression est nette : les trois dernières saisons sont "
                             "les meilleures de la carrière.")
            elif r < e - 2.5:
                parts.append("La production recule sur les trois dernières saisons — "
                             "l'âge ou le rôle pèsent.")
            else:
                parts.append("Le niveau de production est stable d'une saison à l'autre.")

        if self.age >= 33:
            parts.append(f"À {self.age} ans, l'essentiel de la carrière est derrière.")
        elif self.age <= 22:
            parts.append(f"À {self.age} ans, la marge de progression reste importante.")

        if champs:
            parts.append(f"{champs} titre{'s' if champs > 1 else ''} au palmarès"
                         + (f" et {awards} distinction{'s' if awards > 1 else ''} individuelle"
                            f"{'s' if awards > 1 else ''}." if awards else "."))
        elif awards:
            parts.append(f"{awards} distinction{'s' if awards > 1 else ''} individuelle"
                         f"{'s' if awards > 1 else ''}, mais aucun titre collectif.")
        else:
            parts.append("Ni titre ni distinction individuelle pour l'instant.")

        if self.nba_seasons >= 5:
            parts.append(f"{self.nba_seasons} saisons en NBA : le plus haut niveau est atteint "
                         "et tenu.")
        elif self.nba_seasons:
            parts.append(f"{self.nba_seasons} saison{'s' if self.nba_seasons > 1 else ''} "
                         "en NBA à ce jour.")
        elif self.age >= 28:
            parts.append("La NBA reste hors de portée à ce stade.")

        status = self.club_status()
        if status:
            parts.append(f"Statut de **{status.lower()}** à {self.current_team} "
                         f"({self.seasons_with_team} saisons).")
        return " ".join(parts)
