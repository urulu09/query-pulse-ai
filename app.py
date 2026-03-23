"""
╔═══════════════════════════════════════════════╗
║         QUERY PULSE AI  —  app.py             ║
║   Natural Language  →  Professional SQL       ║
╚═══════════════════════════════════════════════╝
"""

import streamlit as st
import openai
import re
import time
import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Query Pulse AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Dark Mode + Custom Design
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&display=swap');

/* ── CSS Variables ── */
:root {
    --bg-base:       #0a0c10;
    --bg-card:       #10141c;
    --bg-input:      #141820;
    --bg-hover:      #1a2030;
    --accent:        #00e5ff;
    --accent-dim:    #00e5ff22;
    --accent-glow:   0 0 24px #00e5ff55;
    --green:         #00ff9d;
    --red:           #ff4d6d;
    --yellow:        #ffd166;
    --text-primary:  #e8eaf0;
    --text-muted:    #5a6380;
    --text-dim:      #8892b0;
    --border:        #1e2436;
    --border-accent: #00e5ff44;
    --radius:        10px;
    --mono:          'Space Mono', monospace;
    --display:       'Syne', sans-serif;
}

/* ── Reset & Base ── */
html, body, [class*="css"] {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: var(--display) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2rem 4rem !important;
    max-width: 820px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* ═══════════════ SIDEBAR ════════════════════ */
[data-testid="stSidebar"] {
    background-color: #0d1017 !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 1.8rem 1.4rem 2rem !important;
}
.sb-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 1.4rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}
.sb-header-icon { font-size: 1.1rem; }
.sb-header-title {
    font-family: var(--display);
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: 0.3px;
}
.sb-label {
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--accent);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 5px;
}
.sb-label::before {
    content: '';
    display: inline-block;
    width: 10px; height: 1px;
    background: var(--accent);
}
/* File uploader dark styling */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed #2a3450 !important;
    border-radius: var(--radius) !important;
    transition: border-color .25s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #00e5ff88 !important;
}
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: var(--text-muted) !important;
    font-family: var(--mono) !important;
    font-size: 0.70rem !important;
}
[data-testid="stFileUploaderDropzone"] small {
    color: var(--text-muted) !important;
    font-family: var(--mono) !important;
    font-size: 0.62rem !important;
}
/* Schema preview card */
.schema-card {
    background: #060a10;
    border: 1px solid #00e5ff1a;
    border-radius: var(--radius);
    padding: 0.85rem 1rem;
    margin-top: 0.7rem;
    max-height: 290px;
    overflow-y: auto;
}
.schema-card pre {
    font-family: var(--mono) !important;
    font-size: 0.65rem !important;
    line-height: 1.7 !important;
    color: #7ec8e3 !important;
    margin: 0 !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
}
.schema-status {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 0.8rem;
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--green);
    letter-spacing: 1px;
}
.schema-status .dot-green {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 6px var(--green);
    flex-shrink: 0;
}
.schema-inactive {
    font-family: var(--mono);
    font-size: 0.66rem;
    color: var(--text-muted);
    line-height: 1.7;
    padding: 0.3rem 0;
}
.sb-divider { height: 1px; background: var(--border); margin: 1.2rem 0; }
.sb-tip {
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--text-muted);
    line-height: 1.75;
    padding: 0.7rem 0.85rem;
    background: var(--bg-card);
    border-radius: 6px;
    border-left: 2px solid #00e5ff44;
}
/* Schema-aware mode badge on main area */
.schema-mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #00ff9d0d;
    border: 1px solid #00ff9d30;
    border-radius: 20px;
    padding: 3px 10px;
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--green);
    letter-spacing: 1px;
    margin-bottom: 0.8rem;
}
.schema-mode-badge .dot-g {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 5px var(--green);
}

