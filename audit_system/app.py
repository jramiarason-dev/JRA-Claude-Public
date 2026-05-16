"""
AuditIQ — Streamlit interface — 4 tabs (Intelligence Dashboard + 3 audit tabs)
Launch: streamlit run app.py (from audit_system/)
"""

import sys
import os
import json
import tempfile
from datetime import datetime
from pathlib import Path

import streamlit as st

_HERE = Path(__file__).parent.resolve()
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

st.set_page_config(
    page_title="AuditIQ",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state (init before CSS) ───────────────────────────────────────────
_SS_DEFAULTS = {
    # Dashboard
    "dash_cves": None, "dash_regs": None, "dash_audit_recs": None, "dash_updated": None,
    # Tab 1
    "t1_risks": None, "t1_regs": None, "t1_docx": None, "t1_topic": None,
    "t1_jurs": None, "t1_pub_recs": None,
    # Tab 2
    "t2_rationale": None, "t2_background": None, "t2_org_plan": None,
    "t2_tests": None, "t2_analytics": None, "t2_pptx": None, "t2_xlsx": None,
    # Tab 3
    "t3_report": None,
    # UX
    "theme": "dark",
    "history": [],
    "_tpl_applied": False,
    "_tpl_name": "",
    # Static data
    "dash_source": "static",   # "static" | "live"
    "ref_search": "",
    "t1_mode": "live",   # "live" | "static"
    "t2_mode": "live",
    "t3_mode": "live",
}
for _k, _v in _SS_DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── Example cards (hardcoded, always visible) ─────────────────────────────────
_EXAMPLE_RISK = """
<div style="border:1px solid rgba(239,68,68,0.4);border-radius:10px;padding:14px 18px;margin-bottom:14px;background:rgba(239,68,68,0.06)">
  <div style="font-size:10.5px;font-weight:600;color:#ef4444aa;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">📌 Example — AML/KYC Risk Indicator</div>
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
    <span style="background:rgba(239,68,68,0.15);color:#ef4444;border:1px solid rgba(239,68,68,0.35);border-radius:4px;padding:2px 9px;font-size:11px;font-weight:700">🔴 CRITICAL</span>
    <span style="font-size:13.5px;font-weight:600;color:var(--text-primary)">R002 — Inadequate PEP Screening</span>
    <span style="margin-left:auto;font-size:11px;color:var(--text-muted)">Prob: <span style="color:#ef4444;font-weight:600">High</span> &nbsp;·&nbsp; Impact: <span style="color:#ef4444;font-weight:600">High</span></span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:12px">
    <div>
      <div style="font-size:11px;font-weight:600;color:var(--text-muted);margin-bottom:4px;text-transform:uppercase">EXPECTED CONTROLS</div>
      <ul style="margin:0;padding-left:16px;color:var(--text-secondary);line-height:1.8">
        <li>Automated screening tool (World-Check / Refinitiv)</li>
        <li>Quarterly PEP list refresh</li>
        <li>EDD mandatory for all PEPs</li>
      </ul>
    </div>
    <div>
      <div style="font-size:11px;font-weight:600;color:#ef4444aa;margin-bottom:4px;text-transform:uppercase">RED FLAGS</div>
      <ul style="margin:0;padding-left:16px;color:var(--text-secondary);line-height:1.8">
        <li>Manual screening only</li>
        <li>No adverse media check</li>
        <li>Outdated PEP lists (>90 days)</li>
      </ul>
    </div>
  </div>
</div>
"""

_EXAMPLE_PUB_REC = """
<div style="border:1px solid rgba(79,126,248,0.3);border-radius:10px;padding:14px 18px;margin-bottom:14px;background:rgba(79,126,248,0.05)">
  <div style="font-size:10.5px;font-weight:600;color:#7fa8fbaa;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">📌 Example — Public Audit Recommendation</div>
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
    <span style="color:#7fa8fb;font-weight:600;font-size:13px">FATF</span>
    <span style="color:var(--text-muted);font-size:12px">· 2023 ·</span>
    <span style="background:rgba(239,68,68,0.12);color:#ef4444;border:1px solid rgba(239,68,68,0.32);border-radius:4px;padding:1px 7px;font-size:11px;font-weight:700">High Priority</span>
  </div>
  <p style="font-size:12.5px;color:var(--text-secondary);line-height:1.8;margin:0 0 8px;font-style:italic">
    "Private banks must implement risk-based EDD for all HNWI clients with assets above USD 1M, including source of wealth verification and annual review."
  </p>
  <div style="font-size:11.5px;color:var(--text-muted)">🏦 Directly applicable to Swiss private banking — triggers enhanced CDD obligations for HNWI client base.</div>
</div>
"""

_EXAMPLE_TEST = """
<div style="border:1px solid rgba(249,115,22,0.35);border-radius:10px;padding:14px 18px;margin-bottom:14px;background:rgba(249,115,22,0.06)">
  <div style="font-size:10.5px;font-weight:600;color:#f97316aa;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">📌 Example — Audit Test (Cyber Risk)</div>
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap">
    <span style="color:#7fa8fb;font-weight:700;font-size:13px">T011</span>
    <span style="background:rgba(79,126,248,0.12);color:#7fa8fb;border:1px solid rgba(79,126,248,0.28);border-radius:4px;padding:1px 7px;font-size:11px;font-weight:600">📊 DA</span>
    <span style="background:rgba(249,115,22,0.10);color:#f97316;border:1px solid rgba(249,115,22,0.30);border-radius:4px;padding:1px 7px;font-size:11px;font-weight:700">HIGH</span>
    <span style="font-size:13px;font-weight:600;color:var(--text-primary)">Verify MFA enforcement on all privileged accounts</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;font-size:12px;color:var(--text-secondary)">
    <div><span style="font-size:11px;color:var(--text-muted);font-weight:600;display:block;margin-bottom:2px">PROCEDURE</span>Extract admin accounts from AD/IAM, cross-ref with MFA enrollment logs, verify all remote-access channels.</div>
    <div><span style="font-size:11px;color:var(--text-muted);font-weight:600;display:block;margin-bottom:2px">POPULATION</span>All privileged accounts (~50-150)</div>
    <div><span style="font-size:11px;color:var(--text-muted);font-weight:600;display:block;margin-bottom:2px">FAILURE CRITERIA</span><span style="color:#ef4444">Any admin account without MFA enrolled and enforced</span></div>
  </div>
</div>
"""

_EXAMPLE_DA = """
<div style="border:1px solid rgba(34,211,165,0.3);border-radius:10px;padding:14px 18px;margin-bottom:14px;background:rgba(34,211,165,0.04)">
  <div style="font-size:10.5px;font-weight:600;color:#22d3a5aa;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">📌 Example — Data Analytics Scenario (Cyber Risk)</div>
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap">
    <span style="color:#22d3a5;font-weight:700;font-size:13px">DA013</span>
    <span style="font-size:13px;font-weight:600;color:var(--text-primary)">Privileged Access Anomaly Detection</span>
    <span style="margin-left:auto;background:rgba(234,179,8,0.12);color:#eab308;border:1px solid rgba(234,179,8,0.28);border-radius:4px;padding:1px 7px;font-size:11px;font-weight:600">🟡 Medium</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;font-size:12px;color:var(--text-secondary)">
    <div><span style="font-size:11px;color:var(--text-muted);font-weight:600;display:block;margin-bottom:2px">OBJECTIVE</span>Detect abnormal admin activity patterns suggesting insider threat or compromised credentials</div>
    <div><span style="font-size:11px;color:var(--text-muted);font-weight:600;display:block;margin-bottom:2px">DATA SOURCES</span>AD logs · SIEM · PAM system · HR database</div>
    <div><span style="font-size:11px;color:var(--text-muted);font-weight:600;display:block;margin-bottom:2px">ANOMALY DETECTED</span><span style="color:#f97316">Logins outside business hours, bulk exports, lateral movement, foreign IP access</span></div>
  </div>
  <div style="margin-top:10px;font-size:11.5px;color:var(--text-muted)">Tools: <span style="color:#7fa8fb">Python / Splunk</span> &nbsp;·&nbsp; Analysis: Anomaly Detection</div>
</div>
"""

_EXAMPLE_FINDING = """
<div style="border:1px solid rgba(249,115,22,0.4);border-radius:10px;padding:18px 22px;margin-bottom:14px;background:rgba(249,115,22,0.05)">
  <div style="font-size:10.5px;font-weight:600;color:#f97316aa;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:10px">📌 Example — Audit Report Finding</div>
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;flex-wrap:wrap">
    <span style="background:rgba(249,115,22,0.12);color:#f97316;border:1px solid rgba(249,115,22,0.32);border-radius:4px;padding:2px 10px;font-size:12px;font-weight:700">FINDING #1 — HIGH</span>
    <span style="font-size:13px;font-weight:600;color:var(--text-primary)">AML/KYC — Incomplete Source of Wealth Documentation</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;font-size:12.5px">
    <div>
      <div style="font-size:11px;color:var(--text-muted);font-weight:600;text-transform:uppercase;margin-bottom:4px">Observation</div>
      <p style="color:var(--text-secondary);margin:0;line-height:1.8">8 out of 30 client files tested (27%) lack updated source of wealth documentation despite assets exceeding CHF 5M threshold.</p>
    </div>
    <div>
      <div style="font-size:11px;color:var(--text-muted);font-weight:600;text-transform:uppercase;margin-bottom:4px">Risk</div>
      <p style="color:var(--text-secondary);margin:0;line-height:1.8">Regulatory sanction, reputational damage, potential facilitation of money laundering.</p>
    </div>
  </div>
  <div style="margin-top:12px;padding-top:12px;border-top:1px solid var(--border-divider)">
    <div style="font-size:11px;color:var(--text-muted);font-weight:600;text-transform:uppercase;margin-bottom:4px">Recommendation</div>
    <p style="color:var(--text-secondary);margin:0 0 8px;font-size:12.5px;line-height:1.8">Implement systematic annual review of SoW documentation for all clients above CHF 1M AuM. Assign ownership to Compliance team by Q2 2025.</p>
    <div style="font-size:11.5px;color:var(--text-muted)">
      Ref: <span style="color:#7fa8fb">FINMA-RS 2011/1 §15 · FATF R.10</span> &nbsp;·&nbsp; Management Response: <span style="color:#22d3a5">Due Q2 2025</span>
    </div>
  </div>
</div>
"""

# ── Theme CSS injection ────────────────────────────────────────────────────────
_is_dark = st.session_state.theme == "dark"

# Part 1: CSS variables (f-string for theme-dependent values)
if _is_dark:
    _theme_vars = """
    :root {
      --bg-app: #080b12;
      --bg-card: #0f121e;
      --bg-input: #10141f;
      --bg-sidebar: #0c0f1a;
      --text-primary: #dde3f5;
      --text-secondary: #8392bb;
      --text-muted: #424d72;
      --text-label: #8392bb;
      --border-subtle: rgba(255,255,255,0.07);
      --border-input: rgba(255,255,255,0.08);
      --border-divider: rgba(255,255,255,0.05);
      --tab-inactive: #5a6488;
      --tab-active: #a0b4f8;
      --tab-active-border: #4f7ef8;
      --btn-primary-bg: linear-gradient(135deg,#2d54d4 0%,#4f7ef8 100%);
      --btn-secondary-bg: rgba(79,126,248,0.10);
      --btn-secondary-color: #7fa8fb;
      --btn-secondary-border: rgba(79,126,248,0.25);
      --ctx-pill-bg: rgba(34,211,165,0.07);
      --ctx-pill-border: rgba(34,211,165,0.18);
      --ctx-pill-color: #22d3a5;
      --output-box-bg: #0f121e;
      --output-box-border: rgba(255,255,255,0.07);
      --output-box-text: #c8d0e8;
      --section-title-color: #dde3f5;
      --footer-color: #262e47;
      --tbl-row-border: rgba(255,255,255,0.04);
      --sidebar-header-color: #7fa8fb;
    }
    """
else:
    _theme_vars = """
    :root {
      --bg-app: #f5f7fa;
      --bg-card: #ffffff;
      --bg-input: #ffffff;
      --bg-sidebar: #eef0f6;
      --text-primary: #1a2040;
      --text-secondary: #4a5580;
      --text-muted: #8a95b8;
      --text-label: #4a5580;
      --border-subtle: rgba(0,0,0,0.07);
      --border-input: rgba(0,0,0,0.12);
      --border-divider: rgba(0,0,0,0.06);
      --tab-inactive: #6b7599;
      --tab-active: #2d54d4;
      --tab-active-border: #2d54d4;
      --btn-primary-bg: linear-gradient(135deg,#2d54d4 0%,#4f7ef8 100%);
      --btn-secondary-bg: rgba(45,84,212,0.08);
      --btn-secondary-color: #2d54d4;
      --btn-secondary-border: rgba(45,84,212,0.25);
      --ctx-pill-bg: rgba(34,211,165,0.08);
      --ctx-pill-border: rgba(34,211,165,0.25);
      --ctx-pill-color: #0d8f72;
      --output-box-bg: #ffffff;
      --output-box-border: rgba(0,0,0,0.08);
      --output-box-text: #2a3050;
      --section-title-color: #1a2040;
      --footer-color: #a0a8c0;
      --tbl-row-border: rgba(0,0,0,0.04);
      --sidebar-header-color: #2d54d4;
    }
    """

st.markdown(f"<style>{_theme_vars}</style>", unsafe_allow_html=True)

# Part 2: Static CSS using var() — no f-string needed
st.markdown("""
<style>
  html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
  .stApp { background-color: var(--bg-app) !important; color: var(--text-primary); }
  .main .block-container { padding: 2rem 3rem 4rem; max-width: 1060px; }

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-subtle);
  }
  section[data-testid="stSidebar"] .stMarkdown p { color: var(--text-secondary); font-size: 13px; }
  section[data-testid="stSidebar"] button {
    background: var(--btn-secondary-bg) !important;
    color: var(--btn-secondary-color) !important;
    border: 1px solid var(--btn-secondary-border) !important;
    border-radius: 7px !important; font-size: 12px !important;
    padding: 4px 10px !important; width: 100%; text-align: left;
  }
  section[data-testid="stSidebar"] button:hover { opacity: 0.82; }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid var(--border-subtle);
    gap: 0;
  }
  .stTabs [data-baseweb="tab"] {
    font-size: 13.5px !important; font-weight: 500 !important;
    color: var(--tab-inactive) !important;
    padding: 10px 22px !important;
    border-bottom: 2px solid transparent !important;
  }
  .stTabs [aria-selected="true"] {
    color: var(--tab-active) !important;
    border-bottom: 2px solid var(--tab-active-border) !important;
    background: transparent !important;
  }

  /* ── Inputs ── */
  .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border-input) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-size: 13.5px !important;
  }
  .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(79,126,248,0.5) !important;
    box-shadow: 0 0 0 3px rgba(79,126,248,0.08) !important;
  }
  label[data-testid="stWidgetLabel"] p {
    font-size: 13px !important; color: var(--text-label) !important; font-weight: 500;
  }

  /* ── Buttons ── */
  div[data-testid="stButton"] > button[kind="primary"] {
    background: var(--btn-primary-bg);
    border: none; border-radius: 9px; color: #fff;
    font-size: 13.5px; font-weight: 600; padding: 10px 28px;
    transition: opacity 0.15s;
  }
  div[data-testid="stButton"] > button[kind="primary"]:hover { opacity: 0.88; }
  div[data-testid="stButton"] > button[kind="primary"]:disabled {
    background: #1a1f32 !important; color: #3a4566 !important;
  }
  div[data-testid="stButton"] > button:not([kind="primary"]) {
    background: var(--btn-secondary-bg);
    color: var(--btn-secondary-color);
    border: 1px solid var(--btn-secondary-border);
    border-radius: 8px; font-size: 13px; font-weight: 500;
  }
  div[data-testid="stDownloadButton"] button {
    background: var(--btn-secondary-bg); color: var(--btn-secondary-color);
    border: 1px solid var(--btn-secondary-border); border-radius: 8px;
    font-size: 13px; font-weight: 500;
  }
  div[data-testid="stDownloadButton"] button:hover { opacity: 0.82; }

  div[data-testid="stFileUploader"] {
    border: 1px dashed var(--border-input) !important;
    border-radius: 10px !important; background: var(--bg-input) !important;
  }
  div[data-testid="stAlert"] { border-radius: 9px !important; font-size: 13px !important; }
  hr { border: none; border-top: 1px solid var(--border-divider) !important; margin: 1.8rem 0; }

  /* ── Content blocks ── */
  .output-box {
    background: var(--output-box-bg);
    border: 1px solid var(--output-box-border);
    border-radius: 10px; padding: 20px 24px;
    font-size: 13px; line-height: 1.9; white-space: pre-wrap;
    color: var(--output-box-text); max-height: 560px; overflow-y: auto;
  }
  .section-title {
    font-size: 15px; font-weight: 600; color: var(--section-title-color);
    margin: 1.8rem 0 1rem; letter-spacing: -0.2px;
  }
  .ctx-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--ctx-pill-bg); border: 1px solid var(--ctx-pill-border);
    color: var(--ctx-pill-color); border-radius: 8px; padding: 6px 14px;
    font-size: 12.5px; font-weight: 500; margin-bottom: 1.4rem;
  }

  /* ── Data table ── */
  .data-table { width: 100%; border-collapse: collapse; font-size: 12.5px; margin-bottom: 0.5rem; }
  .data-table th {
    padding: 9px 13px; text-align: left; font-weight: 600;
    font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.5px;
  }
  .data-table td { padding: 10px 13px; vertical-align: top; line-height: 1.6; }
  .data-table tr:not(:last-child) td { border-bottom: 1px solid var(--tbl-row-border); }

  /* ── Badges ── */
  .badge-critical { display:inline-block; background:rgba(239,68,68,0.15); color:#ef4444;
    border:1px solid rgba(239,68,68,0.35); border-radius:4px; padding:2px 8px;
    font-size:11px; font-weight:700; white-space:nowrap; }
  .badge-high { display:inline-block; background:rgba(249,115,22,0.12); color:#f97316;
    border:1px solid rgba(249,115,22,0.32); border-radius:4px; padding:2px 8px;
    font-size:11px; font-weight:700; white-space:nowrap; }
  .badge-medium { display:inline-block; background:rgba(234,179,8,0.10); color:#eab308;
    border:1px solid rgba(234,179,8,0.28); border-radius:4px; padding:2px 8px;
    font-size:11px; font-weight:700; white-space:nowrap; }
  .badge-open { display:inline-block; background:rgba(34,211,165,0.10); color:#22d3a5;
    border:1px solid rgba(34,211,165,0.28); border-radius:4px; padding:2px 8px;
    font-size:11px; font-weight:600; white-space:nowrap; }
  .badge-info { display:inline-block; background:rgba(79,126,248,0.10); color:#7fa8fb;
    border:1px solid rgba(79,126,248,0.28); border-radius:4px; padding:2px 8px;
    font-size:11px; font-weight:600; white-space:nowrap; }

  /* ── Progress bar ── */
  .progress-bar-wrap {
    display: flex; align-items: center; gap: 0; margin: 0.6rem 0 1.6rem;
  }
  .pb-step {
    display: flex; align-items: center; gap: 8px;
    font-size: 12.5px; font-weight: 500; padding: 7px 16px;
    border-radius: 20px; transition: all 0.2s;
  }
  .pb-step.done {
    background: rgba(34,211,165,0.10); color: #22d3a5;
    border: 1px solid rgba(34,211,165,0.25);
  }
  .pb-step.active {
    background: rgba(79,126,248,0.12); color: #7fa8fb;
    border: 1px solid rgba(79,126,248,0.30);
  }
  .pb-step.pending { color: var(--text-muted); border: 1px solid var(--border-subtle); }
  .pb-connector { flex: 1; height: 1px; background: var(--border-subtle); margin: 0 4px; min-width: 16px; }

  /* ── Gauge ── */
  .gauge-wrap { display: flex; align-items: center; gap: 32px; margin: 1rem 0 1.4rem; }
  .gauge-circle {
    width: 110px; height: 110px; border-radius: 50%; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    flex-direction: column; font-weight: 700;
  }
  .gauge-score { font-size: 30px; line-height: 1; }
  .gauge-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px; }
  .gauge-breakdown { flex: 1; }
  .gbar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 7px; font-size: 12px; }
  .gbar-label { width: 68px; color: var(--text-secondary); text-align: right; flex-shrink: 0; }
  .gbar-track { flex: 1; background: var(--border-subtle); border-radius: 4px; height: 8px; overflow: hidden; }
  .gbar-fill { height: 100%; border-radius: 4px; transition: width 0.4s; }
  .gbar-count { width: 20px; text-align: right; color: var(--text-secondary); flex-shrink: 0; }

  /* ── History item ── */
  .hist-item {
    background: var(--bg-card); border: 1px solid var(--border-subtle);
    border-radius: 8px; padding: 8px 12px; margin-bottom: 6px; font-size: 12px;
    cursor: pointer;
  }
  .hist-topic { color: var(--text-primary); font-weight: 600; }
  .hist-meta { color: var(--text-muted); font-size: 11px; margin-top: 2px; }

  /* ── Footer ── */
  .footer { font-size: 11px; color: var(--footer-color); text-align: center; margin-top: 2.5rem; letter-spacing: 0.3px; }

  /* ── Mobile responsive ── */
  @media (max-width: 768px) {
    .main .block-container { padding: 1rem 1rem 3rem !important; }
    .data-table { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }
    div[data-testid="stButton"] > button[kind="primary"] { width: 100% !important; }
    div[data-testid="stDownloadButton"] button { width: 100% !important; }
    .gauge-wrap { flex-direction: column; align-items: flex-start; }
    .stColumns { flex-direction: column !important; }
    .stColumns > div { width: 100% !important; min-width: 100% !important; }
  }

  /* ── Print ── */
  @media print {
    section[data-testid="stSidebar"] { display: none !important; }
    div[data-testid="stButton"], div[data-testid="stDownloadButton"],
    div[data-testid="stFileUploader"], div[data-testid="stTextInput"],
    div[data-testid="stTextArea"], div[data-testid="stMultiSelect"],
    div[data-testid="stSelectbox"], .stTabs [data-baseweb="tab-list"],
    .no-print { display: none !important; }
    .stApp { background: #fff !important; color: #000 !important; }
    .output-box { max-height: none !important; overflow: visible !important;
      background: #fff !important; color: #000 !important; border-color: #ccc !important; }
    .data-table td, .data-table th { border: 1px solid #ccc !important; color: #000 !important; }
    .section-title { color: #000 !important; }
  }
</style>
""", unsafe_allow_html=True)

# ── API key (backend only) ────────────────────────────────────────────────────
try:
    _api_key = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    _api_key = os.environ.get("ANTHROPIC_API_KEY", "")

if _api_key:
    os.environ["ANTHROPIC_API_KEY"] = _api_key

# ── Module imports ────────────────────────────────────────────────────────────
_READY = False
_ERR = ""
try:
    import anthropic as _ant
    import agent1_regulatory as _a1
    import agent2_audit_plan as _a2
    import agent3_report as _a3
    from base_agent import upload_file as _upload_file, build_file_content_blocks, MODEL
    from generators import (
        generate_regulatory_framework_docx,
        generate_audit_plan_ppt,
        generate_audit_procedures_excel,
        generate_audit_report_docx,
    )
    _READY = True
except ImportError as e:
    _ERR = str(e)

# ── Static data (always available, zero API calls) ────────────────────────────
from data import (
    REGULATORY_FRAMEWORKS, AUDIT_TEMPLATES as _DATA_TEMPLATES,
    RISK_INDICATORS, PUBLIC_AUDIT_RECOMMENDATIONS,
    CVE_BANKING, IIA_STANDARDS_2024, DATA_ANALYTICS_SCENARIOS,
    AUDIT_TESTS_LIBRARY, TOPIC_THEME_MAP,
)

JURISDICTIONS = ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU / DORA", "UK / FCA+PRA"]
OUTPUT_DIR = str(_HERE / "outputs")
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# ── Templates ─────────────────────────────────────────────────────────────────
TEMPLATES = {
    "— Select a template —": {},
    "AML / KYC & Transaction Monitoring": {
        "topic": "AML/KYC & Transaction Monitoring",
        "jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "EU / DORA", "UK / FCA+PRA"],
        "scope": "All group entities. Focus on customer onboarding, CDD/EDD, transaction monitoring, STR/SAR filing, and PEP/sanctions screening.",
    },
    "Cyber Risk & IT Security": {
        "topic": "Cyber Risk & IT Security",
        "jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU / DORA", "UK / FCA+PRA"],
        "scope": "IT infrastructure, cybersecurity controls, incident response, third-party IT vendors, and data protection.",
    },
    "Credit Risk & Lending": {
        "topic": "Credit Risk & Lending",
        "jurisdictions": ["CH / FINMA", "SG / MAS", "EU / DORA", "UK / FCA+PRA"],
        "scope": "Lombard lending, mortgage portfolios, credit underwriting, collateral management, and credit risk monitoring.",
    },
    "Operational Risk & Business Continuity": {
        "topic": "Operational Risk & Business Continuity",
        "jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU / DORA", "UK / FCA+PRA"],
        "scope": "Operational risk framework, BCP/DR testing, key person dependencies, and outsourcing arrangements.",
    },
    "Data Privacy & GDPR/nDSG": {
        "topic": "Data Privacy & GDPR / nDSG",
        "jurisdictions": ["CH / FINMA", "EU / DORA", "UK / FCA+PRA"],
        "scope": "Client data handling, consent management, data retention policies, cross-border data transfers, and breach notification.",
    },
    "Market Risk & Trading": {
        "topic": "Market Risk & Trading",
        "jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "EU / DORA", "UK / FCA+PRA"],
        "scope": "Trading book, VaR models, stress testing, market risk limits, and front-office controls.",
    },
    "Third Party & Vendor Risk": {
        "topic": "Third Party & Vendor Risk",
        "jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU / DORA", "UK / FCA+PRA"],
        "scope": "Critical outsourcing arrangements, vendor due diligence, contract management, and sub-outsourcing oversight.",
    },
    "Governance & Internal Controls": {
        "topic": "Governance & Internal Controls",
        "jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU / DORA", "UK / FCA+PRA"],
        "scope": "Board oversight, three lines of defence, risk committee effectiveness, and control framework assessment.",
    },
}

