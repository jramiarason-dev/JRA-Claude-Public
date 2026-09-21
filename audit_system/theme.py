"""Stylesheet for the AuditIQ Streamlit app.

Kept out of app.py so the application file stays readable: this is ~880
lines of CSS with no Python in it. Both values are plain string literals —
no interpolation — so app.py injects them unchanged.
"""

# CSS custom properties, consumed by BASE_CSS through var().
THEME_VARS = """
    :root {
      --bg-main:         #07090f;
      --bg-app:          #07090f;
      --bg-primary:      #07090f;
      --bg-secondary:    #0b0f1a;
      --bg-card:         #0d1117;
      --bg-card-hover:   #131925;
      --bg-input:        #0d1117;
      --bg-sidebar:      #080b12;
      --border-subtle:   rgba(255,255,255,0.06);
      --border-medium:   rgba(255,255,255,0.10);
      --border-input:    rgba(255,255,255,0.08);
      --border-accent:   rgba(99,102,241,0.30);
      --border-divider:  rgba(255,255,255,0.05);
      --text-primary:    #eef2ff;
      --text-secondary:  #94a3b8;
      --text-muted:      #4a5568;
      --text-accent:     #a5b4fc;
      --text-label:      #8392bb;
      --accent-primary:  #6366f1;
      --accent-secondary:#818cf8;
      --accent-hover:    #818cf8;
      --accent-glow:     rgba(99,102,241,0.15);
      --accent-blue:     #6366f1;
      --shadow-card:     0 1px 3px rgba(0,0,0,0.4), 0 4px 16px rgba(0,0,0,0.25);
      --shadow-elevated: 0 2px 8px rgba(0,0,0,0.5), 0 12px 32px rgba(0,0,0,0.3);
      --radius-sm:       8px;
      --radius-md:       12px;
      --radius-lg:       16px;
      --critical:        #ef4444;
      --critical-bg:     rgba(239,68,68,0.10);
      --high:            #f97316;
      --high-bg:         rgba(249,115,22,0.10);
      --moderate:        #eab308;
      --moderate-bg:     rgba(234,179,8,0.10);
      --low:             #22c55e;
      --low-bg:          rgba(34,197,94,0.10);
      --tab-inactive:          #5a6488;
      --tab-active:            #818cf8;
      --tab-active-border:     #6366f1;
      --btn-primary-bg:        linear-gradient(135deg,#6366f1 0%,#4f46e5 100%);
      --btn-secondary-bg:      rgba(99,102,241,0.14);
      --btn-secondary-color:   #818cf8;
      --btn-secondary-border:  rgba(99,102,241,0.25);
      --ctx-pill-bg:           rgba(34,211,165,0.07);
      --ctx-pill-border:       rgba(34,211,165,0.18);
      --ctx-pill-color:        #22d3a5;
      --output-box-bg:         #0d1117;
      --output-box-border:     rgba(255,255,255,0.06);
      --output-box-text:       #eef2ff;
      --section-title-color:   #eef2ff;
      --footer-color:          #4a5568;
      --tbl-row-border:        rgba(255,255,255,0.05);
      --sidebar-header-color:  #4a5568;
    }
    """

# Static rules. Uses var() throughout, so no f-string is needed.
BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, p, span, div, label, input, textarea, select, button {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
h1, h2, h3 {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  letter-spacing: -0.5px;
}
.stApp {
  background: var(--bg-main) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}
.main .block-container {
  padding: 2rem 2.5rem 4rem !important;
  max-width: 1100px !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: var(--bg-sidebar) !important;
  border-right: 1px solid var(--border-subtle) !important;
}
section[data-testid="stSidebar"] .stMarkdown p { color: var(--text-secondary); font-size: 13px; }

/* ── Tabs — glassmorphism pill style ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-card) !important;
  border-radius: 12px !important;
  padding: 4px !important;
  border: 1px solid var(--border-subtle) !important;
  gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 8px !important;
  color: var(--text-muted) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  padding: 8px 16px !important;
  border: none !important;
  transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(99,102,241,0.20) 0%, rgba(99,102,241,0.10) 100%) !important;
  color: var(--accent-hover) !important;
  font-weight: 600 !important;
  box-shadow: 0 1px 0 rgba(99,102,241,0.4), inset 0 1px 0 rgba(99,102,241,0.1) !important;
}
.stTabs [data-baseweb="tab"]:hover {
  background: rgba(255,255,255,0.04) !important;
  color: var(--text-secondary) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="select"] > div:first-child {
  background: var(--bg-input) !important;
  border: 1px solid var(--border-medium) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
  font-size: 13.5px !important;
  transition: border-color 0.15s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: rgba(99,102,241,0.5) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
  outline: none !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label, .stMultiSelect label,
label[data-testid="stWidgetLabel"] p {
  font-size: 12px !important;
  font-weight: 600 !important;
  color: var(--text-secondary) !important;
  letter-spacing: 0.3px !important;
  text-transform: uppercase !important;
}
/* ── Labels ── */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
  font-size: 12px !important;
  font-weight: 600 !important;
  letter-spacing: 0.04em !important;
  text-transform: uppercase !important;
  color: var(--text-muted) !important;
  margin-bottom: 4px !important;
}
::placeholder { color: var(--text-muted) !important; font-style: italic; }