/* ═══════════════ HERO HEADER ════════════════ */
.qp-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    position: relative;
}
.qp-logo {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.5rem;
}
.qp-logo-icon {
    font-size: 1.8rem;
    filter: drop-shadow(0 0 12px var(--accent));
    animation: pulse-icon 2.4s ease-in-out infinite;
}
@keyframes pulse-icon {
    0%, 100% { filter: drop-shadow(0 0 10px #00e5ff88); }
    50%       { filter: drop-shadow(0 0 22px #00e5ffcc); }
}
.qp-title {
    font-family: var(--display) !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #ffffff 30%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1 !important;
}
.qp-tagline {
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    color: var(--text-muted) !important;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.4rem !important;
}
.qp-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    margin: 1.6rem 0;
    opacity: 0.35;
}

/* ═══════════════ SECTION LABELS ═════════════ */
.qp-label {
    font-family: var(--mono) !important;
    font-size: 0.68rem !important;
    color: var(--accent) !important;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 0.5rem !important;
    display: flex;
    align-items: center;
    gap: 6px;
}
.qp-label::before {
    content: '';
    display: inline-block;
    width: 14px; height: 1px;
    background: var(--accent);
}

/* ═══════════════ TEXT AREA ══════════════════ */
.stTextArea textarea {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
    font-family: var(--display) !important;
    font-size: 0.95rem !important;
    padding: 14px 16px !important;
    resize: vertical !important;
    transition: border-color .25s, box-shadow .25s !important;
    caret-color: var(--accent) !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: var(--accent-glow) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: var(--text-muted) !important; }
.stTextArea label { display: none !important; }

/* ═══════════════ SELECTS ════════════════════ */
.stSelectbox > div > div {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
    font-size: 0.88rem !important;
}
.stSelectbox label { display: none !important; }
div[data-baseweb="select"] * { background-color: var(--bg-input) !important; }
div[data-baseweb="popover"] * {
    background-color: var(--bg-card) !important;
    border-color: var(--border) !important;
}

/* ═══════════════ GENERATE BUTTON ════════════ */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #00bcd4, #00e5ff) !important;
    color: #0a0c10 !important;
    font-family: var(--display) !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 1px;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: transform .15s, box-shadow .2s !important;
    box-shadow: 0 4px 20px #00e5ff33 !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 28px #00e5ff55 !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ═══════════════ SQL OUTPUT CARD ════════════ */
.sql-card {
    background: var(--bg-card);
    border: 1px solid var(--border-accent);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    position: relative;
    margin-top: 0.5rem;
    box-shadow: 0 4px 30px #00e5ff0a;
}
.sql-card pre {
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    line-height: 1.75 !important;
    color: #cdd6f4 !important;
    margin: 0 !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
}
.kw  { color: var(--accent);   font-weight: 700; }
.fn  { color: var(--green); }
.str { color: var(--yellow); }
.cmt { color: var(--text-muted); font-style: italic; }
.num { color: #f08080; }

.sql-status-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 1rem;
    padding-top: 0.8rem;
    border-top: 1px solid var(--border);
}
.sql-badge {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 5px;
}
.sql-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 6px var(--green);
}

/* ═══════════════ STATS ROW ══════════════════ */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}
.stat-chip {
    flex: 1;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.8rem;
    text-align: center;
}
.stat-chip .val {
    font-family: var(--mono);
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--accent);
}
.stat-chip .lbl {
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ═══════════════ ALERTS ═════════════════════ */
.qp-alert {
    border-radius: var(--radius);
    padding: 0.9rem 1.2rem;
    font-size: 0.85rem;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-top: 0.5rem;
    font-family: var(--mono);
}
.qp-alert-error {
    background: #ff4d6d15;
    border: 1px solid #ff4d6d44;
    color: #ff8fa3;
}
.qp-alert-warn {
    background: #ffd16615;
    border: 1px solid #ffd16644;
    color: #ffd166;
}
.qp-alert-info {
    background: var(--accent-dim);
    border: 1px solid var(--border-accent);
    color: var(--accent);
}
.qp-alert-missing-key {
    background: #12091f;
    border: 1px solid #7c3aed55;
    color: #c4b5fd;
    border-radius: var(--radius);
    padding: 1.3rem 1.5rem;
    font-size: 0.85rem;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-top: 1.5rem;
    font-family: var(--mono);
    line-height: 1.7;
    box-shadow: 0 0 30px #7c3aed18;
}
.qp-alert-missing-key strong { color: #e9d5ff; font-size: 0.9rem; }
.qp-alert-missing-key code {
    background: #2d1f4e;
    padding: 1px 6px;
    border-radius: 4px;
    font-size: 0.78rem;
    color: #a78bfa;
}
.qp-alert-missing-key pre {
    background: #0a0614;
    border: 1px solid #7c3aed33;
    border-radius: 6px;
    padding: 8px 14px;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: #ffd166;
    margin: 0.5rem 0 0.3rem;
    white-space: pre;
}
.qp-alert-icon { font-size: 1rem; flex-shrink: 0; }

/* ═══════════════ EXAMPLES PANEL ════════════ */
.example-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    margin-top: 0.5rem;
}

/* ═══════════════ HISTORY ITEM ══════════════ */
.history-item {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.8rem;
    color: var(--text-dim);
    font-family: var(--mono);
}
.history-item .hi-prompt {
    color: var(--text-primary);
    font-family: var(--display);
    font-size: 0.82rem;
    margin-bottom: 4px;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.history-item .hi-meta {
    color: var(--text-muted);
    font-size: 0.68rem;
    letter-spacing: 1px;
}

/* ═══════════════ FOOTER ═════════════════════ */
.qp-footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}
.qp-footer span {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ═══════════════ COPY BUTTON ════════════════ */
div[data-testid="stCopyButton"] button {
    background: var(--bg-hover) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-dim) !important;
    border-radius: 6px !important;
    font-size: 0.7rem !important;
}
div[data-testid="stCopyButton"] button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ═══════════════ SPINNER ════════════════════ */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ═══════════════ EXPANDER ═══════════════════ */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-dim) !important;
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
    letter-spacing: 1.5px !important;
}
.streamlit-expanderContent {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
}
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
    """
    Read uploaded .sql / .txt file.
    Returns: (raw_text, char_count, table_count)
    """
    raw = uploaded_file.read().decode("utf-8", errors="replace")
    # Estimate table count by counting CREATE TABLE occurrences
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
    """
    If a schema is loaded, prepend it as context and add strict column constraints.
    """
    if not schema_text:
        return prompt.strip()

    return f"""=== DATABASE SCHEMA ===
The following is the exact schema of the target database.
You MUST use ONLY the table names and column names defined here.
Do NOT invent, guess, or hallucinate any table or column that is not listed below.

{schema_text.strip()}

=== END OF SCHEMA ===

Now generate a {{}}-dialect SQL query for the following request.
Use exclusively the tables and columns from the schema above.

REQUEST: {prompt.strip()}"""