_disabled = not _api_key or not _READY


# ── Utility functions ─────────────────────────────────────────────────────────

def _client():
    return _ant.Anthropic(api_key=_api_key)


def _call(client, prompt, system="You are an expert audit consultant specialising in private banking and wealth management.", max_tokens=6000):
    resp = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()


def _web_search_call(client, prompt, system="", max_tokens=6000):
    messages = [{"role": "user", "content": prompt}]
    texts = []
    ws_tool = [{"type": "web_search_20250305", "name": "web_search"}]
    for _ in range(8):
        kwargs = dict(model=MODEL, max_tokens=max_tokens, tools=ws_tool, messages=messages)
        if system:
            kwargs["system"] = system
        r = client.messages.create(**kwargs)
        for b in r.content:
            if hasattr(b, "text") and b.text:
                texts.append(b.text)
        if r.stop_reason == "end_turn":
            break
        if r.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": r.content})
            tool_results = []
            for b in r.content:
                if getattr(b, "type", None) == "tool_use":
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": b.id,
                        "content": "Search completed by server.",
                    })
            if tool_results:
                messages.append({"role": "user", "content": tool_results})
            else:
                break
        else:
            break
    return "\n".join(texts).strip()


def _parse_json(text):
    t = text.strip()
    if t.startswith("```"):
        for part in t.split("```"):
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("[") or part.startswith("{"):
                t = part
                break
    try:
        return json.loads(t)
    except Exception:
        pass
    start = t.find("[")
    end = t.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(t[start:end + 1])
        except Exception:
            pass
    return None


def _upload_sf(client, f):
    if not f:
        return None
    suf = Path(f.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suf) as tmp:
        tmp.write(f.read())
        tmp_path = tmp.name
    try:
        return _upload_file(client, tmp_path)
    finally:
        os.unlink(tmp_path)


def _agentic_loop(client, sys_prompt, tools, messages, tool_fn):
    texts, extra = [], {}
    while True:
        r = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=sys_prompt,
            messages=messages,
            tools=tools,
            betas=["files-api-2025-04-14"],
        )
        for b in r.content:
            if hasattr(b, "text") and b.text:
                texts.append(b.text)
        messages.append({"role": "assistant", "content": r.content})
        if r.stop_reason == "end_turn":
            break
        if r.stop_reason == "tool_use":
            results = []
            for b in r.content:
                if b.type != "tool_use":
                    continue
                txt, ex = tool_fn(b.name, b.input)
                extra.update(ex)
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": txt})
            if results:
                messages.append({"role": "user", "content": results})
            else:
                break
        else:
            break
    return "\n".join(texts), extra


# ── Static data helpers ───────────────────────────────────────────────────────

def _topic_to_theme(topic: str) -> str | None:
    """Map a free-text audit topic to a THEME key used in RISK_INDICATORS etc."""
    if not topic:
        return None
    up = topic.upper()
    for kw, theme in TOPIC_THEME_MAP.items():
        if kw in up:
            return theme
    return None


