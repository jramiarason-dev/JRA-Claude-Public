"""Admin — Data ingestion, templates, library management, demo reset."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import io
import pandas as pd
from datetime import datetime

import database as db

st.set_page_config(page_title="Admin — EA Governance", page_icon="⚙️", layout="wide")

st.markdown("""
<style>
  .stApp { background: #F4F6FA; }
  .stTabs [aria-selected="true"] { background: #1E2761; color: #fff !important; }
</style>
""", unsafe_allow_html=True)

current_user = st.session_state.get("current_user", "Head of EA")
current_role = st.session_state.get("current_role", "EA Lead")

st.markdown("""
<div style="background:#fff;border-radius:12px;padding:20px 24px;margin-bottom:20px;border-left:5px solid #6B7280;">
  <h1 style="margin:0;color:#1E2761;font-size:1.6rem;">⚙️ Administration</h1>
  <p style="margin:4px 0 0;color:#6B7280;">Data ingestion, CSV templates, library management, and demo data reset</p>
</div>
""", unsafe_allow_html=True)

if current_role not in ("EA Reviewer", "EA Lead"):
    st.warning("Admin functions are restricted to EA team members.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(["📥 Bulk Import", "📤 CSV Templates", "📊 Database Summary", "🔄 Demo Reset"])

EA_MEMBERS = [
    "Head of EA", "Sr EA 1 — PWM / Application", "Sr EA 2 — PAS / Data & Security",
    "Sr EA 3 — Ops / Process", "Risk & Compliance EA", "Cloud Architect EA",
]

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: Bulk Import
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Bulk Import")
    st.markdown("Upload a CSV or Excel file to bulk-import standards, patterns, or ADRs.")

    import_type = st.selectbox("Import type", ["Standards", "Patterns", "ADRs"])

    uploaded = st.file_uploader("Upload CSV or XLSX", type=["csv","xlsx"])

    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)

            st.success(f"File loaded: **{len(df)}** rows, {len(df.columns)} columns")
            st.dataframe(df.head(10), use_container_width=True)

            if st.button(f"Import {len(df)} {import_type} →", type="primary"):
                imported = 0
                errors   = []

                for _, row in df.iterrows():
                    try:
                        if import_type == "Standards":
                            std_id = row.get("std_id") or db.next_std_id()
                            scope  = [s.strip() for s in str(row.get("scope","")).split(",")] if row.get("scope") else []
                            db.create_standard({
                                "std_id": str(std_id),
                                "title": str(row.get("title","")),
                                "category": str(row.get("category","")),
                                "status": str(row.get("status","Active")),
                                "description": str(row.get("description","")),
                                "rationale": str(row.get("rationale","")),
                                "scope": scope,
                                "compliance_level": str(row.get("compliance_level","Recommended")),
                                "owner": str(row.get("owner","")),
                                "related_adrs": [],
                                "related_patterns": [],
                            })
                            imported += 1

                        elif import_type == "Patterns":
                            pat_id = row.get("pat_id") or db.next_pat_id()
                            rel_std = [s.strip() for s in str(row.get("related_standards","")).split(",")] if row.get("related_standards") else []
                            db.create_pattern({
                                "pat_id": str(pat_id),
                                "title": str(row.get("title","")),
                                "category": str(row.get("category","")),
                                "problem": str(row.get("problem","")),
                                "solution": str(row.get("solution","")),
                                "when_to_use": str(row.get("when_to_use","")),
                                "when_not_to_use": str(row.get("when_not_to_use","")),
                                "example": str(row.get("example","")),
                                "status": str(row.get("status","Approved")),
                                "owner": str(row.get("owner","")),
                                "related_standards": rel_std,
                            })
                            imported += 1

                        elif import_type == "ADRs":
                            adr_number = row.get("adr_number") or db.next_adr_ref()
                            db.create_adr({
                                "adr_number": str(adr_number),
                                "title": str(row.get("title","")),
                                "status": str(row.get("status","Proposed")),
                                "context": str(row.get("context","")),
                                "decision": str(row.get("decision","")),
                                "rationale": str(row.get("rationale","")),
                                "consequences_positive": str(row.get("consequences_positive","")),
                                "consequences_negative": str(row.get("consequences_negative","")),
                                "alternatives": str(row.get("alternatives","")),
                                "bl_domain": str(row.get("bl_domain","")),
                                "tech_domain": str(row.get("tech_domain","")),
                                "author": str(row.get("author","")),
                                "reviewers": [],
                                "related_standards": [],
                                "related_requests": [],
                            })
                            imported += 1

                    except Exception as e:
                        errors.append(f"Row error: {e}")

                db.log_activity(current_user, f"Bulk imported {import_type}",
                                "system", "IMPORT", f"{imported} rows imported")

                st.success(f"Imported **{imported}** {import_type}.")
                if errors:
                    st.warning(f"{len(errors)} row(s) had errors:")
                    for err in errors[:10]:
                        st.text(err)
                st.rerun()

        except Exception as e:
            st.error(f"Failed to read file: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: CSV Templates
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Download CSV Templates")
    st.markdown("Download these templates, fill them in, and upload via the Bulk Import tab.")

    templates = {
        "Standards": pd.DataFrame(columns=[
            "std_id","title","category","status","description","rationale",
            "scope","compliance_level","owner"
        ]),
        "Patterns": pd.DataFrame(columns=[
            "pat_id","title","category","problem","solution","when_to_use",
            "when_not_to_use","example","status","owner","related_standards"
        ]),
        "ADRs": pd.DataFrame(columns=[
            "adr_number","title","status","context","decision","rationale",
            "consequences_positive","consequences_negative","alternatives",
            "bl_domain","tech_domain","author"
        ]),
    }

    for name, df in templates.items():
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)
        st.download_button(
            label=f"⬇ Download {name} Template",
            data=csv_buf.getvalue(),
            file_name=f"ea_governance_{name.lower()}_template.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.subheader("Export Current Data")

    export_type = st.selectbox("Select data to export", ["Standards", "Patterns", "ADRs",
                                                          "Architecture Reviews", "Standards Exceptions"])
    if st.button("Generate Export"):
        if export_type == "Standards":
            data = db.get_standards()
        elif export_type == "Patterns":
            data = db.get_patterns()
        elif export_type == "ADRs":
            data = db.get_adrs()
        elif export_type == "Architecture Reviews":
            data = db.get_arch_reviews()
        else:
            data = db.get_std_exceptions()

        if data:
            df_export = pd.DataFrame(data)
            csv_out = df_export.to_csv(index=False)
            st.download_button(
                label=f"⬇ Download {export_type} CSV",
                data=csv_out,
                file_name=f"ea_governance_{export_type.lower().replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
        else:
            st.info(f"No {export_type} data to export.")

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: Database Summary
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Database Summary")

    conn = db.get_connection()
    tables = [
        "users", "arch_reviews", "arch_review_decisions",
        "std_exceptions", "std_exception_decisions",
        "adrs", "standards", "patterns", "activity_log"
    ]
    summary = []
    for tbl in tables:
        cnt = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        summary.append({"Table": tbl, "Row count": cnt})
    conn.close()

    st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Activity Log (last 50 entries)")
    recent = db.get_recent_activity(50)
    if recent:
        df_act = pd.DataFrame(recent)[["logged_at","actor","action","entity_type","entity_ref","details"]]
        st.dataframe(df_act, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4: Demo Reset
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Reset to Demo Data")
    st.warning("""
⚠️ **This will delete ALL current data** and reload the original demo data set.

This includes:
- All architecture review requests and decisions
- All standards exception requests and decisions
- All ADRs
- All activity log entries

Standards and patterns will be reset to the 10 seed standards and 6 seed patterns.
    """)

    confirm = st.checkbox("I understand this will delete all data and cannot be undone.")
    if confirm:
        if st.button("🔄 Reset to Demo Data", type="primary"):
            with st.spinner("Resetting database..."):
                db.reset_to_demo()
            st.success("Database reset to demo data successfully!")
            st.balloons()
            st.rerun()
