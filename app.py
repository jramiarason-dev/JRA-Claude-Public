"""
AuditIQ — Interface Streamlit pour les 3 agents d'audit
Posez ce fichier à la racine de votre repo, à côté de main.py
"""

import streamlit as st
import os
import tempfile
from pathlib import Path

# ── Configuration de la page ──────────────────────────────────────────────────
st.set_page_config(
    page_title="AuditIQ — Agents d'audit",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personnalisé ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0d0f18; }
    .stApp { background-color: #0d0f18; color: #e4e8f5; }
    section[data-testid="stSidebar"] { background-color: #13172a; border-right: 1px solid rgba(255,255,255,0.07); }
    .agent-card { background: #181d30; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
    .agent-title { font-size: 16px; font-weight: 700; margin-bottom: 6px; }
    .agent-desc { font-size: 13px; color: #8b95b8; line-height: 1.6; }
    .output-box { background: #181d30; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 16px; font-size: 13px; line-height: 1.8; white-space: pre-wrap; }
    .status-ok { color: #34d399; font-weight: 600; }
    .status-err { color: #fb7185; font-weight: 600; }
    div[data-testid="stDownloadButton"] button { background: #1e3a5f; color: #5b8df6; border: 1px solid rgba(91,141,246,0.4); border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ── Vérification des imports agents ──────────────────────────────────────────
AGENTS_OK = False
try:
    from agent1_regulatory import Agent1Regulatory
    from agent2_audit_plan import Agent2AuditPlan
    from agent3_report import Agent3Report
    AGENTS_OK = True
except ImportError as e:
    pass  # géré dans l'UI

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏦 AuditIQ")
    st.markdown("**Système multi-agents d'audit**")
    st.markdown("---")

    # Clé API
    st.markdown("### 🔑 Configuration")
    api_key = st.text_input(
        "Clé API Anthropic",
        type="password",
        value=os.environ.get("ANTHROPIC_API_KEY", ""),
        placeholder="sk-ant-...",
        help="Votre clé API Anthropic. Elle n'est jamais stockée.",
    )
    if api_key:
        os.environ["ANTHROPIC_API_KEY"] = api_key
        st.markdown('<p class="status-ok">✓ Clé API configurée</p>', unsafe_allow_html=True)
    else:
        st.warning("Entrez votre clé API pour commencer.")

    st.markdown("---")

    # Navigation
    st.markdown("### 📂 Agents")
    agent_choice = st.radio(
        "Sélectionnez un agent",
        options=[
            "🧭 Agent 1 — Regulatory Framework",
            "📋 Agent 2 — Audit Plan",
            "📄 Agent 3 — Audit Report",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### ℹ️ Juridictions couvertes")
    st.markdown("""
    🇨🇭 Suisse / FINMA  
    🇸🇬 Singapour / MAS  
    🇭🇰 Hong Kong / SFC+HKMA  
    🇧🇸 Bahamas / SCB  
    🇪🇺 Europe / EU  
    🇬🇧 Royaume-Uni / FCA+PRA  
    """)

    if not AGENTS_OK:
        st.markdown("---")
        st.error("⚠️ Agents non trouvés. Vérifiez que `app.py` est dans le même dossier que vos agents.")

# ── Contexte partagé entre agents (session state) ─────────────────────────────
if "reg_context" not in st.session_state:
    st.session_state.reg_context = ""
if "audit_plan_context" not in st.session_state:
    st.session_state.audit_plan_context = ""
if "agent1_result" not in st.session_state:
    st.session_state.agent1_result = None
if "agent2_result" not in st.session_state:
    st.session_state.agent2_result = None
if "agent3_result" not in st.session_state:
    st.session_state.agent3_result = None

# ═════════════════════════════════════════════════════════════════════════════
# AGENT 1 — REGULATORY FRAMEWORK
# ═════════════════════════════════════════════════════════════════════════════
if "Agent 1" in agent_choice:
    st.markdown("# 🧭 Agent 1 — Regulatory Framework")
    st.markdown("Compile toutes les lois, réglementations et guidelines applicables pour un sujet d'audit donné, sur 6 juridictions.")

    col1, col2 = st.columns([2, 1])

    with col1:
        audit_topic = st.text_input(
            "Sujet d'audit",
            placeholder="Ex: AML/KYC, Credit Risk, Cybersecurity, Operational Risk…",
        )

        jurisdictions = st.multiselect(
            "Juridictions à couvrir",
            options=["CH/FINMA", "SG/MAS", "HK/SFC+HKMA", "Bahamas/SCB", "EU", "UK/FCA+PRA"],
            default=["CH/FINMA", "SG/MAS", "HK/SFC+HKMA", "Bahamas/SCB", "EU", "UK/FCA+PRA"],
        )

        focus_areas = st.multiselect(
            "Domaines prioritaires",
            options=["AML/CFT", "KYC/CDD", "Risque opérationnel", "Cybersécurité", "Gouvernance", "Reporting", "Gestion des risques", "Protection des données"],
            default=[],
        )

    with col2:
        st.markdown("**📎 Document optionnel**")
        uploaded_file = st.file_uploader(
            "Upload (PDF, Word, Excel, TXT)",
            type=["pdf", "docx", "xlsx", "txt"],
            help="Le document sera analysé par l'agent pour enrichir le contexte réglementaire.",
        )

    st.markdown("---")

    run_agent1 = st.button("▶ Lancer l'Agent 1", type="primary", disabled=not api_key or not audit_topic)

    if run_agent1:
        if not AGENTS_OK:
            st.error("Les fichiers agents (agent1_regulatory.py etc.) ne sont pas trouvés dans ce dossier.")
        else:
            with st.spinner("🔍 Agent 1 en cours — compilation du cadre réglementaire…"):
                try:
                    agent = Agent1Regulatory()

                    # Upload du fichier si présent
                    file_id = None
                    if uploaded_file:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
                            tmp.write(uploaded_file.read())
                            tmp_path = tmp.name
                        file_id = agent.upload_file(tmp_path)
                        os.unlink(tmp_path)

                    # Construction du prompt
                    jur_str = ", ".join(jurisdictions)
                    focus_str = ", ".join(focus_areas) if focus_areas else "tous domaines"
                    prompt = f"Audit topic: {audit_topic}. Jurisdictions: {jur_str}. Focus: {focus_str}."

                    # Appel de l'agent
                    result = agent.run(prompt, file_id=file_id)

                    st.session_state.agent1_result = result
                    st.session_state.reg_context = result.get("text", "")

                    st.success("✅ Agent 1 terminé !")

                except Exception as e:
                    st.error(f"Erreur : {e}")

    # Affichage des résultats
    if st.session_state.agent1_result:
        res = st.session_state.agent1_result
        st.markdown("### 📊 Résultats")

        tabs = st.tabs(["📝 Contenu réglementaire", "📥 Téléchargements"])

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
                    "⬇️ Télécharger le Regulatory Framework (.docx)",
                    data=docx_bytes,
                    file_name=f"Regulatory_Framework_{audit_topic.replace(' ','_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            else:
                docx_path = res.get("docx_path")
                if docx_path and os.path.exists(docx_path):
                    with open(docx_path, "rb") as f:
                        st.download_button(
                            "⬇️ Télécharger le Regulatory Framework (.docx)",
                            data=f.read(),
                            file_name=f"Regulatory_Framework_{audit_topic.replace(' ','_')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        )

        st.info("💡 Le contexte réglementaire de l'Agent 1 est automatiquement transmis à l'Agent 2.")

# ═════════════════════════════════════════════════════════════════════════════
# AGENT 2 — AUDIT PLAN
# ═════════════════════════════════════════════════════════════════════════════
elif "Agent 2" in agent_choice:
    st.markdown("# 📋 Agent 2 — Audit Plan")
    st.markdown("Génère le plan d'audit (PowerPoint) et les procédures détaillées avec tests, tailles d'échantillon et évaluations de risques (Excel).")

    # Contexte de l'Agent 1
    if st.session_state.reg_context:
        st.success("✅ Contexte réglementaire de l'Agent 1 disponible et sera utilisé automatiquement.")
    else:
        st.warning("⚠️ Aucun contexte de l'Agent 1. Lancez d'abord l'Agent 1, ou entrez le sujet manuellement.")

    col1, col2 = st.columns([2, 1])

    with col1:
        audit_topic_2 = st.text_input(
            "Sujet d'audit",
            placeholder="Ex: AML/KYC, Credit Risk, Cybersecurity…",
        )

        risk_appetite = st.select_slider(
            "Appétit au risque de l'organisation",
            options=["Très faible", "Faible", "Modéré", "Élevé", "Très élevé"],
            value="Modéré",
        )

        audit_scope = st.text_area(
            "Périmètre de l'audit",
            placeholder="Ex: Toutes les entités du groupe en Suisse, Singapour et Hong Kong. Focus sur les processus onboarding et transaction monitoring.",
            height=100,
        )

    with col2:
        st.markdown("**📎 Document optionnel**")
        uploaded_file_2 = st.file_uploader(
            "Upload (PDF, Word, Excel, TXT)",
            type=["pdf", "docx", "xlsx", "txt"],
            key="upload2",
        )

        output_options = st.multiselect(
            "Outputs à générer",
            options=["PowerPoint (plan d'audit)", "Excel (procédures détaillées)"],
            default=["PowerPoint (plan d'audit)", "Excel (procédures détaillées)"],
        )

    st.markdown("---")

    run_agent2 = st.button("▶ Lancer l'Agent 2", type="primary", disabled=not api_key or not audit_topic_2)

    if run_agent2:
        if not AGENTS_OK:
            st.error("Les fichiers agents ne sont pas trouvés dans ce dossier.")
        else:
            with st.spinner("📋 Agent 2 en cours — génération du plan d'audit…"):
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

                    st.success("✅ Agent 2 terminé !")

                except Exception as e:
                    st.error(f"Erreur : {e}")

    # Résultats
    if st.session_state.agent2_result:
        res = st.session_state.agent2_result
        st.markdown("### 📊 Résultats")

        tabs = st.tabs(["📝 Plan d'audit", "📥 Téléchargements"])

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
                    st.download_button("⬇️ Plan d'audit (.pptx)", data=pptx_bytes,
                        file_name=f"Audit_Plan_{audit_topic_2.replace(' ','_')}.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
                elif pptx_path and os.path.exists(pptx_path):
                    with open(pptx_path, "rb") as f:
                        st.download_button("⬇️ Plan d'audit (.pptx)", data=f.read(),
                            file_name=f"Audit_Plan_{audit_topic_2.replace(' ','_')}.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")

            with col_b:
                xlsx_bytes = res.get("xlsx_bytes")
                xlsx_path = res.get("xlsx_path")
                if xlsx_bytes:
                    st.download_button("⬇️ Procédures détaillées (.xlsx)", data=xlsx_bytes,
                        file_name=f"Audit_Procedures_{audit_topic_2.replace(' ','_')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                elif xlsx_path and os.path.exists(xlsx_path):
                    with open(xlsx_path, "rb") as f:
                        st.download_button("⬇️ Procédures détaillées (.xlsx)", data=f.read(),
                            file_name=f"Audit_Procedures_{audit_topic_2.replace(' ','_')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ═════════════════════════════════════════════════════════════════════════════
# AGENT 3 — AUDIT REPORT
# ═════════════════════════════════════════════════════════════════════════════
elif "Agent 3" in agent_choice:
    st.markdown("# 📄 Agent 3 — Audit Report")
    st.markdown("Rédige un rapport d'audit formel aligné IIA à partir de vos observations et findings, exporté en Word professionnel.")

    col1, col2 = st.columns([2, 1])

    with col1:
        audit_name = st.text_input(
            "Nom de l'audit",
            placeholder="Ex: Audit AML/KYC — Groupe Banque Privée — 2025",
        )

        observations = st.text_area(
            "Observations et findings",
            placeholder="""Entrez vos observations ici. Par exemple :

1. Le processus de surveillance des transactions ne couvre pas les virements inférieurs à CHF 10'000 — risque de fractionnement non détecté.
2. Les dossiers KYC de 12 clients sur 50 testés sont incomplets (informations bénéficiaires effectifs manquantes).
3. Absence de procédure documentée pour les clients PEP dans l'entité de Singapour.
...""",
            height=250,
        )

        audit_opinion = st.select_slider(
            "Opinion d'audit proposée",
            options=["Satisfaisant", "Partiellement satisfaisant", "Insatisfaisant"],
            value="Partiellement satisfaisant",
        )

        report_lang = st.radio("Langue du rapport", options=["Français", "English"], horizontal=True)

    with col2:
        st.markdown("**📎 Documents à analyser**")
        uploaded_files_3 = st.file_uploader(
            "Issues log, workpapers, APM… (PDF, Word, Excel, TXT)",
            type=["pdf", "docx", "xlsx", "txt"],
            accept_multiple_files=True,
            key="upload3",
        )

        st.markdown("**⚙️ Options du rapport**")
        include_exec_summary = st.checkbox("Résumé exécutif", value=True)
        include_findings_table = st.checkbox("Tableau des findings", value=True)
        include_recommendations = st.checkbox("Recommandations", value=True)
        include_action_plan = st.checkbox("Plan d'action", value=True)

    st.markdown("---")

    run_agent3 = st.button("▶ Lancer l'Agent 3", type="primary",
        disabled=not api_key or not audit_name or not observations)

    if run_agent3:
        if not AGENTS_OK:
            st.error("Les fichiers agents ne sont pas trouvés dans ce dossier.")
        else:
            with st.spinner("📄 Agent 3 en cours — rédaction du rapport d'audit…"):
                try:
                    agent = Agent3Report()

                    # Upload des fichiers
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
                    prompt = f"""
Audit name: {audit_name}
Language: {lang_str}
Audit opinion: {audit_opinion}
Include: {options_str}

Observations and findings:
{observations}
"""
                    if st.session_state.reg_context:
                        prompt += f"\n\nRegulatory context:\n{st.session_state.reg_context[:2000]}"

                    result = agent.run(prompt, file_ids=file_ids if file_ids else None)
                    st.session_state.agent3_result = result

                    st.success("✅ Rapport généré !")

                except Exception as e:
                    st.error(f"Erreur : {e}")

    # Résultats
    if st.session_state.agent3_result:
        res = st.session_state.agent3_result
        st.markdown("### 📊 Résultats")

        tabs = st.tabs(["📝 Aperçu du rapport", "📥 Téléchargement Word"])

        with tabs[0]:
            text_content = res.get("text", "")
            if text_content:
                st.markdown(f'<div class="output-box">{text_content}</div>', unsafe_allow_html=True)

        with tabs[1]:
            docx_bytes = res.get("docx_bytes")
            docx_path = res.get("docx_path")
            fname = f"Rapport_Audit_{audit_name.replace(' ','_')}.docx" if audit_name else "Rapport_Audit.docx"

            if docx_bytes:
                st.download_button("⬇️ Télécharger le rapport (.docx)", data=docx_bytes,
                    file_name=fname,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            elif docx_path and os.path.exists(docx_path):
                with open(docx_path, "rb") as f:
                    st.download_button("⬇️ Télécharger le rapport (.docx)", data=f.read(),
                        file_name=fname,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            else:
                st.info("Le fichier Word sera disponible dans le dossier de l'application.")

        # Follow-up / révision
        st.markdown("---")
        st.markdown("### 💬 Demander une révision")
        followup = st.text_area("Instruction de révision", placeholder="Ex: Reformule la recommandation 3 de manière plus ferme. Ajoute un paragraphe sur le risque résiduel.")
        if st.button("▶ Réviser le rapport", disabled=not followup or not api_key):
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
    '<p style="font-size:11px;color:#4d5780;text-align:center">AuditIQ · Système multi-agents · Banque Privée · '
    'CH · SG · HK · Bahamas · EU · UK</p>',
    unsafe_allow_html=True
)
