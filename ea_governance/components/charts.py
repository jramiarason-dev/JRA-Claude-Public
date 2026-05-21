"""Plotly chart wrappers for EA Governance dashboards."""
import plotly.graph_objects as go
import plotly.express as px

NAVY   = "#1E2761"
STEEL  = "#4A90D9"
GREEN  = "#059669"
AMBER  = "#D97706"
RED    = "#DC2626"
PURPLE = "#7C3AED"
TEAL   = "#0D9488"

STATUS_COLOR_MAP = {
    "Draft":            "#6B7280",
    "Submitted":        STEEL,
    "Under Review":     AMBER,
    "Decision Pending": PURPLE,
    "Approved":         GREEN,
    "Rejected":         RED,
    "Escalated":        PURPLE,
    "SAB Escalation":   RED,
    "Closed":           "#9CA3AF",
    "Proposed":         STEEL,
    "Accepted":         GREEN,
    "Deprecated":       "#6B7280",
    "Superseded":       AMBER,
    "Active":           GREEN,
    "Under review":     AMBER,
}


def status_donut(data: list[dict], title: str = "") -> go.Figure:
    """data = [{"status": "...", "cnt": N}, ...]"""
    labels = [d["status"] for d in data]
    values = [d["cnt"] for d in data]
    colors = [STATUS_COLOR_MAP.get(s, "#9CA3AF") for s in labels]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
        textinfo="label+percent",
        hovertemplate="%{label}: %{value}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(color=NAVY, size=14)),
        margin=dict(t=40, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=260,
    )
    return fig


def bar_by_status(data: list[dict], x_col: str, y_col: str, title: str = "") -> go.Figure:
    labels = [d[x_col] for d in data]
    values = [d[y_col] for d in data]
    colors = [STATUS_COLOR_MAP.get(l, STEEL) for l in labels]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        text=values, textposition="outside",
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(color=NAVY, size=14)),
        margin=dict(t=40, b=20, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        xaxis=dict(tickfont=dict(size=11)),
        height=260,
    )
    return fig


def sla_gauge(pct_on_time: float) -> go.Figure:
    color = GREEN if pct_on_time >= 80 else (AMBER if pct_on_time >= 60 else RED)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct_on_time,
        number={"suffix": "%"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 60],  "color": "#FEE2E2"},
                {"range": [60, 80], "color": "#FEF3C7"},
                {"range": [80, 100],"color": "#D1FAE5"},
            ],
        },
        title={"text": "SLA Compliance"},
    ))
    fig.update_layout(
        height=220,
        margin=dict(t=30, b=10, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig
