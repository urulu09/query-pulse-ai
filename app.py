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
/* ════════════════════════════════════════════════════════════════════════
   TURKCELL SQL AI — Enterprise SaaS UI
   Brand: #003DA5 primary · #FFC72C accent · #F5F7FA background
════════════════════════════════════════════════════════════════════════ */

/* ── FONTS ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── DESIGN TOKENS ──────────────────────────────────────────────────── */
:root {
  /* brand */
  --b1:        #003DA5;   /* primary blue  */
  --b2:        #0057D9;   /* secondary blue */
  --b3:        #E8EFFE;   /* blue tint     */
  --b4:        #F0F4FF;   /* lightest blue  */
  --yellow:    #FFC72C;   /* accent yellow  */
  --yel-dk:    #E6AE00;   /* hover yellow   */
  --yel-lt:    #FFF9E6;   /* yellow tint    */

  /* neutrals */
  --bg:        #F5F7FA;   /* page bg       */
  --white:     #FFFFFF;
  --text:      #0F1623;   /* primary text   */
  --text-2:    #3D4A5C;   /* secondary      */
  --text-3:    #6B7A90;   /* muted          */
  --text-4:    #9AA5B4;   /* disabled/hint  */
  --border:    #DCE3ED;
  --border-lt: #EEF2F7;

  /* status */
  --ok:        #0D7F4D;
  --ok-bg:     #EDFAF3;
  --ok-brd:    #A3DFBE;
  --warn:      #B45309;
  --warn-bg:   #FFFBEB;
  --warn-brd:  #FDE68A;
  --err:       #B91C1C;
  --err-bg:    #FEF2F2;
  --err-brd:   #FECACA;

  /* shadows */
  --sh-sm:     0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
  --sh:        0 4px 12px rgba(0,0,0,.07), 0 1px 4px rgba(0,0,0,.04);
  --sh-md:     0 8px 24px rgba(0,0,0,.09), 0 2px 6px rgba(0,0,0,.05);
  --sh-blue:   0 0 0 3px rgba(0,61,165,.14);

  /* spacing & shape */
  --r:         10px;
  --r-sm:      7px;
  --r-lg:      14px;
  --sans:      'Inter', system-ui, sans-serif;
  --mono:      'JetBrains Mono', 'Roboto Mono', monospace;
}

/* ── PAGE RESET ─────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body {
  background: var(--bg) !important;
  min-height: 100vh;
  font-family: var(--sans) !important;
  color: var(--text);
  -webkit-font-smoothing: antialiased;
}

/* kill every Streamlit background wrapper */
.stApp,
.stApp > div,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section.main,
section.main > div,
.block-container {
  background: transparent !important;
}

#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--b2); }

/* ── MAIN CONTAINER ─────────────────────────────────────────────────── */
.block-container {
  max-width: 1100px !important;
  padding: 0 1.5rem 5rem !important;
  margin: 0 auto !important;
}

/* remove default streamlit element gaps */
div[data-testid="stVerticalBlock"] > div { margin-bottom: 0 !important; }
div[data-testid="element-container"] { margin: 0 !important; padding: 0 !important; }

/* ════════════════════════════════════════════════════════════════════════
   HEADER
════════════════════════════════════════════════════════════════════════ */
.hdr {
  background: linear-gradient(100deg, #002A80 0%, var(--b1) 45%, var(--b2) 100%);
  margin: 0 -1.5rem 1.8rem;
  padding: 0 2.5rem;
  height: 62px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 16px rgba(0,30,100,.22), 0 1px 0 rgba(255,255,255,.06) inset;
  position: relative;
  overflow: hidden;
}
/* decorative top shimmer */
.hdr::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg,transparent,rgba(255,255,255,.30),transparent);
}
/* decorative right glow */
.hdr::after {
  content: "";
  position: absolute;
  right: -60px; top: -40px;
  width: 280px; height: 160px;
  background: radial-gradient(ellipse,rgba(255,199,44,.12),transparent 70%);
  pointer-events: none;
}
.hdr-left  { display:flex; align-items:center; gap:14px; z-index:1; }
.hdr-logo  {
  height: 34px; width: auto; display: block;
  background: rgba(255,255,255,.97);
  border-radius: 7px;
  padding: 3px 9px;
  box-shadow: 0 1px 4px rgba(0,0,0,.12);
}
.hdr-vline { width:1px; height:22px; background:rgba(255,255,255,.22); flex-shrink:0; }
.hdr-title {
  font-size: 1.05rem; font-weight: 800;
  color: #fff;
  letter-spacing: .3px;
  line-height: 1.2;
}
.hdr-sub {
  font-size: .52rem; font-weight: 500;
  color: rgba(255,255,255,.48);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-top: 2px;
}
.hdr-pill {
  z-index: 1;
  background: rgba(255,255,255,.12);
  border: 1px solid rgba(255,255,255,.22);
  border-radius: 20px;
  padding: 4px 14px;
  font-size: .58rem; font-weight: 600;
  color: rgba(255,255,255,.80);
  letter-spacing: .9px;
  text-transform: uppercase;
  backdrop-filter: blur(4px);
}

/* ════════════════════════════════════════════════════════════════════════
   CARDS  (base)
════════════════════════════════════════════════════════════════════════ */
.card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  box-shadow: var(--sh);
  padding: 1.5rem 1.8rem 1.6rem;
  margin-bottom: .9rem;
  transition: box-shadow .2s;
}
.card:hover { box-shadow: var(--sh-md); }

