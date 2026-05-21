# EA Governance Animator

A standalone Streamlit application to animate the Enterprise Architecture (EA) governance of a private bank's Technology division.

## Features

- **Workflow A** — Architecture Review Requests: submit, route, review, and decide on solution architecture reviews
- **Workflow B** — Standards Exception Requests: manage deviations from approved architecture standards
- **Workflow D** — Architecture Decision Records (ADRs): create and maintain formal architecture decisions
- **Standards & Patterns Library**: browse, search, and manage the EA knowledge base
- **Dashboard**: metrics, queue management, and activity feed
- **Admin**: bulk import, CSV templates, database summary, demo reset

## Tech Stack

- Python 3.11+
- Streamlit
- SQLite (stdlib `sqlite3`)
- Plotly
- Pandas

## Installation

```bash
cd ea_governance
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

The database initialises automatically on first run and is pre-loaded with realistic demo data.

## Enabling AI Features (optional)

```bash
export ANTHROPIC_API_KEY=your_key_here
streamlit run app.py
```

When `ANTHROPIC_API_KEY` is set, the AI Assistant panel activates and provides:
- Pre-filled routing scores from submission text analysis
- Draft review pre-assessments
- Relevant standards suggestions
- ADR section drafting

## File Structure

```
ea_governance/
├── app.py                    # Entry point, navigation, session state, user selector
├── database.py               # SQLite init, all CRUD functions
├── routing_engine.py         # Scoring logic, routing rules, domain assignment
├── ai_assistant.py           # AI stub (activate with ANTHROPIC_API_KEY)
├── pages/
│   ├── 01_dashboard.py       # Home: metrics, queue, activity feed
│   ├── 02_workflow_a.py      # Architecture Review — submit + review + decide
│   ├── 03_workflow_b.py      # Standards Exception — submit + review + decide
│   ├── 04_adr.py             # ADR management
│   ├── 05_standards.py       # Standards & Patterns Library
│   └── 06_admin.py           # Data ingestion, templates, library management
├── components/
│   ├── cards.py              # Request cards, ADR cards, standard cards
│   ├── badges.py             # Status badges, routing tier badges, SLA indicators
│   ├── forms.py              # Reusable form components
│   └── charts.py             # Plotly chart wrappers
├── data/
│   ├── ea_governance.db      # SQLite database (auto-created on first run)
│   └── seed_data.py          # Pre-load standards, patterns, EA team members
├── requirements.txt
└── README.md
```

## Governance Model

### EA Team (6 members)
| Member | BL Domain | Tech Domain |
|---|---|---|
| Head of EA | — (matrix coordinator) | Strategy & Governance |
| Sr EA 1 | PWM (Wealth Management) | Application/Integration |
| Sr EA 2 | PAS (Asset Services) | Data/API/Security |
| Sr EA 3 | Ops (Operations) | Business Process/Workflow |
| Risk & Compliance EA | Cross-BL | Governance/Controls |
| Cloud Architect EA | PTech | Cloud/Infrastructure |

### Governance Tiers
| Tier | Forum | Cadence | SLA |
|---|---|---|---|
| Tier 1 | SAB (Solution Architecture Board) | Quarterly | — |
| Tier 2 | Architecture Review | Monthly / on-request | 14 days |
| Tier 3 | CoP (Community of Practice) | Monthly | — |

### Routing Score Table (Workflow A)
| Score | Routing Tier |
|---|---|
| 0–3 | Fast-track (domain EA, 5-day SLA) |
| 4–6 | Standard Review (Tier 2, 14-day SLA) |
| 7–9 | Extended Review (Tier 2 full panel) |
| 10+ or confirmed violation | SAB Escalation (Tier 1) |
