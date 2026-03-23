"""
╔══════════════════════════════════════════════════╗
║   TURKCELL SQL AI  —  app.py  v4                 ║
║   Rebranded · Gradient BG · Dark Sidebar         ║
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
# GLOBAL CSS  ·  V4  ·  Turkcell SQL AI
# ─────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Roboto+Mono:wght@400;500&display=swap');

/* ── Turkcell Token Sistemi ── */
:root {
    --tc-blue:         #0047BA;
    --tc-blue-dark:    #003090;
    --tc-blue-deeper:  #002D72;
    --tc-blue-mid:     #1565C0;
    --tc-blue-light:   #E8F0FB;
    --tc-yellow:       #FFD100;
    --tc-yellow-hover: #C9A800;
    --tc-navy:         #001A5E;
    --tc-text:         #12213A;
    --tc-text-muted:   #526080;
    --tc-text-light:   #8898AA;
    --tc-border:       #C8D8EE;
    --tc-border-light: #E4EDF8;
    --tc-white:        #FFFFFF;
    --tc-success:      #00A651;
    --tc-error:        #C62828;
    --tc-warn:         #E65100;
    --tc-radius:       8px;
    --tc-radius-lg:    14px;
    --tc-shadow:       0 2px 14px rgba(0,71,186,0.10);
    --tc-shadow-lg:    0 6px 32px rgba(0,71,186,0.13);
    --sans:            'Inter', system-ui, sans-serif;
    --mono:            'Roboto Mono', monospace;
}

/* ══════════════════════════════════════════════
   GRADIENT ANA ARKA PLAN
══════════════════════════════════════════════ */
html, body {
    background: linear-gradient(160deg, #FFFFFF 0%, #D6ECFF 55%, #B8DEFF 100%) !important;
    min-height: 100vh;
}
[class*="css"], .stApp {
    background: transparent !important;
    font-family: var(--sans) !important;
    color: var(--tc-text) !important;
    font-size: 14px;
}
/* Streamlit's main wrapper — keep transparent */
.stApp > div:first-child { background: transparent !important; }
.block-container {
    background: transparent !important;
    padding: 0 2rem 5rem !important;
    max-width: 880px !important;
}

/* ── Hide chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--tc-blue); border-radius: 3px; }

/* ══════════════════════════════════════════════
   HEADER  —  Koyu Mavi Şerit + Turkcell Logo
══════════════════════════════════════════════ */
.tc-header {
    background: linear-gradient(90deg, var(--tc-blue-dark) 0%, var(--tc-blue) 70%, #1A6DD4 100%);
    margin: -1rem -2rem 0;
    padding: 0 2.2rem;
    height: 68px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 3px 16px rgba(0,48,144,0.30);
    position: relative;
    overflow: hidden;
}
/* Subtle diagonal light sweep */
.tc-header::before {
    content: '';
    position: absolute;
    top: -40px; right: 80px;
    width: 220px; height: 160px;
    background: radial-gradient(ellipse, rgba(255,255,255,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.tc-logo-wrap {
    display: flex;
    align-items: center;
    gap: 14px;
}
/* Turkcell logo placeholder — sarı T harfi badge */
.tc-logo-badge {
    width: 40px; height: 40px;
    background: var(--tc-yellow);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--sans);
    font-size: 1.35rem;
    font-weight: 900;
    color: var(--tc-blue-dark);
    letter-spacing: -1px;
    box-shadow: 0 2px 10px rgba(255,209,0,0.45);
    flex-shrink: 0;
    line-height: 1;
    user-select: none;
}
.tc-brand-text {}
.tc-brand-name {
    font-family: var(--sans);
    font-size: 1.18rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.2px;
    line-height: 1.15;
}
.tc-brand-tagline {
    font-family: var(--mono);
    font-size: 0.60rem;
    color: rgba(255,255,255,0.52);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 1px;
}
.tc-header-pill {
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 20px;
    padding: 5px 16px;
    font-family: var(--sans);
    font-size: 0.62rem;
    font-weight: 600;
    color: rgba(255,255,255,0.80);
    letter-spacing: 1.2px;
    text-transform: uppercase;
}

/* ══════════════════════════════════════════════
   SIDEBAR  —  Koyu Lacivert / Dark Navy
══════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background-color: var(--tc-blue-deeper) !important;
    border-right: none !important;
    box-shadow: 3px 0 20px rgba(0,20,60,0.20);
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 1.2rem 2rem !important;
}
/* Sidebar inner top banner */
.sb-inner-top {
    background: rgba(0,0,0,0.18);
    margin: 0 -1.2rem 1.4rem;
    padding: 1rem 1.2rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    display: flex;
    align-items: center;
    gap: 9px;
}
.sb-inner-top-icon {
    font-size: 1.05rem;
    opacity: 0.9;
}
.sb-inner-top-title {
    font-family: var(--sans);
    font-size: 0.82rem;
    font-weight: 700;
    color: rgba(255,255,255,0.92);
    letter-spacing: 0.2px;
}
/* Sidebar labels */
.sb-label {
    font-family: var(--sans);
    font-size: 0.63rem;
    font-weight: 600;
    color: rgba(255,255,255,0.55);
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 0.55rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.sb-label::before {
    content: '';
    display: inline-block;
    width: 3px; height: 12px;
    background: var(--tc-yellow);
    border-radius: 2px;
}
/* File uploader on dark sidebar */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1.5px dashed rgba(255,255,255,0.20) !important;
    border-radius: var(--tc-radius) !important;
    transition: border-color .2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--tc-yellow) !important;
}
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: rgba(255,255,255,0.45) !important;
    font-family: var(--sans) !important;
    font-size: 0.70rem !important;
}
[data-testid="stFileUploaderDropzone"] small {
    color: rgba(255,255,255,0.30) !important;
    font-family: var(--sans) !important;
    font-size: 0.60rem !important;
}
/* Schema preview card inside dark sidebar */
.schema-card {
    background: rgba(0,0,0,0.22);
    border: 1px solid rgba(255,255,255,0.10);
    border-left: 3px solid var(--tc-yellow);
    border-radius: var(--tc-radius);
    padding: 0.85rem 1rem;
    margin-top: 0.7rem;
    max-height: 260px;
    overflow-y: auto;
}
.schema-card pre {
    font-family: var(--mono) !important;
    font-size: 0.64rem !important;
    line-height: 1.7 !important;
    color: rgba(255,255,255,0.72) !important;
    margin: 0 !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
}
.schema-status {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 0.7rem;
    font-family: var(--sans);
    font-size: 0.63rem;
    font-weight: 600;
    color: #4ADE80;
    letter-spacing: 0.3px;
}
.schema-status .dot-green {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4ADE80;
    flex-shrink: 0;
}
.schema-inactive {
    font-family: var(--sans);
    font-size: 0.70rem;
    color: rgba(255,255,255,0.38);
    line-height: 1.75;
    padding: 0.3rem 0;
}
.sb-divider {
    height: 1px;
    background: rgba(255,255,255,0.10);
    margin: 1.1rem 0;
}
.sb-tip {
    font-family: var(--mono);
    font-size: 0.60rem;
    color: rgba(255,255,255,0.42);
    line-height: 1.80;
    padding: 0.7rem 0.85rem;
    background: rgba(0,0,0,0.18);
    border-radius: var(--tc-radius);
    border-left: 2px solid var(--tc-yellow);
}
.sb-tip code {
    color: var(--tc-yellow);
    font-family: var(--mono);
}
.sb-tip strong { color: rgba(255,255,255,0.65); }

/* ══════════════════════════════════════════════
   SECTION LABELS  (ana alan)
══════════════════════════════════════════════ */
.tc-label {
    font-family: var(--sans) !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    color: var(--tc-blue-dark) !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.55rem !important;
    display: flex;
    align-items: center;
    gap: 7px;
}
.tc-label::before {
    content: '';
    display: inline-block;
    width: 3px; height: 15px;
    background: var(--tc-yellow);
    border-radius: 2px;
}

/* ══════════════════════════════════════════════
   DIVIDER
══════════════════════════════════════════════ */
.tc-divider {
    height: 1px;
    background: var(--tc-border);
    margin: 1.4rem 0;
    opacity: 0.6;
}

/* ══════════════════════════════════════════════
   SCHEMA MODE BADGE
══════════════════════════════════════════════ */
.schema-mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,166,81,0.10);
    border: 1px solid rgba(0,166,81,0.30);
    border-radius: 20px;
    padding: 4px 13px;
    font-family: var(--sans);
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--tc-success);
    letter-spacing: 0.3px;
    margin-bottom: 0.8rem;
}
.schema-mode-badge .dot-g {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--tc-success);
}

/* ══════════════════════════════════════════════
   SELECTS
══════════════════════════════════════════════ */
.stSelectbox > div > div {
    background-color: rgba(255,255,255,0.85) !important;
    border: 1.5px solid var(--tc-border) !important;
    border-radius: var(--tc-radius) !important;
    color: var(--tc-text) !important;
    font-family: var(--sans) !important;
    font-size: 0.85rem !important;
    backdrop-filter: blur(6px);
    transition: border-color .2s !important;
}
.stSelectbox > div > div:hover,
.stSelectbox > div > div:focus-within {
    border-color: var(--tc-blue) !important;
    background-color: rgba(255,255,255,0.96) !important;
}
.stSelectbox label {
    font-family: var(--sans) !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    color: var(--tc-text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}
div[data-baseweb="select"] * {
    background-color: rgba(255,255,255,0.96) !important;
}
div[data-baseweb="popover"] * {
    background-color: #FFFFFF !important;
    border-color: var(--tc-border) !important;
    color: var(--tc-text) !important;
}

/* ══════════════════════════════════════════════
   TEXT AREA
══════════════════════════════════════════════ */
.stTextArea textarea {
    background-color: rgba(255,255,255,0.88) !important;
    border: 1.5px solid var(--tc-border) !important;
    border-radius: var(--tc-radius) !important;
    color: var(--tc-text) !important;
    font-family: var(--sans) !important;
    font-size: 0.90rem !important;
    padding: 12px 14px !important;
    resize: vertical !important;
    backdrop-filter: blur(6px);
    transition: border-color .2s, box-shadow .2s !important;
}
.stTextArea textarea:focus {
    border-color: var(--tc-blue) !important;
    background-color: rgba(255,255,255,0.98) !important;
    box-shadow: 0 0 0 3px rgba(0,71,186,0.12) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: var(--tc-text-light) !important; }
.stTextArea label { display: none !important; }

/* ══════════════════════════════════════════════
   GENERATE BUTTON  —  Turkcell Sarısı, Kompakt
══════════════════════════════════════════════ */
.stButton > button {
    width: 100% !important;
    background: var(--tc-yellow) !important;
    color: var(--tc-blue-dark) !important;
    font-family: var(--sans) !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.2px;
    border: none !important;
    border-radius: var(--tc-radius) !important;
    /* Daha kompakt padding — V3'teki devasa boyutu küçültür */
    padding: 0.58rem 1.8rem !important;
    cursor: pointer !important;
    transition: background .18s, box-shadow .18s, transform .10s !important;
    box-shadow: 0 2px 10px rgba(255,209,0,0.32) !important;
}
.stButton > button:hover {
    background: var(--tc-yellow-hover, #C9A800) !important;
    box-shadow: 0 4px 18px rgba(200,168,0,0.40) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 1px 6px rgba(200,168,0,0.28) !important;
}

/* ══════════════════════════════════════════════
   SQL SONUÇ KARTI  —  Glassmorphism Card
══════════════════════════════════════════════ */
.sql-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid var(--tc-border);
    border-top: 3px solid var(--tc-blue);
    border-radius: var(--tc-radius-lg);
    padding: 1.4rem 1.6rem;
    margin-top: 0.5rem;
    box-shadow: var(--tc-shadow-lg);
    backdrop-filter: blur(8px);
}
.sql-card pre {
    font-family: var(--mono) !important;
    font-size: 0.81rem !important;
    line-height: 1.78 !important;
    color: #12213A !important;
    margin: 0 !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
}
/* Syntax highlight — kurumsal Turkcell tonları */
.kw  { color: #0047BA; font-weight: 700; }
.fn  { color: #00875A; }
.str { color: #B83C2B; }
.cmt { color: #8898AA; font-style: italic; }
.num { color: #6D28D9; }

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
    font-size: 0.63rem;
    font-weight: 600;
    color: var(--tc-blue-dark);
    letter-spacing: 0.3px;
}
.sql-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--tc-success);
}

/* ══════════════════════════════════════════════
   STATS ROW
══════════════════════════════════════════════ */
.stats-row {
    display: flex;
    gap: 0.8rem;
    margin-top: 1rem;
}
.stat-chip {
    flex: 1;
    background: rgba(255,255,255,0.82);
    border: 1px solid var(--tc-border);
    border-radius: var(--tc-radius);
    padding: 0.85rem 0.8rem;
    text-align: center;
    box-shadow: 0 1px 8px rgba(0,71,186,0.07);
    backdrop-filter: blur(6px);
    transition: box-shadow .2s, transform .15s;
}
.stat-chip:hover {
    box-shadow: var(--tc-shadow);
    transform: translateY(-1px);
}
.stat-chip .val {
    font-family: var(--sans);
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--tc-blue);
}
.stat-chip .lbl {
    font-size: 0.60rem;
    font-weight: 600;
    color: var(--tc-text-muted);
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ══════════════════════════════════════════════
   ALERTS
══════════════════════════════════════════════ */
.qp-alert {
    border-radius: var(--tc-radius);
    padding: 0.85rem 1.1rem;
    font-size: 0.82rem;
    font-family: var(--sans);
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-top: 0.6rem;
    backdrop-filter: blur(6px);
}
.qp-alert-error {
    background: rgba(255,235,238,0.90);
    border: 1px solid #FFCDD2;
    border-left: 4px solid var(--tc-error);
    color: var(--tc-error);
}
.qp-alert-warn {
    background: rgba(255,243,224,0.90);
    border: 1px solid #FFE0B2;
    border-left: 4px solid var(--tc-warn);
    color: var(--tc-warn);
}
.qp-alert-info {
    background: rgba(232,240,251,0.90);
    border: 1px solid var(--tc-border);
    border-left: 4px solid var(--tc-blue);
    color: var(--tc-blue);
}
.qp-alert-missing-key {
    background: rgba(243,240,255,0.92);
    border: 1px solid #C5B8F8;
    border-left: 4px solid #7C3AED;
    color: #4C1D95;
    border-radius: var(--tc-radius);
    padding: 1.2rem 1.4rem;
    font-size: 0.84rem;
    display: flex;
    align-items: flex-start;
    gap: 13px;
    margin-top: 1.5rem;
    font-family: var(--sans);
    line-height: 1.7;
}
.qp-alert-missing-key strong { color: #3B0764; }
.qp-alert-missing-key code {
    background: #EDE9FE;
    padding: 1px 6px;
    border-radius: 4px;
    font-family: var(--mono);
    font-size: 0.76rem;
    color: #7C3AED;
}
.qp-alert-missing-key pre {
    background: #F5F3FF;
    border: 1px solid #DDD6FE;
    border-radius: 6px;
    padding: 7px 12px;
    font-family: var(--mono);
    font-size: 0.76rem;
    color: #5B21B6;
    margin: 0.4rem 0 0.2rem;
}
.qp-alert-icon { font-size: 1rem; flex-shrink: 0; }

/* ══════════════════════════════════════════════
   EXPANDER
══════════════════════════════════════════════ */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.75) !important;
    border: 1px solid var(--tc-border) !important;
    border-radius: var(--tc-radius) !important;
    color: var(--tc-text-muted) !important;
    font-family: var(--sans) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    backdrop-filter: blur(6px);
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.80) !important;
    border: 1px solid var(--tc-border) !important;
    border-top: none !important;
    backdrop-filter: blur(6px);
}

/* ══════════════════════════════════════════════
   HISTORY ITEM
══════════════════════════════════════════════ */
.history-item {
    background: rgba(255,255,255,0.82);
    border: 1px solid var(--tc-border);
    border-left: 3px solid var(--tc-yellow);
    border-radius: var(--tc-radius);
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    backdrop-filter: blur(4px);
}
.history-item .hi-prompt {
    color: var(--tc-text);
    font-family: var(--sans);
    font-size: 0.82rem;
    font-weight: 500;
    margin-bottom: 3px;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.history-item .hi-meta {
    color: var(--tc-text-light);
    font-size: 0.63rem;
    font-family: var(--sans);
}

/* ══════════════════════════════════════════════
   CODE BLOCK
══════════════════════════════════════════════ */
.stCodeBlock {
    border: 1px solid var(--tc-border) !important;
    border-radius: var(--tc-radius) !important;
    box-shadow: 0 1px 6px rgba(0,71,186,0.06) !important;
}
.stCodeBlock pre {
    background: rgba(232,240,251,0.60) !important;
    font-family: var(--mono) !important;
    font-size: 0.80rem !important;
}
div[data-testid="stCopyButton"] button {
    background: rgba(255,255,255,0.70) !important;
    border: 1px solid var(--tc-border) !important;
    color: var(--tc-blue) !important;
    border-radius: 6px !important;
    font-size: 0.68rem !important;
}
div[data-testid="stCopyButton"] button:hover {
    background: var(--tc-blue) !important;
    color: #FFFFFF !important;
}

/* ══════════════════════════════════════════════
   SPINNER
══════════════════════════════════════════════ */
.stSpinner > div { border-top-color: var(--tc-blue) !important; }

/* ══════════════════════════════════════════════
   FOOTER
══════════════════════════════════════════════ */
.tc-footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid var(--tc-border);
}
.tc-footer span {
    font-family: var(--sans);
    font-size: 0.63rem;
    color: var(--tc-text-light);
    letter-spacing: 0.8px;
}
.tc-footer strong { color: var(--tc-blue); font-weight: 700; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""


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
        pattern = re.compile(rf'\b({re.escape(kw)})\b', re.IGNORECASE)
        sql = pattern.sub(r'<span class="kw">\1</span>', sql)
    return sql


def parse_schema_file(uploaded_file) -> tuple[str, int, int]:
    raw = uploaded_file.read().decode("utf-8", errors="replace")
    table_count = len(re.findall(r'\bCREATE\s+TABLE\b', raw, re.IGNORECASE))
    return raw, len(raw), table_count


def build_system_prompt(dialect: str, style: str) -> str:
    style_map = {
        "Standard":  "Use standard, clean SQL formatting with uppercase keywords.",
        "Compact":   "Return compact SQL without extra newlines, suitable for inline use.",
        "Annotated": "Add brief SQL comments above each major clause explaining what it does.",
    }
    return f"""You are Turkcell SQL AI, an expert SQL engineer specialising in {dialect}.