/* upload card — tinted blue */
.upload-card {
  background: linear-gradient(135deg, #EEF3FF 0%, #E3ECFF 100%);
  border: 1.5px dashed rgba(0,61,165,.24);
  border-radius: var(--r-lg);
  padding: 1.1rem 1.6rem .9rem;
  margin-bottom: .9rem;
  transition: border-color .2s;
}
.upload-card:hover { border-color: var(--b1); }

/* section divider inside card */
.card-sep {
  height: 1px;
  background: var(--border-lt);
  margin: 1.1rem -1.8rem;   /* bleeds to card edges */
}

/* ── labels ─────────────────────────────────────────────────────────── */
.lbl {
  font-size: .65rem; font-weight: 700;
  color: var(--b1);
  letter-spacing: 1.6px;
  text-transform: uppercase;
  margin-bottom: .5rem;
  display: flex; align-items: center; gap: 7px;
}
.lbl::before {
  content: "";
  width: 3px; height: 13px;
  background: var(--yellow);
  border-radius: 2px; flex-shrink: 0;
}
.upload-lbl {
  font-size: .68rem; font-weight: 700;
  color: var(--b1);
  letter-spacing: 1.4px;
  text-transform: uppercase;
  margin-bottom: .5rem;
  display: flex; align-items: center; gap: 7px;
}
.upload-lbl::before {
  content: "";
  width: 3px; height: 13px;
  background: var(--yellow);
  border-radius: 2px; flex-shrink: 0;
}

/* ── help text ──────────────────────────────────────────────────────── */
.upload-help {
  font-size: .71rem; color: var(--text-3); line-height: 1.65;
  padding: .45rem .75rem;
  background: rgba(255,255,255,.65);
  border-radius: var(--r-sm);
  border-left: 2px solid rgba(0,61,165,.24);
  margin-top: .5rem;
}
.upload-help code {
  background: rgba(0,61,165,.08);
  color: var(--b1);
  padding: 1px 5px;
  border-radius: 4px;
  font-family: var(--mono);
  font-size: .68rem;
}

/* ── schema loaded ──────────────────────────────────────────────────── */
.schema-ok {
  display: flex; align-items: center; gap: 7px;
  margin-top: .5rem;
  font-size: .70rem; font-weight: 600;
  color: var(--ok);
}
.schema-ok .dot {
  width: 7px; height: 7px;
  border-radius: 50%; background: var(--ok); flex-shrink: 0;
}
.tbl-row { display:flex; flex-wrap:wrap; gap:.3rem; margin-top:.4rem; }
.tbl-chip {
  background: rgba(0,61,165,.07);
  border: 1px solid rgba(0,61,165,.16);
  border-radius: 20px;
  padding: 2px 10px;
  font-family: var(--mono);
  font-size: .63rem; font-weight: 500;
  color: var(--b1);
}
.tbl-more {
  background: var(--border-lt);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 2px 10px;
  font-size: .63rem; color: var(--text-3);
}

/* ════════════════════════════════════════════════════════════════════════
   WIDGETS
════════════════════════════════════════════════════════════════════════ */

/* file uploader */
[data-testid="stFileUploader"] { background: transparent !important; border: none !important; }
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploaderDropzone"] {
  background: rgba(255,255,255,.75) !important;
  border: 1.5px dashed rgba(0,61,165,.28) !important;
  border-radius: var(--r) !important;
  transition: border-color .2s, background .2s !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
  border-color: var(--b1) !important;
  background: #fff !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span {
  color: var(--text-3) !important; font-size: .74rem !important;
}
[data-testid="stFileUploaderDropzone"] small {
  color: var(--text-4) !important; font-size: .61rem !important;
}

