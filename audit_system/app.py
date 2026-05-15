"""
AuditIQ — Interface Streamlit pour les 3 agents d'audit
Lance depuis audit_system/ : streamlit run app.py
"""

import sys
import os
import json
import tempfile
from pathlib import Path

import streamlit as st

# ── Ensure audit_system is on path (works from any CWD) ──────────────────────
_HERE = Path(__file__).parent.resolve()
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

st.set_page_config(
    page_title="AuditIQ",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
  .stApp { background-color: #080b12; color: #dde3f5; }
  .main .block-container { padding: 2.5rem 3rem 4rem; max-width: 880px; }

  section[data-testid="stSidebar"] {
    background-color: #0c0f1a;
    border-right: 1px solid rgba(255,255,255,0.05);
  }
  section[data-testid="stSidebar"] .block-container { padding: 2rem 1.4rem; }

  .brand { display:flex; align-items:center; gap:10px; margin-bottom:1.8rem; }
  .brand-name { font-size:18px; font-weight:700; letter-spacing:-0.3px; color:#e8edf8; }
  .brand-sub  { font-size:11px; color:#424d72; text-transform:uppercase; letter-spacing:0.8px; margin-top:1px; }
  .nav-label  { font-size:10px; font-weight:600; color:#3a4566; text-transform:uppercase;
                letter-spacing:1px; margin:1.6rem 0 0.6rem; }

  .api-ok   { display:inline-flex; align-items:center; gap:6px; color:#22d3a5; font-size:12px;
              font-weight:600; background:rgba(34,211,165,0.08); border:1px solid rgba(34,211,165,0.2);
              border-radius:6px; padding:5px 10px; }
  .api-miss { display:inline-flex; align-items:center; gap:6px; color:#ef4444; font-size:12px;
              font-weight:600; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.2);
              border-radius:6px; padding:5px 10px; }

  .jur-grid  { display:flex; flex-wrap:wrap; gap:6px; margin-top:8px; }
  .jur-badge { font-size:11px; color:#8392bb; background:rgba(255,255,255,0.04);
               border:1px solid rgba(255,255,255,0.07); border-radius:5px; padding:3px 8px; }

  .page-header h1 { font-size:24px; font-weight:700; color:#e8edf8; margin:0 0 6px;
                    letter-spacing:-0.4px; }
  .page-header p  { font-size:13.5px; color:#5a6488; margin:0 0 2rem; line-height:1.6; }

  .stTextInput input, .stTextArea textarea {
    background-color:#10141f !important; border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:8px !important; color:#dde3f5 !important; font-size:13.5px !important;
  }
  .stTextInput input:focus, .stTextArea textarea:focus {
    border-color:rgba(79,126,248,0.5) !important;
    box-shadow:0 0 0 3px rgba(79,126,248,0.08) !important;
  }
  label[data-testid="stWidgetLabel"] p { font-size:13px !important; color:#8392bb !important; font-weight:500; }

  div[data-testid="stFileUploader"] {
    border:1px dashed rgba(255,255,255,0.1) !important;
    border-radius:10px !important; background:#10141f !important;
  }

  div[data-testid="stButton"] > button[kind="primary"] {
    background:linear-gradient(135deg,#2d54d4 0%,#4f7ef8 100%);
    border:none; border-radius:9px; color:#fff;
    font-size:13.5px; font-weight:600; padding:10px 24px; transition:opacity 0.15s;
  }
  div[data-testid="stButton"] > button[kind="primary"]:hover { opacity:0.88; }
  div[data-testid="stButton"] > button[kind="primary"]:disabled {
    background:#1a1f32 !important; color:#3a4566 !important; }

  div[data-testid="stDownloadButton"] button {
    background:rgba(79,126,248,0.1); color:#7fa8fb;
    border:1px solid rgba(79,126,248,0.25); border-radius:8px;
    font-size:13px; font-weight:500;
  }
  div[data-testid="stDownloadButton"] button:hover { background:rgba(79,126,248,0.18); }

  hr { border:none; border-top:1px solid rgba(255,255,255,0.05) !important; margin:1.8rem 0; }
  div[data-testid="stAlert"] { border-radius:9px !important; font-size:13px !important; }
  button[data-baseweb="tab"] { font-size:13px !important; color:#5a6488 !important; }
  button[data-baseweb="tab"][aria-selected="true"] { color:#a0b4f8 !important; }

  .output-box {
    background:#0f121e; border:1px solid rgba(255,255,255,0.07); border-radius:10px;
    padding:20px; font-size:13px; line-height:1.85; white-space:pre-wrap;
    color:#c8d0e8; max-height:540px; overflow-y:auto;
  }

  .ctx-pill { display:inline-flex; align-items:center; gap:8px; background:rgba(34,211,165,0.07);
              border:1px solid rgba(34,211,165,0.18); color:#22d3a5; border-radius:8px;
              padding:7px 14px; font-size:12.5px; font-weight:500; margin-bottom:1.6rem; }
  .ctx-miss { display:inline-flex; align-items:center; gap:8px; background:rgba(245,158,11,0.07);
              border:1px solid rgba(245,158,11,0.2); color:#f59e0b; border-radius:8px;
              padding:7px 14px; font-size:12.5px; font-weight:500; margin-bottom:1.6rem; }

  .risk-section { margin:2rem 0 1rem; }
  .risk-section h3 { font-size:16px; font-weight:600; color:#dde3f5; margin-bottom:1rem; }

  .footer { font-size:11px; color:#262e47; text-align:center; margin-top:3rem; letter-spacing:0.3px; }
</style>
""", unsafe_allow_html=True)

# ── API key — never from UI ───────────────────────────────────────────────────
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")

if api_key:
    os.environ["ANTHROPIC_API_KEY"] = api_key

# ── Agent imports ─────────────────────────────────────────────────────────────
AGENTS_OK = False
_import_error = ""
try:
    import anthropic as _anthropic
    import agent1_regulatory as _a1
    import agent2_audit_plan as _a2
    import agent3_report as _a3
    from base_agent import upload_file as _upload_file, build_file_content_blocks, MODEL
    from generators import (generate_regulatory_framework_docx,
                             generate_audit_plan_ppt,
                             generate_audit_procedures_excel,
                             generate_audit_report_docx)
    AGENTS_OK = True
except ImportError as e:
    _import_error = str(e)

JURISDICTIONS = ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU", "UK / FCA+PRA"]
OUTPUT_DIR = str(_HERE / "outputs")
Path(OUTPUT_DIR).mkdir(exist_ok=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_client():
    return _anthropic.Anthropic(api_key=api_key)


def _upload_streamlit_file(client, uploaded_file):
    if not uploaded_file:
        return None
    suffix = Path(uploaded_file.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    try:
        return _upload_file(client, tmp_path)
    finally:
        os.unlink(tmp_path)


def _agentic_loop(client, system_prompt, tools, messages, tool_handler):
    """Run the agentic tool-use loop. Returns (text_output, extra_dict)."""
    text_parts, extra = [], {}
    while True:
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=system_prompt,
            messages=messages,
            tools=tools,
            betas=["files-api-2025-04-14"],
        )
        for block in response.content:
            if hasattr(block, "text") and block.text:
                text_parts.append(block.text)
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            break
        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                result_text, result_extra = tool_handler(block.name, block.input)
                extra.update(result_extra)
                tool_results.append({"type": "tool_result",
                                     "tool_use_id": block.id,
                                     "content": result_text})
            if tool_results:
                messages.append({"role": "user", "content": tool_results})
            else:
                break
        else:
            break
    return "\n".join(text_parts), extra


def _generate_risk_analysis(client, topic: str, context: str = "") -> list[dict]:
    """Call Claude for a structured risk analysis (simple non-agentic call)."""
    ctx_snippet = f"\nContext summary:\n{context[:800]}" if context else ""
    prompt = (
        f"Audit topic: {topic}\n"
        f"Institution: Swiss private bank and asset manager (CH, SG, HK, Bahamas, EU, UK)"
        f"{ctx_snippet}\n\n"
        "Identify 6–9 key risks for this audit topic, spread across 3 severity levels.\n"
        "Respond ONLY with a valid JSON array — no markdown, no preamble:\n"
        '[{"level":"Critique|Élevé|Modéré","name":"<5-8 words>","description":"<2-3 sentences>",'
        '"impact":"<1-2 sentences>","control":"<1-2 sentences>"}]'
    )
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1].lstrip("json").strip()
        return json.loads(raw)
    except Exception:
        return []


def _display_risk_section(risks: list[dict]):
    if not risks:
        return
    st.markdown('<div class="risk-section"><h3>⚠️ Risques identifiés</h3></div>', unsafe_allow_html=True)
    level_style = {
        "Critique": ("#ef4444", "rgba(239,68,68,0.10)", "rgba(239,68,68,0.25)"),
        "Élevé":    ("#f97316", "rgba(249,115,22,0.10)", "rgba(249,115,22,0.25)"),
        "Modéré":   ("#eab308", "rgba(234,179,8,0.08)",  "rgba(234,179,8,0.22)"),
    }
    for level in ["Critique", "Élevé", "Modéré"]:
        bucket = [r for r in risks if r.get("level") == level]
        if not bucket:
            continue
        col, bg, border = level_style.get(level, ("#6b7280", "rgba(107,114,128,0.08)", "rgba(107,114,128,0.2)"))
        st.markdown(
            f'<div style="margin:1rem 0 0.5rem">'
            f'<span style="background:{bg};border:1px solid {border};color:{col};'
            f'border-radius:5px;padding:3px 12px;font-size:12px;font-weight:700">{level}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        for r in bucket:
            st.markdown(
                f'<div style="background:#0f121e;border:1px solid {border};border-left:3px solid {col};'
                f'border-radius:8px;padding:14px 18px;margin-bottom:10px">'
                f'<div style="font-size:13.5px;font-weight:600;color:#dde3f5;margin-bottom:8px">{r.get("name","")}</div>'
                f'<div style="font-size:12.5px;color:#8392bb;margin-bottom:5px">'
                f'<span style="color:#6b7599;font-weight:500">Description :</span> {r.get("description","")}</div>'
                f'<div style="font-size:12.5px;color:#8392bb;margin-bottom:5px">'
                f'<span style="color:#6b7599;font-weight:500">Impact :</span> {r.get("impact","")}</div>'
                f'<div style="font-size:12.5px;color:#8392bb">'
                f'<span style="color:#6b7599;font-weight:500">Contrôle attendu :</span> {r.get("control","")}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


def _debug_expander(raw):
    with st.expander("Détails techniques"):
        st.write("**Type retourné :**", type(raw).__name__)
        if isinstance(raw, dict):
            st.write("**Clés disponibles :**", list(raw.keys()))
            for k, v in raw.items():
                st.write(f"**{k}** ({type(v).__name__}) :", str(v)[:500] if v else "(vide)")
        else:
            st.write(raw)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand">
      <span style="font-size:22px">🏦</span>
      <div>
        <div class="brand-name">AuditIQ</div>
        <div class="brand-sub">Multi-agent audit system</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if api_key:
        st.markdown('<div class="api-ok">✓ API Anthropic configurée</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="api-miss">✗ ANTHROPIC_API_KEY manquante</div>', unsafe_allow_html=True)
        st.caption("Définissez la variable d'environnement `ANTHROPIC_API_KEY` ou ajoutez-la dans `.streamlit/secrets.toml`.")

    st.markdown('<p class="nav-label" style="margin-top:2rem">Agents</p>', unsafe_allow_html=True)
    agent_choice = st.radio(
        "Agent",
        options=[
            "Agent 1 — Regulatory Framework",
            "Agent 2 — Audit Plan",
            "Agent 3 — Audit Report",
        ],
        label_visibility="collapsed",
    )

    st.markdown('<p class="nav-label" style="margin-top:2rem">Juridictions couvertes</p>', unsafe_allow_html=True)
    badges = "".join(f'<span class="jur-badge">{j}</span>' for j in JURISDICTIONS)
    st.markdown(f'<div class="jur-grid">{badges}</div>', unsafe_allow_html=True)

    if not AGENTS_OK:
        st.markdown("---")
        st.error(f"Agents non chargés : `{_import_error}`")

# ── Session state ─────────────────────────────────────────────────────────────
for _k in ("reg_context", "audit_plan_context"):
    if _k not in st.session_state:
        st.session_state[_k] = ""
for _k in ("agent1_result", "agent2_result", "agent3_result",
           "risks1", "risks2", "risks3"):
    if _k not in st.session_state:
        st.session_state[_k] = None

_api_disabled = not api_key or not AGENTS_OK

# ═════════════════════════════════════════════════════════════════════════════
# AGENT 1 — REGULATORY FRAMEWORK
# ═════════════════════════════════════════════════════════════════════════════
if "Agent 1" in agent_choice:
    st.markdown("""
    <div class="page-header">
      <h1>Regulatory Framework</h1>
      <p>Compile les lois, réglementations et guidelines applicables sur 6 juridictions.</p>
    </div>
    """, unsafe_allow_html=True)

    audit_topic = st.text_input("Sujet d'audit",
        placeholder="Ex : AML/KYC, Credit Risk, Cybersecurity, Operational Risk…")
    focus_areas = st.multiselect("Domaines prioritaires *(optionnel)*",
        options=["AML/CFT", "KYC/CDD", "Risque opérationnel", "Cybersécurité",
                 "Gouvernance", "Reporting", "Gestion des risques", "Protection des données"])
    uploaded_file = st.file_uploader(
        "Document de référence *(optionnel — PDF, Word, Excel, TXT)*",
        type=["pdf", "docx", "xlsx", "txt"])

    st.markdown("<div style='margin-top:1.4rem'></div>", unsafe_allow_html=True)

    if st.button("Lancer l'analyse", type="primary",
                 disabled=_api_disabled or not audit_topic):
        with st.spinner("Compilation du cadre réglementaire en cours…"):
            try:
                client = _make_client()
                file_ids_mimes = []
                if uploaded_file:
                    fm = _upload_streamlit_file(client, uploaded_file)
                    if fm:
                        file_ids_mimes.append(fm)

                jur_str   = ", ".join(JURISDICTIONS)
                focus_str = ", ".join(focus_areas) if focus_areas else "tous domaines"
                user_content = []
                if file_ids_mimes:
                    user_content.extend(build_file_content_blocks(file_ids_mimes))
                    user_content.append({"type": "text",
                        "text": f"I have uploaded {len(file_ids_mimes)} document(s) for context."})
                user_content.append({"type": "text", "text": (
                    f"Compile a comprehensive regulatory framework.\n\n"
                    f"**Audit Topic:** {audit_topic}\n"
                    f"**Focus:** {focus_str}\n"
                    f"**Jurisdictions:** {jur_str}\n\n"
                    f"For each jurisdiction: cite specific laws, circulars, key requirements, upcoming changes. "
                    f"Highlight cross-jurisdictional overlaps and top 5 priority areas. "
                    f"Then call `save_regulatory_framework` to export."
                )})

                def _h1(name, inp):
                    if name == "save_regulatory_framework":
                        try:
                            p = generate_regulatory_framework_docx(inp, OUTPUT_DIR)
                            return f"Saved: {p}", {"docx_path": p}
                        except Exception as e:
                            return f"Error: {e}", {}
                    return "Unknown tool", {}

                text_out, extra = _agentic_loop(
                    client, _a1.SYSTEM_PROMPT, _a1.TOOLS,
                    [{"role": "user", "content": user_content}], _h1)

                result = {"text": text_out, "topic": audit_topic}
                if "docx_path" in extra and Path(extra["docx_path"]).exists():
                    result["docx_bytes"] = Path(extra["docx_path"]).read_bytes()

                st.session_state.agent1_result = result
                st.session_state.reg_context   = text_out

                # Risk analysis
                with st.spinner("Analyse des risques en cours…"):
                    st.session_state.risks1 = _generate_risk_analysis(client, audit_topic, text_out)

                st.success("Analyse terminée.")
            except Exception as e:
                st.error(f"Erreur : {e}")

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.agent1_result:
        res   = st.session_state.agent1_result
        topic = res.get("topic", "audit")
        st.markdown("---")

        # 1. Résultat principal
        st.markdown("#### Cadre réglementaire")
        text = res.get("text", "")
        if text:
            st.markdown(f'<div class="output-box">{text}</div>', unsafe_allow_html=True)
        else:
            st.info("Aucun contenu textuel retourné — vérifiez les détails techniques ci-dessous.")

        # 2. Risques
        if st.session_state.risks1:
            st.markdown("---")
            _display_risk_section(st.session_state.risks1)

        # 3. Export (après affichage)
        docx = res.get("docx_bytes")
        if docx:
            st.markdown("---")
            st.download_button(
                "⬇ Télécharger le Regulatory Framework (.docx)",
                data=docx,
                file_name=f"Regulatory_Framework_{topic.replace(' ','_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        # 4. Debug
        _debug_expander(res)

        st.info("Le contexte réglementaire est automatiquement transmis à l'Agent 2.")

# ═════════════════════════════════════════════════════════════════════════════
# AGENT 2 — AUDIT PLAN
# ═════════════════════════════════════════════════════════════════════════════
elif "Agent 2" in agent_choice:
    st.markdown("""
    <div class="page-header">
      <h1>Audit Plan</h1>
      <p>Génère le plan d'audit (PowerPoint) et les procédures détaillées (Excel).</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.reg_context:
        st.markdown('<div class="ctx-pill">✓ Contexte réglementaire (Agent 1) disponible</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="ctx-miss">⚠ Aucun contexte Agent 1 — saisissez le sujet manuellement</div>',
                    unsafe_allow_html=True)

    audit_topic_2 = st.text_input("Sujet d'audit",
        placeholder="Ex : AML/KYC, Credit Risk, Cybersecurity…")
    risk_appetite = st.select_slider("Appétit au risque",
        options=["Très faible", "Faible", "Modéré", "Élevé", "Très élevé"], value="Modéré")
    audit_scope = st.text_area("Périmètre *(optionnel)*",
        placeholder="Ex : Toutes les entités du groupe en CH, SG et HK. Focus onboarding et transaction monitoring.",
        height=90)
    uploaded_file_2 = st.file_uploader(
        "Document de référence *(optionnel)*",
        type=["pdf", "docx", "xlsx", "txt"], key="upload2")

    st.markdown("<div style='margin-top:1.4rem'></div>", unsafe_allow_html=True)

    if st.button("Générer le plan d'audit", type="primary",
                 disabled=_api_disabled or not audit_topic_2):
        with st.spinner("Génération du plan d'audit en cours…"):
            try:
                client = _make_client()
                file_ids_mimes = []
                if uploaded_file_2:
                    fm = _upload_streamlit_file(client, uploaded_file_2)
                    if fm:
                        file_ids_mimes.append(fm)

                extra_ctx = ""
                if st.session_state.reg_context:
                    extra_ctx = f"\n\nREGULATORY CONTEXT:\n{st.session_state.reg_context[:3000]}"

                user_content = []
                if file_ids_mimes:
                    user_content.extend(build_file_content_blocks(file_ids_mimes))
                user_content.append({"type": "text", "text": (
                    f"Create a comprehensive risk-based audit plan.\n\n"
                    f"**Audit Topic:** {audit_topic_2}\n"
                    f"**Risk Appetite:** {risk_appetite}\n"
                    f"**Scope:** {audit_scope or 'All entities'}\n"
                    f"**Institution:** Swiss private bank/asset manager (CH, SG, HK, Bahamas, EU, UK)"
                    f"{extra_ctx}\n\n"
                    f"1. Identify 6-12 distinct audit subjects → call `generate_audit_plan_ppt`.\n"
                    f"2. For each subject design 4-8 procedures → call `generate_audit_procedures_excel`."
                )})

                def _h2(name, inp):
                    if name == "generate_audit_plan_ppt":
                        try:
                            p = generate_audit_plan_ppt(inp, OUTPUT_DIR)
                            return f"PPT saved: {p}. Now generate procedures Excel.", {"ppt_path": p}
                        except Exception as e:
                            return f"Error: {e}", {}
                    elif name == "generate_audit_procedures_excel":
                        try:
                            p = generate_audit_procedures_excel(inp, OUTPUT_DIR)
                            return f"Excel saved: {p}.", {"excel_path": p}
                        except Exception as e:
                            return f"Error: {e}", {}
                    return "Unknown tool", {}

                text_out, extra = _agentic_loop(
                    client, _a2.SYSTEM_PROMPT, _a2.TOOLS,
                    [{"role": "user", "content": user_content}], _h2)

                result = {"text": text_out, "topic": audit_topic_2}
                if "ppt_path" in extra and Path(extra["ppt_path"]).exists():
                    result["pptx_bytes"] = Path(extra["ppt_path"]).read_bytes()
                if "excel_path" in extra and Path(extra["excel_path"]).exists():
                    result["xlsx_bytes"] = Path(extra["excel_path"]).read_bytes()

                st.session_state.agent2_result       = result
                st.session_state.audit_plan_context  = text_out

                with st.spinner("Analyse des risques en cours…"):
                    st.session_state.risks2 = _generate_risk_analysis(client, audit_topic_2, text_out)

                st.success("Plan d'audit généré.")
            except Exception as e:
                st.error(f"Erreur : {e}")

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.agent2_result:
        res   = st.session_state.agent2_result
        topic = res.get("topic", "audit")
        st.markdown("---")

        # 1. Résultat principal
        st.markdown("#### Plan d'audit")
        text = res.get("text", "")
        if text:
            st.markdown(f'<div class="output-box">{text}</div>', unsafe_allow_html=True)
        else:
            st.info("Aucun contenu textuel retourné — vérifiez les détails techniques ci-dessous.")

        # 2. Risques
        if st.session_state.risks2:
            st.markdown("---")
            _display_risk_section(st.session_state.risks2)

        # 3. Exports (après affichage)
        pptx = res.get("pptx_bytes")
        xlsx = res.get("xlsx_bytes")
        if pptx or xlsx:
            st.markdown("---")
            col_a, col_b = st.columns(2)
            if pptx:
                col_a.download_button("⬇ Plan d'audit (.pptx)", data=pptx,
                    file_name=f"Audit_Plan_{topic.replace(' ','_')}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
            if xlsx:
                col_b.download_button("⬇ Procédures détaillées (.xlsx)", data=xlsx,
                    file_name=f"Audit_Procedures_{topic.replace(' ','_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # 4. Debug
        _debug_expander(res)

# ═════════════════════════════════════════════════════════════════════════════
# AGENT 3 — AUDIT REPORT
# ═════════════════════════════════════════════════════════════════════════════
elif "Agent 3" in agent_choice:
    st.markdown("""
    <div class="page-header">
      <h1>Audit Report</h1>
      <p>Rédige un rapport d'audit formel aligné IIA, exporté en Word professionnel.</p>
    </div>
    """, unsafe_allow_html=True)

    audit_name = st.text_input("Nom de l'audit",
        placeholder="Ex : Audit AML/KYC — Groupe Banque Privée — 2025")
    observations = st.text_area("Observations et findings",
        placeholder="""Ex :
1. Le processus de surveillance ne couvre pas les virements < CHF 10'000.
2. Dossiers KYC incomplets pour 12 clients sur 50 testés.
3. Absence de procédure PEP dans l'entité de Singapour.""",
        height=220)

    col_op, col_lang = st.columns([2, 1])
    with col_op:
        audit_opinion = st.select_slider("Opinion d'audit",
            options=["Satisfactory", "Needs Improvement", "Unsatisfactory", "Critical"],
            value="Needs Improvement")
    with col_lang:
        report_lang = st.radio("Langue", options=["Français", "English"], horizontal=True)

    st.markdown("<div style='margin-top:0.4rem'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    inc_exec   = c1.checkbox("Résumé exécutif", value=True)
    inc_find   = c2.checkbox("Tableau findings", value=True)
    inc_reco   = c3.checkbox("Recommandations", value=True)
    inc_action = c4.checkbox("Plan d'action",   value=True)

    uploaded_files_3 = st.file_uploader(
        "Documents à analyser *(optionnel — issues log, workpapers…)*",
        type=["pdf", "docx", "xlsx", "txt"], accept_multiple_files=True, key="upload3")

    st.markdown("<div style='margin-top:1.4rem'></div>", unsafe_allow_html=True)

    if st.button("Générer le rapport", type="primary",
                 disabled=_api_disabled or not audit_name or not observations):
        with st.spinner("Rédaction du rapport d'audit en cours…"):
            try:
                client = _make_client()
                file_ids_mimes = []
                for uf in (uploaded_files_3 or []):
                    fm = _upload_streamlit_file(client, uf)
                    if fm:
                        file_ids_mimes.append(fm)

                options_str = ", ".join(filter(None, [
                    "executive summary" if inc_exec   else "",
                    "findings table"    if inc_find   else "",
                    "recommendations"   if inc_reco   else "",
                    "action plan"       if inc_action else "",
                ]))
                lang_str = "French" if report_lang == "Français" else "English"
                reg_ctx  = f"\n\nRegulatory context:\n{st.session_state.reg_context[:2000]}" \
                           if st.session_state.reg_context else ""

                user_content = []
                if file_ids_mimes:
                    user_content.extend(build_file_content_blocks(file_ids_mimes))
                    user_content.append({"type": "text",
                        "text": f"I have uploaded {len(file_ids_mimes)} document(s) with audit evidence."})
                user_content.append({"type": "text", "text": (
                    f"Draft a professional audit report.\n\n"
                    f"**Report Title:** {audit_name}\n"
                    f"**Language:** {lang_str}\n"
                    f"**Suggested Opinion:** {audit_opinion}\n"
                    f"**Include:** {options_str}"
                    f"{reg_ctx}\n\n"
                    f"**Observations:**\n{observations}\n\n"
                    f"Structure findings by severity (Critical first) with risk rating, impact, "
                    f"root cause, recommendation, target date. Then call `generate_audit_report`."
                )})

                def _h3(name, inp):
                    if name == "generate_audit_report":
                        try:
                            p = generate_audit_report_docx(inp, OUTPUT_DIR)
                            return f"Saved: {p}", {"docx_path": p}
                        except Exception as e:
                            return f"Error: {e}", {}
                    return "Unknown tool", {}

                text_out, extra = _agentic_loop(
                    client, _a3.SYSTEM_PROMPT, _a3.TOOLS,
                    [{"role": "user", "content": user_content}], _h3)

                result = {"text": text_out, "name": audit_name}
                if "docx_path" in extra and Path(extra["docx_path"]).exists():
                    result["docx_bytes"] = Path(extra["docx_path"]).read_bytes()

                st.session_state.agent3_result = result

                with st.spinner("Analyse des risques en cours…"):
                    st.session_state.risks3 = _generate_risk_analysis(
                        client, audit_name, text_out)

                st.success("Rapport généré.")
            except Exception as e:
                st.error(f"Erreur : {e}")

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.agent3_result:
        res  = st.session_state.agent3_result
        name = res.get("name", "audit")
        fname = f"Rapport_Audit_{name.replace(' ','_')}.docx"
        st.markdown("---")

        # 1. Résultat principal
        st.markdown("#### Rapport d'audit")
        text = res.get("text", "")
        if text:
            st.markdown(f'<div class="output-box">{text}</div>', unsafe_allow_html=True)
        else:
            st.info("Aucun contenu textuel retourné — vérifiez les détails techniques ci-dessous.")

        # 2. Risques
        if st.session_state.risks3:
            st.markdown("---")
            _display_risk_section(st.session_state.risks3)

        # 3. Export (après affichage)
        docx = res.get("docx_bytes")
        if docx:
            st.markdown("---")
            st.download_button("⬇ Télécharger le rapport (.docx)", data=docx,
                file_name=fname,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        # 4. Debug
        _debug_expander(res)

        # 5. Révision
        st.markdown("---")
        st.markdown("**Demander une révision**")
        followup = st.text_area("Instruction", label_visibility="collapsed", height=80,
            placeholder="Ex : Reformule la recommandation 3 de manière plus ferme.")
        if st.button("Réviser le rapport", disabled=not followup or _api_disabled):
            with st.spinner("Révision en cours…"):
                try:
                    client = _make_client()
                    rev_content = [{"type": "text", "text": (
                        f"Previous report:\n{res.get('text','')[:2000]}\n\n"
                        f"Revision: {followup}\n\n"
                        f"Apply revision and call `generate_audit_report` to export."
                    )}]

                    def _h3r(name, inp):
                        if name == "generate_audit_report":
                            try:
                                p = generate_audit_report_docx(inp, OUTPUT_DIR)
                                return f"Saved: {p}", {"docx_path": p}
                            except Exception as e:
                                return f"Error: {e}", {}
                        return "Unknown tool", {}

                    text2, extra2 = _agentic_loop(
                        client, _a3.SYSTEM_PROMPT, _a3.TOOLS,
                        [{"role": "user", "content": rev_content}], _h3r)

                    res2 = {"text": text2, "name": name}
                    if "docx_path" in extra2 and Path(extra2["docx_path"]).exists():
                        res2["docx_bytes"] = Path(extra2["docx_path"]).read_bytes()
                    st.session_state.agent3_result = res2
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur : {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p class="footer">AuditIQ · Système multi-agents · Banque Privée · CH · SG · HK · Bahamas · EU · UK</p>',
    unsafe_allow_html=True,
)
