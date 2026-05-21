"""Coloured HTML badge helpers."""

STATUS_COLORS = {
    "Draft":            ("#6B7280", "#F3F4F6"),
    "Submitted":        ("#1D4ED8", "#DBEAFE"),
    "Under Review":     ("#D97706", "#FEF3C7"),
    "Decision Pending": ("#7C3AED", "#EDE9FE"),
    "Approved":         ("#059669", "#D1FAE5"),
    "Rejected":         ("#DC2626", "#FEE2E2"),
    "Escalated":        ("#7C3AED", "#EDE9FE"),
    "SAB Escalation":   ("#7C3AED", "#EDE9FE"),
    "Closed":           ("#6B7280", "#F3F4F6"),
    "Proposed":         ("#1D4ED8", "#DBEAFE"),
    "Accepted":         ("#059669", "#D1FAE5"),
    "Deprecated":       ("#6B7280", "#F3F4F6"),
    "Superseded":       ("#D97706", "#FEF3C7"),
    "Active":           ("#059669", "#D1FAE5"),
    "Under review":     ("#D97706", "#FEF3C7"),
    "Approved temp":    ("#0891B2", "#CFFAFE"),
}

TIER_COLORS = {
    "Fast-track":       ("#0D9488", "#CCFBF1"),
    "Standard Review":  ("#1D4ED8", "#DBEAFE"),
    "Extended Review":  ("#D97706", "#FEF3C7"),
    "SAB Escalation":   ("#DC2626", "#FEE2E2"),
}

COMPLIANCE_COLORS = {
    "Mandatory":    ("#DC2626", "#FEE2E2"),
    "Recommended":  ("#D97706", "#FEF3C7"),
    "Optional":     ("#6B7280", "#F3F4F6"),
}


def _badge(text: str, fg: str, bg: str) -> str:
    return (
        f'<span style="background:{bg};color:{fg};padding:2px 10px;'
        f'border-radius:12px;font-size:0.78rem;font-weight:600;'
        f'white-space:nowrap;">{text}</span>'
    )


def status_badge(status: str) -> str:
    fg, bg = STATUS_COLORS.get(status, ("#374151", "#E5E7EB"))
    return _badge(status, fg, bg)


def tier_badge(tier: str) -> str:
    fg, bg = TIER_COLORS.get(tier, ("#374151", "#E5E7EB"))
    return _badge(tier, fg, bg)


def compliance_badge(level: str) -> str:
    fg, bg = COMPLIANCE_COLORS.get(level, ("#374151", "#E5E7EB"))
    return _badge(level, fg, bg)


def sla_badge(days_remaining) -> str:
    if days_remaining is None:
        return _badge("No SLA", "#6B7280", "#F3F4F6")
    if days_remaining < 0:
        return _badge(f"Overdue {abs(days_remaining)}d", "#DC2626", "#FEE2E2")
    if days_remaining <= 5:
        return _badge(f"{days_remaining}d left", "#D97706", "#FEF3C7")
    return _badge(f"{days_remaining}d left", "#059669", "#D1FAE5")