RULES:
1. Output ONLY valid {dialect} SQL — no markdown fences, no explanation text before or after.
2. {style_map.get(style, '')}
3. Use meaningful table and column aliases.
4. Prefer CTEs (WITH clauses) for complex queries to improve readability.
5. Handle NULL values safely with COALESCE or IS NULL checks where appropriate.
6. For analytical queries, use window functions instead of subqueries when possible.
7. Always end the query with a semicolon.
8. If the request is ambiguous, make the most reasonable assumption and proceed.
9. If the request cannot be converted to SQL, reply with exactly: ERROR: Not a valid SQL request.

Dialect notes:
- PostgreSQL: ILIKE for case-insensitive search, EXTRACT() for dates.
- MySQL: DATE_FORMAT(), IFNULL().
- SQLite: strftime() for dates.
- SQL Server (T-SQL): TOP instead of LIMIT, GETDATE(), square bracket identifiers.
- BigQuery: backtick identifiers, SAFE_DIVIDE(), ARRAY/STRUCT if needed.
- Snowflake: QUALIFY for window-filtered rows, IFF(), FLATTEN for semi-structured data.
"""


def build_user_message(prompt: str, schema_text: str | None) -> str:
    if not schema_text:
        return prompt.strip()
    return f"""=== DATABASE SCHEMA ===