def _static_label():
    """Small badge marking data as static reference (no API call)."""
    st.markdown(
        '<span style="background:rgba(34,211,165,0.10);color:#22d3a5;'
        'border:1px solid rgba(34,211,165,0.25);border-radius:4px;'
        'padding:2px 9px;font-size:11px;font-weight:600;vertical-align:middle">'
        '📚 Reference Data</span>',
        unsafe_allow_html=True,
    )


def _show_risk_indicators(theme: str, search: str = ""):
    """Display RISK_INDICATORS for a given theme with optional search filter."""
    risks = RISK_INDICATORS.get(theme, [])
    if search:
        q = search.lower()
        risks = [r for r in risks if q in (r.get("title","") + r.get("description","") + r.get("private_banking_specifics","")).lower()]
    if not risks:
        st.caption("No matching risks.")
        return

    _LEVEL_COLOR = {"Critical": "#ef4444", "High": "#f97316", "Moderate": "#eab308"}
    _LEVEL_BG    = {"Critical": "rgba(239,68,68,0.08)", "High": "rgba(249,115,22,0.08)", "Moderate": "rgba(234,179,8,0.06)"}

    for r in risks:
        col = _LEVEL_COLOR.get(r["level"], "#8392bb")
        bg  = _LEVEL_BG.get(r["level"], "transparent")
        prob_color  = {"High": "#ef4444", "Medium": "#eab308", "Low": "#22d3a5"}.get(r.get("probability",""), "#8392bb")
        impact_color = {"High": "#ef4444", "Medium": "#eab308", "Low": "#22d3a5"}.get(r.get("impact",""), "#8392bb")

        controls_html = "".join(f"<li>{c}</li>" for c in r.get("expected_controls", []))
        flags_html    = "".join(f"<li>{f}</li>" for f in r.get("red_flags", []))

        st.markdown(f"""
        <div style="border:1px solid {col}33;border-radius:9px;padding:14px 18px;margin-bottom:12px;background:{bg}">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <span style="background:{col}22;color:{col};border:1px solid {col}44;border-radius:4px;
                   padding:2px 9px;font-size:11px;font-weight:700">{r["level"]}</span>
            <span style="font-size:13.5px;font-weight:600;color:var(--text-primary)">{r.get("id","")} — {r["title"]}</span>
            <span style="margin-left:auto;font-size:11px;color:var(--text-muted)">
              Prob: <span style="color:{prob_color};font-weight:600">{r.get("probability","")}</span>
              &nbsp;·&nbsp; Impact: <span style="color:{impact_color};font-weight:600">{r.get("impact","")}</span>
            </span>
          </div>
          <p style="font-size:12.5px;color:var(--text-secondary);margin:0 0 10px;line-height:1.7">{r["description"]}</p>
          <details style="margin-bottom:6px">
            <summary style="font-size:12px;color:#7fa8fb;cursor:pointer;font-weight:500">Controls &amp; Red Flags</summary>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:8px">
              <div>
                <div style="font-size:11px;font-weight:600;color:var(--text-muted);margin-bottom:4px">EXPECTED CONTROLS</div>
                <ul style="margin:0;padding-left:16px;font-size:12px;color:var(--text-secondary);line-height:1.8">{controls_html}</ul>
              </div>
              <div>
                <div style="font-size:11px;font-weight:600;color:#ef4444aa;margin-bottom:4px">RED FLAGS</div>
                <ul style="margin:0;padding-left:16px;font-size:12px;color:var(--text-secondary);line-height:1.8">{flags_html}</ul>
              </div>
            </div>
            <div style="margin-top:10px;font-size:11.5px;color:var(--text-muted);font-style:italic">
              🏦 {r.get("private_banking_specifics","")}
            </div>
          </details>
        </div>
        """, unsafe_allow_html=True)


def _show_pub_recs(theme: str, search: str = ""):
    """Display PUBLIC_AUDIT_RECOMMENDATIONS filtered by theme and search."""
    recs = [r for r in PUBLIC_AUDIT_RECOMMENDATIONS if r.get("theme") == theme]
    if search:
        q = search.lower()
        recs = [r for r in recs if q in (r.get("source","") + r.get("recommendation","") + r.get("private_banking_relevance","")).lower()]
    if not recs:
        st.caption("No recommendations for this theme.")
        return

    rows = ""
    for r in recs:
        pri = r.get("priority", "")
        badge = '<span class="badge-high">High</span>' if pri == "High" else '<span class="badge-medium">Medium</span>'
        rows += (
            f'<tr>'
            f'<td style="padding:9px 13px;color:#7fa8fb;font-weight:500;white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("source","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-muted);text-align:center;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("year","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("recommendation","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-muted);font-size:11.5px;font-style:italic;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("private_banking_relevance","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{badge}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(79,126,248,0.07);border-bottom:1px solid rgba(79,126,248,0.18)">
        <th style="color:#7fa8fb;width:12%">Source</th><th style="color:#7fa8fb;width:5%;text-align:center">Year</th>
        <th style="color:#7fa8fb;width:40%">Recommendation</th>
        <th style="color:#7fa8fb;width:35%">Private Banking Relevance</th>
        <th style="color:#7fa8fb;width:8%">Priority</th>
      </tr></thead><tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)


def _show_da_scenarios(theme: str, search: str = ""):
    """Display DATA_ANALYTICS_SCENARIOS for a theme."""
    scenarios = DATA_ANALYTICS_SCENARIOS.get(theme, [])
    if search:
        q = search.lower()
        scenarios = [s for s in scenarios if q in (s.get("title","") + s.get("objective","") + s.get("anomaly_searched","")).lower()]
    if not scenarios:
        st.caption("No scenarios for this theme.")
        return

    _CMPLX = {"Low": "#22d3a5", "Medium": "#eab308", "High": "#f97316"}
    rows = ""
    for s in scenarios:
        cx_col = _CMPLX.get(s.get("complexity",""), "#8392bb")
        ds = " · ".join(s.get("data_sources", []))
        tools = " · ".join(s.get("tools", []))
        rows += (
            f'<tr>'
            f'<td style="padding:9px 13px;color:#7fa8fb;font-weight:600;white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{s.get("id","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-primary);font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{s.get("title","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{s.get("objective","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{s.get("analysis_type","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-muted);font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{s.get("anomaly_searched","")}</td>'
            f'<td style="padding:9px 13px;font-size:11px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">'
            f'<span style="color:{cx_col};font-weight:600">{s.get("complexity","")}</span>'
            f'<br><span style="color:var(--text-muted)">{tools}</span></td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(79,126,248,0.07);border-bottom:1px solid rgba(79,126,248,0.18)">
        <th style="color:#7fa8fb;width:6%">ID</th><th style="color:#7fa8fb;width:18%">Scenario</th>
        <th style="color:#7fa8fb;width:25%">Objective</th><th style="color:#7fa8fb;width:12%">Analysis Type</th>
        <th style="color:#7fa8fb;width:28%">Anomaly Searched</th><th style="color:#7fa8fb;width:11%">Complexity / Tools</th>
      </tr></thead><tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)


def _show_regulatory_frameworks(jur_filter: str = "All", search: str = ""):
    """Display REGULATORY_FRAMEWORKS grouped by jurisdiction."""
    for jur, regs in REGULATORY_FRAMEWORKS.items():
        if jur_filter != "All" and jur != jur_filter:
            continue
        filtered = regs
        if search:
            q = search.lower()
            filtered = [r for r in regs if q in (r.get("reference","") + r.get("title","") + " ".join(r.get("applies_to",[]))).lower()]
        if not filtered:
            continue
        with st.expander(f"**{jur}** — {len(filtered)} texts", expanded=(jur_filter != "All")):
            rows = ""
            for r in filtered:
                applies = " &nbsp;".join(f'<span class="badge-info">{t}</span>' for t in r.get("applies_to", []))
                reqs = "".join(f"<li>{k}</li>" for k in r.get("key_requirements", []))
                rows += (
                    f'<tr>'
                    f'<td style="padding:9px 13px;color:#7fa8fb;font-weight:600;white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("reference","")}</td>'
                    f'<td style="padding:9px 13px;color:var(--text-primary);font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("title","")}<br><span style="font-size:11px;color:var(--text-muted)">{r.get("authority","")} · {r.get("year","")}</span></td>'
                    f'<td style="padding:9px 13px;color:var(--text-secondary);font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("scope","")}</td>'
                    f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{applies}</td>'
                    f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)"><ul style="margin:0;padding-left:15px;font-size:11.5px;color:var(--text-secondary);line-height:1.7">{reqs}</ul></td>'
                    f'</tr>'
                )
            st.markdown(f"""
            <table class="data-table" style="font-size:12px">
              <thead><tr style="background:rgba(79,126,248,0.07);border-bottom:1px solid rgba(79,126,248,0.18)">
                <th style="color:#7fa8fb;width:10%">Reference</th><th style="color:#7fa8fb;width:18%">Title</th>
                <th style="color:#7fa8fb;width:22%">Scope</th><th style="color:#7fa8fb;width:14%">Applies To</th>
                <th style="color:#7fa8fb;width:36%">Key Requirements</th>
              </tr></thead><tbody>{rows}</tbody>
            </table>""", unsafe_allow_html=True)


def _show_cve_static(search: str = "", sev_filter: str = "All"):
    """Display CVE_BANKING with optional filters."""
    cves = CVE_BANKING
    if sev_filter != "All":
        cves = [c for c in cves if c.get("severity") == sev_filter]
    if search:
        q = search.lower()
        cves = [c for c in cves if q in (c.get("cve_id","") + c.get("system_affected","") + c.get("description","")).lower()]
    if not cves:
        st.caption("No CVEs match the filter.")
        return

    rows = ""
    for c in cves:
        sev = c.get("severity","")
        badge = '<span class="badge-critical">Critical</span>' if sev == "Critical" else '<span class="badge-high">High</span>'
        cvss = c.get("cvss_score", "")
        rows += (
            f'<tr>'
            f'<td style="padding:9px 13px;color:var(--text-primary);font-weight:600;white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{c.get("cve_id","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-muted);white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{c.get("date","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{badge} <span style="font-size:11px;color:var(--text-muted)">CVSS {cvss}</span></td>'
            f'<td style="padding:9px 13px;color:var(--text-primary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{c.get("system_affected","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{c.get("description","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{c.get("banking_relevance","")}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(239,68,68,0.06);border-bottom:1px solid rgba(239,68,68,0.18)">
        <th style="color:#ef4444;width:10%">CVE ID</th><th style="color:#6b7599;width:7%">Date</th>
        <th style="color:#6b7599;width:10%">Severity</th><th style="color:#6b7599;width:16%">System</th>
        <th style="color:#6b7599;width:28%">Description</th><th style="color:#6b7599;width:29%">Banking Relevance</th>
      </tr></thead><tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)


def _mode_toggle(key: str, label_live: str = "⚡ Live Analysis", label_static: str = "📚 Static Reference Data"):
    """Render a two-button toggle for live vs static mode. Updates session_state[key] on click."""
    _cur = st.session_state.get(key, "live")
    _c1, _c2, _ = st.columns([1.4, 1.9, 4])
    if _c1.button(label_live, key=f"_toggle_{key}_live",
                  type="primary" if _cur == "live" else "secondary"):
        st.session_state[key] = "live"
        st.rerun()
    if _c2.button(label_static, key=f"_toggle_{key}_static",
                  type="primary" if _cur == "static" else "secondary"):
        st.session_state[key] = "static"
        st.rerun()


def _show_tests_library(theme: str, search: str = "", level_filter: str = "All", type_filter: str = "All"):
    """Display AUDIT_TESTS_LIBRARY for a given theme with filters."""
    tests = AUDIT_TESTS_LIBRARY.get(theme, [])
    if level_filter != "All":
        tests = [t for t in tests if t.get("level") == level_filter]
    if type_filter != "All" and type_filter == "Data Analytics":
        tests = [t for t in tests if t.get("category") == "Data Analytics"]
    elif type_filter == "Standard":
        tests = [t for t in tests if t.get("category") == "Standard"]
    if search:
        q = search.lower()
        tests = [t for t in tests if q in (t.get("objective","") + t.get("procedure","") + t.get("id","")).lower()]
    if not tests:
        st.caption("No tests match the filter.")
        return
    _LEVEL_COLOR = {"Critical": "#ef4444", "High": "#f97316", "Moderate": "#eab308"}
    _LEVEL_BG    = {"Critical": "rgba(239,68,68,0.08)", "High": "rgba(249,115,22,0.08)", "Moderate": "rgba(234,179,8,0.06)"}
    _DA_BADGE = '<span style="background:rgba(79,126,248,0.12);color:#7fa8fb;border:1px solid rgba(79,126,248,0.28);border-radius:4px;padding:1px 7px;font-size:11px;font-weight:600">📊 DA</span>'
    rows = ""
    for t in tests:
        lv = t.get("level", "")
        col = _LEVEL_COLOR.get(lv, "#8392bb")
        bg  = _LEVEL_BG.get(lv, "transparent")
        da  = _DA_BADGE if t.get("category") == "Data Analytics" else ""
        lv_badge = f'<span style="background:{bg};color:{col};border:1px solid {col}44;border-radius:4px;padding:1px 7px;font-size:11px;font-weight:700">{lv}</span>'
        rows += (
            f'<tr style="background:{bg}">'
            f'<td style="padding:9px 12px;color:#7fa8fb;font-weight:700;white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("id","")} {da}</td>'
            f'<td style="padding:9px 12px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{lv_badge}</td>'
            f'<td style="padding:9px 12px;color:var(--text-primary);font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("objective","")}</td>'
            f'<td style="padding:9px 12px;color:var(--text-secondary);font-size:12px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("procedure","")}</td>'
            f'<td style="padding:9px 12px;color:var(--text-muted);font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("population","")}</td>'
            f'<td style="padding:9px 12px;color:var(--text-muted);font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("sample_size","")}</td>'
            f'<td style="padding:9px 12px;color:#ef4444;font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("failure_criteria","")}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(79,126,248,0.07);border-bottom:1px solid rgba(79,126,248,0.18)">
        <th style="color:#7fa8fb;width:8%">ID</th>
        <th style="color:#7fa8fb;width:8%">Level</th>
        <th style="color:#7fa8fb;width:20%">Objective</th>
        <th style="color:#7fa8fb;width:26%">Procedure</th>
        <th style="color:#7fa8fb;width:16%">Population</th>
        <th style="color:#7fa8fb;width:12%">Sample Size</th>
        <th style="color:#7fa8fb;width:10%">Failure Criteria</th>
      </tr></thead><tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)


