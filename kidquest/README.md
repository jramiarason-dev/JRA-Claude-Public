# 🎓 KidQuest — UI/UX Redesign

Refonte complète de KidQuest Academy : **prototype interactif multi-écrans**
(HTML + React + tokens JRA Studio), bilingue FR/EN, responsive, dark mode,
mascottes originales, carte de quête style jeu vidéo.

> ⚠️ **Statut : prototype visuel.** Données mockées dans `data.js`.
> Pour brancher la vraie logique Claude / persistence backend,
> remplacer `data.js` + `kidquest_academy.py`.

---

## 🚀 Déploiement Streamlit Cloud

### Option A — App séparée (recommandé pour tester)
1. Sur https://share.streamlit.io → **New app**
2. Repo : `jramiarason-dev/JRA-Claude-Public`
3. Branch : `main`
4. **Main file path** : `kidquest/streamlit_app.py`
5. Deploy

### Option B — Remplacer kidquest_academy.py
Si tu veux que l'ancienne route Streamlit pointe vers le nouveau :
```bash
mv kidquest_academy.py kidquest_academy.py.old
cp kidquest/streamlit_app.py kidquest_academy.py
```

---

## 🖥️ Lancer en local

```bash
streamlit run kidquest/streamlit_app.py
# Ou ouvrir directement le HTML standalone :
open kidquest/index.html
```

---

## 📁 Structure du dossier `kidquest/`

```
kidquest/
├── streamlit_app.py     # Launcher Streamlit (sert index.html inliné)
├── index.html           # ⭐ App standalone — TOUT inliné (CSS, JS, données)
│
├── style.css            # Styles KidQuest (source)
├── tokens.css           # Tokens JRA Studio (source)
├── data.js              # i18n FR/EN, mondes, niveaux, trophées, avatars
│
├── mascots.jsx          # Lumi (chouette), Globi (tortue), Pixel (renard)
├── screens.jsx          # Onboarding, World, Quest, Quiz, Profil, Parents…
├── main.jsx             # Root React + routing + persistence localStorage
└── tweaks-panel.jsx     # Panneau de tweaks
```

`index.html` est la **vérité** — tous les autres `.css/.js/.jsx`
sont les sources éditables. Après chaque modif des sources, regénérer :

```bash
# (script Python rapide ou voir les notes dans le repo)
```

---

## 🎨 Écrans

1. **Onboarding** — langue → avatar → prénom (3 étapes)
2. **World Map** — 3 îles-hubs : English Quest, Geo Explorer, Math Arena
3. **Quest Map** — 8 niveaux en zigzag par hub (verrouillés / actuel / terminés / boss 👑)
4. **Quiz** — mascotte + bulle, options emoji, feedback animé
5. **Reward** — confettis, étoiles qui poppent, badge débloqué
6. **Trophées** — 10 trophées (collection)
7. **Profil** — stats, progression, changement d'avatar
8. **Espace parents** — PIN 1234, réglages (difficulté, dark mode, etc.)

---

## 🦊 Mascottes (SVG inline, originales)

- 🦉 **Lumi** la chouette à lunettes — English Quest
- 🐢 **Globi** la tortue exploratrice — Geo Explorer
- 🦊 **Pixel** le renard — Math Arena

---

## ⚙️ Tweaks

- Palette d'accent (orange / teal / violet / jaune)
- Mode sombre
- Difficulté (facile / moyen / difficile)
- Lecture vocale on/off
- Temps quotidien max
- Reset (efface le localStorage)

---

*Propulsé par Claude AI · Anthropic*
