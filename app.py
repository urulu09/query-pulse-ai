"""
TURKCELL SQL AI — app.py  v4.0
SQL Explanation · Clipboard · Compact cards · Table preview · Refined footer
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

# ══════════════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════════════
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
  --rad:     14px;
  --rad-s:   8px;
}

/* ─ reset & base ─────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body {
  background: linear-gradient(170deg,#f8fbff 0%,#edf3fc 100%) !important;
  min-height: 100vh; font-family: var(--sans) !important;
}
.stApp, .stApp > div,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section.main, section.main > div,
.block-container { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="collapsedControl"] { display: none !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: var(--navy); border-radius: 4px; }

/* ─ container ─────────────────────────────────────────────────────────── */
.block-container {
  max-width: 860px !important;
  padding: 0 1rem 2rem !important;
  margin: 0 auto !important;
}

/* ─ kill default streamlit spacing ───────────────────────────────────── */
div[data-testid="stVerticalBlock"] > div { margin-bottom: 0 !important; }
div[data-testid="element-container"] { margin: 0 !important; padding: 0 !important; }

/* ══════════════ HEADER ══════════════════════════════════════════════════ */
.hdr {
  background: linear-gradient(90deg,#001A5E 0%,#0047BA 100%);
  margin: 0 -1rem 1.2rem;
  padding: 0 1.8rem;
  height: 54px;
  display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 3px 14px rgba(0,30,110,.24);
  position: relative; overflow: hidden;
}
.hdr::after { content:""; position:absolute; inset:0; background:linear-gradient(90deg,transparent 60%,rgba(255,255,255,.04)); pointer-events:none; }
.hdr-left  { display:flex; align-items:center; gap:12px; z-index:1; }
.hdr-logo  { height:30px; width:auto; display:block; background:rgba(255,255,255,.95); border-radius:6px; padding:3px 8px; }
.hdr-vline { width:1px; height:20px; background:rgba(255,255,255,.25); }
.hdr-title { font-size:.98rem; font-weight:800; color:#fff; letter-spacing:.4px; line-height:1.2; }
.hdr-sub   { font-size:.52rem; color:rgba(255,255,255,.45); letter-spacing:2px; text-transform:uppercase; margin-top:2px; }
.hdr-pill  { z-index:1; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.22); border-radius:20px; padding:3px 13px; font-size:.57rem; font-weight:600; color:rgba(255,255,255,.76); letter-spacing:.9px; text-transform:uppercase; }

/* ══════════════ CARDS ═══════════════════════════════════════════════════ */
.card {
  background: var(--white);
  border: 1px solid var(--brd);
  border-radius: var(--rad);
  box-shadow: 0 3px 20px rgba(0,0,0,.055), 0 1px 4px rgba(0,71,186,.04);
  padding: 1.3rem 1.6rem 1.4rem;
  margin-bottom: .8rem;
}
.upload-card {
  background: linear-gradient(135deg,#EBF3FF 0%,#dceeff 100%);
  border: 1.5px dashed rgba(0,71,186,.26);
  border-radius: var(--rad);
  padding: 1rem 1.4rem .8rem;
  margin-bottom: .8rem;
}
.card-sep { height:1px; background:#F0F4FA; margin:.9rem 0; }

/* ─ labels ─────────────────────────────────────────────────────────────── */
.lbl { font-size:.62rem; font-weight:700; color:var(--navy-dk); letter-spacing:1.8px; text-transform:uppercase; margin-bottom:.45rem; display:flex; align-items:center; gap:6px; }
.lbl::before { content:""; width:3px; height:12px; background:var(--yel); border-radius:2px; flex-shrink:0; }
.upload-lbl { font-size:.70rem; font-weight:700; color:var(--navy-dk); letter-spacing:1.4px; text-transform:uppercase; margin-bottom:.45rem; display:flex; align-items:center; gap:6px; }
.upload-lbl::before { content:""; width:3px; height:12px; background:var(--yel); border-radius:2px; flex-shrink:0; }

/* ─ help text ──────────────────────────────────────────────────────────── */
.upload-help { font-size:.70rem; color:var(--muted); line-height:1.6; padding:.4rem .65rem; background:rgba(255,255,255,.55); border-radius:var(--rad-s); border-left:2px solid rgba(0,71,186,.22); margin-top:.45rem; }
.upload-help code { background:rgba(0,71,186,.08); color:var(--navy); padding:1px 4px; border-radius:4px; font-family:var(--mono); font-size:.67rem; }

/* ─ schema loaded ──────────────────────────────────────────────────────── */
.schema-ok { display:flex; align-items:center; gap:6px; margin-top:.45rem; font-size:.68rem; font-weight:600; color:var(--ok); }
.schema-ok .dot { width:6px; height:6px; border-radius:50%; background:var(--ok); flex-shrink:0; }
.tbl-row   { display:flex; flex-wrap:wrap; gap:.28rem; margin-top:.38rem; }
.tbl-chip  { background:rgba(0,71,186,.08); border:1px solid rgba(0,71,186,.18); border-radius:20px; padding:2px 9px; font-family:var(--mono); font-size:.63rem; font-weight:500; color:var(--navy-dk); }
.tbl-more  { background:rgba(160,174,192,.13); border:1px solid var(--brd); border-radius:20px; padding:2px 9px; font-size:.63rem; color:var(--muted); }

/* ─ file uploader ──────────────────────────────────────────────────────── */
[data-testid="stFileUploader"] { background:transparent !important; border:none !important; }
[data-testid="stFileUploader"] label { display:none !important; }
[data-testid="stFileUploaderDropzone"] { background:rgba(255,255,255,.65) !important; border:1.5px dashed rgba(0,71,186,.28) !important; border-radius:var(--rad-s) !important; transition:border-color .2s !important; }
[data-testid="stFileUploaderDropzone"]:hover { border-color:var(--navy) !important; background:#fff !important; }
[data-testid="stFileUploaderDropzoneInstructions"] span { color:var(--muted) !important; font-size:.73rem !important; }
[data-testid="stFileUploaderDropzone"] small { color:var(--subtle) !important; font-size:.60rem !important; }

/* ─ selects ────────────────────────────────────────────────────────────── */
.stSelectbox label { font-size:.60rem !important; font-weight:700 !important; color:var(--muted) !important; text-transform:uppercase !important; letter-spacing:.8px !important; }
.stSelectbox > div > div { background:#FAFCFF !important; border:1.5px solid var(--brd) !important; border-radius:var(--rad-s) !important; font-family:var(--sans) !important; font-size:.83rem !important; color:var(--text) !important; transition:border-color .18s !important; }
.stSelectbox > div > div:focus-within { border-color:var(--navy) !important; box-shadow:0 0 0 3px rgba(0,71,186,.10) !important; }
div[data-baseweb="select"] *  { background:#fff !important; color:var(--text) !important; }
div[data-baseweb="popover"] * { background:#fff !important; border-color:var(--brd) !important; color:var(--text) !important; }

/* ─ textarea ────────────────────────────────────────────────────────────── */
.stTextArea label { display:none !important; }
.stTextArea textarea { background:#FAFCFF !important; border:1.5px solid var(--brd) !important; border-radius:var(--rad-s) !important; font-family:var(--sans) !important; font-size:.87rem !important; line-height:1.6 !important; color:var(--text) !important; padding:10px 12px !important; resize:vertical !important; transition:border-color .18s, box-shadow .18s !important; }
.stTextArea textarea:focus { border-color:var(--navy) !important; background:#fff !important; box-shadow:0 0 0 3px rgba(0,71,186,.10) !important; outline:none !important; }
.stTextArea textarea::placeholder { color:var(--subtle) !important; }

/* ─ generate button ─────────────────────────────────────────────────────── */
.stButton > button {
  background: var(--yel) !important; color: #001A5E !important;
  font-family: var(--sans) !important; font-weight: 700 !important;
  font-size: .875rem !important; border: none !important;
  border-radius: var(--rad-s) !important; padding: .62rem 2.6rem !important;
  cursor: pointer !important; display: block !important; margin: .45rem auto 0 !important;
  transition: background .15s, box-shadow .15s, transform .10s !important;
  box-shadow: 0 3px 12px rgba(255,209,0,.30) !important;
}
.stButton > button:hover  { background:var(--yel-dk) !important; box-shadow:0 4px 18px rgba(200,168,0,.38) !important; transform:translateY(-1px) !important; }
.stButton > button:active { transform:translateY(0) !important; }

/* ══════════════ SQL DARK CARD ═══════════════════════════════════════════ */
.sql-card {
  background: #1E2433; border:1px solid #2D3448; border-radius:var(--rad);
  padding:1.2rem 1.4rem 1rem; box-shadow:0 5px 24px rgba(0,0,0,.16); margin-top:.5rem;
}
.sql-card pre { font-family:var(--mono) !important; font-size:.78rem !important; line-height:1.78 !important; color:#CDD6F4 !important; margin:0 !important; white-space:pre-wrap !important; word-break:break-word !important; }
.kw  { color:#89DCEB; font-weight:700; }
.fn  { color:#A6E3A1; }
.str { color:#F38BA8; }
.cmt { color:#6C7086; font-style:italic; }
.num { color:#CBA6F7; }
.sql-bar { display:flex; align-items:center; justify-content:space-between; margin-top:.8rem; padding-top:.65rem; border-top:1px solid #2D3448; }
.sql-tag { display:inline-flex; align-items:center; gap:4px; background:rgba(137,220,235,.12); border-radius:20px; padding:2px 9px; font-size:.60rem; font-weight:600; color:#89DCEB; }
.sql-tag .dot { width:5px; height:5px; border-radius:50%; background:#A6E3A1; }

/* ── clipboard button ─────────────────────────────────────────────────── */
.clip-btn {
  display: inline-flex; align-items: center; gap: 5px;
  background: rgba(137,220,235,.12); border: 1px solid rgba(137,220,235,.28);
  border-radius: var(--rad-s); padding: 3px 11px;
  font-family: var(--sans); font-size: .68rem; font-weight: 600;
  color: #89DCEB; cursor: pointer; transition: background .15s;
}
.clip-btn:hover { background: rgba(137,220,235,.22); }
.clip-btn.copied { color: #A6E3A1; border-color: rgba(166,227,161,.40); }

/* ══════════════ EXPLANATION CARD ════════════════════════════════════════ */
.exp-card {
  background: #fff; border: 1px solid var(--brd);
  border-left: 3px solid var(--yel); border-radius: var(--rad);
  padding: 1rem 1.3rem; margin-top: .7rem;
  box-shadow: 0 2px 12px rgba(0,0,0,.04);
}
.exp-title { font-size:.68rem; font-weight:700; color:var(--navy-dk); letter-spacing:1.5px; text-transform:uppercase; margin-bottom:.55rem; display:flex; align-items:center; gap:6px; }
.exp-title::before { content:""; width:3px; height:12px; background:var(--yel); border-radius:2px; flex-shrink:0; }
.exp-card ul { margin:.3rem 0 0 1.1rem; padding:0; list-style:none; }
.exp-card ul li { font-size:.80rem; color:var(--text); line-height:1.65; margin-bottom:.28rem; padding-left:1rem; position:relative; }
.exp-card ul li::before { content:"▸"; position:absolute; left:0; color:var(--navy); font-size:.70rem; top:.08rem; }
.exp-loading { font-size:.78rem; color:var(--muted); font-style:italic; padding:.2rem 0; }

/* ─ download (secondary style) ───────────────────────────────────────── */
.dl-wrap { margin-top:.55rem; }
.dl-wrap a { display:inline-flex; align-items:center; gap:5px; background:transparent; border:1.5px solid rgba(0,71,186,.35); border-radius:var(--rad-s); padding:.35rem .85rem; font-size:.72rem; font-weight:600; color:var(--navy); text-decoration:none; transition:background .15s, border-color .15s; }
.dl-wrap a:hover { background:var(--navy-lt); border-color:var(--navy); }

/* ─ stats ───────────────────────────────────────────────────────────────── */
.stats { display:flex; gap:.6rem; margin-top:.7rem; }
.stat { flex:1; background:var(--white); border:1px solid var(--brd); border-radius:var(--rad-s); padding:.7rem .6rem; text-align:center; box-shadow:0 1px 5px rgba(0,71,186,.04); transition:box-shadow .15s, transform .12s; }
.stat:hover { box-shadow:0 3px 12px rgba(0,71,186,.09); transform:translateY(-1px); }
.stat .v { font-size:1.1rem; font-weight:800; color:var(--navy); }
.stat .l { font-size:.57rem; font-weight:700; color:var(--muted); letter-spacing:.8px; text-transform:uppercase; margin-top:2px; }

/* ─ alerts ──────────────────────────────────────────────────────────────── */
.alert { background:var(--white); border:1px solid #BEE3F8; border-left:4px solid var(--navy); border-radius:var(--rad); padding:1rem 1.2rem; margin-top:.8rem; box-shadow:0 2px 8px rgba(0,71,186,.06); font-family:var(--sans); }
.alert.warn { border-left-color:#D69E2E; border-color:#FAF089; }
.alert.info { border-left-color:var(--ok); border-color:#C6F6D5; }
.alert-h { display:flex; align-items:center; gap:9px; margin-bottom:.45rem; }
.alert-ic { width:28px; height:28px; border-radius:7px; background:var(--navy-lt); display:flex; align-items:center; justify-content:center; font-size:.82rem; flex-shrink:0; }
.alert.warn .alert-ic { background:#FEFCBF; }
.alert.info .alert-ic { background:#F0FFF4; }
.alert-title { font-size:.84rem; font-weight:700; color:var(--navy-dk); }
.alert.warn .alert-title { color:#744210; }
.alert.info .alert-title { color:#276749; }
.alert-body { font-size:.78rem; color:var(--muted); line-height:1.6; padding-left:37px; }
.alert-body code { background:var(--navy-lt); padding:1px 4px; border-radius:4px; font-family:var(--mono); font-size:.71rem; color:var(--navy); }
.alert-body pre  { background:#F8FAFF; border:1px solid #BEE3F8; border-radius:5px; padding:6px 10px; font-family:var(--mono); font-size:.71rem; color:var(--navy-dk); margin:.4rem 0 .1rem; }

/* ─ schema badge ────────────────────────────────────────────────────────── */
.sbadge { display:inline-flex; align-items:center; gap:5px; background:rgba(56,161,105,.09); border:1px solid rgba(56,161,105,.24); border-radius:20px; padding:2px 10px; font-size:.61rem; font-weight:600; color:var(--ok); margin-bottom:.55rem; }
.sbadge .dg { width:5px; height:5px; border-radius:50%; background:var(--ok); }

/* ─ expander ────────────────────────────────────────────────────────────── */
.streamlit-expanderHeader { background:rgba(255,255,255,.90) !important; border:1px solid var(--brd) !important; border-radius:var(--rad-s) !important; font-family:var(--sans) !important; font-size:.74rem !important; font-weight:600 !important; color:var(--muted) !important; }
.streamlit-expanderContent { background:rgba(255,255,255,.93) !important; border:1px solid var(--brd) !important; border-top:none !important; }

/* ─ history ─────────────────────────────────────────────────────────────── */
.hi { background:var(--white); border:1px solid var(--brd); border-left:3px solid var(--yel); border-radius:var(--rad-s); padding:.65rem .9rem; margin-bottom:.35rem; box-shadow:0 1px 4px rgba(0,71,186,.04); }
.hi .hp { font-size:.78rem; font-weight:500; color:var(--text); margin-bottom:2px; display:-webkit-box; -webkit-line-clamp:1; -webkit-box-orient:vertical; overflow:hidden; }
.hi .hm { font-size:.60rem; color:var(--subtle); }

/* ─ code block ──────────────────────────────────────────────────────────── */
.stCodeBlock { border:1px solid #2D3448 !important; border-radius:var(--rad-s) !important; }
.stCodeBlock pre { background:#1E2433 !important; font-family:var(--mono) !important; font-size:.77rem !important; color:#CDD6F4 !important; }
div[data-testid="stCopyButton"] button { background:rgba(137,220,235,.12) !important; border:1px solid rgba(137,220,235,.25) !important; color:#89DCEB !important; border-radius:5px !important; font-size:.64rem !important; }
div[data-testid="stCopyButton"] button:hover { background:#89DCEB !important; color:#1E2433 !important; }
.stSpinner > div { border-top-color:var(--navy) !important; }
.pdiv { height:1px; background:var(--brd); margin:1rem 0; opacity:.4; }

/* ══════════════ FOOTER ══════════════════════════════════════════════════ */
.foot {
  text-align: center;
  padding: .9rem 0 .4rem;
  border-top: 1px solid var(--brd);
  margin-top: 2.5rem;
}
.foot p { font-family:var(--sans); font-size:.59rem; color:var(--subtle); letter-spacing:.4px; margin:0; }
.foot p+p { margin-top:.18rem; }
.foot strong { color:var(--muted); font-weight:600; }
</style>
""", unsafe_allow_html=True)


