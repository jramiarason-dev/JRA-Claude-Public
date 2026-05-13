"""
AuditIQ — Interface Streamlit pour les 3 agents d'audit
"""

import sys
import os
import tempfile
from pathlib import Path

import streamlit as st

# ── Add audit_system to path ──────────────────────────────────────────────────
AUDIT_SYS = Path(__file__).parent / "audit_system"
if str(AUDIT_SYS) not in sys.path:
    sys.path.insert(0, str(AUDIT_SYS))

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
  .main .block-container { padding: 2.5rem 3rem 4rem; max-width: 860px; }

  section[data-testid="stSidebar"] {
    background-color: #0c0f1a;
    border-right: 1px solid rgba(255,255,255,0.05);
  }
  section[data-testid="stSidebar"] .block-container { padding: 2rem 1.4rem; }

  .brand { display: flex; align-items: center; gap: 10px; margin-bottom: 1.8rem; }
  .brand-icon { font-size: 22px; }
  .brand-name { font-size: 18px; font-weight: 700; letter-spacing: -0.3px; color: #e8edf8; }
  .brand-sub { font-size: 11px; color: #424d72; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 1px; }

  .nav-label { font-size: 10px; font-weight: 600; color: #3a4566; text-transform: uppercase;
               letter-spacing: 1px; margin: 1.6rem 0 0.6rem; }
  div[data-testid="stRadio"] label { font-size: 13.5px !important; }
  div[data-testid="stRadio"] > div { gap: 2px !important; }

  .api-ok   { display:inline-flex; align-items:center; gap:6px; color:#22d3a5;
              font-size:12px; font-weight:600; background:rgba(34,211,165,0.08);
              border:1px solid rgba(34,211,165,0.2); border-radius:6px; padding:5px 10px; }
  .api-miss { display:inline-flex; align-items:center; gap:6px; color:#f59e0b;
              font-size:12px; font-weight:600; background:rgba(245,158,11,0.08);
              border:1px solid rgba(245,158,11,0.2); border-radius:6px; padding:5px 10px; }

  .jur-grid { display:flex; flex-wrap:wrap; gap:6px; margin-top: 8px; }
  .jur-badge { font-size:11px; color:#8392bb; background:rgba(255,255,255,0.04);
               border:1px solid rgba(255,255,255,0.07); border-radius:5px; padding:3px 8px; }

  .page-header { margin-bottom: 2rem; }
  .page-header h1 { font-size:24px; font-weight:700; color:#e8edf8; margin:0 0 6px;
                    letter-spacing:-0.4px; }
  .page-header p  { font-size:13.5px; color:#5a6488; margin:0; line-height:1.6; }

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
  label[data-testid="stWidgetLabel"] p { font-size:13px !important; color:#8392bb !important; font-weight:500; }

  div[data-testid="stFileUploader"] {
    border: 1px dashed rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    background: #10141f !important;
  }

  div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #2d54d4 0%, #4f7ef8 100%);
    border: none; border-radius: 9px; color: #ffffff;
    font-size: 13.5px; font-weight: 600; padding: 10px 24px;
    transition: opacity 0.15s;
  }
  div[data-testid="stButton"] > button[kind="primary"]:hover { opacity: 0.88; }
  div[data-testid="stButton"] > button[kind="primary"]:disabled {
    background: #1a1f32 !important; color: #3a4566 !important; }

  div[data-testid="stButton"] > button[kind="secondary"] {
    background: transparent; border: 1px solid rgba(255,255,255,0.1);
    border-radius: 9px; color: #8392bb; font-size: 13px; padding: 8px 18px;
  }

  div[data-testid="stDownloadButton"] button {
    background: rgba(79,126,248,0.1); color: #7fa8fb;
    border: 1px solid rgba(79,126,248,0.25); border-radius: 8px;
    font-size: 13px; font-weight: 500;
  }
  div[data-testid="stDownloadButton"] button:hover { background: rgba(79,126,248,0.18); }

  hr { border: none; border-top: 1px solid rgba(255,255,255,0.05) !important; margin: 1.8rem 0; }
  div[data-testid="stAlert"] { border-radius: 9px !important; font-size: 13px !important; }
  button[data-baseweb="tab"] { font-size: 13px !important; color: #5a6488 !important; }
  button[data-baseweb="tab"][aria-selected="true"] { color: #a0b4f8 !important; }

  .output-box {
    background: #0f121e; border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px; padding: 20px; font-size: 13px; line-height: 1.85;
    white-space: pre-wrap; color: #c8d0e8; max-height: 520px; overflow-y: auto;
  }

  .ctx-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(34,211,165,0.07); border: 1px solid rgba(34,211,165,0.18);
    color: #22d3a5; border-radius: 8px; padding: 7px 14px;
    font-size: 12.5px; font-weight:500; margin-bottom: 1.6rem;
  }
  .ctx-miss {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(245,158,11,0.07); border: 1px solid rgba(245,158,11,0.2);
    color: #f59e0b; border-radius: 8px; padding: 7px 14px;
    font-size: 12.5px; font-weight:500; margin-bottom: 1.6rem;
  }

  label[data-testid="stCheckbox"] p { font-size:13px !important; color:#8392bb !important; }
  div[data-testid="stSpinner"] p { font-size: 13px !important; color: #5a6488 !important; }
  .footer { font-size:11px; color:#262e47; text-align:center; margin-top:3rem; letter-spacing:0.3px; }
</style>
""", unsafe_allow_html=True)

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
OUTPUT_DIR = str(Path(__file__).parent / "outputs")
Path(OUTPUT_DIR).mkdir(exist_ok=True)


def _make_client(api_key: str):
    return _anthropic.Anthropic(api_key=api_key)


def _upload_streamlit_file(client, uploaded_file) -> tuple[str, str] | None:
    """Upload a Streamlit UploadedFile to the Anthropic Files API."""
    if not uploaded_file:
        return None
    suffix = Path(uploaded_file.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    try:
        result = _upload_file(client, tmp_path)
        return result
    finally:
        os.unlink(tmp_path)


def _extract_text(response) -> str:
    """Extract text content from an Anthropic message response."""
    parts = []
    for block in response.content:
        if hasattr(block, "text") and block.text:
            parts.append(block.text)
    return "\n".join(parts)


def _agentic_loop(client, system_prompt, tools, messages, tool_handler) -> tuple[str, dict]:
    """Run the agentic loop. Returns (text_output, extra_results)."""
    text_parts = []
    extra = {}

    while True:
        kwargs = dict(
            model=MODEL,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=system_prompt,
            messages=messages,
            tools=tools,
            betas=["files-api-2025-04-14"],
        )
        response = client.beta.messages.create(**kwargs)

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
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result_text,
                })
            if tool_results:
                messages.append({"role": "user", "content": tool_results})
            else:
                break
        else:
            break

    return "\n".join(text_parts), extra


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand">
      <span class="brand-icon">🏦</span>
      <div>
        <div class="brand-name">AuditIQ</div>
        <div class="brand-sub">Multi-agent audit system</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="nav-label">Configuration</p>', unsafe_allow_html=True)
    api_key = st.text_input(
        "Clé API Anthropic",
        type="password",
        value=os.environ.get("ANTHROPIC_API_KEY", ""),
        placeholder="sk-ant-...",
        label_visibility="collapsed",
    )
    if api_key:
        os.environ["ANTHROPIC_API_KEY"] = api_key
        st.markdown('<div class="api-ok">✓ Clé API configurée</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="api-miss">⚠ Clé API requise</div>', unsafe_allow_html=True)

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
for key in ("reg_context", "audit_plan_context"):
    if key not in st.session_state:
        st.session_state[key] = ""
for key in ("agent1_result", "agent2_result", "agent3_result"):
    if key not in st.session_state:
        st.session_state[key] = None

# ═════════════════════════════════════════════════════════════════════════════
# AGENT 1
# ═════════════════════════════════════════════════════════════════════════════
if "Agent 1" in agent_choice:
    st.markdown("""
    <div class="page-header">
      <h1>Regulatory Framework</h1>
      <p>Compile les lois, réglementations et guidelines applicables sur 6 juridictions pour un sujet d'audit donné.</p>
    </div>
    """, unsafe_allow_html=True)

    audit_topic = st.text_input(
        "Sujet d'audit",
        placeholder="Ex : AML/KYC, Credit Risk, Cybersecurity, Operational Risk…",
    )

    focus_areas = st.multiselect(
        "Domaines prioritaires *(optionnel)*",
        options=["AML/CFT", "KYC/CDD", "Risque opérationnel", "Cybersécurité",
                 "Gouvernance", "Reporting", "Gestion des risques", "Protection des données"],
        default=[],
    )

    uploaded_file = st.file_uploader(
        "Document de référence *(optionnel — PDF, Word, Excel, TXT)*",
        type=["pdf", "docx", "xlsx", "txt"],
    )

    st.markdown("<div style='margin-top:1.4rem'></div>", unsafe_allow_html=True)
    run_agent1 = st.button("Lancer l'analyse", type="primary",
                           disabled=not api_key or not audit_topic or not AGENTS_OK)

    if run_agent1:
        with st.spinner("Compilation du cadre réglementaire en cours…"):
            try:
                client = _make_client(api_key)
                file_ids_mimes = []
                if uploaded_file:
                    fid_mime = _upload_streamlit_file(client, uploaded_file)
                    if fid_mime:
                        file_ids_mimes.append(fid_mime)

                jur_str   = ", ".join(JURISDICTIONS)
                focus_str = ", ".join(focus_areas) if focus_areas else "tous domaines"

                user_content: list = []
                if file_ids_mimes:
                    user_content.extend(build_file_content_blocks(file_ids_mimes))
                    user_content.append({"type": "text",
                        "text": f"I have uploaded {len(file_ids_mimes)} document(s) for context."})

                user_content.append({"type": "text", "text": (
                    f"Please compile a comprehensive regulatory framework for the following audit topic:\n\n"
                    f"**Audit Topic:** {audit_topic}\n"
                    f"**Focus Areas:** {focus_str}\n"
                    f"**Institution:** Swiss private bank and asset manager with operations in: {jur_str}.\n\n"
                    f"For EACH jurisdiction, list key regulations with precise citations, key requirements, "
                    f"and upcoming changes. Then highlight cross-jurisdictional considerations and top 5 "
                    f"priority areas. Once complete, call `save_regulatory_framework` to export."
                )})

                messages = [{"role": "user", "content": user_content}]

                def _handle_a1(tool_name, tool_input):
                    if tool_name == "save_regulatory_framework":
                        try:
                            path = generate_regulatory_framework_docx(tool_input, OUTPUT_DIR)
                            return f"Framework saved: {path}", {"docx_path": path}
                        except Exception as e:
                            return f"Error saving document: {e}", {}
                    return "Unknown tool", {}

                text_out, extra = _agentic_loop(
                    client, _a1.SYSTEM_PROMPT, _a1.TOOLS, messages, _handle_a1)

                result = {"text": text_out}
                if "docx_path" in extra and Path(extra["docx_path"]).exists():
                    result["docx_bytes"] = Path(extra["docx_path"]).read_bytes()

                st.session_state.agent1_result = result
                st.session_state.reg_context = text_out
                st.success("Analyse terminée.")
            except Exception as e:
                st.error(f"Erreur : {e}")

    if st.session_state.agent1_result:
        res = st.session_state.agent1_result
        st.markdown("---")
        tabs = st.tabs(["Contenu réglementaire", "Téléchargement"])
        with tabs[0]:
            if res.get("text"):
                st.markdown(f'<div class="output-box">{res["text"]}</div>', unsafe_allow_html=True)
            else:
                st.info("Le contenu réglementaire a été exporté directement en Word.")
        with tabs[1]:
            if res.get("docx_bytes"):
                st.download_button(
                    "⬇ Télécharger le Regulatory Framework (.docx)",
                    data=res["docx_bytes"],
                    file_name=f"Regulatory_Framework_{audit_topic.replace(' ','_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            else:
                st.info("Aucun document Word généré — relancez l'agent pour obtenir l'export.")

        st.info("Le contexte réglementaire est automatiquement transmis à l'Agent 2.")

# ═════════════════════════════════════════════════════════════════════════════
# AGENT 2
# ═════════════════════════════════════════════════════════════════════════════
elif "Agent 2" in agent_choice:
    st.markdown("""
    <div class="page-header">
      <h1>Audit Plan</h1>
      <p>Génère le plan d'audit (PowerPoint) et les procédures détaillées avec tests, tailles d'échantillon et évaluations de risques (Excel).</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.reg_context:
        st.markdown('<div class="ctx-pill">✓ Contexte réglementaire (Agent 1) disponible</div>', unsafe_allow_html=True)
    else:
        st.markdown("<div class='ctx-miss'>⚠ Aucun contexte Agent 1 — saisissez le sujet manuellement</div>", unsafe_allow_html=True)

    audit_topic_2 = st.text_input(
        "Sujet d'audit",
        placeholder="Ex : AML/KYC, Credit Risk, Cybersecurity…",
    )

    risk_appetite = st.select_slider(
        "Appétit au risque de l'organisation",
        options=["Très faible", "Faible", "Modéré", "Élevé", "Très élevé"],
        value="Modéré",
    )

    audit_scope = st.text_area(
        "Périmètre de l'audit *(optionnel)*",
        placeholder="Ex : Toutes les entités du groupe en Suisse, Singapour et Hong Kong. Focus sur les processus onboarding et transaction monitoring.",
        height=90,
    )

    uploaded_file_2 = st.file_uploader(
        "Document de référence *(optionnel — PDF, Word, Excel, TXT)*",
        type=["pdf", "docx", "xlsx", "txt"],
        key="upload2",
    )

    st.markdown("<div style='margin-top:1.4rem'></div>", unsafe_allow_html=True)
    run_agent2 = st.button("Générer le plan d'audit", type="primary",
                           disabled=not api_key or not audit_topic_2 or not AGENTS_OK)

    if run_agent2:
        with st.spinner("Génération du plan d'audit en cours…"):
            try:
                client = _make_client(api_key)
                file_ids_mimes = []
                if uploaded_file_2:
                    fid_mime = _upload_streamlit_file(client, uploaded_file_2)
                    if fid_mime:
                        file_ids_mimes.append(fid_mime)

                extra_context = ""
                if st.session_state.reg_context:
                    extra_context = f"\n\nREGULATORY CONTEXT (from Agent 1):\n{st.session_state.reg_context[:3000]}"

                user_content: list = []
                if file_ids_mimes:
                    user_content.extend(build_file_content_blocks(file_ids_mimes))

                user_content.append({"type": "text", "text": (
                    f"Create a comprehensive, risk-based audit plan for the following:\n\n"
                    f"**Audit Topic:** {audit_topic_2}\n"
                    f"**Risk Appetite:** {risk_appetite}\n"
                    f"**Scope:** {audit_scope or 'All entities'}\n"
                    f"**Institution:** Swiss private bank and asset manager (CH, SG, HK, Bahamas, EU, UK)\n"
                    f"{extra_context}\n\n"
                    f"1. Identify 6-12 distinct audit subjects, then call `generate_audit_plan_ppt`.\n"
                    f"2. For each subject, design 4-8 detailed procedures, then call `generate_audit_procedures_excel`.\n"
                    f"Be thorough and professional."
                )})

                messages = [{"role": "user", "content": user_content}]

                def _handle_a2(tool_name, tool_input):
                    if tool_name == "generate_audit_plan_ppt":
                        try:
                            path = generate_audit_plan_ppt(tool_input, OUTPUT_DIR)
                            return f"PPT generated: {path}. Now generate the procedures Excel.", {"ppt_path": path}
                        except Exception as e:
                            return f"Error: {e}", {}
                    elif tool_name == "generate_audit_procedures_excel":
                        try:
                            path = generate_audit_procedures_excel(tool_input, OUTPUT_DIR)
                            return f"Excel generated: {path}. Audit plan complete.", {"excel_path": path}
                        except Exception as e:
                            return f"Error: {e}", {}
                    return "Unknown tool", {}

                text_out, extra = _agentic_loop(
                    client, _a2.SYSTEM_PROMPT, _a2.TOOLS, messages, _handle_a2)

                result = {"text": text_out}
                if "ppt_path" in extra and Path(extra["ppt_path"]).exists():
                    result["pptx_bytes"] = Path(extra["ppt_path"]).read_bytes()
                if "excel_path" in extra and Path(extra["excel_path"]).exists():
                    result["xlsx_bytes"] = Path(extra["excel_path"]).read_bytes()

                st.session_state.agent2_result = result
                st.session_state.audit_plan_context = text_out
                st.success("Plan d'audit généré.")
            except Exception as e:
                st.error(f"Erreur : {e}")

    if st.session_state.agent2_result:
        res = st.session_state.agent2_result
        st.markdown("---")
        tabs = st.tabs(["Plan d'audit", "Téléchargements"])
        with tabs[0]:
            if res.get("text"):
                st.markdown(f'<div class="output-box">{res["text"]}</div>', unsafe_allow_html=True)
        with tabs[1]:
            col_a, col_b = st.columns(2)
            with col_a:
                if res.get("pptx_bytes"):
                    st.download_button("⬇ Plan d'audit (.pptx)", data=res["pptx_bytes"],
                        file_name=f"Audit_Plan_{audit_topic_2.replace(' ','_')}.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
            with col_b:
                if res.get("xlsx_bytes"):
                    st.download_button("⬇ Procédures détaillées (.xlsx)", data=res["xlsx_bytes"],
                        file_name=f"Audit_Procedures_{audit_topic_2.replace(' ','_')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ═════════════════════════════════════════════════════════════════════════════
# AGENT 3
# ═════════════════════════════════════════════════════════════════════════════
elif "Agent 3" in agent_choice:
    st.markdown("""
    <div class="page-header">
      <h1>Audit Report</h1>
      <p>Rédige un rapport d'audit formel aligné IIA à partir de vos observations et findings, exporté en Word professionnel.</p>
    </div>
    """, unsafe_allow_html=True)

    audit_name = st.text_input(
        "Nom de l'audit",
        placeholder="Ex : Audit AML/KYC — Groupe Banque Privée — 2025",
    )

    observations = st.text_area(
        "Observations et findings",
        placeholder="""Ex :

1. Le processus de surveillance des transactions ne couvre pas les virements inférieurs à CHF 10'000 — risque de fractionnement non détecté.
2. Les dossiers KYC de 12 clients sur 50 testés sont incomplets (informations bénéficiaires effectifs manquantes).
3. Absence de procédure documentée pour les clients PEP dans l'entité de Singapour.""",
        height=220,
    )

    col_op, col_lang = st.columns([2, 1])
    with col_op:
        audit_opinion = st.select_slider(
            "Opinion d'audit",
            options=["Satisfactory", "Needs Improvement", "Unsatisfactory", "Critical"],
            value="Needs Improvement",
        )
    with col_lang:
        report_lang = st.radio("Langue", options=["Français", "English"], horizontal=True)

    st.markdown("<div style='margin-top:0.4rem'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    include_exec_summary   = c1.checkbox("Résumé exécutif", value=True)
    include_findings_table = c2.checkbox("Tableau findings", value=True)
    include_recommendations = c3.checkbox("Recommandations", value=True)
    include_action_plan    = c4.checkbox("Plan d'action", value=True)

    uploaded_files_3 = st.file_uploader(
        "Documents à analyser *(optionnel — issues log, workpapers, APM…)*",
        type=["pdf", "docx", "xlsx", "txt"],
        accept_multiple_files=True,
        key="upload3",
    )

    st.markdown("<div style='margin-top:1.4rem'></div>", unsafe_allow_html=True)
    run_agent3 = st.button("Générer le rapport", type="primary",
                           disabled=not api_key or not audit_name or not observations or not AGENTS_OK)

    if run_agent3:
        with st.spinner("Rédaction du rapport d'audit en cours…"):
            try:
                client = _make_client(api_key)
                file_ids_mimes = []
                for uf in (uploaded_files_3 or []):
                    fid_mime = _upload_streamlit_file(client, uf)
                    if fid_mime:
                        file_ids_mimes.append(fid_mime)

                options_str = ", ".join(filter(None, [
                    "executive summary" if include_exec_summary else "",
                    "findings table" if include_findings_table else "",
                    "recommendations" if include_recommendations else "",
                    "action plan" if include_action_plan else "",
                ]))
                lang_str = "French" if report_lang == "Français" else "English"

                user_content: list = []
                if file_ids_mimes:
                    user_content.extend(build_file_content_blocks(file_ids_mimes))
                    user_content.append({"type": "text",
                        "text": f"I have uploaded {len(file_ids_mimes)} document(s) with audit evidence."})

                reg_ctx = ""
                if st.session_state.reg_context:
                    reg_ctx = f"\n\nRegulatory context:\n{st.session_state.reg_context[:2000]}"

                user_content.append({"type": "text", "text": (
                    f"Draft a professional audit report:\n\n"
                    f"**Report Title:** {audit_name}\n"
                    f"**Language:** {lang_str}\n"
                    f"**Suggested Opinion:** {audit_opinion}\n"
                    f"**Include:** {options_str}\n"
                    f"{reg_ctx}\n\n"
                    f"**Observations and findings:**\n{observations}\n\n"
                    f"Structure each finding with risk rating, impact, root cause, recommendation, "
                    f"and target date. Order by severity. Then call `generate_audit_report` to export."
                )})

                messages = [{"role": "user", "content": user_content}]

                def _handle_a3(tool_name, tool_input):
                    if tool_name == "generate_audit_report":
                        try:
                            path = generate_audit_report_docx(tool_input, OUTPUT_DIR)
                            return f"Report saved: {path}", {"docx_path": path}
                        except Exception as e:
                            return f"Error: {e}", {}
                    return "Unknown tool", {}

                text_out, extra = _agentic_loop(
                    client, _a3.SYSTEM_PROMPT, _a3.TOOLS, messages, _handle_a3)

                result = {"text": text_out}
                if "docx_path" in extra and Path(extra["docx_path"]).exists():
                    result["docx_bytes"] = Path(extra["docx_path"]).read_bytes()

                st.session_state.agent3_result = result
                st.success("Rapport généré.")
            except Exception as e:
                st.error(f"Erreur : {e}")

    if st.session_state.agent3_result:
        res = st.session_state.agent3_result
        st.markdown("---")
        tabs = st.tabs(["Aperçu du rapport", "Téléchargement Word"])
        with tabs[0]:
            if res.get("text"):
                st.markdown(f'<div class="output-box">{res["text"]}</div>', unsafe_allow_html=True)
        with tabs[1]:
            fname = f"Rapport_Audit_{audit_name.replace(' ','_')}.docx" if audit_name else "Rapport_Audit.docx"
            if res.get("docx_bytes"):
                st.download_button("⬇ Télécharger le rapport (.docx)", data=res["docx_bytes"],
                    file_name=fname,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            else:
                st.info("Le fichier Word sera disponible après génération.")

        st.markdown("---")
        st.markdown("**Demander une révision**")
        followup = st.text_area(
            "Instruction",
            placeholder="Ex : Reformule la recommandation 3 de manière plus ferme. Ajoute un paragraphe sur le risque résiduel.",
            height=80,
            label_visibility="collapsed",
        )
        if st.button("Réviser le rapport", disabled=not followup or not api_key or not AGENTS_OK):
            with st.spinner("Révision en cours…"):
                try:
                    client = _make_client(api_key)
                    prior_text = res.get("text", "")[:2000]
                    rev_content = [{"type": "text", "text":
                        f"Previous report:\n{prior_text}\n\nRevision requested: {followup}\n\n"
                        f"Apply the revision and call `generate_audit_report` to export the updated report."}]
                    messages2 = [{"role": "user", "content": rev_content}]

                    def _handle_a3_rev(tool_name, tool_input):
                        if tool_name == "generate_audit_report":
                            try:
                                path = generate_audit_report_docx(tool_input, OUTPUT_DIR)
                                return f"Updated report saved: {path}", {"docx_path": path}
                            except Exception as e:
                                return f"Error: {e}", {}
                        return "Unknown tool", {}

                    text_out2, extra2 = _agentic_loop(
                        client, _a3.SYSTEM_PROMPT, _a3.TOOLS, messages2, _handle_a3_rev)

                    result2 = {"text": text_out2}
                    if "docx_path" in extra2 and Path(extra2["docx_path"]).exists():
                        result2["docx_bytes"] = Path(extra2["docx_path"]).read_bytes()
                    st.session_state.agent3_result = result2
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur : {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p class="footer">AuditIQ · Système multi-agents · Banque Privée · CH · SG · HK · Bahamas · EU · UK</p>',
    unsafe_allow_html=True,
)
