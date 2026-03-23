"""
TURKCELL SQL AI — app.py v9
Clean · Single card · Sidebar restored · Corporate footer
"""

import streamlit as st
import openai
import re, time, datetime, base64 as b64lib

LOGO_B64 = "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"
LOGO_SRC  = f"data:image/png;base64,{LOGO_B64}"

st.set_page_config(
    page_title="TURKCELL SQL AI",
    page_icon="🟡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Roboto+Mono:wght@400;500&display=swap');

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
  --error:     #C53030;
  --warn:      #B7791F;
  --sans:      'Inter', system-ui, sans-serif;
  --mono:      'Roboto Mono', monospace;
  --r:         12px;
  --r-sm:      8px;
}

/* ── RESET ── */
*, *::before, *::after { box-sizing: border-box; }

/* ── ARKA PLAN ── */
html, body {
  background: linear-gradient(170deg, #f8fbff 0%, #edf3fc 100%) !important;
  min-height: 100vh;
}
.stApp,
.stApp > div,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section.main,
section.main > div { background: transparent !important; font-family: var(--sans) !important; }

/* ── STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden !important; }

/* ── CONTAINER: 820px ortalı ── */
.block-container {
  max-width: 820px !important;
  padding: 0 1.2rem 5rem !important;
  margin: 0 auto !important;
  background: transparent !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: var(--blue); border-radius: 4px; }

/* ════════════════════════════════════════
   HEADER
════════════════════════════════════════ */
.tc-hdr {
  background: linear-gradient(90deg, #001A5E 0%, #0047BA 100%);
  margin: 0 -1.2rem 2rem;
  padding: 0 2rem;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 3px 14px rgba(0,30,100,.26);
  position: relative;
  overflow: hidden;
}
.tc-hdr::after {
  content: "";
  position: absolute; inset: 0;
  background: linear-gradient(90deg, transparent 50%, rgba(255,255,255,.04));
  pointer-events: none;
}
.tc-hdr-left {
  display: flex; align-items: center; gap: 13px; z-index: 1;
}
.tc-hdr-logo {
  height: 30px; width: auto; display: block;
  background: rgba(255,255,255,.96);
  border-radius: 6px;
  padding: 3px 8px;
}
.tc-hdr-name {
  font-family: var(--sans);
  font-size: 1rem; font-weight: 800;
  color: #fff; letter-spacing: .5px; line-height: 1.2;
}
.tc-hdr-sub {
  font-size: .54rem; font-weight: 400;
  color: rgba(255,255,255,.45);
  letter-spacing: 2px; text-transform: uppercase; margin-top: 2px;
}
.tc-hdr-pill {
  z-index: 1;
  background: rgba(255,255,255,.11);
  border: 1px solid rgba(255,255,255,.20);
  border-radius: 20px; padding: 4px 14px;
  font-size: .58rem; font-weight: 600;
  color: rgba(255,255,255,.75);
  letter-spacing: 1px; text-transform: uppercase;
}

/* ════════════════════════════════════════
   SIDEBAR — #0047BA lacivert
   Tüm Streamlit sarmalayıcıları kapatılıyor
════════════════════════════════════════ */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div > div,
[data-testid="stSidebarContent"],
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
  background: #0047BA !important;
  border-right: none !important;
}
[data-testid="stSidebar"] {
  box-shadow: 4px 0 24px rgba(0,20,90,.20) !important;
  min-width: 230px !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small {
  color: rgba(255,255,255,.85) !important;
  font-family: var(--sans) !important;
}
.sb-top {
  background: rgba(0,0,0,.20);
  padding: .9rem 1.1rem;
  border-bottom: 1px solid rgba(255,255,255,.10);
  margin-bottom: 1.3rem;
  display: flex; align-items: center; gap: 9px;
}
.sb-top-title {
  font-size: .68rem !important; font-weight: 700 !important;
  color: rgba(255,255,255,.92) !important;
  letter-spacing: 2.2px !important; text-transform: uppercase !important;
}
.sb-inner { padding: 0 1.1rem; }
.sb-lbl {
  font-size: .56rem !important; font-weight: 700 !important;
  color: rgba(255,255,255,.42) !important;
  letter-spacing: 2.4px !important; text-transform: uppercase !important;
  margin-bottom: .5rem;
  display: flex; align-items: center; gap: 6px;
}
.sb-lbl::before {
  content: "";
  width: 3px; height: 10px;
  background: var(--yellow);
  border-radius: 2px; flex-shrink: 0;
}
[data-testid="stFileUploader"] {
  background: rgba(255,255,255,.07) !important;
  border: 1.5px dashed rgba(255,255,255,.24) !important;
  border-radius: var(--r-sm) !important;
  transition: border-color .2s, background .2s !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--yellow) !important;
  background: rgba(255,209,0,.06) !important;
}
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploaderDropzoneInstructions"] span {
  color: rgba(255,255,255,.38) !important; font-size: .68rem !important;
}
[data-testid="stFileUploaderDropzone"] small {
  color: rgba(255,255,255,.25) !important; font-size: .58rem !important;
}
.sb-schema {
  background: rgba(0,0,0,.22);
  border: 1px solid rgba(255,255,255,.10);
  border-left: 3px solid var(--yellow);
  border-radius: var(--r-sm);
  padding: .75rem .9rem; margin-top: .65rem;
  max-height: 220px; overflow-y: auto;
}
.sb-schema pre {
  font-family: var(--mono) !important; font-size: .62rem !important;
  line-height: 1.7 !important; color: rgba(255,255,255,.65) !important;
  margin: 0 !important; white-space: pre-wrap !important; word-break: break-word !important;
}
.sb-ok {
  display: flex; align-items: center; gap: 6px;
  margin-top: .65rem; font-size: .61rem !important;
  font-weight: 600 !important; color: #4ADE80 !important;
}
.sb-ok .dg { width: 6px; height: 6px; border-radius: 50%; background: #4ADE80; flex-shrink: 0; }
.sb-none { font-size: .67rem !important; color: rgba(255,255,255,.30) !important; line-height: 1.8; padding: .2rem 0; }
.sb-hr { height: 1px; background: rgba(255,255,255,.10); margin: .9rem 0; }
.sb-tip {
  font-family: var(--mono) !important; font-size: .57rem !important;
  color: rgba(255,255,255,.30) !important; line-height: 1.85;
  padding: .6rem .8rem; background: rgba(0,0,0,.18);
  border-radius: var(--r-sm); border-left: 2px solid rgba(255,209,0,.45);
}
.sb-tip code { color: var(--yellow) !important; }
.sb-tip strong { color: rgba(255,255,255,.52) !important; }

/* ════════════════════════════════════════
   MAIN CARD — tek beyaz panel
════════════════════════════════════════ */
.main-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--r);
  box-shadow: 0 4px 28px rgba(0,0,0,.06), 0 1px 4px rgba(0,71,186,.04);
  padding: 1.9rem 2rem 2.1rem;
  margin-bottom: 1.2rem;
}
.card-sep { height: 1px; background: #F0F4FA; margin: 1.3rem 0; }

/* ── Section labels ── */
.tc-lbl {
  font-size: .63rem !important; font-weight: 700 !important;
  color: var(--blue-dk) !important; letter-spacing: 1.8px; text-transform: uppercase;
  margin-bottom: .55rem !important; display: flex; align-items: center; gap: 7px;
}
.tc-lbl::before {
  content: ""; width: 3px; height: 13px;
  background: var(--yellow); border-radius: 2px; flex-shrink: 0;
}

/* ── Selects ── */
.stSelectbox label {
  font-size: .62rem !important; font-weight: 700 !important;
  color: var(--muted) !important; text-transform: uppercase !important; letter-spacing: .9px !important;
}
.stSelectbox > div > div {
  background: #fafcff !important; border: 1.5px solid var(--border) !important;
  border-radius: var(--r-sm) !important; font-family: var(--sans) !important;
  font-size: .84rem !important; color: var(--text) !important; transition: border-color .18s !important;
}
.stSelectbox > div > div:focus-within {
  border-color: var(--blue) !important; box-shadow: 0 0 0 3px rgba(0,71,186,.10) !important;
}
div[data-baseweb="select"] * { background: #fff !important; color: var(--text) !important; }
div[data-baseweb="popover"] * { background: #fff !important; border-color: var(--border) !important; color: var(--text) !important; }

/* ── Textarea ── */
.stTextArea label { display: none !important; }
.stTextArea textarea {
  background: #fafcff !important; border: 1.5px solid var(--border) !important;
  border-radius: var(--r-sm) !important; font-family: var(--sans) !important;
  font-size: .88rem !important; line-height: 1.65 !important;
  color: var(--text) !important; padding: 11px 13px !important; resize: vertical !important;
  transition: border-color .18s, box-shadow .18s !important;
}
.stTextArea textarea:focus {
  border-color: var(--blue) !important; background: #fff !important;
  box-shadow: 0 0 0 3px rgba(0,71,186,.10) !important; outline: none !important;
}
.stTextArea textarea::placeholder { color: var(--light) !important; }

/* ── Buton: sarı, 240px ortalı ── */
.stButton > button {
  background: var(--yellow) !important; color: #001A5E !important;
  font-family: var(--sans) !important; font-weight: 700 !important;
  font-size: .875rem !important; border: none !important;
  border-radius: var(--r-sm) !important;
  padding: .65rem 0 !important; width: 240px !important;
  display: block !important; margin: .5rem auto 0 !important;
  cursor: pointer !important;
  transition: background .15s, box-shadow .15s, transform .10s !important;
  box-shadow: 0 3px 12px rgba(255,209,0,.28) !important;
}
.stButton > button:hover {
  background: var(--yellow-dk) !important;
  box-shadow: 0 5px 20px rgba(200,168,0,.36) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ════════════════════════════════════════
   SQL KART
════════════════════════════════════════ */
.sql-card {
  background: #fff; border: 1px solid var(--border);
  border-top: 3px solid var(--blue); border-radius: var(--r);
  padding: 1.3rem 1.5rem 1.1rem;
  box-shadow: 0 4px 22px rgba(0,0,0,.05); margin-top: .5rem;
}
.sql-card pre {
  font-family: var(--mono) !important; font-size: .79rem !important;
  line-height: 1.78 !important; color: var(--text) !important;
  margin: 0 !important; white-space: pre-wrap !important; word-break: break-word !important;
}
.kw  { color: #0047BA; font-weight: 700; }
.fn  { color: #047857; }
.str { color: #B91C1C; }
.cmt { color: #9CA3AF; font-style: italic; }
.num { color: #7C3AED; }
.sql-bar {
  display: flex; align-items: center; justify-content: space-between;
  margin-top: .9rem; padding-top: .75rem; border-top: 1px solid #F0F4FA;
}
.sql-tag {
  display: inline-flex; align-items: center; gap: 5px;
  background: var(--blue-lt); border-radius: 20px; padding: 3px 10px;
  font-size: .61rem; font-weight: 600; color: var(--blue-dk);
}
.sql-tag .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--success); }

/* ── İndir ── */
.dl-wrap { margin-top: .75rem; }
.dl-wrap a {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--blue-lt); border: 1.5px solid var(--blue);
  border-radius: var(--r-sm); padding: .42rem 1rem;
  font-size: .76rem; font-weight: 600; color: var(--blue);
  text-decoration: none; transition: background .15s, color .15s;
}
.dl-wrap a:hover { background: var(--blue); color: #fff; }

/* ── Stats ── */
.stats-row { display: flex; gap: .7rem; margin-top: .9rem; }
.stat {
  flex: 1; background: #fff; border: 1px solid var(--border);
  border-radius: var(--r-sm); padding: .82rem; text-align: center;
  box-shadow: 0 1px 5px rgba(0,71,186,.04); transition: box-shadow .18s, transform .15s;
}
.stat:hover { box-shadow: 0 4px 14px rgba(0,71,186,.10); transform: translateY(-1px); }
.stat .v { font-size: 1.15rem; font-weight: 800; color: var(--blue); }
.stat .l { font-size: .58rem; font-weight: 700; color: var(--muted); letter-spacing: .8px; text-transform: uppercase; margin-top: 2px; }

/* ════════════════════════════════════════
   KURUMSAL UYARI PENCERESI (API hatası)
════════════════════════════════════════ */
.corp-alert {
  background: #fff; border: 1px solid #BFDBFE;
  border-left: 4px solid var(--blue); border-radius: var(--r);
  padding: 1.4rem 1.6rem; margin-top: 1rem;
  box-shadow: 0 2px 12px rgba(0,71,186,.08);
  font-family: var(--sans);
}
.corp-alert-header {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: .65rem;
}
.corp-alert-icon {
  width: 32px; height: 32px; border-radius: 8px;
  background: var(--blue-lt);
  display: flex; align-items: center; justify-content: center;
  font-size: .9rem; flex-shrink: 0;
}
.corp-alert-title {
  font-size: .88rem; font-weight: 700; color: var(--blue-dk);
}
.corp-alert-body {
  font-size: .80rem; color: var(--muted); line-height: 1.65;
  padding-left: 42px;
}
.corp-alert-body code {
  background: var(--blue-lt); padding: 1px 6px; border-radius: 4px;
  font-family: var(--mono); font-size: .74rem; color: var(--blue);
}
.corp-alert-body pre {
  background: #F8FAFF; border: 1px solid #DBEAFE; border-radius: 6px;
  padding: 7px 12px; font-family: var(--mono); font-size: .74rem;
  color: var(--blue-dk); margin: .5rem 0 .2rem;
}
.corp-alert.warn-variant {
  border-left-color: #D97706; border-color: #FDE68A;
}
.corp-alert.warn-variant .corp-alert-icon { background: #FFFBEB; }
.corp-alert.warn-variant .corp-alert-title { color: #92400E; }

/* ── Schema badge ── */
.schema-badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(5,150,105,.08); border: 1px solid rgba(5,150,105,.24);
  border-radius: 20px; padding: 3px 12px;
  font-size: .62rem; font-weight: 600; color: var(--success); margin-bottom: .7rem;
}
.schema-badge .dg { width: 6px; height: 6px; border-radius: 50%; background: var(--success); }

/* ── Expander ── */
.streamlit-expanderHeader {
  background: rgba(255,255,255,.85) !important; border: 1px solid var(--border) !important;
  border-radius: var(--r-sm) !important; font-family: var(--sans) !important;
  font-size: .75rem !important; font-weight: 600 !important; color: var(--muted) !important;
}
.streamlit-expanderContent {
  background: rgba(255,255,255,.90) !important; border: 1px solid var(--border) !important;
  border-top: none !important;
}

/* ── History item ── */
.h-item {
  background: #fff; border: 1px solid var(--border);
  border-left: 3px solid var(--yellow); border-radius: var(--r-sm);
  padding: .7rem .95rem; margin-bottom: .4rem;
  box-shadow: 0 1px 4px rgba(0,71,186,.04);
}
.h-item .hp {
  font-size: .80rem; font-weight: 500; color: var(--text);
  margin-bottom: 2px; display: -webkit-box;
  -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden;
}
.h-item .hm { font-size: .61rem; color: var(--light); }

/* ── Code block ── */
.stCodeBlock { border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; }
.stCodeBlock pre { background: #f8fafc !important; font-family: var(--mono) !important; font-size: .78rem !important; }
div[data-testid="stCopyButton"] button {
  background: var(--blue-lt) !important; border: 1px solid var(--border) !important;
  color: var(--blue) !important; border-radius: 5px !important; font-size: .66rem !important;
}
div[data-testid="stCopyButton"] button:hover { background: var(--blue) !important; color: #fff !important; }
.stSpinner > div { border-top-color: var(--blue) !important; }
.page-div { height: 1px; background: var(--border); margin: 1.3rem 0; opacity: .4; }

/* ════════════════════════════════════════
   FOOTER
════════════════════════════════════════ */
.tc-footer {
  text-align: center;
  margin-top: 3.5rem;
  padding: 1.1rem 0 .5rem;
  border-top: 1px solid var(--border);
}
.tc-footer p {
  font-family: var(--sans);
  font-size: .60rem;
  color: var(--light);
  letter-spacing: .5px;
  margin: 0;
}
.tc-footer p + p { margin-top: .25rem; }
.tc-footer strong { color: var(--muted); font-weight: 600; }
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

def corp_alert(icon, title, body, variant=""):
    return f"""
    <div class="corp-alert {variant}">
      <div class="corp-alert-header">
        <div class="corp-alert-icon">{icon}</div>
        <div class="corp-alert-title">{title}</div>
      </div>
      <div class="corp-alert-body">{body}</div>
    </div>"""


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-top">
      <span style="font-size:.9rem">🗄️</span>
      <span class="sb-top-title">Şema Bağlamı</span>
    </div>
    <div class="sb-inner">
      <p class="sb-lbl">📂 Şema Dosyası Yükle</p>
    </div>
    """, unsafe_allow_html=True)

    uf = st.file_uploader("schema_uploader", type=["sql","txt"],
                          accept_multiple_files=False,
                          label_visibility="collapsed")
    schema_text, schema_meta = None, {}

    if uf:
        try:
            raw, chars, tables = parse_schema(uf)
            if chars > 80_000:
                st.markdown(corp_alert("⚠️","Dosya Çok Büyük",
                    "Şema dosyası 80 KB limitini aşıyor. Kullanılmayan tabloları kaldırın.",
                    "warn-variant"), unsafe_allow_html=True)
            else:
                schema_text = raw
                schema_meta = {"name":uf.name,"tables":tables,"chars":chars}
                prev = raw[:700] + ("\n…" if len(raw)>700 else "")
                st.markdown(f"""<div class="sb-inner">
                <div class="sb-schema"><pre>{prev}</pre></div>
                <div class="sb-ok"><span class="dg"></span>{tables} tablo · {chars:,} karakter</div>
                </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.markdown(corp_alert("❌","Dosya Hatası",f"Dosya okunamadı: {e}"),
                        unsafe_allow_html=True)
    else:
        st.markdown("""<div class="sb-inner">
        <p class="sb-none">Şema yüklenmedi.<br>AI genel bilgisiyle<br>tablo yapılarını tahmin eder.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="sb-inner">
    <div class="sb-hr"></div>
    <div class="sb-tip">
      💡 <strong>İpucu:</strong><br>
      <code>pg_dump --schema-only</code><br>
      <code>SHOW CREATE TABLE t</code> (MySQL)
    </div>
    </div>""", unsafe_allow_html=True)


# ─── API Key ──────────────────────────────────────────────────────────────────
api_key = st.secrets.get("OPENAI_API_KEY","")
if not api_key:
    st.markdown(corp_alert(
        "🔐", "API Anahtarı Bulunamadı",
        """Uygulamanın çalışması için bir OpenAI API anahtarı gereklidir.<br><br>
        <code>.streamlit/secrets.toml</code> dosyasına şu satırı ekleyin:
        <pre>OPENAI_API_KEY = "sk-..."</pre>
        Streamlit Cloud kullanıyorsanız: <strong>App Settings › Secrets</strong>"""
    ), unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="tc-hdr">
  <div class="tc-hdr-left">
    <img class="tc-hdr-logo" src="{LOGO_SRC}" alt="Turkcell">
    <div>
      <div class="tc-hdr-name">TURKCELL SQL AI</div>
      <div class="tc-hdr-sub">Natural Language → SQL</div>
    </div>
  </div>
  <div class="tc-hdr-pill">OpenAI Destekli</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CARD
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# — Yapılandırma ——————————————————————————————————————————————————————————————
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

# — Schema badge (şema yüklüyse) ——————————————————————————————————————————————
if schema_text:
    st.markdown(f"""<div class="schema-badge">
    <span class="dg"></span>
    Şema Modu Aktif &nbsp;·&nbsp; {schema_meta['name']} &nbsp;·&nbsp; {schema_meta['tables']} tablo
    </div>""", unsafe_allow_html=True)

# — Prompt ———————————————————————————————————————————————————————————————————
st.markdown('<p class="tc-lbl">✦ Doğal Dil ile Açıkla</p>', unsafe_allow_html=True)
prompt = st.text_area(
    "p_area",
    value=st.session_state.lp,
    height=125,
    placeholder=(
        "Örn. → Geçen ay kaydolan ama henüz sipariş vermemiş kullanıcıları "
        "referans kaynağına göre gruplandır ve kayıt tarihine göre sırala…"
    ),
    key="p_key",
    label_visibility="collapsed",
)

st.markdown('<div style="height:.15rem"></div>', unsafe_allow_html=True)
go = st.button("⚡  SQL Oluştur", key="go_btn")

st.markdown('</div>', unsafe_allow_html=True)  # /main-card


# ══════════════════════════════════════════════════════════════════════════════
# GENERATE
# ══════════════════════════════════════════════════════════════════════════════
if go:
    st.session_state.lp = prompt
    if not prompt.strip():
        st.markdown(corp_alert("✏️","Boş Prompt",
            "Lütfen SQL üretmek için bir açıklama girin.", "warn-variant"),
            unsafe_allow_html=True)
        st.stop()

    with st.spinner("SQL oluşturuluyor…"):
        try:
            res = run_sql(prompt, api_key, dialect, style, model, schema_text)
        except openai.AuthenticationError:
            st.markdown(corp_alert("🔑","Kimlik Doğrulama Hatası",
                "API anahtarınız OpenAI tarafından reddedildi. "
                "Anahtarın geçerli ve aktif olduğundan emin olun."),
                unsafe_allow_html=True); st.stop()
        except openai.RateLimitError:
            st.markdown(corp_alert("⏱","İstek Limiti Aşıldı",
                "OpenAI kota limitinize ulaşıldı. "
                "Birkaç saniye bekleyip tekrar deneyin veya planınızı yükseltin."),
                unsafe_allow_html=True); st.stop()
        except openai.APIConnectionError:
            st.markdown(corp_alert("🌐","Bağlantı Hatası",
                "OpenAI API'ye ulaşılamadı. "
                "İnternet bağlantınızı kontrol edip tekrar deneyin."),
                unsafe_allow_html=True); st.stop()
        except Exception as e:
            st.markdown(corp_alert("⚙️","Beklenmeyen Hata",
                f"İşlem sırasında bir sorun oluştu:<br><code>{e}</code>"),
                unsafe_allow_html=True); st.stop()

    ok, err = validate(res["sql"])
    if not ok:
        st.markdown(corp_alert("⚠️","Model Bildirimi", err, "warn-variant"),
            unsafe_allow_html=True); st.stop()

    # Geçmişe kaydet
    st.session_state.qc += 1
    st.session_state.tt += res["tokens"]
    st.session_state.history.insert(0,{
        "prompt":  prompt, "sql": res["sql"], "dialect": dialect,
        "ts":      datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        "tokens":  res["tokens"],
        "schema":  schema_meta.get("name","—") if schema_text else "—",
    })
    st.session_state.history = st.session_state.history[:30]

    # SQL kartı
    sb = ""
    if schema_text:
        sb = (f'<span class="sql-tag" style="background:#D1FAE5;color:#065F46;">' +
              f'<span class="dot" style="background:#059669"></span>{schema_meta["name"]}</span>')

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
# SORGU GEÇMİŞİ
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.history:
    st.markdown('<div class="page-div"></div>', unsafe_allow_html=True)
    with st.expander(
        f"📜  Sorgu Geçmişi  ({len(st.session_state.history)} kayıt)",
        expanded=False
    ):
        for i, e in enumerate(st.session_state.history):
            tag = f" · 🗄 {e['schema']}" if e.get("schema") and e["schema"] != "—" else ""
            st.markdown(f"""
            <div class="h-item">
              <div class="hp">{e["prompt"]}</div>
              <div class="hm">{e["ts"]} · {e["dialect"]}{tag} · {e["tokens"]} token</div>
            </div>""", unsafe_allow_html=True)
            st.code(e["sql"], language="sql")
            st.markdown(dl_link(e["sql"]), unsafe_allow_html=True)
            if i < len(st.session_state.history) - 1:
                st.markdown('<div style="height:.2rem"></div>', unsafe_allow_html=True)

        st.markdown('<div style="height:.35rem"></div>', unsafe_allow_html=True)
        if st.button("🗑  Geçmişi Temizle", key="clr"):
            st.session_state.update({"history":[],"qc":0,"tt":0})
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="tc-footer">
  <p>© {datetime.datetime.now().year} <strong>TURKCELL SQL AI</strong> &nbsp;|&nbsp; L2 DevOps Operations</p>
  <p>OpenAI ile güçlendirilmiştir &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; Tüm hakları saklıdır.</p>
</div>""", unsafe_allow_html=True)