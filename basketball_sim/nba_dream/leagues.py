POSITIONS = ["PG", "SG", "SF", "PF", "C"]

COUNTRIES = {
    "France": {
        "flag": "🇫🇷",
        "start_league": "High School FR",
        "path": ["High School FR", "Pro B", "Betclic Elite", "Euroleague", "NBA"]
    },
    "Suisse": {
        "flag": "🇨🇭",
        "start_league": "High School CH",
        "path": ["High School CH", "SBL", "Pro B", "Betclic Elite", "NBA"]
    },
    "Espagne": {
        "flag": "🇪🇸",
        "start_league": "High School ES",
        "path": ["High School ES", "LEB Gold", "ACB", "Euroleague", "NBA"]
    },
    "USA (NCAA)": {
        "flag": "🇺🇸",
        "start_league": "High School US",
        "path": ["High School US", "NCAA", "NBA"]
    },
}

LEAGUES = {
    "High School FR": {
        "name": "Lycée Sport-Études",
        "country": "France",
        "level": 1,
        "difficulty": 0.3,
        "reputation_gain": 5,
        "scout_presence": 0.05,
        "salary": 0,
        "games": 20,
        "teams": ["INSEP", "Pôle Espoirs Paris", "Pôle Espoirs Lyon", "Pôle Espoirs Bordeaux",
                  "Centre de Formation Asvel", "Académie JL Bourg", "Académie Nanterre", "SIG Académie"],
    },
    "High School CH": {
        "name": "Swiss Basketball Academy",
        "country": "Suisse",
        "level": 1,
        "difficulty": 0.25,
        "reputation_gain": 4,
        "scout_presence": 0.03,
        "salary": 0,
        "games": 16,
        "teams": ["Swiss Basketball Academy", "Bern Académie", "Genève Basket", "Lausanne Sport",
                  "Zürich Lions", "Basel Starwings Jeunes", "Lions de Genève", "BC Winterthur"],
    },
    "High School ES": {
        "name": "Liga EBA Júnior",
        "country": "Espagne",
        "level": 1,
        "difficulty": 0.35,
        "reputation_gain": 6,
        "scout_presence": 0.06,
        "salary": 0,
        "games": 22,
        "teams": ["Real Madrid Júnior", "FC Barcelona Júnior", "Valencia BC Júnior", "Estudiantes Júnior",
                  "Baskonia Júnior", "Unicaja Júnior", "Joventut Júnior", "Gran Canaria Júnior"],
    },
    "High School US": {
        "name": "US High School",
        "country": "USA",
        "level": 1,
        "difficulty": 0.4,
        "reputation_gain": 8,
        "scout_presence": 0.1,
        "salary": 0,
        "games": 25,
        "teams": ["Oak Hill Academy", "Montverde Academy", "Sierra Canyon", "La Lumiere",
                  "Prolific Prep", "IMG Academy", "Bishop Gorman", "St. Vincent-St. Mary"],
    },
    "SBL": {
        "name": "Swiss Basketball League",
        "country": "Suisse",
        "level": 2,
        "difficulty": 0.4,
        "reputation_gain": 8,
        "scout_presence": 0.08,
        "salary": 15000,
        "games": 26,
        "teams": ["Lions de Genève", "Starwings Basel", "Bern Capitals", "Neuchâtel Basket",
                  "Monthey Chablais", "Lugano Tigers", "Nyon Nanoteck", "Köniz Bern Bears"],
    },
    "Pro B": {
        "name": "Pro B (France)",
        "country": "France",
        "level": 3,
        "difficulty": 0.5,
        "reputation_gain": 10,
        "scout_presence": 0.12,
        "salary": 25000,
        "games": 30,
        "teams": ["Blois Académie", "Saint-Chamond", "Nantes", "Poitiers",
                  "Roanne", "Vichy", "Caen", "Quimper", "Nancy", "Chartres"],
    },
    "LEB Gold": {
        "name": "LEB Gold (Espagne)",
        "country": "Espagne",
        "level": 3,
        "difficulty": 0.52,
        "reputation_gain": 11,
        "scout_presence": 0.13,
        "salary": 28000,
        "games": 30,
        "teams": ["Palencia", "Oviedo", "Albacite", "Valladolid",
                  "Breogán", "Tarazona", "Almería", "Leyma Coruña", "Peixe Inef Lleida", "Coosur Betis B"],
    },
    "NCAA": {
        "name": "NCAA Division I",
        "country": "USA",
        "level": 4,
        "difficulty": 0.65,
        "reputation_gain": 18,
        "scout_presence": 0.35,
        "salary": 0,
        "games": 35,
        "teams": ["Duke", "Kentucky", "Kansas", "North Carolina", "Gonzaga",
                  "Michigan State", "UCLA", "Villanova", "Arizona", "Houston"],
    },
    "Betclic Elite": {
        "name": "Betclic Elite (France)",
        "country": "France",
        "level": 4,
        "difficulty": 0.6,
        "reputation_gain": 15,
        "scout_presence": 0.2,
        "salary": 80000,
        "games": 34,
        "teams": ["ASVEL", "Monaco", "Paris Basketball", "Boulogne-Levallois",
                  "Strasbourg", "JL Bourg", "Nanterre", "Le Mans", "Limoges", "Dijon"],
    },
    "ACB": {
        "name": "Liga ACB (Espagne)",
        "country": "Espagne",
        "level": 4,
        "difficulty": 0.65,
        "reputation_gain": 16,
        "scout_presence": 0.22,
        "salary": 100000,
        "games": 34,
        "teams": ["Real Madrid", "FC Barcelona", "Valencia BC", "Baskonia",
                  "Unicaja", "Gran Canaria", "Joventut", "Estudiantes", "Murcia", "Bilbao"],
    },
    "Euroleague": {
        "name": "EuroLeague",
        "country": "Europe",
        "level": 5,
        "difficulty": 0.78,
        "reputation_gain": 25,
        "scout_presence": 0.5,
        "salary": 250000,
        "games": 38,
        "teams": ["Real Madrid", "CSKA Moscow", "Fenerbahçe", "Olympiacos",
                  "ASVEL", "Monaco", "FC Barcelona", "Panathinaikos", "Alba Berlin", "Virtus Bologna"],
    },
    "NBA": {
        "name": "NBA",
        "country": "USA",
        "level": 6,
        "difficulty": 0.95,
        "reputation_gain": 50,
        "scout_presence": 1.0,
        "salary": 1000000,
        "games": 82,
        "teams": ["Los Angeles Lakers", "Golden State Warriors", "Boston Celtics", "Miami Heat",
                  "Chicago Bulls", "New York Knicks", "Dallas Mavericks", "Brooklyn Nets",
                  "Milwaukee Bucks", "Phoenix Suns", "Denver Nuggets", "Memphis Grizzlies"],
    },
}

LEAGUE_ORDER = [
    "High School FR", "High School CH", "High School ES", "High School US",
    "SBL", "Pro B", "LEB Gold", "NCAA",
    "Betclic Elite", "ACB", "Euroleague", "NBA"
]

def get_next_league(current_league: str, country: str) -> str | None:
    path = COUNTRIES[country]["path"]
    if current_league in path:
        idx = path.index(current_league)
        if idx + 1 < len(path):
            return path[idx + 1]
    return None

def get_league_level(league_name: str) -> int:
    return LEAGUES.get(league_name, {}).get("level", 0)
