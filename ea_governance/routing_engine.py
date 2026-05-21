from datetime import datetime, timedelta
import json


BL_TO_EA = {
    "PWM":      "Sr EA 1 — PWM / Application",
    "PAS":      "Sr EA 2 — PAS / Data & Security",
    "Ops":      "Sr EA 3 — Ops / Process",
    "PTech":    "Cloud Architect EA",
    "Cross-BL": "Risk & Compliance EA",
}

SECURITY_CATEGORIES = {"Security", "Data"}


def score_arch_review(complexity: str, arch_type: str, affected_bls: list,
                      urgency: str, standard_violation: str) -> dict:
    scores = {}

    complexity_map = {"Low": 0, "Medium": 1, "High": 2}
    scores["complexity"] = complexity_map.get(complexity, 0)

    type_map = {
        "Minor change": 0,
        "New solution": 1,
        "Pattern exception": 2,
        "Cross-product dependency": 3,
    }
    scores["arch_type"] = type_map.get(arch_type, 0)

    n = len(affected_bls) if isinstance(affected_bls, list) else 1
    if n <= 1:
        scores["bls_affected"] = 0
    elif n == 2:
        scores["bls_affected"] = 1
    elif n == 3:
        scores["bls_affected"] = 2
    else:
        scores["bls_affected"] = 3

    scores["urgency"] = 1 if urgency == "Urgent" else 0

    violation_map = {"No": 0, "Suspected": 1, "Confirmed": 2}
    scores["standard_violation"] = violation_map.get(standard_violation, 0)

    total = sum(scores.values())
    return {"scores": scores, "total": total}


def route_arch_review(total: int, standard_violation: str) -> dict:
    if standard_violation == "Confirmed" or total >= 10:
        tier = "SAB Escalation"
        sla_days = None
    elif total >= 7:
        tier = "Extended Review"
        sla_days = 14
    elif total >= 4:
        tier = "Standard Review"
        sla_days = 14
    else:
        tier = "Fast-track"
        sla_days = 5

    sla_deadline = None
    if sla_days:
        sla_deadline = (datetime.now() + timedelta(days=sla_days)).isoformat()

    return {"tier": tier, "sla_days": sla_days, "sla_deadline": sla_deadline}


def assign_ea_arch_review(affected_bls: list, submitter_bl: str) -> str:
    bls = affected_bls if isinstance(affected_bls, list) else []
    if len(bls) > 1:
        return "Head of EA"
    primary = bls[0] if bls else submitter_bl
    return BL_TO_EA.get(primary, "Head of EA")


def score_description(scores: dict) -> str:
    """Return a human-readable score breakdown."""
    labels = {
        "complexity":          "Complexity",
        "arch_type":           "Architecture type",
        "bls_affected":        "Business lines affected",
        "urgency":             "Urgency",
        "standard_violation":  "Standard violation",
    }
    parts = []
    for k, v in scores.items():
        parts.append(f"{labels.get(k, k)} = {v}")
    return ", ".join(parts)


def route_std_exception(duration: str, risk_level: str, standard_category: str) -> dict:
    """Route a standards exception request."""
    if standard_category in SECURITY_CATEGORIES:
        tier = "SAB Escalation"
        sla_days = None
    elif duration == "Permanent" or risk_level == "High":
        tier = "SAB Escalation"
        sla_days = None
    else:
        tier = "Standard Review"
        sla_days = 14

    sla_deadline = None
    if sla_days:
        sla_deadline = (datetime.now() + timedelta(days=sla_days)).isoformat()

    return {"tier": tier, "sla_days": sla_days, "sla_deadline": sla_deadline}


def assign_ea_exception(submitter_bl: str) -> str:
    """Domain EA + always Risk & Compliance EA as co-reviewer."""
    domain_ea = BL_TO_EA.get(submitter_bl, "Head of EA")
    co_reviewer = "Risk & Compliance EA"
    if domain_ea == co_reviewer:
        return domain_ea
    return f"{domain_ea} + {co_reviewer}"


def sla_days_remaining(sla_deadline_str: str) -> int | None:
    if not sla_deadline_str:
        return None
    try:
        deadline = datetime.fromisoformat(sla_deadline_str)
        delta = deadline - datetime.now()
        return delta.days
    except Exception:
        return None
