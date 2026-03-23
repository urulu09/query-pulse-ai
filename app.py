"""
╔══════════════════════════════════════════════════╗
║   TURKCELL SQL AI  —  app.py  v5                 ║
║   Container · Cards · Refined Header · Premium  ║
╚══════════════════════════════════════════════════╝
"""

import streamlit as st
import openai
import re
import time
import datetime

# ─────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Turkcell SQL AI",
    page_icon="🟡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────
# GLOBAL CSS  ·  V5  ·  Premium Turkcell
# ─────────────────────────────────────────────────
st.markdown("""
<style>
/* ══ Google Fonts ══ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Roboto+Mono:wght@400;500&display=swap');

/* ══ Design Tokens ══ */
:root {
    --tc-blue:         #0047BA;
    --tc-blue-dark:    #003090;
    --tc-blue-deeper:  #002D72;
    --tc-blue-mid:     #1565C0;
    --tc-blue-light:   #EBF2FC;
    --tc-yellow:       #FFD100;
    --tc-yellow-hover: #C9A800;
    --tc-navy:         #001A5E;
    --tc-text:         #111827;
    --tc-text-sub:     #374151;
    --tc-text-muted:   #6B7280;
    --tc-text-light:   #9CA3AF;
    --tc-border:       #D1DCF0;
    --tc-border-light: #E8EFF8;
    --tc-white:        #FFFFFF;
    --tc-success:      #059669;
    --tc-error:        #DC2626;
    --tc-warn:         #D97706;
    --tc-card-radius:  16px;
    --tc-radius:       8px;
    --tc-card-shadow:  0 4px 20px rgba(0, 0, 0, 0.05);
    --tc-shadow:       0 2px 12px rgba(0, 71, 186, 0.09);
    --tc-shadow-lg:    0 8px 32px rgba(0, 71, 186, 0.11);
    --sans:            'Inter', system-ui, -apple-system, sans-serif;
    --mono:            'Roboto Mono', monospace;
}

/* ══════════════════════════════════════
   GRADIENT ANA ARKA PLAN (yumuşatıldı)
══════════════════════════════════════ */
html, body {
    background: linear-gradient(175deg,
        #FFFFFF    0%,
        #F5FAFE   30%,
        #EBF4FF   65%,
        #F0F8FF  100%) !important;
    min-height: 100vh;
}
[class*="css"], .stApp, .stApp > div:first-child,
section[data-testid="stSidebarContent"] { background: transparent !important; }
.stApp { font-family: var(--sans) !important; color: var(--tc-text) !important; }

/* ══ Hide Streamlit chrome ══ */
#MainMenu, footer, header { visibility: hidden; }

/* ══════════════════════════════════════
   CONTAINER — 800px sabit, ortalı
══════════════════════════════════════ */
.block-container {
    background: transparent !important;
    max-width: 800px !important;
    padding: 0 1.5rem 5rem !important;
    margin: 0 auto !important;
}

/* ══ Scrollbar ══ */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--tc-blue); border-radius: 3px; }

/* ══════════════════════════════════════
   HEADER — İnce, Zarif Mavi Şerit
══════════════════════════════════════ */
.tc-header {
    background: linear-gradient(92deg,
        #002D72  0%,
        #0047BA 55%,
        #1460CC 100%);
    margin: -1rem -1.5rem 0;
    padding: 0 2rem;
    height: 56px;              /* daha ince: 68px → 56px */
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 12px rgba(0, 40, 120, 0.28);
    position: relative;
    overflow: hidden;
}
.tc-header::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg,
        transparent 60%,
        rgba(255,255,255,0.04) 100%);
    pointer-events: none;
}
/* Logo + Marka */
.tc-logo-wrap {
    display: flex;
    align-items: center;
    gap: 11px;
    z-index: 1;
}
.tc-logo-badge {
    width: 32px; height: 32px;        /* küçüldü */
    background: var(--tc-yellow);
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--sans);
    font-size: 1.05rem;
    font-weight: 900;
    color: #002D72;
    box-shadow: 0 2px 8px rgba(255,209,0,0.40);
    flex-shrink: 0;
    line-height: 1;
    user-select: none;
    letter-spacing: -1px;
}
.tc-brand-name {
    font-family: var(--sans);
    font-size: 1.02rem;               /* biraz küçüldü */
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.1px;
    line-height: 1.2;
}
.tc-brand-tagline {
    font-family: var(--sans);
    font-size: 0.58rem;
    font-weight: 400;
    color: rgba(255,255,255,0.48);
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-top: 1px;
}
.tc-header-pill {
    z-index: 1;
    background: rgba(255,255,255,0.11);
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 20px;
    padding: 4px 14px;
    font-family: var(--sans);
    font-size: 0.60rem;
    font-weight: 600;
    color: rgba(255,255,255,0.75);
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ══════════════════════════════════════
   SIDEBAR — Derin Lacivert, Premium
══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background-color: #002D72 !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(0, 20, 80, 0.18);
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 1.1rem 2rem !important;
}
.sb-inner-top {
    background: rgba(0, 0, 0, 0.20);
    margin: 0 -1.1rem 1.5rem;
    padding: 0.9rem 1.1rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    display: flex;
    align-items: center;
    gap: 8px;
}
.sb-inner-top-icon { font-size: 0.95rem; opacity: 0.85; }
.sb-inner-top-title {
    font-family: var(--sans);
    font-size: 0.72rem;               /* küçüldü */
    font-weight: 700;
    color: rgba(255,255,255,0.88);
    letter-spacing: 2px;              /* daha geniş */
    text-transform: uppercase;        /* uppercase */
}
/* Sidebar section labels */
.sb-label {
    font-family: var(--sans);
    font-size: 0.58rem;               /* küçüldü */
    font-weight: 700;
    color: rgba(255,255,255,0.42);
    letter-spacing: 2.5px;            /* premium spacing */
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.sb-label::before {
    content: '';
    display: inline-block;
    width: 3px; height: 10px;
    background: var(--tc-yellow);
    border-radius: 2px;
    flex-shrink: 0;
}
/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1.5px dashed rgba(255,255,255,0.18) !important;
    border-radius: var(--tc-radius) !important;
    transition: border-color .2s, background .2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--tc-yellow) !important;
    background: rgba(255,209,0,0.04) !important;
}
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: rgba(255,255,255,0.38) !important;
    font-family: var(--sans) !important;
    font-size: 0.68rem !important;
}
[data-testid="stFileUploaderDropzone"] small {
    color: rgba(255,255,255,0.25) !important;
    font-family: var(--sans) !important;
    font-size: 0.58rem !important;
}
/* Schema card inside dark sidebar */
.schema-card {
    background: rgba(0,0,0,0.24);
    border: 1px solid rgba(255,255,255,0.09);
    border-left: 3px solid var(--tc-yellow);
    border-radius: var(--tc-radius);
    padding: 0.8rem 0.9rem;
    margin-top: 0.65rem;
    max-height: 250px;
    overflow-y: auto;
}
.schema-card pre {
    font-family: var(--mono) !important;
    font-size: 0.63rem !important;
    line-height: 1.72 !important;
    color: rgba(255,255,255,0.68) !important;
    margin: 0 !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
}
.schema-status {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 0.65rem;
    font-family: var(--sans);
    font-size: 0.62rem;
    font-weight: 600;
    color: #34D399;
    letter-spacing: 0.3px;
}
.schema-status .dot-green {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #34D399;
    flex-shrink: 0;
}
.schema-inactive {
    font-family: var(--sans);
    font-size: 0.68rem;
    color: rgba(255,255,255,0.32);
    line-height: 1.8;
    padding: 0.25rem 0;
}
.sb-divider {
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 1rem 0;
}
.sb-tip {
    font-family: var(--mono);
    font-size: 0.58rem;
    color: rgba(255,255,255,0.36);
    line-height: 1.85;
    padding: 0.65rem 0.8rem;
    background: rgba(0,0,0,0.18);
    border-radius: var(--tc-radius);
    border-left: 2px solid rgba(255,209,0,0.5);
}
.sb-tip code  { color: var(--tc-yellow); font-family: var(--mono); }
.sb-tip strong { color: rgba(255,255,255,0.55); }

/* ══════════════════════════════════════
   ANA ALAN SECTION LABELS
══════════════════════════════════════ */
.tc-label {
    font-family: var(--sans) !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    color: var(--tc-blue-dark) !important;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 0.6rem !important;
    display: flex;
    align-items: center;
    gap: 8px;
}
.tc-label::before {
    content: '';
    display: inline-block;
    width: 3px; height: 14px;
    background: var(--tc-yellow);
    border-radius: 2px;
    flex-shrink: 0;
}

/* ══════════════════════════════════════
   CARD WRAPPER  (Yapılandırma + Prompt)
══════════════════════════════════════ */
.tc-card {
    background: var(--tc-white);
    border: 1px solid var(--tc-border-light);
    border-radius: var(--tc-card-radius);
    padding: 1.5rem 1.6rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: var(--tc-card-shadow);
}
/* Config card alt bölücü */
.tc-card-divider {
    height: 1px;
    background: var(--tc-border-light);
    margin: 1.2rem -1.6rem;
}

/* ══════════════════════════════════════
   DIVIDER (sayfalar arası)
══════════════════════════════════════ */
.tc-divider {
    height: 1px;
    background: var(--tc-border);
    margin: 1.4rem 0;
    opacity: 0.5;
}

/* ══════════════════════════════════════
   SCHEMA MODE BADGE
══════════════════════════════════════ */
.schema-mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(5,150,105,0.08);
    border: 1px solid rgba(5,150,105,0.25);
    border-radius: 20px;
    padding: 4px 13px;
    font-family: var(--sans);
    font-size: 0.63rem;
    font-weight: 600;
    color: var(--tc-success);
    letter-spacing: 0.3px;
    margin-bottom: 0.75rem;
}
.schema-mode-badge .dot-g {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--tc-success);
}

/* ══════════════════════════════════════
   SELECTS
══════════════════════════════════════ */
.stSelectbox > div > div {
    background-color: #FAFBFD !important;
    border: 1.5px solid var(--tc-border) !important;
    border-radius: var(--tc-radius) !important;
    color: var(--tc-text) !important;
    font-family: var(--sans) !important;
    font-size: 0.84rem !important;
    transition: border-color .2s !important;
}
.stSelectbox > div > div:hover,
.stSelectbox > div > div:focus-within {
    border-color: var(--tc-blue) !important;
    background-color: #FFFFFF !important;
}
.stSelectbox label {
    font-family: var(--sans) !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    color: var(--tc-text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
div[data-baseweb="select"] * { background-color: #FFFFFF !important; }
div[data-baseweb="popover"] * {
    background-color: #FFFFFF !important;
    border-color: var(--tc-border) !important;
    color: var(--tc-text) !important;
}

/* ══════════════════════════════════════
   TEXT AREA
══════════════════════════════════════ */
.stTextArea textarea {
    background-color: #FAFBFD !important;
    border: 1.5px solid var(--tc-border) !important;
    border-radius: var(--tc-radius) !important;
    color: var(--tc-text) !important;
    font-family: var(--sans) !important;
    font-size: 0.88rem !important;
    line-height: 1.6 !important;
    padding: 12px 14px !important;
    resize: vertical !important;
    transition: border-color .2s, box-shadow .2s !important;
}
.stTextArea textarea:focus {
    border-color: var(--tc-blue) !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 0 0 3px rgba(0,71,186,0.10) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: var(--tc-text-light) !important; }
.stTextArea label { display: none !important; }

/* ══════════════════════════════════════
   GENERATE BUTTON — Kompakt, Sarı, Bold
══════════════════════════════════════ */
.stButton > button {
    width: 100% !important;
    background: var(--tc-yellow) !important;
    color: var(--tc-blue) !important;          /* lacivert yazı */
    font-family: var(--sans) !important;
    font-weight: 700 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.2px;
    border: none !important;
    border-radius: var(--tc-card-radius) !important; /* kart köşeleriyle uyumlu: 16px */
    padding: 0.68rem 2rem !important;
    cursor: pointer !important;
    transition: background .18s, box-shadow .18s, transform .10s !important;
    box-shadow: 0 3px 12px rgba(255,209,0,0.28) !important;
    margin-top: 0.1rem !important;
}
.stButton > button:hover {
    background: var(--tc-yellow-hover) !important;
    box-shadow: 0 5px 20px rgba(200,168,0,0.35) !important;
    transform: translateY(-1px) !important;
    color: var(--tc-navy) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 1px 6px rgba(200,168,0,0.22) !important;
}

/* ══════════════════════════════════════
   SQL SONUÇ KARTI
══════════════════════════════════════ */
.sql-card {
    background: var(--tc-white);
    border: 1px solid var(--tc-border-light);
    border-top: 3px solid var(--tc-blue);
    border-radius: var(--tc-card-radius);
    padding: 1.4rem 1.6rem;
    margin-top: 0.5rem;
    box-shadow: var(--tc-card-shadow);
}
.sql-card pre {
    font-family: var(--mono) !important;
    font-size: 0.80rem !important;
    line-height: 1.78 !important;
    color: var(--tc-text) !important;
    margin: 0 !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
}
/* SQL syntax highlight */
.kw  { color: #0047BA; font-weight: 700; }
.fn  { color: #047857; }
.str { color: #B91C1C; }
.cmt { color: #9CA3AF; font-style: italic; }
.num { color: #7C3AED; }

.sql-status-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 1rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--tc-border-light);
}
.sql-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: var(--tc-blue-light);
    border-radius: 20px;
    padding: 3px 10px;
    font-family: var(--sans);
    font-size: 0.62rem;
    font-weight: 600;
    color: var(--tc-blue-dark);
    letter-spacing: 0.2px;
}
.sql-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--tc-success);
}

/* ══════════════════════════════════════
   STATS ROW
══════════════════════════════════════ */
.stats-row { display: flex; gap: 0.75rem; margin-top: 0.85rem; }
.stat-chip {
    flex: 1;
    background: var(--tc-white);
    border: 1px solid var(--tc-border-light);
    border-radius: var(--tc-radius);
    padding: 0.85rem 0.75rem;
    text-align: center;
    box-shadow: 0 1px 6px rgba(0,71,186,0.05);
    transition: box-shadow .2s, transform .15s;
}
.stat-chip:hover { box-shadow: var(--tc-shadow); transform: translateY(-1px); }
.stat-chip .val {
    font-family: var(--sans);
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--tc-blue);
}
.stat-chip .lbl {
    font-size: 0.59rem;
    font-weight: 700;
    color: var(--tc-text-muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ══════════════════════════════════════
   ALERTS
══════════════════════════════════════ */
.qp-alert {
    border-radius: var(--tc-radius);
    padding: 0.82rem 1.1rem;
    font-size: 0.81rem;
    font-family: var(--sans);
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-top: 0.6rem;
}
.qp-alert-error {
    background: #FEF2F2;
    border: 1px solid #FECACA;
    border-left: 4px solid var(--tc-error);
    color: var(--tc-error);
}
.qp-alert-warn {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-left: 4px solid var(--tc-warn);
    color: var(--tc-warn);
}
.qp-alert-info {
    background: var(--tc-blue-light);
    border: 1px solid var(--tc-border);
    border-left: 4px solid var(--tc-blue);
    color: var(--tc-blue);
}
.qp-alert-missing-key {
    background: #F5F3FF;
    border: 1px solid #DDD6FE;
    border-left: 4px solid #7C3AED;
    color: #4C1D95;
    border-radius: var(--tc-radius);
    padding: 1.2rem 1.4rem;
    font-size: 0.83rem;
    display: flex;
    align-items: flex-start;
    gap: 13px;
    margin-top: 1.5rem;
    font-family: var(--sans);
    line-height: 1.7;
}
.qp-alert-missing-key strong { color: #3B0764; }
.qp-alert-missing-key code {
    background: #EDE9FE; padding: 1px 6px; border-radius: 4px;
    font-family: var(--mono); font-size: 0.75rem; color: #7C3AED;
}
.qp-alert-missing-key pre {
    background: #F5F3FF; border: 1px solid #DDD6FE; border-radius: 6px;
    padding: 7px 12px; font-family: var(--mono); font-size: 0.75rem;
    color: #5B21B6; margin: 0.4rem 0 0.2rem;
}
.qp-alert-icon { font-size: 1rem; flex-shrink: 0; }

/* ══════════════════════════════════════
   EXPANDER
══════════════════════════════════════ */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.80) !important;
    border: 1px solid var(--tc-border-light) !important;
    border-radius: var(--tc-radius) !important;
    color: var(--tc-text-muted) !important;
    font-family: var(--sans) !important;
    font-size: 0.76rem !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid var(--tc-border-light) !important;
    border-top: none !important;
}

/* ══════════════════════════════════════
   HISTORY ITEM
══════════════════════════════════════ */
.history-item {
    background: var(--tc-white);
    border: 1px solid var(--tc-border-light);
    border-left: 3px solid var(--tc-yellow);
    border-radius: var(--tc-radius);
    padding: 0.72rem 1rem;
    margin-bottom: 0.45rem;
    box-shadow: 0 1px 4px rgba(0,71,186,0.04);
}
.history-item .hi-prompt {
    color: var(--tc-text);
    font-family: var(--sans);
    font-size: 0.81rem;
    font-weight: 500;
    margin-bottom: 3px;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.history-item .hi-meta {
    color: var(--tc-text-light);
    font-size: 0.62rem;
    font-family: var(--sans);
}

/* ══════════════════════════════════════
   CODE BLOCK
══════════════════════════════════════ */
.stCodeBlock { border: 1px solid var(--tc-border-light) !important; border-radius: var(--tc-radius) !important; }
.stCodeBlock pre { background: #F8FAFC !important; font-family: var(--mono) !important; font-size: 0.79rem !important; }
div[data-testid="stCopyButton"] button {
    background: var(--tc-blue-light) !important;
    border: 1px solid var(--tc-border) !important;
    color: var(--tc-blue) !important;
    border-radius: 6px !important;
    font-size: 0.67rem !important;
}
div[data-testid="stCopyButton"] button:hover {
    background: var(--tc-blue) !important;
    color: #FFFFFF !important;
}

/* ══════════════════════════════════════
   SPINNER
══════════════════════════════════════ */
.stSpinner > div { border-top-color: var(--tc-blue) !important; }

/* ══════════════════════════════════════
   FOOTER
══════════════════════════════════════ */
.tc-footer {
    text-align: center;
    margin-top: 3.5rem;
    padding-top: 1.2rem;
    border-top: 1px solid var(--tc-border-light);
}
.tc-footer span {
    font-family: var(--sans);
    font-size: 0.62rem;
    color: var(--tc-text-light);
    letter-spacing: 0.5px;
}
.tc-footer strong { color: var(--tc-blue); font-weight: 700; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for k, v in [("history", []), ("query_count", 0), ("total_tokens", 0), ("last_prompt", "")]:
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
SQL_KEYWORDS = [
    "SELECT", "FROM", "WHERE", "JOIN", "LEFT JOIN", "RIGHT JOIN",
    "INNER JOIN", "FULL OUTER JOIN", "ON", "GROUP BY", "ORDER BY",
    "HAVING", "LIMIT", "OFFSET", "INSERT INTO", "VALUES", "UPDATE",
    "SET", "DELETE", "CREATE TABLE", "ALTER TABLE", "DROP TABLE",
    "WITH", "AS", "AND", "OR", "NOT", "IN", "BETWEEN", "LIKE",
    "IS NULL", "IS NOT NULL", "DISTINCT", "UNION", "UNION ALL",
    "INTERSECT", "EXCEPT", "CASE", "WHEN", "THEN", "ELSE", "END",
    "ASC", "DESC", "COALESCE", "NULLIF", "CAST", "OVER", "PARTITION BY",
    "ROW_NUMBER", "RANK", "DENSE_RANK", "LAG", "LEAD",
]

def highlight_sql(sql: str) -> str:
    for kw in sorted(SQL_KEYWORDS, key=len, reverse=True):
        sql = re.compile(rf'\b({re.escape(kw)})\b', re.IGNORECASE).sub(
            r'<span class="kw">\1</span>', sql)
    return sql

def parse_schema_file(f) -> tuple[str, int, int]:
    raw = f.read().decode("utf-8", errors="replace")
    return raw, len(raw), len(re.findall(r'\bCREATE\s+TABLE\b', raw, re.IGNORECASE))

def build_system_prompt(dialect: str, style: str) -> str:
    style_map = {
        "Standard":  "Use standard, clean SQL formatting with uppercase keywords.",
        "Compact":   "Return compact SQL without extra newlines.",
        "Annotated": "Add brief SQL comments above each major clause.",
    }
    return f"""You are Turkcell SQL AI, an expert SQL engineer specialising in {dialect}.
RULES:
1. Output ONLY valid {dialect} SQL — no markdown fences, no explanation.
2. {style_map.get(style, '')}
3. Use meaningful aliases. Prefer CTEs for complex queries.
4. Handle NULLs safely. Use window functions where appropriate.
5. Always end with a semicolon.
6. If the request cannot become SQL: ERROR: Not a valid SQL request.
Dialect notes — PostgreSQL: ILIKE, EXTRACT(); MySQL: DATE_FORMAT(), IFNULL();
SQLite: strftime(); T-SQL: TOP, GETDATE(), [brackets]; BigQuery: backticks, SAFE_DIVIDE();
Snowflake: QUALIFY, IFF(), FLATTEN."""

def build_user_message(prompt: str, schema_text: str | None) -> str:
    if not schema_text:
        return prompt.strip()
    return f"""=== DATABASE SCHEMA ===
Use ONLY these table/column names. Do NOT invent any.

{schema_text.strip()}

=== END SCHEMA ===

REQUEST: {prompt.strip()}"""

def generate_sql(prompt, api_key, dialect, style, model, schema_text=None):
    client = openai.OpenAI(api_key=api_key)
    t0 = time.time()
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": build_system_prompt(dialect, style)},
            {"role": "user",   "content": build_user_message(prompt, schema_text)},
        ],
        temperature=0.2, max_tokens=1400,
    )
    return {
        "sql":     resp.choices[0].message.content.strip(),
        "tokens":  resp.usage.total_tokens,
        "elapsed": round(time.time() - t0, 2),
    }

def validate(sql):
    if sql.startswith("ERROR:"):
        return False, sql.replace("ERROR:", "").strip()
    if len(sql) < 10:
        return False, "Model çok kısa bir yanıt döndürdü."
    return True, ""


# ═════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-inner-top">
        <span class="sb-inner-top-icon">🗄️</span>
        <span class="sb-inner-top-title">Şema Bağlamı</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sb-label">📂 Şema Dosyası Yükle</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "schema", type=["sql", "txt"],
        accept_multiple_files=False,
        label_visibility="collapsed",
    )

    schema_text: str | None = None
    schema_meta: dict = {}

    if uploaded_file:
        try:
            raw, char_count, table_count = parse_schema_file(uploaded_file)
            if char_count > 80_000:
                st.markdown("""<div class="qp-alert qp-alert-warn" style="font-size:.67rem;padding:.55rem .8rem;">
                <span>⚠</span><span>Dosya 80 KB limitini aşıyor.</span></div>""", unsafe_allow_html=True)
            else:
                schema_text = raw
                schema_meta = {"name": uploaded_file.name, "tables": table_count, "chars": char_count}
                preview = raw[:750] + ("\n…" if len(raw) > 750 else "")
                st.markdown(f"""<div class="schema-card"><pre>{preview}</pre></div>
                <div class="schema-status"><span class="dot-green"></span>
                {table_count} tablo · {char_count:,} karakter</div>""", unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""<div class="qp-alert qp-alert-error" style="font-size:.67rem;padding:.55rem .8rem;">
            <span>✖</span><span>{e}</span></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<p class="schema-inactive">Şema yüklenmedi.<br>
        AI genel bilgisiyle<br>tablo yapılarını tahmin eder.</p>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown("""<div class="sb-tip">💡 <strong>İpucu:</strong><br>
    <code>pg_dump --schema-only</code> (PostgreSQL)<br>
    <code>SHOW CREATE TABLE</code> (MySQL)</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# API KEY
# ─────────────────────────────────────────────
resolved_api_key = st.secrets.get("OPENAI_API_KEY", "")
if not resolved_api_key:
    st.markdown("""<div class="qp-alert qp-alert-missing-key">
    <span class="qp-alert-icon">🔐</span>
    <div><strong>API anahtarı bulunamadı.</strong><br>
    <span style="font-size:.77rem;opacity:.85;">
    <code>.streamlit/secrets.toml</code> dosyasına şu satırı ekleyin:</span>
    <pre>OPENAI_API_KEY = "sk-..."</pre>
    <span style="font-size:.70rem;opacity:.60;">
    Streamlit Cloud → App Settings › Secrets bölümüne de ekleyebilirsiniz.</span>
    </div></div>""", unsafe_allow_html=True)
    st.stop()


# ═════════════════════════════════════════════════
# HEADER
# ═════════════════════════════════════════════════
st.markdown("""
<div class="tc-header">
    <div class="tc-logo-wrap">
        <div class="tc-logo-badge">T</div>
        <div>
            <div class="tc-brand-name">Turkcell SQL AI</div>
            <div class="tc-brand-tagline">Natural Language → SQL</div>
        </div>
    </div>
    <div class="tc-header-pill">OpenAI Destekli</div>
</div>
<div style="height:1.8rem"></div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════
# CARD 1 — Yapılandırma
# ═════════════════════════════════════════════════
st.markdown('<div class="tc-card">', unsafe_allow_html=True)
st.markdown('<p class="tc-label">⚙ Yapılandırma</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([2, 2, 2])
with c1:
    dialect = st.selectbox("Dialect",
        ["PostgreSQL", "MySQL", "SQLite", "SQL Server (T-SQL)", "BigQuery", "Snowflake"],
        key="dialect_select")
with c2:
    style = st.selectbox("Stil",
        ["Standard", "Annotated", "Compact"], key="style_select")
with c3:
    model = st.selectbox("Model",
        ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"], key="model_select")

st.markdown('</div>', unsafe_allow_html=True)  # /card1


# ═════════════════════════════════════════════════
# QUICK EXAMPLES
# ═════════════════════════════════════════════════
EXAMPLES = [
    ("📦", "Top 10 customers by total revenue in 2024"),
    ("📊", "Monthly active users grouped by country, last 6 months"),
    ("🔍", "Orders delivered more than 3 days late"),
    ("🔗", "Products never purchased, joined with category names"),
    ("📈", "Running total of sales per day using a window function"),
    ("⚠️", "Duplicate email addresses in the users table"),
]
with st.expander("✦  Hızlı Örnekler — tıklayarak yükle", expanded=False):
    cols = st.columns(2)
    for i, (icon, text) in enumerate(EXAMPLES):
        with cols[i % 2]:
            if st.button(f"{icon}  {text}", key=f"ex_{i}", use_container_width=True):
                st.session_state.last_prompt = text
                st.rerun()


# ═════════════════════════════════════════════════
# CARD 2 — Prompt + Buton
# ═════════════════════════════════════════════════
st.markdown('<div class="tc-card">', unsafe_allow_html=True)

if schema_text:
    st.markdown(f"""<div class="schema-mode-badge">
    <span class="dot-g"></span>
    Şema Modu Aktif &nbsp;·&nbsp; {schema_meta['name']} &nbsp;·&nbsp; {schema_meta['tables']} tablo
    </div>""", unsafe_allow_html=True)

st.markdown('<p class="tc-label">✦ Doğal Dil ile Açıkla</p>', unsafe_allow_html=True)

prompt = st.text_area(
    "prompt",
    value=st.session_state.last_prompt,
    height=115,
    placeholder=(
        "Örn. → Geçen ay kaydolan ancak henüz sipariş vermemiş kullanıcıları,\n"
        "       referans kaynağına göre gruplandırarak kayıt tarihine göre sırala…"
    ),
    key="prompt_input",
)

generate_clicked = st.button("⚡  SQL Oluştur", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)  # /card2


# ─────────────────────────────────────────────
# GENERATE LOGIC
# ─────────────────────────────────────────────
if generate_clicked:
    if not prompt.strip():
        st.markdown("""<div class="qp-alert qp-alert-warn">
        <span class="qp-alert-icon">⚠</span>
        <span>Lütfen oluşturmadan önce bir açıklama girin.</span></div>""",
        unsafe_allow_html=True); st.stop()

    with st.spinner("Şemaya özel SQL oluşturuluyor…" if schema_text else "SQL oluşturuluyor…"):
        try:
            result = generate_sql(prompt, resolved_api_key, dialect, style, model, schema_text)
        except openai.AuthenticationError:
            st.markdown("""<div class="qp-alert qp-alert-error"><span class="qp-alert-icon">✖</span>
            <span><strong>Kimlik doğrulama hatası.</strong> API anahtarınız geçersiz.</span></div>""",
            unsafe_allow_html=True); st.stop()
        except openai.RateLimitError:
            st.markdown("""<div class="qp-alert qp-alert-error"><span class="qp-alert-icon">✖</span>
            <span><strong>İstek limiti aşıldı.</strong> Kısa süre sonra tekrar deneyin.</span></div>""",
            unsafe_allow_html=True); st.stop()
        except openai.APIConnectionError:
            st.markdown("""<div class="qp-alert qp-alert-error"><span class="qp-alert-icon">✖</span>
            <span><strong>Bağlantı hatası.</strong> OpenAI API'ye ulaşılamadı.</span></div>""",
            unsafe_allow_html=True); st.stop()
        except Exception as e:
            st.markdown(f"""<div class="qp-alert qp-alert-error"><span class="qp-alert-icon">✖</span>
            <span><strong>Hata:</strong> {str(e)}</span></div>""",
            unsafe_allow_html=True); st.stop()

    ok, err_msg = validate(result["sql"])
    if not ok:
        st.markdown(f"""<div class="qp-alert qp-alert-warn"><span class="qp-alert-icon">⚠</span>
        <span><strong>Model Bildirimi:</strong> {err_msg}</span></div>""",
        unsafe_allow_html=True); st.stop()

    # Store
    st.session_state.query_count  += 1
    st.session_state.total_tokens += result["tokens"]
    st.session_state.history.insert(0, {
        "prompt":      prompt, "sql": result["sql"], "dialect": dialect,
        "ts":          datetime.datetime.now().strftime("%H:%M:%S"),
        "tokens":      result["tokens"],
        "schema_name": schema_meta.get("name", "—") if schema_text else "—",
    })
    st.session_state.history = st.session_state.history[:20]

    # Output card
    st.markdown('<div style="height:.6rem"></div>', unsafe_allow_html=True)
    st.markdown('<p class="tc-label">✦ Oluşturulan SQL</p>', unsafe_allow_html=True)

    schema_badge_html = (
        f'<span class="sql-badge" style="background:#D1FAE5;color:#065F46;">'
        f'<span class="dot" style="background:#059669"></span>{schema_meta["name"]}</span>'
        if schema_text else ""
    )
    st.markdown(f"""
    <div class="sql-card">
        <pre>{highlight_sql(result["sql"])}</pre>
        <div class="sql-status-bar">
            <span class="sql-badge"><span class="dot"></span>{dialect}</span>
            <div style="display:flex;gap:.5rem;align-items:center;">
                {schema_badge_html}
                <span class="sql-badge">{result['elapsed']}s · {result['tokens']} token</span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.code(result["sql"], language="sql")

    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-chip"><div class="val">{st.session_state.query_count}</div><div class="lbl">Toplam Sorgu</div></div>
        <div class="stat-chip"><div class="val">{result['elapsed']}s</div><div class="lbl">Yanıt Süresi</div></div>
        <div class="stat-chip"><div class="val">{st.session_state.total_tokens}</div><div class="lbl">Token Kullanımı</div></div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HISTORY
# ─────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="tc-divider"></div>', unsafe_allow_html=True)
    with st.expander(f"🕑  Sorgu Geçmişi  ({len(st.session_state.history)} kayıt)", expanded=False):
        for entry in st.session_state.history:
            tag = f" · 🗄 {entry['schema_name']}" if entry.get("schema_name") and entry["schema_name"] != "—" else ""
            st.markdown(f"""<div class="history-item">
            <div class="hi-prompt">{entry['prompt']}</div>
            <div class="hi-meta">{entry['ts']} · {entry['dialect']}{tag} · {entry['tokens']} token</div>
            </div>""", unsafe_allow_html=True)
            st.code(entry["sql"], language="sql")
        if st.button("🗑  Geçmişi Temizle", key="clear_history"):
            st.session_state.update({"history": [], "query_count": 0, "total_tokens": 0})
            st.rerun()


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="tc-footer">
    <span><strong>Turkcell SQL AI</strong> &nbsp;·&nbsp; OpenAI ile güçlendirilmiştir &nbsp;·&nbsp; Streamlit üzerinde çalışır</span>
</div>""", unsafe_allow_html=True)