Use ONLY the table names and column names defined below. Do NOT invent any table or column.

{schema_text.strip()}

=== END OF SCHEMA ===

Generate SQL for the following request using exclusively the tables and columns above.
REQUEST: {prompt.strip()}"""


def generate_sql(
    prompt: str,
    api_key: str,
    dialect: str,
    style: str,
    model: str,
    schema_text: str | None = None,
) -> dict:
    client   = openai.OpenAI(api_key=api_key)
    start    = time.time()
    user_msg = build_user_message(prompt, schema_text)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": build_system_prompt(dialect, style)},
            {"role": "user",   "content": user_msg},
        ],
        temperature=0.2,
        max_tokens=1400,
    )
    elapsed = round(time.time() - start, 2)
    sql     = response.choices[0].message.content.strip()
    tokens  = response.usage.total_tokens
    return {"sql": sql, "tokens": tokens, "elapsed": elapsed}


def validate_result(sql: str) -> tuple[bool, str]:
    if sql.startswith("ERROR:"):
        return False, sql.replace("ERROR:", "").strip()
    if len(sql) < 10:
        return False, "Model çok kısa bir yanıt döndürdü."
    return True, ""


# ═════════════════════════════════════════════════
# SIDEBAR  —  Koyu Lacivert + Şema Yükleme
# ═════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-inner-top">
        <span class="sb-inner-top-icon">🗄️</span>
        <span class="sb-inner-top-title">Şema Bağlamı</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sb-label">📂 Şema dosyası yükle</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "schema_upload",
        type=["sql", "txt"],
        accept_multiple_files=False,
        label_visibility="collapsed",
        help="CREATE TABLE tanımlarını içeren .sql veya .txt dosyası yükleyin.",
    )

    schema_text: str | None = None
    schema_meta: dict       = {}

    if uploaded_file is not None:
        try:
            raw, char_count, table_count = parse_schema_file(uploaded_file)
            if char_count > 80_000:
                st.markdown("""
                <div class="qp-alert qp-alert-warn" style="font-size:.68rem;padding:.6rem .85rem;">
                    <span>⚠</span><span>Dosya 80 KB limitini aşıyor. Kullanılmayan tabloları kaldırın.</span>
                </div>""", unsafe_allow_html=True)
            else:
                schema_text = raw
                schema_meta = {"name": uploaded_file.name, "tables": table_count, "chars": char_count}
                preview = raw[:800] + ("\n…" if len(raw) > 800 else "")
                st.markdown(f"""
                <div class="schema-card"><pre>{preview}</pre></div>
                <div class="schema-status">
                    <span class="dot-green"></span>
                    {table_count} tablo · {char_count:,} karakter
                </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class="qp-alert qp-alert-error" style="font-size:.68rem;padding:.6rem .85rem;">
                <span>✖</span><span>Dosya okunamadı: {e}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <p class="schema-inactive">
            Şema yüklenmedi.<br>
            AI genel bilgisiyle<br>tablo yapılarını tahmin eder.
        </p>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-tip">
        💡 <strong>İpucu:</strong><br>
        <code>pg_dump --schema-only</code> (PostgreSQL)<br>
        <code>SHOW CREATE TABLE</code> (MySQL)
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# API KEY — yalnızca st.secrets
# ─────────────────────────────────────────────
resolved_api_key = st.secrets.get("OPENAI_API_KEY", "")

