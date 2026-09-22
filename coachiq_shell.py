"""Assemblage de la page CoachIQ (HTML + CSS + React/JSX).

Les points d'entrée Streamlit décrivent seulement *quelles* données injecter ;
la liste des écrans et les dépendances CDN vivent ici. Auparavant chaque
entrée recopiait ce gabarit, et `streamlit_app.py` avait dérivé : il ne
chargeait pas les écrans Tactiques/Comparer/Tendances/Simulateur vers
lesquels `app.jsx` route pourtant, donc cliquer « Tactiques » levait une
ReferenceError et vidait l'écran.
"""

from pathlib import Path
from typing import Iterable

__all__ = ["build_html", "read_asset", "UI_SOURCES"]

_ROOT = Path(__file__).parent

# Ordre de chargement significatif : les primitives d'abord, `app.jsx` en
# dernier car c'est lui qui monte le composant racine.
UI_SOURCES: tuple[str, ...] = (
    "tweaks-panel.jsx",
    "components-ui.jsx",
    "components-shell.jsx",
    "screen-dashboard.jsx",
    "screen-matches.jsx",
    "screen-prematch.jsx",
    "screen-postmatch.jsx",
    "screen-misc.jsx",
    "screen-tactics.jsx",
    "screen-compare.jsx",
    "screen-trends.jsx",
    "screen-simulator.jsx",
    "app.jsx",
)

# Builds de production : 144 Ko contre 1,2 Mo pour les builds de
# développement, qui portent en plus les avertissements et le mode strict.
# Hashes calculés sur les paquets npm publiés (identiques à ceux du CDN).
_CDN_SCRIPTS: tuple[tuple[str, str], ...] = (
    ("https://unpkg.com/react@18.3.1/umd/react.production.min.js",
     "sha384-DGyLxAyjq0f9SPpVevD6IgztCFlnMF6oW/XQGmfe+IsZ8TqEiDrcHkMLKI6fiB/Z"),
    ("https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js",
     "sha384-gTGxhz21lVGYNMcdJOyq01Edg0jhn/c22nsx0kyqP0TxaV5WVdsSH1fSDUf5YJj1"),
    ("https://unpkg.com/@babel/standalone@7.29.0/babel.min.js",
     "sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y"),
)


def read_asset(rel: str) -> str:
    """Lit un fichier du projet en UTF-8."""
    return (_ROOT / rel).read_text(encoding="utf-8")


def _cdn_tags() -> str:
    return "\n  ".join(
        f'<script src="{url}" integrity="{sri}" crossorigin="anonymous"></script>'
        for url, sri in _CDN_SCRIPTS
    )


def build_html(data_scripts: Iterable[str] = ()) -> str:
    """Construit la page autonome.

    data_scripts : sources JavaScript déjà sérialisées (`window.X = {...};`)
    injectées avant les composants, pour que les écrans les trouvent au
    moment du rendu.
    """
    inline_data = "\n  ".join(f"<script>{src}</script>" for src in data_scripts)
    ui = "\n  ".join(
        f'<script type="text/babel" data-presets="react">{read_asset(name)}</script>'
        for name in UI_SOURCES
    )
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>CoachIQ</title>
<style>{read_asset("tokens.css")}</style>
<style>{read_asset("styles.css")}</style>
<style>html,body{{margin:0;padding:0;overflow-x:hidden}}</style>
</head>
<body data-product="coachiq">
  <div id="root"></div>

  {_cdn_tags()}

  <script>{read_asset("data.js")}</script>
  {inline_data}
  {ui}
</body>
</html>"""
