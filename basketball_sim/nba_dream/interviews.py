"""End-of-season press conference: what you say moves mental, leadership and standing."""
import random

# Each answer carries its own cost. Blaming the staff feels good and burns leadership;
# hiding behind clichés protects nothing and convinces no one.
INTERVIEWS = {
    "champion": {
        "question": "Vous êtes champion. Ce titre, il est à qui ?",
        "answers": [
            {"text": "À ce groupe. Je n'ai fait que ma part du travail.",
             "tone": "humble", "mental": 2, "leadership": 3, "morale": 6, "reputation": 2,
             "fans": ("positive", "Les supporters saluent un discours de patron."),
             "staff": ("positive", "Le staff apprécie que tu mettes le collectif en avant.")},
            {"text": "Je savais que je pouvais les emmener là. J'ai tenu parole.",
             "tone": "confident", "mental": 3, "leadership": 0, "morale": 10, "reputation": 6,
             "fans": ("positive", "Les fans adorent l'assurance, les réseaux s'enflamment."),
             "staff": ("neutral", "Le vestiaire trouve la formule un peu personnelle.")},
            {"text": "On a gagné malgré les choix du coach, franchement.",
             "tone": "defiant", "mental": -3, "leadership": -5, "morale": 3, "reputation": 3,
             "fans": ("neutral", "Une partie du public trouve la sortie déplacée un soir de titre."),
             "staff": ("negative", "Le staff technique encaisse mal la pique publique.")},
        ],
    },
    "finalist": {
        "question": "Battu en finale. Qu'est-ce qui a manqué ?",
        "answers": [
            {"text": "Eux. Ils ont été meilleurs, il faut savoir le dire.",
             "tone": "humble", "mental": 3, "leadership": 2, "morale": -2, "reputation": 1,
             "fans": ("positive", "Le public retient la dignité dans la défaite."),
             "staff": ("positive", "La direction note ta maturité.")},
            {"text": "Il a manqué que je prenne le dernier tir. On me l'a refusé.",
             "tone": "defiant", "mental": -2, "leadership": -4, "morale": 4, "reputation": 4,
             "fans": ("neutral", "Les fans se divisent : ego ou ambition ?"),
             "staff": ("negative", "Le coach répond publiquement. Ambiance.")},
            {"text": "Je préfère ne pas commenter à chaud.",
             "tone": "evasive", "mental": 0, "leadership": -1, "morale": -3, "reputation": -2,
             "fans": ("negative", "Le silence passe mal après une finale perdue."),
             "staff": ("neutral", "La direction ne relève pas.")},
        ],
    },
    "playoff_exit": {
        "question": "Éliminé plus tôt que prévu. Une explication ?",
        "answers": [
            {"text": "On a manqué de constance, moi le premier.",
             "tone": "humble", "mental": 3, "leadership": 2, "morale": -3, "reputation": 0,
             "fans": ("positive", "L'autocritique est plutôt bien reçue."),
             "staff": ("positive", "Le staff apprécie que tu ne te défausses pas.")},
            {"text": "On reviendra plus forts. Notez-le.",
             "tone": "confident", "mental": 2, "leadership": 3, "morale": 5, "reputation": 2,
             "fans": ("positive", "La promesse fait son effet dans les tribunes."),
             "staff": ("neutral", "La direction attend de voir.")},
            {"text": "Avec cet effectif, il ne fallait pas espérer mieux.",
             "tone": "defiant", "mental": -4, "leadership": -5, "morale": -4, "reputation": 1,
             "fans": ("negative", "Les supporters prennent la phrase pour eux. Sifflets annoncés."),
             "staff": ("negative", "Tes coéquipiers ont lu la déclaration.")},
        ],
    },
    "no_playoffs": {
        "question": "Une saison sans playoffs. Vous assumez votre part ?",
        "answers": [
            {"text": "Entièrement. Je dois être meilleur, c'est tout.",
             "tone": "humble", "mental": 4, "leadership": 2, "morale": -4, "reputation": 0,
             "fans": ("positive", "Le public respecte la franchise."),
             "staff": ("positive", "La direction retient l'exigence envers toi-même.")},
            {"text": "Je suis le seul à m'être battu jusqu'au bout.",
             "tone": "defiant", "mental": -3, "leadership": -6, "morale": 2, "reputation": 2,
             "fans": ("neutral", "Certains te donnent raison, le vestiaire beaucoup moins."),
             "staff": ("negative", "Deux cadres répondent dans la presse. Le mal est fait.")},
            {"text": "C'est une saison de transition, rien de plus.",
             "tone": "evasive", "mental": -1, "leadership": 0, "morale": -2, "reputation": -3,
             "fans": ("negative", "La formule agace un public qui a payé sa place."),
             "staff": ("neutral", "Réponse jugée tiède en interne.")},
        ],
    },
    "benched": {
        "question": "Peu de minutes cette saison. Frustré ?",
        "answers": [
            {"text": "J'apprends tous les jours à l'entraînement. Mon tour viendra.",
             "tone": "humble", "mental": 4, "leadership": 1, "morale": 2, "reputation": -1,
             "fans": ("positive", "Le public apprécie le professionnalisme."),
             "staff": ("positive", "Le coach cite ton attitude en exemple.")},
            {"text": "Oui. Je mérite mieux et je compte le prouver.",
             "tone": "confident", "mental": 2, "leadership": 1, "morale": 6, "reputation": 3,
             "fans": ("positive", "Les fans réclament déjà plus de temps de jeu pour toi."),
             "staff": ("neutral", "Le staff prend note, sans promesse.")},
            {"text": "Le coach ne m'aime pas, c'est aussi simple que ça.",
             "tone": "defiant", "mental": -5, "leadership": -4, "morale": -6, "reputation": 2,
             "fans": ("neutral", "La déclaration fait le tour des réseaux."),
             "staff": ("negative", "Relation avec le staff durablement abîmée.")},
        ],
    },
    "breakout": {
        "question": "Une saison énorme. Vous vous situez où, maintenant ?",
        "answers": [
            {"text": "Encore loin du compte. Je travaille.",
             "tone": "humble", "mental": 3, "leadership": 2, "morale": 3, "reputation": 1,
             "fans": ("positive", "Humilité saluée, la cote grimpe quand même."),
             "staff": ("positive", "Exactement le discours que la direction voulait entendre.")},
            {"text": "Parmi les meilleurs de cette ligue. Les chiffres parlent.",
             "tone": "confident", "mental": 2, "leadership": 1, "morale": 8, "reputation": 8,
             "fans": ("positive", "Le public valide, le maillot se vend."),
             "staff": ("neutral", "La direction surveille l'ego.")},
            {"text": "Au-dessus de ce club, pour être honnête.",
             "tone": "defiant", "mental": -2, "leadership": -5, "morale": 4, "reputation": 7,
             "fans": ("negative", "Les supporters se sentent trahis. Sifflets probables."),
             "staff": ("negative", "La direction envisage déjà de te transférer.")},
        ],
    },
    "injured": {
        "question": "Une saison hachée par les blessures. Comment ça va ?",
        "answers": [
            {"text": "Je reviendrai. Je n'ai jamais rien lâché.",
             "tone": "confident", "mental": 4, "leadership": 2, "morale": 5, "reputation": 1,
             "fans": ("positive", "Message de soutien massif des tribunes."),
             "staff": ("positive", "Le staff médical salue ton état d'esprit.")},
            {"text": "Difficile. Je ne vais pas prétendre le contraire.",
             "tone": "humble", "mental": 2, "leadership": 0, "morale": -2, "reputation": 0,
             "fans": ("positive", "La sincérité touche le public."),
             "staff": ("neutral", "La direction prend acte.")},
            {"text": "On m'a fait jouer blessé. Voilà le vrai sujet.",
             "tone": "defiant", "mental": -3, "leadership": -3, "morale": -2, "reputation": 4,
             "fans": ("neutral", "L'accusation lance une polémique."),
             "staff": ("negative", "Le staff médical dément. Climat tendu.")},
        ],
    },
    "rookie": {
        "question": "Première saison chez les pros. Un bilan ?",
        "answers": [
            {"text": "J'observe, j'écoute, j'apprends.",
             "tone": "humble", "mental": 3, "leadership": 1, "morale": 2, "reputation": 0,
             "fans": ("positive", "Le public apprécie la tête sur les épaules."),
             "staff": ("positive", "Les anciens te prennent sous leur aile.")},
            {"text": "Je ne suis pas venu pour faire de la figuration.",
             "tone": "confident", "mental": 2, "leadership": 2, "morale": 6, "reputation": 4,
             "fans": ("positive", "Le caractère plaît."),
             "staff": ("neutral", "Le vestiaire attend de voir sur le terrain.")},
            {"text": "Franchement, le niveau ne m'a pas impressionné.",
             "tone": "defiant", "mental": -4, "leadership": -4, "morale": 3, "reputation": 3,
             "fans": ("neutral", "Sortie très commentée pour un débutant."),
             "staff": ("negative", "Les cadres du vestiaire n'ont pas apprécié.")},
        ],
    },
    "veteran": {
        "question": "À votre âge, combien de saisons encore ?",
        "answers": [
            {"text": "Tant que je suis utile au groupe.",
             "tone": "humble", "mental": 3, "leadership": 4, "morale": 3, "reputation": 0,
             "fans": ("positive", "Ovation annoncée au prochain match à domicile."),
             "staff": ("positive", "La direction évoque déjà un rôle après-carrière.")},
            {"text": "Assez pour gagner encore quelque chose.",
             "tone": "confident", "mental": 3, "leadership": 3, "morale": 6, "reputation": 2,
             "fans": ("positive", "L'ambition d'un ancien galvanise le public."),
             "staff": ("positive", "Le staff aime cette énergie.")},
            {"text": "Plus que la plupart des jeunes de ce vestiaire.",
             "tone": "defiant", "mental": -2, "leadership": -4, "morale": 4, "reputation": 1,
             "fans": ("neutral", "La formule amuse autant qu'elle gêne."),
             "staff": ("negative", "Les jeunes joueurs se sont sentis visés.")},
        ],
    },
}

