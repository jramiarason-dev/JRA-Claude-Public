"""EA Governance Animator — Entry point."""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import database as db
from database import get_ea_members, get_recent_activity

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EA Governance — Private Bank",
    page_icon="🏛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #1E2761 !important;
    color: #E8EDF8 !important;
  }
  [data-testid="stSidebar"] .stMarkdown,
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] .stSelectbox label { color: #E8EDF8 !important; }
  [data-testid="stSidebar"] .stSelectbox > div > div {
    background: #2D3A7C; border-color: #3D4F9F; color: #E8EDF8;
  }
  [data-testid="stSidebar"] hr { border-color: #3D4F9F; }

  /* Main background */
  .stApp { background: #F4F6FA; }
  .main .block-container { padding-top: 1.5rem; }

  /* Cards */
  div[data-testid="stExpander"] { background: #fff; border-radius: 10px; }

  /* Buttons */
  .stButton > button {
    background: #1E2761; color: #fff; border: none;
    border-radius: 8px; font-weight: 600;
  }
  .stButton > button:hover { background: #2D3A7C; }

  /* Metric cards */
  [data-testid="stMetric"] {
    background: #fff; border-radius: 10px;
    padding: 12px 16px; border: 1px solid #E5E7EB;
  }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] { gap: 8px; }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    font-weight: 600; color: #6B7280;
  }
  .stTabs [aria-selected="true"] {
    background: #1E2761; color: #fff !important;
  }

  /* Success / warning / error override */
  .stSuccess { border-left-color: #059669 !important; }
  .stWarning { border-left-color: #D97706 !important; }
  .stError   { border-left-color: #DC2626 !important; }

  /* Table */
  .stDataFrame { border-radius: 10px; overflow: hidden; }

  /* Page header */
  .page-header {
    background: #fff; border-radius: 12px;
    padding: 20px 24px; margin-bottom: 20px;
    border-left: 5px solid #1E2761;
    display: flex; justify-content: space-between; align-items: center;
  }
  .page-header h1 { margin: 0; color: #1E2761; font-size: 1.6rem; }
  .page-header p  { margin: 4px 0 0; color: #6B7280; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# ── DB init on first run ──────────────────────────────────────────────────────
if "db_initialized" not in st.session_state:
    db.init_db()
    conn = db.get_connection()
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    if user_count == 0:
        from data.seed_data import seed
        seed()
    st.session_state["db_initialized"] = True

# ── Session state defaults ────────────────────────────────────────────────────
if "current_user" not in st.session_state:
    st.session_state["current_user"] = "Head of EA"
if "current_role" not in st.session_state:
    st.session_state["current_role"] = "EA Lead"
if "notifications" not in st.session_state:
    st.session_state["notifications"] = []

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="text-align:center;padding:16px 0 8px;">
  <div style="font-size:2rem;">🏛</div>
  <div style="font-weight:700;font-size:1.1rem;color:#E8EDF8;">EA Governance</div>
  <div style="font-size:0.75rem;color:#94A3B8;">Private Bank — Technology</div>
</div>
""", unsafe_allow_html=True)
    st.markdown("---")

    # User selector
    ea_members = get_ea_members()
    all_users = [
        {"name": "Head of EA",                      "role": "EA Lead"},
        {"name": "Sr EA 1 — PWM / Application",     "role": "EA Reviewer"},
        {"name": "Sr EA 2 — PAS / Data & Security", "role": "EA Reviewer"},
        {"name": "Sr EA 3 — Ops / Process",         "role": "EA Reviewer"},
        {"name": "Risk & Compliance EA",            "role": "EA Reviewer"},
        {"name": "Cloud Architect EA",              "role": "EA Reviewer"},
        {"name": "Solution Architect (Observer)",   "role": "Submitter"},
        {"name": "CTO",                             "role": "Observer"},
    ]

    user_names = [u["name"] for u in all_users]
    current_idx = user_names.index(st.session_state["current_user"]) if st.session_state["current_user"] in user_names else 0

    selected_user = st.selectbox(
        "Active user",
        user_names,
        index=current_idx,
        key="user_selector",
    )

    for u in all_users:
        if u["name"] == selected_user:
            st.session_state["current_user"] = u["name"]
            st.session_state["current_role"] = u["role"]
            break

    role_colors = {
        "EA Lead":     "#059669",
        "EA Reviewer": "#4A90D9",
        "Submitter":   "#D97706",
        "Observer":    "#6B7280",
    }
    role = st.session_state["current_role"]
    rc   = role_colors.get(role, "#6B7280")

    st.markdown(f"""
<div style="background:#2D3A7C;border-radius:8px;padding:10px 14px;margin:8px 0;">
  <div style="font-size:0.78rem;color:#94A3B8;">Logged in as</div>
  <div style="font-weight:600;color:#E8EDF8;font-size:0.9rem;">{selected_user}</div>
  <div style="margin-top:4px;">
    <span style="background:{rc};color:#fff;padding:2px 8px;border-radius:10px;font-size:0.72rem;font-weight:600;">{role}</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # Pending queue badge
    from database import get_arch_reviews, get_std_exceptions
    my_ar = [r for r in get_arch_reviews() if r["assigned_ea"] and st.session_state["current_user"] in r["assigned_ea"]
             and r["status"] not in ("Approved","Rejected","Closed","Escalated")]
    my_ex = [r for r in get_std_exceptions() if r["assigned_ea"] and st.session_state["current_user"] in r["assigned_ea"]
             and r["status"] not in ("Approved","Rejected","Closed","SAB Escalation")]
    pending = len(my_ar) + len(my_ex)

    if pending > 0:
        st.markdown(f"""
<div style="background:#DC2626;color:#fff;border-radius:8px;padding:8px 14px;
            text-align:center;font-weight:700;font-size:0.9rem;">
  🔔 {pending} item(s) pending your review
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # Navigation
    st.markdown('<div style="color:#94A3B8;font-size:0.75rem;font-weight:600;letter-spacing:0.05em;padding:4px 0;">NAVIGATION</div>', unsafe_allow_html=True)

    pages = {
        "🏠 Dashboard":             "pages/01_dashboard.py",
        "📋 Architecture Reviews":  "pages/02_workflow_a.py",
        "⚠️ Standards Exceptions":  "pages/03_workflow_b.py",
        "📖 ADR Management":        "pages/04_adr.py",
        "📚 Standards Library":     "pages/05_standards.py",
        "⚙️ Admin":                 "pages/06_admin.py",
    }

    st.markdown("""
<div style="font-size:0.85rem;color:#B8C4E0;line-height:2.2;">
  Use the sidebar pages above ↑ to navigate.<br/>
  Or click below for quick links:
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # Recent activity (compact)
    st.markdown('<div style="color:#94A3B8;font-size:0.75rem;font-weight:600;letter-spacing:0.05em;padding:4px 0;">RECENT ACTIVITY</div>', unsafe_allow_html=True)
    recent = get_recent_activity(5)
    for act in recent:
        ts = act["logged_at"][:16] if act.get("logged_at") else ""
        st.markdown(f"""
<div style="font-size:0.73rem;color:#B8C4E0;border-left:2px solid #3D4F9F;padding-left:8px;margin:4px 0;">
  <span style="color:#94A3B8;">{ts}</span><br/>
  <b>{act.get('actor','')}</b> — {act.get('action','')} <span style="color:#7B8CC0;">{act.get('entity_ref','')}</span>
</div>
""", unsafe_allow_html=True)

# ── Landing page content ──────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div>
    <h1>🏛 EA Governance Animator</h1>
    <p>Enterprise Architecture governance platform — Private Bank Technology Division</p>
  </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info("**📋 Architecture Reviews**\nSubmit and track solution architecture review requests through Tier 1–3 governance.")
with col2:
    st.info("**⚠️ Standards Exceptions**\nRequest and manage deviations from approved architecture standards and patterns.")
with col3:
    st.info("**📖 ADRs**\nCreate and consult formal Architecture Decision Records with full provenance.")
with col4:
    st.info("**📚 Standards Library**\nBrowse, search, and manage the bank's architecture standards and patterns catalogue.")

st.markdown("---")
st.markdown("""
<div style="background:#fff;border-radius:10px;padding:20px;border:1px solid #E5E7EB;">
  <h3 style="color:#1E2761;margin-top:0;">Getting Started</h3>
  <p style="color:#374151;">
    Use the <b>navigation pages</b> in the Streamlit sidebar (left) to access each module.
    Select your user identity at the top of the sidebar to simulate different roles.
  </p>
  <ul style="color:#374151;">
    <li><b>EA Lead / EA Reviewer</b>: full access including review decisions and library management</li>
    <li><b>Submitter</b>: can submit requests and track their own items</li>
    <li><b>Observer</b>: read-only access to all content</li>
  </ul>
  <p style="color:#6B7280;font-size:0.85rem;margin-bottom:0;">
    Demo data is pre-loaded. Use the Admin page to reset to demo state at any time.
  </p>
</div>
""", unsafe_allow_html=True)