# ── session state ─────────────────────────────────────────────────────────────
for k, v in [("history",[]),("qc",0),("tt",0),("lp","")]:
    if k not in st.session_state: st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════
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

def extract_tables(raw):
    return re.findall(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?\W*(\w+)", raw, re.I)

def sys_prompt(dialect, style):
    sm = {"Standard":"Uppercase keywords, clean multi-line formatting.",
          "Compact":"Compact, minimal whitespace.",
          "Annotated":"Add a brief comment above each major clause."}
    return (f"You are TURKCELL SQL AI, expert in {dialect}.\n"
            f"Output ONLY valid {dialect} SQL — no markdown fences, no prose.\n"
            f"{sm.get(style,'')} Use CTEs for complex queries. End with semicolon.\n"
            f"If not a valid SQL request reply exactly: ERROR: Not a valid SQL request.")

def explain_prompt(sql, dialect):
    return (
        f"Aşağıdaki {dialect} SQL sorgusunu kısa ve anlaşılır Türkçe ile açıkla.\n"
        f"Yanıtını SADECE madde madde (bullet list) ver, her madde '•' ile başlasın.\n"
        f"Hangi tabloların kullanıldığını, hangi filtrelerin uygulandığını, "
        f"hangi sütunların döndürüldüğünü ve varsa gruplama/sıralama işlemlerini belirt.\n"
        f"Toplam 4-6 madde yaz, markdown kullanma, sadece düz metin.\n\n"
        f"SQL:\n{sql}"
    )

def user_msg(prompt, schema):
    if not schema: return prompt.strip()
    return (f"=== SCHEMA ===\n{schema.strip()}\n=== END ===\n"
            f"Use ONLY these tables/columns.\nREQUEST: {prompt.strip()}")

def run_sql(prompt, key, dialect, style, model, schema=None):
    t0 = time.time()
    r = openai.OpenAI(api_key=key).chat.completions.create(
        model=model,
        messages=[{"role":"system","content":sys_prompt(dialect,style)},
                  {"role":"user",  "content":user_msg(prompt,schema)}],
        temperature=0.2, max_tokens=1400,
    )
    return {"sql":r.choices[0].message.content.strip(),
            "tokens":r.usage.total_tokens, "elapsed":round(time.time()-t0,2)}

def run_explain(sql, key, dialect, model):
    r = openai.OpenAI(api_key=key).chat.completions.create(
        model=model,
        messages=[{"role":"user","content":explain_prompt(sql,dialect)}],
        temperature=0.3, max_tokens=400,
    )
    return r.choices[0].message.content.strip()

def chk(sql):
    if sql.startswith("ERROR:"): return False, sql[6:].strip()
    if len(sql) < 10: return False, "Model beklenmedik kısa yanıt döndürdü."
    return True, ""

def dl(sql):
    enc = b64lib.b64encode(sql.encode()).decode()
    ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return (f'<div class="dl-wrap"><a href="data:file/sql;base64,{enc}" '
            f'download="query_{ts}.sql">📥 Download SQL</a></div>')

def mk_alert(icon, title, body, v=""):
    return (f'<div class="alert {v}"><div class="alert-h">'
            f'<div class="alert-ic">{icon}</div>'
            f'<div class="alert-title">{title}</div></div>'
            f'<div class="alert-body">{body}</div></div>')

def clipboard_js(sql_escaped):
    """Returns HTML for a copy-to-clipboard button."""
    return f"""
<button class="clip-btn" id="clipbtn"
  onclick="navigator.clipboard.writeText(document.getElementById('sqlraw').textContent)
    .then(()=>{{
      var b=document.getElementById('clipbtn');
      b.textContent='✓ Kopyalandı'; b.classList.add('copied');
      setTimeout(()=>{{b.textContent='📋 Kopyala'; b.classList.remove('copied');}},1800);
    }})">
  📋 Kopyala
</button>
<pre id="sqlraw" style="display:none">{sql_escaped}</pre>
"""


# ── api key ───────────────────────────────────────────────────────────────────
api_key = st.secrets.get("OPENAI_API_KEY","")
if not api_key:
    st.markdown(
        f'<div class="hdr"><div class="hdr-left">'
        f'<img class="hdr-logo" src="{LOGO_SRC}" alt="logo">'
        f'<div class="hdr-vline"></div>'
        f'<div><div class="hdr-title">TURKCELL SQL AI</div>'
        f'<div class="hdr-sub">Natural Language → SQL</div></div>'
        f'</div><div class="hdr-pill">v4.0</div></div>',
        unsafe_allow_html=True)
    st.markdown(mk_alert("🔐","API Anahtarı Bulunamadı",
        '<code>.streamlit/secrets.toml</code> dosyasına ekleyin:'
        '<pre>OPENAI_API_KEY = "sk-..."</pre>'
        'Streamlit Cloud: <strong>App Settings › Secrets</strong>'),
        unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div class="hdr"><div class="hdr-left">'
    f'<img class="hdr-logo" src="{LOGO_SRC}" alt="logo">'
    f'<div class="hdr-vline"></div>'
    f'<div><div class="hdr-title">TURKCELL SQL AI</div>'
    f'<div class="hdr-sub">Natural Language → SQL</div></div>'
    f'</div><div class="hdr-pill">v4.0 · OpenAI</div></div>',
    unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  UPLOAD CARD
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown('<p class="upload-lbl">📂 Veritabanı Şemasını Yükle (.sql, .txt)</p>', unsafe_allow_html=True)

uf = st.file_uploader("sf", type=["sql","txt"],
                      accept_multiple_files=False,
                      label_visibility="collapsed")
schema_text, schema_meta = None, {}

if uf:
    try:
        raw, chars, tables = parse_schema(uf)
        if chars > 80_000:
            st.markdown(mk_alert("⚠️","Dosya Çok Büyük",
                "Şema 80 KB limitini aşıyor. Kullanılmayan tabloları kaldırın.","warn"),
                unsafe_allow_html=True)
        else:
            schema_text = raw
            tbl_names   = extract_tables(raw)
            schema_meta = {"name":uf.name,"tables":len(tbl_names),"chars":chars}
            MAX_SHOW    = 14
            chips = "".join(f'<span class="tbl-chip">⬡ {t}</span>' for t in tbl_names[:MAX_SHOW])
            if len(tbl_names) > MAX_SHOW:
                chips += f'<span class="tbl-more">+{len(tbl_names)-MAX_SHOW} daha</span>'
            st.markdown(
                f'<div class="schema-ok"><span class="dot"></span>'
                f'<strong>{uf.name}</strong> yüklendi — {len(tbl_names)} tablo · {chars:,} karakter</div>'
                + (f'<div class="tbl-row">{chips}</div>' if chips else ""),
                unsafe_allow_html=True)
    except Exception as e:
        st.markdown(mk_alert("❌","Dosya Hatası",f"Okunamadı: {e}"),unsafe_allow_html=True)

st.markdown(
    '<div class="upload-help">💡 <strong>İpucu:</strong> ' +
    '<code>pg_dump --schema-only</code> (PostgreSQL) veya ' +
    '<code>SHOW CREATE TABLE</code> (MySQL) ile şemanızı dışa aktarıp ' +
    '<code>.sql</code> dosyası olarak kaydedin.</div>',
    unsafe_allow_html=True)

if not uf:
    st.markdown(mk_alert("ℹ️","Şema Yüklenmedi — Genel Bilgi Kullanılıyor",
        "AI tablo/sütun isimlerini açıklamanızdan çıkaracak. "
        "Daha doğru sonuçlar için şema dosyası yükleyin.","info"),
        unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  FORM CARD: configuration + prompt
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<p class="lbl">⚙ Yapılandırma</p>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    dialect = st.selectbox("Dialect",
        ["PostgreSQL","MySQL","SQLite","SQL Server (T-SQL)","BigQuery","Snowflake"],key="d")
with c2:
    style = st.selectbox("Stil",["Standard","Annotated","Compact"],key="s")
with c3:
    model = st.selectbox("Model",["gpt-4o","gpt-4o-mini","gpt-4-turbo"],key="m")

st.markdown('<div class="card-sep"></div>', unsafe_allow_html=True)

if schema_text:
    st.markdown(
        f'<div class="sbadge"><span class="dg"></span>' +
        f'Şema Modu · {schema_meta["name"]} · {schema_meta["tables"]} tablo</div>',
        unsafe_allow_html=True)

st.markdown('<p class="lbl">✦ Doğal Dil ile Açıkla</p>', unsafe_allow_html=True)
prompt = st.text_area("p", value=st.session_state.lp, height=120,
    placeholder="Örn. → Geçen ay kaydolan ama henüz sipariş vermemiş kullanıcıları referans kaynağına göre gruplandır…",
    key="pk", label_visibility="collapsed")

go = st.button("⚡  SQL Oluştur", key="go")

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  GENERATE
# ══════════════════════════════════════════════════════════════════════════
if go:
    st.session_state.lp = prompt
    if not prompt.strip():
        st.markdown(mk_alert("✏️","Boş Prompt",
            "Lütfen SQL üretmek için bir açıklama girin.","warn"),
            unsafe_allow_html=True)
        st.stop()

    with st.spinner("SQL oluşturuluyor…"):
        try:
            res = run_sql(prompt, api_key, dialect, style, model, schema_text)
        except openai.AuthenticationError:
            st.markdown(mk_alert("🔑","Kimlik Hatası",
                "API anahtarı reddedildi."),unsafe_allow_html=True); st.stop()
        except openai.RateLimitError:
            st.markdown(mk_alert("⏱","Limit Aşıldı",
                "OpenAI kotası doldu. Kısa süre bekleyip tekrar deneyin."),
                unsafe_allow_html=True); st.stop()
        except openai.APIConnectionError:
            st.markdown(mk_alert("🌐","Bağlantı Hatası",
                "OpenAI API'ye ulaşılamadı."),unsafe_allow_html=True); st.stop()
        except Exception as e:
            st.markdown(mk_alert("⚙️","Beklenmeyen Hata",
                f"Sorun oluştu:<br><code>{e}</code>"),
                unsafe_allow_html=True); st.stop()

    valid, err = chk(res["sql"])
    if not valid:
        st.markdown(mk_alert("⚠️","Model Bildirimi",err,"warn"),
            unsafe_allow_html=True); st.stop()

    # store history
    st.session_state.qc += 1
    st.session_state.tt += res["tokens"]
    st.session_state.history.insert(0,{
        "prompt":prompt,"sql":res["sql"],"dialect":dialect,
        "ts":datetime.datetime.now().strftime("%d %b %Y %H:%M"),
        "tokens":res["tokens"],
        "schema":schema_meta.get("name","—") if schema_text else "—",
    })
    st.session_state.history = st.session_state.history[:30]

    # ── dark SQL card ─────────────────────────────────────────────────────
    sb = ""
    if schema_text:
        sb = ('<span class="sql-tag" style="background:rgba(166,227,161,.12);color:#A6E3A1;">' +
              '<span class="dot" style="background:#A6E3A1"></span>' +
              f'{schema_meta["name"]}</span>')

    sql_esc = res["sql"].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"','&quot;').replace("'","&#39;")

    st.markdown(
        f'<div class="sql-card">'
        f'<pre>{hl(res["sql"])}</pre>'
        f'<div class="sql-bar">'
        f'<span class="sql-tag"><span class="dot"></span>{dialect}</span>'
        f'<div style="display:flex;gap:.45rem;align-items:center;">{sb}'
        + clipboard_js(sql_esc) +
        f'<span class="sql-tag">{res["elapsed"]}s · {res["tokens"]} tok</span>'
        f'</div></div></div>',
        unsafe_allow_html=True)

    # native copy button + download (secondary)
    col_code, col_dl = st.columns([4, 1])
    with col_code:
        st.code(res["sql"], language="sql")
    with col_dl:
        st.markdown(dl(res["sql"]), unsafe_allow_html=True)

    # stats
    st.markdown(
        f'<div class="stats">'
        f'<div class="stat"><div class="v">{st.session_state.qc}</div><div class="l">Sorgular</div></div>'
        f'<div class="stat"><div class="v">{res["elapsed"]}s</div><div class="l">Süre</div></div>'
        f'<div class="stat"><div class="v">{st.session_state.tt}</div><div class="l">Token</div></div>'
        f'</div>',
        unsafe_allow_html=True)

    # ── SQL EXPLANATION ───────────────────────────────────────────────────
    st.markdown(
        '<div class="exp-card">'
        '<div class="exp-title">💡 Sorgu Açıklaması</div>'
        '<p class="exp-loading">Türkçe açıklama oluşturuluyor…</p>'
        '</div>',
        unsafe_allow_html=True)

    with st.spinner(""):
        try:
            explanation = run_explain(res["sql"], api_key, dialect, model)
            lines = [l.strip().lstrip("•-* ").strip()
                     for l in explanation.splitlines() if l.strip()]
            bullets = "".join(f"<li>{l}</li>" for l in lines if l)
            st.markdown(
                '<div class="exp-card">'
                '<div class="exp-title">💡 Sorgu Açıklaması</div>'
                f'<ul>{bullets}</ul>'
                '</div>',
                unsafe_allow_html=True)
        except Exception:
            pass   # explanation is non-critical, fail silently


# ══════════════════════════════════════════════════════════════════════════
#  HISTORY
# ══════════════════════════════════════════════════════════════════════════
if st.session_state.history:
    st.markdown('<div class="pdiv"></div>', unsafe_allow_html=True)
    with st.expander(f"📜  Sorgu Geçmişi  ({len(st.session_state.history)} kayıt)", expanded=False):
        for i, e in enumerate(st.session_state.history):
            tag = f" · 🗄 {e['schema']}" if e.get("schema") and e["schema"] != "—" else ""
            st.markdown(
                f'<div class="hi"><div class="hp">{e["prompt"]}</div>'
                f'<div class="hm">{e["ts"]} · {e["dialect"]}{tag} · {e["tokens"]} tok</div></div>',
                unsafe_allow_html=True)
            st.code(e["sql"], language="sql")
            st.markdown(dl(e["sql"]), unsafe_allow_html=True)
            if i < len(st.session_state.history)-1:
                st.markdown('<div style="height:.15rem"></div>', unsafe_allow_html=True)
        st.markdown('<div style="height:.25rem"></div>', unsafe_allow_html=True)
        if st.button("🗑  Geçmişi Temizle", key="clr"):
            st.session_state.update({"history":[],"qc":0,"tt":0})
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="foot">'
    '<p>© 2026 <strong>TURKCELL SQL AI</strong> | L2 DevOps Operations | Powered by OpenAI</p>'
    '<p>Global Bilgi · Streamlit · Tüm hakları saklıdır.</p>'
    '</div>',
    unsafe_allow_html=True)