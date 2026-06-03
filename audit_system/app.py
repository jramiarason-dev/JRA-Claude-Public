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
import html as _html
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

_HERE = Path(__file__).parent.resolve()
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

st.set_page_config(
    page_title="AuditIQ",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Demo Mode content ─────────────────────────────────────────────────────────
_DEMO_CONTENT = {
    "template": "Third Party & Vendor Risk",
    "topic": "Third Party & Vendor Risk Management",
    "jurisdictions": ["CH / FINMA", "EU / DORA", "UK / FCA+PRA"],
    "entity": "🏦 Private Banking",
    "t1_summary": """<b>Executive Summary</b><br>
The Third Party & Vendor Risk assessment identifies <b>23 risk indicators</b> across 4 criticality tiers for the institution's outsourcing and vendor ecosystem. Critical gaps were identified in sub-outsourcing oversight, exit strategy documentation, and real-time SLA monitoring under DORA Article 28 requirements.<br><br>
<b>Top 5 Risk Indicators:</b><br>
• <span style='color:#ef4444;font-weight:600'>CRITICAL</span> — No documented exit strategy for Tier-1 cloud providers (AWS, Azure); lock-in risk not quantified<br>
• <span style='color:#ef4444;font-weight:600'>CRITICAL</span> — Sub-outsourcing chains not fully mapped; 3 critical vendors identified with undisclosed fourth-party dependencies<br>
• <span style='color:#f97316;font-weight:600'>HIGH</span> — SOC 2 Type II reports missing or expired for 7 of 19 critical vendors; last assessment >18 months<br>
• <span style='color:#f97316;font-weight:600'>HIGH</span> — Contracts with IT vendors lack mandatory audit rights clauses per FINMA Circ. 2023/1<br>
• <span style='color:#eab308;font-weight:600'>MODERATE</span> — Vendor performance SLA dashboards not integrated; manual quarterly reviews only<br><br>
<b>Regulatory Exposure:</b> DORA (EU 2022/2554) Art. 28–30 · FINMA Circ. 2023/1 · FCA SS2/21 · EBA/GL/2019/02""",
    "t2_rationale": """Third Party & Vendor Risk has been elevated to a Board-level priority following the DORA implementation deadline (Jan 2025) and a series of industry incidents linked to critical IT outsourcing failures. The institution's dependency on 3 hyper-scaler cloud providers and 19 critical vendors with cross-border data flows creates a concentrated systemic exposure requiring structured audit intervention.

Regulatory pressure has intensified: FINMA issued targeted review letters in Q3 2024 to 12 private banks regarding sub-outsourcing transparency, and the FCA's 2024 Operational Resilience review flagged vendor concentration as a sector-wide vulnerability. This audit addresses both first-line control adequacy and second-line oversight effectiveness.""",
    "t2_background": """The institution outsources approximately 68% of its IT infrastructure to third-party providers, with AWS (primary cloud), Temenos (core banking), and Bloomberg (market data) constituting Tier-1 critical dependencies. The vendor management framework was last comprehensively reviewed in 2021 and has not been updated to reflect DORA's enhanced ICT third-party risk requirements.

Key structural gaps include: (1) the absence of a centralised vendor register with real-time risk scoring; (2) no automated alerting for vendor financial distress or adverse media; (3) exit and substitution strategies documented for only 4 of 11 Tier-1 vendors. Internal audit's prior recommendation (2023-AUD-047) to implement a vendor risk platform remains open after 14 months.""",
    "t2_org_plan": """**Audit Organisation — Third Party & Vendor Risk**

**Engagement Lead:** Senior IT Audit Manager
**Team:** 2 IT auditors + 1 regulatory specialist (DORA)
**Duration:** 6 weeks (Fieldwork: weeks 1–4 | Reporting: weeks 5–6)
**Audit Universe Scope:** 19 critical vendors + vendor management function (IT Risk, Procurement, Legal)

**Work Programme:**
1. Vendor Register & Classification (Week 1) — Completeness, tiering criteria, DORA ICT mapping
2. Contractual Compliance (Week 1–2) — Audit rights, SLA terms, data portability, exit clauses
3. Due Diligence & Ongoing Monitoring (Week 2–3) — SOC 2 currency, cyber assessments, financial health
4. Sub-outsourcing & Fourth-Party Risk (Week 3) — Chain mapping, approval records, concentration
5. Exit Strategy Testing (Week 4) — Documentation, RTO/RPO feasibility, dry-run evidence
6. DORA Art. 28 Compliance Check (Week 4) — Contractual requirements checklist vs. binding register""",
    "t3_report": """# Internal Audit Report — Third Party & Vendor Risk Management
**Reference:** AUD-2025-TPR-001 | **Status:** DRAFT FOR DISCUSSION
**Audit Period:** Q1–Q2 2025 | **Fieldwork Completed:** May 2025

---

## Executive Summary
Internal Audit conducted a full-scope review of the institution's Third Party & Vendor Risk management framework across 19 critical vendors and the supporting governance structure. The review identified **4 Critical findings, 6 High findings, and 9 Moderate/Low observations**, representing a significant deterioration from the prior audit cycle (2023: 1 Critical, 4 High).

**Overall Audit Opinion: UNSATISFACTORY**

The vendor management framework does not yet meet DORA Article 28–30 requirements or FINMA Circular 2023/1 expectations. Immediate remediation is required for exit strategy documentation and sub-outsourcing transparency.

---

## Key Findings

### Finding 1 — CRITICAL: Absence of Viable Exit Strategies (DORA Art. 29)
Exit and substitution plans are documented for only 4 of 11 Tier-1 critical vendors. No dry-run exercises have been conducted. For AWS (primary cloud provider), the estimated migration effort exceeds 18 months with no interim continuity measures.
**Recommendation:** Complete exit strategy documentation for all Tier-1 vendors by Q3 2025; conduct tabletop exercise for top 3 critical vendors by Q4 2025.

### Finding 2 — CRITICAL: Undisclosed Sub-outsourcing Chains
Three critical vendors (anonymised: Vendor A, C, F) have material fourth-party dependencies not disclosed in contracts or communicated to the institution. These sub-processors handle production data, creating unassessed concentration and data residency risks.
**Recommendation:** Mandate contractual notification of material sub-outsourcing within 30 days; conduct emergency assessment of identified chains.

### Finding 3 — HIGH: Expired Due Diligence Documentation
SOC 2 Type II reports are missing or older than 18 months for 7 of 19 critical vendors. Three vendors have had adverse media events (financial distress, data breach) with no documented impact assessment.
**Recommendation:** Implement automated due diligence refresh workflow; escalate 3 vendors to enhanced monitoring.

---

## Management Response & Action Plan
Management accepts all findings. A Vendor Risk Remediation Programme has been initiated with a dedicated budget of CHF 450,000 for FY2025–2026, including procurement of a third-party risk management platform (target: Q3 2025).""",
    "dash_stats": {
        "risks_identified": 23,
        "audit_tests": 47,
        "frameworks": 6,
        "vendors_reviewed": 19,
    },
    "gen_steps_t1": [
        ("🔍", "Scanning THIRD_PARTY_RISK indicator library…", 0.6),
        ("📋", "Mapping to FINMA Circ. 2023/1 · DORA Art. 28 · FCA SS2/21…", 0.8),
        ("⚖️", "Scoring 23 risk indicators across 4 criticality tiers…", 0.7),
        ("📊", "Building risk heat-map and exposure matrix…", 0.5),
        ("✅", "Finalising executive summary…", 0.4),
    ],
    "gen_steps_t2": [
        ("🔍", "Loading audit tests library — THIRD_PARTY_RISK…", 0.5),
        ("🧠", "Structuring engagement rationale and background…", 0.8),
        ("📋", "Drafting 6-week work programme…", 0.7),
        ("⚖️", "Validating against DORA ICT risk requirements…", 0.6),
        ("✅", "Audit plan ready — 47 tests mapped…", 0.4),
    ],
    "gen_steps_t3": [
        ("📂", "Compiling findings from fieldwork evidence…", 0.6),
        ("⚖️", "Applying UNSATISFACTORY opinion criteria…", 0.5),
        ("📝", "Drafting management responses and action plans…", 0.8),
        ("🔍", "Cross-checking regulatory references…", 0.6),
        ("✅", "Audit report finalised — ready for review…", 0.4),
    ],
}

# ── Session state (init before CSS) ───────────────────────────────────────────
_SS_DEFAULTS = {
    # Dashboard
    "dash_cves": None, "dash_regs": None, "dash_audit_recs": None, "dash_updated": None,
    # Tab 1
    "t1_risks": None, "t1_regs": None, "t1_docx": None, "t1_topic": None,
    "t1_jurs": None, "t1_pub_recs": None,
    "topic_tab1": "",  # typed (not yet run) topic from Tab 1
    # Tab 2
    "t2_rationale": None, "t2_background": None, "t2_org_plan": None,
    "t2_tests": None, "t2_analytics": None, "t2_pptx": None, "t2_xlsx": None,
    # Tab 3
    "t3_report": None,
    "t1_xlsx": None, "t1_pptx2": None, "t3_xlsx": None, "t3_pptx2": None,
    "t1_pdf": None, "t2_pdf": None, "t3_pdf": None,
    "report_generated": False,
    "report_timestamp": None,
    "report_data": None,        # structured report dict assembled from static data
    "report_findings_raw": "",  # raw findings text persisted across interactions
    # UX
    "theme": "dark",
    "history": [],
    "_tpl_applied": False,
    "_tpl_name": "",
    "t1_show_form": True,
    "t2_show_form": True,
    "t1_jurs_pills": None,
    "t1_topic_in": "", "t2_topic_in": "",
    "t3_docs_analysis": None,
    "t3_observations": [],
    "t3_analysis_xlsx": None,
    "t3_analysis_pdf": None,
    "t4_recommendations": None,
    "t2_test_statuses": {},
    "t0_prior_recs": [],
    "t4_exec_summary": None,
    # Demo
    "demo_mode": False,
    # Auth
    "signed_in": False,
    # Help
    "help_open": False,
    "help_lang": "Français",
    # Stub UI features
    "voice_active": False,
    "last_voice_transcript": "",
    "cowork_open": False,
    "whats_new_dismissed": False,
    "active_tab": 0,
    "entity_type": "🏦 Private Banking",
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
        <li>&#9888; Manual screening only</li><li>&#9888; No adverse media check</li>
        <li>&#9888; Outdated sanctions lists (&gt;30 days)</li><li>&#9888; No source of wealth documentation</li>
      </ul>
    </div>
  </div>
  <div style="margin-top:10px;font-size:11px;color:#5a6488">Ref: FINMA-RS 2011/1 &middot; FATF R.12</div>
</div>
"""

_EXAMPLE_REGULATION = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="font-size:13px;font-weight:600;color:#dde3f5;margin-bottom:4px">🇨🇭 CH/FINMA &mdash; FINMA-RS 2011/1 &mdash; Anti-Money Laundering Ordinance</div>
  <div style="font-size:11px;color:#8392bb;margin-bottom:10px">FINMA &middot; 2011 (updated 2020) &middot; AML, KYC, PEP, Correspondent Banking</div>
  <div style="font-size:10.5px;font-weight:700;color:#8392bb;text-transform:uppercase;margin-bottom:5px">Key Requirements</div>
  <ul style="margin:0;padding-left:14px;font-size:12px;color:#c8d0e8;line-height:1.9">
    <li>Risk-based CDD for all clients</li><li>EDD mandatory for PEPs and HNWI &gt;CHF 1M</li>
    <li>Annual review of high-risk relationships</li><li>Transaction monitoring thresholds defined</li>
    <li>10-year document retention</li>
  </ul>
  <div style="margin-top:8px;font-size:11px;color:#5a6488">Applies to: AML &middot; KYC &middot; PEP &middot; Correspondent Banking</div>
</div>
"""

_EXAMPLE_PUB_REC = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap">
    <span style="font-size:13px;font-weight:600;color:#818cf8">FATF Guidance &mdash; Private Banking</span>
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
  <div style="font-size:13px;font-weight:600;color:#dde3f5;margin-bottom:10px">💡 RATIONALE &mdash; Cyber Risk Audit 2025</div>
  <div style="font-size:12px;color:#c8d0e8;line-height:1.85;margin-bottom:8px"><strong style="color:#818cf8">Why now:</strong> DORA entered into force January 2025. FINMA observed a 40% increase in cyber incidents in Swiss private banks (2024). MAS TRM 2021 requires annual ICT audit.</div>
  <div style="font-size:12px;color:#c8d0e8;line-height:1.85;margin-bottom:8px"><strong style="color:#818cf8">Strategic context:</strong> Private banks managing HNWI data face elevated threats from ransomware and social engineering. Cloud migration increases attack surface across all jurisdictions.</div>
  <div style="font-size:12px;color:#c8d0e8;line-height:1.85"><strong style="color:#818cf8">Benchmark:</strong> 78% of peer institutions suffered at least one cyber incident in 2023 (BCBS Sound Practices Survey).</div>
</div>
"""

_EXAMPLE_TEST = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap">
    <span style="color:#818cf8;font-weight:700;font-size:13px">T011</span>
    <span style="background:rgba(99,102,241,0.15);color:#818cf8;border:1px solid rgba(99,102,241,0.35);border-radius:4px;padding:1px 7px;font-size:11px;font-weight:600">📊 DA</span>
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
    <div><span style="color:#8392bb;font-weight:600">Data Sources:</span> <span style="color:#c8d0e8">AD logs &middot; SIEM (Splunk) &middot; PAM system</span></div>
    <div><span style="color:#8392bb;font-weight:600">Analysis Type:</span> <span style="color:#c8d0e8">Anomaly Detection</span></div>
  </div>
  <ul style="margin:0;padding-left:14px;font-size:11.5px;color:#c8d0e8;line-height:1.9">
    <li>Logins outside business hours (22h&ndash;6h)</li><li>Bulk data exports &gt;500 records</li>
    <li>Lateral movement across network segments</li><li>Failed logins &gt;5 attempts</li>
  </ul>
  <div style="margin-top:8px;font-size:11px;color:#5a6488">Tools: <span style="color:#818cf8">Python (pandas) / Splunk / SQL</span></div>
</div>
"""

_EXAMPLE_FINDING = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;flex-wrap:wrap">
    <span style="background:rgba(249,115,22,0.15);color:#f97316;border:1px solid rgba(249,115,22,0.4);border-radius:4px;padding:2px 10px;font-size:12px;font-weight:700">FINDING #1 &mdash; 🔴 HIGH</span>
    <span style="font-size:13px;font-weight:600;color:#dde3f5">AML/KYC &mdash; Inadequate Source of Wealth Documentation</span>
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
    <div style="font-size:11px;color:#5a6488">Ref: <span style="color:#818cf8">FINMA-RS 2011/1 §15 &middot; FATF R.10</span> &nbsp;&middot;&nbsp; Rating: <span style="color:#f97316;font-weight:600">High</span> &nbsp;&middot;&nbsp; Due: <span style="color:#22d3a5">Q2 2025</span></div>
  </div>
</div>
"""

_EXAMPLE_IIA_STD = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="font-size:13px;font-weight:600;color:#dde3f5;margin-bottom:4px">IIA GIAS 2024 &mdash; TR-2: Cybersecurity (Topical Requirement)</div>
  <div style="font-size:11px;color:#8392bb;margin-bottom:10px">Effective: January 9, 2024 &middot; Domain: Topical Requirements</div>
  <p style="font-size:12.5px;color:#c8d0e8;line-height:1.85;margin:0 0 8px;font-style:italic">"Internal auditors must evaluate cybersecurity governance, risk management, and controls as a core component of the audit universe. Given the escalating threat landscape, cybersecurity must be assessed with specialist knowledge or co-sourced expertise."</p>
  <div style="font-size:11.5px;color:#8392bb">Banking Application: <span style="color:#c8d0e8">DORA (effective Jan 2025) requires ICT risk assessment, major incident reporting, and third-party ICT oversight. Internal audit must verify DORA compliance for EU-facing operations.</span></div>
</div>
"""

_EXAMPLE_DORA = f"""
<div style="{_EX_S}">
{_EX_L}
  <div style="font-size:13px;font-weight:600;color:#dde3f5;margin-bottom:4px">🇪🇺 EU &mdash; DORA (Digital Operational Resilience Act) &mdash; In force January 2025</div>
  <div style="font-size:11.5px;color:#8392bb;margin-bottom:10px">European Parliament &middot; 2022/2554 &middot; ICT, Cyber, Third-Party Risk</div>
  <div style="font-size:10.5px;font-weight:700;color:#8392bb;text-transform:uppercase;margin-bottom:5px">Key Requirements</div>
  <ul style="margin:0;padding-left:14px;font-size:12px;color:#c8d0e8;line-height:1.9">
    <li>ICT risk management framework mandatory</li><li>Third-party ICT provider oversight (Art. 28&ndash;30)</li>
    <li>Major incident reporting within 4 hours</li><li>Annual TLPT (Threat-Led Penetration Testing)</li>
    <li>Digital resilience testing programme</li>
  </ul>
  <div style="margin-top:8px;font-size:11.5px;color:#8392bb">Audit Focus: <span style="color:#c8d0e8">ICT governance &middot; vendor contracts &middot; incident response &middot; TLPT evidence</span></div>
</div>
"""

# ── Theme CSS injection (dark only) ───────────────────────────────────────────

# Part 1: CSS variables
_theme_vars = """
    :root {
      --bg-main:         #07090f;
      --bg-app:          #07090f;
      --bg-primary:      #07090f;
      --bg-secondary:    #0b0f1a;
      --bg-card:         #0d1117;
      --bg-card-hover:   #131925;
      --bg-input:        #0d1117;
      --bg-sidebar:      #080b12;
      --border-subtle:   rgba(255,255,255,0.06);
      --border-medium:   rgba(255,255,255,0.10);
      --border-input:    rgba(255,255,255,0.08);
      --border-accent:   rgba(99,102,241,0.30);
      --border-divider:  rgba(255,255,255,0.05);
      --text-primary:    #eef2ff;
      --text-secondary:  #94a3b8;
      --text-muted:      #4a5568;
      --text-accent:     #a5b4fc;
      --text-label:      #8392bb;
      --accent-primary:  #6366f1;
      --accent-secondary:#818cf8;
      --accent-hover:    #818cf8;
      --accent-glow:     rgba(99,102,241,0.15);
      --accent-blue:     #6366f1;
      --shadow-card:     0 1px 3px rgba(0,0,0,0.4), 0 4px 16px rgba(0,0,0,0.25);
      --shadow-elevated: 0 2px 8px rgba(0,0,0,0.5), 0 12px 32px rgba(0,0,0,0.3);
      --radius-sm:       8px;
      --radius-md:       12px;
      --radius-lg:       16px;
      --critical:        #ef4444;
      --critical-bg:     rgba(239,68,68,0.10);
      --high:            #f97316;
      --high-bg:         rgba(249,115,22,0.10);
      --moderate:        #eab308;
      --moderate-bg:     rgba(234,179,8,0.10);
      --low:             #22c55e;
      --low-bg:          rgba(34,197,94,0.10);
      --tab-inactive:          #5a6488;
      --tab-active:            #818cf8;
      --tab-active-border:     #6366f1;
      --btn-primary-bg:        linear-gradient(135deg,#6366f1 0%,#4f46e5 100%);
      --btn-secondary-bg:      rgba(99,102,241,0.14);
      --btn-secondary-color:   #818cf8;
      --btn-secondary-border:  rgba(99,102,241,0.25);
      --ctx-pill-bg:           rgba(34,211,165,0.07);
      --ctx-pill-border:       rgba(34,211,165,0.18);
      --ctx-pill-color:        #22d3a5;
      --output-box-bg:         #0d1117;
      --output-box-border:     rgba(255,255,255,0.06);
      --output-box-text:       #eef2ff;
      --section-title-color:   #eef2ff;
      --footer-color:          #4a5568;
      --tbl-row-border:        rgba(255,255,255,0.05);
      --sidebar-header-color:  #4a5568;
    }
    """

st.markdown(f"<style>{_theme_vars}</style>", unsafe_allow_html=True)
# Part 2: Static CSS using var() — no f-string needed
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, p, span, div, label, input, textarea, select, button {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
h1, h2, h3 {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  letter-spacing: -0.5px;
}
.stApp {
  background: var(--bg-main) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}
.main .block-container {
  padding: 2rem 2.5rem 4rem !important;
  max-width: 1100px !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: var(--bg-sidebar) !important;
  border-right: 1px solid var(--border-subtle) !important;
}
section[data-testid="stSidebar"] .stMarkdown p { color: var(--text-secondary); font-size: 13px; }

/* ── Tabs — glassmorphism pill style ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-card) !important;
  border-radius: 12px !important;
  padding: 4px !important;
  border: 1px solid var(--border-subtle) !important;
  gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 8px !important;
  color: var(--text-muted) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  padding: 8px 16px !important;
  border: none !important;
  transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(99,102,241,0.20) 0%, rgba(99,102,241,0.10) 100%) !important;
  color: var(--accent-hover) !important;
  font-weight: 600 !important;
  box-shadow: 0 1px 0 rgba(99,102,241,0.4), inset 0 1px 0 rgba(99,102,241,0.1) !important;
}
.stTabs [data-baseweb="tab"]:hover {
  background: rgba(255,255,255,0.04) !important;
  color: var(--text-secondary) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="select"] > div:first-child {
  background: var(--bg-input) !important;
  border: 1px solid var(--border-medium) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
  font-size: 13.5px !important;
  transition: border-color 0.15s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: rgba(99,102,241,0.5) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
  outline: none !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label, .stMultiSelect label,
label[data-testid="stWidgetLabel"] p {
  font-size: 12px !important;
  font-weight: 600 !important;
  color: var(--text-secondary) !important;
  letter-spacing: 0.3px !important;
  text-transform: uppercase !important;
}
/* ── Labels ── */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
  font-size: 12px !important;
  font-weight: 600 !important;
  letter-spacing: 0.04em !important;
  text-transform: uppercase !important;
  color: var(--text-muted) !important;
  margin-bottom: 4px !important;
}
::placeholder { color: var(--text-muted) !important; font-style: italic; }

/* ── Buttons ── */
div[data-testid="stButton"] > button {
  border-radius: var(--radius-sm) !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  letter-spacing: 0.01em !important;
  transition: all 0.15s ease !important;
  border: 1px solid var(--border-medium) !important;
  background: rgba(255,255,255,0.04) !important;
  color: var(--text-secondary) !important;
}
div[data-testid="stButton"] > button:hover {
  background: rgba(255,255,255,0.08) !important;
  border-color: rgba(255,255,255,0.16) !important;
  color: var(--text-primary) !important;
}
div[data-testid="stButton"] > button[kind="primary"],
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
  border: none !important;
  color: #fff !important;
  box-shadow: 0 2px 12px rgba(99,102,241,0.35) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
  box-shadow: 0 4px 20px rgba(99,102,241,0.5) !important;
  transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:active { transform: translateY(0) !important; }
div[data-testid="stButton"] > button[kind="primary"]:disabled {
  background: #1a1f32 !important; color: #3a4566 !important;
}
div[data-testid="stDownloadButton"] button {
  border-radius: var(--radius-sm) !important;
  font-weight: 600 !important;
  font-size: 12.5px !important;
  border: 1px solid var(--border-medium) !important;
  background: rgba(255,255,255,0.04) !important;
  color: var(--text-secondary) !important;
  min-height: 36px !important;
  transition: all 0.15s ease !important;
}
div[data-testid="stDownloadButton"] button:hover {
  background: rgba(255,255,255,0.08) !important;
  color: var(--text-primary) !important;
}
/* Uniform export bar button heights */
div[data-testid="stButton"] button { min-height: 36px !important; }
.wk-btn button {
  background: rgba(255,102,0,.08) !important;
  border: 1px solid rgba(255,102,0,.25) !important;
  color: #ff8533 !important;
  border-radius: 8px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  min-height: 36px !important;
}
.wk-btn button:hover {
  background: rgba(255,102,0,.15) !important;
  border-color: rgba(255,102,0,.45) !important;
}
div[data-testid="stFileUploader"] {
  border: 1px dashed var(--border-medium) !important;
  border-radius: 10px !important; background: var(--bg-input) !important;
}
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
  border:1px solid rgba(239,68,68,0.35); border-radius:20px; padding:2px 8px;
  font-size:11px; font-weight:700; white-space:nowrap; }
.badge-high { display:inline-block; background:rgba(249,115,22,0.12); color:#f97316;
  border:1px solid rgba(249,115,22,0.32); border-radius:20px; padding:2px 8px;
  font-size:11px; font-weight:700; white-space:nowrap; }
.badge-medium { display:inline-block; background:rgba(234,179,8,0.10); color:#eab308;
  border:1px solid rgba(234,179,8,0.28); border-radius:20px; padding:2px 8px;
  font-size:11px; font-weight:700; white-space:nowrap; }
.badge-open { display:inline-block; background:rgba(34,211,165,0.10); color:#22d3a5;
  border:1px solid rgba(34,211,165,0.28); border-radius:20px; padding:2px 8px;
  font-size:11px; font-weight:600; white-space:nowrap; }
.badge-info { display:inline-block; background:rgba(99,102,241,0.10); color:#818cf8;
  border:1px solid rgba(99,102,241,0.28); border-radius:20px; padding:2px 8px;
  font-size:11px; font-weight:600; white-space:nowrap; }

/* ── Risk cards — glassmorphism ── */
.risk-card {
  background: rgba(15,21,32,0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 12px;
  border: 1px solid var(--border-subtle);
  padding: 16px;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
  margin-bottom: 12px;
}
.risk-card:hover {
  transform: translateY(-2px);
  border-color: var(--border-accent);
  box-shadow: 0 8px 32px rgba(99,102,241,0.08);
}
.risk-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
}
.risk-card-critical::before { background: linear-gradient(90deg, #ef4444, transparent); }
.risk-card-high::before     { background: linear-gradient(90deg, #f97316, transparent); }
.risk-card-moderate::before { background: linear-gradient(90deg, #eab308, transparent); }

/* ── Progress bar ── */
.progress-bar-wrap { display: flex; align-items: center; gap: 0; margin: 0.6rem 0 1.6rem; }
.pb-step {
  display: flex; align-items: center; gap: 8px;
  font-size: 12.5px; font-weight: 500; padding: 7px 16px;
  border-radius: 20px; transition: all 0.2s;
}
.pb-step.done { background: rgba(34,211,165,0.10); color: #22d3a5; border: 1px solid rgba(34,211,165,0.25); }
.pb-step.active { background: rgba(99,102,241,0.12); color: #818cf8; border: 1px solid rgba(99,102,241,0.30); }
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

/* ── Expanders ── */
.streamlit-expanderHeader {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 8px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: var(--text-secondary) !important;
  padding: 12px 16px !important;
  transition: all 0.2s ease !important;
}
.streamlit-expanderHeader:hover {
  border-color: var(--border-accent) !important;
  color: var(--text-accent) !important;
  background: var(--bg-card-hover) !important;
}
.streamlit-expanderContent {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-top: none !important;
  border-radius: 0 0 8px 8px !important;
  padding: 16px !important;
}

/* ── History item ── */
.hist-item {
  background: var(--bg-card); border: 1px solid var(--border-subtle);
  border-radius: 8px; padding: 8px 12px; margin-bottom: 6px; font-size: 12px; cursor: pointer;
}
.hist-topic { color: var(--text-primary); font-weight: 600; }
.hist-meta { color: var(--text-muted); font-size: 11px; margin-top: 2px; }

/* ── Footer ── */
.footer { font-size: 11px; color: var(--footer-color); text-align: center; margin-top: 2.5rem; letter-spacing: 0.3px; }

/* ── Mode toggle radio — overridden by utility classes below ── */

/* ── Sidebar section cards ── */
.sidebar-section {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 10px; padding: 12px; margin-bottom: 12px;
}
.sidebar-section-title {
  font-size: 10px; font-weight: 700; letter-spacing: 1.5px;
  color: var(--sidebar-header-color); text-transform: uppercase; margin-bottom: 10px;
}

/* ── Section header ── */
.section-header {
  display: flex; align-items: center; gap: 10px;
  margin: 24px 0 16px 0; padding-bottom: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.section-header-icon {
  width: 32px; height: 32px;
  background: rgba(99,102,241,0.10);
  border: 1px solid rgba(99,102,241,0.20);
  border-radius: 8px; display: flex;
  align-items: center; justify-content: center; flex-shrink: 0;
}
.section-count-badge {
  background: rgba(99,102,241,0.12); color: #6366f1;
  border: 1px solid rgba(99,102,241,0.2); border-radius: 20px;
  padding: 2px 8px; font-size: 11px; font-weight: 600; margin-left: 8px;
}

/* ── Loading spinner ── */
@keyframes spin { to { transform: rotate(360deg); } }
.loading-spinner {
  display: flex; align-items: center; gap: 12px;
  background: rgba(99,102,241,0.06);
  border: 1px solid rgba(99,102,241,0.15);
  border-radius: 10px; padding: 16px 20px; margin: 16px 0;
}
.loading-spinner-dot {
  width: 16px; height: 16px;
  border: 2px solid rgba(99,102,241,0.2);
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  flex-shrink: 0;
}

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

/* ── Sidebar styling ── */
section[data-testid="stSidebar"] {
  background: var(--bg-sidebar) !important;
  border-right: 1px solid var(--border-subtle) !important;
  width: 248px !important;
  min-width: 248px !important;
}
section[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="collapsedControl"] { display: none !important; }
/* Remove Streamlit default main-area left padding (sidebar already takes space) */
.main .block-container { padding-left: 1.5rem !important; }

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

/* ── Metric cards ── */
[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
  padding: 20px 24px !important;
  box-shadow: var(--shadow-card) !important;
  transition: box-shadow 0.2s ease !important;
}
[data-testid="stMetric"]:hover {
  box-shadow: var(--shadow-elevated) !important;
}
[data-testid="stMetric"] label {
  font-size: 11px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: .08em !important;
  color: var(--text-muted) !important;
}
[data-testid="stMetricValue"] > div {
  font-size: 30px !important;
  font-weight: 800 !important;
  color: var(--text-primary) !important;
  letter-spacing: -0.04em !important;
}
[data-testid="stMetricDelta"] {
  font-size: 12px !important;
  font-weight: 600 !important;
  border-radius: 6px !important;
  padding: 2px 6px !important;
}

/* ── Multiselect tags ── */
.stMultiSelect [data-baseweb="tag"] {
  background: rgba(99,102,241,.15) !important;
  border: 1px solid rgba(99,102,241,.3) !important;
  color: #818cf8 !important;
  border-radius: 6px !important;
  font-size: 12px !important;
}
.stMultiSelect [data-baseweb="tag"] span { color: #818cf8 !important; }
.stMultiSelect [data-baseweb="tag"] button { color: #818cf8 !important; opacity: .7; }
.stMultiSelect [data-baseweb="select"] > div {
  background: var(--bg-input) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 8px !important;
}

/* ── Native progress bar ── */
.stProgress > div > div {
  background: rgba(255,255,255,.06) !important;
  border-radius: 6px !important;
  height: 6px !important;
}
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, #6366f1, #818cf8) !important;
  border-radius: 6px !important;
}

/* ── Checkboxes ── */
.stCheckbox label span { color: var(--text-secondary) !important; font-size: 13px !important; }
.stCheckbox [data-baseweb="checkbox"] span {
  border-color: var(--border-medium) !important;
  background: rgba(255,255,255,.03) !important;
  border-radius: 4px !important;
}

/* ── Slider ── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
  background: var(--accent-primary) !important;
  border-color: var(--accent-primary) !important;
  box-shadow: 0 0 0 4px var(--accent-glow) !important;
}

/* ── Expander (Streamlit 1.58 selectors) ── */
[data-testid="stExpander"] {
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
  background: var(--bg-card) !important;
  overflow: hidden !important;
  box-shadow: var(--shadow-card) !important;
  margin-bottom: 10px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] details > summary {
  background: var(--bg-card) !important;
  color: var(--text-secondary) !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  padding: 12px 16px 12px 36px !important;
  list-style: none !important;
  display: block !important;
  position: relative !important;
  cursor: pointer !important;
  letter-spacing: 0.01em !important;
}
/* Nuclear icon suppression: hide every child that is not the label p/span */
[data-testid="stExpander"] summary::-webkit-details-marker { display:none !important; }
[data-testid="stExpander"] summary::marker { content:"" !important; }
/* Hide ALL direct children (icons) and then re-show only the label */
[data-testid="stExpander"] summary > * {
  display: none !important;
}
/* Re-show label elements — Streamlit puts the label in p or span[data-testid] */
[data-testid="stExpander"] summary > p,
[data-testid="stExpander"] summary > div > p,
[data-testid="stExpander"] summary [data-testid="StyledLabelText"],
[data-testid="stExpander"] summary [class*="Label"],
[data-testid="stExpander"] summary [class*="label"] {
  display: inline !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: var(--text-secondary) !important;
}
/* CSS arrow indicator replacing the icon */
[data-testid="stExpander"] summary::before,
[data-testid="stExpander"] details > summary::before {
  content: "›" !important;
  position: absolute !important;
  left: 12px !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  font-size: 16px !important;
  font-weight: 700 !important;
  color: var(--text-muted) !important;
  transition: transform .15s !important;
  font-family: 'Inter', sans-serif !important;
}
[data-testid="stExpander"] details[open] > summary::before {
  content: "⌄" !important;
  transform: translateY(-60%) !important;
}
[data-testid="stExpander"] summary:hover {
  background: var(--bg-card-hover) !important;
  color: var(--text-accent) !important;
}
[data-testid="stExpander"] > div > div {
  padding: 12px 16px 16px !important;
}

/* ── Selectbox / dropdown menu ── */
[data-baseweb="popover"] [role="listbox"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 10px !important;
  box-shadow: 0 8px 32px rgba(0,0,0,.45) !important;
}
[data-baseweb="option"] {
  background: transparent !important;
  color: var(--text-secondary) !important;
  font-size: 13px !important;
}
[data-baseweb="option"]:hover, [data-baseweb="option"][aria-selected="true"] {
  background: rgba(99,102,241,.1) !important;
  color: var(--text-primary) !important;
}

/* ── Code blocks ── */
.stCodeBlock code, pre {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 8px !important;
  font-size: 12.5px !important;
  color: #c9cde0 !important;
}

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
  border-radius: 10px !important;
  overflow: hidden !important;
  border: 1px solid var(--border-subtle) !important;
}

/* ── Info / warning / success / error boxes — overridden by utility classes ── */

/* ── Column vertical spacing ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
  gap: 0 !important;
}

/* ── Tab panel content ── */
[data-testid="stTabsContent"] {
  padding-top: 1.2rem !important;
}

/* ── Agent card layout ── */
.agent-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px 28px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-card);
}
.agent-badge-pill {
  display: inline-block;
  background: rgba(99,102,241,0.15);
  color: #818cf8;
  border: 1px solid rgba(99,102,241,0.35);
  border-radius: 20px;
  padding: 3px 12px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.agent-status-pill {
  display: inline-block;
  border-radius: 20px;
  padding: 2px 10px;
  font-size: 11px;
  font-weight: 600;
  margin-right: 6px;
}
.agent-status-ready {
  background: rgba(34,211,165,0.12);
  color: #22d3a5;
  border: 1px solid rgba(34,211,165,0.3);
}
.agent-status-live {
  background: rgba(249,115,22,0.12);
  color: #f97316;
  border: 1px solid rgba(249,115,22,0.3);
}
.param-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-muted);
  margin-bottom: 6px;
}
.jur-pills-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}
.gen-btn-wrap {
  margin-top: 20px;
}
div[data-testid="stButton"].gen-btn > button {
  background: linear-gradient(135deg, #6366f1, #818cf8) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  padding: 14px 32px !important;
  min-height: 52px !important;
  width: 100% !important;
  letter-spacing: 0.3px !important;
}
div[data-testid="stButton"].gen-btn > button:hover {
  opacity: 0.9 !important;
}
div[data-testid="stButton"].back-btn > button {
  background: rgba(255,255,255,0.05) !important;
  color: var(--text-secondary) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 8px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
}

/* ── Page section header ── */
.page-section-header {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  margin: 28px 0 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-subtle);
}

/* ── Stat grid card ── */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}
.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 18px 20px;
  box-shadow: var(--shadow-card);
}
.stat-card-value {
  font-size: 26px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin-bottom: 4px;
}
.stat-card-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--text-muted);
}

/* ── Nav item improvements ── */
.nav-status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-left: auto;
  flex-shrink: 0;
}

/* ── Section divider ── */
.section-divider {
  border: none;
  border-top: 1px solid var(--border-subtle);
  margin: 24px 0;
}

/* ── Info banner ── */
.info-banner {
  background: rgba(99,102,241,0.06);
  border: 1px solid rgba(99,102,241,0.15);
  border-radius: var(--radius-sm);
  padding: 10px 16px;
  font-size: 12.5px;
  color: var(--text-secondary);
  margin-bottom: 16px;
  line-height: 1.6;
}

/* ── Radio button group ── */
div[data-testid="stRadio"] > div {
  gap: 8px !important;
  flex-wrap: wrap !important;
}
div[data-testid="stRadio"] label {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-medium) !important;
  border-radius: var(--radius-sm) !important;
  padding: 6px 16px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: var(--text-secondary) !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
  background: rgba(99,102,241,0.15) !important;
  border-color: rgba(99,102,241,0.4) !important;
  color: #a5b4fc !important;
}
div[data-testid="stRadio"] input[type="radio"] {
  display: none !important;
}

/* ── Alert boxes ── */
[data-testid="stAlert"] {
  border-radius: var(--radius-sm) !important;
  border-width: 1px !important;
  font-size: 13px !important;
  padding: 10px 16px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.18); }

/* ── Caption text ── */
[data-testid="stCaptionContainer"] p {
  font-size: 11.5px !important;
  color: var(--text-muted) !important;
  line-height: 1.6 !important;
}

/* ── Utility button active glow ─────────────────────────────── */
.util-voice-active button, .util-cowork-active button, .util-help-active button {
  background: rgba(99,102,241,0.18) !important;
  border: 1px solid rgba(99,102,241,0.5) !important;
  color: #818cf8 !important;
  box-shadow: 0 0 8px rgba(99,102,241,0.35) !important;
}

/* ── Demo Mode button ── */
.demo-btn button {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  color: #94a3b8 !important;
  border-radius: 8px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  width: 100% !important;
}
.demo-btn-active button {
  background: rgba(255,140,0,.15) !important;
  border: 1px solid rgba(255,140,0,.4) !important;
  color: #ffaa33 !important;
  border-radius: 8px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  width: 100% !important;
}

/* ── Demo stat cards ── */
@keyframes countup {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.demo-stat-card {
  animation: countup 0.6s ease forwards;
  background: rgba(99,102,241,.08);
  border: 1px solid rgba(99,102,241,.2);
  border-radius: 12px;
  padding: 16px 20px;
  text-align: center;
}
.demo-stat-number {
  font-size: 32px;
  font-weight: 800;
  color: #818cf8;
  font-family: 'Plus Jakarta Sans', sans-serif;
}
.demo-stat-label {
  font-size: 11px;
  color: #4a5568;
  text-transform: uppercase;
  letter-spacing: .08em;
  margin-top: 4px;
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
try:
    from data import (
        REGULATORY_FRAMEWORKS, AUDIT_TEMPLATES as _DATA_TEMPLATES,
        RISK_INDICATORS, PUBLIC_AUDIT_RECOMMENDATIONS,
        CVE_BANKING, IIA_STANDARDS_2024, DATA_ANALYTICS_SCENARIOS,
        AUDIT_TESTS_LIBRARY, TOPIC_THEME_MAP, TOPIC_KEY_MAPPING,
        THEMATIC_BACKGROUND, REGULATORY_CALENDAR, HNWI_RED_FLAGS,
        MANAGEMENT_ACTION_TEMPLATES, ENTITY_CONTEXT,
    )
except ImportError as _data_err:
    st.error(f"Failed to load data module: {_data_err}")
    st.stop()

# ── Global constants ───────────────────────────────────────────────────────────

_ENTITY_COLORS = {
    "🏦 Private Banking":                   ("#0a2540", "#818cf8"),
    "📊 Asset Management":                  ("#0a2a12", "#4ade80"),
    "🏢 Management Company (ManCo)":        ("#2a1f0a", "#f59e0b"),
    "🔀 Alternative Investment (PE/RE/HF)": ("#1e0a2a", "#c084fc"),
    "🏛️ Group / Holding":                   ("#0a2028", "#22d3ee"),
}

_ENTITY_KEYS = {
    "🏦 Private Banking":                   "PRIVATE_BANKING",
    "📊 Asset Management":                  "ASSET_MANAGEMENT",
    "🏢 Management Company (ManCo)":        "MANAGEMENT_COMPANY",
    "🔀 Alternative Investment (PE/RE/HF)": "ALTERNATIVE_INVESTMENT",
    "🏛️ Group / Holding":                   "GROUP_HOLDING",
}

# Per-entity full color themes (accent + derived tones)
_ENTITY_THEMES = {
    "🏦 Private Banking": {
        "primary": "#6366f1", "hover": "#818cf8",
        "glow": "rgba(99,102,241,0.18)",
        "bg_btn": "linear-gradient(135deg,#6366f1 0%,#4f46e5 100%)",
        "sec_bg": "rgba(99,102,241,0.12)", "sec_color": "#818cf8",
        "sec_border": "rgba(99,102,241,0.22)",
    },
    "📊 Asset Management": {
        "primary": "#22c55e", "hover": "#4ade80",
        "glow": "rgba(34,197,94,0.18)",
        "bg_btn": "linear-gradient(135deg,#22c55e 0%,#16a34a 100%)",
        "sec_bg": "rgba(34,197,94,0.12)", "sec_color": "#4ade80",
        "sec_border": "rgba(34,197,94,0.22)",
    },
    "🏢 Management Company (ManCo)": {
        "primary": "#f59e0b", "hover": "#fbbf24",
        "glow": "rgba(245,158,11,0.18)",
        "bg_btn": "linear-gradient(135deg,#f59e0b 0%,#d97706 100%)",
        "sec_bg": "rgba(245,158,11,0.12)", "sec_color": "#fbbf24",
        "sec_border": "rgba(245,158,11,0.22)",
    },
    "🔀 Alternative Investment (PE/RE/HF)": {
        "primary": "#c084fc", "hover": "#d8b4fe",
        "glow": "rgba(192,132,252,0.18)",
        "bg_btn": "linear-gradient(135deg,#c084fc 0%,#a855f7 100%)",
        "sec_bg": "rgba(192,132,252,0.12)", "sec_color": "#d8b4fe",
        "sec_border": "rgba(192,132,252,0.22)",
    },
    "🏛️ Group / Holding": {
        "primary": "#06b6d4", "hover": "#22d3ee",
        "glow": "rgba(6,182,212,0.18)",
        "bg_btn": "linear-gradient(135deg,#06b6d4 0%,#0891b2 100%)",
        "sec_bg": "rgba(6,182,212,0.12)", "sec_color": "#22d3ee",
        "sec_border": "rgba(6,182,212,0.22)",
    },
}

def _ent_slug(name: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]", "-", name.lower()).strip("-")


# ── Entity-aware accent CSS injection ────────────────────────────────────────
def _inject_entity_theme() -> None:
    _et = st.session_state.get("entity_type", "🏦 Private Banking")
    _t = _ENTITY_THEMES.get(_et, _ENTITY_THEMES["🏦 Private Banking"])
    st.markdown(f"""<style>
:root {{
  --accent-primary:      {_t['primary']};
  --accent-hover:        {_t['hover']};
  --accent-glow:         {_t['glow']};
  --tab-active:          {_t['primary']};
  --tab-active-border:   {_t['primary']};
  --btn-primary-bg:      {_t['bg_btn']};
  --btn-secondary-bg:    {_t['sec_bg']};
  --btn-secondary-color: {_t['sec_color']};
  --btn-secondary-border:{_t['sec_border']};
  --sidebar-header-color:{_t['primary']};
  --border-accent:       {_t['primary']}4d;
  --text-accent:         {_t['hover']};
}}
div[data-testid="stButton"]>button[kind="primary"]{{
  background:{_t['bg_btn']} !important;
  box-shadow:0 2px 8px {_t['glow']} !important;
}}
div[data-testid="stButton"]>button[kind="primary"]:hover{{
  background:{_t['bg_btn']} !important;
  box-shadow:0 4px 16px {_t['glow']} !important;
  filter:brightness(1.08);
}}
.section-header-icon{{
  background:{_t['glow']} !important;
  border-color:{_t['primary']}33 !important;
}}
.section-count-badge{{
  background:{_t['sec_bg']} !important;
  color:{_t['primary']} !important;
  border-color:{_t['primary']}33 !important;
}}
.loading-spinner{{
  background:{_t['glow']} !important;
  border-color:{_t['primary']}26 !important;
}}
.loading-spinner-dot{{
  border-top-color:{_t['primary']} !important;
  border-color:{_t['primary']}33 !important;
}}
</style>""", unsafe_allow_html=True)

_inject_entity_theme()


TAB_TITLES = {
    0: "🌐 Intelligence Dashboard",
    1: "🔍 Risk Analysis",
    2: "📋 Audit Plan & Testing",
    3: "📄 Audit Report",
    5: "📡 Continuous Audit",
    6: "🏢 Third Party & Vendor 360",
    7: "🔍 KYC / AML Compliance",
}

TAB_SUBTITLES = {
    0: "Stay informed before launching an audit",
    1: "Identify risks and applicable regulations for your audit topic",
    2: "Build your audit plan and test programme",
    3: "Generate your formal audit report",
    5: "Real-time monitoring · Risk KPIs · Alert feed",
    6: "Vendor risk scoring · KYC · Outsourcing oversight",
    7: "Client risk · PEP · Sanctions · Remediation pipeline",
}

_TAB_NAMES = {
    "Français": ["Tableau de bord", "Analyse des Risques", "Plan & Tests", "Document Analyser", "Rapport d'Audit", "Audit Continu", "Tiers & Fournisseurs", "KYC / AML"],
    "English":  ["Dashboard", "Risk Analysis", "Audit Plan", "Document Analyser", "Audit Report", "Continuous Audit", "Vendor 360", "KYC / AML"],
}


def _entity_badge_html(entity_type: str, size: str = "13px") -> str:
    bg, col = _ENTITY_COLORS.get(entity_type, ("#0a2540", "#818cf8"))
    return (
        f'<span style="background:{bg};color:{col};border:1px solid {col}55;'
        f'border-radius:6px;padding:2px 10px;font-size:{size};font-weight:600">'
        f'{entity_type}</span>'
    )

JURISDICTIONS = ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU / DORA", "UK / FCA+PRA"]
OUTPUT_DIR = str(_HERE / "outputs")
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# ── UI helpers ────────────────────────────────────────────────────────────────

# ── Jurisdiction → flag emoji ─────────────────────────────────────────────────
_JUR_FLAG = {
    "CH / FINMA":      "🇨🇭",
    "SG / MAS":        "🇸🇬",
    "HK / SFC+HKMA":  "🇭🇰",
    "Bahamas / SCB":   "🇧🇸",
    "EU / DORA":       "🇪🇺",
    "UK / FCA+PRA":    "🇬🇧",
}

def _make_pdf(title: str, sections: list) -> bytes:
    """Generate a simple PDF. sections = [(heading, body_text), ...]"""
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.set_margins(18, 18, 18)
        pdf.add_page()
        # Title
        pdf.set_font("Helvetica", style="B", size=16)
        pdf.multi_cell(0, 10, title)
        pdf.ln(4)
        pdf.set_draw_color(80, 80, 200)
        pdf.line(18, pdf.get_y(), 192, pdf.get_y())
        pdf.ln(4)
        for heading, body in sections:
            if not body:
                continue
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.multi_cell(0, 7, heading)
            pdf.set_font("Helvetica", size=9)
            safe_body = body.encode("latin-1", errors="replace").decode("latin-1")
            pdf.multi_cell(0, 5, safe_body)
            pdf.ln(3)
        return bytes(pdf.output())
    except Exception:
        return b""


def _demo_stream_generate(steps: list, result_key_values: dict):
    """Show animated multi-step generation then write results to session_state."""
    import time
    prog = st.progress(0, text="")
    status = st.empty()
    n = len(steps)
    for i, (icon, label, delay) in enumerate(steps):
        status.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;'
            f'padding:10px 14px;background:rgba(99,102,241,.07);'
            f'border:1px solid rgba(99,102,241,.2);border-radius:10px;'
            f'font-size:13px;color:#a5b4fc">'
            f'<span style="font-size:16px">{icon}</span>{label}</div>',
            unsafe_allow_html=True,
        )
        prog.progress(int((i + 1) / n * 100), text="")
        time.sleep(delay)
    prog.empty()
    status.empty()
    for k, v in result_key_values.items():
        st.session_state[k] = v


_ICON_MAP = {
    "shield": "🛡️", "search": "🔍", "file-text": "📄", "bar-chart": "📊",
    "alert-triangle": "⚠️", "check-circle": "✅", "info": "ℹ️",
    "download": "⬇️", "upload": "⬆️", "globe": "🌐", "lock": "🔒",
    "users": "👥", "building": "🏦", "calendar": "📅", "clock": "🕐",
    "double-arrow-right": "»", "arrow-right": "›", "chevron-right": "›",
    "zap": "⚡", "star": "★", "flag": "🚩", "target": "🎯",
}

def lucide_icon(name: str, size: int = 16, color: str = "currentColor") -> str:
    """Returns an emoji icon (Lucide removed — not compatible with Streamlit CSP)."""
    emoji = _ICON_MAP.get(name, "•")
    return (
        f'<span style="font-size:{size}px;color:{color};'
        f'vertical-align:middle;display:inline-block;">{emoji}</span>'
    )


def severity_badge(level: str, size: str = "normal") -> str:
    """Returns a styled severity badge HTML span."""
    _colors = {
        "Critical": ("#ef4444", "rgba(239,68,68,0.12)"),
        "High":     ("#f97316", "rgba(249,115,22,0.12)"),
        "Moderate": ("#eab308", "rgba(234,179,8,0.12)"),
        "Low":      ("#22c55e", "rgba(34,197,94,0.12)"),
    }
    color, bg = _colors.get(level, ("#94a3b8", "rgba(148,163,184,0.12)"))
    font_size = "10px" if size == "small" else "11px"
    return (
        f'<span style="display:inline-flex;align-items:center;gap:4px;'
        f'background:{bg};color:{color};border:1px solid {color}40;'
        f'border-radius:20px;padding:2px 8px;font-size:{font_size};'
        f'font-weight:700;letter-spacing:0.5px;box-shadow:0 0 8px {color}20;">'
        f'<span style="width:5px;height:5px;border-radius:50%;background:{color};'
        f'box-shadow:0 0 4px {color};display:inline-block;"></span>'
        f'{level.upper()}</span>'
    )


def section_header(icon_name: str, title: str, subtitle: str = "", count: int = None) -> str:
    """Returns a styled section header HTML block with Lucide icon."""
    count_html = (
        f'<span class="section-count-badge">{count}</span>'
        if count is not None else ""
    )
    subtitle_html = (
        f'<div style="font-size:12px;color:#475569;margin-top:2px;">{subtitle}</div>'
        if subtitle else ""
    )
    return f"""
    <div class="section-header">
      <div class="section-header-icon">
        <span style="font-size:16px;color:#6366f1;">{_ICON_MAP.get(icon_name, "•")}</span>
      </div>
      <div>
        <div style="font-size:15px;font-weight:700;color:#e2e8f0;
                    display:flex;align-items:center;">
          {title}{count_html}
        </div>
        {subtitle_html}
      </div>
    </div>
    """


def show_loading(message: str) -> None:
    """Render a styled loading indicator."""
    st.markdown(f"""
    <div class="loading-spinner">
      <div class="loading-spinner-dot"></div>
      <span style="font-size:13px;color:#818cf8;font-weight:500;">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def _tab_actions_bar(tab_key: str, subtitle: str, exports: list) -> None:
    """Render tab header: entity badge + subtitle left, export buttons right.

    exports = list of (label, data_or_none, filename, mime) tuples.
    """
    _entity = st.session_state.get("entity_type", "🏦 Private Banking")
    _t = _ENTITY_THEMES.get(_entity, _ENTITY_THEMES["🏦 Private Banking"])
    _h_left, _h_right = st.columns([6, 4], gap="small")
    with _h_left:
        st.markdown(
            f'<div style="margin-bottom:4px">{_entity_badge_html(_entity)}</div>'
            f'<p style="color:#5a6488;font-size:13px;margin:0 0 0.4rem">{subtitle}</p>',
            unsafe_allow_html=True,
        )
    with _h_right:
        # Export buttons row — aligned right
        _has_any = any(d for _, d, _, _ in exports)
        _btn_count = len(exports) + 1  # +1 for Teammate+
        _ecols = st.columns(_btn_count, gap="small")

        # Download buttons
        for i, (lbl, data, fname, mime) in enumerate(exports):
            with _ecols[i]:
                if data:
                    st.download_button(
                        lbl, data=data, file_name=fname, mime=mime,
                        key=f"_top_dl_{tab_key}_{i}",
                        use_container_width=True,
                    )
                else:
                    st.button(lbl, key=f"_top_dl_dis_{tab_key}_{i}",
                              disabled=True, use_container_width=True)

        # Teammate+ always visible
        with _ecols[-1]:
            st.markdown(f'<div class="wk-btn">', unsafe_allow_html=True)
            if st.button("📤 TM+", key=f"wk_top_{tab_key}",
                         help="Export to Wolters Kluwer Teammate+",
                         use_container_width=True):
                st.toast("✅ Données exportées vers Teammate+ (Wolters Kluwer)", icon="📤")
            st.markdown("</div>", unsafe_allow_html=True)


def render_table(headers: list, rows: list, highlight_col: int = None) -> str:
    """Render a styled HTML table for use with st.markdown(..., unsafe_allow_html=True)."""
    header_html = "".join(
        f'<th style="padding:10px 14px;font-size:11px;font-weight:700;'
        f'letter-spacing:0.8px;text-transform:uppercase;color:#475569;'
        f'border-bottom:1px solid rgba(255,255,255,0.06);white-space:nowrap;">{h}</th>'
        for h in headers
    )
    rows_html = ""
    for i, row in enumerate(rows):
        cells = ""
        for j, cell in enumerate(row):
            is_hi = (j == highlight_col)
            cells += (
                f'<td style="padding:10px 14px;font-size:13px;'
                f'color:{"#e2e8f0" if is_hi else "#94a3b8"};'
                f'font-weight:{"600" if is_hi else "400"};'
                f'border-bottom:1px solid rgba(255,255,255,0.03);">{cell}</td>'
            )
        bg = "rgba(255,255,255,0.01)" if i % 2 else "transparent"
        rows_html += f'<tr style="background:{bg};">{cells}</tr>'
    return (
        f'<div style="overflow-x:auto;border-radius:10px;'
        f'border:1px solid rgba(255,255,255,0.06);">'
        f'<table style="width:100%;border-collapse:collapse;background:var(--bg-card);">'
        f'<thead><tr>{header_html}</tr></thead>'
        f'<tbody>{rows_html}</tbody></table></div>'
    )


def render_risk_cards(risks: list) -> None:
    """Render risk indicators as glassmorphism cards grouped by severity."""
    if not risks:
        st.markdown(
            '<div style="text-align:center;padding:40px;color:#475569;">'
            'No risks found for this topic.</div>',
            unsafe_allow_html=True,
        )
        return

    critical = [r for r in risks if r.get("level") == "Critical"]
    high     = [r for r in risks if r.get("level") == "High"]
    moderate = [r for r in risks if r.get("level") == "Moderate"]

    for group, color, label in [
        (critical, "#ef4444", "Critical"),
        (high,     "#f97316", "High"),
        (moderate, "#eab308", "Moderate"),
    ]:
        if not group:
            continue
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin:20px 0 12px 0;">
          <div style="width:8px;height:8px;border-radius:50%;background:{color};
                      box-shadow:0 0 8px {color}88;"></div>
          <span style="font-size:11px;font-weight:700;letter-spacing:1.5px;
                        color:{color};">{label.upper()}</span>
          <span style="font-size:11px;color:#475569;">({len(group)} risks)</span>
        </div>
        """, unsafe_allow_html=True)

        ncols = min(len(group), 3)
        cols = st.columns(ncols)
        for i, risk in enumerate(group):
            controls  = risk.get("expected_controls", [])
            red_flags = risk.get("red_flags", [])
            desc      = risk.get("description", "")
            desc_short = desc[:120] + ("..." if len(desc) > 120 else "")
            with cols[i % ncols]:
                st.markdown(f"""
                <div class="risk-card risk-card-{label.lower()}"
                     style="border:1px solid {color}22;">
                  <div style="font-size:11px;font-weight:700;color:{color};
                              letter-spacing:1px;margin-bottom:6px;">{label.upper()}</div>
                  <div style="font-size:14px;font-weight:600;color:#e2e8f0;
                              margin-bottom:8px;line-height:1.3;">
                    {risk.get("title", "")}
                  </div>
                  <div style="font-size:12px;color:#64748b;margin-bottom:10px;
                              line-height:1.5;">{desc_short}</div>
                  <div style="font-size:11px;color:#475569;margin-bottom:4px;">
                    PROBABILITY · {risk.get("probability","N/A")}
                    &nbsp;·&nbsp; IMPACT · {risk.get("impact","N/A")}
                  </div>
                  <div style="border-top:1px solid rgba(255,255,255,0.05);
                              margin-top:10px;padding-top:10px;
                              font-size:11px;color:#475569;">
                    {len(controls)} controls expected &nbsp;·&nbsp;
                    {len(red_flags)} red flags
                  </div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("View details", expanded=False):
                    if controls:
                        st.markdown("**Expected Controls**")
                        for c in controls:
                            st.markdown(f"• {c}")
                    if red_flags:
                        st.markdown("**Red Flags**")
                        for f in red_flags:
                            st.markdown(f"⚠ {f}")


# ── Templates ─────────────────────────────────────────────────────────────────
_TPL_SEPARATORS = {"— Select a template —", "── CORE AUDIT TOPICS ──", "── SPECIALIZED TOPICS ──", "── IT AUDIT ──"}

TEMPLATES = {
    "— Select a template —": {},
    "── CORE AUDIT TOPICS ──": {},
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
    "── SPECIALIZED TOPICS ──": {},
    "Artificial Intelligence & Model Risk": {
        "topic": "Artificial Intelligence & Model Risk",
        "jurisdictions": ["CH / FINMA", "EU / DORA", "UK / FCA+PRA", "SG / MAS"],
        "scope": (
            "AI and machine learning models used in investment decisions, credit scoring, "
            "AML transaction monitoring, client onboarding and risk management. "
            "Includes third-party AI tools and internally developed models."
        ),
    },
    "Cloud Risk & Infrastructure": {
        "topic": "Cloud Risk & Infrastructure",
        "jurisdictions": ["CH / FINMA", "EU / DORA", "SG / MAS", "UK / FCA+PRA"],
        "scope": (
            "Cloud infrastructure and services (IaaS, PaaS, SaaS) including public cloud "
            "providers (AWS, Azure, GCP), hybrid environments and cloud-hosted critical "
            "applications (core banking, CRM, data analytics)."
        ),
    },
    "Resilience & Business Continuity": {
        "topic": "Resilience & Business Continuity",
        "jurisdictions": ["CH / FINMA", "EU / DORA", "UK / FCA+PRA", "SG / MAS"],
        "scope": (
            "Business continuity and disaster recovery arrangements for critical business "
            "services, IT systems and third-party dependencies. Includes BCP testing, "
            "RTO/RPO definitions and crisis management framework."
        ),
    },
    "Change Management & IT Development": {
        "topic": "Change Management & IT Development",
        "jurisdictions": ["CH / FINMA", "EU / DORA", "SG / MAS", "UK / FCA+PRA"],
        "scope": (
            "IT change management processes including SDLC, release management, patch "
            "management, emergency changes and DevSecOps practices across all critical "
            "banking systems."
        ),
    },
    "Access Management & Identity": {
        "topic": "Access Management & Identity",
        "jurisdictions": ["CH / FINMA", "EU / DORA", "SG / MAS", "UK / FCA+PRA"],
        "scope": (
            "Logical access management including PAM, IAM, MFA, active directory, "
            "and access recertification processes across all critical banking systems."
        ),
    },
    "Procurement & Sourcing": {
        "topic": "Procurement & Sourcing",
        "jurisdictions": ["CH / FINMA", "EU / DORA", "UK / FCA+PRA", "SG / MAS"],
        "scope": (
            "End-to-end procurement including sourcing strategy, vendor selection, "
            "contract negotiation, purchase-to-pay cycle and supplier relationship "
            "management across all spend categories."
        ),
    },
    "IT Production & Infrastructure": {
        "topic": "IT Production & Infrastructure",
        "jurisdictions": ["CH / FINMA", "EU / DORA", "SG / MAS", "UK / FCA+PRA"],
        "scope": (
            "IT production environment including server infrastructure, network architecture, "
            "database management, monitoring, capacity management, patch management, "
            "and IT operations centre processes."
        ),
    },
    "IT Operating Model & Governance": {
        "topic": "IT Operating Model & Governance",
        "jurisdictions": ["CH / FINMA", "EU / DORA", "SG / MAS", "UK / FCA+PRA"],
        "scope": (
            "IT governance framework including IT strategy alignment, IT risk management, "
            "governance committees, IT policy framework, IT budget oversight, "
            "and IT audit committee reporting."
        ),
    },
    "Wealth Management Advisory & Suitability": {
        "topic": "Wealth Management Advisory & Suitability",
        "jurisdictions": ["CH / FINMA", "EU / DORA", "UK / FCA+PRA", "HK / SFC+HKMA", "SG / MAS"],
        "scope": (
            "Investment advisory and discretionary portfolio management for HNWI clients. "
            "Includes suitability assessment, investment recommendations, conflicts of "
            "interest management, product governance and client reporting."
        ),
    },
    "── IT AUDIT ──": {},
    "API Security & Open Banking": {
        "topic": "API Security & Open Banking",
        "jurisdictions": ["CH / FINMA", "EU / DORA", "UK / FCA+PRA", "SG / MAS"],
        "scope": (
            "All production APIs including core banking APIs, open banking (PSD2) interfaces, "
            "mobile banking APIs, and third-party integration endpoints. Covers authentication, "
            "authorisation, input validation, data exposure, rate limiting, and API inventory management."
        ),
    },
    "Payment Fraud & SWIFT CSP": {
        "topic": "Payment Fraud & SWIFT CSP",
        "jurisdictions": ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "EU / DORA", "UK / FCA+PRA"],
        "scope": (
            "SWIFT infrastructure and CSP CSCF v2025 compliance, payment fraud controls including "
            "BEC prevention, dual-control on high-value payments, nostro reconciliation, "
            "correspondent banking due diligence, and payment anomaly detection."
        ),
    },
}

_disabled = not _api_key or not _READY


# ── Utility functions ─────────────────────────────────────────────────────────

def _client():
    return _ant.Anthropic(api_key=_api_key)


def _call(client, prompt, system="You are an expert audit consultant specialising in financial services.", max_tokens=6000):
    # System sent as a cacheable block; stream + get_final_message avoids HTTP
    # timeouts on large max_tokens while keeping an identical return contract.
    system_blocks = [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
    with client.messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        system=system_blocks,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        resp = stream.get_final_message()
    return next((b.text for b in resp.content if getattr(b, "type", None) == "text"), "").strip()


def _web_search_call(client, prompt, system="", max_tokens=6000):
    messages = [{"role": "user", "content": prompt}]
    texts = []
    ws_tool = [{"type": "web_search_20250305", "name": "web_search"}]
    for _ in range(8):
        kwargs = dict(model=MODEL, max_tokens=max_tokens, tools=ws_tool, messages=messages)
        if system:
            kwargs["system"] = [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
        with client.messages.stream(**kwargs) as stream:
            r = stream.get_final_message()
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
    system_blocks = [{"type": "text", "text": sys_prompt, "cache_control": {"type": "ephemeral"}}]
    while True:
        with client.beta.messages.stream(
            model=MODEL,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=system_blocks,
            messages=messages,
            tools=tools,
            betas=["files-api-2025-04-14"],
        ) as stream:
            r = stream.get_final_message()
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
    """Map a free-text audit topic to a THEME key used in RISK_INDICATORS etc.
    Checks TOPIC_KEY_MAPPING for exact template name match first,
    then falls back to keyword matching via TOPIC_THEME_MAP.
    """
    if not topic:
        return None
    # Exact match against template names
    keys = TOPIC_KEY_MAPPING.get(topic)
    if keys:
        return keys[0]
    # Fuzzy keyword match
    up = topic.upper()
    for kw, theme in TOPIC_THEME_MAP.items():
        if kw in up:
            return theme
    return None


@st.cache_data(show_spinner=False)
def get_data_for_topic(topic: str, entity_type: str = "🏦 Private Banking") -> dict:
    """Return aggregated risks, tests, DA scenarios, and entity-specific overlays for a topic."""
    # Initialise result with safe defaults for every expected key
    result: dict = {
        "risks":            [],
        "tests":            [],
        "kris":             [],
        "da_scenarios":     [],
        "regulatory_focus": [],
        "regulatory_refs":  [],
        "scope_suggestion": "",
        "risk_emphasis":    [],
        "typical_findings": [],
        "background_angle": "financial services",
        "entity_key":       "PRIVATE_BANKING",
        "keys":             [],
    }

    keys = TOPIC_KEY_MAPPING.get(topic, [])
    if not keys:
        theme = _topic_to_theme(topic)
        keys = [theme] if theme else []
    result["keys"] = keys

    risks, tests, da_scenarios = [], [], []
    for key in keys:
        risks.extend(RISK_INDICATORS.get(key, []))
        tests.extend(AUDIT_TESTS_LIBRARY.get(key, []))
        da_scenarios.extend(DATA_ANALYTICS_SCENARIOS.get(key, []))
    result["risks"] = risks
    result["tests"] = tests
    result["da_scenarios"] = da_scenarios

    # Entity-specific overlay from ENTITY_CONTEXT
    _ent_data  = ENTITY_CONTEXT.get(entity_type, {})
    _topic_key = keys[0] if keys else None
    _ent_topic = _ent_data.get("topics", {}).get(_topic_key, {}) if _topic_key else {}

    result["regulatory_focus"] = _ent_data.get("regulatory_focus", [])
    result["regulatory_refs"]  = _ent_topic.get("regulatory_refs", [])
    result["scope_suggestion"] = _ent_topic.get("scope_suggestion", "")
    result["risk_emphasis"]    = _ent_topic.get("risk_emphasis", [])
    result["typical_findings"] = _ent_topic.get("typical_findings", [])
    result["background_angle"] = _ent_data.get("background_angle", "financial services")
    result["entity_key"]       = _ENTITY_KEYS.get(entity_type, "PRIVATE_BANKING")

    return result


def _entity_institution_str(entity_type: str | None = None, jurs: list | None = None) -> str:
    """Return a prompt-ready institution description adapted to the current entity type."""
    ent = entity_type or st.session_state.get("entity_type", "🏦 Private Banking")
    ctx = ENTITY_CONTEXT.get(ent, {})
    angle = ctx.get("background_angle", "financial services")
    jur_str = (", ".join(j.split(" / ")[0] for j in jurs) if jurs else "CH, SG, HK") if jurs else "CH, SG, HK"
    return f"{angle.title()} institution ({jur_str})"


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
            <span style="font-size:13.5px;font-weight:600;color:var(--text-primary)">{r.get("id","")} &mdash; {r["title"]}</span>
            <span style="margin-left:auto;font-size:11px;color:var(--text-muted)">
              Prob: <span style="color:{prob_color};font-weight:600">{r.get("probability","")}</span>
              &nbsp;&middot;&nbsp; Impact: <span style="color:{impact_color};font-weight:600">{r.get("impact","")}</span>
            </span>
          </div>
          <p style="font-size:12.5px;color:var(--text-secondary);margin:0 0 10px;line-height:1.7">{r["description"]}</p>
          <details style="margin-bottom:6px">
            <summary style="font-size:12px;color:#818cf8;cursor:pointer;font-weight:500">Controls &amp; Red Flags</summary>
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
            f'<td style="padding:9px 13px;color:#818cf8;font-weight:500;white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("source","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-muted);text-align:center;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("year","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("recommendation","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-muted);font-size:11.5px;font-style:italic;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("private_banking_relevance","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{badge}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(99,102,241,0.07);border-bottom:1px solid rgba(99,102,241,0.18)">
        <th style="color:#818cf8;width:12%">Source</th><th style="color:#818cf8;width:5%;text-align:center">Year</th>
        <th style="color:#818cf8;width:40%">Recommendation</th>
        <th style="color:#818cf8;width:35%">Private Banking Relevance</th>
        <th style="color:#818cf8;width:8%">Priority</th>
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
            f'<td style="padding:9px 13px;color:#818cf8;font-weight:600;white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{s.get("id","")}</td>'
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
      <thead><tr style="background:rgba(99,102,241,0.07);border-bottom:1px solid rgba(99,102,241,0.18)">
        <th style="color:#818cf8;width:6%">ID</th><th style="color:#818cf8;width:18%">Scenario</th>
        <th style="color:#818cf8;width:25%">Objective</th><th style="color:#818cf8;width:12%">Analysis Type</th>
        <th style="color:#818cf8;width:28%">Anomaly Searched</th><th style="color:#818cf8;width:11%">Complexity / Tools</th>
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
        "Entry into force":      "#818cf8",
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
            <span style="background:rgba(99,102,241,0.08);color:#818cf8;border:1px solid rgba(99,102,241,0.2);
                  border-radius:4px;padding:2px 8px;font-size:10px;font-weight:600;white-space:nowrap">{e.get("jurisdiction","")}</span>
            <span style="font-size:13px;font-weight:600;color:#dde3f5;flex:1">{e.get("reg_id","")} &mdash; {e.get("regulation","")}</span>
            <span style="font-size:12px;font-weight:700;color:{date_color};white-space:nowrap">{date_display}{upcoming_badge}{past_badge}</span>
          </div>
          <p style="font-size:12px;color:var(--text-secondary);margin:0 0 8px;line-height:1.7">{e.get("description","")}</p>
          <details>
            <summary style="font-size:11.5px;color:#818cf8;cursor:pointer;font-weight:500">Impact &middot; Action required &middot; Audit relevance</summary>
            <div style="margin-top:10px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px">
              <div>
                <div style="font-size:10px;font-weight:700;color:#5a6488;margin-bottom:4px;text-transform:uppercase">Impact &mdash; Private Banking</div>
                <p style="font-size:11.5px;color:var(--text-secondary);margin:0;line-height:1.65">{e.get("impact_private_banking","")}</p>
              </div>
              <div>
                <div style="font-size:10px;font-weight:700;color:#5a6488;margin-bottom:4px;text-transform:uppercase">Action Required</div>
                <p style="font-size:11.5px;color:var(--text-secondary);margin:0;line-height:1.65">{e.get("action_required","")}</p>
              </div>
              <div>
                <div style="font-size:10px;font-weight:700;color:#818cf8;margin-bottom:4px;text-transform:uppercase">Audit Relevance</div>
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
    _CAT_C = {"AML": "#818cf8", "Fraud": "#ef4444", "Suitability": "#a78bfa", "Tax": "#22d3a5", "Conduct": "#f97316"}

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
            <span style="font-size:13px;font-weight:600;color:#dde3f5">{e.get("rf_id","")} &mdash; {e.get("title","")}</span>
          </div>
          <p style="font-size:12.5px;color:var(--text-secondary);margin:0 0 8px;line-height:1.7">{e.get("description","")}</p>
          <details>
            <summary style="font-size:11.5px;color:#818cf8;cursor:pointer;font-weight:500">Detection &middot; Regulation &middot; PB context &middot; Examples</summary>
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
    _SEC_C  = "#818cf8"
    _SEC_BG = "rgba(99,102,241,0.06)"

    card = THEMATIC_BACKGROUND.get(theme_key)
    if not card:
        available = ", ".join(k.replace("_", " ").title() for k in THEMATIC_BACKGROUND)
        st.markdown(
            f'<div style="background:rgba(234,179,8,0.07);border:1px solid rgba(234,179,8,0.3);'
            f'border-radius:8px;padding:14px 18px">'
            f'<p style="color:#eab308;font-size:12.5px;margin:0 0 6px;font-weight:600">'
            f'⚠️ No thematic profile found for this topic.</p>'
            f'<p style="color:#c8d0e8;font-size:12px;margin:0">Available themes: '
            f'<span style="color:#818cf8">{available}</span></p></div>',
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
        _jflag = _JUR_FLAG.get(jur, "🌐")
        with st.expander(f"{_jflag} **{jur}** — {len(filtered)} texts", expanded=(jur_filter != "All")):
            rows = ""
            for r in filtered:
                applies = " &nbsp;".join(f'<span class="badge-info">{t}</span>' for t in r.get("applies_to", []))
                reqs = "".join(f"<li>{k}</li>" for k in r.get("key_requirements", []))
                rows += (
                    f'<tr>'
                    f'<td style="padding:9px 13px;color:#818cf8;font-weight:600;white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("reference","")}</td>'
                    f'<td style="padding:9px 13px;color:var(--text-primary);font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("title","")}<br><span style="font-size:11px;color:var(--text-muted)">{r.get("authority","")} &middot; {r.get("year","")}</span></td>'
                    f'<td style="padding:9px 13px;color:var(--text-secondary);font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("scope","")}</td>'
                    f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{applies}</td>'
                    f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)"><ul style="margin:0;padding-left:15px;font-size:11.5px;color:var(--text-secondary);line-height:1.7">{reqs}</ul></td>'
                    f'</tr>'
                )
            st.markdown(f"""
            <table class="data-table" style="font-size:12px">
              <thead><tr style="background:rgba(99,102,241,0.07);border-bottom:1px solid rgba(99,102,241,0.18)">
                <th style="color:#818cf8;width:10%">Reference</th><th style="color:#818cf8;width:18%">Title</th>
                <th style="color:#818cf8;width:22%">Scope</th><th style="color:#818cf8;width:14%">Applies To</th>
                <th style="color:#818cf8;width:36%">Key Requirements</th>
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
    """Mode toggle using pill buttons. Returns 'static' or 'live'."""
    key = f"_mode_state_{tab_key}"
    if key not in st.session_state:
        st.session_state[key] = "static"

    col1, col2, col3 = st.columns([2, 2, 8])
    with col1:
        if st.button(
            "📚 Static",
            key=f"_btn_static_{tab_key}",
            type="primary" if st.session_state[key] == "static" else "secondary",
        ):
            st.session_state[key] = "static"
            # sync legacy key too
            st.session_state[tab_key] = _MODE_STATIC
            st.rerun()
    with col2:
        if st.button(
            "⚡ Live",
            key=f"_btn_live_{tab_key}",
            type="primary" if st.session_state[key] == "live" else "secondary",
        ):
            st.session_state[key] = "live"
            st.session_state[tab_key] = _MODE_LIVE
            st.rerun()
    st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)
    return st.session_state[key]


_LEVEL_COLOR = {"Critical": "#ef4444", "High": "#f97316", "Moderate": "#eab308"}
_LEVEL_BG    = {"Critical": "rgba(239,68,68,0.08)", "High": "rgba(249,115,22,0.08)", "Moderate": "rgba(234,179,8,0.06)"}
_LEVEL_EMOJI = {"Critical": "🔴", "High": "🟠", "Moderate": "🟡"}

_STOPWORDS = {"the","a","an","and","or","of","for","in","to","is","are","be","that","all","with","on",
              "at","by","as","its","from","it","this","that","if","any","no","each","per","must","will"}


def _words(text: str) -> set:
    """Tokenize text into lowercase words, filtering stopwords and short tokens."""
    import re
    if not text or not isinstance(text, str):
        return set()
    return {w for w in re.findall(r'[a-zA-Z]{3,}', text.lower()) if w not in _STOPWORDS}


def _build_risk_test_map(theme: str, live_risks: list | None = None) -> dict:
    """Build test_id → {risk_id, risk_title, risk_level, control} mapping.

    Uses keyword overlap between test objective/procedure and risk title/expected_controls.
    Result is cached in session_state to avoid recomputation on every interaction.
    """
    cache_key = f"_rtmap_{theme}_{'live' if live_risks is not None else 'static'}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    tests = AUDIT_TESTS_LIBRARY.get(theme, [])
    risks = live_risks if live_risks is not None else RISK_INDICATORS.get(theme, [])

    def _score(test, risk) -> int:
        t_words = _words(test.get("objective", "") + " " + test.get("procedure", ""))
        r_words = _words(
            (risk.get("title") or risk.get("name", "")) + " " +
            " ".join(risk.get("expected_controls", []))
        )
        return len(t_words & r_words)

    def _best_control(test, risk) -> str:
        controls = risk.get("expected_controls", [])
        if not controls:
            return ""
        t_words = _words(test.get("objective", "") + " " + test.get("procedure", ""))
        best, best_s = controls[0], 0
        for ctrl in controls:
            s = len(_words(ctrl) & t_words)
            if s > best_s:
                best_s, best = s, ctrl
        return best

    result = {}
    for t in tests:
        best_risk, best_s = None, 0
        for r in risks:
            s = _score(t, r)
            if s > best_s:
                best_s, best_risk = s, r
        if best_risk:
            rid = best_risk.get("id") or best_risk.get("name", "")
            result[t["id"]] = {
                "risk_id":    rid,
                "risk_title": best_risk.get("title") or best_risk.get("name", ""),
                "risk_level": best_risk.get("level", ""),
                "control":    _best_control(t, best_risk),
            }

    st.session_state[cache_key] = result
    return result


def _show_risk_coverage_summary(theme: str, risk_map: dict, live_risks: list | None = None):
    """Render Risk Coverage Summary below the test table."""
    risks = live_risks if live_risks is not None else RISK_INDICATORS.get(theme, [])
    if not risks:
        return

    covered_ids = {v["risk_id"] for v in risk_map.values()}
    total = len(risks)
    covered = sum(1 for r in risks if (r.get("id") or r.get("name", "")) in covered_ids)
    pct = round(covered / total * 100) if total else 0

    uncovered = [r for r in risks if (r.get("id") or r.get("name", "")) not in covered_ids]
    uncovered_critical_high = [r for r in uncovered if r.get("level") in ("Critical", "High")]

    pct_color = "#22d3a5" if pct >= 80 else ("#eab308" if pct >= 50 else "#ef4444")
    uncov_rows = "".join(
        f'<li><span style="color:#818cf8;font-weight:700">{r.get("id") or ""}</span>'
        f' &mdash; {r.get("title") or r.get("name","")} &nbsp;'
        f'<span style="color:{_LEVEL_COLOR.get(r.get("level",""),"#8392bb")};font-size:11px">'
        f'{_LEVEL_EMOJI.get(r.get("level",""),"")} {r.get("level","")}</span></li>'
        for r in uncovered
    )

    st.markdown(f"""
    <div style="background:rgba(99,102,241,0.04);border:1px solid rgba(99,102,241,0.18);
                border-radius:8px;padding:16px 20px;margin-top:18px">
      <div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.7px;
                  color:#818cf8;margin-bottom:12px">Risk Coverage Summary</div>
      <div style="display:flex;gap:32px;flex-wrap:wrap;margin-bottom:12px">
        <div style="font-size:13px;color:var(--text-secondary)">
          Total risks identified: <strong style="color:var(--text-primary)">{total}</strong></div>
        <div style="font-size:13px;color:var(--text-secondary)">
          Covered by ≥1 test: <strong style="color:var(--text-primary)">{covered}</strong></div>
        <div style="font-size:13px;color:var(--text-secondary)">
          Coverage rate: <strong style="color:{pct_color};font-size:15px">{pct}%</strong></div>
      </div>
      {"" if not uncovered else f'''
      <div style="font-size:11.5px;font-weight:700;color:#8392bb;margin-bottom:6px">⚠️ Uncovered risks:</div>
      <ul style="margin:0;padding-left:16px;font-size:12px;color:var(--text-secondary);line-height:1.9">{uncov_rows}</ul>
      '''}
    </div>""", unsafe_allow_html=True)

    if uncovered_critical_high:
        names = ", ".join(
            (r.get("id") or "") + " " + (r.get("title") or r.get("name", ""))
            for r in uncovered_critical_high
        )
        st.warning(
            f"⚠️ {len(uncovered_critical_high)} Critical/High risk(s) have no associated test. "
            f"Consider adding coverage for: {names}"
        )


def _show_tests_library(theme: str, search: str = "", level_filter: str = "All",
                        type_filter: str = "All", risk_level_filter: str = "All",
                        live_risks: list | None = None):
    """Display AUDIT_TESTS_LIBRARY for a given theme with risk mapping columns."""
    risk_map = _build_risk_test_map(theme, live_risks)
    tests = AUDIT_TESTS_LIBRARY.get(theme, [])

    # Apply filters
    if level_filter != "All":
        tests = [t for t in tests if t.get("level") == level_filter]
    if type_filter == "Data Analytics":
        tests = [t for t in tests if t.get("category") == "Data Analytics"]
    elif type_filter == "Standard":
        tests = [t for t in tests if t.get("category") == "Standard"]
    if risk_level_filter != "All":
        tests = [t for t in tests if risk_map.get(t["id"], {}).get("risk_level") == risk_level_filter]
    if search:
        q = search.lower()
        tests = [t for t in tests if q in (t.get("objective","") + t.get("procedure","") + t.get("id","")).lower()]

    # Sort: Critical risks first, then High, then Moderate
    _rl_order = {"Critical": 0, "High": 1, "Moderate": 2}
    tests = sorted(tests, key=lambda t: _rl_order.get(risk_map.get(t["id"], {}).get("risk_level",""), 3))

    if not tests:
        st.caption("No tests match the filter.")
        _show_risk_coverage_summary(theme, risk_map, live_risks)
        return

    _DA_BADGE = '<span style="background:rgba(99,102,241,0.12);color:#818cf8;border:1px solid rgba(99,102,241,0.28);border-radius:4px;padding:1px 7px;font-size:11px;font-weight:600">📊 DA</span>'
    rows = ""
    for t in tests:
        lv = t.get("level", "")
        col = _LEVEL_COLOR.get(lv, "#8392bb")
        bg  = _LEVEL_BG.get(lv, "transparent")
        da  = _DA_BADGE if t.get("category") == "Data Analytics" else ""
        lv_badge = f'<span style="background:{bg};color:{col};border:1px solid {col}44;border-radius:4px;padding:1px 7px;font-size:11px;font-weight:700">{lv}</span>'
        tr_ref = t.get("tr_reference", "")
        tr_cell = (f'<span style="background:rgba(99,102,241,0.09);color:#818cf8;border:1px solid rgba(99,102,241,0.25);'
                   f'border-radius:3px;padding:1px 5px;font-size:10px;white-space:nowrap">{tr_ref}</span>' if tr_ref else "")

        rm = risk_map.get(t["id"], {})
        r_title = rm.get("risk_title", "—")
        r_id    = rm.get("risk_id", "")
        r_lv    = rm.get("risk_level", "")
        r_ctrl  = rm.get("control", "—")
        r_col   = _LEVEL_COLOR.get(r_lv, "#8392bb")
        r_bg    = _LEVEL_BG.get(r_lv, "transparent")
        r_emoji = _LEVEL_EMOJI.get(r_lv, "")
        risk_cell = (
            f'<div style="white-space:nowrap;color:#818cf8;font-size:11px;font-weight:700">{r_id}</div>'
            f'<div style="font-size:11.5px;color:var(--text-secondary)">{r_title}</div>'
            f'<div style="margin-top:3px"><span style="background:{r_bg};color:{r_col};border:1px solid {r_col}44;'
            f'border-radius:3px;padding:1px 6px;font-size:10.5px;font-weight:700">{r_emoji} {r_lv}</span></div>'
        ) if rm else "—"
        ctrl_cell = f'<span style="font-size:11.5px;color:var(--text-secondary);font-style:italic">{r_ctrl}</span>' if r_ctrl and r_ctrl != "&mdash;" else "&mdash;"

        rows += (
            f'<tr style="background:{bg}">'
            f'<td style="padding:9px 12px;color:#818cf8;font-weight:700;white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("id","")} {da}</td>'
            f'<td style="padding:9px 12px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{lv_badge}</td>'
            f'<td style="padding:9px 12px;color:var(--text-primary);font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("objective","")}</td>'
            f'<td style="padding:9px 12px;color:var(--text-secondary);font-size:12px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("procedure","")}</td>'
            f'<td style="padding:9px 12px;color:var(--text-muted);font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("sample_size","")}</td>'
            f'<td style="padding:9px 12px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{risk_cell}</td>'
            f'<td style="padding:9px 12px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{ctrl_cell}</td>'
            f'<td style="padding:9px 12px;color:#ef4444;font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("failure_criteria","")}</td>'
            f'<td style="padding:9px 12px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{tr_cell}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(99,102,241,0.07);border-bottom:1px solid rgba(99,102,241,0.18)">
        <th style="color:#818cf8;width:6%">ID</th>
        <th style="color:#818cf8;width:6%">Level</th>
        <th style="color:#818cf8;width:16%">Objective</th>
        <th style="color:#818cf8;width:20%">Procedure</th>
        <th style="color:#818cf8;width:9%">Sample</th>
        <th style="color:#818cf8;width:14%">Associated Risk</th>
        <th style="color:#818cf8;width:14%">Control Verified</th>
        <th style="color:#818cf8;width:10%">Failure Criteria</th>
        <th style="color:#818cf8;width:5%">TR</th>
      </tr></thead><tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)

    _show_risk_coverage_summary(theme, risk_map, live_risks)


def _render_iia_standard(s):
    """Render a single IIA standard entry — handles both plain and sectioned (TR) structures."""
    is_tr = s.get("topical_requirement", False) and s.get("sections")
    tr_marker = " · TR" if is_tr else ""
    with st.expander(f"**{s['standard_id']}**{tr_marker} — {s['title']}"):
        if is_tr:
            src_txt = s.get("source_guide", "")
            st.markdown(
                f'<div style="margin-bottom:10px">'
                f'<span style="background:rgba(99,102,241,0.15);color:#818cf8;border:1px solid rgba(99,102,241,0.35);border-radius:4px;padding:2px 9px;font-size:11px;font-weight:700">TR &mdash; Topical Requirement</span>'
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
                        fw_badges = " &nbsp;".join(f'<span style="background:rgba(99,102,241,0.09);color:#818cf8;border:1px solid rgba(99,102,241,0.25);border-radius:3px;padding:1px 5px;font-size:10px">{f}</span>' for f in req.get("frameworks", []))
                        st.markdown(f"""
                        <div style="border-left:3px solid rgba(99,102,241,0.4);padding:10px 14px;margin-bottom:10px;background:rgba(99,102,241,0.04);border-radius:0 6px 6px 0">
                          <div style="font-size:11.5px;font-weight:700;color:#818cf8;margin-bottom:4px">{req['id']}</div>
                          <p style="margin:0 0 8px;font-size:12.5px;color:var(--text-secondary);line-height:1.8">{req['text']}</p>
                          <div style="font-size:10.5px;color:#5a6488">{fw_badges}</div>
                        </div>""", unsafe_allow_html=True)
        else:
            reqs = "".join(f"<li>{r}</li>" for r in s.get("key_requirements", []))
            st.markdown(f"""
            <div>
              <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;color:#818cf8;margin-bottom:6px">Key Requirements</div>
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
        + _step("Risk Analysis", "&#10003;" if t1_done else "1", s1)
        + '<div class="pb-connector"></div>'
        + _step("Audit Plan", "&#10003;" if t2_done else "2", s2)
        + '<div class="pb-connector"></div>'
        + _step("Audit Report", "&#10003;" if t3_done else "3", s3)
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
      this.textContent='&#10003; Copied!';
      setTimeout(()=>{{this.textContent='⎘ Copy'}},1800);
    }})" style="
      background:rgba(99,102,241,0.10);color:#818cf8;
      border:1px solid rgba(99,102,241,0.25);border-radius:8px;
      font-size:12px;font-weight:500;padding:5px 14px;cursor:pointer;
      font-family:-apple-system,BlinkMacSystemFont,sans-serif;
    ">⎘ Copy</button>
    """
    st.html(html)




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
        src_html = (f'<a href="{link}" target="_blank" style="color:#818cf8;font-size:11px">{link[:40]}&hellip;</a>'
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
            f'<td style="padding:9px 13px;color:#818cf8;font-weight:500;vertical-align:top;white-space:nowrap;border-bottom:1px solid var(--tbl-row-border)">{r.get("authority","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{type_badge}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{title_html}{open_badge}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("key_impact","")}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(99,102,241,0.07);border-bottom:1px solid rgba(99,102,241,0.18)">
        <th style="color:#818cf8;width:8%">Date</th>
        <th style="color:#818cf8;width:10%">Authority</th>
        <th style="color:#818cf8;width:10%">Type</th>
        <th style="color:#818cf8;width:35%">Title</th>
        <th style="color:#818cf8;width:37%">Key Impact</th>
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
            f'<td style="padding:9px 13px;color:#818cf8;font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("source","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-primary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("theme","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("recommendation","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{badge}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(99,102,241,0.07);border-bottom:1px solid rgba(99,102,241,0.18)">
        <th style="color:#818cf8;width:8%">Date</th>
        <th style="color:#818cf8;width:14%">Source</th>
        <th style="color:#818cf8;width:16%">Theme</th>
        <th style="color:#818cf8;width:52%">Recommendation</th>
        <th style="color:#818cf8;width:10%">Priority</th>
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
            f'<td style="padding:9px 13px;color:#818cf8;font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("source","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;text-align:center;border-bottom:1px solid var(--tbl-row-border)">{r.get("year","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("recommendation","")}</td>'
            f'<td style="padding:9px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("applicability","")}</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(99,102,241,0.07);border-bottom:1px solid rgba(99,102,241,0.18)">
        <th style="color:#818cf8;width:16%">Source</th>
        <th style="color:#818cf8;width:7%;text-align:center">Year</th>
        <th style="color:#818cf8;width:46%">Recommendation</th>
        <th style="color:#818cf8;width:31%">Applicability to Private Banking</th>
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
        f'<td style="padding:10px 13px;color:#818cf8;font-weight:500;vertical-align:top;white-space:nowrap;border-bottom:1px solid var(--tbl-row-border)">{r.get("jurisdiction","")}</td>'
        f'<td style="padding:10px 13px;color:var(--text-primary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("text","")}</td>'
        f'<td style="padding:10px 13px;color:var(--text-secondary);vertical-align:top;font-size:11.5px;border-bottom:1px solid var(--tbl-row-border)">{r.get("reference","")}</td>'
        f'<td style="padding:10px 13px;color:var(--text-secondary);vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("requirement","")}</td>'
        f'</tr>'
        for r in regs
    )
    st.markdown(f"""
    <table class="data-table">
      <thead><tr style="background:rgba(99,102,241,0.08);border-bottom:1px solid rgba(99,102,241,0.2)">
        <th style="color:#818cf8;width:15%">Jurisdiction</th>
        <th style="color:#818cf8;width:22%">Regulation</th>
        <th style="color:#818cf8;width:16%">Reference</th>
        <th style="color:#818cf8;width:47%">Key Requirement</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


def _tests_table(tests):
    if not tests:
        return
    rows = "".join(
        f'<tr>'
        f'<td style="padding:9px 10px;color:#818cf8;font-weight:600;text-align:center;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{t.get("num","")}</td>'
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
      <thead><tr style="background:rgba(99,102,241,0.08);border-bottom:1px solid rgba(99,102,241,0.2)">
        <th style="color:#818cf8;width:4%;text-align:center">No.</th>
        <th style="color:#818cf8;width:16%">Objective</th>
        <th style="color:#818cf8;width:27%">Procedure</th>
        <th style="color:#818cf8;width:14%">Population</th>
        <th style="color:#818cf8;width:12%">Sample Size</th>
        <th style="color:#818cf8;width:27%">Failure Criteria</th>
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
      <thead><tr style="background:rgba(99,102,241,0.08);border-bottom:1px solid rgba(99,102,241,0.2)">
        <th style="color:#818cf8;width:18%">Scenario</th>
        <th style="color:#818cf8;width:20%">Objective</th>
        <th style="color:#818cf8;width:18%">Data Source</th>
        <th style="color:#818cf8;width:16%">Analysis Type</th>
        <th style="color:#818cf8;width:28%">Anomaly Detected</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


# ── Sign-in gate ─────────────────────────────────────────────────────────────
if not st.session_state.signed_in:
    # ── Hide Streamlit chrome (theme handles bg/colors) ────────────────────────
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
header[data-testid="stHeader"],.stDeployButton,
[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebar"]{display:none!important;}
html,body{font-family:'Inter',sans-serif!important;}
.main .block-container{
  padding-left:0!important;padding-right:0!important;
  padding-top:0!important;padding-bottom:0!important;
  max-width:100%!important;
}
[data-testid="stHorizontalBlock"]{gap:0!important;}
/* Reset column internal padding so form starts at top without scrolling */
[data-testid="stHorizontalBlock"]>[data-testid="stColumn"]>[data-testid="stVerticalBlock"]{
  padding-top:0!important;gap:4px!important;
}
/* Input styling */
.si-field .stTextInput input{
  background:rgba(255,255,255,.05)!important;
  border:1px solid rgba(255,255,255,.1)!important;
  border-radius:10px!important;color:#eef0f8!important;
  font-size:14px!important;font-family:'Inter',sans-serif!important;
  padding:11px 14px!important;
}
.si-field .stTextInput input:focus{
  border-color:rgba(99,102,241,.55)!important;
  box-shadow:0 0 0 3px rgba(99,102,241,.15)!important;outline:none!important;
}
.si-field .stTextInput label,
.si-field .stTextInput p,
.si-field [data-testid="InputInstructions"]{display:none!important;}
/* Submit button */
.si-btn-submit button{
  background:linear-gradient(135deg,#4f46e5,#6366f1)!important;
  color:#fff!important;border:none!important;border-radius:10px!important;
  font-size:15px!important;font-weight:700!important;padding:13px 20px!important;
  box-shadow:0 8px 24px rgba(99,102,241,.4)!important;width:100%!important;
}
.si-btn-submit button:hover{
  transform:translateY(-1px)!important;
  box-shadow:0 12px 30px rgba(99,102,241,.55)!important;
}
/* SSO buttons */
.si-btn-sso button{
  background:rgba(255,255,255,.04)!important;
  border:1px solid rgba(255,255,255,.1)!important;
  color:#c9cde0!important;border-radius:10px!important;
  font-size:12.5px!important;font-weight:600!important;padding:11px!important;width:100%!important;
}
.si-btn-sso button:hover{
  background:rgba(255,255,255,.08)!important;color:#eef0f8!important;
}
/* Refine login form card */
.form-card {
  background: rgba(13,17,23,0.95) !important;
  border: 1px solid rgba(255,255,255,0.07) !important;
  border-radius: 20px !important;
  padding: 40px 44px !important;
  box-shadow: 0 8px 40px rgba(0,0,0,0.6), 0 1px 0 rgba(255,255,255,0.04) inset !important;
  backdrop-filter: blur(20px) !important;
}
/* Brand title */
.brand-title {
  font-size: 28px !important;
  font-weight: 800 !important;
  letter-spacing: -0.04em !important;
  color: #eef2ff !important;
}
/* Form inputs */
.stTextInput input {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 10px !important;
  color: #eef2ff !important;
  font-size: 14px !important;
  padding: 12px 16px !important;
  height: 46px !important;
}
.stTextInput input:focus {
  border-color: rgba(99,102,241,0.5) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}
/* Sign-in button */
div[data-testid="stButton"] > button[kind="primary"] {
  height: 46px !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  letter-spacing: 0.02em !important;
  border-radius: 10px !important;
}
/* Left panel gradient shape */
.hero-bg {
  background: radial-gradient(ellipse 80% 60% at 40% 50%, rgba(99,102,241,0.18) 0%, rgba(99,102,241,0.04) 60%, transparent 100%) !important;
}
/* Orb glow pulse */
@keyframes si-pulse{
  0%,100%{box-shadow:0 0 50px 15px rgba(99,102,241,.22),0 0 100px 30px rgba(79,126,248,.08);}
  50%{box-shadow:0 0 80px 28px rgba(99,102,241,.35),0 0 150px 55px rgba(79,126,248,.14);}
}
/* Orbital ring spin (applied inside a tilted wrapper) */
@keyframes si-ring-spin{from{transform:rotate(0deg);}to{transform:rotate(360deg);}}
/* Secondary slower ring */
@keyframes si-ring-spin2{from{transform:rotate(0deg);}to{transform:rotate(-360deg);}}
/* Atmospheric shimmer on the globe */
@keyframes si-shimmer{
  0%,100%{opacity:.18;} 50%{opacity:.32;}
}
</style>
""", unsafe_allow_html=True)

    _col_l, _col_r = st.columns([1.1, 0.9], gap="small")

    # ── LEFT: entire visual in one self-contained HTML div ────────────────────
    with _col_l:
        st.markdown("""
<div style="
  min-height:100vh;width:100%;box-sizing:border-box;
  background:radial-gradient(ellipse at 30% 20%,#11173a 0%,#07090f 70%);
  padding:clamp(32px,6vh,72px) clamp(28px,6vw,80px);
  display:flex;flex-direction:column;justify-content:flex-start;
  position:relative;overflow:hidden;
">
  <!-- star field -->
  <div style="position:absolute;inset:0;pointer-events:none;z-index:0;
    background-image:
      radial-gradient(1px 1px at 13% 22%,rgba(255,255,255,.5) 0,transparent 50%),
      radial-gradient(1px 1px at 28% 78%,rgba(255,255,255,.32) 0,transparent 50%),
      radial-gradient(1px 1px at 41% 14%,rgba(255,255,255,.4) 0,transparent 50%),
      radial-gradient(1px 1px at 9% 54%,rgba(255,255,255,.3) 0,transparent 50%),
      radial-gradient(1px 1px at 62% 35%,rgba(255,255,255,.28) 0,transparent 50%),
      radial-gradient(1px 1px at 21% 38%,rgba(255,255,255,.25) 0,transparent 50%);
    opacity:.65;">
  </div>

  <!-- brand row -->
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;position:relative;z-index:1">
    <div style="width:38px;height:38px;border-radius:11px;
      background:linear-gradient(135deg,#6366f1,#4f46e5);
      display:grid;place-items:center;color:#fff;font-weight:800;font-size:16px;
      box-shadow:0 0 0 1px rgba(255,255,255,.12) inset,0 8px 24px rgba(99,102,241,.45)">A</div>
    <span style="font-size:22px;font-weight:800;letter-spacing:-.02em;color:#eef0f8">
      Audit<b style="color:#818cf8">IQ</b></span>
    <span style="font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
      background:rgba(99,102,241,.14);border:1px solid rgba(99,102,241,.3);
      color:#818cf8;padding:2px 8px;border-radius:999px">Pro</span>
  </div>

  <!-- abstract brand mark -->
  <div style="margin:22px 0 26px;position:relative;z-index:1">
    <div style="width:72px;height:72px;border-radius:20px;
      background:linear-gradient(135deg,#6366f1 0%,#4f46e5 60%,#3730a3 100%);
      display:grid;place-items:center;
      box-shadow:0 0 0 1px rgba(255,255,255,.1) inset,0 12px 40px rgba(99,102,241,.5),0 0 80px rgba(99,102,241,.15)">
      <span style="font-size:32px;font-weight:900;color:#fff;letter-spacing:-.04em">A</span>
    </div>
  </div>

  <!-- hero headline -->
  <h1 style="font-size:clamp(26px,3.5vw,46px);font-weight:800;
    letter-spacing:-.03em;line-height:1.06;color:#eef0f8;margin:0 0 10px;position:relative;z-index:1">
    Audit bancaire,<br>
    <span style="background:linear-gradient(120deg,#aab6ff 0%,#6366f1 70%);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
      augmenté par l'IA.
    </span>
  </h1>
  <p style="font-size:12px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;
    color:#8392bb;margin:0 0 22px;position:relative;z-index:1">
    CH · SG · HK · Bahamas · EU · UK</p>

  <!-- jurisdiction flags -->
  <div style="display:flex;flex-wrap:wrap;gap:8px;position:relative;z-index:1">
""" + "".join(
        f'<span style="display:inline-flex;align-items:center;gap:5px;padding:5px 12px;'
        f'border-radius:999px;background:rgba(255,255,255,.04);'
        f'border:1px solid rgba(255,255,255,.08);font-size:13px;font-weight:700;color:#c9cde0">'
        f'{_JUR_FLAG.get(j,"🌐")} {j.split("/")[1].strip()}</span>'
        for j in JURISDICTIONS
    ) + """
  </div>
</div>
""", unsafe_allow_html=True)

    # ── RIGHT: dark panel header + native Streamlit form ─────────────────────
    with _col_r:
        # Header only — no min-height so fields sit immediately below
        st.markdown("""
<div style="
  padding:28px clamp(20px,4vw,52px) 0;
  background:linear-gradient(180deg,rgba(11,15,26,.9),rgba(7,9,15,.96));
  border-left:1px solid rgba(255,255,255,.08);
  box-sizing:border-box;">
<h2 style="font-size:26px;font-weight:800;letter-spacing:-.02em;color:#eef0f8;margin:0 0 6px">
  Connexion</h2>
<p style="font-size:13.5px;color:#8392bb;margin:0 0 20px;line-height:1.5">
  Accédez à votre espace d'audit sécurisé.</p>
<p style="font-size:12px;font-weight:600;color:#c9cde0;letter-spacing:.02em;margin:0 0 4px">
  Adresse e-mail</p>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="si-field" style="padding:0 clamp(20px,4vw,52px);margin-top:-4px">', unsafe_allow_html=True)
        _email = st.text_input("email", value="lucas.brunner@helvetia-private.ch",
                               label_visibility="collapsed", key="si_email")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div style="padding:0 clamp(20px,4vw,52px);
  background:linear-gradient(180deg,rgba(11,15,26,.9),rgba(7,9,15,.96));
  border-left:1px solid rgba(255,255,255,.08)">
<p style="font-size:12px;font-weight:600;color:#c9cde0;letter-spacing:.02em;margin:10px 0 4px">
  Mot de passe</p>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="si-field" style="padding:0 clamp(20px,4vw,52px);margin-top:-4px">', unsafe_allow_html=True)
        _pwd = st.text_input("pwd", value="auditiq-demo", type="password",
                             label_visibility="collapsed", key="si_pwd")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        st.markdown('<div class="si-btn-submit" style="padding:0 clamp(20px,4vw,52px)">', unsafe_allow_html=True)
        if st.button("Se connecter  →", key="si_submit", use_container_width=True):
            st.session_state.signed_in = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div style="padding:10px clamp(20px,4vw,52px) 0;
  background:linear-gradient(180deg,rgba(11,15,26,.9),rgba(7,9,15,.96));
  border-left:1px solid rgba(255,255,255,.08)">
<div style="display:flex;align-items:center;gap:12px;color:#5a6488;
  font-size:11px;text-transform:uppercase;letter-spacing:.1em;margin:2px 0 10px">
  <div style="flex:1;height:1px;background:rgba(255,255,255,.08)"></div>
  <span>ou</span>
  <div style="flex:1;height:1px;background:rgba(255,255,255,.08)"></div>
</div>
</div>
""", unsafe_allow_html=True)

        _c1, _c2 = st.columns(2, gap="small")
        with _c1:
            st.markdown('<div class="si-btn-sso" style="padding:0 0 0 clamp(20px,4vw,52px)">', unsafe_allow_html=True)
            if st.button("🔑  SSO", key="si_sso1", use_container_width=True):
                st.session_state.signed_in = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with _c2:
            st.markdown('<div class="si-btn-sso">', unsafe_allow_html=True)
            if st.button("🪪  Carte", key="si_sso2", use_container_width=True):
                st.session_state.signed_in = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # Security badges
        st.markdown("""
<div style="padding:20px clamp(20px,4vw,52px) 32px;
  background:linear-gradient(180deg,rgba(11,15,26,.9),rgba(7,9,15,.96));
  border-left:1px solid rgba(255,255,255,.08);
  display:flex;flex-direction:column;align-items:center;gap:10px">
  <span style="display:inline-flex;align-items:center;gap:6px;font-size:9px;
    font-weight:700;letter-spacing:.06em;text-transform:uppercase;
    background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.25);
    color:#22c55e;padding:3px 10px;border-radius:999px">
    <span style="width:5px;height:5px;border-radius:50%;background:#22c55e;
      display:inline-block"></span>
    Connexion chiffrée · TLS 1.3
  </span>
  <span style="font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:#5a6488">
    AuditIQ · Banque privée suisse</span>
</div>
""", unsafe_allow_html=True)

    st.stop()




# ── Help content ──────────────────────────────────────────────────────────────

_HELP = {
    0: {  # Intelligence Dashboard
        "Français": """**🌐 Tableau de bord Intelligence**
*Votre veille réglementaire et cyber en un coup d'œil — avant même d'ouvrir un dossier.*

**À quoi ça sert ?**
→ Rester informé avant de lancer un audit : régulations récentes, CVEs, recommandations publiques.

**Comment l'utiliser ?**
- 📚 **Données statiques** : référentiel intégré, disponible sans connexion
- ⚡ **Live** : données en temps réel depuis sources publiques

**Les sections :**
- 🔴 **CVEs** : vulnérabilités cyber bancaires récentes
- 📰 **Réglementation** : publications FINMA, MAS, FCA, EBA…
- 🏦 **Recommandations** : bonnes pratiques publiques d'audit bancaire
- 📋 **Snapshot** : résumé de votre dernier rapport généré

💡 *Astuce : commencez ici pour identifier votre prochain sujet d'audit.*

**🎙️ Commande vocale :** Cliquez sur l'icône 🎙️ dans la barre latérale et dites : "Dashboard", "Analyse des Risques", "Audit Plan", "Document", "Rapport", "Help".""",

        "English": """**🌐 Intelligence Dashboard**
*Your regulatory and cyber radar — know what's moving before you open a file.*

**What is it for?**
→ Stay informed before launching an audit: recent regulations, CVEs, public recommendations.

**How to use it?**
- 📚 **Static data**: built-in knowledge base, no internet required
- ⚡ **Live**: real-time data from public sources

**Sections:**
- 🔴 **CVEs**: recent banking cyber vulnerabilities
- 📰 **Regulatory**: FINMA, MAS, FCA, EBA publications
- 🏦 **Recommendations**: public banking audit best practices
- 📋 **Snapshot**: summary of your last generated report

💡 *Tip: start here to identify your next audit topic.*

**🎙️ Voice command:** Click the 🎙️ icon in the sidebar and say: "Dashboard", "Risk Analysis", "Audit Plan", "Document", "Report", "Help".""",
    },
    1: {  # Risk Analysis
        "Français": """**🔍 Analyse des Risques**
*En 30 secondes, obtenez la cartographie complète des risques et des réglementations applicables à votre mission.*

**À quoi ça sert ?**
→ Identifier les risques et réglementations applicables à votre sujet d'audit.

**Comment remplir les champs ?**
- **Audit Topic** : saisissez le thème — ex. AML/KYC, Cyber Risk, Credit Risk
  → Ou choisissez un template dans *Quick Start Template*
- **Jurisdictions** : sélectionnez tous les pays applicables à l'entité auditée

**Résultats obtenus :**
- Cartographie des risques par niveau
- Réglementations applicables
- Recommandations publiques sur ce thème

💡 *Astuce : les données statiques suffisent pour 80% des missions. Utilisez Live uniquement pour les sujets très récents.*""",

        "English": """**🔍 Risk Analysis**
*In 30 seconds, get a full risk map and the exact regulations that apply to your engagement.*

**What is it for?**
→ Identify risks and applicable regulations for your audit topic.

**How to fill in the fields?**
- **Audit Topic**: enter the theme — e.g. AML/KYC, Cyber Risk, Credit Risk
  → Or pick a template from *Quick Start Template*
- **Jurisdictions**: select all countries applicable to the audited entity

**Results:**
- Risk map by severity level
- Applicable regulations
- Public recommendations on this topic

💡 *Tip: static data covers 80% of missions. Use Live only for very recent topics.*""",
    },
    2: {  # Audit Plan & Testing
        "Français": """**📋 Plan d'Audit & Tests**
*De l'analyse des risques au programme de tests complet — prêt à exporter en quelques clics.*

**À quoi ça sert ?**
→ Construire le plan d'audit et la liste des tests à réaliser.

**Comment remplir les champs ?**
- **Audit Topic** : pré-rempli depuis l'onglet 1, modifiable
- **Audit Scope** : décrivez le périmètre — ex. *"Processus KYC, entités CH et SG, période 2024"*

**Résultats obtenus :**
- **Rationale** : pourquoi cet audit
- **Background** : contexte et enjeux
- **Tests** : liste détaillée avec lien vers les risques associés
- **Data Analytics** : scénarios d'analyse possibles

💡 *Astuce : vérifiez le "Risk Coverage Summary" — tout risque Critical doit avoir au moins 1 test.*""",

        "English": """**📋 Audit Plan & Testing**
*From risk analysis to a complete test programme — ready to export in a few clicks.*

**What is it for?**
→ Build the audit plan and test list.

**How to fill in the fields?**
- **Audit Topic**: pre-filled from tab 1, editable
- **Audit Scope**: describe the perimeter — e.g. *"KYC process, CH and SG entities, FY2024"*

**Results:**
- **Rationale**: why this audit
- **Background**: context and issues
- **Tests**: detailed list linked to associated risks
- **Data Analytics**: possible analysis scenarios

💡 *Tip: check the "Risk Coverage Summary" — every Critical risk must have at least 1 test.*""",
    },
    3: {  # Document Analyser
        "Français": """**📂 Analyseur de Documents**
*Déposez vos documents — le bon spécialiste IA prend le relais automatiquement selon votre domaine.*

**À quoi ça sert ?**
→ Analyser des documents d'audit (politiques, rapports, données MIS) et identifier des observations, avec un expert IA adapté au domaine.

**Détection automatique du spécialiste**
L'IA sélectionne le bon profil d'expert selon le topic saisi :
- *AML/KYC* → **Spécialiste AML & KYC** (CAMS · FATF · FINMA 2011/1)
- *Cyber / DORA* → **Spécialiste Cyber & Tech Risk** (CISSP · ISO 27001 · DORA)
- *Third Party* → **Spécialiste Third Party Risk** (CRISC · FINMA 2018/3)
- *Credit Risk* → **Spécialiste Crédit & Capital** (FRM · Bâle IV · IFRS 9)
- *GDPR* → **Spécialiste Data Privacy** (CIPP/E · RGPD · nDSG)
- *Governance / Op Risk / Market Risk* → profils dédiés

**Comment l'utiliser ?**
- **Upload** : glissez-déposez vos fichiers (PDF, Word, Excel, TXT — multi-fichiers)
- **Topic** : pré-rempli depuis l'onglet 1, modifiable
- **Context** : précisez un focus — ex. *"Concentrez-vous sur les écarts politique/pratique"*

**Résultats obtenus :**
- Observations par niveau de risque (Critical / High / Moderate / Low)
- Lien automatique vers les tests du programme d'audit
- **➕ Add to Report** pour pousser chaque observation vers l'onglet Rapport

💡 *Astuce : uploadez des rapports précédents pour identifier les thèmes récurrents.*""",

        "English": """**📂 Document Analyser**
*Drop your documents — the right AI specialist steps in automatically based on your audit domain.*

**What is it for?**
→ Analyse audit documents (policies, reports, MIS data) and surface observations, with a domain-matched AI expert.

**Automatic specialist detection**
The AI selects the right expert profile based on the topic you enter:
- *AML/KYC* → **AML & KYC Compliance Specialist** (CAMS · FATF · FINMA 2011/1)
- *Cyber / DORA* → **Cyber & Technology Risk Specialist** (CISSP · ISO 27001 · DORA)
- *Third Party* → **Third Party Risk Specialist** (CRISC · FINMA 2018/3)
- *Credit Risk* → **Credit Risk & Capital Specialist** (FRM · Basel IV · IFRS 9)
- *GDPR* → **Data Privacy Specialist** (CIPP/E · GDPR · nDSG)
- *Governance / Op Risk / Market Risk* → dedicated profiles

**How to use it?**
- **Upload**: drag-and-drop your files (PDF, Word, Excel, TXT — multiple files supported)
- **Topic**: pre-filled from tab 1, editable
- **Context**: specify a focus area — e.g. *"Focus on gaps between policy and practice"*

**Results:**
- Observations by risk level (Critical / High / Moderate / Low)
- Automatic link to audit programme tests
- **➕ Add to Report** button to push each observation to the Audit Report tab

💡 *Tip: upload prior audit reports to surface recurring themes.*""",
    },
    4: {  # Audit Report
        "Français": """**📄 Rapport d'Audit**
*Du constat brut au rapport IIA-standard prêt pour le comité — en un seul écran.*

**À quoi ça sert ?**
→ Assembler le rapport final, gérer les recommandations, et générer le résumé comité.

**📋 Recommendations**
- **📝 My Observations** : vos observations (depuis Document Analyser ou saisie manuelle) + génération des recommandations
- **📄 Example Report** : exemple de constat IIA-standard pré-rempli, comme modèle de référence

**📄 Report** — 4 sous-sections :
1. **Executive Summary** : résumé 1 page pour le comité d'audit, exportable en PDF
2. **Narrative & Findings** : storytelling du rapport complet + fiches de constats
3. **Recommendation Details** : détail structuré de chaque observation (repris en direct du sous-onglet Recommendations)
4. **KPIs** : métriques de la mission — risques, couverture des tests, constats par criticité, recos N-1 ouvertes

**Exports disponibles :** Word (docx) · Excel (xlsx) · PowerPoint (pptx) · PDF

**🎙️ Commande vocale :**
- Dites *"Rapport"* ou *"Report"* pour naviguer ici directement

💡 *Astuce : complétez d'abord les onglets 1, 2 et 3 pour un rapport plus riche et contextualisé.*""",

        "English": """**📄 Audit Report**
*From raw findings to an IIA-standard report ready for the audit committee — in one screen.*

**What is it for?**
→ Assemble the final report, manage recommendations, and generate the committee summary.

**📋 Recommendations**
- **📝 My Observations**: your observations (from Document Analyser or manual entry) + recommendation generation
- **📄 Example Report**: a pre-filled IIA-standard finding shown as a reference template

**📄 Report** — 4 sub-sections:
1. **Executive Summary**: 1-page committee-ready summary, exportable as PDF
2. **Narrative & Findings**: full report storytelling + finding cards
3. **Recommendation Details**: structured detail for every observation (pulled live from the Recommendations tab)
4. **KPIs**: engagement metrics — risks, test coverage, findings by criticality, open N-1 recommendations

**Available exports:** Word (docx) · Excel (xlsx) · PowerPoint (pptx) · PDF

**🎙️ Voice command:**
- Say *"Report"* or *"Rapport"* to navigate here directly

💡 *Tip: complete tabs 1, 2, and 3 first for a richer, more contextualised report.*""",
    },
    5: {  # Continuous Audit Dashboard
        "Français": """**📡 Audit Continu**
*Vos contrôles tournent 24h/24 — cet écran vous dit ce qui a échoué cette nuit.*

**À quoi ça sert ?**
→ Superviser en temps réel l'efficacité des contrôles automatisés et détecter les anomalies avant qu'elles deviennent des constats d'audit.

**Les 4 blocs :**
- **⚙ Automated Control Tests** : résultats des contrôles automatisés (fréquence, couverture population, Pass / Fail / Exception)
- **🔴 Exception Feed** : sorties brutes des tests — breaks de réconciliation, retards STR, dépassements VaR, avec impact CHF
- **📈 Control Health — 12 semaines** : sparklines colorées par contrôle pour visualiser les tendances de dégradation
- **🗺 Coverage Matrix** : grille Entités × Processus — identifiez d'un coup d'œil les zones sans monitoring continu

**Comment lire la matrice de couverture ?**
- 🟢 **Continuous** : contrôle automatisé actif
- 🔵 **Periodic** : audit périodique planifié
- 🟠 **Gap** : lacune identifiée, action requise
- 🔴 **None** : aucune couverture

💡 *Astuce : un contrôle en rouge 3 semaines de suite dans les sparklines doit déclencher une mission d'audit ciblée.*""",

        "English": """**📡 Continuous Audit Dashboard**
*Your controls run 24/7 — this screen tells you what failed last night.*

**What is it for?**
→ Monitor automated control effectiveness in real time and detect anomalies before they become audit findings.

**The 4 blocks:**
- **⚙ Automated Control Tests**: automated control results (frequency, population coverage, Pass / Fail / Exception)
- **🔴 Exception Feed**: raw test outputs — reconciliation breaks, STR delays, VaR breaches, with CHF impact
- **📈 Control Health — 12 weeks**: colour-coded sparklines per control to visualise degradation trends
- **🗺 Coverage Matrix**: Entities × Processes grid — spot coverage gaps at a glance

**How to read the coverage matrix:**
- 🟢 **Continuous**: active automated control
- 🔵 **Periodic**: periodic audit scheduled
- 🟠 **Gap**: gap identified, action needed
- 🔴 **None**: no coverage at all

💡 *Tip: a control showing red 3 weeks in a row in the sparklines should trigger a targeted audit engagement.*""",
    },
    6: {  # Third Party & Vendor 360
        "Français": """**🏢 Third Party & Vendor 360**
*Chaque fournisseur est un vecteur de risque — cet écran le rend visible avant que le régulateur ne le signale.*

**À quoi ça sert ?**
→ Piloter le risque tiers en un seul écran : scoring de risque, statut KYC, SLA, actions ouvertes et couverture réglementaire.

**Les sections :**
- **KPI row** : nombre de fournisseurs, critiques, révisions dues, brèches SLA
- **Vendor Scorecard** : tableau de bord des 8 principaux fournisseurs avec score de risque (0–100), statut KYC, état SLA
- **Critical vendor drill-down** : fiche détaillée Clearstream avec valeur contrat, entités, plan de sortie et actions ouvertes
- **Regulatory refs** : FINMA 2018/3 · MAS TRM · FCA SS2/21 · DORA Art. 28-30 · EBA

**Comment lire le score de risque ?**
- 🟢 ≥ 85 : risque faible
- 🟠 70–84 : surveillance renforcée
- 🔴 < 70 : action immédiate requise

💡 *Astuce : un fournisseur avec SLA "Breach" et score < 80 doit être escaladé au responsable des achats et au MLRO.*""",

        "English": """**🏢 Third Party & Vendor 360**
*Every vendor is a risk vector — this screen makes it visible before the regulator flags it.*

**What is it for?**
→ Manage third-party risk in a single screen: risk scoring, KYC status, SLA, open actions, and regulatory coverage.

**Sections:**
- **KPI row**: number of vendors, critical vendors, due reviews, SLA breaches
- **Vendor Scorecard**: dashboard of top vendors with risk score (0–100), KYC status, SLA health
- **Critical vendor drill-down**: Clearstream detail card with contract value, entities, exit plan, and open actions
- **Regulatory refs**: FINMA 2018/3 · MAS TRM · FCA SS2/21 · DORA Art. 28-30 · EBA

**How to read the risk score?**
- 🟢 ≥ 85: low risk
- 🟠 70–84: enhanced monitoring needed
- 🔴 < 70: immediate action required

💡 *Tip: a vendor with SLA "Breach" and score below 80 should be escalated to the procurement lead and MLRO.*""",
    },
    7: {  # KYC / AML Compliance
        "Français": """**🔍 KYC / AML Compliance**
*Détectez la criminalité financière avant que le régulateur ne vous pose la question.*

**À quoi ça sert ?**
→ Superviser la file PEP/Sanctions, piloter la pipeline de remédiation et suivre la couverture CDD/EDD.

**Les sections :**
- **KPI row** : clients revus, PEP flaggés, hits sanctions, remédiations ouvertes
- **PEP / Sanctions Alert Queue** : tableau des alertes actives avec niveau de risque, type (PEP / Sanctions / Adverse Media), juridiction, statut et ancienneté
- **Remediation Pipeline** : Kanban en 3 colonnes — *To Review / In Progress / Closed* — avec priorité colorée par risque
- **CDD / EDD Coverage** : jauges SVG de couverture CDD standard, EDD renforcée, revues PEP, screening sanctions

**Comment lire les statuts de la file ?**
- 🔴 **Escalated** : dossier remonté au MLRO ou à la direction
- 🔵 **In Review** : EDD ou entretien client en cours
- 🟠 **Pending** : en attente d'affectation
- 🟢 **Assigned** : auditeur désigné

**Références réglementaires :** FATF R.10 · FINMA AML Circ. 2011/1 · MAS Notice 626 · AMLD6 · UK POCA 2002

💡 *Astuce : tout client avec statut "Escalated" depuis > 5 jours doit faire l'objet d'un suivi écrit dans le système de gestion des incidents.*""",

        "English": """**🔍 KYC / AML Compliance**
*Catch financial crime before the regulator asks the question.*

**What is it for?**
→ Monitor the PEP/Sanctions alert queue, drive the remediation pipeline, and track CDD/EDD coverage.

**Sections:**
- **KPI row**: clients reviewed, PEP flagged, sanctions hits, open remediations
- **PEP / Sanctions Alert Queue**: active alert table with risk level, flag type (PEP / Sanctions / Adverse Media), jurisdiction, status, and age
- **Remediation Pipeline**: 3-column Kanban — *To Review / In Progress / Closed* — with colour-coded risk priority
- **CDD / EDD Coverage**: SVG gauge charts for standard CDD, enhanced EDD, PEP reviews, sanctions screening

**How to read alert queue statuses?**
- 🔴 **Escalated**: case referred to MLRO or senior management
- 🔵 **In Review**: EDD or client interview in progress
- 🟠 **Pending**: awaiting assignment
- 🟢 **Assigned**: auditor designated

**Regulatory references:** FATF R.10 · FINMA AML Circ. 2011/1 · MAS Notice 626 · AMLD6 · UK POCA 2002

💡 *Tip: any client with "Escalated" status for more than 5 days must have a written follow-up logged in the incident management system.*""",
    },
}

def _show_help_panel():
    """Render the contextual help panel in the sidebar."""
    lang = st.session_state.get("help_lang", "Français")
    tab_idx = st.session_state.get("active_tab", 0)

    # Language selector — compact, full sidebar width
    new_lang = st.radio(
        "Language", ["🇫🇷 Français", "🇬🇧 English"],
        index=0 if lang == "Français" else 1,
        horizontal=True, label_visibility="collapsed",
        key="_help_lang_radio",
    )
    st.session_state["help_lang"] = "English" if "English" in new_lang else "Français"
    lang = st.session_state["help_lang"]

    # Tab selector — selectbox fits the narrow sidebar width
    tab_labels = _TAB_NAMES[lang]
    _safe_idx = tab_idx if tab_idx < len(tab_labels) else 0
    selected_tab = st.selectbox(
        "Section", tab_labels,
        index=_safe_idx,
        label_visibility="collapsed",
        key="_help_tab_select",
    )
    selected_idx = tab_labels.index(selected_tab)

    # Render content
    content = _HELP.get(selected_idx, {}).get(lang, "")
    st.markdown('<hr style="border:0;border-top:1px solid rgba(127,168,251,0.2);margin:8px 0 10px"/>', unsafe_allow_html=True)
    st.markdown(content)

    if st.button("✕ Close help", key="_help_close", use_container_width=True):
        st.session_state["help_open"] = False
        st.rerun()


# ── Shared state used by header and sidebar ───────────────────────────────────
_cur_ent   = st.session_state.get("entity_type", "🏦 Private Banking")
_cur_t     = _ENTITY_THEMES.get(_cur_ent, _ENTITY_THEMES["🏦 Private Banking"])
_active    = st.session_state.get("active_tab", 0)
_NAV_NAMES = {
    0: "Intelligence Dashboard",
    1: "Risk Analysis",
    2: "Audit Plan & Testing",
    3: "Document Analyser",
    4: "Audit Report",
}

# ── Entity switcher CSS (sidebar pills) ──────────────────────────────────────
_ent_btn_css = ""
for _ename, _et in _ENTITY_THEMES.items():
    _sl = _ent_slug(_ename)
    _ent_btn_css += f"""
    .ent-{_sl} button{{
      background:rgba(255,255,255,.04) !important;
      border:1px solid {_et['primary']}44 !important;
      color:{_et['primary']} !important;
      border-radius:8px !important;
      font-size:11px !important; font-weight:600 !important;
      height:32px !important; min-width:0 !important;
      white-space:nowrap !important; overflow:hidden !important;
      text-overflow:ellipsis !important; transition:all .15s;
    }}
    .ent-{_sl} button:hover{{
      background:{_et['sec_bg']} !important;
      border-color:{_et['primary']}88 !important;
    }}
    .ent-{_sl}-active button{{
      background:{_et['primary']} !important;
      border:1px solid {_et['primary']} !important;
      color:#fff !important; border-radius:8px !important;
      font-size:11px !important; font-weight:700 !important;
      height:32px !important; min-width:0 !important;
      white-space:nowrap !important; overflow:hidden !important;
      text-overflow:ellipsis !important;
      box-shadow:0 0 12px {_et['glow']} !important;
    }}
    """
st.markdown(f"<style>{_ent_btn_css}</style>", unsafe_allow_html=True)

# ── Sidebar nav CSS ───────────────────────────────────────────────────────────
_nav_primary = _cur_t["primary"]
_nav_glow    = _cur_t["glow"]
st.markdown(f"""<style>
.nav-item button{{
  background:transparent !important; border:none !important;
  color:#8392bb !important; text-align:left !important;
  font-size:13px !important; font-weight:500 !important;
  padding:8px 16px !important; width:100% !important;
  border-radius:8px !important; justify-content:flex-start !important;
}}
.nav-item button:hover{{
  background:rgba(255,255,255,0.05) !important; color:#eef0f8 !important;
}}
.nav-active button{{
  background:{_nav_primary}22 !important; border:none !important;
  color:{_nav_primary} !important; text-align:left !important;
  font-size:13px !important; font-weight:700 !important;
  padding:8px 16px !important; width:100% !important;
  border-radius:8px !important; justify-content:flex-start !important;
  box-shadow:0 0 8px {_nav_glow} !important;
}}
.nav-stub button{{
  background:transparent !important; border:none !important;
  color:#3d4a6b !important; text-align:left !important;
  font-size:13px !important; font-weight:400 !important;
  padding:8px 16px !important; width:100% !important;
  border-radius:8px !important; justify-content:flex-start !important;
  cursor:default !important;
}}
</style>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # ── Logo ─────────────────────────────────────────────────────────────────
    st.markdown(f"""
<div style="padding:20px 16px 12px;border-bottom:1px solid rgba(255,255,255,0.07)">
  <div style="display:flex;align-items:center;gap:10px">
    <div style="width:36px;height:36px;border-radius:10px;flex-shrink:0;
      background:{_cur_t['bg_btn']};display:grid;place-items:center;
      box-shadow:0 0 16px {_cur_t['glow']}">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <div>
      <span style="font-size:18px;font-weight:800;letter-spacing:-.02em;color:#eef0f8">
        Audit<span style="color:{_cur_t['hover']}">IQ</span>
      </span>
      <span style="font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
        background:rgba(99,102,241,.18);border:1px solid rgba(99,102,241,.3);
        color:#818cf8;padding:1px 7px;border-radius:999px;margin-left:6px">Pro</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Workflow status for nav dots ─────────────────────────────────────────
    _wf_status = {
        0: "done" if (st.session_state.get("dash_regs") or st.session_state.get("t1_pub_recs")) else "idle",
        1: "done" if st.session_state.get("t1_risks") else ("active" if _active == 1 else "idle"),
        2: "done" if st.session_state.get("t2_tests") else ("active" if _active == 2 else "idle"),
        3: "done" if st.session_state.get("t3_docs_analysis") else ("active" if _active == 3 else "idle"),
        4: "done" if st.session_state.get("t3_report") else ("active" if _active == 4 else "idle"),
        5: "done",
        6: "done",
        7: "done",
    }
    _WF_DOT = {
        "done":   "background:#22d3a5",
        "active": "background:#f97316",
        "idle":   "background:#2d3a4e",
    }

    # ── MENU section ─────────────────────────────────────────────────────────
    st.markdown("""
<div style="padding:16px 16px 4px">
  <span style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3d4a6b">Menu</span>
</div>
""", unsafe_allow_html=True)

    _cls0 = "nav-active" if _active == 0 else "nav-item"
    st.markdown(f'<div class="{_cls0}">', unsafe_allow_html=True)
    if st.button("⊞  Tableau de bord", key="_nav0", use_container_width=True):
        st.session_state["active_tab"] = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if _wf_status[0] == "done":
        st.markdown('<div style="font-size:10px;color:#22d3a5;margin:-12px 0 4px 14px;font-weight:600">✓ up to date</div>', unsafe_allow_html=True)
    elif _wf_status[0] == "active":
        st.markdown('<div style="font-size:10px;color:#f97316;margin:-12px 0 4px 14px;font-weight:600">● active</div>', unsafe_allow_html=True)

    _cls1 = "nav-active" if _active == 1 else "nav-item"
    st.markdown(f'<div class="{_cls1}">', unsafe_allow_html=True)
    if st.button("≡  Risk Analysis", key="_nav1", use_container_width=True):
        st.session_state["active_tab"] = 1
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if _wf_status[1] == "done":
        st.markdown('<div style="font-size:10px;color:#22d3a5;margin:-12px 0 4px 14px;font-weight:600">✓ up to date</div>', unsafe_allow_html=True)
    elif _wf_status[1] == "active":
        st.markdown('<div style="font-size:10px;color:#f97316;margin:-12px 0 4px 14px;font-weight:600">● active</div>', unsafe_allow_html=True)

    # ── AGENTS IA section ────────────────────────────────────────────────────
    st.markdown("""
<div style="padding:16px 16px 4px">
  <span style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3d4a6b">Agents IA</span>
</div>
""", unsafe_allow_html=True)

    _cls2 = "nav-active" if _active == 2 else "nav-item"
    st.markdown(f'<div class="{_cls2}">', unsafe_allow_html=True)
    if st.button("📋  Audit Plan & Testing", key="_nav2", use_container_width=True):
        st.session_state["active_tab"] = 2
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if _wf_status[2] == "done":
        st.markdown('<div style="font-size:10px;color:#22d3a5;margin:-12px 0 4px 14px;font-weight:600">✓ up to date</div>', unsafe_allow_html=True)
    elif _wf_status[2] == "active":
        st.markdown('<div style="font-size:10px;color:#f97316;margin:-12px 0 4px 14px;font-weight:600">● active</div>', unsafe_allow_html=True)

    _cls3 = "nav-active" if _active == 3 else "nav-item"
    st.markdown(f'<div class="{_cls3}">', unsafe_allow_html=True)
    if st.button("🔍  Document Analyser", key="nav_3", use_container_width=True):
        st.session_state["active_tab"] = 3
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if _wf_status[3] == "done":
        st.markdown('<div style="font-size:10px;color:#22d3a5;margin:-12px 0 4px 14px;font-weight:600">✓ up to date</div>', unsafe_allow_html=True)
    elif _wf_status[3] == "active":
        st.markdown('<div style="font-size:10px;color:#f97316;margin:-12px 0 4px 14px;font-weight:600">● active</div>', unsafe_allow_html=True)

    _cls4 = "nav-active" if _active == 4 else "nav-item"
    st.markdown(f'<div class="{_cls4}">', unsafe_allow_html=True)
    if st.button("📄  Rapport d'audit", key="_nav3", use_container_width=True):
        st.session_state["active_tab"] = 4
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if _wf_status[4] == "done":
        st.markdown('<div style="font-size:10px;color:#22d3a5;margin:-12px 0 4px 14px;font-weight:600">✓ up to date</div>', unsafe_allow_html=True)
    elif _wf_status[4] == "active":
        st.markdown('<div style="font-size:10px;color:#f97316;margin:-12px 0 4px 14px;font-weight:600">● active</div>', unsafe_allow_html=True)

    # ── MONITORING section ───────────────────────────────────────────────────
    st.markdown("""
<div style="padding:16px 16px 4px;border-top:1px solid rgba(255,255,255,0.05);margin-top:8px">
  <span style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3d4a6b">Monitoring</span>
</div>
""", unsafe_allow_html=True)

    _cls5 = "nav-active" if _active == 5 else "nav-item"
    st.markdown(f'<div class="{_cls5}">', unsafe_allow_html=True)
    if st.button("📡  Continuous Audit", key="_nav5", use_container_width=True):
        st.session_state["active_tab"] = 5
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;color:#22d3a5;margin:-12px 0 4px 14px;font-weight:600">✓ live</div>', unsafe_allow_html=True)

    _cls6 = "nav-active" if _active == 6 else "nav-item"
    st.markdown(f'<div class="{_cls6}">', unsafe_allow_html=True)
    if st.button("🏢  Vendor 360", key="_nav6", use_container_width=True):
        st.session_state["active_tab"] = 6
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;color:#22d3a5;margin:-12px 0 4px 14px;font-weight:600">✓ live</div>', unsafe_allow_html=True)

    _cls7 = "nav-active" if _active == 7 else "nav-item"
    st.markdown(f'<div class="{_cls7}">', unsafe_allow_html=True)
    if st.button("🔍  KYC / AML", key="_nav7", use_container_width=True):
        st.session_state["active_tab"] = 7
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;color:#22d3a5;margin:-12px 0 4px 14px;font-weight:600">✓ live</div>', unsafe_allow_html=True)

    # ── Entity selector (compact selectbox) ──────────────────────────────────
    st.markdown("""
<div style="padding:16px 16px 4px;border-top:1px solid rgba(255,255,255,0.05);margin-top:8px">
  <span style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3d4a6b">Environnement</span>
</div>
""", unsafe_allow_html=True)
    _ent_opts = list(_ENTITY_THEMES.keys())
    _ent_idx  = _ent_opts.index(_cur_ent) if _cur_ent in _ent_opts else 0
    _ent_sel  = st.selectbox(
        "Entité", _ent_opts, index=_ent_idx,
        key="_sb_entity_sel", label_visibility="collapsed",
    )
    if _ent_sel != _cur_ent:
        st.session_state["entity_type"] = _ent_sel
        st.rerun()

    # ── Jurisdiction flags ───────────────────────────────────────────────────
    _jurs_active = st.session_state.get("t1_jurs_pills") or st.session_state.get("t1_jurs") or []
    if not isinstance(_jurs_active, list):
        _jurs_active = list(_jurs_active)
    _flags_html = " ".join(
        f'<span title="{j}" style="font-size:16px;opacity:{1.0 if not _jurs_active or j in _jurs_active else 0.3}">'
        f'{_JUR_FLAG.get(j, "🌐")}</span>'
        for j in JURISDICTIONS
    )
    st.markdown(
        f'<div style="padding:6px 16px 12px;display:flex;flex-wrap:wrap;gap:6px">{_flags_html}</div>',
        unsafe_allow_html=True,
    )

    # ── Demo Mode toggle ──────────────────────────────────────────────────────
    _demo_on = st.session_state.get("demo_mode", False)
    _demo_cls = "demo-btn-active" if _demo_on else "demo-btn"
    _demo_lbl = "🎬 Demo Mode: ON" if _demo_on else "🎬 Demo Mode"
    st.markdown(f'<div style="padding:4px 8px 8px"><div class="{_demo_cls}">', unsafe_allow_html=True)
    if st.button(_demo_lbl, key="_demo_mode_btn", use_container_width=True):
        if not _demo_on:
            # Activate demo mode
            st.session_state["demo_mode"] = True
            st.session_state["t1_topic_in"] = _DEMO_CONTENT["topic"]
            st.session_state["t1_jurs_pills"] = _DEMO_CONTENT["jurisdictions"]
            st.session_state["t1_jurs_in"] = _DEMO_CONTENT["jurisdictions"]
            st.session_state["entity_type"] = _DEMO_CONTENT["entity"]
            st.session_state["_tpl_name"] = _DEMO_CONTENT["template"]
        else:
            # Deactivate demo mode
            st.session_state["demo_mode"] = False
            st.session_state["t1_topic_in"] = ""
            st.session_state["t1_jurs_pills"] = None
            st.session_state["t1_jurs_in"] = []
            st.session_state["entity_type"] = "🏦 Private Banking"
            st.session_state["_tpl_name"] = ""
            st.session_state["t1_risks"] = None
            st.session_state["t2_rationale"] = None
            st.session_state["t2_background"] = None
            st.session_state["t2_org_plan"] = None
            st.session_state["t3_report"] = None
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Utility buttons (dark mode only — no theme toggle) ───────────────────
    st.markdown('<div style="padding:8px 8px 4px;border-top:1px solid rgba(255,255,255,0.05)">', unsafe_allow_html=True)
    _sb_u2, _sb_u3, _sb_u4 = st.columns(3, gap="small")
    _voice_cls = "util-voice-active" if st.session_state.get("voice_active") else ""
    with _sb_u2:
        st.markdown(f'<div class="{_voice_cls}">', unsafe_allow_html=True)
        if st.button("🎙️", key="_voice_toggle_btn", help="Commande vocale"):
            st.session_state["voice_active"] = not st.session_state.get("voice_active", False)
            if not st.session_state["voice_active"]:
                st.session_state["last_voice_transcript"] = ""
        st.markdown("</div>", unsafe_allow_html=True)
    _cowork_cls = "util-cowork-active" if st.session_state.get("cowork_open") else ""
    with _sb_u3:
        st.markdown(f'<div class="{_cowork_cls}">', unsafe_allow_html=True)
        if st.button("✨", key="_cowork_toggle_btn", help="Suggestions Claude"):
            st.session_state["cowork_open"] = not st.session_state.get("cowork_open", False)
        st.markdown("</div>", unsafe_allow_html=True)
    _help_cls = "util-help-active" if st.session_state.get("help_open") else ""
    with _sb_u4:
        st.markdown(f'<div class="{_help_cls}">', unsafe_allow_html=True)
        if st.button("❓", key="_help_toggle_btn", help="Help / Aide"):
            st.session_state["help_open"] = not st.session_state.get("help_open", False)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── User info ────────────────────────────────────────────────────────────
    st.markdown(f"""
<div style="padding:12px 16px 20px;border-top:1px solid rgba(255,255,255,0.07)">
  <div style="display:flex;align-items:center;gap:10px">
    <div style="width:32px;height:32px;border-radius:50%;flex-shrink:0;
      background:{_cur_t['bg_btn']};display:grid;place-items:center;
      font-size:12px;font-weight:800;color:#fff">LB</div>
    <div style="flex:1;min-width:0">
      <div style="font-size:13px;font-weight:600;color:#eef0f8;
        white-space:nowrap;overflow:hidden;text-overflow:ellipsis">L. Brunner</div>
      <div style="font-size:11px;color:#5a6488">Auditeur senior</div>
    </div>
    <span style="font-size:16px">🔔</span>
  </div>
</div>
""", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
    if st.button("← Sign out", key="sidebar_logout", use_container_width=True):
        st.session_state["signed_in"] = False
        st.rerun()

    # ── Voice command panel ───────────────────────────────────────────────────
    if st.session_state.get("voice_active", False):
        st.markdown("""
<div style="border-top:1px solid rgba(255,255,255,.07);margin-top:12px;padding-top:12px">
  <span style="font-size:10px;font-weight:700;letter-spacing:.10em;text-transform:uppercase;color:#818cf8">🎙️ Voice Command</span>
</div>""", unsafe_allow_html=True)
        _vc_typed = st.text_input(
            "Command", placeholder="e.g. Risk Analysis, Dashboard…",
            key="_vc_text_input", label_visibility="collapsed",
        )
        st.caption("Try: Dashboard · Risk · Audit Plan · Document · Report · Help")
        if _vc_typed:
            _vc_t = _vc_typed.strip().lower()
            if any(w in _vc_t for w in ["dashboard", "tableau de bord", "accueil", "home"]):
                st.session_state["active_tab"] = 0
            elif any(w in _vc_t for w in ["risk", "risque", "analyse des risques", "risk analysis"]):
                st.session_state["active_tab"] = 1
            elif any(w in _vc_t for w in ["audit plan", "plan audit", "tests", "testing"]):
                st.session_state["active_tab"] = 2
            elif any(w in _vc_t for w in ["document", "analyser document"]):
                st.session_state["active_tab"] = 3
            elif any(w in _vc_t for w in ["rapport", "report", "recommandation"]):
                st.session_state["active_tab"] = 4
            elif any(w in _vc_t for w in ["help", "aide"]):
                st.session_state["help_open"] = True
            elif any(w in _vc_t for w in ["suggestion", "claude", "cowork"]):
                st.session_state["cowork_open"] = True
            st.session_state["last_voice_transcript"] = _vc_typed.strip()
            st.session_state["voice_active"] = False
            st.rerun()

    if st.session_state.get("last_voice_transcript") and not st.session_state.get("voice_active", False):
        _vt = st.session_state["last_voice_transcript"]
        _active_tab_name = {0: "Dashboard", 1: "Risk Analysis", 2: "Audit Plan",
                            3: "Document Analyser", 4: "Audit Report",
                            5: "Continuous Audit", 6: "Vendor 360", 7: "KYC / AML"}.get(
                            st.session_state.get("active_tab", 0), "")
        st.markdown(f"""
<div style="background:rgba(99,102,241,.08);border:1px solid rgba(99,102,241,.2);
  border-radius:8px;padding:8px 12px;margin-top:6px;font-size:11px">
  <span style="color:#818cf8;font-weight:600">✓</span>
  <span style="color:#94a3b8"> "{_vt}"</span>
  {f'<span style="color:#22d3a5"> → {_active_tab_name}</span>' if _active_tab_name else ""}
</div>""", unsafe_allow_html=True)

    # ── Claude Cowork panel ───────────────────────────────────────────────────
    if st.session_state.get("cowork_open", False):
        st.markdown("""
<div style="border-top:1px solid rgba(255,255,255,.07);margin-top:12px;padding-top:12px">
  <span style="font-size:10px;font-weight:700;letter-spacing:.10em;text-transform:uppercase;color:#f97316">✨ Claude Suggestions</span>
</div>""", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:11.5px;color:#6b7a99;margin:6px 0 8px;line-height:1.6">'
            'Context-aware suggestions will appear here. Integration in progress.</div>',
            unsafe_allow_html=True,
        )
        st.button("Generate suggestions", disabled=True, key="_cowork_generate_btn",
                  use_container_width=True)

    # ── Help panel ────────────────────────────────────────────────────────────
    if st.session_state.get("help_open", False):
        st.markdown("""
<div style="border-top:1px solid rgba(255,255,255,.07);margin-top:12px;padding-top:12px">
  <span style="font-size:10px;font-weight:700;letter-spacing:.10em;text-transform:uppercase;color:#22d3a5">❓ Help</span>
</div>""", unsafe_allow_html=True)
        _show_help_panel()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN HEADER (breadcrumb + new audit button)
# ══════════════════════════════════════════════════════════════════════════════
with st.container():
    _ent_display = _cur_ent.split(" ", 1)[1] if " " in _cur_ent and _cur_ent[0] in "🏦🏢🏗️💼🏛️" else _cur_ent
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:6px;padding:16px 0 8px">
  <span style="font-size:13px;color:#5a6488;font-weight:500">AuditIQ</span>
  <span style="color:#3d4a6b;font-size:13px">/</span>
  <span style="font-size:13px;font-weight:700;color:#eef0f8">{_NAV_NAMES.get(_active, "Dashboard")}</span>
  {_entity_badge_html(_ent_display)}
</div>
""", unsafe_allow_html=True)


if not _api_key:
    st.error("Access not configured. Please contact your administrator.")
    st.stop()
if not _READY:
    st.error(f"Required modules unavailable: {_ERR}")
    st.stop()

# ═════════════════════════════════════════════════════════════════════════════

# ── Report generation helpers ─────────────────────────────────────────────────

_CRIT_KW = {
    "Critical": ["critical","no control","zero control","absent","violation","breach",
                 "sanctions","illegal","prohibited","fraud","completely missing","total absence"],
    "High":     ["significant","material","major","inadequate","insufficient","not functioning",
                 "serious","systemic","pervasive","high risk","failing","not performed"],
    "Medium":   ["partial","limited","delayed","outdated","inconsistent","incomplete",
                 "gap","occasional","moderate","medium"],
    "Low":      ["minor","observation","enhancement","improvement","opportunity",
                 "suggestion","best practice","low"],
}

_THEME_KW_FINDING = {
    "AML_KYC":              ["kyc","aml","pep","cdd","edd","transaction monitoring","str",
                             "suspicious","watchlist","sanctions screening","beneficial owner","fatf"],
    "CYBER_RISK":           ["cyber","mfa","multifactor","vulnerability","patch","privileged",
                             "authentication","password","firewall","endpoint","dlp","backup"],
    "CREDIT_RISK":          ["credit","loan","collateral","ltv","concentration","lombard",
                             "exposure","provision","credit risk"],
    "OPERATIONAL_RISK":     ["operational","bcp","business continuity","rcsa","operational loss",
                             "process","manual error","incident","rpa"],
    "DATA_PRIVACY":         ["data","privacy","gdpr","ndsg","personal data","data breach",
                             "dpo","consent","retention"],
    "MARKET_RISK":          ["market risk","frtb","var","sensitivity","trading book",
                             "valuation","mark-to-model","structured product"],
    "THIRD_PARTY_RISK":     ["third party","vendor","outsourc","supplier","fourth party",
                             "right to audit","sub-contractor"],
    "GOVERNANCE":           ["governance","board","committee","three lines","independence",
                             "charter","conflict of interest","segregation of duties"],
    "LIQUIDITY_RISK":       ["liquidity","lcr","nsfr","hqla","deposit","run risk","funding gap"],
    "FRAUD":                ["fraud","misappropriation","fictitious","embezzlement","rogue"],
    "INVESTMENT_SUITABILITY": ["suitability","appropriateness","investment","product governance",
                             "kid","target market","mis-selling","finsa"],
    "TAX_COMPLIANCE":       ["tax","fatca","crs","aeoi","undeclared","withholding","tax evasion"],
    "CRYPTO":               ["crypto","digital asset","vasp","token","blockchain","stablecoin","mica"],
    "ESG":                  ["esg","climate","sustainable","green","environmental","tcfd"],
    "CROSS_BORDER":         ["cross-border","correspondent","passporting","extraterritorial","booking"],
}

_DUE_DATE_MAP = {"Critical": "Within 1 month", "High": "Within 3 months",
                 "Medium": "Within 6 months", "Low": "Within 12 months"}
_OPINION_COLORS = {
    "Unsatisfactory":       ("rgba(239,68,68,0.18)", "#ef4444", "background:#3d1a1a"),
    "Partially Satisfactory": ("rgba(249,115,22,0.18)", "#f97316", "background:#3d2a1a"),
    "Satisfactory":         ("rgba(34,197,94,0.12)", "#22c55e", "background:#1a3d1a"),
}


def _infer_criticality(text: str) -> str:
    tl = text.lower()
    for lvl in ("Critical", "High", "Medium", "Low"):
        if any(k in tl for k in _CRIT_KW[lvl]):
            return lvl
    return "Medium"


def _infer_finding_theme(text: str) -> str:
    tl = text.lower()
    scores = {t: sum(1 for k in kws if k in tl) for t, kws in _THEME_KW_FINDING.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "OPERATIONAL_RISK"


def _parse_findings(raw_text: str) -> list:
    """Parse free-text observations into structured finding dicts."""
    import re
    if not raw_text or not raw_text.strip():
        return []
    # Split by numbered items, bullets, or paragraph breaks
    chunks = re.split(r'\n(?=\s*[\d]+[\.\)]\s|\s*[-•]\s)', raw_text.strip())
    if len(chunks) <= 1:
        chunks = [b.strip() for b in raw_text.strip().split('\n\n') if b.strip()]
    if len(chunks) <= 1:
        chunks = [b.strip() for b in raw_text.strip().splitlines() if b.strip()]

    findings, order = [], {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    for chunk in chunks:
        clean = re.sub(r'^\s*[\d]+[\.\)]\s*', '', chunk.strip())
        clean = re.sub(r'^\s*[-•]\s*', '', clean).strip()
        if not clean:
            continue
        crit  = _infer_criticality(clean)
        theme = _infer_finding_theme(clean)
        title = clean[:72].rstrip('.,;') + ('…' if len(clean) > 72 else '')
        findings.append({
            "title": title, "criticality": crit, "description": clean,
            "theme": theme, "due_date": _DUE_DATE_MAP[crit], "status": "Open",
        })
    findings.sort(key=lambda f: order.get(f["criticality"], 4))
    for i, f in enumerate(findings):
        f["idx"] = i + 1
    return findings


def _classify_opinion(findings: list) -> tuple:
    n_crit = sum(1 for f in findings if f.get("criticality") == "Critical")
    n_high = sum(1 for f in findings if f.get("criticality") == "High")
    if n_crit >= 1:
        return "Unsatisfactory", f"{n_crit} Critical finding(s) identified &mdash; immediate remediation required."
    if n_high >= 3:
        return "Partially Satisfactory", f"{n_high} High findings indicate material control weaknesses."
    if n_high >= 1:
        return "Partially Satisfactory", f"{n_high} High finding(s) &mdash; controls are partially effective."
    return "Satisfactory", "No Critical or High findings; control environment is broadly effective."


@st.cache_data(show_spinner=False)
def _get_best_risk(finding_text: str, theme: str) -> dict | None:
    """Match a finding to the best risk in RISK_INDICATORS via keyword overlap."""
    if not finding_text:
        return None
    # Normalise theme key
    theme_key = theme.upper().replace(" ","_").replace("/","_").replace("-","_")
    risks = RISK_INDICATORS.get(theme_key, [])
    # Fallback: search all themes when theme has no risks
    if not risks:
        risks = [r for v in RISK_INDICATORS.values() for r in v]
    if not risks:
        return None
    t_words = _words(finding_text)
    if not t_words:
        return risks[0]
    best, best_s = risks[0], 0
    for r in risks:
        r_text = (r.get("title","") + " " + r.get("description","") + " " +
                  " ".join(r.get("expected_controls",[])) + " " +
                  " ".join(r.get("red_flags",[])))
        r_words = _words(r_text)
        if not r_words:
            continue
        score = len(t_words & r_words)
        if score > best_s:
            best_s, best = score, r
    return best if best_s > 0 else risks[0]


def _get_reg_refs(theme: str, jurisdictions: list) -> list:
    """Return up to 3 framework references relevant to theme × jurisdiction."""
    topic_map = {
        "AML_KYC": ["AML","KYC","PEP"],
        "CYBER_RISK": ["Operational Risk","Cybersecurity","BCP"],
        "CREDIT_RISK": ["Credit Risk"],
        "OPERATIONAL_RISK": ["Operational Risk","BCP","Governance"],
        "DATA_PRIVACY": ["Data Privacy"],
        "MARKET_RISK": ["Market Risk"],
        "THIRD_PARTY_RISK": ["Outsourcing"],
        "GOVERNANCE": ["Governance"],
        "LIQUIDITY_RISK": ["Liquidity Risk"],
    }
    kws = topic_map.get(theme, [theme.replace("_"," ").title()])
    refs = []
    for jur in (jurisdictions or ["CH / FINMA"])[:3]:
        for fw in REGULATORY_FRAMEWORKS.get(jur, []):
            applies = fw.get("applies_to", [])
            if any(any(k.lower() in a.lower() for a in applies) for k in kws):
                refs.append(f"{fw.get('reference','')} &mdash; {fw.get('title','')}")
                if len(refs) >= 3:
                    return refs
    return refs or ["Refer to applicable regulatory framework"]


def _render_heat_map_html(findings: list) -> str:
    _P = {"High": 0, "Medium": 1, "Low": 2}
    _I = {"High": 0, "Medium": 1, "Low": 2}
    _BG = [
        ["rgba(239,68,68,0.28)", "rgba(239,68,68,0.16)", "rgba(249,115,22,0.20)"],
        ["rgba(239,68,68,0.16)", "rgba(249,115,22,0.20)", "rgba(234,179,8,0.16)"],
        ["rgba(249,115,22,0.20)", "rgba(234,179,8,0.16)", "rgba(34,197,94,0.12)"],
    ]
    cells = [[[] for _ in range(3)] for _ in range(3)]
    for f in findings:
        risk = _get_best_risk(f["description"], f["theme"])
        prob = risk.get("probability","Medium") if risk else "Medium"
        imp  = risk.get("impact","Medium") if risk else "Medium"
        cells[_P.get(prob,1)][_I.get(imp,1)].append(f"F{f['idx']}")

    rows = ""
    for pi, plbl in enumerate(("High Prob.","Med. Prob.","Low Prob.")):
        cells_html = ""
        for ii in range(3):
            items = cells[pi][ii]
            badges = " ".join(
                f'<span style="background:rgba(255,255,255,0.1);border-radius:3px;padding:2px 6px;'
                f'font-size:10.5px;color:#dde3f5;font-weight:600">{it}</span>' for it in items
            )
            cells_html += (
                f'<td style="width:28%;padding:12px 8px;text-align:center;'
                f'background:{_BG[pi][ii]};border:1px solid rgba(255,255,255,0.07)">'
                f'{badges if badges else "<span style=" + chr(34) + "color:#3a4468;font-size:11px" + chr(34) + ">&mdash;</span>"}</td>'
            )
        rows += f'<tr><td style="padding:8px 12px;font-size:11.5px;color:#8392bb;white-space:nowrap">{plbl}</td>{cells_html}</tr>'

    return f"""<div style="margin:14px 0">
      <div style="font-size:10.5px;color:#5a6488;margin-bottom:8px">F# = Finding number &nbsp;&middot;&nbsp; Axes: Probability (vertical) &times; Impact (horizontal)</div>
      <table style="width:100%;border-collapse:collapse;font-size:12px">
        <thead><tr>
          <th style="padding:8px 12px;color:#5a6488;font-size:11px;text-align:left">↕ Prob / Impact &#8594;</th>
          <th style="padding:8px;text-align:center;color:#8392bb">High Impact</th>
          <th style="padding:8px;text-align:center;color:#8392bb">Med. Impact</th>
          <th style="padding:8px;text-align:center;color:#8392bb">Low Impact</th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table></div>"""


def _assemble_report_static(findings_raw, topic, scope, jurisdictions,
                             t1_risks, t2_rationale, t2_background) -> dict:
    """Build all report sections from static data — zero API calls."""
    findings = _parse_findings(findings_raw)
    theme    = _topic_to_theme(topic) or "AML_KYC"
    opinion, opinion_just = _classify_opinion(findings)
    jurs = jurisdictions or ["CH / FINMA"]

    # Overall context
    bg_card  = THEMATIC_BACKGROUND.get(theme, {})
    bg_text  = t2_background or bg_card.get("overview","") or ""
    rat_text = t2_rationale  or bg_card.get("why_now","") or (
        f"This internal audit of {topic} was conducted to assess the adequacy and effectiveness "
        f"of the control environment within the {_entity_institution_str()} {topic} framework."
    )
    reg_refs = _get_reg_refs(theme, jurs)
    reg_sent = ("Applicable regulatory frameworks include: " + "; ".join(reg_refs[:3]) + ".") if reg_refs else ""
    overall  = f"{rat_text}\n\n{bg_text}\n\n{reg_sent}".strip()

    n_c = sum(1 for f in findings if f["criticality"]=="Critical")
    n_h = sum(1 for f in findings if f["criticality"]=="High")
    n_m = sum(1 for f in findings if f["criticality"]=="Medium")
    n_l = sum(1 for f in findings if f["criticality"]=="Low")

    # Enrich each finding
    detailed = []
    for f in findings:
        try:
            risk = _get_best_risk(f["description"], f["theme"])
        except Exception:
            risk = None
        try:
            refs_f = _get_reg_refs(f["theme"], jurs)
        except Exception:
            refs_f = []
        try:
            actions = (MANAGEMENT_ACTION_TEMPLATES.get(f["theme"]) or
                       MANAGEMENT_ACTION_TEMPLATES.get("OPERATIONAL_RISK",[]))[:3]
        except Exception:
            actions = []
        if risk:
            imp_text = "; ".join(str(x) for x in risk.get("red_flags",[])[:2]) or (
                "Potential regulatory breach, reputational harm, and financial loss.")
        else:
            imp_text = "Potential regulatory breach, reputational harm, and financial loss."
        detailed.append({**f, "risk": risk, "reg_refs": refs_f,
                         "impact": imp_text, "mgmt_actions": actions})

    theme_groups: dict = {}
    for f in findings:
        theme_groups.setdefault(f["theme"], []).append(f)

    return {
        "topic": topic or "&mdash;", "scope": scope or "All group entities",
        "jurisdictions": ", ".join(jurs), "period": datetime.now().strftime("%Y"),
        "overall_context": overall,
        "n_total": len(findings), "n_crit": n_c, "n_high": n_h, "n_med": n_m, "n_low": n_l,
        "top3": findings[:3], "opinion": opinion, "opinion_just": opinion_just,
        "findings": findings, "detailed": detailed, "theme_groups": theme_groups,
        "theme": theme, "jurs": jurs,
    }


def _show_report_section1(rd: dict):
    """Render Section 1 — Executive Summary."""
    opinion = rd["opinion"]
    op_bg, op_col, op_card_bg = _OPINION_COLORS.get(opinion, ("rgba(99,102,241,0.1)","#818cf8","background:#1a1e33"))

    # A — Audit Context
    ctx_rows = "".join(
        f'<tr><td style="padding:7px 14px;color:#8392bb;font-size:12px;white-space:nowrap;width:30%;'
        f'border-bottom:1px solid rgba(255,255,255,0.05)">{k}</td>'
        f'<td style="padding:7px 14px;color:var(--text-primary);font-size:12.5px;font-weight:500;'
        f'border-bottom:1px solid rgba(255,255,255,0.05)">{v}</td></tr>'
        for k, v in [("Audit Topic", rd["topic"]), ("Jurisdictions", rd["jurisdictions"]),
                     ("Audit Scope", rd["scope"]), ("Period", rd["period"])]
    )
    st.markdown(f"""
    <div style="background:#0f1423;border-left:4px solid #818cf8;border-radius:0 10px 10px 0;padding:20px 24px;margin-bottom:18px">
      <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#818cf8;margin-bottom:14px">A &mdash; Audit Context</div>
      <table style="width:100%;border-collapse:collapse">{ctx_rows}</table>
    </div>""", unsafe_allow_html=True)

    # B — Overall Context
    ctx_paras = rd["overall_context"].replace("\n\n","</p><p style='margin:0 0 10px;font-size:13px;color:var(--text-secondary);line-height:1.8'>")
    st.markdown(f"""
    <div style="background:#0f1423;border-left:4px solid #818cf8;border-radius:0 10px 10px 0;padding:20px 24px;margin-bottom:18px">
      <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#818cf8;margin-bottom:12px">B &mdash; Overall Context</div>
      <p style="margin:0 0 10px;font-size:13px;color:var(--text-secondary);line-height:1.8">{ctx_paras}</p>
    </div>""", unsafe_allow_html=True)

    # C — Key Observations Summary
    top3_html = "".join(
        f'<li style="margin-bottom:5px;font-size:12.5px;color:var(--text-secondary)">'
        f'<span style="color:{_LEVEL_COLOR.get(f["criticality"],"#8392bb")};font-weight:700">'
        f'{_LEVEL_EMOJI.get(f["criticality"],"")} F{f["idx"]}</span> &mdash; {f["title"]}</li>'
        for f in rd["top3"]
    )
    st.markdown(f"""
    <div style="background:#0f1423;border-left:4px solid #818cf8;border-radius:0 10px 10px 0;padding:20px 24px;margin-bottom:18px">
      <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#818cf8;margin-bottom:12px">C &mdash; Key Observations Summary</div>
      <div style="display:flex;gap:28px;flex-wrap:wrap;margin-bottom:14px">
        <div style="font-size:13px;color:var(--text-secondary)">Total observations: <strong style="color:var(--text-primary);font-size:15px">{rd["n_total"]}</strong></div>
        <div style="font-size:13px;color:#ef4444">🔴 Critical: <strong>{rd["n_crit"]}</strong></div>
        <div style="font-size:13px;color:#f97316">🟠 High: <strong>{rd["n_high"]}</strong></div>
        <div style="font-size:13px;color:#eab308">🟡 Medium: <strong>{rd["n_med"]}</strong></div>
        <div style="font-size:13px;color:#22c55e">🟢 Low: <strong>{rd["n_low"]}</strong></div>
      </div>
      {"<div style='font-size:11.5px;font-weight:700;color:#8392bb;margin-bottom:6px'>Top observations:</div><ul style='margin:0;padding-left:18px'>" + top3_html + "</ul>" if top3_html else ""}
    </div>""", unsafe_allow_html=True)

    # D — Audit Opinion
    st.markdown(f"""
    <div style="{op_card_bg};border-left:4px solid {op_col};border-radius:0 10px 10px 0;padding:20px 24px;margin-bottom:18px">
      <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:{op_col};margin-bottom:12px">D &mdash; Audit Opinion</div>
      <div style="display:flex;align-items:center;gap:14px">
        <span style="background:{op_bg};color:{op_col};border:1px solid {op_col}66;border-radius:6px;
              padding:6px 16px;font-size:14px;font-weight:700">{opinion}</span>
        <span style="font-size:13px;color:var(--text-secondary)">{rd["opinion_just"]}</span>
      </div>
    </div>""", unsafe_allow_html=True)


def _show_report_section2(rd: dict):
    """Render Section 2 — Summary of Findings."""
    findings = rd["findings"]
    if not findings:
        st.caption("No findings recorded.")
        return

    # A — Narrative Introduction
    theme_lbl = rd["theme"].replace("_"," ").title()
    bg_card   = THEMATIC_BACKGROUND.get(rd["theme"], {})
    intro     = (bg_card.get("overview","") or
                 f"The audit of {rd['topic']} was conducted across {rd['jurisdictions']}. "
                 f"The fieldwork identified {rd['n_total']} observations across the {theme_lbl} domain, "
                 f"with {rd['n_crit']} Critical and {rd['n_high']} High priority findings requiring "
                 f"management attention.")

    st.markdown(f"""
    <div style="background:#0f1423;border-left:4px solid #818cf8;border-radius:0 10px 10px 0;padding:18px 22px;margin-bottom:18px">
      <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#818cf8;margin-bottom:10px">A &mdash; Narrative Introduction</div>
      <p style="margin:0;font-size:13px;color:var(--text-secondary);line-height:1.8">{intro[:500]}</p>
    </div>""", unsafe_allow_html=True)

    # B — Findings by Theme
    st.markdown('<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#818cf8;margin:16px 0 10px">B &mdash; Findings Overview by Domain</div>', unsafe_allow_html=True)
    for theme_key, theme_findings in rd["theme_groups"].items():
        theme_label = theme_key.replace("_"," ").title()
        bg_t = THEMATIC_BACKGROUND.get(theme_key, {})
        narrative = (bg_t.get("overview","") or
                     f"In the {theme_label} domain, {len(theme_findings)} observation(s) were identified. "
                     f"These findings indicate areas where the control framework requires strengthening "
                     f"to meet regulatory expectations and industry standards.")
        max_crit = min(["Critical","High","Medium","Low"],
                       key=lambda x: {"Critical":0,"High":1,"Medium":2,"Low":3}.get(x,4)
                       if any(f["criticality"]==x for f in theme_findings) else 99)
        max_col  = _LEVEL_COLOR.get(max_crit, "#8392bb")
        max_emoji = _LEVEL_EMOJI.get(max_crit, "")
        refs_t   = _get_reg_refs(theme_key, rd["jurs"])
        st.markdown(f"""
        <div style="background:#0c1220;border:1px solid rgba(99,102,241,0.15);border-left:4px solid {max_col};
                    border-radius:0 8px 8px 0;padding:16px 20px;margin-bottom:12px">
          <div style="font-size:13px;font-weight:700;color:var(--text-primary);margin-bottom:8px">
            {max_emoji} Domain: {theme_label}
          </div>
          <p style="margin:0 0 12px;font-size:12.5px;color:var(--text-secondary);line-height:1.8">{narrative[:400]}</p>
          <div style="display:flex;gap:20px;flex-wrap:wrap;font-size:12px">
            <span style="color:#8392bb">Findings in this area: <strong style="color:var(--text-primary)">{len(theme_findings)}</strong></span>
            <span style="color:#8392bb">Risk exposure: <strong style="color:{max_col}">{max_emoji} {max_crit}</strong></span>
            <span style="color:#8392bb;font-size:11px">Regulatory ref: {refs_t[0] if refs_t else "&mdash;"}</span>
          </div>
        </div>""", unsafe_allow_html=True)

    # C — Heat Map
    st.markdown('<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#818cf8;margin:18px 0 8px">C &mdash; Findings Heat Map</div>', unsafe_allow_html=True)
    st.markdown(_render_heat_map_html(findings), unsafe_allow_html=True)


def _show_report_section3(rd: dict):
    """Render Section 3 — Detailed Recommendations (one expander per finding)."""
    if not rd["detailed"]:
        st.caption("No findings recorded.")
        return
    for f in rd["detailed"]:
        crit   = f["criticality"]
        col    = _LEVEL_COLOR.get(crit, "#8392bb")
        emoji  = _LEVEL_EMOJI.get(crit, "")
        risk   = f.get("risk")
        refs   = f.get("reg_refs", [])
        acts   = f.get("mgmt_actions", [])
        is_expanded = (crit == "Critical")

        with st.expander(f"**Finding #{f['idx']}** — {emoji} {crit} — {f['title']}", expanded=is_expanded):
            # Observation
            st.markdown(f"""
            <div style="background:#0c1220;border-left:3px solid {col};border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:12px">
              <div style="font-size:10.5px;font-weight:700;text-transform:uppercase;color:{col};margin-bottom:6px">Observation</div>
              <p style="margin:0;font-size:13px;color:var(--text-secondary);line-height:1.8">{f['description']}</p>
            </div>""", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            # Associated Risk
            with col1:
                if risk:
                    r_lv  = risk.get("level","")
                    r_col = _LEVEL_COLOR.get(r_lv,"#8392bb")
                    r_bg  = _LEVEL_BG.get(r_lv,"transparent")
                    ctrls = "".join(f"<li>{c}</li>" for c in risk.get("expected_controls",[])[:3])
                    st.markdown(f"""
                    <div style="background:#0c1220;border-left:3px solid {r_col};border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:12px">
                      <div style="font-size:10.5px;font-weight:700;text-transform:uppercase;color:{r_col};margin-bottom:6px">Associated Risk</div>
                      <div style="font-size:12px;color:#818cf8;font-weight:700;margin-bottom:3px">{risk.get("id","")}</div>
                      <div style="font-size:12.5px;color:var(--text-primary);font-weight:600;margin-bottom:6px">{risk.get("title","")}</div>
                      <span style="background:{r_bg};color:{r_col};border:1px solid {r_col}44;border-radius:4px;padding:1px 8px;font-size:11px;font-weight:700">{_LEVEL_EMOJI.get(r_lv,"")} {r_lv}</span>
                      {"<ul style='margin:8px 0 0;padding-left:15px;font-size:11.5px;color:var(--text-secondary);line-height:1.7'>" + ctrls + "</ul>" if ctrls else ""}
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown('<div style="color:#5a6488;font-size:12px;padding:14px">No matching risk found in indicator library.</div>', unsafe_allow_html=True)

            # Regulatory Reference + Impact
            with col2:
                refs_html = "".join(f"<li style='font-size:11.5px'>{r}</li>" for r in refs)
                st.markdown(f"""
                <div style="background:#0c1220;border-left:3px solid #818cf8;border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:12px">
                  <div style="font-size:10.5px;font-weight:700;text-transform:uppercase;color:#818cf8;margin-bottom:6px">Regulatory Reference</div>
                  <ul style="margin:0;padding-left:15px;color:var(--text-secondary);line-height:1.8">{refs_html or "<li>See applicable framework</li>"}</ul>
                </div>""", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background:#0c1220;border-left:3px solid #eab308;border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:12px">
                  <div style="font-size:10.5px;font-weight:700;text-transform:uppercase;color:#eab308;margin-bottom:6px">Impact</div>
                  <p style="margin:0;font-size:12.5px;color:var(--text-secondary);line-height:1.8">{f['impact']}</p>
                </div>""", unsafe_allow_html=True)

            # Recommendation
            rec_text = (risk.get("expected_controls",[None])[0] if risk else None) or (
                f"Implement adequate controls to address the identified gap in {f['theme'].replace('_',' ').lower()}. "
                f"Ensure documented procedures, clear ownership, and periodic testing aligned with IIA Standard 14.2."
            )
            st.markdown(f"""
            <div style="background:#0c1220;border-left:3px solid #22d3a5;border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:12px">
              <div style="font-size:10.5px;font-weight:700;text-transform:uppercase;color:#22d3a5;margin-bottom:6px">Recommendation</div>
              <p style="margin:0;font-size:13px;color:var(--text-secondary);line-height:1.8">{rec_text}</p>
            </div>""", unsafe_allow_html=True)

            # Management Actions + Due Date
            actions_html = "".join(
                f'<tr><td style="padding:7px 12px;color:var(--text-secondary);font-size:12px;border-bottom:1px solid rgba(255,255,255,0.05)">{a.get("action","")}</td>'
                f'<td style="padding:7px 12px;color:#818cf8;font-size:11.5px;white-space:nowrap;border-bottom:1px solid rgba(255,255,255,0.05)">{a.get("owner","")}</td>'
                f'<td style="padding:7px 12px;color:#22d3a5;font-size:11.5px;white-space:nowrap;border-bottom:1px solid rgba(255,255,255,0.05)">{a.get("due","")}</td></tr>'
                for a in acts
            ) if acts else '<tr><td colspan="3" style="padding:8px;color:#5a6488;font-size:12px">No specific actions defined for this domain.</td></tr>'

            st.markdown(f"""
            <div style="display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap">
              <div style="flex:2;min-width:260px;background:#0c1220;border-left:3px solid #818cf8;border-radius:0 8px 8px 0;padding:14px 18px">
                <div style="font-size:10.5px;font-weight:700;text-transform:uppercase;color:#818cf8;margin-bottom:8px">Proposed Management Actions</div>
                <table style="width:100%;border-collapse:collapse">
                  <thead><tr>
                    <th style="padding:5px 12px;font-size:10px;color:#5a6488;text-align:left">Action</th>
                    <th style="padding:5px 12px;font-size:10px;color:#5a6488;text-align:left">Owner</th>
                    <th style="padding:5px 12px;font-size:10px;color:#5a6488;text-align:left">Due</th>
                  </tr></thead>
                  <tbody>{actions_html}</tbody>
                </table>
              </div>
              <div style="min-width:160px;background:#0c1220;border-left:3px solid {col};border-radius:0 8px 8px 0;padding:14px 18px;text-align:center">
                <div style="font-size:10.5px;font-weight:700;text-transform:uppercase;color:{col};margin-bottom:8px">Suggested Due Date</div>
                <div style="font-size:13px;font-weight:700;color:{col}">{emoji} {crit}</div>
                <div style="font-size:12.5px;color:var(--text-primary);margin-top:6px;font-weight:600">{f['due_date']}</div>
              </div>
            </div>""", unsafe_allow_html=True)


def _show_report_section4(rd: dict):
    """Render Section 4 — Action Plan Summary Table."""
    findings = rd["detailed"]
    if not findings:
        st.caption("No findings recorded.")
        return
    rows = ""
    for f in findings:
        crit  = f["criticality"]
        col   = _LEVEL_COLOR.get(crit,"#8392bb")
        emoji = _LEVEL_EMOJI.get(crit,"")
        acts  = f.get("mgmt_actions",[])
        owner = acts[0].get("owner","TBD") if acts else "TBD"
        rows += (
            f'<tr>'
            f'<td style="padding:8px 12px;color:#818cf8;font-weight:700;text-align:center;border-bottom:1px solid var(--tbl-row-border)">F{f["idx"]}</td>'
            f'<td style="padding:8px 12px;color:var(--text-primary);border-bottom:1px solid var(--tbl-row-border)">{f["title"]}</td>'
            f'<td style="padding:8px 12px;text-align:center;border-bottom:1px solid var(--tbl-row-border)"><span style="background:{_LEVEL_BG.get(crit,"transparent")};color:{col};border:1px solid {col}44;border-radius:4px;padding:1px 8px;font-size:11px;font-weight:700">{emoji} {crit}</span></td>'
            f'<td style="padding:8px 12px;color:var(--text-secondary);font-size:11.5px;border-bottom:1px solid var(--tbl-row-border)">'
            + (f'{acts[0]["action"][:70]}&hellip;' if acts and len(acts[0].get("action",""))>70 else (acts[0].get("action","&mdash;") if acts else "&mdash;")) +
            f'</td>'
            f'<td style="padding:8px 12px;color:#818cf8;font-size:11.5px;border-bottom:1px solid var(--tbl-row-border)">{owner}</td>'
            f'<td style="padding:8px 12px;color:#22d3a5;font-size:11.5px;white-space:nowrap;border-bottom:1px solid var(--tbl-row-border)">{f["due_date"]}</td>'
            f'<td style="padding:8px 12px;text-align:center;border-bottom:1px solid var(--tbl-row-border)"><span style="background:rgba(99,102,241,0.1);color:#818cf8;border:1px solid rgba(99,102,241,0.3);border-radius:4px;padding:1px 8px;font-size:11px">Open</span></td>'
            f'</tr>'
        )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(99,102,241,0.07);border-bottom:1px solid rgba(99,102,241,0.18)">
        <th style="color:#818cf8;width:4%">#</th>
        <th style="color:#818cf8;width:22%">Finding</th>
        <th style="color:#818cf8;width:9%">Rating</th>
        <th style="color:#818cf8;width:28%">Recommendation</th>
        <th style="color:#818cf8;width:13%">Owner</th>
        <th style="color:#818cf8;width:12%">Due Date</th>
        <th style="color:#818cf8;width:8%">Status</th>
      </tr></thead><tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)


def _show_audit_snapshot():
    """Render Tab 0 Section E — Latest Audit Snapshot."""
    if not st.session_state.get("report_generated") or not st.session_state.get("report_data"):
        st.markdown(
            '<p style="color:#5a6488;font-size:12.5px;font-style:italic;padding:6px 0">'
            'No audit report generated yet. Complete the Risk Analysis, Audit Plan, and generate a '
            'report in the Audit Report tab to see the snapshot here.</p>',
            unsafe_allow_html=True,
        )
        return

    rd = st.session_state["report_data"]
    ts = st.session_state.get("report_timestamp","")
    opinion = rd["opinion"]
    op_bg, op_col, op_card_bg = _OPINION_COLORS.get(opinion, ("rgba(99,102,241,0.1)","#818cf8","background:#1a1e33"))
    top_html = "".join(
        f'<li style="font-size:12px;color:var(--text-secondary);margin-bottom:4px">'
        f'<span style="color:{_LEVEL_COLOR.get(f["criticality"],"#8392bb")};font-weight:700">'
        f'{_LEVEL_EMOJI.get(f["criticality"],"")} F{f["idx"]}</span> &mdash; {f["title"]}</li>'
        for f in rd.get("top3",[])
    )
    ctx_text = rd.get("overall_context","")[:400] + ("…" if len(rd.get("overall_context",""))>400 else "")

    st.markdown(f"""
    <div style="background:#0f1423;border-left:4px solid #818cf8;border-radius:0 10px 10px 0;padding:18px 22px">
      <div style="font-size:11px;font-weight:700;color:#818cf8;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:4px">📋 Latest Audit Snapshot</div>
      <div style="font-size:12px;color:#5a6488;margin-bottom:14px">Based on: <strong style="color:#8392bb">{rd["topic"]}</strong> &middot; Generated: {ts}</div>

      <div style="font-size:10.5px;font-weight:700;color:#5a6488;text-transform:uppercase;margin-bottom:6px">── Audit Context ──</div>
      <div style="font-size:12.5px;color:var(--text-secondary);margin-bottom:12px">
        <span style="color:#8392bb">Topic:</span> {rd["topic"]} &nbsp;&middot;&nbsp;
        <span style="color:#8392bb">Scope:</span> {rd["scope"]} &nbsp;&middot;&nbsp;
        <span style="color:#8392bb">Jurisdictions:</span> {rd["jurisdictions"]}
      </div>

      <div style="font-size:10.5px;font-weight:700;color:#5a6488;text-transform:uppercase;margin-bottom:6px">── Overall Context ──</div>
      <p style="font-size:12.5px;color:var(--text-secondary);line-height:1.8;margin:0 0 14px">{ctx_text}</p>

      <div style="font-size:10.5px;font-weight:700;color:#5a6488;text-transform:uppercase;margin-bottom:8px">── Key Observations ──</div>
      <div style="display:flex;gap:20px;flex-wrap:wrap;margin-bottom:10px;font-size:12.5px">
        <span>Total findings: <strong style="color:var(--text-primary)">{rd["n_total"]}</strong></span>
        <span style="color:#ef4444">🔴 Critical: <strong>{rd["n_crit"]}</strong></span>
        <span style="color:#f97316">🟠 High: <strong>{rd["n_high"]}</strong></span>
        <span style="color:#eab308">🟡 Medium: <strong>{rd["n_med"]}</strong></span>
        <span style="color:#22c55e">🟢 Low: <strong>{rd["n_low"]}</strong></span>
      </div>
      {"<ul style='margin:0 0 14px;padding-left:18px'>" + top_html + "</ul>" if top_html else ""}

      <div style="display:flex;align-items:center;gap:12px">
        <span style="font-size:12px;color:#8392bb">Opinion:</span>
        <span style="{op_card_bg};color:{op_col};border:1px solid {op_col}66;border-radius:6px;padding:4px 14px;font-size:13px;font-weight:700">{opinion}</span>
      </div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────

# ═════════════════════════════════════════════════════════════════════════════
# SECTIONS (sidebar-driven, no tabs)
# ═════════════════════════════════════════════════════════════════════════════
_active = st.session_state.get("active_tab", 0)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 0 — INTELLIGENCE DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
if _active == 0:
    st.markdown(
        '<div style="font-size:24px;font-weight:800;color:var(--text-primary);letter-spacing:-0.03em;margin-bottom:4px">Intelligence Dashboard</div>'
        '<div style="font-size:13px;color:var(--text-muted);margin-bottom:28px">Overview of regulatory intelligence and audit activity</div>',
        unsafe_allow_html=True,
    )
    _tab_actions_bar("t0", "Stay informed before launching an audit — CVEs, regulations, recommendations.", [])

    # ── "What's New" banner (dismissible) ─────────────────────────────────────
    if not st.session_state.get("whats_new_dismissed", False):
        _whats_new = [
            (5, "📡 Continuous Audit", "Automated control testing, exception feed & 12-week health trends"),
            (6, "🏢 Vendor 360", "Third-party risk scoring, KYC status & outsourcing oversight"),
            (7, "🔍 KYC / AML", "PEP/sanctions queue, remediation pipeline & CDD coverage"),
            (3, "📂 Document Analyser", "Now auto-assigns a domain specialist based on your audit topic"),
        ]
        _wn_items = "".join(
            f'<div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:8px">'
            f'<span style="font-size:13px;font-weight:700;color:#eef0f8;white-space:nowrap">{_t}</span>'
            f'<span style="font-size:12px;color:#94a3b8">— {_d}</span></div>'
            for _, _t, _d in _whats_new
        )
        st.markdown(
            f'<div style="background:linear-gradient(135deg,rgba(99,102,241,.12),rgba(34,211,165,.06));'
            f'border:1px solid rgba(99,102,241,.3);border-radius:14px;padding:18px 22px;margin-bottom:18px">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">'
            f'<span style="font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;'
            f'background:rgba(34,211,165,.15);color:#22d3a5;border:1px solid rgba(34,211,165,.4);'
            f'border-radius:20px;padding:3px 12px">✨ What\'s New</span>'
            f'<span style="font-size:13px;color:#6b7a99">Recently added to AuditIQ</span></div>'
            f'{_wn_items}</div>',
            unsafe_allow_html=True,
        )
        _wn_cols = st.columns([1, 1, 1, 1, 1.4], gap="small")
        for _ci, (_idx, _title, _) in enumerate(_whats_new):
            if _wn_cols[_ci].button(f"Open {_title.split(' ',1)[1]}", key=f"_wn_go_{_idx}", use_container_width=True):
                st.session_state["active_tab"] = _idx
                st.session_state["whats_new_dismissed"] = True
                st.rerun()
        if _wn_cols[4].button("✓ Got it, dismiss", key="_wn_dismiss", use_container_width=True):
            st.session_state["whats_new_dismissed"] = True
            st.rerun()
        st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)

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

    # ── Session context stats ──────────────────────────────────────────────────
    _ds_n_risks  = len(st.session_state.get("t1_risks") or [])
    _ds_n_tests  = len(st.session_state.get("t2_tests") or [])
    _ds_n_obs    = len(st.session_state.get("t3_observations") or [])
    _ds_n_prior  = sum(1 for r in (st.session_state.get("t0_prior_recs") or [])
                       if r.get("status") in ("Open", "Not implemented", "Partially implemented"))
    _ds_topic    = st.session_state.get("t1_topic") or ""
    _ds_jurs     = st.session_state.get("t1_jurs") or []
    if any([_ds_n_risks, _ds_n_tests, _ds_n_obs, _ds_n_prior, _ds_topic]):
        _sc1, _sc2, _sc3, _sc4 = st.columns(4, gap="small")
        _stat_style = "background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;padding:16px 20px;text-align:center;box-shadow:var(--shadow-card)"
        _sc1.markdown(
            f'<div style="{_stat_style}"><div style="font-size:26px;font-weight:800;color:var(--accent-secondary);letter-spacing:-0.03em;line-height:1">{_ds_n_risks or "—"}</div>'
            f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:var(--text-muted);margin-top:6px">Risks</div></div>',
            unsafe_allow_html=True,
        )
        _sc2.markdown(
            f'<div style="{_stat_style}"><div style="font-size:26px;font-weight:800;color:var(--accent-secondary);letter-spacing:-0.03em;line-height:1">{_ds_n_tests or "—"}</div>'
            f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:var(--text-muted);margin-top:6px">Tests</div></div>',
            unsafe_allow_html=True,
        )
        _sc3.markdown(
            f'<div style="{_stat_style}"><div style="font-size:26px;font-weight:800;color:var(--accent-secondary);letter-spacing:-0.03em;line-height:1">{_ds_n_obs or "—"}</div>'
            f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:var(--text-muted);margin-top:6px">Observations</div></div>',
            unsafe_allow_html=True,
        )
        _sc4.markdown(
            f'<div style="{_stat_style}"><div style="font-size:26px;font-weight:800;color:{"#f97316" if _ds_n_prior else "var(--accent-secondary)"};letter-spacing:-0.03em;line-height:1">{_ds_n_prior or "—"}</div>'
            f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:var(--text-muted);margin-top:6px">Open N-1</div></div>',
            unsafe_allow_html=True,
        )
        if _ds_topic:
            _jur_chips = " ".join(f'<span style="background:rgba(99,102,241,0.1);color:#818cf8;border:1px solid rgba(99,102,241,0.2);border-radius:20px;padding:1px 8px;font-size:11px">{_JUR_FLAG.get(j,"")}{j.split("/")[0].strip()}</span>' for j in _ds_jurs)
            st.markdown(
                f'<div style="margin-top:10px;padding:8px 16px;background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:8px;font-size:12px;color:var(--text-muted);display:flex;align-items:center;gap:10px;flex-wrap:wrap">'
                f'<span style="color:var(--text-secondary);font-weight:600">Current audit:</span>'
                f'<span style="color:var(--text-primary)">{_ds_topic}</span>'
                + (f'<span style="color:var(--text-muted)">·</span>{_jur_chips}' if _jur_chips else "")
                + '</div>',
                unsafe_allow_html=True,
            )
        st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    # ── Live cyberthreat map (Kaspersky) ──────────────────────────────────────
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;margin:8px 0 12px">'
        '<span style="font-size:14px;font-weight:700;color:var(--text-primary);text-transform:uppercase;letter-spacing:.06em">🌍 Live Cyberthreat Map</span>'
        '<span style="font-size:11px;color:var(--text-muted)">Real-time global threat activity · source: Kaspersky</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    components.iframe(
        "https://cybermap.kaspersky.com/en/widget/dynamic/dark",
        height=560,
        scrolling=False,
    )
    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)

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
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{len(CVE_BANKING)} entries &middot; 2021-2024</span></div>',
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
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{_total_regs} texts &middot; CH &middot; EU &middot; UK &middot; SG &middot; HK &middot; Bahamas &middot; International</span></div>',
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
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{len(PUBLIC_AUDIT_RECOMMENDATIONS)} entries &middot; FATF &middot; FINMA &middot; MAS &middot; FCA &middot; EBA &middot; Basel &middot; IIA &middot; IMF</span></div>',
                unsafe_allow_html=True,
            )
            _rec_sc1, _rec_sc2 = st.columns([3, 2])
            _rec_sq = _rec_sc1.text_input("Search recommendations", placeholder="Filter recommendations…", key="_rec_sq", label_visibility="collapsed")
            _rec_stheme = _rec_sc2.selectbox("Theme", ["All"] + _all_themes, key="_rec_stheme", label_visibility="collapsed")
            for _t in (_all_themes if _rec_stheme == "All" else [_rec_stheme]):
                if _rec_stheme == "All":
                    st.markdown(f'<div style="font-size:12px;font-weight:600;color:#818cf8;margin:10px 0 4px">{_t}</div>', unsafe_allow_html=True)
                _show_pub_recs(theme=_t, search=_rec_sq)

        with st.expander("📅 D — Regulatory Calendar 2025–2026", expanded=False):
            _cal_juris  = sorted({e["jurisdiction"] for e in REGULATORY_CALENDAR})
            _cal_types  = sorted({e["type"] for e in REGULATORY_CALENDAR})
            _cal_prios  = ["High", "Medium", "Low"]
            # Entity-aware jurisdiction pre-filter suggestion
            _t0_entity  = st.session_state.get("entity_type", "🏦 Private Banking")
            _ENTITY_JUR_HINT = {
                "🏦 Private Banking":                   "Filtered for Private Banking regulators",
                "📊 Asset Management":                  "Filtered for Asset Management regulators (ESMA, FINMA, FCA, MAS)",
                "🏢 Management Company (ManCo)":        "Filtered for ManCo regulators (ESMA, CSSF, CBI, FINMA)",
                "🔀 Alternative Investment (PE/RE/HF)": "Filtered for Alternative Investment regulators (ESMA, SEC, FCA)",
            }
            st.markdown(
                f'<div class="section-title">D. Regulatory Calendar 2025&ndash;2026'
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">'
                f'{len(REGULATORY_CALENDAR)} entries &middot; CH &middot; EU &middot; UK &middot; SG &middot; HK &middot; Global</span></div>',
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

        with st.expander("📋 E — Latest Audit Snapshot", expanded=False):
            st.markdown(
                '<div class="section-title">E. Latest Audit Snapshot'
                '<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">'
                'Populated automatically after generating a report in the Audit Report tab</span></div>',
                unsafe_allow_html=True,
            )
            _show_audit_snapshot()

        if st.session_state.get("demo_mode"):
            st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
            st.markdown(
                '<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;'
                'color:var(--text-muted);margin-bottom:12px">🎬 Demo — Engagement Metrics</div>',
                unsafe_allow_html=True,
            )
            _ds = _DEMO_CONTENT["dash_stats"]
            _dc1, _dc2, _dc3, _dc4 = st.columns(4, gap="small")
            for _col, _num, _lbl in [
                (_dc1, _ds["risks_identified"], "Risks Identified"),
                (_dc2, _ds["audit_tests"],      "Audit Tests"),
                (_dc3, _ds["frameworks"],       "Frameworks"),
                (_dc4, _ds["vendors_reviewed"], "Vendors Reviewed"),
            ]:
                _col.markdown(
                    f'<div class="demo-stat-card">'
                    f'<div class="demo-stat-number">{_num}</div>'
                    f'<div class="demo-stat-label">{_lbl}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("<div class='no-print' style='margin-top:1rem'>", unsafe_allow_html=True)
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
                    f"Focus on {ENTITY_CONTEXT.get(st.session_state.get('entity_type','🏦 Private Banking'),{}).get('background_angle','financial services')}, regulatory compliance, and risk management. "
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
                f'<div class="section-title">A. Latest CVEs &mdash; Financial Sector'
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{n_cve} entries &middot; High & Critical &middot; last 3 months</span>'
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
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{n_reg} publications &middot; FINMA &middot; MAS &middot; SFC &middot; HKMA &middot; EBA &middot; FCA &middot; PRA &middot; BCBS &middot; FSB &middot; FATF</span></div>',
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
                f'<div class="section-title">C. Latest Public Audit Recommendations &mdash; Banking'
                f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{n_rec} entries &middot; last 12 months</span></div>',
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
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("🔄 Prior Recommendations Follow-up (N-1)", expanded=False):
        st.markdown(
            '<div style="font-size:12px;color:var(--text-muted);margin-bottom:12px">'
            'Paste prior-cycle recommendations from Teammate+ to track implementation status. '
            'Open items feed into the risk profile of the current audit.</div>',
            unsafe_allow_html=True,
        )
        _prior_recs = list(st.session_state.get("t0_prior_recs") or [])
        _raw_input = st.text_area(
            "Paste prior recommendations (one per line)",
            placeholder="e.g.\n1. Strengthen AML transaction monitoring thresholds — Owner: CCO — Due: 2025-06-30\n2. Update KYC refresh policy…",
            height=100,
            key="t0_prior_input",
            label_visibility="collapsed",
        )
        if st.button("Import recommendations", key="t0_import_recs"):
            if _raw_input.strip():
                _lines = [l.strip() for l in _raw_input.strip().splitlines() if l.strip()]
                _new_recs = []
                for _idx, _line in enumerate(_lines):
                    _new_recs.append({
                        "id": str(_idx),
                        "text": _line.lstrip("0123456789.-) "),
                        "status": "Open",
                        "note": "",
                    })
                st.session_state["t0_prior_recs"] = _new_recs
                st.rerun()
        if _prior_recs:
            _STATUS_FOLLOW = ["Open", "Implemented", "Partially implemented", "Not implemented", "N/A"]
            _f_cnt = {s: sum(1 for r in _prior_recs if r.get("status") == s) for s in _STATUS_FOLLOW}
            _open_n = _f_cnt.get("Open", 0) + _f_cnt.get("Not implemented", 0) + _f_cnt.get("Partially implemented", 0)
            if _open_n:
                st.warning(f"⚠ {_open_n} open item(s) — consider including in current audit scope.")
            _pr_updated = False
            for _ri, _rec in enumerate(_prior_recs):
                _fcol1, _fcol2, _fcol3 = st.columns([4, 2, 3])
                _fcol1.markdown(
                    f'<div style="font-size:12.5px;color:var(--text-secondary);padding-top:6px">{_rec.get("text","")}</div>',
                    unsafe_allow_html=True,
                )
                _new_fs = _fcol2.selectbox(
                    "Status", _STATUS_FOLLOW,
                    index=_STATUS_FOLLOW.index(_rec.get("status", "Open")) if _rec.get("status", "Open") in _STATUS_FOLLOW else 0,
                    key=f"t0_fs_{_ri}",
                    label_visibility="collapsed",
                )
                _new_fn = _fcol3.text_input(
                    "Note", value=_rec.get("note", ""),
                    placeholder="Evidence or comment…",
                    key=f"t0_fn_{_ri}",
                    label_visibility="collapsed",
                )
                if _new_fs != _rec.get("status") or _new_fn != _rec.get("note", ""):
                    _prior_recs[_ri]["status"] = _new_fs
                    _prior_recs[_ri]["note"] = _new_fn
                    _pr_updated = True
            if _pr_updated:
                st.session_state["t0_prior_recs"] = _prior_recs
            if st.button("Clear all", key="t0_clear_recs"):
                st.session_state["t0_prior_recs"] = []
                st.rerun()

    # Public Audit Recommendations (populated from Risk Analysis live run)
    with st.expander("📋 Public Audit Recommendations", expanded=False):
        _dash_pub = st.session_state.get("t1_pub_recs") or []
        if _dash_pub:
            _pub_recs_table(_dash_pub)
        else:
            st.caption("Run a Risk Analysis (live mode) to populate recommendations here.")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — RISK ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
elif _active == 1:
    _tab_actions_bar("t1",
        "Risk mapping, applicable regulations, and public audit recommendations by topic.",
        [
            ("📗 Excel", st.session_state.get("t1_xlsx"),
             "Risk_Analysis.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            ("📝 Word", st.session_state.get("t1_docx"),
             "Risk_Analysis.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            ("📙 PPT", st.session_state.get("t1_pptx2"),
             "Risk_Analysis.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
            ("📕 PDF", st.session_state.get("t1_pdf"),
             "Risk_Analysis.pdf", "application/pdf"),
        ]
    )
    _t1_mode = render_mode_toggle("mode_tab1")

    # Form / results toggle
    _t1_show_form = st.session_state.get("t1_show_form", True)
    _t1_has_results = bool(st.session_state.get("t1_risks") or st.session_state.get("t1_regs"))
    _t1_in_results = _t1_mode == "live" and _t1_has_results and not _t1_show_form

    if not _t1_in_results:
        _t1_form_col, _t1_ctx_col = st.columns([11, 9], gap="large")

        with _t1_ctx_col:
            # ── Agent Card ──────────────────────────────────────────────────────
            _t1_entity_name = st.session_state.get("entity_type", "🏦 Private Banking")
            _t1_status_pill = '<span class="agent-status-pill agent-status-live">⚡ Live</span>' if _t1_mode == "live" else '<span class="agent-status-pill agent-status-ready">📚 Static</span>'
            st.markdown(f"""
            <div class="agent-card">
              <div class="agent-badge-pill">AGENT 1</div>
              <div style="font-size:17px;font-weight:700;color:var(--text-primary);margin-bottom:6px">Agent 1 — Risk Analysis</div>
              <div style="font-size:12.5px;color:var(--text-secondary);margin-bottom:14px">Identifies key risks, applicable regulations, and public audit recommendations for your selected topic and jurisdictions.</div>
              <div>{_t1_status_pill}</div>
            </div>""", unsafe_allow_html=True)

            # Entity context hint
            _t1_entity   = st.session_state.get("entity_type", "🏦 Private Banking")
            _t1_ent_ctx  = ENTITY_CONTEXT.get(_t1_entity, {})
            _t1_reg_focus = _t1_ent_ctx.get("regulatory_focus", [])
            if _t1_reg_focus:
                _bg, _col = _ENTITY_COLORS.get(_t1_entity, ("#0a2540", "#818cf8"))
                st.markdown(
                    f'<div style="background:{_bg};border-left:3px solid {_col};border-radius:0 6px 6px 0;'
                    f'padding:8px 12px;margin-bottom:12px;font-size:12px;color:#c8d0e8">'
                    f'<span style="font-weight:700;color:{_col}">Regulatory focus:</span> '
                    f'{" &middot; ".join(_t1_reg_focus[:5])}</div>',
                    unsafe_allow_html=True,
                )

        with _t1_form_col:
            # ── Quick Start Template ─────────────────────────────────────────────
            tpl_name = st.selectbox(
                "Quick Start Template",
                options=list(TEMPLATES.keys()),
                key="t1_tpl_select",
                help="Pre-fill topic, jurisdictions and scope with a predefined audit template.",
                format_func=lambda x: x,
            )
            if tpl_name not in _TPL_SEPARATORS and tpl_name != st.session_state._tpl_name:
                tpl = TEMPLATES[tpl_name]
                _cur_entity  = st.session_state.get("entity_type", "🏦 Private Banking")
                _tpl_topic_key = (TOPIC_KEY_MAPPING.get(tpl_name) or [None])[0]
                _entity_ctx  = ENTITY_CONTEXT.get(_cur_entity, {})
                _entity_scope = (
                    _entity_ctx.get("topics", {}).get(_tpl_topic_key, {}).get("scope_suggestion", "")
                    if _tpl_topic_key else ""
                )
                st.session_state["t1_topic_in"] = tpl.get("topic", "")
                st.session_state["t1_jurs_pills"] = tpl.get("jurisdictions", JURISDICTIONS[:4])
                st.session_state["t1_jurs_in"] = tpl.get("jurisdictions", JURISDICTIONS[:4])
                st.session_state._tpl_name = tpl_name
                st.session_state._tpl_scope = _entity_scope or tpl.get("scope", "")
                st.rerun()

            _tpl_scope_default = st.session_state.get("_tpl_scope", "")

            audit_topic = st.text_input(
                "Audit Topic",
                placeholder="e.g. AML/KYC, Credit Risk, Cybersecurity, Operational Risk…",
                key="t1_topic_in",
                help="Enter the main audit topic or domain to analyze. Must be at least 3 characters.",
            )
            st.session_state["topic_tab1"] = audit_topic or ""

            # ── Jurisdiction multiselect ─────────────────────────────────────────────
            _JURS_DISPLAY = {j: f"{_JUR_FLAG.get(j, '🌐')} {j}" for j in JURISDICTIONS}
            _jurs_current = st.session_state.get("t1_jurs_pills") or JURISDICTIONS[:4]
            if not isinstance(_jurs_current, list):
                _jurs_current = list(_jurs_current)
            jurisdictions = st.multiselect(
                "Jurisdictions",
                options=JURISDICTIONS,
                default=_jurs_current,
                format_func=lambda x: _JURS_DISPLAY.get(x, x),
                key="t1_jurs_in",
                help="Select one or more jurisdictions.",
            )
            if jurisdictions != _jurs_current:
                st.session_state["t1_jurs_pills"] = jurisdictions

            # Input validation
            _t1_valid = True
            if audit_topic and len(audit_topic.strip()) < 3:
                st.warning("⚠ Audit topic must be at least 3 characters.")
                _t1_valid = False
            if not jurisdictions:
                st.warning("⚠ Please select at least one jurisdiction.")
                _t1_valid = False

        if st.session_state.get("demo_mode") and _t1_mode == "live":
            st.markdown('<div class="gen-btn-wrap">', unsafe_allow_html=True)
            st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
            if st.button("✦ Generate Risk Analysis", key="t1_run_demo", use_container_width=True):
                with st.spinner(""):
                    _demo_stream_generate(
                        _DEMO_CONTENT["gen_steps_t1"],
                        {
                            "t1_risks": _DEMO_CONTENT["t1_summary"],
                            "t1_topic": _DEMO_CONTENT["topic"],
                            "t1_jurs": _DEMO_CONTENT["jurisdictions"],
                        }
                    )
                    st.session_state["t1_show_form"] = False
                    st.rerun()
            st.markdown("</div></div>", unsafe_allow_html=True)

        if _t1_mode == "live" and not st.session_state.get("demo_mode"):
            st.markdown('<div class="gen-btn-wrap">', unsafe_allow_html=True)
            st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
            if st.button("✦ Générer l'analyse", disabled=_disabled or not audit_topic or not _t1_valid, key="t1_run"):
                with st.spinner("Analyzing…"):
                    try:
                        c = _client()
                        jur_str = ", ".join(jurisdictions) if jurisdictions else "all jurisdictions"
                        _t1_inst = _entity_institution_str(jurs=jurisdictions)

                        risks_raw = _call(c, f"""Audit topic: {audit_topic}
Jurisdictions: {jur_str}
Institution: {_t1_inst}

Identify 10-12 key risks for this audit topic across 3 severity levels.
Respond ONLY with a valid JSON array — no markdown, no preamble:
[{{"level":"Critical|High|Moderate","name":"<5-8 words>","description":"<2-3 sentences>","impact":"<1-2 sentences, quantified where possible>","likelihood":"High|Medium|Low","control":"<1-2 sentences on expected control mechanism>"}}]""",
                            max_tokens=5000)

                        regs_raw = _call(c, f"""Audit topic: {audit_topic}
Jurisdictions: {jur_str}
Institution: {_t1_inst}

List applicable regulations for this institution type and audit topic.
Respond ONLY with a valid JSON array — 12-18 entries, no markdown:
[{{"jurisdiction":"<e.g. CH / FINMA>","text":"<law or regulation name>","reference":"<specific article/circular number>","requirement":"<key requirement in 1-2 sentences>"}}]""",
                            max_tokens=5000)

                        _t1_bg_angle = ENTITY_CONTEXT.get(
                            st.session_state.get("entity_type","🏦 Private Banking"), {}
                        ).get("background_angle","financial services")
                        pub_recs_raw = _web_search_call(c,
                            f"Search for public audit recommendations and supervisory findings specifically about '{audit_topic}' "
                            f"in {_t1_bg_angle}, from the last 3 years. "
                            f"Sources: Basel Committee, IMF FSAPs, Big 4 public reports, IIA, FINMA, MAS, FCA, EBA, FATF. "
                            f"Return a JSON array of 6-10 real entries found:\n"
                            f'[{{"source":"<issuing body>","year":"YYYY","recommendation":"<recommendation summary, 2-3 sentences>","applicability":"<how it applies to {_t1_bg_angle}>"}}]',
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
                                f"Institution: {_t1_inst}\n"
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
                        try:
                            _risks_txt = "\n".join(
                                f"[{r.get('level','')}] {r.get('title','')} — {r.get('description','')}"
                                for r in (st.session_state.t1_risks or [])
                            )
                            _regs_txt = "\n".join(
                                r if isinstance(r, str) else f"{r.get('reference','')} — {r.get('title','')}"
                                for r in (st.session_state.t1_regs or [])
                            )
                            st.session_state.t1_pdf = _make_pdf(
                                f"Risk Analysis — {audit_topic}",
                                [("Risks Identified", _risks_txt), ("Applicable Regulations", _regs_txt)],
                            )
                        except Exception:
                            pass

                        st.session_state["t1_show_form"] = False
                        st.rerun()

                    except Exception:
                        st.error("An error occurred. Please try again.")
            st.markdown('</div></div>', unsafe_allow_html=True)

        if _t1_mode == "static":
            # ── Static Reference Data mode ─────────────────────────────────────────
            _static_label()
            _t1_entity_type = st.session_state.get("t1_entity_type", "🏦 Private Banking")
            try:
                _t1_entity_data = get_data_for_topic(
                    audit_topic if audit_topic else "AML / KYC & Transaction Monitoring",
                    entity_type=_t1_entity_type,
                )
            except Exception:
                _t1_entity_data = {
                    "risks": [], "tests": [], "kris": [],
                    "da_scenarios": [], "regulatory_focus": [],
                    "scope_suggestion": "", "typical_findings": [],
                    "background_angle": "", "entity_key": "PRIVATE_BANKING",
                    "keys": [],
                }
            _t1_entity_key   = _t1_entity_data.get("entity_key", "PRIVATE_BANKING")
            _t1_entity_color = _ENTITY_COLORS.get(_t1_entity_key, "#818cf8")
            _entity_label    = _t1_entity_type.split(" ", 1)[1] if " " in _t1_entity_type else _t1_entity_type
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:12px;margin:8px 0 16px">'
                f'<span style="background:{_t1_entity_color}22;color:{_t1_entity_color};border:1px solid {_t1_entity_color}44;'
                f'border-radius:6px;padding:4px 14px;font-size:12px;font-weight:700">📊 {_entity_label} context</span>'
                f'<span style="font-size:11.5px;color:#5a6488;font-style:italic">'
                f'Risks and regulations adapted for {_t1_entity_type}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            _t1_theme = _topic_to_theme(audit_topic) if audit_topic else "AML_KYC"
            _t1_theme = _t1_theme or "AML_KYC"
            _t1_theme_label = _t1_theme.replace("_", " ").title()

            # Resolve entity-specific data for this topic
            _ri_entity     = st.session_state.get("entity_type", "🏦 Private Banking")
            _ri_ent_data   = ENTITY_CONTEXT.get(_ri_entity, {})
            _ri_topic_data = _ri_ent_data.get("topics", {}).get(_t1_theme, {})
            _ri_reg_refs   = _ri_topic_data.get("regulatory_refs", [])
            _ri_emphasis   = [e.lower() for e in _ri_topic_data.get("risk_emphasis", [])]
            _ri_findings   = _ri_topic_data.get("typical_findings", [])
            _ri_bg, _ri_col = _ENTITY_COLORS.get(_ri_entity, ("#0a2540", "#818cf8"))
            _ri_bg_lbl     = _ri_ent_data.get("background_angle", "financial services")

            with st.expander("🗺️ A — Risk Indicators", expanded=True):
                # Section header with entity context badge
                _ri_badge_html = _entity_badge_html(_ri_entity, "11px")
                st.markdown(
                    f'<div class="section-title" style="display:flex;align-items:center;justify-content:space-between">'
                    f'<span>A. Risk Indicators &mdash; {_t1_theme_label}'
                    f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">'
                    f'{len(RISK_INDICATORS.get(_t1_theme, []))} risks in library</span></span>'
                    f'<span style="font-size:11px;color:#5a6488">{_ri_badge_html} context</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                # Entity-specific context panel
                if _ri_reg_refs or _ri_emphasis:
                    _reg_str  = " &nbsp;·&nbsp; ".join(_ri_reg_refs[:4]) if _ri_reg_refs else ""
                    _emp_str  = " &nbsp;·&nbsp; ".join(e.capitalize() for e in _ri_topic_data.get("risk_emphasis", [])[:4])
                    st.markdown(
                        f'<div style="background:{_ri_bg};border-left:3px solid {_ri_col};border-radius:0 6px 6px 0;'
                        f'padding:8px 14px;margin:6px 0 12px;font-size:12px;color:#c8d0e8">'
                        f'<span style="font-size:11px;color:{_ri_col};font-weight:700">Risks and regulations adapted for {_ri_entity}</span><br>'
                        + (f'<span style="font-size:11.5px"><b>Regulatory focus:</b> {_reg_str}</span><br>' if _reg_str else "")
                        + (f'<span style="font-size:11.5px"><b>Key risk areas:</b> {_emp_str}</span>' if _emp_str else "")
                        + '</div>',
                        unsafe_allow_html=True,
                    )
                st.markdown(_EXAMPLE_RISK, unsafe_allow_html=True)
                _ri_c1, _ri_c2 = st.columns([3, 1.5])
                _ri_sq = _ri_c1.text_input("Search risks", placeholder="Filter risks…", key="_ri_sq", label_visibility="collapsed")
                _ri_slv = _ri_c2.selectbox("Level", ["All", "Critical", "High", "Moderate"], key="_ri_slv", label_visibility="collapsed")
                _entity_specific_risks = _t1_entity_data.get("additional_risks", [])
                _base_risks = RISK_INDICATORS.get(_t1_theme, [])
                _ri_filtered = _entity_specific_risks + _base_risks
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
                        _ctrls  = "".join(f"<li>{c}</li>" for c in _r.get("expected_controls", []))
                        _flags  = "".join(f"<li>{f}</li>" for f in _r.get("red_flags", []))
                        # Highlight risks matching entity emphasis
                        _rtitle_low = _r.get("title","").lower()
                        _entity_match = any(kw in _rtitle_low for kw in _ri_emphasis)
                        _star_badge   = (
                            f'<span style="background:{_ri_col}22;color:{_ri_col};border:1px solid {_ri_col}44;'
                            f'border-radius:4px;padding:1px 7px;font-size:10px;font-weight:700;margin-left:6px">★ Entity focus</span>'
                            if _entity_match else ""
                        )
                        _specifics_lbl = f"🏢 {_ri_bg_lbl.title()} context"
                        _specifics_txt = _r.get("private_banking_specifics","")
                        st.markdown(f"""
                        <div style="border:1px solid {_col}33;border-radius:9px;padding:14px 18px;margin-bottom:12px;background:{_bg}">
                          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
                            <span style="background:{_col}22;color:{_col};border:1px solid {_col}44;border-radius:4px;padding:2px 9px;font-size:11px;font-weight:700">{_r["level"]}</span>
                            <span style="font-size:13.5px;font-weight:600;color:var(--text-primary)">{_r.get("id","")} &mdash; {_r["title"]}</span>{_star_badge}
                            <span style="margin-left:auto;font-size:11px;color:var(--text-muted)">Prob: <span style="color:{_pcolor};font-weight:600">{_r.get("probability","")}</span> &nbsp;&middot;&nbsp; Impact: <span style="color:{_icolor};font-weight:600">{_r.get("impact","")}</span></span>
                          </div>
                          <p style="font-size:12.5px;color:var(--text-secondary);margin:0 0 10px;line-height:1.7">{_r["description"]}</p>
                          <details>
                            <summary style="font-size:12px;color:#818cf8;cursor:pointer;font-weight:500">Controls &amp; Red Flags</summary>
                            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:8px">
                              <div><div style="font-size:11px;font-weight:600;color:var(--text-muted);margin-bottom:4px">EXPECTED CONTROLS</div>
                              <ul style="margin:0;padding-left:16px;font-size:12px;color:var(--text-secondary);line-height:1.8">{_ctrls}</ul></div>
                              <div><div style="font-size:11px;font-weight:600;color:#ef4444aa;margin-bottom:4px">RED FLAGS</div>
                              <ul style="margin:0;padding-left:16px;font-size:12px;color:var(--text-secondary);line-height:1.8">{_flags}</ul></div>
                            </div>
                            <div style="margin-top:10px;font-size:11.5px;color:var(--text-muted);font-style:italic">{_specifics_lbl}: {_specifics_txt}</div>
                          </details>
                        </div>""", unsafe_allow_html=True)
                    # Entity-specific typical findings for this topic
                    if _ri_findings:
                        st.markdown(
                            f'<div style="background:{_ri_bg};border-left:3px solid {_ri_col};border-radius:0 6px 6px 0;'
                            f'padding:8px 14px;margin-top:10px;font-size:12px;color:#c8d0e8">'
                            f'<span style="font-weight:700;color:{_ri_col}">Typical findings for {_ri_entity}:</span><br>'
                            + "".join(f'<span style="display:block;margin-top:3px">&bull; {f}</span>' for f in _ri_findings)
                            + '</div>',
                            unsafe_allow_html=True,
                        )
                else:
                    st.caption("No risks match the filter.")

            st.markdown("<div class='no-print' style='margin-top:1rem'>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        # ── Results mode: show "← Modifier" back button ────────────────────────
        audit_topic = st.session_state.get("t1_topic", "") or ""
        jurisdictions = st.session_state.get("t1_jurs") or st.session_state.get("t1_jurs_pills") or JURISDICTIONS[:4]
        _t1_valid = True
        _t1_theme = _topic_to_theme(audit_topic) if audit_topic else "AML_KYC"
        _t1_theme = _t1_theme or "AML_KYC"

        _back_c, _ = st.columns([2, 6])
        with _back_c:
            st.markdown('<div class="back-btn">', unsafe_allow_html=True)
            if st.button("← Modifier", key="t1_back"):
                st.session_state["t1_show_form"] = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Results display
        topic_lbl = st.session_state.t1_topic or "audit"
        st.markdown("---")

        # Risk Score Dashboard
        st.markdown('<div class="section-title">Risk Score</div>', unsafe_allow_html=True)
        _t1_risks_val = st.session_state.t1_risks
        _t1_risks_is_str = isinstance(_t1_risks_val, str)
        if not _t1_risks_is_str:
            _risk_score_display(_t1_risks_val, len(st.session_state.t1_jurs or []))

        with st.expander("🗺️ A — Risk Mapping", expanded=True):
            st.markdown('<div class="section-title">A. Risk Mapping</div>', unsafe_allow_html=True)
            if _t1_risks_is_str and st.session_state.get("demo_mode"):
                st.markdown(
                    f'<div class="output-box" style="max-height:320px">{_t1_risks_val}</div>',
                    unsafe_allow_html=True,
                )
            else:
                filtered_risks = _filter_data(
                    _t1_risks_val or [],
                    ["name", "description", "impact", "control"],
                    "t1_risks",
                    level_field="level",
                )
                _risk_table(filtered_risks)
            col_copy_a, _ = st.columns([1, 5])
            with col_copy_a:
                _copy_data = (st.session_state.t1_risks if isinstance(st.session_state.t1_risks, str)
                              else json.dumps(st.session_state.t1_risks or [], indent=2))
                _copy_button(_copy_data, "t1_risks_copy")

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

        # ── Auto-generate static exports if not yet done ─────────────────────
        if not st.session_state.t1_xlsx and _t1_theme and RISK_INDICATORS.get(_t1_theme):
            try:
                _static_risks = [
                    {"level": r.get("level",""), "name": r.get("title",""),
                     "description": r.get("description",""), "impact": "",
                     "likelihood": r.get("probability",""), "control": ", ".join(r.get("expected_controls",[])[:2])}
                    for r in RISK_INDICATORS.get(_t1_theme, [])
                ]
                p_xlsx = generate_risk_analysis_excel(
                    {"topic": audit_topic or _t1_theme, "risks": _static_risks, "regs": [], "pub_recs": []},
                    OUTPUT_DIR)
                st.session_state.t1_xlsx = Path(p_xlsx).read_bytes()
            except Exception:
                pass
        if not st.session_state.t1_pdf and _t1_theme and RISK_INDICATORS.get(_t1_theme):
            try:
                _pdf_risks_txt = "\n".join(
                    f"[{r.get('level','')}] {r.get('title','')} — {r.get('description','')[:120]}"
                    for r in RISK_INDICATORS.get(_t1_theme, [])
                )
                st.session_state.t1_pdf = _make_pdf(
                    f"Risk Analysis — {audit_topic or _t1_theme}",
                    [("Risk Indicators", _pdf_risks_txt)],
                )
            except Exception:
                pass

        st.markdown("---")
        _t1_has_exports = st.session_state.t1_docx or st.session_state.t1_xlsx or st.session_state.t1_pptx2 or st.session_state.t1_pdf
        if _t1_has_exports:
            _e1, _e2, _e3, _e4 = st.columns(4)
            if st.session_state.t1_docx:
                _e1.download_button(
                    "📝 Word",
                    data=st.session_state.t1_docx,
                    file_name=f"Risk_Analysis_{topic_lbl.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
            if st.session_state.t1_xlsx:
                _e2.download_button(
                    "📗 Excel",
                    data=st.session_state.t1_xlsx,
                    file_name=f"Risk_Analysis_{topic_lbl.replace(' ', '_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )
            if st.session_state.t1_pptx2:
                _e3.download_button(
                    "📙 PPT",
                    data=st.session_state.t1_pptx2,
                    file_name=f"Risk_Analysis_{topic_lbl.replace(' ', '_')}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True,
                )
            if st.session_state.t1_pdf:
                _e4.download_button(
                    "📕 PDF",
                    data=st.session_state.t1_pdf,
                    file_name=f"Risk_Analysis_{topic_lbl.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )



# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — AUDIT PLAN
# ─────────────────────────────────────────────────────────────────────────────
elif _active == 2:
    _tab_actions_bar("t2",
        "Structured audit planning, test programme, and data analytics scenarios.",
        [
            ("📙 PPT", st.session_state.get("t2_pptx"),
             "Audit_Plan.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
            ("📗 Excel", st.session_state.get("t2_xlsx"),
             "Audit_Tests.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            ("📕 PDF", st.session_state.get("t2_pdf"),
             "Audit_Plan.pdf", "application/pdf"),
        ]
    )
    _t2_mode = render_mode_toggle("mode_tab2")

    # Form / results toggle
    _t2_show_form = st.session_state.get("t2_show_form", True)
    _t2_has_results = bool(st.session_state.get("t2_rationale") or st.session_state.get("t2_tests"))
    _t2_in_results = _t2_mode == "live" and _t2_has_results and not _t2_show_form

    if not _t2_in_results:
        _t2_form_col, _t2_ctx_col = st.columns([11, 9], gap="large")

        with _t2_ctx_col:
            # ── Agent Card ──────────────────────────────────────────────────────
            st.markdown("""
            <div class="agent-card">
              <div class="agent-badge-pill">AGENT 2</div>
              <div style="font-size:17px;font-weight:700;color:var(--text-primary);margin-bottom:6px">Agent 2 — Audit Plan</div>
              <div style="font-size:12.5px;color:var(--text-secondary);margin-bottom:14px">Generates a structured audit programme with test procedures, data analytics scenarios, and rationale tailored to your entity and scope.</div>
            </div>""", unsafe_allow_html=True)

            # Entity context hint for Tab 2 (right col)
            _t2_entity  = st.session_state.get("entity_type", "🏦 Private Banking")
            _t2_ent_ctx = ENTITY_CONTEXT.get(_t2_entity, {})

        with _t2_form_col:
            if st.session_state.t1_topic:
                st.markdown(f'<div class="ctx-pill">&#10003; Topic: {_html.escape(str(st.session_state.t1_topic or ""))}</div>', unsafe_allow_html=True)

            # Pre-fill from Tab 1 if Tab 2 field is still empty
            if not st.session_state.get("t2_topic_in"):
                _prefill = st.session_state.get("topic_tab1") or st.session_state.get("t1_topic") or ""
                if _prefill:
                    st.session_state["t2_topic_in"] = _prefill

            topic2 = st.text_input(
                "Audit Topic",
                placeholder="e.g. AML/KYC, Credit Risk, Cybersecurity…",
                key="t2_topic_in",
            )
            if st.session_state.get("topic_tab1"):
                st.markdown(
                    '<p style="color:#5a6488;font-size:11px;margin:-8px 0 8px">ℹ️ Pre-filled from Risk Analysis. You can modify it freely.</p>',
                    unsafe_allow_html=True,
                )

            # Entity context hint (left col — needs topic2 to compute theme)
            _t2_theme   = _topic_to_theme(topic2 or "") or _topic_to_theme(st.session_state.get("topic_tab1", "") or "")
            _t2_topic_data = _t2_ent_ctx.get("topics", {}).get(_t2_theme or "", {}) if _t2_theme else {}
            _t2_test_emphasis = _t2_topic_data.get("risk_emphasis", [])
            if _t2_test_emphasis:
                _bg2, _col2 = _ENTITY_COLORS.get(_t2_entity, ("#0a2540", "#818cf8"))
                st.markdown(
                    f'<div style="background:{_bg2};border-left:3px solid {_col2};border-radius:0 6px 6px 0;'
                    f'padding:8px 12px;margin:4px 0 10px;font-size:12px;color:#c8d0e8">'
                    f'<span style="font-weight:700;color:{_col2}">{_t2_entity} &mdash; key risk areas:</span> '
                    f'{" &middot; ".join(_t2_test_emphasis)}</div>',
                    unsafe_allow_html=True,
                )

            # Resolve scope: template > entity context > empty
            _t2_scope_default = st.session_state.get("_tpl_scope", "")
            if not _t2_scope_default and _t2_theme and _t2_topic_data:
                _t2_scope_default = _t2_topic_data.get("scope_suggestion", "")
            scope = st.text_area(
                "Audit Scope",
                value=_t2_scope_default,
                placeholder="e.g. All group entities in CH, SG and HK. Focus on client onboarding and transaction monitoring.",
                height=80,
                key="t2_scope_in",
                help="Define the perimeter of the audit: entities, geographies, processes, and systems in scope.",
            )

            st.caption("📎 Supporting documents (optional — PDF, Word, Excel, TXT)")
            uploads2 = st.file_uploader(
                "Supporting documents", label_visibility="collapsed",
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
                <span style="font-size:12.5px;font-weight:600;color:#dde3f5">{_t2_tr_label} &mdash; {_t2_tr_match['title']}</span>
                <span style="font-size:11px;color:#5a6488;font-style:italic">{_tr_src} &middot; Mandatory</span>
              </div>
              <p style="font-size:12px;color:#c8d0e8;margin:0 0 8px;line-height:1.8">This audit topic triggers a mandatory IIA Topical Requirement. All assurance engagements must cover the following key areas:</p>
              <ul style="margin:0;padding-left:16px;font-size:12px;color:#c8d0e8;line-height:1.9">{_tr_keys}</ul>
              <div style="margin-top:8px;font-size:11px;color:#5a6488">See Tab 3 &#8594; IIA Standards Reference &#8594; {_t2_tr_match['standard_id']} for full requirements with framework mapping.</div>
            </div>""", unsafe_allow_html=True)

        if st.session_state.get("demo_mode") and _t2_mode == "live":
            st.markdown('<div class="gen-btn-wrap">', unsafe_allow_html=True)
            st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
            if st.button("✦ Generate Audit Plan", key="t2_run_demo", use_container_width=True):
                with st.spinner(""):
                    _demo_stream_generate(
                        _DEMO_CONTENT["gen_steps_t2"],
                        {
                            "t2_rationale": _DEMO_CONTENT["t2_rationale"],
                            "t2_background": _DEMO_CONTENT["t2_background"],
                            "t2_org_plan": _DEMO_CONTENT["t2_org_plan"],
                        }
                    )
                    st.session_state["t2_show_form"] = False
                    st.rerun()
            st.markdown("</div></div>", unsafe_allow_html=True)

        if _t2_mode == "live" and not st.session_state.get("demo_mode"):
            st.markdown('<div class="gen-btn-wrap">', unsafe_allow_html=True)
            st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
            if st.button("✦ Générer le plan", disabled=_disabled or not topic2 or not _t2_valid, key="t2_run"):
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

                        _t2_ent     = st.session_state.get("entity_type", "🏦 Private Banking")
                        _t2_bg_ang  = ENTITY_CONTEXT.get(_t2_ent, {}).get("background_angle", "financial services")
                        _t2_inst    = _entity_institution_str(jurs=st.session_state.t1_jurs or JURISDICTIONS[:3])
                        sys_prompt  = f"You are a senior audit partner at a Big 4 firm specialising in {_t2_bg_ang}. Write in English, professional tone, concise and precise."

                        rationale = _call(c, f"""Audit topic: {topic2}
Institution: {_t2_inst}
Scope: {scope or "All group entities"}{top_risks_str}{doc_ctx}

Write a concise RATIONALE section (2-3 paragraphs) explaining why this audit is relevant RIGHT NOW.
Cover: current regulatory triggers, recent enforcement actions or industry incidents, emerging risk trends specific to {_t2_bg_ang}.
Plain prose, no headers. Bold key terms where appropriate.""",
                            system=sys_prompt, max_tokens=2000)

                        background = _call(c, f"""Audit topic: {topic2}
Institution: {_t2_inst}
Scope: {scope or "All group entities"}{top_risks_str}{doc_ctx}

Write a BACKGROUND INFORMATION section (3-4 paragraphs). Tone: McKinsey/EY — strategic, consultative.
Cover: market context, current state in {_t2_bg_ang}, key challenges and regulatory landscape for this institution type.
Plain prose, no headers. Bold key terms where appropriate.""",
                            system=sys_prompt, max_tokens=2500)

                        org_plan = _call(c, f"""Audit topic: {topic2}
Institution: {_t2_inst}
Scope: {scope or "All entities"}{top_risks_str}{doc_ctx}

Write a structured AUDIT PLAN with three inline sections (use **bold** for section names):

**Organization** — Key business units, governance structure, and stakeholders in scope.

**Activities in Scope** — Business processes, systems, and activities in the audit perimeter.

**Audit Objectives & Methodology** — 3-4 clear objectives. Risk-based, IIA-aligned. Key techniques.

Plain prose per section.""",
                            system=sys_prompt, max_tokens=2500)

                        tests_raw = _call(c, f"""Audit topic: {topic2}
Institution: {_t2_inst}
Scope: {scope or "All entities"}{top_risks_str}

Generate EXACTLY 15 audit test procedures. ONLY valid JSON array, no markdown:
[{{"num":1,"objective":"<1 sentence>","procedure":"<2-3 sentences>","population":"<what is tested>","sample_size":"<method and size>","failure_criteria":"<control failure definition>"}}]""",
                            system=sys_prompt, max_tokens=7000)
                        tests = _parse_json(tests_raw)

                        analytics_raw = _call(c, f"""Audit topic: {topic2}
Institution: {_t2_inst}
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
                                f"Institution: {_t2_inst}\n"
                                f"Scope: {scope or 'All entities'}"
                                f"{extra_ctx}\n\n"
                                f"1. Identify 6-10 audit subjects → call generate_audit_plan_ppt.\n"
                                f"2. For each design 4-8 procedures → call generate_audit_procedures_excel."
                            )}]}], _h2)

                        if "ppt_path" in extra and Path(extra["ppt_path"]).exists():
                            st.session_state.t2_pptx = Path(extra["ppt_path"]).read_bytes()
                        if "excel_path" in extra and Path(extra["excel_path"]).exists():
                            st.session_state.t2_xlsx = Path(extra["excel_path"]).read_bytes()
                        try:
                            _t2_sections = [(h, str(v)) for h, v in [
                                ("Rationale",      st.session_state.t2_rationale or ""),
                                ("Background",     st.session_state.t2_background or ""),
                                ("Audit Programme",st.session_state.t2_org_plan   or ""),
                            ] if v]
                            st.session_state.t2_pdf = _make_pdf(f"Audit Plan — {topic2}", _t2_sections)
                        except Exception:
                            pass

                        st.session_state["t2_show_form"] = False
                        st.rerun()

                    except Exception:
                        st.error("An error occurred. Please try again.")
            st.markdown('</div></div>', unsafe_allow_html=True)

        if _t2_mode == "static":
            # ── Static Reference Data mode ─────────────────────────────────────────
            _static_label()
            _t2_theme_static = _topic_to_theme(topic2) if topic2 else "CYBER_RISK"
            _t2_theme_static = _t2_theme_static or "CYBER_RISK"
            _t2_theme_label = _t2_theme_static.replace("_", " ").title()
            _n_tests = len(AUDIT_TESTS_LIBRARY.get(_t2_theme_static, []))
            _n_da = len(DATA_ANALYTICS_SCENARIOS.get(_t2_theme_static, []))

            st.markdown(_EXAMPLE_RATIONALE, unsafe_allow_html=True)

            try:
                _t2_static_entity_data = get_data_for_topic(
                    topic2 if topic2 else "AML / KYC & Transaction Monitoring",
                    entity_type=st.session_state.get("t1_entity_type", "🏦 Private Banking"),
                )
            except Exception:
                _t2_static_entity_data = {
                    "risks": [], "tests": [], "kris": [],
                    "da_scenarios": [], "regulatory_focus": [],
                    "scope_suggestion": "", "typical_findings": [],
                    "background_angle": "", "entity_key": "PRIVATE_BANKING",
                    "keys": [],
                }
            with st.expander("📖 A — Rationale & Thematic Background", expanded=True):
                st.markdown(
                    f'<div class="section-title">A. Rationale &amp; Thematic Background &mdash; {_t2_theme_label}</div>',
                    unsafe_allow_html=True,
                )
                _bg_angle = _t2_static_entity_data.get("background_angle", "")
                if _bg_angle:
                    st.markdown(
                        f'<div style="background:rgba(99,102,241,0.08);border-left:3px solid #6366f1;'
                        f'border-radius:0 8px 8px 0;padding:10px 16px;margin-bottom:14px;'
                        f'font-size:12.5px;color:#c8d0e8;font-style:italic">'
                        f'💡 {_bg_angle}</div>',
                        unsafe_allow_html=True,
                    )
                _show_thematic_background(_t2_theme_static)
                _typical = _t2_static_entity_data.get("typical_findings", [])
                if _typical:
                    st.markdown(
                        '<div style="margin-top:14px"><div style="font-size:12px;font-weight:700;'
                        'color:#818cf8;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.5px">'
                        '★ Typical Findings for this Entity Type</div>',
                        unsafe_allow_html=True,
                    )
                    for _tf in _typical:
                        st.markdown(
                            f'<div style="font-size:12.5px;color:#c8d0e8;padding:4px 0 4px 14px;'
                            f'border-left:2px solid rgba(127,168,251,0.3)">• {_tf}</div>',
                            unsafe_allow_html=True,
                        )
                    st.markdown('</div>', unsafe_allow_html=True)

            with st.expander("🗂️ B — Audit Tests Library", expanded=False):
                st.markdown(
                    f'<div class="section-title">B. Audit Tests Library &mdash; {_t2_theme_label}'
                    f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{_n_tests} tests available for this topic</span></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(_EXAMPLE_TEST, unsafe_allow_html=True)
                _tl_c1, _tl_c2, _tl_c3, _tl_c4 = st.columns([3, 1.5, 1.8, 1.8])
                _tl_sq    = _tl_c1.text_input("Search tests", placeholder="Filter tests…", key="_tl_sq", label_visibility="collapsed")
                _tl_slv   = _tl_c2.selectbox("Level", ["All", "Critical", "High", "Moderate"], key="_tl_slv", label_visibility="collapsed")
                _tl_stype = _tl_c3.selectbox("Type", ["All", "Standard", "Data Analytics"], key="_tl_stype", label_visibility="collapsed")
                _tl_rlv   = _tl_c4.selectbox("Filter by Risk Level", ["All", "🔴 Critical", "🟠 High", "🟡 Moderate"], key="_tl_rlv", label_visibility="collapsed")
                _rl_map   = {"All": "All", "🔴 Critical": "Critical", "🟠 High": "High", "🟡 Moderate": "Moderate"}
                _show_tests_library(_t2_theme_static, search=_tl_sq, level_filter=_tl_slv, type_filter=_tl_stype,
                                    risk_level_filter=_rl_map[_tl_rlv])

            with st.expander("📊 C — Data Analytics Scenarios", expanded=False):
                st.markdown(
                    f'<div class="section-title">C. Data Analytics Scenarios &mdash; {_t2_theme_label}'
                    f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{_n_da} scenarios</span></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(_EXAMPLE_DA, unsafe_allow_html=True)
                _da_c1 = st.columns([3])[0]
                _da_sq = _da_c1.text_input("Search scenarios", placeholder="Filter scenarios…", key="_da_sq", label_visibility="collapsed")
                _show_da_scenarios(_t2_theme_static, search=_da_sq)

            st.markdown("<div class='no-print' style='margin-top:1rem'>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        # ── Results mode: show "← Modifier" back button ────────────────────────
        topic2 = st.session_state.get("t2_topic_in", "") or st.session_state.get("t1_topic", "") or ""
        scope = st.session_state.get("t2_scope_in", "") or ""
        uploads2 = []
        _t2_valid = True

        _back_c2, _ = st.columns([2, 6])
        with _back_c2:
            st.markdown('<div class="back-btn">', unsafe_allow_html=True)
            if st.button("← Modifier", key="t2_back"):
                st.session_state["t2_show_form"] = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Results display
        topic2_lbl = st.session_state.t1_topic or topic2 or "audit"
        st.markdown("---")

        with st.expander("💡 1 — Rationale", expanded=True):
            st.markdown('<div class="section-title">1. Rationale</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{_html.escape(st.session_state.t2_rationale or "")}</div>', unsafe_allow_html=True)
            _copy_button(st.session_state.t2_rationale, "t2_rat_copy")

        with st.expander("📖 2 — Background Information", expanded=False):
            st.markdown('<div class="section-title">2. Background Information</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{_html.escape(st.session_state.t2_background or "")}</div>', unsafe_allow_html=True)
            _copy_button(st.session_state.t2_background or "", "t2_bg_copy")

        with st.expander("📋 3 — Audit Plan", expanded=False):
            st.markdown('<div class="section-title">3. Audit Plan</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{_html.escape(st.session_state.t2_org_plan or "")}</div>', unsafe_allow_html=True)
            _copy_button(st.session_state.t2_org_plan or "", "t2_plan_copy")

        with st.expander("🧪 4 — Test List", expanded=False):
            n_tests = len(st.session_state.t2_tests or [])
            st.markdown(f'<div class="section-title">4. Test List &mdash; {n_tests} procedures</div>', unsafe_allow_html=True)
            filtered_tests = _filter_data(
                st.session_state.t2_tests or [],
                ["objective", "procedure", "population", "failure_criteria"],
                "t2_tests",
            )
            _tests_table(filtered_tests)

        with st.expander("📊 5 — Data Analytics Scenarios", expanded=False):
            n_analytics = len(st.session_state.t2_analytics or [])
            st.markdown(f'<div class="section-title">5. Data Analytics Scenarios &mdash; {n_analytics} scenarios</div>', unsafe_allow_html=True)
            filtered_analytics = _filter_data(
                st.session_state.t2_analytics or [],
                ["scenario", "objective", "data_source", "analysis_type", "anomaly"],
                "t2_analytics",
            )
            _analytics_table(filtered_analytics)

        # Static test library with risk mapping (live mode)
        _live_theme = _topic_to_theme(topic2) or "AML_KYC"
        _live_risks = st.session_state.t1_risks or None
        _live_n_tests = len(AUDIT_TESTS_LIBRARY.get(_live_theme, []))
        with st.expander(f"🗂️ 6 — Test Library & Risk Coverage ({_live_n_tests} tests)", expanded=False):
            st.markdown(
                f'<div class="section-title">6. Test Library &amp; Risk Coverage &mdash; {_live_theme.replace("_"," ").title()}</div>',
                unsafe_allow_html=True,
            )
            _live_c1, _live_c2, _live_c3, _live_c4 = st.columns([3, 1.5, 1.8, 1.8])
            _live_sq   = _live_c1.text_input("Search", placeholder="Filter tests…", key="_live_tl_sq", label_visibility="collapsed")
            _live_slv  = _live_c2.selectbox("Level", ["All", "Critical", "High", "Moderate"], key="_live_tl_slv", label_visibility="collapsed")
            _live_stype = _live_c3.selectbox("Type", ["All", "Standard", "Data Analytics"], key="_live_tl_stype", label_visibility="collapsed")
            _live_rlv  = _live_c4.selectbox("Risk Level", ["All", "🔴 Critical", "🟠 High", "🟡 Moderate"], key="_live_tl_rlv", label_visibility="collapsed")
            _rl_map2   = {"All": "All", "🔴 Critical": "Critical", "🟠 High": "High", "🟡 Moderate": "Moderate"}
            _show_tests_library(_live_theme, search=_live_sq, level_filter=_live_slv, type_filter=_live_stype,
                                risk_level_filter=_rl_map2[_live_rlv], live_risks=_live_risks)

        # ── Auto-generate static exports if not yet done ─────────────────────
        _t2_theme_static = _topic_to_theme(topic2) if topic2 else "CYBER_RISK"
        _t2_theme_static = _t2_theme_static or "CYBER_RISK"
        if not st.session_state.t2_pdf and _t2_theme_static and AUDIT_TESTS_LIBRARY.get(_t2_theme_static):
            try:
                _t2_tests_txt = "\n".join(
                    f"[{t.get('level','')}] {t.get('id','')} — {t.get('objective','')[:120]}"
                    for t in AUDIT_TESTS_LIBRARY.get(_t2_theme_static, [])
                )
                st.session_state.t2_pdf = _make_pdf(
                    f"Audit Plan — {topic2 or _t2_theme_static}",
                    [("Audit Tests", _t2_tests_txt)],
                )
            except Exception:
                pass

        pptx = st.session_state.t2_pptx
        xlsx = st.session_state.t2_xlsx
        pdf2 = st.session_state.t2_pdf
        if pptx or xlsx or pdf2:
            st.markdown("---")
            _t2_ecols = st.columns(4)
            if pptx:
                _t2_ecols[0].download_button(
                    "📙 PPT", data=pptx,
                    file_name=f"Audit_Plan_{topic2_lbl.replace(' ', '_')}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True,
                )
            if xlsx:
                _t2_ecols[1].download_button(
                    "📗 Excel", data=xlsx,
                    file_name=f"Audit_Tests_{topic2_lbl.replace(' ', '_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )
            if pdf2:
                _t2_ecols[2].download_button(
                    "📕 PDF", data=pdf2,
                    file_name=f"Audit_Plan_{topic2_lbl.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )



    # ── Test Execution Tracker ────────────────────────────────────────────────
    if st.session_state.get("t2_tests") or st.session_state.get("t2_org_plan"):
        with st.expander("📋 Test Execution Tracker", expanded=False):
            st.markdown(
                '<div style="font-size:12px;color:var(--text-muted);margin-bottom:12px">'
                'Track test progress locally — export to Teammate+ when complete.</div>',
                unsafe_allow_html=True,
            )
            _tr_statuses = dict(st.session_state.get("t2_test_statuses") or {})
            _tr_tests = list(st.session_state.get("t2_tests") or [])
            _STATUS_OPTS = ["—", "In Progress", "Completed", "Exception", "N/A"]
            _STATUS_COLOR = {"Completed": "#22d3a5", "Exception": "#ef4444", "In Progress": "#f97316", "N/A": "#5a6488", "—": "#3d4a6b"}
            if not _tr_tests:
                st.caption("Generate an Audit Plan (live mode) to populate tests here.")
            else:
                _tr_cnt = {s: sum(1 for v in _tr_statuses.values() if v.get("status") == s) for s in _STATUS_OPTS[1:]}
                _tr_total = len(_tr_tests)
                _tr_done = _tr_cnt.get("Completed", 0) + _tr_cnt.get("N/A", 0)
                _tr_pills = "".join(
                    f'<span style="background:{_STATUS_COLOR[s]}22;color:{_STATUS_COLOR[s]};border:1px solid {_STATUS_COLOR[s]}44;'
                    f'border-radius:20px;padding:2px 10px;font-size:11px;font-weight:600;margin-right:6px">'
                    f'{s}: {_tr_cnt.get(s, 0)}</span>'
                    for s in _STATUS_OPTS[1:]
                )
                st.markdown(
                    f'<div style="margin-bottom:14px">{_tr_pills}'
                    f'<span style="font-size:11px;color:var(--text-muted);margin-left:8px">{_tr_done}/{_tr_total} complete</span></div>',
                    unsafe_allow_html=True,
                )
                _tr_changed = False
                for _t in _tr_tests:
                    _tid = _t.get("test_id") or _t.get("id") or str(_tr_tests.index(_t))
                    _cur_st = _tr_statuses.get(_tid, {}).get("status", "—")
                    _cur_nt = _tr_statuses.get(_tid, {}).get("note", "")
                    with st.expander(
                        f'{_t.get("test_id", "?")} — {_t.get("title", "Test")}',
                        expanded=(_cur_st == "Exception"),
                    ):
                        _ec1, _ec2 = st.columns([2, 4])
                        _new_st = _ec1.selectbox(
                            "Status", _STATUS_OPTS,
                            index=_STATUS_OPTS.index(_cur_st) if _cur_st in _STATUS_OPTS else 0,
                            key=f"t2_ts_sel_{_tid}",
                            label_visibility="collapsed",
                        )
                        _new_nt = _ec2.text_input(
                            "Note / exception detail",
                            value=_cur_nt,
                            placeholder="Brief note or exception detail…",
                            key=f"t2_ts_note_{_tid}",
                            label_visibility="collapsed",
                        )
                        if _new_st != _cur_st or _new_nt != _cur_nt:
                            _tr_statuses[_tid] = {"status": _new_st, "note": _new_nt}
                            _tr_changed = True
                if _tr_changed:
                    st.session_state["t2_test_statuses"] = _tr_statuses
                if st.button("📤 Export tracker for Teammate+", key="t2_tracker_export"):
                    _tr_lines = ["Test ID\tTitle\tStatus\tNote"]
                    for _t in _tr_tests:
                        _tid = _t.get("test_id") or str(_tr_tests.index(_t))
                        _sv = _tr_statuses.get(_tid, {})
                        _tr_lines.append(f'{_tid}\t{_t.get("title", "")}\t{_sv.get("status", "—")}\t{_sv.get("note", "")}')
                    st.download_button(
                        "↓ Download tracker (.tsv)",
                        data="\n".join(_tr_lines).encode("utf-8"),
                        file_name=f"Test_Tracker_{st.session_state.get('t1_topic', 'audit').replace(' ', '_')}.tsv",
                        mime="text/tab-separated-values",
                        key="t2_tracker_dl",
                    )

# TAB 3 — DOCUMENT ANALYSER
# ─────────────────────────────────────────────────────────────────────────────
elif _active == 3:
    # Domain specialist profiles — keyed by domain, matched from audit topic keywords
    _T3_SPECIALISTS = {
        "aml_kyc": {
            "kw": ["aml", "kyc", "cdd", "edd", "str", "sar", "pep", "sanction", "transaction monitor", "anti-money", "beneficial owner", "fatf"],
            "name": "AML & KYC Compliance Specialist", "initials": "AK",
            "color": "#818cf8", "bg": "#1a1a3e",
            "domain": "Anti-Money Laundering · Know Your Customer · Sanctions",
            "expertise": ["STR / SAR filing governance", "CDD / EDD frameworks", "PEP & sanctions screening", "Transaction monitoring systems", "MLRO governance & oversight"],
            "credentials": ["CAMS", "CFCS", "Ex-FINMA supervisory team"],
            "regs": ["FATF R.10 / R.16 / R.20", "FINMA Circ. 2011/1", "MAS Notice 626", "AMLD6", "UK POCA 2002"],
            "role": "You are a senior AML & KYC compliance specialist with 20 years of experience in private banking. Expert in FATF recommendations, FINMA AML circular, CDD/EDD frameworks, STR/SAR obligations, and PEP screening.",
        },
        "third_party": {
            "kw": ["third party", "vendor", "outsourc", "supplier", "counterparty", "sla", "clearstream", "swift", "temenos", "bloomberg"],
            "name": "Third Party Risk Specialist", "initials": "TP",
            "color": "#22d3a5", "bg": "#0d2b1d",
            "domain": "Vendor Risk · Outsourcing · SLA Governance",
            "expertise": ["Critical vendor assessment", "SLA breach analysis", "Exit strategy review", "Sub-outsourcing chain audit", "Concentration risk"],
            "credentials": ["CRISC", "CTPRP", "Ex-MAS supervision"],
            "regs": ["FINMA Circ. 2018/3", "MAS TRM Guidelines 2021", "FCA SS2/21", "DORA Art. 28-30", "EBA/GL/2019/02"],
            "role": "You are a senior third-party and vendor risk specialist. Expert in outsourcing governance, SLA analysis, critical vendor assessment, and regulatory requirements under FINMA 2018/3, MAS TRM, FCA SS2/21, and DORA.",
        },
        "cyber": {
            "kw": ["cyber", "it risk", "technology risk", "dora", "iso 27001", "nist", "penetrat", "privileged access", "infosec", "information security", "bcm", "bcp", "disaster recover", "ransomware", "cloud security"],
            "name": "Cyber & Technology Risk Specialist", "initials": "CT",
            "color": "#f97316", "bg": "#2e1f0a",
            "domain": "Cyber Security · IT Risk · Operational Resilience",
            "expertise": ["Penetration test review", "Privileged access management (PAM)", "DORA ICT governance", "Business continuity testing", "Cloud security posture"],
            "credentials": ["CISSP", "CISM", "ISO 27001 Lead Auditor"],
            "regs": ["DORA (EU 2022/2554)", "MAS TRM 2021", "NIST CSF 2.0", "ISO/IEC 27001:2022", "FINMA Circ. 2023/1"],
            "role": "You are a senior cyber and technology risk specialist. Expert in DORA, ISO 27001, NIST CSF, privileged access management, and IT resilience frameworks for private banks.",
        },
        "credit_risk": {
            "kw": ["credit risk", "lending", "loan", "impairment", "ecl", "ifrs 9", "provision", "collateral", "basel", "npl", "credit appetite", "rwa"],
            "name": "Credit Risk & Capital Specialist", "initials": "CR",
            "color": "#ef4444", "bg": "#3b0e0e",
            "domain": "Credit Risk · Capital Adequacy · IFRS 9",
            "expertise": ["ECL provisioning (IFRS 9)", "Credit appetite framework", "Collateral valuation", "Basel IV RWA computation", "Large exposure monitoring"],
            "credentials": ["FRM", "CFA", "Ex-SNB banking supervision"],
            "regs": ["Basel IV / CRR III", "FINMA CAO", "IFRS 9", "EBA/GL/2020/06", "MAS Notice 612"],
            "role": "You are a senior credit risk and capital specialist. Expert in IFRS 9 ECL modelling, Basel IV, collateral frameworks, and credit governance in private banking.",
        },
        "market_risk": {
            "kw": ["market risk", "var", "trading", "frtb", "interest rate risk", "fx risk", "derivative", "hedging", "limit breach", "stress test", "liquidity"],
            "name": "Market & Liquidity Risk Specialist", "initials": "MR",
            "color": "#eab308", "bg": "#2e2000",
            "domain": "Market Risk · FRTB · Liquidity",
            "expertise": ["VaR / CVaR governance", "FRTB SA / IMA implementation", "Limit framework review", "ILAAP / LCR / NSFR", "Stress testing & scenario analysis"],
            "credentials": ["FRM", "PRM", "Ex-UBS Market Risk"],
            "regs": ["Basel III/IV - FRTB", "FINMA Circ. 2019/2", "MAS Notice 637", "EBA/GL/2018/02 ILAAP"],
            "role": "You are a senior market and liquidity risk specialist. Expert in VaR governance, FRTB, stress testing, and liquidity risk frameworks for private banks.",
        },
        "data_privacy": {
            "kw": ["gdpr", "data privacy", "data protection", "personal data", "retention", "dpo", "consent", "data breach", "ndsg", "pdpa", "data subject"],
            "name": "Data Privacy & GDPR Specialist", "initials": "DP",
            "color": "#a78bfa", "bg": "#1a0e3b",
            "domain": "GDPR · Data Privacy · Information Governance",
            "expertise": ["GDPR Art. 13-22 data subject rights", "Retention schedule audit", "Data breach response review", "Cross-border transfer (SCCs)", "DPIA review"],
            "credentials": ["CIPP/E", "CIPM", "Certified DPO"],
            "regs": ["GDPR (EU 2016/679)", "UK GDPR / DPA 2018", "Swiss nDSG", "PDPA (SG)", "PIPL (CN)"],
            "role": "You are a senior data privacy specialist. Expert in GDPR, UK GDPR, Swiss nDSG, and PDPA compliance, specialising in retention audits, data subject rights, and cross-border transfer mechanisms.",
        },
        "governance": {
            "kw": ["governance", "board", "committee", "three line", "control framework", "rcsa", "risk appetite", "compliance framework", "regulatory", "policy"],
            "name": "Governance & Regulatory Compliance Specialist", "initials": "GR",
            "color": "#38bdf8", "bg": "#0a2540",
            "domain": "Corporate Governance · Risk Framework · Regulatory Affairs",
            "expertise": ["Three Lines Model design", "RCSA framework review", "Risk appetite statement", "Board & committee governance", "Regulatory engagement strategy"],
            "credentials": ["CIA", "CRMA", "Ex-FINMA enforcement"],
            "regs": ["COSO 2017", "IIA Standards 2024", "FINMA Corporate Governance Circ.", "MAS Corp. Gov. Guidelines", "FCA SYSC"],
            "role": "You are a senior governance and regulatory compliance specialist. Expert in corporate governance, three-lines-of-defence, COSO, IIA standards, and multi-jurisdictional regulatory requirements.",
        },
        "operational_risk": {
            "kw": ["operational risk", "op risk", "bcp", "bcm", "rto", "rpo", "incident", "operational resilience", "process gap", "procedure", "important business service"],
            "name": "Operational Resilience Specialist", "initials": "OR",
            "color": "#fb923c", "bg": "#2a1505",
            "domain": "Operational Risk · Business Continuity · Resilience",
            "expertise": ["BIA & BCP testing review", "RTO / RPO gap analysis", "Incident management governance", "Important business services (IBS)", "Scenario & stress analysis"],
            "credentials": ["MBCI", "ISO 22301 Lead Auditor", "Ex-PRA supervision"],
            "regs": ["FCA/PRA SS1/21 Op. Resilience", "DORA Art. 11-14", "MAS Notice 634", "FINMA Circ. 2023/1"],
            "role": "You are a senior operational resilience specialist. Expert in BCP/BCM testing, important business services mapping, RTO/RPO governance, and multi-jurisdictional resilience requirements.",
        },
    }
    _T3_DEFAULT_SPEC = {
        "name": "Senior Internal Audit Specialist", "initials": "IA",
        "color": "#818cf8", "bg": "#1a1a3e",
        "domain": "Internal Audit · Risk & Control · Multi-domain",
        "expertise": ["Control framework assessment", "Risk-based audit approach", "Regulatory compliance review", "Observation & finding writing", "IIA Standards application"],
        "credentials": ["CIA", "CISA", "CFE"],
        "regs": ["IIA Standards 2024", "COSO 2017", "FINMA · MAS · FCA · DORA"],
        "role": "You are a senior internal auditor with broad expertise across all risk domains in private banking. Analyse documents through a risk-based audit lens.",
    }

    def _t3_detect_specialist(topic: str) -> dict:
        t = topic.lower()
        for _sp in _T3_SPECIALISTS.values():
            if any(kw in t for kw in _sp["kw"]):
                return _sp
        return _T3_DEFAULT_SPEC

    st.markdown(
        '<div style="font-size:12px;color:var(--text-muted);margin-bottom:16px">'
        'Upload audit documents — a domain specialist AI analyses findings, maps them to your audit tests, and surfaces observations.</div>',
        unsafe_allow_html=True,
    )

    st.caption("📎 Upload documents to analyse (PDF, Word, Excel, TXT — multiple files)")
    t3_uploads = st.file_uploader(
        "Documents", label_visibility="collapsed",
        type=["pdf", "docx", "xlsx", "txt"], accept_multiple_files=True, key="t3_upload_docs",
    )
    _t3_topic_default = st.session_state.get("t1_topic") or st.session_state.get("topic_tab1") or ""
    t3_topic = st.text_input(
        "Audit Topic / Context",
        value=_t3_topic_default,
        placeholder="e.g. AML/KYC, Credit Risk, Cyber, Third Party…",
        key="t3_topic_in",
    )

    # Specialist card — auto-detected from current topic value, updates on rerun
    _t3_cur_topic = st.session_state.get("t3_topic_in") or t3_topic or ""
    _t3_spec = _t3_detect_specialist(_t3_cur_topic)
    _sp_exp_html = "".join([f'<li style="margin-bottom:3px">{e}</li>' for e in _t3_spec["expertise"]])
    _sp_creds_html = "  ".join([f'<span style="background:{_t3_spec["bg"]};color:{_t3_spec["color"]};border:1px solid {_t3_spec["color"]}55;border-radius:20px;padding:2px 9px;font-size:10px;font-weight:700">{c}</span>' for c in _t3_spec["credentials"]])
    _sp_regs_html = "  ".join([f'<span style="color:#4a5568;font-size:10.5px">* {r}</span>' for r in _t3_spec["regs"]])
    st.markdown(f"""
<div style="background:var(--bg-card);border:1px solid {_t3_spec["color"]}44;border-radius:12px;padding:18px 22px;margin:12px 0 16px;position:relative;overflow:hidden">
  <div style="position:absolute;top:0;left:0;width:4px;height:100%;background:{_t3_spec["color"]}"></div>
  <div style="display:flex;gap:16px;align-items:flex-start">
    <div style="min-width:52px;height:52px;border-radius:50%;background:{_t3_spec["bg"]};border:2px solid {_t3_spec["color"]};
         display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:800;color:{_t3_spec["color"]};flex-shrink:0">
      {_t3_spec["initials"]}
    </div>
    <div style="flex:1;min-width:0">
      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:4px">
        <span style="font-size:15px;font-weight:700;color:#eef0f8">{_t3_spec["name"]}</span>
        <span style="background:{_t3_spec["bg"]};color:{_t3_spec["color"]};border:1px solid {_t3_spec["color"]}55;border-radius:6px;padding:2px 9px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.06em">Domain Specialist</span>
      </div>
      <div style="font-size:11.5px;color:{_t3_spec["color"]};font-weight:600;margin-bottom:10px">{_t3_spec["domain"]}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:11.5px">
        <div>
          <div style="color:#6b7a99;font-weight:700;text-transform:uppercase;font-size:10px;letter-spacing:.06em;margin-bottom:4px">Expertise</div>
          <ul style="margin:0;padding-left:14px;color:#eef0f8;line-height:1.7">{_sp_exp_html}</ul>
        </div>
        <div>
          <div style="color:#6b7a99;font-weight:700;text-transform:uppercase;font-size:10px;letter-spacing:.06em;margin-bottom:6px">Credentials</div>
          <div style="margin-bottom:10px">{_sp_creds_html}</div>
          <div style="color:#6b7a99;font-weight:700;text-transform:uppercase;font-size:10px;letter-spacing:.06em;margin-bottom:4px">Regulatory frame</div>
          <div style="line-height:1.9">{_sp_regs_html}</div>
        </div>
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    t3_notes = st.text_area(
        "Additional context or focus areas (optional)",
        placeholder="e.g. Focus on gaps between policy and practice. Cross-reference with FINMA Circular 2011/1.",
        height=80,
        key="t3_notes_in",
    )
    st.markdown('<div class="gen-btn-wrap"><div class="gen-btn">', unsafe_allow_html=True)
    _t3_can_run = bool(t3_uploads) and bool(t3_topic)
    if st.button("✦ Analyser les documents", disabled=_disabled or not _t3_can_run, key="t3_run"):
        with st.spinner(f"{_t3_spec['name']} is reviewing the documents..."):
            try:
                c = _client()
                file_ids3 = []
                for uf in (t3_uploads or []):
                    fm = _upload_sf(c, uf)
                    if fm:
                        file_ids3.append(fm)
                _t3_tests_ctx = ""
                if st.session_state.get("t2_tests"):
                    _tests_sample = st.session_state.t2_tests[:5] if isinstance(st.session_state.t2_tests, list) else []
                    if _tests_sample:
                        _t3_tests_ctx = "\n\nAudit tests in programme:\n" + "\n".join(
                            f"- {t.get('test_id', '')}: {t.get('title', '')}" for t in _tests_sample
                        )
                _t3_inst = _entity_institution_str(jurs=st.session_state.get("t1_jurs") or JURISDICTIONS[:4])
                doc_note = f"{len(file_ids3)} document(s) provided." if file_ids3 else "No documents attached — analyse based on topic only."
                analysis_raw = _call(c,
                    f"Audit topic: {t3_topic}\nInstitution: {_t3_inst}\n{doc_note}"
                    + (f"\nAdditional context: {t3_notes}" if t3_notes else "")
                    + _t3_tests_ctx
                    + "\n\nAnalyse the provided documents. Identify key findings, control gaps, and potential audit observations. "
                    "For each observation link it to relevant audit tests where possible.\n"
                    "Respond ONLY with valid JSON:\n"
                    '[{"observation":"<concise observation title>","detail":"<2-3 sentences>","risk_level":"Critical|High|Moderate|Low","linked_tests":["<test id or title>"],"source":"<document name or inferred>"}]',
                    system=_t3_spec["role"] + " Analyse documents and identify potential audit observations. Return ONLY a valid JSON array.",
                    max_tokens=4000,
                )
                st.session_state["t3_docs_analysis"] = _parse_json(analysis_raw) or []
            except Exception:
                st.error("Analysis failed. Please try again.")
    st.markdown('</div></div>', unsafe_allow_html=True)

    _t3_analysis = st.session_state.get("t3_docs_analysis") or []
    if _t3_analysis:
        st.markdown("---")
        st.markdown('<div class="section-title">Observations & Findings</div>', unsafe_allow_html=True)
        _LVLC4 = {"Critical": "#ef4444", "High": "#f97316", "Moderate": "#eab308", "Low": "#22d3a5"}
        _obs_list = list(st.session_state.get("t3_observations") or [])
        _obs_ids = {o["id"] for o in _obs_list}
        for _i, _obs in enumerate(_t3_analysis):
            _ocol = _LVLC4.get(_obs.get("risk_level", ""), "#8392bb")
            _tests_str = ", ".join(_obs.get("linked_tests") or []) or "—"
            _already_added = str(_i) in _obs_ids
            st.markdown(f"""
            <div style="border:1px solid {_ocol}33;border-radius:9px;padding:14px 18px;margin-bottom:10px;background:{_ocol}08">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
                <span style="background:{_ocol}22;color:{_ocol};border:1px solid {_ocol}44;border-radius:4px;padding:2px 9px;font-size:11px;font-weight:700">{_obs.get("risk_level","")}</span>
                <span style="font-size:13.5px;font-weight:600;color:var(--text-primary)">{_obs.get("observation","")}</span>
              </div>
              <p style="font-size:12.5px;color:var(--text-secondary);margin:0 0 8px;line-height:1.7">{_obs.get("detail","")}</p>
              <div style="font-size:11.5px;color:var(--text-muted)">🔗 Linked tests: {_tests_str} &nbsp;·&nbsp; 📄 Source: {_obs.get("source","—")}</div>
            </div>""", unsafe_allow_html=True)
            if not _already_added:
                if st.button("➕ Add to Report", key=f"t3_add_obs_{_i}"):
                    _obs_list.append({
                        "id": str(_i),
                        "observation": _obs.get("observation", ""),
                        "detail": _obs.get("detail", ""),
                        "risk_level": _obs.get("risk_level", ""),
                        "linked_tests": _obs.get("linked_tests", []),
                        "source": _obs.get("source", "Document Analyser"),
                    })
                    st.session_state["t3_observations"] = _obs_list
                    st.rerun()
            else:
                st.caption("✓ Added to Report")
        _n_added = len(st.session_state.get("t3_observations") or [])
        if _n_added:
            st.success(f"{_n_added} observation(s) added to the Audit Report tab.")

        # ── Exports for Document Analyser ─────────────────────────────────
        if _t3_analysis:
            st.markdown("---")
            _t3_exp_cols = st.columns([2, 2, 2, 2])
            # Excel export
            if not st.session_state.get("t3_analysis_xlsx"):
                try:
                    import openpyxl
                    from io import BytesIO
                    wb = openpyxl.Workbook()
                    ws = wb.active
                    ws.title = "Observations"
                    ws.append(["Risk Level", "Observation", "Detail", "Linked Tests", "Source"])
                    for _o in _t3_analysis:
                        ws.append([
                            _o.get("risk_level",""), _o.get("observation",""),
                            _o.get("detail",""), ", ".join(_o.get("linked_tests") or []),
                            _o.get("source",""),
                        ])
                    _buf = BytesIO(); wb.save(_buf); _buf.seek(0)
                    st.session_state["t3_analysis_xlsx"] = _buf.getvalue()
                except Exception:
                    pass
            if not st.session_state.get("t3_analysis_pdf"):
                try:
                    _obs_txt = "\n".join(
                        f"[{o.get('risk_level','')}] {o.get('observation','')} — {o.get('detail','')[:100]}"
                        for o in _t3_analysis
                    )
                    st.session_state["t3_analysis_pdf"] = _make_pdf(
                        f"Document Analysis — {t3_topic}",
                        [("Observations", _obs_txt)],
                    )
                except Exception:
                    pass
            with _t3_exp_cols[0]:
                if st.session_state.get("t3_analysis_xlsx"):
                    st.download_button("📗 Excel", data=st.session_state["t3_analysis_xlsx"],
                        file_name="Document_Analysis.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True, key="t3_dl_xlsx")
                else:
                    st.button("📗 Excel", disabled=True, use_container_width=True, key="t3_dl_xlsx_dis")
            with _t3_exp_cols[1]:
                if st.session_state.get("t3_analysis_pdf"):
                    st.download_button("📕 PDF", data=st.session_state["t3_analysis_pdf"],
                        file_name="Document_Analysis.pdf",
                        mime="application/pdf",
                        use_container_width=True, key="t3_dl_pdf")
                else:
                    st.button("📕 PDF", disabled=True, use_container_width=True, key="t3_dl_pdf_dis")


# TAB 4 — AUDIT REPORT
# ─────────────────────────────────────────────────────────────────────────────
elif _active == 4:
    _tab_actions_bar("t3",
        "IIA-standard audit report — assembled from Risk Analysis and Audit Plan context.",
        [
            ("📝 Word", st.session_state.get("t3_docx_bytes") or (
                st.session_state.get("report_data") and None),
             "Audit_Report.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            ("📗 Excel", st.session_state.get("t3_xlsx"),
             "Audit_Findings.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            ("📙 PPT", st.session_state.get("t3_pptx2"),
             "Audit_Report.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
            ("📕 PDF", st.session_state.get("t3_pdf"),
             "Audit_Report.pdf", "application/pdf"),
        ]
    )
    _t4_section = st.radio(
        "Section",
        ["📋 Recommendations", "📄 Report"],
        horizontal=True,
        label_visibility="collapsed",
        key="t4_section_select",
    )
    st.markdown("<div style='margin-bottom:12px'></div>", unsafe_allow_html=True)

    # Inner navigation per section
    _t4_rec_view = None
    _t4_rep_view = None
    if _t4_section == "📋 Recommendations":
        _t4_rec_view = st.radio(
            "View",
            ["📝 My Observations", "📄 Example Report"],
            horizontal=True,
            label_visibility="collapsed",
            key="t4_rec_view_select",
        )
    elif _t4_section == "📄 Report":
        _t4_rep_view = st.radio(
            "View",
            ["1 · Executive Summary", "2 · Narrative & Findings", "3 · Recommendation Details", "4 · KPIs"],
            horizontal=True,
            label_visibility="collapsed",
            key="t4_rep_view_select",
        )
    st.markdown("<div style='margin-bottom:16px'></div>", unsafe_allow_html=True)

    if _t4_rec_view == "📝 My Observations":
        # Show observations from Document Analyser + allow manual add
        _t4_obs = list(st.session_state.get("t3_observations") or [])
        if _t4_obs:
            st.markdown('<div class="section-title">Observations</div>', unsafe_allow_html=True)
            for _ob in _t4_obs:
                _ocol2 = {"Critical":"#ef4444","High":"#f97316","Moderate":"#eab308","Low":"#22d3a5"}.get(_ob.get("risk_level",""), "#8392bb")
                st.markdown(
                    f'<div style="border:1px solid {_ocol2}33;border-radius:8px;padding:10px 16px;margin-bottom:8px;background:{_ocol2}08">'
                    f'<span style="font-size:12.5px;font-weight:600;color:var(--text-primary)">{_ob.get("observation","")}</span>'
                    f'<span style="font-size:11px;color:var(--text-muted);margin-left:10px">— {_ob.get("source","")}</span></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No observations yet. Add them from Document Analyser or manually below.")

        st.markdown("**Add observation manually**")
        _t4_manual = st.text_area("Observation text", placeholder="Describe the finding…", height=80, key="t4_manual_obs")
        if st.button("Add observation", key="t4_add_manual_obs"):
            if _t4_manual.strip():
                _t4_obs.append({
                    "id": f"m_{int(datetime.now().timestamp())}",
                    "observation": _t4_manual.strip(),
                    "detail": "",
                    "risk_level": "Moderate",
                    "linked_tests": [],
                    "source": "Manual",
                })
                st.session_state["t3_observations"] = _t4_obs
                st.rerun()

        st.markdown('<div class="gen-btn-wrap"><div class="gen-btn">', unsafe_allow_html=True)
        _t4_obs_current = st.session_state.get("t3_observations") or []
        if st.button("✦ Generate Recommendations", disabled=_disabled or not _t4_obs_current, key="t4_recs_run"):
            with st.spinner("Generating recommendations…"):
                try:
                    c = _client()
                    _obs_text = "\n".join(
                        f"Observation {_i+1}: {o.get('observation','')} — {o.get('detail','')} [Risk: {o.get('risk_level','')}]"
                        for _i, o in enumerate(_t4_obs_current)
                    )
                    _t4_inst = _entity_institution_str(jurs=st.session_state.get("t1_jurs") or JURISDICTIONS[:4])
                    recs_raw = _call(c,
                        f"Institution: {_t4_inst}\nAudit topic: {st.session_state.get('t1_topic','')}\n\n"
                        f"Observations:\n{_obs_text}\n\n"
                        "For each observation, write a structured audit recommendation using this exact format:\n\n"
                        "Observation N: <title>\n"
                        "Condition: <what was found>\n"
                        "Criteria: <what should be according to standards/policy>\n"
                        "Cause: <root cause>\n"
                        "Effect: <risk or impact if not addressed>\n"
                        "Recommendation: <specific action>\n"
                        "Management Response: [to be completed]\n\n"
                        "Write all recommendations in professional English.",
                        system="You are a senior Big 4 audit partner writing formal audit recommendations.",
                        max_tokens=4000,
                    )
                    st.session_state["t4_recommendations"] = recs_raw
                except Exception:
                    st.error("Generation failed. Please try again.")
        st.markdown('</div></div>', unsafe_allow_html=True)

        _t4_recs = st.session_state.get("t4_recommendations")
        if _t4_recs:
            st.markdown("---")
            st.markdown('<div class="section-title">Generated Recommendations</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:10px;'
                f'padding:18px 22px;font-size:13px;color:var(--text-secondary);white-space:pre-wrap;line-height:1.8">{_t4_recs}</div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "docx ↓  Recommendations",
                data=_t4_recs.encode("utf-8"),
                file_name="Audit_Recommendations.txt",
                mime="text/plain",
                key="t4_recs_dl",
            )

    elif _t4_rec_view == "📄 Example Report":
        st.markdown(
            '<div style="font-size:12px;color:var(--text-muted);margin-bottom:16px">'
            'Reference example — a fully written IIA-standard audit finding, to illustrate the expected structure and tone.</div>',
            unsafe_allow_html=True,
        )
        _ex_findings = [
            {
                "ref": "F-01", "level": "High", "title": "Incomplete source-of-wealth documentation for high-risk PEP clients",
                "condition": "For 8 of 25 PEP client files sampled (32%), source-of-wealth (SoW) documentation was either missing or not refreshed within the mandatory 12-month cycle. In 3 cases, the SoW corroboration relied solely on client self-declaration without independent evidence.",
                "criteria": "FINMA Circular 2011/1 and the bank's AML Policy require documented, independently corroborated SoW for all PEP relationships, refreshed annually as part of enhanced due diligence (EDD).",
                "cause": "The periodic review workflow did not enforce SoW refresh as a blocking control; relationship managers could close a review without uploading updated evidence.",
                "effect": "Heightened exposure to money-laundering and reputational risk; potential regulatory finding and remediation order in the event of a FINMA inspection.",
                "recommendation": "Implement a blocking control in the client lifecycle system preventing periodic-review sign-off until corroborated SoW evidence is attached. Remediate the 8 flagged files within 60 days.",
                "response": "Agreed. Compliance to deploy the blocking control by Q3 2026; flagged files remediated within 60 days. Owner: Head of Compliance.",
            },
            {
                "ref": "F-02", "level": "Moderate", "title": "Delayed off-boarding of dormant privileged access",
                "condition": "Testing of privileged access revealed 12 accounts belonging to leavers or role-changers that remained active between 14 and 47 days beyond the personnel change effective date.",
                "criteria": "The Information Security Policy mandates deactivation of privileged access within 24 hours of a leaver/mover event.",
                "cause": "The HR-to-IAM off-boarding trigger was manual and reliant on email notification, with no automated reconciliation against the HR master.",
                "effect": "Window of unauthorised access to sensitive systems, increasing insider-threat and data-exfiltration risk.",
                "recommendation": "Automate the HR-to-IAM leaver/mover feed with a daily reconciliation exception report reviewed by IT Security.",
                "response": "Agreed. IT to implement automated feed and daily reconciliation by Q4 2026. Owner: CISO.",
            },
        ]
        _ex_lvlc = {"Critical": "#ef4444", "High": "#f97316", "Moderate": "#eab308", "Low": "#22d3a5"}
        for _f in _ex_findings:
            _fc = _ex_lvlc.get(_f["level"], "#8392bb")
            st.markdown(
                f'<div style="border:1px solid {_fc}33;border-radius:12px;padding:18px 22px;margin-bottom:14px;background:{_fc}08">'
                f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">'
                f'<span style="background:{_fc}22;color:{_fc};border:1px solid {_fc}55;border-radius:6px;padding:2px 10px;font-size:11px;font-weight:700">{_f["ref"]} · {_f["level"]}</span>'
                f'<span style="font-size:14px;font-weight:700;color:#eef0f8">{_f["title"]}</span></div>'
                f'<div style="font-size:12.5px;line-height:1.8;color:#94a3b8">'
                f'<p style="margin:0 0 6px"><b style="color:#cbd5e1">Condition:</b> {_f["condition"]}</p>'
                f'<p style="margin:0 0 6px"><b style="color:#cbd5e1">Criteria:</b> {_f["criteria"]}</p>'
                f'<p style="margin:0 0 6px"><b style="color:#cbd5e1">Cause:</b> {_f["cause"]}</p>'
                f'<p style="margin:0 0 6px"><b style="color:#cbd5e1">Effect:</b> {_f["effect"]}</p>'
                f'<p style="margin:0 0 6px"><b style="color:{_fc}">Recommendation:</b> {_f["recommendation"]}</p>'
                f'<p style="margin:0"><b style="color:#22d3a5">Management Response:</b> {_f["response"]}</p>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
        st.caption("💡 This is a static reference example. Use 'My Observations' to build your own findings from the Document Analyser or manual entry.")

    elif _t4_rep_view == "2 · Narrative & Findings":
        _t3_mode = render_mode_toggle("mode_tab3")
        st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)

        # ── Context pills from previous tabs ──────────────────────────────────────
        _t3_ctx = []
        _t3_topic   = st.session_state.get("topic_tab1") or st.session_state.get("t1_topic") or ""
        _t3_scope   = st.session_state.get("t2_scope_in","")
        _t3_jurs    = st.session_state.get("t1_jurs") or ["CH / FINMA"]
        _t3_risks   = st.session_state.get("t1_risks")
        _t3_rat     = st.session_state.get("t2_rationale")
        _t3_bg      = st.session_state.get("t2_background")
        if _t3_topic:   _t3_ctx.append(f"&#10003; Topic: {_t3_topic}")
        if _t3_scope:   _t3_ctx.append("&#10003; Scope defined")
        if _t3_risks:   _t3_ctx.append(f"&#10003; {len(_t3_risks)} risks from Tab 1")
        if _t3_rat:     _t3_ctx.append("&#10003; Rationale from Tab 2")
        if _t3_ctx:
            st.markdown(f'<div class="ctx-pill">{" &nbsp;&middot;&nbsp; ".join(_t3_ctx)}</div>', unsafe_allow_html=True)

        # Entity context hint for Tab 3
        _t3_entity    = st.session_state.get("entity_type", "🏦 Private Banking")
        _t3_ent_ctx   = ENTITY_CONTEXT.get(_t3_entity, {})
        _t3_findings  = _t3_ent_ctx.get("typical_findings", [])
        if _t3_findings:
            _bg3, _col3 = _ENTITY_COLORS.get(_t3_entity, ("#0a2540", "#818cf8"))
            st.markdown(
                f'<div style="background:{_bg3};border-left:3px solid {_col3};border-radius:0 6px 6px 0;'
                f'padding:8px 12px;margin:4px 0 12px;font-size:12px;color:#c8d0e8">'
                f'<span style="font-weight:700;color:{_col3}">{_t3_entity} &mdash; typical findings:</span><br>'
                + "".join(f'<span style="margin-right:14px">&bull; {f}</span>' for f in _t3_findings[:4])
                + '</div>',
                unsafe_allow_html=True,
            )

        # ── Shared inputs (both modes) ─────────────────────────────────────────────
        # Persist findings across interactions
        _t3_findings_raw = st.text_area(
            "Audit Observations & Findings",
            value=st.session_state.get("report_findings_raw",""),
            placeholder=(
                "Enter your field observations, one per line or as free text.\n"
                "Include: what was observed, where, evidence gathered.\n\n"
                "Example:\n"
                "1. Transaction monitoring does not cover transfers below CHF 10,000. Tested on 50 alerts.\n"
                "2. KYC files incomplete for 8 out of 40 High-risk clients — missing source of wealth documentation.\n"
                "3. No PEP screening procedure at Singapore entity — manual process only."
            ),
            height=200,
            key="t3_findings_in",
            help="Each line or paragraph becomes a structured finding with inferred criticality and risk mapping.",
        )
        st.session_state["report_findings_raw"] = _t3_findings_raw

        if _t3_mode == "static":
            # ── Static mode: assemble report from static data ──────────────────────
            _static_label()
            _t3_valid = bool(_t3_findings_raw.strip())
            if not _t3_valid:
                st.info("ℹ️ Enter at least one observation above to generate the report.")

            if st.button("Generate Report", type="primary", disabled=not _t3_valid, key="t3_run_static"):
                with st.spinner("Generating report…"):
                    rd = _assemble_report_static(
                        _t3_findings_raw, _t3_topic, _t3_scope, _t3_jurs,
                        _t3_risks, _t3_rat, _t3_bg,
                    )
                    st.session_state["report_data"]      = rd
                    st.session_state["report_generated"] = True
                    st.session_state["report_timestamp"] = datetime.now().strftime("%d %b %Y %H:%M")
                    st.rerun()

            if st.session_state.get("report_generated") and st.session_state.get("report_data"):
                rd    = st.session_state["report_data"]
                ts    = st.session_state.get("report_timestamp","")
                rname = f"Audit_Report_{rd['topic'].replace(' ','_')}"
                st.markdown("---")
                st.markdown(
                    f'<div style="font-size:11px;color:#5a6488;margin-bottom:16px">Report generated: {ts} &nbsp;&middot;&nbsp; '
                    f'Topic: <strong style="color:#8392bb">{rd["topic"]}</strong> &nbsp;&middot;&nbsp; '
                    f'{rd["n_total"]} finding(s)</div>',
                    unsafe_allow_html=True,
                )

                with st.expander("📊 Section 1 — Executive Summary", expanded=True):
                    st.markdown('<div class="section-title">1. Executive Summary</div>', unsafe_allow_html=True)
                    _show_report_section1(rd)

                with st.expander("📖 Section 2 — Summary of Findings", expanded=False):
                    st.markdown('<div class="section-title">2. Summary of Findings</div>', unsafe_allow_html=True)
                    _show_report_section2(rd)

                with st.expander("🔍 Section 3 — Detailed Recommendations", expanded=False):
                    st.markdown('<div class="section-title">3. Detailed Recommendations</div>', unsafe_allow_html=True)
                    _show_report_section3(rd)

                with st.expander("✅ Section 4 — Action Plan Summary", expanded=False):
                    st.markdown('<div class="section-title">4. Action Plan Summary</div>', unsafe_allow_html=True)
                    _show_report_section4(rd)

                # IIA Standards & Regulatory Reference (kept as reference)
                with st.expander("📚 A — IIA Standards Reference 2024", expanded=False):
                    st.markdown(f'<div class="section-title">A. IIA Standards Reference &mdash; 2024 <span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{len(IIA_STANDARDS_2024)} standards</span></div>', unsafe_allow_html=True)
                    _iia_sq3 = st.text_input("Search IIA Standards", placeholder="Filter standards…", key="_iia_sq3", label_visibility="collapsed")
                    _iia_f3 = IIA_STANDARDS_2024
                    if _iia_sq3:
                        _qi3 = _iia_sq3.lower()
                        _iia_f3 = [s for s in IIA_STANDARDS_2024 if _qi3 in (s.get("title","") + s.get("standard_id","")).lower()]
                    for _s3 in _iia_f3:
                        _render_iia_standard(_s3)

                with st.expander("⚖️ B — Regulatory Reference Panel", expanded=False):
                    st.markdown(f'<div class="section-title">B. Regulatory Reference &mdash; {" &middot; ".join(_t3_jurs[:3])}</div>', unsafe_allow_html=True)
                    _reg3_sq = st.text_input("Search frameworks", placeholder="Filter frameworks…", key="_reg3_sq", label_visibility="collapsed")
                    for _jur3 in _t3_jurs:
                        _reg3_items = REGULATORY_FRAMEWORKS.get(_jur3, [])
                        if _reg3_sq:
                            _qrg = _reg3_sq.lower()
                            _reg3_items = [r for r in _reg3_items if _qrg in (r.get("title","") + r.get("reference","")).lower()]
                        if _reg3_items:
                            with st.expander(f"**{_jur3}** — {len(_reg3_items)} texts"):
                                _rows3 = "".join(
                                    f'<tr><td style="padding:8px 12px;color:#818cf8;font-weight:600;white-space:nowrap;border-bottom:1px solid var(--tbl-row-border)">{r.get("reference","")}</td>'
                                    f'<td style="padding:8px 12px;color:var(--text-primary);border-bottom:1px solid var(--tbl-row-border)">{r.get("title","")}</td>'
                                    f'<td style="padding:8px 12px;color:var(--text-secondary);font-size:11.5px;border-bottom:1px solid var(--tbl-row-border)">{r.get("scope","")[:120]}</td></tr>'
                                    for r in _reg3_items
                                )
                                st.markdown(f'<table class="data-table" style="font-size:12px"><thead><tr style="background:rgba(99,102,241,0.07)"><th style="color:#818cf8;padding:8px 12px;width:15%">Reference</th><th style="color:#818cf8;padding:8px 12px;width:40%">Title</th><th style="color:#818cf8;padding:8px 12px;width:45%">Scope</th></tr></thead><tbody>{_rows3}</tbody></table>', unsafe_allow_html=True)

                # ── Revision expander ─────────────────────────────────────────────
                with st.expander("✏️ Request a Revision", expanded=False):
                    st.markdown('<div style="font-size:13px;color:var(--text-secondary);margin-bottom:10px">Modify your observations above and click <strong>Generate Report</strong> again to refresh all sections.</div>', unsafe_allow_html=True)
                    _rev_note = st.text_input(
                        "What would you like to revise?",
                        placeholder="e.g. Add that finding #2 also affects the HK entity.",
                        key="t3_rev_static_in",
                    )
                    if _rev_note:
                        st.info(f"ℹ️ Update your findings text above to incorporate: '{_rev_note}', then click Generate Report.")

                # ── Export buttons ────────────────────────────────────────────────
                st.markdown("---")
                _fe1, _fe2, _fe3 = st.columns([2, 2, 2])
                _fe1.caption("docx — available after live generation")
                try:
                    _action_rows = [
                        {"Finding": f"F{f['idx']}: {f['title']}", "Rating": f['criticality'],
                         "Due Date": f['due_date'], "Status": "Open",
                         "Owner": (f.get('mgmt_actions',[{}])[0].get('owner','TBD') if f.get('mgmt_actions') else 'TBD'),
                         "Recommendation": (f.get('mgmt_actions',[{}])[0].get('action','') if f.get('mgmt_actions') else '')}
                        for f in rd["detailed"]
                    ]
                    import io, pandas as pd
                    _ap_xlsx_buf = io.BytesIO()
                    pd.DataFrame(_action_rows).to_excel(_ap_xlsx_buf, index=False)
                    _ap_xlsx_buf.seek(0)
                    _fe2.download_button("📗 Excel", data=_ap_xlsx_buf,
                                         file_name=f"{rname}_ActionPlan.xlsx",
                                         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                except Exception:
                    pass
                _fe3.caption("pptx — available after live generation")

            else:
                # Reference panels shown before report is generated
                st.markdown("---")
                st.markdown(_EXAMPLE_FINDING, unsafe_allow_html=True)
                with st.expander("📚 A — IIA Standards Reference 2024", expanded=True):
                    st.markdown(f'<div class="section-title">A. IIA Standards Reference &mdash; 2024 <span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{len(IIA_STANDARDS_2024)} standards</span></div>', unsafe_allow_html=True)
                    st.markdown(_EXAMPLE_IIA_STD, unsafe_allow_html=True)
                    _iia_sq = st.text_input("Search IIA Standards", placeholder="Filter standards…", key="_iia_sq", label_visibility="collapsed")
                    _iia_filtered = IIA_STANDARDS_2024
                    if _iia_sq:
                        _qi = _iia_sq.lower()
                        _iia_filtered = [s for s in IIA_STANDARDS_2024 if _qi in (s.get("title","") + s.get("description","") + s.get("standard_id","")).lower()]
                    for _s in _iia_filtered:
                        _render_iia_standard(_s)
                with st.expander("⚖️ B — Regulatory Reference Panel", expanded=False):
                    _t3_jurs_disp = st.session_state.get("t1_jurs") or list(REGULATORY_FRAMEWORKS.keys())[:3]
                    st.markdown(f'<div class="section-title">B. Regulatory Reference &mdash; {" &middot; ".join(_t3_jurs_disp[:4])}</div>', unsafe_allow_html=True)
                    st.markdown(_EXAMPLE_DORA, unsafe_allow_html=True)
                    _reg3b_sq = st.text_input("Search frameworks", placeholder="Filter frameworks…", key="_reg3b_sq", label_visibility="collapsed")
                    for _jur in _t3_jurs_disp:
                        _r3b = [r for r in REGULATORY_FRAMEWORKS.get(_jur,[]) if not _reg3b_sq or _reg3b_sq.lower() in (r.get("title","") + r.get("reference","")).lower()]
                        if _r3b:
                            with st.expander(f"**{_jur}** — {len(_r3b)} texts"):
                                _rows3b = "".join(
                                    f'<tr><td style="padding:9px 13px;color:#818cf8;font-weight:600;white-space:nowrap;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("reference","")}</td>'
                                    f'<td style="padding:9px 13px;color:var(--text-primary);font-weight:500;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("title","")}<br><span style="font-size:11px;color:var(--text-muted)">{r.get("authority","")} &middot; {r.get("year","")}</span></td>'
                                    f'<td style="padding:9px 13px;color:var(--text-secondary);font-size:11.5px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)">{r.get("scope","")}</td>'
                                    f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid var(--tbl-row-border)"><ul style="margin:0;padding-left:15px;font-size:11.5px;color:var(--text-secondary);line-height:1.7">{"".join(f"<li>{k}</li>" for k in r.get("key_requirements",[]))}</ul></td>'
                                    f'</tr>'
                                    for r in _r3b
                                )
                                st.markdown(f'<table class="data-table" style="font-size:12px"><thead><tr style="background:rgba(99,102,241,0.07);border-bottom:1px solid rgba(99,102,241,0.18)"><th style="color:#818cf8;width:10%">Reference</th><th style="color:#818cf8;width:22%">Title</th><th style="color:#818cf8;width:22%">Scope</th><th style="color:#818cf8;width:46%">Key Requirements</th></tr></thead><tbody>{_rows3b}</tbody></table>', unsafe_allow_html=True)
                st.markdown("<div class='no-print' style='margin-top:1rem'>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        if _t3_mode == "live":
            # ── Live mode: API-generated report ────────────────────────────────────
            _t3_ctx_live = []
            if st.session_state.t1_topic:
                _t3_ctx_live.append(f"&#10003; Topic: {st.session_state.t1_topic}")
            if st.session_state.t2_org_plan:
                _t3_ctx_live.append("&#10003; Audit plan available")
            if _t3_ctx_live:
                st.markdown(f'<div class="ctx-pill">{" &nbsp;&middot;&nbsp; ".join(_t3_ctx_live)}</div>', unsafe_allow_html=True)

            default_name = f"Internal Audit — {st.session_state.t1_topic} — {datetime.now().year}" if st.session_state.t1_topic else ""
            audit_name = st.text_input(
                "Report Title",
                value=default_name,
                placeholder="e.g. Internal Audit — AML/KYC — Private Banking Group — 2025",
                key="t3_name_in",
            )

            uploads3 = st.file_uploader(
                "Working papers (optional — PDF, Word, Excel, TXT)",
                type=["pdf", "docx", "xlsx", "txt"], accept_multiple_files=True, key="t3_upload",
            )
            st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

            _t3_live_valid = bool(audit_name and _t3_findings_raw.strip())
            if not _t3_live_valid and not st.session_state.get("demo_mode"):
                st.warning("⚠ Enter a report title and at least one observation to generate the report.")

            if st.session_state.get("demo_mode"):
                if st.button("✦ Generate Audit Report", key="t3_run_demo", use_container_width=True):
                    with st.spinner(""):
                        _demo_stream_generate(
                            _DEMO_CONTENT["gen_steps_t3"],
                            {
                                "t3_report": {"text": _DEMO_CONTENT["t3_report"], "name": "AUD-2025-TPR-001"},
                            }
                        )
                        st.rerun()

            if not st.session_state.get("demo_mode") and st.button("Generate Report", type="primary",
                         disabled=_disabled or not _t3_live_valid, key="t3_run"):
                with st.spinner("Generating report…"):
                    try:
                        c = _client()
                        file_ids3 = []
                        for uf in (uploads3 or []):
                            fm = _upload_sf(c, uf)
                            if fm:
                                file_ids3.append(fm)

                        reg_ctx  = (f"\n\nApplicable regulations:\n{json.dumps(st.session_state.t1_regs, indent=2)[:1500]}"
                                    if st.session_state.t1_regs else "")
                        plan_ctx = (f"\n\nAudit plan:\n{st.session_state.t2_org_plan[:900]}"
                                    if st.session_state.t2_org_plan else "")
                        jur_str  = ", ".join(_t3_jurs)

                        user_content = []
                        if file_ids3:
                            user_content.extend(build_file_content_blocks(file_ids3))
                            user_content.append({"type": "text", "text": f"{len(file_ids3)} working paper(s) attached."})

                        user_content.append({"type": "text", "text": (
                            f"Draft a professional IIA-standard internal audit report in English.\n\n"
                            f"Report title: {audit_name}\n"
                            f"Institution: {_entity_institution_str(jurs=_t3_jurs)}"
                            f"{reg_ctx}{plan_ctx}\n\n"
                            f"Issues log:\n{_t3_findings_raw}\n\n"
                            f"Structure:\n"
                            f"1. Executive Summary — opinion, key findings, priority actions\n"
                            f"2. Background & Context\n"
                            f"3. Scope & Methodology\n"
                            f"4. Findings — sorted by severity (Critical first): rating, impact, root cause, recommendation, owner, target date\n"
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

                        # Also build static enrichment for snapshot / Tab 0
                        _rd_static = _assemble_report_static(
                            _t3_findings_raw, _t3_topic, _t3_scope, _t3_jurs, _t3_risks, _t3_rat, _t3_bg,
                        )
                        st.session_state["report_data"]      = _rd_static
                        st.session_state["report_generated"] = True
                        st.session_state["report_timestamp"] = datetime.now().strftime("%d %b %Y %H:%M")

                        _obs_lines = [ln.strip("0123456789. \t-") for ln in _t3_findings_raw.strip().splitlines() if ln.strip()]
                        _findings_export = [{"title": ln[:80], "rating": "High", "observation": ln,
                                             "risk":"","recommendation":"","owner":"","due_date":""} for ln in _obs_lines if ln]
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
                        try:
                            _rd = st.session_state.get("report_data") or {}
                            _t3_sections = [(k.replace("_"," ").title(), str(v))
                                            for k, v in _rd.items()
                                            if v and k not in ("findings","top3","detailed","theme_groups")]
                            if not _t3_sections:
                                _t3_sections = [("Findings", _t3_findings_raw)]
                            st.session_state.t3_pdf = _make_pdf(audit_name or "Audit Report", _t3_sections)
                        except Exception:
                            pass

                    except Exception:
                        st.error("An error occurred. Please try again.")

            # Results (live mode)
            if st.session_state.t3_report:
                res  = st.session_state.t3_report
                name = res.get("name","report")
                st.markdown("---")

                with st.expander("📄 A — Generated Audit Report", expanded=True):
                    st.markdown('<div class="section-title">Generated Audit Report</div>', unsafe_allow_html=True)
                    text = res.get("text","")
                    if text:
                        st.markdown(f'<div class="output-box">{text}</div>', unsafe_allow_html=True)
                        _copy_button(text, "t3_report_copy")
                    else:
                        st.info("Report content is available in the export file.")
                    st.markdown("---")
                    _t3_has_exports = res.get("docx_bytes") or st.session_state.t3_xlsx or st.session_state.t3_pptx2
                    if _t3_has_exports:
                        _f1, _f2, _f3 = st.columns([2, 2, 2])
                        if res.get("docx_bytes"):
                            _f1.download_button("📝 Word", data=res["docx_bytes"],
                                                file_name=f"Audit_Report_{name.replace(' ','_')}.docx",
                                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                        if st.session_state.t3_xlsx:
                            _f2.download_button("📗 Excel", data=st.session_state.t3_xlsx,
                                                file_name=f"Audit_Findings_{name.replace(' ','_')}.xlsx",
                                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                        if st.session_state.t3_pptx2:
                            _f3.download_button("📙 PPT", data=st.session_state.t3_pptx2,
                                                file_name=f"Audit_Report_{name.replace(' ','_')}.pptx",
                                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")


                # Static-enriched sections also shown in live mode
                if st.session_state.get("report_data"):
                    _rd2 = st.session_state["report_data"]
                    with st.expander("📊 Section 1 — Executive Summary (Structured)", expanded=False):
                        _show_report_section1(_rd2)
                    with st.expander("🔍 Section 3 — Detailed Recommendations", expanded=False):
                        _show_report_section3(_rd2)
                    with st.expander("✅ Section 4 — Action Plan", expanded=False):
                        _show_report_section4(_rd2)

                with st.expander("✏️ Request a Revision", expanded=False):
                    st.markdown('<div class="section-title">Targeted Revision</div>', unsafe_allow_html=True)
                    followup = st.text_area(
                        "What would you like to revise?", label_visibility="collapsed", height=80,
                        placeholder="e.g. Strengthen recommendation 3. Add a 30-day deadline for the KYC finding.",
                        key="t3_rev_in",
                    )
                    if st.button("Revise", disabled=not followup or _disabled, key="t3_rev_btn"):
                        with st.spinner("Applying revisions…"):
                            try:
                                c = _client()
                                rev_content = [{"type":"text","text":(
                                    f"Previous report:\n{res.get('text','')[:3000]}\n\n"
                                    f"Revision instructions: {followup}\n\nApply revisions precisely. Then call generate_audit_report to export."
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
                                    [{"role":"user","content":rev_content}], _h3r)
                                res2 = {"text": text2, "name": name}
                                if "docx_path" in extra2 and Path(extra2["docx_path"]).exists():
                                    res2["docx_bytes"] = Path(extra2["docx_path"]).read_bytes()
                                st.session_state.t3_report = res2
                                st.rerun()
                            except Exception:
                                st.error("An error occurred. Please try again.")

    elif _t4_rep_view == "1 · Executive Summary":
        st.markdown(
            '<div style="font-size:12px;color:var(--text-muted);margin-bottom:16px">'
            '1-page summary for the Audit Committee — generated from all data collected in this session.</div>',
            unsafe_allow_html=True,
        )
        _t4_topic   = st.session_state.get("t1_topic") or "—"
        _t4_entity  = st.session_state.get("entity_type", "🏦 Private Banking")
        _t4_jurs    = ", ".join(st.session_state.get("t1_jurs") or []) or "—"
        _t4_n_risks = len(st.session_state.get("t1_risks") or [])
        _t4_n_tests = len(st.session_state.get("t2_tests") or [])
        _t4_n_obs   = len(st.session_state.get("t3_observations") or [])
        _t4_n_prior = sum(1 for r in (st.session_state.get("t0_prior_recs") or [])
                          if r.get("status") in ("Open", "Not implemented", "Partially implemented"))
        _t4_tstat   = dict(st.session_state.get("t2_test_statuses") or {})
        _t4_exc     = [tid for tid, sv in _t4_tstat.items() if sv.get("status") == "Exception"]
        _t4_done_n  = sum(1 for sv in _t4_tstat.values() if sv.get("status") in ("Completed", "N/A"))
        _exc_col    = "#ef4444" if _t4_exc else "#22d3a5"
        _prior_col  = "#f97316" if _t4_n_prior else "#22d3a5"
        st.markdown(f"""
        <div class="agent-card" style="margin-bottom:20px">
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;text-align:center">
            <div><div style="font-size:22px;font-weight:800;color:var(--accent-primary)">{_t4_n_risks}</div><div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px">Risks identified</div></div>
            <div><div style="font-size:22px;font-weight:800;color:var(--accent-primary)">{_t4_n_tests}</div><div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px">Tests planned</div></div>
            <div><div style="font-size:22px;font-weight:800;color:{_exc_col}">{len(_t4_exc)}</div><div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px">Exceptions</div></div>
            <div><div style="font-size:22px;font-weight:800;color:{_prior_col}">{_t4_n_prior}</div><div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px">Open N-1 items</div></div>
          </div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="gen-btn-wrap"><div class="gen-btn">', unsafe_allow_html=True)
        if st.button("✦ Generate Executive Summary", disabled=_disabled or _t4_topic == "—", key="t4_exec_run"):
            with st.spinner("Generating executive summary…"):
                try:
                    c = _client()
                    _exc_detail = ""
                    if _t4_exc:
                        _exc_tests = [t for t in (st.session_state.get("t2_tests") or [])
                                      if (t.get("test_id") or "") in _t4_exc]
                        _exc_detail = "\nExceptions noted on: " + ", ".join(t.get("title", "") for t in _exc_tests)
                    _obs_summary = "\n".join(
                        f"- [{o.get('risk_level', '')}] {o.get('observation', '')}"
                        for o in (st.session_state.get("t3_observations") or [])
                    )
                    _prior_summary = "\n".join(
                        f"- {r.get('text', '')} [{r.get('status', '')}]"
                        for r in (st.session_state.get("t0_prior_recs") or [])
                        if r.get("status") in ("Open", "Not implemented", "Partially implemented")
                    )
                    _recs_text = st.session_state.get("t4_recommendations") or ""
                    exec_raw = _call(c,
                        f"Audit topic: {_t4_topic}\nEntity: {_t4_entity}\nJurisdictions: {_t4_jurs}\n"
                        f"Risks identified: {_t4_n_risks} | Tests planned: {_t4_n_tests} | "
                        f"Tests with exceptions: {len(_t4_exc)} | Observations: {_t4_n_obs}"
                        + (_exc_detail or "")
                        + (f"\n\nKey observations:\n{_obs_summary}" if _obs_summary else "")
                        + (f"\n\nOpen prior-cycle items:\n{_prior_summary}" if _prior_summary else "")
                        + (f"\n\nDraft recommendations summary:\n{_recs_text[:800]}" if _recs_text else "")
                        + "\n\nWrite a concise Audit Committee Executive Summary (max 1 page). Structure:\n"
                        "1. OVERALL AUDIT OPINION (1 sentence: Satisfactory / Partially Satisfactory / Unsatisfactory + rationale)\n"
                        "2. SCOPE & OBJECTIVES (2-3 sentences)\n"
                        "3. KEY FINDINGS (bullet points, max 5, ranked by risk)\n"
                        "4. EXCEPTIONS NOTED (if any)\n"
                        "5. PRIOR CYCLE FOLLOW-UP STATUS (if applicable)\n"
                        "6. OVERALL CONCLUSION & NEXT STEPS (2-3 sentences)\n\n"
                        "Tone: formal, concise, suitable for a board-level audience. No jargon.",
                        system="You are a Chief Audit Executive writing an executive summary for the Audit Committee.",
                        max_tokens=2000,
                    )
                    st.session_state["t4_exec_summary"] = exec_raw
                except Exception:
                    st.error("Generation failed. Please try again.")
        st.markdown('</div></div>', unsafe_allow_html=True)
        _t4_exec = st.session_state.get("t4_exec_summary")
        if _t4_exec:
            st.markdown("---")
            st.markdown(
                f'<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:10px;'
                f'padding:24px 28px;font-size:13px;color:var(--text-secondary);white-space:pre-wrap;line-height:1.9">{_t4_exec}</div>',
                unsafe_allow_html=True,
            )
            _ex1, _ex2 = st.columns(2)
            _ex1.download_button(
                "docx ↓  Executive Summary",
                data=_t4_exec.encode("utf-8"),
                file_name=f"ExecSummary_{_t4_topic.replace(' ', '_')}.txt",
                mime="text/plain",
                key="t4_exec_dl_txt",
            )
            try:
                _exec_pdf = _make_pdf(
                    f"Audit Committee — Executive Summary\n{_t4_topic}",
                    [("Executive Summary", _t4_exec)],
                )
                if _exec_pdf:
                    _ex2.download_button(
                        "pdf ↓  Executive Summary",
                        data=_exec_pdf,
                        file_name=f"ExecSummary_{_t4_topic.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        key="t4_exec_dl_pdf",
                    )
            except Exception:
                pass

    elif _t4_rep_view == "3 · Recommendation Details":
        st.markdown(
            '<div style="font-size:12px;color:var(--text-muted);margin-bottom:16px">'
            'Structured detail for every observation — pulled live from the Recommendations tab.</div>',
            unsafe_allow_html=True,
        )
        _rd_obs = list(st.session_state.get("t3_observations") or [])
        if not _rd_obs:
            st.info("No observations yet. Add them in **📋 Recommendations → My Observations** (from the Document Analyser or manually).")
        else:
            _rd_lvlc = {"Critical": "#ef4444", "High": "#f97316", "Moderate": "#eab308", "Low": "#22d3a5"}
            for _ri, _ob in enumerate(_rd_obs):
                _rc = _rd_lvlc.get(_ob.get("risk_level", ""), "#8392bb")
                _tests = ", ".join(_ob.get("linked_tests") or []) or "—"
                _detail = _ob.get("detail") or "—"
                st.markdown(
                    f'<div style="border:1px solid {_rc}33;border-left:4px solid {_rc};border-radius:10px;'
                    f'padding:16px 20px;margin-bottom:12px;background:{_rc}08">'
                    f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">'
                    f'<span style="background:{_rc}22;color:{_rc};border:1px solid {_rc}55;border-radius:6px;padding:2px 9px;font-size:11px;font-weight:700">R-{_ri+1:02d} · {_ob.get("risk_level","")}</span>'
                    f'<span style="font-size:13.5px;font-weight:700;color:#eef0f8">{_ob.get("observation","")}</span></div>'
                    f'<p style="font-size:12.5px;color:#94a3b8;line-height:1.7;margin:0 0 8px">{_detail}</p>'
                    f'<div style="font-size:11.5px;color:#6b7a99">🔗 Linked tests: {_tests} &nbsp;·&nbsp; 📄 Source: {_ob.get("source","—")}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    elif _t4_rep_view == "4 · KPIs":
        st.markdown(
            '<div style="font-size:12px;color:var(--text-muted);margin-bottom:16px">'
            'Audit engagement metrics — computed from this session\'s data.</div>',
            unsafe_allow_html=True,
        )
        _kp_risks = st.session_state.get("t1_risks") or []
        _kp_tests = st.session_state.get("t2_tests") or []
        _kp_obs   = st.session_state.get("t3_observations") or []
        _kp_prior = st.session_state.get("t0_prior_recs") or []
        _kp_tstat = dict(st.session_state.get("t2_test_statuses") or {})
        # Findings by criticality
        _kp_by_lvl = {"Critical": 0, "High": 0, "Moderate": 0, "Low": 0}
        for _o in _kp_obs:
            _lv = _o.get("risk_level", "")
            if _lv in _kp_by_lvl:
                _kp_by_lvl[_lv] += 1
        # Test completion
        _kp_done = sum(1 for _s in _kp_tstat.values() if str(_s).lower() in ("done", "complete", "completed", "pass", "passed"))
        _kp_test_pct = int(round(100 * _kp_done / len(_kp_tests))) if _kp_tests else 0
        # Prior recs open
        _kp_open_prior = sum(1 for r in _kp_prior if r.get("status") in ("Open", "Not implemented", "Partially implemented"))

        _kp_cards = [
            ("Risks Identified", len(_kp_risks), "#818cf8", "from Risk Analysis"),
            ("Tests in Programme", len(_kp_tests), "#818cf8", f"{_kp_test_pct}% marked complete"),
            ("Observations Raised", len(_kp_obs), "#f97316", "from Document Analyser"),
            ("Prior Recs Open (N-1)", _kp_open_prior, "#ef4444" if _kp_open_prior else "#22d3a5", "follow-up required"),
        ]
        _kp_cols = st.columns(4, gap="small")
        for _kc, (_lbl, _val, _col, _sub) in enumerate(_kp_cards):
            _kp_cols[_kc].markdown(
                f'<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;'
                f'padding:18px 20px;text-align:center;box-shadow:var(--shadow-card)">'
                f'<div style="font-size:30px;font-weight:800;color:{_col};line-height:1">{_val}</div>'
                f'<div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#6b7a99;margin:6px 0 2px">{_lbl}</div>'
                f'<div style="font-size:10.5px;color:#4a5568">{_sub}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='margin:24px 0 10px'><span style='font-size:13px;font-weight:700;color:#eef0f8;text-transform:uppercase;letter-spacing:.06em'>Findings by Criticality</span></div>", unsafe_allow_html=True)
        _kp_lvlc = {"Critical": "#ef4444", "High": "#f97316", "Moderate": "#eab308", "Low": "#22d3a5"}
        _kp_max = max(_kp_by_lvl.values()) or 1
        for _lvl, _cnt in _kp_by_lvl.items():
            _lc = _kp_lvlc[_lvl]
            _pct = int(round(100 * _cnt / _kp_max)) if _cnt else 0
            st.markdown(
                f'<div style="margin-bottom:10px">'
                f'<div style="display:flex;justify-content:space-between;margin-bottom:4px">'
                f'<span style="font-size:12px;color:#eef0f8;font-weight:600">{_lvl}</span>'
                f'<span style="font-size:12px;color:{_lc};font-weight:700">{_cnt}</span></div>'
                f'<div style="background:rgba(255,255,255,.06);border-radius:4px;height:8px;overflow:hidden">'
                f'<div style="width:{_pct}%;height:100%;background:{_lc};border-radius:4px"></div></div></div>',
                unsafe_allow_html=True,
            )
        if not _kp_obs:
            st.caption("No observations yet — criticality breakdown will populate as findings are raised.")


# TAB 5 — CONTINUOUS AUDIT DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
elif _active == 5:
    # Automated control test results
    _t5_controls = [
        {"id": "CTL-001", "process": "AML Transaction Monitoring",  "freq": "Daily",   "last_run": "2026-06-03 06:00", "coverage": 100, "result": "Exception", "exceptions": 3},
        {"id": "CTL-002", "process": "Privileged Access Review",     "freq": "Weekly",  "last_run": "2026-06-02 22:00", "coverage": 97,  "result": "Fail",      "exceptions": 47},
        {"id": "CTL-003", "process": "Reconciliation CHF/USD T+1",   "freq": "Daily",   "last_run": "2026-06-03 07:30", "coverage": 100, "result": "Exception", "exceptions": 3},
        {"id": "CTL-004", "process": "Sanctions Screening (OFAC/EU)","freq": "Daily",   "last_run": "2026-06-03 06:30", "coverage": 100, "result": "Pass",      "exceptions": 0},
        {"id": "CTL-005", "process": "VaR Limit Monitoring",         "freq": "Daily",   "last_run": "2026-06-03 05:45", "coverage": 100, "result": "Fail",      "exceptions": 1},
        {"id": "CTL-006", "process": "KYC Periodic Review SLA",      "freq": "Weekly",  "last_run": "2026-06-02 20:00", "coverage": 89,  "result": "Exception", "exceptions": 12},
        {"id": "CTL-007", "process": "Segregation of Duties (SoD)",  "freq": "Monthly", "last_run": "2026-06-01 02:00", "coverage": 95,  "result": "Pass",      "exceptions": 0},
        {"id": "CTL-008", "process": "GDPR Data Retention Check",    "freq": "Monthly", "last_run": "2026-06-01 03:00", "coverage": 84,  "result": "Fail",      "exceptions": 2},
        {"id": "CTL-009", "process": "Dormant Account Review",       "freq": "Weekly",  "last_run": "2026-06-02 21:00", "coverage": 100, "result": "Pass",      "exceptions": 0},
        {"id": "CTL-010", "process": "Outsourcing SLA Monitor",      "freq": "Daily",   "last_run": "2026-06-03 06:15", "coverage": 100, "result": "Exception", "exceptions": 1},
    ]
    # Exception & anomaly feed (specific automated test outputs)
    _t5_exceptions = [
        {"ts": "03 Jun 06:00", "ctl": "CTL-001", "type": "STR Delay",         "entity": "SG / MAS",   "desc": "3 STR filings overdue > 30 days — CHF 2.1M aggregate",                  "impact": "CHF 2.1M",   "status": "Escalated"},
        {"ts": "02 Jun 22:00", "ctl": "CTL-002", "type": "Access Anomaly",    "entity": "CH / FINMA", "desc": "47 privileged accounts active without JIRA ticket — no change window",    "impact": "—",          "status": "Assigned"},
        {"ts": "03 Jun 07:30", "ctl": "CTL-003", "type": "Rec Break",         "entity": "HK / SFC",   "desc": "3 T+1 breaks — CHF 142k unmatched, counterparty: Deutsche Bank HK",       "impact": "CHF 142k",   "status": "In Review"},
        {"ts": "03 Jun 05:45", "ctl": "CTL-005", "type": "Limit Breach",      "entity": "HK / SFC",   "desc": "VaR CHF 8.4M vs limit CHF 7.0M — 3rd consecutive breach, HK desk",        "impact": "CHF 1.4M ↑", "status": "Escalated"},
        {"ts": "02 Jun 20:00", "ctl": "CTL-006", "type": "SLA Overrun",       "entity": "CH / FINMA", "desc": "12 clients: KYC review > 365 days overdue — enhanced CDD required",        "impact": "—",          "status": "Assigned"},
        {"ts": "01 Jun 03:00", "ctl": "CTL-008", "type": "Retention Breach",  "entity": "EU / DORA",  "desc": "2 datasets retained beyond 7-yr GDPR limit — 12,400 records flagged",       "impact": "—",          "status": "In Review"},
        {"ts": "03 Jun 06:15", "ctl": "CTL-010", "type": "SLA Breach",        "entity": "CH / FINMA", "desc": "Clearstream uptime 94.1% vs 99.5% SLA — cumulative loss CHF 38k",          "impact": "CHF 38k",    "status": "Escalated"},
    ]
    # Control health: 12-week sparkline data (P=pass, W=warning, F=fail)
    _t5_health = [
        {"id": "CTL-001", "name": "AML Txn Monitoring",   "weeks": list("PPPPPPPPWWPF")},
        {"id": "CTL-002", "name": "Privileged Access",    "weeks": list("PPWWPPPPPPWF")},
        {"id": "CTL-003", "name": "Reconciliation T+1",   "weeks": list("PPPPPPWPPWPW")},
        {"id": "CTL-004", "name": "Sanctions Screening",  "weeks": list("PPPPPPPPPPPP")},
        {"id": "CTL-005", "name": "VaR Limit Monitor",    "weeks": list("PPPPWWPPPWWF")},
        {"id": "CTL-006", "name": "KYC Review SLA",       "weeks": list("PWWPPPWWWWWW")},
        {"id": "CTL-007", "name": "SoD Check",            "weeks": list("PPPPPPPPPPPP")},
        {"id": "CTL-008", "name": "GDPR Retention",       "weeks": list("PPPPPPWWWWWF")},
    ]
    # Audit universe coverage matrix
    _t5_entities = ["CH / FINMA", "SG / MAS", "HK / SFC", "UK / FCA", "EU / DORA", "Bahamas"]
    _t5_processes = ["AML/KYC", "Market Risk", "Credit Risk", "Cyber/IT", "Third Party", "GDPR/Data", "Op. Risk"]
    # C=continuous, P=periodic, G=gap, N=none
    _t5_matrix = [
        ["C","C","P","C","C","P","P"],  # CH / FINMA
        ["C","P","P","C","C","P","P"],  # SG / MAS
        ["C","C","P","P","P","G","P"],  # HK / SFC
        ["C","P","G","C","P","C","P"],  # UK / FCA
        ["P","P","G","C","C","C","P"],  # EU / DORA
        ["P","G","N","G","G","N","G"],  # Bahamas
    ]
    _t5_matrix_legend = {"C": ("#0d2b1d","#22d3a5","Continuous"), "P": ("#1a2340","#818cf8","Periodic"), "G": ("#2e1f0a","#f97316","Gap"), "N": ("#1a0a0a","#ef4444","None")}

    _t5_badge = {"Exception": ("#2e1f0a","#f97316"), "Fail": ("#3b0e0e","#ef4444"), "Pass": ("#0d2b1d","#22d3a5")}
    _t5_st_color = {"Escalated": "#ef4444", "Assigned": "#f97316", "In Review": "#818cf8", "Closed": "#22d3a5"}
    _t5_dot = {"P": "#22d3a5", "W": "#f97316", "F": "#ef4444"}

    st.markdown("""
<div style="margin-bottom:24px">
  <div style="font-size:22px;font-weight:800;color:#eef0f8;margin-bottom:4px">📡 Continuous Audit Dashboard</div>
  <div style="font-size:13px;color:#6b7a99">Automated control testing · Exception detection · Coverage monitoring</div>
</div>
""", unsafe_allow_html=True)

    # ── Block 1: Automated Control Test Results ───────────────────────────────
    st.markdown("<div style='margin:0 0 12px'><span style='font-size:13px;font-weight:700;color:#eef0f8;text-transform:uppercase;letter-spacing:.06em'>⚙ Automated Control Test Results</span></div>", unsafe_allow_html=True)
    _ctl_rows = ""
    for _c in _t5_controls:
        _rbg, _rcl = _t5_badge.get(_c["result"], ("#1a1a2e", "#818cf8"))
        _rbadge = f'<span style="background:{_rbg};color:{_rcl};border:1px solid {_rcl}55;border-radius:20px;padding:2px 8px;font-size:11px;font-weight:700">{_c["result"]}</span>'
        _cov_col = "#22d3a5" if _c["coverage"] >= 95 else ("#f97316" if _c["coverage"] >= 85 else "#ef4444")
        _exc_col = "#ef4444" if _c["exceptions"] > 10 else ("#f97316" if _c["exceptions"] > 0 else "#22d3a5")
        _exc_val = f'<span style="color:{_exc_col};font-weight:700">{_c["exceptions"]}</span>' if _c["exceptions"] > 0 else '<span style="color:#22d3a5">—</span>'
        _ctl_rows += f'<tr style="border-bottom:1px solid rgba(255,255,255,.04)"><td style="padding:9px 12px;color:#818cf8;font-size:11px;font-weight:700">{_c["id"]}</td><td style="padding:9px 12px;color:#eef0f8;font-size:12px">{_c["process"]}</td><td style="padding:9px 12px;color:#6b7a99;font-size:11px">{_c["freq"]}</td><td style="padding:9px 12px;color:#4a5568;font-size:11px">{_c["last_run"]}</td><td style="padding:9px 12px;text-align:center"><span style="color:{_cov_col};font-weight:700;font-size:12px">{_c["coverage"]}%</span></td><td style="padding:9px 12px">{_rbadge}</td><td style="padding:9px 12px;text-align:center">{_exc_val}</td></tr>'
    st.markdown(f"""
<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;overflow:hidden;margin-bottom:28px">
<table style="width:100%;border-collapse:collapse;font-family:inherit">
  <thead><tr style="background:rgba(99,102,241,.08);border-bottom:1px solid var(--border-subtle)">
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Control</th>
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Process</th>
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Frequency</th>
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Last Run</th>
    <th style="padding:9px 12px;text-align:center;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Coverage</th>
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Result</th>
    <th style="padding:9px 12px;text-align:center;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Exceptions</th>
  </tr></thead>
  <tbody>{_ctl_rows}</tbody>
</table></div>""", unsafe_allow_html=True)

    # ── Block 2: Exception & Anomaly Feed ────────────────────────────────────
    st.markdown("<div style='margin:0 0 12px'><span style='font-size:13px;font-weight:700;color:#eef0f8;text-transform:uppercase;letter-spacing:.06em'>🔴 Exception &amp; Anomaly Feed</span></div>", unsafe_allow_html=True)
    _exc_rows = ""
    for _e in _t5_exceptions:
        _sc = _t5_st_color.get(_e["status"], "#6b7a99")
        _exc_rows += f'<tr style="border-bottom:1px solid rgba(255,255,255,.04)"><td style="padding:9px 12px;color:#4a5568;font-size:11px;white-space:nowrap">{_e["ts"]}</td><td style="padding:9px 12px;color:#818cf8;font-size:11px;font-weight:700">{_e["ctl"]}</td><td style="padding:9px 12px;color:#f97316;font-size:11px;font-weight:600">{_e["type"]}</td><td style="padding:9px 12px;color:#6b7a99;font-size:11px">{_e["entity"]}</td><td style="padding:9px 12px;color:#eef0f8;font-size:11px">{_e["desc"]}</td><td style="padding:9px 12px;color:#ef4444;font-size:11px;font-weight:700;white-space:nowrap">{_e["impact"]}</td><td style="padding:9px 12px"><span style="color:{_sc};font-size:11px;font-weight:700">{_e["status"]}</span></td></tr>'
    st.markdown(f"""
<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;overflow:hidden;margin-bottom:28px">
<table style="width:100%;border-collapse:collapse;font-family:inherit">
  <thead><tr style="background:rgba(239,68,68,.06);border-bottom:1px solid var(--border-subtle)">
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Timestamp</th>
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Control</th>
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Type</th>
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Entity</th>
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Anomaly Detected</th>
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Impact</th>
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Status</th>
  </tr></thead>
  <tbody>{_exc_rows}</tbody>
</table></div>""", unsafe_allow_html=True)

    # ── Block 3: Control Health Trend (12-week sparklines) ───────────────────
    st.markdown("<div style='margin:0 0 12px'><span style='font-size:13px;font-weight:700;color:#eef0f8;text-transform:uppercase;letter-spacing:.06em'>📈 Control Health — 12-Week Trend</span></div>", unsafe_allow_html=True)
    _wk_labels = "".join([f'<td style="padding:0 2px;text-align:center;font-size:9px;color:#4a5568">W{i+1}</td>' for i in range(12)])
    _health_rows = ""
    for _h in _t5_health:
        _dots = "".join([f'<td style="padding:3px 2px;text-align:center"><div style="width:10px;height:10px;border-radius:2px;background:{_t5_dot.get(_w,"#2d3a4e")};margin:0 auto"></div></td>' for _w in _h["weeks"]])
        _last_w = _h["weeks"][-1]
        _trend_col = _t5_dot.get(_last_w, "#4a5568")
        _trend_lbl = {"P": "Pass", "W": "Warn", "F": "Fail"}.get(_last_w, "—")
        _health_rows += f'<tr style="border-bottom:1px solid rgba(255,255,255,.04)"><td style="padding:8px 12px;color:#6b7a99;font-size:11px;font-weight:600;white-space:nowrap">{_h["id"]}</td><td style="padding:8px 12px;color:#eef0f8;font-size:12px">{_h["name"]}</td>{_dots}<td style="padding:8px 12px;text-align:center"><span style="color:{_trend_col};font-size:11px;font-weight:700">{_trend_lbl}</span></td></tr>'
    st.markdown(f"""
<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;overflow:hidden;margin-bottom:28px">
<table style="width:100%;border-collapse:collapse;font-family:inherit">
  <thead><tr style="background:rgba(99,102,241,.08);border-bottom:1px solid var(--border-subtle)">
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">ID</th>
    <th style="padding:9px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Control</th>
    {_wk_labels}
    <th style="padding:9px 12px;text-align:center;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Latest</th>
  </tr></thead>
  <tbody>{_health_rows}</tbody>
</table>
<div style="padding:8px 12px;display:flex;gap:16px;border-top:1px solid rgba(255,255,255,.04)">
  <span style="font-size:10px;color:#6b7a99">Legend:</span>
  <span style="font-size:10px;color:#22d3a5">■ Pass</span>
  <span style="font-size:10px;color:#f97316">■ Warning</span>
  <span style="font-size:10px;color:#ef4444">■ Fail</span>
</div>
</div>""", unsafe_allow_html=True)

    # ── Block 4: Audit Universe Coverage Matrix ───────────────────────────────
    st.markdown("<div style='margin:0 0 12px'><span style='font-size:13px;font-weight:700;color:#eef0f8;text-transform:uppercase;letter-spacing:.06em'>🗺 Audit Universe Coverage</span></div>", unsafe_allow_html=True)
    _proc_headers = "".join([f'<th style="padding:10px 8px;text-align:center;font-size:10px;color:#6b7a99;font-weight:700;text-transform:uppercase;white-space:nowrap">{_p}</th>' for _p in _t5_processes])
    _matrix_rows = ""
    for _ei, _ent in enumerate(_t5_entities):
        _cells = ""
        for _ci, _code in enumerate(_t5_matrix[_ei]):
            _mbg, _mcl, _mlbl = _t5_matrix_legend[_code]
            _cells += f'<td style="padding:10px 8px;text-align:center"><span style="background:{_mbg};color:{_mcl};border:1px solid {_mcl}55;border-radius:6px;padding:3px 10px;font-size:10px;font-weight:700;white-space:nowrap">{_mlbl}</span></td>'
        _matrix_rows += f'<tr style="border-bottom:1px solid rgba(255,255,255,.04)"><td style="padding:10px 12px;color:#eef0f8;font-size:12px;font-weight:600;white-space:nowrap">{_ent}</td>{_cells}</tr>'
    st.markdown(f"""
<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;overflow:hidden">
<table style="width:100%;border-collapse:collapse;font-family:inherit">
  <thead><tr style="background:rgba(99,102,241,.08);border-bottom:1px solid var(--border-subtle)">
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Entity</th>
    {_proc_headers}
  </tr></thead>
  <tbody>{_matrix_rows}</tbody>
</table>
<div style="padding:8px 12px;display:flex;gap:16px;border-top:1px solid rgba(255,255,255,.04)">
  <span style="font-size:10px;color:#6b7a99">Coverage type:</span>
  <span style="font-size:10px;color:#22d3a5">■ Continuous</span>
  <span style="font-size:10px;color:#818cf8">■ Periodic</span>
  <span style="font-size:10px;color:#f97316">■ Gap identified</span>
  <span style="font-size:10px;color:#ef4444">■ No coverage</span>
</div>
</div>
""", unsafe_allow_html=True)


# TAB 6 — THIRD PARTY & VENDOR 360
# ─────────────────────────────────────────────────────────────────────────────
elif _active == 6:
    _t6_kpis = [
        {"label": "Total Vendors",    "value": "143", "delta": "+4 onboarded Q2",   "color": "#818cf8"},
        {"label": "Critical Vendors", "value": "23",  "delta": "Tier 1 — FINMA reg", "color": "#ef4444"},
        {"label": "Due Reviews",      "value": "11",  "delta": "Next 30 days",       "color": "#f97316"},
        {"label": "SLA Breaches",     "value": "3",   "delta": "↑ from 1 last qtr",  "color": "#ef4444"},
    ]
    _t6_vendors = [
        {"name": "Clearstream Banking", "cat": "Custody",       "score": 91, "kyc": "Approved", "review": "2026-03-15", "sla": "Breach",    "critical": True},
        {"name": "Bloomberg L.P.",      "cat": "Data / Market", "score": 96, "kyc": "Approved", "review": "2026-01-20", "sla": "OK",        "critical": True},
        {"name": "SWIFT SCRL",          "cat": "Messaging",     "score": 89, "kyc": "Approved", "review": "2026-02-10", "sla": "OK",        "critical": True},
        {"name": "Temenos AG",          "cat": "Core Banking",  "score": 84, "kyc": "Approved", "review": "2026-04-01", "sla": "OK",        "critical": True},
        {"name": "AWS (Amazon)",        "cat": "Cloud / Infra", "score": 88, "kyc": "Approved", "review": "2026-03-28", "sla": "OK",        "critical": True},
        {"name": "Refinitiv (LSEG)",    "cat": "Data / KYC",    "score": 77, "kyc": "In Review","review": "2026-05-05", "sla": "Warning",   "critical": False},
        {"name": "Finastra",            "cat": "Software",      "score": 72, "kyc": "Approved", "review": "2026-02-28", "sla": "OK",        "critical": False},
        {"name": "Deloitte SA",         "cat": "Consulting",    "score": 85, "kyc": "Approved", "review": "2026-04-15", "sla": "OK",        "critical": False},
    ]
    _t6_actions = [
        {"id": "ACT-001", "priority": "Critical", "desc": "Escalate SLA breach to Clearstream — uptime 94.1% vs 99.5% contracted", "due": "2026-06-10"},
        {"id": "ACT-002", "priority": "High",     "desc": "Complete Refinitiv annual KYC review — pending legal sign-off",         "due": "2026-06-20"},
        {"id": "ACT-003", "priority": "High",     "desc": "Update exit strategy plan — Clearstream & Temenos (FINMA Art.8b)",      "due": "2026-06-30"},
    ]
    _t6_regs = ["FINMA Circ. 2018/3 — Outsourcing", "MAS TRM Guidelines 2021", "FCA SS2/21 — Outsourcing", "DORA Art. 28–30 — ICT Third Party", "EBA/GL/2019/02 — Outsourcing"]

    _kyc_color = {"Approved": "#22d3a5", "In Review": "#f97316", "Pending": "#ef4444"}

    st.markdown("""
<div style="margin-bottom:24px">
  <div style="font-size:22px;font-weight:800;color:#eef0f8;margin-bottom:4px">🏢 Third Party &amp; Vendor 360</div>
  <div style="font-size:13px;color:#6b7a99">Vendor risk scoring · KYC · Outsourcing oversight</div>
</div>
""", unsafe_allow_html=True)

    # KPI cards
    _t6c = st.columns(4, gap="small")
    for _i, _kpi in enumerate(_t6_kpis):
        _t6c[_i].markdown(f"""
<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;
     padding:18px 20px;text-align:center;box-shadow:var(--shadow-card)">
  <div style="font-size:32px;font-weight:800;color:{_kpi['color']}">{_kpi['value']}</div>
  <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;
       color:#6b7a99;margin:4px 0">{_kpi['label']}</div>
  <div style="font-size:11px;color:#4a5568">{_kpi['delta']}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:28px 0 12px'><span style='font-size:13px;font-weight:700;color:#eef0f8;text-transform:uppercase;letter-spacing:.06em'>🏦 Vendor Scorecard</span></div>", unsafe_allow_html=True)

    # Vendor table
    _v_rows = ""
    for _v in _t6_vendors:
        _s = _v["score"]
        _s_color = "#22d3a5" if _s >= 85 else ("#f97316" if _s >= 70 else "#ef4444")
        _k_color = _kyc_color.get(_v["kyc"], "#6b7a99")
        _sla_color = "#ef4444" if _v["sla"] == "Breach" else ("#f97316" if _v["sla"] == "Warning" else "#22d3a5")
        _crit = '<span style="color:#ef4444;font-weight:700;font-size:11px">● Critical</span>' if _v["critical"] else '<span style="color:#4a5568;font-size:11px">—</span>'
        _v_rows += f'<tr style="border-bottom:1px solid rgba(255,255,255,.04)"><td style="padding:10px 12px;color:#eef0f8;font-size:12px;font-weight:600">{_v["name"]}</td><td style="padding:10px 12px;color:#6b7a99;font-size:11px">{_v["cat"]}</td><td style="padding:10px 12px;text-align:center"><span style="font-size:16px;font-weight:800;color:{_s_color}">{_s}</span></td><td style="padding:10px 12px"><span style="color:{_k_color};font-size:11px;font-weight:700">{_v["kyc"]}</span></td><td style="padding:10px 12px;color:#4a5568;font-size:11px">{_v["review"]}</td><td style="padding:10px 12px"><span style="color:{_sla_color};font-size:11px;font-weight:700">{_v["sla"]}</span></td><td style="padding:10px 12px">{_crit}</td></tr>'

    st.markdown(f"""
<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;overflow:hidden">
<table style="width:100%;border-collapse:collapse;font-family:inherit">
  <thead><tr style="background:rgba(99,102,241,.08);border-bottom:1px solid var(--border-subtle)">
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Vendor</th>
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Category</th>
    <th style="padding:10px 12px;text-align:center;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Score</th>
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">KYC Status</th>
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Last Review</th>
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">SLA</th>
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Tier</th>
  </tr></thead>
  <tbody>{_v_rows}</tbody>
</table></div>""", unsafe_allow_html=True)

    # Critical vendor drill-down
    st.markdown("<div style='margin:28px 0 12px'><span style='font-size:13px;font-weight:700;color:#eef0f8;text-transform:uppercase;letter-spacing:.06em'>🔎 Critical Vendor — Clearstream Banking</span></div>", unsafe_allow_html=True)

    _dcol1, _dcol2 = st.columns([2, 1], gap="medium")
    with _dcol1:
        st.markdown("""
<div style="background:var(--bg-card);border:1px solid rgba(239,68,68,.3);border-radius:12px;padding:20px 24px">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
    <span style="font-size:18px;font-weight:800;color:#eef0f8">Clearstream Banking S.A.</span>
    <span style="background:#3b0e0e;color:#ef4444;border:1px solid #ef444455;border-radius:20px;padding:2px 10px;font-size:11px;font-weight:700">Critical</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:12px">
    <div><span style="color:#6b7a99">Category</span><br><span style="color:#eef0f8;font-weight:600">Custody &amp; Settlement</span></div>
    <div><span style="color:#6b7a99">Risk Score</span><br><span style="color:#f97316;font-weight:800;font-size:18px">91 / 100</span></div>
    <div><span style="color:#6b7a99">KYC Status</span><br><span style="color:#22d3a5;font-weight:600">Approved (2025-09-15)</span></div>
    <div><span style="color:#6b7a99">Contract Value</span><br><span style="color:#eef0f8;font-weight:600">CHF 4.2M / year</span></div>
    <div><span style="color:#6b7a99">SLA Uptime</span><br><span style="color:#ef4444;font-weight:700">94.1% (contracted 99.5%)</span></div>
    <div><span style="color:#6b7a99">Exit Strategy</span><br><span style="color:#f97316;font-weight:600">Draft — in review</span></div>
    <div><span style="color:#6b7a99">Jurisdictions</span><br><span style="color:#eef0f8">CH · LU · SG · HK</span></div>
    <div><span style="color:#6b7a99">Next Review</span><br><span style="color:#818cf8;font-weight:600">2026-09-15</span></div>
  </div>
</div>""", unsafe_allow_html=True)

    with _dcol2:
        _a_rows = ""
        for _ac in _t6_actions:
            _ac_color = "#ef4444" if _ac["priority"] == "Critical" else "#f97316"
            _a_rows += f'<div style="border-left:3px solid {_ac_color};padding:10px 12px;margin-bottom:8px;background:rgba(255,255,255,.03);border-radius:0 8px 8px 0"><div style="font-size:11px;color:{_ac_color};font-weight:700;margin-bottom:4px">{_ac["id"]} · {_ac["priority"]}</div><div style="font-size:11px;color:#eef0f8">{_ac["desc"]}</div><div style="font-size:10px;color:#4a5568;margin-top:4px">Due: {_ac["due"]}</div></div>'
        st.markdown(f'<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;padding:16px"><div style="font-size:12px;font-weight:700;color:#eef0f8;margin-bottom:12px;text-transform:uppercase;letter-spacing:.05em">Open Actions</div>{_a_rows}</div>', unsafe_allow_html=True)

    # Regulatory refs
    st.markdown("<div style='margin:24px 0 10px'><span style='font-size:12px;color:#6b7a99;font-weight:600'>Regulatory references:</span></div>", unsafe_allow_html=True)
    _reg_pills = " ".join([f'<span style="background:rgba(99,102,241,.1);color:#818cf8;border:1px solid rgba(99,102,241,.25);border-radius:20px;padding:3px 12px;font-size:11px;font-weight:600;margin-right:6px">{_r}</span>' for _r in _t6_regs])
    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:6px">{_reg_pills}</div>', unsafe_allow_html=True)


# TAB 7 — KYC / AML COMPLIANCE
# ─────────────────────────────────────────────────────────────────────────────
elif _active == 7:
    _t7_kpis = [
        {"label": "Clients Reviewed", "value": "2,847", "delta": "Q2 2026",           "color": "#818cf8"},
        {"label": "PEP Flagged",      "value": "34",    "delta": "12 high-risk",       "color": "#f97316"},
        {"label": "Sanctions Hits",   "value": "7",     "delta": "3 pending escalation","color": "#ef4444"},
        {"label": "Remediation Open", "value": "18",    "delta": "↓ 5 closed this week","color": "#f97316"},
    ]
    _t7_alerts = [
        {"ref": "CLI-0047", "level": "Critical", "flag": "Sanctions",      "jurisdiction": "CH / FINMA", "status": "Escalated",   "days": 3},
        {"ref": "CLI-0123", "level": "Critical", "flag": "PEP — Tier 1",   "jurisdiction": "SG / MAS",   "status": "Escalated",   "days": 7},
        {"ref": "CLI-0291", "level": "High",     "flag": "Adverse Media",   "jurisdiction": "HK / SFC",   "status": "In Review",   "days": 14},
        {"ref": "CLI-0388", "level": "High",     "flag": "PEP — Tier 2",   "jurisdiction": "UK / FCA",   "status": "In Review",   "days": 21},
        {"ref": "CLI-0512", "level": "High",     "flag": "Sanctions",      "jurisdiction": "EU / DORA",  "status": "Pending",     "days": 5},
        {"ref": "CLI-0601", "level": "Moderate", "flag": "Adverse Media",   "jurisdiction": "Bahamas",    "status": "Assigned",    "days": 30},
    ]
    _t7_kanban = {
        "To Review": [
            {"ref": "CLI-0512", "level": "High",     "flag": "Sanctions — OFAC list",  "since": "2 days"},
            {"ref": "CLI-0644", "level": "Moderate", "flag": "PEP — indirect exposure","since": "5 days"},
            {"ref": "CLI-0701", "level": "High",     "flag": "Adverse Media — press",  "since": "1 day"},
        ],
        "In Progress": [
            {"ref": "CLI-0291", "level": "High",     "flag": "EDD under way — HK",     "since": "14 days"},
            {"ref": "CLI-0388", "level": "High",     "flag": "PEP interview scheduled","since": "21 days"},
            {"ref": "CLI-0123", "level": "Critical", "flag": "MLRO sign-off pending",  "since": "7 days"},
        ],
        "Closed": [
            {"ref": "CLI-0205", "level": "Moderate", "flag": "CDD renewed — cleared",  "since": "3 days ago"},
            {"ref": "CLI-0317", "level": "High",     "flag": "Exited relationship",     "since": "5 days ago"},
            {"ref": "CLI-0482", "level": "Moderate", "flag": "False positive confirmed","since": "8 days ago"},
        ],
    }
    _t7_regs = ["FATF Rec. 10 — CDD", "FINMA AML Circular 2011/1", "MAS Notice 626", "JMLSG Guidance (UK)", "AMLD6 (EU)"]

    _lvl_color = {"Critical": ("#3b0e0e", "#ef4444"), "High": ("#3b1f0a", "#f97316"), "Moderate": ("#1a2e1a", "#22d3a5")}
    _kanban_col_color = {"To Review": "#f97316", "In Progress": "#818cf8", "Closed": "#22d3a5"}

    st.markdown("""
<div style="margin-bottom:24px">
  <div style="font-size:22px;font-weight:800;color:#eef0f8;margin-bottom:4px">🔍 KYC / AML Compliance</div>
  <div style="font-size:13px;color:#6b7a99">Client risk · PEP · Sanctions · Remediation pipeline</div>
</div>
""", unsafe_allow_html=True)

    # KPI cards
    _t7c = st.columns(4, gap="small")
    for _i, _kpi in enumerate(_t7_kpis):
        _t7c[_i].markdown(f"""
<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;
     padding:18px 20px;text-align:center;box-shadow:var(--shadow-card)">
  <div style="font-size:32px;font-weight:800;color:{_kpi['color']}">{_kpi['value']}</div>
  <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;
       color:#6b7a99;margin:4px 0">{_kpi['label']}</div>
  <div style="font-size:11px;color:#4a5568">{_kpi['delta']}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:28px 0 12px'><span style='font-size:13px;font-weight:700;color:#eef0f8;text-transform:uppercase;letter-spacing:.06em'>🚨 PEP / Sanctions Alert Queue</span></div>", unsafe_allow_html=True)

    # Alert table
    _st_color = {"Escalated": "#ef4444", "In Review": "#818cf8", "Pending": "#f97316", "Assigned": "#22d3a5"}
    _al_rows = ""
    for _al in _t7_alerts:
        _bg, _cl = _lvl_color.get(_al["level"], ("#1a1a2e", "#818cf8"))
        _badge = f'<span style="background:{_bg};color:{_cl};border:1px solid {_cl}55;border-radius:20px;padding:2px 8px;font-size:11px;font-weight:700">{_al["level"]}</span>'
        _sc = _st_color.get(_al["status"], "#6b7a99")
        _al_rows += f'<tr style="border-bottom:1px solid rgba(255,255,255,.04)"><td style="padding:10px 12px;color:#818cf8;font-size:12px;font-weight:600">{_al["ref"]}</td><td style="padding:10px 12px">{_badge}</td><td style="padding:10px 12px;color:#eef0f8;font-size:12px">{_al["flag"]}</td><td style="padding:10px 12px;color:#6b7a99;font-size:11px">{_al["jurisdiction"]}</td><td style="padding:10px 12px"><span style="color:{_sc};font-size:11px;font-weight:700">{_al["status"]}</span></td><td style="padding:10px 12px;color:#4a5568;font-size:11px">{_al["days"]}d open</td></tr>'

    st.markdown(f"""
<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;overflow:hidden">
<table style="width:100%;border-collapse:collapse;font-family:inherit">
  <thead><tr style="background:rgba(99,102,241,.08);border-bottom:1px solid var(--border-subtle)">
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Client Ref</th>
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Level</th>
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Flag Type</th>
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Jurisdiction</th>
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Status</th>
    <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7a99;font-weight:700;text-transform:uppercase">Age</th>
  </tr></thead>
  <tbody>{_al_rows}</tbody>
</table></div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:28px 0 12px'><span style='font-size:13px;font-weight:700;color:#eef0f8;text-transform:uppercase;letter-spacing:.06em'>🔄 Remediation Pipeline</span></div>", unsafe_allow_html=True)

    # Kanban
    _k_cols = st.columns(3, gap="medium")
    for _ki, (_col_name, _cases) in enumerate(_t7_kanban.items()):
        _hdr_color = _kanban_col_color[_col_name]
        _cards_html = ""
        for _case in _cases:
            _cbg, _ccl = _lvl_color.get(_case["level"], ("#1a1a2e", "#818cf8"))
            _cards_html += f'<div style="border-left:3px solid {_ccl};background:rgba(255,255,255,.03);border-radius:0 8px 8px 0;padding:10px 12px;margin-bottom:8px"><div style="font-size:11px;color:#818cf8;font-weight:700;margin-bottom:4px">{_case["ref"]}</div><div style="font-size:11px;color:#eef0f8">{_case["flag"]}</div><div style="font-size:10px;color:#4a5568;margin-top:4px">{_case["since"]}</div></div>'
        _k_cols[_ki].markdown(f"""
<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;padding:16px">
  <div style="font-size:12px;font-weight:700;color:{_hdr_color};margin-bottom:12px;text-transform:uppercase;letter-spacing:.06em;border-bottom:1px solid rgba(255,255,255,.06);padding-bottom:8px">{_col_name}</div>
  {_cards_html}
</div>""", unsafe_allow_html=True)

    # CDD coverage
    st.markdown("<div style='margin:28px 0 12px'><span style='font-size:13px;font-weight:700;color:#eef0f8;text-transform:uppercase;letter-spacing:.06em'>📋 CDD / EDD Coverage</span></div>", unsafe_allow_html=True)
    _cdd_data = [
        ("Standard CDD",   94, "#22d3a5"),
        ("Enhanced EDD",   81, "#818cf8"),
        ("PEP Review",     76, "#f97316"),
        ("Sanctions Screen",97,"#22d3a5"),
    ]
    _cdd_cols = st.columns(4, gap="small")
    for _ci, (_lbl, _pct, _col) in enumerate(_cdd_data):
        _cdd_cols[_ci].markdown(f"""
<div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;padding:16px 20px;text-align:center">
  <div style="position:relative;width:72px;height:72px;margin:0 auto 10px">
    <svg viewBox="0 0 36 36" style="width:72px;height:72px;transform:rotate(-90deg)">
      <circle cx="18" cy="18" r="15.9" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="3"/>
      <circle cx="18" cy="18" r="15.9" fill="none" stroke="{_col}" stroke-width="3"
        stroke-dasharray="{_pct} {100 - _pct}" stroke-linecap="round"/>
    </svg>
    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
         font-size:14px;font-weight:800;color:{_col}">{_pct}%</div>
  </div>
  <div style="font-size:11px;font-weight:700;color:#eef0f8;text-transform:uppercase;letter-spacing:.05em">{_lbl}</div>
</div>""", unsafe_allow_html=True)

    # Regulatory footer
    st.markdown("<div style='margin:24px 0 10px'><span style='font-size:12px;color:#6b7a99;font-weight:600'>Regulatory references:</span></div>", unsafe_allow_html=True)
    _t7_reg_pills = " ".join([f'<span style="background:rgba(99,102,241,.1);color:#818cf8;border:1px solid rgba(99,102,241,.25);border-radius:20px;padding:3px 12px;font-size:11px;font-weight:600;margin-right:6px">{_r}</span>' for _r in _t7_regs])
    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:6px">{_t7_reg_pills}</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p class="footer">AuditIQ &middot; Internal Audit System &middot; Private Banking &middot; CH &middot; SG &middot; HK &middot; Bahamas &middot; EU &middot; UK</p>',
    unsafe_allow_html=True,
)