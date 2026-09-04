# AuditIQ

Internal-audit assistant for Swiss private banks and asset managers. Streamlit
front end over a static reference library plus three Claude agents.

Live: <https://audit-jra.streamlit.app>

## Run it

```bash
cd audit_system
pip install -r requirements.txt
cp .env.example .env          # fill in ANTHROPIC_API_KEY
streamlit run app.py
```

The CLI for the three agents, without the UI:

```bash
python main.py               # interactive menu
python main.py --agent 1     # or 2, 3
```

## Configuration

| Variable | Required | Effect |
|---|---|---|
| `ANTHROPIC_API_KEY` | yes | Backend key. The app refuses to start without it, including in static mode. |
| `AUDITIQ_PASSWORD` | no | Shared sign-in password. **Unset means the app is open to anyone with the URL.** |

Locally these come from `.env` or the environment; on Streamlit Cloud, from
**App settings → Secrets**. Never commit either value — `.gitignore` covers
`.env` and `**/.streamlit/secrets.toml`.

## Layout

```
app.py            Streamlit app — the seven sections, top to bottom
data.py           Static reference library (~17k lines): regulations, risks,
                  audit tests, CVEs, IIA standards, calendars, entity context
base_agent.py     Claude client, model id, file upload, prompt caching
agent1..3_*.py    System prompts and tool schemas for the three agents
generators.py     Word / Excel / PowerPoint / PDF exporters
main.py           CLI entry point for the agents
auditiq/          React prototype (design reference, not wired to the app)
tests/            unittest suite — no pytest, no network
```

### Sections

`app.py` dispatches on `st.session_state["active_tab"]`, an index into the
`_SECTIONS` tuple near the top of the file. That tuple is the single source of
truth: the sidebar nav, the breadcrumb and the help panel all read from it, and
the named constants (`DASHBOARD`, `RISK_ANALYSIS`, …) are what the dispatch
compares against. Adding or removing a section means editing `_SECTIONS` and the
matching `_HELP` entry — `tests/test_app_smoke.py` fails if the two drift apart.

### Data invariants

`RISK_INDICATORS`, `AUDIT_TESTS_LIBRARY` and `DATA_ANALYTICS_SCENARIOS` are keyed
by the same theme strings and must stay in lockstep; `TOPIC_KEY_MAPPING` may only
point at themes that exist. A theme present in one dict and missing from another
produces a blank panel rather than an error, so `tests/test_data_integrity.py`
guards the invariant instead.

## Tests

```bash
cd audit_system
python -m unittest discover -s tests -v
```

Standard library only. The suite renders every section headlessly through
Streamlit's `AppTest` — a real regression net for a single-script app — and also
checks the data invariants, the sign-in gate, output escaping and the model id.
It makes no network calls; a placeholder API key is enough. CI runs it on every
push (`.github/workflows/ci.yml`).

## Extracting this project

`audit_system/` is self-contained: it carries its own `requirements.txt`,
`.streamlit/config.toml`, `.env.example` and tests, adds its own directory to
`sys.path`, and imports nothing from the parent repository. Moving it to its own
repository is a copy:

```bash
cp -r audit_system/ ../auditiq && cd ../auditiq && git init
```

Two things live outside the folder and would need to come along: the CI workflow
(`.github/workflows/ci.yml`, whose `working-directory` would drop to `.`) and the
`.gitignore` rules for `.env`, `**/.streamlit/secrets.toml` and `outputs/`.

## Security notes

- **Sign-in is open by default.** With `AUDITIQ_PASSWORD` unset, anyone reaching
  the URL gets in — including to the features that spend API credit. Set it for
  any deployment that is not a public demo. The SSO and card buttons are
  mock-ups: they refuse rather than authenticate whenever a password is set.
- **Everything user-typed is rendered through `unsafe_allow_html`.** Escape with
  `_e()` at the render site, and build link targets with `_safe_link()`. Do not
  escape at capture — the same values go unescaped to the exporters.
- **Generated reports accumulate in `outputs/`**, one directory shared by every
  session, named by timestamp and never cleaned up. Fine for a single-user demo;
  not fine for a multi-user deployment.
- **The dashboard embeds a third-party iframe** (`cybermap.kaspersky.com`). Every
  page view sends the viewer's IP, User-Agent and referring hostname to that
  vendor, and the frame runs remote JavaScript with no sandbox or CSP. Worth a
  deliberate decision before this is pointed at anything but demo data.