/* selects */
.stSelectbox label {
  font-size: .62rem !important; font-weight: 700 !important;
  color: var(--text-3) !important;
  text-transform: uppercase !important;
  letter-spacing: .9px !important;
}
.stSelectbox > div > div {
  background: var(--white) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: var(--r-sm) !important;
  font-family: var(--sans) !important;
  font-size: .84rem !important;
  color: var(--text) !important;
  transition: border-color .18s, box-shadow .18s !important;
}
.stSelectbox > div > div:focus-within {
  border-color: var(--b1) !important;
  box-shadow: var(--sh-blue) !important;
}
div[data-baseweb="select"] * { background: #fff !important; color: var(--text) !important; }
div[data-baseweb="popover"] * {
  background: #fff !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
}

/* textarea ── INPUT FIELD */
.stTextArea label { display: none !important; }
.stTextArea textarea {
  background: var(--white) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: var(--r) !important;
  font-family: var(--sans) !important;
  font-size: .9rem !important;
  line-height: 1.65 !important;
  color: var(--text) !important;
  padding: 12px 14px !important;
  resize: vertical !important;
  transition: border-color .18s, box-shadow .18s !important;
  box-shadow: var(--sh-sm) !important;
}
.stTextArea textarea:focus {
  border-color: var(--b1) !important;
  box-shadow: var(--sh-blue) !important;
  outline: none !important;
}
.stTextArea textarea::placeholder { color: var(--text-4) !important; }

/* PRIMARY BUTTON ── Generate SQL */
.stButton > button {
  background: var(--yellow) !important;
  color: var(--b1) !important;
  font-family: var(--sans) !important;
  font-weight: 700 !important;
  font-size: .9rem !important;
  border: none !important;
  border-radius: var(--r-sm) !important;
  padding: .68rem 2.8rem !important;
  cursor: pointer !important;
  display: block !important;
  margin: .55rem auto 0 !important;
  transition: background .15s, box-shadow .15s, transform .10s !important;
  box-shadow: 0 4px 14px rgba(255,199,44,.38) !important;
  letter-spacing: .2px;
}
.stButton > button:hover {
  background: var(--yel-dk) !important;
  box-shadow: 0 6px 20px rgba(255,199,44,.50) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active {
  transform: translateY(0) !important;
  box-shadow: 0 2px 8px rgba(255,199,44,.28) !important;
}

/* ════════════════════════════════════════════════════════════════════════
   SQL OUTPUT CARD  (dark code theme)
════════════════════════════════════════════════════════════════════════ */
.sql-card {
  background: #161B2A;
  border: 1px solid #252E45;
  border-radius: var(--r-lg);
  padding: 1.3rem 1.5rem 1rem;
  box-shadow: 0 8px 30px rgba(0,0,0,.20), 0 2px 8px rgba(0,0,0,.12);
  margin-top: .6rem;
}
.sql-card pre {
  font-family: var(--mono) !important;
  font-size: .80rem !important;
  line-height: 1.82 !important;
  color: #CDD6F4 !important;
  margin: 0 !important;
  white-space: pre-wrap !important;
  word-break: break-word !important;
}
/* Catppuccin Mocha syntax palette */
.kw  { color: #89DCEB; font-weight: 700; }  /* cyan  — keywords    */
.fn  { color: #A6E3A1; }                     /* green — functions   */
.str { color: #F38BA8; }                     /* pink  — strings     */
.cmt { color: #45475A; font-style: italic; } /* gray  — comments    */
.num { color: #CBA6F7; }                     /* mauve — numbers     */

.sql-bar {
  display: flex; align-items: center; justify-content: space-between;
  margin-top: .9rem; padding-top: .72rem;
  border-top: 1px solid #252E45;
}
.sql-tag {
  display: inline-flex; align-items: center; gap: 5px;
  background: rgba(137,220,235,.10);
  border: 1px solid rgba(137,220,235,.22);
  border-radius: 20px;
  padding: 3px 11px;
  font-size: .61rem; font-weight: 600;
  color: #89DCEB;
}
.sql-tag .dot { width: 6px; height: 6px; border-radius: 50%; background: #A6E3A1; }

/* ── clipboard ──────────────────────────────────────────────────────── */
.clip-btn {
  display: inline-flex; align-items: center; gap: 5px;
  background: rgba(137,220,235,.10);
  border: 1px solid rgba(137,220,235,.22);
  border-radius: var(--r-sm);
  padding: 3px 12px;
  font-family: var(--sans);
  font-size: .68rem; font-weight: 600;
  color: #89DCEB; cursor: pointer;
  transition: background .15s;
}
.clip-btn:hover  { background: rgba(137,220,235,.22); }
.clip-btn.copied { color: #A6E3A1; border-color: rgba(166,227,161,.35); }

/* ── download link (secondary) ──────────────────────────────────────── */
.dl-wrap { margin-top: .6rem; }
.dl-wrap a {
  display: inline-flex; align-items: center; gap: 5px;
  background: transparent;
  border: 1.5px solid rgba(0,61,165,.30);
  border-radius: var(--r-sm);
  padding: .36rem .9rem;
  font-size: .72rem; font-weight: 600;
  color: var(--b1); text-decoration: none;
  transition: background .15s, border-color .15s;
}
.dl-wrap a:hover { background: var(--b3); border-color: var(--b1); }

/* ════════════════════════════════════════════════════════════════════════
   STATUS BADGES
════════════════════════════════════════════════════════════════════════ */
.status-safe {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--ok-bg);
  border: 1px solid var(--ok-brd);
  border-radius: 20px; padding: 3px 13px;
  font-size: .67rem; font-weight: 700; color: var(--ok);
}
.status-safe::before  { content:"●"; font-size:.55rem; color: var(--ok); }

.status-risky {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--warn-bg);
  border: 1px solid var(--warn-brd);
  border-radius: 20px; padding: 3px 13px;
  font-size: .67rem; font-weight: 700; color: var(--warn);
}
.status-risky::before { content:"●"; font-size:.55rem; color: var(--warn); }

.status-invalid {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--err-bg);
  border: 1px solid var(--err-brd);
  border-radius: 20px; padding: 3px 13px;
  font-size: .67rem; font-weight: 700; color: var(--err);
}
.status-invalid::before { content:"●"; font-size:.55rem; color: var(--err); }

/* ════════════════════════════════════════════════════════════════════════
   REVIEW CARD
════════════════════════════════════════════════════════════════════════ */
.review-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 1.1rem 1.4rem;
  margin-top: .7rem;
  box-shadow: var(--sh);
}
.review-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: .8rem;
  margin-top: .6rem;
}
.review-col-title {
  font-size: .60rem; font-weight: 700;
  color: var(--text-3);
  letter-spacing: 1.4px; text-transform: uppercase;
  margin-bottom: .35rem;
}
.review-col ul { margin: 0; padding: 0; list-style: none; }
.review-col ul li {
  font-size: .78rem; color: var(--text-2);
  line-height: 1.6; margin-bottom: .24rem;
  padding-left: 1rem; position: relative;
}
.review-col ul li::before {
  content: "▸"; position: absolute; left: 0;
  color: var(--b1); font-size: .65rem; top: .10rem;
}
.review-col.issues ul li::before { color: var(--warn); }
.review-col.notes  ul li::before { color: var(--b2); }

/* ════════════════════════════════════════════════════════════════════════
   INTENT CARD
════════════════════════════════════════════════════════════════════════ */
.intent-card {
  background: var(--b4);
  border: 1px solid rgba(0,61,165,.15);
  border-radius: var(--r-lg);
  padding: .95rem 1.2rem;
  margin-top: .6rem;
}
.intent-grid {
  display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: .6rem; margin-top: .5rem;
}
.intent-item {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: .55rem .75rem;
  transition: box-shadow .15s;
}
.intent-item:hover { box-shadow: var(--sh-sm); }
.intent-item-label {
  font-size: .57rem; font-weight: 700;
  color: var(--text-3);
  letter-spacing: 1.2px; text-transform: uppercase;
  margin-bottom: .22rem;
}
.intent-item-val { font-size: .76rem; color: var(--text); line-height: 1.5; }
.intent-item-val .tag {
  display: inline-block;
  background: rgba(0,61,165,.08);
  border-radius: 12px; padding: 1px 8px;
  font-size: .64rem; color: var(--b1);
  margin: .1rem .12rem .1rem 0;
}
.intent-item-val .tag-warn {
  background: rgba(180,83,9,.09);
  color: var(--warn);
}
.intent-summary { font-size: .82rem; color: var(--b1); font-weight: 500; line-height: 1.55; }

/* ════════════════════════════════════════════════════════════════════════
   EXPLANATION CARD
════════════════════════════════════════════════════════════════════════ */
.exp-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-left: 3px solid var(--yellow);
  border-radius: var(--r-lg);
  padding: 1.1rem 1.4rem;
  margin-top: .7rem;
  box-shadow: var(--sh);
}
.exp-title {
  font-size: .65rem; font-weight: 700;
  color: var(--b1);
  letter-spacing: 1.5px; text-transform: uppercase;
  margin-bottom: .55rem;
  display: flex; align-items: center; gap: 7px;
}
.exp-title::before {
  content: ""; width: 3px; height: 12px;
  background: var(--yellow); border-radius: 2px; flex-shrink: 0;
}
.exp-card ul { margin: .2rem 0 0 1rem; padding: 0; list-style: none; }
.exp-card ul li {
  font-size: .81rem; color: var(--text-2);
  line-height: 1.65; margin-bottom: .28rem;
  padding-left: 1rem; position: relative;
}
.exp-card ul li::before {
  content: "▸"; position: absolute; left: 0;
  color: var(--b2); font-size: .68rem; top: .10rem;
}

/* ════════════════════════════════════════════════════════════════════════
   ALERTS  (corporate style)
════════════════════════════════════════════════════════════════════════ */
.alert {
  background: var(--white);
  border: 1px solid #BFDBFE;
  border-left: 4px solid var(--b1);
  border-radius: var(--r);
  padding: 1.1rem 1.3rem;
  margin-top: .9rem;
  box-shadow: var(--sh-sm);
  font-family: var(--sans);
}
.alert.warn  { border-left-color: var(--warn); border-color: var(--warn-brd); }
.alert.info  { border-left-color: var(--ok);   border-color: var(--ok-brd);   }
.alert-h {
  display: flex; align-items: center; gap: 9px;
  margin-bottom: .5rem;
}
.alert-ic {
  width: 30px; height: 30px; border-radius: 8px;
  background: var(--b3);
  display: flex; align-items: center; justify-content: center;
  font-size: .85rem; flex-shrink: 0;
}
.alert.warn .alert-ic { background: var(--warn-bg); }
.alert.info .alert-ic { background: var(--ok-bg); }
.alert-title { font-size: .85rem; font-weight: 700; color: var(--b1); }
.alert.warn .alert-title { color: var(--warn); }
.alert.info .alert-title { color: var(--ok);   }
.alert-body {
  font-size: .79rem; color: var(--text-3);
  line-height: 1.65; padding-left: 39px;
}
.alert-body code {
  background: var(--b3); padding: 1px 5px;
  border-radius: 4px; font-family: var(--mono);
  font-size: .72rem; color: var(--b1);
}
.alert-body pre {
  background: var(--b4);
  border: 1px solid rgba(0,61,165,.18);
  border-radius: var(--r-sm);
  padding: 7px 11px;
  font-family: var(--mono); font-size: .72rem;
  color: var(--b1); margin: .45rem 0 .15rem;
}

/* ── schema badge ───────────────────────────────────────────────────── */
.sbadge {
  display: inline-flex; align-items: center; gap: 5px;
  background: var(--ok-bg);
  border: 1px solid var(--ok-brd);
  border-radius: 20px; padding: 3px 12px;
  font-size: .62rem; font-weight: 600;
  color: var(--ok); margin-bottom: .6rem;
}
.sbadge .dg { width: 5px; height: 5px; border-radius: 50%; background: var(--ok); }

/* ════════════════════════════════════════════════════════════════════════
   STATS ROW
════════════════════════════════════════════════════════════════════════ */
.stats {
  display: flex; gap: .75rem;
  margin-top: .85rem;
}
.stat {
  flex: 1;
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: .85rem .75rem;
  text-align: center;
  box-shadow: var(--sh-sm);
  transition: box-shadow .18s, transform .14s;
}
.stat:hover { box-shadow: var(--sh); transform: translateY(-2px); }
.stat .v { font-size: 1.2rem; font-weight: 800; color: var(--b1); }
.stat .l {
  font-size: .58rem; font-weight: 700;
  color: var(--text-3);
  letter-spacing: .9px; text-transform: uppercase;
  margin-top: 3px;
}

/* ════════════════════════════════════════════════════════════════════════
   EXPANDER  (History)
════════════════════════════════════════════════════════════════════════ */
.streamlit-expanderHeader {
  background: var(--white) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
  font-family: var(--sans) !important;
  font-size: .76rem !important;
  font-weight: 600 !important;
  color: var(--text-2) !important;
  box-shadow: var(--sh-sm) !important;
}
.streamlit-expanderContent {
  background: var(--white) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
}

/* ── history item ───────────────────────────────────────────────────── */
.hi {
  background: var(--white);
  border: 1px solid var(--border);
  border-left: 3px solid var(--yellow);
  border-radius: var(--r);
  padding: .72rem 1rem;
  margin-bottom: .4rem;
  box-shadow: var(--sh-sm);
  transition: box-shadow .15s;
}
.hi:hover { box-shadow: var(--sh); }
.hi .hp {
  font-size: .80rem; font-weight: 500; color: var(--text);
  margin-bottom: 3px;
  display: -webkit-box;
  -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden;
}
.hi .hm { font-size: .61rem; color: var(--text-4); }

/* ── code block (native st.code) ────────────────────────────────────── */
.stCodeBlock {
  border: 1px solid #252E45 !important;
  border-radius: var(--r) !important;
  box-shadow: 0 4px 16px rgba(0,0,0,.14) !important;
}
.stCodeBlock pre {
  background: #161B2A !important;
  font-family: var(--mono) !important;
  font-size: .79rem !important;
  color: #CDD6F4 !important;
}
div[data-testid="stCopyButton"] button {
  background: rgba(137,220,235,.10) !important;
  border: 1px solid rgba(137,220,235,.25) !important;
  color: #89DCEB !important;
  border-radius: 5px !important;
  font-size: .65rem !important;
}
div[data-testid="stCopyButton"] button:hover {
  background: #89DCEB !important; color: #161B2A !important;
}

/* ── spinner ────────────────────────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--b2) !important; }

/* ── page divider ───────────────────────────────────────────────────── */
.pdiv { height: 1px; background: var(--border); margin: 1.1rem 0; opacity: .5; }

/* ════════════════════════════════════════════════════════════════════════
   FOOTER
════════════════════════════════════════════════════════════════════════ */
.foot {
  text-align: center;
  padding: 1rem 0 .5rem;
  border-top: 1px solid var(--border);
  margin-top: 2.5rem;
}
.foot p {
  font-family: var(--sans);
  font-size: .60rem; color: var(--text-4);
  letter-spacing: .4px; margin: 0;
}
.foot p + p { margin-top: .2rem; }
.foot strong { color: var(--text-3); font-weight: 600; }
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

# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────
PIPELINE_SYSTEM = """You are TURKCELL SQL AI – an enterprise-grade SQL assistant.

Your job is to convert natural language into SAFE, CORRECT, and BUSINESS-ACCURATE SQL queries.

You MUST follow a structured reasoning pipeline.
You MUST follow all steps in order. You MUST NOT skip steps.

==================================
GLOBAL RULES
==================================
- ONLY generate SELECT queries
- NEVER generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE
- NEVER invent tables or columns
- Use ONLY the provided schema
- If something is ambiguous, DO NOT guess silently
- Prefer correctness over speed
- Assume corporate production environment
If user intent implies data modification, politely refuse.

==================================
STEP 1 – INTENT ANALYSIS
==================================
Analyze the user request carefully.
Extract: business intent, time meaning (be explicit), filters, metrics, ambiguity.

IMPORTANT: If the request contains ambiguous business terms like:
- "borçlu" → interpret as (total_amount - paid_amount) > 0
- "aktif müşteri" → has at least one activity/order in the defined period
- "yeni müşteri" → first transaction/registration within the defined period
- "hiç ödeme yapmamış" → paid_amount = 0 OR no payment records exist
You MUST state your assumption explicitly in the "assumptions" field.

Output MUST be valid JSON:
{
  "intent_summary": "",
  "time_interpretation": "",
  "filters": [],
  "metrics": [],
  "grouping": [],
  "assumptions": [],
  "ambiguities": []
}

==================================
STEP 2 – SQL GENERATION
==================================
Generate SQL using the structured intent from Step 1 and the provided schema.

Rules:
- PREFER mathematical conditions over status columns
  DO NOT rely only on: status = 'UNPAID'
  INSTEAD USE: (total_amount - paid_amount) > 0
- Use explicit JOIN (never implicit comma joins)
- Avoid SELECT *
- Use table aliases
- Apply correct time logic
- Keep query readable and maintainable

==================================
STEP 3 – SQL REVIEW
==================================
Review as a senior data engineer. Check for:
- Invalid/invented tables or columns
- Missing or incorrect JOIN conditions
- Cartesian joins
- Performance risks (no date filter, full table scans)
- Logical mismatches with the stated intent

Output MUST be valid JSON:
{
  "status": "SAFE | RISKY | INVALID",
  "issues": [],
  "notes": []
}

==================================
STEP 4 – BUSINESS EXPLANATION
==================================
Write a short, clear business explanation in Turkish (3-5 bullet points).
Cover:
- What the query does in plain language
- Which tables and joins are used
- What assumptions were made and WHY
- Any caveats the business user should know

==================================
FINAL OUTPUT FORMAT
==================================
Return your response in FOUR clearly separated sections:
--- INTENT ---
(JSON from Step 1)
--- SQL ---
(SQL query only, no fences, no prose)
--- REVIEW ---
(JSON from Step 3)
--- EXPLANATION ---
(bullet points from Step 4, plain text, each line starts with •)
Do NOT add any extra text outside these four sections."""


def build_user_msg(prompt, dialect, style, schema):
    style_note = {
        "Standard":  "Use uppercase keywords and clean multi-line formatting.",
        "Compact":   "Use compact, minimal whitespace.",
        "Annotated": "Add a brief SQL comment above each major clause.",
    }.get(style, "")

    parts = [f"DIALECT: {dialect}", f"STYLE: {style_note}"]
    if schema:
        parts.append(f"DATABASE SCHEMA:\n{schema.strip()}")
    parts.append(f"USER REQUEST: {prompt.strip()}")
    return "\n\n".join(parts)


def run_pipeline(prompt, key, dialect, style, model, schema=None):
    """Single API call → returns {intent, sql, review, tokens, elapsed}."""
    t0 = time.time()
    client = openai.OpenAI(api_key=key)
    r = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": PIPELINE_SYSTEM},
            {"role": "user",   "content": build_user_msg(prompt, dialect, style, schema)},
        ],
        temperature=0.1,
        max_tokens=2400,
    )
    raw_out = r.choices[0].message.content.strip()
    elapsed = round(time.time() - t0, 2)
    tokens  = r.usage.total_tokens

    # ── parse four sections ──────────────────────────────────────────────────
    def extract(tag, text):
        m = re.search(rf"---\s*{tag}\s*---(.+?)(?=---\s*[A-Z]|$)", text, re.S | re.I)
        return m.group(1).strip() if m else ""

    intent_raw      = extract("INTENT",      raw_out)
    sql_raw         = extract("SQL",         raw_out)
    review_raw      = extract("REVIEW",      raw_out)
    explanation_raw = extract("EXPLANATION", raw_out)

    # parse JSON blocks safely
    def safe_json(text):
        text = text.strip()
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try: return json.loads(m.group(0))
            except Exception: pass
        return {}

    intent = safe_json(intent_raw)
    review = safe_json(review_raw)
    sql    = sql_raw.strip()

    # strip any stray fences from SQL block
    sql = re.sub(r"^```[a-zA-Z]*\n?", "", sql).strip()
    sql = re.sub(r"\n?```$", "", sql).strip()

    # normalise explanation into bullet list
    exp_lines = [
        l.strip().lstrip("•-* ").strip()
        for l in explanation_raw.splitlines()
        if l.strip() and not l.strip().startswith("---")
    ]

    return {
        "sql":         sql,
        "intent":      intent,
        "review":      review,
        "explanation": exp_lines,
        "tokens":      tokens,
        "elapsed":     elapsed,
        "raw":         raw_out,
    }


def run_explain(sql, key, dialect, model):
    """Separate Turkish explanation call (non-critical)."""
    explain_sys = (
        f"Aşağıdaki {dialect} SQL sorgusunu kısa ve anlaşılır Türkçe ile açıkla.\n"
        f"Yanıtını SADECE madde madde ver, her madde '•' ile başlasın.\n"
        f"Hangi tabloların kullanıldığını, hangi filtrelerin uygulandığını, "
        f"hangi sütunların döndürüldüğünü ve varsa gruplama/sıralama işlemlerini belirt.\n"
        f"Toplam 4-6 madde yaz, markdown kullanma, sadece düz metin.\n\nSQL:\n{sql}"
    )
    r = openai.OpenAI(api_key=key).chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": explain_sys}],
        temperature=0.3, max_tokens=400,
    )
    return r.choices[0].message.content.strip()