def _show_iia_standards():
    """Display IIA_STANDARDS_2024 in expandable cards."""
    for s in IIA_STANDARDS_2024:
        reqs = "".join(f"<li>{r}</li>" for r in s.get("key_requirements", []))
        with st.expander(f"**{s['standard_id']}** — {s['title']}"):
            st.markdown(f"""
            <p style="font-size:13px;color:var(--text-secondary);line-height:1.8;margin-bottom:12px">{s['description']}</p>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
              <div>
                <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;
                     color:#7fa8fb;margin-bottom:6px">Key Requirements</div>
                <ul style="margin:0;padding-left:16px;font-size:12.5px;color:var(--text-secondary);line-height:1.8">{reqs}</ul>
              </div>
              <div style="background:rgba(34,211,165,0.06);border:1px solid rgba(34,211,165,0.18);
                          border-radius:8px;padding:12px">
                <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;
                     color:#22d3a5;margin-bottom:6px">🏦 Banking Relevance</div>
                <p style="margin:0;font-size:12.5px;color:var(--text-secondary);line-height:1.8">{s['relevance_to_banking']}</p>
              </div>
            </div>
            """, unsafe_allow_html=True)


# ── UX helpers ────────────────────────────────────────────────────────────────

def _save_history(topic, jurs, risks, regs, pub_recs):
    """Save current analysis to FIFO history (max 5)."""
    n_critical = sum(1 for r in (risks or []) if r.get("level") == "Critical")
    n_high = sum(1 for r in (risks or []) if r.get("level") == "High")
    entry = {
        "topic": topic,
        "jurs": jurs or [],
        "timestamp": datetime.now().strftime("%d %b %Y %H:%M"),
        "n_critical": n_critical,
        "n_high": n_high,
        "n_regs": len(regs or []),
    }
    hist = st.session_state.history or []
    hist = [h for h in hist if h.get("topic") != topic]
    hist.insert(0, entry)
    st.session_state.history = hist[:5]


