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
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
  .stApp { background-color: #080b12; color: #dde3f5; }
  .main .block-container { padding: 2rem 3rem 4rem; max-width: 1060px; }

  .stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    gap: 0;
  }
  .stTabs [data-baseweb="tab"] {
    font-size: 13.5px !important;
    font-weight: 500 !important;
    color: #5a6488 !important;
    padding: 10px 22px !important;
    border-bottom: 2px solid transparent !important;
  }
  .stTabs [aria-selected="true"] {
    color: #a0b4f8 !important;
    border-bottom: 2px solid #4f7ef8 !important;
    background: transparent !important;
  }

  .stTextInput input, .stTextArea textarea {
    background-color: #10141f !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    color: #dde3f5 !important;
    font-size: 13.5px !important;
  }
  .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(79,126,248,0.5) !important;
    box-shadow: 0 0 0 3px rgba(79,126,248,0.08) !important;
  }
  label[data-testid="stWidgetLabel"] p { font-size: 13px !important; color: #8392bb !important; font-weight: 500; }

  div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #2d54d4 0%, #4f7ef8 100%);
    border: none; border-radius: 9px; color: #fff;
    font-size: 13.5px; font-weight: 600; padding: 10px 28px;
    transition: opacity 0.15s;
  }
  div[data-testid="stButton"] > button[kind="primary"]:hover { opacity: 0.88; }
  div[data-testid="stButton"] > button[kind="primary"]:disabled {
    background: #1a1f32 !important; color: #3a4566 !important;
  }
  div[data-testid="stButton"] > button:not([kind="primary"]) {
    background: rgba(79,126,248,0.1); color: #7fa8fb;
    border: 1px solid rgba(79,126,248,0.25); border-radius: 8px;
    font-size: 13px; font-weight: 500;
  }

  div[data-testid="stDownloadButton"] button {
    background: rgba(79,126,248,0.1); color: #7fa8fb;
    border: 1px solid rgba(79,126,248,0.25); border-radius: 8px;
    font-size: 13px; font-weight: 500;
  }
  div[data-testid="stDownloadButton"] button:hover { background: rgba(79,126,248,0.18); }

  div[data-testid="stFileUploader"] {
    border: 1px dashed rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; background: #10141f !important;
  }

  div[data-testid="stAlert"] { border-radius: 9px !important; font-size: 13px !important; }

  hr { border: none; border-top: 1px solid rgba(255,255,255,0.05) !important; margin: 1.8rem 0; }

  .output-box {
    background: #0f121e; border: 1px solid rgba(255,255,255,0.07); border-radius: 10px;
    padding: 20px 24px; font-size: 13px; line-height: 1.9; white-space: pre-wrap;
    color: #c8d0e8; max-height: 560px; overflow-y: auto;
  }

  .section-title {
    font-size: 15px; font-weight: 600; color: #dde3f5;
    margin: 1.8rem 0 1rem; letter-spacing: -0.2px;
  }
  .ctx-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(34,211,165,0.07); border: 1px solid rgba(34,211,165,0.18);
    color: #22d3a5; border-radius: 8px; padding: 6px 14px;
    font-size: 12.5px; font-weight: 500; margin-bottom: 1.4rem;
  }
  .data-table {
    width: 100%; border-collapse: collapse; font-size: 12.5px; margin-bottom: 0.5rem;
  }
  .data-table th {
    padding: 9px 13px; text-align: left; font-weight: 600;
    font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.5px;
  }
  .data-table td { padding: 10px 13px; vertical-align: top; line-height: 1.6; }
  .data-table tr:not(:last-child) td { border-bottom: 1px solid rgba(255,255,255,0.04); }

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

  .footer { font-size: 11px; color: #262e47; text-align: center; margin-top: 2.5rem; letter-spacing: 0.3px; }

  section[data-testid="stSidebar"] { display: none !important; }
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

JURISDICTIONS = ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU / DORA", "UK / FCA+PRA"]
OUTPUT_DIR = str(_HERE / "outputs")
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# ── Session state ─────────────────────────────────────────────────────────────
_SS = [
    # Dashboard
    "dash_cves", "dash_regs", "dash_audit_recs", "dash_updated",
    # Tab 1
    "t1_risks", "t1_regs", "t1_docx", "t1_topic", "t1_jurs", "t1_pub_recs",
    # Tab 2
    "t2_rationale", "t2_background", "t2_org_plan", "t2_tests", "t2_analytics",
    "t2_pptx", "t2_xlsx",
    # Tab 3
    "t3_report",
]
for _k in _SS:
    if _k not in st.session_state:
        st.session_state[_k] = None

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
    """Run a message with web_search tool. Handles the tool-use loop."""
    messages = [{"role": "user", "content": prompt}]
    texts = []
    ws_tool = [{"type": "web_search_20250305", "name": "web_search"}]
    for _ in range(8):  # max iterations
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
    # Try to extract JSON array from mixed text
    try:
        return json.loads(t)
    except Exception:
        pass
    # Find first [ ... ] block
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
        src_html = f'<a href="{link}" target="_blank" style="color:#7fa8fb;font-size:11px">{link[:40]}…</a>' if link.startswith("http") else f'<span style="color:#424d72;font-size:11.5px">{link}</span>'
        rows += (
            f'<tr>'
            f'<td style="padding:9px 13px;color:#dde3f5;font-weight:600;vertical-align:top;white-space:nowrap;border-bottom:1px solid rgba(255,255,255,0.04)">{c.get("cve_id","")}</td>'
            f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;white-space:nowrap;border-bottom:1px solid rgba(255,255,255,0.04)">{c.get("date","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{badge}</td>'
            f'<td style="padding:9px 13px;color:#dde3f5;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{c.get("system","")}</td>'
            f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{c.get("description","")}</td>'
            f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{c.get("action","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{src_html}</td>'
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
        title_html = (f'<a href="{link}" target="_blank" style="color:#dde3f5;text-decoration:underline;text-underline-offset:2px">{r.get("title","")}</a>'
                      if link.startswith("http") else f'<span style="color:#dde3f5">{r.get("title","")}</span>')
        rows += (
            f'<tr>'
            f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;white-space:nowrap;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("date","")}</td>'
            f'<td style="padding:9px 13px;color:#7fa8fb;font-weight:500;vertical-align:top;white-space:nowrap;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("authority","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{type_badge}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{title_html}{open_badge}</td>'
            f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("key_impact","")}</td>'
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
            f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;white-space:nowrap;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("date","")}</td>'
            f'<td style="padding:9px 13px;color:#7fa8fb;font-weight:500;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("source","")}</td>'
            f'<td style="padding:9px 13px;color:#dde3f5;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("theme","")}</td>'
            f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("recommendation","")}</td>'
            f'<td style="padding:9px 13px;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{badge}</td>'
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
            f'<td style="padding:9px 13px;color:#7fa8fb;font-weight:500;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("source","")}</td>'
            f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;text-align:center;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("year","")}</td>'
            f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("recommendation","")}</td>'
            f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("applicability","")}</td>'
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
            f'<td style="padding:10px 13px;color:#dde3f5;font-weight:500;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("name","")}</td>'
            f'<td style="padding:10px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("description","")}</td>'
            f'<td style="padding:10px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("impact","")}</td>'
            f'<td style="padding:10px 13px;color:#8392bb;vertical-align:top;text-align:center;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("likelihood","")}</td>'
            f'<td style="padding:10px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("control","")}</td>'
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
        f'<td style="padding:10px 13px;color:#7fa8fb;font-weight:500;vertical-align:top;white-space:nowrap;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("jurisdiction","")}</td>'
        f'<td style="padding:10px 13px;color:#dde3f5;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("text","")}</td>'
        f'<td style="padding:10px 13px;color:#8392bb;vertical-align:top;font-size:11.5px;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("reference","")}</td>'
        f'<td style="padding:10px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("requirement","")}</td>'
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
        f'<td style="padding:9px 10px;color:#7fa8fb;font-weight:600;text-align:center;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{t.get("num","")}</td>'
        f'<td style="padding:9px 10px;color:#dde3f5;font-weight:500;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{t.get("objective","")}</td>'
        f'<td style="padding:9px 10px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{t.get("procedure","")}</td>'
        f'<td style="padding:9px 10px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{t.get("population","")}</td>'
        f'<td style="padding:9px 10px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{t.get("sample_size","")}</td>'
        f'<td style="padding:9px 10px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{t.get("failure_criteria","")}</td>'
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
        f'<td style="padding:9px 13px;color:#dde3f5;font-weight:500;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{s.get("scenario","")}</td>'
        f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{s.get("objective","")}</td>'
        f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{s.get("data_source","")}</td>'
        f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{s.get("analysis_type","")}</td>'
        f'<td style="padding:9px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{s.get("anomaly","")}</td>'
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


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:14px;padding:1.2rem 0 1.8rem">
  <span style="font-size:28px">🏦</span>
  <div>
    <div style="font-size:20px;font-weight:700;color:#e8edf8;letter-spacing:-0.4px">AuditIQ</div>
    <div style="font-size:11.5px;color:#424d72;text-transform:uppercase;letter-spacing:1px;margin-top:2px">
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
    hcol1, hcol2 = st.columns([5, 1])
    with hcol1:
        st.markdown('<p style="color:#5a6488;font-size:13.5px;margin:0 0 0.4rem">Live intelligence feed: CVEs, regulatory updates, and public audit recommendations.</p>', unsafe_allow_html=True)
        if st.session_state.dash_updated:
            st.markdown(f'<p style="color:#2d3655;font-size:12px;margin:0">Last updated: {st.session_state.dash_updated}</p>', unsafe_allow_html=True)
    with hcol2:
        refresh = st.button("Refresh Dashboard", key="dash_refresh")

    st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)

    run_dash = refresh or (
        st.session_state.dash_cves is None and
        st.session_state.dash_regs is None and
        st.session_state.dash_audit_recs is None
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

                # A) CVEs
                cves_raw = _web_search_call(c,
                    "Search NVD (nvd.nist.gov), CISA KEV (cisa.gov/known-exploited-vulnerabilities), "
                    "and vendor security advisories for CVEs published in the last 3 months targeting financial sector systems: "
                    "core banking platforms, SWIFT/messaging, trading systems, IAM/PAM, payment gateways, ATM software, banking APIs. "
                    "Include only High and Critical severity CVEs. "
                    "Return a JSON array of 8-12 real CVEs found:\n"
                    '[{"cve_id":"CVE-XXXX-XXXXX","date":"YYYY-MM-DD","severity":"Critical|High",'
                    '"system":"<affected system>","description":"<1-2 sentences>","action":"<recommended action>","source":"<URL or NVD/CISA/vendor>"}]',
                    system=sys_dash, max_tokens=5000)

                # B) Regulatory updates
                regs_raw = _web_search_call(c,
                    "Search the official websites and press releases of FINMA, MAS, SFC, HKMA, EBA, FCA, PRA, BCBS, FSB, FATF "
                    "for regulatory publications from the last 6 months AND upcoming consultations/rules open or expected in the next 12 months. "
                    "Focus on banking, AML, capital requirements, operational resilience, digital assets, wealth management. "
                    "Return a JSON array of 12-16 real entries found:\n"
                    '[{"date":"YYYY-MM-DD","authority":"<regulator>","type":"Consultation|Final Rule|Circular|Guidance",'
                    '"title":"<full publication title>","key_impact":"<1-2 sentences on impact for private banks>",'
                    '"link":"<URL if found, else empty>","open_until":"<consultation deadline YYYY-MM-DD if applicable, else null>"}]',
                    system=sys_dash, max_tokens=6000)

                # C) Public audit recommendations
                recs_raw = _web_search_call(c,
                    "Search for public audit recommendations and reports published in the last 12 months targeting banks and wealth managers, from: "
                    "Basel Committee on Banking Supervision, IMF Financial Sector Assessment Programs (FSAPs), "
                    "Big 4 thought leadership reports (publicly available), IIA Global, FINMA, MAS, FCA, EBA supervisory reports. "
                    "Focus on private banking, wealth management, HNWI, cross-border. "
                    "Return a JSON array of 8-12 real entries:\n"
                    '[{"date":"YYYY-MM-DD","source":"<issuing body>","theme":"<topic area>",'
                    '"recommendation":"<recommendation summary, 2-3 sentences>","priority":"High|Medium"}]',
                    system=sys_dash, max_tokens=5000)

                st.session_state.dash_cves      = _parse_json(cves_raw) or []
                st.session_state.dash_regs      = _parse_json(regs_raw) or []
                st.session_state.dash_audit_recs = _parse_json(recs_raw) or []
                st.session_state.dash_updated   = datetime.now().strftime("%d %b %Y, %H:%M UTC")

            except Exception:
                st.error("An error occurred while fetching intelligence data. Please try again.")

    # Display
    if st.session_state.dash_cves is not None:
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
        _cve_table(st.session_state.dash_cves)

        # B) Regulatory updates
        st.markdown("---")
        n_reg = len(st.session_state.dash_regs or [])
        all_types = sorted({r.get("type","") for r in (st.session_state.dash_regs or []) if r.get("type")})
        st.markdown(
            f'<div class="section-title">B. Regulatory Updates'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{n_reg} publications · FINMA · MAS · SFC · HKMA · EBA · FCA · PRA · BCBS · FSB · FATF</span></div>',
            unsafe_allow_html=True,
        )
        if all_types:
            selected_types = st.multiselect(
                "Filter by type", options=all_types, default=all_types,
                key="dash_type_filter", label_visibility="collapsed"
            )
        else:
            selected_types = []
        _reg_updates_table(st.session_state.dash_regs, selected_types if selected_types else None)

        # C) Audit recommendations
        st.markdown("---")
        n_rec = len(st.session_state.dash_audit_recs or [])
        st.markdown(
            f'<div class="section-title">C. Latest Public Audit Recommendations — Banking'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{n_rec} entries · last 12 months</span></div>',
            unsafe_allow_html=True,
        )
        _audit_recs_table(st.session_state.dash_audit_recs)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — RISK ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<p style="color:#5a6488;font-size:13.5px;margin:0 0 1.8rem">Risk mapping, applicable regulations, and public audit recommendations by topic.</p>', unsafe_allow_html=True)

    audit_topic = st.text_input("Audit Topic", placeholder="e.g. AML/KYC, Credit Risk, Cybersecurity, Operational Risk…", key="t1_topic_in")
    jurisdictions = st.multiselect("Jurisdictions", options=JURISDICTIONS, default=JURISDICTIONS[:4], key="t1_jurs_in")

    st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

    if st.button("Analyze", type="primary", disabled=_disabled or not audit_topic, key="t1_run"):
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

                # D) Public audit recommendations (web search)
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

                # Generate .docx export via agent
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

    # Results
    if st.session_state.t1_risks or st.session_state.t1_regs:
        topic_lbl = st.session_state.t1_topic or "audit"
        st.markdown("---")

        st.markdown('<div class="section-title">A. Risk Mapping</div>', unsafe_allow_html=True)
        _risk_table(st.session_state.t1_risks)

        st.markdown("---")
        st.markdown('<div class="section-title">B. Applicable Regulations</div>', unsafe_allow_html=True)
        _reg_table(st.session_state.t1_regs)

        st.markdown("---")
        n_pub = len(st.session_state.t1_pub_recs or [])
        st.markdown(
            f'<div class="section-title">C. Public Audit Recommendations — {topic_lbl}'
            f'<span style="font-size:12px;font-weight:400;color:#5a6488;margin-left:10px">{n_pub} entries found</span></div>',
            unsafe_allow_html=True,
        )
        _pub_recs_table(st.session_state.t1_pub_recs)

        if st.session_state.t1_docx:
            st.markdown("---")
            st.download_button(
                "⬇  Download Full Analysis (.docx)",
                data=st.session_state.t1_docx,
                file_name=f"Risk_Analysis_{topic_lbl.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — AUDIT PLAN
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<p style="color:#5a6488;font-size:13.5px;margin:0 0 1.4rem">Structured audit planning, test programme, and data analytics scenarios.</p>', unsafe_allow_html=True)

    if st.session_state.t1_topic:
        st.markdown(f'<div class="ctx-pill">✓ Topic: {st.session_state.t1_topic}</div>', unsafe_allow_html=True)

    topic2 = st.text_input("Audit Topic",
        value=st.session_state.t1_topic or "",
        placeholder="e.g. AML/KYC, Credit Risk, Cybersecurity…", key="t2_topic_in")

    scope = st.text_area("Audit Scope",
        placeholder="e.g. All group entities in CH, SG and HK. Focus on client onboarding and transaction monitoring.",
        height=80, key="t2_scope_in")

    uploads2 = st.file_uploader(
        "Supporting documents (optional — PDF, Word, Excel, TXT)",
        type=["pdf", "docx", "xlsx", "txt"], accept_multiple_files=True, key="t2_upload")

    st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

    if st.button("Generate Plan", type="primary", disabled=_disabled or not topic2, key="t2_run"):
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

    # Results
    if st.session_state.t2_rationale:
        topic2_lbl = st.session_state.t1_topic or topic2 or "audit"
        st.markdown("---")

        st.markdown('<div class="section-title">1. Rationale</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-box">{st.session_state.t2_rationale}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-title">2. Background Information</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-box">{st.session_state.t2_background}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-title">3. Audit Plan</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-box">{st.session_state.t2_org_plan}</div>', unsafe_allow_html=True)

        st.markdown("---")
        n_tests = len(st.session_state.t2_tests or [])
        st.markdown(f'<div class="section-title">4. Test List — {n_tests} procedures</div>', unsafe_allow_html=True)
        _tests_table(st.session_state.t2_tests)

        st.markdown("---")
        n_analytics = len(st.session_state.t2_analytics or [])
        st.markdown(f'<div class="section-title">5. Data Analytics Scenarios — {n_analytics} scenarios</div>', unsafe_allow_html=True)
        _analytics_table(st.session_state.t2_analytics)

        pptx = st.session_state.t2_pptx
        xlsx = st.session_state.t2_xlsx
        if pptx or xlsx:
            st.markdown("---")
            ca, cb = st.columns(2)
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


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — AUDIT REPORT
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<p style="color:#5a6488;font-size:13.5px;margin:0 0 1.4rem">Formal IIA-standard audit report in English.</p>', unsafe_allow_html=True)

    ctx_parts = []
    if st.session_state.t1_topic:
        ctx_parts.append(f"✓ Topic: {st.session_state.t1_topic}")
    if st.session_state.t2_org_plan:
        ctx_parts.append("✓ Audit plan available")
    if ctx_parts:
        st.markdown(f'<div class="ctx-pill">{" &nbsp;·&nbsp; ".join(ctx_parts)}</div>', unsafe_allow_html=True)

    default_name = f"Internal Audit — {st.session_state.t1_topic} — 2025" if st.session_state.t1_topic else ""
    audit_name = st.text_input("Report Title",
        value=default_name,
        placeholder="e.g. Internal Audit — AML/KYC — Private Banking Group — 2025", key="t3_name_in")

    observations = st.text_area("Issues Log",
        placeholder="e.g.\n1. Transaction monitoring does not cover transfers below CHF 10,000.\n2. Incomplete KYC files for 12 out of 50 clients tested.\n3. No PEP screening procedure in place at the Singapore entity.",
        height=200, key="t3_obs_in")

    uploads3 = st.file_uploader("Working papers (optional — PDF, Word, Excel, TXT)",
        type=["pdf", "docx", "xlsx", "txt"], accept_multiple_files=True, key="t3_upload")

    st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

    if st.button("Generate Report", type="primary",
                 disabled=_disabled or not audit_name or not observations, key="t3_run"):
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

    # Results
    if st.session_state.t3_report:
        res  = st.session_state.t3_report
        name = res.get("name", "report")
        st.markdown("---")

        st.markdown('<div class="section-title">Audit Report</div>', unsafe_allow_html=True)
        text = res.get("text", "")
        if text:
            st.markdown(f'<div class="output-box">{text}</div>', unsafe_allow_html=True)
        else:
            st.info("Report content is available in the export file.")

        docx = res.get("docx_bytes")
        if docx:
            st.markdown("---")
            st.download_button(
                "⬇  Download Report (.docx)",
                data=docx,
                file_name=f"Audit_Report_{name.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        st.markdown("---")
        st.markdown('<div class="section-title">Targeted Revision</div>', unsafe_allow_html=True)
        followup = st.text_area("Revision instructions", label_visibility="collapsed", height=80,
            placeholder="e.g. Strengthen recommendation 3. Add a 30-day deadline for the KYC finding.",
            key="t3_rev_in")

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