def chk(sql):
    if not sql or sql.upper().startswith("ERROR"):
        return False, sql.replace("ERROR:", "").strip() if sql else "Model yanıt vermedi."
    # block write ops
    danger = re.compile(r"^\s*(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|GRANT|REVOKE)\b", re.I)
    if danger.search(sql):
        return False, "Güvenlik: Yalnızca SELECT sorguları üretilebilir. Yazma işlemi reddedildi."
    if len(sql) < 10: return False, "Model beklenmedik kısa yanıt döndürdü."
    return True, ""

def dl(sql):
  # ── "AI NE ANLADI" bloğu ─────────────────────────────────────────────────────
def render_intent_block(intent: dict) -> None:
    """SQL üretilmeden önce AI'ın isteği nasıl yorumladığını gösterir."""
    if not intent:
        return

    def _pills(items, color="#003DA5"):
        if not items:
            return "—"
        style = (f"display:inline-block;background:rgba(0,61,165,.09);"
                 f"border:1px solid rgba(0,61,165,.18);border-radius:20px;"
                 f"padding:2px 10px;font-size:.72rem;font-family:monospace;"
                 f"color:{color};margin:2px 3px 2px 0")
        return " ".join(f'<span style="{style}">{i}</span>'
                        for i in items if str(i).strip())

    summary     = intent.get("intent_summary", "—")
    time_val    = intent.get("time_interpretation") or intent.get("time_range") or "—"
    filters     = intent.get("filters",     [])
    metrics     = intent.get("metrics",     [])
    entities    = intent.get("entities",    [])
    assumptions = intent.get("assumptions", [])
    ambiguities = intent.get("ambiguities") or intent.get("missing_info") or []

    rows = [
        ("🕐", "Zaman",         f'<span style="color:#0057D9;font-weight:600">{time_val}</span>'),
        ("🏷️", "Filtreler",     _pills(filters)),
        ("📊", "Metrikler",     _pills(metrics)),
        ("🔗", "Tablolar",      _pills(entities, "#0D7F4D")),
        ("❓", "Belirsizlikler",_pills(ambiguities, "#B45309") if ambiguities else "—"),
    ]

    rows_html = "".join(
        f'<div style="display:flex;gap:8px;align-items:baseline;'
        f'padding:.28rem 0;border-bottom:1px solid rgba(0,61,165,.07)">'
        f'<span style="font-size:.72rem;width:18px;flex-shrink:0">{ic}</span>'
        f'<span style="font-size:.60rem;font-weight:700;color:#6B7A90;'
        f'letter-spacing:1.2px;text-transform:uppercase;width:90px;flex-shrink:0">'
        f'{lbl}</span>'
        f'<span style="font-size:.77rem;color:#3D4A5C;line-height:1.5">{val}</span>'
        f'</div>'
        for ic, lbl, val in rows
    )

    assumption_html = "".join(
        f'<div style="display:flex;gap:6px;background:rgba(255,199,44,.12);'
        f'border:1px solid rgba(255,199,44,.35);border-radius:7px;'
        f'padding:.4rem .75rem;margin-top:.3rem;font-size:.75rem;color:#3D4A5C">'
        f'<span>⚡</span><span>{a}</span></div>'
        for a in assumptions if str(a).strip()
    )

    html = f"""
<div style="background:linear-gradient(135deg,#EEF5FF,#E6EFFF);
            border:1px solid rgba(0,61,165,.16);border-radius:12px;
            overflow:hidden;margin:.6rem 0;
            box-shadow:0 4px 12px rgba(0,0,0,.07)">
  <!-- header -->
  <div style="background:linear-gradient(90deg,#003DA5,#0057D9);
              padding:.6rem 1.2rem;display:flex;align-items:center;gap:9px">
    <span style="font-size:1.05rem">🧠</span>
    <span style="font-size:.65rem;font-weight:700;color:#fff;
                 letter-spacing:1.8px;text-transform:uppercase">
      AI NE ANLADI?
    </span>
    <span style="margin-left:auto;background:rgba(255,255,255,.15);
                 border:1px solid rgba(255,255,255,.25);border-radius:20px;
                 padding:2px 11px;font-size:.58rem;font-weight:600;
                 color:rgba(255,255,255,.85)">Intent Analizi</span>
  </div>
  <!-- summary -->
  <div style="padding:.8rem 1.2rem .55rem;font-size:.83rem;font-weight:500;
              color:#003DA5;line-height:1.55;
              border-bottom:1px solid rgba(0,61,165,.10)">
    <span style="display:inline-block;width:20px;height:20px;
                 background:#FFC72C;border-radius:5px;text-align:center;
                 line-height:20px;font-size:.70rem;margin-right:6px;
                 vertical-align:middle">→</span>
    {summary}
  </div>
  <!-- detail rows -->
  <div style="padding:.65rem 1.2rem .5rem">{rows_html}</div>
  <!-- assumptions -->
  {"<div style='padding:0 1rem .7rem'>" + assumption_html + "</div>" if assumption_html else ""}
</div>"""

    st.markdown(html, unsafe_allow_html=True)
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
        f'</div><div class="hdr-pill">v4.1</div></div>',
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
    f'</div><div class="hdr-pill">v4.1 · Pipeline</div></div>',
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

    with st.spinner("Pipeline çalışıyor: Intent → SQL → Review…"):
        try:
            res = run_pipeline(prompt, api_key, dialect, style, model, schema_text)
        except openai.AuthenticationError:
            st.markdown(mk_alert("🔑","Kimlik Hatası","API anahtarı reddedildi."),
                unsafe_allow_html=True); st.stop()
        except openai.RateLimitError:
            st.markdown(mk_alert("⏱","Limit Aşıldı","OpenAI kotası doldu. Kısa süre bekleyip tekrar deneyin."),
                unsafe_allow_html=True); st.stop()
        except openai.APIConnectionError:
            st.markdown(mk_alert("🌐","Bağlantı Hatası","OpenAI API'ye ulaşılamadı."),
                unsafe_allow_html=True); st.stop()
        except Exception as e:
            st.markdown(mk_alert("⚙️","Beklenmeyen Hata",f"Sorun oluştu:<br><code>{e}</code>"),
                unsafe_allow_html=True); st.stop()

    valid, err = chk(res["sql"])
    if not valid:
        st.markdown(mk_alert("⚠️","Güvenlik Reddi",err,"warn"),
            unsafe_allow_html=True); st.stop()

    # ── store history ─────────────────────────────────────────────────────
    st.session_state.qc += 1
    st.session_state.tt += res["tokens"]
    st.session_state.history.insert(0,{
        "prompt": prompt, "sql": res["sql"], "dialect": dialect,
        "ts":     datetime.datetime.now().strftime("%d %b %Y %H:%M"),
        "tokens": res["tokens"],
        "schema": schema_meta.get("name","—") if schema_text else "—",
    })
    st.session_state.history = st.session_state.history[:30]

    # ── INTENT CARD ──────────────────────────────────────────────────────
    intent = res.get("intent", {})
    if intent:
        def tag_list(items, warn=False):
            cls = "tag-warn" if warn else "tag"
            if not items: return f'<span class="{cls}">—</span>'
            return " ".join(f'<span class="{cls}">{i}</span>' for i in items if i)

        st.markdown(
            '<div class="intent-card">'
            '<div class="exp-title">🎯 Intent Analizi</div>'
            f'<div class="intent-summary">{intent.get("intent_summary","—")}</div>'
            '<div class="intent-grid">'
            f'<div class="intent-item"><div class="intent-item-label">Zaman Yorumu</div><div class="intent-item-val">{intent.get("time_interpretation", intent.get("time_range","—")) or "—"}</div></div>'
            f'<div class="intent-item"><div class="intent-item-label">Tablolar</div><div class="intent-item-val">{tag_list(intent.get("entities",[]))}</div></div>'
            f'<div class="intent-item"><div class="intent-item-label">Metrikler</div><div class="intent-item-val">{tag_list(intent.get("metrics",[]))}</div></div>'
            f'<div class="intent-item"><div class="intent-item-label">Filtreler</div><div class="intent-item-val">{tag_list(intent.get("filters",[]))}</div></div>'
            f'<div class="intent-item"><div class="intent-item-label">Gruplama</div><div class="intent-item-val">{tag_list(intent.get("grouping",[]))}</div></div>'
            f'<div class="intent-item"><div class="intent-item-label">Belirsizlikler</div><div class="intent-item-val">{tag_list(intent.get("ambiguities", intent.get("missing_info",[])), warn=True)}</div></div>'
            '</div></div>',
            unsafe_allow_html=True)

    # ── SQL CARD (dark) ───────────────────────────────────────────────────
    sb = ""
    if schema_text:
        sb = ('<span class="sql-tag" style="background:rgba(166,227,161,.12);color:#A6E3A1;">' +
              '<span class="dot" style="background:#A6E3A1"></span>' +
              f'{schema_meta["name"]}</span>')

    sql_esc = res["sql"].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")\
                        .replace('"',"&quot;").replace("'","&#39;")

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

    col_code, col_dl = st.columns([4, 1])
    with col_code:
        st.code(res["sql"], language="sql")
    with col_dl:
        st.markdown(dl(res["sql"]), unsafe_allow_html=True)

    # ── REVIEW CARD ──────────────────────────────────────────────────────
    review = res.get("review", {})
    if review:
        status = review.get("status","SAFE").upper()
        status_html = {
            "SAFE":    '<span class="status-safe">✓ SAFE</span>',
            "RISKY":   '<span class="status-risky">⚠ RISKY</span>',
            "INVALID": '<span class="status-invalid">✗ INVALID</span>',
        }.get(status, f'<span class="status-safe">{status}</span>')

        issues = review.get("issues", [])
        notes  = review.get("notes",  [])
        issue_li = "".join(f"<li>{i}</li>" for i in issues) if issues else "<li>Sorun tespit edilmedi</li>"
        notes_li = "".join(f"<li>{n}</li>" for n in notes)  if notes  else "<li>—</li>"

        st.markdown(
            '<div class="review-card">'
            '<div class="exp-title">🔍 SQL İnceleme</div>'
            f'<div style="margin:.3rem 0 .55rem">{status_html}</div>'
            '<div class="review-grid">'
            '<div class="review-col issues"><div class="review-col-title">Sorunlar</div><ul>' + issue_li + '</ul></div>'
            '<div class="review-col notes"><div class="review-col-title">Notlar</div><ul>' + notes_li + '</ul></div>'
            '</div></div>',
            unsafe_allow_html=True)

    # ── STATS ─────────────────────────────────────────────────────────────
    st.markdown(
        f'<div class="stats">'
        f'<div class="stat"><div class="v">{st.session_state.qc}</div><div class="l">Sorgular</div></div>'
        f'<div class="stat"><div class="v">{res["elapsed"]}s</div><div class="l">Süre</div></div>'
        f'<div class="stat"><div class="v">{st.session_state.tt}</div><div class="l">Token</div></div>'
        f'</div>',
        unsafe_allow_html=True)

    # ── EXPLANATION (from pipeline Step 4) ────────────────────────────────
    exp_lines = res.get("explanation", [])

    # Fallback: if pipeline didn't return explanation, call separately
    if not exp_lines:
        try:
            fallback = run_explain(res["sql"], api_key, dialect, model)
            exp_lines = [l.strip().lstrip("•-* ").strip()
                         for l in fallback.splitlines() if l.strip()]
        except Exception:
            pass

    if exp_lines:
        bullets = "".join(f"<li>{l}</li>" for l in exp_lines if l)
        # highlight any assumption lines with a distinct style
        bullets_rich = ""
        for l in exp_lines:
            if l:
                lower = l.lower()
                is_assumption = any(w in lower for w in
                    ["varsayım","kabul edildi","tanım","assumption",
                     "yorumlandı","borçlu","aktif","hiç ödeme"])
                if is_assumption:
                    bullets_rich += f'<li style="color:var(--navy);font-weight:600;">{l}</li>'
                else:
                    bullets_rich += f"<li>{l}</li>"
        st.markdown(
            '<div class="exp-card"><div class="exp-title">💡 İş Açıklaması & Varsayımlar</div>'
            f'<ul>{bullets_rich}</ul></div>',
            unsafe_allow_html=True)


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