/* ── Buttons ── */
div[data-testid="stButton"] > button {
  border-radius: var(--radius-sm) !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  letter-spacing: 0.01em !important;
  transition: all 0.15s ease !important;
  border: 1px solid var(--border-medium) !important;
  background: rgba(255,255,255,0.04) !important;
  color: var(--text-secondary) !important;
}
div[data-testid="stButton"] > button:hover {
  background: rgba(255,255,255,0.08) !important;
  border-color: rgba(255,255,255,0.16) !important;
  color: var(--text-primary) !important;
}
div[data-testid="stButton"] > button[kind="primary"],
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
  border: none !important;
  color: #fff !important;
  box-shadow: 0 2px 12px rgba(99,102,241,0.35) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
  box-shadow: 0 4px 20px rgba(99,102,241,0.5) !important;
  transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:active { transform: translateY(0) !important; }
div[data-testid="stButton"] > button[kind="primary"]:disabled {
  background: #1a1f32 !important; color: #3a4566 !important;
}
div[data-testid="stDownloadButton"] button {
  border-radius: var(--radius-sm) !important;
  font-weight: 600 !important;
  font-size: 12.5px !important;
  border: 1px solid var(--border-medium) !important;
  background: rgba(255,255,255,0.04) !important;
  color: var(--text-secondary) !important;
  min-height: 36px !important;
  transition: all 0.15s ease !important;
}
div[data-testid="stDownloadButton"] button:hover {
  background: rgba(255,255,255,0.08) !important;
  color: var(--text-primary) !important;
}
/* Uniform export bar button heights */
div[data-testid="stButton"] button { min-height: 36px !important; }
.wk-btn button {
  background: rgba(255,102,0,.08) !important;
  border: 1px solid rgba(255,102,0,.25) !important;
  color: #ff8533 !important;
  border-radius: 8px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  min-height: 36px !important;
}
.wk-btn button:hover {
  background: rgba(255,102,0,.15) !important;
  border-color: rgba(255,102,0,.45) !important;
}
div[data-testid="stFileUploader"] {
  border: 1px dashed var(--border-medium) !important;
  border-radius: 10px !important; background: var(--bg-input) !important;
}
hr { border: none; border-top: 1px solid var(--border-divider) !important; margin: 1.8rem 0; }

/* ── Content blocks ── */
.output-box {
  background: var(--output-box-bg);
  border: 1px solid var(--output-box-border);
  border-radius: 10px; padding: 20px 24px;
  font-size: 13px; line-height: 1.9; white-space: pre-wrap;
  color: var(--output-box-text); max-height: 560px; overflow-y: auto;
}
.section-title {
  font-size: 15px; font-weight: 600; color: var(--section-title-color);
  margin: 1.8rem 0 1rem; letter-spacing: -0.2px;
}
.ctx-pill {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--ctx-pill-bg); border: 1px solid var(--ctx-pill-border);
  color: var(--ctx-pill-color); border-radius: 8px; padding: 6px 14px;
  font-size: 12.5px; font-weight: 500; margin-bottom: 1.4rem;
}

/* ── Data table ── */
.data-table { width: 100%; border-collapse: collapse; font-size: 12.5px; margin-bottom: 0.5rem; }
.data-table th {
  padding: 9px 13px; text-align: left; font-weight: 600;
  font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.5px;
}
.data-table td { padding: 10px 13px; vertical-align: top; line-height: 1.6; }
.data-table tr:not(:last-child) td { border-bottom: 1px solid var(--tbl-row-border); }

/* ── Badges ── */
.badge-critical { display:inline-block; background:rgba(239,68,68,0.15); color:#ef4444;
  border:1px solid rgba(239,68,68,0.35); border-radius:20px; padding:2px 8px;
  font-size:11px; font-weight:700; white-space:nowrap; }
