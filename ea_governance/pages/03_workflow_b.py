"""Workflow B — Standards Exception Requests."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
from datetime import datetime

import database as db
from routing_engine import route_std_exception, assign_ea_exception, sla_days_remaining
from components.badges import status_badge, tier_badge, sla_badge
from components.forms import BL_OPTIONS

st.set_page_config(page_title="Standards Exceptions — EA Governance", page_icon="⚠️", layout="wide")

st.markdown("""
<style>
  .stApp { background: #F4F6FA; }
  [data-testid="stMetric"] { background:#fff;border-radius:10px;padding:12px 16px;border:1px solid #E5E7EB; }
  .stTabs [aria-selected="true"] { background: #1E2761; color: #fff !important; }
</style>
""", unsafe_allow_html=True)

current_user = st.session_state.get("current_user", "Head of EA")
current_role = st.session_state.get("current_role", "EA Lead")

st.markdown("""
<div style="background:#fff;border-radius:12px;padding:20px 24px;margin-bottom:20px;border-left:5px solid #D97706;">
  <h1 style="margin:0;color:#1E2761;font-size:1.6rem;">⚠️ Standards Exception Requests</h1>
  <p style="margin:4px 0 0;color:#6B7280;">Workflow B — Request and manage deviations from approved architecture standards</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📥 Submit Exception Request", "📋 All Exceptions", "🔍 Review & Decide"])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: Submit
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("New Standards Exception Request")
    st.info("Requesting an exception to an approved standard requires EA review and, in some cases, SAB approval.")

    # Load standards for dropdown
    standards = db.get_standards(status="Active")
    std_options = {f"{s['std_id']} — {s['title']}": s for s in standards}

    with st.form("ex_submit_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            title          = st.text_input("Request title *", placeholder="e.g. Temporary exception: direct DB access")
            submitter_name = st.text_input("Your name *", value=current_user)
            submitter_role = st.text_input("Your role *", placeholder="Solution Architect / Product Owner")
            submitter_bl   = st.selectbox("Your Business Line *", BL_OPTIONS)
        with col2:
            std_label = st.selectbox("Standard being excepted *", list(std_options.keys()) if std_options else ["No active standards"])
            duration  = st.selectbox("Duration *", ["Temporary","Permanent"])
            if duration == "Temporary":
                end_date = st.date_input("Exception end date *")
            else:
                end_date = None
            risk_level = st.selectbox("Risk level of exception *", ["Low","Medium","High"])

        justification = st.text_area("Justification *", height=120,
                                     placeholder="Why is this exception needed? What is the business/technical driver?")
        compensating_controls = st.text_area("Proposed compensating controls *", height=80,
                                              placeholder="What mitigations will be in place?")
        risk_ack = st.checkbox("I acknowledge the risk of deviating from this standard *")

        submitted = st.form_submit_button("Submit Exception Request →", type="primary")

    if submitted:
        errors = []
        if not title.strip():              errors.append("Title is required.")
        if not submitter_name.strip():     errors.append("Your name is required.")
        if not justification.strip():      errors.append("Justification is required.")
        if not compensating_controls.strip(): errors.append("Compensating controls are required.")
        if not risk_ack:                   errors.append("You must acknowledge the risk.")
        if not std_options:                errors.append("No active standards available to except.")

        if errors:
            for e in errors: st.error(e)
        else:
            selected_std = std_options.get(std_label)
            std_category = selected_std["category"] if selected_std else ""
            std_id       = selected_std["std_id"] if selected_std else ""

            route_result = route_std_exception(duration, risk_level, std_category)
            assigned_ea  = assign_ea_exception(submitter_bl)
            reference    = db.next_ex_ref()

            end_date_str = end_date.isoformat() if end_date and duration == "Temporary" else None

            db.create_std_exception({
                "reference": reference,
                "title": title,
                "submitter_name": submitter_name,
                "submitter_bl": submitter_bl,
                "standard_id": std_id,
                "justification": justification,
                "duration": duration,
                "end_date": end_date_str,
                "risk_acknowledged": True,
                "compensating_controls": compensating_controls,
                "routing_tier": route_result["tier"],
                "assigned_ea": assigned_ea,
                "status": "Submitted",
                "sla_deadline": route_result["sla_deadline"],
            })

            db.log_activity(current_user, "Submitted exception", "std_exception", reference,
                            f"{std_id} | {duration} | {risk_level} risk → {route_result['tier']}")

            st.success(f"**{reference}** submitted successfully!")
            st.markdown(f"""
<div style="background:#FEF3C7;border-radius:10px;padding:16px;border-left:4px solid #D97706;">
  <b>Routing result</b><br/>
  Duration: <b>{duration}</b> | Risk: <b>{risk_level}</b> | Standard category: <b>{std_category}</b><br/>
  Tier: {tier_badge(route_result['tier'])} | Assigned to: <b>{assigned_ea}</b>
  {"<br/><b style='color:#DC2626;'>⬆ Escalated to SAB — no SLA applies, board scheduling required</b>" if route_result['tier'] == 'SAB Escalation' else f"<br/>SLA: <b>{route_result.get('sla_days','')} days</b>"}
  {"<br/><span style='color:#DC2626;'>Security/Data standard exception always requires SAB approval</span>" if std_category in ('Security','Data') else ""}
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: All Exceptions
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("All Standards Exception Requests")

    fcol1, fcol2 = st.columns(2)
    with fcol1:
        f_status = st.selectbox("Filter by status",
                                ["All","Submitted","Under Review","Decision Pending",
                                 "Approved","Rejected","SAB Escalation","Closed"])
    with fcol2:
        f_bl = st.selectbox("Filter by BL", ["All"] + BL_OPTIONS)

    exceptions = db.get_std_exceptions(status=None if f_status == "All" else f_status)
    if f_bl != "All":
        exceptions = [e for e in exceptions if e.get("submitter_bl") == f_bl]

    if not exceptions:
        st.info("No exception requests match the current filters.")
    else:
        for e in exceptions:
            days = sla_days_remaining(e.get("sla_deadline"))
            std  = db.get_standard(e.get("standard_id",""))
            std_title = std["title"] if std else e.get("standard_id","")

            with st.expander(f"**{e['reference']}** — {e['title']}", expanded=False):
                c1, c2, c3 = st.columns(3)
                c1.markdown(status_badge(e["status"]), unsafe_allow_html=True)
                c2.markdown(tier_badge(e.get("routing_tier","")), unsafe_allow_html=True)
                c3.markdown(sla_badge(days), unsafe_allow_html=True)

                st.markdown(f"""
| Field | Value |
|---|---|
| Submitter | {e.get('submitter_name','')} |
| Business Line | {e.get('submitter_bl','')} |
| Standard | {e.get('standard_id','')} — {std_title} |
| Duration | {e.get('duration','')} {f"(until {e.get('end_date','')})" if e.get('end_date') else ''} |
| Assigned EA | {e.get('assigned_ea','')} |
| Submitted | {e.get('submitted_at','')[:16]} |
""")
                st.markdown(f"**Justification:** {e.get('justification','')}")
                st.markdown(f"**Compensating controls:** {e.get('compensating_controls','')}")

                decisions = db.get_std_exception_decisions(e["id"])
                if decisions:
                    st.markdown("**Decisions:**")
                    for d in decisions:
                        st.markdown(f"""
<div style="background:#F8FAFC;border-radius:8px;padding:12px;margin:4px 0;border:1px solid #E5E7EB;">
  <b>{d['reviewer_name']}</b> — {d['decided_at'][:16]}<br/>
  Decision: <b>{d['decision']}</b><br/>
  {f"Conditions: {d['conditions']}<br/>" if d.get('conditions') else ""}
  {f"Comments: {d['comments']}" if d.get('comments') else ""}
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: Review & Decide
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    if current_role not in ("EA Reviewer", "EA Lead"):
        st.warning("Review and decision actions are available to EA team members only.")
    else:
        st.subheader("Exception Review Queue — EA Decision Panel")

        reviewable = db.get_std_exceptions()
        reviewable = [e for e in reviewable
                      if e["status"] in ("Submitted","Under Review","Decision Pending")
                      and (current_role == "EA Lead" or
                           (e.get("assigned_ea") and current_user in e["assigned_ea"]))]

        if not reviewable:
            st.success("No exception requests pending your review.")
        else:
            options = {f"{e['reference']} — {e['title']}": e["id"] for e in reviewable}
            chosen_label = st.selectbox("Select exception to review", list(options.keys()))
            ex_id = options[chosen_label]
            ex = db.get_std_exception(ex_id)

            if ex:
                if ex["status"] == "Submitted":
                    if st.button("▶ Start Review"):
                        db.save_std_exception_decision({
                            "exception_id": ex_id,
                            "reviewer_name": current_user,
                            "decision": "Under Review",
                            "conditions": "",
                            "comments": "Review started.",
                            "new_status": "Under Review",
                        })
                        db.log_activity(current_user, "Started review", "std_exception",
                                        ex["reference"], "Status → Under Review")
                        st.rerun()

                std = db.get_standard(ex.get("standard_id",""))
                std_title = std["title"] if std else ""

                st.markdown(f"""
<div style="background:#FEF9C3;border-radius:10px;padding:16px;border:1px solid #FDE68A;margin:12px 0;">
  <b style="color:#1E2761;">{ex['reference']}</b> — {ex['title']}<br/>
  {tier_badge(ex.get('routing_tier',''))} {status_badge(ex['status'])}
  <hr style="border-color:#FDE68A;margin:8px 0;">
  <b>Standard:</b> {ex.get('standard_id','')} — {std_title}<br/>
  <b>Duration:</b> {ex.get('duration','')} {f"(until {ex.get('end_date','')})" if ex.get('end_date') else ''}<br/>
  <b>Submitter:</b> {ex.get('submitter_name','')} — {ex.get('submitter_bl','')}<br/><br/>
  <b>Justification:</b> {ex.get('justification','')}<br/><br/>
  <b>Compensating controls:</b> {ex.get('compensating_controls','')}
</div>
""", unsafe_allow_html=True)

                st.subheader("Decision Form")
                with st.form(f"ex_decision_{ex_id}"):
                    decision = st.selectbox("Decision *",
                                            ["Approve","Approve temporarily","Reject","Escalate SAB"])
                    conditions = st.text_area("Conditions (if applicable)", height=80)
                    comments   = st.text_area("Rationale / comments *", height=100)
                    submit_dec = st.form_submit_button("Submit Decision →", type="primary")

                if submit_dec:
                    if not comments.strip():
                        st.error("Rationale / comments required.")
                    else:
                        status_map = {
                            "Approve":           "Approved",
                            "Approve temporarily": "Approved",
                            "Reject":            "Rejected",
                            "Escalate SAB":      "SAB Escalation",
                        }
                        new_status = status_map[decision]
                        db.save_std_exception_decision({
                            "exception_id": ex_id,
                            "reviewer_name": current_user,
                            "decision": decision,
                            "conditions": conditions,
                            "comments": comments,
                            "new_status": new_status,
                        })
                        db.log_activity(current_user, f"Decision: {decision}",
                                        "std_exception", ex["reference"], comments[:80])
                        st.success(f"Decision recorded — status updated to **{new_status}**.")
                        if decision == "Approve temporarily":
                            st.info("Exception logged in Standards Library with expiry tracking.")
                        if decision == "Escalate SAB":
                            st.warning("⬆ Escalated to SAB.")
                        st.rerun()
