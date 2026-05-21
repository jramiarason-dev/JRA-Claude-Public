import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "ea_governance.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            bl_domain TEXT,
            tech_domain TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS arch_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference TEXT UNIQUE,
            title TEXT NOT NULL,
            submitter_name TEXT,
            submitter_role TEXT,
            submitter_bl TEXT,
            description TEXT,
            arch_type TEXT,
            affected_bls TEXT,
            complexity TEXT,
            urgency TEXT,
            standard_violation TEXT,
            attachment_path TEXT,
            routing_score INTEGER,
            routing_tier TEXT,
            assigned_ea TEXT,
            status TEXT DEFAULT 'Submitted',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sla_deadline TIMESTAMP,
            updated_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS arch_review_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_id INTEGER REFERENCES arch_reviews(id),
            reviewer_name TEXT,
            standards_alignment TEXT,
            risk_assessment TEXT,
            feasibility TEXT,
            recommendation TEXT,
            conditions TEXT,
            comments TEXT,
            decided_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS std_exceptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference TEXT UNIQUE,
            title TEXT NOT NULL,
            submitter_name TEXT,
            submitter_bl TEXT,
            standard_id TEXT,
            justification TEXT,
            duration TEXT,
            end_date DATE,
            risk_acknowledged BOOLEAN,
            compensating_controls TEXT,
            routing_tier TEXT,
            assigned_ea TEXT,
            status TEXT DEFAULT 'Submitted',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sla_deadline TIMESTAMP,
            updated_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS std_exception_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exception_id INTEGER REFERENCES std_exceptions(id),
            reviewer_name TEXT,
            decision TEXT,
            conditions TEXT,
            comments TEXT,
            decided_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS adrs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            adr_number TEXT UNIQUE,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'Proposed',
            context TEXT,
            decision TEXT,
            rationale TEXT,
            consequences_positive TEXT,
            consequences_negative TEXT,
            alternatives TEXT,
            bl_domain TEXT,
            tech_domain TEXT,
            author TEXT,
            reviewers TEXT,
            related_standards TEXT,
            related_requests TEXT,
            superseded_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS standards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            std_id TEXT UNIQUE,
            title TEXT NOT NULL,
            category TEXT,
            status TEXT DEFAULT 'Active',
            description TEXT,
            rationale TEXT,
            scope TEXT,
            compliance_level TEXT,
            owner TEXT,
            related_adrs TEXT,
            related_patterns TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pat_id TEXT UNIQUE,
            title TEXT NOT NULL,
            category TEXT,
            problem TEXT,
            solution TEXT,
            when_to_use TEXT,
            when_not_to_use TEXT,
            example TEXT,
            status TEXT DEFAULT 'Approved',
            owner TEXT,
            related_standards TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor TEXT,
            action TEXT,
            entity_type TEXT,
            entity_ref TEXT,
            details TEXT,
            logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


# ── Reference generators ──────────────────────────────────────────────────────

def _next_ref(prefix: str, table: str, col: str) -> str:
    year = datetime.now().year
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} LIKE ?", (f"{prefix}-{year}-%",))
    n = c.fetchone()[0] + 1
    conn.close()
    return f"{prefix}-{year}-{n:03d}"


def next_ar_ref():   return _next_ref("AR",  "arch_reviews",  "reference")
def next_ex_ref():   return _next_ref("EX",  "std_exceptions", "reference")
def next_adr_ref():  return _next_ref("ADR", "adrs",           "adr_number")
def next_std_id():   return _next_ref("STD", "standards",      "std_id")
def next_pat_id():   return _next_ref("PAT", "patterns",       "pat_id")


# ── Activity log ──────────────────────────────────────────────────────────────

def log_activity(actor: str, action: str, entity_type: str, entity_ref: str, details: str = ""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO activity_log (actor, action, entity_type, entity_ref, details) VALUES (?,?,?,?,?)",
        (actor, action, entity_type, entity_ref, details)
    )
    conn.commit()
    conn.close()


def get_recent_activity(limit: int = 20):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM activity_log ORDER BY logged_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Users ─────────────────────────────────────────────────────────────────────

def get_all_users():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_ea_members():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM users WHERE role IN ('EA Reviewer','EA Lead') ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Arch Reviews ──────────────────────────────────────────────────────────────

