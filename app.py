"""
╔══════════════════════════════════════════════════╗
║   QUERY PULSE AI  —  app.py                      ║
║   Turkcell Kurumsal Tema · Natural Lang → SQL    ║
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
    page_title="Query Pulse AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────
# GLOBAL CSS — Turkcell Kurumsal Tema
# ─────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts: Inter + Roboto Mono ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Roboto+Mono:wght@400;500&display=swap');

/* ── Turkcell Renk Paleti ── */
:root {
    --tc-blue:        #0047BA;
    --tc-blue-dark:   #003090;
    --tc-blue-mid:    #1565C0;
    --tc-blue-light:  #E8F0FB;
    --tc-blue-pale:   #F0F5FA;
    --tc-yellow:      #FFD100;
    --tc-yellow-dark: #E6BC00;
    --tc-yellow-pale: #FFFBE6;
    --tc-navy:        #001A5E;
    --tc-text:        #1A1A2E;
    --tc-text-muted:  #5A6A8A;
    --tc-text-light:  #8898AA;
    --tc-border:      #D0DCF0;
    --tc-border-light:#E8EEF8;
    --tc-white:       #FFFFFF;
    --tc-bg:          #F5F7FB;
    --tc-success:     #00A651;
    --tc-error:       #D32F2F;
    --tc-warn:        #F57C00;
    --tc-radius:      8px;
    --tc-radius-lg:   12px;
    --tc-shadow:      0 2px 12px rgba(0,71,186,0.10);
    --tc-shadow-lg:   0 4px 24px rgba(0,71,186,0.14);
    --sans:           'Inter', system-ui, sans-serif;
    --mono:           'Roboto Mono', monospace;
}

/* ── Reset & Base ── */
html, body, [class*="css"] {
    background-color: var(--tc-bg) !important;
    color: var(--tc-text) !important;
    font-family: var(--sans) !important;
    font-size: 14px;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 2rem 4rem !important;
    max-width: 860px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--tc-border-light); }
::-webkit-scrollbar-thumb { background: var(--tc-blue); border-radius: 3px; }

/* ════════════════ HEADER ══════════════════════ */
.tc-header {
    background: linear-gradient(135deg, var(--tc-blue-dark) 0%, var(--tc-blue) 60%, var(--tc-blue-mid) 100%);
    margin: -1rem -2rem 0;
    padding: 0 2.5rem;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 8px rgba(0,48,144,0.25);
    position: relative;
    overflow: hidden;
}
.tc-header::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 200px; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04));
    pointer-events: none;
}
.tc-header-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}
.tc-header-icon {
    width: 36px; height: 36px;
    background: var(--tc-yellow);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    box-shadow: 0 2px 8px rgba(255,209,0,0.4);
    flex-shrink: 0;
}
.tc-header-title {
    font-family: var(--sans) !important;
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    margin: 0 !important;
    padding: 0 !important;
    letter-spacing: -0.3px;
    line-height: 1 !important;
}
.tc-header-sub {
    font-family: var(--mono) !important;
    font-size: 0.62rem !important;
    color: rgba(255,255,255,0.55) !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 2px !important;
}
.tc-header-badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 4px 14px;
    font-family: var(--mono);
    font-size: 0.62rem;
    color: rgba(255,255,255,0.8);
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* ════════════════ SECTION LABELS ══════════════ */
.tc-label {
    font-family: var(--sans) !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    color: var(--tc-blue) !important;
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
    width: 3px; height: 14px;
    background: var(--tc-yellow);
    border-radius: 2px;
}

/* ════════════════ DIVIDER ══════════════════════ */
.tc-divider {
    height: 1px;
    background: var(--tc-border);
    margin: 1.4rem 0;
}
.tc-divider-blue {
    height: 2px;
    background: linear-gradient(90deg, var(--tc-blue), transparent);
    margin: 1.4rem 0;
    border-radius: 2px;
}

/* ════════════════ SIDEBAR ══════════════════════ */
[data-testid="stSidebar"] {
    background-color: var(--tc-blue-pale) !important;
    border-right: 1px solid var(--tc-border) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 1.2rem 2rem !important;
}
.sb-top-bar {
    background: var(--tc-blue);
    margin: 0 -1.2rem 1.4rem;
    padding: 1rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sb-top-bar-icon { font-size: 1rem; }
.sb-top-bar-title {
    font-family: var(--sans);
    font-size: 0.82rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: 0.2px;
}
.sb-label {
    font-family: var(--sans);
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--tc-navy);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 5px;
}
.sb-label::before {
    content: '';
    display: inline-block;
    width: 3px; height: 12px;
    background: var(--tc-yellow);
    border-radius: 2px;
}
[data-testid="stFileUploader"] {
    background: var(--tc-white) !important;
    border: 2px dashed var(--tc-border) !important;
    border-radius: var(--tc-radius) !important;
    transition: border-color .2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--tc-blue) !important;
}
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: var(--tc-text-muted) !important;
    font-family: var(--sans) !important;
    font-size: 0.72rem !important;
}
[data-testid="stFileUploaderDropzone"] small {
    color: var(--tc-text-light) !important;
    font-family: var(--sans) !important;
    font-size: 0.62rem !important;
}
.schema-card {
    background: var(--tc-white);
    border: 1px solid var(--tc-border);
    border-left: 3px solid var(--tc-blue);
    border-radius: var(--tc-radius);
    padding: 0.85rem 1rem;
    margin-top: 0.7rem;
    max-height: 260px;
    overflow-y: auto;
    box-shadow: var(--tc-shadow);
}
.schema-card pre {
    font-family: var(--mono) !important;
    font-size: 0.65rem !important;
    line-height: 1.7 !important;
    color: var(--tc-blue-dark) !important;
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
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--tc-success);
    letter-spacing: 0.5px;
}
.schema-status .dot-green {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--tc-success);
    flex-shrink: 0;
}
.schema-inactive {
    font-family: var(--sans);
    font-size: 0.72rem;
    color: var(--tc-text-muted);
    line-height: 1.7;
    padding: 0.3rem 0;
}
.sb-divider { height: 1px; background: var(--tc-border); margin: 1.1rem 0; }
.sb-tip {
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--tc-text-muted);
    line-height: 1.75;
    padding: 0.7rem 0.85rem;
    background: var(--tc-white);
    border-radius: var(--tc-radius);
    border-left: 3px solid var(--tc-blue);
    box-shadow: 0 1px 4px rgba(0,71,186,0.06);
}

/* ════════════════ SCHEMA MODE BADGE ═══════════ */
.schema-mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #E8F5E9;
    border: 1px solid #A5D6A7;
    border-radius: 20px;
    padding: 4px 12px;
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

/* ════════════════ CONFIG CARDS ════════════════ */
.config-section {
    background: var(--tc-white);
    border: 1px solid var(--tc-border);
    border-radius: var(--tc-radius-lg);
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: var(--tc-shadow);
}

/* ════════════════ SELECTS ══════════════════════ */
.stSelectbox > div > div {
    background-color: var(--tc-white) !important;
    border: 1.5px solid var(--tc-border) !important;
    border-radius: var(--tc-radius) !important;
    color: var(--tc-text) !important;
    font-family: var(--sans) !important;
    font-size: 0.85rem !important;
    transition: border-color .2s !important;
}
.stSelectbox > div > div:hover,
.stSelectbox > div > div:focus-within {
    border-color: var(--tc-blue) !important;
}
.stSelectbox label {
    font-family: var(--sans) !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    color: var(--tc-text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}
div[data-baseweb="select"] * { background-color: var(--tc-white) !important; }
div[data-baseweb="popover"] * {
    background-color: var(--tc-white) !important;
    border-color: var(--tc-border) !important;
    color: var(--tc-text) !important;
}

/* ════════════════ TEXT AREA ════════════════════ */
.stTextArea textarea {
    background-color: var(--tc-white) !important;
    border: 1.5px solid var(--tc-border) !important;
    border-radius: var(--tc-radius) !important;
    color: var(--tc-text) !important;
    font-family: var(--sans) !important;
    font-size: 0.9rem !important;
    padding: 12px 14px !important;
    resize: vertical !important;
    transition: border-color .2s, box-shadow .2s !important;
    box-shadow: 0 1px 4px rgba(0,71,186,0.05) !important;
}
.stTextArea textarea:focus {
    border-color: var(--tc-blue) !important;
    box-shadow: 0 0 0 3px rgba(0,71,186,0.10) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: var(--tc-text-light) !important; }
.stTextArea label { display: none !important; }

/* ════════════════ GENERATE BUTTON ════════════ */
.stButton > button {
    width: 100% !important;
    background: var(--tc-yellow) !important;
    color: var(--tc-navy) !important;
    font-family: var(--sans) !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.3px;
    border: none !important;
    border-radius: var(--tc-radius) !important;
    padding: 0.72rem 2rem !important;
    cursor: pointer !important;
    transition: background .15s, box-shadow .2s, transform .1s !important;
    box-shadow: 0 3px 12px rgba(255,209,0,0.35) !important;
}
.stButton > button:hover {
    background: var(--tc-yellow-dark) !important;
    box-shadow: 0 5px 20px rgba(255,209,0,0.45) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(255,209,0,0.3) !important;
}

/* ════════════════ SQL OUTPUT CARD ════════════ */
.sql-card {
    background: var(--tc-white);
    border: 1px solid var(--tc-border);
    border-top: 3px solid var(--tc-blue);
    border-radius: var(--tc-radius-lg);
    padding: 1.4rem 1.6rem;
    margin-top: 0.5rem;
    box-shadow: var(--tc-shadow-lg);
}
.sql-card pre {
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    line-height: 1.75 !important;
    color: var(--tc-blue-dark) !important;
    margin: 0 !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
}
/* SQL syntax highlight */
.kw  { color: var(--tc-blue);      font-weight: 700; }
.fn  { color: var(--tc-success); }
.str { color: #C0392B; }
.cmt { color: var(--tc-text-light); font-style: italic; }
.num { color: #7B1FA2; }

.sql-status-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 1rem;
    padding-top: 0.8rem;
    border-top: 1px solid var(--tc-border-light);
}
.sql-badge {
    font-family: var(--sans);
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--tc-text-muted);
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 5px;
    background: var(--tc-blue-light);
    padding: 3px 9px;
    border-radius: 20px;
}
.sql-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--tc-success);
}

/* ════════════════ STATS ROW ════════════════════ */
.stats-row {
    display: flex;
    gap: 0.8rem;
    margin-top: 1rem;
}
.stat-chip {
    flex: 1;
    background: var(--tc-white);
    border: 1px solid var(--tc-border);
    border-radius: var(--tc-radius);
    padding: 0.9rem 0.8rem;
    text-align: center;
    box-shadow: 0 1px 6px rgba(0,71,186,0.07);
    transition: box-shadow .2s;
}
.stat-chip:hover { box-shadow: var(--tc-shadow); }
.stat-chip .val {
    font-family: var(--sans);
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--tc-blue);
}
.stat-chip .lbl {
    font-size: 0.62rem;
    font-weight: 600;
    color: var(--tc-text-muted);
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ════════════════ ALERTS ══════════════════════ */
.qp-alert {
    border-radius: var(--tc-radius);
    padding: 0.9rem 1.2rem;
    font-size: 0.82rem;
    font-family: var(--sans);
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-top: 0.6rem;
}
.qp-alert-error {
    background: #FFEBEE;
    border: 1px solid #FFCDD2;
    color: var(--tc-error);
    border-left: 4px solid var(--tc-error);
}
.qp-alert-warn {
    background: #FFF3E0;
    border: 1px solid #FFE0B2;
    color: var(--tc-warn);
    border-left: 4px solid var(--tc-warn);
}
.qp-alert-info {
    background: var(--tc-blue-light);
    border: 1px solid var(--tc-border);
    color: var(--tc-blue);
    border-left: 4px solid var(--tc-blue);
}
.qp-alert-missing-key {
    background: #F3F0FF;
    border: 1px solid #C5B8F8;
    border-left: 4px solid #7C3AED;
    color: #4C1D95;
    border-radius: var(--tc-radius);
    padding: 1.3rem 1.5rem;
    font-size: 0.85rem;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-top: 1.5rem;
    font-family: var(--sans);
    line-height: 1.7;
}
.qp-alert-missing-key strong { color: #3B0764; font-size: 0.9rem; }
.qp-alert-missing-key code {
    background: #EDE9FE;
    padding: 1px 6px;
    border-radius: 4px;
    font-size: 0.78rem;
    font-family: var(--mono);
    color: #7C3AED;
}
.qp-alert-missing-key pre {
    background: #F5F3FF;
    border: 1px solid #DDD6FE;
    border-radius: 6px;
    padding: 8px 14px;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: #5B21B6;
    margin: 0.5rem 0 0.3rem;
    white-space: pre;
}
.qp-alert-icon { font-size: 1rem; flex-shrink: 0; }

/* ════════════════ EXPANDER ════════════════════ */
.streamlit-expanderHeader {
    background: var(--tc-white) !important;
    border: 1px solid var(--tc-border) !important;
    border-radius: var(--tc-radius) !important;
    color: var(--tc-text-muted) !important;
    font-family: var(--sans) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
}
.streamlit-expanderContent {
    background: var(--tc-white) !important;
    border: 1px solid var(--tc-border) !important;
    border-top: none !important;
}

/* ════════════════ HISTORY ITEM ════════════════ */
.history-item {
    background: var(--tc-white);
    border: 1px solid var(--tc-border);
    border-left: 3px solid var(--tc-yellow);
    border-radius: var(--tc-radius);
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 1px 4px rgba(0,71,186,0.06);
}
.history-item .hi-prompt {
    color: var(--tc-text);
    font-family: var(--sans);
    font-size: 0.82rem;
    font-weight: 500;
    margin-bottom: 4px;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.history-item .hi-meta {
    color: var(--tc-text-light);
    font-size: 0.65rem;
    letter-spacing: 0.3px;
    font-family: var(--sans);
}

/* ════════════════ COPY BUTTON ════════════════ */
div[data-testid="stCopyButton"] button {
    background: var(--tc-blue-light) !important;
    border: 1px solid var(--tc-border) !important;
    color: var(--tc-blue) !important;
    border-radius: 6px !important;
    font-size: 0.7rem !important;
}
div[data-testid="stCopyButton"] button:hover {
    background: var(--tc-blue) !important;
    color: var(--tc-white) !important;
}

/* ════════════════ SPINNER ══════════════════════ */
.stSpinner > div { border-top-color: var(--tc-blue) !important; }

/* ════════════════ CODE BLOCK ══════════════════ */
.stCodeBlock {
    border: 1px solid var(--tc-border) !important;
    border-radius: var(--tc-radius) !important;
}
.stCodeBlock pre {
    background: var(--tc-blue-pale) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
}

/* ════════════════ FOOTER ══════════════════════ */
.tc-footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid var(--tc-border);
}
.tc-footer span {
    font-family: var(--sans);
    font-size: 0.65rem;
    color: var(--tc-text-light);
    letter-spacing: 1px;
}
.tc-footer strong { color: var(--tc-blue); font-weight: 600; }
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
    style_instructions = {
        "Standard":  "Use standard, clean SQL formatting with uppercase keywords.",
        "Compact":   "Return compact SQL without extra newlines, suitable for inline use.",
        "Annotated": "Add brief SQL comments above each major clause explaining what it does.",
    }
    return f"""You are QueryPulse AI, an expert SQL engineer specialising in {dialect}.

