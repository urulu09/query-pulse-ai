"""
TURKCELL SQL AI — app.py  (Enterprise UI · Final)
"""

import streamlit as st
import openai
import re, time, datetime, base64 as b64lib

# ── embedded logo ─────────────────────────────────────────────────────────────
_LOGO_B64 = "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"
LOGO_SRC  = f"data:image/png;base64,{_LOGO_B64}"

# ── page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="TURKCELL SQL AI",
    page_icon="🟡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>

/* 1. FONTS ----------------------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Roboto+Mono:wght@400;500&display=swap');

/* 2. DESIGN TOKENS --------------------------------------------------------- */
:root {
  --navy:     #0047BA;
  --navy-dk:  #002272;
  --navy-lt:  #EBF3FF;
  --yellow:   #FFD100;
  --yel-dk:   #C9A800;
  --text:     #1A202C;
  --muted:    #718096;
  --subtle:   #A0AEC0;
  --brd:      #E2E8F0;
  --white:    #FFFFFF;
  --ok:       #38A169;
  --sans:     'Inter', system-ui, sans-serif;
  --mono:     'Roboto Mono', monospace;
  --r:        15px;
  --r-sm:     8px;
}

/* 3. GLOBAL RESET ---------------------------------------------------------- */
*, *::before, *::after { box-sizing: border-box; }

html, body {
  background: linear-gradient(180deg, #FFFFFF 0%, #F0F2F6 100%) !important;
  min-height: 100vh;
  font-family: var(--sans) !important;
}

/* transparent wrappers */
.stApp,
.stApp > div,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section.main,
section.main > div { background: transparent !important; }

/* hide chrome */
#MainMenu, footer, header,
button[title="View fullscreen"] { visibility: hidden !important; }

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: var(--navy); border-radius: 4px; }

/* 4. CONTENT COLUMN : 850 px centred --------------------------------------- */
.block-container {
  max-width: 850px !important;
  padding: 0 1rem 5rem !important;
  margin: 0 auto !important;
  background: transparent !important;
}

/* 5. SIDEBAR --------------------------------------------------------------- */

/* Paint EVERY node Streamlit generates for the sidebar navy blue.          */
/* We intentionally use a blanket * rule so future Streamlit versions       */
/* cannot introduce an unpainted child node.                                */