def generate_sql(
    prompt: str,
    api_key: str,
    dialect: str,
    style: str,
    model: str,
    schema_text: str | None = None,
) -> dict:
    """Call OpenAI and return {sql, tokens, elapsed}."""
    client  = openai.OpenAI(api_key=api_key)
    start   = time.time()
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
    <div class="sb-header">
        <span class="sb-header-icon">🗄️</span>
        <span class="sb-header-title">Schema Context</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sb-label">📂 Upload schema file</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "schema_upload",
        type=["sql", "txt"],
        accept_multiple_files=False,
        label_visibility="collapsed",
        help="Upload a .sql or .txt file containing your CREATE TABLE definitions.",
    )

    schema_text: str | None = None
    schema_meta: dict       = {}

    if uploaded_file is not None:
        try:
            raw, char_count, table_count = parse_schema_file(uploaded_file)

            # Guard: file too large (>80 KB is risky for context window)
            if char_count > 80_000:
                st.markdown("""
                <div class="qp-alert qp-alert-warn" style="font-size:.7rem;padding:.7rem .9rem;">
                    <span>⚠</span>
                    <span>Schema file exceeds 80 KB. Please trim unused tables to stay within context limits.</span>
                </div>""", unsafe_allow_html=True)
            else:
                schema_text = raw
                schema_meta = {
                    "name":   uploaded_file.name,
                    "tables": table_count,
                    "chars":  char_count,
                }

                # Preview card
                preview = raw[:900] + ("\n…" if len(raw) > 900 else "")
                st.markdown(f"""
                <div class="schema-card">
                    <pre>{preview}</pre>
                </div>
                <div class="schema-status">
                    <span class="dot-green"></span>
                    {table_count} table{'s' if table_count != 1 else ''} · {char_count:,} chars
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f"""
            <div class="qp-alert qp-alert-error" style="font-size:.7rem;padding:.7rem .9rem;">
                <span>✖</span>
                <span>Could not read file: {e}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <p class="schema-inactive">
            No schema loaded.<br>
            AI will use general knowledge<br>
            to infer table structures.
        </p>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-tip">
        💡 <strong>Tip:</strong> Export your schema with<br>
        <code>pg_dump --schema-only</code> (PostgreSQL)<br>
        or <code>SHOW CREATE TABLE</code> (MySQL) and paste into a .sql file.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# API KEY — secrets only
# ─────────────────────────────────────────────
resolved_api_key = st.secrets.get("OPENAI_API_KEY", "")

if not resolved_api_key:
    st.markdown("""
    <div class="qp-alert qp-alert-missing-key">
        <span class="qp-alert-icon">🔐</span>
        <div>
            <strong>API anahtarı bulunamadı.</strong><br>
            <span style="font-size:0.78rem;opacity:.8;">
                Projenizin <code>.streamlit/secrets.toml</code> dosyasına şu satırı ekleyin
                ve uygulamayı yeniden başlatın:
            </span>
            <pre>OPENAI_API_KEY = "sk-..."</pre>
            <span style="font-size:0.72rem;opacity:.6;">
                Streamlit Cloud kullanıyorsanız → App Settings › Secrets bölümüne ekleyin.
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="qp-header">
    <div class="qp-logo">
        <span class="qp-logo-icon">⚡</span>
        <h1 class="qp-title">Query Pulse AI</h1>
    </div>
    <p class="qp-tagline">Natural Language → Professional SQL</p>
</div>
<div class="qp-divider"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONFIGURATION ROW
# ─────────────────────────────────────────────
st.markdown('<p class="qp-label">⚙ Configuration</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    dialect = st.selectbox(
        "dialect",
        ["PostgreSQL", "MySQL", "SQLite", "SQL Server (T-SQL)", "BigQuery", "Snowflake"],
        key="dialect_select",
    )
with col2:
    style = st.selectbox(
        "style",
        ["Standard", "Annotated", "Compact"],
        key="style_select",
    )
with col3:
    model = st.selectbox(
        "model",
        ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
        key="model_select",
    )

st.markdown('<div class="qp-divider"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# EXAMPLE PROMPTS
# ─────────────────────────────────────────────
EXAMPLES = [
    ("📦", "Show the top 10 customers by total revenue in 2024"),
    ("📊", "Monthly active users grouped by country for the last 6 months"),
    ("🔍", "Find all orders that were delivered more than 3 days late"),
    ("🔗", "Products never purchased, joined with their category names"),
    ("📈", "Running total of sales per day using a window function"),
    ("⚠️",  "Duplicate email addresses in the users table"),
]

with st.expander("✦  Quick examples — click to load", expanded=False):
    cols = st.columns(2)
    for i, (icon, text) in enumerate(EXAMPLES):
        with cols[i % 2]:
            if st.button(f"{icon}  {text}", key=f"ex_{i}", use_container_width=True):
                st.session_state.last_prompt = text
                st.rerun()


# ─────────────────────────────────────────────
# SCHEMA MODE BADGE (only when schema loaded)
# ─────────────────────────────────────────────
if schema_text:
    st.markdown(f"""
    <div class="schema-mode-badge">
        <span class="dot-g"></span>
        Schema-Aware Mode · {schema_meta['name']} · {schema_meta['tables']} table{'s' if schema_meta['tables'] != 1 else ''}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PROMPT INPUT
# ─────────────────────────────────────────────
st.markdown('<p class="qp-label">✦ Natural Language Prompt</p>', unsafe_allow_html=True)

placeholder_with = (
    "e.g. → List all users who signed up last month but haven't placed an order yet.\n"
    "       AI will use only the columns defined in your uploaded schema."
)
placeholder_without = (
    "e.g. → List all users who signed up last month but haven't made a purchase yet,\n"
    "       grouped by their referral source and sorted by sign-up date…"
)

prompt = st.text_area(
    "prompt",
    value=st.session_state.last_prompt,
    height=110,
    placeholder=placeholder_with if schema_text else placeholder_without,
    key="prompt_input",
)

generate_clicked = st.button("⚡  Generate SQL", use_container_width=True)


# ─────────────────────────────────────────────
# GENERATE LOGIC
# ─────────────────────────────────────────────
if generate_clicked:
    if not prompt.strip():
        st.markdown("""
        <div class="qp-alert qp-alert-warn">
            <span class="qp-alert-icon">⚠</span>
            <span>Please enter a prompt before generating.</span>
        </div>""", unsafe_allow_html=True)
        st.stop()

    spinner_msg = "Generating schema-aware SQL…" if schema_text else "Generating SQL…"

    with st.spinner(spinner_msg):
        try:
            result = generate_sql(
                prompt=prompt,
                api_key=resolved_api_key,
                dialect=dialect,
                style=style,
                model=model,
                schema_text=schema_text,   # None → general mode
            )
        except openai.AuthenticationError:
            st.markdown("""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>Authentication failed.</strong> Your API key was rejected by OpenAI.</span>
            </div>""", unsafe_allow_html=True)
            st.stop()
        except openai.RateLimitError:
            st.markdown("""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>Rate limit exceeded.</strong> Try again shortly or upgrade your plan.</span>
            </div>""", unsafe_allow_html=True)
            st.stop()
        except openai.APIConnectionError:
            st.markdown("""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>Connection error.</strong> Could not reach the OpenAI API.</span>
            </div>""", unsafe_allow_html=True)
            st.stop()
        except openai.BadRequestError as e:
            st.markdown(f"""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>Bad request.</strong> {str(e)}</span>
            </div>""", unsafe_allow_html=True)
            st.stop()
        except Exception as e:
            st.markdown(f"""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>Unexpected error:</strong> {str(e)}</span>
            </div>""", unsafe_allow_html=True)
            st.stop()

    ok, err_msg = validate_result(result["sql"])
    if not ok:
        st.markdown(f"""
        <div class="qp-alert qp-alert-warn">
            <span class="qp-alert-icon">⚠</span>
            <span><strong>Model Notice:</strong> {err_msg}</span>
        </div>""", unsafe_allow_html=True)
        st.stop()

    # ── Store in history ──
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
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    st.markdown('<p class="qp-label">✦ Generated SQL</p>', unsafe_allow_html=True)

    schema_badge = (
        f'<span class="sql-badge" style="color:var(--green);">'
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
            <div style="display:flex;gap:1rem;align-items:center;">
                {schema_badge}
                <span class="sql-badge">{result['elapsed']}s · {result['tokens']} tokens</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.code(result["sql"], language="sql")

    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-chip">
            <div class="val">{st.session_state.query_count}</div>
            <div class="lbl">Total Queries</div>
        </div>
        <div class="stat-chip">
            <div class="val">{result['elapsed']}s</div>
            <div class="lbl">Response Time</div>
        </div>
        <div class="stat-chip">
            <div class="val">{st.session_state.total_tokens}</div>
            <div class="lbl">Tokens Used</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HISTORY PANEL
# ─────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="qp-divider"></div>', unsafe_allow_html=True)
    with st.expander(f"🕑  Query History  ({len(st.session_state.history)} entries)", expanded=False):
        for entry in st.session_state.history:
            schema_tag = f" · 🗄 {entry['schema_name']}" if entry.get("schema_name") and entry["schema_name"] != "—" else ""
            st.markdown(f"""
            <div class="history-item">
                <div class="hi-prompt">{entry['prompt']}</div>
                <div class="hi-meta">{entry['ts']} · {entry['dialect']}{schema_tag} · {entry['tokens']} tokens</div>
            </div>
            """, unsafe_allow_html=True)
            st.code(entry["sql"], language="sql")

        if st.button("🗑  Clear History", key="clear_history"):
            st.session_state.history      = []
            st.session_state.query_count  = 0
            st.session_state.total_tokens = 0
            st.rerun()


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="qp-footer">
    <span>Query Pulse AI &nbsp;·&nbsp; Powered by OpenAI &nbsp;·&nbsp; Built with Streamlit</span>
</div>
""", unsafe_allow_html=True)