.badge-high { display:inline-block; background:rgba(249,115,22,0.12); color:#f97316;
  border:1px solid rgba(249,115,22,0.32); border-radius:20px; padding:2px 8px;
  font-size:11px; font-weight:700; white-space:nowrap; }
.badge-medium { display:inline-block; background:rgba(234,179,8,0.10); color:#eab308;
  border:1px solid rgba(234,179,8,0.28); border-radius:20px; padding:2px 8px;
  font-size:11px; font-weight:700; white-space:nowrap; }
.badge-open { display:inline-block; background:rgba(34,211,165,0.10); color:#22d3a5;
  border:1px solid rgba(34,211,165,0.28); border-radius:20px; padding:2px 8px;
  font-size:11px; font-weight:600; white-space:nowrap; }
.badge-info { display:inline-block; background:rgba(99,102,241,0.10); color:#818cf8;
  border:1px solid rgba(99,102,241,0.28); border-radius:20px; padding:2px 8px;
  font-size:11px; font-weight:600; white-space:nowrap; }

/* ── Risk cards — glassmorphism ── */
.risk-card {
  background: rgba(15,21,32,0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 12px;
  border: 1px solid var(--border-subtle);
  padding: 16px;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
  margin-bottom: 12px;
}
.risk-card:hover {
  transform: translateY(-2px);
  border-color: var(--border-accent);
  box-shadow: 0 8px 32px rgba(99,102,241,0.08);
}
.risk-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
}
.risk-card-critical::before { background: linear-gradient(90deg, #ef4444, transparent); }
.risk-card-high::before     { background: linear-gradient(90deg, #f97316, transparent); }
.risk-card-moderate::before { background: linear-gradient(90deg, #eab308, transparent); }

/* ── Progress bar ── */
.progress-bar-wrap { display: flex; align-items: center; gap: 0; margin: 0.6rem 0 1.6rem; }
.pb-step {
  display: flex; align-items: center; gap: 8px;
  font-size: 12.5px; font-weight: 500; padding: 7px 16px;
  border-radius: 20px; transition: all 0.2s;
}
.pb-step.done { background: rgba(34,211,165,0.10); color: #22d3a5; border: 1px solid rgba(34,211,165,0.25); }
.pb-step.active { background: rgba(99,102,241,0.12); color: #818cf8; border: 1px solid rgba(99,102,241,0.30); }
.pb-step.pending { color: var(--text-muted); border: 1px solid var(--border-subtle); }
.pb-connector { flex: 1; height: 1px; background: var(--border-subtle); margin: 0 4px; min-width: 16px; }

/* ── Gauge ── */
.gauge-wrap { display: flex; align-items: center; gap: 32px; margin: 1rem 0 1.4rem; }
.gauge-circle {
  width: 110px; height: 110px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  flex-direction: column; font-weight: 700;
}
.gauge-score { font-size: 30px; line-height: 1; }
.gauge-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px; }
.gauge-breakdown { flex: 1; }
.gbar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 7px; font-size: 12px; }
.gbar-label { width: 68px; color: var(--text-secondary); text-align: right; flex-shrink: 0; }
.gbar-track { flex: 1; background: var(--border-subtle); border-radius: 4px; height: 8px; overflow: hidden; }
.gbar-fill { height: 100%; border-radius: 4px; transition: width 0.4s; }
.gbar-count { width: 20px; text-align: right; color: var(--text-secondary); flex-shrink: 0; }

/* ── Expanders ── */
.streamlit-expanderHeader {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 8px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: var(--text-secondary) !important;
  padding: 12px 16px !important;
  transition: all 0.2s ease !important;
}
.streamlit-expanderHeader:hover {
  border-color: var(--border-accent) !important;
  color: var(--text-accent) !important;
  background: var(--bg-card-hover) !important;
}
.streamlit-expanderContent {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-top: none !important;
  border-radius: 0 0 8px 8px !important;
  padding: 16px !important;
}

/* ── History item ── */
.hist-item {
  background: var(--bg-card); border: 1px solid var(--border-subtle);
  border-radius: 8px; padding: 8px 12px; margin-bottom: 6px; font-size: 12px; cursor: pointer;
}
.hist-topic { color: var(--text-primary); font-weight: 600; }
.hist-meta { color: var(--text-muted); font-size: 11px; margin-top: 2px; }

/* ── Footer ── */
.footer { font-size: 11px; color: var(--footer-color); text-align: center; margin-top: 2.5rem; letter-spacing: 0.3px; }

/* ── Mode toggle radio — overridden by utility classes below ── */

/* ── Sidebar section cards ── */
.sidebar-section {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 10px; padding: 12px; margin-bottom: 12px;
}
.sidebar-section-title {
  font-size: 10px; font-weight: 700; letter-spacing: 1.5px;
  color: var(--sidebar-header-color); text-transform: uppercase; margin-bottom: 10px;
}

/* ── Section header ── */
.section-header {
  display: flex; align-items: center; gap: 10px;
  margin: 24px 0 16px 0; padding-bottom: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.section-header-icon {
  width: 32px; height: 32px;
  background: rgba(99,102,241,0.10);
  border: 1px solid rgba(99,102,241,0.20);
  border-radius: 8px; display: flex;
  align-items: center; justify-content: center; flex-shrink: 0;
}
.section-count-badge {
  background: rgba(99,102,241,0.12); color: #6366f1;
  border: 1px solid rgba(99,102,241,0.2); border-radius: 20px;
  padding: 2px 8px; font-size: 11px; font-weight: 600; margin-left: 8px;
}

/* ── Loading spinner ── */
@keyframes spin { to { transform: rotate(360deg); } }
.loading-spinner {
  display: flex; align-items: center; gap: 12px;
  background: rgba(99,102,241,0.06);
  border: 1px solid rgba(99,102,241,0.15);
  border-radius: 10px; padding: 16px 20px; margin: 16px 0;
}
.loading-spinner-dot {
  width: 16px; height: 16px;
  border: 2px solid rgba(99,102,241,0.2);
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  flex-shrink: 0;
}

/* ── Mobile responsive ── */
@media (max-width: 768px) {
  .main .block-container { padding: 1rem 1rem 3rem !important; }
  .data-table { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }
  div[data-testid="stButton"] > button[kind="primary"] { width: 100% !important; }
  div[data-testid="stDownloadButton"] button { width: 100% !important; }
  .gauge-wrap { flex-direction: column; align-items: flex-start; }
  .stColumns { flex-direction: column !important; }
  .stColumns > div { width: 100% !important; min-width: 100% !important; }
}

/* ── Sidebar styling ── */
section[data-testid="stSidebar"] {
  background: var(--bg-sidebar) !important;
  border-right: 1px solid var(--border-subtle) !important;
  width: 248px !important;
  min-width: 248px !important;
}
section[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="collapsedControl"] { display: none !important; }
/* Remove Streamlit default main-area left padding (sidebar already takes space) */
.main .block-container { padding-left: 1.5rem !important; }

/* ── Print ── */
@media print {
  section[data-testid="stSidebar"] { display: none !important; }
  div[data-testid="stButton"], div[data-testid="stDownloadButton"],
  div[data-testid="stFileUploader"], div[data-testid="stTextInput"],
  div[data-testid="stTextArea"], div[data-testid="stMultiSelect"],
  div[data-testid="stSelectbox"], .stTabs [data-baseweb="tab-list"],
  .no-print { display: none !important; }
  .stApp { background: #fff !important; color: #000 !important; }
  .output-box { max-height: none !important; overflow: visible !important;
    background: #fff !important; color: #000 !important; border-color: #ccc !important; }
  .data-table td, .data-table th { border: 1px solid #ccc !important; color: #000 !important; }
  .section-title { color: #000 !important; }
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
  padding: 20px 24px !important;
  box-shadow: var(--shadow-card) !important;
  transition: box-shadow 0.2s ease !important;
}
[data-testid="stMetric"]:hover {
  box-shadow: var(--shadow-elevated) !important;
}
[data-testid="stMetric"] label {
  font-size: 11px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: .08em !important;
  color: var(--text-muted) !important;
}
[data-testid="stMetricValue"] > div {
  font-size: 30px !important;
  font-weight: 800 !important;
  color: var(--text-primary) !important;
  letter-spacing: -0.04em !important;
}
[data-testid="stMetricDelta"] {
  font-size: 12px !important;
  font-weight: 600 !important;
  border-radius: 6px !important;
  padding: 2px 6px !important;
}

/* ── Multiselect tags ── */
.stMultiSelect [data-baseweb="tag"] {
  background: rgba(99,102,241,.15) !important;
  border: 1px solid rgba(99,102,241,.3) !important;
  color: #818cf8 !important;
  border-radius: 6px !important;
  font-size: 12px !important;
}
.stMultiSelect [data-baseweb="tag"] span { color: #818cf8 !important; }
.stMultiSelect [data-baseweb="tag"] button { color: #818cf8 !important; opacity: .7; }
.stMultiSelect [data-baseweb="select"] > div {
  background: var(--bg-input) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 8px !important;
}

/* ── Native progress bar ── */
.stProgress > div > div {
  background: rgba(255,255,255,.06) !important;
  border-radius: 6px !important;
  height: 6px !important;
}
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, #6366f1, #818cf8) !important;
  border-radius: 6px !important;
}

/* ── Checkboxes ── */
.stCheckbox label span { color: var(--text-secondary) !important; font-size: 13px !important; }
.stCheckbox [data-baseweb="checkbox"] span {
  border-color: var(--border-medium) !important;
  background: rgba(255,255,255,.03) !important;
  border-radius: 4px !important;
}

/* ── Slider ── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
  background: var(--accent-primary) !important;
  border-color: var(--accent-primary) !important;
  box-shadow: 0 0 0 4px var(--accent-glow) !important;
}

/* ── Expander (Streamlit 1.58 selectors) ── */
[data-testid="stExpander"] {
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
  background: var(--bg-card) !important;
  overflow: hidden !important;
  box-shadow: var(--shadow-card) !important;
  margin-bottom: 10px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] details > summary {
  background: var(--bg-card) !important;
  color: var(--text-secondary) !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  padding: 12px 16px 12px 36px !important;
  list-style: none !important;
  display: block !important;
  position: relative !important;
  cursor: pointer !important;
  letter-spacing: 0.01em !important;
}
/* Nuclear icon suppression: hide every child that is not the label p/span */
[data-testid="stExpander"] summary::-webkit-details-marker { display:none !important; }
[data-testid="stExpander"] summary::marker { content:"" !important; }
/* Hide ALL direct children (icons) and then re-show only the label */
[data-testid="stExpander"] summary > * {
  display: none !important;
}
/* Re-show label elements — Streamlit puts the label in p or span[data-testid] */
[data-testid="stExpander"] summary > p,
[data-testid="stExpander"] summary > div > p,
[data-testid="stExpander"] summary [data-testid="StyledLabelText"],
[data-testid="stExpander"] summary [class*="Label"],
[data-testid="stExpander"] summary [class*="label"] {
  display: inline !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: var(--text-secondary) !important;
}
/* CSS arrow indicator replacing the icon */
[data-testid="stExpander"] summary::before,
[data-testid="stExpander"] details > summary::before {
  content: "›" !important;
  position: absolute !important;
  left: 12px !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  font-size: 16px !important;
  font-weight: 700 !important;
  color: var(--text-muted) !important;
  transition: transform .15s !important;
  font-family: 'Inter', sans-serif !important;
}
[data-testid="stExpander"] details[open] > summary::before {
  content: "⌄" !important;
  transform: translateY(-60%) !important;
}
[data-testid="stExpander"] summary:hover {
  background: var(--bg-card-hover) !important;
  color: var(--text-accent) !important;
}
[data-testid="stExpander"] > div > div {
  padding: 12px 16px 16px !important;
}

/* ── Selectbox / dropdown menu ── */
[data-baseweb="popover"] [role="listbox"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 10px !important;
  box-shadow: 0 8px 32px rgba(0,0,0,.45) !important;
}
[data-baseweb="option"] {
  background: transparent !important;
  color: var(--text-secondary) !important;
  font-size: 13px !important;
}
[data-baseweb="option"]:hover, [data-baseweb="option"][aria-selected="true"] {
  background: rgba(99,102,241,.1) !important;
  color: var(--text-primary) !important;
}

/* ── Code blocks ── */
.stCodeBlock code, pre {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 8px !important;
  font-size: 12.5px !important;
  color: #c9cde0 !important;
}

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
  border-radius: 10px !important;
  overflow: hidden !important;
  border: 1px solid var(--border-subtle) !important;
}

/* ── Info / warning / success / error boxes — overridden by utility classes ── */

/* ── Column vertical spacing ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
  gap: 0 !important;
}

/* ── Tab panel content ── */
[data-testid="stTabsContent"] {
  padding-top: 1.2rem !important;
}

/* ── Agent card layout ── */
.agent-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px 28px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-card);
}
.agent-badge-pill {
  display: inline-block;
  background: rgba(99,102,241,0.15);
  color: #818cf8;
  border: 1px solid rgba(99,102,241,0.35);
  border-radius: 20px;
  padding: 3px 12px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.agent-status-pill {
  display: inline-block;
  border-radius: 20px;
  padding: 2px 10px;
  font-size: 11px;
  font-weight: 600;
  margin-right: 6px;
}
.agent-status-ready {
  background: rgba(34,211,165,0.12);
  color: #22d3a5;
  border: 1px solid rgba(34,211,165,0.3);
}
.agent-status-live {
  background: rgba(249,115,22,0.12);
  color: #f97316;
  border: 1px solid rgba(249,115,22,0.3);
}
.param-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-muted);
  margin-bottom: 6px;
}
.jur-pills-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}
.gen-btn-wrap {
  margin-top: 20px;
}
div[data-testid="stButton"].gen-btn > button {
  background: linear-gradient(135deg, #6366f1, #818cf8) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  padding: 14px 32px !important;
  min-height: 52px !important;
  width: 100% !important;
  letter-spacing: 0.3px !important;
}
div[data-testid="stButton"].gen-btn > button:hover {
  opacity: 0.9 !important;
}
div[data-testid="stButton"].back-btn > button {
  background: rgba(255,255,255,0.05) !important;
  color: var(--text-secondary) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 8px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
}

/* ── Page section header ── */
.page-section-header {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  margin: 28px 0 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-subtle);
}

/* ── Stat grid card ── */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}
.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 18px 20px;
  box-shadow: var(--shadow-card);
}
.stat-card-value {
  font-size: 26px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin-bottom: 4px;
}
.stat-card-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--text-muted);
}

/* ── Nav item improvements ── */
.nav-status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-left: auto;
  flex-shrink: 0;
}

/* ── Section divider ── */
.section-divider {
  border: none;
  border-top: 1px solid var(--border-subtle);
  margin: 24px 0;
}

/* ── Info banner ── */
.info-banner {
  background: rgba(99,102,241,0.06);
  border: 1px solid rgba(99,102,241,0.15);
  border-radius: var(--radius-sm);
  padding: 10px 16px;
  font-size: 12.5px;
  color: var(--text-secondary);
  margin-bottom: 16px;
  line-height: 1.6;
}

/* ── Radio button group ── */
div[data-testid="stRadio"] > div {
  gap: 8px !important;
  flex-wrap: wrap !important;
}
div[data-testid="stRadio"] label {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-medium) !important;
  border-radius: var(--radius-sm) !important;
  padding: 6px 16px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: var(--text-secondary) !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
  background: rgba(99,102,241,0.15) !important;
  border-color: rgba(99,102,241,0.4) !important;
  color: #a5b4fc !important;
}
div[data-testid="stRadio"] input[type="radio"] {
  display: none !important;
}

/* ── Alert boxes ── */
[data-testid="stAlert"] {
  border-radius: var(--radius-sm) !important;
  border-width: 1px !important;
  font-size: 13px !important;
  padding: 10px 16px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.18); }

