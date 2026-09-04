import random
from dataclasses import dataclass, field
from typing import Optional

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
    award: Optional[str] = None
    event: Optional[str] = None

@dataclass
class Player:
    name: str
    country: str
    position: str
    age: int = 17

    athleticism: int = 50
    shooting: int = 50
    basketball_iq: int = 50
    mental: int = 50
    leadership: int = 50

    current_league: str = ""
    current_team: str = ""
    reputation: int = 0
    morale: int = 75
    fitness: int = 100

    total_earnings: int = 0

    draft_eligible: bool = False
    draft_round: Optional[int] = None
    draft_pick: Optional[int] = None

    season_number: int = 0
    career_history: list = field(default_factory=list)
    events_log: list = field(default_factory=list)

    in_nba: bool = False
    nba_seasons: int = 0
    nba_championships: int = 0

    def overall_rating(self) -> int:
        weights = {"athleticism": 0.2, "shooting": 0.25, "basketball_iq": 0.25, "mental": 0.2, "leadership": 0.1}
        score = (self.athleticism * weights["athleticism"] + self.shooting * weights["shooting"] +
                 self.basketball_iq * weights["basketball_iq"] + self.mental * weights["mental"] +
                 self.leadership * weights["leadership"])
        return int(score)

    def nba_prospect_score(self) -> int:
        return int(self.athleticism * 0.3 + self.shooting * 0.2 + self.basketball_iq * 0.2 +
                   self.mental * 0.15 + self.reputation * 0.15)

    def position_label(self) -> str:
        labels = {"PG": "Meneur", "SG": "Arrière", "SF": "Ailier", "PF": "Ailier Fort", "C": "Pivot"}
        return labels.get(self.position, self.position)

    def train(self, focus: str):
        gains = {
            "Tir": {"shooting": random.randint(2, 5), "mental": random.randint(0, 2)},
            "Athletisme": {"athleticism": random.randint(2, 5), "fitness": random.randint(0, 3)},
            "QI Basketball": {"basketball_iq": random.randint(2, 5), "leadership": random.randint(0, 2)},
            "Mental": {"mental": random.randint(2, 5), "leadership": random.randint(1, 3)},
            "Physique Complet": {"athleticism": random.randint(1, 3), "shooting": random.randint(1, 2),
                                  "basketball_iq": random.randint(1, 2), "mental": random.randint(1, 2)},
        }
        if focus in gains:
            for attr, val in gains[focus].items():
                if hasattr(self, attr):
                    setattr(self, attr, min(99, getattr(self, attr) + val))

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
