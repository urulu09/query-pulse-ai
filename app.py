"""
TURKCELL SQL AI — app.py  v4.1
"""
import streamlit as st
import openai
import re, time, datetime, json, base64 as b64lib
import sqlite3, hashlib
try:
    import bcrypt
    BCRYPT_OK = True
except ImportError:
    BCRYPT_OK = False

_L = "/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAC3ALYDASIAAhEBAxEB/8QAHAABAQACAwEBAAAAAAAAAAAAAAgBBwIFBgME/8QAQhAAAQMCAgQNAgMGBAcAAAAAAAECAwQFBhEHEiExCAkTGDdBUVZhdpS01BQiMnGBFiRSkdHhFSOhwTZCcnOys8L/xAAbAQEAAgMBAQAAAAAAAAAAAAAAAQQCAwUGB//EAC4RAAICAgEDAgMIAwEAAAAAAAABAgMEEQUSITFBUSJhkQYTFBUycYGxM6HRwf/aAAwDAQACEQMRAD8A89wTdBuGdLOjq4YjxHesQUtXTXeSiYyglgZGrGwwvRVR8L11s5HdeWSJsNwcz3R13mxn6mk+Ofi4uLoQvPmSf21MUyATnzPdHXebGfqaT445nujrvNjP1NJ8cowAE58z3R13mxn6mk+OOZ7o67zYz9TSfHKMABOfM90dd5sZ+ppPjjme6Ou82M/U0nxyjAATnzPdHXebGfqaT445nujrvNjP1NJ8cowAE58z3R13mxn6mk+OOZ7o67zYz9TSfHKMABOfM90dd5sZ+ppPjjme6Ou82M/U0nxyjAATnzPdHXebGfqaT445nujrvNjP1NJ8cowAE58z3R13mxn6mk+OOZ7o67zYz9TSfHKMABOfM90dd5sZ+ppPjjme6Ou82M/U0nxyjAATnzPdHXebGfqaT445nujrvNjP1NJ8cowAE58z3R13mxn6mk+OCjAATNxcXQhefMk/tqYpkmbi4uhC8+ZJ/bUxTIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABM3FxdCF58yT+2pimSZuLi6ELz5kn9tTFMgAAAAAAAAAAAAAAZoAAAAAAAAAAAAAAAAAAATNxcXQhefMk/tqYpkmbi4uhC8+ZJ/bUxTIAAAAAAAAAAMLvM5+Bxkc1iK5yoiImaqpDaS2DIPKXjF8ED1ioY+XcmxXquTf7nTLi67q/NFhROzU/ueUzPtnxeLNw6nLXnS2jpVcTk2R3rX7mw8zkeLteM1VyMr4ERFX8cf8AQ9dTVMVTC2WByPY5M0VFOtxnN4fJxbx57a9PDK2RiXY71Yj7AxmZOsVgAAAAAAAAAAACZuLi6ELz5kn9tTFMkzcXF0IXnzJP7amKZAAAAAAAAUAAxmePx7dXtcy2U6uRz0zkVu/JdyHsFQ6d1ppIbpUXeodrqrUVEcmxiIn9jic9jZGXiuiiXT1P4n7R9S3hWQqt65revC+Z5vDNifHVRVtySOKFNrGSKmbndWw7PHsdClqa5yMSoRycnlv8f9Dy+ILtLc650iuVsLFyjYi7k7fzPjQ0NwucmrDHJLls1nLsT9T5kuVxoY9nF4NPX1dlL1b99a+h6H8LZKccm+eten/n/T8W89Fgm6vpLg2jkd/kzLqoi/8AK7q/megwxZoLbE9KlYZKp2/Lbqp2Hm8YJSwXxr6LJrkRHORvU7MU8NlcHXVyLsSltJx/d91/0meXXmyljqPbXZmxW5+ByOES5tavaiHM+zQl1RTPJAAGQAAAAAAAAAJm4uLoQvPmSf21MUyTNxcXQhefMk/tqYpkAAAAAAAAAAHQY6mfDY3oxVTlHI1fyO/Py3Kjgr6Z1NUs1o16s8ihymPZk4dlNT1KSaRux7I12xnLwma/wtY33SflJc20rF+5ety9iHe4mvEVngS22xjGS6v3K1PwJ/U9DFBFb7esdNHqsjaqoiGq6yaSpqpJ5VVXvcqrmfN+VrX2Z4+FFH+aze5f3o7+M3yV7nP9MfCMLPOsqyrM/XdvdrLmp+qyUklwu0EO1yK9HPVepqLtPjRUVXWypFTQPkcvYmxPzU2DhiyMtUOvIqPqHp9zk6vBDhfZzgsrk8mNk0/u09tv1+SLvIZtWPW1H9T7HdNTLJDkYTeZPua7I8aAASAAAAAAAAACZuLi6ELz5kn9tTFMkzcXF0IXnzJP7amKZAAMKdPjLENtwphutv8AdpHR0lIzWfqpm5yqqI1qJ2qqon6kxi5NRXlkSkorb8HcnCWWKLLlJGMz3azsifW8KGwrHKrsNV7XtdlEnLNyeniuWxf5nleEzidmLMBYNxHSwSUkVa+dyROfmrcl1dqp+R0quKvdkYWLpT9f4OfZyVKrcq3toq9FRURUXNF3KDwNbjSzYH0WWe83qV+p9DTsjijTN8rljbsRP9zxOE+Ejhm8XuG3XC1VVrjnekcdQ+RHszVck1tiZJ47StDCvsi5QjtL1LE8ymtqM5abN4OmhbIkbpWI9dzVdtOakl8IW8xWThE227TrK+mpYKaZ7Y12uRFcuw2ho60+YfxfiiGwSWuqtk9S5W0z5JEe2R3Ui5JsVf1LFvF2xpjbBbTW38jRXyFcrJVy7NPS+ZuPeipvPxS222ZrLLS06ZbVcrUNP464QtpwziaqsiYbuVTJSPVkr5HJDt7URUVVTsXYZxfpEsukHQJiq4WfloJaenRlRBLsfGqqipu3ovb4KVnxM7eh2w+FtLbSfk3fmFcOpQl3RuembTpH+7JEjN32ZZf6HOSWKPLlJGMz3azsszTfA+c52ipyucrl+ul3rn2HkuG097GYZ1XOamtNnkv/AEm6rjk8p4qfZbW9GuebrG/ENFKIqKiKi5ofJ9VTsmSF88TZF3NV6Iq/oaAwnwjsNRvtlmrLVXU1KyKKB1a56KiKjUarlb2Z+J9cfLgV3CGtC3F17/x5XU/I8i1i0+9dXNVXP8yVxtsZuNia7N+N+CHn1yipQaf8m/GzQukWNsrFem9qOTM+hLOjx714Xt7ar3av1NZsz2GxNJWnrD+DsUy4fZbaq51FOqJUviejGxKqZ6qZ/iVM9v8AIm3jrFZGuv4m0mK8+twc59kno3C5URFVVyQ+cFTTzqqQzxyK3ejXouRqPAmm2zY7v9Vh+ks9ZTs+mlk5d725q1rf4epVTxOm4Mv7ELiPEf7KLelqNRn1P1zWI3LXdlq6qr15mDwbIQm7E0467a9/6M1mQnKKhpp7N9AJuBRLgAABM3FxdCF58yT+2pimSZuLi6ELz5kn9tTFMgGFNU8K2KWXQtdFiRzkZNTufl/Dyrf98jazuw6TG8qwYUuUqWh15yp3J9C1qO+oRdmrkuxU7fA34tjruhJLw0aMmCsqlF+qI0uuI8JzaB7dhynpmpiCK4LLK9Icl1PuzXX68802eB2Wk1FTQNo5VUyT95/81Px3qhrsRUrLFYdEs1nuUtQjpp4453LszTVTlNjG7c13bilLPoqtFboksuDcUw8u6ji1lfC7VdFIqqrtV36qniepycurGdc3v9TbW9+h57Hx7L+uK9kt614ZpzhIXCkuui3A89troKynhjbFM6GRHpHIkLftdkuxU7FPP6d7jhG4YUwTDhmSgfVxUDWztpkTXZ9jPtfltR2tnsXbvKOtGiHB9vwXVYRdT1FZbqmZZ3cvJm9smSJrNciJkqZHUYV0BYDsF6iurIq2tlgej4WVUqOY1yblyREzy8SjRyWNVFLv8Levnv3Ld3H32Sfj4tb+WjS2md9LTadcOSXzV+mjoqFarlUzRETPWz8DGLq6w1nCdtlZhd1LPRfUUyq6jROTe9GprauWxf65m/Md6HMJYzxK2/3n651QkTYljimRsatbnlsyz6+0+GBNCWC8H35t7oI6upq48+QWpkRyRZ9aIiJt/MmPJ46qW99Si1r07kPj73Y/GnLe/wBjSdTpDxXjTEGInUdfhixU0MLmPSuZG180SK5EbrORVeu/Z1ZnQaIs10T6UURc0+ipV2bvxyFAXzQBgC7Ygmu8sFbAs71klp4ZkbE5y7VXLLNNvVmdxgXRJhTCNLeKSgZVVNNd4mxVUVVIj2uY3W2JkifxqTLlMVVdNa147a9n7+pEeOvdnVP5+vueM4Hd0trtH0lpbX0y3BlVLMtLyqcqjM0TW1d+rtTbuPO8Nz8GGuzWm/8Ag2po/wBEeFsD4knvliWtbPNA6BY5ZtdjWuc1y5JlnvanWfr0m6NLBpBbRJfJKxn0auWP6eRG/iyzzzRewpxzaY5/4hb6X3+paeLbLD+5et+CYtPtywfXYfwczDUtvdPDbmtqkp0aisXVb9r8uvPPeehxq2RvCYwm2RHI9IqBHIu9Fy2/qbWtvB70fUN7iubYa6ZsT0kbTSz60SuTdmmWap4ZnoL5otw7ecf0uNaqStbcqVY1Y1kqJH9m7NMvHtLf5njx1GLbWpd37srLjrpNylpNtf6NFYRuVvtHC1vdXdK2noaf6uqbytRIjG5ruTNdm06mS62XDXCfvNyxXDr0Da6dy68XKJk9ucbsutMlRTf+OtDGC8XX9b7Xw1dPXv1eUfTSo1JFTcrkVF25Im01zp+qqamxrCyr0UPv0EFO1iXBWyNWVckyTWj3om7J3j1GeNl132JRT7x0/C8exhfjWUw3JrtLa9fqeK0DVVFXacL3WW2NIqKemrZIGaurqsXNUTLq2HpeBl/xdi3/ALcf/sefTg0YEvsmMbli67WiSy2+aGWOCndGsarynU1q7UaieHYbi0b6McPYDuFwrrLLWvlr0RJuXlRyJkqrsyRO0x5LLqi7al3bUUv49zPBxrH93Y+yTb+p7lNwCbgebO8AAATNxcXQhefMk/tqYpkmbi4uhC8+ZJ/bUxTIBhUzMK38jkBoHHVTPPYZy7TIAMZKMlMgAZGFQyADGrtzM5AADIxkZAAyMZGQAYVM95jU7TkADijTKIZAAAAAAABM3FxdCF58yT+2pimSZuLi6ELz5kn9tTFMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEzcXF0IXnzJP7amKZJm4uLoQvPmSf21MUyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATNxcXQhefMk/tqYpkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//2Q=="
LOGO_SRC = f"data:image/png;base64,{_L}"

st.set_page_config(
    page_title="turkcell.sql.ai.com.tr",
    page_icon="🟡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
  --b1:#003DA5;--b2:#0057D9;--b3:#E8EFFE;--b4:#F0F4FF;
  --yellow:#FFC72C;--yel-dk:#E6AE00;--yel-lt:#FFF9E6;
  --bg:#F5F7FA;--white:#FFFFFF;--text:#0F1623;--text-2:#3D4A5C;
  --text-3:#6B7A90;--text-4:#9AA5B4;--border:#DCE3ED;--border-lt:#EEF2F7;
  --ok:#0D7F4D;--ok-bg:#EDFAF3;--ok-brd:#A3DFBE;
  --warn:#B45309;--warn-bg:#FFFBEB;--warn-brd:#FDE68A;
  --err:#B91C1C;--err-bg:#FEF2F2;--err-brd:#FECACA;
  --sh-sm:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);
  --sh:0 4px 12px rgba(0,0,0,.07),0 1px 4px rgba(0,0,0,.04);
  --sh-md:0 8px 24px rgba(0,0,0,.09),0 2px 6px rgba(0,0,0,.05);
  --sh-blue:0 0 0 3px rgba(0,61,165,.14);
  --r:10px;--r-sm:7px;--r-lg:14px;
  --sans:'Inter',system-ui,sans-serif;
  --mono:'JetBrains Mono','Roboto Mono',monospace;
}
*,*::before,*::after{box-sizing:border-box;}
html,body{background:var(--bg)!important;min-height:100vh;font-family:var(--sans)!important;color:var(--text);-webkit-font-smoothing:antialiased;}
.stApp,.stApp>div,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],section.main,section.main>div,.block-container{background:transparent!important;}
#MainMenu,footer,header{visibility:hidden!important;}
[data-testid="collapsedControl"]{display:none!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px;}
::-webkit-scrollbar-thumb:hover{background:var(--b2);}
.block-container{max-width:1100px!important;padding:0 1.5rem 5rem!important;margin:0 auto!important;}
div[data-testid="stVerticalBlock"]>div{margin-bottom:0!important;}
div[data-testid="element-container"]{margin:0!important;padding:0!important;}

