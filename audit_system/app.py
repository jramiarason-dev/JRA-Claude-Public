# RULE: All HTML content must use st.markdown(..., unsafe_allow_html=True)
# Never use st.write() or st.text() for HTML strings
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
    "t1_xlsx": None, "t1_pptx2": None, "t3_xlsx": None, "t3_pptx2": None,
    # UX
    "theme": "dark",
    "history": [],
    "_tpl_applied": False,
    "_tpl_name": "",
    # Static data
    "dash_source": "static",   # "static" | "live"
    "ref_search": "",
    "mode_tab1": "📚 Static Reference Data",
    "mode_tab2": "📚 Static Reference Data",
    "mode_tab3": "📚 Static Reference Data",
}
for _k, _v in _SS_DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── Example cards (hardcoded, always visible, #0a2540 bg, #3b82f6 border) ─────
_EX_S = "background:#0a2540;border-left:4px solid #3b82f6;border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:14px"
_EX_L = '<div style="font-size:10.5px;font-weight:700;font-style:italic;color:#3b82f6;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:10px">📌 EXAMPLE</div>'

_EXAMPLE_RISK = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap">
    <span style="background:rgba(239,68,68,0.18);color:#ef4444;border:1px solid rgba(239,68,68,0.4);border-radius:4px;padding:2px 9px;font-size:11px;font-weight:700">🔴 CRITICAL</span>
    <span style="font-size:13px;font-weight:600;color:#dde3f5">Inadequate PEP Screening</span>
    <span style="font-size:11px;color:#8392bb">Private Banking / AML-KYC</span>
  </div>
  <div style="font-size:12px;color:#8392bb;margin-bottom:10px">Probability: <span style="color:#ef4444;font-weight:600">High</span> &nbsp;|&nbsp; Impact: <span style="color:#ef4444;font-weight:600">High</span></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;font-size:12px">
    <div>
      <div style="font-size:10.5px;font-weight:700;color:#8392bb;text-transform:uppercase;margin-bottom:5px">Expected Controls</div>
      <ul style="margin:0;padding-left:14px;color:#c8d0e8;line-height:1.9">
        <li>Automated PEP/sanctions screening tool</li><li>Enhanced Due Diligence mandatory for PEPs</li>
        <li>Quarterly review of PEP client list</li><li>Senior management approval required</li>
      </ul>
    </div>
    <div>
      <div style="font-size:10.5px;font-weight:700;color:#8392bb;text-transform:uppercase;margin-bottom:5px">Red Flags</div>
      <ul style="margin:0;padding-left:14px;color:#c8d0e8;line-height:1.9">
        <li>⚠ Manual screening only</li><li>⚠ No adverse media check</li>
        <li>⚠ Outdated sanctions lists (&gt;30 days)</li><li>⚠ No source of wealth documentation</li>
      </ul>
    </div>
  </div>
  <div style="margin-top:10px;font-size:11px;color:#5a6488">Ref: FINMA-RS 2011/1 · FATF R.12</div>
</div>
"""

_EXAMPLE_REGULATION = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="font-size:13px;font-weight:600;color:#dde3f5;margin-bottom:4px">🇨🇭 CH/FINMA — FINMA-RS 2011/1 — Anti-Money Laundering Ordinance</div>
  <div style="font-size:11px;color:#8392bb;margin-bottom:10px">FINMA · 2011 (updated 2020) · AML, KYC, PEP, Correspondent Banking</div>
  <div style="font-size:10.5px;font-weight:700;color:#8392bb;text-transform:uppercase;margin-bottom:5px">Key Requirements</div>
  <ul style="margin:0;padding-left:14px;font-size:12px;color:#c8d0e8;line-height:1.9">
    <li>Risk-based CDD for all clients</li><li>EDD mandatory for PEPs and HNWI &gt;CHF 1M</li>
    <li>Annual review of high-risk relationships</li><li>Transaction monitoring thresholds defined</li>
    <li>10-year document retention</li>
  </ul>
  <div style="margin-top:8px;font-size:11px;color:#5a6488">Applies to: AML · KYC · PEP · Correspondent Banking</div>
</div>
"""

_EXAMPLE_PUB_REC = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap">
    <span style="font-size:13px;font-weight:600;color:#7fa8fb">FATF Guidance — Private Banking</span>
    <span style="font-size:11.5px;color:#8392bb">2023</span>
    <span style="background:rgba(239,68,68,0.15);color:#ef4444;border:1px solid rgba(239,68,68,0.35);border-radius:4px;padding:1px 7px;font-size:11px;font-weight:700">🔴 High Priority</span>
  </div>
  <p style="font-size:12.5px;color:#c8d0e8;line-height:1.85;margin:0 0 8px;font-style:italic">
    "Private banks must implement risk-based EDD for all HNWI clients with assets above USD 1M, including source of wealth verification and mandatory annual review. Beneficial ownership must be verified at onboarding and upon material change."
  </p>
  <div style="font-size:11.5px;color:#8392bb">Private Banking Relevance: <span style="color:#ef4444;font-weight:600">Critical</span></div>
</div>
"""

_EXAMPLE_RATIONALE = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="font-size:13px;font-weight:600;color:#dde3f5;margin-bottom:10px">💡 RATIONALE — Cyber Risk Audit 2025</div>
  <div style="font-size:12px;color:#c8d0e8;line-height:1.85;margin-bottom:8px"><strong style="color:#7fa8fb">Why now:</strong> DORA entered into force January 2025. FINMA observed a 40% increase in cyber incidents in Swiss private banks (2024). MAS TRM 2021 requires annual ICT audit.</div>
  <div style="font-size:12px;color:#c8d0e8;line-height:1.85;margin-bottom:8px"><strong style="color:#7fa8fb">Strategic context:</strong> Private banks managing HNWI data face elevated threats from ransomware and social engineering. Cloud migration increases attack surface across all jurisdictions.</div>
  <div style="font-size:12px;color:#c8d0e8;line-height:1.85"><strong style="color:#7fa8fb">Benchmark:</strong> 78% of peer institutions suffered at least one cyber incident in 2023 (BCBS Sound Practices Survey).</div>
</div>
"""

_EXAMPLE_TEST = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap">
    <span style="color:#7fa8fb;font-weight:700;font-size:13px">T011</span>
    <span style="background:rgba(79,126,248,0.15);color:#7fa8fb;border:1px solid rgba(79,126,248,0.35);border-radius:4px;padding:1px 7px;font-size:11px;font-weight:600">📊 DA</span>
    <span style="background:rgba(249,115,22,0.15);color:#f97316;border:1px solid rgba(249,115,22,0.35);border-radius:4px;padding:1px 7px;font-size:11px;font-weight:700">🔴 HIGH</span>
    <span style="font-size:13px;font-weight:600;color:#dde3f5">MFA Enforcement on Privileged Accounts</span>
  </div>
  <div style="font-size:11.5px;color:#8392bb;margin-bottom:6px"><strong style="color:#c8d0e8">Objective:</strong> Verify MFA is enforced on all privileged and admin accounts</div>
  <div style="font-size:11.5px;color:#8392bb;margin-bottom:8px"><strong style="color:#c8d0e8">Procedure:</strong> Extract full list of admin accounts from Active Directory. Cross-ref with MFA enrollment logs. Identify accounts without MFA enrolled.</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;font-size:11.5px">
    <div><span style="color:#8392bb;font-weight:600">Population:</span> <span style="color:#c8d0e8">All privileged accounts (~50)</span></div>
    <div><span style="color:#8392bb;font-weight:600">Sample Size:</span> <span style="color:#c8d0e8">100% (full population)</span></div>
    <div><span style="color:#8392bb;font-weight:600">Failure:</span> <span style="color:#ef4444">Any admin account without MFA = immediate finding</span></div>
  </div>
</div>
"""

_EXAMPLE_DA = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap">
    <span style="color:#22d3a5;font-weight:700;font-size:13px">DA023</span>
    <span style="font-size:13px;font-weight:600;color:#dde3f5">Privileged Access Anomaly Detection</span>
    <span style="margin-left:auto;background:rgba(234,179,8,0.15);color:#eab308;border:1px solid rgba(234,179,8,0.35);border-radius:4px;padding:1px 7px;font-size:11px;font-weight:600">🟡 Medium</span>
  </div>
  <div style="font-size:11.5px;color:#8392bb;margin-bottom:5px">Theme: <span style="color:#c8d0e8">Cyber Risk</span></div>
  <div style="font-size:11.5px;color:#8392bb;margin-bottom:8px"><strong style="color:#c8d0e8">Objective:</strong> Detect abnormal admin activity indicative of insider threat or compromise</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:11.5px;margin-bottom:8px">
    <div><span style="color:#8392bb;font-weight:600">Data Sources:</span> <span style="color:#c8d0e8">AD logs · SIEM (Splunk) · PAM system</span></div>
    <div><span style="color:#8392bb;font-weight:600">Analysis Type:</span> <span style="color:#c8d0e8">Anomaly Detection</span></div>
  </div>
  <ul style="margin:0;padding-left:14px;font-size:11.5px;color:#c8d0e8;line-height:1.9">
    <li>Logins outside business hours (22h–6h)</li><li>Bulk data exports &gt;500 records</li>
    <li>Lateral movement across network segments</li><li>Failed logins &gt;5 attempts</li>
  </ul>
  <div style="margin-top:8px;font-size:11px;color:#5a6488">Tools: <span style="color:#7fa8fb">Python (pandas) / Splunk / SQL</span></div>
</div>
"""

_EXAMPLE_FINDING = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;flex-wrap:wrap">
    <span style="background:rgba(249,115,22,0.15);color:#f97316;border:1px solid rgba(249,115,22,0.4);border-radius:4px;padding:2px 10px;font-size:12px;font-weight:700">FINDING #1 — 🔴 HIGH</span>
    <span style="font-size:13px;font-weight:600;color:#dde3f5">AML/KYC — Inadequate Source of Wealth Documentation</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;font-size:12px;margin-bottom:12px">
    <div><div style="font-size:10.5px;font-weight:700;color:#8392bb;text-transform:uppercase;margin-bottom:4px">Observation</div>
    <p style="color:#c8d0e8;margin:0;line-height:1.85">8 out of 30 client files tested (27%) lack updated SoW documentation despite AuM exceeding CHF 5M threshold. Last review dated over 36 months ago.</p></div>
    <div><div style="font-size:10.5px;font-weight:700;color:#8392bb;text-transform:uppercase;margin-bottom:4px">Risk</div>
    <p style="color:#c8d0e8;margin:0;line-height:1.85">Regulatory sanction (FINMA), reputational damage, potential facilitation of money laundering via private banking.</p></div>
  </div>
  <div style="padding-top:10px;border-top:1px solid rgba(255,255,255,0.06)">
    <div style="font-size:10.5px;font-weight:700;color:#8392bb;text-transform:uppercase;margin-bottom:4px">Recommendation</div>
    <p style="color:#c8d0e8;margin:0 0 8px;font-size:12px;line-height:1.85">Implement systematic annual SoW review for all clients above CHF 1M AuM. Assign ownership to Compliance team. Complete remediation by Q2 2025.</p>
    <div style="font-size:11px;color:#5a6488">Ref: <span style="color:#7fa8fb">FINMA-RS 2011/1 §15 · FATF R.10</span> &nbsp;·&nbsp; Rating: <span style="color:#f97316;font-weight:600">High</span> &nbsp;·&nbsp; Due: <span style="color:#22d3a5">Q2 2025</span></div>
  </div>
</div>
"""

_EXAMPLE_IIA_STD = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="font-size:13px;font-weight:600;color:#dde3f5;margin-bottom:4px">IIA GIAS 2024 — TR-2: Cybersecurity (Topical Requirement)</div>
  <div style="font-size:11px;color:#8392bb;margin-bottom:10px">Effective: January 9, 2024 · Domain: Topical Requirements</div>
  <p style="font-size:12.5px;color:#c8d0e8;line-height:1.85;margin:0 0 8px;font-style:italic">"Internal auditors must evaluate cybersecurity governance, risk management, and controls as a core component of the audit universe. Given the escalating threat landscape, cybersecurity must be assessed with specialist knowledge or co-sourced expertise."</p>
  <div style="font-size:11.5px;color:#8392bb">Banking Application: <span style="color:#c8d0e8">DORA (effective Jan 2025) requires ICT risk assessment, major incident reporting, and third-party ICT oversight. Internal audit must verify DORA compliance for EU-facing operations.</span></div>
</div>
"""

_EXAMPLE_DORA = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="font-size:13px;font-weight:600;color:#dde3f5;margin-bottom:4px">🇪🇺 EU — DORA (Digital Operational Resilience Act) — In force January 2025</div>
  <div style="font-size:11.5px;color:#8392bb;margin-bottom:10px">European Parliament · 2022/2554 · ICT, Cyber, Third-Party Risk</div>
  <div style="font-size:10.5px;font-weight:700;color:#8392bb;text-transform:uppercase;margin-bottom:5px">Key Requirements</div>
  <ul style="margin:0;padding-left:14px;font-size:12px;color:#c8d0e8;line-height:1.9">
    <li>ICT risk management framework mandatory</li><li>Third-party ICT provider oversight (Art. 28–30)</li>
    <li>Major incident reporting within 4 hours</li><li>Annual TLPT (Threat-Led Penetration Testing)</li>
    <li>Digital resilience testing programme</li>
  </ul>
  <div style="margin-top:8px;font-size:11.5px;color:#8392bb">Audit Focus: <span style="color:#c8d0e8">ICT governance · vendor contracts · incident response · TLPT evidence</span></div>
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

  /* ── Mode toggle radio ── */
  div[data-testid="stRadio"] > div {
    display: flex;
    flex-direction: row;
    gap: 12px;
    background: #13172a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 6px 10px;
    width: fit-content;
  }
  div[data-testid="stRadio"] label {
    color: #5a6488;
    font-size: 13px;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 6px;
    cursor: pointer;
  }
  div[data-testid="stRadio"] label:has(input:checked) {
    background: #1e2a45;
    color: #7fa8fb;
    font-weight: 600;
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
        generate_risk_analysis_excel,
        generate_audit_findings_excel,
        generate_tab1_pptx,
        generate_report_pptx,
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
    THEMATIC_BACKGROUND, REGULATORY_CALENDAR, HNWI_RED_FLAGS,
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


# ── Regulatory Calendar helper ────────────────────────────────────────────────
def _parse_cal_date(d: str):
    """Return (date_obj_or_None, display_str) from a date string like '2025-03-31' or '2025-Q2'."""
    import re
    from datetime import date
    if re.match(r"\d{4}-\d{2}-\d{2}$", d):
        try:
            return date.fromisoformat(d), d
        except ValueError:
            return None, d
    m = re.match(r"(\d{4})-Q([1-4])$", d)
    if m:
        year, q = int(m.group(1)), int(m.group(2))
        end_month = q * 3
        import calendar as _cal
        last_day = _cal.monthrange(year, end_month)[1]
        try:
            return date(year, end_month, last_day), f"Q{q} {year}"
        except ValueError:
            return None, d
    return None, d


def _show_regulatory_calendar(jur_filter="All", type_filter="All", prio_filter="All", year_filter="All"):
    """Render REGULATORY_CALENDAR with filters and upcoming-deadline badges."""
    from datetime import date, timedelta
    today = date.today()
    horizon = today + timedelta(days=90)

    _PRIO_C  = {"High": "#ef4444", "Medium": "#f97316", "Low": "#22d3a5"}
    _PRIO_BG = {"High": "rgba(239,68,68,0.08)", "Medium": "rgba(249,115,22,0.08)", "Low": "rgba(34,211,165,0.06)"}
    _TYPE_C  = {
        "Entry into force":      "#7fa8fb",
        "Implementation deadline": "#ef4444",
        "Consultation":          "#eab308",
        "Review":                "#a78bfa",
    }

    entries = list(REGULATORY_CALENDAR)
    if jur_filter  != "All": entries = [e for e in entries if e["jurisdiction"] == jur_filter]
    if type_filter != "All": entries = [e for e in entries if e["type"] == type_filter]
    if prio_filter != "All": entries = [e for e in entries if e["priority"] == prio_filter]
    if year_filter != "All":
        entries = [e for e in entries if str(e["date"]).startswith(year_filter)]

    if not entries:
        st.caption("No entries match the selected filters.")
        return

    upcoming_count = 0
    for e in entries:
        dt, _ = _parse_cal_date(e["date"])
        if dt and today <= dt <= horizon:
            upcoming_count += 1

    if upcoming_count:
        st.markdown(
            f'<div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);'
            f'border-radius:7px;padding:8px 14px;margin-bottom:12px;font-size:12px;color:#ef4444">'
            f'⚠️ <strong>{upcoming_count} deadline{"s" if upcoming_count>1 else ""}</strong> '
            f'within the next 90 days</div>',
            unsafe_allow_html=True,
        )

    for e in entries:
        dt, date_display = _parse_cal_date(e["date"])
        is_upcoming = bool(dt and today <= dt <= horizon)
        is_past     = bool(dt and dt < today)

        prio    = e.get("priority", "Medium")
        etype   = e.get("type", "")
        pcolor  = _PRIO_C.get(prio, "#8392bb")
        pbg     = _PRIO_BG.get(prio, "transparent")
        tcolor  = _TYPE_C.get(etype, "#8392bb")
        border_color = "#ef4444" if is_upcoming else (pcolor + "55")
        date_color   = "#ef4444" if is_upcoming else ("#5a6488" if is_past else "#c8d0e8")

        upcoming_badge = (
            '<span style="background:rgba(239,68,68,0.15);color:#ef4444;border:1px solid rgba(239,68,68,0.4);'
            'border-radius:4px;padding:1px 7px;font-size:10px;font-weight:700;margin-left:6px">⚠️ Upcoming</span>'
            if is_upcoming else ""
        )
        past_badge = (
            '<span style="background:rgba(90,100,136,0.12);color:#5a6488;border:1px solid rgba(90,100,136,0.25);'
            'border-radius:4px;padding:1px 7px;font-size:10px;font-weight:500;margin-left:6px">Past</span>'
            if is_past else ""
        )

        examples_html = "".join(
            f'<li style="margin-bottom:3px;color:#8392bb;font-style:italic">{ex}</li>'
            for ex in (e.get("examples") or [])
        )

        st.markdown(f"""
        <div style="border:1px solid {border_color};border-radius:9px;padding:14px 18px;
                    margin-bottom:10px;background:{pbg if is_upcoming else 'rgba(19,23,42,0.4)'}">
          <div style="display:flex;align-items:flex-start;gap:10px;flex-wrap:wrap;margin-bottom:8px">
            <span style="background:{tcolor}22;color:{tcolor};border:1px solid {tcolor}44;
                  border-radius:4px;padding:2px 8px;font-size:10px;font-weight:700;white-space:nowrap">{etype}</span>
            <span style="background:{pcolor}18;color:{pcolor};border:1px solid {pcolor}33;
                  border-radius:4px;padding:2px 8px;font-size:10px;font-weight:700;white-space:nowrap">{prio}</span>
            <span style="background:rgba(79,126,248,0.08);color:#7fa8fb;border:1px solid rgba(79,126,248,0.2);
                  border-radius:4px;padding:2px 8px;font-size:10px;font-weight:600;white-space:nowrap">{e.get("jurisdiction","")}</span>
            <span style="font-size:13px;font-weight:600;color:#dde3f5;flex:1">{e.get("reg_id","")} — {e.get("regulation","")}</span>
            <span style="font-size:12px;font-weight:700;color:{date_color};white-space:nowrap">{date_display}{upcoming_badge}{past_badge}</span>
          </div>
          <p style="font-size:12px;color:var(--text-secondary);margin:0 0 8px;line-height:1.7">{e.get("description","")}</p>
          <details>
            <summary style="font-size:11.5px;color:#7fa8fb;cursor:pointer;font-weight:500">Impact · Action required · Audit relevance</summary>
            <div style="margin-top:10px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px">
              <div>
                <div style="font-size:10px;font-weight:700;color:#5a6488;margin-bottom:4px;text-transform:uppercase">Impact — Private Banking</div>
                <p style="font-size:11.5px;color:var(--text-secondary);margin:0;line-height:1.65">{e.get("impact_private_banking","")}</p>
              </div>
              <div>
                <div style="font-size:10px;font-weight:700;color:#5a6488;margin-bottom:4px;text-transform:uppercase">Action Required</div>
                <p style="font-size:11.5px;color:var(--text-secondary);margin:0;line-height:1.65">{e.get("action_required","")}</p>
              </div>
              <div>
                <div style="font-size:10px;font-weight:700;color:#7fa8fb;margin-bottom:4px;text-transform:uppercase">Audit Relevance</div>
                <p style="font-size:11.5px;color:#a8b4d8;margin:0;line-height:1.65">{e.get("audit_relevance","")}</p>
              </div>
            </div>
          </details>
        </div>""", unsafe_allow_html=True)


# ── HNWI Red Flags helper ─────────────────────────────────────────────────────
def _show_red_flags(cat_filter="All", level_filter="All", search=""):
    """Render HNWI_RED_FLAGS with filters, coloured badges, and italic examples."""
    _RL_C  = {"Critical": "#ef4444", "High": "#f97316", "Medium": "#eab308"}
    _RL_BG = {"Critical": "rgba(239,68,68,0.07)", "High": "rgba(249,115,22,0.07)", "Medium": "rgba(234,179,8,0.06)"}
    _CAT_C = {"AML": "#7fa8fb", "Fraud": "#ef4444", "Suitability": "#a78bfa", "Tax": "#22d3a5", "Conduct": "#f97316"}

    entries = list(HNWI_RED_FLAGS)
    if cat_filter   != "All": entries = [e for e in entries if e["category"] == cat_filter]
    if level_filter != "All": entries = [e for e in entries if e["risk_level"] == level_filter]
    if search:
        q = search.lower()
        entries = [e for e in entries if q in (e.get("title","") + e.get("description","") + e.get("private_banking_context","")).lower()]

    if not entries:
        st.caption("No red flags match the selected filters.")
        return

    for e in entries:
        rl  = e.get("risk_level", "High")
        cat = e.get("category", "")
        rc  = _RL_C.get(rl, "#8392bb")
        rbg = _RL_BG.get(rl, "transparent")
        cc  = _CAT_C.get(cat, "#8392bb")

        examples_html = "".join(
            f'<li style="color:#6b7899;font-style:italic;font-size:11.5px;margin-bottom:2px">{ex}</li>'
            for ex in (e.get("examples") or [])
        )

        st.markdown(f"""
        <div style="border:1px solid {rc}33;border-radius:9px;padding:13px 17px;margin-bottom:10px;background:{rbg}">
          <div style="display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:7px">
            <span style="background:{rc}20;color:{rc};border:1px solid {rc}44;border-radius:4px;
                  padding:2px 8px;font-size:10px;font-weight:700">{rl}</span>
            <span style="background:{cc}18;color:{cc};border:1px solid {cc}33;border-radius:4px;
                  padding:2px 8px;font-size:10px;font-weight:600">{cat}</span>
            <span style="font-size:13px;font-weight:600;color:#dde3f5">{e.get("rf_id","")} — {e.get("title","")}</span>
          </div>
          <p style="font-size:12.5px;color:var(--text-secondary);margin:0 0 8px;line-height:1.7">{e.get("description","")}</p>
          <details>
            <summary style="font-size:11.5px;color:#7fa8fb;cursor:pointer;font-weight:500">Detection · Regulation · PB context · Examples</summary>
            <div style="margin-top:10px;display:grid;grid-template-columns:1fr 1fr;gap:12px">
              <div>
                <div style="font-size:10px;font-weight:700;color:#5a6488;margin-bottom:4px;text-transform:uppercase">Detection Method</div>
                <p style="font-size:11.5px;color:var(--text-secondary);margin:0 0 10px;line-height:1.65">{e.get("detection_method","")}</p>
                <div style="font-size:10px;font-weight:700;color:#5a6488;margin-bottom:4px;text-transform:uppercase">Regulatory Reference</div>
                <p style="font-size:11.5px;color:#a8b4d8;margin:0;line-height:1.65">{e.get("regulatory_reference","")}</p>
              </div>
              <div>
                <div style="font-size:10px;font-weight:700;color:#5a6488;margin-bottom:4px;text-transform:uppercase">Private Banking Context</div>
                <p style="font-size:11.5px;color:var(--text-secondary);margin:0 0 10px;line-height:1.65">{e.get("private_banking_context","")}</p>
                <div style="font-size:10px;font-weight:700;color:#5a6488;margin-bottom:4px;text-transform:uppercase">Examples</div>
                <ul style="margin:0;padding-left:15px;line-height:1.8">{examples_html}</ul>
              </div>
            </div>
          </details>
        </div>""", unsafe_allow_html=True)


# ── Thematic Background helper ────────────────────────────────────────────────
def _show_thematic_background(theme_key: str):
    """Render a THEMATIC_BACKGROUND card with all subsections."""
    _SEC_C  = "#7fa8fb"
    _SEC_BG = "rgba(79,126,248,0.06)"

    card = THEMATIC_BACKGROUND.get(theme_key)
    if not card:
        available = ", ".join(k.replace("_", " ").title() for k in THEMATIC_BACKGROUND)
        st.markdown(
            f'<div style="background:rgba(234,179,8,0.07);border:1px solid rgba(234,179,8,0.3);'
            f'border-radius:8px;padding:14px 18px">'
            f'<p style="color:#eab308;font-size:12.5px;margin:0 0 6px;font-weight:600">'
            f'⚠️ No thematic profile found for this topic.</p>'
            f'<p style="color:#c8d0e8;font-size:12px;margin:0">Available themes: '
            f'<span style="color:#7fa8fb">{available}</span></p></div>',
            unsafe_allow_html=True,
        )
        return

    def _section(icon, label, content, is_list=False):
        if is_list:
            items = "".join(
                f'<li style="margin-bottom:5px;color:var(--text-secondary);font-size:12px;line-height:1.65">{s}</li>'
                for s in content
            )
            body = f'<ul style="margin:0;padding-left:18px">{items}</ul>'
        else:
            body = f'<p style="font-size:12.5px;color:var(--text-secondary);margin:0;line-height:1.8;white-space:pre-line">{content}</p>'
        st.markdown(
            f'<div style="background:{_SEC_BG};border-left:3px solid {_SEC_C}33;'
            f'border-radius:0 7px 7px 0;padding:12px 16px;margin-bottom:10px">'
            f'<div style="font-size:11px;font-weight:700;color:{_SEC_C};text-transform:uppercase;'
            f'letter-spacing:0.5px;margin-bottom:6px">{icon} {label}</div>'
            f'{body}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">'
        f'<span style="font-size:15px;font-weight:700;color:#dde3f5">{card.get("theme","")}</span>'
        f'<span style="background:rgba(34,211,165,0.1);color:#22d3a5;border:1px solid rgba(34,211,165,0.25);'
        f'border-radius:4px;padding:1px 8px;font-size:10px;font-weight:600">Static Intelligence</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    _section("🌍", "Market Context",           card.get("market_context", ""))
    _section("🏦", "Private Banking Issues",   card.get("private_banking_issues", ""))
    _section("⚖️", "Regulatory Pressure",       card.get("regulatory_pressure", ""))
    _section("📈", "Industry Trends",           card.get("industry_trends", ""))
    _section("⚠️", "Peer Incidents",            card.get("peer_incidents", ""))
    _section("📊", "Key Statistics",            card.get("key_statistics", []), is_list=True)
    _section("💡", "Strategic Angle",           card.get("mckinsey_angle", ""))


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


_MODE_STATIC = "📚 Static Reference Data"
_MODE_LIVE   = "⚡ Live Analysis"


def render_mode_toggle(tab_key: str) -> str:
    """Uniform mode toggle using st.radio(). Returns 'static' or 'live'."""
    if tab_key not in st.session_state:
        st.session_state[tab_key] = _MODE_STATIC
    selected = st.radio(
        "Mode",
        options=[_MODE_STATIC, _MODE_LIVE],
        key=tab_key,
        horizontal=True,
        label_visibility="collapsed",
    )
    st.divider()
    return "static" if selected == _MODE_STATIC else "live"


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
        tr_ref = t.get("tr_reference", "")
        tr_cell = f'<span style="background:rgba(79,126,248,0.09);color:#7fa8fb;border:1px solid rgba(79,126,248,0.25);border-radius:3px;padding:1px 5px;font-size:10px;white-space:nowrap">{tr_ref}</span>' if tr_ref else ""
        rows += (
            f'<tr style="background:{bg}">'
            f'<td style="padding:9px 12px;color:#7fa8fb;font-weight:700;white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("id","")} {da}</td>'
            f'<td style="padding:9px 12px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{lv_badge}</td>'
            f'<td style="padding:9px 12px;color:var(--text-primary);font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("objective","")}</td>'
            f'<td style="padding:9px 12px;color:var(--text-secondary);font-size:12px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("procedure","")}</td>'
            f'<td style="padding:9px 12px;color:var(--text-muted);font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("population","")}</td>'
            f'<td style="padding:9px 12px;color:var(--text-muted);font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("sample_size","")}</td>'
            f'<td style="padding:9px 12px;color:#ef4444;font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("failure_criteria","")}</td>'
            f'<td style="padding:9px 12px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{tr_cell}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(79,126,248,0.07);border-bottom:1px solid rgba(79,126,248,0.18)">
        <th style="color:#7fa8fb;width:7%">ID</th>
        <th style="color:#7fa8fb;width:7%">Level</th>
        <th style="color:#7fa8fb;width:18%">Objective</th>
        <th style="color:#7fa8fb;width:24%">Procedure</th>
        <th style="color:#7fa8fb;width:14%">Population</th>
        <th style="color:#7fa8fb;width:11%">Sample Size</th>
        <th style="color:#7fa8fb;width:11%">Failure Criteria</th>
        <th style="color:#7fa8fb;width:8%">TR Ref</th>
      </tr></thead><tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)


def _render_iia_standard(s):
    """Render a single IIA standard entry — handles both plain and sectioned (TR) structures."""
    is_tr = s.get("topical_requirement", False) and s.get("sections")
    tr_marker = " · TR" if is_tr else ""
    with st.expander(f"**{s['standard_id']}**{tr_marker} — {s['title']}"):
        if is_tr:
            src_txt = s.get("source_guide", "")
            st.markdown(
                f'<div style="margin-bottom:10px">'
                f'<span style="background:rgba(79,126,248,0.15);color:#7fa8fb;border:1px solid rgba(79,126,248,0.35);border-radius:4px;padding:2px 9px;font-size:11px;font-weight:700">TR — Topical Requirement</span>'
                + (f' &nbsp;<span style="font-size:11px;color:#5a6488;font-style:italic">{src_txt}</span>' if src_txt else "")
                + '</div>',
                unsafe_allow_html=True,
            )
        st.markdown(f'<p style="font-size:13px;color:var(--text-secondary);line-height:1.8;margin-bottom:12px">{s["description"]}</p>', unsafe_allow_html=True)
        banking = s.get("banking_application", s.get("relevance_to_banking", ""))
        st.markdown(f"""
        <div style="background:rgba(34,211,165,0.06);border:1px solid rgba(34,211,165,0.18);border-radius:8px;padding:12px;margin-bottom:12px">
          <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;color:#22d3a5;margin-bottom:6px">🏦 Banking Application</div>
          <p style="margin:0;font-size:12.5px;color:var(--text-secondary);line-height:1.8">{banking}</p>
        </div>""", unsafe_allow_html=True)
        if is_tr:
            for sec in s["sections"]:
                sec_icon = sec.get("icon", "")
                with st.expander(f"{sec_icon} {sec['section_title']} — {len(sec['requirements'])} requirements", expanded=False):
                    for req in sec["requirements"]:
                        fw_badges = " &nbsp;".join(f'<span style="background:rgba(79,126,248,0.09);color:#7fa8fb;border:1px solid rgba(79,126,248,0.25);border-radius:3px;padding:1px 5px;font-size:10px">{f}</span>' for f in req.get("frameworks", []))
                        st.markdown(f"""
                        <div style="border-left:3px solid rgba(79,126,248,0.4);padding:10px 14px;margin-bottom:10px;background:rgba(79,126,248,0.04);border-radius:0 6px 6px 0">
                          <div style="font-size:11.5px;font-weight:700;color:#7fa8fb;margin-bottom:4px">{req['id']}</div>
                          <p style="margin:0 0 8px;font-size:12.5px;color:var(--text-secondary);line-height:1.8">{req['text']}</p>
                          <div style="font-size:10.5px;color:#5a6488">{fw_badges}</div>
                        </div>""", unsafe_allow_html=True)
        else:
            reqs = "".join(f"<li>{r}</li>" for r in s.get("key_requirements", []))
            st.markdown(f"""
            <div>
              <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;color:#7fa8fb;margin-bottom:6px">Key Requirements</div>
              <ul style="margin:0;padding-left:16px;font-size:12.5px;color:var(--text-secondary);line-height:1.8">{reqs}</ul>
            </div>""", unsafe_allow_html=True)


def _show_iia_standards():
    """Display IIA_STANDARDS_2024 in expandable cards."""
    for s in IIA_STANDARDS_2024:
        _render_iia_standard(s)


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
<div style="text-align:center;margin-bottom:32px;padding-top:1rem">
  <h1 style="font-size:42px;font-weight:800;letter-spacing:-1px;margin:0">🏦 AuditIQ</h1>
  <p style="font-size:16px;color:#8b95b8;font-style:italic;margin-top:4px;margin-bottom:0">
    From risk to insight — audit intelligence for private banking.
  </p>
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
    "📋  Audit Plan & Testing",
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

        with st.expander("🔴 A — Banking CVE Reference", expanded=True):
            st.markdown(
                f'<div class="section-title">A. Banking CVE Reference'
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{len(CVE_BANKING)} entries · 2021-2024</span></div>',
                unsafe_allow_html=True,
            )
            _cve_sc1, _cve_sc2, _cve_sc3 = st.columns([3, 1.2, 1.2])
            _cve_sq = _cve_sc1.text_input("Search CVEs", placeholder="Filter CVEs…", key="_cve_sq", label_visibility="collapsed")
            _cve_ssev = _cve_sc2.selectbox("Severity", _sev_opts, key="_cve_ssev", label_visibility="collapsed")
            _show_cve_static(search=_cve_sq, sev_filter=_cve_ssev)

        with st.expander("📰 B — Regulatory Frameworks Reference", expanded=False):
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

        with st.expander("🏦 C — Public Audit Recommendations", expanded=False):
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

        with st.expander("📅 D — Regulatory Calendar 2025–2026", expanded=False):
            _cal_juris  = sorted({e["jurisdiction"] for e in REGULATORY_CALENDAR})
            _cal_types  = sorted({e["type"] for e in REGULATORY_CALENDAR})
            _cal_prios  = ["High", "Medium", "Low"]
            st.markdown(
                f'<div class="section-title">D. Regulatory Calendar 2025–2026'
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">'
                f'{len(REGULATORY_CALENDAR)} entries · CH · EU · UK · SG · HK · Global</span></div>',
                unsafe_allow_html=True,
            )
            _cal_c1, _cal_c2, _cal_c3, _cal_c4 = st.columns([1.4, 2, 1.2, 1.2])
            _cal_jur  = _cal_c1.selectbox("Jurisdiction", ["All"] + _cal_juris, key="_cal_jur",  label_visibility="collapsed")
            _cal_type = _cal_c2.selectbox("Type",         ["All"] + _cal_types,  key="_cal_type", label_visibility="collapsed")
            _cal_prio = _cal_c3.selectbox("Priority",     ["All"] + _cal_prios,  key="_cal_prio", label_visibility="collapsed")
            _cal_year = _cal_c4.selectbox("Year",         ["All", "2025", "2026"], key="_cal_year", label_visibility="collapsed")
            _show_regulatory_calendar(
                jur_filter=_cal_jur, type_filter=_cal_type,
                prio_filter=_cal_prio, year_filter=_cal_year,
            )

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
        with st.expander("🔴 A — Latest CVEs — Financial Sector", expanded=True):
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

        with st.expander("📰 B — Regulatory Updates", expanded=False):
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

        with st.expander("🏦 C — Latest Public Audit Recommendations", expanded=False):
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
    _t1_mode = render_mode_toggle("mode_tab1")
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

    if _t1_mode == "static":
        # ── Static Reference Data mode ─────────────────────────────────────────
        _static_label()
        _t1_theme = _topic_to_theme(audit_topic) if audit_topic else "AML_KYC"
        _t1_theme = _t1_theme or "AML_KYC"
        _t1_theme_label = _t1_theme.replace("_", " ").title()

        with st.expander("🗺️ A — Risk Indicators", expanded=True):
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

        with st.expander("📋 B — Public Audit Recommendations", expanded=False):
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

        _rf_cats = sorted({e["category"] for e in HNWI_RED_FLAGS})
        with st.expander("🚨 C — HNWI Red Flags", expanded=False):
            st.markdown(
                f'<div class="section-title">C. HNWI Red Flags — Private Banking'
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">'
                f'{len(HNWI_RED_FLAGS)} red flags · AML · Fraud · Suitability · Tax · Conduct</span></div>',
                unsafe_allow_html=True,
            )
            _rf_c1, _rf_c2, _rf_c3 = st.columns([3, 1.5, 1.5])
            _rf_sq   = _rf_c1.text_input("Search red flags", placeholder="Filter red flags…", key="_rf_sq",   label_visibility="collapsed")
            _rf_scat = _rf_c2.selectbox("Category", ["All"] + _rf_cats,                        key="_rf_scat", label_visibility="collapsed")
            _rf_slv  = _rf_c3.selectbox("Risk Level", ["All", "Critical", "High", "Medium"],    key="_rf_slv",  label_visibility="collapsed")
            _show_red_flags(cat_filter=_rf_scat, level_filter=_rf_slv, search=_rf_sq)

        st.markdown("<div class='no-print' style='margin-top:1rem'>", unsafe_allow_html=True)
        _print_button()
        st.markdown("</div>", unsafe_allow_html=True)

    if _t1_mode == "live":
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

                    try:
                        p_xlsx = generate_risk_analysis_excel({
                            "topic": audit_topic,
                            "risks": st.session_state.t1_risks or [],
                            "regs": st.session_state.t1_regs or [],
                            "pub_recs": st.session_state.t1_pub_recs or [],
                        }, OUTPUT_DIR)
                        st.session_state.t1_xlsx = Path(p_xlsx).read_bytes()
                    except Exception:
                        pass
                    try:
                        p_pptx = generate_tab1_pptx({
                            "topic": audit_topic,
                            "jurs": jurisdictions,
                            "risks": st.session_state.t1_risks or [],
                            "regs": st.session_state.t1_regs or [],
                        }, OUTPUT_DIR)
                        st.session_state.t1_pptx2 = Path(p_pptx).read_bytes()
                    except Exception:
                        pass

                except Exception:
                    st.error("An error occurred. Please try again.")

    # Results (live mode only)
    if _t1_mode == "live" and (st.session_state.t1_risks or st.session_state.t1_regs):
        topic_lbl = st.session_state.t1_topic or "audit"
        st.markdown("---")

        # Risk Score Dashboard
        st.markdown('<div class="section-title">Risk Score</div>', unsafe_allow_html=True)
        _risk_score_display(st.session_state.t1_risks, len(st.session_state.t1_jurs or []))

        with st.expander("🗺️ A — Risk Mapping", expanded=True):
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

        with st.expander("📜 B — Applicable Regulations", expanded=False):
            st.markdown('<div class="section-title">B. Applicable Regulations</div>', unsafe_allow_html=True)
            st.markdown(_EXAMPLE_REGULATION, unsafe_allow_html=True)
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

        with st.expander("📋 C — Public Audit Recommendations", expanded=False):
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

        st.markdown("---")
        _t1_has_exports = st.session_state.t1_docx or st.session_state.t1_xlsx or st.session_state.t1_pptx2
        if _t1_has_exports:
            _e1, _e2, _e3, _e4 = st.columns([2, 2, 2, 1])
            if st.session_state.t1_docx:
                _e1.download_button(
                    "📄 Export Word",
                    data=st.session_state.t1_docx,
                    file_name=f"Risk_Analysis_{topic_lbl.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            if st.session_state.t1_xlsx:
                _e2.download_button(
                    "📊 Export Excel",
                    data=st.session_state.t1_xlsx,
                    file_name=f"Risk_Analysis_{topic_lbl.replace(' ', '_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            if st.session_state.t1_pptx2:
                _e3.download_button(
                    "📑 Export PPT",
                    data=st.session_state.t1_pptx2,
                    file_name=f"Risk_Analysis_{topic_lbl.replace(' ', '_')}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
            with _e4:
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
    _t2_mode = render_mode_toggle("mode_tab2")
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

    # IIA Topical Requirement banner
    _t2_topic_upper = (topic2 or "").upper()
    _t2_tr_match = None
    if any(k in _t2_topic_upper for k in ("CYBER", "ICT", "INFORMATION SECURITY", "DORA", "RANSOMWARE")):
        _t2_tr_match = next((s for s in IIA_STANDARDS_2024 if s["standard_id"] == "TR-2"), None)
        _t2_tr_label = "🔒 TR-Cyber"
    elif any(k in _t2_topic_upper for k in ("THIRD", "VENDOR", "OUTSOURC", "SUPPLY CHAIN")):
        _t2_tr_match = next((s for s in IIA_STANDARDS_2024 if s["standard_id"] == "TR-5"), None)
        _t2_tr_label = "🤝 TR-Third"
    if _t2_tr_match:
        _tr_src = _t2_tr_match.get("source_guide", "IIA User Guide 2025")
        _tr_keys = "".join(f"<li style='margin-bottom:3px'>{k}</li>" for k in _t2_tr_match.get("key_requirements", []))
        st.markdown(f"""
        <div style="background:rgba(234,179,8,0.07);border:1px solid rgba(234,179,8,0.35);border-left:4px solid #eab308;border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:16px">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <span style="background:rgba(234,179,8,0.18);color:#eab308;border:1px solid rgba(234,179,8,0.45);border-radius:4px;padding:2px 9px;font-size:11px;font-weight:700">⚠️ IIA TOPICAL REQUIREMENT APPLICABLE</span>
            <span style="font-size:12.5px;font-weight:600;color:#dde3f5">{_t2_tr_label} — {_t2_tr_match['title']}</span>
            <span style="font-size:11px;color:#5a6488;font-style:italic">{_tr_src} · Mandatory</span>
          </div>
          <p style="font-size:12px;color:#c8d0e8;margin:0 0 8px;line-height:1.8">This audit topic triggers a mandatory IIA Topical Requirement. All assurance engagements must cover the following key areas:</p>
          <ul style="margin:0;padding-left:16px;font-size:12px;color:#c8d0e8;line-height:1.9">{_tr_keys}</ul>
          <div style="margin-top:8px;font-size:11px;color:#5a6488">See Tab 3 → IIA Standards Reference → {_t2_tr_match['standard_id']} for full requirements with framework mapping.</div>
        </div>""", unsafe_allow_html=True)

    if _t2_mode == "static":
        # ── Static Reference Data mode ─────────────────────────────────────────
        _static_label()
        _t2_theme = _topic_to_theme(topic2) if topic2 else "CYBER_RISK"
        _t2_theme = _t2_theme or "CYBER_RISK"
        _t2_theme_label = _t2_theme.replace("_", " ").title()
        _n_tests = len(AUDIT_TESTS_LIBRARY.get(_t2_theme, []))
        _n_da = len(DATA_ANALYTICS_SCENARIOS.get(_t2_theme, []))

        st.markdown(_EXAMPLE_RATIONALE, unsafe_allow_html=True)

        with st.expander("📖 A — Rationale & Thematic Background", expanded=True):
            st.markdown(
                f'<div class="section-title">A. Rationale &amp; Thematic Background — {_t2_theme_label}</div>',
                unsafe_allow_html=True,
            )
            _show_thematic_background(_t2_theme)

        with st.expander("🗂️ B — Audit Tests Library", expanded=False):
            st.markdown(
                f'<div class="section-title">B. Audit Tests Library — {_t2_theme_label}'
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{_n_tests} tests available for this topic</span></div>',
                unsafe_allow_html=True,
            )
            st.markdown(_EXAMPLE_TEST, unsafe_allow_html=True)
            _tl_c1, _tl_c2, _tl_c3 = st.columns([3, 1.5, 1.8])
            _tl_sq = _tl_c1.text_input("Search tests", placeholder="Filter tests…", key="_tl_sq", label_visibility="collapsed")
            _tl_slv = _tl_c2.selectbox("Level", ["All", "Critical", "High", "Moderate"], key="_tl_slv", label_visibility="collapsed")
            _tl_stype = _tl_c3.selectbox("Type", ["All", "Standard", "Data Analytics"], key="_tl_stype", label_visibility="collapsed")
            _show_tests_library(_t2_theme, search=_tl_sq, level_filter=_tl_slv, type_filter=_tl_stype)

        with st.expander("📊 C — Data Analytics Scenarios", expanded=False):
            st.markdown(
                f'<div class="section-title">C. Data Analytics Scenarios — {_t2_theme_label}'
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

    if _t2_mode == "live":
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
    if _t2_mode == "live" and st.session_state.t2_rationale:
        topic2_lbl = st.session_state.t1_topic or topic2 or "audit"
        st.markdown("---")

        with st.expander("💡 1 — Rationale", expanded=True):
            st.markdown('<div class="section-title">1. Rationale</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{st.session_state.t2_rationale}</div>', unsafe_allow_html=True)
            _copy_button(st.session_state.t2_rationale, "t2_rat_copy")

        with st.expander("📖 2 — Background Information", expanded=False):
            st.markdown('<div class="section-title">2. Background Information</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{st.session_state.t2_background}</div>', unsafe_allow_html=True)
            _copy_button(st.session_state.t2_background or "", "t2_bg_copy")

        with st.expander("📋 3 — Audit Plan", expanded=False):
            st.markdown('<div class="section-title">3. Audit Plan</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{st.session_state.t2_org_plan}</div>', unsafe_allow_html=True)
            _copy_button(st.session_state.t2_org_plan or "", "t2_plan_copy")

        with st.expander("🧪 4 — Test List", expanded=False):
            n_tests = len(st.session_state.t2_tests or [])
            st.markdown(f'<div class="section-title">4. Test List — {n_tests} procedures</div>', unsafe_allow_html=True)
            filtered_tests = _filter_data(
                st.session_state.t2_tests or [],
                ["objective", "procedure", "population", "failure_criteria"],
                "t2_tests",
            )
            _tests_table(filtered_tests)

        with st.expander("📊 5 — Data Analytics Scenarios", expanded=False):
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
                    "📄 Export Word (.pptx)", data=pptx,
                    file_name=f"Audit_Plan_{topic2_lbl.replace(' ', '_')}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
            if xlsx:
                cb.download_button(
                    "📊 Export Excel (.xlsx)", data=xlsx,
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
    _t3_mode = render_mode_toggle("mode_tab3")
    st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)

    if _t3_mode == "static":
        # ── Static Reference Data mode ─────────────────────────────────────────
        _static_label()
        _t3_jurs = st.session_state.get("t1_jurs") or list(REGULATORY_FRAMEWORKS.keys())[:3]

        # Example finding
        st.markdown("---")
        st.markdown('<div class="section-title">📌 Audit Finding Template</div>', unsafe_allow_html=True)
        st.markdown(_EXAMPLE_FINDING, unsafe_allow_html=True)

        with st.expander("📚 A — IIA Standards Reference 2024", expanded=True):
            st.markdown(
                f'<div class="section-title">A. IIA Standards Reference — 2024'
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{len(IIA_STANDARDS_2024)} standards</span></div>',
                unsafe_allow_html=True,
            )
            st.markdown(_EXAMPLE_IIA_STD, unsafe_allow_html=True)
            _iia_sq = st.text_input("Search IIA Standards", placeholder="Filter standards…", key="_iia_sq", label_visibility="collapsed")
            _iia_filtered = IIA_STANDARDS_2024
            if _iia_sq:
                _qi = _iia_sq.lower()
                _iia_filtered = [s for s in IIA_STANDARDS_2024 if _qi in (s.get("title","") + s.get("description","") + s.get("standard_id","")).lower()]
            for _s in _iia_filtered:
                _render_iia_standard(_s)

        with st.expander("⚖️ B — Regulatory Reference Panel", expanded=False):
            _selected_jurs_display = " · ".join(_t3_jurs[:4])
            st.markdown(
                f'<div class="section-title">B. Regulatory Reference'
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{_selected_jurs_display}</span></div>',
                unsafe_allow_html=True,
            )
            st.markdown(_EXAMPLE_DORA, unsafe_allow_html=True)
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

    if _t3_mode == "live":
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

                    _obs_lines = [ln.strip("0123456789. \t-") for ln in observations.strip().splitlines() if ln.strip()]
                    _findings_export = [{"title": ln[:80], "rating": "High", "observation": ln, "risk": "", "recommendation": "", "owner": "", "due_date": ""} for ln in _obs_lines if ln]
                    try:
                        p_xlsx3 = generate_audit_findings_excel({"name": audit_name, "findings": _findings_export}, OUTPUT_DIR)
                        st.session_state.t3_xlsx = Path(p_xlsx3).read_bytes()
                    except Exception:
                        pass
                    try:
                        p_pptx3 = generate_report_pptx({"name": audit_name, "findings": _findings_export}, OUTPUT_DIR)
                        st.session_state.t3_pptx2 = Path(p_pptx3).read_bytes()
                    except Exception:
                        pass

                except Exception:
                    st.error("An error occurred. Please try again.")

        # Results (live mode only)
        if st.session_state.t3_report:
            res  = st.session_state.t3_report
            name = res.get("name", "report")
            st.markdown("---")

            with st.expander("📄 A — Audit Report", expanded=True):
                st.markdown('<div class="section-title">Audit Report</div>', unsafe_allow_html=True)
                text = res.get("text", "")
                if text:
                    st.markdown(f'<div class="output-box">{text}</div>', unsafe_allow_html=True)
                    _copy_button(text, "t3_report_copy")
                else:
                    st.info("Report content is available in the export file.")

                st.markdown("---")
                _t3_has_exports = res.get("docx_bytes") or st.session_state.t3_xlsx or st.session_state.t3_pptx2
                if _t3_has_exports:
                    _f1, _f2, _f3, _f4 = st.columns([2, 2, 2, 1])
                    if res.get("docx_bytes"):
                        _f1.download_button(
                            "📄 Export Word",
                            data=res["docx_bytes"],
                            file_name=f"Audit_Report_{name.replace(' ', '_')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        )
                    if st.session_state.t3_xlsx:
                        _f2.download_button(
                            "📊 Export Excel",
                            data=st.session_state.t3_xlsx,
                            file_name=f"Audit_Findings_{name.replace(' ', '_')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                    if st.session_state.t3_pptx2:
                        _f3.download_button(
                            "📑 Export PPT",
                            data=st.session_state.t3_pptx2,
                            file_name=f"Audit_Report_{name.replace(' ', '_')}.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        )
                    with _f4:
                        _print_button()
                else:
                    st.markdown("<div style='margin-top:0.5rem'>", unsafe_allow_html=True)
                    _print_button()
                    st.markdown("</div>", unsafe_allow_html=True)

            with st.expander("✏️ B — Targeted Revision", expanded=False):
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
