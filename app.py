"""
TURKCELL SQL AI — app.py v10
New logo (Global Bilgi) · Sidebar fixed · Single card · Clean layout
"""

import streamlit as st
import openai
import re, time, datetime, base64 as b64lib

# ── Logo (gömülü base64, dışa bağımlılık yok) ─────────────────────────────
LOGO_B64 = "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"
LOGO_SRC  = f"data:image/png;base64,{LOGO_B64}"

st.set_page_config(
    page_title="TURKCELL SQL AI",
    page_icon="🟡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  CSS  —  sıfırdan, çakışmasız
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Roboto+Mono:wght@400;500&display=swap');

/* ── tokens ── */
:root {
  --blue:      #0047BA;
  --blue-dk:   #002D72;
  --blue-lt:   #EBF3FF;
  --yellow:    #FFD100;
  --yellow-dk: #C9A800;
  --text:      #111827;
  --muted:     #6B7280;
  --light:     #9CA3AF;
  --border:    #E2E8F0;
  --success:   #059669;
  --sans:      'Inter', system-ui, sans-serif;
  --mono:      'Roboto Mono', monospace;
  --r:         14px;
  --r-sm:      8px;
}

/* ── arka plan ── */
html, body {
  background: linear-gradient(165deg,#f9fbff 0%,#edf3fc 100%) !important;
  min-height: 100vh;
}

/* ── tüm Streamlit sarmalayıcıları şeffaf ── */
.stApp,
.stApp > div,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section.main,
section.main > div,
.block-container { background: transparent !important; }

/* ── Streamlit chrome gizle ── */
#MainMenu, footer, header { visibility: hidden !important; height: 0 !important; }

/* ── scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: var(--blue); border-radius: 4px; }

/* ── ana container: 800px ortalı ── */
.block-container {
  max-width: 800px !important;
  padding: 0 1.25rem 5rem !important;
  margin: 0 auto !important;
  font-family: var(--sans) !important;
}

/* ════════════ HEADER ════════════════════════════════════════════════════════ */
.tc-hdr {
  background: linear-gradient(90deg,#001A5E 0%,#0047BA 100%);
  margin: 0 -1.25rem 2rem;
  padding: 0 1.8rem;
  height: 56px;
  display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 3px 16px rgba(0,30,110,.26);
  position: relative; overflow: hidden;
}
.tc-hdr::after {
  content:""; position:absolute; inset:0;
  background:linear-gradient(90deg,transparent 55%,rgba(255,255,255,.04));
  pointer-events:none;
}
.tc-hdr-left { display:flex; align-items:center; gap:14px; z-index:1; }

/* logo: beyaz pill kapsayıcı */
.tc-hdr-logo-wrap {
  height: 36px;
  background: rgba(255,255,255,.96);
  border-radius: 8px;
  padding: 4px 10px;
  display: flex; align-items: center;
}
.tc-hdr-logo-wrap img { height: 28px; width: auto; display: block; }

.tc-hdr-name {
  font-family:var(--sans); font-size:1rem; font-weight:800;
  color:#fff; letter-spacing:.5px; line-height:1.2;
}
.tc-hdr-sub {
  font-size:.54rem; font-weight:400;
  color:rgba(255,255,255,.45); letter-spacing:2px;
  text-transform:uppercase; margin-top:2px;
}
.tc-hdr-pill {
  z-index:1;
  background:rgba(255,255,255,.11); border:1px solid rgba(255,255,255,.20);
  border-radius:20px; padding:4px 14px;
  font-size:.58rem; font-weight:600;
  color:rgba(255,255,255,.76); letter-spacing:1px; text-transform:uppercase;
}

/* ════════════ SIDEBAR ═══════════════════════════════════════════════════════
   Streamlit sidebar 7+ katmanlı — hepsini kapatıyoruz
════════════════════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div > div,
[data-testid="stSidebarContent"],
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] [data-testid="stVerticalBlock"],
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
  background: #0047BA !important;
  border-right: none !important;
}
[data-testid="stSidebar"] {
  box-shadow: 4px 0 24px rgba(0,20,90,.22) !important;
  min-width: 230px !important;
}
/* sidebar içindeki tüm metin elementleri beyaz */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span:not(.sb-top-title),
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stMarkdown p {
  color: rgba(255,255,255,.82) !important;
  font-family: var(--sans) !important;
}
/* sidebar üst başlık şeridi */
.sb-top {
  background: rgba(0,0,0,.22);
  padding: .9rem 1.1rem;
  border-bottom: 1px solid rgba(255,255,255,.10);
  margin-bottom: 1.2rem;
  display: flex; align-items: center; gap: 9px;
}
.sb-top-title {
  font-family:var(--sans) !important; font-size:.68rem !important;
  font-weight:700 !important; color:rgba(255,255,255,.92) !important;
  letter-spacing:2.2px !important; text-transform:uppercase !important;
}
/* sidebar label */
.sb-lbl {
  font-family:var(--sans) !important; font-size:.56rem !important;
  font-weight:700 !important; color:rgba(255,255,255,.42) !important;
  letter-spacing:2.4px !important; text-transform:uppercase !important;
  margin-bottom:.5rem; display:flex; align-items:center; gap:6px;
}
.sb-lbl::before {
  content:""; width:3px; height:10px; background:var(--yellow);
  border-radius:2px; flex-shrink:0;
}
/* file uploader — koyu sidebar üzerinde */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
  background: rgba(255,255,255,.07) !important;
  border: 1.5px dashed rgba(255,255,255,.28) !important;
  border-radius: var(--r-sm) !important;
  transition: border-color .2s !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
  border-color: var(--yellow) !important;
  background: rgba(255,209,0,.06) !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] label { display:none !important; }
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] p {
  color: rgba(255,255,255,.40) !important; font-size:.68rem !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] small {
  color: rgba(255,255,255,.26) !important; font-size:.58rem !important;
}
/* şema önizleme kartı */
.sb-schema {
  background: rgba(0,0,0,.25); border:1px solid rgba(255,255,255,.10);
  border-left:3px solid var(--yellow); border-radius:var(--r-sm);
  padding:.75rem .9rem; margin-top:.65rem;
  max-height:220px; overflow-y:auto;
}
.sb-schema pre {
  font-family:var(--mono) !important; font-size:.62rem !important;
  line-height:1.7 !important; color:rgba(255,255,255,.65) !important;
  margin:0 !important; white-space:pre-wrap !important; word-break:break-word !important;
}
.sb-ok {
  display:flex; align-items:center; gap:6px; margin-top:.65rem;
  font-size:.61rem !important; font-weight:600 !important; color:#4ADE80 !important;
}
.sb-ok .dg { width:6px; height:6px; border-radius:50%; background:#4ADE80; flex-shrink:0; }
.sb-none {
  font-size:.67rem !important; color:rgba(255,255,255,.30) !important;
  line-height:1.8; padding:.2rem 0;
}
.sb-hr { height:1px; background:rgba(255,255,255,.10); margin:.9rem 0; }
.sb-tip {
  font-family:var(--mono) !important; font-size:.57rem !important;
  color:rgba(255,255,255,.30) !important; line-height:1.85;
  padding:.6rem .8rem; background:rgba(0,0,0,.18);
  border-radius:var(--r-sm); border-left:2px solid rgba(255,209,0,.45);
}
.sb-tip code { color:var(--yellow) !important; }
.sb-tip strong { color:rgba(255,255,255,.52) !important; }

/* ════════════ ANA KART ══════════════════════════════════════════════════════ */
.main-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 15px;
  box-shadow: 0 4px 28px rgba(0,0,0,.06), 0 1px 5px rgba(0,71,186,.04);
  padding: 1.9rem 2rem 2.1rem;
  margin-bottom: 1.2rem;
}
.card-sep { height:1px; background:#F0F4FA; margin:1.3rem 0; }

/* ── section labels ── */
.tc-lbl {
  font-size:.63rem !important; font-weight:700 !important;
  color:var(--blue-dk) !important; letter-spacing:1.8px; text-transform:uppercase;
  margin-bottom:.55rem !important; display:flex; align-items:center; gap:7px;
}
.tc-lbl::before {
  content:""; width:3px; height:13px; background:var(--yellow);
  border-radius:2px; flex-shrink:0;
}

/* ── selects ── */
.stSelectbox label {
  font-size:.62rem !important; font-weight:700 !important;
  color:var(--muted) !important; text-transform:uppercase !important; letter-spacing:.9px !important;
}
.stSelectbox > div > div {
  background:#fafcff !important; border:1.5px solid var(--border) !important;
  border-radius:var(--r-sm) !important; font-family:var(--sans) !important;
  font-size:.84rem !important; color:var(--text) !important; transition:border-color .18s !important;
}
.stSelectbox > div > div:focus-within {
  border-color:var(--blue) !important; box-shadow:0 0 0 3px rgba(0,71,186,.10) !important;
}
div[data-baseweb="select"] * { background:#fff !important; color:var(--text) !important; }
div[data-baseweb="popover"] * { background:#fff !important; border-color:var(--border) !important; color:var(--text) !important; }

/* ── textarea ── */
.stTextArea label { display:none !important; }
.stTextArea textarea {
  background:#fafcff !important; border:1.5px solid var(--border) !important;
  border-radius:var(--r-sm) !important; font-family:var(--sans) !important;
  font-size:.88rem !important; line-height:1.65 !important;
  color:var(--text) !important; padding:11px 13px !important; resize:vertical !important;
  transition:border-color .18s, box-shadow .18s !important;
}
.stTextArea textarea:focus {
  border-color:var(--blue) !important; background:#fff !important;
  box-shadow:0 0 0 3px rgba(0,71,186,.10) !important; outline:none !important;
}
.stTextArea textarea::placeholder { color:var(--light) !important; }

/* ── buton ── */
.stButton > button {
  background:var(--yellow) !important; color:#001A5E !important;
  font-family:var(--sans) !important; font-weight:700 !important;
  font-size:.875rem !important; border:none !important;
  border-radius:var(--r-sm) !important;
  padding:.65rem 0 !important; width:240px !important;
  display:block !important; margin:.5rem auto 0 !important;
  cursor:pointer !important;
  transition:background .15s, box-shadow .15s, transform .10s !important;
  box-shadow:0 3px 12px rgba(255,209,0,.28) !important;
}
.stButton > button:hover {
  background:var(--yellow-dk) !important;
  box-shadow:0 5px 20px rgba(200,168,0,.36) !important;
  transform:translateY(-1px) !important;
}
.stButton > button:active { transform:translateY(0) !important; }

/* ════════════ SQL KART ══════════════════════════════════════════════════════ */
.sql-card {
  background:#fff; border:1px solid var(--border);
  border-top:3px solid var(--blue); border-radius:15px;
  padding:1.3rem 1.5rem 1.1rem;
  box-shadow:0 4px 22px rgba(0,0,0,.05); margin-top:.5rem;
}
.sql-card pre {
  font-family:var(--mono) !important; font-size:.79rem !important;
  line-height:1.78 !important; color:var(--text) !important;
  margin:0 !important; white-space:pre-wrap !important; word-break:break-word !important;
}
.kw  { color:#0047BA; font-weight:700; }
.fn  { color:#047857; }
.str { color:#B91C1C; }
.cmt { color:#9CA3AF; font-style:italic; }
.num { color:#7C3AED; }
.sql-bar {
  display:flex; align-items:center; justify-content:space-between;
  margin-top:.9rem; padding-top:.75rem; border-top:1px solid #F0F4FA;
}
.sql-tag {
  display:inline-flex; align-items:center; gap:5px;
  background:var(--blue-lt); border-radius:20px; padding:3px 10px;
  font-size:.61rem; font-weight:600; color:var(--blue-dk);
}
.sql-tag .dot { width:6px; height:6px; border-radius:50%; background:var(--success); }

/* ── indirme butonu ── */
.dl-wrap { margin-top:.75rem; }
.dl-wrap a {
  display:inline-flex; align-items:center; gap:6px;
  background:var(--blue-lt); border:1.5px solid var(--blue);
  border-radius:var(--r-sm); padding:.42rem 1rem;
  font-size:.76rem; font-weight:600; color:var(--blue);
  text-decoration:none; transition:background .15s, color .15s;
}
.dl-wrap a:hover { background:var(--blue); color:#fff; }

/* ── stats ── */
.stats-row { display:flex; gap:.7rem; margin-top:.9rem; }
.stat {
  flex:1; background:#fff; border:1px solid var(--border);
  border-radius:var(--r-sm); padding:.82rem; text-align:center;
  box-shadow:0 1px 5px rgba(0,71,186,.04); transition:box-shadow .18s, transform .15s;
}
.stat:hover { box-shadow:0 4px 14px rgba(0,71,186,.10); transform:translateY(-1px); }
.stat .v { font-size:1.15rem; font-weight:800; color:var(--blue); }
.stat .l { font-size:.58rem; font-weight:700; color:var(--muted); letter-spacing:.8px; text-transform:uppercase; margin-top:2px; }

/* ════════════ KURUMSAL UYARI PANELI ═════════════════════════════════════════ */
.corp-alert {
  background:#fff; border:1px solid #BFDBFE; border-left:4px solid var(--blue);
  border-radius:var(--r); padding:1.4rem 1.6rem; margin-top:1rem;
  box-shadow:0 2px 12px rgba(0,71,186,.08); font-family:var(--sans);
}
.corp-alert.warn { border-left-color:#D97706; border-color:#FDE68A; }
.corp-alert-hd { display:flex; align-items:center; gap:10px; margin-bottom:.65rem; }
.corp-alert-icon {
  width:32px; height:32px; border-radius:8px; background:var(--blue-lt);
  display:flex; align-items:center; justify-content:center; font-size:.9rem; flex-shrink:0;
}
.corp-alert.warn .corp-alert-icon { background:#FFFBEB; }
.corp-alert-title { font-size:.88rem; font-weight:700; color:var(--blue-dk); }
.corp-alert.warn .corp-alert-title { color:#92400E; }
.corp-alert-body { font-size:.80rem; color:var(--muted); line-height:1.65; padding-left:42px; }
.corp-alert-body code { background:var(--blue-lt); padding:1px 6px; border-radius:4px; font-family:var(--mono); font-size:.74rem; color:var(--blue); }
.corp-alert-body pre { background:#F8FAFF; border:1px solid #DBEAFE; border-radius:6px; padding:7px 12px; font-family:var(--mono); font-size:.74rem; color:var(--blue-dk); margin:.5rem 0 .2rem; }

/* ── schema badge ── */
.schema-badge {
  display:inline-flex; align-items:center; gap:6px;
  background:rgba(5,150,105,.08); border:1px solid rgba(5,150,105,.24);
  border-radius:20px; padding:3px 12px;
  font-size:.62rem; font-weight:600; color:var(--success); margin-bottom:.7rem;
}
.schema-badge .dg { width:6px; height:6px; border-radius:50%; background:var(--success); }

/* ── expander ── */
.streamlit-expanderHeader {
  background:rgba(255,255,255,.88) !important; border:1px solid var(--border) !important;
  border-radius:var(--r-sm) !important; font-family:var(--sans) !important;
  font-size:.75rem !important; font-weight:600 !important; color:var(--muted) !important;
}
.streamlit-expanderContent {
  background:rgba(255,255,255,.92) !important; border:1px solid var(--border) !important; border-top:none !important;
}

/* ── history item ── */
.h-item {
  background:#fff; border:1px solid var(--border); border-left:3px solid var(--yellow);
  border-radius:var(--r-sm); padding:.7rem .95rem; margin-bottom:.4rem;
  box-shadow:0 1px 4px rgba(0,71,186,.04);
}
.h-item .hp { font-size:.80rem; font-weight:500; color:var(--text); margin-bottom:2px; display:-webkit-box; -webkit-line-clamp:1; -webkit-box-orient:vertical; overflow:hidden; }
.h-item .hm { font-size:.61rem; color:var(--light); }

/* ── code block ── */
.stCodeBlock { border:1px solid var(--border) !important; border-radius:var(--r-sm) !important; }
.stCodeBlock pre { background:#f8fafc !important; font-family:var(--mono) !important; font-size:.78rem !important; }
div[data-testid="stCopyButton"] button { background:var(--blue-lt) !important; border:1px solid var(--border) !important; color:var(--blue) !important; border-radius:5px !important; font-size:.66rem !important; }
div[data-testid="stCopyButton"] button:hover { background:var(--blue) !important; color:#fff !important; }
.stSpinner > div { border-top-color:var(--blue) !important; }
.page-div { height:1px; background:var(--border); margin:1.3rem 0; opacity:.4; }

/* ════════════ FOOTER ════════════════════════════════════════════════════════ */
.tc-footer {
  text-align:center; margin-top:3.5rem;
  padding:1.1rem 0 .5rem; border-top:1px solid var(--border);
}
.tc-footer p { font-family:var(--sans); font-size:.60rem; color:var(--light); letter-spacing:.5px; margin:0; }
.tc-footer p + p { margin-top:.25rem; }
.tc-footer strong { color:var(--muted); font-weight:600; }
</style>
""", unsafe_allow_html=True)


# ─── Session state ────────────────────────────────────────────────────────────
for k, v in [("history",[]),("qc",0),("tt",0),("lp","")]:
    if k not in st.session_state: st.session_state[k] = v


# ─── Helpers ──────────────────────────────────────────────────────────────────
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
    sm = {"Standard": "Uppercase keywords, clean multi-line formatting.",
          "Compact":  "Compact, minimal whitespace.",
          "Annotated":"Add a brief comment above each major clause."}
    return (f"You are TURKCELL SQL AI, expert in {dialect}.\n"
            f"Output ONLY valid {dialect} SQL — no markdown fences, no prose.\n"
            f"{sm.get(style,'')} Use CTEs for complex queries. End with semicolon.\n"
            f"If not a valid SQL request reply exactly: ERROR: Not a valid SQL request.")

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
            "tokens":r.usage.total_tokens,
            "elapsed":round(time.time()-t0,2)}

def validate(sql):
    if sql.startswith("ERROR:"): return False, sql[6:].strip()
    if len(sql) < 10:            return False, "Model beklenmedik kısa yanıt döndürdü."
    return True, ""

def dl_link(sql):
    enc = b64lib.b64encode(sql.encode()).decode()
    ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return (f'<div class="dl-wrap"><a href="data:file/sql;base64,{enc}" ' +
            f'download="query_{ts}.sql">📥 SQL Olarak İndir</a></div>')

def corp_alert(icon, title, body, extra=""):
    return f"""<div class="corp-alert {extra}">
      <div class="corp-alert-hd">
        <div class="corp-alert-icon">{icon}</div>
        <div class="corp-alert-title">{title}</div>
      </div>
      <div class="corp-alert-body">{body}</div>
    </div>"""


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-top">
      <span style="font-size:.9rem">🗄️</span>
      <span class="sb-top-title">Şema Bağlamı</span>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="padding:0 1.1rem">', unsafe_allow_html=True)
    st.markdown('<p class="sb-lbl">📂 Şema Dosyası Yükle</p>', unsafe_allow_html=True)

    uf = st.file_uploader("schema_uploader", type=["sql","txt"],
                          accept_multiple_files=False,
                          label_visibility="collapsed")
    schema_text, schema_meta = None, {}

    if uf:
        try:
            raw, chars, tables = parse_schema(uf)
            if chars > 80_000:
                st.markdown(corp_alert("⚠️","Dosya Çok Büyük",
                    "Şema dosyası 80 KB limitini aşıyor.", "warn"),
                    unsafe_allow_html=True)
            else:
                schema_text = raw
                schema_meta = {"name":uf.name,"tables":tables,"chars":chars}
                prev = raw[:700] + ("\n…" if len(raw)>700 else "")
                st.markdown(f"""
                <div class="sb-schema"><pre>{prev}</pre></div>
                <div class="sb-ok"><span class="dg"></span>
                {tables} tablo · {chars:,} karakter</div>""",
                unsafe_allow_html=True)
        except Exception as e:
            st.markdown(corp_alert("❌","Dosya Hatası",f"Okunamadı: {e}"),
                        unsafe_allow_html=True)
    else:
        st.markdown("""<p class="sb-none">Şema yüklenmedi.<br>
        AI genel bilgisiyle tahmin eder.</p>""", unsafe_allow_html=True)

    st.markdown("""<div class="sb-hr"></div>
    <div class="sb-tip">💡 <strong>İpucu:</strong><br>
    <code>pg_dump --schema-only</code><br>
    <code>SHOW CREATE TABLE t</code> (MySQL)
    </div></div>""", unsafe_allow_html=True)


# ─── API Key ──────────────────────────────────────────────────────────────────
api_key = st.secrets.get("OPENAI_API_KEY","")
if not api_key:
    st.markdown(corp_alert("🔐","API Anahtarı Bulunamadı",
        """Uygulamanın çalışması için OpenAI API anahtarı gereklidir.<br><br>
        <code>.streamlit/secrets.toml</code> dosyasına ekleyin:<pre>OPENAI_API_KEY = "sk-..."</pre>
        Streamlit Cloud: <strong>App Settings › Secrets</strong>"""
    ), unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="tc-hdr">
  <div class="tc-hdr-left">
    <div class="tc-hdr-logo-wrap">
      <img src="{LOGO_SRC}" alt="Global Bilgi">
    </div>
    <div>
      <div class="tc-hdr-name">TURKCELL SQL AI</div>
      <div class="tc-hdr-sub">Natural Language → SQL</div>
    </div>
  </div>
  <div class="tc-hdr-pill">OpenAI Destekli</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ANA KART
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown('<p class="tc-lbl">⚙ Yapılandırma</p>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    dialect = st.selectbox("Dialect",
        ["PostgreSQL","MySQL","SQLite","SQL Server (T-SQL)","BigQuery","Snowflake"], key="d")
with c2:
    style = st.selectbox("Stil", ["Standard","Annotated","Compact"], key="s")
with c3:
    model = st.selectbox("Model", ["gpt-4o","gpt-4o-mini","gpt-4-turbo"], key="m")

st.markdown('<div class="card-sep"></div>', unsafe_allow_html=True)

if schema_text:
    st.markdown(f"""<div class="schema-badge">
    <span class="dg"></span>
    Şema Modu Aktif &nbsp;·&nbsp; {schema_meta['name']} &nbsp;·&nbsp; {schema_meta['tables']} tablo
    </div>""", unsafe_allow_html=True)

st.markdown('<p class="tc-lbl">✦ Doğal Dil ile Açıkla</p>', unsafe_allow_html=True)
prompt = st.text_area("p_area", value=st.session_state.lp, height=125,
    placeholder="Örn. → Geçen ay kaydolan ama henüz sipariş vermemiş kullanıcıları referans kaynağına göre gruplandır…",
    key="p_key", label_visibility="collapsed")

go = st.button("⚡  SQL Oluştur", key="go_btn")

st.markdown('</div>', unsafe_allow_html=True)   # /main-card


# ══════════════════════════════════════════════════════════════════════════════
#  GENERATE
# ══════════════════════════════════════════════════════════════════════════════
if go:
    st.session_state.lp = prompt
    if not prompt.strip():
        st.markdown(corp_alert("✏️","Boş Prompt",
            "Lütfen SQL üretmek için bir açıklama girin.","warn"),
            unsafe_allow_html=True)
        st.stop()

    with st.spinner("SQL oluşturuluyor…"):
        try:
            res = run_sql(prompt, api_key, dialect, style, model, schema_text)
        except openai.AuthenticationError:
            st.markdown(corp_alert("🔑","Kimlik Doğrulama Hatası",
                "API anahtarınız reddedildi. Geçerli ve aktif olduğunu kontrol edin."),
                unsafe_allow_html=True); st.stop()
        except openai.RateLimitError:
            st.markdown(corp_alert("⏱","İstek Limiti Aşıldı",
                "OpenAI kota limitinize ulaşıldı. Birkaç saniye bekleyip tekrar deneyin."),
                unsafe_allow_html=True); st.stop()
        except openai.APIConnectionError:
            st.markdown(corp_alert("🌐","Bağlantı Hatası",
                "OpenAI API'ye ulaşılamadı. İnternet bağlantınızı kontrol edin."),
                unsafe_allow_html=True); st.stop()
        except Exception as e:
            st.markdown(corp_alert("⚙️","Beklenmeyen Hata",
                f"İşlem sırasında sorun oluştu:<br><code>{e}</code>"),
                unsafe_allow_html=True); st.stop()

    ok, err = validate(res["sql"])
    if not ok:
        st.markdown(corp_alert("⚠️","Model Bildirimi",err,"warn"),
            unsafe_allow_html=True); st.stop()

    st.session_state.qc += 1
    st.session_state.tt += res["tokens"]
    st.session_state.history.insert(0,{
        "prompt":prompt, "sql":res["sql"], "dialect":dialect,
        "ts":datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        "tokens":res["tokens"],
        "schema":schema_meta.get("name","—") if schema_text else "—",
    })
    st.session_state.history = st.session_state.history[:30]

    sb = ""
    if schema_text:
        sb = (f'<span class="sql-tag" style="background:#D1FAE5;color:#065F46;">' +
              f'<span class="dot" style="background:#059669"></span>' +
              f'{schema_meta["name"]}</span>')

    st.markdown(f"""
    <div class="sql-card">
      <pre>{hl(res["sql"])}</pre>
      <div class="sql-bar">
        <span class="sql-tag"><span class="dot"></span>{dialect}</span>
        <div style="display:flex;gap:.5rem;align-items:center;">
          {sb}
          <span class="sql-tag">{res["elapsed"]}s · {res["tokens"]} token</span>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.code(res["sql"], language="sql")
    st.markdown(dl_link(res["sql"]), unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stats-row">
      <div class="stat"><div class="v">{st.session_state.qc}</div><div class="l">Toplam Sorgu</div></div>
      <div class="stat"><div class="v">{res["elapsed"]}s</div><div class="l">Yanıt Süresi</div></div>
      <div class="stat"><div class="v">{st.session_state.tt}</div><div class="l">Token</div></div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SORGU GEÇMİŞİ
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.history:
    st.markdown('<div class="page-div"></div>', unsafe_allow_html=True)
    with st.expander(f"📜  Sorgu Geçmişi  ({len(st.session_state.history)} kayıt)", expanded=False):
        for i, e in enumerate(st.session_state.history):
            tag = f" · 🗄 {e['schema']}" if e.get("schema") and e["schema"] != "—" else ""
            st.markdown(f"""<div class="h-item">
            <div class="hp">{e["prompt"]}</div>
            <div class="hm">{e["ts"]} · {e["dialect"]}{tag} · {e["tokens"]} token</div>
            </div>""", unsafe_allow_html=True)
            st.code(e["sql"], language="sql")
            st.markdown(dl_link(e["sql"]), unsafe_allow_html=True)
            if i < len(st.session_state.history)-1:
                st.markdown('<div style="height:.2rem"></div>', unsafe_allow_html=True)
        st.markdown('<div style="height:.35rem"></div>', unsafe_allow_html=True)
        if st.button("🗑  Geçmişi Temizle", key="clr"):
            st.session_state.update({"history":[],"qc":0,"tt":0})
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="tc-footer">
  <p>© {datetime.datetime.now().year} <strong>TURKCELL SQL AI</strong> &nbsp;|&nbsp; L2 DevOps Operations</p>
  <p>OpenAI ile güçlendirilmiştir &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; Tüm hakları saklıdır.</p>
</div>""", unsafe_allow_html=True)