RULES:
1. Output ONLY valid {dialect} SQL — no markdown fences, no explanation text before or after.
2. {style_instructions.get(style, '')}
3. Use meaningful table and column aliases.
4. Prefer CTEs (WITH clauses) for complex queries to improve readability.
5. Handle NULL values safely with COALESCE or IS NULL checks where appropriate.
6. For analytical queries, use window functions instead of subqueries when possible.
7. Always end the query with a semicolon.
8. If the request is ambiguous, make the most reasonable assumption and proceed.
9. If the request cannot be converted to SQL, reply with exactly: ERROR: Not a valid SQL request.

Dialect-specific notes:
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
The following is the exact schema of the target database.
You MUST use ONLY the table names and column names defined here.
Do NOT invent, guess, or hallucinate any table or column that is not listed below.

{schema_text.strip()}

=== END OF SCHEMA ===

Now generate SQL for the following request using exclusively the tables and columns above.

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
        return False, "Model returned an unexpectedly short response."
    return True, ""


# ═════════════════════════════════════════════
# SIDEBAR — Schema Uploader
# ═════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-top-bar">
        <span class="sb-top-bar-icon">🗄️</span>
        <span class="sb-top-bar-title">Şema Bağlamı</span>
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
                <div class="qp-alert qp-alert-warn" style="font-size:.7rem;padding:.65rem .9rem;">
                    <span>⚠</span>
                    <span>Dosya 80 KB sınırını aşıyor. Kullanılmayan tabloları kaldırın.</span>
                </div>""", unsafe_allow_html=True)
            else:
                schema_text = raw
                schema_meta = {
                    "name":   uploaded_file.name,
                    "tables": table_count,
                    "chars":  char_count,
                }
                preview = raw[:800] + ("\n…" if len(raw) > 800 else "")
                st.markdown(f"""
                <div class="schema-card">
                    <pre>{preview}</pre>
                </div>
                <div class="schema-status">
                    <span class="dot-green"></span>
                    {table_count} tablo · {char_count:,} karakter
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class="qp-alert qp-alert-error" style="font-size:.7rem;padding:.65rem .9rem;">
                <span>✖</span>
                <span>Dosya okunamadı: {e}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <p class="schema-inactive">
            Şema yüklenmedi.<br>
            AI genel bilgisiyle tablo<br>
            yapılarını tahmin edecek.
        </p>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-tip">
        💡 <strong>İpucu:</strong> Şemanı dışa aktar:<br>
        <code>pg_dump --schema-only</code> (PostgreSQL)<br>
        <code>SHOW CREATE TABLE</code> (MySQL)
    </div>
    """, unsafe_allow_html=True)


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
                Projenizin <code>.streamlit/secrets.toml</code> dosyasına şu satırı ekleyin
                ve uygulamayı yeniden başlatın:
            </span>
            <pre>OPENAI_API_KEY = "sk-..."</pre>
            <span style="font-size:0.72rem;opacity:.65;">
                Streamlit Cloud → App Settings › Secrets bölümüne de ekleyebilirsiniz.
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────
# HEADER — Turkcell Mavi Şerit
# ─────────────────────────────────────────────
st.markdown("""
<div class="tc-header">
    <div class="tc-header-brand">
        <div class="tc-header-icon">⚡</div>
        <div>
            <div class="tc-header-title">Query Pulse AI</div>
            <div class="tc-header-sub">Natural Language → SQL</div>
        </div>
    </div>
    <div class="tc-header-badge">Powered by OpenAI</div>
