"""
KidQuest — Streamlit launcher.
Serves the redesigned HTML/React prototype full-bleed.
"""
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="KidQuest — L'aventure du savoir",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      #MainMenu, header, footer { visibility: hidden; height: 0; }
      .block-container { padding: 0 !important; max-width: 100% !important; }
      [data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
      [data-testid="stSidebar"] { display: none; }
      body, .stApp { background: #FFF6E8; }
      iframe { border: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# The inlined HTML — everything bundled in (no external file fetches).
HTML = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")

# Full-bleed render. Height is generous; internal scroll lives inside the app.
components.html(HTML, height=1600, scrolling=True)
