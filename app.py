"""
TURKCELL SQL AI — app.py v8
Fix: logo renkli · sidebar görünür · tek kart · buton ortalı · layout temiz
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

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Roboto+Mono:wght@400;500&display=swap');

:root {
  --blue:        #0047BA;
  --blue-dk:     #002D72;
  --blue-sb:     #003DA6;
  --blue-lt:     #EBF3FF;
  --yellow:      #FFD100;
  --yellow-dk:   #C9A800;
  --text:        #111827;
  --muted:       #6B7280;
  --light:       #9CA3AF;
  --border:      #E2E8F0;
  --border-lt:   #F0F4FA;
  --success:     #059669;
  --error:       #DC2626;
  --warn:        #D97706;
  --sans:        'Inter', system-ui, sans-serif;
  --mono:        'Roboto Mono', monospace;
  --r:           12px;
  --r-sm:        8px;
}

/* ─ RESET ─────────────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

/* ─ ARKA PLAN: gradient ───────────────────────────────────────────────────── */
html, body,
.stApp,
.stApp > div,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section.main,
section.main > div,
.main > div,
div[class^="block-container"] {
  background: linear-gradient(175deg, #ffffff 0%, #f4f8ff 50%, #eaf2ff 100%) !important;
  font-family: var(--sans) !important;
  color: var(--text) !important;
}

/* ─ STREAMLIT CHROME GİZLE ────────────────────────────────────────────────── */
#MainMenu, footer, header,
button[data-testid="baseButton-header"],
[data-testid="collapsedControl"] { visibility: hidden !important; height: 0 !important; }

/* ─ ANA CONTAINER — 760px ortalı ─────────────────────────────────────────── */
.block-container {
  max-width: 760px !important;
  padding: 0 1rem 6rem !important;
  margin: 0 auto !important;
  background: transparent !important;
}

/* ─ SCROLLBAR ─────────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--blue); border-radius: 4px; }

/* ════════════════════════════════════════════════════════════════════════════
   HEADER — ince, lacivert şerit, renkli logo
════════════════════════════════════════════════════════════════════════════ */
.tc-hdr {
  background: linear-gradient(90deg, #001A5E 0%, #0047BA 100%);
  margin: 0 -1rem 2rem;
  padding: 0 1.75rem;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 3px 14px rgba(0,35,110,.28);
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}
.tc-hdr::after {
  content: "";
  position: absolute;
  right: 0; top: 0; bottom: 0;
  width: 260px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.04));
  pointer-events: none;
}
.tc-hdr-left {
  display: flex;
  align-items: center;
  gap: 13px;
  z-index: 1;
}
/* ── Logo: orijinal renkler, arka planı temiz ── */
.tc-hdr-logo {
  height: 32px;
  width: auto;
  display: block;
  /* filter YOK — logo sarı+mavi renkleriyle görünür */
  background: rgba(255,255,255,.95);
  border-radius: 6px;
  padding: 3px 7px;
}
.tc-hdr-title {
  font-family: var(--sans);
  font-size: 1rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: .6px;
  line-height: 1;
}
.tc-hdr-sub {
  font-family: var(--sans);
  font-size: .55rem;
  font-weight: 400;
  color: rgba(255,255,255,.48);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-top: 3px;
}
.tc-hdr-pill {
  z-index: 1;
  background: rgba(255,255,255,.12);
  border: 1px solid rgba(255,255,255,.22);
  border-radius: 20px;
  padding: 4px 14px;
  font-family: var(--sans);
  font-size: .58rem;
  font-weight: 600;
  color: rgba(255,255,255,.80);
  letter-spacing: 1.1px;
  text-transform: uppercase;
}

/* ════════════════════════════════════════════════════════════════════════════
   SIDEBAR — #002D72 lacivert, beyaz yazılar
   ÖNEMLİ: Streamlit sidebar CSS'i çok katmanlı, tüm seçicileri kapatıyoruz
════════════════════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div > div,
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
  background: #002D72 !important;
  border-right: none !important;
}
[data-testid="stSidebar"] {
  box-shadow: 4px 0 22px rgba(0,18,72,.22) !important;
  min-width: 240px !important;
}
[data-testid="stSidebar"] * {
  color: rgba(255,255,255,.82) !important;
  font-family: var(--sans) !important;
}
[data-testid="stSidebarContent"] {
  background: #002D72 !important;
  padding: 0 !important;
}
.sb-top {
  background: rgba(0,0,0,.22);
  padding: .9rem 1.1rem;
  border-bottom: 1px solid rgba(255,255,255,.09);
  display: flex;
  align-items: center;
  gap: 9px;
  margin-bottom: 1.2rem;
}
.sb-top-title {
  font-family: var(--sans) !important;
  font-size: .68rem !important;
  font-weight: 700 !important;
  color: rgba(255,255,255,.92) !important;
  letter-spacing: 2.2px !important;
  text-transform: uppercase !important;
}
.sb-wrap { padding: 0 1.1rem; }
.sb-lbl {
  font-family: var(--sans) !important;
  font-size: .57rem !important;
  font-weight: 700 !important;
  color: rgba(255,255,255,.42) !important;
  letter-spacing: 2.4px !important;
  text-transform: uppercase !important;
  margin-bottom: .5rem;
  display: flex;
  align-items: center;
  gap: 6px;
}
.sb-lbl::before {
  content: "";
  width: 3px; height: 10px;
  background: var(--yellow);
  border-radius: 2px;
  flex-shrink: 0;
}
[data-testid="stFileUploader"] {
  background: rgba(255,255,255,.07) !important;
  border: 1.5px dashed rgba(255,255,255,.22) !important;
  border-radius: var(--r-sm) !important;
  transition: border-color .2s !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--yellow) !important;
  background: rgba(255,209,0,.06) !important;
}
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] p {
  color: rgba(255,255,255,.38) !important;
  font-size: .68rem !important;
}
[data-testid="stFileUploaderDropzone"] small {
  color: rgba(255,255,255,.25) !important;
  font-size: .58rem !important;
}
.sb-schema-card {
  background: rgba(0,0,0,.25);
  border: 1px solid rgba(255,255,255,.10);
  border-left: 3px solid var(--yellow);
  border-radius: var(--r-sm);
  padding: .75rem .9rem;
  margin-top: .65rem;
  max-height: 220px;
  overflow-y: auto;
}
.sb-schema-card pre {
  font-family: var(--mono) !important;
  font-size: .62rem !important;
  line-height: 1.7 !important;
  color: rgba(255,255,255,.65) !important;
  margin: 0 !important;
  white-space: pre-wrap !important;
  word-break: break-word !important;
}
.sb-status {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: .65rem;
  font-size: .61rem !important;
  font-weight: 600 !important;
  color: #4ADE80 !important;
}
.sb-status .dg {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #4ADE80;
  flex-shrink: 0;
}
.sb-inactive {
  font-size: .67rem !important;
  color: rgba(255,255,255,.30) !important;
  line-height: 1.8;
  padding: .2rem 0;
}
.sb-div { height: 1px; background: rgba(255,255,255,.09); margin: .9rem 0; }
.sb-tip {
  font-family: var(--mono) !important;
  font-size: .57rem !important;
  color: rgba(255,255,255,.30) !important;
  line-height: 1.85;
  padding: .6rem .8rem;
  background: rgba(0,0,0,.18);
  border-radius: var(--r-sm);
  border-left: 2px solid rgba(255,209,0,.45);
}
.sb-tip code { color: var(--yellow) !important; }
.sb-tip strong { color: rgba(255,255,255,.55) !important; }

/* ════════════════════════════════════════════════════════════════════════════
   ANA PANEL — TEK BEYAZ KART
   HTML div sarmalayıcılar kullanmıyoruz, CSS class ile çözüyoruz
════════════════════════════════════════════════════════════════════════════ */
.main-panel-wrap {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--r);
  box-shadow: 0 4px 24px rgba(0,0,0,.06), 0 1px 4px rgba(0,71,186,.05);
  padding: 1.8rem 1.9rem 2rem;
  margin-bottom: 1.2rem;
}
.panel-div {
  height: 1px;
  background: var(--border-lt);
  margin: 1.3rem 0;
}

/* ─ SECTION LABELS ────────────────────────────────────────────────────────── */
.tc-lbl {
  font-family: var(--sans) !important;
  font-size: .63rem !important;
  font-weight: 700 !important;
  color: var(--blue-dk) !important;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  margin-bottom: .55rem !important;
  display: flex;
  align-items: center;
  gap: 7px;
}
.tc-lbl::before {
  content: "";
  width: 3px; height: 13px;
  background: var(--yellow);
  border-radius: 2px;
  flex-shrink: 0;
}

/* ─ SELECTS ───────────────────────────────────────────────────────────────── */
.stSelectbox label {
  font-family: var(--sans) !important;
  font-size: .62rem !important;
  font-weight: 700 !important;
  color: var(--muted) !important;
  text-transform: uppercase !important;
  letter-spacing: .9px !important;
}
.stSelectbox > div > div {
  background: #fafcff !important;
  border: 1.5px solid var(--border) !important;
  border-radius: var(--r-sm) !important;
  font-family: var(--sans) !important;
  font-size: .84rem !important;
  color: var(--text) !important;
  transition: border-color .18s, box-shadow .18s !important;
}
.stSelectbox > div > div:focus-within {
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 3px rgba(0,71,186,.10) !important;
}
div[data-baseweb="select"] * { background: #fff !important; color: var(--text) !important; }
div[data-baseweb="popover"] * {
  background: #fff !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
}

/* ─ TEXTAREA ──────────────────────────────────────────────────────────────── */
.stTextArea label { display: none !important; }
.stTextArea textarea {
  background: #fafcff !important;
  border: 1.5px solid var(--border) !important;
  border-radius: var(--r-sm) !important;
  font-family: var(--sans) !important;
  font-size: .88rem !important;
  line-height: 1.65 !important;
  color: var(--text) !important;
  padding: 11px 13px !important;
  resize: vertical !important;
  transition: border-color .18s, box-shadow .18s !important;
}
.stTextArea textarea:focus {
  border-color: var(--blue) !important;
  background: #fff !important;
  box-shadow: 0 0 0 3px rgba(0,71,186,.10) !important;
  outline: none !important;
}
.stTextArea textarea::placeholder { color: var(--light) !important; }

/* ─ BUTON: sarı, sabit genişlik 240px, ortalı ────────────────────────────── */
.stButton > button {
  background: var(--yellow) !important;
  color: #001A5E !important;
  font-family: var(--sans) !important;
  font-weight: 700 !important;
  font-size: .875rem !important;
  letter-spacing: .2px;
  border: none !important;
  border-radius: var(--r-sm) !important;
  padding: .65rem 0 !important;
  width: 240px !important;
  display: block !important;
  margin: .4rem auto 0 !important;
  cursor: pointer !important;
  transition: background .15s, box-shadow .15s, transform .10s !important;
  box-shadow: 0 3px 12px rgba(255,209,0,.30) !important;
}
.stButton > button:hover {
  background: var(--yellow-dk) !important;
  box-shadow: 0 5px 20px rgba(200,168,0,.38) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active {
  transform: translateY(0) !important;
  box-shadow: 0 2px 8px rgba(200,168,0,.22) !important;
}

/* ─ SQL SONUÇ KARTI ───────────────────────────────────────────────────────── */
.sql-card {
  background: #fff;
  border: 1px solid var(--border);
  border-top: 3px solid var(--blue);
  border-radius: var(--r);
  padding: 1.3rem 1.5rem 1.1rem;
  box-shadow: 0 4px 22px rgba(0,0,0,.05);
  margin-top: .5rem;
}
.sql-card pre {
  font-family: var(--mono) !important;
  font-size: .79rem !important;
  line-height: 1.78 !important;
  color: var(--text) !important;
  margin: 0 !important;
  white-space: pre-wrap !important;
  word-break: break-word !important;
}
.kw  { color: #0047BA; font-weight: 700; }
.fn  { color: #047857; }
.str { color: #B91C1C; }
.cmt { color: #9CA3AF; font-style: italic; }
.num { color: #7C3AED; }
.sql-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: .9rem;
  padding-top: .75rem;
  border-top: 1px solid var(--border-lt);
}
.sql-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: var(--blue-lt);
  border-radius: 20px;
  padding: 3px 10px;
  font-family: var(--sans);
  font-size: .61rem;
  font-weight: 600;
  color: var(--blue-dk);
}
.sql-badge .dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--success);
}

/* ─ İNDİR BUTONU ─────────────────────────────────────────────────────────── */
.dl-wrap { margin-top: .75rem; }
.dl-wrap a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--blue-lt);
  border: 1.5px solid var(--blue);
  border-radius: var(--r-sm);
  padding: .42rem 1rem;
  font-family: var(--sans);
  font-size: .76rem;
  font-weight: 600;
  color: var(--blue);
  text-decoration: none;
  transition: background .15s, color .15s;
}
.dl-wrap a:hover { background: var(--blue); color: #fff; }

/* ─ STATS ─────────────────────────────────────────────────────────────────── */
.stats-row { display: flex; gap: .7rem; margin-top: .9rem; }
.stat {
  flex: 1;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  padding: .82rem;
  text-align: center;
  box-shadow: 0 1px 5px rgba(0,71,186,.04);
  transition: box-shadow .18s, transform .15s;
}
.stat:hover { box-shadow: 0 4px 14px rgba(0,71,186,.10); transform: translateY(-1px); }
.stat .v { font-family: var(--sans); font-size: 1.15rem; font-weight: 800; color: var(--blue); }
.stat .l { font-size: .58rem; font-weight: 700; color: var(--muted); letter-spacing: .8px; text-transform: uppercase; margin-top: 2px; }

/* ─ ALERTS ────────────────────────────────────────────────────────────────── */
.alert {
  border-radius: var(--r-sm);
  padding: .8rem 1rem;
  font-family: var(--sans);
  font-size: .81rem;
  display: flex;
  align-items: flex-start;
  gap: 9px;
  margin-top: .5rem;
}
.alert-warn  { background: #fffbeb; border: 1px solid #fde68a; border-left: 4px solid var(--warn);  color: var(--warn);  }
.alert-error { background: #fef2f2; border: 1px solid #fecaca; border-left: 4px solid var(--error); color: var(--error); }
.alert-key {
  background: #f5f3ff;
  border: 1px solid #ddd6fe;
  border-left: 4px solid #7C3AED;
  color: #4C1D95;
  border-radius: var(--r-sm);
  padding: 1.1rem 1.3rem;
  font-family: var(--sans);
  font-size: .82rem;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-top: 1.2rem;
  line-height: 1.7;
}
.alert-key strong { color: #3B0764; }
.alert-key code { background: #ede9fe; padding: 1px 5px; border-radius: 4px; font-family: var(--mono); font-size: .74rem; color: #7C3AED; }
.alert-key pre  { background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 5px; padding: 6px 11px; font-family: var(--mono); font-size: .74rem; color: #5B21B6; margin: .35rem 0 .15rem; }

/* ─ SCHEMA BADGE ──────────────────────────────────────────────────────────── */
.schema-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(5,150,105,.08);
  border: 1px solid rgba(5,150,105,.24);
  border-radius: 20px;
  padding: 3px 12px;
  font-family: var(--sans);
  font-size: .62rem;
  font-weight: 600;
  color: var(--success);
  margin-bottom: .7rem;
}
.schema-badge .dg { width: 6px; height: 6px; border-radius: 50%; background: var(--success); }

/* ─ EXPANDER ──────────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
  background: rgba(255,255,255,.85) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-sm) !important;
  font-family: var(--sans) !important;
  font-size: .75rem !important;
  font-weight: 600 !important;
  color: var(--muted) !important;
}
.streamlit-expanderContent {
  background: rgba(255,255,255,.90) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
}

/* ─ HISTORY ITEM ──────────────────────────────────────────────────────────── */
.h-item {
  background: #fff;
  border: 1px solid var(--border);
  border-left: 3px solid var(--yellow);
  border-radius: var(--r-sm);
  padding: .7rem .95rem;
  margin-bottom: .4rem;
  box-shadow: 0 1px 4px rgba(0,71,186,.04);
}
.h-item .hp { font-family: var(--sans); font-size: .80rem; font-weight: 500; color: var(--text); margin-bottom: 2px; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }
.h-item .hm { font-family: var(--sans); font-size: .61rem; color: var(--light); }

/* ─ CODE BLOCK ────────────────────────────────────────────────────────────── */
.stCodeBlock { border: 1px solid var(--border) !important; border-radius: var(--r-sm) !important; }
.stCodeBlock pre { background: #f8fafc !important; font-family: var(--mono) !important; font-size: .78rem !important; }
div[data-testid="stCopyButton"] button { background: var(--blue-lt) !important; border: 1px solid var(--border) !important; color: var(--blue) !important; border-radius: 5px !important; font-size: .66rem !important; }
div[data-testid="stCopyButton"] button:hover { background: var(--blue) !important; color: #fff !important; }
.stSpinner > div { border-top-color: var(--blue) !important; }

/* ─ DIVIDER ───────────────────────────────────────────────────────────────── */
.page-div { height: 1px; background: var(--border); margin: 1.3rem 0; opacity: .5; }

/* ─ FOOTER ────────────────────────────────────────────────────────────────── */
.tc-foot { text-align: center; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--border); }
.tc-foot span { font-family: var(--sans); font-size: .61rem; color: var(--light); letter-spacing: .4px; }
.tc-foot strong { color: var(--blue); font-weight: 700; }
</style>
""", unsafe_allow_html=True)


