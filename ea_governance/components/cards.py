"""HTML card builders for requests, ADRs, and standards."""
import streamlit as st
from components.badges import status_badge, tier_badge, sla_badge, compliance_badge
from routing_engine import sla_days_remaining


def request_card(row: dict, workflow: str = "AR") -> None:
    days = sla_days_remaining(row.get("sla_deadline"))
    ref = row.get("reference", "")
    status = row.get("status", "")
    tier = row.get("routing_tier", "")

    with st.container():
        st.markdown(f"""
<div style="background:#fff;border:1px solid #E5E7EB;border-radius:10px;
            padding:16px 20px;margin-bottom:12px;
            border-left:4px solid #1E2761;">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
    <div>
      <span style="font-size:0.78rem;color:#6B7280;font-family:monospace;">{ref}</span>
      <h4 style="margin:2px 0 6px;color:#1E2761;font-size:1rem;">{row.get('title','')}</h4>
      <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">
        {status_badge(status)}
        {tier_badge(tier) if tier else ''}
        {sla_badge(days)}
      </div>
    </div>
    <div style="text-align:right;font-size:0.8rem;color:#6B7280;">
      <div>Assigned: <b>{row.get('assigned_ea','—')}</b></div>
      <div>BL: <b>{row.get('submitter_bl','—')}</b></div>
      <div>Score: <b>{row.get('routing_score','—')}</b></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


def adr_card(row: dict) -> None:
    with st.container():
        st.markdown(f"""
<div style="background:#fff;border:1px solid #E5E7EB;border-radius:10px;
            padding:16px 20px;margin-bottom:12px;border-left:4px solid #4A90D9;">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
    <div>
      <span style="font-size:0.78rem;color:#6B7280;font-family:monospace;">{row.get('adr_number','')}</span>
      <h4 style="margin:2px 0 6px;color:#1E2761;font-size:1rem;">{row.get('title','')}</h4>
      <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">
        {status_badge(row.get('status',''))}
        <span style="font-size:0.78rem;color:#374151;background:#F3F4F6;
                     padding:2px 8px;border-radius:8px;">{row.get('bl_domain','')}</span>
        <span style="font-size:0.78rem;color:#374151;background:#F3F4F6;
                     padding:2px 8px;border-radius:8px;">{row.get('tech_domain','')}</span>
      </div>
    </div>
    <div style="text-align:right;font-size:0.8rem;color:#6B7280;">
      <div>Author: <b>{row.get('author','—')}</b></div>
      <div>{row.get('created_at','')[:10]}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


def standard_card(row: dict, exception_count: int = 0) -> None:
    exc_html = ""
    if exception_count > 0:
        exc_html = f'<span style="font-size:0.78rem;color:#D97706;background:#FEF3C7;padding:2px 8px;border-radius:8px;">⚠ {exception_count} active exception(s)</span>'

    with st.container():
        st.markdown(f"""
<div style="background:#fff;border:1px solid #E5E7EB;border-radius:10px;
            padding:16px 20px;margin-bottom:12px;border-left:4px solid #059669;">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
    <div>
      <span style="font-size:0.78rem;color:#6B7280;font-family:monospace;">{row.get('std_id','')}</span>
      <h4 style="margin:2px 0 6px;color:#1E2761;font-size:1rem;">{row.get('title','')}</h4>
      <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">
        {status_badge(row.get('status',''))}
        {compliance_badge(row.get('compliance_level',''))}
        <span style="font-size:0.78rem;color:#374151;background:#F3F4F6;
                     padding:2px 8px;border-radius:8px;">{row.get('category','')}</span>
        {exc_html}
      </div>
    </div>
    <div style="text-align:right;font-size:0.8rem;color:#6B7280;">
      <div>Owner: <b>{row.get('owner','—')}</b></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
