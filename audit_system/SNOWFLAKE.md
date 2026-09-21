# AuditIQ on Streamlit in Snowflake

What a reviewer needs to know before this goes on a stage, and what to do about
each item. Written against Snowflake's published limitations for Streamlit apps;
**re-check them against your account's current release** — the runtime defaults
changed during 2026 and the container runtime only reached GA in March.

## The short version

The app runs on Snowflake **with no code changes and no API key**, in static
reference mode: the reference library, audit tests, IIA standards, red flags,
regulatory calendar and report assembly all work. The ✦ AI generation buttons
stay disabled behind a banner until outbound access and `anthropic` are
available. `tests/test_app_smoke.py::TestDegradesWithoutOptionalPackages`
enforces exactly that, by rendering every section with `anthropic` and `rich`
made unimportable.

Which runtime you pick decides how much more you get:

| | Warehouse runtime | Container runtime |
|---|---|---|
| Packages | Snowflake Anaconda channel only | + PyPI, via an external access integration |
| `anthropic` | not available → static mode | installable |
| `st.secrets` | not supported | supported, also mapped to env vars |
| Outbound network | needs an external access integration | needs an external access integration |
| Verdict | works, static mode | works, full features |

## Deploying

Put these on the stage — the whole directory except `tests/`, `main.py`,
`auditiq/` and `AuditIQ.html`, none of which the app imports:

```
app.py            environment.yml
theme.py          base_agent.py
data.py           agent1_regulatory.py
generators.py     agent2_audit_plan.py
                  agent3_report.py
```

```sql
CREATE STREAMLIT auditiq
  ROOT_LOCATION = '@my_db.my_schema.auditiq_stage'
  MAIN_FILE     = 'app.py'
  QUERY_WAREHOUSE = my_wh;
```

Snowflake reads `environment.yml`, not `requirements.txt`. Both are kept in
sync deliberately: `requirements.txt` is for local development and CI,
`environment.yml` is the Snowflake manifest.

## Enabling the AI features

Two things are needed, and both are administrator actions:

1. **Outbound access** to `api.anthropic.com`, via a network rule and an
   external access integration attached to the Streamlit object.
2. **The `anthropic` package**, which means the container runtime (the
   warehouse runtime cannot install from PyPI).

Then supply the key. The app reads `st.secrets["ANTHROPIC_API_KEY"]` and falls
back to the `ANTHROPIC_API_KEY` environment variable, so a Snowflake secret
mapped into the container satisfies it either way. `AUDITIQ_PASSWORD` works the
same way — see the sign-in note below.

## Things a reviewer will and should ask about

**The sign-in screen is not authentication.** With `AUDITIQ_PASSWORD` unset the
app is open to anyone who can open it, and the SSO and card buttons are
mock-ups. On Snowflake this is defensible — Snowflake authenticates the user
before the app renders and the app grants no data access of its own — but it
means the screen is decoration there, not a control. Either set the password or
drop the screen; do not leave it looking like a gate that isn't one.

**Fonts are fetched from Google.** `theme.py` opens with
`@import url('https://fonts.googleapis.com/…')`. If outbound access is closed
the browser simply falls back to the system font stack — cosmetic only, nothing
breaks. It is still a third-party request from the client, which some banks
will not accept; inline the two faces, or delete the `@import` and let the
fallbacks do the work.

**`st.set_page_config`.** The warehouse runtime ignores `page_title`,
`page_icon` and `menu_items`. `layout="wide"` and
`initial_sidebar_state` — the two that matter here — are honoured.

**No custom components and no iframes.** The app uses neither. Keep it that
way: the warehouse runtime cannot load component scripts from external domains.

**The 32 MB message limit** (warehouse runtime) applies to a single Streamlit
command's payload. The largest thing this app renders is the red-flag library
(45 entries) and the audit-test tables — orders of magnitude below it.

**Exports never touch a shared filesystem.** `_export_bytes()` stages each
document in a private `TemporaryDirectory` under `/tmp`, reads the bytes and
lets the directory go. Nothing accumulates on the stage or between sessions.

**`data.py` is 16.8k lines of reference data.** That is the bulk of the
repository and it is data, not logic — review it as a dataset. Its invariants
(three theme-keyed dicts that must stay in lockstep, unique test ids, no
shadowed module-level names) are enforced by `tests/test_data_integrity.py`.

## Known gaps, stated plainly

- **`app.py` is still 6.4k lines.** The stylesheet is out (`theme.py`) and the
  dead code is gone, but the seven section bodies and their helpers remain in
  one script. Splitting them is mechanically safe — there are no forward
  references — and the test suite would catch a mistake, but it has not been
  done. Expect a reviewer to raise it.
- **The three agent modules and `main.py` are CLI-shaped.** They work, and the
  Streamlit app only borrows `MODEL`, `upload_file` and
  `build_file_content_blocks` from `base_agent`, but they were written for a
  terminal. On Snowflake they are dead weight — leave them off the stage.
- **`auditiq/` and `AuditIQ.html`** are a React prototype kept as a design
  reference. Not wired to anything. Do not deploy them.
