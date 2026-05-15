"""
AuditIQ — Interface Streamlit 3 onglets
Démarrage : streamlit run app.py (depuis audit_system/)
"""

import sys
import os
import json
import tempfile
from pathlib import Path
from datetime import date

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
  .main .block-container { padding: 2rem 3rem 4rem; max-width: 980px; }

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

  .footer { font-size: 11px; color: #262e47; text-align: center; margin-top: 2.5rem; letter-spacing: 0.3px; }

  section[data-testid="stSidebar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Clé d'accès (backend uniquement) ─────────────────────────────────────────
try:
    _api_key = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    _api_key = os.environ.get("ANTHROPIC_API_KEY", "")

if _api_key:
    os.environ["ANTHROPIC_API_KEY"] = _api_key

# ── Imports modules ───────────────────────────────────────────────────────────
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
    "t1_risks", "t1_regs", "t1_docx", "t1_topic", "t1_entity", "t1_jurs",
    "t2_background", "t2_plan", "t2_tests", "t2_pptx", "t2_xlsx",
    "t3_report",
]
for _k in _SS:
    if _k not in st.session_state:
        st.session_state[_k] = None

_disabled = not _api_key or not _READY

# ── Fonctions utilitaires ─────────────────────────────────────────────────────

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


# ── Composants d'affichage ────────────────────────────────────────────────────

_LEVEL_STYLE = {
    "Critique": ("#ef4444", "rgba(239,68,68,0.10)", "rgba(239,68,68,0.28)"),
    "Élevé":    ("#f97316", "rgba(249,115,22,0.10)", "rgba(249,115,22,0.28)"),
    "Modéré":   ("#eab308", "rgba(234,179,8,0.08)",  "rgba(234,179,8,0.24)"),
}


def _risk_table(risks):
    if not risks:
        return
    for level in ["Critique", "Élevé", "Modéré"]:
        bucket = [r for r in risks if r.get("level") == level]
        if not bucket:
            continue
        col, bg, border = _LEVEL_STYLE.get(level, ("#6b7280", "rgba(107,114,128,0.08)", "rgba(107,114,128,0.2)"))
        rows = "".join(
            f'<tr>'
            f'<td style="padding:10px 13px;color:#dde3f5;font-weight:500;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("name","")}</td>'
            f'<td style="padding:10px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("description","")}</td>'
            f'<td style="padding:10px 13px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("impact","")}</td>'
            f'<td style="padding:10px 13px;color:#8392bb;vertical-align:top;text-align:center;border-bottom:1px solid rgba(255,255,255,0.04)">{r.get("probability","")}</td>'
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
            <th style="color:{col};width:18%">Risque</th>
            <th style="color:#6b7599;width:26%">Description</th>
            <th style="color:#6b7599;width:20%">Impact</th>
            <th style="color:#6b7599;width:12%;text-align:center">Probabilité</th>
            <th style="color:#6b7599;width:24%">Contrôle attendu</th>
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
        <th style="color:#7fa8fb;width:15%">Juridiction</th>
        <th style="color:#7fa8fb;width:22%">Texte</th>
        <th style="color:#7fa8fb;width:16%">Référence</th>
        <th style="color:#7fa8fb;width:47%">Exigence clé</th>
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
        f'<td style="padding:9px 10px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{t.get("sample","")}</td>'
        f'<td style="padding:9px 10px;color:#8392bb;vertical-align:top;border-bottom:1px solid rgba(255,255,255,0.04)">{t.get("failure_criterion","")}</td>'
        f'</tr>'
        for t in tests
    )
    st.markdown(f"""
    <table class="data-table" style="font-size:12px">
      <thead><tr style="background:rgba(79,126,248,0.08);border-bottom:1px solid rgba(79,126,248,0.2)">
        <th style="color:#7fa8fb;width:4%;text-align:center">N°</th>
        <th style="color:#7fa8fb;width:16%">Objectif</th>
        <th style="color:#7fa8fb;width:27%">Procédure</th>
        <th style="color:#7fa8fb;width:15%">Population</th>
        <th style="color:#7fa8fb;width:12%">Échantillon</th>
        <th style="color:#7fa8fb;width:26%">Critère de défaillance</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


# ── En-tête ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:14px;padding:1.2rem 0 1.8rem">
  <span style="font-size:28px">🏦</span>
  <div>
    <div style="font-size:20px;font-weight:700;color:#e8edf8;letter-spacing:-0.4px">AuditIQ</div>
    <div style="font-size:11.5px;color:#424d72;text-transform:uppercase;letter-spacing:1px;margin-top:2px">
      Système d'audit — Banque Privée · Multi-juridictions
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if not _api_key:
    st.error("Accès non configuré. Contactez l'administrateur.")
    st.stop()
if not _READY:
    st.error(f"Modules indisponibles : {_ERR}")
    st.stop()

# ═════════════════════════════════════════════════════════════════════════════
# ONGLETS
# ═════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["🔍  Analyse & Risques", "📋  Plan d'audit", "📄  Rapport final"])


# ─────────────────────────────────────────────────────────────────────────────
# ONGLET 1 — ANALYSE & RISQUES
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<p style="color:#5a6488;font-size:13.5px;margin:0 0 1.8rem">Cartographie des risques et réglementations applicables par juridiction.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        audit_topic = st.text_input("Sujet d'audit", placeholder="Ex : AML/KYC, Risque de crédit, Cybersécurité…", key="t1_topic_in")
    with c2:
        entity = st.text_input("Entité auditée", placeholder="Ex : Banque Privée XYZ — Groupe", key="t1_entity_in")

    jurisdictions = st.multiselect("Juridictions", options=JURISDICTIONS, default=JURISDICTIONS[:4], key="t1_jurs_in")

    st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

    if st.button("Analyser", type="primary", disabled=_disabled or not audit_topic, key="t1_run"):
        with st.spinner("Analyse en cours…"):
            try:
                c = _client()
                jur_str = ", ".join(jurisdictions) if jurisdictions else "toutes juridictions"
                entity_str = entity or "Swiss private bank and asset manager (HNWI, wealth management, cross-border)"

                risks_raw = _call(c, f"""Audit topic: {audit_topic}
Entity: {entity_str}
Jurisdictions: {jur_str}

Identify 10-12 key risks for this audit topic across 3 severity levels.
Respond ONLY with a valid JSON array — no markdown, no preamble:
[{{"level":"Critique|Élevé|Modéré","name":"<5-8 words>","description":"<2-3 sentences>","impact":"<1-2 sentences, quantified where possible>","probability":"Élevée|Moyenne|Faible","control":"<1-2 sentences on expected control mechanism>"}}]""",
                    max_tokens=5000)

                regs_raw = _call(c, f"""Audit topic: {audit_topic}
Jurisdictions: {jur_str}
Entity: Swiss private bank / wealth manager (HNWI, gestion de fortune, cross-border)

List applicable regulations, specific to private banking.
Respond ONLY with a valid JSON array — 12-18 entries, no markdown:
[{{"jurisdiction":"<e.g. CH / FINMA>","text":"<law or regulation name>","reference":"<specific article/circular>","requirement":"<key requirement in 1-2 sentences>"}}]""",
                    max_tokens=5000)

                risks = _parse_json(risks_raw)
                regs  = _parse_json(regs_raw)

                st.session_state.t1_risks  = risks
                st.session_state.t1_regs   = regs
                st.session_state.t1_topic  = audit_topic
                st.session_state.t1_entity = entity
                st.session_state.t1_jurs   = jurisdictions

                # Export .docx via agent
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
                        f"Entity: {entity_str}\n"
                        f"Jurisdictions: {jur_str}\n\n"
                        f"Cover: identified risks, applicable regulations, cross-jurisdictional analysis. "
                        f"Then call save_regulatory_framework to export."
                    )}]}], _h1)

                if "docx_path" in extra and Path(extra["docx_path"]).exists():
                    st.session_state.t1_docx = Path(extra["docx_path"]).read_bytes()

            except Exception:
                st.error("Une erreur est survenue. Veuillez réessayer.")

    # Résultats
    if st.session_state.t1_risks or st.session_state.t1_regs:
        topic_lbl = st.session_state.t1_topic or "audit"
        st.markdown("---")

        st.markdown('<div class="section-title">Cartographie des risques</div>', unsafe_allow_html=True)
        _risk_table(st.session_state.t1_risks)

        st.markdown("---")
        st.markdown('<div class="section-title">Réglementations applicables</div>', unsafe_allow_html=True)
        _reg_table(st.session_state.t1_regs)

        if st.session_state.t1_docx:
            st.markdown("---")
            st.download_button(
                "⬇  Télécharger l'analyse complète (.docx)",
                data=st.session_state.t1_docx,
                file_name=f"Analyse_Risques_{topic_lbl.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )


# ─────────────────────────────────────────────────────────────────────────────
# ONGLET 2 — PLAN D'AUDIT
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<p style="color:#5a6488;font-size:13.5px;margin:0 0 1.4rem">Planification structurée et programme de travail détaillé.</p>', unsafe_allow_html=True)

    if st.session_state.t1_topic:
        st.markdown(f'<div class="ctx-pill">✓ Sujet : {st.session_state.t1_topic}</div>', unsafe_allow_html=True)

    topic2 = st.text_input("Sujet d'audit",
        value=st.session_state.t1_topic or "",
        placeholder="Ex : AML/KYC, Risque de crédit…", key="t2_topic_in")

    scope = st.text_area("Périmètre de l'audit",
        placeholder="Ex : Toutes entités du groupe en CH, SG et HK. Focus onboarding et transaction monitoring.",
        height=80, key="t2_scope_in")

    c1, c2 = st.columns([2, 2])
    with c1:
        risk_appetite = st.select_slider("Appétit au risque",
            options=["Faible", "Modéré", "Élevé"], value="Modéré", key="t2_ra_in")
    with c2:
        cd1, cd2 = st.columns(2)
        with cd1:
            date_start = st.date_input("Début de mission", value=date.today(), key="t2_d1_in")
        with cd2:
            d2_default = date(date.today().year, min(date.today().month + 3, 12), date.today().day)
            date_end = st.date_input("Fin de mission", value=d2_default, key="t2_d2_in")

    st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

    if st.button("Générer le plan", type="primary", disabled=_disabled or not topic2, key="t2_run"):
        with st.spinner("Génération en cours…"):
            try:
                c = _client()
                jur_str = ", ".join(st.session_state.t1_jurs or JURISDICTIONS[:3])
                period_str = f"{date_start.strftime('%d/%m/%Y')} – {date_end.strftime('%d/%m/%Y')}"
                top_risks_str = ""
                if st.session_state.t1_risks:
                    top = [r["name"] for r in st.session_state.t1_risks if r.get("level") == "Critique"][:4]
                    if top:
                        top_risks_str = f"\nRisques critiques identifiés : {', '.join(top)}"

                bg = _call(c, f"""You are a senior audit partner at a Big 4 firm writing for a Swiss private bank client.

Topic: {topic2}
Scope: {scope or "All group entities"}
Jurisdictions: {jur_str}
Risk appetite: {risk_appetite}{top_risks_str}

Write in French. Tone: McKinsey/EY — strategic, consultative, structured.
Produce a professional background section (3-4 paragraphs, NO section headers):
1. Market context and recent regulatory trends for this topic in private banking
2. Key challenges for wealth managers / HNWI institutions
3. Rationale for audit prioritisation at this time

Plain prose only. Use **bold** for key terms where appropriate.""",
                    max_tokens=3000)

                plan_txt = _call(c, f"""You are a senior internal auditor (IIA-certified).
Topic: {topic2}
Entity: Swiss private bank / asset manager (cross-border: CH, SG, HK, Bahamas, EU, UK)
Scope: {scope or "All entities and processes"}
Risk appetite: {risk_appetite}
Period: {period_str}{top_risks_str}

Write a structured audit plan in French (NO JSON). Sections:
**Objectifs** — 3-4 clear audit objectives
**Périmètre** — entities, processes, geographic coverage, exclusions
**Méthodologie** — approach (risk-based), standards (IIA, ISAE), techniques
**Ressources et calendrier** — team, key milestones

Plain prose, professional tone.""",
                    max_tokens=3000)

                tests_raw = _call(c, f"""You are a senior internal auditor.
Topic: {topic2}
Scope: {scope or "All entities"}
Risk appetite: {risk_appetite}{top_risks_str}

Generate EXACTLY 15 audit test procedures in French.
Respond ONLY with a valid JSON array — no markdown, no preamble:
[{{"num":1,"objective":"<test objective, 1 sentence>","procedure":"<step-by-step procedure, 2-3 sentences>","population":"<what is being tested>","sample":"<sampling method and size>","failure_criterion":"<what constitutes a control failure>"}}]""",
                    max_tokens=7000)

                tests = _parse_json(tests_raw)

                st.session_state.t2_background = bg
                st.session_state.t2_plan       = plan_txt
                st.session_state.t2_tests      = tests

                # Export files via agents
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
                        f"Risk appetite: {risk_appetite}\n"
                        f"Scope: {scope or 'All entities'}\n"
                        f"Period: {period_str}"
                        f"{extra_ctx}\n\n"
                        f"1. Identify 6-10 audit subjects → call generate_audit_plan_ppt.\n"
                        f"2. For each design 4-8 procedures → call generate_audit_procedures_excel."
                    )}]}], _h2)

                if "ppt_path" in extra and Path(extra["ppt_path"]).exists():
                    st.session_state.t2_pptx = Path(extra["ppt_path"]).read_bytes()
                if "excel_path" in extra and Path(extra["excel_path"]).exists():
                    st.session_state.t2_xlsx = Path(extra["excel_path"]).read_bytes()

            except Exception:
                st.error("Une erreur est survenue. Veuillez réessayer.")

    # Résultats
    if st.session_state.t2_background:
        topic2_lbl = st.session_state.t1_topic or topic2 or "audit"
        st.markdown("---")

        st.markdown('<div class="section-title">Contexte et enjeux</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-box">{st.session_state.t2_background}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-title">Plan d\'audit</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-box">{st.session_state.t2_plan}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-title">Programme de tests — ' + str(len(st.session_state.t2_tests or [])) + ' procédures</div>', unsafe_allow_html=True)
        _tests_table(st.session_state.t2_tests)

        pptx = st.session_state.t2_pptx
        xlsx = st.session_state.t2_xlsx
        if pptx or xlsx:
            st.markdown("---")
            ca, cb = st.columns(2)
            if pptx:
                ca.download_button(
                    "⬇  Plan d'audit (.pptx)", data=pptx,
                    file_name=f"Plan_Audit_{topic2_lbl.replace(' ', '_')}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
            if xlsx:
                cb.download_button(
                    "⬇  Programme de tests (.xlsx)", data=xlsx,
                    file_name=f"Tests_Audit_{topic2_lbl.replace(' ', '_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )


# ─────────────────────────────────────────────────────────────────────────────
# ONGLET 3 — RAPPORT FINAL
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<p style="color:#5a6488;font-size:13.5px;margin:0 0 1.4rem">Rédaction du rapport formel conforme aux standards IIA.</p>', unsafe_allow_html=True)

    ctx_parts = []
    if st.session_state.t1_topic:
        ctx_parts.append(f"✓ Sujet : {st.session_state.t1_topic}")
    if st.session_state.t2_plan:
        ctx_parts.append("✓ Plan d'audit disponible")
    if ctx_parts:
        st.markdown(f'<div class="ctx-pill">{" &nbsp;·&nbsp; ".join(ctx_parts)}</div>', unsafe_allow_html=True)

    default_name = f"Audit {st.session_state.t1_topic} — 2025" if st.session_state.t1_topic else ""
    audit_name = st.text_input("Intitulé du rapport",
        value=default_name,
        placeholder="Ex : Audit AML/KYC — Groupe Banque Privée — 2025", key="t3_name_in")

    observations = st.text_area("Issues et observations",
        placeholder="Ex :\n1. Surveillance des virements < CHF 10'000 non couverte.\n2. Dossiers KYC incomplets pour 12/50 clients testés.\n3. Absence de procédure PEP dans l'entité de Singapour.",
        height=200, key="t3_obs_in")

    c1, c2 = st.columns([2, 1])
    with c1:
        opinion = st.select_slider("Opinion d'audit",
            options=["Satisfaisant", "Partiellement satisfaisant", "Insatisfaisant"],
            value="Partiellement satisfaisant", key="t3_op_in")
    with c2:
        lang = st.radio("Langue du rapport", options=["Français", "English"],
            horizontal=True, key="t3_lang_in")

    uploads = st.file_uploader("Documents de travail (optionnel)",
        type=["pdf", "docx", "xlsx", "txt"], accept_multiple_files=True, key="t3_upload")

    st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

    if st.button("Générer le rapport", type="primary",
                 disabled=_disabled or not audit_name or not observations, key="t3_run"):
        with st.spinner("Rédaction en cours…"):
            try:
                c = _client()
                file_ids = []
                for uf in (uploads or []):
                    fm = _upload_sf(c, uf)
                    if fm:
                        file_ids.append(fm)

                lang_str = "French" if lang == "Français" else "English"
                reg_ctx = (f"\n\nApplicable regulations:\n{json.dumps(st.session_state.t1_regs, indent=2)[:1500]}"
                           if st.session_state.t1_regs else "")
                plan_ctx = (f"\n\nAudit plan summary:\n{st.session_state.t2_plan[:900]}"
                            if st.session_state.t2_plan else "")

                user_content = []
                if file_ids:
                    user_content.extend(build_file_content_blocks(file_ids))
                    user_content.append({"type": "text", "text": f"{len(file_ids)} supporting document(s) attached."})

                user_content.append({"type": "text", "text": (
                    f"Draft a professional IIA-standard internal audit report.\n\n"
                    f"Report title: {audit_name}\n"
                    f"Language: {lang_str}\n"
                    f"Audit opinion: {opinion}\n"
                    f"Institution: Swiss private bank (HNWI, cross-border: CH, SG, HK, Bahamas, EU, UK)"
                    f"{reg_ctx}{plan_ctx}\n\n"
                    f"Observations and findings:\n{observations}\n\n"
                    f"Structure the report:\n"
                    f"1. Executive summary (opinion, key findings, recommended actions)\n"
                    f"2. Background and context (institution, regulatory environment)\n"
                    f"3. Scope and methodology\n"
                    f"4. Findings — sorted by severity (Critical first), each with: "
                    f"risk rating, impact, root cause, recommendation, owner, target date\n"
                    f"5. Action plan (table)\n"
                    f"6. Motivated final opinion\n\n"
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
                st.error("Une erreur est survenue. Veuillez réessayer.")

    # Résultats
    if st.session_state.t3_report:
        res  = st.session_state.t3_report
        name = res.get("name", "rapport")
        st.markdown("---")

        st.markdown('<div class="section-title">Rapport d\'audit</div>', unsafe_allow_html=True)
        text = res.get("text", "")
        if text:
            st.markdown(f'<div class="output-box">{text}</div>', unsafe_allow_html=True)
        else:
            st.info("Le contenu du rapport est disponible dans l'export.")

        docx = res.get("docx_bytes")
        if docx:
            st.markdown("---")
            st.download_button(
                "⬇  Télécharger le rapport (.docx)",
                data=docx,
                file_name=f"Rapport_Audit_{name.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        # Révision ciblée
        st.markdown("---")
        st.markdown('<div class="section-title">Révision ciblée</div>', unsafe_allow_html=True)
        followup = st.text_area("Instructions", label_visibility="collapsed", height=80,
            placeholder="Ex : Reformulez la recommandation 3 de manière plus ferme. Ajoutez un délai de 30 jours pour le finding KYC.",
            key="t3_rev_in")

        if st.button("Réviser", disabled=not followup or _disabled, key="t3_rev_btn"):
            with st.spinner("Révision en cours…"):
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
                    st.error("Une erreur est survenue. Veuillez réessayer.")

# ── Pied de page ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p class="footer">AuditIQ · Audit multi-juridictions · Banque Privée · CH · SG · HK · Bahamas · EU · UK</p>',
    unsafe_allow_html=True,
)