.hdr{background:linear-gradient(100deg,#002A80 0%,var(--b1) 45%,var(--b2) 100%);margin:0 -1.5rem 1.8rem;padding:0 2.5rem;height:62px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 2px 16px rgba(0,30,100,.22),0 1px 0 rgba(255,255,255,.06) inset;position:relative;overflow:hidden;}
.hdr::before{content:"";position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.30),transparent);}
.hdr::after{content:"";position:absolute;right:-60px;top:-40px;width:280px;height:160px;background:radial-gradient(ellipse,rgba(255,199,44,.12),transparent 70%);pointer-events:none;}
.hdr-left{display:flex;align-items:center;gap:14px;z-index:1;}
.hdr-logo{height:34px;width:auto;display:block;background:rgba(255,255,255,.97);border-radius:7px;padding:3px 9px;box-shadow:0 1px 4px rgba(0,0,0,.12);}
.hdr-vline{width:1px;height:22px;background:rgba(255,255,255,.22);flex-shrink:0;}
.hdr-title{font-size:1.05rem;font-weight:800;color:#fff;letter-spacing:.3px;line-height:1.2;}
.hdr-sub{font-size:.52rem;font-weight:500;color:rgba(255,255,255,.48);letter-spacing:2px;text-transform:uppercase;margin-top:2px;}
.hdr-pill{z-index:1;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:20px;padding:4px 14px;font-size:.58rem;font-weight:600;color:rgba(255,255,255,.80);letter-spacing:.9px;text-transform:uppercase;backdrop-filter:blur(4px);}

.card{background:var(--white);border:1px solid var(--border);border-radius:var(--r-lg);box-shadow:var(--sh);padding:1.5rem 1.8rem 1.6rem;margin-bottom:.9rem;transition:box-shadow .2s;}
.card:hover{box-shadow:var(--sh-md);}
.upload-card{background:linear-gradient(135deg,#EEF3FF 0%,#E3ECFF 100%);border:1.5px dashed rgba(0,61,165,.24);border-radius:var(--r-lg);padding:1.1rem 1.6rem .9rem;margin-bottom:.9rem;transition:border-color .2s;}
.upload-card:hover{border-color:var(--b1);}
.card-sep{height:1px;background:var(--border-lt);margin:1.1rem -1.8rem;}
.lbl{font-size:.65rem;font-weight:700;color:var(--b1);letter-spacing:1.6px;text-transform:uppercase;margin-bottom:.5rem;display:flex;align-items:center;gap:7px;}
.lbl::before{content:"";width:3px;height:13px;background:var(--yellow);border-radius:2px;flex-shrink:0;}
.upload-lbl{font-size:.68rem;font-weight:700;color:var(--b1);letter-spacing:1.4px;text-transform:uppercase;margin-bottom:.5rem;display:flex;align-items:center;gap:7px;}
.upload-lbl::before{content:"";width:3px;height:13px;background:var(--yellow);border-radius:2px;flex-shrink:0;}
.upload-help{font-size:.71rem;color:var(--text-3);line-height:1.65;padding:.45rem .75rem;background:rgba(255,255,255,.65);border-radius:var(--r-sm);border-left:2px solid rgba(0,61,165,.24);margin-top:.5rem;}
.upload-help code{background:rgba(0,61,165,.08);color:var(--b1);padding:1px 5px;border-radius:4px;font-family:var(--mono);font-size:.68rem;}
.schema-ok{display:flex;align-items:center;gap:7px;margin-top:.5rem;font-size:.70rem;font-weight:600;color:var(--ok);}
.schema-ok .dot{width:7px;height:7px;border-radius:50%;background:var(--ok);flex-shrink:0;}
.tbl-row{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.4rem;}
.tbl-chip{background:rgba(0,61,165,.07);border:1px solid rgba(0,61,165,.16);border-radius:20px;padding:2px 10px;font-family:var(--mono);font-size:.63rem;font-weight:500;color:var(--b1);}
.tbl-more{background:var(--border-lt);border:1px solid var(--border);border-radius:20px;padding:2px 10px;font-size:.63rem;color:var(--text-3);}

[data-testid="stFileUploader"]{background:transparent!important;border:none!important;}
[data-testid="stFileUploader"] label{display:none!important;}
[data-testid="stFileUploaderDropzone"]{background:rgba(255,255,255,.75)!important;border:1.5px dashed rgba(0,61,165,.28)!important;border-radius:var(--r)!important;transition:border-color .2s,background .2s!important;}
[data-testid="stFileUploaderDropzone"]:hover{border-color:var(--b1)!important;background:#fff!important;}
[data-testid="stFileUploaderDropzoneInstructions"] span{color:var(--text-3)!important;font-size:.74rem!important;}
[data-testid="stFileUploaderDropzone"] small{color:var(--text-4)!important;font-size:.61rem!important;}

.stSelectbox label{font-size:.62rem!important;font-weight:700!important;color:var(--text-3)!important;text-transform:uppercase!important;letter-spacing:.9px!important;}
.stSelectbox>div>div{background:var(--white)!important;border:1.5px solid var(--border)!important;border-radius:var(--r-sm)!important;font-family:var(--sans)!important;font-size:.84rem!important;color:var(--text)!important;transition:border-color .18s,box-shadow .18s!important;}
.stSelectbox>div>div:focus-within{border-color:var(--b1)!important;box-shadow:var(--sh-blue)!important;}
div[data-baseweb="select"]*{background:#fff!important;color:var(--text)!important;}
div[data-baseweb="popover"]*{background:#fff!important;border-color:var(--border)!important;color:var(--text)!important;}

.stTextArea label{display:none!important;}
.stTextArea textarea{background:var(--white)!important;border:1.5px solid var(--border)!important;border-radius:var(--r)!important;font-family:var(--sans)!important;font-size:.9rem!important;line-height:1.65!important;color:var(--text)!important;padding:12px 14px!important;resize:vertical!important;transition:border-color .18s,box-shadow .18s!important;box-shadow:var(--sh-sm)!important;}
.stTextArea textarea:focus{border-color:var(--b1)!important;box-shadow:var(--sh-blue)!important;outline:none!important;}
.stTextArea textarea::placeholder{color:var(--text-4)!important;}

.stButton>button{background:var(--yellow)!important;color:var(--b1)!important;font-family:var(--sans)!important;font-weight:700!important;font-size:.9rem!important;border:none!important;border-radius:var(--r-sm)!important;padding:.68rem 2.8rem!important;cursor:pointer!important;display:block!important;margin:.55rem auto 0!important;transition:background .15s,box-shadow .15s,transform .10s!important;box-shadow:0 4px 14px rgba(255,199,44,.38)!important;letter-spacing:.2px;}
.stButton>button:hover{background:var(--yel-dk)!important;box-shadow:0 6px 20px rgba(255,199,44,.50)!important;transform:translateY(-1px)!important;}
.stButton>button:active{transform:translateY(0)!important;box-shadow:0 2px 8px rgba(255,199,44,.28)!important;}

.sql-card{background:#161B2A;border:1px solid #252E45;border-radius:var(--r-lg);padding:1.3rem 1.5rem 1rem;box-shadow:0 8px 30px rgba(0,0,0,.20),0 2px 8px rgba(0,0,0,.12);margin-top:.6rem;}
.sql-card pre{font-family:var(--mono)!important;font-size:.80rem!important;line-height:1.82!important;color:#CDD6F4!important;margin:0!important;white-space:pre-wrap!important;word-break:break-word!important;}
.kw{color:#89DCEB;font-weight:700;}.fn{color:#A6E3A1;}.str{color:#F38BA8;}.cmt{color:#45475A;font-style:italic;}.num{color:#CBA6F7;}
.sql-bar{display:flex;align-items:center;justify-content:space-between;margin-top:.9rem;padding-top:.72rem;border-top:1px solid #252E45;}
.sql-tag{display:inline-flex;align-items:center;gap:5px;background:rgba(137,220,235,.10);border:1px solid rgba(137,220,235,.22);border-radius:20px;padding:3px 11px;font-size:.61rem;font-weight:600;color:#89DCEB;}
.sql-tag .dot{width:6px;height:6px;border-radius:50%;background:#A6E3A1;}
.clip-btn{display:inline-flex;align-items:center;gap:5px;background:rgba(137,220,235,.10);border:1px solid rgba(137,220,235,.22);border-radius:var(--r-sm);padding:3px 12px;font-family:var(--sans);font-size:.68rem;font-weight:600;color:#89DCEB;cursor:pointer;transition:background .15s;}
.clip-btn:hover{background:rgba(137,220,235,.22);}
.clip-btn.copied{color:#A6E3A1;border-color:rgba(166,227,161,.35);}
.dl-wrap{margin-top:.6rem;}
.dl-wrap a{display:inline-flex;align-items:center;gap:5px;background:transparent;border:1.5px solid rgba(0,61,165,.30);border-radius:var(--r-sm);padding:.36rem .9rem;font-size:.72rem;font-weight:600;color:var(--b1);text-decoration:none;transition:background .15s,border-color .15s;}
.dl-wrap a:hover{background:var(--b3);border-color:var(--b1);}

.status-safe{display:inline-flex;align-items:center;gap:6px;background:var(--ok-bg);border:1px solid var(--ok-brd);border-radius:20px;padding:3px 13px;font-size:.67rem;font-weight:700;color:var(--ok);}
.status-safe::before{content:"●";font-size:.55rem;color:var(--ok);}
.status-risky{display:inline-flex;align-items:center;gap:6px;background:var(--warn-bg);border:1px solid var(--warn-brd);border-radius:20px;padding:3px 13px;font-size:.67rem;font-weight:700;color:var(--warn);}
.status-risky::before{content:"●";font-size:.55rem;color:var(--warn);}
.status-invalid{display:inline-flex;align-items:center;gap:6px;background:var(--err-bg);border:1px solid var(--err-brd);border-radius:20px;padding:3px 13px;font-size:.67rem;font-weight:700;color:var(--err);}
.status-invalid::before{content:"●";font-size:.55rem;color:var(--err);}

.review-card{background:var(--white);border:1px solid var(--border);border-radius:var(--r-lg);padding:1.1rem 1.4rem;margin-top:.7rem;box-shadow:var(--sh);}
.review-grid{display:grid;grid-template-columns:1fr 1fr;gap:.8rem;margin-top:.6rem;}
.review-col-title{font-size:.60rem;font-weight:700;color:var(--text-3);letter-spacing:1.4px;text-transform:uppercase;margin-bottom:.35rem;}
.review-col ul{margin:0;padding:0;list-style:none;}
.review-col ul li{font-size:.78rem;color:var(--text-2);line-height:1.6;margin-bottom:.24rem;padding-left:1rem;position:relative;}
.review-col ul li::before{content:"▸";position:absolute;left:0;color:var(--b1);font-size:.65rem;top:.10rem;}
.review-col.issues ul li::before{color:var(--warn);}
.review-col.notes ul li::before{color:var(--b2);}

.intent-card{background:var(--b4);border:1px solid rgba(0,61,165,.15);border-radius:var(--r-lg);padding:.95rem 1.2rem;margin-top:.6rem;}
.intent-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.6rem;margin-top:.5rem;}
.intent-item{background:var(--white);border:1px solid var(--border);border-radius:var(--r);padding:.55rem .75rem;transition:box-shadow .15s;}
.intent-item:hover{box-shadow:var(--sh-sm);}
.intent-item-label{font-size:.57rem;font-weight:700;color:var(--text-3);letter-spacing:1.2px;text-transform:uppercase;margin-bottom:.22rem;}
.intent-item-val{font-size:.76rem;color:var(--text);line-height:1.5;}
.intent-item-val .tag{display:inline-block;background:rgba(0,61,165,.08);border-radius:12px;padding:1px 8px;font-size:.64rem;color:var(--b1);margin:.1rem .12rem .1rem 0;}
.intent-item-val .tag-warn{background:rgba(180,83,9,.09);color:var(--warn);}
.intent-summary{font-size:.82rem;color:var(--b1);font-weight:500;line-height:1.55;}

.exp-card{background:var(--white);border:1px solid var(--border);border-left:3px solid var(--yellow);border-radius:var(--r-lg);padding:1.1rem 1.4rem;margin-top:.7rem;box-shadow:var(--sh);}
.exp-title{font-size:.65rem;font-weight:700;color:var(--b1);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:.55rem;display:flex;align-items:center;gap:7px;}
.exp-title::before{content:"";width:3px;height:12px;background:var(--yellow);border-radius:2px;flex-shrink:0;}
.exp-card ul{margin:.2rem 0 0 1rem;padding:0;list-style:none;}
.exp-card ul li{font-size:.81rem;color:var(--text-2);line-height:1.65;margin-bottom:.28rem;padding-left:1rem;position:relative;}
.exp-card ul li::before{content:"▸";position:absolute;left:0;color:var(--b2);font-size:.68rem;top:.10rem;}

.alert{background:var(--white);border:1px solid #BFDBFE;border-left:4px solid var(--b1);border-radius:var(--r);padding:1.1rem 1.3rem;margin-top:.9rem;box-shadow:var(--sh-sm);font-family:var(--sans);}
.alert.warn{border-left-color:var(--warn);border-color:var(--warn-brd);}
.alert.info{border-left-color:var(--ok);border-color:var(--ok-brd);}
.alert-h{display:flex;align-items:center;gap:9px;margin-bottom:.5rem;}
.alert-ic{width:30px;height:30px;border-radius:8px;background:var(--b3);display:flex;align-items:center;justify-content:center;font-size:.85rem;flex-shrink:0;}
.alert.warn .alert-ic{background:var(--warn-bg);}
.alert.info .alert-ic{background:var(--ok-bg);}
.alert-title{font-size:.85rem;font-weight:700;color:var(--b1);}
.alert.warn .alert-title{color:var(--warn);}
.alert.info .alert-title{color:var(--ok);}
.alert-body{font-size:.79rem;color:var(--text-3);line-height:1.65;padding-left:39px;}
.alert-body code{background:var(--b3);padding:1px 5px;border-radius:4px;font-family:var(--mono);font-size:.72rem;color:var(--b1);}
.alert-body pre{background:var(--b4);border:1px solid rgba(0,61,165,.18);border-radius:var(--r-sm);padding:7px 11px;font-family:var(--mono);font-size:.72rem;color:var(--b1);margin:.45rem 0 .15rem;}
.sbadge{display:inline-flex;align-items:center;gap:5px;background:var(--ok-bg);border:1px solid var(--ok-brd);border-radius:20px;padding:3px 12px;font-size:.62rem;font-weight:600;color:var(--ok);margin-bottom:.6rem;}
.sbadge .dg{width:5px;height:5px;border-radius:50%;background:var(--ok);}

.stats{display:flex;gap:.75rem;margin-top:.85rem;}
.stat{flex:1;background:var(--white);border:1px solid var(--border);border-radius:var(--r);padding:.85rem .75rem;text-align:center;box-shadow:var(--sh-sm);transition:box-shadow .18s,transform .14s;}
.stat:hover{box-shadow:var(--sh);transform:translateY(-2px);}
.stat .v{font-size:1.2rem;font-weight:800;color:var(--b1);}
.stat .l{font-size:.58rem;font-weight:700;color:var(--text-3);letter-spacing:.9px;text-transform:uppercase;margin-top:3px;}

.streamlit-expanderHeader{background:#FFFBEB!important;border:1.5px solid #FCD34D!important;border-radius:var(--r)!important;font-family:var(--sans)!important;font-size:.78rem!important;font-weight:700!important;color:#92400E!important;box-shadow:0 2px 8px rgba(245,158,11,.18)!important;padding:10px 16px!important;}
.streamlit-expanderHeader:hover{background:#FEF3C7!important;border-color:#F59E0B!important;}
.streamlit-expanderContent{background:#FFFDF5!important;border:1.5px solid #FCD34D!important;border-top:none!important;border-radius:0 0 var(--r) var(--r)!important;padding:4px 0!important;}
.streamlit-expanderHeader svg{color:#B45309!important;fill:#B45309!important;}
.hi{background:var(--white);border:1px solid var(--border);border-left:3px solid var(--yellow);border-radius:var(--r);padding:.72rem 1rem;margin-bottom:.4rem;box-shadow:var(--sh-sm);transition:box-shadow .15s;}
.hi:hover{box-shadow:var(--sh);}
.hi .hp{font-size:.80rem;font-weight:500;color:var(--text);margin-bottom:3px;display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden;}
.hi .hm{font-size:.61rem;color:var(--text-4);}

.stCodeBlock{border:1px solid #252E45!important;border-radius:var(--r)!important;box-shadow:0 4px 16px rgba(0,0,0,.14)!important;}
.stCodeBlock pre{background:#161B2A!important;font-family:var(--mono)!important;font-size:.79rem!important;color:#CDD6F4!important;}
div[data-testid="stCopyButton"] button{background:rgba(137,220,235,.10)!important;border:1px solid rgba(137,220,235,.25)!important;color:#89DCEB!important;border-radius:5px!important;font-size:.65rem!important;}
div[data-testid="stCopyButton"] button:hover{background:#89DCEB!important;color:#161B2A!important;}
.stSpinner>div{border-top-color:var(--b2)!important;}
.pdiv{height:1px;background:var(--border);margin:1.1rem 0;opacity:.5;}

.foot{text-align:center;padding:1rem 0 .5rem;border-top:1px solid var(--border);margin-top:2.5rem;}
.foot p{font-family:var(--sans);font-size:.60rem;color:var(--text-4);letter-spacing:.4px;margin:0;}
.foot p+p{margin-top:.2rem;}
.foot strong{color:var(--text-3);font-weight:600;}

/* Şablon kullan butonları — sarı değil, nötr koyu */
div[data-testid="stVerticalBlock"] .stButton > button[kind="secondary"],
div[data-testid="stHorizontalBlock"] .stButton > button {
  background: #1E293B !important;
  color: #F1F5F9 !important;
  border: none !important;
  font-size: .8rem !important;
  font-weight: 600 !important;
  padding: .35rem .8rem !important;
  border-radius: 6px !important;
  box-shadow: none !important;
  transform: none !important;
}
div[data-testid="stVerticalBlock"] .stButton > button[kind="secondary"]:hover,
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
  background: #334155 !important;
  box-shadow: none !important;
  transform: none !important;
}

/* nav butonları */
div[data-testid="column"]:nth-last-child(-n+2) .stButton>button {
  background: rgba(255,255,255,.12) !important;
  color: #fff !important;
  border: 1px solid rgba(255,255,255,.25) !important;
  border-radius: 6px !important;
  font-size: .72rem !important;
  padding: .3rem .6rem !important;
  margin: 0 !important;
  box-shadow: none !important;
  transform: none !important;
}
div[data-testid="column"]:nth-last-child(-n+2) .stButton>button:hover {
  background: rgba(255,255,255,.22) !important;
  box-shadow: none !important;
  transform: none !important;
}

</style>
""", unsafe_allow_html=True)


# ── session state ─────────────────────────────────────────────────────────────
for k, v in [("history",[]),("qc",0),("tt",0),("lp",""),
              ("logged_in",False),("username",""),("role",""),
              ("user_id",None),("page","main"),
              ("cache_hit",False),("last_res",None),("preview_sql",""),
              ("chat_history",[]),("chat_mode",False),
              ("briefing_shown",False),("auto_go",False),
              ("ac_reset",0),("prompt_reset",0),("followup_reset",0),
              ("explain_result","")]:
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════
#  VERİTABANI — SQLite
# ══════════════════════════════════════════════════════════════════════════
DB_PATH = "turkcell_sql_ai.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    # Kullanıcılar
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    UNIQUE NOT NULL,
            fullname    TEXT    NOT NULL DEFAULT '',
            password_hash TEXT  NOT NULL,
            role        TEXT    NOT NULL DEFAULT 'analyst',
            is_active   INTEGER DEFAULT 1,
            created_at  TEXT    DEFAULT (datetime('now')),
            last_login  TEXT
        )
    """)

    # Şemalar
    c.execute("""
        CREATE TABLE IF NOT EXISTS schemas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            name        TEXT    NOT NULL,
            description TEXT    DEFAULT '',
            content     TEXT    NOT NULL,
            table_count INTEGER DEFAULT 0,
            created_at  TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Sorgu geçmişi (audit log)
    c.execute("""
        CREATE TABLE IF NOT EXISTS query_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            username    TEXT    NOT NULL,
            prompt      TEXT    NOT NULL,
            sql_out     TEXT,
            dialect     TEXT,
            style       TEXT,
            sql_mode    TEXT,
            schema_name TEXT    DEFAULT '',
            tokens      INTEGER DEFAULT 0,
            elapsed_sec REAL    DEFAULT 0,
            risk_level  TEXT    DEFAULT '',
            kvkk_hit    INTEGER DEFAULT 0,
            created_at  TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()

    # Önbellek tablosu
    c.execute("""
        CREATE TABLE IF NOT EXISTS query_cache (
            cache_key   TEXT PRIMARY KEY,
            prompt      TEXT,
            result_json TEXT,
            dialect     TEXT,
            hit_count   INTEGER DEFAULT 1,
            created_at  TEXT DEFAULT (datetime('now'))
        )
    """)

    # Şablon tablosu
    c.execute("""
        CREATE TABLE IF NOT EXISTS templates (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            category    TEXT NOT NULL,
            title       TEXT NOT NULL,
            prompt      TEXT NOT NULL,
            icon        TEXT DEFAULT '📋',
            scope       TEXT DEFAULT 'system',
            user_id     INTEGER DEFAULT NULL,
            team_role   TEXT DEFAULT NULL,
            created_by  TEXT DEFAULT 'system',
            created_at  TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()

    # DB Bağlantıları tablosu
    c.execute("""
        CREATE TABLE IF NOT EXISTS db_connections (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            name        TEXT NOT NULL,
            db_type     TEXT NOT NULL DEFAULT 'postgresql',
            host        TEXT DEFAULT '',
            port        INTEGER DEFAULT 5432,
            database    TEXT DEFAULT '',
            username    TEXT DEFAULT '',
            password    TEXT DEFAULT '',
            is_active   INTEGER DEFAULT 1,
            last_tested TEXT,
            created_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()

    # ── MIGRATION: templates tablosuna yeni sütunlar ekle (varsa atla) ──────
    _existing_cols = [r[1] for r in c.execute("PRAGMA table_info(templates)").fetchall()]
    if 'scope' not in _existing_cols:
        c.execute("ALTER TABLE templates ADD COLUMN scope TEXT DEFAULT 'system'")
    if 'user_id' not in _existing_cols:
        c.execute("ALTER TABLE templates ADD COLUMN user_id INTEGER DEFAULT NULL")
    if 'team_role' not in _existing_cols:
        c.execute("ALTER TABLE templates ADD COLUMN team_role TEXT DEFAULT NULL")
    conn.commit()

    # Admin kullanıcı yoksa oluştur
    existing = c.execute("SELECT id FROM users WHERE username='admin'").fetchone()
    if not existing:
        pw_hash = _hash_pw("admin123")
        c.execute(
            "INSERT INTO users (username, fullname, password_hash, role) VALUES (?,?,?,?)",
            ("admin", "Sistem Yöneticisi", pw_hash, "admin")
        )
        conn.commit()

    conn.close()

def _hash_pw(password: str) -> str:
    if BCRYPT_OK:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashlib.sha256(password.encode()).hexdigest()

def _check_pw(password: str, hashed: str) -> bool:
    if BCRYPT_OK:
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except Exception:
            pass
    return hashlib.sha256(password.encode()).hexdigest() == hashed

def db_login(username: str, password: str):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM users WHERE username=? AND is_active=1", (username,)
    ).fetchone()
    conn.close()
    if row and _check_pw(password, row["password_hash"]):
        conn2 = get_db()
        conn2.execute("UPDATE users SET last_login=datetime('now') WHERE id=?", (row["id"],))
        conn2.commit(); conn2.close()
        return dict(row)
    return None

def db_log_query(user_id, username, prompt, sql_out, dialect, style,
                 sql_mode, schema_name, tokens, elapsed, risk_level="", kvkk_hit=0):
    conn = get_db()
    conn.execute("""
        INSERT INTO query_log
        (user_id,username,prompt,sql_out,dialect,style,sql_mode,
         schema_name,tokens,elapsed_sec,risk_level,kvkk_hit)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (user_id, username, prompt, sql_out, dialect, style, sql_mode,
          schema_name, tokens, elapsed, risk_level, kvkk_hit))
    conn.commit(); conn.close()

def db_get_history(user_id, limit=50):
    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM query_log
        WHERE user_id=?
        ORDER BY created_at DESC LIMIT ?
    """, (user_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def db_get_all_history(limit=200):
    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM query_log
        ORDER BY created_at DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def db_save_schema(user_id, name, description, content, table_count):
    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM schemas WHERE user_id=? AND name=?", (user_id, name)
    ).fetchone()
    if existing:
        conn.execute("""
            UPDATE schemas SET description=?, content=?, table_count=?,
            created_at=datetime('now') WHERE id=?
        """, (description, content, table_count, existing["id"]))
        action = "güncellendi"
    else:
        conn.execute("""
            INSERT INTO schemas (user_id, name, description, content, table_count)
            VALUES (?,?,?,?,?)
        """, (user_id, name, description, content, table_count))
        action = "kaydedildi"
    conn.commit(); conn.close()
    return action

def db_get_schemas(user_id, role):
    conn = get_db()
    if role == "admin":
        rows = conn.execute("""
            SELECT s.*, u.username as owner
            FROM schemas s JOIN users u ON s.user_id=u.id
            ORDER BY s.created_at DESC
        """).fetchall()
    else:
        rows = conn.execute("""
            SELECT s.*, u.username as owner
            FROM schemas s JOIN users u ON s.user_id=u.id
            WHERE s.user_id=?
            ORDER BY s.created_at DESC
        """, (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def db_delete_schema(schema_id, user_id, role):
    conn = get_db()
    if role == "admin":
        conn.execute("DELETE FROM schemas WHERE id=?", (schema_id,))
    else:
        conn.execute("DELETE FROM schemas WHERE id=? AND user_id=?", (schema_id, user_id))
    conn.commit(); conn.close()

def db_get_users():
    conn = get_db()
    rows = conn.execute("SELECT id,username,fullname,role,is_active,created_at,last_login FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def db_add_user(username, fullname, password, role):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username,fullname,password_hash,role) VALUES (?,?,?,?)",
            (username, fullname, _hash_pw(password), role)
        )
        conn.commit()
        conn.close()
        return True, "Kullanıcı oluşturuldu."
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Bu kullanıcı adı zaten var."

def db_toggle_user(user_id, active):
    conn = get_db()
    conn.execute("UPDATE users SET is_active=? WHERE id=?", (active, user_id))
    conn.commit(); conn.close()

def db_change_password(user_id, new_password):
    conn = get_db()
    conn.execute("UPDATE users SET password_hash=? WHERE id=?", (_hash_pw(new_password), user_id))
    conn.commit(); conn.close()

# ── ÖNBELLEK ──────────────────────────────────────────────────────────────
def _cache_key(prompt, dialect, schema_content):
    import hashlib
    raw = f'{prompt.strip()}|{dialect}|{(schema_content or "")[:500]}'
    return hashlib.md5(raw.encode()).hexdigest()

def cache_get(key):
    conn = get_db()
    row = conn.execute("SELECT result_json FROM query_cache WHERE cache_key=?", (key,)).fetchone()
    if row:
        conn.execute("UPDATE query_cache SET hit_count=hit_count+1 WHERE cache_key=?", (key,))
        conn.commit()
    conn.close()
    return json.loads(row['result_json']) if row else None

def cache_set(key, prompt, result, dialect):
    conn = get_db()
    conn.execute("""
        INSERT OR REPLACE INTO query_cache (cache_key,prompt,result_json,dialect)
        VALUES (?,?,?,?)
    """, (key, prompt, json.dumps(result), dialect))
    conn.commit(); conn.close()

# ── ŞABLONLAR ─────────────────────────────────────────────────────────────
def templates_get(user_id=None, role=None):
    """3 katman: system (herkes) + team (aynı rol) + personal (sadece ben)"""
    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM templates
        WHERE scope='system'
           OR (scope='personal' AND user_id=?)
           OR (scope='team'    AND team_role=?)
        ORDER BY scope DESC, category, title
    """, (user_id, role)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def templates_add(category, title, prompt, icon, created_by,
                  scope='system', user_id=None, team_role=None):
    conn = get_db()
    conn.execute("""
        INSERT INTO templates (category,title,prompt,icon,created_by,scope,user_id,team_role)
        VALUES (?,?,?,?,?,?,?,?)
    """, (category, title, prompt, icon, created_by, scope, user_id, team_role))
    conn.commit(); conn.close()

def templates_delete(tid, user_id=None, role=None):
    """Sadece kendi şablonunu silebilir. Admin hepsini silebilir."""
    conn = get_db()
    if role == 'admin':
        conn.execute("DELETE FROM templates WHERE id=?", (tid,))
    else:
        conn.execute("DELETE FROM templates WHERE id=? AND user_id=?", (tid, user_id))
    conn.commit(); conn.close()

def templates_auto_suggest(user_id, limit=5):
    """Kullanıcının en sık sorduğu promptlardan otomatik şablon önerisi üret."""
    conn = get_db()
    # En çok tekrarlanan sorgular — en az 2 kez sorulmuş
    rows = conn.execute("""
        SELECT prompt, COUNT(*) as cnt, schema_name, dialect
        FROM query_log
        WHERE user_id=?
        GROUP BY prompt
        HAVING cnt >= 2
        ORDER BY cnt DESC
        LIMIT ?
    """, (user_id, limit)).fetchall()
    conn.close()
    # Kişisel şablon olarak zaten kaydedilmişleri çıkar
    existing = get_db().execute(
        "SELECT prompt FROM templates WHERE user_id=? AND scope='personal'",
        (user_id,)
    ).fetchall()
    existing_prompts = {r[0] for r in existing}
    return [dict(r) for r in rows if r['prompt'] not in existing_prompts]

# ── DB BAĞLANTI FONKSİYONLARI ───────────────────────────────────────────────
def db_conn_save(user_id, name, db_type, host, port, database, uname, password):
    conn = get_db()
    existing = conn.execute(
        'SELECT id FROM db_connections WHERE user_id=? AND name=?', (user_id, name)
    ).fetchone()
    if existing:
        conn.execute("""
            UPDATE db_connections SET db_type=?,host=?,port=?,database=?,
            username=?,password=? WHERE id=?
        """, (db_type, host, port, database, uname, password, existing['id']))
    else:
        conn.execute("""
            INSERT INTO db_connections (user_id,name,db_type,host,port,database,username,password)
            VALUES (?,?,?,?,?,?,?,?)
        """, (user_id, name, db_type, host, port, database, uname, password))
    conn.commit(); conn.close()

def db_conn_list(user_id, role):
    conn = get_db()
    if role == 'admin':
        rows = conn.execute("""
            SELECT c.*, u.username as owner FROM db_connections c
            JOIN users u ON c.user_id=u.id ORDER BY c.created_at DESC
        """).fetchall()
    else:
        rows = conn.execute("""
            SELECT c.*, u.username as owner FROM db_connections c
            JOIN users u ON c.user_id=u.id WHERE c.user_id=? ORDER BY c.created_at DESC
        """, (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def db_conn_delete(conn_id, user_id, role):
    conn = get_db()
    if role == 'admin':
        conn.execute('DELETE FROM db_connections WHERE id=?', (conn_id,))
    else:
        conn.execute('DELETE FROM db_connections WHERE id=? AND user_id=?', (conn_id, user_id))
    conn.commit(); conn.close()

def db_conn_test(c):
    """Bağlantıyı test et, (ok:bool, msg:str) döner."""
    try:
        if c['db_type'] == 'postgresql':
            import psycopg2
            cn = psycopg2.connect(host=c['host'],port=c['port'],
                database=c['database'],user=c['username'],password=c['password'],
                connect_timeout=5)
            cur = cn.cursor()
            # Şemayı çek
            cur.execute("""
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema='public'
                ORDER BY table_name, ordinal_position
            """)
            rows = cur.fetchall()
            cn.close()
            return True, rows
        elif c['db_type'] == 'mysql':
            import pymysql
            cn = pymysql.connect(host=c['host'],port=int(c['port']),
                db=c['database'],user=c['username'],password=c['password'],
                connect_timeout=5)
            cur = cn.cursor()
            cur.execute('SHOW TABLES')
            rows = cur.fetchall()
            cn.close()
            return True, rows
        elif c['db_type'] == 'sqlite':
            import sqlite3 as _sl
            cn = _sl.connect(c['database'])
            cur = cn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            rows = cur.fetchall()
            cn.close()
            return True, rows
        return False, [('Desteklenmeyen DB tipi',)]
    except Exception as e:
        return False, [(str(e),)]

def schema_from_pg_rows(rows):
    """information_schema satırlarından CREATE TABLE DDL üret."""
    from collections import defaultdict
    tables = defaultdict(list)
    for tbl, col, dtype in rows:
        tables[tbl].append(f'    {col} {dtype}')
    lines = []
    for tbl, cols in tables.items():
        lines.append(f'CREATE TABLE {tbl} (')
        lines.append(',\n'.join(cols))
        lines.append(');\n')
    return '\n'.join(lines)

# ── DASHBOARD FONKSİYONLARI ──────────────────────────────────────────────────
def dash_stats():
    conn = get_db()
    total_q    = conn.execute('SELECT COUNT(*) FROM query_log').fetchone()[0]
    today_q    = conn.execute("SELECT COUNT(*) FROM query_log WHERE created_at>=date('now')").fetchone()[0]
    week_q     = conn.execute("SELECT COUNT(*) FROM query_log WHERE created_at>=date('now','-7 days')").fetchone()[0]
    total_u    = conn.execute('SELECT COUNT(*) FROM users WHERE is_active=1').fetchone()[0]
    kvkk_q     = conn.execute('SELECT COUNT(*) FROM query_log WHERE kvkk_hit=1').fetchone()[0]
    risky_q    = conn.execute("SELECT COUNT(*) FROM query_log WHERE risk_level='RISKY'").fetchone()[0]
    invalid_q  = conn.execute("SELECT COUNT(*) FROM query_log WHERE risk_level='INVALID'").fetchone()[0]
    cache_hits = conn.execute('SELECT SUM(hit_count)-COUNT(*) FROM query_cache').fetchone()[0] or 0
    # Kullanıcı bazlı sorgu sayısı
    by_user = conn.execute("""
        SELECT username, COUNT(*) as cnt FROM query_log
        GROUP BY username ORDER BY cnt DESC LIMIT 10
    """).fetchall()
    by_user = [{'username': r[0], 'cnt': r[1]} for r in by_user]
    # Günlük sorgu (son 7 gün)
    by_day = conn.execute("""
        SELECT date(created_at) as day, COUNT(*) as cnt FROM query_log
        WHERE created_at>=date('now','-7 days')
        GROUP BY day ORDER BY day
    """).fetchall()
    by_day = [{'day': r[0], 'cnt': r[1]} for r in by_day]
    # Risk dağılımı
    by_risk = conn.execute("""
        SELECT risk_level, COUNT(*) as cnt FROM query_log
        WHERE risk_level != '' GROUP BY risk_level
    """).fetchall()
    by_risk = [{'risk_level': r[0], 'cnt': r[1]} for r in by_risk]
    # KVKK tetikleyen sorgular
    kvkk_list = conn.execute("""
        SELECT username, prompt, created_at FROM query_log
        WHERE kvkk_hit=1 ORDER BY created_at DESC LIMIT 20
    """).fetchall()
    kvkk_list = [{'username': r[0], 'prompt': r[1], 'created_at': r[2]} for r in kvkk_list]
    conn.close()
    return {
        'total_q': total_q, 'today_q': today_q, 'week_q': week_q,
        'total_u': total_u, 'kvkk_q': kvkk_q, 'risky_q': risky_q,
        'invalid_q': invalid_q, 'cache_hits': cache_hits,
        'by_user': [dict(r) for r in by_user],
        'by_day':  [dict(r) for r in by_day],
        'by_risk': [dict(r) for r in by_risk],
        'kvkk_list': [dict(r) for r in kvkk_list],
    }

def _seed_templates():
    """Sistem şablonlarını bir kez yükle."""
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM templates").fetchone()[0]
    conn.close()
    if count > 0: return
    defaults = [
        ("📊 CRM",    "En fazla sipariş veren 10 müşteri",
         "Son 3 ayda en fazla sipariş veren 10 müşteriyi sipariş sayısı ve toplam tutarıyla listele", "👥"),
        ("📊 CRM",    "Yeni kayıt — sipariş vermemiş",
         "Geçen ay kaydolan ama henüz sipariş vermemiş müşterileri referans kaynağına göre gruplandır", "🆕"),
        ("💰 Finans", "Gecikmiş faturalar",
         "Faturası 90 günü aşan abonelerin tarife bazında toplam borç tutarını göster", "⚠️"),
        ("💰 Finans", "Tahsilat oranı",
         "Geçen ay tarife bazında toplam fatura tutarı ve tahsilat oranını göster", "📈"),
        ("📡 Telekom","Churn riski yüksek aboneler",
         "Churn riski yüksek olan altın segment aboneleri son 3 aydaki müşteri hizmetleri araması ile birlikte listele", "🚨"),
        ("📡 Telekom","Baz istasyonu arızaları",
         "Son 30 günde en çok arıza bildirimi gelen 5 baz istasyonunu şehir ve teknoloji tipiyle listele", "📡"),
        ("🔍 Denetim","KVKK onaysız aktif aboneler",
         "KVKK onayı olmayan ama aktif olan abonelerin sayısını aktivasyon tarihi aralığına göre göster", "⚖️"),
        ("🔍 Denetim","Segment bazlı gelir dağılımı",
         "Aktif abonelerin segment ve tarife tipine göre dağılımını ve ortalama aylık ücretini göster", "📊"),
    ]
    for cat, title, prompt, icon in defaults:
        templates_add(cat, title, prompt, icon, 'system')

# Rol → izin verilen SQL modları
ROLE_MODES = {
    "viewer":  ["🔒 Read-Only"],
    "analyst": ["🔒 Read-Only", "✏️ Write (DML)"],
    "dba":     ["🔒 Read-Only", "✏️ Write (DML)", "🔧 DDL"],
    "admin":   ["🔒 Read-Only", "✏️ Write (DML)", "🔧 DDL", "⚡ Full (Tamümü)"],
}
ROLE_LABELS = {
    "viewer":  "👁 Viewer",
    "analyst": "📊 Analyst",
    "dba":     "🔧 DBA",
    "admin":   "⚡ Admin",
}

# DB başlat → önce tablolar oluşsun, sonra seed
init_db()
_seed_templates()


# ══════════════════════════════════════════════════════════════════════════
#  GİRİŞ EKRANI
# ══════════════════════════════════════════════════════════════════════════
def render_login():
    st.markdown(
        f'''<div class="hdr"><div class="hdr-left">
        <img class="hdr-logo" src="{LOGO_SRC}" alt="logo">
        <div class="hdr-vline"></div>
        <div><div class="hdr-title">turkcell.sql.ai.com.tr</div>
        <div class="hdr-sub">Natural Language → SQL</div></div>
        </div><div class="hdr-pill">v4.1 · Pipeline</div></div>''',
        unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
        st.markdown(
            '''<div style="background:#fff;border:1px solid #DCE3ED;border-radius:14px;
            padding:2rem 2.2rem;box-shadow:0 8px 30px rgba(0,0,0,.10);">
            <div style="text-align:center;margin-bottom:1.5rem">
            <div style="font-size:2rem">🔐</div>
            <div style="font-size:1.1rem;font-weight:800;color:#003DA5;margin-top:.4rem">Giriş Yap</div>
            <div style="font-size:.72rem;color:#9AA5B4;margin-top:.2rem">TURKCELL SQL AI</div>
            </div>''',
            unsafe_allow_html=True)

        username = st.text_input("Kullanıcı Adı", placeholder="kullanici_adi", key="login_user")
        password = st.text_input("Şifre", type="password", placeholder="••••••••", key="login_pw")

        if st.button("⚡  Giriş Yap", key="login_btn"):
            if username.strip() and password.strip():
                user = db_login(username.strip(), password.strip())
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username  = user["username"]
                    st.session_state.role      = user["role"]
                    st.session_state.user_id   = user["id"]
                    st.session_state.page      = "main"
                    st.rerun()
                else:
                    st.error("❌ Kullanıcı adı veya şifre hatalı.")
            else:
                st.warning("Lütfen kullanıcı adı ve şifre girin.")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(
            '''<div style="text-align:center;margin-top:1rem;font-size:.65rem;color:#9AA5B4">
            © 2026 turkcell.sql.ai.com.tr · L2 DevOps Operations
            </div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  ADMİN PANELİ
# ══════════════════════════════════════════════════════════════════════════
def render_admin():
    st.markdown(
        f'<div class="hdr"><div class="hdr-left">'
        f'<img class="hdr-logo" src="{LOGO_SRC}" alt="logo">'
        f'<div class="hdr-vline"></div>'
        f'<div><div class="hdr-title">turkcell.sql.ai.com.tr</div>'
        f'<div class="hdr-sub">Admin Paneli</div></div>'
        f'</div><div class="hdr-pill">⚡ Admin</div></div>',
        unsafe_allow_html=True)

    # Ana sayfa butonu
    if st.button("◀  Ana Sayfaya Dön", key="admin_back"):
        st.session_state.page = "main"
        st.rerun()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["👥 Kullanıcılar", "📜 Audit Log", "🗄️ Tüm Şemalar", "📊 Dashboard", "🔌 DB Bağlantıları", "🔗 REST API"])

    # ── KULLANICILAR TAB ─────────────────────────────────────────────────────
    with tab1:
        # Kullanıcı listesi
        st.markdown(
            "<p style='font-size:.65rem;font-weight:700;color:#003DA5;"
            "letter-spacing:1.5px;text-transform:uppercase;margin:.8rem 0 .5rem'>👥 Kullanıcı Listesi</p>",
            unsafe_allow_html=True)

        users = db_get_users()
        for u in users:
            active_badge = "🟢" if u["is_active"] else "🔴"
            role_label   = ROLE_LABELS.get(u["role"], u["role"])
            last = u["last_login"][:16] if u["last_login"] else "—"
            role_colors  = {"viewer":"#6B7A90","analyst":"#003DA5","dba":"#7C3AED","admin":"#B45309"}
            rc = role_colors.get(u["role"],"#374151")

            st.markdown(
                f"<div style='background:#fff;border:1px solid #DCE3ED;border-radius:10px;"
                f"padding:.7rem 1rem;margin-bottom:.4rem;"
                f"display:flex;align-items:center;gap:.8rem'>"
                f"<span style='font-size:1.1rem'>{active_badge}</span>"
                f"<div style='flex:1'>"
                f"<span style='font-weight:700;color:#0F1623;font-size:.9rem'>{u['username']}</span>"
                f"<span style='color:#6B7A90;font-size:.82rem'> · {u['fullname']}</span><br>"
                f"<span style='font-size:.68rem;color:#9AA5B4'>Son giriş: {last}</span>"
                f"</div>"
                f"<span style='background:{rc}18;color:{rc};border:1px solid {rc}44;"
                f"border-radius:20px;padding:2px 10px;font-size:.68rem;font-weight:700'>"
                f"{role_label}</span>"
                f"</div>",
                unsafe_allow_html=True)

            if u["username"] != "admin":
                _ca, _cb, _cc = st.columns([3, 1.2, 1.2])
                with _cb:
                    new_state = 0 if u["is_active"] else 1
                    lbl = "🔒 Pasif" if u["is_active"] else "✅ Aktif"
                    if st.button(lbl, key=f"tog_{u['id']}", use_container_width=True):
                        db_toggle_user(u["id"], new_state); st.rerun()
                with _cc:
                    if st.button("🗑 Sil", key=f"del_{u['id']}", use_container_width=True):
                        conn = get_db()
                        conn.execute("DELETE FROM users WHERE id=?", (u["id"],))
                        conn.commit(); conn.close(); st.rerun()

            # Şifre sıfırlama (admin)
            if u["username"] != "admin":
                with st.expander(f"🔑 {u['username']} şifresini sıfırla", expanded=False):
                    _rp_col1, _rp_col2 = st.columns([2,1])
                    with _rp_col1:
                        _reset_pw = st.text_input("Yeni şifre", key=f"rpw_{u['id']}", type="password")
                    with _rp_col2:
                        st.markdown("<div style='margin-top:1.7rem'></div>", unsafe_allow_html=True)
                        if st.button("Güncelle", key=f"rset_{u['id']}"):
                            if _reset_pw and len(_reset_pw) >= 6:
                                db_change_password(u["id"], _reset_pw)
                                st.success(f"✅ {u['username']} şifresi güncellendi.")
                            else:
                                st.error("En az 6 karakter girin.")

        # Yeni kullanıcı
        st.markdown(
            "<p style='font-size:.65rem;font-weight:700;color:#003DA5;"
            "letter-spacing:1.5px;text-transform:uppercase;margin:1.2rem 0 .5rem'>➕ Yeni Kullanıcı Ekle</p>",
            unsafe_allow_html=True)

        st.markdown(
            "<div style='background:#F0F4FF;border:1px solid #BFDBFE;border-radius:12px;padding:1rem 1.2rem'>",
            unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            new_user = st.text_input("Kullanıcı Adı", key="nu_user",
                placeholder="ornek_kullanici")
            new_full = st.text_input("Ad Soyad", key="nu_full",
                placeholder="Adı Soyadı")
        with c2:
            new_pw   = st.text_input("Şifre", type="password", key="nu_pw",
                placeholder="min 6 karakter")
            new_role = st.selectbox("Rol", ["viewer","analyst","dba","admin"],
                key="nu_role",
                format_func=lambda r: ROLE_LABELS.get(r, r))
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("➕ Kullanıcı Oluştur", key="create_user"):
            if new_user.strip() and new_pw.strip():
                ok, msg = db_add_user(new_user.strip(), new_full.strip(), new_pw, new_role)
                if ok: st.success(f"✅ {msg}")
                else:  st.error(f"❌ {msg}")
                st.rerun()
            else:
                st.warning("Kullanıcı adı ve şifre zorunlu.")

    # ── AUDİT LOG TAB ────────────────────────────────────────────────────────
    with tab2:
        st.markdown(
            "<p style='font-size:.65rem;font-weight:700;color:#003DA5;"
            "letter-spacing:1.5px;text-transform:uppercase;margin:.8rem 0 .5rem'>📜 Sorgu Audit Log</p>",
            unsafe_allow_html=True)
        logs = db_get_all_history(200)
        if not logs:
            st.info("Henüz sorgu kaydı yok.")
        else:
            st.caption(f"Toplam {len(logs)} kayıt")
            for entry in logs:
                risk_col  = {"SAFE":"#0D7F4D","RISKY":"#B45309","INVALID":"#B91C1C"}.get(
                    entry.get("risk_level",""), "#6B7A90")
                risk_bg   = {"SAFE":"#EDFAF3","RISKY":"#FFFBEB","INVALID":"#FEF2F2"}.get(
                    entry.get("risk_level",""), "#F5F7FA")
                risk_lbl  = entry.get("risk_level","—") or "—"
                kvkk_flag = "🔏 KVKK" if entry.get("kvkk_hit") else ""
                st.markdown(
                    f"<div style='background:#fff;border:1px solid #DCE3ED;"
                    f"border-left:3px solid {risk_col};border-radius:10px;"
                    f"padding:.6rem 1rem;margin-bottom:.35rem'>"
                    f"<div style='font-size:.82rem;font-weight:500;color:#0F1623;"
                    f"margin-bottom:.2rem;white-space:nowrap;overflow:hidden;"
                    f"text-overflow:ellipsis'>{entry['prompt']}</div>"
                    f"<div style='display:flex;gap:.5rem;flex-wrap:wrap;align-items:center'>"
                    f"<span style='font-size:.65rem;color:#6B7A90'>{entry['created_at'][:16]}</span>"
                    f"<span style='font-size:.65rem;font-weight:600;color:#003DA5'>👤 {entry['username']}</span>"
                    f"<span style='font-size:.65rem;color:#6B7A90'>{entry.get('dialect','')} · {entry.get('sql_mode','')}</span>"
                    f"<span style='background:{risk_bg};color:{risk_col};border-radius:10px;"
                    f"padding:1px 8px;font-size:.62rem;font-weight:700'>{risk_lbl}</span>"
                    f"{'<span style=\"font-size:.62rem;color:#7C3AED\">'+kvkk_flag+'</span>' if kvkk_flag else ''}"
                    f"<span style='font-size:.62rem;color:#9AA5B4'>{entry.get('tokens',0)} tok"
                    f" · {entry.get('elapsed_sec',0):.1f}s</span>"
                    f"</div></div>",
                    unsafe_allow_html=True)

    # ── ŞEMALAR TAB ──────────────────────────────────────────────────────────
    with tab3:
        st.markdown(
            "<p style='font-size:.65rem;font-weight:700;color:#003DA5;"
            "letter-spacing:1.5px;text-transform:uppercase;margin:.8rem 0 .5rem'>🗄️ Kayıtlı Şemalar</p>",
            unsafe_allow_html=True)
        schemas = db_get_schemas(None, "admin")
        if not schemas:
            st.info("Henüz kayıtlı şema yok.")
        else:
            for sch in schemas:
                _sa, _sb = st.columns([5, 1])
                with _sa:
                    st.markdown(
                        f"<div style='background:#fff;border:1px solid #DCE3ED;"
                        f"border-radius:10px;padding:.6rem 1rem'>"
                        f"<span style='font-weight:700;color:#003DA5'>{sch['name']}</span>"
                        f"<span style='color:#6B7A90;font-size:.82rem'> · 👤 {sch['owner']}"
                        f" · {sch['table_count']} tablo</span>"
                        f"{'<br><span style=\"font-size:.75rem;color:#9AA5B4\">'+sch['description']+'</span>' if sch.get('description') else ''}"
                        f"</div>",
                        unsafe_allow_html=True)
                with _sb:
                    if st.button("🗑 Sil", key=f"del_sch_{sch['id']}", use_container_width=True):
                        db_delete_schema(sch["id"], None, "admin"); st.rerun()

    # ── DASHBOARD TAB ────────────────────────────────────────────────────────
    with tab4:
        st.markdown(
            "<p style='font-size:.65rem;font-weight:700;color:#003DA5;"
            "letter-spacing:1.5px;text-transform:uppercase;margin:.8rem 0 .5rem'>📊 Kullanım Dashboard</p>",
            unsafe_allow_html=True)
        ds = dash_stats()

        # ── Özet kartlar ─────────────────────────────────────────────────────
        _dc1,_dc2,_dc3,_dc4,_dc5,_dc6 = st.columns(6)
        for _col, _val, _lbl, _color in [
            (_dc1, ds['total_q'],  'Toplam Sorgu',  '#003DA5'),
            (_dc2, ds['today_q'],  'Bugün',         '#0D7F4D'),
            (_dc3, ds['week_q'],   'Bu Hafta',      '#7C3AED'),
            (_dc4, ds['kvkk_q'],   'KVKK Uyarısı', '#B91C1C'),
            (_dc5, ds['risky_q'],  'Riskli Sorgu',  '#B45309'),
            (_dc6, ds['cache_hits'],'Önbellek Hit', '#0891B2'),
        ]:
            with _col:
                st.markdown(
                    f"<div style='background:#fff;border:1px solid #DCE3ED;border-radius:10px;"
                    f"padding:.7rem .8rem;text-align:center;border-top:3px solid {_color}'>"
                    f"<div style='font-size:1.6rem;font-weight:800;color:{_color}'>{_val}</div>"
                    f"<div style='font-size:.66rem;color:#9AA5B4;margin-top:.2rem'>{_lbl}</div>"
                    f"</div>", unsafe_allow_html=True)

        st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)

        # ── Kullanıcı bazlı sorgu + Risk dağılımı ────────────────────────────
        _dl, _dr = st.columns(2)
        with _dl:
            st.markdown(
                "<p style='font-size:.65rem;font-weight:700;color:#003DA5;"
                "letter-spacing:1.2px;text-transform:uppercase;margin:.5rem 0'>👤 Kullanıcı Bazlı Sorgular</p>",
                unsafe_allow_html=True)
            for _u in ds['by_user']:
                _cnt = _u.get('cnt', _u.get('COUNT(*)', 0))
                _pct = round(_cnt / ds['total_q'] * 100) if ds['total_q'] else 0
                st.markdown(
                    f"<div style='display:flex;align-items:center;gap:.6rem;margin-bottom:.35rem'>"
                    f"<span style='font-size:.8rem;font-weight:600;color:#0F1623;min-width:90px'>"
                    f"{_u.get('username','?')}</span>"
                    f"<div style='flex:1;height:8px;background:#F1F5F9;border-radius:99px'>"
                    f"<div style='width:{_pct}%;height:100%;background:#003DA5;border-radius:99px'></div>"
                    f"</div>"
                    f"<span style='font-size:.75rem;color:#6B7A90;min-width:32px;text-align:right'>"
                    f"{_cnt}</span></div>",
                    unsafe_allow_html=True)

        with _dr:
            st.markdown(
                "<p style='font-size:.65rem;font-weight:700;color:#003DA5;"
                "letter-spacing:1.2px;text-transform:uppercase;margin:.5rem 0'>🛡️ Risk Dağılımı</p>",
                unsafe_allow_html=True)
            _risk_colors = {'SAFE':'#0D7F4D','RISKY':'#B45309','INVALID':'#B91C1C'}
            _total_risk  = sum(r['cnt'] for r in ds['by_risk']) or 1
            for _r in ds['by_risk']:
                _rcnt = _r.get('cnt', _r.get('COUNT(*)', 0))
                _rc  = _risk_colors.get(_r.get('risk_level',''),'#9AA5B4')
                _pct = round(_rcnt / _total_risk * 100)
                st.markdown(
                    f"<div style='display:flex;align-items:center;gap:.6rem;margin-bottom:.5rem'>"
                    f"<span style='background:{_rc}18;color:{_rc};border:1px solid {_rc}44;"
                    f"border-radius:20px;padding:1px 10px;font-size:.65rem;font-weight:700;"
                    f"min-width:72px;text-align:center'>{_r['risk_level']}</span>"
                    f"<div style='flex:1;height:8px;background:#F1F5F9;border-radius:99px'>"
                    f"<div style='width:{_pct}%;height:100%;background:{_rc};border-radius:99px'></div>"
                    f"</div>"
                    f"<span style='font-size:.75rem;color:#6B7A90;min-width:36px;text-align:right'>"
                    f"{_rcnt} ({_pct}%)</span></div>",
                    unsafe_allow_html=True)

        st.markdown('<div style="height:.6rem"></div>', unsafe_allow_html=True)

        # ── KVKK Uyarı Listesi ───────────────────────────────────────────────
        if ds['kvkk_list']:
            st.markdown(
                "<p style='font-size:.65rem;font-weight:700;color:#B91C1C;"
                "letter-spacing:1.2px;text-transform:uppercase;margin:.5rem 0'>🔏 Son KVKK Uyarıları</p>",
                unsafe_allow_html=True)
            for _kv in ds['kvkk_list']:
                st.markdown(
                    f"<div style='background:#FEF2F2;border-left:3px solid #B91C1C;"
                    f"border-radius:8px;padding:.5rem .9rem;margin-bottom:.3rem'>"
                    f"<span style='font-size:.8rem;font-weight:500;color:#0F1623'>{_kv.get('prompt','')}</span>"
                    f"<span style='font-size:.68rem;color:#9AA5B4;margin-left:.6rem'>"
                    f"👤 {_kv.get('username','?')} · {str(_kv.get('created_at',''))[:16]}</span></div>",
                    unsafe_allow_html=True)

        # ── Günlük trend (son 7 gün) ─────────────────────────────────────────
        if ds['by_day']:
            st.markdown(
                "<p style='font-size:.65rem;font-weight:700;color:#003DA5;"
                "letter-spacing:1.2px;text-transform:uppercase;margin:.5rem 0'>📅 Son 7 Gün Sorgu Trendi</p>",
                unsafe_allow_html=True)
            _max_day = max(d.get('cnt', d.get('COUNT(*)',0)) for d in ds['by_day']) or 1
            _bar_html = '<div style="display:flex;align-items:flex-end;gap:6px;height:80px">'
            for _d in ds['by_day']:
                _dcnt = _d.get('cnt', _d.get('COUNT(*)',0))
                _h = round(_dcnt / _max_day * 72)
                _bar_html += (
                    f"<div style='display:flex;flex-direction:column;align-items:center;flex:1'>"
                    f"<span style='font-size:.6rem;color:#6B7A90;margin-bottom:2px'>{_dcnt}</span>"
                    f"<div style='width:100%;height:{_h}px;background:#003DA5;"
                    f"border-radius:4px 4px 0 0'></div>"
                    f"<span style='font-size:.58rem;color:#9AA5B4;margin-top:2px'>"
                    f"{str(_d.get('day',''))[5:]}</span></div>"
                )
            _bar_html += '</div>'
            st.markdown(_bar_html, unsafe_allow_html=True)

    # ── DB BAĞLANTILARI TAB ──────────────────────────────────────────────────
    with tab5:
        st.markdown(
            "<p style='font-size:.65rem;font-weight:700;color:#003DA5;"
            "letter-spacing:1.5px;text-transform:uppercase;margin:.8rem 0 .5rem'>🔌 Veritabanı Bağlantıları</p>",
            unsafe_allow_html=True)

        # Mevcut bağlantılar
        _conns = db_conn_list(st.session_state.user_id, st.session_state.role)
        if not _conns:
            st.info('Henüz bağlantı tanımlanmamış. Aşağıdan ekleyin.')
        for _c in _conns:
            _cca, _ccb, _ccc = st.columns([4, 1.2, 1.2])
            with _cca:
                st.markdown(
                    f"<div style='background:#fff;border:1px solid #DCE3ED;"
                    f"border-radius:10px;padding:.55rem 1rem'>"
                    f"<span style='font-weight:700;color:#003DA5'>{_c['name']}</span>"
                    f"<span style='color:#6B7A90;font-size:.8rem'> · {_c['db_type'].upper()}"
                    f" · {_c['host']}:{_c['port']}/{_c['database']}</span>"
                    f"<span style='font-size:.7rem;color:#9AA5B4'> · 👤 {_c.get('owner','')}</span>"
                    f"</div>", unsafe_allow_html=True)
            with _ccb:
                if st.button('🔗 Test Et', key=f'test_{_c["id"]}', use_container_width=True):
                    _ok, _rows = db_conn_test(_c)
                    if _ok:
                        # Şemayı otomatik oluştur ve kaydet
                        if isinstance(_rows[0], tuple) and len(_rows[0]) == 3:
                            _schema_str = schema_from_pg_rows(_rows)
                            _tbl_count = len(set(r[0] for r in _rows))
                            db_save_schema(
                                st.session_state.user_id,
                                f"{_c['name']}_auto",
                                f"{_c['name']} — otomatik çekilen şema",
                                _schema_str, _tbl_count
                            )
                            st.success(f'✅ Bağlantı başarılı! {_tbl_count} tablo bulundu. Şema otomatik kaydedildi.')
                        else:
                            st.success(f'✅ Bağlantı başarılı! {len(_rows)} tablo.')
                        # Son test zamanını kaydet
                        _cn2 = get_db()
                        _cn2.execute("UPDATE db_connections SET last_tested=datetime('now') WHERE id=?", (_c['id'],))
                        _cn2.commit(); _cn2.close()
                        st.rerun()
                    else:
                        st.error(f'❌ {_rows[0][0] if _rows else "Bağlanamadı"}')
            with _ccc:
                if st.button('🗑 Sil', key=f'del_conn_{_c["id"]}', use_container_width=True):
                    db_conn_delete(_c['id'], st.session_state.user_id, st.session_state.role)
                    st.rerun()

        # Yeni bağlantı formu
        st.markdown(
            "<p style='font-size:.65rem;font-weight:700;color:#003DA5;"
            "letter-spacing:1.5px;text-transform:uppercase;margin:1.2rem 0 .5rem'>➕ Yeni Bağlantı Ekle</p>",
            unsafe_allow_html=True)
        st.markdown(
            "<div style='background:#F0F4FF;border:1px solid #BFDBFE;border-radius:12px;padding:1rem 1.2rem'>",
            unsafe_allow_html=True)
        _nc1, _nc2, _nc3 = st.columns(3)
        with _nc1:
            _cn_name = st.text_input('Bağlantı Adı', key='cn_name', placeholder='prod_crm')
            _cn_type = st.selectbox('DB Tipi', ['postgresql','mysql','sqlite'], key='cn_type')
        with _nc2:
            _cn_host = st.text_input('Host', key='cn_host', placeholder='localhost')
            _cn_port = st.number_input('Port', key='cn_port', value=5432, min_value=1, max_value=65535)
        with _nc3:
            _cn_db   = st.text_input('Veritabanı', key='cn_db', placeholder='mydb')
            _cn_user = st.text_input('Kullanıcı', key='cn_user')
        _cn_pw = st.text_input('Şifre', type='password', key='cn_pw')
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button('💾 Bağlantıyı Kaydet', key='save_conn'):
            if _cn_name and _cn_host and _cn_db:
                db_conn_save(st.session_state.user_id, _cn_name, _cn_type,
                             _cn_host, int(_cn_port), _cn_db, _cn_user, _cn_pw)
                st.success(f'✅ "{_cn_name}" bağlantısı kaydedildi. Test Et butonuyla şemayı otomatik çek.')
                st.rerun()
            else:
                st.warning('Bağlantı adı, host ve veritabanı zorunlu.')


    # ── REST API TAB ────────────────────────────────────────────────────────
    with tab6:
        _lbl = "<p style='font-size:.65rem;font-weight:700;color:#003DA5;"\
            "letter-spacing:1.5px;text-transform:uppercase;margin:.8rem 0 .5rem'"\
            ">🔗 REST API Entegrasyonu</p>"
        st.markdown(_lbl, unsafe_allow_html=True)

        _api_token = st.secrets.get('API_TOKEN', '')
        _base = st.secrets.get('API_BASE_URL', 'https://turkcell.sql.ai.com.tr/api')
        _tok  = _api_token if _api_token else 'YOUR-TOKEN-HERE'
        if not _api_token:
            st.markdown(
                "<div style='background:#FFFBEB;border:1px solid #FDE68A;"
                "border-left:3px solid #D97706;border-radius:8px;"
                "padding:.55rem 1rem;font-size:.75rem;color:#92400E'>"
                "⚠️ API_TOKEN tanımlı değil. Aşağıdaki curl örnekleri placeholder ile gösteriliyor."
                "<br><code>secrets.toml</code> dosyasına "
                "<code>API_TOKEN = \"sk-...\"</code> ekleyin."
                "</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='background:#EDFAF3;border:1px solid #A3DFBE;border-radius:8px;"
                "padding:.55rem 1rem;font-size:.75rem;color:#0D7F4D;font-weight:600'>"
                "✅ API Token aktif — Endpointler kullanıma hazır</div>",
                unsafe_allow_html=True)

        st.markdown("<p style='font-size:.65rem;font-weight:700;color:#003DA5;"
            "letter-spacing:1.2px;text-transform:uppercase;margin:.8rem 0 .4rem'>"
            "Endpoint Listesi</p>", unsafe_allow_html=True)

        _ep_list = [
            ('POST','/generate','SQL üret'),
            ('GET', '/history', 'Geçmiş listele'),
            ('GET', '/stats',   'İstatistik al'),
            ('POST','/validate','SQL kontrol et'),
        ]
        _curl_map = {
            '/generate': ('curl -X POST {b}/generate'  + chr(10)
                         + '  -H "Authorization: Bearer {t}"' + chr(10)
                         + '  -H "Content-Type: application/json"' + chr(10)
                         + '  -d \'{"prompt":"Aktif aboneler","dialect":"PostgreSQL"}\''),
            '/history':  ('curl -X GET {b}/history?limit=20' + chr(10)
                         + '  -H "Authorization: Bearer {t}"'),
            '/stats':    ('curl -X GET {b}/stats' + chr(10)
                         + '  -H "Authorization: Bearer {t}"'),
            '/validate': ('curl -X POST {b}/validate' + chr(10)
                         + '  -H "Authorization: Bearer {t}"' + chr(10)
                         + '  -H "Content-Type: application/json"' + chr(10)
                         + '  -d \'{"sql":"SELECT * FROM subscribers","sql_mode":"Read-Only"}\''),
        }
        for _m, _p, _d in _ep_list:
            _mc = '#0D7F4D' if _m == 'GET' else '#003DA5'
            _mb = '#EDFAF3' if _m == 'GET' else '#EBF3FF'
            with st.expander(_m + ' ' + _p + ' — ' + _d, expanded=False):
                st.markdown(
                    "<span style='background:" + _mb + ";color:" + _mc + ";"
                    "border-radius:4px;padding:2px 8px;font-size:.72rem;font-weight:700'>"
                    + _m + "</span> <code style='font-size:.8rem'>" + _base + _p + "</code>",
                    unsafe_allow_html=True)
                _curl_text = _curl_map.get(_p, "# Bu endpoint için örnek yok")
                # Token ve base url'yi string birleştirme ile yerleştir
                _curl_text = _curl_text.replace("{b}", _base).replace("{t}", _tok)
                st.code(_curl_text, language="bash")

        st.markdown("<p style='font-size:.65rem;font-weight:700;color:#003DA5;"
            "letter-spacing:1.2px;text-transform:uppercase;margin:.8rem 0 .4rem'>"
            "Örnek Yanıt</p>", unsafe_allow_html=True)
        _sample = '{"sql":"SELECT...","review":{"status":"SAFE"},"tokens":312,"cached":false}'
        st.code(_sample, language='json')

        st.markdown(
            "<div style='background:#F0F4FF;border:1px solid #BFDBFE;border-radius:10px;"
            "padding:.8rem 1.1rem;font-size:.78rem;color:#374151;line-height:1.8'>"
            "<b>Slack:</b> /sql komutu → POST /generate → SQL kanala<br>"
            "<b>Teams:</b> Power Automate → HTTP /generate → Adaptive Card<br>"
            "<b>PG Advisor:</b> /generate → optimize pipeline</div>",
            unsafe_allow_html=True)


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

def dl(sql):
    enc = b64lib.b64encode(sql.encode()).decode()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return (f'<div class="dl-wrap"><a href="data:file/sql;base64,{enc}" '
            f'download="query_{ts}.sql">📥 Download SQL</a></div>')

def chk(sql, sql_mode="\U0001f512 Read-Only"):
    if not sql or sql.upper().startswith("ERROR"):
        return False, sql.replace("ERROR:", "").strip() if sql else "Model yan\u0131t vermedi."
    if len(sql) < 10:
        return False, "Model beklenmedik k\u0131sa yan\u0131t d\u00f6nd\u00fcrdi."

    ddl_re  = re.compile(r"^\s*(CREATE|ALTER|DROP|TRUNCATE|GRANT|REVOKE)\b", re.I)
    dml_re  = re.compile(r"^\s*(INSERT|UPDATE|DELETE|MERGE)\b", re.I)
    any_re  = re.compile(r"^\s*(INSERT|UPDATE|DELETE|MERGE|CREATE|ALTER|DROP|TRUNCATE|GRANT|REVOKE)\b", re.I)
    upd_del = re.compile(r"\b(UPDATE|DELETE)\b", re.I)

    if sql_mode == "\U0001f512 Read-Only":
        if any_re.search(sql):
            return False, "Read-Only modda yaln\u0131zca SELECT/WITH/CREATE VIEW \u00fcretilebilir. SQL Modunu de\u011fi\u015ftirin."

    elif sql_mode == "\u270f\ufe0f Write (DML)":
        if ddl_re.search(sql):
            return False, "Write modda CREATE/ALTER/DROP izinsiz. DDL modu se\u00e7in."
        if upd_del.search(sql) and not re.search(r"\bWHERE\b", sql, re.I):
            return False, "G\u00fcvenlik: WHERE ko\u015fulsuz UPDATE/DELETE t\u00fcm tabloyu etkiler \u2014 reddedildi."

    elif sql_mode == "\U0001f527 DDL":
        if dml_re.search(sql):
            return False, "DDL modda INSERT/UPDATE/DELETE izinsiz. Write modu se\u00e7in."

    else:  # Full
        if upd_del.search(sql) and not re.search(r"\bWHERE\b", sql, re.I):
            return False, "G\u00fcvenlik: WHERE ko\u015fulsuz UPDATE/DELETE t\u00fcm tabloyu etkiler \u2014 reddedildi."

    return True, ""
def mk_alert(icon, title, body, v=""):
    return (f'<div class="alert {v}"><div class="alert-h">'
            f'<div class="alert-ic">{icon}</div>'
            f'<div class="alert-title">{title}</div></div>'
            f'<div class="alert-body">{body}</div></div>')

def clipboard_js(sql_escaped):
    return f"""<button class="clip-btn" id="clipbtn"
  onclick="navigator.clipboard.writeText(document.getElementById('sqlraw').textContent)
    .then(()=>{{var b=document.getElementById('clipbtn');b.textContent='✓ Kopyalandı';
    b.classList.add('copied');setTimeout(()=>{{b.textContent='📋 Kopyala';
    b.classList.remove('copied');}},1800);}})">📋 Kopyala</button>
<pre id="sqlraw" style="display:none">{sql_escaped}</pre>"""

def render_risk_score(sql: str) -> None:
    s = sql.upper()

    # ── KATMAN 1: SQL GÜVENLİK ───────────────────────────────────────────
    INVALID_RULES = [
        (re.compile(r'\b(DELETE|UPDATE|INSERT|DROP|TRUNCATE|ALTER|GRANT|REVOKE)\b'),
         "Yazma/yıkıcı operasyon tespit edildi",
         "Bu SQL yıkıcı bir komut içeriyor. Read-Only modda bu tür sorgulara izin verilmez."),
    ]
    RISKY_RULES = [
        (re.compile(r'\bSELECT\s+\*'),
         "SELECT * kullanımı",
         "Tüm sütunlar çekiliyor. Gereksiz veri transferi yaratır, performansı düşürür ve veri sızıntısı riskini artırır. Yalnızca ihtiyaç duyulan sütunları listeleyin."),
        # Akıllı WHERE kontrolü: WHERE/HAVING/JOIN-ON/LIMIT/GROUP BY varsa filtreli kabul et
        # CTE içindeki JOIN'ler ayrı sayılır - sadece tek SELECT'te 3+ JOIN sorun
        # WITH yapısı her CTE'yi izole eder, JOIN'ler dağıtık olur
        (re.compile(r'\bLIKE\s+[\'"]%'),
         "Önek joker (%) kullanımı",
         "LIKE '%deger' şeklindeki sorgular indeksi devre dışı bırakır. Tam tablo taramasına neden olur."),
        (re.compile(r'\bNOT\s+IN\b'),
         "NOT IN operatörü",
         "Büyük alt sorgularda NOT IN ciddi performans kaybına yol açar. NOT EXISTS veya LEFT JOIN ile değiştirilmesi önerilir."),
        # Subquery tespit (parantez içinde SELECT) — bu kontrol akıllı blokta yapılır
        (re.compile(r'\bUPDATE\b(?!.*\bWHERE\b)', re.S),
         "WHERE'siz UPDATE",
         "WHERE koşulu olmayan UPDATE tüm satırları günceller. Bu geri alınamaz bir veri değişikliğidir."),
        (re.compile(r'\bDELETE\b(?!.*\bWHERE\b)', re.S),
         "WHERE'siz DELETE",
         "WHERE koşulu olmayan DELETE tüm tabloyu siler. Bu işlem geri alınamaz."),
        (re.compile(r'\bTRUNCATE\b'),
         "TRUNCATE komutu",
         "TRUNCATE tablo içeriğini tamamen ve geri alınamaz biçimde siler. Transaction içinde kullanılmalıdır."),
        (re.compile(r'\bDROP\s+TABLE\b'),
         "DROP TABLE komutu",
         "Tablo tamamen silinir. IF EXISTS guard eklenmeli ve işlem öncesi yedek alınmalıdır."),
    ]

    sql_invalids, sql_risks = [], []
    for pat, title, detail in INVALID_RULES:
        if pat.search(s):
            sql_invalids.append((title, detail))
    if not sql_invalids:
        for pat, title, detail in RISKY_RULES:
            if pat.search(s):
                sql_risks.append((title, detail))

        # ── AKILLI JOIN KONTROLÜ ──────────────────────────────────────────
        # CTE varsa her CTE içindeki JOIN'leri ayrı sayalım
        # Eşik: Tek blokta 4+ JOIN varsa uyar (3 JOIN normal birleştirme)
        _has_cte = bool(re.search(r'\bWITH\b', s))
        if _has_cte:
            _select_blocks = re.split(r'\bSELECT\b', s)
            _max_joins_per_block = max(
                len(re.findall(r'\bJOIN\b', block)) for block in _select_blocks
            ) if _select_blocks else 0
            if _max_joins_per_block >= 4:
                sql_risks.append((
                    "4+ JOIN tek blokta",
                    "Tek bir SELECT bloğunda 4+ JOIN var. CTE ile böl veya filtre ekle."
                ))
        else:
            _total_joins = len(re.findall(r'\bJOIN\b', s))
            if _total_joins >= 4:
                sql_risks.append((
                    "4+ JOIN tespit edildi",
                    "Çok sayıda JOIN sorgunun karmaşıklığını artırır. CTE kullanmayı düşünün."
                ))

        # ── AKILLI SUBQUERY KONTROLÜ ──────────────────────────────────────
        # Parantez içinde SELECT varsa subquery — CTE olsa bile uyarı ver
        # CTE tanımı dışında: WHERE col = (SELECT ...) gibi
        # Strateji: WITH bloğunu çıkar, geri kalanda paranthesized SELECT ara
        _sql_no_with = re.sub(r'\bWITH\b.*?\)\s*(?=SELECT)', '', s, count=1, flags=re.S | re.I)
        if re.search(r'\(\s*SELECT\b', _sql_no_with):
            sql_risks.append((
                "İç içe SELECT (subquery)",
                "Subquery tespit edildi. Performans için CTE (WITH ...) yapısına çevirmeyi düşünün."
            ))

        # ── AKILLI FİLTRE KONTROLÜ ──────────────────────────────────────
        # WHERE/HAVING/LIMIT/GROUP BY varsa veya JOIN ON koşulu varsa filtreli sayılır
        has_where  = bool(re.search(r'\bWHERE\b', s))
        has_having = bool(re.search(r'\bHAVING\b', s))
        has_limit  = bool(re.search(r'\bLIMIT\b', s))
        has_join_on= bool(re.search(r'\bJOIN\b.*\bON\b', s, re.S))
        has_group  = bool(re.search(r'\bGROUP\s+BY\b', s))
        has_agg    = bool(re.search(r'\b(COUNT|SUM|AVG|MAX|MIN)\s*\(', s))

        # Sadece SELECT * FROM table; gibi tamamen filtresiz sorgularda uyar
        is_pure_unfiltered = (
            not has_where and not has_having and not has_limit
            and not has_join_on and not has_group and not has_agg
            and 'FROM' in s
        )
        if is_pure_unfiltered:
            sql_risks.append((
                "Filtreleme eksik",
                "Sorgu hiçbir WHERE / GROUP BY / LIMIT içermiyor. Tüm tablo taranacak."
            ))

    # Akıllı kontrol sayacı eklenince total_sql değişir
    smart_filter_added = 1

    total_sql   = len(RISKY_RULES) + len(INVALID_RULES) + smart_filter_added
    issues_sql  = len(sql_invalids) + len(sql_risks)
    ok_sql      = total_sql - issues_sql
    pct_ok_sql  = round(ok_sql  / total_sql * 100)
    pct_bad_sql = 100 - pct_ok_sql

    if sql_invalids:
        sql_status = "GEÇERSİZ"; sql_icon = "✗"
        sql_badge_bg = "#FEF2F2"; sql_badge_fg = "#B91C1C"
        sql_bar_ok = "#EF4444";   sql_bar_bad = "#FCA5A5"
    elif sql_risks:
        sql_status = "RİSKLİ";   sql_icon = "⚠"
        sql_badge_bg = "#FFFBEB"; sql_badge_fg = "#B45309"
        sql_bar_ok = "#F59E0B";   sql_bar_bad = "#FDE68A"
    else:
        sql_status = "GÜVENLİ";  sql_icon = "✓"
        sql_badge_bg = "#EDFAF3"; sql_badge_fg = "#0D7F4D"
        sql_bar_ok = "#10B981";   sql_bar_bad = "#D1FAE5"

    # ── KATMAN 2: KVKK ───────────────────────────────────────────────────
    KVKK_RULES = [
        (re.compile(r'\b(tc_no|tckn|kimlik_no|national_id|ssn|passport)\b', re.I),
         "KİMLİK",     "#7C3AED",
         "TC Kimlik / Pasaport numarası",
         "En kritik kişisel veri kategorisi. KVKK Madde 6 kapsamında özel nitelikli veridir. İşlenmesi için açık rıza zorunludur."),
        (re.compile(r'\b(first_name|last_name|full_name|soyad|isim|customer_name|musteri_adi)\b', re.I),
         "AD-SOYAD",   "#7C3AED",
         "İsim / Soyisim",
         "Doğrudan tanımlayıcı kişisel veridir (KVKK Md.4). Kişiyi doğrudan belirler veya belirlenebilir kılar."),
        (re.compile(r'\b(email|e_mail|mail|eposta)\b', re.I),
         "E-POSTA",    "#DB2777",
         "E-posta adresi",
         "Elektronik iletişim verisidir. İzinsiz pazarlama amaçlı kullanımı yasaktır."),
        (re.compile(r'\b(phone|telefon|gsm|mobile|cep|tel)\b', re.I),
         "TELEFON",    "#DB2777",
         "Telefon numarası",
         "İletişim kişisel verisidir. Turkcell çalışan/müşteri verileri için ek koruma gerektirir."),
        (re.compile(r'\b(address|adres|home_address|shipping_address|delivery_address|location|konum|latitude|longitude)\b', re.I),
         "KONUM",      "#0891B2",
         "Adres / Konum verisi",
         "Kişinin fiziksel konumunu tespit etmeye olanak tanır. Konum takibi için ayrıca onay gereklidir."),
        (re.compile(r'\b(iban|bic|swift|card_no|credit_card|banka|account_no|hesap)\b', re.I),
         "FİNANSAL",  "#D97706",
         "Banka / Kart bilgisi",
         "Finansal kişisel veridir. PCI-DSS standartları da geçerlidir. Şifreli saklama zorunludur."),
        (re.compile(r'\b(salary|maas|ucret|income)\b', re.I),
         "GELİR",     "#D97706",
         "Maaş / Gelir bilgisi",
         "Hassas finansal kişisel veridir. İşlenmesi için meşru amaç ve orantılılık ilkesi aranır."),
        (re.compile(r'\b(health|saglik|hastalik|disease|tani|diagnosis|birth_date|dogum_tarihi|birth_year)\b', re.I),
         "SAĞLIK/YAŞ","#DC2626",
         "Sağlık / Doğum verisi",
         "Özel nitelikli kişisel veridir (KVKK Md.6). Açık rıza olmadan işlenemez."),
        (re.compile(r'\b(ip_address|ip_addr|device_id|user_agent|cookie|session_id)\b', re.I),
         "DİJİTAL",   "#6366F1",
         "IP / Cihaz kimliği",
         "Dijital iz verisidir. Kişiyi dolaylı olarak tanımlamaya olanak tanır."),
        (re.compile(r'\b(password|sifre|token|secret|hash|pin)\b', re.I),
         "GÜVENLİK",  "#B91C1C",
         "Şifre / Token alanı",
         "KESİNLİKLE sorgu çıktısında olmamalıdır. Varlığı ciddi güvenlik açığına işaret eder."),
    ]

    kvkk_hits = []
    for pat, kategori, renk, baslik, aciklama in KVKK_RULES:
        if pat.search(sql):
            kvkk_hits.append((kategori, renk, baslik, aciklama))

    total_kvkk   = len(KVKK_RULES)
    issues_kvkk  = len(kvkk_hits)
    ok_kvkk      = total_kvkk - issues_kvkk
    pct_ok_kvkk  = round(ok_kvkk  / total_kvkk * 100)
    pct_bad_kvkk = 100 - pct_ok_kvkk

    if issues_kvkk == 0:
        kvkk_status = "TEMİZ";       kvkk_icon = "✓"
        kvkk_badge_bg = "#EDFAF3";   kvkk_badge_fg = "#0D7F4D"
    elif issues_kvkk <= 2:
        kvkk_status = "DİKKAT";      kvkk_icon = "⚠"
        kvkk_badge_bg = "#FFFBEB";   kvkk_badge_fg = "#B45309"
    else:
        kvkk_status = "YÜKSEK RİSK"; kvkk_icon = "🔴"
        kvkk_badge_bg = "#FEF2F2";   kvkk_badge_fg = "#B91C1C"

    # ── ANA KART ─────────────────────────────────────────────────────────
    # SQL bulgu satırları (özet — ana kartta)
    sql_summary_html = ""
    all_issues = sql_invalids + sql_risks
    for title, detail in all_issues:
        dot = "#EF4444" if (title, detail) in sql_invalids else "#F59E0B"
        sql_summary_html += (
            "<div style='display:flex;align-items:flex-start;gap:8px;"
            "padding:5px 0;border-bottom:1px solid #F1F5F9'>"
            "<span style='color:" + dot + ";font-size:10px;flex-shrink:0;margin-top:2px'>●</span>"
            "<span style='font-size:12px;color:#374151;line-height:1.5'>" + title + "</span>"
            "</div>"
        )
    if not all_issues:
        sql_summary_html = (
            "<span style='font-size:12px;color:#0D7F4D;font-style:italic'>"
            "✓ Tüm güvenlik kuralları karşılandı</span>"
        )

    # KVKK bulgu satırları (özet — ana kartta)
    kvkk_summary_html = ""
    for kategori, renk, baslik, aciklama in kvkk_hits:
        kvkk_summary_html += (
            "<div style='display:flex;align-items:flex-start;gap:8px;"
            "padding:5px 0;border-bottom:1px solid #F1F5F9'>"
            "<span style='background:" + renk + ";color:#fff;border-radius:4px;"
            "padding:1px 7px;font-size:10px;font-weight:700;flex-shrink:0;"
            "margin-top:2px'>" + kategori + "</span>"
            "<span style='font-size:12px;color:#374151;line-height:1.5'>" + baslik + "</span>"
            "</div>"
        )
    if not kvkk_hits:
        kvkk_summary_html = (
            "<span style='font-size:12px;color:#0D7F4D;font-style:italic'>"
            "✓ Kişisel/hassas veri sütunu tespit edilmedi</span>"
        )

    # KVKK uyarı notu
    kvkk_note_html = ""
    if kvkk_hits:
        kvkk_note_html = (
            "<div style='background:#FFF8F0;border:1px solid #FDE68A;"
            "border-left:3px solid #D97706;border-radius:8px;"
            "padding:10px 14px;margin-top:12px;"
            "font-size:12px;color:#92400E;line-height:1.7'>"
            "<strong>⚖️ KVKK / GDPR Hatırlatma:</strong> "
            "Bu sorgu kişisel veri içeren sütunlara erişiyor. "
            "Turkcell İç Denetim prosedürleri gereği:<br>"
            "① Veri sahibi onayı alındı mı?<br>"
            "② Erişim amacı kayıt altında mı?<br>"
            "③ Sonuçlar güvenli ortamda işlenecek mi?<br>"
            "<span style='font-size:11px;opacity:0.75'>"
            "KVKK Md.4 — Kişisel verilerin işlenmesinde genel ilkeler</span>"
            "</div>"
        )

    # ── ANA KART HTML ─────────────────────────────────────────────────────
    card = (
        "<div style='background:#fff;border:1px solid #E2E8F0;border-radius:14px;"
        "padding:18px 22px;margin:10px 0;"
        "box-shadow:0 4px 16px rgba(0,0,0,0.07);font-family:Inter,system-ui,sans-serif'>"

        # Başlık
        "<div style='display:flex;align-items:center;justify-content:space-between;"
        "margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #F1F5F9'>"
        "<span style='font-size:11px;font-weight:700;color:#003DA5;"
        "letter-spacing:1.6px;text-transform:uppercase'>"
        "🛡️ Güvenlik &amp; Uyumluluk Raporu</span>"
        "<span style='font-size:10px;color:#9AA5B4'>İç Denetim Katmanı · v4.1</span>"
        "</div>"

        # İki kolon
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:14px'>"

        # ── SOL: SQL ──
        "<div style='border:1px solid #E2E8F0;border-radius:10px;padding:14px'>"
        "<div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:10px'>"
        "<span style='font-size:11px;font-weight:700;color:#374151;"
        "letter-spacing:1px;text-transform:uppercase'>⚙️ SQL Güvenlik</span>"
        "<span style='background:" + sql_badge_bg + ";color:" + sql_badge_fg + ";"
        "border:1px solid " + sql_badge_fg + "44;border-radius:20px;"
        "padding:2px 11px;font-size:11px;font-weight:700'>"
        + sql_icon + " " + sql_status + "</span>"
        "</div>"
        # bar
        "<div style='height:10px;background:#F1F5F9;border-radius:99px;overflow:hidden;margin-bottom:8px'>"
        "<div style='height:100%;display:flex'>"
        "<div style='width:" + str(pct_ok_sql) + "%;background:" + sql_bar_ok + ";transition:width .4s'></div>"
        "<div style='width:" + str(pct_bad_sql) + "%;background:" + sql_bar_bad + ";transition:width .4s'></div>"
        "</div></div>"
        # legend + yüzde
        "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'>"
        "<div style='display:flex;gap:14px'>"
        "<span style='display:flex;align-items:center;gap:5px;font-size:11px;color:#6B7280'>"
        "<span style='width:8px;height:8px;border-radius:50%;background:" + sql_bar_ok + ";display:inline-block'></span>"
        "Olumlu <strong style='color:#111827'>" + str(pct_ok_sql) + "%</strong></span>"
        "<span style='display:flex;align-items:center;gap:5px;font-size:11px;color:#6B7280'>"
        "<span style='width:8px;height:8px;border-radius:50%;background:" + sql_bar_bad + ";display:inline-block'></span>"
        "Olumsuz <strong style='color:#111827'>" + str(pct_bad_sql) + "%</strong></span>"
        "</div>"
        "<span style='font-size:10px;color:#9AA5B4'>" + str(ok_sql) + "/" + str(total_sql) + " kural</span>"
        "</div>"
        # bulgular özeti
        "<div style='font-size:10px;font-weight:700;color:#9AA5B4;"
        "letter-spacing:1.2px;text-transform:uppercase;margin-bottom:6px'>Bulgular</div>"
        + sql_summary_html +
        "</div>"

        # ── SAĞ: KVKK ──
        "<div style='border:1px solid #E2E8F0;border-radius:10px;padding:14px'>"
        "<div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:10px'>"
        "<span style='font-size:11px;font-weight:700;color:#374151;"
        "letter-spacing:1px;text-transform:uppercase'>🔏 KVKK / Veri Gizliliği</span>"
        "<span style='background:" + kvkk_badge_bg + ";color:" + kvkk_badge_fg + ";"
        "border:1px solid " + kvkk_badge_fg + "44;border-radius:20px;"
        "padding:2px 11px;font-size:11px;font-weight:700'>"
        + kvkk_icon + " " + kvkk_status + "</span>"
        "</div>"
        # bar
        "<div style='height:10px;background:#F1F5F9;border-radius:99px;overflow:hidden;margin-bottom:8px'>"
        "<div style='height:100%;display:flex'>"
        "<div style='width:" + str(pct_ok_kvkk) + "%;background:#10B981;transition:width .4s'></div>"
        "<div style='width:" + str(pct_bad_kvkk) + "%;background:#7C3AED;transition:width .4s'></div>"
        "</div></div>"
        # legend
        "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'>"
        "<div style='display:flex;gap:14px'>"
        "<span style='display:flex;align-items:center;gap:5px;font-size:11px;color:#6B7280'>"
        "<span style='width:8px;height:8px;border-radius:50%;background:#10B981;display:inline-block'></span>"
        "Temiz <strong style='color:#111827'>" + str(pct_ok_kvkk) + "%</strong></span>"
        "<span style='display:flex;align-items:center;gap:5px;font-size:11px;color:#6B7280'>"
        "<span style='width:8px;height:8px;border-radius:50%;background:#7C3AED;display:inline-block'></span>"
        "Kişisel Veri <strong style='color:#111827'>" + str(pct_bad_kvkk) + "%</strong></span>"
        "</div>"
        "<span style='font-size:10px;color:#9AA5B4'>" + str(ok_kvkk) + "/" + str(total_kvkk) + " kategori</span>"
        "</div>"
        # kvkk özeti
        "<div style='font-size:10px;font-weight:700;color:#9AA5B4;"
        "letter-spacing:1.2px;text-transform:uppercase;margin-bottom:6px'>Tespit Edilen Kategoriler</div>"
        + kvkk_summary_html +
        "</div>"
        "</div>"  # grid

        + kvkk_note_html +

        # Genel durum
        "<div style='display:flex;align-items:center;gap:8px;"
        "border-top:1px solid #F1F5F9;padding-top:12px;margin-top:4px;flex-wrap:wrap'>"
        "<span style='font-size:11px;font-weight:700;color:#6B7A90;"
        "letter-spacing:1px;text-transform:uppercase;flex-shrink:0'>Genel Durum:</span>"
        "<span style='background:" + sql_badge_bg + ";color:" + sql_badge_fg + ";"
        "border:1px solid " + sql_badge_fg + "33;border-radius:20px;"
        "padding:3px 13px;font-size:11px;font-weight:700'>"
        "SQL " + sql_icon + " " + sql_status + "</span>"
        "<span style='background:" + kvkk_badge_bg + ";color:" + kvkk_badge_fg + ";"
        "border:1px solid " + kvkk_badge_fg + "33;border-radius:20px;"
        "padding:3px 13px;font-size:11px;font-weight:700'>"
        "KVKK " + kvkk_icon + " " + kvkk_status + "</span>"
        "<span style='font-size:10px;color:#9AA5B4;margin-left:auto'>"
        "Turkcell İç Denetim · TURKCELL SQL AI v4.1</span>"
        "</div>"
        "</div>"
    )

    st.markdown(card, unsafe_allow_html=True)

    # ── DETAY EXPANDER: SQL KURALLARI ─────────────────────────────────────
    if all_issues or True:  # Her zaman göster
        exp_label = (
            "📋  SQL Kural Detayları — "
            + str(ok_sql) + "/" + str(total_sql) + " kural geçti"
            + ("  |  " + str(issues_sql) + " sorun" if issues_sql else "  |  Tüm kurallar ✓")
        )
        with st.expander(exp_label, expanded=False):
            # Başlık
            st.markdown(
                "<p style='font-size:12px;color:#6B7A90;margin:0 0 12px'>"
                "Her kural için durum, açıklama ve öneri aşağıda listelenmiştir.</p>",
                unsafe_allow_html=True
            )

            # Tüm kuralları listele
            all_rules_display = []
            # INVALID kuralları
            for pat, title, detail in INVALID_RULES:
                triggered = pat.search(s)
                all_rules_display.append(("INVALID", title, detail, bool(triggered)))
            # RISKY kuralları
            for pat, title, detail in RISKY_RULES:
                triggered = pat.search(s)
                all_rules_display.append(("RISKY", title, detail, bool(triggered)))

            for rule_type, title, detail, triggered in all_rules_display:
                if triggered:
                    bg    = "#FEF2F2" if rule_type == "INVALID" else "#FFFBEB"
                    left  = "#EF4444" if rule_type == "INVALID" else "#F59E0B"
                    icon  = "✗" if rule_type == "INVALID" else "⚠"
                    t_col = "#B91C1C" if rule_type == "INVALID" else "#B45309"
                    badge_txt = "GEÇERSİZ" if rule_type == "INVALID" else "RİSK"
                    badge_bg2 = "#FEF2F2" if rule_type == "INVALID" else "#FFFBEB"
                else:
                    bg    = "#F0FFF4"; left  = "#10B981"
                    icon  = "✓";       t_col = "#0D7F4D"
                    badge_txt = "GEÇTİ"; badge_bg2 = "#EDFAF3"

                st.markdown(
                    "<div style='background:" + bg + ";border:1px solid " + left + "33;"
                    "border-left:3px solid " + left + ";border-radius:8px;"
                    "padding:10px 14px;margin-bottom:8px'>"
                    "<div style='display:flex;align-items:center;gap:8px;margin-bottom:4px'>"
                    "<span style='font-size:13px'>" + icon + "</span>"
                    "<span style='font-size:13px;font-weight:700;color:" + t_col + ";flex:1'>" + title + "</span>"
                    "<span style='background:" + badge_bg2 + ";color:" + t_col + ";"
                    "border:1px solid " + t_col + "33;border-radius:12px;"
                    "padding:1px 9px;font-size:10px;font-weight:700'>" + badge_txt + "</span>"
                    "</div>"
                    "<p style='font-size:12px;color:#374151;line-height:1.6;margin:0'>" + detail + "</p>"
                    "</div>",
                    unsafe_allow_html=True
                )

    # ── DETAY EXPANDER: KVKK KATEGORİLERİ ───────────────────────────────
    kvkk_exp_label = (
        "🔏  KVKK Kategori Detayları — "
        + str(ok_kvkk) + "/" + str(total_kvkk) + " kategori temiz"
        + ("  |  " + str(issues_kvkk) + " kişisel veri" if issues_kvkk else "  |  Tüm kategoriler ✓")
    )
    with st.expander(kvkk_exp_label, expanded=False):
        st.markdown(
            "<p style='font-size:12px;color:#6B7A90;margin:0 0 12px'>"
            "Her KVKK veri kategorisi için sorgu tarama sonucu ve yasal dayanak aşağıdadır.</p>",
            unsafe_allow_html=True
        )

        for pat, kategori, renk, baslik, aciklama in KVKK_RULES:
            triggered = bool(pat.search(sql))
            if triggered:
                bg2   = "#FAF5FF"; left2 = renk; icon2 = "⚠"; t_col2 = renk
            else:
                bg2   = "#F0FFF4"; left2 = "#10B981"; icon2 = "✓"; t_col2 = "#0D7F4D"

            st.markdown(
                "<div style='background:" + bg2 + ";border:1px solid " + left2 + "33;"
                "border-left:3px solid " + left2 + ";border-radius:8px;"
                "padding:10px 14px;margin-bottom:8px'>"
                "<div style='display:flex;align-items:center;gap:8px;margin-bottom:4px'>"
                "<span style='font-size:13px'>" + icon2 + "</span>"
                "<span style='background:" + renk + ";color:#fff;border-radius:4px;"
                "padding:1px 8px;font-size:10px;font-weight:700'>" + kategori + "</span>"
                "<span style='font-size:13px;font-weight:700;color:" + t_col2 + ";flex:1'>"
                + baslik + "</span>"
                "<span style='background:" + bg2 + ";color:" + t_col2 + ";"
                "border:1px solid " + t_col2 + "33;border-radius:12px;"
                "padding:1px 9px;font-size:10px;font-weight:700'>"
                + ("TESPİT EDİLDİ" if triggered else "TEMİZ") + "</span>"
                "</div>"
                "<p style='font-size:12px;color:#374151;line-height:1.6;margin:0'>" + aciklama + "</p>"
                "</div>",
                unsafe_allow_html=True
            )



# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────
PIPELINE_SYSTEM = """You are TURKCELL SQL AI – an enterprise-grade SQL assistant.

Your job is to convert natural language into SAFE, CORRECT, and BUSINESS-ACCURATE SQL queries.

You MUST follow a structured reasoning pipeline.
You MUST follow all steps in order. You MUST NOT skip steps.

==================================
GLOBAL RULES
==================================
SQL MODE defines what operations are allowed. Respect it strictly.

READ-ONLY  → Only SELECT, WITH/CTE, CREATE VIEW
WRITE      → Also INSERT INTO...SELECT, UPDATE, DELETE, MERGE/UPSERT
DDL        → Also CREATE TABLE, ALTER TABLE, DROP TABLE,
             CREATE INDEX, CREATE SEQUENCE
FULL       → All SQL — add -- WARNING on destructive statements

ALWAYS:
- Never invent tables or columns — use ONLY the provided schema
- If something is ambiguous, DO NOT guess silently
- Prefer correctness over speed
- For UPDATE/DELETE: always require a WHERE clause
- Add -- WARNING comment on any destructive statement
- For multi-step ops: wrap in BEGIN; ... COMMIT; where supported
- Use CTEs over nested subqueries for readability

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
  "ambiguities": [],
  "operation_type": "SELECT | INSERT | UPDATE | DELETE | DDL | MIXED"
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
- For INSERT: list column names explicitly, never positional order
- For UPDATE/DELETE: always include WHERE; add -- WARNING comment
- For DDL: add IF NOT EXISTS / IF EXISTS guards
- For analytics: prefer CTEs over nested subqueries

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
  "notes": [],
  "transaction_recommended": true
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


def build_user_msg(prompt, dialect, style, schema, sql_mode="🔒 Read-Only"):
    style_note = {
        "Standard":  "Use uppercase keywords and clean multi-line formatting.",
        "Compact":   "Use compact, minimal whitespace.",
        "Annotated": "Add a brief SQL comment above each major clause.",
    }.get(style, "")
    mode_map = {
        "🔒 Read-Only":   "READ-ONLY — Only SELECT, WITH/CTE, CREATE VIEW allowed.",
        "✏️ Write (DML)": "WRITE — SELECT + INSERT INTO...SELECT, UPDATE (with WHERE), DELETE (with WHERE), MERGE allowed.",
        "🔧 DDL":           "DDL — SELECT + CREATE TABLE/INDEX/SEQUENCE, ALTER TABLE, DROP (with IF EXISTS guard) allowed.",
        "⚡ Full (Tamümü)":  "FULL — All SQL allowed. Add -- WARNING on any destructive statement (DELETE, DROP, TRUNCATE, UPDATE).",
    }
    mode_note = mode_map.get(sql_mode, mode_map["🔒 Read-Only"])
    parts = [f"DIALECT: {dialect}", f"SQL MODE: {mode_note}", f"STYLE: {style_note}"]
    if schema:
        parts.append(f"DATABASE SCHEMA:\n{schema.strip()}")
    parts.append(f"USER REQUEST: {prompt.strip()}")
    return "\n\n".join(parts)


def run_pipeline(prompt, key, dialect, style, model, schema=None, sql_mode="🔒 Read-Only"):
    t0 = time.time()
    client = openai.OpenAI(api_key=key)
    r = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": PIPELINE_SYSTEM},
            {"role": "user",   "content": build_user_msg(prompt, dialect, style, schema, sql_mode)},
        ],
        temperature=0.1,
        max_tokens=2400,
    )
    raw_out = r.choices[0].message.content.strip()
    elapsed = round(time.time() - t0, 2)
    tokens  = r.usage.total_tokens

    def extract(tag, text):
        m = re.search(rf"---\s*{tag}\s*---(.+?)(?=---\s*[A-Z]|$)", text, re.S | re.I)
        return m.group(1).strip() if m else ""

    intent_raw      = extract("INTENT",      raw_out)
    sql_raw         = extract("SQL",         raw_out)
    review_raw      = extract("REVIEW",      raw_out)
    explanation_raw = extract("EXPLANATION", raw_out)

    def safe_json(text):
        text = text.strip()
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
        return {}

    intent = safe_json(intent_raw)
    review = safe_json(review_raw)
    sql    = sql_raw.strip()
    sql = re.sub(r"^```[a-zA-Z]*\n?", "", sql).strip()
    sql = re.sub(r"\n?```$", "", sql).strip()

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


# ── auth guard ───────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    render_login()
    st.stop()

# ── nav bar → header altında render edilecek (aşağıda) ──────────────────────

# Admin sayfası
if st.session_state.page == "admin":
    render_admin()
    st.stop()

# Rol bazlı SQL modu kısıtlaması
_allowed_modes = ROLE_MODES.get(st.session_state.role, ["🔒 Read-Only"])

# ── SABAH BRİFİNGİ — günde bir kez göster ──────────────────────────────────
if not st.session_state.briefing_shown:
    _today = __import__("datetime").date.today().isoformat()
    _brief_conn = get_db()
    _brief_stats = {
        "today_q":   _brief_conn.execute(
            "SELECT COUNT(*) FROM query_log WHERE user_id=? AND created_at>=?",
            (st.session_state.user_id, _today)).fetchone()[0],
        "kvkk_today":_brief_conn.execute(
            "SELECT COUNT(*) FROM query_log WHERE user_id=? AND kvkk_hit=1 AND created_at>=?",
            (st.session_state.user_id, _today)).fetchone()[0],
        "total_q":   _brief_conn.execute(
            "SELECT COUNT(*) FROM query_log WHERE user_id=?",
            (st.session_state.user_id,)).fetchone()[0],
        "last_prompt":_brief_conn.execute(
            "SELECT prompt FROM query_log WHERE user_id=? ORDER BY created_at DESC LIMIT 1",
            (st.session_state.user_id,)).fetchone(),
    }
    _brief_conn.close()
    _hour = __import__("datetime").datetime.now().hour
    _greeting = "Günaydın" if _hour < 12 else ("İyi akşamlar" if _hour >= 18 else "İyi günler")
    _brief_html = (
        f"<div style='background:linear-gradient(135deg,#003DA5,#0057D9);"
        f"border-radius:12px;padding:1rem 1.3rem;margin:.5rem 0 .8rem;"
        f"display:flex;align-items:center;justify-content:space-between;gap:1rem'>"
        f"<div>"
        f"<div style='font-size:.78rem;color:#CADCFC;margin-bottom:.25rem'>"
        f"☀️ {_greeting}, <b style='color:#FFC72C'>{st.session_state.username}</b></div>"
        f"<div style='display:flex;gap:1.2rem;flex-wrap:wrap'>"
        f"<span style='font-size:.72rem;color:#fff'>"
        f"📊 Bugün <b>{_brief_stats['today_q']}</b> sorgu</span>"
        f"<span style='font-size:.72rem;color:#fff'>"
        f"📈 Toplam <b>{_brief_stats['total_q']}</b> sorgu</span>"
        + (f"<span style='font-size:.72rem;color:#FCA5A5'>"
           f"🔏 Bugün <b>{_brief_stats['kvkk_today']}</b> KVKK uyarısı</span>"
           if _brief_stats["kvkk_today"] > 0 else "")
        + (f"<span style='font-size:.72rem;color:#CADCFC'>"
           f"🔁 Son: <i>{_brief_stats['last_prompt'][0][:45]}…</i></span>"
           if _brief_stats["last_prompt"] else "")
        + f"</div></div>"
        f"</div>"
    )
    st.markdown(_brief_html, unsafe_allow_html=True)
    st.session_state.briefing_shown = True


# ── api key ───────────────────────────────────────────────────────────────────
api_key = st.secrets.get("OPENAI_API_KEY", "")
if not api_key:
    st.markdown(
        f'<div class="hdr"><div class="hdr-left">'
        f'<img class="hdr-logo" src="{LOGO_SRC}" alt="logo">'
        f'<div class="hdr-vline"></div>'
        f'<div><div class="hdr-title">turkcell.sql.ai.com.tr</div>'
        f'<div class="hdr-sub">Natural Language → SQL</div></div>'
        f'</div><div class="hdr-pill">v4.1</div></div>',
        unsafe_allow_html=True)
    st.markdown(mk_alert("🔐", "API Anahtarı Bulunamadı",
        '<code>.streamlit/secrets.toml</code> dosyasına ekleyin:'
        '<pre>OPENAI_API_KEY = "sk-..."</pre>'
        'Streamlit Cloud: <strong>App Settings › Secrets</strong>'),
        unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════
# Header HTML
st.markdown(
    f'<div class="hdr"><div class="hdr-left">'
    f'<img class="hdr-logo" src="{LOGO_SRC}" alt="logo">'
    f'<div class="hdr-vline"></div>'
    f'<div><div class="hdr-title">turkcell.sql.ai.com.tr</div>'
    f'<div class="hdr-sub">Natural Language → SQL</div></div>'
    f'</div><div class="hdr-pill">👤 {st.session_state.username} · {ROLE_LABELS.get(st.session_state.role,"")}</div></div>',
    unsafe_allow_html=True)

# ── NAV BAR — header altında butonlar ───────────────────────────────────────
_nc = st.columns([1, 1, 1, 1, 1])
with _nc[4]:
    if st.button("🚪 Çıkış", key="logout", use_container_width=True):
        for k in ["logged_in","username","role","user_id","page","history","qc","tt","lp"]:
            st.session_state[k] = False if k=="logged_in" else (
                "main" if k=="page" else (
                [] if k=="history" else (
                0 if k in ["qc","tt"] else "")))
        st.rerun()
with _nc[3]:
    if st.session_state.role == "admin":
        if st.session_state.page == "admin":
            if st.button("◀ Ana Sayfa", key="goto_main", use_container_width=True):
                st.session_state.page = "main"
                st.rerun()
        else:
            if st.button("⚡ Admin Paneli", key="goto_admin", use_container_width=True):
                st.session_state.page = "admin"
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════
#  UPLOAD CARD
# ══════════════════════════════════════════════════════════════════════════
# ── KİŞİSEL ÖNERİ MOTORU ───────────────────────────────────────────────────
_rec_history = db_get_history(st.session_state.user_id, limit=30)
if _rec_history:
    # En sık tekrarlanan prompt'ları bul
    from collections import Counter
    _prompt_counts = Counter(e['prompt'] for e in _rec_history)
    _top_prompts   = [p for p,c in _prompt_counts.most_common(3) if c >= 2]
    # Son 24 saatte sorulmamış önerileri göster
    import datetime as _dt
    _yesterday = (_dt.datetime.now() - _dt.timedelta(days=1)).strftime('%Y-%m-%d %H:%M')
    _recent    = {e['prompt'] for e in _rec_history if e.get('created_at','') > _yesterday}
    _suggestions = [p for p in _top_prompts if p not in _recent]
    if _suggestions:
        st.markdown(
            "<div style='background:#F0F4FF;border:1px solid #BFDBFE;"
            "border-left:3px solid #003DA5;border-radius:10px;"
            "padding:.7rem 1rem;margin-bottom:.8rem'>"
            "<span style='font-size:.65rem;font-weight:700;color:#003DA5;"
            "letter-spacing:1.2px;text-transform:uppercase'>🧠 Sık Kullandıklarınız</span>",
            unsafe_allow_html=True)
        _sug_cols = st.columns(len(_suggestions))
        for _si, _sug in enumerate(_suggestions):
            with _sug_cols[_si]:
                _short = _sug[:45] + '…' if len(_sug) > 45 else _sug
                if st.button(f'🔁 {_short}', key=f'sug_{_si}', use_container_width=True):
                    _old_key = f'pk_{st.session_state.prompt_reset}'
                    if _old_key in st.session_state:
                        del st.session_state[_old_key]
                    st.session_state.lp = _sug
                    st.session_state.prompt_reset += 1
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown('<p class="upload-lbl">📂 Veritabanı Şemasını Yükle (.sql, .txt)</p>', unsafe_allow_html=True)

# ── Kayıtlı DB bağlantılarından şema yükle ──────────────────────────────────
_saved_conns = db_conn_list(st.session_state.user_id, st.session_state.role)
if _saved_conns:
    _conn_names = [c["name"] for c in _saved_conns]
    _sel_conn = st.selectbox(
        "🔌 Kayıtlı bağlantıdan şema yükle",
        ["— Elle yükle —"] + _conn_names,
        key="sel_conn"
    )
    if _sel_conn != "— Elle yükle —":
        _found_conn = next((c for c in _saved_conns if c["name"]==_sel_conn), None)
        if _found_conn:
            _saved_schemas = db_get_schemas(st.session_state.user_id, st.session_state.role)
            _auto_schema = next((s for s in _saved_schemas if s["name"]==f"{_sel_conn}_auto"), None)
            if _auto_schema:
                schema_text = _auto_schema["content"]
                schema_meta = {"name":_auto_schema["name"],
                               "tables":_auto_schema["table_count"],
                               "chars":len(_auto_schema["content"])}
                st.success(f"✅ '{_sel_conn}' şeması yüklendi ({_auto_schema[chr(39)]}")
            else:
                st.warning("Bu bağlantı için henüz şema çekilmemiş. Admin Paneli → DB Bağlantıları → Test Et.")

uf = st.file_uploader("sf", type=["sql", "txt"],
                      accept_multiple_files=False,
                      label_visibility="collapsed")
schema_text, schema_meta = None, {}

if uf:
    try:
        raw, chars, tables = parse_schema(uf)
        if chars > 500_000:
            st.markdown(mk_alert("⚠️", "Dosya Çok Büyük",
                "Şema 500 KB limitini aşıyor. Kullanılmayan tabloları kaldırın.", "warn"),
                unsafe_allow_html=True)
        else:
            schema_text = raw
            tbl_names   = extract_tables(raw)
            schema_meta = {"name": uf.name, "tables": len(tbl_names), "chars": chars}
            MAX_SHOW    = 14
            chips = "".join(f'<span class="tbl-chip">⬡ {t}</span>' for t in tbl_names[:MAX_SHOW])
            if len(tbl_names) > MAX_SHOW:
                chips += f'<span class="tbl-more">+{len(tbl_names)-MAX_SHOW} daha</span>'
            st.markdown(
                f'<div class="schema-ok"><span class="dot"></span>'
                f'<strong>{uf.name}</strong> yüklendi — {len(tbl_names)} tablo · {chars:,} karakter</div>'
                + (f'<div class="tbl-row">{chips}</div>' if chips else ""),
                unsafe_allow_html=True)
            _sch_col1, _sch_col2 = st.columns([3,1])
            with _sch_col1:
                _sch_desc = st.text_input("Şema açıklaması (opsiyonel)", key="sch_desc", placeholder="CRM veritabanı, prod ortamı...")
            with _sch_col2:
                st.markdown("<div style='margin-top:1.7rem'></div>", unsafe_allow_html=True)
                if st.button("💾 Şemayı Kaydet", key="save_schema"):
                    _action = db_save_schema(st.session_state.user_id, uf.name, _sch_desc, raw, len(tbl_names))
                    st.success(f"✅ '{uf.name}' {_action}!")
            # Kayıtlı şemalar
            _saved = db_get_schemas(st.session_state.user_id, st.session_state.role)
            if _saved:
                _sel = st.selectbox("📂 Kayıtlı şema yükle", ["— Seç —"] + [s["name"] for s in _saved], key="sel_schema")
                if _sel != "— Seç —":
                    _found = next((s for s in _saved if s["name"]==_sel), None)
                    if _found:
                        schema_text = _found["content"]
                        schema_meta = {"name":_found["name"],"tables":_found["table_count"],"chars":len(_found["content"])}
                        st.success(f"✅ '{_sel}' yüklendi ({_found['table_count']} tablo)")
    except Exception as e:
        st.markdown(mk_alert("❌", "Dosya Hatası", f"Okunamadı: {e}"), unsafe_allow_html=True)

st.markdown(
    '<div class="upload-help">💡 <strong>İpucu:</strong> '
    '<code>pg_dump --schema-only</code> (PostgreSQL) veya '
    '<code>SHOW CREATE TABLE</code> (MySQL) ile şemanızı dışa aktarıp '
    '<code>.sql</code> dosyası olarak kaydedin.</div>',
    unsafe_allow_html=True)

if not uf:
    st.markdown(mk_alert("ℹ️", "Şema Yüklenmedi — Genel Bilgi Kullanılıyor",
        "AI tablo/sütun isimlerini açıklamanızdan çıkaracak. "
        "Daha doğru sonuçlar için şema dosyası yükleyin.", "info"),
        unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  FORM CARD
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<p class="lbl">⚙ Yapılandırma</p>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    dialect = st.selectbox("Dialect",
        ["PostgreSQL", "MySQL", "SQLite", "SQL Server (T-SQL)", "BigQuery", "Snowflake"], key="d")
with c2:
    style = st.selectbox("Stil", ["Standard", "Annotated", "Compact"], key="s")
with c3:
    model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"], key="m")
with c4:
    sql_mode = st.selectbox("SQL Modu",
        _allowed_modes,
        key="sql_mode",
        help=f"Rolünüz ({st.session_state.role}): {len(_allowed_modes)} mod kullanılabilir")

st.markdown('<div class="card-sep"></div>', unsafe_allow_html=True)

if schema_text:
    st.markdown(
        f'<div class="sbadge"><span class="dg"></span>'
        f'Şema Modu · {schema_meta["name"]} · {schema_meta["tables"]} tablo</div>',
        unsafe_allow_html=True)

# ── ŞABLON SEÇİCİ — 3 KATMAN ───────────────────────────────────────────────
_tmpls = templates_get(st.session_state.user_id, st.session_state.role)
_sys_tmpls  = [t for t in _tmpls if t.get('scope','system') == 'system']
_team_tmpls = [t for t in _tmpls if t.get('scope') == 'team']
_per_tmpls  = [t for t in _tmpls if t.get('scope') == 'personal']

st.markdown('<p class="lbl">📋 Şablonlar</p>', unsafe_allow_html=True)

# Şablon kart yardımcısı
def _tpl_card(t, key, scope_color, scope_bg, show_delete=False, del_key=None):
    prompt_short = t['prompt'][:80] + ('…' if len(t['prompt']) > 80 else '')
    # Tıklanınca prompt'u session_state'e yaz — st.button yerine HTML kart
    st.markdown(
        f"<div style='"
        f"background:{scope_bg};"
        f"border:1px solid {scope_color}55;"
        f"border-left:4px solid {scope_color};"
        f"border-radius:10px;"
        f"padding:.8rem 1rem;"
        f"margin-bottom:.4rem;"
        f"cursor:pointer;"
        f"transition:box-shadow .15s;"
        f"'>"
        f"<div style='font-size:.9rem;font-weight:700;color:#0F1623;margin-bottom:.3rem'>"
        f"{t['icon']}  {t['title']}</div>"
        f"<div style='font-size:.76rem;color:#374151;line-height:1.5;"
        f"background:rgba(255,255,255,.6);border-radius:6px;padding:.3rem .5rem'>"
        f"{prompt_short}</div>"
        f"</div>",
        unsafe_allow_html=True)
    if show_delete:
        _cb1, _cb2 = st.columns([4, 1])
        with _cb1:
            if st.button(f'▶  {t["title"]} — Kullan', key=key, use_container_width=True):
                _old_key = f'pk_{st.session_state.prompt_reset}'
                if _old_key in st.session_state:
                    del st.session_state[_old_key]
                st.session_state.lp = t['prompt']
                st.session_state.prompt_reset += 1
                st.rerun()
        with _cb2:
            if st.button('🗑', key=del_key, use_container_width=True):
                templates_delete(t['id'], st.session_state.user_id, st.session_state.role)
                st.rerun()
    else:
        if st.button(f'▶  {t["title"]} — Kullan', key=key, use_container_width=True):
            _old_key = f'pk_{st.session_state.prompt_reset}'
            if _old_key in st.session_state:
                del st.session_state[_old_key]
            st.session_state.lp = t['prompt']
            st.session_state.prompt_reset += 1
            st.rerun()

# ── Ana 3 sekme ──────────────────────────────────────────────────────────
_scope_tabs = st.tabs([
    f'Sistem ({len(_sys_tmpls)})',
    f'Ekip ({len(_team_tmpls)})',
    f'Kişisel ({len(_per_tmpls)})',
])

# ── SİSTEM ŞABLONLARI ─────────────────────────────────────────────────────
with _scope_tabs[0]:
    if _sys_tmpls:
        # Admin tüm kategorileri görür, diğerleri sadece şemasıyla uyumlu olanları
        _visible_sys = _sys_tmpls if st.session_state.role == 'admin' else [
            t for t in _sys_tmpls
            if not schema_text or any(
                kw.lower() in (schema_text or '').lower()
                for kw in t['title'].lower().split()
            ) or t['category'] in ['🔍 Denetim']
        ]
        if not _visible_sys:
            _visible_sys = _sys_tmpls  # hiç eşleşme yoksa hepsini göster

        _cats = sorted(set(t['category'] for t in _visible_sys))
        _cat_tabs = st.tabs([c.split(' ',1)[1] if ' ' in c else c for c in _cats])
        for _ci, _ct in enumerate(_cat_tabs):
            with _ct:
                _ct_tmpls = [t for t in _visible_sys if t['category']==_cats[_ci]]
                _tcols = st.columns(min(len(_ct_tmpls), 3))
                for _ti, _t in enumerate(_ct_tmpls):
                    with _tcols[_ti % 3]:
                        _tpl_card(_t, f"sys_{_t['id']}", "#003DA5", "#F0F4FF")
    else:
        st.info('Sistem şablonu yok.')

    if st.session_state.role == 'admin':
        with st.expander('➕ Sistem Şablonu Ekle', expanded=False):
            _sc1, _sc2 = st.columns(2)
            with _sc1:
                _s_cat   = st.text_input('Kategori', key='sc_cat', placeholder='📊 CRM')
                _s_title = st.text_input('Başlık', key='sc_title')
            with _sc2:
                _s_icon  = st.text_input('İkon', key='sc_icon', value='📋')
                _s_save  = st.button('💾 Kaydet', key='sc_save')
            _s_prompt = st.text_area('Prompt', key='sc_prompt', height=70)
            if _s_save and _s_cat and _s_title and _s_prompt:
                templates_add(_s_cat, _s_title, _s_prompt, _s_icon,
                              st.session_state.username, scope='system')
                st.success('✅ Sistem şablonu eklendi!'); st.rerun()

# ── EKİP ŞABLONLARI ───────────────────────────────────────────────────────
with _scope_tabs[1]:
    if _team_tmpls:
        _tcols2 = st.columns(min(len(_team_tmpls), 3))
        for _ti, _t in enumerate(_team_tmpls):
            with _tcols2[_ti % 3]:
                _tpl_card(_t, f"team_{_t['id']}", "#0891B2", "#EBF8FF")
    else:
        st.markdown(
            f"<div style='background:#F0F4FF;border:1px solid #BFDBFE;border-radius:10px;"
            f"padding:.8rem 1rem;font-size:.82rem;color:#6B7A90'>"
            f"👥 <b>{st.session_state.role}</b> ekibi için henüz şablon yok. "
            f"Aşağıdan ekleyebilirsiniz.</div>",
            unsafe_allow_html=True)
    with st.expander('➕ Ekip Şablonu Ekle', expanded=False):
        st.caption(f'Bu şablon tüm {st.session_state.role} rolündeki kullanıcılara görünür.')
        _ec1, _ec2 = st.columns(2)
        with _ec1:
            _e_cat   = st.text_input('Kategori', key='ec_cat', placeholder='📡 Ekibim')
            _e_title = st.text_input('Başlık', key='ec_title')
        with _ec2:
            _e_icon  = st.text_input('İkon', key='ec_icon', value='👥')
            _e_save  = st.button('💾 Kaydet', key='ec_save')
        _e_prompt = st.text_area('Prompt', key='ec_prompt', height=70)
        if _e_save and _e_cat and _e_title and _e_prompt:
            templates_add(_e_cat, _e_title, _e_prompt, _e_icon,
                          st.session_state.username,
                          scope='team', team_role=st.session_state.role)
            st.success(f"✅ '{st.session_state.role}' ekibine şablon eklendi!"); st.rerun()

# ── KİŞİSEL ŞABLONLAR ─────────────────────────────────────────────────────
with _scope_tabs[2]:
    _suggestions = templates_auto_suggest(st.session_state.user_id)
    if _suggestions:
        st.markdown(
            "<div style='background:#FFFBEB;border:1px solid #FDE68A;"
            "border-left:3px solid #D97706;border-radius:10px;"
            "padding:.6rem 1rem;margin-bottom:.7rem'>"
            "<span style='font-size:.65rem;font-weight:700;color:#B45309;"
            "letter-spacing:1.2px;text-transform:uppercase'>✨ Otomatik Öneri</span>"
            "<br><span style='font-size:.78rem;color:#92400E'>"
            "Bu sorguları en az 2 kez sordunuz — kişisel şablonunuza eklemek ister misiniz?</span>"
            "</div>", unsafe_allow_html=True)
        for _sg in _suggestions:
            _sga, _sgb = st.columns([5, 1])
            with _sga:
                st.markdown(
                    f"<div style='background:#FFFDF5;border:1px solid #FDE68A;"
                    f"border-radius:8px;padding:.5rem .8rem;margin-bottom:.3rem'>"
                    f"<div style='font-size:.84rem;font-weight:600;color:#0F1623'>"
                    f"🔁 {_sg['prompt'][:65]}{'…' if len(_sg['prompt'])>65 else ''}</div>"
                    f"<div style='font-size:.7rem;color:#9AA5B4;margin-top:.15rem'>"
                    f"{_sg['cnt']} kez soruldu</div>"
                    f"</div>", unsafe_allow_html=True)
            with _sgb:
                if st.button('➕', key=f"sg_{hash(_sg['prompt'])}", use_container_width=True):
                    templates_add(
                        '⭐ Favorilerim',
                        _sg['prompt'][:40] + ('…' if len(_sg['prompt'])>40 else ''),
                        _sg['prompt'], '⭐',
                        st.session_state.username,
                        scope='personal', user_id=st.session_state.user_id)
                    st.success('✅ Favorilerime eklendi!'); st.rerun()

    if _per_tmpls:
        _pcols = st.columns(min(len(_per_tmpls), 3))
        for _pi, _pt in enumerate(_per_tmpls):
            with _pcols[_pi % 3]:
                _tpl_card(_pt, f"per_u_{_pt['id']}", "#0D7F4D", "#EDFAF3",
                          show_delete=True, del_key=f"per_d_{_pt['id']}")
    else:
        if not _suggestions:
            st.markdown(
                "<div style='background:#F5F7FA;border:1px solid #DCE3ED;border-radius:10px;"
                "padding:.8rem 1rem;font-size:.82rem;color:#6B7A90'>"
                "👤 Henüz kişisel şablonunuz yok. Aşağıdan ekleyebilir veya "
                "sık kullandığınız sorgular otomatik önerilir.</div>",
                unsafe_allow_html=True)

    # Manuel kişisel şablon ekle
    with st.expander('➕ Kişisel Şablon Ekle', expanded=False):
        _pc1, _pc2 = st.columns(2)
        with _pc1:
            _p_cat   = st.text_input('Kategori', key='pc_cat', placeholder='⭐ Favorilerim')
            _p_title = st.text_input('Başlık', key='pc_title')
        with _pc2:
            _p_icon  = st.text_input('İkon', key='pc_icon', value='⭐')
            _p_save  = st.button('💾 Kaydet', key='pc_save')
        _p_prompt = st.text_area('Prompt', key='pc_prompt', height=70)
        if _p_save and _p_cat and _p_title and _p_prompt:
            templates_add(_p_cat, _p_title, _p_prompt, _p_icon,
                          st.session_state.username,
                          scope='personal',
                          user_id=st.session_state.user_id)
            st.success('✅ Kişisel şablonunuza eklendi!'); st.rerun()

st.markdown('<div class="card-sep"></div>', unsafe_allow_html=True)

# ── AKILLI TAMAMLAMA ─────────────────────────────────────────────────────────
st.markdown(
    "<div style='background:#fff;border:1px solid #DCE3ED;border-radius:10px;"
    "padding:.5rem .9rem;margin-bottom:.4rem;display:flex;align-items:center;gap:.5rem'>"
    "<span style='font-size:.9rem'>🔍</span>"
    "<span style='font-size:.8rem;color:#9AA5B4'>Hızlı arama — yazmaya başla, şablon ve geçmişten öneri gelsin</span>"
    "</div>", unsafe_allow_html=True)

_ac_input = st.text_input(
    'ac_input', value='',
    placeholder='Örn: churn, fatura, abone, tarife, alarm...',
    key=f'ac_input_{st.session_state.ac_reset}',
    label_visibility='collapsed')

if _ac_input and len(_ac_input) >= 2:
    _ac_conn = get_db()
    _ac_rows = _ac_conn.execute(
        "SELECT DISTINCT prompt FROM query_log "
        "WHERE user_id=? AND LOWER(prompt) LIKE LOWER(?) "
        "ORDER BY created_at DESC LIMIT 5",
        (st.session_state.user_id, f'%{_ac_input}%')).fetchall()
    _ac_tmpls = _ac_conn.execute(
        "SELECT DISTINCT prompt, title FROM templates "
        "WHERE (scope='system' OR scope='team' OR user_id=?) "
        "AND (LOWER(prompt) LIKE LOWER(?) OR LOWER(title) LIKE LOWER(?) OR LOWER(category) LIKE LOWER(?)) "
        "LIMIT 6",
        (st.session_state.user_id,
         f'%{_ac_input}%', f'%{_ac_input}%', f'%{_ac_input}%')).fetchall()
    _ac_conn.close()

    _all_ac = [(r[0], '🕐 Geçmişten') for r in _ac_rows] +               [(r[0], '📋 ' + r[1]) for r in _ac_tmpls]
    _seen = set()
    _unique_ac = []
    for _p, _s in _all_ac:
        if _p not in _seen:
            _seen.add(_p)
            _unique_ac.append((_p, _s))

    if _unique_ac:
        st.markdown(
            '<div style="background:#F0F4FF;border:1px solid #BFDBFE;'
            'border-left:3px solid #003DA5;border-radius:8px;'
            'padding:.4rem .8rem;margin-bottom:.3rem">'
            '<span style="font-size:.65rem;font-weight:700;color:#003DA5;'
            'letter-spacing:1.2px;text-transform:uppercase">'
            f'💡 {len(_unique_ac)} Öneri Bulundu</span></div>',
            unsafe_allow_html=True)
        for _ac_i, (_ac_prompt, _ac_src) in enumerate(_unique_ac):
            _acc1, _acc2 = st.columns([5, 1])
            with _acc1:
                _short = _ac_prompt[:80] + ('…' if len(_ac_prompt) > 80 else '')
                st.markdown(
                    '<div style="background:#fff;border:1px solid #DCE3ED;'
                    'border-radius:8px;padding:.45rem .8rem;margin-bottom:.25rem">'
                    f'<div style="font-size:.7rem;color:#003DA5;font-weight:600;margin-bottom:.1rem">{_ac_src}</div>'
                    f'<div style="font-size:.82rem;color:#1A202C">{_short}</div>'
                    '</div>',
                    unsafe_allow_html=True)
            with _acc2:
                st.markdown('<div style="margin-top:.4rem"></div>', unsafe_allow_html=True)
                if st.button('▶ Seç', key=f'ac_{_ac_i}_{st.session_state.ac_reset}',
                             use_container_width=True):
                    # Önce eski widget state'ini sil
                    _old_key = f'pk_{st.session_state.prompt_reset}'
                    if _old_key in st.session_state:
                        del st.session_state[_old_key]
                    st.session_state.lp = _ac_prompt
                    st.session_state.ac_reset += 1
                    st.session_state.prompt_reset += 1
                    st.rerun()
    else:
        _no_result = f'🔍 <b style="color:#374151">{_ac_input}</b> için öneri bulunamadı'
        st.markdown(
            '<div style="background:#F5F7FA;border:1px solid #DCE3ED;'
            'border-radius:8px;padding:.4rem .8rem;margin-bottom:.3rem;'
            f'font-size:.78rem;color:#9AA5B4">{_no_result} — prompt kutusuna direkt yazabilirsiniz.</div>',
            unsafe_allow_html=True)

st.markdown('<p class="lbl">✦ Doğal Dil ile Açıkla</p>', unsafe_allow_html=True)
prompt = st.text_area("p", value=st.session_state.lp, height=120,
    placeholder="Örn. → Geçen ay kaydolan ama henüz sipariş vermemiş kullanıcıları referans kaynağına göre gruplandır…",
    key=f"pk_{st.session_state.prompt_reset}", label_visibility="collapsed")

go = st.button("⚡  SQL Oluştur", key="go")

# Sohbet modundan gelen otomatik tetikleme
if st.session_state.get('auto_go', False):
    go = True
    st.session_state.auto_go = False

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  GENERATE
# ══════════════════════════════════════════════════════════════════════════
if go:
    st.session_state.lp = prompt
    if not prompt.strip():
        st.markdown(mk_alert("✏️", "Boş Prompt",
            "Lütfen SQL üretmek için bir açıklama girin.", "warn"),
            unsafe_allow_html=True)
        st.stop()

    # ── Önbellek kontrolü ─────────────────────────────────────────────────
    _ck  = _cache_key(prompt, dialect, schema_text)
    _cached = cache_get(_ck)
    if _cached:
        res = _cached
        st.session_state.cache_hit = True
        st.markdown(
            '<div style="background:#EDFAF3;border:1px solid #A3DFBE;border-radius:8px;'
            'padding:.45rem 1rem;margin:.4rem 0;font-size:.76rem;color:#0D7F4D;font-weight:600">'
            '⚡ Önbellekten yüklendi — API çağrısı yapılmadı</div>',
            unsafe_allow_html=True)
    else:
        st.session_state.cache_hit = False
    if not _cached:
     with st.spinner("Pipeline çalışıyor: Intent → SQL → Review…"):
      try:
        res = run_pipeline(prompt, api_key, dialect, style, model, schema_text, sql_mode)
      except openai.AuthenticationError:
        st.markdown(mk_alert("🔑", "Kimlik Hatası", "API anahtarı reddedildi."),
            unsafe_allow_html=True); st.stop()
      except openai.RateLimitError:
        st.markdown(mk_alert("⏱", "Limit Aşıldı", "OpenAI kotası doldu. Kısa süre bekleyip tekrar deneyin."),
            unsafe_allow_html=True); st.stop()
      except openai.APIConnectionError:
        st.markdown(mk_alert("🌐", "Bağlantı Hatası", "OpenAI API'ye ulaşılamadı."),
            unsafe_allow_html=True); st.stop()
      except Exception as e:
        st.markdown(mk_alert("⚙️", "Beklenmeyen Hata", f"Sorun oluştu:<br><code>{e}</code>"),
            unsafe_allow_html=True); st.stop()
     # Önbelleğe kaydet
     cache_set(_ck, prompt, res, dialect)

    valid, err = chk(res["sql"], sql_mode)
    if not valid:
        st.markdown(mk_alert("⚠️", "Güvenlik Reddi", err, "warn"),
            unsafe_allow_html=True); st.stop()

    # ── store history ─────────────────────────────────────────────────────
    st.session_state.qc += 1
    st.session_state.tt += res["tokens"]
    _review = res.get("review",{})
    _risk   = _review.get("status","") if _review else ""
    _schema_nm = schema_meta.get("name","") if schema_text else ""
    # SQLite audit log
    db_log_query(
        st.session_state.user_id, st.session_state.username,
        prompt, res["sql"], dialect, style, sql_mode,
        _schema_nm, res["tokens"], res["elapsed"], _risk, 0
    )
    st.session_state.history.insert(0, {
        "prompt":  prompt,
        "sql":     res["sql"],
        "dialect": dialect,
        "ts":      datetime.datetime.now().strftime("%d %b %Y %H:%M"),
        "tokens":  res["tokens"],
        "schema":  _schema_nm or "—",
    })
    st.session_state.history = st.session_state.history[:30]

    # ── INTENT CARD ──────────────────────────────────────────────────────
    intent = res.get("intent", {})
    if intent:
        def tag_list(items, warn=False):
            cls = "tag-warn" if warn else "tag"
            if not items:
                return f'<span class="{cls}">—</span>'
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
    mode_colors = {
        "🔒 Read-Only":   ("rgba(13,127,77,.15)",   "#A6E3A1"),
        "✏️ Write (DML)": ("rgba(251,146,60,.15)",  "#FB923C"),
        "🔧 DDL":           ("rgba(167,139,250,.15)", "#C4B5FD"),
        "⚡ Full (Tamümü)":  ("rgba(249,115,22,.18)",  "#FDBA74"),
    }
    mc_bg, mc_fg = mode_colors.get(sql_mode, mode_colors["🔒 Read-Only"])
    mode_label   = sql_mode.split("(")[0].strip()
    mode_tag = (f'<span class="sql-tag" style="background:{mc_bg};color:{mc_fg};">'
                f'{mode_label}</span>')

    sb = ""
    if schema_text:
        sb = ('<span class="sql-tag" style="background:rgba(166,227,161,.12);color:#A6E3A1;">'
              '<span class="dot" style="background:#A6E3A1"></span>'
              f'{schema_meta["name"]}</span>')

    sql_esc = (res["sql"]
               .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
               .replace('"', "&quot;").replace("'", "&#39;"))

    st.markdown(
        f'<div class="sql-card">'
        f'<pre>{hl(res["sql"])}</pre>'
        f'<div class="sql-bar">'
        f'<span class="sql-tag"><span class="dot"></span>{dialect}</span>'
        f'<div style="display:flex;gap:.45rem;align-items:center;">{mode_tag}{sb}'
        + clipboard_js(sql_esc) +
        f'<span class="sql-tag">{res["elapsed"]}s · {res["tokens"]} tok</span>'
        f'</div></div></div>',
        unsafe_allow_html=True)

    # ── RISK SCORE ────────────────────────────────────────────────────────
    render_risk_score(res["sql"])

    # ── AUTO-TEST DISCOVERY (Syntax Check) ────────────────────────────────
    with st.expander('🧪  Otomatik Test — Syntax & Dry-Run Kontrolü', expanded=False):
        st.markdown(
            "<div style='background:#F0F4FF;border:1px solid #BFDBFE;"
            "border-left:3px solid #003DA5;border-radius:8px;"
            "padding:.5rem .9rem;margin-bottom:.6rem;font-size:.78rem;color:#374151'>"
            "💡 SQL'i çalıştırmadan önce <b>syntax kontrolü</b> ve <b>dry-run</b> "
            "(EXPLAIN) testi yapar. Hata varsa yakalar, performans tahminini gösterir."
            "</div>", unsafe_allow_html=True)
        if st.button('🧪 SQL\'i Otomatik Test Et', key='auto_test'):
            _test_results = []

            # Test 1: Boş SQL kontrolü
            if not res["sql"].strip():
                _test_results.append(('FAIL', 'Boş SQL', 'SQL içeriği boş'))
            else:
                _test_results.append(('PASS', 'SQL içeriği var', f'{len(res["sql"])} karakter'))

            # Test 2: SELECT/INSERT/UPDATE/DELETE/CREATE/ALTER ile başlama kontrolü
            _first_word = res["sql"].strip().upper().split()[0] if res["sql"].strip() else ''
            _valid_starts = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER',
                             'DROP', 'TRUNCATE', 'WITH', 'EXPLAIN']
            if _first_word in _valid_starts:
                _test_results.append(('PASS', 'Geçerli başlangıç', f'{_first_word} ile başlıyor'))
            else:
                _test_results.append(('FAIL', 'Geçersiz başlangıç', f'{_first_word} ile başlıyor (beklenen: SELECT/INSERT/...)'))

            # Test 3: Parantez dengesi
            _open_p = res["sql"].count('(')
            _close_p = res["sql"].count(')')
            if _open_p == _close_p:
                _test_results.append(('PASS', 'Parantez dengesi', f'{_open_p} açık = {_close_p} kapalı'))
            else:
                _test_results.append(('FAIL', 'Parantez dengesizliği', f'{_open_p} açık ≠ {_close_p} kapalı'))

            # Test 4: Tek tırnak dengesi
            _quotes = res["sql"].count("'")
            if _quotes % 2 == 0:
                _test_results.append(('PASS', 'Tırnak dengesi', f'{_quotes} tırnak (çift)'))
            else:
                _test_results.append(('FAIL', 'Tırnak dengesizliği', f'{_quotes} tırnak (tek)'))

            # Test 5: Şema referansı kontrolü
            if schema_text:
                _tables_in_schema = re.findall(r'CREATE\s+TABLE\s+(\w+)', schema_text, re.I)
                _tables_in_sql = re.findall(r'\bFROM\s+(\w+)|\bJOIN\s+(\w+)', res["sql"], re.I)
                _used_tables = set()
                for t1, t2 in _tables_in_sql:
                    _used_tables.add((t1 or t2).lower())
                _missing = [t for t in _used_tables if t not in [s.lower() for s in _tables_in_schema]]
                if not _missing:
                    _test_results.append(('PASS', 'Tablo referansları', f'{len(_used_tables)} tablo şemada mevcut'))
                else:
                    _test_results.append(('WARN', 'Bilinmeyen tablo', f'Şemada bulunmayan: {", ".join(_missing[:3])}'))
            else:
                _test_results.append(('WARN', 'Şema yok', 'Tablo doğrulaması atlanıyor'))

            # Test 6: PostgreSQL EXPLAIN dry-run (PREVIEW_DB varsa)
            _preview_db_url = st.secrets.get('PREVIEW_DB_URL', '')
            if _preview_db_url and dialect.lower() == 'postgresql':
                try:
                    import psycopg2
                    _conn = psycopg2.connect(_preview_db_url)
                    _cur = _conn.cursor()
                    _cur.execute(f"EXPLAIN {res['sql']}")
                    _plan = _cur.fetchall()
                    _conn.close()
                    _test_results.append(('PASS', 'EXPLAIN dry-run', f'{len(_plan)} satır plan başarılı'))
                except Exception as _ex:
                    _test_results.append(('FAIL', 'EXPLAIN hatası', str(_ex)[:100]))
            else:
                _test_results.append(('SKIP', 'EXPLAIN dry-run', 'PREVIEW_DB_URL tanımlı değil'))

            # Sonuçları göster
            _passed = sum(1 for r,_,_ in _test_results if r == 'PASS')
            _failed = sum(1 for r,_,_ in _test_results if r == 'FAIL')
            _warned = sum(1 for r,_,_ in _test_results if r == 'WARN')
            _total = len(_test_results)

            _overall_color = '#0D7F4D' if _failed == 0 else '#B91C1C'
            _overall_bg = '#EDFAF3' if _failed == 0 else '#FEF2F2'
            _overall_text = '✅ TÜM TESTLER GEÇTİ' if _failed == 0 else f'❌ {_failed} TEST BAŞARISIZ'

            st.markdown(
                f"<div style='background:{_overall_bg};border:2px solid {_overall_color};"
                f"border-radius:10px;padding:.8rem 1.2rem;margin-bottom:.7rem'>"
                f"<div style='font-size:1rem;font-weight:700;color:{_overall_color};margin-bottom:.3rem'>"
                f"{_overall_text}</div>"
                f"<div style='font-size:.8rem;color:#374151'>"
                f"{_passed}/{_total} geçti · {_warned} uyarı · {_failed} hata</div>"
                f"</div>", unsafe_allow_html=True)

            # Test detayları
            for _status, _title, _detail in _test_results:
                _icon = {'PASS':'✓', 'FAIL':'✗', 'WARN':'⚠', 'SKIP':'⊘'}.get(_status, '•')
                _color = {'PASS':'#0D7F4D', 'FAIL':'#B91C1C', 'WARN':'#B45309', 'SKIP':'#6B7A90'}.get(_status, '#6B7A90')
                _bg = {'PASS':'#EDFAF3', 'FAIL':'#FEF2F2', 'WARN':'#FFFBEB', 'SKIP':'#F5F7FA'}.get(_status, '#F5F7FA')
                st.markdown(
                    f"<div style='background:{_bg};border:1px solid {_color}55;"
                    f"border-left:3px solid {_color};border-radius:6px;"
                    f"padding:.4rem .8rem;margin-bottom:.25rem'>"
                    f"<span style='font-size:.85rem;font-weight:700;color:{_color}'>{_icon} {_title}</span>"
                    f"<span style='font-size:.75rem;color:#6B7A90;margin-left:.5rem'>· {_detail}</span>"
                    f"</div>", unsafe_allow_html=True)

    # ── COPY + DOWNLOAD ───────────────────────────────────────────────────
    col_code, col_dl = st.columns([4, 1])
    with col_code:
        st.code(res["sql"], language="sql")
    with col_dl:
        st.markdown(dl(res["sql"]), unsafe_allow_html=True)

    # ── SORGU PAYLAŞMA ─────────────────────────────────────────────────────
    with st.expander('🤝  Bu Sorguyu Ekiple Paylaş', expanded=False):
        st.markdown(
            "<div style='background:#F0F4FF;border:1px solid #BFDBFE;"
            "border-left:3px solid #003DA5;border-radius:8px;"
            "padding:.6rem 1rem;margin-bottom:.6rem;font-size:.78rem;color:#374151'>"
            "Bu SQL sorgusu ekip şablonuna eklenir — "
            f"tüm <b>{st.session_state.role}</b> rolündeki kullanıcılar kullanabilir."
            "</div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='display:grid;grid-template-columns:1fr 1fr;gap:.7rem;margin-bottom:.5rem'>"
            "<div><label style='font-size:.72rem;font-weight:700;color:#003DA5;"
            "display:block;margin-bottom:.25rem'>📝 Şablon Adı</label></div>"
            "<div><label style='font-size:.72rem;font-weight:700;color:#003DA5;"
            "display:block;margin-bottom:.25rem'>📂 Kategori</label></div>"
            "</div>", unsafe_allow_html=True)
        _sh_col1, _sh_col2 = st.columns(2)
        with _sh_col1:
            _sh_title = st.text_input('Şablon Adı', key='sh_title',
                placeholder='örn: Gecikmiş Fatura Analizi',
                label_visibility='collapsed')
        with _sh_col2:
            _sh_cat   = st.text_input('Kategori', key='sh_cat',
                value=f'👥 {st.session_state.role.title()}',
                placeholder='📊 Ekibim',
                label_visibility='collapsed')

        st.markdown(
            "<div style='display:grid;grid-template-columns:1fr 1fr;gap:.7rem;margin-bottom:.25rem'>"
            "<div><label style='font-size:.72rem;font-weight:700;color:#003DA5;"
            "display:block'>🎨 İkon</label></div>"
            "<div><label style='font-size:.72rem;font-weight:700;color:#003DA5;"
            "display:block'>🎯 Kime görünsün?</label></div>"
            "</div>", unsafe_allow_html=True)
        _sh_col3, _sh_col4 = st.columns(2)
        with _sh_col3:
            _sh_icon  = st.text_input('İkon', key='sh_icon', value='🤝',
                label_visibility='collapsed')
        with _sh_col4:
            _sh_scope = st.radio('Kime', ['Ekip', 'Kişisel'], key='sh_scope',
                horizontal=True, label_visibility='collapsed')
        if st.button('📤  Paylaş & Şablona Ekle', key='share_sql'):
            if _sh_title.strip():
                _scope_val    = 'team'     if _sh_scope == 'Ekip' else 'personal'
                _team_role_v  = st.session_state.role if _sh_scope == 'Ekip' else None
                _user_id_v    = st.session_state.user_id if _sh_scope == 'Kişisel' else None
                templates_add(
                    _sh_cat, _sh_title.strip(), prompt, _sh_icon,
                    st.session_state.username,
                    scope=_scope_val,
                    user_id=_user_id_v,
                    team_role=_team_role_v
                )
                _msg = f"✅ '{_sh_title}' ekip şablonuna eklendi!" if _sh_scope=='Ekip' \
                       else f"✅ '{_sh_title}' kişisel şablonuna eklendi!"
                st.success(_msg)
                st.rerun()
            else:
                st.warning('Şablon adı boş olamaz.')

    # ── VERİYİ YORUMLA (SQL bazlı) — önizleme yoksa da çalışır ───────────
    _has_explain = bool(st.session_state.get('explain_result', ''))
    with st.expander('📊  Sorguyu Yorumla — SQL Açıklaması', expanded=_has_explain):
        st.markdown(
            "<div style='background:#F0F4FF;border:1px solid #BFDBFE;"
            "border-left:3px solid #003DA5;border-radius:8px;"
            "padding:.5rem .9rem;margin-bottom:.6rem;font-size:.78rem;color:#374151'>"
            "💡 SQL sorgusunun <b>ne yaptığını Türkçe</b> açıklar. "
            "Hangi tabloları birleştiriyor, hangi filtre uyguluyor, "
            "neyi getirmeye çalışıyor — net ve iş odaklı."
            "</div>", unsafe_allow_html=True)
        _exp_col1, _exp_col2 = st.columns([3, 1])
        with _exp_col1:
            _explain_btn = st.button('🔍 SQL\'i Türkçe Açıkla', key='explain_sql', use_container_width=True)
        with _exp_col2:
            if _has_explain:
                if st.button('🗑 Temizle', key='clear_explain', use_container_width=True):
                    st.session_state.explain_result = ''
                    st.rerun()
        if _explain_btn:
            if not api_key:
                st.error('⚠️ OpenAI API key tanımlı değil. Streamlit Cloud → Manage app → Secrets içine OPENAI_API_KEY ekleyin.')
            else:
                with st.spinner('SQL analiz ediliyor — birkaç saniye sürebilir…'):
                    try:
                        _exp_client = openai.OpenAI(api_key=api_key)
                        _exp_r = _exp_client.chat.completions.create(
                            model=model, max_tokens=500,
                            messages=[
                                {'role':'system','content':'Sen Turkcell kıdemli veri analistisin. SQL sorgularını Türkçe net ve iş odaklı açıkla. Madde madde yaz.'},
                                {'role':'user','content':f'Aşağıdaki SQL sorgusunu kısa ve net Türkçe madde madde açıkla. Ne sorguluyor, hangi tabloları birleştiriyor, hangi filtreleri uyguluyor, ne amaç güdüyor. Maksimum 4-5 madde, her madde tek satır.\n\nSQL:\n{res["sql"]}'}
                            ])
                        _exp = _exp_r.choices[0].message.content
                        if not _exp or not _exp.strip():
                            st.warning('OpenAI boş yanıt döndü. Tekrar deneyin.')
                        else:
                            st.session_state.explain_result = _exp
                            st.rerun()
                    except openai.AuthenticationError:
                        st.error('❌ OpenAI API key geçersiz. Streamlit Cloud secrets içinden kontrol edin.')
                    except openai.RateLimitError:
                        st.error('❌ OpenAI rate limit aşıldı. Birkaç saniye sonra tekrar deneyin.')
                    except Exception as _ee:
                        st.error(f'❌ Yorum hatası: {type(_ee).__name__} — {str(_ee)[:200]}')
        # Önceden alınan sonucu göster
        if _has_explain:
            _exp_saved = st.session_state.explain_result
            _items = [ln.lstrip('•-–* ').strip() for ln in _exp_saved.split('\n') if ln.strip()]
            st.markdown(
                "<div style='background:#F0F4FF;border:1px solid #BFDBFE;"
                "border-left:3px solid #003DA5;border-radius:10px;"
                "padding:1rem 1.2rem;margin-top:.6rem'>"
                "<div style='font-size:.7rem;font-weight:700;color:#003DA5;"
                "letter-spacing:1.2px;text-transform:uppercase;margin-bottom:.6rem'>"
                "📊 SQL Açıklaması</div>"
                + ''.join(
                    f"<div style='display:flex;gap:.6rem;margin-bottom:.5rem;"
                    f"padding:.5rem .7rem;background:#fff;border-radius:6px'>"
                    f"<span style='color:#003DA5;font-weight:700;flex-shrink:0'>{idx+1}.</span>"
                    f"<span style='font-size:.85rem;color:#1A202C;line-height:1.5'>{item}</span></div>"
                    for idx, item in enumerate(_items)
                )
                + "</div>", unsafe_allow_html=True)

    # ── SONUÇ ÖNİZLEME ───────────────────────────────────────────────────
    _preview_db = st.secrets.get('PREVIEW_DB_URL', '')
    if _preview_db or st.secrets.get('PREVIEW_DB_TYPE',''):
        with st.expander('▶  Sorgu Sonuçlarını Önizle (ilk 50 satır)', expanded=False):
            if st.button('🔄 Sorguyu Çalıştır', key='run_preview'):
                try:
                    _db_type = st.secrets.get('PREVIEW_DB_TYPE','sqlite')
                    if _db_type == 'sqlite':
                        import sqlite3 as _sqlite
                        _pconn = _sqlite.connect(st.secrets.get('PREVIEW_DB_PATH', DB_PATH))
                        _pdf = __import__('pandas').read_sql_query(
                            res['sql'] + (' LIMIT 50' if 'LIMIT' not in res['sql'].upper() else ''),
                            _pconn)
                        _pconn.close()
                    elif _db_type == 'postgresql':
                        import psycopg2, pandas as _pd
                        _pconn = psycopg2.connect(_preview_db)
                        _pdf = _pd.read_sql_query(
                            res['sql'] + (' LIMIT 50' if 'LIMIT' not in res['sql'].upper() else ''),
                            _pconn)
                        _pconn.close()
                    else:
                        st.warning('Desteklenmeyen DB tipi. PREVIEW_DB_TYPE: sqlite veya postgresql')
                        _pdf = None

                    if _pdf is not None:
                        st.markdown(
                            f'<div style="font-size:.72rem;color:#0D7F4D;font-weight:600;'
                            f'margin-bottom:.4rem">✅ {len(_pdf)} satır döndü</div>',
                            unsafe_allow_html=True)
                        st.dataframe(_pdf, use_container_width=True)
                        # CSV indir
                        _csv = _pdf.to_csv(index=False).encode('utf-8')
                        _csv_b64 = b64lib.b64encode(_csv).decode()
                        _ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                        st.markdown(
                            f'<div class="dl-wrap"><a href="data:file/csv;base64,{_csv_b64}"'
                            f' download="result_{_ts}.csv">📥 CSV İndir</a></div>',
                            unsafe_allow_html=True)

                        # ── OTOMATİK GÖRSELLEŞTİRME ────────────────────────
                        try:
                            import pandas as _pd_viz
                            _num_cols = _pdf.select_dtypes(include='number').columns.tolist()
                            _str_cols = _pdf.select_dtypes(exclude='number').columns.tolist()
                            if len(_num_cols) >= 1 and len(_str_cols) >= 1 and len(_pdf) <= 50:
                                _chart_col = _num_cols[0]
                                _label_col = _str_cols[0]
                                _chart_df  = _pdf[[_label_col, _chart_col]].copy()
                                _chart_df  = _chart_df.set_index(_label_col)
                                st.markdown(
                                    f"<div style='font-size:.65rem;font-weight:700;color:#003DA5;"
                                    f"letter-spacing:1.2px;text-transform:uppercase;"
                                    f"margin:.6rem 0 .3rem'>📊 Otomatik Grafik — {_chart_col}</div>",
                                    unsafe_allow_html=True)
                                # Satır sayısına göre grafik tipi seç
                                if len(_pdf) <= 10:
                                    st.bar_chart(_chart_df, use_container_width=True)
                                else:
                                    st.line_chart(_chart_df, use_container_width=True)
                        except Exception:
                            pass  # grafik başarısız olursa sessizce atla

                        # ── DOĞAL DİL YORUM ─────────────────────────────────
                        if st.button('📊 Veriyi Türkçe Yorumla', key='interpret_data'):
                            _interpret_prompt = (
                                'Aşağıdaki SQL sorgu sonucunu bir iş analistine '
                                'açıklar gibi Türkçe, kısa ve net yorumla.\n'
                                'Önemli trendleri, dikkat çekici değerleri ve '
                                'önerileri madde madde yaz. Maks 5 madde.\n\n'
                                f'Sorgu: {prompt}\n\n'
                                f'Sonuç (ilk 10 satır):\n'
                                + _pdf.head(10).to_string(index=False)
                            )
                            with st.spinner('Veri yorumlanıyor…'):
                                try:
                                    _ic = openai.OpenAI(api_key=api_key)
                                    _ir = _ic.chat.completions.create(
                                        model=model,
                                        max_tokens=600,
                                        messages=[
                                            {'role':'system','content':'Sen Turkcell için çalışan kıdemli bir veri analistisin. Verileri Türkçe, net ve iş odaklı yorumla.'},
                                            {'role':'user','content':_interpret_prompt}
                                        ]
                                    )
                                    _interp = _ir.choices[0].message.content
                                    st.markdown(
                                        "<div style='background:#F0F4FF;border:1px solid #BFDBFE;"
                                        "border-left:3px solid #003DA5;border-radius:10px;"
                                        "padding:.8rem 1.1rem;margin-top:.6rem'>"
                                        "<div style='font-size:.65rem;font-weight:700;color:#003DA5;"
                                        "letter-spacing:1.2px;text-transform:uppercase;margin-bottom:.5rem'>"
                                        "📊 Veri Yorumu</div>"
                                        + ''.join(
                                            f"<div style='display:flex;gap:.5rem;margin-bottom:.35rem'>"
                                            f"<span style='color:#003DA5;flex-shrink:0'>•</span>"
                                            f"<span style='font-size:.82rem;color:#374151'>{ln.lstrip('•-– ').strip()}</span></div>"
                                            for ln in _interp.split('\n') if ln.strip()
                                        )
                                        + "</div>",
                                        unsafe_allow_html=True)
                                except Exception as _iie:
                                    st.error(f'Yorum hatası: {_iie}')
                except Exception as _pe:
                    st.error(f'❌ Sorgu hatası: {_pe}')
    else:
        st.markdown(
            '<div style="background:#F5F7FA;border:1px solid #DCE3ED;border-radius:8px;'
            'padding:.45rem 1rem;margin:.4rem 0;font-size:.74rem;color:#9AA5B4">'
            '💡 Sonuç önizleme için <code>secrets.toml</code> dosyasına '
            '<code>PREVIEW_DB_TYPE</code> ve bağlantı bilgilerini ekleyin.</div>',
            unsafe_allow_html=True)

    # ── REVIEW CARD ──────────────────────────────────────────────────────
    review = res.get("review", {})
    if review:
        status = review.get("status", "SAFE").upper()
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
            '<div class="review-col issues"><div class="review-col-title">Sorunlar</div><ul>'
            + issue_li + '</ul></div>'
            '<div class="review-col notes"><div class="review-col-title">Notlar</div><ul>'
            + notes_li + '</ul></div>'
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

    # ── EXPLANATION ───────────────────────────────────────────────────────
    exp_lines = res.get("explanation", [])
    if exp_lines:
        bullets_rich = ""
        for line in exp_lines:
            if line:
                lower = line.lower()
                is_assumption = any(w in lower for w in
                    ["varsayım", "kabul edildi", "tanım", "assumption",
                     "yorumlandı", "borçlu", "aktif", "hiç ödeme"])
                if is_assumption:
                    bullets_rich += f'<li style="color:var(--b1);font-weight:600;">{line}</li>'
                else:
                    bullets_rich += f"<li>{line}</li>"
        st.markdown(
            '<div class="exp-card"><div class="exp-title">💡 İş Açıklaması & Varsayımlar</div>'
            f'<ul>{bullets_rich}</ul></div>',
            unsafe_allow_html=True)


    # ── SOHBET MODU — devam et ────────────────────────────────────────────────
    st.markdown(
        "<div style='background:#F5F7FA;border:1px solid #DCE3ED;"
        "border-radius:10px;padding:.7rem 1rem;margin:.5rem 0'>"
        "<span style='font-size:.65rem;font-weight:700;color:#6B7A90;"
        "letter-spacing:1.2px;text-transform:uppercase'>💬 Bu Sorguya Devam Et</span>"
        "</div>", unsafe_allow_html=True)
    _chat_col1, _chat_col2 = st.columns([5, 1])
    with _chat_col1:
        _followup = st.text_input(
            'followup', placeholder='Örn: Bunları şehre göre grupla · Sadece platinum olanları getir…',
            key=f'followup_input_{st.session_state.followup_reset}',
            label_visibility='collapsed')
    with _chat_col2:
        st.markdown("<div style='margin-top:.05rem'></div>", unsafe_allow_html=True)
        _followup_go = st.button('➜ Devam', key=f'followup_go_{st.session_state.followup_reset}',
                                 use_container_width=True)
    if _followup_go and _followup.strip():
        _chat_prompt = (
            f'Önceki sorgu: {prompt}\n'
            f'Üretilen SQL:\n{res["sql"]}\n\n'
            f'Devam isteği: {_followup}\n\n'
            f'Yukarıdaki SQL\'i bu isteğe göre güncelle veya genişlet. '
            f'Orijinal iş mantığını koru, sadece istenen değişikliği ekle.'
        )
        st.session_state.chat_history.append({
            'prompt': prompt, 'sql': res['sql'], 'followup': _followup
        })
        # Eski textarea state'ini temizle
        _old_pk = f'pk_{st.session_state.prompt_reset}'
        if _old_pk in st.session_state:
            del st.session_state[_old_pk]
        st.session_state.lp = _chat_prompt
        st.session_state.prompt_reset += 1
        st.session_state.followup_reset += 1
        st.session_state.auto_go = True
        st.rerun()
    # Chat geçmişi göster
    if st.session_state.chat_history:
        with st.expander(f'💬 Sohbet Geçmişi ({len(st.session_state.chat_history)} adım)', expanded=False):
            for _ci, _ch in enumerate(st.session_state.chat_history):
                st.markdown(
                    f"<div style='border-left:3px solid #003DA5;padding:.4rem .8rem;"
                    f"margin-bottom:.4rem;background:#F0F4FF;border-radius:6px'>"
                    f"<div style='font-size:.75rem;font-weight:600;color:#003DA5'>"
                    f"Adım {_ci+1}: {_ch['prompt'][:60]}…</div>"
                    f"<div style='font-size:.7rem;color:#6B7A90;margin-top:.15rem'>"
                    f"↳ {_ch['followup']}</div></div>",
                    unsafe_allow_html=True)
            if st.button('🗑 Sohbeti Temizle', key='clear_chat'):
                st.session_state.chat_history = []
                st.rerun()

    # ── OTOMATİK SORGU İYİLEŞTİRME ──────────────────────────────────────────
    _review_status = res.get('review', {}).get('status', '') if res.get('review') else ''
    # RISKY/INVALID ya da risk skoru düşükse iyileştirme öner
    _show_improve = _review_status in ('RISKY', 'INVALID')
    if _show_improve:
        st.markdown(
            "<div style='background:#FFFBEB;border:1px solid #FDE68A;"
            "border-left:3px solid #D97706;border-radius:10px;"
            "padding:.7rem 1rem;margin:.6rem 0;display:flex;align-items:center;gap:.8rem'>"
            "<span style='font-size:.8rem;color:#92400E'>"
            "⚠️ Bu sorgunun risk skoru yüksek. Sistem daha güvenli bir versiyon üretebilir.</span>",
            unsafe_allow_html=True)
        if st.button('🔄  Daha Güvenli Versiyon Üret', key='improve_sql'):
            _improve_prompt = (
                'Aşağıdaki SQL sorgusunu daha güvenli hale getir.\n'
                'Kurallar:\n'
                '- SELECT * varsa sütunları açıkça yaz\n'
                '- WHERE filtresi eksikse ekle\n'
                '- İç içe SELECT varsa CTE ile yeniden yaz\n'
                '- Orijinal iş mantığını koru\n\n'
                f'Orijinal prompt: {prompt}\n\n'
                f'Mevcut SQL:\n{res["sql"]}'
            )
            with st.spinner('Güvenli versiyon üretiliyor…'):
                try:
                    _imp_res = run_pipeline(
                        _improve_prompt, api_key, dialect, style, model, schema_text, sql_mode
                    )
                    if _imp_res.get('sql'):
                        st.markdown(
                            "<div style='background:#EDFAF3;border:1px solid #A3DFBE;"
                            "border-radius:8px;padding:.5rem 1rem;margin:.4rem 0;"
                            "font-size:.75rem;font-weight:600;color:#0D7F4D'>"
                            "✅ Güvenli versiyon üretildi</div>",
                            unsafe_allow_html=True)
                        st.code(_imp_res['sql'], language='sql')
                        st.markdown(dl(_imp_res['sql']), unsafe_allow_html=True)
                        render_risk_score(_imp_res['sql'])
                except Exception as _ie:
                    st.error(f'İyileştirme hatası: {_ie}')

# ══════════════════════════════════════════════════════════════════════════
#  HISTORY — DB'den kullanıcı bazlı
# ══════════════════════════════════════════════════════════════════════════
_db_history = db_get_history(st.session_state.user_id, limit=50)
_hist_count = len(_db_history)

st.markdown('<div class="pdiv"></div>', unsafe_allow_html=True)
with st.expander(f"📜  Sorgu Geçmişi  ({_hist_count} kayıt)", expanded=False):
    if not _db_history:
        st.info("Henüz sorgu geçmişi yok.")
    else:
        # Arama kutusu
        _search = st.text_input("🔍 Geçmişte ara", placeholder="prompt veya SQL ara...",
                                 key="hist_search", label_visibility="collapsed")
        _filtered = [e for e in _db_history
                     if not _search or _search.lower() in e["prompt"].lower()
                     or _search.lower() in (e.get("sql_out") or "").lower()]

        st.caption(f"{len(_filtered)} sonuç gösteriliyor")

        for i, e in enumerate(_filtered):
            tag       = f" · 🗄 {e['schema_name']}" if e.get("schema_name") else ""
            risk_col  = {"SAFE":"#0D7F4D","RISKY":"#B45309","INVALID":"#B91C1C"}.get(
                e.get("risk_level",""), "#9AA5B4")
            risk_lbl  = e.get("risk_level","") or ""
            kvkk_flag = " · 🔏" if e.get("kvkk_hit") else ""

            st.markdown(
                f'<div class="hi">'
                f'<div class="hp">{e["prompt"]}</div>'
                f'<div class="hm">'
                f'{e["created_at"][:16]} · {e.get("dialect","")}{tag}'
                f' · <span style="color:{risk_col};font-weight:600">{risk_lbl}</span>'
                f'{kvkk_flag} · {e.get("tokens",0)} tok'
                f'</div></div>',
                unsafe_allow_html=True)

            if e.get("sql_out"):
                st.code(e["sql_out"], language="sql")
                st.markdown(dl(e["sql_out"]), unsafe_allow_html=True)

            if i < len(_filtered) - 1:
                st.markdown('<div style="height:.1rem"></div>', unsafe_allow_html=True)

        st.markdown('<div style="height:.2rem"></div>', unsafe_allow_html=True)
        if st.button("🗑  Oturum Geçmişini Temizle", key="clr"):
            st.session_state.update({"history": [], "qc": 0, "tt": 0})
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════
#  ŞİFRE DEĞİŞTİRME — kullanıcı kendi şifresini değiştirebilir
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="pdiv"></div>', unsafe_allow_html=True)
with st.expander("🔑  Şifremi Değiştir", expanded=False):
    st.markdown(
        "<div style='background:#F0F4FF;border:1px solid #BFDBFE;"
        "border-radius:10px;padding:1rem 1.2rem;margin-bottom:.5rem'>"
        "<p style='font-size:.75rem;color:#003DA5;margin:0 0 .6rem;font-weight:600'>"
        "Mevcut şifrenizi girin ve yeni şifrenizi belirleyin.</p></div>",
        unsafe_allow_html=True)
    _pw_col1, _pw_col2 = st.columns(2)
    with _pw_col1:
        _cur_pw  = st.text_input("Mevcut Şifre", type="password", key="cur_pw")
        _new_pw  = st.text_input("Yeni Şifre", type="password", key="new_pw",
                                  placeholder="min 6 karakter")
    with _pw_col2:
        _new_pw2 = st.text_input("Yeni Şifre (tekrar)", type="password", key="new_pw2")
        st.markdown("<div style='margin-top:1.7rem'></div>", unsafe_allow_html=True)
        if st.button("🔑 Şifremi Güncelle", key="change_pw"):
            if not _cur_pw or not _new_pw or not _new_pw2:
                st.warning("Tüm alanları doldurun.")
            elif _new_pw != _new_pw2:
                st.error("❌ Yeni şifreler eşleşmiyor.")
            elif len(_new_pw) < 6:
                st.error("❌ Şifre en az 6 karakter olmalı.")
            else:
                _user_check = db_login(st.session_state.username, _cur_pw)
                if not _user_check:
                    st.error("❌ Mevcut şifre hatalı.")
                else:
                    db_change_password(st.session_state.user_id, _new_pw)
                    st.success("✅ Şifreniz güncellendi!")

# ══════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="foot">'
    '<p>© 2026 <strong>turkcell.sql.ai.com.tr</strong> | TURKCELL SQL AI | L2 DevOps Operations | Powered by OpenAI</p>'
    '<p>Global Bilgi · Streamlit · Tüm hakları saklıdır.</p>'
    '</div>',
    unsafe_allow_html=True)