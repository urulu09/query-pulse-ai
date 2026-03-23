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

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Query Pulse AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
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

/* ═══════════════ API KEY INPUT ══════════════ */
.stTextInput input {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    letter-spacing: 1px;
    transition: border-color .25s !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: var(--accent-glow) !important;
}
.stTextInput label { display: none !important; }

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
/* SQL syntax highlight via spans */
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
.qp-alert-icon { font-size: 1rem; flex-shrink: 0; }

/* ═══════════════ EXAMPLES PANEL ════════════ */
.example-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    margin-top: 0.5rem;
}
.example-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.7rem 0.9rem;
    font-size: 0.78rem;
    color: var(--text-dim);
    cursor: pointer;
    transition: border-color .2s, color .2s;
    font-family: var(--display);
}
.example-card:hover {
    border-color: var(--accent);
    color: var(--text-primary);
}
.example-card .ex-icon { margin-right: 5px; }

/* ═══════════════ SIDEBAR TOGGLE ════════════ */
.config-row {
    display: flex;
    gap: 0.8rem;
    align-items: stretch;
}
.config-row > div { flex: 1; }

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

/* ═══════════════ SPINNER OVERRIDE ══════════ */
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
    st.session_state.history = []          # list of {prompt, sql, dialect, ts}
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
    """Minimal keyword highlighting via HTML spans."""
    # Sort by length desc so longer keywords match first
    for kw in sorted(SQL_KEYWORDS, key=len, reverse=True):
        pattern = re.compile(rf'\b({re.escape(kw)})\b', re.IGNORECASE)
        sql = pattern.sub(r'<span class="kw">\1</span>', sql)
    return sql


