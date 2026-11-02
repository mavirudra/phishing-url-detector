import base64
import streamlit as st
import joblib
import pandas as pd
from features import features

GITHUB = "https://github.com/mavirudra"

st.set_page_config(page_title="Phishing URL Detector", page_icon="🛡️")

LIGHT = {
    "bg": "#FAFAF8", "bg-alt": "#F2F1EB", "ink": "#14181F", "ink-soft": "#454C57",
    "muted": "#6B7280", "accent": "#2D6A4F", "line": "#E5E3DD",
    "term": "#14181F", "term-text": "#D7E4DC", "term-hint": "#7FBFA1",
    "bad": "#B3382C", "bad-soft": "#F7E9E6",
}
DARK = {
    "bg": "#0F1318", "bg-alt": "#171C23", "ink": "#ECEBE4", "ink-soft": "#B3B9C2",
    "muted": "#8A919C", "accent": "#7FBFA1", "line": "#2A313B",
    "term": "#0A0D11", "term-text": "#D7E4DC", "term-hint": "#7FBFA1",
    "bad": "#E5675A", "bad-soft": "#2B1B19",
}

if "dark" not in st.session_state:
    st.session_state.dark = False

def toggle_theme():
    st.session_state.dark = not st.session_state.dark

theme = DARK if st.session_state.dark else LIGHT
root = ":root{" + ";".join(f"--{k}:{v}" for k, v in theme.items()) + "}"
st.markdown(f"<style>{root}</style>", unsafe_allow_html=True)


# ---------- moon / sun pill toggle (fixed to top-right) ----------
def icon(kind, color):
    if kind == "moon":
        body = f'<path fill="{color}" d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>'
    else:
        body = (
            f'<circle cx="12" cy="12" r="4.5" fill="{color}"/>'
            f'<g stroke="{color}" stroke-width="2" stroke-linecap="round">'
            '<path d="M12 1.5V4M12 20v2.5M1.5 12H4M20 12h2.5M4.58 4.58l1.76 1.76'
            'M17.66 17.66l1.76 1.76M4.58 19.42l1.76-1.76M17.66 6.34l1.76-1.76"/></g>'
        )
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{body}</svg>'
    return 'url("data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode() + '")'

if st.session_state.dark:
    active, inactive, a_side, i_side = "moon", "sun", "left", "right"
else:
    active, inactive, a_side, i_side = "sun", "moon", "right", "left"

TOGGLE_CSS = """
<style>
.st-key-theme_btn { position: fixed; top: 14px; right: 18px; z-index: 1000;
                    width: auto !important; }
.st-key-theme_btn .stButton > button,
.st-key-theme_btn .stButton > button:hover,
.st-key-theme_btn .stButton > button:focus,
.st-key-theme_btn .stButton > button:active {
    position: relative; width: 76px; min-width: 0; height: 38px; min-height: 0; padding: 0;
    background: __PILL__; border: 1px solid __LINE__; border-radius: 10px;
    box-shadow: none; outline: none; cursor: pointer;
}
.st-key-theme_btn .stButton > button p,
.st-key-theme_btn .stButton > button span { display: none; }
.st-key-theme_btn .stButton > button::before {
    content: ""; position: absolute; top: 3px; __A_SIDE__: 3px; width: 34px; height: 30px;
    border-radius: 7px; background-color: __KNOB__; background-image: __A_ICON__;
    background-repeat: no-repeat; background-position: center; background-size: 18px;
}
.st-key-theme_btn .stButton > button::after {
    content: ""; position: absolute; top: 3px; __I_SIDE__: 3px; width: 34px; height: 30px;
    background-image: __I_ICON__; background-repeat: no-repeat;
    background-position: center; background-size: 18px;
}
</style>
"""
st.markdown(
    TOGGLE_CSS.replace("__PILL__", theme["bg-alt"]).replace("__LINE__", theme["line"])
    .replace("__KNOB__", theme["accent"])
    .replace("__A_SIDE__", a_side).replace("__I_SIDE__", i_side)
    .replace("__A_ICON__", icon(active, theme["bg"]))
    .replace("__I_ICON__", icon(inactive, theme["muted"])),
    unsafe_allow_html=True,
)


# ---------- typing hint inside the input box (CSS only) ----------
def hint_keyframes(phrases, hold=14, gap=4, ms=85):
    frames = []
    for p in phrases:
        frames += [p[:i] for i in range(1, len(p) + 1)]       # type
        frames += [p] * hold                                  # pause
        frames += [p[:i] for i in range(len(p) - 1, -1, -1)]  # backspace
        frames += [""] * gap
    n = len(frames)
    stops = "".join(f'{i * 100 / n:.3f}%{{content:"{t}|"}}' for i, t in enumerate(frames))
    stops += f'100%{{content:"{frames[0]}|"}}'
    return stops, n * ms / 1000