# ─── Session state ────────────────────────────────────────────────────────────
for k, v in [("history",[]),("query_count",0),("total_tokens",0),("last_prompt","")]:
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
    sm = {
        "Standard":  "Uppercase keywords, clean multi-line formatting.",
        "Compact":   "Compact, minimal whitespace.",
        "Annotated": "Add a brief comment above each major clause.",
    }
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
        messages=[
            {"role":"system","content":sys_prompt(dialect,style)},
            {"role":"user",  "content":user_msg(prompt,schema)},
        ],
        temperature=0.2, max_tokens=1400,
    )
    return {
        "sql":     r.choices[0].message.content.strip(),
        "tokens":  r.usage.total_tokens,
        "elapsed": round(time.time()-t0, 2),
    }

def validate(sql):
    if sql.startswith("ERROR:"): return False, sql[6:].strip()
    if len(sql) < 10:            return False, "Model çok kısa yanıt döndürdü."
    return True, ""

def dl_link(sql: str) -> str:
    enc = b64lib.b64encode(sql.encode()).decode()
    ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return (f'<div class="dl-wrap"><a href="data:file/sql;base64,{enc}" ' +
            f'download="query_{ts}.sql">📥 SQL Olarak İndir</a></div>')


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-top">
      <span style="font-size:.9rem">🗄️</span>
      <span class="sb-top-title">Şema Bağlamı</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-wrap">', unsafe_allow_html=True)
    st.markdown('<p class="sb-lbl">📂 Şema Dosyası Yükle</p>', unsafe_allow_html=True)

    uf = st.file_uploader("schema_file", type=["sql","txt"],
                          accept_multiple_files=False,
                          label_visibility="collapsed")

    schema_text, schema_meta = None, {}

    if uf:
        try:
            raw, chars, tables = parse_schema(uf)
            if chars > 80_000:
                st.markdown("""<div class="alert alert-warn" style="font-size:.66rem;padding:.5rem .8rem;">
                ⚠ 80 KB limitini aşıyor. Tabloları azaltın.</div>""", unsafe_allow_html=True)
            else:
                schema_text = raw
                schema_meta = {"name": uf.name, "tables": tables, "chars": chars}
                preview = raw[:700] + ("\n…" if len(raw) > 700 else "")
                st.markdown(f"""
                <div class="sb-schema-card"><pre>{preview}</pre></div>
                <div class="sb-status">
                  <span class="dg"></span>{tables} tablo · {chars:,} karakter
                </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""<div class="alert alert-error"
            style="font-size:.66rem;padding:.5rem .8rem;">✖ {e}</div>""",
            unsafe_allow_html=True)
    else:
        st.markdown("""<p class="sb-inactive">
        Şema yüklenmedi.<br>AI genel bilgisiyle tahmin eder.</p>""",
        unsafe_allow_html=True)

    st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
    st.markdown("""<div class="sb-tip">
    💡 <strong>İpucu:</strong><br>
    <code>pg_dump --schema-only</code> (PostgreSQL)<br>
    <code>SHOW CREATE TABLE tablo</code> (MySQL)
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── API Key ──────────────────────────────────────────────────────────────────
api_key = st.secrets.get("OPENAI_API_KEY", "")
if not api_key:
    st.markdown("""<div class="alert-key">
    <span style="font-size:1rem;flex-shrink:0">🔐</span>
    <div><strong>API anahtarı bulunamadı.</strong><br>
    <span style="font-size:.77rem;opacity:.85;">
      <code>.streamlit/secrets.toml</code> dosyasına ekleyin:
    </span>
    <pre>OPENAI_API_KEY = "sk-..."</pre>
    <span style="font-size:.70rem;opacity:.60;">
      Streamlit Cloud → App Settings › Secrets
    </span></div></div>""", unsafe_allow_html=True)
    st.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER — renkli logo, TURKCELL SQL AI
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="tc-hdr">
  <div class="tc-hdr-left">
    <img class="tc-hdr-logo" src="{LOGO_SRC}" alt="Turkcell">
    <div>
      <div class="tc-hdr-title">TURKCELL SQL AI</div>
      <div class="tc-hdr-sub">Natural Language → SQL</div>
    </div>
  </div>
  <div class="tc-hdr-pill">OpenAI Destekli</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ANA PANEL — TEK KART, HTML WRAPPER (Streamlit columns içinde güvenli)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="main-panel-wrap">', unsafe_allow_html=True)

# — Yapılandırma ——————————————————————————————————————————————————————————————
st.markdown('<p class="tc-lbl">⚙ Yapılandırma</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    dialect = st.selectbox("Dialect",
        ["PostgreSQL","MySQL","SQLite","SQL Server (T-SQL)","BigQuery","Snowflake"],
        key="d_sel")
with col2:
    style = st.selectbox("Stil",
        ["Standard","Annotated","Compact"],
        key="s_sel")
with col3:
    model = st.selectbox("Model",
        ["gpt-4o","gpt-4o-mini","gpt-4-turbo"],
        key="m_sel")

st.markdown('<div class="panel-div"></div>', unsafe_allow_html=True)

# — Hızlı örnekler ——————————————————————————————————————————————————————————
EXAMPLES = [
    ("📦", "Top 10 customers by total revenue in 2024"),
    ("📊", "Monthly active users by country, last 6 months"),
    ("🔍", "Orders delivered more than 3 days late"),
    ("🔗", "Products never purchased with category names"),
    ("📈", "Running daily sales total — window function"),
    ("⚠️", "Duplicate email addresses in users table"),
]
with st.expander("✦  Hızlı Örnekler — tıklayarak yükle", expanded=False):
    ec1, ec2 = st.columns(2)
    for i, (icon, txt) in enumerate(EXAMPLES):
        with (ec1 if i % 2 == 0 else ec2):
            if st.button(f"{icon}  {txt}", key=f"ex{i}", use_container_width=True):
                st.session_state.last_prompt = txt
                st.rerun()

st.markdown('<div class="panel-div"></div>', unsafe_allow_html=True)

# — Schema badge ——————————————————————————————————————————————————————————————
if schema_text:
    st.markdown(f"""<div class="schema-badge">
    <span class="dg"></span>
    Şema Modu Aktif &nbsp;·&nbsp; {schema_meta['name']} &nbsp;·&nbsp; {schema_meta['tables']} tablo
    </div>""", unsafe_allow_html=True)

# — Prompt ———————————————————————————————————————————————————————————————————
st.markdown('<p class="tc-lbl">✦ Doğal Dil ile Açıkla</p>', unsafe_allow_html=True)
prompt = st.text_area(
    "prompt_area",
    value=st.session_state.last_prompt,
    height=120,
    placeholder=(
        "Örn. → Geçen ay kaydolan ama henüz sipariş vermemiş kullanıcıları "
        "referans kaynağına göre gruplandır ve kayıt tarihine göre sırala…"
    ),
    key="prompt_key",
    label_visibility="collapsed",
)

# — Buton ————————————————————————————————————————————————————————————————————
st.markdown('<div style="height:.2rem"></div>', unsafe_allow_html=True)
go = st.button("⚡  SQL Oluştur", key="go_btn")

st.markdown('</div>', unsafe_allow_html=True)  # /main-panel-wrap


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATE
# ═══════════════════════════════════════════════════════════════════════════════
if go:
    if not prompt.strip():
        st.markdown("""<div class="alert alert-warn">
        <span>⚠</span><span>Lütfen bir açıklama girin.</span></div>""",
        unsafe_allow_html=True)
        st.stop()

    spin_msg = "Şemaya özel SQL oluşturuluyor…" if schema_text else "SQL oluşturuluyor…"
    with st.spinner(spin_msg):
        try:
            res = run_sql(prompt, api_key, dialect, style, model, schema_text)
        except openai.AuthenticationError:
            st.markdown("""<div class="alert alert-error"><span>✖</span>
            <span><strong>Kimlik hatası.</strong> API anahtarı geçersiz.</span></div>""",
            unsafe_allow_html=True); st.stop()
        except openai.RateLimitError:
            st.markdown("""<div class="alert alert-error"><span>✖</span>
            <span><strong>Limit aşıldı.</strong> Kısa süre sonra tekrar deneyin.</span></div>""",
            unsafe_allow_html=True); st.stop()
        except openai.APIConnectionError:
            st.markdown("""<div class="alert alert-error"><span>✖</span>
            <span><strong>Bağlantı hatası.</strong> API'ye ulaşılamadı.</span></div>""",
            unsafe_allow_html=True); st.stop()
        except Exception as e:
            st.markdown(f"""<div class="alert alert-error"><span>✖</span>
            <span><strong>Hata:</strong> {e}</span></div>""",
            unsafe_allow_html=True); st.stop()

    ok, err = validate(res["sql"])
    if not ok:
        st.markdown(f"""<div class="alert alert-warn"><span>⚠</span>
        <span>{err}</span></div>""", unsafe_allow_html=True); st.stop()

    # Geçmişe kaydet
    st.session_state.query_count  += 1
    st.session_state.total_tokens += res["tokens"]
    st.session_state.history.insert(0, {
        "prompt":  prompt,
        "sql":     res["sql"],
        "dialect": dialect,
        "ts":      datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        "tokens":  res["tokens"],
        "schema":  schema_meta.get("name","—") if schema_text else "—",
    })
    st.session_state.history = st.session_state.history[:30]

    # SQL kartı
    sb_html = ""
    if schema_text:
        sb_html = (f'<span class="sql-badge" style="background:#D1FAE5;color:#065F46;">' +
                   f'<span class="dot" style="background:#059669"></span>' +
                   f'{schema_meta["name"]}</span>')

    st.markdown(f"""
    <div class="sql-card">
      <pre>{hl(res["sql"])}</pre>
      <div class="sql-status">
        <span class="sql-badge"><span class="dot"></span>{dialect}</span>
        <div style="display:flex;gap:.5rem;align-items:center;">
          {sb_html}
          <span class="sql-badge">{res["elapsed"]}s · {res["tokens"]} token</span>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.code(res["sql"], language="sql")

    # 📥 İndir
    st.markdown(dl_link(res["sql"]), unsafe_allow_html=True)

    # Stats
    st.markdown(f"""
    <div class="stats-row">
      <div class="stat">
        <div class="v">{st.session_state.query_count}</div>
        <div class="l">Toplam Sorgu</div>
      </div>
      <div class="stat">
        <div class="v">{res["elapsed"]}s</div>
        <div class="l">Yanıt Süresi</div>
      </div>
      <div class="stat">
        <div class="v">{st.session_state.total_tokens}</div>
        <div class="l">Token</div>
      </div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SORGU GEÇMİŞİ
# ═══════════════════════════════════════════════════════════════════════════════
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
            if i < len(st.session_state.history) - 1:
                st.markdown('<div style="height:.25rem"></div>', unsafe_allow_html=True)

        st.markdown('<div style="height:.4rem"></div>', unsafe_allow_html=True)
        if st.button("🗑  Geçmişi Temizle", key="clr_btn"):
            st.session_state.update({"history":[],"query_count":0,"total_tokens":0})
            st.rerun()

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="tc-foot">
  <span>
    <strong>TURKCELL SQL AI</strong>
    &nbsp;·&nbsp; OpenAI ile güçlendirilmiştir
    &nbsp;·&nbsp; Streamlit
  </span>
</div>""", unsafe_allow_html=True)