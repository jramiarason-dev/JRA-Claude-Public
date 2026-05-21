"""Workflow A — Architecture Review Requests."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
from datetime import datetime

import database as db
from routing_engine import (score_arch_review, route_arch_review,
                             assign_ea_arch_review, score_description,
                             sla_days_remaining)
from components.badges import status_badge, tier_badge, sla_badge
from components.forms import ai_assistant_panel, BL_OPTIONS, ARCH_TYPES, COMPLEXITY, URGENCY, VIOLATION

st.set_page_config(page_title="Architecture Reviews — EA Governance", page_icon="📋", layout="wide")

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
<div style="background:#fff;border-radius:12px;padding:20px 24px;margin-bottom:20px;border-left:5px solid #1E2761;">
  <h1 style="margin:0;color:#1E2761;font-size:1.6rem;">📋 Architecture Review Requests</h1>
  <p style="margin:4px 0 0;color:#6B7280;">Workflow A — Submit, track, and decide on architecture review requests</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📥 Submit New Request", "📋 All Requests", "🔍 Review & Decide"])

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: Submit
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("New Architecture Review Request")
    ai_assistant_panel("workflow_a_submit")

    with st.form("ar_submit_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title *", placeholder="e.g. New PWM Client Portal — API Layer")
            submitter_name = st.text_input("Your name *", value=current_user)
            submitter_role = st.text_input("Your role *", placeholder="Solution Architect / Product Owner")
            submitter_bl = st.selectbox("Your Business Line *", BL_OPTIONS)
        with col2:
            arch_type = st.selectbox("Architecture type *", ARCH_TYPES)
            complexity = st.selectbox("Estimated complexity *", COMPLEXITY)
            urgency = st.selectbox("Urgency *", URGENCY)
            standard_violation = st.selectbox("Standard violation flag *", VIOLATION)

        affected_bls = st.multiselect("Affected Business Lines *", BL_OPTIONS, default=[submitter_bl])
        description = st.text_area("Description *", height=140,
                                   placeholder="Describe the solution, the change, and its architecture impact.")
        attachment = st.file_uploader("Attachment (optional)", type=["pdf","pptx","docx","png","jpg"])

        submitted = st.form_submit_button("Submit for Review →", type="primary")

    if submitted:
        errors = []
        if not title.strip():      errors.append("Title is required.")
        if not submitter_name.strip(): errors.append("Your name is required.")
        if not submitter_role.strip(): errors.append("Your role is required.")
        if not description.strip(): errors.append("Description is required.")
        if not affected_bls:        errors.append("Select at least one affected BL.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            # Routing engine
            score_result = score_arch_review(complexity, arch_type, affected_bls, urgency, standard_violation)
            route_result = route_arch_review(score_result["total"], standard_violation)
            assigned_ea  = assign_ea_arch_review(affected_bls, submitter_bl)
            reference    = db.next_ar_ref()

            attachment_path = ""
            if attachment:
                os.makedirs("data/uploads", exist_ok=True)
                attachment_path = f"data/uploads/{reference}_{attachment.name}"
                with open(attachment_path, "wb") as f:
                    f.write(attachment.getbuffer())

            row_id = db.create_arch_review({
                "reference": reference,
                "title": title,
                "submitter_name": submitter_name,
                "submitter_role": submitter_role,
                "submitter_bl": submitter_bl,
                "description": description,
                "arch_type": arch_type,
                "affected_bls": affected_bls,
                "complexity": complexity,
                "urgency": urgency,
                "standard_violation": standard_violation,
                "attachment_path": attachment_path,
                "routing_score": score_result["total"],
                "routing_tier": route_result["tier"],
                "assigned_ea": assigned_ea,
                "status": "Submitted",
                "sla_deadline": route_result["sla_deadline"],
            })

            db.log_activity(current_user, "Submitted request", "arch_review", reference,
                            f"Score {score_result['total']} → {route_result['tier']}")

            # Score breakdown
            breakdown = score_description(score_result["scores"])
            st.success(f"**{reference}** submitted successfully!")
            st.markdown(f"""