stops, duration = hint_keyframes(["Hello..!", "Please paste a URL here"])
st.markdown(
    "<style>@keyframes hint{" + stops + "}"
    ".st-key-urlbox::before{animation:hint " + f"{duration:.2f}" + "s step-end infinite;}</style>",
    unsafe_allow_html=True,
)


# ---------- page styles ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

.stApp { background: var(--bg); color: var(--ink); font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 720px; padding-top: 2rem; }

/* hero */
.eyebrow { font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: var(--accent);
           display: flex; align-items: center; gap: 8px; margin-top: 3rem; }
.dot { width: 7px; height: 7px; border-radius: 50%; background: var(--accent);
       display: inline-block; }
.stApp h1.title { font-family: 'Fraunces', serif; font-weight: 600; color: var(--ink);
                  font-size: clamp(38px, 7vw, 56px); line-height: 1.05;
                  letter-spacing: -0.01em; margin: 0; padding: 0; }
.sub { color: var(--ink-soft); font-size: 17px; margin: 0 0 1rem; }

/* terminal-style input */
.stTextInput div[data-baseweb="input"] { background: var(--term); border: 1px solid var(--term);
                                         border-radius: 3px; }
.stTextInput div[data-baseweb="input"]:focus-within { border-color: var(--accent); }
.stTextInput input { background: var(--term); color: var(--term-text); caret-color: var(--accent);
                     font-family: 'IBM Plex Mono', monospace; font-size: 14px; padding: 0.8rem; }

/* typing hint overlay: hidden once the box is clicked or has text */
.st-key-urlbox { position: relative; }
.st-key-urlbox::before {
    content: "|"; position: absolute; left: calc(0.8rem + 2px); top: 50%;
    transform: translateY(-50%); z-index: 2; pointer-events: none;
    font-family: 'IBM Plex Mono', monospace; font-size: 14px; color: var(--term-hint);
}
.st-key-urlbox:focus-within::before { display: none; }
.st-key-urlbox:has(input:not(:placeholder-shown))::before { display: none; }

/* check button */
.st-key-check .stButton > button { background: var(--ink); border: 1px solid var(--ink);
                                   border-radius: 3px; padding: 0.55rem 1.4rem; }
.st-key-check .stButton > button p { font-family: 'IBM Plex Mono', monospace; font-size: 13px;
                                     color: var(--bg); }
.st-key-check .stButton > button:hover { background: var(--accent); border-color: var(--accent); }

/* result */
.stApp div.result { background: var(--bg-alt); border: 1px solid var(--line);
                    border-left: 3px solid var(--accent); border-radius: 3px;
                    padding: 18px 20px; margin-top: 12px; }
.stApp div.result.bad { background: var(--bad-soft); border-left-color: var(--bad); }
.result .label { font-family: 'IBM Plex Mono', monospace; font-size: 12px;
                 letter-spacing: 0.05em; color: var(--muted); }
.stApp div.result h2 { font-family: 'Fraunces', serif; font-weight: 500; font-size: 28px;
                       color: var(--ink); margin: 6px 0 14px; padding: 0; }
.track { height: 4px; background: var(--line); border-radius: 2px; }
.fill { height: 100%; border-radius: 2px; background: var(--accent); }
.bad .fill { background: var(--bad); }

/* footer */
.foot { margin-top: 4rem; padding-top: 1.2rem; border-top: 1px solid var(--line); }
div.foot a { display: inline-flex; align-items: center; gap: 8px; text-decoration: none;
             font-family: 'IBM Plex Mono', monospace; font-size: 13px;
             color: var(--ink-soft) !important; }
div.foot a:hover { color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

st.button("Toggle theme", key="theme_btn", on_click=toggle_theme)

st.markdown('<div class="eyebrow"><span class="dot"></span>PHISHING URL DETECTOR</div>',
            unsafe_allow_html=True)
st.markdown('<h1 class="title">Is this link safe?</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub">Paste a URL and a Random Forest model scores it '
            'from the structure of the link alone.</p>', unsafe_allow_html=True)

url = st.text_input("URL", key="urlbox", placeholder=" ",
                    label_visibility="collapsed").strip()
st.button("Check URL", key="check")

if url:
    prob = model.predict_proba(pd.DataFrame([features(url)]))[0][1]
    cls, verdict = ("bad", "Likely phishing") if prob > 0.5 else ("good", "Looks legit")
    st.markdown(
        f'<div class="result {cls}">'
        f'<div class="label">VERDICT · {prob:.0%} PHISHING PROBABILITY</div>'
        f'<h2>{verdict}</h2>'
        f'<div class="track"><div class="fill" style="width:{prob*100:.0f}%"></div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown(f"""
<div class="foot"><a href="{GITHUB}" target="_blank" rel="noopener">
<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
GitHub</a></div>
""", unsafe_allow_html=True)