</div>
<div style="height:1.8rem"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONFIGURATION CARD
# ─────────────────────────────────────────────
st.markdown('<p class="tc-label">⚙ Yapılandırma</p>', unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        dialect = st.selectbox(
            "Dialect",
            ["PostgreSQL", "MySQL", "SQLite", "SQL Server (T-SQL)", "BigQuery", "Snowflake"],
            key="dialect_select",
        )
    with col2:
        style = st.selectbox(
            "Stil",
            ["Standard", "Annotated", "Compact"],
            key="style_select",
        )
    with col3:
        model = st.selectbox(
            "Model",
            ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
            key="model_select",
        )

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


# ─────────────────────────────────────────────
# SCHEMA MODE BADGE
# ─────────────────────────────────────────────
if schema_text:
    st.markdown(f"""
    <div class="schema-mode-badge">
        <span class="dot-g"></span>
        Şema Modu Aktif &nbsp;·&nbsp; {schema_meta['name']} &nbsp;·&nbsp; {schema_meta['tables']} tablo
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PROMPT INPUT
# ─────────────────────────────────────────────
st.markdown('<p class="tc-label">✦ Doğal Dil ile Açıkla</p>', unsafe_allow_html=True)

placeholder_schema = (
    "Örn. → Geçen ay kaydolan ancak henüz sipariş vermemiş kullanıcıları listele.\n"
    "       AI yalnızca yüklenen şemadaki sütunları kullanacak."
)
placeholder_general = (
    "Örn. → Geçen ay kaydolan ancak henüz satın alma yapmamış kullanıcıları,\n"
    "       referans kaynağına göre gruplandırarak kayıt tarihine göre sırala…"
)

prompt = st.text_area(
    "prompt",
    value=st.session_state.last_prompt,
    height=115,
    placeholder=placeholder_schema if schema_text else placeholder_general,
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
                prompt=prompt,
                api_key=resolved_api_key,
                dialect=dialect,
                style=style,
                model=model,
                schema_text=schema_text,
            )
        except openai.AuthenticationError:
            st.markdown("""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>Kimlik doğrulama hatası.</strong> API anahtarınız OpenAI tarafından reddedildi.</span>
            </div>""", unsafe_allow_html=True)
            st.stop()
        except openai.RateLimitError:
            st.markdown("""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>İstek limiti aşıldı.</strong> OpenAI kotanız doldu. Kısa süre sonra tekrar deneyin.</span>
            </div>""", unsafe_allow_html=True)
            st.stop()
        except openai.APIConnectionError:
            st.markdown("""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>Bağlantı hatası.</strong> OpenAI API'ye ulaşılamadı.</span>
            </div>""", unsafe_allow_html=True)
            st.stop()
        except openai.BadRequestError as e:
            st.markdown(f"""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>Hatalı istek.</strong> {str(e)}</span>
            </div>""", unsafe_allow_html=True)
            st.stop()
        except Exception as e:
            st.markdown(f"""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>Beklenmeyen hata:</strong> {str(e)}</span>
            </div>""", unsafe_allow_html=True)
            st.stop()

    ok, err_msg = validate_result(result["sql"])
    if not ok:
        st.markdown(f"""
        <div class="qp-alert qp-alert-warn">
            <span class="qp-alert-icon">⚠</span>
            <span><strong>Model Bildirimi:</strong> {err_msg}</span>
        </div>""", unsafe_allow_html=True)
        st.stop()

    # ── Store ──
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

    # ── Output ──
    st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)
    st.markdown('<p class="tc-label">✦ Oluşturulan SQL</p>', unsafe_allow_html=True)

    schema_badge_html = (
        f'<span class="sql-badge" style="background:#E8F5E9;color:#2E7D32;">'
        f'<span class="dot"></span>{schema_meta["name"]}</span>'
        if schema_text else ""
    )

    highlighted = highlight_sql(result["sql"])
    st.markdown(f"""
    <div class="sql-card">
        <pre>{highlighted}</pre>
        <div class="sql-status-bar">
            <span class="sql-badge">
                <span class="dot"></span>
                {dialect}
            </span>
            <div style="display:flex;gap:0.6rem;align-items:center;">
                {schema_badge_html}
                <span class="sql-badge">{result['elapsed']}s · {result['tokens']} token</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    </div>
    """, unsafe_allow_html=True)


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
            </div>
            """, unsafe_allow_html=True)
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
        <strong>Query Pulse AI</strong> &nbsp;·&nbsp; OpenAI ile güçlendirilmiştir &nbsp;·&nbsp; Streamlit üzerinde çalışır
    </span>
</div>
""", unsafe_allow_html=True)