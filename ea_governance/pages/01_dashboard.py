"""Dashboard — Home page with metrics, queue, and activity feed."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from database import (get_dashboard_metrics, get_arch_reviews, get_std_exceptions,
                      get_recent_activity)
from routing_engine import sla_days_remaining
from components.badges import status_badge, tier_badge, sla_badge
from components.charts import status_donut, bar_by_status

st.set_page_config(page_title="Dashboard — EA Governance", page_icon="🏠", layout="wide")

st.markdown("""
<style>
  .stApp { background: #F4F6FA; }
  [data-testid="stMetric"] {
    background: #fff; border-radius: 10px;
    padding: 12px 16px; border: 1px solid #E5E7EB;
  }
  .stTabs [aria-selected="true"] { background: #1E2761; color: #fff !important; }
</style>
""", unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
current_user = st.session_state.get("current_user", "Head of EA")
current_role = st.session_state.get("current_role", "EA Lead")

st.markdown(f"""
<div style="background:#fff;border-radius:12px;padding:20px 24px;margin-bottom:20px;
            border-left:5px solid #1E2761;">
  <h1 style="margin:0;color:#1E2761;font-size:1.6rem;">🏠 Dashboard</h1>
  <p style="margin:4px 0 0;color:#6B7280;">
    Welcome, <b>{current_user}</b> — {current_role} &nbsp;|&nbsp; EA Governance Overview
  </p>
</div>
""", unsafe_allow_html=True)

# ── Metrics row ───────────────────────────────────────────────────────────────
metrics = get_dashboard_metrics()

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("Open Reviews (A)", metrics["ar_open"])
with col2:
    st.metric("Open Exceptions (B)", metrics["ex_open"])
with col3:
    st.metric("Overdue — Reviews", metrics["ar_overdue"],
              delta=f"-{metrics['ar_overdue']} past SLA" if metrics["ar_overdue"] else None,
              delta_color="inverse")
with col4:
    st.metric("Overdue — Exceptions", metrics["ex_overdue"],
              delta=f"-{metrics['ex_overdue']} past SLA" if metrics["ex_overdue"] else None,
              delta_color="inverse")
with col5:
    st.metric("SAB Queue", metrics["sab_items"])
with col6:
    total_std = sum(d["cnt"] for d in metrics["std_by_status"])
    active_std = next((d["cnt"] for d in metrics["std_by_status"] if d["status"] == "Active"), 0)
    st.metric("Active Standards", active_std, delta=f"of {total_std} total")

st.markdown("---")

# ── Charts row ────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    if metrics["ar_by_status"]:
        fig = status_donut(metrics["ar_by_status"], "Architecture Reviews by Status")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No architecture reviews yet.")

with c2:
    if metrics["adr_by_status"]:
        fig = status_donut(metrics["adr_by_status"], "ADRs by Status")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No ADRs yet.")

with c3:
    if metrics["std_by_status"]:
        fig = bar_by_status(metrics["std_by_status"], "status", "cnt", "Standards Library Health")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No standards yet.")

st.markdown("---")

# ── My Queue + Activity Feed ──────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📥 My Queue", "📋 All Open Reviews", "🕐 Activity Feed"])

with tab1:
    all_ar = get_arch_reviews()
    all_ex = get_std_exceptions()

    my_ar = [r for r in all_ar
             if r.get("assigned_ea") and current_user in r["assigned_ea"]
             and r["status"] not in ("Approved","Rejected","Closed","Escalated")]
    my_ex = [r for r in all_ex
             if r.get("assigned_ea") and current_user in r["assigned_ea"]
             and r["status"] not in ("Approved","Rejected","Closed","SAB Escalation")]

    if not my_ar and not my_ex:
        st.success("Your queue is empty — no pending items.")
    else:
        if my_ar:
            st.markdown("**Architecture Reviews assigned to you**")
            for r in my_ar:
                days = sla_days_remaining(r.get("sla_deadline"))
                cols = st.columns([3,1,1,1,1])
                cols[0].markdown(f"**{r['reference']}** — {r['title']}")
                cols[1].markdown(status_badge(r["status"]), unsafe_allow_html=True)
                cols[2].markdown(tier_badge(r.get("routing_tier","")), unsafe_allow_html=True)
                cols[3].markdown(sla_badge(days), unsafe_allow_html=True)
                cols[4].page_link("pages/02_workflow_a.py", label="Open →")

        if my_ex:
            st.markdown("**Standards Exceptions assigned to you**")
            for r in my_ex:
                days = sla_days_remaining(r.get("sla_deadline"))
                cols = st.columns([3,1,1,1,1])
                cols[0].markdown(f"**{r['reference']}** — {r['title']}")
                cols[1].markdown(status_badge(r["status"]), unsafe_allow_html=True)
                cols[2].markdown(tier_badge(r.get("routing_tier","")), unsafe_allow_html=True)
                cols[3].markdown(sla_badge(days), unsafe_allow_html=True)
                cols[4].page_link("pages/03_workflow_b.py", label="Open →")

with tab2:
    open_reviews = [r for r in get_arch_reviews()
                    if r["status"] not in ("Approved","Rejected","Closed","Escalated")]

    if not open_reviews:
        st.info("No open architecture reviews.")
    else:
        df_data = []
        for r in open_reviews:
            days = sla_days_remaining(r.get("sla_deadline"))
            days_str = f"{days}d" if days is not None else "No SLA"
            df_data.append({
                "Reference": r["reference"],
                "Title": r["title"],
                "Status": r["status"],
                "Tier": r.get("routing_tier",""),
                "Assigned EA": r.get("assigned_ea",""),
                "BL": r.get("submitter_bl",""),
                "Score": r.get("routing_score",""),
                "SLA": days_str,
            })
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

with tab3:
    recent = get_recent_activity(20)
    if not recent:
        st.info("No activity yet.")
    else:
        for act in recent:
            ts = act.get("logged_at","")[:16]
            entity_color = {
                "arch_review": "#4A90D9",
                "std_exception": "#D97706",
                "adr": "#7C3AED",
                "standard": "#059669",
                "pattern": "#059669",
                "system": "#6B7280",
            }.get(act.get("entity_type",""), "#6B7280")

            st.markdown(f"""
<div style="background:#fff;border-radius:8px;padding:10px 14px;margin:4px 0;
            border-left:3px solid {entity_color};border:1px solid #E5E7EB;
            border-left:3px solid {entity_color};">
  <span style="color:#6B7280;font-size:0.8rem;">{ts}</span> &nbsp;
  <b style="color:#1E2761;">{act.get('actor','')}</b> —
  {act.get('action','')}
  <span style="font-family:monospace;color:{entity_color};font-size:0.8rem;">
    [{act.get('entity_ref','')}]
  </span>
  <br/><span style="color:#6B7280;font-size:0.8rem;">{act.get('details','')}</span>
</div>
""", unsafe_allow_html=True)