if not resolved_api_key:
    st.markdown("""
    <div class="qp-alert qp-alert-missing-key">
        <span class="qp-alert-icon">🔐</span>
        <div>
            <strong>API anahtarı bulunamadı.</strong><br>
            <span style="font-size:0.78rem;opacity:.85;">
                Projenizin <code>.streamlit/secrets.toml</code> dosyasına şu satırı ekleyin:
            </span>
            <pre>OPENAI_API_KEY = "sk-..."</pre>
            <span style="font-size:0.70rem;opacity:.60;">
                Streamlit Cloud → App Settings › Secrets bölümü de kullanılabilir.
            </span>
        </div>
    </div>""", unsafe_allow_html=True)
    st.stop()


# ═════════════════════════════════════════════════
# HEADER  —  Turkcell Mavi Şerit + Sarı Logo Badge
# ═════════════════════════════════════════════════
st.markdown("""
<div class="tc-header">
    <div class="tc-logo-wrap">
        <div class="tc-logo-badge">T</div>
        <div class="tc-brand-text">
            <div class="tc-brand-name">Turkcell SQL AI</div>
            <div class="tc-brand-tagline">Natural Language → SQL</div>
        </div>
    </div>
    <div class="tc-header-pill">Powered by OpenAI</div>
</div>
<div style="height:1.8rem"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
st.markdown('<p class="tc-label">⚙ Yapılandırma</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    dialect = st.selectbox("Dialect",
        ["PostgreSQL", "MySQL", "SQLite", "SQL Server (T-SQL)", "BigQuery", "Snowflake"],
        key="dialect_select")
with col2:
    style = st.selectbox("Stil",
        ["Standard", "Annotated", "Compact"],
        key="style_select")
with col3:
    model = st.selectbox("Model",
        ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
        key="model_select")

st.markdown('<div class="tc-divider"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# EXAMPLE PROMPTS
# ─────────────────────────────────────────────
EXAMPLES = [
    ("📦", "Show the top 10 customers by total revenue in 2024"),
    ("📊", "Monthly active users grouped by country for the last 6 months"),
    ("🔍", "Find all orders that were delivered more than 3 days late"),
    ("🔗", "Products never purchased, joined with their category names"),
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

# Schema badge
if schema_text:
    st.markdown(f"""
    <div class="schema-mode-badge">
        <span class="dot-g"></span>
        Şema Modu Aktif &nbsp;·&nbsp; {schema_meta['name']} &nbsp;·&nbsp; {schema_meta['tables']} tablo
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PROMPT INPUT
# ─────────────────────────────────────────────
st.markdown('<p class="tc-label">✦ Doğal Dil ile Açıkla</p>', unsafe_allow_html=True)

prompt = st.text_area(
    "prompt",
    value=st.session_state.last_prompt,
    height=115,
    placeholder=(
        "Örn. → Geçen ay kaydolan ancak henüz sipariş vermemiş kullanıcıları listele,\n"
        "       referans kaynağına göre gruplandırarak kayıt tarihine göre sırala…"
    ),
    key="prompt_input",
)

generate_clicked = st.button("⚡  SQL Oluştur", use_container_width=True)


# ─────────────────────────────────────────────
# GENERATE LOGIC
# ─────────────────────────────────────────────
if generate_clicked:
    if not prompt.strip():
        st.markdown("""
        <div class="qp-alert qp-alert-warn">
            <span class="qp-alert-icon">⚠</span>
            <span>Lütfen oluşturmadan önce bir açıklama girin.</span>
        </div>""", unsafe_allow_html=True)
        st.stop()

    spinner_msg = "Şemaya özel SQL oluşturuluyor…" if schema_text else "SQL oluşturuluyor…"

    with st.spinner(spinner_msg):
        try:
            result = generate_sql(
                prompt=prompt, api_key=resolved_api_key,
                dialect=dialect, style=style, model=model,
                schema_text=schema_text,
            )
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
        except openai.BadRequestError as e:
            st.markdown(f"""<div class="qp-alert qp-alert-error"><span class="qp-alert-icon">✖</span>
            <span><strong>Hatalı istek.</strong> {str(e)}</span></div>""",
            unsafe_allow_html=True); st.stop()
        except Exception as e:
            st.markdown(f"""<div class="qp-alert qp-alert-error"><span class="qp-alert-icon">✖</span>
            <span><strong>Beklenmeyen hata:</strong> {str(e)}</span></div>""",
            unsafe_allow_html=True); st.stop()

    ok, err_msg = validate_result(result["sql"])
    if not ok:
        st.markdown(f"""<div class="qp-alert qp-alert-warn"><span class="qp-alert-icon">⚠</span>
        <span><strong>Model Bildirimi:</strong> {err_msg}</span></div>""",
        unsafe_allow_html=True); st.stop()

    # Store
    st.session_state.query_count  += 1
    st.session_state.total_tokens += result["tokens"]
    st.session_state.history.insert(0, {
        "prompt":      prompt,
        "sql":         result["sql"],
        "dialect":     dialect,
        "ts":          datetime.datetime.now().strftime("%H:%M:%S"),
        "tokens":      result["tokens"],
        "schema_name": schema_meta.get("name", "—") if schema_text else "—",
    })
    st.session_state.history = st.session_state.history[:20]

    # Output
    st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)
    st.markdown('<p class="tc-label">✦ Oluşturulan SQL</p>', unsafe_allow_html=True)

    schema_badge_html = (
        f'<span class="sql-badge" style="background:#D1FAE5;color:#065F46;">'
        f'<span class="dot" style="background:#059669"></span>{schema_meta["name"]}</span>'
        if schema_text else ""
    )

    highlighted = highlight_sql(result["sql"])
    st.markdown(f"""
    <div class="sql-card">
        <pre>{highlighted}</pre>
        <div class="sql-status-bar">
            <span class="sql-badge"><span class="dot"></span>{dialect}</span>
            <div style="display:flex;gap:0.55rem;align-items:center;">
                {schema_badge_html}
                <span class="sql-badge">{result['elapsed']}s · {result['tokens']} token</span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.code(result["sql"], language="sql")

    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-chip">
            <div class="val">{st.session_state.query_count}</div>
            <div class="lbl">Toplam Sorgu</div>
        </div>
        <div class="stat-chip">
            <div class="val">{result['elapsed']}s</div>
            <div class="lbl">Yanıt Süresi</div>
        </div>
        <div class="stat-chip">
            <div class="val">{st.session_state.total_tokens}</div>
            <div class="lbl">Token Kullanımı</div>
        </div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HISTORY PANEL
# ─────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="tc-divider"></div>', unsafe_allow_html=True)
    with st.expander(f"🕑  Sorgu Geçmişi  ({len(st.session_state.history)} kayıt)", expanded=False):
        for entry in st.session_state.history:
            schema_tag = f" · 🗄 {entry['schema_name']}" if entry.get("schema_name") and entry["schema_name"] != "—" else ""
            st.markdown(f"""
            <div class="history-item">
                <div class="hi-prompt">{entry['prompt']}</div>
                <div class="hi-meta">{entry['ts']} · {entry['dialect']}{schema_tag} · {entry['tokens']} token</div>
            </div>""", unsafe_allow_html=True)
            st.code(entry["sql"], language="sql")

        if st.button("🗑  Geçmişi Temizle", key="clear_history"):
            st.session_state.history      = []
            st.session_state.query_count  = 0
            st.session_state.total_tokens = 0
            st.rerun()


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="tc-footer">
    <span>
        <strong>Turkcell SQL AI</strong> &nbsp;·&nbsp; OpenAI ile güçlendirilmiştir &nbsp;·&nbsp; Streamlit üzerinde çalışır
    </span>
</div>""", unsafe_allow_html=True)