"""
TURKCELL SQL AI — app.py  (Single-Page Enterprise UI · No Sidebar)
"""
import streamlit as st
import openai
import re, time, datetime, base64 as b64lib

_L = "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"
LOGO_SRC = f"data:image/png;base64,{_L}"

st.set_page_config(
    page_title="TURKCELL SQL AI",
    page_icon="🟡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Roboto+Mono:wght@400;500&display=swap');

:root {
  --navy:    #0047BA;
  --navy-dk: #002272;
  --navy-lt: #EBF3FF;
  --yel:     #FFD100;
  --yel-dk:  #C9A800;
  --text:    #1A202C;
  --muted:   #718096;
  --subtle:  #A0AEC0;
  --brd:     #E2E8F0;
  --white:   #FFFFFF;
  --ok:      #38A169;
  --sans:    'Inter', system-ui, sans-serif;
  --mono:    'Roboto Mono', monospace;
  --rad:     15px;
  --rad-s:   9px;
}

/* ── base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body {
  background: linear-gradient(170deg, #f8fbff 0%, #edf3fc 100%) !important;
  min-height: 100vh;
  font-family: var(--sans) !important;
}

.stApp,
.stApp > div,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section.main,
section.main > div,
.block-container { background: transparent !important; }

#MainMenu, footer, header { visibility: hidden !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: var(--navy); border-radius: 4px; }

/* ── centered 900px container ── */
.block-container {
  max-width: 900px !important;
  padding: 0 1rem 5rem !important;
  margin: 0 auto !important;
}

/* ── collapse sidebar toggle ── */
[data-testid="collapsedControl"] { display: none !important; }

/* ══════════════ HEADER ════════════════════════════════════════════════════ */
.hdr {
  background: linear-gradient(90deg, #001A5E 0%, #0047BA 100%);
  margin: 0 -1rem 2rem;
  padding: 0 2rem;
  height: 58px;
  display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 3px 14px rgba(0,30,110,.24);
  position: relative; overflow: hidden;
}
.hdr::after { content:""; position:absolute; inset:0; background:linear-gradient(90deg,transparent 60%,rgba(255,255,255,.04)); pointer-events:none; }
.hdr-left { display:flex; align-items:center; gap:13px; z-index:1; }
.hdr-logo { height:32px; width:auto; display:block; background:rgba(255,255,255,.95); border-radius:7px; padding:3px 9px; }
.hdr-vline { width:1px; height:22px; background:rgba(255,255,255,.25); }
.hdr-title { font-size:1.02rem; font-weight:800; color:#fff; letter-spacing:.4px; line-height:1.2; }
.hdr-sub   { font-size:.53rem; color:rgba(255,255,255,.45); letter-spacing:2px; text-transform:uppercase; margin-top:2px; }
.hdr-pill  { z-index:1; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.22); border-radius:20px; padding:4px 14px; font-size:.58rem; font-weight:600; color:rgba(255,255,255,.78); letter-spacing:.9px; text-transform:uppercase; }

/* ══════════════ CARDS ═════════════════════════════════════════════════════ */
.card {
  background: var(--white);
  border: 1px solid var(--brd);
  border-radius: var(--rad);
  box-shadow: 0 4px 24px rgba(0,0,0,.06), 0 1px 4px rgba(0,71,186,.04);
  padding: 1.6rem 1.8rem;
  margin-bottom: 1.1rem;
}
.upload-card {
  background: linear-gradient(135deg, #EBF3FF 0%, #dceeff 100%);
  border: 1.5px dashed rgba(0,71,186,.30);
  border-radius: var(--rad);
  padding: 1.4rem 1.8rem;
  margin-bottom: 1.1rem;
  transition: border-color .2s, background .2s;
}
.upload-card:hover { border-color: var(--navy); }
.upload-card-title {
  font-size: .72rem; font-weight: 700; color: var(--navy-dk);
  letter-spacing: 1.5px; text-transform: uppercase;
  display: flex; align-items: center; gap: 7px;
  margin-bottom: .85rem;
}
.upload-card-title::before { content:""; width:3px; height:13px; background:var(--yel); border-radius:2px; flex-shrink:0; }

.schema-ok { display:flex; align-items:center; gap:7px; margin-top:.7rem; font-size:.70rem; font-weight:600; color:var(--ok); }
.schema-ok .dot { width:7px; height:7px; border-radius:50%; background:var(--ok); flex-shrink:0; }
.schema-prev { background:#fff; border:1px solid var(--brd); border-left:3px solid var(--yel); border-radius:var(--rad-s); padding:.65rem .85rem; margin-top:.65rem; max-height:160px; overflow-y:auto; }
.schema-prev pre { font-family:var(--mono) !important; font-size:.63rem !important; line-height:1.7 !important; color:var(--text) !important; margin:0 !important; white-space:pre-wrap !important; word-break:break-word !important; }

/* ══════════════ SECTION LABELS ════════════════════════════════════════════ */
.lbl { font-size:.63rem; font-weight:700; color:var(--navy-dk); letter-spacing:1.8px; text-transform:uppercase; margin-bottom:.55rem; display:flex; align-items:center; gap:7px; }
.lbl::before { content:""; width:3px; height:13px; background:var(--yel); border-radius:2px; flex-shrink:0; }
.card-sep { height:1px; background:#F0F4FA; margin:1.25rem 0; }

/* ══════════════ WIDGETS ═══════════════════════════════════════════════════ */
/* file uploader */
[data-testid="stFileUploader"] { background: transparent !important; border: none !important; }
[data-testid="stFileUploader"] label { display:none !important; }
[data-testid="stFileUploaderDropzone"] {
  background: rgba(255,255,255,.70) !important;
  border: 1.5px dashed rgba(0,71,186,.30) !important;
  border-radius: var(--rad-s) !important;
  transition: border-color .2s, background .2s !important;
}
[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--navy) !important; background: #fff !important; }
[data-testid="stFileUploaderDropzoneInstructions"] span { color: var(--muted) !important; font-size:.75rem !important; }
[data-testid="stFileUploaderDropzone"] small { color: var(--subtle) !important; font-size:.62rem !important; }

/* selects */
.stSelectbox label { font-size:.62rem !important; font-weight:700 !important; color:var(--muted) !important; text-transform:uppercase !important; letter-spacing:.9px !important; }
.stSelectbox > div > div { background:#FAFCFF !important; border:1.5px solid var(--brd) !important; border-radius:var(--rad-s) !important; font-family:var(--sans) !important; font-size:.84rem !important; color:var(--text) !important; transition:border-color .18s !important; }
.stSelectbox > div > div:focus-within { border-color:var(--navy) !important; box-shadow:0 0 0 3px rgba(0,71,186,.10) !important; }
div[data-baseweb="select"] *  { background:#fff !important; color:var(--text) !important; }
div[data-baseweb="popover"] * { background:#fff !important; border-color:var(--brd) !important; color:var(--text) !important; }

/* textarea */
.stTextArea label { display:none !important; }
.stTextArea textarea { background:#FAFCFF !important; border:1.5px solid var(--brd) !important; border-radius:var(--rad-s) !important; font-family:var(--sans) !important; font-size:.88rem !important; line-height:1.65 !important; color:var(--text) !important; padding:12px 14px !important; resize:vertical !important; transition:border-color .18s, box-shadow .18s !important; }
.stTextArea textarea:focus { border-color:var(--navy) !important; background:#fff !important; box-shadow:0 0 0 3px rgba(0,71,186,.10) !important; outline:none !important; }
.stTextArea textarea::placeholder { color:var(--subtle) !important; }

/* button */
.stButton > button {
  background: var(--yel) !important; color: #001A5E !important;
  font-family: var(--sans) !important; font-weight: 700 !important;
  font-size: .9rem !important; border: none !important;
  border-radius: var(--rad-s) !important;
  padding: .68rem 2.8rem !important;
  cursor: pointer !important;
  transition: background .15s, box-shadow .15s, transform .10s !important;
  box-shadow: 0 3px 14px rgba(255,209,0,.32) !important;
  display: block !important; margin: .55rem auto 0 !important;
}
.stButton > button:hover  { background:var(--yel-dk) !important; box-shadow:0 5px 22px rgba(200,168,0,.40) !important; transform:translateY(-1px) !important; }
.stButton > button:active { transform:translateY(0) !important; }

/* ══════════════ SQL CARD (dark) ═══════════════════════════════════════════ */
.sql-card {
  background: #1E2433;
  border: 1px solid #2D3448;
  border-radius: var(--rad);
  padding: 1.3rem 1.5rem 1.1rem;
  box-shadow: 0 6px 28px rgba(0,0,0,.18);
  margin-top: .5rem;
}
.sql-card pre { font-family:var(--mono) !important; font-size:.80rem !important; line-height:1.80 !important; color:#CDD6F4 !important; margin:0 !important; white-space:pre-wrap !important; word-break:break-word !important; }
.kw  { color:#89DCEB; font-weight:700; }
.fn  { color:#A6E3A1; }
.str { color:#F38BA8; }
.cmt { color:#6C7086; font-style:italic; }
.num { color:#CBA6F7; }
.sql-bar { display:flex; align-items:center; justify-content:space-between; margin-top:.9rem; padding-top:.75rem; border-top:1px solid #2D3448; }
.sql-tag { display:inline-flex; align-items:center; gap:5px; background:rgba(137,220,235,.12); border-radius:20px; padding:3px 10px; font-size:.61rem; font-weight:600; color:#89DCEB; }
.sql-tag .dot { width:6px; height:6px; border-radius:50%; background:#A6E3A1; }

/* download */
.dl { margin-top:.75rem; }
.dl a { display:inline-flex; align-items:center; gap:6px; background:var(--navy-lt); border:1.5px solid var(--navy); border-radius:var(--rad-s); padding:.42rem 1rem; font-size:.76rem; font-weight:600; color:var(--navy); text-decoration:none; transition:background .15s, color .15s; }
.dl a:hover { background:var(--navy); color:#fff; }

/* stats */
.stats { display:flex; gap:.7rem; margin-top:.9rem; }
.stat { flex:1; background:var(--white); border:1px solid var(--brd); border-radius:var(--rad-s); padding:.8rem; text-align:center; box-shadow:0 1px 5px rgba(0,71,186,.04); transition:box-shadow .18s, transform .15s; }
.stat:hover { box-shadow:0 4px 14px rgba(0,71,186,.10); transform:translateY(-1px); }
.stat .v { font-size:1.15rem; font-weight:800; color:var(--navy); }
.stat .l { font-size:.58rem; font-weight:700; color:var(--muted); letter-spacing:.8px; text-transform:uppercase; margin-top:2px; }

/* alerts */
.alert { background:var(--white); border-left:4px solid var(--navy); border:1px solid #BEE3F8; border-left:4px solid var(--navy); border-radius:var(--rad); padding:1.2rem 1.4rem; margin-top:1rem; box-shadow:0 2px 10px rgba(0,71,186,.07); font-family:var(--sans); }
.alert.warn { border-left-color:#D69E2E; border-color:#FAF089; }
.alert.info { border-left-color:var(--ok); border-color:#C6F6D5; }
.alert-h { display:flex; align-items:center; gap:10px; margin-bottom:.55rem; }
.alert-ic { width:30px; height:30px; border-radius:8px; background:var(--navy-lt); display:flex; align-items:center; justify-content:center; font-size:.85rem; flex-shrink:0; }
.alert.warn .alert-ic { background:#FEFCBF; }
.alert.info .alert-ic { background:#F0FFF4; }
.alert-title { font-size:.86rem; font-weight:700; color:var(--navy-dk); }
.alert.warn .alert-title { color:#744210; }
.alert.info .alert-title { color:#276749; }
.alert-body { font-size:.80rem; color:var(--muted); line-height:1.65; padding-left:40px; }
.alert-body code { background:var(--navy-lt); padding:1px 5px; border-radius:4px; font-family:var(--mono); font-size:.74rem; color:var(--navy); }
.alert-body pre  { background:#F8FAFF; border:1px solid #BEE3F8; border-radius:6px; padding:7px 11px; font-family:var(--mono); font-size:.74rem; color:var(--navy-dk); margin:.45rem 0 .15rem; }

/* schema badge */
.sbadge { display:inline-flex; align-items:center; gap:6px; background:rgba(56,161,105,.09); border:1px solid rgba(56,161,105,.26); border-radius:20px; padding:3px 12px; font-size:.62rem; font-weight:600; color:var(--ok); margin-bottom:.65rem; }
.sbadge .dg { width:6px; height:6px; border-radius:50%; background:var(--ok); }

/* expander */
.streamlit-expanderHeader { background:rgba(255,255,255,.90) !important; border:1px solid var(--brd) !important; border-radius:var(--rad-s) !important; font-family:var(--sans) !important; font-size:.75rem !important; font-weight:600 !important; color:var(--muted) !important; }
.streamlit-expanderContent { background:rgba(255,255,255,.93) !important; border:1px solid var(--brd) !important; border-top:none !important; }

/* history */
.hi { background:var(--white); border:1px solid var(--brd); border-left:3px solid var(--yel); border-radius:var(--rad-s); padding:.7rem .95rem; margin-bottom:.4rem; box-shadow:0 1px 4px rgba(0,71,186,.04); }
.hi .hp { font-size:.80rem; font-weight:500; color:var(--text); margin-bottom:2px; display:-webkit-box; -webkit-line-clamp:1; -webkit-box-orient:vertical; overflow:hidden; }
.hi .hm { font-size:.61rem; color:var(--subtle); }

/* code */
.stCodeBlock { border:1px solid #2D3448 !important; border-radius:var(--rad-s) !important; }
.stCodeBlock pre { background:#1E2433 !important; font-family:var(--mono) !important; font-size:.78rem !important; color:#CDD6F4 !important; }
div[data-testid="stCopyButton"] button { background:rgba(137,220,235,.12) !important; border:1px solid rgba(137,220,235,.25) !important; color:#89DCEB !important; border-radius:5px !important; font-size:.66rem !important; }
div[data-testid="stCopyButton"] button:hover { background:#89DCEB !important; color:#1E2433 !important; }

.stSpinner > div { border-top-color:var(--navy) !important; }
.pdiv { height:1px; background:var(--brd); margin:1.2rem 0; opacity:.45; }

/* footer */
.foot { text-align:center; margin-top:3rem; padding:1rem 0 .5rem; border-top:1px solid var(--brd); }
.foot p { font-family:var(--sans); font-size:.60rem; color:var(--subtle); letter-spacing:.5px; margin:0; }
.foot p+p { margin-top:.2rem; }
.foot strong { color:var(--muted); font-weight:600; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
for k, v in [("history", []), ("qc", 0), ("tt", 0), ("lp", "")]:
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────
SQL_KW = [
    "SELECT","FROM","WHERE","JOIN","LEFT JOIN","RIGHT JOIN","INNER JOIN",
    "FULL OUTER JOIN","ON","GROUP BY","ORDER BY","HAVING","LIMIT","OFFSET",
    "INSERT INTO","VALUES","UPDATE","SET","DELETE","CREATE TABLE","ALTER TABLE",
    "DROP TABLE","WITH","AS","AND","OR","NOT","IN","BETWEEN","LIKE",
    "IS NULL","IS NOT NULL","DISTINCT","UNION","UNION ALL","INTERSECT","EXCEPT",
    "CASE","WHEN","THEN","ELSE","END","ASC","DESC","COALESCE","NULLIF","CAST",
    "OVER","PARTITION BY","ROW_NUMBER","RANK","DENSE_RANK","LAG","LEAD",
]

def hl(sql):
    for kw in sorted(SQL_KW, key=len, reverse=True):
        sql = re.compile(rf"\b({re.escape(kw)})\b", re.I).sub(
            r'<span class="kw">\1</span>', sql)
    return sql

def parse_schema(f):
    raw = f.read().decode("utf-8", errors="replace")
    return raw, len(raw), len(re.findall(r"\bCREATE\s+TABLE\b", raw, re.I))

def sys_prompt(dialect, style):
    sm = {
        "Standard":  "Uppercase keywords, clean multi-line formatting.",
        "Compact":   "Compact, minimal whitespace.",
        "Annotated": "Add a brief comment above each major clause.",
    }
    return (
        f"You are TURKCELL SQL AI, expert in {dialect}.\n"
        f"Output ONLY valid {dialect} SQL — no markdown fences, no prose.\n"
        f"{sm.get(style, '')} Use CTEs for complex queries. End with semicolon.\n"
        f"If not a valid SQL request reply exactly: ERROR: Not a valid SQL request."
    )

def user_msg(prompt, schema):
    if not schema:
        return prompt.strip()
    return (
        f"=== SCHEMA ===\n{schema.strip()}\n=== END ===\n"
        f"Use ONLY these tables/columns.\nREQUEST: {prompt.strip()}"
    )

def run_sql(prompt, key, dialect, style, model, schema=None):
    t0 = time.time()
    r = openai.OpenAI(api_key=key).chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": sys_prompt(dialect, style)},
            {"role": "user",   "content": user_msg(prompt, schema)},
        ],
        temperature=0.2, max_tokens=1400,
    )
    return {
        "sql":     r.choices[0].message.content.strip(),
        "tokens":  r.usage.total_tokens,
        "elapsed": round(time.time() - t0, 2),
    }

def chk(sql):
    if sql.startswith("ERROR:"):
        return False, sql[6:].strip()
    if len(sql) < 10:
        return False, "Model returned an unexpectedly short response."
    return True, ""

def dl(sql):
    enc = b64lib.b64encode(sql.encode()).decode()
    ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return (
        f'<div class="dl"><a href="data:file/sql;base64,{enc}" '
        f'download="query_{ts}.sql">📥 Download SQL</a></div>'
    )

def mk_alert(icon, title, body, v=""):
    return (
        f'<div class="alert {v}">'
        f'<div class="alert-h"><div class="alert-ic">{icon}</div>'
        f'<div class="alert-title">{title}</div></div>'
        f'<div class="alert-body">{body}</div></div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
#  API KEY
# ─────────────────────────────────────────────────────────────────────────────
api_key = st.secrets.get("OPENAI_API_KEY", "")
if not api_key:
    # show header first so page isn't completely blank
    st.markdown(
        f'<div class="hdr">'
        f'<div class="hdr-left">'
        f'  <img class="hdr-logo" src="{LOGO_SRC}" alt="logo">'
        f'  <div class="hdr-vline"></div>'
        f'  <div><div class="hdr-title">TURKCELL SQL AI</div>'
        f'  <div class="hdr-sub">Natural Language → SQL</div></div>'
        f'</div>'
        f'<div class="hdr-pill">Powered by OpenAI</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        mk_alert("🔐", "API Key Not Found",
                 'Add your OpenAI key to <code>.streamlit/secrets.toml</code>:'
                 '<pre>OPENAI_API_KEY = "sk-..."</pre>'
                 'Streamlit Cloud → <strong>App Settings › Secrets</strong>'),
        unsafe_allow_html=True,
    )
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    f'<div class="hdr">'
    f'<div class="hdr-left">'
    f'  <img class="hdr-logo" src="{LOGO_SRC}" alt="logo">'
    f'  <div class="hdr-vline"></div>'
    f'  <div><div class="hdr-title">TURKCELL SQL AI</div>'
    f'  <div class="hdr-sub">Natural Language → SQL</div></div>'
    f'</div>'
    f'<div class="hdr-pill">Powered by OpenAI</div></div>',
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
#  1. SCHEMA UPLOAD CARD  (top of main page)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="upload-card">'
    '<div class="upload-card-title">'
    '📂 Upload Your Database Schema (.sql, .txt)'
    '</div>',
    unsafe_allow_html=True,
)

uf = st.file_uploader(
    "schema_file",
    type=["sql", "txt"],
    accept_multiple_files=False,
    label_visibility="collapsed",
    help="Upload a .sql or .txt file containing CREATE TABLE statements.",
)

schema_text, schema_meta = None, {}

if uf:
    try:
        raw, chars, tables = parse_schema(uf)
        if chars > 80_000:
            st.markdown(
                mk_alert("⚠️", "File Too Large",
                         "Schema exceeds 80 KB. Remove unused tables.", "warn"),
                unsafe_allow_html=True,
            )
        else:
            schema_text = raw
            schema_meta = {"name": uf.name, "tables": tables, "chars": chars}
            prev = raw[:600] + ("\n…" if len(raw) > 600 else "")
            st.markdown(
                f'<div class="schema-ok"><span class="dot"></span>'
                f'<strong>{uf.name}</strong> loaded — {tables} tables · {chars:,} chars</div>'
                f'<div class="schema-prev"><pre>{prev}</pre></div>',
                unsafe_allow_html=True,
            )
    except Exception as e:
        st.markdown(mk_alert("❌", "File Error", f"Could not read: {e}"), unsafe_allow_html=True)
else:
    st.markdown(
        mk_alert("ℹ️", "No Schema — Using General Knowledge",
                 "AI will infer table/column names from your description. "
                 "Upload a schema file above for more accurate results.", "info"),
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)   # /upload-card


# ─────────────────────────────────────────────────────────────────────────────
#  2. CONFIG + PROMPT CARD
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)

# ── Configuration ─────────────────────────────────────────────────────────────
st.markdown('<p class="lbl">⚙ Configuration</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    dialect = st.selectbox(
        "Dialect",
        ["PostgreSQL", "MySQL", "SQLite", "SQL Server (T-SQL)", "BigQuery", "Snowflake"],
        key="d",
    )
with c2:
    style = st.selectbox("Style", ["Standard", "Annotated", "Compact"], key="s")
with c3:
    model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"], key="m")

st.markdown('<div class="card-sep"></div>', unsafe_allow_html=True)

# ── Schema badge ──────────────────────────────────────────────────────────────
if schema_text:
    st.markdown(
        f'<div class="sbadge"><span class="dg"></span>'
        f'Schema Mode Active · {schema_meta["name"]} · {schema_meta["tables"]} tables</div>',
        unsafe_allow_html=True,
    )

# ── Prompt ────────────────────────────────────────────────────────────────────
st.markdown('<p class="lbl">✦ Describe in Natural Language</p>', unsafe_allow_html=True)
prompt = st.text_area(
    "p",
    value=st.session_state.lp,
    height=130,
    placeholder=(
        "e.g. → List users who signed up last month but haven't placed an order yet, "
        "grouped by referral source, sorted by registration date…"
    ),
    key="pk",
    label_visibility="collapsed",
)

go = st.button("⚡  Generate SQL", key="go")

st.markdown('</div>', unsafe_allow_html=True)   # /card


# ─────────────────────────────────────────────────────────────────────────────
#  GENERATE
# ─────────────────────────────────────────────────────────────────────────────
if go:
    st.session_state.lp = prompt

    if not prompt.strip():
        st.markdown(
            mk_alert("✏️", "Empty Prompt",
                     "Please enter a description before generating.", "warn"),
            unsafe_allow_html=True,
        )
        st.stop()

    with st.spinner("Generating SQL…"):
        try:
            res = run_sql(prompt, api_key, dialect, style, model, schema_text)
        except openai.AuthenticationError:
            st.markdown(mk_alert("🔑", "Authentication Error",
                "API key rejected. Verify it is valid and active."),
                unsafe_allow_html=True); st.stop()
        except openai.RateLimitError:
            st.markdown(mk_alert("⏱", "Rate Limit Exceeded",
                "OpenAI quota reached. Wait and try again."),
                unsafe_allow_html=True); st.stop()
        except openai.APIConnectionError:
            st.markdown(mk_alert("🌐", "Connection Error",
                "Could not reach the OpenAI API. Check your internet connection."),
                unsafe_allow_html=True); st.stop()
        except Exception as e:
            st.markdown(mk_alert("⚙️", "Unexpected Error",
                f"Something went wrong:<br><code>{e}</code>"),
                unsafe_allow_html=True); st.stop()

    valid, err = chk(res["sql"])
    if not valid:
        st.markdown(mk_alert("⚠️", "Model Notice", err, "warn"),
            unsafe_allow_html=True); st.stop()

    # store
    st.session_state.qc += 1
    st.session_state.tt += res["tokens"]
    st.session_state.history.insert(0, {
        "prompt":  prompt,
        "sql":     res["sql"],
        "dialect": dialect,
        "ts":      datetime.datetime.now().strftime("%d %b %Y %H:%M"),
        "tokens":  res["tokens"],
        "schema":  schema_meta.get("name", "—") if schema_text else "—",
    })
    st.session_state.history = st.session_state.history[:30]

    # ── dark SQL card ─────────────────────────────────────────────────────────
    sb = ""
    if schema_text:
        sb = (
            f'<span class="sql-tag" style="background:rgba(166,227,161,.12);color:#A6E3A1;">'
            f'<span class="dot" style="background:#A6E3A1"></span>'
            f'{schema_meta["name"]}</span>'
        )

    st.markdown(
        f'<div class="sql-card">'
        f'<pre>{hl(res["sql"])}</pre>'
        f'<div class="sql-bar">'
        f'<span class="sql-tag"><span class="dot"></span>{dialect}</span>'
        f'<div style="display:flex;gap:.5rem;align-items:center;">{sb}'
        f'<span class="sql-tag">{res["elapsed"]}s · {res["tokens"]} tokens</span>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    st.code(res["sql"], language="sql")
    st.markdown(dl(res["sql"]), unsafe_allow_html=True)

    # stats
    st.markdown(
        f'<div class="stats">'
        f'<div class="stat"><div class="v">{st.session_state.qc}</div><div class="l">Queries</div></div>'
        f'<div class="stat"><div class="v">{res["elapsed"]}s</div><div class="l">Response</div></div>'
        f'<div class="stat"><div class="v">{st.session_state.tt}</div><div class="l">Tokens</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
#  QUERY HISTORY
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="pdiv"></div>', unsafe_allow_html=True)
    with st.expander(
        f"📜  Query History  ({len(st.session_state.history)} records)",
        expanded=False,
    ):
        for i, e in enumerate(st.session_state.history):
            tag = f" · 🗄 {e['schema']}" if e.get("schema") and e["schema"] != "—" else ""
            st.markdown(
                f'<div class="hi">'
                f'<div class="hp">{e["prompt"]}</div>'
                f'<div class="hm">{e["ts"]} · {e["dialect"]}{tag} · {e["tokens"]} tokens</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.code(e["sql"], language="sql")
            st.markdown(dl(e["sql"]), unsafe_allow_html=True)
            if i < len(st.session_state.history) - 1:
                st.markdown('<div style="height:.2rem"></div>', unsafe_allow_html=True)

        st.markdown('<div style="height:.3rem"></div>', unsafe_allow_html=True)
        if st.button("🗑  Clear History", key="clr"):
            st.session_state.update({"history": [], "qc": 0, "tt": 0})
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────────────────
yr = datetime.datetime.now().year
st.markdown(
    f'<div class="foot">'
    f'<p>© {yr} <strong>TURKCELL SQL AI</strong> | L2 DevOps Operations</p>'
    f'<p>Powered by OpenAI · Streamlit · All rights reserved.</p>'
    f'</div>',
    unsafe_allow_html=True,
)