/* ── Caption text ── */
[data-testid="stCaptionContainer"] p {
  font-size: 11.5px !important;
  color: var(--text-muted) !important;
  line-height: 1.6 !important;
}

/* ── Utility button active glow ─────────────────────────────── */
.util-voice-active button, .util-cowork-active button, .util-help-active button {
  background: rgba(99,102,241,0.18) !important;
  border: 1px solid rgba(99,102,241,0.5) !important;
  color: #818cf8 !important;
  box-shadow: 0 0 8px rgba(99,102,241,0.35) !important;
}

/* ── Demo Mode button ── */
.demo-btn button {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  color: #94a3b8 !important;
  border-radius: 8px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  width: 100% !important;
}
.demo-btn-active button {
  background: rgba(255,140,0,.15) !important;
  border: 1px solid rgba(255,140,0,.4) !important;
  color: #ffaa33 !important;
  border-radius: 8px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  width: 100% !important;
}

/* ── Demo stat cards ── */
@keyframes countup {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.demo-stat-card {
  animation: countup 0.6s ease forwards;
  background: rgba(99,102,241,.08);
  border: 1px solid rgba(99,102,241,.2);
  border-radius: 12px;
  padding: 16px 20px;
  text-align: center;
}
.demo-stat-number {
  font-size: 32px;
  font-weight: 800;
  color: #818cf8;
  font-family: 'Plus Jakarta Sans', sans-serif;
}
.demo-stat-label {
  font-size: 11px;
  color: #4a5568;
  text-transform: uppercase;
  letter-spacing: .08em;
  margin-top: 4px;
}
</style>
"""