<div style="background:#D1FAE5;border-radius:10px;padding:16px;border-left:4px solid #059669;">
  <b>Routing result</b><br/>
  Score: <b>{score_result['total']}/12</b> → Tier: {tier_badge(route_result['tier'])}
  <br/>Assigned to: <b>{assigned_ea}</b>
  <br/><span style="font-size:0.85rem;color:#374151;">Breakdown: {breakdown}</span>
  {"<br/><span style='color:#D97706;'><b>⚠ Standard violation flagged — confirm with EA reviewer</b></span>" if standard_violation != "No" else ""}
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: All Requests
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("All Architecture Review Requests")

    # Filters
    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        f_status = st.selectbox("Filter by status", ["All","Submitted","Under Review","Decision Pending",
                                                       "Approved","Rejected","Escalated","Closed"])
    with fcol2:
        f_tier = st.selectbox("Filter by tier", ["All","Fast-track","Standard Review","Extended Review","SAB Escalation"])
    with fcol3:
        f_bl = st.selectbox("Filter by BL", ["All"] + BL_OPTIONS)

    reviews = db.get_arch_reviews(status=None if f_status == "All" else f_status)
    if f_tier != "All":
        reviews = [r for r in reviews if r.get("routing_tier") == f_tier]
    if f_bl != "All":
        reviews = [r for r in reviews if r.get("submitter_bl") == f_bl]

    if not reviews:
        st.info("No requests match the current filters.")
    else:
        for r in reviews:
            days = sla_days_remaining(r.get("sla_deadline"))
            with st.expander(f"**{r['reference']}** — {r['title']}", expanded=False):
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(status_badge(r["status"]), unsafe_allow_html=True)
                c2.markdown(tier_badge(r.get("routing_tier","")), unsafe_allow_html=True)
                c3.markdown(sla_badge(days), unsafe_allow_html=True)
                c4.markdown(f"Score: **{r.get('routing_score','—')}**")

                st.markdown(f"""
| Field | Value |
|---|---|
| Submitter | {r.get('submitter_name','')} — {r.get('submitter_role','')} |
| Business Line | {r.get('submitter_bl','')} |
| Arch Type | {r.get('arch_type','')} |
| Complexity | {r.get('complexity','')} |
| Urgency | {r.get('urgency','')} |
| Standard Violation | {r.get('standard_violation','')} |
| Affected BLs | {', '.join(json.loads(r.get('affected_bls','[]')))} |
| Assigned EA | {r.get('assigned_ea','')} |
| Submitted | {r.get('submitted_at','')[:16]} |
""")
                st.markdown(f"**Description:** {r.get('description','')}")

                decisions = db.get_arch_review_decisions(r["id"])
                if decisions:
                    st.markdown("**Review decisions:**")
                    for d in decisions:
                        st.markdown(f"""
<div style="background:#F8FAFC;border-radius:8px;padding:12px;margin:4px 0;border:1px solid #E5E7EB;">
  <b>{d['reviewer_name']}</b> — {d['decided_at'][:16]}<br/>
  Alignment: {d['standards_alignment']} | Risk: {d['risk_assessment']} | Feasibility: {d['feasibility']}<br/>
  <b>Recommendation: {d['recommendation']}</b><br/>
  {f"Conditions: {d['conditions']}<br/>" if d.get('conditions') else ""}
  {f"Comments: {d['comments']}" if d.get('comments') else ""}
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: Review & Decide (EA members only)
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    if current_role not in ("EA Reviewer", "EA Lead"):
        st.warning("Review and decision actions are available to EA team members only.")
    else:
        st.subheader("Review Queue — EA Decision Panel")

        reviewable = db.get_arch_reviews()
        reviewable = [r for r in reviewable
                      if r["status"] in ("Submitted","Under Review","Decision Pending")
                      and (current_role == "EA Lead" or
                           (r.get("assigned_ea") and current_user in r["assigned_ea"]))]

        if not reviewable:
            st.success("No requests pending your review.")
        else:
            options = {f"{r['reference']} — {r['title']}": r["id"] for r in reviewable}
            chosen_label = st.selectbox("Select request to review", list(options.keys()))
            review_id = options[chosen_label]
            review = db.get_arch_review(review_id)

            if review:
                # Mark as Under Review
                if review["status"] == "Submitted":
                    if st.button("▶ Start Review (mark as Under Review)"):
                        db.update_arch_review_status(review_id, "Under Review", current_user)
                        db.log_activity(current_user, "Started review", "arch_review",
                                        review["reference"], "Status → Under Review")
                        st.success("Status updated to Under Review.")
                        st.rerun()

                st.markdown(f"""
<div style="background:#F8FAFC;border-radius:10px;padding:16px;border:1px solid #E5E7EB;margin:12px 0;">
  <b style="color:#1E2761;">{review['reference']}</b> — {review['title']}<br/>
  {tier_badge(review.get('routing_tier',''))} {status_badge(review['status'])}
  {sla_badge(sla_days_remaining(review.get('sla_deadline')))}
  <hr style="border-color:#E5E7EB;margin:8px 0;">
  <b>Submitter:</b> {review.get('submitter_name','')} ({review.get('submitter_role','')}) — {review.get('submitter_bl','')}<br/>
  <b>Arch type:</b> {review.get('arch_type','')} | Complexity: {review.get('complexity','')} | Violation: {review.get('standard_violation','')}<br/>
  <b>Affected BLs:</b> {', '.join(json.loads(review.get('affected_bls','[]')))}<br/>
  <b>Score:</b> {review.get('routing_score','')}/12 → {review.get('routing_tier','')}<br/><br/>
  <b>Description:</b> {review.get('description','')}
</div>
""", unsafe_allow_html=True)

                ai_assistant_panel("workflow_a_review")

                st.markdown("---")
                st.subheader("Decision Form")

                with st.form(f"decision_form_{review_id}"):
                    d_col1, d_col2, d_col3 = st.columns(3)
                    with d_col1:
                        standards_alignment = st.selectbox("Standards alignment *",
                                                           ["Aligned","Partial","Non-compliant"])
                    with d_col2:
                        risk_assessment = st.selectbox("Risk assessment *",
                                                       ["Low","Medium","High"])
                    with d_col3:
                        feasibility = st.selectbox("Technical feasibility *",
                                                   ["Yes","With conditions","No"])

                    recommendation = st.selectbox("Recommendation *",
                                                  ["Approve","Approve with conditions",
                                                   "Reject","Escalate to SAB"])
                    conditions = st.text_area("Conditions (if applicable)", height=80)
                    comments   = st.text_area("Comments / rationale *", height=100)

                    decide = st.form_submit_button("Submit Decision →", type="primary")

                if decide:
                    if not comments.strip():
                        st.error("Comments / rationale are required.")
                    else:
                        status_map = {
                            "Approve":                "Approved",
                            "Approve with conditions": "Approved",
                            "Reject":                 "Rejected",
                            "Escalate to SAB":        "Escalated",
                        }
                        new_status = status_map[recommendation]

                        db.save_arch_review_decision({
                            "review_id": review_id,
                            "reviewer_name": current_user,
                            "standards_alignment": standards_alignment,
                            "risk_assessment": risk_assessment,
                            "feasibility": feasibility,
                            "recommendation": recommendation,
                            "conditions": conditions,
                            "comments": comments,
                            "new_status": new_status,
                        })
                        db.log_activity(current_user, f"Decision: {recommendation}",
                                        "arch_review", review["reference"],
                                        f"Risk: {risk_assessment} | Alignment: {standards_alignment}")
                        st.success(f"Decision recorded — status updated to **{new_status}**.")
                        if recommendation == "Escalate to SAB":
                            st.warning("⬆ SAB agenda item created. Head of EA notified.")
                        st.rerun()