def _build_progress_bar():
    """Render step indicator above tabs."""
    t1_done = bool(st.session_state.t1_risks or st.session_state.t1_regs)
    t2_done = bool(st.session_state.t2_rationale)
    t3_done = bool(st.session_state.t3_report)

    def _step(label, icon, state):
        cls = {"done": "pb-step done", "active": "pb-step active", "pending": "pb-step pending"}[state]
        return f'<div class="{cls}">{icon} {label}</div>'

    s1 = "done" if t1_done else "active"
    s2 = "done" if t2_done else ("active" if t1_done else "pending")
    s3 = "done" if t3_done else ("active" if t2_done else "pending")

    html = (
        '<div class="progress-bar-wrap no-print">'
        + _step("Risk Analysis", "✓" if t1_done else "1", s1)
        + '<div class="pb-connector"></div>'
        + _step("Audit Plan", "✓" if t2_done else "2", s2)
        + '<div class="pb-connector"></div>'
        + _step("Audit Report", "✓" if t3_done else "3", s3)
        + '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def _risk_score_display(risks, n_jurs):
    """Render circular gauge + breakdown bars for risk score."""
    n_c = sum(1 for r in (risks or []) if r.get("level") == "Critical")
    n_h = sum(1 for r in (risks or []) if r.get("level") == "High")
    n_m = sum(1 for r in (risks or []) if r.get("level") == "Moderate")

    score = min(100, n_c * 15 + n_h * 8 + n_m * 3 + n_jurs * 2)

    if score <= 30:
        label, color, bg = "Low", "#22d3a5", "rgba(34,211,165,0.12)"
    elif score <= 60:
        label, color, bg = "Moderate", "#eab308", "rgba(234,179,8,0.12)"
    elif score <= 80:
        label, color, bg = "High", "#f97316", "rgba(249,115,22,0.12)"
    else:
        label, color, bg = "Critical", "#ef4444", "rgba(239,68,68,0.12)"

    pct = score  # 0-100
    gauge_css = (
        f"background: conic-gradient({color} {pct * 3.6}deg, rgba(255,255,255,0.06) 0deg);"
        f"background-color: var(--bg-card);"
    )

    total = max(1, n_c + n_h + n_m)

    def _bar(lbl, count, bar_color):
        w = int(count / total * 100)
        return (
            f'<div class="gbar-row">'
            f'<div class="gbar-label">{lbl}</div>'
            f'<div class="gbar-track"><div class="gbar-fill" style="width:{w}%;background:{bar_color}"></div></div>'
            f'<div class="gbar-count">{count}</div>'
            f'</div>'
        )

    breakdown = (
        _bar("Critical", n_c, "#ef4444")
        + _bar("High", n_h, "#f97316")
        + _bar("Moderate", n_m, "#eab308")
    )

    st.markdown(
        f'<div class="gauge-wrap">'
        f'<div class="gauge-circle" style="{gauge_css}">'
        f'<span class="gauge-score" style="color:{color}">{score}</span>'
        f'<span class="gauge-label" style="color:{color}">{label}</span>'
        f'</div>'
        f'<div class="gauge-breakdown">{breakdown}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _filter_data(data, text_fields, filter_key, level_field=None, jur_field=None):
    """Render search/filter controls and return filtered list."""
    if not data:
        return data

    col_parts = [3]
    if level_field:
        col_parts.append(1.4)
    if jur_field:
        col_parts.append(1.4)
    cols = st.columns(col_parts)

    search = cols[0].text_input(
        "Search", placeholder="Filter…",
        key=f"_search_{filter_key}", label_visibility="collapsed"
    )

    level_filter = None
    if level_field and len(cols) > 1:
        levels = sorted({str(d.get(level_field, "")) for d in data if d.get(level_field)})
        if levels:
            level_filter = cols[1].selectbox(
                "Level", options=["All"] + levels,
                key=f"_lvl_{filter_key}", label_visibility="collapsed"
            )

    jur_filter = None
    if jur_field and len(cols) > (2 if level_field else 1):
        jurs = sorted({str(d.get(jur_field, "")) for d in data if d.get(jur_field)})
        if jurs:
            idx = 2 if level_field else 1
            jur_filter = cols[idx].selectbox(
                "Jurisdiction", options=["All"] + jurs,
                key=f"_jur_{filter_key}", label_visibility="collapsed"
            )

    filtered = data
    if search:
        q = search.lower()
        filtered = [
            d for d in filtered
            if any(q in str(d.get(f, "")).lower() for f in text_fields)
        ]
    if level_filter and level_filter != "All":
        filtered = [d for d in filtered if str(d.get(level_field, "")) == level_filter]
    if jur_filter and jur_filter != "All":
        filtered = [d for d in filtered if str(d.get(jur_field, "")) == jur_filter]

    return filtered


def _copy_button(text_to_copy, key_id):
    """Render a copy-to-clipboard button via JS (no API call)."""
    safe = text_to_copy.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    html = f"""
    <button onclick="navigator.clipboard.writeText(`{safe}`).then(()=>{{
      this.textContent='✓ Copied!';
      setTimeout(()=>{{this.textContent='⎘ Copy'}},1800);
    }})" style="
      background:rgba(79,126,248,0.10);color:#7fa8fb;
      border:1px solid rgba(79,126,248,0.25);border-radius:8px;
      font-size:12px;font-weight:500;padding:5px 14px;cursor:pointer;
      font-family:-apple-system,BlinkMacSystemFont,sans-serif;
    ">⎘ Copy</button>
    """
    st.components.v1.html(html, height=40)


def _print_button():
    """Render a print button via JS (no API call)."""
    html = """
    <button onclick="window.print()" style="
      background:rgba(79,126,248,0.10);color:#7fa8fb;
      border:1px solid rgba(79,126,248,0.25);border-radius:8px;
      font-size:12px;font-weight:500;padding:5px 14px;cursor:pointer;
      font-family:-apple-system,BlinkMacSystemFont,sans-serif;
    ">🖨 Print / PDF</button>
    """
    st.components.v1.html(html, height=40)


# ── Display components ────────────────────────────────────────────────────────

_LEVEL_STYLE = {
    "Critical": ("#ef4444", "rgba(239,68,68,0.10)", "rgba(239,68,68,0.28)"),
    "High":     ("#f97316", "rgba(249,115,22,0.10)", "rgba(249,115,22,0.28)"),
    "Moderate": ("#eab308", "rgba(234,179,8,0.08)",  "rgba(234,179,8,0.24)"),
}

_SEV_BADGE = {
    "Critical": '<span class="badge-critical">Critical</span>',
    "High":     '<span class="badge-high">High</span>',
    "Medium":   '<span class="badge-medium">Medium</span>',
    "High Priority": '<span class="badge-high">High</span>',
    "Medium Priority": '<span class="badge-medium">Medium</span>',
}

_TYPE_BADGE = {
    "Consultation": '<span class="badge-open">Consultation</span>',
    "Final Rule":   '<span class="badge-critical">Final Rule</span>',
    "Circular":     '<span class="badge-info">Circular</span>',
    "Guidance":     '<span class="badge-info">Guidance</span>',
}


def _cve_table(cves):
    if not cves:
        st.markdown('<p style="color:#424d72;font-size:13px">No data available.</p>', unsafe_allow_html=True)
        return
    rows = ""
    for c in cves:
        sev = c.get("severity", "")
        badge = _SEV_BADGE.get(sev, f'<span class="badge-info">{sev}</span>')
        link = c.get("source", "")
        src_html = (f'<a href="{link}" target="_blank" style="color:#7fa8fb;font-size:11px">{link[:40]}…</a>'
                    if link.startswith("http") else f'<span style="color:#424d72;font-size:11.5px">{link}</span>')
        rows += (
            f'<tr>'
            f'<td style="padding:9px 13px;color:var(--text-primary);font-weight:600;vertical-align:top;white-space:nowrap;border-bottom:1px solid var(--tbl-row-border)">{c.get("cve_id","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;white-space:nowrap;border-bottom:1px solid var(--tbl-row-border)">{c.get("date","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{badge}</td>'
            f'<td style="padding:9px 13px;color:var(--text-primary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{c.get("system","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{c.get("description","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{c.get("action","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{src_html}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(239,68,68,0.06);border-bottom:1px solid rgba(239,68,68,0.18)">
        <th style="color:#ef4444;width:10%">CVE ID</th>
        <th style="color:#6b7599;width:8%">Date</th>
        <th style="color:#6b7599;width:8%">Severity</th>
        <th style="color:#6b7599;width:12%">System</th>
        <th style="color:#6b7599;width:28%">Description</th>
        <th style="color:#6b7599;width:22%">Recommended Action</th>
        <th style="color:#6b7599;width:12%">Source</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


def _reg_updates_table(regs, type_filter=None):
    if not regs:
        st.markdown('<p style="color:#424d72;font-size:13px">No data available.</p>', unsafe_allow_html=True)
        return
    filtered = regs
    if type_filter:
        filtered = [r for r in regs if r.get("type", "") in type_filter]
    rows = ""
    for r in filtered:
        rtype = r.get("type", "")
        type_badge = _TYPE_BADGE.get(rtype, f'<span class="badge-info">{rtype}</span>')
        open_until = r.get("open_until", "") or ""
        open_badge = f'&nbsp;<span class="badge-open">Open until {open_until}</span>' if open_until else ""
        link = r.get("link", "") or ""
        title_html = (f'<a href="{link}" target="_blank" style="color:var(--text-primary);text-decoration:underline;text-underline-offset:2px">{r.get("title","")}</a>'
                      if link.startswith("http") else f'<span style="color:var(--text-primary)">{r.get("title","")}</span>')
        rows += (
            f'<tr>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;white-space:nowrap;border-bottom:1px solid var(--tbl-row-border)">{r.get("date","")}</td>'
            f'<td style="padding:9px 13px;color:#7fa8fb;font-weight:500;vertical-align:top;white-space:nowrap;border-bottom:1px solid var(--tbl-row-border)">{r.get("authority","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{type_badge}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{title_html}{open_badge}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("key_impact","")}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(79,126,248,0.07);border-bottom:1px solid rgba(79,126,248,0.18)">
        <th style="color:#7fa8fb;width:8%">Date</th>
        <th style="color:#7fa8fb;width:10%">Authority</th>
        <th style="color:#7fa8fb;width:10%">Type</th>
        <th style="color:#7fa8fb;width:35%">Title</th>
        <th style="color:#7fa8fb;width:37%">Key Impact</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


def _audit_recs_table(recs):
    if not recs:
        st.markdown('<p style="color:#424d72;font-size:13px">No data available.</p>', unsafe_allow_html=True)
        return
    rows = ""
    for r in recs:
        pri = r.get("priority", "")
        badge = _SEV_BADGE.get(pri, _SEV_BADGE.get(f"{pri} Priority", f'<span class="badge-info">{pri}</span>'))
        rows += (
            f'<tr>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;white-space:nowrap;border-bottom:1px solid var(--tbl-row-border)">{r.get("date","")}</td>'
            f'<td style="padding:9px 13px;color:#7fa8fb;font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("source","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-primary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("theme","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("recommendation","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{badge}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(79,126,248,0.07);border-bottom:1px solid rgba(79,126,248,0.18)">
        <th style="color:#7fa8fb;width:8%">Date</th>
        <th style="color:#7fa8fb;width:14%">Source</th>
        <th style="color:#7fa8fb;width:16%">Theme</th>
        <th style="color:#7fa8fb;width:52%">Recommendation</th>
        <th style="color:#7fa8fb;width:10%">Priority</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


def _pub_recs_table(recs):
    if not recs:
        st.markdown('<p style="color:#424d72;font-size:13px">No data available.</p>', unsafe_allow_html=True)
        return
    rows = ""
    for r in recs:
        rows += (
            f'<tr>'
            f'<td style="padding:9px 13px;color:#7fa8fb;font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("source","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;text-align:center;border-bottom:1px solid var(--tbl-row-border)">{r.get("year","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("recommendation","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("applicability","")}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(79,126,248,0.07);border-bottom:1px solid rgba(79,126,248,0.18)">
        <th style="color:#7fa8fb;width:16%">Source</th>
        <th style="color:#7fa8fb;width:7%;text-align:center">Year</th>
        <th style="color:#7fa8fb;width:46%">Recommendation</th>
        <th style="color:#7fa8fb;width:31%">Applicability to Private Banking</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


def _risk_table(risks):
    if not risks:
        return
    for level in ["Critical", "High", "Moderate"]:
        bucket = [r for r in risks if r.get("level") == level]
        if not bucket:
            continue
        col, bg, border = _LEVEL_STYLE.get(level, ("#6b7280", "rgba(107,114,128,0.08)", "rgba(107,114,128,0.2)"))
        rows = "".join(
            f'<tr>'
            f'<td style="padding:10px 13px;color:var(--text-primary);font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("name","")}</td>'
            f'<td style="padding:10px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("description","")}</td>'
            f'<td style="padding:10px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("impact","")}</td>'
            f'<td style="padding:10px 13px;color:var(--text-secondary);vertical-align:top;text-align:center;border-bottom:1px solid var(--tbl-row-border)">{r.get("likelihood","")}</td>'
            f'<td style="padding:10px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("control","")}</td>'
            f'</tr>'
            for r in bucket
        )
        st.markdown(f"""
        <div style="margin:1.4rem 0 0.6rem">
          <span style="background:{bg};border:1px solid {border};color:{col};
                       border-radius:5px;padding:4px 14px;font-size:12px;font-weight:700">{level}</span>
        </div>
        <table class="data-table" style="margin-bottom:1.2rem">
          <thead><tr style="background:{bg};border-bottom:1px solid {border}">
            <th style="color:{col};width:18%">Risk</th>
            <th style="color:#6b7599;width:26%">Description</th>
            <th style="color:#6b7599;width:20%">Impact</th>
            <th style="color:#6b7599;width:12%;text-align:center">Likelihood</th>
            <th style="color:#6b7599;width:24%">Expected Control</th>
          </tr></thead>
          <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)


def _reg_table(regs):
    if not regs:
        return
    rows = "".join(
        f'<tr>'
        f'<td style="padding:10px 13px;color:#7fa8fb;font-weight:500;vertical-align:top;white-space:nowrap;border-bottom:1px solid var(--tbl-row-border)">{r.get("jurisdiction","")}</td>'
        f'<td style="padding:10px 13px;color:var(--text-primary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("text","")}</td>'
        f'<td style="padding:10px 13px;color:var(--text-secondary);vertical-align:top;font-size:11.5px;border-bottom:1px solid var(--tbl-row-border)">{r.get("reference","")}</td>'
        f'<td style="padding:10px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("requirement","")}</td>'
        f'</tr>'
        for r in regs
    )
    st.markdown(f"""
    <table class="data-table">
      <thead><tr style="background:rgba(79,126,248,0.08);border-bottom:1px solid rgba(79,126,248,0.2)">
        <th style="color:#7fa8fb;width:15%">Jurisdiction</th>
        <th style="color:#7fa8fb;width:22%">Regulation</th>
        <th style="color:#7fa8fb;width:16%">Reference</th>
        <th style="color:#7fa8fb;width:47%">Key Requirement</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


def _tests_table(tests):
    if not tests:
        return
    rows = "".join(
        f'<tr>'
        f'<td style="padding:9px 10px;color:#7fa8fb;font-weight:600;text-align:center;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("num","")}</td>'
        f'<td style="padding:9px 10px;color:var(--text-primary);font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("objective","")}</td>'
        f'<td style="padding:9px 10px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("procedure","")}</td>'
        f'<td style="padding:9px 10px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("population","")}</td>'
        f'<td style="padding:9px 10px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("sample_size","")}</td>'
        f'<td style="padding:9px 10px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("failure_criteria","")}</td>'
        f'</tr>'
        for t in tests
    )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(79,126,248,0.08);border-bottom:1px solid rgba(79,126,248,0.2)">
        <th style="color:#7fa8fb;width:4%;text-align:center">No.</th>
        <th style="color:#7fa8fb;width:16%">Objective</th>
        <th style="color:#7fa8fb;width:27%">Procedure</th>
        <th style="color:#7fa8fb;width:14%">Population</th>
        <th style="color:#7fa8fb;width:12%">Sample Size</th>
        <th style="color:#7fa8fb;width:27%">Failure Criteria</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


def _analytics_table(scenarios):
    if not scenarios:
        return
    rows = "".join(
        f'<tr>'
        f'<td style="padding:9px 13px;color:var(--text-primary);font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{s.get("scenario","")}</td>'
        f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{s.get("objective","")}</td>'
        f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{s.get("data_source","")}</td>'
        f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{s.get("analysis_type","")}</td>'
        f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{s.get("anomaly","")}</td>'
        f'</tr>'
        for s in scenarios
    )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(79,126,248,0.08);border-bottom:1px solid rgba(79,126,248,0.2)">
        <th style="color:#7fa8fb;width:18%">Scenario</th>
        <th style="color:#7fa8fb;width:20%">Objective</th>
        <th style="color:#7fa8fb;width:18%">Data Source</th>
        <th style="color:#7fa8fb;width:16%">Analysis Type</th>
        <th style="color:#7fa8fb;width:28%">Anomaly Detected</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Theme toggle
    _theme_lbl = "☀️ Light mode" if _is_dark else "🌙 Dark mode"
    if st.button(_theme_lbl, key="theme_toggle"):
        st.session_state.theme = "light" if _is_dark else "dark"
        st.rerun()

    st.markdown("---")

    # Current audit summary
    st.markdown(f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--sidebar-header-color);margin-bottom:8px">Current Audit</div>', unsafe_allow_html=True)

    if st.session_state.t1_topic:
        st.markdown(f'<div style="font-size:13px;font-weight:600;color:var(--text-primary);margin-bottom:4px">{st.session_state.t1_topic}</div>', unsafe_allow_html=True)
        if st.session_state.t1_jurs:
            jurs_short = " · ".join(j.split(" / ")[0] for j in st.session_state.t1_jurs)
            st.markdown(f'<div style="font-size:11.5px;color:var(--text-muted);margin-bottom:10px">{jurs_short}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:12.5px;color:var(--text-muted);margin-bottom:10px">No analysis yet.</div>', unsafe_allow_html=True)

    # Status per tab
    def _status_icon(done):
        return "✅" if done else "⬜"

    t1_done = bool(st.session_state.t1_risks or st.session_state.t1_regs)
    t2_done = bool(st.session_state.t2_rationale)
    t3_done = bool(st.session_state.t3_report)

    st.markdown(
        f'<div style="font-size:12.5px;color:var(--text-secondary);line-height:2">'
        f'{_status_icon(t1_done)} Risk Analysis<br>'
        f'{_status_icon(t2_done)} Audit Plan<br>'
        f'{_status_icon(t3_done)} Audit Report'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Recent analyses history
    if st.session_state.history:
        st.markdown(f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--sidebar-header-color);margin-bottom:8px">📁 Recent Analyses</div>', unsafe_allow_html=True)
        for i, h in enumerate(st.session_state.history):
            n_c = h.get("n_critical", 0)
            n_h = h.get("n_high", 0)
            risk_str = f"{n_c}C {n_h}H" if (n_c or n_h) else ""
            btn_lbl = f"{h['topic'][:22]}{'…' if len(h['topic'])>22 else ''}"
            if st.button(btn_lbl, key=f"hist_load_{i}"):
                # Reload topic + jurs into session state for Tab 1
                st.session_state["t1_topic_in"] = h["topic"]
                st.session_state["t1_jurs_in"] = h["jurs"]
                st.rerun()
            ts_line = f"{h['timestamp']}"
            if risk_str:
                ts_line += f" · {risk_str}"
            st.markdown(f'<div style="font-size:10.5px;color:var(--text-muted);margin:-4px 0 6px 4px">{ts_line}</div>', unsafe_allow_html=True)

    # ── Reference Data search ─────────────────────────────────────────────────
    st.markdown("---")
    ref_open = st.checkbox("📚 Reference Data", key="ref_data_open")
    if ref_open:
        st.markdown(f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--sidebar-header-color);margin-bottom:6px">Global Search</div>', unsafe_allow_html=True)
        ref_q = st.text_input("Search", placeholder="e.g. GDPR, AML, cyber, FINMA…", key="ref_search_q", label_visibility="collapsed")
        if ref_q:
            q = ref_q.lower()
            hits = []
            for theme, risks in RISK_INDICATORS.items():
                for r in risks:
                    if q in (r.get("title", "") + r.get("description", "")).lower():
                        hits.append(f'🔴 **Risk** `{theme}` — {r["title"]}')
            for r in PUBLIC_AUDIT_RECOMMENDATIONS:
                if q in (r.get("source", "") + r.get("recommendation", "")).lower():
                    hits.append(f'📋 **Rec** `{r.get("theme", "")}` — {r.get("source", "")} ({r.get("year", "")})')
            for jur, regs in REGULATORY_FRAMEWORKS.items():
                for r in regs:
                    if q in (r.get("title", "") + r.get("reference", "") + " ".join(r.get("applies_to", []))).lower():
                        hits.append(f'📜 **Reg** `{jur}` — {r.get("reference", "")} {r.get("title", "")[:40]}')
            for c in CVE_BANKING:
                if q in (c.get("cve_id", "") + c.get("system_affected", "") + c.get("description", "")).lower():
                    hits.append(f'⚠️ **CVE** {c.get("cve_id", "")} — {c.get("system_affected", "")}')
            for theme, scenarios in DATA_ANALYTICS_SCENARIOS.items():
                for s in scenarios:
                    if q in (s.get("title", "") + s.get("objective", "")).lower():
                        hits.append(f'📊 **DA** `{theme}` — {s.get("id", "")} {s.get("title", "")[:40]}')
            if hits:
                st.markdown(f'<div style="font-size:10.5px;color:var(--text-muted);margin-bottom:5px">{len(hits)} result(s)</div>', unsafe_allow_html=True)
                for h in hits[:25]:
                    st.markdown(f'<div style="font-size:11.5px;color:var(--text-secondary);padding:3px 0;border-bottom:1px solid var(--border-divider);line-height:1.5">{h}</div>', unsafe_allow_html=True)
                if len(hits) > 25:
                    st.markdown(f'<div style="font-size:10.5px;color:var(--text-muted);margin-top:4px">…and {len(hits) - 25} more</div>', unsafe_allow_html=True)
            else:
                st.caption("No matches found.")


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:14px;padding:1.2rem 0 1.8rem">
  <span style="font-size:28px">🏦</span>
  <div>
    <div style="font-size:20px;font-weight:700;color:var(--text-primary);letter-spacing:-0.4px">AuditIQ</div>
    <div style="font-size:11.5px;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;margin-top:2px">
      Internal Audit System · Private Banking · Multi-Jurisdiction
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if not _api_key:
    st.error("Access not configured. Please contact your administrator.")
    st.stop()
if not _READY:
    st.error(f"Required modules unavailable: {_ERR}")
    st.stop()

# ── Progress bar ──────────────────────────────────────────────────────────────
_build_progress_bar()

# ═════════════════════════════════════════════════════════════════════════════
# TABS
# ═════════════════════════════════════════════════════════════════════════════
tab0, tab1, tab2, tab3 = st.tabs([
    "🌐  Intelligence Dashboard",
    "🔍  Risk Analysis",
    "📋  Audit Plan",
    "📄  Audit Report",
])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 0 — INTELLIGENCE DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
with tab0:
    # Source selector
    _src_c1, _src_c2, _ = st.columns([1.3, 1.5, 4])
    _t0_static = st.session_state.dash_source == "static"
    if _src_c1.button("📚 Static Reference", key="dash_src_static",
                      type="primary" if _t0_static else "secondary"):
        st.session_state.dash_source = "static"
        st.rerun()
    if _src_c2.button("🌐 Live Intelligence", key="dash_src_live",
                      type="primary" if not _t0_static else "secondary"):
        st.session_state.dash_source = "live"
        st.rerun()

    st.markdown("<div style='margin-top:0.4rem'></div>", unsafe_allow_html=True)

    refresh = False  # only set inside the live branch below

    if st.session_state.dash_source == "static":
        # ── Static reference data (zero API calls) ────────────────────────────
        _static_label()
        st.markdown("<div style='margin-top:0.6rem'></div>", unsafe_allow_html=True)

        _sev_opts = ["All", "Critical", "High"]
        _jur_opts = ["All"] + list(REGULATORY_FRAMEWORKS.keys())

        # A) CVEs
        st.markdown("---")
        st.markdown(
            f'<div class="section-title">A. Banking CVE Reference'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{len(CVE_BANKING)} entries · 2021-2024</span></div>',
            unsafe_allow_html=True,
        )
        _cve_sc1, _cve_sc2, _cve_sc3 = st.columns([3, 1.2, 1.2])
        _cve_sq = _cve_sc1.text_input("Search CVEs", placeholder="Filter CVEs…", key="_cve_sq", label_visibility="collapsed")
        _cve_ssev = _cve_sc2.selectbox("Severity", _sev_opts, key="_cve_ssev", label_visibility="collapsed")
        _show_cve_static(search=_cve_sq, sev_filter=_cve_ssev)

        # B) Regulatory frameworks
        st.markdown("---")
        _total_regs = sum(len(v) for v in REGULATORY_FRAMEWORKS.values())
        st.markdown(
            f'<div class="section-title">B. Regulatory Frameworks Reference'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{_total_regs} texts · CH · EU · UK · SG · HK · Bahamas · International</span></div>',
            unsafe_allow_html=True,
        )
        _reg_sc1, _reg_sc2, _reg_sc3 = st.columns([3, 2, 1])
        _reg_sq = _reg_sc1.text_input("Search frameworks", placeholder="Filter frameworks…", key="_reg_sq", label_visibility="collapsed")
        _reg_sjur = _reg_sc2.selectbox("Jurisdiction", _jur_opts, key="_reg_sjur", label_visibility="collapsed")
        _show_regulatory_frameworks(jur_filter=_reg_sjur, search=_reg_sq)

        # C) Public audit recommendations
        st.markdown("---")
        _all_themes = list(dict.fromkeys(r.get("theme", "") for r in PUBLIC_AUDIT_RECOMMENDATIONS))
        st.markdown(
            f'<div class="section-title">C. Public Audit Recommendations'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{len(PUBLIC_AUDIT_RECOMMENDATIONS)} entries · FATF · FINMA · MAS · FCA · EBA · Basel · IIA · IMF</span></div>',
            unsafe_allow_html=True,
        )
        _rec_sc1, _rec_sc2 = st.columns([3, 2])
        _rec_sq = _rec_sc1.text_input("Search recommendations", placeholder="Filter recommendations…", key="_rec_sq", label_visibility="collapsed")
        _rec_stheme = _rec_sc2.selectbox("Theme", ["All"] + _all_themes, key="_rec_stheme", label_visibility="collapsed")
        for _t in (_all_themes if _rec_stheme == "All" else [_rec_stheme]):
            if _rec_stheme == "All":
                st.markdown(f'<div style="font-size:12px;font-weight:600;color:#7fa8fb;margin:10px 0 4px">{_t}</div>', unsafe_allow_html=True)
            _show_pub_recs(theme=_t, search=_rec_sq)

        st.markdown("<div class='no-print' style='margin-top:1rem'>", unsafe_allow_html=True)
        _print_button()
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # ── Live intelligence ─────────────────────────────────────────────────
        hcol1, hcol2 = st.columns([5, 1])
        with hcol1:
            st.markdown('<p style="color:#5a6488;font-size:13.5px;margin:0 0 0.4rem">Live intelligence feed: CVEs, regulatory updates, and public audit recommendations.</p>', unsafe_allow_html=True)
            if st.session_state.dash_updated:
                st.markdown(f'<p style="color:#2d3655;font-size:12px;margin:0">Last updated: {st.session_state.dash_updated}</p>', unsafe_allow_html=True)
        with hcol2:
            refresh = st.button("Refresh Dashboard", key="dash_refresh")

    st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)

    run_dash = (st.session_state.dash_source == "live") and (
        refresh or (
            st.session_state.dash_cves is None and
            st.session_state.dash_regs is None and
            st.session_state.dash_audit_recs is None
        )
    )

    if run_dash:
        with st.spinner("Fetching latest intelligence…"):
            try:
                c = _client()
                sys_dash = (
                    "You are a financial sector intelligence analyst. "
                    "Search the web for real, current information. "
                    "Return ONLY valid JSON arrays — no markdown, no preamble, no commentary. "
                    "Include only real entries found via search. "
                    "If nothing is found for a field, use an empty string."
                )

                cves_raw = _web_search_call(c,
                    "Search NVD (nvd.nist.gov), CISA KEV (cisa.gov/known-exploited-vulnerabilities), "
                    "and vendor security advisories for CVEs published in the last 3 months targeting financial sector systems: "
                    "core banking platforms, SWIFT/messaging, trading systems, IAM/PAM, payment gateways, ATM software, banking APIs. "
                    "Include only High and Critical severity CVEs. "
                    "Return a JSON array of 8-12 real CVEs found:\n"
                    '[{"cve_id":"CVE-XXXX-XXXXX","date":"YYYY-MM-DD","severity":"Critical|High",'
                    '"system":"<affected system>","description":"<1-2 sentences>","action":"<recommended action>","source":"<URL or NVD/CISA/vendor>"}]',
                    system=sys_dash, max_tokens=5000)

                regs_raw = _web_search_call(c,
                    "Search the official websites and press releases of FINMA, MAS, SFC, HKMA, EBA, FCA, PRA, BCBS, FSB, FATF "
                    "for regulatory publications from the last 6 months AND upcoming consultations/rules open or expected in the next 12 months. "
                    "Focus on banking, AML, capital requirements, operational resilience, digital assets, wealth management. "
                    "Return a JSON array of 12-16 real entries found:\n"
                    '[{"date":"YYYY-MM-DD","authority":"<regulator>","type":"Consultation|Final Rule|Circular|Guidance",'
                    '"title":"<full publication title>","key_impact":"<1-2 sentences on impact for private banks>",'
                    '"link":"<URL if found, else empty>","open_until":"<consultation deadline YYYY-MM-DD if applicable, else null>"}]',
                    system=sys_dash, max_tokens=6000)

                recs_raw = _web_search_call(c,
                    "Search for public audit recommendations and reports published in the last 12 months targeting banks and wealth managers, from: "
                    "Basel Committee on Banking Supervision, IMF Financial Sector Assessment Programs (FSAPs), "
                    "Big 4 thought leadership reports (publicly available), IIA Global, FINMA, MAS, FCA, EBA supervisory reports. "
                    "Focus on private banking, wealth management, HNWI, cross-border. "
                    "Return a JSON array of 8-12 real entries:\n"
                    '[{"date":"YYYY-MM-DD","source":"<issuing body>","theme":"<topic area>",'
                    '"recommendation":"<recommendation summary, 2-3 sentences>","priority":"High|Medium"}]',
                    system=sys_dash, max_tokens=5000)

                st.session_state.dash_cves       = _parse_json(cves_raw) or []
                st.session_state.dash_regs       = _parse_json(regs_raw) or []
                st.session_state.dash_audit_recs = _parse_json(recs_raw) or []
                st.session_state.dash_updated    = datetime.now().strftime("%d %b %Y, %H:%M UTC")

            except Exception:
                st.error("An error occurred while fetching intelligence data. Please try again.")

    if st.session_state.dash_source == "live" and st.session_state.dash_cves is not None:
        # A) CVEs
        st.markdown("---")
        n_cve = len(st.session_state.dash_cves or [])
        crit_count = sum(1 for c in (st.session_state.dash_cves or []) if c.get("severity") == "Critical")
        crit_badge = f' &nbsp;<span class="badge-critical">{crit_count} Critical</span>' if crit_count else ""
        st.markdown(
            f'<div class="section-title">A. Latest CVEs — Financial Sector'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{n_cve} entries · High & Critical · last 3 months</span>'
            f'{crit_badge}</div>',
            unsafe_allow_html=True,
        )
        filtered_cves = _filter_data(
            st.session_state.dash_cves or [],
            ["cve_id", "system", "description", "action"],
            "dash_cves",
            level_field="severity",
        )
        _cve_table(filtered_cves)

        # B) Regulatory updates
        st.markdown("---")
        n_reg = len(st.session_state.dash_regs or [])
        all_types = sorted({r.get("type", "") for r in (st.session_state.dash_regs or []) if r.get("type")})
        st.markdown(
            f'<div class="section-title">B. Regulatory Updates'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{n_reg} publications · FINMA · MAS · SFC · HKMA · EBA · FCA · PRA · BCBS · FSB · FATF</span></div>',
            unsafe_allow_html=True,
        )
        filtered_regs = _filter_data(
            st.session_state.dash_regs or [],
            ["authority", "title", "key_impact"],
            "dash_regs",
            level_field="type",
        )
        _reg_updates_table(filtered_regs)

        # C) Audit recommendations
        st.markdown("---")
        n_rec = len(st.session_state.dash_audit_recs or [])
        st.markdown(
            f'<div class="section-title">C. Latest Public Audit Recommendations — Banking'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{n_rec} entries · last 12 months</span></div>',
            unsafe_allow_html=True,
        )
        filtered_arecs = _filter_data(
            st.session_state.dash_audit_recs or [],
            ["source", "theme", "recommendation"],
            "dash_arecs",
            level_field="priority",
        )
        _audit_recs_table(filtered_arecs)

        st.markdown("<div class='no-print' style='margin-top:1rem'>", unsafe_allow_html=True)
        _print_button()
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — RISK ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<p style="color:#5a6488;font-size:13.5px;margin:0 0 0.8rem">Risk mapping, applicable regulations, and public audit recommendations by topic.</p>', unsafe_allow_html=True)
    _mode_toggle("t1_mode")
    st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)

    # Quick Start Template
    tpl_name = st.selectbox(
        "Quick Start Template",
        options=list(TEMPLATES.keys()),
        key="t1_tpl_select",
        help="Pre-fill topic, jurisdictions and scope with a predefined audit template.",
    )
    if tpl_name != "— Select a template —" and tpl_name != st.session_state._tpl_name:
        tpl = TEMPLATES[tpl_name]
        st.session_state["t1_topic_in"] = tpl.get("topic", "")
        st.session_state["t1_jurs_in"]  = tpl.get("jurisdictions", JURISDICTIONS[:4])
        st.session_state._tpl_name = tpl_name
        st.session_state._tpl_scope = tpl.get("scope", "")
        st.rerun()

    _tpl_scope_default = st.session_state.get("_tpl_scope", "")

    audit_topic = st.text_input(
        "Audit Topic",
        placeholder="e.g. AML/KYC, Credit Risk, Cybersecurity, Operational Risk…",
        key="t1_topic_in",
        help="Enter the main audit topic or domain to analyze (e.g. 'AML/KYC', 'Cyber Risk'). Must be at least 3 characters.",
    )
    jurisdictions = st.multiselect(
        "Jurisdictions",
        options=JURISDICTIONS,
        default=st.session_state.get("t1_jurs_in") or JURISDICTIONS[:4],
        key="t1_jurs_in",
        help="Select one or more jurisdictions. Each adds regulatory and risk context specific to that regulator.",
    )

    st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

    # Input validation
    _t1_valid = True
    if audit_topic and len(audit_topic.strip()) < 3:
        st.warning("⚠ Audit topic must be at least 3 characters. Try: 'AML/KYC', 'Credit Risk', or 'Cybersecurity'.")
        _t1_valid = False
    if not jurisdictions:
        st.warning("⚠ Please select at least one jurisdiction.")
        _t1_valid = False

    if st.session_state.t1_mode == "static":
        # ── Static Reference Data mode ─────────────────────────────────────────
        _static_label()
        _t1_theme = _topic_to_theme(audit_topic) if audit_topic else "AML_KYC"
        _t1_theme = _t1_theme or "AML_KYC"
        _t1_theme_label = _t1_theme.replace("_", " ").title()

        # A) Risk Indicators
        st.markdown("---")
        st.markdown(
            f'<div class="section-title">A. Risk Indicators — {_t1_theme_label}'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">'
            f'{len(RISK_INDICATORS.get(_t1_theme, []))} risks in library</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(_EXAMPLE_RISK, unsafe_allow_html=True)
        _ri_c1, _ri_c2 = st.columns([3, 1.5])
        _ri_sq = _ri_c1.text_input("Search risks", placeholder="Filter risks…", key="_ri_sq", label_visibility="collapsed")
        _ri_slv = _ri_c2.selectbox("Level", ["All", "Critical", "High", "Moderate"], key="_ri_slv", label_visibility="collapsed")
        _ri_filtered = RISK_INDICATORS.get(_t1_theme, [])
        if _ri_slv != "All":
            _ri_filtered = [r for r in _ri_filtered if r.get("level") == _ri_slv]
        if _ri_sq:
            _qr = _ri_sq.lower()
            _ri_filtered = [r for r in _ri_filtered if _qr in (r.get("title","") + r.get("description","")).lower()]
        if _ri_filtered:
            _LVLC = {"Critical": "#ef4444", "High": "#f97316", "Moderate": "#eab308"}
            _LVLBG = {"Critical": "rgba(239,68,68,0.08)", "High": "rgba(249,115,22,0.08)", "Moderate": "rgba(234,179,8,0.06)"}
            for _r in _ri_filtered:
                _col = _LVLC.get(_r["level"], "#8392bb")
                _bg  = _LVLBG.get(_r["level"], "transparent")
                _pcolor = {"High": "#ef4444", "Medium": "#eab308", "Low": "#22d3a5"}.get(_r.get("probability",""), "#8392bb")
                _icolor = {"High": "#ef4444", "Medium": "#eab308", "Low": "#22d3a5"}.get(_r.get("impact",""), "#8392bb")
                _ctrls = "".join(f"<li>{c}</li>" for c in _r.get("expected_controls", []))
                _flags = "".join(f"<li>{f}</li>" for f in _r.get("red_flags", []))
                st.markdown(f"""
                <div style="border:1px solid {_col}33;border-radius:9px;padding:14px 18px;margin-bottom:12px;background:{_bg}">
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
                    <span style="background:{_col}22;color:{_col};border:1px solid {_col}44;border-radius:4px;padding:2px 9px;font-size:11px;font-weight:700">{_r["level"]}</span>
                    <span style="font-size:13.5px;font-weight:600;color:var(--text-primary)">{_r.get("id","")} — {_r["title"]}</span>
                    <span style="margin-left:auto;font-size:11px;color:var(--text-muted)">Prob: <span style="color:{_pcolor};font-weight:600">{_r.get("probability","")}</span> &nbsp;·&nbsp; Impact: <span style="color:{_icolor};font-weight:600">{_r.get("impact","")}</span></span>
                  </div>
                  <p style="font-size:12.5px;color:var(--text-secondary);margin:0 0 10px;line-height:1.7">{_r["description"]}</p>
                  <details>
                    <summary style="font-size:12px;color:#7fa8fb;cursor:pointer;font-weight:500">Controls &amp; Red Flags</summary>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:8px">
                      <div><div style="font-size:11px;font-weight:600;color:var(--text-muted);margin-bottom:4px">EXPECTED CONTROLS</div>
                      <ul style="margin:0;padding-left:16px;font-size:12px;color:var(--text-secondary);line-height:1.8">{_ctrls}</ul></div>
                      <div><div style="font-size:11px;font-weight:600;color:#ef4444aa;margin-bottom:4px">RED FLAGS</div>
                      <ul style="margin:0;padding-left:16px;font-size:12px;color:var(--text-secondary);line-height:1.8">{_flags}</ul></div>
                    </div>
                    <div style="margin-top:10px;font-size:11.5px;color:var(--text-muted);font-style:italic">🏦 {_r.get("private_banking_specifics","")}</div>
                  </details>
                </div>""", unsafe_allow_html=True)
        else:
            st.caption("No risks match the filter.")

        # B) Public Audit Recommendations
        st.markdown("---")
        _all_rec_sources = sorted({r.get("source","") for r in PUBLIC_AUDIT_RECOMMENDATIONS if r.get("source")})
        st.markdown(
            f'<div class="section-title">B. Public Audit Recommendations — {_t1_theme_label}'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">'
            f'{len([r for r in PUBLIC_AUDIT_RECOMMENDATIONS if r.get("theme") == _t1_theme])} entries</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(_EXAMPLE_PUB_REC, unsafe_allow_html=True)
        _pr_c1, _pr_c2 = st.columns([3, 2])
        _pr_sq = _pr_c1.text_input("Search recommendations", placeholder="Filter…", key="_pr_sq", label_visibility="collapsed")
        _pr_ssrc = _pr_c2.selectbox("Source", ["All"] + _all_rec_sources, key="_pr_ssrc", label_visibility="collapsed")
        _show_pub_recs(_t1_theme, search=_pr_sq)

        st.markdown("<div class='no-print' style='margin-top:1rem'>", unsafe_allow_html=True)
        _print_button()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.t1_mode == "live":
        if st.button("Analyze", type="primary", disabled=_disabled or not audit_topic or not _t1_valid, key="t1_run"):
            with st.spinner("Analyzing…"):
                try:
                    c = _client()
                    jur_str = ", ".join(jurisdictions) if jurisdictions else "all jurisdictions"

                    risks_raw = _call(c, f"""Audit topic: {audit_topic}
Jurisdictions: {jur_str}
Institution: Swiss private bank and asset manager (HNWI, wealth management, cross-border)

Identify 10-12 key risks for this audit topic across 3 severity levels.
Respond ONLY with a valid JSON array — no markdown, no preamble:
[{{"level":"Critical|High|Moderate","name":"<5-8 words>","description":"<2-3 sentences>","impact":"<1-2 sentences, quantified where possible>","likelihood":"High|Medium|Low","control":"<1-2 sentences on expected control mechanism>"}}]""",
                        max_tokens=5000)

                    regs_raw = _call(c, f"""Audit topic: {audit_topic}
Jurisdictions: {jur_str}
Institution: Swiss private bank / wealth manager (HNWI, wealth management, cross-border)

List applicable regulations specific to private banking and wealth management.
Respond ONLY with a valid JSON array — 12-18 entries, no markdown:
[{{"jurisdiction":"<e.g. CH / FINMA>","text":"<law or regulation name>","reference":"<specific article/circular number>","requirement":"<key requirement in 1-2 sentences>"}}]""",
                        max_tokens=5000)

                    pub_recs_raw = _web_search_call(c,
                        f"Search for public audit recommendations and supervisory findings specifically about '{audit_topic}' "
                        f"in private banking and wealth management, from the last 3 years. "
                        f"Sources: Basel Committee, IMF FSAPs, Big 4 public reports, IIA, FINMA, MAS, FCA, EBA, FATF. "
                        f"Return a JSON array of 6-10 real entries found:\n"
                        f'[{{"source":"<issuing body>","year":"YYYY","recommendation":"<recommendation summary, 2-3 sentences>","applicability":"<how it applies to private banks>"}}]',
                        system="You are a financial sector audit intelligence analyst. Search the web for real published information. Return ONLY a valid JSON array. No markdown, no commentary.",
                        max_tokens=4000)

                    st.session_state.t1_risks    = _parse_json(risks_raw)
                    st.session_state.t1_regs     = _parse_json(regs_raw)
                    st.session_state.t1_pub_recs = _parse_json(pub_recs_raw) or []
                    st.session_state.t1_topic    = audit_topic
                    st.session_state.t1_jurs     = jurisdictions

                    _save_history(audit_topic, jurisdictions, st.session_state.t1_risks, st.session_state.t1_regs, st.session_state.t1_pub_recs)

                    def _h1(name, inp):
                        if name == "save_regulatory_framework":
                            try:
                                p = generate_regulatory_framework_docx(inp, OUTPUT_DIR)
                                return f"Saved: {p}", {"docx_path": p}
                            except Exception as ex:
                                return f"Error: {ex}", {}
                        return "Unknown tool", {}

                    _, extra = _agentic_loop(c, _a1.SYSTEM_PROMPT, _a1.TOOLS,
                        [{"role": "user", "content": [{"type": "text", "text": (
                            f"Generate a comprehensive regulatory framework report.\n\n"
                            f"Audit Topic: {audit_topic}\n"
                            f"Institution: Swiss private bank / wealth manager (HNWI, cross-border)\n"
                            f"Jurisdictions: {jur_str}\n\n"
                            f"Cover: identified risks, applicable regulations, cross-jurisdictional analysis. "
                            f"Then call save_regulatory_framework to export."
                        )}]}], _h1)

                    if "docx_path" in extra and Path(extra["docx_path"]).exists():
                        st.session_state.t1_docx = Path(extra["docx_path"]).read_bytes()

                except Exception:
                    st.error("An error occurred. Please try again.")

    # Results (live mode only)
    if st.session_state.t1_mode == "live" and (st.session_state.t1_risks or st.session_state.t1_regs):
        topic_lbl = st.session_state.t1_topic or "audit"
        st.markdown("---")

        # Risk Score Dashboard
        st.markdown('<div class="section-title">Risk Score</div>', unsafe_allow_html=True)
        _risk_score_display(st.session_state.t1_risks, len(st.session_state.t1_jurs or []))

        st.markdown("---")
        st.markdown('<div class="section-title">A. Risk Mapping</div>', unsafe_allow_html=True)

        filtered_risks = _filter_data(
            st.session_state.t1_risks or [],
            ["name", "description", "impact", "control"],
            "t1_risks",
            level_field="level",
        )
        _risk_table(filtered_risks)

        col_copy_a, _ = st.columns([1, 5])
        with col_copy_a:
            _copy_button(
                json.dumps(st.session_state.t1_risks or [], indent=2),
                "t1_risks_copy"
            )

        st.markdown("---")
        st.markdown('<div class="section-title">B. Applicable Regulations</div>', unsafe_allow_html=True)

        filtered_t1_regs = _filter_data(
            st.session_state.t1_regs or [],
            ["jurisdiction", "text", "reference", "requirement"],
            "t1_regs",
            jur_field="jurisdiction",
        )
        _reg_table(filtered_t1_regs)

        col_copy_b, _ = st.columns([1, 5])
        with col_copy_b:
            _copy_button(
                json.dumps(st.session_state.t1_regs or [], indent=2),
                "t1_regs_copy"
            )

        st.markdown("---")
        n_pub = len(st.session_state.t1_pub_recs or [])
        st.markdown(
            f'<div class="section-title">C. Public Audit Recommendations — {topic_lbl}'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{n_pub} entries found</span></div>',
            unsafe_allow_html=True,
        )

        filtered_pub = _filter_data(
            st.session_state.t1_pub_recs or [],
            ["source", "recommendation", "applicability"],
            "t1_pub_recs",
        )
        _pub_recs_table(filtered_pub)

        col_copy_c, _ = st.columns([1, 5])
        with col_copy_c:
            _copy_button(
                json.dumps(st.session_state.t1_pub_recs or [], indent=2),
                "t1_pub_copy"
            )

        if st.session_state.t1_docx:
            st.markdown("---")
            dl_col, print_col = st.columns([2, 1])
            with dl_col:
                st.download_button(
                    "⬇  Download Full Analysis (.docx)",
                    data=st.session_state.t1_docx,
                    file_name=f"Risk_Analysis_{topic_lbl.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            with print_col:
                _print_button()
        else:
            st.markdown("<div style='margin-top:1rem'>", unsafe_allow_html=True)
            _print_button()
            st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — AUDIT PLAN
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<p style="color:#5a6488;font-size:13.5px;margin:0 0 0.8rem">Structured audit planning, test programme, and data analytics scenarios.</p>', unsafe_allow_html=True)
    _mode_toggle("t2_mode")
    st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)

    if st.session_state.t1_topic:
        st.markdown(f'<div class="ctx-pill">✓ Topic: {st.session_state.t1_topic}</div>', unsafe_allow_html=True)

    topic2 = st.text_input(
        "Audit Topic",
        value=st.session_state.t1_topic or "",
        placeholder="e.g. AML/KYC, Credit Risk, Cybersecurity…",
        key="t2_topic_in",
    )

    scope = st.text_area(
        "Audit Scope",
        value=st.session_state.get("_tpl_scope", ""),
        placeholder="e.g. All group entities in CH, SG and HK. Focus on client onboarding and transaction monitoring.",
        height=80,
        key="t2_scope_in",
        help="Define the perimeter of the audit: entities, geographies, processes, and systems in scope.",
    )

    uploads2 = st.file_uploader(
        "Supporting documents (optional — PDF, Word, Excel, TXT)",
        type=["pdf", "docx", "xlsx", "txt"], accept_multiple_files=True, key="t2_upload",
    )

    st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

    # Input validation
    _t2_valid = True
    if topic2 and not scope.strip():
        st.warning("⚠ Please define the audit scope before generating the plan.")
        _t2_valid = False

    if st.session_state.t2_mode == "static":
        # ── Static Reference Data mode ─────────────────────────────────────────
        _static_label()
        _t2_theme = _topic_to_theme(topic2) if topic2 else "CYBER_RISK"
        _t2_theme = _t2_theme or "CYBER_RISK"
        _t2_theme_label = _t2_theme.replace("_", " ").title()
        _n_tests = len(AUDIT_TESTS_LIBRARY.get(_t2_theme, []))
        _n_da = len(DATA_ANALYTICS_SCENARIOS.get(_t2_theme, []))

        # A) Audit Tests Library
        st.markdown("---")
        st.markdown(
            f'<div class="section-title">A. Audit Tests Library — {_t2_theme_label}'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{_n_tests} tests available for this topic</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(_EXAMPLE_TEST, unsafe_allow_html=True)
        _tl_c1, _tl_c2, _tl_c3 = st.columns([3, 1.5, 1.8])
        _tl_sq = _tl_c1.text_input("Search tests", placeholder="Filter tests…", key="_tl_sq", label_visibility="collapsed")
        _tl_slv = _tl_c2.selectbox("Level", ["All", "Critical", "High", "Moderate"], key="_tl_slv", label_visibility="collapsed")
        _tl_stype = _tl_c3.selectbox("Type", ["All", "Standard", "Data Analytics"], key="_tl_stype", label_visibility="collapsed")
        _show_tests_library(_t2_theme, search=_tl_sq, level_filter=_tl_slv, type_filter=_tl_stype)

        # B) Data Analytics Scenarios
        st.markdown("---")
        st.markdown(
            f'<div class="section-title">B. Data Analytics Scenarios — {_t2_theme_label}'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{_n_da} scenarios</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(_EXAMPLE_DA, unsafe_allow_html=True)
        _da_c1 = st.columns([3])[0]
        _da_sq = _da_c1.text_input("Search scenarios", placeholder="Filter scenarios…", key="_da_sq", label_visibility="collapsed")
        _show_da_scenarios(_t2_theme, search=_da_sq)

        st.markdown("<div class='no-print' style='margin-top:1rem'>", unsafe_allow_html=True)
        _print_button()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.t2_mode == "live":
        if st.button("Generate Plan", type="primary", disabled=_disabled or not topic2 or not _t2_valid, key="t2_run"):
            with st.spinner("Generating…"):
                try:
                    c = _client()
                    jur_str = ", ".join(st.session_state.t1_jurs or JURISDICTIONS[:3])
                    top_risks_str = ""
                    if st.session_state.t1_risks:
                        top = [r["name"] for r in st.session_state.t1_risks if r.get("level") == "Critical"][:4]
                        if top:
                            top_risks_str = f"\nKey critical risks identified: {', '.join(top)}"

                    file_ids2 = []
                    for uf in (uploads2 or []):
                        fm = _upload_sf(c, uf)
                        if fm:
                            file_ids2.append(fm)
                    doc_ctx = f"\n{len(file_ids2)} supporting document(s) provided for context." if file_ids2 else ""

                    sys_prompt = "You are a senior audit partner at a Big 4 firm specialising in private banking. Write in English, professional tone, concise and precise."

                    rationale = _call(c, f"""Audit topic: {topic2}
Institution: Swiss private bank (HNWI, cross-border: {jur_str})
Scope: {scope or "All group entities"}{top_risks_str}{doc_ctx}

Write a concise RATIONALE section (2-3 paragraphs) explaining why this audit is relevant RIGHT NOW.
Cover: current regulatory triggers, recent enforcement actions or industry incidents, emerging risk trends specific to private banking.
Plain prose, no headers. Bold key terms where appropriate.""",
                        system=sys_prompt, max_tokens=2000)

                    background = _call(c, f"""Audit topic: {topic2}
Institution: Swiss private bank (HNWI, cross-border: {jur_str})
Scope: {scope or "All group entities"}{top_risks_str}{doc_ctx}

Write a BACKGROUND INFORMATION section (3-4 paragraphs). Tone: McKinsey/EY — strategic, consultative.
Cover: market context, current state in global wealth management, key challenges for HNWI institutions, regulatory landscape.
Plain prose, no headers. Bold key terms where appropriate.""",
                        system=sys_prompt, max_tokens=2500)

                    org_plan = _call(c, f"""Audit topic: {topic2}
Institution: Swiss private bank (CH, SG, HK, Bahamas, EU, UK)
Scope: {scope or "All entities"}{top_risks_str}{doc_ctx}

Write a structured AUDIT PLAN with three inline sections (use **bold** for section names):

**Organization** — Key business units, governance structure, and stakeholders in scope.

**Activities in Scope** — Business processes, systems, and activities in the audit perimeter.

**Audit Objectives & Methodology** — 3-4 clear objectives. Risk-based, IIA-aligned. Key techniques.

Plain prose per section.""",
                        system=sys_prompt, max_tokens=2500)

                    tests_raw = _call(c, f"""Audit topic: {topic2}
Institution: Swiss private bank ({jur_str})
Scope: {scope or "All entities"}{top_risks_str}

Generate EXACTLY 15 audit test procedures. ONLY valid JSON array, no markdown:
[{{"num":1,"objective":"<1 sentence>","procedure":"<2-3 sentences>","population":"<what is tested>","sample_size":"<method and size>","failure_criteria":"<control failure definition>"}}]""",
                        system=sys_prompt, max_tokens=7000)
                    tests = _parse_json(tests_raw)

                    analytics_raw = _call(c, f"""Audit topic: {topic2}
Institution: Swiss private bank ({jur_str})
Scope: {scope or "All entities"}{top_risks_str}

Generate 6-8 data analytics scenarios. ONLY valid JSON array, no markdown:
[{{"scenario":"<4-6 words>","objective":"<what it verifies>","data_source":"<system or dataset>","analysis_type":"<e.g. Trend analysis, Exception report>","anomaly":"<red flag being detected>"}}]""",
                        system=sys_prompt, max_tokens=4000)
                    analytics = _parse_json(analytics_raw)

                    st.session_state.t2_rationale  = rationale
                    st.session_state.t2_background = background
                    st.session_state.t2_org_plan   = org_plan
                    st.session_state.t2_tests      = tests
                    st.session_state.t2_analytics  = analytics

                    extra_ctx = ""
                    if st.session_state.t1_regs:
                        extra_ctx = f"\n\nREGULATORY CONTEXT:\n{json.dumps(st.session_state.t1_regs, indent=2)[:2000]}"

                    def _h2(name, inp):
                        if name == "generate_audit_plan_ppt":
                            try:
                                p = generate_audit_plan_ppt(inp, OUTPUT_DIR)
                                return f"PPT saved: {p}. Now generate Excel.", {"ppt_path": p}
                            except Exception as ex:
                                return f"Error: {ex}", {}
                        elif name == "generate_audit_procedures_excel":
                            try:
                                p = generate_audit_procedures_excel(inp, OUTPUT_DIR)
                                return f"Excel saved: {p}.", {"excel_path": p}
                            except Exception as ex:
                                return f"Error: {ex}", {}
                        return "Unknown tool", {}

                    _, extra = _agentic_loop(c, _a2.SYSTEM_PROMPT, _a2.TOOLS,
                        [{"role": "user", "content": [{"type": "text", "text": (
                            f"Create an audit plan for: {topic2}\n"
                            f"Institution: Swiss private bank (CH, SG, HK, Bahamas, EU, UK)\n"
                            f"Scope: {scope or 'All entities'}"
                            f"{extra_ctx}\n\n"
                            f"1. Identify 6-10 audit subjects → call generate_audit_plan_ppt.\n"
                            f"2. For each design 4-8 procedures → call generate_audit_procedures_excel."
                        )}]}], _h2)

                    if "ppt_path" in extra and Path(extra["ppt_path"]).exists():
                        st.session_state.t2_pptx = Path(extra["ppt_path"]).read_bytes()
                    if "excel_path" in extra and Path(extra["excel_path"]).exists():
                        st.session_state.t2_xlsx = Path(extra["excel_path"]).read_bytes()

                except Exception:
                    st.error("An error occurred. Please try again.")

    # Results (live mode only)
    if st.session_state.t2_mode == "live" and st.session_state.t2_rationale:
        topic2_lbl = st.session_state.t1_topic or topic2 or "audit"
        st.markdown("---")

        st.markdown('<div class="section-title">1. Rationale</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-box">{st.session_state.t2_rationale}</div>', unsafe_allow_html=True)
        _copy_button(st.session_state.t2_rationale, "t2_rat_copy")

        st.markdown("---")
        st.markdown('<div class="section-title">2. Background Information</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-box">{st.session_state.t2_background}</div>', unsafe_allow_html=True)
        _copy_button(st.session_state.t2_background or "", "t2_bg_copy")

        st.markdown("---")
        st.markdown('<div class="section-title">3. Audit Plan</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-box">{st.session_state.t2_org_plan}</div>', unsafe_allow_html=True)
        _copy_button(st.session_state.t2_org_plan or "", "t2_plan_copy")

        st.markdown("---")
        n_tests = len(st.session_state.t2_tests or [])
        st.markdown(f'<div class="section-title">4. Test List — {n_tests} procedures</div>', unsafe_allow_html=True)
        filtered_tests = _filter_data(
            st.session_state.t2_tests or [],
            ["objective", "procedure", "population", "failure_criteria"],
            "t2_tests",
        )
        _tests_table(filtered_tests)

        st.markdown("---")
        n_analytics = len(st.session_state.t2_analytics or [])
        st.markdown(f'<div class="section-title">5. Data Analytics Scenarios — {n_analytics} scenarios</div>', unsafe_allow_html=True)
        filtered_analytics = _filter_data(
            st.session_state.t2_analytics or [],
            ["scenario", "objective", "data_source", "analysis_type", "anomaly"],
            "t2_analytics",
        )
        _analytics_table(filtered_analytics)

        pptx = st.session_state.t2_pptx
        xlsx = st.session_state.t2_xlsx
        if pptx or xlsx:
            st.markdown("---")
            ca, cb, cc = st.columns([2, 2, 1])
            if pptx:
                ca.download_button(
                    "⬇  Audit Plan (.pptx)", data=pptx,
                    file_name=f"Audit_Plan_{topic2_lbl.replace(' ', '_')}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
            if xlsx:
                cb.download_button(
                    "⬇  Test Programme (.xlsx)", data=xlsx,
                    file_name=f"Audit_Tests_{topic2_lbl.replace(' ', '_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            with cc:
                _print_button()
        else:
            st.markdown("<div style='margin-top:1rem'>", unsafe_allow_html=True)
            _print_button()
            st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — AUDIT REPORT
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<p style="color:#5a6488;font-size:13.5px;margin:0 0 0.8rem">Formal IIA-standard audit report in English.</p>', unsafe_allow_html=True)
    _mode_toggle("t3_mode")
    st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)

    if st.session_state.t3_mode == "static":
        # ── Static Reference Data mode ─────────────────────────────────────────
        _static_label()
        _t3_jurs = st.session_state.get("t1_jurs") or list(REGULATORY_FRAMEWORKS.keys())[:3]

        # Example finding
        st.markdown("---")
        st.markdown('<div class="section-title">📌 Audit Finding Template</div>', unsafe_allow_html=True)
        st.markdown(_EXAMPLE_FINDING, unsafe_allow_html=True)

        # A) IIA Standards
        st.markdown("---")
        st.markdown(
            f'<div class="section-title">A. IIA Standards Reference — 2024'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{len(IIA_STANDARDS_2024)} standards</span></div>',
            unsafe_allow_html=True,
        )
        _iia_sq = st.text_input("Search IIA Standards", placeholder="Filter standards…", key="_iia_sq", label_visibility="collapsed")
        _iia_filtered = IIA_STANDARDS_2024
        if _iia_sq:
            _qi = _iia_sq.lower()
            _iia_filtered = [s for s in IIA_STANDARDS_2024 if _qi in (s.get("title","") + s.get("description","") + s.get("standard_id","")).lower()]
        for _s in _iia_filtered:
            _reqs = "".join(f"<li>{r}</li>" for r in _s.get("key_requirements", []))
            with st.expander(f"**{_s['standard_id']}** — {_s['title']}"):
                st.markdown(f"""
                <p style="font-size:13px;color:var(--text-secondary);line-height:1.8;margin-bottom:12px">{_s['description']}</p>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
                  <div>
                    <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;color:#7fa8fb;margin-bottom:6px">Key Requirements</div>
                    <ul style="margin:0;padding-left:16px;font-size:12.5px;color:var(--text-secondary);line-height:1.8">{_reqs}</ul>
                  </div>
                  <div style="background:rgba(34,211,165,0.06);border:1px solid rgba(34,211,165,0.18);border-radius:8px;padding:12px">
                    <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;color:#22d3a5;margin-bottom:6px">🏦 Banking Relevance</div>
                    <p style="margin:0;font-size:12.5px;color:var(--text-secondary);line-height:1.8">{_s['relevance_to_banking']}</p>
                  </div>
                </div>""", unsafe_allow_html=True)

        # B) Regulatory Reference
        st.markdown("---")
        _selected_jurs_display = " · ".join(_t3_jurs[:4])
        st.markdown(
            f'<div class="section-title">B. Regulatory Reference'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{_selected_jurs_display}</span></div>',
            unsafe_allow_html=True,
        )
        _reg3_sq = st.text_input("Search frameworks", placeholder="Filter frameworks…", key="_reg3_sq", label_visibility="collapsed")
        for _jur in _t3_jurs:
            _reg3_items = REGULATORY_FRAMEWORKS.get(_jur, [])
            if _reg3_sq:
                _qrg = _reg3_sq.lower()
                _reg3_items = [r for r in _reg3_items if _qrg in (r.get("title","") + r.get("reference","")).lower()]
            if _reg3_items:
                with st.expander(f"**{_jur}** — {len(_reg3_items)} texts"):
                    _rows3 = ""
                    for _r in _reg3_items:
                        _applies3 = " &nbsp;".join(f'<span class="badge-info">{t}</span>' for t in _r.get("applies_to", []))
                        _reqs3 = "".join(f"<li>{k}</li>" for k in _r.get("key_requirements", []))
                        _rows3 += (
                            f'<tr>'
                            f'<td style="padding:9px 13px;color:#7fa8fb;font-weight:600;white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{_r.get("reference","")}</td>'
                            f'<td style="padding:9px 13px;color:var(--text-primary);font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{_r.get("title","")}<br><span style="font-size:11px;color:var(--text-muted)">{_r.get("authority","")} · {_r.get("year","")}</span></td>'
                            f'<td style="padding:9px 13px;color:var(--text-secondary);font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{_r.get("scope","")}</td>'
                            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{_applies3}</td>'
                            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)"><ul style="margin:0;padding-left:15px;font-size:11.5px;color:var(--text-secondary);line-height:1.7">{_reqs3}</ul></td>'
                            f'</tr>'
                        )
                    st.markdown(f"""
                    <table class="data-table" style="font-size:12px">
                      <thead><tr style="background:rgba(79,126,248,0.07);border-bottom:1px solid rgba(79,126,248,0.18)">
                        <th style="color:#7fa8fb;width:10%">Reference</th><th style="color:#7fa8fb;width:18%">Title</th>
                        <th style="color:#7fa8fb;width:22%">Scope</th><th style="color:#7fa8fb;width:14%">Applies To</th>
                        <th style="color:#7fa8fb;width:36%">Key Requirements</th>
                      </tr></thead><tbody>{_rows3}</tbody>
                    </table>""", unsafe_allow_html=True)

        st.markdown("<div class='no-print' style='margin-top:1rem'>", unsafe_allow_html=True)
        _print_button()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.t3_mode == "live":
        ctx_parts = []
        if st.session_state.t1_topic:
            ctx_parts.append(f"✓ Topic: {st.session_state.t1_topic}")
        if st.session_state.t2_org_plan:
            ctx_parts.append("✓ Audit plan available")
        if ctx_parts:
            st.markdown(f'<div class="ctx-pill">{" &nbsp;·&nbsp; ".join(ctx_parts)}</div>', unsafe_allow_html=True)

        default_name = f"Internal Audit — {st.session_state.t1_topic} — 2025" if st.session_state.t1_topic else ""
        audit_name = st.text_input(
            "Report Title",
            value=default_name,
            placeholder="e.g. Internal Audit — AML/KYC — Private Banking Group — 2025",
            key="t3_name_in",
        )

        observations = st.text_area(
            "Issues Log",
            placeholder="e.g.\n1. Transaction monitoring does not cover transfers below CHF 10,000.\n2. Incomplete KYC files for 12 out of 50 clients tested.\n3. No PEP screening procedure in place at the Singapore entity.",
            height=200,
            key="t3_obs_in",
            help="Enter the audit issues and findings identified during fieldwork. Each issue should include the observation and impact.",
        )

        uploads3 = st.file_uploader(
            "Working papers (optional — PDF, Word, Excel, TXT)",
            type=["pdf", "docx", "xlsx", "txt"], accept_multiple_files=True, key="t3_upload",
        )

        st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

        # Input validation
        _t3_valid = True
        if audit_name and not observations.strip():
            st.warning("⚠ Please enter at least one issue in the Issues Log before generating the report.")
            _t3_valid = False

        if st.button(
            "Generate Report", type="primary",
            disabled=_disabled or not audit_name or not observations or not _t3_valid,
            key="t3_run",
        ):
            with st.spinner("Drafting report…"):
                try:
                    c = _client()
                    file_ids3 = []
                    for uf in (uploads3 or []):
                        fm = _upload_sf(c, uf)
                        if fm:
                            file_ids3.append(fm)

                    reg_ctx = (f"\n\nApplicable regulations:\n{json.dumps(st.session_state.t1_regs, indent=2)[:1500]}"
                               if st.session_state.t1_regs else "")
                    plan_ctx = (f"\n\nAudit plan:\n{st.session_state.t2_org_plan[:900]}"
                                if st.session_state.t2_org_plan else "")

                    user_content = []
                    if file_ids3:
                        user_content.extend(build_file_content_blocks(file_ids3))
                        user_content.append({"type": "text", "text": f"{len(file_ids3)} working paper(s) attached."})

                    user_content.append({"type": "text", "text": (
                        f"Draft a professional IIA-standard internal audit report in English.\n\n"
                        f"Report title: {audit_name}\n"
                        f"Institution: Swiss private bank (HNWI, cross-border: CH, SG, HK, Bahamas, EU, UK)"
                        f"{reg_ctx}{plan_ctx}\n\n"
                        f"Issues log:\n{observations}\n\n"
                        f"Structure:\n"
                        f"1. Executive Summary — opinion, key findings, priority actions\n"
                        f"2. Background & Context — institution, regulatory environment\n"
                        f"3. Scope & Methodology\n"
                        f"4. Findings — sorted by severity (Critical first): "
                        f"risk rating, impact, root cause, recommendation, owner, target date\n"
                        f"5. Action Plan — summary table\n"
                        f"6. Audit Opinion — motivated conclusion\n\n"
                        f"Then call generate_audit_report to export."
                    )})

                    def _h3(name, inp):
                        if name == "generate_audit_report":
                            try:
                                p = generate_audit_report_docx(inp, OUTPUT_DIR)
                                return f"Saved: {p}", {"docx_path": p}
                            except Exception as ex:
                                return f"Error: {ex}", {}
                        return "Unknown tool", {}

                    text_out, extra = _agentic_loop(c, _a3.SYSTEM_PROMPT, _a3.TOOLS,
                        [{"role": "user", "content": user_content}], _h3)

                    result = {"text": text_out, "name": audit_name}
                    if "docx_path" in extra and Path(extra["docx_path"]).exists():
                        result["docx_bytes"] = Path(extra["docx_path"]).read_bytes()

                    st.session_state.t3_report = result

                except Exception:
                    st.error("An error occurred. Please try again.")

        # Results (live mode only)
        if st.session_state.t3_report:
            res  = st.session_state.t3_report
            name = res.get("name", "report")
            st.markdown("---")

            st.markdown('<div class="section-title">Audit Report</div>', unsafe_allow_html=True)
            text = res.get("text", "")
            if text:
                st.markdown(f'<div class="output-box">{text}</div>', unsafe_allow_html=True)
                _copy_button(text, "t3_report_copy")
            else:
                st.info("Report content is available in the export file.")

            docx = res.get("docx_bytes")
            if docx:
                st.markdown("---")
                dl_col, print_col = st.columns([2, 1])
                with dl_col:
                    st.download_button(
                        "⬇  Download Report (.docx)",
                        data=docx,
                        file_name=f"Audit_Report_{name.replace(' ', '_')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
                with print_col:
                    _print_button()
            else:
                st.markdown("<div style='margin-top:1rem'>", unsafe_allow_html=True)
                _print_button()
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown('<div class="section-title">Targeted Revision</div>', unsafe_allow_html=True)
            followup = st.text_area(
                "Revision instructions", label_visibility="collapsed", height=80,
                placeholder="e.g. Strengthen recommendation 3. Add a 30-day deadline for the KYC finding.",
                key="t3_rev_in",
            )

            if st.button("Revise", disabled=not followup or _disabled, key="t3_rev_btn"):
                with st.spinner("Applying revisions…"):
                    try:
                        c = _client()
                        rev_content = [{"type": "text", "text": (
                            f"Previous report:\n{res.get('text', '')[:3000]}\n\n"
                            f"Revision instructions: {followup}\n\n"
                            f"Apply revisions precisely. Then call generate_audit_report to export."
                        )}]

                        def _h3r(name, inp):
                            if name == "generate_audit_report":
                                try:
                                    p = generate_audit_report_docx(inp, OUTPUT_DIR)
                                    return f"Saved: {p}", {"docx_path": p}
                                except Exception as ex:
                                    return f"Error: {ex}", {}
                            return "Unknown tool", {}

                        text2, extra2 = _agentic_loop(c, _a3.SYSTEM_PROMPT, _a3.TOOLS,
                            [{"role": "user", "content": rev_content}], _h3r)

                        res2 = {"text": text2, "name": name}
                        if "docx_path" in extra2 and Path(extra2["docx_path"]).exists():
                            res2["docx_bytes"] = Path(extra2["docx_path"]).read_bytes()
                        st.session_state.t3_report = res2
                        st.rerun()

                    except Exception:
                        st.error("An error occurred. Please try again.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p class="footer">AuditIQ · Internal Audit System · Private Banking · CH · SG · HK · Bahamas · EU · UK</p>',
    unsafe_allow_html=True,
)
