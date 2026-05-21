"""Workflow D — Architecture Decision Records (ADRs)."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
from datetime import datetime

import database as db
from components.badges import status_badge
from components.forms import ai_assistant_panel, BL_OPTIONS

st.set_page_config(page_title="ADR Management — EA Governance", page_icon="📖", layout="wide")

st.markdown("""
<style>
  .stApp { background: #F4F6FA; }
  .stTabs [aria-selected="true"] { background: #1E2761; color: #fff !important; }
</style>
""", unsafe_allow_html=True)

current_user = st.session_state.get("current_user", "Head of EA")
current_role = st.session_state.get("current_role", "EA Lead")

EA_MEMBERS = [
    "Head of EA",
    "Sr EA 1 — PWM / Application",
    "Sr EA 2 — PAS / Data & Security",
    "Sr EA 3 — Ops / Process",
    "Risk & Compliance EA",
    "Cloud Architect EA",
]

TECH_DOMAINS = [
    "Application/Integration", "Data/API/Security", "Business Process/Workflow",
    "Governance/Controls", "Cloud/Infrastructure", "Cross-cutting",
]

ADR_STATUSES = ["Proposed", "Accepted", "Deprecated", "Superseded"]

st.markdown("""
<div style="background:#fff;border-radius:12px;padding:20px 24px;margin-bottom:20px;border-left:5px solid #7C3AED;">
  <h1 style="margin:0;color:#1E2761;font-size:1.6rem;">📖 Architecture Decision Records</h1>
  <p style="margin:4px 0 0;color:#6B7280;">Create, manage, and consult formal architecture decisions</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📚 Browse ADRs", "✏️ Create ADR", "🔧 Edit / Update ADR"])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: Browse
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("ADR Library")

    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        f_status = st.selectbox("Status", ["All"] + ADR_STATUSES)
    with fcol2:
        f_bl = st.selectbox("Business Line", ["All"] + BL_OPTIONS)
    with fcol3:
        f_search = st.text_input("Search title / content", placeholder="Type to search...")

    adrs = db.get_adrs(
        status=None if f_status == "All" else f_status,
        bl_domain=None if f_bl == "All" else f_bl,
    )

    if f_search:
        q = f_search.lower()
        adrs = [a for a in adrs
                if q in a.get("title","").lower()
                or q in a.get("context","").lower()
                or q in a.get("decision","").lower()]

    if not adrs:
        st.info("No ADRs match the current filters.")
    else:
        st.markdown(f"**{len(adrs)} ADR(s) found**")
        for adr in adrs:
            reviewers = json.loads(adr.get("reviewers","[]")) if adr.get("reviewers") else []
            rel_std   = json.loads(adr.get("related_standards","[]")) if adr.get("related_standards") else []

            with st.expander(
                f"**{adr['adr_number']}** — {adr['title']}  {adr['status']}",
                expanded=False
            ):
                c1, c2, c3 = st.columns(3)
                c1.markdown(status_badge(adr["status"]), unsafe_allow_html=True)
                c2.markdown(f"**BL:** {adr.get('bl_domain','')}")
                c3.markdown(f"**Domain:** {adr.get('tech_domain','')}")

                st.markdown(f"**Author:** {adr.get('author','')}  |  **Date:** {adr.get('created_at','')[:10]}")
                if reviewers:
                    st.markdown(f"**Reviewers:** {', '.join(reviewers)}")
                if rel_std:
                    st.markdown(f"**Related Standards:** {', '.join(rel_std)}")
                if adr.get("superseded_by"):
                    st.warning(f"Superseded by: **{adr['superseded_by']}**")

                st.markdown("---")
                for section, field in [
                    ("Context", "context"), ("Decision", "decision"), ("Rationale", "rationale"),
                    ("Positive Consequences", "consequences_positive"),
                    ("Negative Consequences", "consequences_negative"),
                    ("Alternatives Considered", "alternatives"),
                ]:
                    if adr.get(field):
                        st.markdown(f"**{section}**")
                        st.markdown(f"> {adr[field]}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: Create ADR
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    if current_role not in ("EA Reviewer", "EA Lead"):
        st.warning("Creating ADRs is restricted to EA team members.")
    else:
        st.subheader("Create New ADR")
        ai_assistant_panel("adr_create")

        # Load standards for multi-select
        std_list = db.get_standards()
        std_choices = [f"{s['std_id']} — {s['title']}" for s in std_list]

        # Load existing AR/EX references
        ar_refs = [r["reference"] for r in db.get_arch_reviews()]
        ex_refs = [e["reference"] for e in db.get_std_exceptions()]
        req_choices = ar_refs + ex_refs

        with st.form("adr_create_form"):
            col1, col2 = st.columns(2)
            with col1:
                adr_title  = st.text_input("ADR Title *", placeholder="e.g. Adopt Kong as API Gateway")
                adr_author = st.selectbox("Author *", EA_MEMBERS,
                                          index=EA_MEMBERS.index(current_user) if current_user in EA_MEMBERS else 0)
                adr_bl     = st.selectbox("Business Line domain", BL_OPTIONS)
            with col2:
                adr_status = st.selectbox("Initial status", ADR_STATUSES)
                adr_tech   = st.selectbox("Technology domain", TECH_DOMAINS)
                adr_reviewers = st.multiselect("Reviewers", EA_MEMBERS)

            adr_context    = st.text_area("Context *", height=100,
                                          placeholder="What situation or problem prompted this decision?")
            adr_decision   = st.text_area("Decision *", height=80,
                                          placeholder="What was decided?")
            adr_rationale  = st.text_area("Rationale *", height=100,
                                          placeholder="Why was this option chosen over alternatives?")

            c1, c2 = st.columns(2)
            with c1:
                adr_pos_cons = st.text_area("Positive consequences", height=80)
            with c2:
                adr_neg_cons = st.text_area("Negative consequences", height=80)

            adr_alternatives = st.text_area("Alternatives considered", height=80)
            adr_rel_std = st.multiselect("Related standards", std_choices)
            adr_rel_req = st.multiselect("Related requests (AR/EX)", req_choices)

            create_adr = st.form_submit_button("Create ADR →", type="primary")

        if create_adr:
            errors = []
            if not adr_title.strip():    errors.append("Title required.")
            if not adr_context.strip():  errors.append("Context required.")
            if not adr_decision.strip(): errors.append("Decision required.")
            if not adr_rationale.strip(): errors.append("Rationale required.")

            if errors:
                for e in errors: st.error(e)
            else:
                adr_number = db.next_adr_ref()
                rel_std_ids = [s.split(" — ")[0] for s in adr_rel_std]

                db.create_adr({
                    "adr_number": adr_number,
                    "title": adr_title,
                    "status": adr_status,
                    "context": adr_context,
                    "decision": adr_decision,
                    "rationale": adr_rationale,
                    "consequences_positive": adr_pos_cons,
                    "consequences_negative": adr_neg_cons,
                    "alternatives": adr_alternatives,
                    "bl_domain": adr_bl,
                    "tech_domain": adr_tech,
                    "author": adr_author,
                    "reviewers": adr_reviewers,
                    "related_standards": rel_std_ids,
                    "related_requests": adr_rel_req,
                })
                db.log_activity(current_user, "Created ADR", "adr", adr_number, adr_title)
                st.success(f"ADR **{adr_number}** created successfully!")
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: Edit / Update
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    if current_role not in ("EA Reviewer", "EA Lead"):
        st.warning("Editing ADRs is restricted to EA team members.")
    else:
        st.subheader("Edit / Update ADR")
        adrs_all = db.get_adrs()
        if not adrs_all:
            st.info("No ADRs yet.")
        else:
            adr_options = {f"{a['adr_number']} — {a['title']}": a["id"] for a in adrs_all}
            chosen = st.selectbox("Select ADR to edit", list(adr_options.keys()))
            adr_id = adr_options[chosen]
            adr = db.get_adr(adr_id)

            if adr:
                reviewers_val = json.loads(adr.get("reviewers","[]")) if adr.get("reviewers") else []
                rel_std_val   = json.loads(adr.get("related_standards","[]")) if adr.get("related_standards") else []
                rel_req_val   = json.loads(adr.get("related_requests","[]")) if adr.get("related_requests") else []

                std_list    = db.get_standards()
                std_choices = [f"{s['std_id']} — {s['title']}" for s in std_list]
                ar_refs     = [r["reference"] for r in db.get_arch_reviews()]
                ex_refs     = [e["reference"] for e in db.get_std_exceptions()]

                with st.form("adr_edit_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        u_title  = st.text_input("Title *", value=adr.get("title",""))
                        u_bl     = st.selectbox("BL domain", BL_OPTIONS,
                                                index=BL_OPTIONS.index(adr["bl_domain"]) if adr.get("bl_domain") in BL_OPTIONS else 0)
                        u_author = st.text_input("Author", value=adr.get("author",""))
                    with col2:
                        u_status = st.selectbox("Status", ADR_STATUSES,
                                                index=ADR_STATUSES.index(adr["status"]) if adr.get("status") in ADR_STATUSES else 0)
                        u_tech   = st.selectbox("Tech domain", TECH_DOMAINS,
                                                index=TECH_DOMAINS.index(adr["tech_domain"]) if adr.get("tech_domain") in TECH_DOMAINS else 0)
                        u_reviewers = st.multiselect("Reviewers", EA_MEMBERS, default=reviewers_val)

                    u_context   = st.text_area("Context", value=adr.get("context",""), height=100)
                    u_decision  = st.text_area("Decision", value=adr.get("decision",""), height=80)
                    u_rationale = st.text_area("Rationale", value=adr.get("rationale",""), height=100)
                    c1, c2 = st.columns(2)
                    with c1:
                        u_pos = st.text_area("Positive consequences", value=adr.get("consequences_positive",""), height=80)
                    with c2:
                        u_neg = st.text_area("Negative consequences", value=adr.get("consequences_negative",""), height=80)
                    u_alt = st.text_area("Alternatives considered", value=adr.get("alternatives",""), height=80)

                    existing_std_labels = [f"{sid} — {db.get_standard(sid)['title']}" if db.get_standard(sid) else sid for sid in rel_std_val]
                    u_rel_std = st.multiselect("Related standards", std_choices, default=[s for s in existing_std_labels if s in std_choices])
                    u_rel_req = st.multiselect("Related requests", ar_refs + ex_refs, default=[r for r in rel_req_val if r in ar_refs + ex_refs])

                    u_superseded_by = st.text_input("Superseded by (ADR number, if applicable)", value=adr.get("superseded_by",""))

                    update_adr = st.form_submit_button("Save Changes →", type="primary")

                if update_adr:
                    rel_std_ids = [s.split(" — ")[0] for s in u_rel_std]
                    db.update_adr(adr_id, {
                        "title": u_title, "status": u_status,
                        "context": u_context, "decision": u_decision,
                        "rationale": u_rationale,
                        "consequences_positive": u_pos,
                        "consequences_negative": u_neg,
                        "alternatives": u_alt,
                        "bl_domain": u_bl, "tech_domain": u_tech,
                        "author": u_author,
                        "reviewers": u_reviewers,
                        "related_standards": rel_std_ids,
                        "related_requests": u_rel_req,
                        "superseded_by": u_superseded_by,
                    })
                    db.log_activity(current_user, "Updated ADR", "adr",
                                    adr["adr_number"], f"Status → {u_status}")
                    st.success("ADR updated.")
                    st.rerun()
