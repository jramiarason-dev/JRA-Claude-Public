"""Reusable form helpers."""
import streamlit as st

BL_OPTIONS = ["PWM", "PAS", "Ops", "PTech", "Cross-BL"]
ARCH_TYPES  = ["New solution", "Significant change", "Pattern exception", "Cross-product dependency"]
COMPLEXITY  = ["Low", "Medium", "High"]
URGENCY     = ["Standard", "Urgent"]
VIOLATION   = ["No", "Suspected", "Confirmed"]
DURATIONS   = ["Permanent", "Temporary"]
EA_MEMBERS  = [
    "Head of EA",
    "Sr EA 1 — PWM / Application",
    "Sr EA 2 — PAS / Data & Security",
    "Sr EA 3 — Ops / Process",
    "Risk & Compliance EA",
    "Cloud Architect EA",
]


def ai_assistant_panel(workflow: str = "submission"):
    """Placeholder AI assistant panel — gracefully disabled until API key is set."""
    from ai_assistant import AI_ENABLED
    with st.expander("🤖 AI Assistant", expanded=False):
        if not AI_ENABLED:
            st.info(
                "**AI Analysis: Not activated** — configure `ANTHROPIC_API_KEY` to enable.\n\n"
                "When activated, the AI assistant will:\n"
                "- Pre-fill routing scores based on submission text\n"
                "- Suggest relevant standards and patterns\n"
                "- Flag potential standard violations\n"
                "- Draft review pre-assessments"
            )
            st.markdown("""
<div style="background:#F4F6FA;border:2px dashed #CBD5E1;border-radius:10px;
            padding:20px;text-align:center;color:#94A3B8;margin-top:8px;">
  AI suggestions will appear here once activated
</div>
""", unsafe_allow_html=True)
        else:
            st.success("AI Assistant active.")