SENTIMENT_ICON = {"positive": "🟢", "neutral": "🟡", "negative": "🔴"}


def pick_interview(record, player) -> tuple:
    """Choose the press conference that fits what just happened. Returns (key, data)."""
    po = record.playoff
    if po and po.champion:                 key = "champion"
    elif po and po.reached_final:          key = "finalist"
    elif record.games <= 8:                key = "injured"
    elif player.age >= 33:                 key = "veteran"
    elif player.season_number <= 1:        key = "rookie"
    elif record.mpg < 12:                  key = "benched"
    elif record.ppg >= 18 or record.award: key = "breakout"
    elif po:                               key = "playoff_exit"
    else:                                  key = "no_playoffs"
    return key, INTERVIEWS[key]


def apply_answer(player, answer: dict) -> dict:
    """Apply an interview answer. Attribute hits here are permanent."""
    before = {"mental": player.mental, "leadership": player.leadership}
    player.mental = max(1, min(99, player.mental + answer["mental"]))
    player.leadership = max(1, min(99, player.leadership + answer["leadership"]))
    player.morale = max(10, min(100, player.morale + answer["morale"]))
    player.reputation = max(0, min(100, player.reputation + answer["reputation"]))
    return {
        "mental_delta": player.mental - before["mental"],
        "leadership_delta": player.leadership - before["leadership"],
        "morale": answer["morale"], "reputation": answer["reputation"],
        "fans": answer["fans"], "staff": answer["staff"],
    }