def create_arch_review(data: dict) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO arch_reviews
        (reference, title, submitter_name, submitter_role, submitter_bl,
         description, arch_type, affected_bls, complexity, urgency,
         standard_violation, attachment_path, routing_score, routing_tier,
         assigned_ea, status, sla_deadline, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data["reference"], data["title"], data["submitter_name"],
        data["submitter_role"], data["submitter_bl"], data["description"],
        data["arch_type"], json.dumps(data.get("affected_bls", [])),
        data["complexity"], data["urgency"], data["standard_violation"],
        data.get("attachment_path", ""), data["routing_score"],
        data["routing_tier"], data["assigned_ea"], data.get("status", "Submitted"),
        data["sla_deadline"], datetime.now().isoformat()
    ))
    row_id = c.lastrowid
    conn.commit()
    conn.close()
    return row_id


def get_arch_reviews(status: Optional[str] = None, assigned_ea: Optional[str] = None):
    conn = get_connection()
    q = "SELECT * FROM arch_reviews WHERE 1=1"
    params = []
    if status:
        q += " AND status = ?"
        params.append(status)
    if assigned_ea:
        q += " AND assigned_ea = ?"
        params.append(assigned_ea)
    q += " ORDER BY submitted_at DESC"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_arch_review(review_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM arch_reviews WHERE id = ?", (review_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_arch_review_status(review_id: int, status: str, actor: str):
    conn = get_connection()
    conn.execute(
        "UPDATE arch_reviews SET status=?, updated_at=? WHERE id=?",
        (status, datetime.now().isoformat(), review_id)
    )
    conn.commit()
    conn.close()


def save_arch_review_decision(data: dict):
    conn = get_connection()
    conn.execute("""
        INSERT INTO arch_review_decisions
        (review_id, reviewer_name, standards_alignment, risk_assessment,
         feasibility, recommendation, conditions, comments)
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        data["review_id"], data["reviewer_name"], data["standards_alignment"],
        data["risk_assessment"], data["feasibility"], data["recommendation"],
        data.get("conditions", ""), data.get("comments", "")
    ))
    conn.execute(
        "UPDATE arch_reviews SET status=?, updated_at=? WHERE id=?",
        (data["new_status"], datetime.now().isoformat(), data["review_id"])
    )
    conn.commit()
    conn.close()


def get_arch_review_decisions(review_id: int):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM arch_review_decisions WHERE review_id=? ORDER BY decided_at DESC",
        (review_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Standards Exceptions ──────────────────────────────────────────────────────

def create_std_exception(data: dict) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO std_exceptions
        (reference, title, submitter_name, submitter_bl, standard_id,
         justification, duration, end_date, risk_acknowledged,
         compensating_controls, routing_tier, assigned_ea, status, sla_deadline, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data["reference"], data["title"], data["submitter_name"],
        data["submitter_bl"], data["standard_id"], data["justification"],
        data["duration"], data.get("end_date"), data["risk_acknowledged"],
        data.get("compensating_controls", ""), data["routing_tier"],
        data["assigned_ea"], data.get("status", "Submitted"),
        data["sla_deadline"], datetime.now().isoformat()
    ))
    row_id = c.lastrowid
    conn.commit()
    conn.close()
    return row_id


def get_std_exceptions(status: Optional[str] = None, assigned_ea: Optional[str] = None):
    conn = get_connection()
    q = "SELECT * FROM std_exceptions WHERE 1=1"
    params = []
    if status:
        q += " AND status = ?"
        params.append(status)
    if assigned_ea:
        q += " AND assigned_ea = ?"
        params.append(assigned_ea)
    q += " ORDER BY submitted_at DESC"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_std_exception(ex_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM std_exceptions WHERE id = ?", (ex_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def save_std_exception_decision(data: dict):
    conn = get_connection()
    conn.execute("""
        INSERT INTO std_exception_decisions
        (exception_id, reviewer_name, decision, conditions, comments)
        VALUES (?,?,?,?,?)
    """, (
        data["exception_id"], data["reviewer_name"], data["decision"],
        data.get("conditions", ""), data.get("comments", "")
    ))
    conn.execute(
        "UPDATE std_exceptions SET status=?, updated_at=? WHERE id=?",
        (data["new_status"], datetime.now().isoformat(), data["exception_id"])
    )
    conn.commit()
    conn.close()


def get_std_exception_decisions(ex_id: int):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM std_exception_decisions WHERE exception_id=? ORDER BY decided_at DESC",
        (ex_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── ADRs ──────────────────────────────────────────────────────────────────────

def create_adr(data: dict) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO adrs
        (adr_number, title, status, context, decision, rationale,
         consequences_positive, consequences_negative, alternatives,
         bl_domain, tech_domain, author, reviewers, related_standards,
         related_requests, superseded_by, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data["adr_number"], data["title"], data.get("status", "Proposed"),
        data.get("context", ""), data.get("decision", ""),
        data.get("rationale", ""), data.get("consequences_positive", ""),
        data.get("consequences_negative", ""), data.get("alternatives", ""),
        data.get("bl_domain", ""), data.get("tech_domain", ""),
        data.get("author", ""), json.dumps(data.get("reviewers", [])),
        json.dumps(data.get("related_standards", [])),
        json.dumps(data.get("related_requests", [])),
        data.get("superseded_by", ""), datetime.now().isoformat()
    ))
    row_id = c.lastrowid
    conn.commit()
    conn.close()
    return row_id


def get_adrs(status: Optional[str] = None, bl_domain: Optional[str] = None):
    conn = get_connection()
    q = "SELECT * FROM adrs WHERE 1=1"
    params = []
    if status:
        q += " AND status = ?"
        params.append(status)
    if bl_domain:
        q += " AND bl_domain = ?"
        params.append(bl_domain)
    q += " ORDER BY created_at DESC"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_adr(adr_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM adrs WHERE id = ?", (adr_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_adr(adr_id: int, data: dict):
    conn = get_connection()
    conn.execute("""
        UPDATE adrs SET title=?, status=?, context=?, decision=?, rationale=?,
        consequences_positive=?, consequences_negative=?, alternatives=?,
        bl_domain=?, tech_domain=?, reviewers=?, related_standards=?,
        related_requests=?, superseded_by=?, updated_at=?
        WHERE id=?
    """, (
        data["title"], data["status"], data.get("context", ""),
        data.get("decision", ""), data.get("rationale", ""),
        data.get("consequences_positive", ""), data.get("consequences_negative", ""),
        data.get("alternatives", ""), data.get("bl_domain", ""),
        data.get("tech_domain", ""), json.dumps(data.get("reviewers", [])),
        json.dumps(data.get("related_standards", [])),
        json.dumps(data.get("related_requests", [])),
        data.get("superseded_by", ""), datetime.now().isoformat(), adr_id
    ))
    conn.commit()
    conn.close()


# ── Standards ─────────────────────────────────────────────────────────────────

def get_standards(status: Optional[str] = None, category: Optional[str] = None):
    conn = get_connection()
    q = "SELECT * FROM standards WHERE 1=1"
    params = []
    if status:
        q += " AND status = ?"
        params.append(status)
    if category:
        q += " AND category = ?"
        params.append(category)
    q += " ORDER BY std_id"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_standard(std_id: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM standards WHERE std_id = ?", (std_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_standard(data: dict) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO standards
        (std_id, title, category, status, description, rationale, scope,
         compliance_level, owner, related_adrs, related_patterns, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data["std_id"], data["title"], data.get("category", ""),
        data.get("status", "Active"), data.get("description", ""),
        data.get("rationale", ""), json.dumps(data.get("scope", [])),
        data.get("compliance_level", "Recommended"), data.get("owner", ""),
        json.dumps(data.get("related_adrs", [])),
        json.dumps(data.get("related_patterns", [])),
        datetime.now().isoformat()
    ))
    row_id = c.lastrowid
    conn.commit()
    conn.close()
    return row_id


def update_standard(std_id: str, data: dict):
    conn = get_connection()
    conn.execute("""
        UPDATE standards SET title=?, category=?, status=?, description=?,
        rationale=?, scope=?, compliance_level=?, owner=?,
        related_adrs=?, related_patterns=?, updated_at=? WHERE std_id=?
    """, (
        data["title"], data.get("category", ""), data.get("status", "Active"),
        data.get("description", ""), data.get("rationale", ""),
        json.dumps(data.get("scope", [])), data.get("compliance_level", "Recommended"),
        data.get("owner", ""), json.dumps(data.get("related_adrs", [])),
        json.dumps(data.get("related_patterns", [])),
        datetime.now().isoformat(), std_id
    ))
    conn.commit()
    conn.close()


def get_standard_exception_count(std_id: str) -> int:
    conn = get_connection()
    row = conn.execute(
        "SELECT COUNT(*) as cnt FROM std_exceptions WHERE standard_id=? AND status NOT IN ('Closed','Rejected')",
        (std_id,)
    ).fetchone()
    conn.close()
    return row["cnt"] if row else 0


def delete_standard(std_id: str) -> bool:
    count = get_standard_exception_count(std_id)
    if count > 0:
        return False
    conn = get_connection()
    conn.execute("DELETE FROM standards WHERE std_id=?", (std_id,))
    conn.commit()
    conn.close()
    return True


# ── Patterns ──────────────────────────────────────────────────────────────────

def get_patterns(status: Optional[str] = None, category: Optional[str] = None):
    conn = get_connection()
    q = "SELECT * FROM patterns WHERE 1=1"
    params = []
    if status:
        q += " AND status = ?"
        params.append(status)
    if category:
        q += " AND category = ?"
        params.append(category)
    q += " ORDER BY pat_id"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_pattern(data: dict) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO patterns
        (pat_id, title, category, problem, solution, when_to_use,
         when_not_to_use, example, status, owner, related_standards, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data["pat_id"], data["title"], data.get("category", ""),
        data.get("problem", ""), data.get("solution", ""),
        data.get("when_to_use", ""), data.get("when_not_to_use", ""),
        data.get("example", ""), data.get("status", "Approved"),
        data.get("owner", ""), json.dumps(data.get("related_standards", [])),
        datetime.now().isoformat()
    ))
    row_id = c.lastrowid
    conn.commit()
    conn.close()
    return row_id


def update_pattern(pat_id: str, data: dict):
    conn = get_connection()
    conn.execute("""
        UPDATE patterns SET title=?, category=?, problem=?, solution=?,
        when_to_use=?, when_not_to_use=?, example=?, status=?, owner=?,
        related_standards=?, updated_at=? WHERE pat_id=?
    """, (
        data["title"], data.get("category", ""), data.get("problem", ""),
        data.get("solution", ""), data.get("when_to_use", ""),
        data.get("when_not_to_use", ""), data.get("example", ""),
        data.get("status", "Approved"), data.get("owner", ""),
        json.dumps(data.get("related_standards", [])),
        datetime.now().isoformat(), pat_id
    ))
    conn.commit()
    conn.close()


# ── Dashboard metrics ─────────────────────────────────────────────────────────

def get_dashboard_metrics():
    conn = get_connection()
    now = datetime.now().isoformat()

    ar_open = conn.execute(
        "SELECT COUNT(*) FROM arch_reviews WHERE status NOT IN ('Closed','Approved','Rejected','Escalated')"
    ).fetchone()[0]
    ar_by_status = conn.execute(
        "SELECT status, COUNT(*) as cnt FROM arch_reviews GROUP BY status"
    ).fetchall()

    ex_open = conn.execute(
        "SELECT COUNT(*) FROM std_exceptions WHERE status NOT IN ('Closed','Approved','Rejected','SAB Escalation')"
    ).fetchone()[0]

    ar_overdue = conn.execute(
        "SELECT COUNT(*) FROM arch_reviews WHERE sla_deadline < ? AND status NOT IN ('Closed','Approved','Rejected','Escalated')",
        (now,)
    ).fetchone()[0]
    ex_overdue = conn.execute(
        "SELECT COUNT(*) FROM std_exceptions WHERE sla_deadline < ? AND status NOT IN ('Closed','Approved','Rejected','SAB Escalation')",
        (now,)
    ).fetchone()[0]

    adr_by_status = conn.execute(
        "SELECT status, COUNT(*) as cnt FROM adrs GROUP BY status"
    ).fetchall()

    std_by_status = conn.execute(
        "SELECT status, COUNT(*) as cnt FROM standards GROUP BY status"
    ).fetchall()

    sab_items = conn.execute(
        "SELECT COUNT(*) FROM arch_reviews WHERE routing_tier='SAB Escalation' AND status NOT IN ('Closed','Approved','Rejected')"
    ).fetchone()[0]

    conn.close()
    return {
        "ar_open": ar_open,
        "ex_open": ex_open,
        "ar_overdue": ar_overdue,
        "ex_overdue": ex_overdue,
        "ar_by_status": [dict(r) for r in ar_by_status],
        "adr_by_status": [dict(r) for r in adr_by_status],
        "std_by_status": [dict(r) for r in std_by_status],
        "sab_items": sab_items,
    }


def reset_to_demo():
    """Drop all data and re-seed."""
    conn = get_connection()
    for tbl in ["activity_log","arch_review_decisions","std_exception_decisions",
                "arch_reviews","std_exceptions","adrs","standards","patterns","users"]:
        conn.execute(f"DELETE FROM {tbl}")
        conn.execute(f"DELETE FROM sqlite_sequence WHERE name='{tbl}'")
    conn.commit()
    conn.close()
    from data.seed_data import seed
    seed()