[data-testid="stSidebar"]                                             { background: #0047BA !important; border-right: none !important; box-shadow: 3px 0 20px rgba(0,20,100,.18) !important; }
[data-testid="stSidebar"] > div                                       { background: #0047BA !important; }
[data-testid="stSidebar"] > div > div                                 { background: #0047BA !important; }
[data-testid="stSidebarContent"]                                      { background: #0047BA !important; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]             { background: #0047BA !important; }
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]{ background: #0047BA !important; }
[data-testid="stSidebar"] section                                     { background: #0047BA !important; }

/* force ALL descendent text white */
[data-testid="stSidebar"] *                { color: #FFFFFF !important; font-family: var(--sans) !important; }
[data-testid="stSidebar"] .stMarkdown p    { color: rgba(255,255,255,.80) !important; font-size: .82rem !important; }
[data-testid="stSidebar"] small            { color: rgba(255,255,255,.50) !important; }

/* file-uploader on dark bg */
[data-testid="stSidebar"] [data-testid="stFileUploader"]             { background: rgba(255,255,255,.08) !important; border: 1.5px dashed rgba(255,255,255,.30) !important; border-radius: var(--r-sm) !important; transition: border-color .2s !important; }
[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover       { border-color: var(--yellow) !important; }
[data-testid="stSidebar"] [data-testid="stFileUploader"] label       { display: none !important; }
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] span { color: rgba(255,255,255,.42) !important; font-size: .70rem !important; }
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] small { color: rgba(255,255,255,.28) !important; font-size: .60rem !important; }

/* sidebar atoms */
.sb-top  { background:rgba(0,0,0,.20); padding:.85rem 1.1rem; border-bottom:1px solid rgba(255,255,255,.10); margin-bottom:1.1rem; display:flex; align-items:center; gap:9px; }
.sb-top .t { font-size:.66rem !important; font-weight:700 !important; color:rgba(255,255,255,.92) !important; letter-spacing:2.2px !important; text-transform:uppercase !important; }
.sb-wrap { padding:0 1.1rem; }
.sb-lbl  { font-size:.56rem !important; font-weight:700 !important; color:rgba(255,255,255,.42) !important; letter-spacing:2.4px !important; text-transform:uppercase !important; display:flex; align-items:center; gap:5px; margin-bottom:.45rem; }
.sb-lbl::before { content:""; width:3px; height:9px; background:var(--yellow); border-radius:2px; flex-shrink:0; }
.sb-none { font-size:.68rem !important; color:rgba(255,255,255,.35) !important; line-height:1.8; padding:.2rem 0; }
.sb-hr   { height:1px; background:rgba(255,255,255,.10); margin:.85rem 0; }
.sb-tip  { font-family:var(--mono) !important; font-size:.58rem !important; color:rgba(255,255,255,.32) !important; line-height:1.8; padding:.55rem .75rem; background:rgba(0,0,0,.18); border-radius:var(--r-sm); border-left:2px solid rgba(255,209,0,.50); }
.sb-tip code   { color:var(--yellow) !important; }
.sb-tip strong { color:rgba(255,255,255,.55) !important; }
.sb-schema { background:rgba(0,0,0,.22); border:1px solid rgba(255,255,255,.10); border-left:3px solid var(--yellow); border-radius:var(--r-sm); padding:.72rem .85rem; margin-top:.55rem; max-height:200px; overflow-y:auto; }
.sb-schema pre { font-family:var(--mono) !important; font-size:.61rem !important; line-height:1.7 !important; color:rgba(255,255,255,.65) !important; margin:0 !important; white-space:pre-wrap !important; word-break:break-word !important; }
.sb-ok { display:flex; align-items:center; gap:6px; margin-top:.55rem; font-size:.61rem !important; font-weight:600 !important; color:#6EE7B7 !important; }
.sb-ok .g { width:6px; height:6px; border-radius:50%; background:#6EE7B7; flex-shrink:0; }

/* 6. HEADER ---------------------------------------------------------------- */
.tc-hdr {
  background: var(--white);
  border-bottom: 2px solid var(--navy);
  margin: 0 -1rem 2rem;
  padding: 0 2rem;
  height: 58px;
  display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 2px 12px rgba(0,35,110,.10);
}
.tc-hdr-left { display:flex; align-items:center; gap:13px; }
.tc-logo-pill { height:34px; display:flex; align-items:center; background:transparent; }
.tc-logo-pill img { height:30px; width:auto; display:block; }
.tc-hdr-divider { width:1px; height:22px; background:var(--brd); }
.tc-hdr-title { font-size:1rem; font-weight:800; color:var(--navy); letter-spacing:.4px; line-height:1; }
.tc-hdr-sub   { font-size:.54rem; color:var(--subtle); letter-spacing:1.8px; text-transform:uppercase; margin-top:2px; }
.tc-hdr-pill  { background:var(--navy-lt); border:1px solid rgba(0,71,186,.20); border-radius:20px; padding:4px 13px; font-size:.58rem; font-weight:600; color:var(--navy); letter-spacing:.8px; text-transform:uppercase; }

/* 7. SECTION LABELS -------------------------------------------------------- */
.tc-lbl { font-size:.63rem; font-weight:700; color:var(--navy-dk); letter-spacing:1.8px; text-transform:uppercase; margin-bottom:.55rem; display:flex; align-items:center; gap:7px; }
.tc-lbl::before { content:""; width:3px; height:13px; background:var(--yellow); border-radius:2px; flex-shrink:0; }

/* 8. SELECT / INPUT WIDGETS ------------------------------------------------ */
.stSelectbox label { font-size:.62rem !important; font-weight:700 !important; color:var(--muted) !important; text-transform:uppercase !important; letter-spacing:.9px !important; }
.stSelectbox > div > div { background:#FAFCFF !important; border:1.5px solid var(--brd) !important; border-radius:var(--r-sm) !important; font-family:var(--sans) !important; font-size:.84rem !important; color:var(--text) !important; transition:border-color .18s !important; }
.stSelectbox > div > div:focus-within { border-color:var(--navy) !important; box-shadow:0 0 0 3px rgba(0,71,186,.10) !important; }
div[data-baseweb="select"] *  { background:#fff !important; color:var(--text) !important; }
div[data-baseweb="popover"] * { background:#fff !important; border-color:var(--brd) !important; color:var(--text) !important; }

.stTextArea label { display:none !important; }
.stTextArea textarea { background:#FAFCFF !important; border:1.5px solid var(--brd) !important; border-radius:var(--r-sm) !important; font-family:var(--sans) !important; font-size:.88rem !important; line-height:1.65 !important; color:var(--text) !important; padding:11px 13px !important; resize:vertical !important; transition:border-color .18s, box-shadow .18s !important; }
.stTextArea textarea:focus { border-color:var(--navy) !important; background:#fff !important; box-shadow:0 0 0 3px rgba(0,71,186,.10) !important; outline:none !important; }
.stTextArea textarea::placeholder { color:var(--subtle) !important; }

/* 9. BUTTON ---------------------------------------------------------------- */
.stButton > button { background:var(--yellow) !important; color:#001A5E !important; font-family:var(--sans) !important; font-weight:700 !important; font-size:.875rem !important; border:none !important; border-radius:var(--r-sm) !important; padding:.65rem 2.5rem !important; cursor:pointer !important; transition:background .15s, box-shadow .15s, transform .10s !important; box-shadow:0 3px 12px rgba(255,209,0,.30) !important; display:block !important; margin:.5rem auto 0 !important; }
.stButton > button:hover  { background:var(--yel-dk) !important; box-shadow:0 5px 20px rgba(200,168,0,.38) !important; transform:translateY(-1px) !important; }
.stButton > button:active { transform:translateY(0) !important; }

/* 10. CARD WRAPPER (st.container border=True override) -------------------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--white) !important;
  border: 1px solid var(--brd) !important;
  border-radius: var(--r) !important;
  box-shadow: 0 4px 28px rgba(0,0,0,.06) !important;
  padding: 1.8rem 2rem !important;
}

/* 11. SQL DARK CODE CARD -------------------------------------------------- */
.sql-card {
  background: #1E2433;
  border: 1px solid #2D3448;
  border-radius: var(--r);
  padding: 1.3rem 1.5rem 1.1rem;
  box-shadow: 0 6px 28px rgba(0,0,0,.18);
  margin-top: .5rem;
}
.sql-card pre { font-family:var(--mono) !important; font-size:.80rem !important; line-height:1.80 !important; color:#CDD6F4 !important; margin:0 !important; white-space:pre-wrap !important; word-break:break-word !important; }
/* syntax colors on dark */
.kw  { color:#89DCEB; font-weight:700; }
.fn  { color:#A6E3A1; }
.str { color:#F38BA8; }
.cmt { color:#6C7086; font-style:italic; }
.num { color:#CBA6F7; }
.sql-bar { display:flex; align-items:center; justify-content:space-between; margin-top:.9rem; padding-top:.75rem; border-top:1px solid #2D3448; }
.sql-tag { display:inline-flex; align-items:center; gap:5px; background:rgba(137,220,235,.12); border-radius:20px; padding:3px 10px; font-size:.61rem; font-weight:600; color:#89DCEB; }
.sql-tag .dot { width:6px; height:6px; border-radius:50%; background:#A6E3A1; }

/* 12. DOWNLOAD LINK ------------------------------------------------------- */
.dl-wrap { margin-top:.75rem; }
.dl-wrap a { display:inline-flex; align-items:center; gap:6px; background:var(--navy-lt); border:1.5px solid var(--navy); border-radius:var(--r-sm); padding:.42rem 1rem; font-size:.76rem; font-weight:600; color:var(--navy); text-decoration:none; transition:background .15s, color .15s; }
.dl-wrap a:hover { background:var(--navy); color:#fff; }

/* 13. STATS --------------------------------------------------------------- */
.stats-row { display:flex; gap:.7rem; margin-top:.9rem; }
.stat { flex:1; background:var(--white); border:1px solid var(--brd); border-radius:var(--r-sm); padding:.82rem; text-align:center; box-shadow:0 1px 5px rgba(0,71,186,.04); transition:box-shadow .18s, transform .15s; }
.stat:hover { box-shadow:0 4px 14px rgba(0,71,186,.10); transform:translateY(-1px); }
.stat .v { font-size:1.15rem; font-weight:800; color:var(--navy); }
.stat .l { font-size:.58rem; font-weight:700; color:var(--muted); letter-spacing:.8px; text-transform:uppercase; margin-top:2px; }

/* 14. ALERTS -------------------------------------------------------------- */
.c-alert { background:var(--white); border:1px solid #BEE3F8; border-left:4px solid var(--navy); border-radius:var(--r); padding:1.2rem 1.4rem; margin-top:1rem; box-shadow:0 2px 10px rgba(0,71,186,.07); font-family:var(--sans); }
.c-alert.warn { border-left-color:#D69E2E; border-color:#FAF089; }
.c-alert.info { border-left-color:#38A169; border-color:#C6F6D5; }
.c-alert-hd { display:flex; align-items:center; gap:10px; margin-bottom:.55rem; }
.c-alert-ic { width:30px; height:30px; border-radius:8px; background:var(--navy-lt); display:flex; align-items:center; justify-content:center; font-size:.85rem; flex-shrink:0; }
.c-alert.warn .c-alert-ic { background:#FEFCBF; }
.c-alert.info .c-alert-ic { background:#F0FFF4; }
.c-alert-title { font-size:.86rem; font-weight:700; color:var(--navy-dk); }
.c-alert.warn .c-alert-title { color:#744210; }
.c-alert.info .c-alert-title { color:#276749; }
.c-alert-body { font-size:.80rem; color:var(--muted); line-height:1.65; padding-left:40px; }
.c-alert-body code { background:var(--navy-lt); padding:1px 5px; border-radius:4px; font-family:var(--mono); font-size:.74rem; color:var(--navy); }
.c-alert-body pre { background:#F8FAFF; border:1px solid #BEE3F8; border-radius:6px; padding:7px 11px; font-family:var(--mono); font-size:.74rem; color:var(--navy-dk); margin:.45rem 0 .15rem; }

/* 15. SCHEMA BADGE -------------------------------------------------------- */
.s-badge { display:inline-flex; align-items:center; gap:6px; background:rgba(56,161,105,.08); border:1px solid rgba(56,161,105,.24); border-radius:20px; padding:3px 12px; font-size:.62rem; font-weight:600; color:var(--ok); margin-bottom:.65rem; }
.s-badge .dg { width:6px; height:6px; border-radius:50%; background:var(--ok); }

/* 16. EXPANDER ------------------------------------------------------------ */
.streamlit-expanderHeader { background:rgba(255,255,255,.90) !important; border:1px solid var(--brd) !important; border-radius:var(--r-sm) !important; font-family:var(--sans) !important; font-size:.75rem !important; font-weight:600 !important; color:var(--muted) !important; }
.streamlit-expanderContent { background:rgba(255,255,255,.93) !important; border:1px solid var(--brd) !important; border-top:none !important; }

/* 17. HISTORY ITEM -------------------------------------------------------- */
.hi { background:var(--white); border:1px solid var(--brd); border-left:3px solid var(--yellow); border-radius:var(--r-sm); padding:.7rem .95rem; margin-bottom:.4rem; box-shadow:0 1px 4px rgba(0,71,186,.04); }
.hi .hp { font-size:.80rem; font-weight:500; color:var(--text); margin-bottom:2px; display:-webkit-box; -webkit-line-clamp:1; -webkit-box-orient:vertical; overflow:hidden; }
.hi .hm { font-size:.61rem; color:var(--subtle); }

/* 18. CODE / COPY --------------------------------------------------------- */
.stCodeBlock { border:1px solid var(--brd) !important; border-radius:var(--r-sm) !important; }
.stCodeBlock pre { background:#1E2433 !important; font-family:var(--mono) !important; font-size:.78rem !important; color:#CDD6F4 !important; }
div[data-testid="stCopyButton"] button { background:rgba(137,220,235,.12) !important; border:1px solid rgba(137,220,235,.25) !important; color:#89DCEB !important; border-radius:5px !important; font-size:.66rem !important; }
div[data-testid="stCopyButton"] button:hover { background:#89DCEB !important; color:#1E2433 !important; }
.stSpinner > div { border-top-color:var(--navy) !important; }

/* 19. MISC ---------------------------------------------------------------- */
.p-div { height:1px; background:var(--brd); margin:1.2rem 0; opacity:.5; }

/* 20. FOOTER -------------------------------------------------------------- */
.tc-foot { text-align:center; margin-top:3rem; padding:1rem 0 .5rem; border-top:1px solid var(--brd); }
.tc-foot p { font-family:var(--sans); font-size:.60rem; color:var(--subtle); letter-spacing:.5px; margin:0; }
.tc-foot p+p { margin-top:.22rem; }
.tc-foot strong { color:var(--muted); font-weight:600; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
for k, v in [("history", []), ("qc", 0), ("tt", 0), ("lp", "")]:
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
SQL_KW = [
    "SELECT","FROM","WHERE","JOIN","LEFT JOIN","RIGHT JOIN","INNER JOIN",
    "FULL OUTER JOIN","ON","GROUP BY","ORDER BY","HAVING","LIMIT","OFFSET",
    "INSERT INTO","VALUES","UPDATE","SET","DELETE","CREATE TABLE","ALTER TABLE",
    "DROP TABLE","WITH","AS","AND","OR","NOT","IN","BETWEEN","LIKE",
    "IS NULL","IS NOT NULL","DISTINCT","UNION","UNION ALL","INTERSECT","EXCEPT",
    "CASE","WHEN","THEN","ELSE","END","ASC","DESC","COALESCE","NULLIF","CAST",
    "OVER","PARTITION BY","ROW_NUMBER","RANK","DENSE_RANK","LAG","LEAD",
]

def hl(sql: str) -> str:
    for kw in sorted(SQL_KW, key=len, reverse=True):
        sql = re.compile(rf"\b({re.escape(kw)})\b", re.I).sub(
            r'<span class="kw">\1</span>', sql)
    return sql

def parse_schema(f):
    raw = f.read().decode("utf-8", errors="replace")
    return raw, len(raw), len(re.findall(r"\bCREATE\s+TABLE\b", raw, re.I))

def sys_prompt(dialect: str, style: str) -> str:
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

def user_msg(prompt: str, schema) -> str:
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

def ok_check(sql: str):
    if sql.startswith("ERROR:"):
        return False, sql[6:].strip()
    if len(sql) < 10:
        return False, "Model returned an unexpectedly short response."
    return True, ""

def dl_link(sql: str) -> str:
    enc = b64lib.b64encode(sql.encode()).decode()
    ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return (
        f'<div class="dl-wrap"><a href="data:file/sql;base64,{enc}" '
        f'download="query_{ts}.sql">📥 Download SQL</a></div>'
    )

def make_alert(icon: str, title: str, body: str, variant: str = "") -> str:
    return (
        f'<div class="c-alert {variant}">'
        f'<div class="c-alert-hd">'
        f'<div class="c-alert-ic">{icon}</div>'
        f'<div class="c-alert-title">{title}</div>'
        f'</div>'
        f'<div class="c-alert-body">{body}</div>'
        f'</div>'
    )


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # top banner
    st.markdown(
        '<div class="sb-top">'
        '<span style="font-size:.88rem">🗄️</span>'
        '<span class="t">Schema Context</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sb-wrap">', unsafe_allow_html=True)
    st.markdown('<p class="sb-lbl">📂 Upload Schema File</p>', unsafe_allow_html=True)

    uf = st.file_uploader(
        "schema_file",
        type=["sql", "txt"],
        accept_multiple_files=False,
        label_visibility="collapsed",
    )

    schema_text, schema_meta = None, {}

    if uf:
        try:
            raw, chars, tables = parse_schema(uf)
            if chars > 80_000:
                st.markdown(
                    make_alert("⚠️", "File Too Large",
                               "Schema exceeds 80 KB. Remove unused tables.", "warn"),
                    unsafe_allow_html=True,
                )
            else:
                schema_text = raw
                schema_meta = {"name": uf.name, "tables": tables, "chars": chars}
                preview = raw[:700] + ("\n…" if len(raw) > 700 else "")
                st.markdown(
                    f'<div class="sb-schema"><pre>{preview}</pre></div>'
                    f'<div class="sb-ok"><span class="g"></span>'
                    f'{tables} tables · {chars:,} chars</div>',
                    unsafe_allow_html=True,
                )
        except Exception as e:
            st.markdown(
                make_alert("❌", "File Error", f"Could not read file: {e}"),
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<p class="sb-none">No schema loaded.<br>'
            'AI will use general knowledge.</p>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="sb-hr"></div>'
        '<div class="sb-tip">💡 <strong>Tip:</strong><br>'
        '<code>pg_dump --schema-only</code><br>'
        '<code>SHOW CREATE TABLE t</code></div>'
        '</div>',   # /sb-wrap
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  API KEY CHECK
# ══════════════════════════════════════════════════════════════════════════════
api_key = st.secrets.get("OPENAI_API_KEY", "")
if not api_key:
    st.markdown(
        make_alert(
            "🔐", "API Key Not Found",
            'Add your OpenAI API key to <code>.streamlit/secrets.toml</code>:'
            '<pre>OPENAI_API_KEY = "sk-..."</pre>'
            'On Streamlit Cloud: <strong>App Settings › Secrets</strong>',
        ),
        unsafe_allow_html=True,
    )
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  HEADER  (white bar, navy bottom border, logo left of title)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div class="tc-hdr">'
    f'  <div class="tc-hdr-left">'
    f'    <div class="tc-logo-pill"><img src="{LOGO_SRC}" alt="logo"></div>'
    f'    <div class="tc-hdr-divider"></div>'
    f'    <div>'
    f'      <div class="tc-hdr-title">TURKCELL SQL AI</div>'
    f'      <div class="tc-hdr-sub">Natural Language → SQL</div>'
    f'    </div>'
    f'  </div>'
    f'  <div class="tc-hdr-pill">Powered by OpenAI</div>'
    f'</div>',
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN FORM  —  single white card via st.container(border=True)
# ══════════════════════════════════════════════════════════════════════════════
with st.container(border=True):

    # ── Configuration ─────────────────────────────────────────────────────────
    st.markdown('<p class="tc-lbl">⚙ Configuration</p>', unsafe_allow_html=True)
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

    st.markdown('<div class="p-div"></div>', unsafe_allow_html=True)

    # ── Schema badge ──────────────────────────────────────────────────────────
    if schema_text:
        st.markdown(
            f'<div class="s-badge"><span class="dg"></span>'
            f'Schema Mode Active · {schema_meta["name"]} · {schema_meta["tables"]} tables</div>',
            unsafe_allow_html=True,
        )

    # ── Prompt ────────────────────────────────────────────────────────────────
    st.markdown('<p class="tc-lbl">✦ Describe in Natural Language</p>', unsafe_allow_html=True)
    prompt = st.text_area(
        "p",
        value=st.session_state.lp,
        height=130,
        placeholder=(
            "e.g. → List all users who signed up last month but haven't placed an order yet, "
            "grouped by referral source and sorted by registration date…"
        ),
        key="pk",
        label_visibility="collapsed",
    )

    go = st.button("⚡  Generate SQL", key="go")


# ══════════════════════════════════════════════════════════════════════════════
#  NO-SCHEMA INFO TOAST
# ══════════════════════════════════════════════════════════════════════════════
if go and not schema_text:
    st.markdown(
        make_alert(
            "ℹ️", "No Schema Loaded — Using General Knowledge",
            "AI will infer table and column names from your description. "
            "For more accurate results, upload a <code>.sql</code> schema file via the sidebar.",
            "info",
        ),
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  GENERATE
# ══════════════════════════════════════════════════════════════════════════════
if go:
    st.session_state.lp = prompt

    if not prompt.strip():
        st.markdown(
            make_alert("✏️", "Empty Prompt",
                       "Please enter a description before generating.", "warn"),
            unsafe_allow_html=True,
        )
        st.stop()

    with st.spinner("Generating SQL…"):
        try:
            res = run_sql(prompt, api_key, dialect, style, model, schema_text)
        except openai.AuthenticationError:
            st.markdown(make_alert("🔑", "Authentication Error",
                "Your API key was rejected. Verify it is valid and active."),
                unsafe_allow_html=True); st.stop()
        except openai.RateLimitError:
            st.markdown(make_alert("⏱", "Rate Limit Exceeded",
                "OpenAI quota reached. Wait a moment and try again."),
                unsafe_allow_html=True); st.stop()
        except openai.APIConnectionError:
            st.markdown(make_alert("🌐", "Connection Error",
                "Could not reach the OpenAI API. Check your internet connection."),
                unsafe_allow_html=True); st.stop()
        except Exception as e:
            st.markdown(make_alert("⚙️", "Unexpected Error",
                f"Something went wrong:<br><code>{e}</code>"),
                unsafe_allow_html=True); st.stop()

    valid, err = ok_check(res["sql"])
    if not valid:
        st.markdown(make_alert("⚠️", "Model Notice", err, "warn"),
            unsafe_allow_html=True); st.stop()

    # ── store ────────────────────────────────────────────────────────────────
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

    # ── SQL dark card ────────────────────────────────────────────────────────
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
        f'<div style="display:flex;gap:.5rem;align-items:center;">'
        f'{sb}'
        f'<span class="sql-tag">{res["elapsed"]}s · {res["tokens"]} tokens</span>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    st.code(res["sql"], language="sql")
    st.markdown(dl_link(res["sql"]), unsafe_allow_html=True)

    # ── stats ────────────────────────────────────────────────────────────────
    st.markdown(
        f'<div class="stats-row">'
        f'<div class="stat"><div class="v">{st.session_state.qc}</div><div class="l">Queries</div></div>'
        f'<div class="stat"><div class="v">{res["elapsed"]}s</div><div class="l">Response</div></div>'
        f'<div class="stat"><div class="v">{st.session_state.tt}</div><div class="l">Tokens</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  QUERY HISTORY
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.history:
    st.markdown('<div class="p-div"></div>', unsafe_allow_html=True)
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
            st.markdown(dl_link(e["sql"]), unsafe_allow_html=True)
            if i < len(st.session_state.history) - 1:
                st.markdown('<div style="height:.2rem"></div>', unsafe_allow_html=True)

        st.markdown('<div style="height:.3rem"></div>', unsafe_allow_html=True)
        if st.button("🗑  Clear History", key="clr"):
            st.session_state.update({"history": [], "qc": 0, "tt": 0})
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════
yr = datetime.datetime.now().year
st.markdown(
    f'<div class="tc-foot">'
    f'<p>© {yr} <strong>TURKCELL SQL AI</strong> | L2 DevOps Operations</p>'
    f'<p>Powered by OpenAI · Streamlit · All rights reserved.</p>'
    f'</div>',
    unsafe_allow_html=True,
)