def build_system_prompt(dialect: str, style: str) -> str:
    style_instructions = {
        "Standard": "Use standard, clean SQL formatting with uppercase keywords.",
        "Compact":  "Return compact SQL without extra newlines, suitable for inline use.",
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
8. If the request is ambiguous, make the most reasonable assumption and proceed — do NOT ask for clarification.
9. If the request cannot be converted to SQL (e.g. it is totally unrelated), reply with exactly: ERROR: Not a valid SQL request.

Dialect-specific notes:
- PostgreSQL: Use ILIKE for case-insensitive search, EXTRACT() for dates, $1/$2 for parameterised queries.
- MySQL: Use LIKE for strings, DATE_FORMAT(), IFNULL().
- SQLite: Minimalist functions; use strftime() for dates.
- SQL Server (T-SQL): Use TOP instead of LIMIT, GETDATE() for current timestamp, square bracket identifiers.
- BigQuery: Use backtick identifiers, SAFE_DIVIDE(), TIMESTAMP functions, ARRAY/STRUCT types if needed.
- Snowflake: Use QUALIFY for window-filtered rows, IFF() for inline conditionals, FLATTEN for semi-structured data.
"""


def generate_sql(prompt: str, api_key: str, dialect: str, style: str, model: str) -> dict:
    """Call OpenAI and return {sql, tokens, elapsed}."""
    client = openai.OpenAI(api_key=api_key)
    start = time.time()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": build_system_prompt(dialect, style)},
            {"role": "user",   "content": prompt.strip()},
        ],
        temperature=0.2,
        max_tokens=1200,
    )

    elapsed = round(time.time() - start, 2)
    sql     = response.choices[0].message.content.strip()
    tokens  = response.usage.total_tokens

    return {"sql": sql, "tokens": tokens, "elapsed": elapsed}


def validate_result(sql: str) -> tuple[bool, str]:
    """Basic sanity checks on the returned SQL."""
    if sql.startswith("ERROR:"):
        return False, sql.replace("ERROR:", "").strip()
    if len(sql) < 10:
        return False, "Model returned an unexpectedly short response."
    return True, ""


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

st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
st.markdown('<p class="qp-label">🔑 OpenAI API Key</p>', unsafe_allow_html=True)
api_key_input = st.text_input("api_key", type="password", placeholder="sk-…  (stored only in session memory)", key="api_key_field")

# Resolve API key: input field → env variable fallback
import os
resolved_api_key = api_key_input.strip() or os.environ.get("OPENAI_API_KEY", "")

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
# PROMPT INPUT
# ─────────────────────────────────────────────
st.markdown('<p class="qp-label">✦ Natural Language Prompt</p>', unsafe_allow_html=True)

prompt = st.text_area(
    "prompt",
    value=st.session_state.last_prompt,
    height=110,
    placeholder=(
        "e.g. → List all users who signed up last month but haven't made a purchase yet,\n"
        "       grouped by their referral source and sorted by sign-up date…"
    ),
    key="prompt_input",
)

generate_clicked = st.button("⚡  Generate SQL", use_container_width=True)


# ─────────────────────────────────────────────
# GENERATE LOGIC
# ─────────────────────────────────────────────
if generate_clicked:
    # ── Input guards ──────────────────────────
    if not prompt.strip():
        st.markdown("""
        <div class="qp-alert qp-alert-warn">
            <span class="qp-alert-icon">⚠</span>
            <span>Please enter a prompt before generating.</span>
        </div>""", unsafe_allow_html=True)
        st.stop()

    if not resolved_api_key:
        st.markdown("""
        <div class="qp-alert qp-alert-error">
            <span class="qp-alert-icon">✖</span>
            <span>No API key found. Enter your OpenAI key above or set the <code>OPENAI_API_KEY</code> environment variable.</span>
        </div>""", unsafe_allow_html=True)
        st.stop()

    if not resolved_api_key.startswith("sk-"):
        st.markdown("""
        <div class="qp-alert qp-alert-warn">
            <span class="qp-alert-icon">⚠</span>
            <span>API key format looks incorrect — OpenAI keys typically start with <code>sk-</code>.</span>
        </div>""", unsafe_allow_html=True)
        st.stop()

    # ── Call API ──────────────────────────────
    with st.spinner("Generating SQL…"):
        try:
            result = generate_sql(
                prompt=prompt,
                api_key=resolved_api_key,
                dialect=dialect,
                style=style,
                model=model,
            )
        except openai.AuthenticationError:
            st.markdown("""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>Authentication failed.</strong> Your API key was rejected by OpenAI. Please check that it is valid and active.</span>
            </div>""", unsafe_allow_html=True)
            st.stop()

        except openai.RateLimitError:
            st.markdown("""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>Rate limit exceeded.</strong> Your OpenAI quota has been reached. Try again shortly or upgrade your plan.</span>
            </div>""", unsafe_allow_html=True)
            st.stop()

        except openai.APIConnectionError:
            st.markdown("""
            <div class="qp-alert qp-alert-error">
                <span class="qp-alert-icon">✖</span>
                <span><strong>Connection error.</strong> Could not reach the OpenAI API. Check your internet connection and try again.</span>
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

    # ── Validate ──────────────────────────────
    ok, err_msg = validate_result(result["sql"])
    if not ok:
        st.markdown(f"""
        <div class="qp-alert qp-alert-warn">
            <span class="qp-alert-icon">⚠</span>
            <span><strong>Model Notice:</strong> {err_msg}</span>
        </div>""", unsafe_allow_html=True)
        st.stop()

    # ── Success: store + render ───────────────
    st.session_state.query_count  += 1
    st.session_state.total_tokens += result["tokens"]

    import datetime
    st.session_state.history.insert(0, {
        "prompt":  prompt,
        "sql":     result["sql"],
        "dialect": dialect,
        "ts":      datetime.datetime.now().strftime("%H:%M:%S"),
        "tokens":  result["tokens"],
    })

    # Keep last 20 entries
    st.session_state.history = st.session_state.history[:20]

    # ── Output Section ────────────────────────
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    st.markdown('<p class="qp-label">✦ Generated SQL</p>', unsafe_allow_html=True)

    highlighted = highlight_sql(result["sql"])
    st.markdown(f"""
    <div class="sql-card">
        <pre>{highlighted}</pre>
        <div class="sql-status-bar">
            <span class="sql-badge">
                <span class="dot"></span>
                {dialect}
            </span>
            <span class="sql-badge">{result['elapsed']}s · {result['tokens']} tokens</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Copy button (native Streamlit)
    st.code(result["sql"], language="sql")

    # Stats chips
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
            st.markdown(f"""
            <div class="history-item">
                <div class="hi-prompt">{entry['prompt']}</div>
                <div class="hi-meta">{entry['ts']} · {entry['dialect']} · {entry['tokens']} tokens</div>
            </div>
            """, unsafe_allow_html=True)
            st.code(entry["sql"], language="sql")

        if st.button("🗑  Clear History", key="clear_history"):
            st.session_state.history     = []
            st.session_state.query_count = 0
            st.session_state.total_tokens= 0
            st.rerun()


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="qp-footer">
    <span>Query Pulse AI &nbsp;·&nbsp; Powered by OpenAI &nbsp;·&nbsp; Built with Streamlit</span>
</div>
""", unsafe_allow_html=True)