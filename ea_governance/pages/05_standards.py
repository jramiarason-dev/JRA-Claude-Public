"""Standards & Patterns Library."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd

import database as db
from components.badges import status_badge, compliance_badge
from components.cards import standard_card
from components.forms import BL_OPTIONS

st.set_page_config(page_title="Standards Library — EA Governance", page_icon="📚", layout="wide")

st.markdown("""
<style>
  .stApp { background: #F4F6FA; }
  .stTabs [aria-selected="true"] { background: #1E2761; color: #fff !important; }
</style>
""", unsafe_allow_html=True)

current_user = st.session_state.get("current_user", "Head of EA")
current_role = st.session_state.get("current_role", "EA Lead")

EA_MEMBERS = [
    "Head of EA", "Sr EA 1 — PWM / Application", "Sr EA 2 — PAS / Data & Security",
    "Sr EA 3 — Ops / Process", "Risk & Compliance EA", "Cloud Architect EA",
]
STD_CATEGORIES = ["Security", "Data", "Integration", "Cloud", "Application", "Process", "Cross-cutting"]
PAT_CATEGORIES = ["Integration", "Data", "Application", "Cloud", "Process"]
COMPLIANCE_LEVELS = ["Mandatory", "Recommended", "Optional"]
STD_STATUSES = ["Active", "Draft", "Under review", "Deprecated"]
PAT_STATUSES = ["Approved", "Experimental", "Deprecated"]

st.markdown("""
<div style="background:#fff;border-radius:12px;padding:20px 24px;margin-bottom:20px;border-left:5px solid #059669;">
  <h1 style="margin:0;color:#1E2761;font-size:1.6rem;">📚 Standards & Patterns Library</h1>
  <p style="margin:4px 0 0;color:#6B7280;">Architecture standards, patterns, and exception tracking — editable by EA members</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📋 Standards", "🔷 Patterns", "✏️ Manage Standards", "✏️ Manage Patterns"])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: Standards browse
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        f_cat    = st.selectbox("Category", ["All"] + STD_CATEGORIES, key="std_cat")
    with fcol2:
        f_status = st.selectbox("Status", ["All"] + STD_STATUSES, key="std_status")
    with fcol3:
        f_comp   = st.selectbox("Compliance level", ["All"] + COMPLIANCE_LEVELS, key="std_comp")
    f_search = st.text_input("Search standards", placeholder="Title, description...", key="std_search")

    standards = db.get_standards(
        status=None if f_status == "All" else f_status,
        category=None if f_cat == "All" else f_cat,
    )
    if f_comp != "All":
        standards = [s for s in standards if s.get("compliance_level") == f_comp]
    if f_search:
        q = f_search.lower()
        standards = [s for s in standards
                     if q in s.get("title","").lower() or q in s.get("description","").lower()]

    st.markdown(f"**{len(standards)} standard(s) found**")

    view_mode = st.radio("View", ["Cards", "Table"], horizontal=True, key="std_view")

    if view_mode == "Table":
        df_data = []
        for s in standards:
            exc_cnt = db.get_standard_exception_count(s["std_id"])
            df_data.append({
                "ID": s["std_id"],
                "Title": s["title"],
                "Category": s["category"],
                "Status": s["status"],
                "Compliance": s["compliance_level"],
                "Owner": s["owner"],
                "Active Exceptions": exc_cnt,
            })
        if df_data:
            st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True)
    else:
        for s in standards:
            exc_cnt = db.get_standard_exception_count(s["std_id"])
            scope   = json.loads(s.get("scope","[]")) if s.get("scope") else []
            rel_adr = json.loads(s.get("related_adrs","[]")) if s.get("related_adrs") else []

            with st.expander(
                f"**{s['std_id']}** — {s['title']}",
                expanded=False
            ):
                c1, c2, c3 = st.columns(3)
                c1.markdown(status_badge(s["status"]), unsafe_allow_html=True)
                c2.markdown(compliance_badge(s["compliance_level"]), unsafe_allow_html=True)
                c3.markdown(f"**Category:** {s['category']}")

                if exc_cnt > 0:
                    st.warning(f"⚠ {exc_cnt} active exception(s) for this standard.")

                st.markdown(f"""
| Field | Value |
|---|---|
| Owner | {s.get('owner','')} |
| Scope | {', '.join(scope)} |
| Related ADRs | {', '.join(rel_adr) if rel_adr else '—'} |
| Created | {s.get('created_at','')[:10]} | Last updated | {s.get('updated_at','')[:10]} |
""")
                st.markdown(f"**Description:** {s.get('description','')}")
                st.markdown(f"**Rationale:** {s.get('rationale','')}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: Patterns browse
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        fp_cat    = st.selectbox("Category", ["All"] + PAT_CATEGORIES, key="pat_cat")
    with fcol2:
        fp_status = st.selectbox("Status", ["All"] + PAT_STATUSES, key="pat_status")
    fp_search = st.text_input("Search patterns", placeholder="Title, problem, solution...", key="pat_search")

    patterns = db.get_patterns(
        status=None if fp_status == "All" else fp_status,
        category=None if fp_cat == "All" else fp_cat,
    )
    if fp_search:
        q = fp_search.lower()
        patterns = [p for p in patterns
                    if q in p.get("title","").lower()
                    or q in p.get("problem","").lower()
                    or q in p.get("solution","").lower()]

    st.markdown(f"**{len(patterns)} pattern(s) found**")

    for p in patterns:
        rel_std = json.loads(p.get("related_standards","[]")) if p.get("related_standards") else []
        with st.expander(f"**{p['pat_id']}** — {p['title']}", expanded=False):
            c1, c2 = st.columns(2)
            c1.markdown(status_badge(p["status"]), unsafe_allow_html=True)
            c2.markdown(f"**Category:** {p['category']}  |  **Owner:** {p.get('owner','')}")

            if rel_std:
                st.markdown(f"**Related standards:** {', '.join(rel_std)}")

            for label, field in [
                ("Problem", "problem"), ("Solution", "solution"),
                ("When to use", "when_to_use"), ("When NOT to use", "when_not_to_use"),
                ("Example", "example"),
            ]:
                if p.get(field):
                    st.markdown(f"**{label}**")
                    if field == "example":
                        st.code(p[field], language="text")
                    else:
                        st.markdown(f"> {p[field]}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: Manage Standards
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    if current_role not in ("EA Reviewer", "EA Lead"):
        st.warning("Standards management is restricted to EA team members.")
    else:
        action = st.radio("Action", ["Create new standard", "Edit existing standard", "Delete standard"],
                          horizontal=True, key="std_action")

        if action == "Create new standard":
            with st.form("std_create_form"):
                col1, col2 = st.columns(2)
                with col1:
                    s_title      = st.text_input("Title *")
                    s_category   = st.selectbox("Category *", STD_CATEGORIES)
                    s_compliance = st.selectbox("Compliance level *", COMPLIANCE_LEVELS)
                    s_owner      = st.selectbox("Owner *", EA_MEMBERS)
                with col2:
                    s_status = st.selectbox("Status", STD_STATUSES)
                    s_scope  = st.multiselect("Scope (BLs)", BL_OPTIONS, default=BL_OPTIONS)

                s_desc     = st.text_area("Description *", height=100)
                s_rationale = st.text_area("Rationale", height=80)

                adr_choices = [f"{a['adr_number']} — {a['title']}" for a in db.get_adrs()]
                s_adrs = st.multiselect("Related ADRs", adr_choices)
                pat_choices = [f"{p['pat_id']} — {p['title']}" for p in db.get_patterns()]
                s_pats = st.multiselect("Related patterns", pat_choices)

                create_std = st.form_submit_button("Create Standard →", type="primary")

            if create_std:
                if not s_title.strip() or not s_desc.strip():
                    st.error("Title and description are required.")
                else:
                    std_id = db.next_std_id()
                    db.create_standard({
                        "std_id": std_id, "title": s_title, "category": s_category,
                        "status": s_status, "description": s_desc, "rationale": s_rationale,
                        "scope": s_scope, "compliance_level": s_compliance, "owner": s_owner,
                        "related_adrs": [a.split(" — ")[0] for a in s_adrs],
                        "related_patterns": [p.split(" — ")[0] for p in s_pats],
                    })
                    db.log_activity(current_user, "Created standard", "standard", std_id, s_title)
                    st.success(f"Standard **{std_id}** created.")
                    st.rerun()

        elif action == "Edit existing standard":
            all_std = db.get_standards()
            if not all_std:
                st.info("No standards yet.")
            else:
                std_map = {f"{s['std_id']} — {s['title']}": s["std_id"] for s in all_std}
                chosen  = st.selectbox("Select standard", list(std_map.keys()))
                std_id  = std_map[chosen]
                s = db.get_standard(std_id)

                if s:
                    scope_val   = json.loads(s.get("scope","[]")) if s.get("scope") else []
                    rel_adr_val = json.loads(s.get("related_adrs","[]")) if s.get("related_adrs") else []
                    rel_pat_val = json.loads(s.get("related_patterns","[]")) if s.get("related_patterns") else []

                    with st.form("std_edit_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            e_title    = st.text_input("Title *", value=s["title"])
                            e_category = st.selectbox("Category", STD_CATEGORIES,
                                                       index=STD_CATEGORIES.index(s["category"]) if s.get("category") in STD_CATEGORIES else 0)
                            e_comp     = st.selectbox("Compliance", COMPLIANCE_LEVELS,
                                                       index=COMPLIANCE_LEVELS.index(s["compliance_level"]) if s.get("compliance_level") in COMPLIANCE_LEVELS else 0)
                            e_owner    = st.selectbox("Owner", EA_MEMBERS,
                                                       index=EA_MEMBERS.index(s["owner"]) if s.get("owner") in EA_MEMBERS else 0)
                        with col2:
                            e_status = st.selectbox("Status", STD_STATUSES,
                                                     index=STD_STATUSES.index(s["status"]) if s.get("status") in STD_STATUSES else 0)
                            e_scope  = st.multiselect("Scope", BL_OPTIONS, default=[b for b in scope_val if b in BL_OPTIONS])

                        e_desc    = st.text_area("Description", value=s.get("description",""), height=100)
                        e_rat     = st.text_area("Rationale", value=s.get("rationale",""), height=80)

                        adr_choices = [f"{a['adr_number']} — {a['title']}" for a in db.get_adrs()]
                        e_adrs = st.multiselect("Related ADRs", adr_choices,
                                                default=[a for a in adr_choices if a.split(" — ")[0] in rel_adr_val])
                        pat_choices = [f"{p['pat_id']} — {p['title']}" for p in db.get_patterns()]
                        e_pats = st.multiselect("Related patterns", pat_choices,
                                                default=[p for p in pat_choices if p.split(" — ")[0] in rel_pat_val])

                        update_std = st.form_submit_button("Save Changes →", type="primary")

                    if update_std:
                        db.update_standard(std_id, {
                            "title": e_title, "category": e_category, "status": e_status,
                            "description": e_desc, "rationale": e_rat, "scope": e_scope,
                            "compliance_level": e_comp, "owner": e_owner,
                            "related_adrs": [a.split(" — ")[0] for a in e_adrs],
                            "related_patterns": [p.split(" — ")[0] for p in e_pats],
                        })
                        db.log_activity(current_user, "Updated standard", "standard", std_id, e_title)
                        st.success(f"Standard **{std_id}** updated.")
                        st.rerun()

        else:  # Delete
            all_std = db.get_standards()
            if not all_std:
                st.info("No standards yet.")
            else:
                std_map = {f"{s['std_id']} — {s['title']}": s["std_id"] for s in all_std}
                chosen  = st.selectbox("Select standard to delete", list(std_map.keys()), key="del_std")
                std_id  = std_map[chosen]
                exc_cnt = db.get_standard_exception_count(std_id)

                if exc_cnt > 0:
                    st.error(f"Cannot delete: {exc_cnt} active exception(s) reference this standard.")
                else:
                    st.warning(f"This will permanently delete **{std_id}**. This cannot be undone.")
                    if st.button("Confirm Delete", type="primary"):
                        success = db.delete_standard(std_id)
                        if success:
                            db.log_activity(current_user, "Deleted standard", "standard", std_id, "")
                            st.success("Standard deleted.")
                            st.rerun()
                        else:
                            st.error("Delete failed — active exceptions still reference this standard.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4: Manage Patterns
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    if current_role not in ("EA Reviewer", "EA Lead"):
        st.warning("Patterns management is restricted to EA team members.")
    else:
        p_action = st.radio("Action", ["Create new pattern", "Edit existing pattern"],
                            horizontal=True, key="pat_action")

        if p_action == "Create new pattern":
            with st.form("pat_create_form"):
                col1, col2 = st.columns(2)
                with col1:
                    p_title    = st.text_input("Title *")
                    p_category = st.selectbox("Category *", PAT_CATEGORIES)
                    p_owner    = st.selectbox("Owner *", EA_MEMBERS)
                with col2:
                    p_status = st.selectbox("Status", PAT_STATUSES)
                    std_choices = [f"{s['std_id']} — {s['title']}" for s in db.get_standards()]
                    p_rel_std = st.multiselect("Related standards", std_choices)

                p_problem      = st.text_area("Problem *", height=80)
                p_solution     = st.text_area("Solution *", height=100)
                col1, col2 = st.columns(2)
                with col1:
                    p_when     = st.text_area("When to use", height=80)
                with col2:
                    p_when_not = st.text_area("When NOT to use", height=80)
                p_example  = st.text_area("Example", height=80, placeholder="Diagram description or pseudocode")

                create_pat = st.form_submit_button("Create Pattern →", type="primary")

            if create_pat:
                if not p_title.strip() or not p_problem.strip() or not p_solution.strip():
                    st.error("Title, problem, and solution are required.")
                else:
                    pat_id = db.next_pat_id()
                    db.create_pattern({
                        "pat_id": pat_id, "title": p_title, "category": p_category,
                        "problem": p_problem, "solution": p_solution,
                        "when_to_use": p_when, "when_not_to_use": p_when_not,
                        "example": p_example, "status": p_status, "owner": p_owner,
                        "related_standards": [s.split(" — ")[0] for s in p_rel_std],
                    })
                    db.log_activity(current_user, "Created pattern", "pattern", pat_id, p_title)
                    st.success(f"Pattern **{pat_id}** created.")
                    st.rerun()

        else:
            all_pat = db.get_patterns()
            if not all_pat:
                st.info("No patterns yet.")
            else:
                pat_map = {f"{p['pat_id']} — {p['title']}": p["pat_id"] for p in all_pat}
                chosen  = st.selectbox("Select pattern", list(pat_map.keys()))
                pat_id  = pat_map[chosen]
                p = next((x for x in all_pat if x["pat_id"] == pat_id), None)

                if p:
                    rel_std_val = json.loads(p.get("related_standards","[]")) if p.get("related_standards") else []
                    std_choices = [f"{s['std_id']} — {s['title']}" for s in db.get_standards()]

                    with st.form("pat_edit_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            pe_title    = st.text_input("Title *", value=p["title"])
                            pe_category = st.selectbox("Category", PAT_CATEGORIES,
                                                        index=PAT_CATEGORIES.index(p["category"]) if p.get("category") in PAT_CATEGORIES else 0)
                            pe_owner    = st.selectbox("Owner", EA_MEMBERS,
                                                        index=EA_MEMBERS.index(p["owner"]) if p.get("owner") in EA_MEMBERS else 0)
                        with col2:
                            pe_status = st.selectbox("Status", PAT_STATUSES,
                                                      index=PAT_STATUSES.index(p["status"]) if p.get("status") in PAT_STATUSES else 0)
                            pe_rel_std = st.multiselect("Related standards", std_choices,
                                                         default=[s for s in std_choices if s.split(" — ")[0] in rel_std_val])

                        pe_problem  = st.text_area("Problem", value=p.get("problem",""), height=80)
                        pe_solution = st.text_area("Solution", value=p.get("solution",""), height=100)
                        c1, c2 = st.columns(2)
                        with c1:
                            pe_when     = st.text_area("When to use", value=p.get("when_to_use",""), height=80)
                        with c2:
                            pe_when_not = st.text_area("When NOT to use", value=p.get("when_not_to_use",""), height=80)
                        pe_example = st.text_area("Example", value=p.get("example",""), height=80)

                        update_pat = st.form_submit_button("Save Changes →", type="primary")

                    if update_pat:
                        db.update_pattern(pat_id, {
                            "title": pe_title, "category": pe_category, "status": pe_status,
                            "problem": pe_problem, "solution": pe_solution,
                            "when_to_use": pe_when, "when_not_to_use": pe_when_not,
                            "example": pe_example, "owner": pe_owner,
                            "related_standards": [s.split(" — ")[0] for s in pe_rel_std],
                        })
                        db.log_activity(current_user, "Updated pattern", "pattern", pat_id, pe_title)
                        st.success(f"Pattern **{pat_id}** updated.")
                        st.rerun()
