"""
AuditIQ — Interface Streamlit pour les 3 agents d'audit
"""

import streamlit as st
import os
import tempfile
from pathlib import Path

st.set_page_config(
    page_title="AuditIQ",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  /* ── Base ── */
  html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
  .stApp { background-color: #080b12; color: #dde3f5; }
  .main .block-container { padding: 2.5rem 3rem 4rem; max-width: 860px; }

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {
    background-color: #0c0f1a;
    border-right: 1px solid rgba(255,255,255,0.05);
  }
  section[data-testid="stSidebar"] .block-container { padding: 2rem 1.4rem; }

  /* ── Logo / Brand ── */
  .brand { display: flex; align-items: center; gap: 10px; margin-bottom: 1.8rem; }
  .brand-icon { font-size: 22px; }
  .brand-name { font-size: 18px; font-weight: 700; letter-spacing: -0.3px; color: #e8edf8; }
  .brand-sub { font-size: 11px; color: #424d72; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 1px; }

  /* ── Sidebar nav ── */
  .nav-label { font-size: 10px; font-weight: 600; color: #3a4566; text-transform: uppercase;
               letter-spacing: 1px; margin: 1.6rem 0 0.6rem; }
  div[data-testid="stRadio"] label { font-size: 13.5px !important; }
  div[data-testid="stRadio"] > div { gap: 2px !important; }

  /* ── API key status ── */
  .api-ok   { display:inline-flex; align-items:center; gap:6px; color:#22d3a5;
              font-size:12px; font-weight:600; background:rgba(34,211,165,0.08);
              border:1px solid rgba(34,211,165,0.2); border-radius:6px; padding:5px 10px; }
  .api-miss { display:inline-flex; align-items:center; gap:6px; color:#f59e0b;
              font-size:12px; font-weight:600; background:rgba(245,158,11,0.08);
              border:1px solid rgba(245,158,11,0.2); border-radius:6px; padding:5px 10px; }

  /* ── Jurisdiction badges ── */
  .jur-grid { display:flex; flex-wrap:wrap; gap:6px; margin-top: 8px; }
  .jur-badge { font-size:11px; color:#8392bb; background:rgba(255,255,255,0.04);
               border:1px solid rgba(255,255,255,0.07); border-radius:5px; padding:3px 8px; }

  /* ── Page header ── */
  .page-header { margin-bottom: 2rem; }
  .page-header h1 { font-size:24px; font-weight:700; color:#e8edf8; margin:0 0 6px;
                    letter-spacing:-0.4px; }
  .page-header p  { font-size:13.5px; color:#5a6488; margin:0; line-height:1.6; }

  /* ── Section label ── */
  .section-label { font-size:11px; font-weight:600; color:#3a4566; text-transform:uppercase;
                   letter-spacing:0.9px; margin-bottom:10px; }

  /* ── Input fields ── */
  .stTextInput input, .stTextArea textarea, .stSelectbox select {
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

  /* ── Select slider ── */
  div[data-testid="stSlider"] .stSlider { margin-top: 4px; }

  /* ── File uploader ── */
  div[data-testid="stFileUploader"] {
    border: 1px dashed rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    background: #10141f !important;
  }
  div[data-testid="stFileUploader"] button { font-size:12px !important; }

  /* ── Primary button ── */
  div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #2d54d4 0%, #4f7ef8 100%);
    border: none;
    border-radius: 9px;
    color: #ffffff;
    font-size: 13.5px;
    font-weight: 600;
    padding: 10px 24px;
    letter-spacing: 0.1px;
    transition: opacity 0.15s;
  }
  div[data-testid="stButton"] > button[kind="primary"]:hover { opacity: 0.88; }
  div[data-testid="stButton"] > button[kind="primary"]:disabled {
    background: #1a1f32 !important; color: #3a4566 !important; }

  /* ── Secondary button ── */
  div[data-testid="stButton"] > button[kind="secondary"] {
    background: transparent;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 9px;
    color: #8392bb;
    font-size: 13px;
    padding: 8px 18px;
  }

  /* ── Download button ── */
  div[data-testid="stDownloadButton"] button {
    background: rgba(79,126,248,0.1);
    color: #7fa8fb;
    border: 1px solid rgba(79,126,248,0.25);
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
  }
  div[data-testid="stDownloadButton"] button:hover { background: rgba(79,126,248,0.18); }

  /* ── Divider ── */
  hr { border: none; border-top: 1px solid rgba(255,255,255,0.05) !important; margin: 1.8rem 0; }

  /* ── Alert / info boxes ── */
  div[data-testid="stAlert"] { border-radius: 9px !important; font-size: 13px !important; }

  /* ── Tabs ── */
  button[data-baseweb="tab"] { font-size: 13px !important; color: #5a6488 !important; }
  button[data-baseweb="tab"][aria-selected="true"] { color: #a0b4f8 !important; }

  /* ── Output box ── */
  .output-box {
    background: #0f121e;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 20px;
    font-size: 13px;
    line-height: 1.85;
    white-space: pre-wrap;
    color: #c8d0e8;
    max-height: 520px;
    overflow-y: auto;
  }

  /* ── Context pill ── */
  .ctx-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(34,211,165,0.07); border: 1px solid rgba(34,211,165,0.18);
    color: #22d3a5; border-radius: 8px; padding: 7px 14px; font-size: 12.5px; font-weight:500;
    margin-bottom: 1.6rem;
  }
  .ctx-miss {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(245,158,11,0.07); border: 1px solid rgba(245,158,11,0.2);
    color: #f59e0b; border-radius: 8px; padding: 7px 14px; font-size: 12.5px; font-weight:500;
    margin-bottom: 1.6rem;
  }

  /* ── Risk slider label ── */
  div[data-testid="stSelectSlider"] > div > div { font-size: 12px !important; }

  /* ── Checkbox ── */
  label[data-testid="stCheckbox"] p { font-size:13px !important; color:#8392bb !important; }

  /* ── Radio horizontal ── */
  div[data-testid="stRadio"][data-horizontal="true"] label { font-size:13px !important; }

  /* ── Footer ── */
  .footer { font-size:11px; color:#262e47; text-align:center; margin-top:3rem; letter-spacing:0.3px; }

  /* ── Spinner ── */
  div[data-testid="stSpinner"] p { font-size: 13px !important; color: #5a6488 !important; }
</style>
""", unsafe_allow_html=True)

# ── Agent imports ─────────────────────────────────────────────────────────────
AGENTS_OK = False
try:
    from agent1_regulatory import Agent1Regulatory
    from agent2_audit_plan import Agent2AuditPlan
    from agent3_report import Agent3Report
    AGENTS_OK = True
except ImportError:
    pass

JURISDICTIONS = ["CH / FINMA", "SG / MAS", "HK / SFC+HKMA", "Bahamas / SCB", "EU", "UK / FCA+PRA"]

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
        st.error("Agents non trouvés. Vérifiez que `app.py` est dans le dossier des agents.")

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
                           disabled=not api_key or not audit_topic)

    if run_agent1:
        if not AGENTS_OK:
            st.error("Les fichiers agents ne sont pas trouvés dans ce dossier.")
        else:
            with st.spinner("Compilation du cadre réglementaire en cours…"):
                try:
                    agent = Agent1Regulatory()
                    file_id = None
                    if uploaded_file:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
                            tmp.write(uploaded_file.read())
                            tmp_path = tmp.name
                        file_id = agent.upload_file(tmp_path)
                        os.unlink(tmp_path)

                    jur_str = ", ".join(JURISDICTIONS)
                    focus_str = ", ".join(focus_areas) if focus_areas else "tous domaines"
                    prompt = f"Audit topic: {audit_topic}. Jurisdictions: {jur_str}. Focus: {focus_str}."
                    result = agent.run(prompt, file_id=file_id)

                    st.session_state.agent1_result = result
                    st.session_state.reg_context = result.get("text", "")
                    st.success("Analyse terminée.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

    if st.session_state.agent1_result:
        res = st.session_state.agent1_result
        st.markdown("---")
        tabs = st.tabs(["Contenu réglementaire", "Téléchargement"])

        with tabs[0]:
            text_content = res.get("text", "")
            if text_content:
                st.markdown(f'<div class="output-box">{text_content}</div>', unsafe_allow_html=True)
            else:
                st.info("Le contenu réglementaire a été exporté directement en Word.")

        with tabs[1]:
            docx_bytes = res.get("docx_bytes")
            if docx_bytes:
                st.download_button(
                    "⬇ Télécharger le Regulatory Framework (.docx)",
                    data=docx_bytes,
                    file_name=f"Regulatory_Framework_{audit_topic.replace(' ','_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            else:
                docx_path = res.get("docx_path")
                if docx_path and os.path.exists(docx_path):
                    with open(docx_path, "rb") as f:
                        st.download_button(
                            "⬇ Télécharger le Regulatory Framework (.docx)",
                            data=f.read(),
                            file_name=f"Regulatory_Framework_{audit_topic.replace(' ','_')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        )

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
        st.markdown('<div class="ctx-miss">⚠ Aucun contexte Agent 1 — lancez d\'abord l\'Agent 1 ou saisissez le sujet manuellement</div>', unsafe_allow_html=True)

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
                           disabled=not api_key or not audit_topic_2)

    if run_agent2:
        if not AGENTS_OK:
            st.error("Les fichiers agents ne sont pas trouvés dans ce dossier.")
        else:
            with st.spinner("Génération du plan d'audit en cours…"):
                try:
                    agent = Agent2AuditPlan()
                    file_id = None
                    if uploaded_file_2:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file_2.name).suffix) as tmp:
                            tmp.write(uploaded_file_2.read())
                            tmp_path = tmp.name
                        file_id = agent.upload_file(tmp_path)
                        os.unlink(tmp_path)

                    prompt = f"Audit topic: {audit_topic_2}. Risk appetite: {risk_appetite}. Scope: {audit_scope}."
                    if st.session_state.reg_context:
                        prompt += f"\n\nRegulatory context from Agent 1:\n{st.session_state.reg_context[:3000]}"

                    result = agent.run(prompt, file_id=file_id)
                    st.session_state.agent2_result = result
                    st.session_state.audit_plan_context = result.get("text", "")
                    st.success("Plan d'audit généré.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

    if st.session_state.agent2_result:
        res = st.session_state.agent2_result
        st.markdown("---")
        tabs = st.tabs(["Plan d'audit", "Téléchargements"])

        with tabs[0]:
            text_content = res.get("text", "")
            if text_content:
                st.markdown(f'<div class="output-box">{text_content}</div>', unsafe_allow_html=True)

        with tabs[1]:
            col_a, col_b = st.columns(2)
            with col_a:
                pptx_bytes = res.get("pptx_bytes")
                pptx_path = res.get("pptx_path")
                if pptx_bytes:
                    st.download_button("⬇ Plan d'audit (.pptx)", data=pptx_bytes,
                        file_name=f"Audit_Plan_{audit_topic_2.replace(' ','_')}.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
                elif pptx_path and os.path.exists(pptx_path):
                    with open(pptx_path, "rb") as f:
                        st.download_button("⬇ Plan d'audit (.pptx)", data=f.read(),
                            file_name=f"Audit_Plan_{audit_topic_2.replace(' ','_')}.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
            with col_b:
                xlsx_bytes = res.get("xlsx_bytes")
                xlsx_path = res.get("xlsx_path")
                if xlsx_bytes:
                    st.download_button("⬇ Procédures détaillées (.xlsx)", data=xlsx_bytes,
                        file_name=f"Audit_Procedures_{audit_topic_2.replace(' ','_')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                elif xlsx_path and os.path.exists(xlsx_path):
                    with open(xlsx_path, "rb") as f:
                        st.download_button("⬇ Procédures détaillées (.xlsx)", data=f.read(),
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
            options=["Satisfaisant", "Partiellement satisfaisant", "Insatisfaisant"],
            value="Partiellement satisfaisant",
        )
    with col_lang:
        report_lang = st.radio("Langue", options=["Français", "English"], horizontal=True)

    st.markdown("<div style='margin-top:0.4rem'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    include_exec_summary  = c1.checkbox("Résumé exécutif", value=True)
    include_findings_table = c2.checkbox("Tableau findings", value=True)
    include_recommendations = c3.checkbox("Recommandations", value=True)
    include_action_plan   = c4.checkbox("Plan d'action", value=True)

    uploaded_files_3 = st.file_uploader(
        "Documents à analyser *(optionnel — issues log, workpapers, APM…)*",
        type=["pdf", "docx", "xlsx", "txt"],
        accept_multiple_files=True,
        key="upload3",
    )

    st.markdown("<div style='margin-top:1.4rem'></div>", unsafe_allow_html=True)
    run_agent3 = st.button("Générer le rapport", type="primary",
                           disabled=not api_key or not audit_name or not observations)

    if run_agent3:
        if not AGENTS_OK:
            st.error("Les fichiers agents ne sont pas trouvés dans ce dossier.")
        else:
            with st.spinner("Rédaction du rapport d'audit en cours…"):
                try:
                    agent = Agent3Report()
                    file_ids = []
                    for uf in (uploaded_files_3 or []):
                        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uf.name).suffix) as tmp:
                            tmp.write(uf.read())
                            tmp_path = tmp.name
                        fid = agent.upload_file(tmp_path)
                        if fid:
                            file_ids.append(fid)
                        os.unlink(tmp_path)

                    options_str = ", ".join(filter(None, [
                        "executive summary" if include_exec_summary else "",
                        "findings table" if include_findings_table else "",
                        "recommendations" if include_recommendations else "",
                        "action plan" if include_action_plan else "",
                    ]))
                    lang_str = "French" if report_lang == "Français" else "English"
                    prompt = f"Audit name: {audit_name}\nLanguage: {lang_str}\nAudit opinion: {audit_opinion}\nInclude: {options_str}\n\nObservations and findings:\n{observations}"
                    if st.session_state.reg_context:
                        prompt += f"\n\nRegulatory context:\n{st.session_state.reg_context[:2000]}"

                    result = agent.run(prompt, file_ids=file_ids if file_ids else None)
                    st.session_state.agent3_result = result
                    st.success("Rapport généré.")
                except Exception as e:
                    st.error(f"Erreur : {e}")

    if st.session_state.agent3_result:
        res = st.session_state.agent3_result
        st.markdown("---")
        tabs = st.tabs(["Aperçu du rapport", "Téléchargement Word"])

        with tabs[0]:
            text_content = res.get("text", "")
            if text_content:
                st.markdown(f'<div class="output-box">{text_content}</div>', unsafe_allow_html=True)

        with tabs[1]:
            fname = f"Rapport_Audit_{audit_name.replace(' ','_')}.docx" if audit_name else "Rapport_Audit.docx"
            docx_bytes = res.get("docx_bytes")
            docx_path = res.get("docx_path")
            if docx_bytes:
                st.download_button("⬇ Télécharger le rapport (.docx)", data=docx_bytes,
                    file_name=fname,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            elif docx_path and os.path.exists(docx_path):
                with open(docx_path, "rb") as f:
                    st.download_button("⬇ Télécharger le rapport (.docx)", data=f.read(),
                        file_name=fname,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            else:
                st.info("Le fichier Word sera disponible dans le dossier de l'application.")

        st.markdown("---")
        st.markdown("**Demander une révision**")
        followup = st.text_area(
            "Instruction",
            placeholder="Ex : Reformule la recommandation 3 de manière plus ferme. Ajoute un paragraphe sur le risque résiduel.",
            height=80,
            label_visibility="collapsed",
        )
        if st.button("Réviser le rapport", disabled=not followup or not api_key):
            with st.spinner("Révision en cours…"):
                try:
                    agent = Agent3Report()
                    revision_prompt = f"Previous report context: {res.get('text','')[:2000]}\n\nRevision requested: {followup}"
                    result2 = agent.run(revision_prompt)
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
