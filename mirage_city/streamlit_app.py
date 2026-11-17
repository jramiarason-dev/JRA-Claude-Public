"""
Mirage City — lanceur Streamlit.
Affiche le jeu HTML/Three.js en plein écran dans la page Streamlit.
"""
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Mirage City",
    page_icon="🌴",
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
      body, .stApp { background: #0b0f17; }
      iframe { border: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Le jeu tient dans un seul fichier ; Three.js est chargé depuis un CDN.
HTML = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")

st.iframe(HTML, height=820)
