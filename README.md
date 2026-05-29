# Julien Ramiarason

**Internal Auditor · Builder · Geneva, Switzerland**

> Automating audit workflows and building AI-powered tools — one project at a time.

---

## Projects

| Project | Description | Stack | Status |
|---|---|---|---|
| [AuditIQ](https://audit-jra.streamlit.app) | AI-powered internal audit app — findings management, closing documents, workflow automation | `Streamlit` `Python` `Anthropic API` | 🟢 Live |
| KidQuest Academy | Gamified learning app for 6-year-olds covering English, Geography, and Maths | `Streamlit` `Python` `Anthropic API` | 🟡 In progress |
| CoachIQ | Sports coaching assistant app | `Streamlit` `Python` | 🟡 In progress |
| CCT CPRC | Excel compliance checker for Swiss collective labor agreements | `Python` `openpyxl` | ✅ Delivered |

---

## Tech Stack

`Python` · `Streamlit` · `Anthropic Claude API` · `SQLite` · `openpyxl` · `GitHub`

---

## About

Internal auditor by day, builder by night.
Focused on audit automation, AI-powered workflows, and tools that make compliance work less painful.
Based in Geneva, working across Swiss financial services.

---

## Contact

📍 Geneva, Switzerland

---

> All projects use anonymized or synthetic data. No confidential bank data is stored or shared.








# 🎓 KidQuest Academy

An interactive bilingual (FR/EN) edutainment platform for children aged 4–7, built with Streamlit.

## Features

- **🦊 English Quest** — Word Match, Listen & Spell, Sentence Builder
- **🌍 Geo Explorer** — Flag Finder, Capital Challenge, Continent Sorter (with live Plotly world map)
- **🔢 Math Arena** — Number Blaster, Count the Objects, Pattern Puzzle
- Global gamification sidebar: star counter, FR/EN badges, per-tab scores
- Bilingual interface (French / English throughout)
- Country data powered by the [Countrylayer REST API](https://countrylayer.com) with offline fallback

## Quick Start

```bash
pip install -r requirements.txt
streamlit run kidquest_academy.py
```

## API Key Setup (Geo Explorer)

The Geo Explorer tab fetches live country data from the **Countrylayer API**.

1. Sign up for a free key at <https://countrylayer.com> (free plan: 250 requests/month).
2. Open `.streamlit/secrets.toml` and replace the placeholder:

```toml
COUNTRYLAYER_API_KEY = "your_actual_key_here"
```

3. Restart the app — country data will be fetched and cached for 1 hour (`@st.cache_data(ttl=3600)`).

> **Without a key** the app falls back to a built-in list of 20 countries so all games remain fully playable.

### Free Plan Limits

| Plan  | Requests/month | HTTPS |
|-------|---------------|-------|
| Free  | 250           | No    |
| Basic | 10 000        | Yes   |

Because responses are cached for 1 hour, the free plan is sufficient for development and light use.

## Deploying to Streamlit Cloud

When deploying to [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Go to **App settings → Secrets**.
2. Paste the contents of `secrets.toml` (with your real key) into the secrets editor.
3. Do **not** commit a real key to your repository.

## Project Structure

```
kidquest_academy.py        # Single-file Streamlit app
requirements.txt
.streamlit/
    secrets.toml           # API key placeholder (never commit real keys)
README.md
```
