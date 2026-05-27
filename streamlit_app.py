"""
CoachIQ — Streamlit entry point.

Loads the HTML/React prototype and embeds it full-bleed inside a
Streamlit page. The prototype is a *UI/UX mockup*; back-end logic
(Claude calls, real data feeds) would replace the mocked data in
data.js when wired up.
"""

from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# ── Page setup ────────────────────────────────────────────────────
st.set_page_config(
    page_title="CoachIQ — Analyse tactique",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Strip Streamlit chrome — the prototype provides its own shell
st.markdown(
    """
    <style>
      #MainMenu, header, footer { visibility: hidden; height: 0; }
      .block-container {
        padding: 0 !important;
        max-width: 100% !important;
      }
      [data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
      [data-testid="stSidebar"] { display: none; }
      body, .stApp { background: #070b14; }
      iframe { border: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Asset loader ──────────────────────────────────────────────────
ROOT = Path(__file__).parent


def read(rel: str) -> str:
    """Read a project file as UTF-8 text."""
    return (ROOT / rel).read_text(encoding="utf-8")


# All UI sources are bundled inline so the page works in
# Streamlit's iframe sandbox (no external file fetches).
CSS_TOKENS = read("tokens.css")
CSS_STYLES = read("styles.css")
JS_DATA    = read("data.js")
JSX_TWEAKS = read("tweaks-panel.jsx")
JSX_UI     = read("components-ui.jsx")
JSX_SHELL  = read("components-shell.jsx")
JSX_DASH   = read("screen-dashboard.jsx")
JSX_MATCH  = read("screen-matches.jsx")
JSX_PRE    = read("screen-prematch.jsx")
JSX_POST   = read("screen-postmatch.jsx")
JSX_MISC   = read("screen-misc.jsx")
JSX_APP    = read("app.jsx")

# ── Build the standalone HTML ────────────────────────────────────
HTML = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>CoachIQ</title>
<style>{CSS_TOKENS}</style>
<style>{CSS_STYLES}</style>
<style>html,body{{margin:0;padding:0;overflow-x:hidden}}</style>
</head>
<body data-product="coachiq">
  <div id="root"></div>

  <script src="https://unpkg.com/react@18.3.1/umd/react.development.js"
          integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L"
          crossorigin="anonymous"></script>
  <script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"
          integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm"
          crossorigin="anonymous"></script>
  <script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"
          integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y"
          crossorigin="anonymous"></script>

  <script>{JS_DATA}</script>
  <script type="text/babel" data-presets="react">{JSX_TWEAKS}</script>
  <script type="text/babel" data-presets="react">{JSX_UI}</script>
  <script type="text/babel" data-presets="react">{JSX_SHELL}</script>
  <script type="text/babel" data-presets="react">{JSX_DASH}</script>
  <script type="text/babel" data-presets="react">{JSX_MATCH}</script>
  <script type="text/babel" data-presets="react">{JSX_PRE}</script>
  <script type="text/babel" data-presets="react">{JSX_POST}</script>
  <script type="text/babel" data-presets="react">{JSX_MISC}</script>
  <script type="text/babel" data-presets="react">{JSX_APP}</script>
</body>
</html>"""

# ── Render full-bleed ────────────────────────────────────────────
# Height is generous so internal scroll happens inside the prototype.
components.html(HTML, height=1400, scrolling=True)
