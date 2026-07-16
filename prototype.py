import streamlit as st
import json, random, re, os, base64
from collections import defaultdict
from PIL import Image
import io

st.set_page_config(page_title="Find the Right Fit — Tynor", page_icon="🦴", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    /* Force Poppins + text color everywhere — light AND dark mode */
    html, body, [class*="css"], [class*="st-"], button, input, label,
    p, span, div, h1, h2, h3, h4, h5, h6, .stMarkdown, .stText {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Global text visibility fix — light mode */
    .stMarkdown p, .stMarkdown li, .stMarkdown span,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stText"] p,
    .stCaption p, .element-container p,
    .stTextInput label p, .stSelectbox label p {
        color: #2b1830 !important;
    }

    /* Alert/warning text */
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] div,
    .stAlert p, .stAlert span { color: #1a0a20 !important; font-weight: 500 !important; }

    /* Product card text */
    [data-testid="stVerticalBlockBorderWrapper"] p,
    [data-testid="stVerticalBlockBorderWrapper"] span,
    [data-testid="stVerticalBlockBorderWrapper"] li { color: #2b1830 !important; }

    /* Fix ALL checkbox text — aggressive global selector */
    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] label span,
    [data-testid="stCheckbox"] label p,
    [data-testid="stCheckbox"] p,
    [data-testid="stCheckbox"] span,
    .stCheckbox label,
    .stCheckbox label span,
    .stCheckbox span {
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }

    /* Fix ALL radio text — aggressive global selector */
    [data-testid="stRadio"] label,
    [data-testid="stRadio"] label span,
    [data-testid="stRadio"] label p,
    [data-testid="stRadio"] p,
    [data-testid="stRadio"] span,
    .stRadio label,
    .stRadio label span,
    .stRadio span {
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }

    /* App background */
    .stApp { background: linear-gradient(180deg, #fbf7fc 0%, #ffffff 100%); }

    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #9B3DAE, #7B2D8B);
        border-radius: 10px;
    }
    .stProgress > div > div { border-radius: 10px; background: #f0e3f5; }

    /* Step summary breadcrumb pill */
    .step-summary {
        background: #ffffff;
        border: 1.5px solid #ecd9f2;
        box-shadow: 0 2px 10px rgba(123,45,139,0.06);
        padding: 10px 16px; border-radius: 999px;
        font-size: 0.82rem; color: #555; margin-bottom: 18px;
        display: inline-block;
    }

    /* Headings */
    h2, h3 { color: #2b1830 !important; font-weight: 700 !important; }
    .stCaption, [data-testid="stCaptionContainer"] { color: #8a7a90 !important; }

    /* Primary buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #dda0e8 0%, #c070d0 60%, #a854bc 100%) !important;
        border: none !important; color: white !important;
        border-radius: 16px !important; font-weight: 800 !important; font-family: 'Poppins', sans-serif !important;
        padding: 0.7rem 1.6rem !important; font-size: 0.97rem !important;
        letter-spacing: 0.2px;
        box-shadow: 0 4px 18px rgba(123,45,139,0.35), inset 0 1px 0 rgba(255,255,255,0.15) !important;
        transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 8px 24px rgba(123,45,139,0.45), inset 0 1px 0 rgba(255,255,255,0.2) !important;
        background: linear-gradient(135deg, #e8b5f0 0%, #d080dc 60%, #b866c8 100%) !important;
    }
    .stButton > button[kind="primary"]:active {
        transform: scale(0.97) translateY(0) !important;
        box-shadow: 0 2px 8px rgba(123,45,139,0.3) !important;
    }

    /* Secondary / Back buttons */
    .stButton > button:not([kind="primary"]) {
        border-radius: 14px !important;
        border: 1.5px solid #e8d8ee !important;
        background: white !important;
        color: #5a3d63 !important;
        font-weight: 700 !important;
        font-family: 'Poppins', sans-serif !important;
        padding: 0.65rem 1.2rem !important;
        transition: all 0.18s ease !important;
    }
    .stButton > button:not([kind="primary"]):hover {
        border-color: #9B3DAE !important;
        background: #fbf3fc !important;
        transform: translateY(-1px);
    }

    /* Region selector buttons — card style */
    section[data-testid="stVerticalBlock"] .stButton > button:not([kind="primary"]) {
        background: white !important;
        border: 1.5px solid #ecd9f2 !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(123,45,139,0.06) !important;
        transition: all 0.18s ease !important;
    }
    section[data-testid="stVerticalBlock"] .stButton > button:not([kind="primary"]):hover {
        border-color: #9B3DAE !important;
        background: linear-gradient(135deg, #fdf5fe, #faecfc) !important;
        color: #7B2D8B !important;
        box-shadow: 0 6px 16px rgba(123,45,139,0.18) !important;
        transform: translateY(-2px);
    }

    /* Radio buttons — playful cards */
    .stRadio > div { gap: 10px; }
    .stRadio > div > label {
        background: white;
        border: 1.5px solid #ecd9f2;
        border-radius: 14px;
        padding: 12px 16px !important;
        cursor: pointer;
        width: 100%;
        box-shadow: 0 1px 6px rgba(123,45,139,0.05);
        transition: all 0.16s ease;
        display: flex !important;
        align-items: center !important;
    }
    .stRadio > div > label p,
    .stRadio > div > label span,
    .stRadio > div > label div {
        color: #2b1830 !important;
        font-size: 0.97rem !important;
        font-weight: 500 !important;
    }
    .stRadio > div > label:hover {
        border-color: #c388d4;
        background: #fdf6fe;
        transform: translateX(2px);
    }
    .stRadio > div > label:hover p,
    .stRadio > div > label:hover span { color: #7B2D8B !important; }
    .stRadio > div > label[data-checked="true"] {
        border-color: #9B3DAE !important;
        background: linear-gradient(135deg, #fbeefd, #f6e3fa) !important;
    }
    .stRadio > div > label[data-checked="true"] p,
    .stRadio > div > label[data-checked="true"] span { color: #7B2D8B !important; font-weight: 600 !important; }

    /* Checkboxes */
    .stCheckbox > label {
        background: white;
        border: 1.5px solid #ecd9f2;
        border-radius: 12px;
        padding: 10px 14px !important;
        margin-bottom: 6px;
        transition: all 0.16s ease;
        display: flex !important;
        align-items: center !important;
        gap: 8px;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    [data-testid="stCheckbox"] { width: 100% !important; }
    .stCheckbox > label p,
    .stCheckbox > label span,
    .stCheckbox > label div { color: #2b1830 !important; font-size: 0.95rem !important; font-weight: 500 !important; }
    .stCheckbox > label:hover { border-color: #c388d4; background: #fdf6fe; }
    .stCheckbox > label:hover p,
    .stCheckbox > label:hover span { color: #7B2D8B !important; }

    /* Text inputs */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1.5px solid #ecd9f2 !important;
        padding: 10px 14px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #9B3DAE !important;
        box-shadow: 0 0 0 3px rgba(155,61,174,0.12) !important;
    }

    /* Product card container */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        border: 1.5px solid #f0e0f5 !important;
        box-shadow: 0 6px 20px rgba(123,45,139,0.08) !important;
        background: white !important;
        padding: 4px;
    }

    /* Divider */
    hr { border-color: #f0e0f5 !important; margin: 1.4rem 0 !important; }

    /* Expander */
    .streamlit-expanderHeader, [data-testid="stExpander"] summary {
        background: #fdf6fe !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        border: 1px solid #f0e0f5 !important;
    }
    [data-testid="stExpander"] { border-radius: 12px !important; }
    /* Fix _arrowWright overlap in light mode too */
    [data-testid="stExpander"] summary { display: flex; align-items: center; gap: 4px; }
    [data-testid="stExpander"] summary > div:first-child { flex-shrink: 0; }

    /* Warning / Error / Success boxes — softer, rounder */
    .stAlert {
        border-radius: 14px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04) !important;
    }
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] div,
    .stAlert p, .stAlert span, .stAlert div {
        color: #2b1830 !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.97rem !important;
        line-height: 1.6 !important;
    }

    /* Slider */
    .stSlider [data-baseweb="slider"] > div > div { background: #9B3DAE !important; }

    /* Page padding */
    .block-container { padding-top: 2.5rem !important; padding-bottom: 3rem !important; max-width: 780px !important; }

    /* Subtle fade-in animation */
    .main .block-container { animation: fadeIn 0.25s ease; }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Background blobs */
    .stApp::before, .stApp::after {
        content: "";
        position: fixed;
        border-radius: 50%;
        filter: blur(60px);
        z-index: -1;
        opacity: 0.35;
    }
    .stApp::before {
        width: 380px; height: 380px;
        background: radial-gradient(circle, #e8b8f0, transparent 70%);
        top: -120px; right: -100px;
    }
    .stApp::after {
        width: 320px; height: 320px;
        background: radial-gradient(circle, #d4a3e8, transparent 70%);
        bottom: -100px; left: -100px;
    }

    /* Button click bounce */
    .stButton > button { transition: all 0.15s cubic-bezier(0.34, 1.56, 0.64, 1) !important; }
    .stButton > button:active { transform: scale(0.96) !important; }

    /* Badge pills for product cards */
    .product-badge {
        display: inline-block;
        background: linear-gradient(135deg, #ff9a56, #ff6b6b);
        color: white; font-size: 0.72rem; font-weight: 700;
        padding: 3px 10px; border-radius: 999px;
        margin-bottom: 6px; letter-spacing: 0.3px;
    }
    .product-badge.top-rated {
        background: linear-gradient(135deg, #9B3DAE, #6a2578);
    }

    /* Step tracker dots */
    .step-tracker {
        display: flex; align-items: center; justify-content: center;
        gap: 6px; margin-bottom: 16px;
    }
    .step-dot {
        width: 9px; height: 9px; border-radius: 50%;
        background: #ecd9f2; transition: all 0.3s ease;
    }
    .step-dot.done { background: linear-gradient(135deg, #9B3DAE, #6a2578); width: 9px; }
    .step-dot.current {
        background: #9B3DAE; width: 22px; border-radius: 5px;
    }

    /* Skeleton shimmer for loading states */
    .skeleton {
        background: linear-gradient(90deg, #f3e6f7 25%, #faf0fb 50%, #f3e6f7 75%);
        background-size: 200% 100%;
        animation: shimmer 1.4s infinite;
        border-radius: 12px;
        height: 18px; margin-bottom: 10px;
    }
    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
</style>
""", unsafe_allow_html=True)

# ── Body map ─────────────────────────────────────────────────────────────────
BODY_MAP_B64 = "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"

# Region zones: (x_min%, y_min%, x_max%, y_max%) as % of image dimensions
# Mapped from the dot positions on the running figure
BODY_MAP_ZONES = {
    "Neck":      (32, 12, 46, 22),
    "Shoulder":  (26, 20, 44, 32),
    "Elbow":     (14, 26, 26, 38),
    "Wrist":     (14, 36, 26, 48),
    "Finger":    (14, 44, 24, 56),
    "Chest":     (34, 28, 48, 40),
    "Back":      (24, 28, 36, 48),
    "Abdominal": (30, 40, 46, 54),
    "Thigh":     (20, 54, 34, 67),
    "Knee":      (38, 52, 50, 63),
    "Calf":      (8,  63, 20, 76),
    "Ankle":     (38, 72, 50, 86),
}

BODY_MAP_DOTS = {
    "Neck":      (38, 16),
    "Shoulder":  (34, 24),
    "Elbow":     (22, 30),
    "Wrist":     (21, 40),
    "Finger":    (20, 48),
    "Chest":     (42, 32),
    "Back":      (32, 36),
    "Abdominal": (40, 45),
    "Thigh":     (30, 58),
    "Knee":      (45, 55),
    "Calf":      (17, 67),
    "Ankle":     (46, 77),
}

def get_region_from_coords(x, y, img_w, img_h):
    x_pct = (x / img_w) * 100
    y_pct = (y / img_h) * 100
    best = None
    best_dist = float('inf')
    for region, (cx, cy) in BODY_MAP_DOTS.items():
        dist = ((x_pct - cx)**2 + (y_pct - cy)**2) ** 0.5
        if dist < best_dist and dist < 18:  # generous radius  # within 12% radius for easier clicking
            best_dist = dist
            best = region
    return best

# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, 'catalog.json'))  as f: catalog  = json.load(f)
    with open(os.path.join(base, 'problems.json')) as f: problems = json.load(f)
    return catalog, problems

catalog, problems = load_data()

# ── Logo ────────────────────────────────────────────────────────────────────
TYNOR_LOGO_B64 = "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dGyUiG6//fbEeny6pzXiwMDAoz//uTEmHh8fNwGPsZybaTRhHmDRwoUmQHjk5z9fs2YNAGRZNqNnm8y10pzHAPBnf/pnBkrt9/vjY2PhBnQ/IYAPi88M3Zgdt5ERInriiScuuugie/vN8CFnsWZ8XHf2WWeZ0Hpk5NDY6Ki5kJM70Pw7D3zGXTj6G7/xG9O8weIFhgBw3HHHbdy48ZWvfCUwUHSak2KYbvfee4/WenRkZHx8TISayxRKx3/PH2IMbHN1rFlz3JVXXmkAg5kuNdIaETdv2nTfffdlWeZtrJMqOidvEFkf2DvvvNOcajPd9prolRdeeOppp/lnxnb3zuke/1KKffv3P/vsL17csuXNb3rT5s2bsyyrm0bUMynbUny9SCl/7/f+2+233y6lVIZviZMTD1P6FAJAXVdDw8O33HLLZZdddtddd5lyy0wfchaDY5DqPMt+9sgjl1122ef/598OD8+JvYHjTmxpxSURns5sjgy6tmnTptdefPF9991nwPMZrBYpieiSSy5Zv/7CiYkJW74KrJvZLpqXZWQ9nmxC0xtuuAF4E8bJ911zqZldcdddd6E1/GxWCImzUARinudlWf7w1luhVSF2mNibAOC6664TQjinKTySTejiQfrsZ//qDW94w9atW7NM1m285CMacKKqrj/ykY8cPHAgy3Ov3EG26YLLGmMYmb+vlBoenvNP//RPb3nLW3bu3CmlNDnS/7UFU9W1lHJ8fPzXPvyR//7fPzE4OAiISulmFWqy0po5Lmm2N85Lu3ZhW/35MJcEEQDceOOvCiG0694hAq/53yN4mPlfEChI60svvfTsc87RWgsppp34RO95991393t9y5dtqxCaFEJrUlrlRb5p06YnNmyYehO2mpEopZcsWfKmN73ZUSK0Kdmb6sXsBs2cRDfffPOGJ54QAutavexTo7SWUj799NP/8MUv5nlu00DiVunMLgeAO/kqrYeGh//py/9044031qr2p8//5R9Dssmk/OQn/8dv/MZvFHke3dnQyu0Lq1ITHcm6P+wObBovmDr26aeddvnlr5+YmBBC2v4zZVmW/X5VVpULJPCIdx1OsWrbwrmiKEjrfln2+2VVVxMTE91u94Zfvn52G9m8xROPP75ly5Zut1tWpmVg+On3ekTU6XSKPC+KQkopUPz0pz8dGRmRUszoODen6dVvvnrZ8mUTExNVWQJg0e0YM/KOdbKb2VlL7MuFEFr/e10vphD613/9ub1793S7XSlllud5nhd5XuRFludlWYaB6/eNWVhdVcPDw7fccvMHfvUDWmuB4rDo3b/fjyZSWmdZ9rnPfe4zn/nM0NDQxESvLPv9fr8qy6qqqrLs9/pA1Ol0cvdjHAYFHpE86LDrhCbZt++/8ca5c+cKxE6nUxRFnufCNcPUWimAWaJYyS+mmTyZPyE8xAmIqq7f+ra3Ll68mFNVZpJTyZHR0bvvvstkKaqO0E7laF8G+zYb5vs/+P5M9zy6FPSad72TQs82zKRtJiVsyo6zixSmg04f0SbUWiA+//wLt9/+I4NImaKCNLsf0ZevyE2PUqo7MLBx48YbbnhvVVWGGwn/f/0xWaKU8vc+8Ynv3XLz0NBQv983aKMpDSutANHItcyBGzXnY2DY7JLt6d+cSqmlS5Zcc801RJQXnVCR8jJhFOLfJyadBgzNjFbNBd3r94855pi3v/3ts0AXQ+n81lv9fcL9erwWwZjqSin379t33z33+tLCdIdVCE106qmnvvLCV5bGEZRFPq2HJc52Ov89JoYATDOcW3/wA3BcGd77BhsmHUKIXr/3oQ9+cO/evUbt/bLDCDirJWRg3g984EObN20eGBiE2CqsrWRhk4VJO8/MdswnA6XNMn73e96zYsUKPm5EJMLCxNkDCXhkmxAifwGvANDve9/7Op2OIUxO51dzI2cAuPuuu3fu3FkUhe/HAs2mbkAA8NDDD7+4ZYuRac4gFkUEgKuvvnp4zpyqrkJTl3Y/myOCnY8wJEWcLPkkIrrzrrsOHTxklaxoCVp+eqxsEEgrNTAw8JlPf+bue+7JpHQ+67PPqTyVhJejZvd9Bu/dtn3bf/2v/8XS4ieRYU1/2dLLMVP+ONNaDwwMvO9972tbSCHAne4WxJd3iRhpeIwECCF6vYnzz7/gVa96FRGJRikG2wwVOQovhNi+Y/vdd9+dZZlSmpyzG2vlHY7A226/bZoVEZ73KqW63e7b3/52rTUKGVpqMcHTy3VyHeGp3Pog5NxiAiiliePHZk+SU0h3BwZ+9rOfferP/kwIoY4gCjV7zxfiXbcSalLVZvTiJij91//zf771rW8ODAwYNKthpP1/s/qWJlyXXnLpGWeckZTBvMrc0sU5vy8Q/aboQTe9A09O+eM2WCLURK21lMLXKpog/mGvKUS85ZZbIOn8zto+kgYpZVmWP7r9R9NJtfnrCykJ4DWvfvXpZ5zR6/UkRl2raBq5O81kp1E8mJlnV+IRneWIgAK11lu3bvFPQFoTacOVEa6EbC6rP/of/2N0bGw60Pxk75VJafZenufr1q698sorr7j88tWrV5ld5BUJs9w0RADw6U99ut/rGdoAGgWZnxjgPY5pegt49kvddP/26uRfvv56aGu7nXnoVkg5PjHu27m8vHnzFB+YmBjP89x1UCNmwCWVUldfffUxxxzzwgsv2E5PM8DNNBHdeeede/bsmTdvnrUhYlOFiAQaUfziF7/YuHHjNGeFqRAJAK5797szKSeUwkwajRowtTy2Nv6a4bZ0RS00B1MymEIIApp1gY4IzD7e+OST9iYUzprcauMRAZTSA4OD99xz93e++13jfDmLCM1cSrVSZ5xxxntvuOHi11587LFrFi5cWNf1rl0vbd60+bbbb7/py19+btOmmc41r7sIIe7/yU++e/PN73jHO8bGxzMhCDSCBMYJid31X5670VRKm0sdEbM801qfcMIJV111JQBI4ZsI2dM6MwePabR0443v/9a3vj04OEAEWimlVbfTfXLjk88++xw//CZV6DWOECIYHh5ef8EFRZELIc0wWfMFQCllXVfnnXf+UUcdpZTyhjnepaosywULFlxzzTWf+cxnppmvYiCsEgqxefPmBx988KqrrrIkPeduZIJJpVQhizvvuGNsbEy6JGda16AQWumVK1ddffXVxqTcbwpwGjkJULe5ws1i+bpFSatWrjzllFPOPuecoaGhhx9++JFHHnn++edhyprVFLkR//MtW7YAgFI1ililbtJCgYj4xS9+qaoqKeUs9oe5SLXWH/vYxz/xid8bHBwEgLqqer0eAS1ZsnTFipWvevWrf+3DH/7t3/6tr37lq9OcjtZfBABf+MIX3vH2d1i+OwgdbgKjblMyk4CHD6lwepvUVEqHh4Zf9apXnn322ceuWbN169ZHHnlk48Ynn3tuk7kA3nXNNXPnzi3LUkpJOu7WZuMybanP/kdrZfj7/+9nPgMzJMhxOOjVr341xT9KKaUqU9E2P4bhSQmDmajX66m6fujBB7vd7vSppMgOJwD43Y//roHO7Hc77ujYqNE66Le//W0zfUHz4Y98+CNEVJUVWZ8U7ZU+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"

def show_header():
    # Dark mode init
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    # Add top padding so header doesn't clip under browser bar
    st.markdown("<div style='padding-top:16px;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.markdown(
            f'<div style="padding-top:8px;background:white;border-radius:8px;padding:6px 10px;display:inline-block;"><img src="data:image/png;base64,{TYNOR_LOGO_B64}" style="max-height:40px; width:auto; max-width:110px; object-fit:contain;"></div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown("<div style='padding-top:4px;'><span style='font-size:1.6rem;font-weight:800;font-family:Poppins,sans-serif;'>Find the Right Fit</span></div>", unsafe_allow_html=True)
        st.caption("Personalised support recommendation by Tynor")
    with col3:
        st.markdown("<div style='padding-top:6px;'></div>", unsafe_allow_html=True)
        icon = "🌙" if not st.session_state.dark_mode else "☀️"
        label = f"{icon} {'Dark' if not st.session_state.dark_mode else 'Light'}"
        if st.button(label, key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # Inject dark/light CSS dynamically
    if st.session_state.dark_mode:
        st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #1a0d1e 0%, #120a15 100%) !important; }
    .stApp::before { opacity: 0.15 !important; }
    .stApp::after { opacity: 0.15 !important; }
    h1,h2,h3,h4,h5,h6,p,span,label { color: #f0e6f5 !important; }
    /* Force inline hardcoded dark text to light in dark mode */
    [style*="color:#2b1830"], [style*="color: #2b1830"] { color: #f0e6f5 !important; }
    [style*="color:#333"], [style*="color: #333"] { color: #e8d5f0 !important; }
    .stCaption, [data-testid="stCaptionContainer"] { color: #b89ec0 !important; }
    .step-summary { background: #2a1332 !important; border-color: #5a3d6e !important; color: #d4b8e0 !important; }
    .stRadio > div > label { background: #2a1332 !important; border-color: #4a2d5a !important; color: #e8d5f0 !important; }
    .stRadio > div > label p, .stRadio > div > label span,
    .stRadio > div > label div, [data-testid="stRadio"] span,
    [data-testid="stRadio"] p, [data-testid="stRadio"] label span { color: #e8d5f0 !important; font-family: 'Poppins', sans-serif !important; }
    .stCheckbox > label p, .stCheckbox > label span,
    .stCheckbox > label div, [data-testid="stCheckbox"] span,
    [data-testid="stCheckbox"] p, [data-testid="stCheckbox"] label span { color: #e8d5f0 !important; font-family: 'Poppins', sans-serif !important; }
    .stCheckbox > label { background: #2a1332 !important; border-color: #4a2d5a !important; }
    .stRadio > div > label:hover { background: #3a1f45 !important; border-color: #9B3DAE !important; }
    .stButton > button:not([kind="primary"]) { background: #2a1332 !important; border-color: #4a2d5a !important; color: #d4b8e0 !important; }
    .stButton > button:not([kind="primary"]):hover { background: #3a1f45 !important; border-color: #9B3DAE !important; }
    .stCheckbox > label { background: #2a1332 !important; border-color: #4a2d5a !important; color: #e8d5f0 !important; }
    .stTextInput > div > div > input { background: #2a1332 !important; border-color: #4a2d5a !important; color: #f0e6f5 !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { background: #1e0f25 !important; border-color: #4a2d5a !important; box-shadow: 0 6px 20px rgba(0,0,0,0.4) !important; }
    .streamlit-expanderHeader, [data-testid="stExpander"] summary { background: #2a1332 !important; border-color: #4a2d5a !important; color: #e8d5f0 !important; }
    /* Fix arrow overlap in expanders */
    [data-testid="stExpander"] summary svg { display: none !important; }
    [data-testid="stExpander"] summary::before { content: "▼ "; font-size: 0.8rem; }
    [data-testid="stExpander"][open] summary::before { content: "▲ "; font-size: 0.8rem; }
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span { color: #e8d5f0 !important; padding-left: 0 !important; }
    hr { border-color: #3a1f45 !important; }
    section[data-testid="stVerticalBlock"] .stButton > button:not([kind="primary"]) { background: #2a1332 !important; border-color: #4a2d5a !important; color: #e8d5f0 !important; }
    section[data-testid="stVerticalBlock"] .stButton > button:not([kind="primary"]):hover { background: #3a1f45 !important; border-color: #9B3DAE !important; color: #c388d4 !important; }
    .stAlert { background: #2a1332 !important; }
    .skeleton { background: linear-gradient(90deg, #2a1332 25%, #3a1f45 50%, #2a1332 75%) !important; }
    /* Force all text visible in dark mode */
    .stMarkdown p, .stMarkdown span, .stMarkdown li,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span { color: #e8d5f0 !important; }
    [data-testid="stAlert"] p, [data-testid="stAlert"] span,
    [data-testid="stAlert"] div { color: #e8d5f0 !important; }
    [data-testid="stVerticalBlockBorderWrapper"] p,
    [data-testid="stVerticalBlockBorderWrapper"] span { color: #e8d5f0 !important; }
    .stButton > button { color: #d4b8e0 !important; }
    .stButton > button[kind="primary"] { 
        color: white !important;
        background: linear-gradient(135deg, #dda0e8 0%, #c070d0 60%, #a854bc 100%) !important;
        border: none !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    .step-dot { background: #3a1f45 !important; }
    .step-dot.done { background: linear-gradient(135deg, #9B3DAE, #6a2578) !important; }
    .step-dot.current { background: #9B3DAE !important; }
</style>""", unsafe_allow_html=True)
    else:
        st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #fbf7fc 0%, #ffffff 100%) !important; }
    h1,h2,h3,h4,h5,h6 { color: #2b1830 !important; }
</style>""", unsafe_allow_html=True)


# ── Size chart images ─────────────────────────────────────────────────────────
# Replace each URL with the real Tynor hosted image URL when you have them
SIZE_CHART_IMAGES = {
    "Knee":         "https://www.tynorstore.com/cdn/shop/files/4_44e75b41-94a4-4b2c-ad82-a1f8bf84e41f.webp?v=1774003438&width=1125",
    "Back / Spine": "https://your-url.com/size-chart-back.jpg",
    "Neck":         "https://your-url.com/size-chart-neck.jpg",
    "Shoulder":     "https://your-url.com/size-chart-shoulder.jpg",
    "Elbow":        "https://your-url.com/size-chart-elbow.jpg",
    "Wrist / Hand": "https://your-url.com/size-chart-wrist.jpg",
    "Ankle":        "https://your-url.com/size-chart-ankle.jpg",
    "Foot":         "https://your-url.com/size-chart-foot.jpg",
    "Leg / Thigh":  "https://your-url.com/size-chart-leg.jpg",
    "Abdominal":    "https://your-url.com/size-chart-abdominal.jpg",
}

def show_size_chart(region):
    url = SIZE_CHART_IMAGES.get(region)
    if not url: return
    # Size chart — no expander
    if "show_size_chart" not in st.session_state: st.session_state["show_size_chart"] = False
    if st.button("Hide size guide" if st.session_state["show_size_chart"] else "How to measure & size guide", use_container_width=True, key=f"size_chart_{region}"):
        st.session_state["show_size_chart"] = not st.session_state["show_size_chart"]
    if st.session_state["show_size_chart"]:
        if "your-url.com" in url:
            st.caption("Size chart image coming soon — replace the URL in SIZE_CHART_IMAGES at the top of this file.")
        else:
            st.image(url, use_container_width=True)

# ── Region-specific questions ─────────────────────────────────────────────────
REGION_QUESTIONS = {
    "Knee": [
        {
            "key": "q_onset",
            "question": "How did it start?",
            "options": ["Sudden injury","Gradual over time","After surgery","Not sure"],
        },
        {
            "key": "q_duration",
            "question": "How long have you had this?",
            "options": ["Under 2 weeks","2 weeks to 3 months","More than 3 months"],
        },
        {
            "key": "q_severity",
            "question": "How bad is it?",
            "options": ["Mild — discomfort but functional","Moderate — limits daily activity","Severe — cannot bear weight"],
            "caption": "**Mild** — manageable · **Moderate** — affects walking/stairs · **Severe** — cannot put weight on it",
        },
        {
            "key": "q_support",
            "question": "What kind of support are you looking for?",
            "options": ["Gentle compression and warmth","Firm stabilisation","Lock / immobilise the knee"],
            "caption": "**Gentle** — warmth & light support · **Firm** — stability and control · **Lock** — restrict movement",
        },
    ],
    "Back": [
        {
            "key": "q_onset",
            "question": "How did it start?",
            "options": ["Sudden strain or injury","Gradual over time","Chronic condition","Post-surgery"],
        },
        {
            "key": "q_duration",
            "question": "How long have you had this?",
            "options": ["Under 2 weeks","2 weeks to 3 months","More than 3 months"],
        },
        {
            "key": "q_severity",
            "question": "How much does it affect you?",
            "options": ["Mild — occasional ache","Moderate — limits bending or sitting","Severe — can barely move"],
        },
        {
            "key": "q_support",
            "question": "What kind of support are you looking for?",
            "options": ["Soft belt for daily wear","Firm belt for work or activity","Rigid brace (post-surgery or serious injury)"],
        },
    ],
    "Neck": [
        {
            "key": "q_onset",
            "question": "How did it start?",
            "options": ["Sudden — whiplash or injury","Gradual","Post-surgery","Woke up with it"],
        },
        {
            "key": "q_duration",
            "question": "How long have you had this?",
            "options": ["Under 2 weeks","2 weeks to 3 months","More than 3 months"],
        },
        {
            "key": "q_severity",
            "question": "How severe is it?",
            "options": ["Mild — stiffness only","Moderate — limits head movement","Severe — cannot turn neck comfortably"],
        },
        {
            "key": "q_support",
            "question": "What kind of collar are you looking for?",
            "options": ["Soft collar — comfort and warmth","Semi-rigid collar — moderate support","Rigid collar — post-surgery or serious injury"],
        },
    ],
    "Shoulder": [
        {
            "key": "q_onset",
            "question": "How did it start?",
            "options": ["Sudden injury","Gradual over time","Post-surgery","After repetitive activity"],
        },
        {
            "key": "q_duration",
            "question": "How long have you had this?",
            "options": ["Under 2 weeks","2 weeks to 3 months","More than 3 months"],
        },
        {
            "key": "q_severity",
            "question": "How bad is it?",
            "options": ["Mild — aches but can lift arm","Moderate — limited arm movement","Severe — cannot raise arm"],
        },
        {
            "key": "q_support",
            "question": "What kind of support are you looking for?",
            "options": ["Compression sleeve","Supportive brace","Immobilisation / sling"],
        },
    ],
    "Elbow": [
        {
            "key": "q_when",
            "question": "When does it hurt?",
            "options": ["Only during gripping or activity","At rest too","Almost constantly"],
        },
        {
            "key": "q_duration",
            "question": "How long have you had this?",
            "options": ["Under 4 weeks","1 to 6 months","More than 6 months"],
        },
        {
            "key": "q_severity",
            "question": "How bad is it?",
            "options": ["Mild — manageable","Moderate — affects typing or lifting","Severe — cannot grip at all"],
        },
        {
            "key": "q_support",
            "question": "What kind of support are you looking for?",
            "options": ["Compression sleeve","Targeted strap (tennis or golfer's elbow)","Full elbow brace (post-injury)"],
        },
    ],
    "Wrist": [
        {
            "key": "q_onset",
            "question": "How did it start?",
            "options": ["Sudden injury","Gradual / repetitive strain","Post-surgery","Not sure"],
        },
        {
            "key": "q_duration",
            "question": "How long have you had this?",
            "options": ["Under 2 weeks","2 weeks to 3 months","More than 3 months"],
        },
        {
            "key": "q_severity",
            "question": "How bad is it?",
            "options": ["Mild — some discomfort","Moderate — limits gripping or typing","Severe — cannot use hand normally"],
        },
        {
            "key": "q_support",
            "question": "What kind of support are you looking for?",
            "options": ["Flexible wrist wrap","Semi-rigid splint","Full immobilisation splint"],
        },
    ],
    "Ankle": [
        {
            "key": "q_onset",
            "question": "How did this happen?",
            "options": ["Sudden twist or injury","Gradual pain","Post-fracture","Post-surgery"],
        },
        {
            "key": "q_duration",
            "question": "How long have you had this?",
            "options": ["Under 2 weeks","2 weeks to 3 months","More than 3 months"],
        },
        {
            "key": "q_severity",
            "question": "How bad is it?",
            "options": ["Mild — slight swelling, can walk","Moderate — limp but can bear weight","Severe — cannot bear weight"],
        },
        {
            "key": "q_support",
            "question": "What kind of support are you looking for?",
            "options": ["Ankle sleeve — compression","Ankle brace with straps — stability","Rigid splint or walker boot — immobilise"],
        },
    ],
    "Foot": [
        {
            "key": "q_concern",
            "question": "What is the main concern?",
            "options": ["Pain during walking","Heel pain","Post-fracture recovery","Post-surgery","Flat feet / arch support"],
        },
        {
            "key": "q_duration",
            "question": "How long have you had this?",
            "options": ["Under 2 weeks","2 weeks to 3 months","More than 3 months"],
        },
        {
            "key": "q_severity",
            "question": "How bad is it?",
            "options": ["Mild — aches but can walk normally","Moderate — affects walking","Severe — cannot walk properly"],
        },
        {
            "key": "q_support",
            "question": "What kind of support are you looking for?",
            "options": ["Cushion or insole","Foot brace","Walker boot","Cast cover"],
        },
    ],
    "Thigh": [
        {
            "key": "q_need",
            "question": "What do you need support for?",
            "options": ["Muscle compression during activity","Moving after injury","Post-fracture recovery","General support"],
        },
        {
            "key": "q_duration",
            "question": "How long have you had this?",
            "options": ["Under 2 weeks","2 weeks to 3 months","More than 3 months"],
        },
        {
            "key": "q_severity",
            "question": "How bad is it?",
            "options": ["Mild — discomfort","Moderate — limits walking","Severe — cannot bear weight"],
        },
        {
            "key": "q_support",
            "question": "What kind of support?",
            "options": ["Compression sleeve","Rigid support / brace","Walking aid"],
        },
    ],
    "Calf": [
        {
            "key": "q_onset",
            "question": "How did it start?",
            "options": ["Sudden strain or cramp","Gradual / overuse","Post-injury","Not sure"],
        },
        {
            "key": "q_duration",
            "question": "How long have you had this?",
            "options": ["Under 2 weeks","2 weeks to 3 months","More than 3 months"],
        },
        {
            "key": "q_severity",
            "question": "How bad is it?",
            "options": ["Mild — some tightness or pain","Moderate — affects walking","Severe — cannot walk properly"],
        },
        {
            "key": "q_support",
            "question": "What kind of support?",
            "options": ["Compression sleeve","Rigid support","Walking aid"],
        },
    ],
    "Finger": [
        {
            "key": "q_onset",
            "question": "How did it happen?",
            "options": ["Sudden injury / jam","Gradual / overuse","Post-surgery","Not sure"],
        },
        {
            "key": "q_duration",
            "question": "How long have you had this?",
            "options": ["Under 2 weeks","2 weeks to 3 months","More than 3 months"],
        },
        {
            "key": "q_severity",
            "question": "How bad is it?",
            "options": ["Mild — some pain or stiffness","Moderate — limits gripping","Severe — cannot bend or use finger"],
        },
        {
            "key": "q_support",
            "question": "What kind of support?",
            "options": ["Buddy strap / finger sleeve","Finger splint — semi-rigid","Full immobilisation splint"],
        },
    ],
    "Chest": [
        {
            "key": "q_onset",
            "question": "How did it start?",
            "options": ["Injury or fracture","Post-surgery","Breathing discomfort","Not sure"],
        },
        {
            "key": "q_duration",
            "question": "How long have you had this?",
            "options": ["Under 2 weeks","2 weeks to 3 months","More than 3 months"],
        },
        {
            "key": "q_severity",
            "question": "How bad is it?",
            "options": ["Mild — discomfort when moving","Moderate — pain on breathing or bending","Severe — very painful at rest"],
        },
        {
            "key": "q_support",
            "question": "What kind of support?",
            "options": ["Compression and pain relief","Protection and immobilisation"],
        },
    ],
    "Abdominal": None,  # handled separately via sub-location branching
}

# Abdominal sub-paths (branched by sub-location)
ABDOMINAL_PATHS = {
    "Post-delivery / post-pregnancy tummy": [
        {"key": "abd_delivery_time",  "question": "How long since delivery?",               "options": ["Under 6 weeks","6 weeks to 6 months","Over 6 months"]},
        {"key": "abd_delivery_type",  "question": "Was it a normal delivery or C-section?", "options": ["Normal delivery","C-section"]},
        {"key": "abd_support_level",  "question": "How much support are you looking for?",  "options": ["Light","Medium","Firm"]},
    ],
    "Hernia support": [
        {"key": "abd_hernia_confirmed","question": "Has the hernia been confirmed by a doctor?","options": ["Yes, diagnosed","Not yet confirmed"]},
        {"key": "abd_hernia_side",     "question": "Which side?",                               "options": ["Right","Left","Both sides","Not sure"]},
        {"key": "abd_activity",        "question": "How active are you?",                       "options": ["Mostly resting","Walking daily","Physical work or standing all day"]},
    ],
    "Rib / chest area": [
        {"key": "abd_rib_cause",   "question": "How did it happen?",       "options": ["Fracture or injury","After surgery","Breathing discomfort without injury"]},
        {"key": "abd_rib_duration","question": "How long?",                "options": ["Under 2 weeks","2 weeks to 3 months","More than 3 months"]},
        {"key": "abd_rib_support", "question": "What kind of support?",    "options": ["Pain relief and compression","Protection and immobilisation"]},
    ],
    "General abdominal support": [
        {"key": "abd_gen_duration","question": "How long?",                "options": ["Under 2 weeks","Ongoing"]},
        {"key": "abd_gen_support", "question": "How much support?",        "options": ["Light everyday support","Medium","Firm"]},
    ],
}

SAFETY_FLAGS = [
    "Recent surgery in this area",
    "Suspected fracture / broken bone",
    "Numbness or tingling",
    "Severe swelling that appeared suddenly",
    "None of the above",
]

SAFETY_FOLLOWUP_QUESTIONS = [
    {
        "key": "safety_timing",
        "question": "How long ago did this happen?",
        "options": ["Just now or today", "Within the last week", "A few weeks ago", "More than a month ago"],
    },
    {
        "key": "safety_mobility",
        "question": "Can you move the affected area?",
        "options": ["Yes, but with pain", "Very limited movement", "Cannot move it at all"],
    },
]

LIFESTYLE_OPTIONS = [
    "Warmth & pain relief (heat therapy)",
    "Cold therapy (swelling / post-exercise)",
    "Gentle everyday support / comfort",
    "Not sure — suggest something general",
]

LIFESTYLE_TAGS = {
    "Warmth & pain relief (heat therapy)":    ["neoprene","wrap","warmth"],
    "Cold therapy (swelling / post-exercise)": ["cool","cold","gel"],
    "Gentle everyday support / comfort":       ["support","comfeel","pair"],
    "Not sure — suggest something general":    [],
}

# General Tynor Cure FAQs
TYNOR_GENERAL_FAQS = [
    ("What are Tynor Cure products?", "Tynor Cure products are orthopaedic solutions designed to relieve pain and support recovery from injuries and musculoskeletal conditions. They also aid in the faster healing of affected areas."),
    ("Who can use Tynor Cure products?", "Tynor Cure products are recommended for anyone recovering from injuries, surgery, or musculoskeletal pain. They are suitable for adults who require support for healing and pain relief."),
    ("What types of injuries can Tynor Cure products help with?", "Tynor Cure products assist in the healing of injuries such as sprains, strains, fractures, and post-surgical recovery. They are designed to provide support and comfort to affected areas."),
    ("What materials are Tynor Cure products made of?", "Tynor Cure products are made from materials specifically focused on recovery and support. These materials ensure durability, comfort, and effective pain relief during the healing process."),
    ("What types of products are included in Tynor Cure?", "The Cure collection by Tynor includes back supports, abdominal belts, knee supports, posture correctors, and other orthopaedic aids designed for pain relief and faster recovery."),
    ("Do Tynor Cure products help in post-surgery recovery?", "Yes, Tynor Cure products provide the support and immobilisation required after surgery. They aid in pain management and help the healing process proceed more smoothly."),
    ("How is Tynor Cure different from Tynor Sports products?", "Tynor Cure focuses on recovery and healing after an injury, whereas Tynor Sports products are designed to prevent injuries during physical activity. Cure products help manage existing conditions."),
    ("How long should I use these products?", "Usage depends on the type and severity of the injury. Follow the product instructions and your doctor's advice to determine the correct duration for optimal healing."),
    ("Do we need to consult a doctor before using Tynor Cure products?", "It is recommended to consult a doctor before using Tynor Cure products, especially for serious injuries or post-surgery recovery. Proper guidance ensures safe and effective use."),
    ("How do I choose the right Tynor Cure product?", "Choose based on the area requiring support and the type of injury. Product descriptions provide guidance, but consulting a healthcare professional ensures the best choice."),
]

FAQS_BY_TYPE = {
    "Support": [
        ("How long should I wear this?",     "4–6 hours to start, building up as tolerated. Remove overnight unless advised by your doctor."),
        ("Can I wash it?",                   "Hand wash in cold water, lay flat to dry. Do not machine wash or tumble dry."),
        ("How do I know the size is right?", "Snug but not tight — you should be able to slide one finger underneath."),
    ],
    "Brace": [
        ("Will this limit my movement?",  "Firm braces limit harmful movement while allowing safe range of motion."),
        ("Do I need a doctor's advice?",  "For moderate-to-severe injuries yes — a physio can advise on the correct setting."),
        ("Can I drive with it on?",       "Only if your doctor has cleared you to drive after your injury or surgery."),
    ],
    "Immobiliser": [
        ("Can I walk with this on?",         "Yes, carefully. The immobiliser is designed to allow safe ambulation."),
        ("How tight should it be?",          "Firm but not painful. Loosen immediately if you notice numbness or colour change."),
        ("How long will I need to wear it?", "Follow your doctor's specific instructions — varies by injury type."),
    ],
    "Therapy": [
        ("How long per session?",            "15–20 minutes cold / 20 minutes heat. At least 45 minutes between sessions."),
        ("Should I apply directly on skin?", "No — always wrap in a thin cloth to avoid burns."),
    ],
    "Default": [
        ("How do I choose the right size?", "Refer to the size guide above. When in doubt, go one size up."),
        ("Can I return it?",                "Contact Tynor customer care within 7 days of delivery for return or exchange queries."),
    ],
}

REGIONS = {
    "Abdominal": ["Abdominal"],
    "Ankle":     ["Ankle","Foot"],
    "Back":      ["Back","Back, neck"],
    "Calf":      ["Calf","Leg"],
    "Chest":     ["Chest"],
    "Elbow":     ["Elbow"],
    "Finger":    ["Hand, Finger"],
    "Knee":      ["Knee"],
    "Neck":      ["Neck","Shoulder, Neck"],
    "Shoulder":  ["Shoulder"],
    "Thigh":     ["Thigh","Leg, thigh"],
    "Wrist":     ["Wrist, hand","Hand, wrist","Wrist, Forearm, hand","Hand","Forearm, arm"],
}

PROBLEM_REGION_MAP = {
    "Finger":    "Wrist / Hand / Elbow",
    "Neck":      "Neck (Cervical)",
    "Shoulder":  None,
    "Elbow":     "Wrist / Hand / Elbow",
    "Wrist":     "Wrist / Hand / Elbow",
    "Chest":     "Ribs / Chest",
    "Back":      "Back / Spine",
    "Abdominal": "Ribs / Chest",
    "Knee":      "Knee",
    "Thigh":     "Mobility / Walking aids",
    "Calf":      "Mobility / Walking aids",
    "Ankle":     "Ankle / Foot",
}

SUB_LOCATION_QUESTIONS = {
    "Finger": {
        "question": "Which finger is affected?",
        "options": ["Index finger","Middle finger","Ring finger","Pinky finger","Thumb","Not sure"],
        "product_tags": {
            "Index finger":   ["finger","splint","mallet"],
            "Middle finger":  ["finger","splint","mallet"],
            "Ring finger":    ["finger","splint","mallet"],
            "Pinky finger":   ["finger","splint"],
            "Thumb":          ["thumb","spica","thumb loop"],
            "Not sure":       [],
        },
    },
    "Knee": {
        "question": "Where exactly in the knee is the problem?",
        "options": ["Front of the knee — kneecap area","Inside edge of the knee","Outside edge of the knee","Back of the knee","All around / not sure"],
        "product_tags": {
            "Front of the knee — kneecap area": ["patellar","patella","open patella","cap"],
            "Inside edge of the knee":          ["oa","hinged","elastic","functional"],
            "Outside edge of the knee":         ["hinged","elastic","functional","wrap"],
            "Back of the knee":                 ["immobilis","rom","adjustable"],
            "All around / not sure":            [],
        },
    },
    "Back": {
        "question": "Which part of your back is affected?",
        "options": ["Lower back — below the waist","Upper / middle back","Tailbone / sacral area","Entire back / not sure"],
        "product_tags": {
            "Lower back — below the waist": ["ls belt","lumbo","lacepull","lumbopore","lumbo sacral"],
            "Upper / middle back":          ["taylor","posture","ash brace","tlso"],
            "Tailbone / sacral area":       ["coccyx","cushion","lumbo sacral"],
            "Entire back / not sure":       [],
        },
    },
    "Neck": {
        "question": "Which movement causes the most pain?",
        "options": ["Looking up or down","Turning left or right","All neck movements hurt","Pain at rest too"],
        "product_tags": {
            "Looking up or down":        ["cervical","collar","philadelphia"],
            "Turning left or right":     ["cervical collar","philadelphia"],
            "All neck movements hurt":   ["philadelphia","cervical orthosis"],
            "Pain at rest too":          ["cervical pillow","neck corrector"],
        },
    },
    "Shoulder": {
        "question": "Where is the shoulder pain?",
        "options": ["Front of the shoulder","Top of the shoulder (near collarbone)","Back of the shoulder / rotator cuff","All around / not sure"],
        "product_tags": {
            "Front of the shoulder":                   ["shoulder support","elastic shoulder"],
            "Top of the shoulder (near collarbone)":   ["clavicle"],
            "Back of the shoulder / rotator cuff":     ["shoulder immobilis","universal shoulder"],
            "All around / not sure":                   [],
        },
    },
    "Elbow": {
        "question": "Where in the elbow is the pain?",
        "options": ["Outer side — tennis elbow","Inner side — golfer's elbow","All around / after injury","Not sure"],
        "product_tags": {
            "Outer side — tennis elbow":     ["tennis elbow","tennis/golfer"],
            "Inner side — golfer's elbow":   ["tennis/golfer","elbow support"],
            "All around / after injury":     ["rom elbow","elbow brace","elbow wrap"],
            "Not sure":                      [],
        },
    },
    "Wrist": {
        "question": "Which part of the wrist is affected?",
        "options": ["Wrist joint","Thumb or base of thumb","Forearm / full wrist area","Not sure"],
        "product_tags": {
            "Wrist joint":               ["wrist support","wrist brace","wristband","wrist wrap"],
            "Thumb or base of thumb":    ["thumb spica","wrist brace with thumb","thumb loop"],
            "Forearm / full wrist area": ["wrist & forearm","forearm splint","wrist splint"],
            "Not sure":                  [],
        },
    },
    "Ankle": {
        "question": "Which part of the ankle is affected?",
        "options": ["Ankle joint — side / all around","Heel","Arch of the foot","Toes or ball of foot","Not sure"],
        "product_tags": {
            "Ankle joint — side / all around": ["ankle binder","ankle support","ankle brace","ankle splint","air ankle"],
            "Heel":                            ["heel","foot support"],
            "Arch of the foot":                ["insole","foot","arch"],
            "Toes or ball of foot":            ["toe","metatarsal","foot"],
            "Not sure":                        [],
        },
    },
    "Thigh": {
        "question": "Which part of the thigh is affected?",
        "options": ["Front of thigh","Back of thigh (hamstring)","Inner thigh","All around / not sure"],
        "product_tags": {
            "Front of thigh":              ["thigh","stump","compression"],
            "Back of thigh (hamstring)":   ["thigh","stump"],
            "Inner thigh":                 ["thigh","stump"],
            "All around / not sure":       [],
        },
    },
    "Calf": {
        "question": "Which part of the calf is affected?",
        "options": ["Back of calf (gastrocnemius)","Shin (front of lower leg)","Both / all around","Not sure"],
        "product_tags": {
            "Back of calf (gastrocnemius)": ["calf","below knee","compression"],
            "Shin (front of lower leg)":    ["shin","below knee"],
            "Both / all around":            ["calf","leg"],
            "Not sure":                     [],
        },
    },
    "Chest": {
        "question": "Where in the chest is the pain?",
        "options": ["Front of chest / sternum","Side ribs","Upper chest","All around / not sure"],
        "product_tags": {
            "Front of chest / sternum": ["chest binder","rib belt"],
            "Side ribs":                ["rib belt","chest"],
            "Upper chest":              ["chest binder","clavicle"],
            "All around / not sure":    [],
        },
    },
    "Abdominal": {
        "question": "What is the concern?",
        "options": ["Post-delivery / post-pregnancy tummy","Hernia support","Rib / chest area","General abdominal support"],
        "product_tags": {
            "Post-delivery / post-pregnancy tummy": ["abdominal belt","abdominal support","pregnancy"],
            "Hernia support":                       ["hernia"],
            "Rib / chest area":                     ["rib belt","chest binder"],
            "General abdominal support":            ["abdominal","abs support"],
        },
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def normalize(s):
    return re.sub(r'\s+', ' ', str(s).lower().strip())

def infer_support_type(sub_cat):
    sl = sub_cat.lower()
    if any(x in sl for x in ['immobilis','walker boot','splint','fracture','cast','walker']): return 'lock'
    if any(x in sl for x in ['brace','hinged','functional','rom','rigid']): return 'firm'
    return 'gentle'

def infer_severity(support_type):
    return {'gentle':['mild','moderate'], 'firm':['moderate','severe'], 'lock':['severe']}[support_type]

def get_products_for_region(region_label):
    bps = REGIONS.get(region_label,[])
    return [p for p in catalog if p['body_part'] in bps]

def get_problems_for_region(region_label):
    key = PROBLEM_REGION_MAP.get(region_label)
    if not key or key not in problems: return []
    return problems[key]

def get_activities_for_region(region_label):
    prods = [p for p in get_products_for_region(region_label) if p['brand']=='Sport']
    acts = []
    for p in prods:
        for a in p.get('activity',[]):
            if a and a.lower() not in ('not applicable','') and a not in acts:
                acts.append(a)
    return sorted(acts)

def faq_for_product(p):
    sl = p['sub_cat'].lower()
    if any(x in sl for x in ['immobilis','splint','walker']): return FAQS_BY_TYPE['Immobiliser']
    if any(x in sl for x in ['brace','hinged','rom']):        return FAQS_BY_TYPE['Brace']
    if any(x in sl for x in ['therapy','cool','hot']):        return FAQS_BY_TYPE['Therapy']
    if 'support' in sl:                                       return FAQS_BY_TYPE['Support']
    return FAQS_BY_TYPE['Default']

def stars(r):
    full = int(r); half = 1 if (r-full)>=0.5 else 0
    return "★"*full + ("½" if half else "") + f" {r}/5"

def avail_badge(avail_dict):
    if not avail_dict: return ""
    statuses = list(avail_dict.values())
    if all(s=='out_of_stock' for s in statuses): return "🔴 Out of stock"
    if any(s=='low_stock' for s in statuses):    return "🟡 Low stock"
    return "🟢 In stock"

def validate_phone(phone):
    cleaned = re.sub(r'\D','', phone.strip())
    if not cleaned: return True, ""
    if len(cleaned) != 10: return False, "Please enter a valid 10-digit mobile number."
    return True, ""

def map_support_label(region, answer):
    """Map region-specific support answer to gentle/firm/lock."""
    gentle_kws = ['gentle','soft','light','compression','sleeve','cushion','insole','wrap','warmth']
    lock_kws   = ['lock','immobilis','rigid','walker boot','sling','cast']
    al = answer.lower()
    if any(k in al for k in lock_kws):   return 'lock'
    if any(k in al for k in gentle_kws): return 'gentle'
    return 'firm'

def map_severity_label(answer):
    al = answer.lower()
    if 'severe' in al or 'cannot' in al or 'can\'t' in al: return 'severe'
    if 'moderate' in al or 'limits' in al or 'limp' in al: return 'moderate'
    return 'mild'

# ── Progress ──────────────────────────────────────────────────────────────────
def show_progress():
    step = st.session_state.step
    step_map = {0:0,1:8,2:16,3:24,4:32,5:40,"sport_support":50,
                "sub_location":46,"severity_q":58,
                "abd_q_0":50,"abd_q_1":58,"abd_q_2":66,
                "safety_q_0":38,"safety_q_1":44,"ai_check":75,"contact":85,"result":100,"see_clinician":100}
    pct = step_map.get(step, 50)
    total_dots = 10
    done_dots = int((pct / 100) * total_dots)
    dots_html = ""
    for i in range(total_dots):
        if i < done_dots:
            dots_html += '<div class="step-dot done"></div>'
        elif i == done_dots:
            dots_html += '<div class="step-dot current"></div>'
        else:
            dots_html += '<div class="step-dot"></div>'
    st.markdown(f'<div class="step-tracker">{dots_html}</div>', unsafe_allow_html=True)

def show_summary():
    ss   = st.session_state
    step = ss.get('step', 0)
    if not isinstance(step, int) or step <= 1: return
    parts = []
    if ss.get('region'):  parts.append(f"{ss['region']}")
    if ss.get('intent'):  parts.append(f"🎯 {ss['intent']}")
    if ss.get('problem'): parts.append(f"🩺 {ss['problem'][:28]}{'…' if len(ss.get('problem',''))>28 else ''}")
    if parts:
        st.markdown(f'<div class="step-summary">{" &nbsp;·&nbsp; ".join(parts)}</div>', unsafe_allow_html=True)

# ── Resolver ──────────────────────────────────────────────────────────────────
def resolve(region_label, brand, problem=None, sub_location=None,
            severity_mapped=None, support_mapped=None,
            activity=None, lifestyle_choice=None):

    pool       = get_products_for_region(region_label)
    candidates = [p for p in pool if p['brand'] == brand]

    if brand == 'Cure' and problem:
        is_freetext = st.session_state.get('problem_is_freetext', False)
        if is_freetext:
            kws = [w for w in normalize(problem).split() if len(w) > 3]
            if kws:
                kw_match = [p for p in candidates
                            if any(k in normalize(p['name']+' '+p['short_desc']) for k in kws)]
                if kw_match: candidates = kw_match
        else:
            prob_entry = next((pb for pb in get_problems_for_region(region_label)
                               if pb['easy_name'] == problem), None)
            if prob_entry:
                suggested = {normalize(n) for n in prob_entry['products']}
                match = [p for p in candidates if normalize(p['name']) in suggested]
                if match: candidates = match

        if sub_location:
            sub_q = SUB_LOCATION_QUESTIONS.get(region_label,{})
            tags  = sub_q.get('product_tags',{}).get(sub_location,[])
            if tags:
                tag_match = [p for p in candidates if any(t in normalize(p['name']) for t in tags)]
                if tag_match: candidates = tag_match

        if severity_mapped:
            sev_match = [p for p in candidates if severity_mapped in infer_severity(infer_support_type(p['sub_cat']))]
            if sev_match: candidates = sev_match

        if support_mapped:
            sup_match = [p for p in candidates if infer_support_type(p['sub_cat']) == support_mapped]
            if sup_match: candidates = sup_match

    elif brand == 'Sport' and activity:
        act_n = normalize(activity)
        act_match = [p for p in candidates
                     if any(act_n in normalize(a) or normalize(a) in act_n for a in p.get('activity',[]))]
        if act_match: candidates = act_match

        if support_mapped:
            sup_match = [p for p in candidates if infer_support_type(p['sub_cat']) == support_mapped]
            if sup_match: candidates = sup_match

    elif brand == 'Life' and lifestyle_choice:
        tags = LIFESTYLE_TAGS.get(lifestyle_choice,[])
        if tags:
            tag_match = [p for p in candidates
                         if any(t in normalize(p['name']+' '+p['sub_cat']+' '+p['short_desc']) for t in tags)]
            if tag_match: candidates = tag_match

    return sorted(candidates, key=lambda p: p['rating'], reverse=True)[:2]

# ── AI Validation ────────────────────────────────────────────────────────────
def validate_with_ai(session_data):
    """Call Groq API to check for inconsistencies in user answers."""
    import requests

    summary = []
    summary.append(f"Region: {session_data.get('region','')}")
    summary.append(f"Age: {session_data.get('age','')}")
    summary.append(f"Gender: {session_data.get('gender','')}")
    summary.append(f"Intent: {session_data.get('intent','')}")
    if session_data.get('problem'):
        summary.append(f"Problem: {session_data.get('problem','')}")
    if session_data.get('sub_location'):
        summary.append(f"Location: {session_data.get('sub_location','')}")
    if session_data.get('q_severity') or session_data.get('severity_mapped'):
        summary.append(f"Severity: {session_data.get('q_severity','') or session_data.get('severity_mapped','')}")
    if session_data.get('activity'):
        summary.append(f"Activity: {session_data.get('activity','')}")
    if session_data.get('sport_support'):
        summary.append(f"Support level: {session_data.get('sport_support','')}")
    if session_data.get('lifestyle_choice'):
        summary.append(f"Lifestyle need: {session_data.get('lifestyle_choice','')}")

    user_summary = "\n".join(summary)

    system_prompt = """You are a clinical validation assistant for Tynor Orthotics.

Your ONLY job is to check if the answers below contain any of these EXACT inconsistencies and flag them:

MUST FLAG (always, no exceptions):
1. Gender is Male AND any of these words appear in Problem or Location: pregnancy, post-delivery, maternity, pregnant, delivery, c-section, womb
2. Gender is Male AND Age is Under 14 AND problem involves pregnancy
3. Age is Under 14 AND Activity or Support involves: gym, weightlifting, maximum, heavy lifting
4. Severity is Severe AND Support level is Gentle
5. Age is Under 14 AND problem involves alcohol, smoking, or adult conditions

If ANY of the above are true, respond with: "Just checking — [brief friendly 1-sentence note about the inconsistency]. Could you confirm?"

If NONE of the above are true, respond with exactly the single word: OK

Rules:
- Be case-insensitive when checking
- Do NOT flag things not in the list above
- Do NOT add any explanation or reasoning
- Output ONLY "OK" or the short "Just checking —" message"""

    try:
        GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        GROQ_KEY = "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"
    url = "https://api.groq.com/openai/v1/chat/completions"

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Customer answers:\n" + user_summary}
        ],
        "max_tokens": 150,
        "temperature": 0.2
    }

    try:
        resp = requests.post(url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + GROQ_KEY
            },
            json=payload, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        text = result["choices"][0]["message"]["content"].strip()
        if text.upper() == "OK":
            return False, ""
        return True, text
    except Exception as e:
        return True, "DEBUG error: " + str(e)


# ── Navigation ────────────────────────────────────────────────────────────────
def push(new_step):
    h = st.session_state.get("history",[])
    h.append(st.session_state.step)
    st.session_state.history = h
    st.session_state.step = new_step

def go_back():
    h = st.session_state.get("history",[])
    if h:
        st.session_state.step = h.pop()
        st.session_state.history = h

def reset():
    for k in list(st.session_state.keys()): del st.session_state[k]

def nav(next_label="Next →", condition=True):
    c1,c2 = st.columns(2)
    with c1:
        if st.session_state.get("history"):
            if st.button("← Back", use_container_width=True):
                go_back(); st.rerun()
    with c2:
        if condition:
            return st.button(next_label, use_container_width=True, type="primary")
    return False

def generate_captcha():
    if "captcha_a" not in st.session_state:
        st.session_state.captcha_a = random.randint(2,9)
        st.session_state.captcha_b = random.randint(2,9)

def get_product_image_url(p):
    """Try to construct Tynor store image URL from product name."""
    slug = re.sub(r'[^a-z0-9\s-]', '', p['name'].lower()).strip().replace(' ', '-').replace('--', '-')
    return f"https://www.tynorstore.com/products/{slug}"

def show_product_card(p, region=None):
    with st.container(border=True):
        badges = ""
        if p.get('rating', 0) >= 4.6:
            badges += '<span class="product-badge top-rated">⭐ Top Rated</span> '
        if p.get('rating', 0) >= 4.4 and p.get('availability'):
            statuses = list(p.get('availability',{}).values())
            if any(s == 'low_stock' for s in statuses):
                badges += '<span class="product-badge">🔥 Selling Fast</span>'
        if badges:
            st.markdown(badges, unsafe_allow_html=True)

        # Product layout: image left, details right
        img_col, info_col = st.columns([1, 2.5])
        with img_col:
            img_url = p.get('image_url') or p.get('image') or None
            if img_url:
                st.image(img_url, use_container_width=True)
            else:
                # Placeholder with product initial
                initial = p['name'][0].upper()
                st.markdown(
                    f"""<div style='background:linear-gradient(135deg,#f0e3f7,#e0c8f0);
                    border-radius:12px;height:120px;display:flex;align-items:center;
                    justify-content:center;font-size:2.5rem;font-weight:700;color:#9B3DAE;'>
                    {initial}</div>""",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<p style='font-size:0.72rem;color:#aaa;text-align:center;margin-top:4px;'>"
                    f"<a href='{get_product_image_url(p)}' target='_blank' style='color:#9B3DAE;'>View on Tynor ↗</a></p>",
                    unsafe_allow_html=True
                )

        with info_col:
            c1,c2 = st.columns([3,1])
            with c1:
                st.markdown(f"### {p['name']}")
                st.caption(f"{p['sub_cat']} · {p['brand']}  {avail_badge(p.get('availability',{}))}")
            with c2:
                st.markdown(f"**{stars(p['rating'])}**")

            mat_kws = ['neoprene','elastic','polypropylene','aluminium','cotton','gel','polyester','foam','knit','lycra','spandex','silicone','rubber','steel']
            material = next((m.title() for m in mat_kws if m in p['short_desc'].lower()), None)
            if material:
                st.caption(f"🧵 Material: {material}")

            attrs = p.get('attributes',[])
            if attrs:
                for a in attrs[:3]:
                    title = a.get('title','').split('\n')[0].strip()
                    body  = a.get('body','').strip() or a.get('title','').split('\n')[-1].strip()
                    if title:
                        st.markdown(f"- **{title}**{'  — '+body if body else ''}")
            else:
                for sent in re.split(r'\. ', p['short_desc'])[:3]:
                    if sent.strip(): st.markdown(f"- {sent.strip().rstrip('.')}")

        why_key = f"why_{p['product_id']}"
        if why_key not in st.session_state: st.session_state[why_key] = False
        if st.button("Hide recommendation reason" if st.session_state[why_key] else "Why we recommended this", use_container_width=True, key=f"whybtn_{p['product_id']}"):
            st.session_state[why_key] = not st.session_state[why_key]
        if st.session_state[why_key]:
            ss = st.session_state
            intent  = ss.get('intent','')
            sub_loc = ss.get('sub_location','')
            lines   = []
            if intent == 'Sport':
                lines.append(f"Activity: **{ss.get('activity','')}**.")
            elif intent == 'Cure':
                lines.append(f"Problem: **{ss.get('problem','')}**.")
                if sub_loc and sub_loc not in ("All around / not sure","Not sure",""):
                    lines.append(f"Location: **{sub_loc}**.")
                for k in ['q_onset','q_duration','q_severity','q_support','q_when','q_concern','q_need']:
                    val = ss.get(k)
                    if val: lines.append(f"{val}.")
            elif intent == 'Lifestyle':
                lines.append(f"Need: **{ss.get('lifestyle_choice','')}**.")
            st.write(" ".join(lines) if lines else "Based on your answers, this product best matches your needs.")

        prices = p.get('prices',{})
        avail  = p.get('availability',{})
        if prices:
            st.markdown("**Select size:**")
            if region and region in SIZE_CHART_IMAGES:
                show_size_chart(region)
            opts = [f"{s} — ₹{v}" + (" *(Low stock)*" if avail.get(s)=='low_stock'
                    else " *(Out of stock)*" if avail.get(s)=='out_of_stock' else "")
                    for s,v in prices.items()]
            chosen = st.radio("", opts, index=0, key=f"sz_{p['product_id']}", label_visibility="collapsed")
            chosen_price = int(re.search(r'₹(\d+)', chosen).group(1)) if '₹' in chosen else 0
            st.caption("🚚 3–5 business days · Free shipping above ₹499")
            b1,b2 = st.columns(2)
            with b1:
                if st.button("🛒 Add to Cart", key=f"cart_{p['product_id']}", use_container_width=True):
                    st.success("Added to cart!")
            with b2:
                if st.button(f"⚡ Buy Now — ₹{chosen_price}", key=f"buy_{p['product_id']}", use_container_width=True, type="primary"):
                    st.success("Redirecting to checkout… (placeholder)")

        faq_card_key = f"faqcard_{p['product_id']}"
        if faq_card_key not in st.session_state: st.session_state[faq_card_key] = False
        if st.button("Hide FAQs" if st.session_state[faq_card_key] else "FAQs", use_container_width=True, key=f"faqbtn_{p['product_id']}"):
            st.session_state[faq_card_key] = not st.session_state[faq_card_key]
        if st.session_state[faq_card_key]:
            for q,a in faq_for_product(p):
                st.markdown(f"**{q}**"); st.write(a)

# ── UI ────────────────────────────────────────────────────────────────────────
show_header()

if "step" not in st.session_state:
    st.session_state.step = 0

step = st.session_state.step
show_progress()

# ── Body map renderer ──────────────────────────────────────────────────────────
def render_body_map(interactive=True):
    try:
        from streamlit_image_coordinates import streamlit_image_coordinates
        import io as _io, base64 as _b64
        from PIL import Image as _Image, ImageDraw as _Draw, ImageFont as _Font

        img_bytes = _b64.b64decode(BODY_MAP_B64)
        img = _Image.open(_io.BytesIO(img_bytes)).convert("RGB")
        IMG_W, IMG_H = img.size

        img_dots = img.copy()
        draw = _Draw.Draw(img_dots)
        selected_r = st.session_state.get("region") or st.session_state.get("pending_region")

        for region, (cx_pct, cy_pct) in BODY_MAP_DOTS.items():
            cx = int(cx_pct / 100 * IMG_W)
            cy = int(cy_pct / 100 * IMG_H)
            is_sel = (region == selected_r)

            if is_sel:
                # Large glowing selected dot
                draw.ellipse([cx-20, cy-20, cx+20, cy+20],
                    fill=(155, 61, 174), outline="white", width=3)
                draw.ellipse([cx-26, cy-26, cx+26, cy+26],
                    fill=None, outline=(155, 61, 174), width=2)
                # Label tag
                label = region
                label_w = len(label) * 7 + 16
                lx, ly = cx + 28, cy - 12
                draw.rounded_rectangle([lx, ly, lx+label_w, ly+24],
                    radius=8, fill=(155, 61, 174))
                draw.text((lx+8, ly+4), label, fill="white")
            else:
                # Pulsing-style dot with ring
                draw.ellipse([cx-13, cy-13, cx+13, cy+13],
                    fill=(220, 60, 60), outline="white", width=2)
                draw.ellipse([cx-18, cy-18, cx+18, cy+18],
                    fill=None, outline=(220, 60, 60), width=1)

        if interactive:
            st.markdown(
                "<p style='text-align:center;font-size:0.82rem;color:#9B3DAE;margin-bottom:4px;'>"
                "👆 Click on a body part</p>",
                unsafe_allow_html=True
            )
            val = streamlit_image_coordinates(img_dots, key="body_map_click", use_column_width=True)
            if val is not None:
                disp_w = val.get("width", IMG_W)
                disp_h = val.get("height", IMG_H)
                found = get_region_from_coords(val["x"], val["y"], disp_w, disp_h)
                if found:
                    st.session_state.region = found
                    push(1)
                    st.rerun()
                else:
                    # show which % was clicked for debugging if needed
                    pass
        else:
            st.image(img_dots, use_container_width=True)

        # Region label + change button
        if selected_r:
            st.markdown(
                f"<div style='text-align:center;font-weight:700;color:#9B3DAE;"
                f"font-size:1.1rem;margin-top:6px;font-family:Poppins,sans-serif;'>"
                f"{selected_r}</div>",
                unsafe_allow_html=True
            )
            if step != 0:
                if st.button("↩ Change region", key="change_reg_btn", use_container_width=True):
                    for k in ["region","age","gender","intent","problem","sub_location",
                               "q_severity","q_support","q_onset","q_duration","q_when",
                               "q_concern","q_need","severity_mapped","support_mapped",
                               "activity","sport_support","lifestyle_choice","safety_flags",
                               "safety_timing","safety_mobility","ai_flag","ai_message","celebrated"]:
                        st.session_state.pop(k, None)
                    st.session_state.step = 0
                    st.session_state.history = []
                    st.rerun()

    except ImportError:
        st.info("💡 Run: `pip install streamlit-image-coordinates` for the interactive body map")
        cols = st.columns(2)
        for i, region in enumerate(REGIONS.keys()):
            with cols[i%2]:
                if st.button(region, use_container_width=True, key=f"bmap_btn_{region}"):
                    st.session_state.region = region
                    st.rerun()

# ── Layout ─────────────────────────────────────────────────────────────────────
# Result and ai_check get special handling; everything else is split-screen
if step == "result":
    # Full width result
    safety_flags = st.session_state.get("safety_flags", [])
    if safety_flags:
        st.warning(f"⚠️ You mentioned: **{', '.join(safety_flags)}**. Please consult a doctor before using any support. The recommendation below is for interim relief only.")
    intent = st.session_state.intent
    region = st.session_state.region

    if intent == "Sport":
        results = resolve(region, "Sport",
                          activity=st.session_state.get("activity"),
                          support_mapped=st.session_state.get("support_mapped"))
    elif intent == "Cure":
        results = resolve(region, "Cure",
                          problem=st.session_state.get("problem"),
                          sub_location=st.session_state.get("sub_location"),
                          severity_mapped=st.session_state.get("severity_mapped"),
                          support_mapped=st.session_state.get("support_mapped"))
    else:
        results = resolve(region, "Life",
                          lifestyle_choice=st.session_state.get("lifestyle_choice"))

    if not results:
        pool = get_products_for_region(region)
        results = sorted(pool, key=lambda p: p['rating'], reverse=True)[:1]

    name = st.session_state.get("contact_name","")
    st.subheader(f"Hey {name.split()[0]}, here's what we recommend 👇" if name else "✅ Recommended for you")

    st.markdown('<div style="max-height:600px;overflow-y:auto;padding-right:6px;scrollbar-width:thin;scrollbar-color:#c388d4 #f9f0fc;">', unsafe_allow_html=True)
    for p in results:
        show_product_card(p, region)
        st.divider()
    st.markdown('</div>', unsafe_allow_html=True)

    # FAQ section — no expander, clean accordion
    faq_key = "faq_open"
    if faq_key not in st.session_state: st.session_state[faq_key] = False
    faq_label = "Hide FAQs" if st.session_state[faq_key] else "Frequently Asked Questions"
    if st.button(faq_label, use_container_width=True, key="faq_btn"):
        st.session_state[faq_key] = not st.session_state[faq_key]
    if st.session_state[faq_key]:
        for q, a in TYNOR_GENERAL_FAQS:
            st.markdown(f"**{q}**"); st.write(a); st.divider()

    fb_key = "fb_open"
    if fb_key not in st.session_state: st.session_state[fb_key] = False
    if st.button("Hide feedback" if st.session_state[fb_key] else "Share your feedback", use_container_width=True, key="fb_btn"):
        st.session_state[fb_key] = not st.session_state[fb_key]
    if st.session_state[fb_key]:
        st.slider("How helpful was this recommendation?", 1, 5, 4)
        st.text_area("Anything to add?", placeholder="Your feedback helps us improve")
        if st.button("Submit feedback", key="submit_fb"): st.success("Thank you!")

    sup_key = "sup_open"
    if sup_key not in st.session_state: st.session_state[sup_key] = False
    if st.button("Hide support info" if st.session_state[sup_key] else "Customer Support", use_container_width=True, key="sup_btn"):
        st.session_state[sup_key] = not st.session_state[sup_key]
    if st.session_state[sup_key]:
        st.markdown("📞 1800-1212-656 · WhatsApp +91 8288853995 · Mon–Sat 9am–6pm\n\n📧 support@tynor.in\n\n🌐 www.tynorstore.com")

    st.caption("⚠️ For general guidance only. Consult a healthcare professional for diagnosis and treatment.")
    if st.button("🔄 Start over", use_container_width=True): reset(); st.rerun()

elif step == "contact":
    # Full width contact form
    st.markdown("<div style='max-width:600px;margin:0 auto;'>", unsafe_allow_html=True)
    st.subheader("You're almost there! 🎉")
    st.caption("Pop in your details to grab your recommendation — or skip ahead, no pressure 😊")
    name  = st.text_input("Your name",     placeholder="e.g. Raj Sharma")
    phone = st.text_input("Mobile number", placeholder="10-digit number", max_chars=10)
    phone_valid, phone_error = validate_phone(phone)
    if phone and not phone_valid: st.error(phone_error)
    email = st.text_input("Email (optional)", placeholder="e.g. raj@email.com")
    st.divider()
    generate_captcha()
    a,b = st.session_state.captcha_a, st.session_state.captcha_b
    st.markdown(f"**🔐 Quick verification:** What is **{a} + {b}?**", unsafe_allow_html=False)
    st.caption("This helps us confirm you're not a bot.")
    ans = st.text_input("Your answer", placeholder="Type the number here")
    captcha_ok = ans.strip() == str(a+b)
    if ans.strip() and not captcha_ok: st.error("Incorrect answer — please try again.")
    st.markdown("")
    b1, b2, b3 = st.columns([1,1,1])
    with b1:
        if st.session_state.get("history"):
            if st.button("← Back", use_container_width=True): go_back(); st.rerun()
    with b2:
        if st.button("Skip →", use_container_width=True):
            if not captcha_ok: st.error("Please complete the verification above.")
            else: push("result"); st.rerun()
    with b3:
        if st.button("See recommendation →", use_container_width=True, type="primary"):
            if not captcha_ok: st.error("Please complete the verification above.")
            elif phone and not phone_valid: st.error(phone_error)
            else:
                st.session_state.contact_name  = name
                st.session_state.contact_phone = phone
                st.session_state.contact_email = email
                push("result"); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # ── Full-width body map + scrollable right panel ──────────────────────────

    if step == 0:
        heading_color = "#f0e6f5" if st.session_state.get("dark_mode") else "#2b1830"
        st.markdown(f"""
<div style="text-align:center; margin-bottom:24px;">
    <div style="font-family:Poppins,sans-serif; font-size:2rem; font-weight:800;
    letter-spacing:1px; color:{heading_color}; text-transform:uppercase;">
    Where does it hurt?
    </div>
    <div style="font-family:Poppins,sans-serif; font-size:1rem; color:#9B3DAE;
    font-weight:500; margin-top:6px;">
    Select the body part closest to your pain
    </div>
</div>
""", unsafe_allow_html=True)

        regions_list = sorted(REGIONS.keys())
        st.markdown('<div style="max-height:420px;overflow-y:auto;padding-right:4px;">', unsafe_allow_html=True)
        for row_start in range(0, len(regions_list), 3):
            cols = st.columns(3)
            for col_idx, region in enumerate(regions_list[row_start:row_start+3]):
                with cols[col_idx]:
                    if st.button(region, use_container_width=True, key=f"rbtn_{region}"):
                        st.session_state.region = region; push(1); st.rerun()
            st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    else:
        # Steps 1+ — full width scrollable
        show_summary()
        st.markdown('<div style="max-height:520px;overflow-y:auto;padding-right:6px;scrollbar-width:thin;scrollbar-color:#c388d4 #f9f0fc;">', unsafe_allow_html=True)
        if True:

            # ── Step 1: Age ──────────────────────────────────────────────────
            if step == 1:
                st.subheader("How old is the person who needs support?")
                age = st.radio("", ["Under 14","14 – 17","18 – 28","29 – 45","45 – 59","60 +"], index=None)
                if nav(condition=age is not None):
                    st.session_state.age = age; push(2); st.rerun()

            # ── Step 2: Gender ───────────────────────────────────────────────
            elif step == 2:
                st.subheader("Gender")
                gender = st.radio("", ["Female","Male","Unisex"], index=None)
                if nav(condition=gender is not None):
                    st.session_state.gender = gender; push(3); st.rerun()

            # ── Step 3: Intent ───────────────────────────────────────────────
            elif step == 3:
                st.subheader("What support do you need?")
                intent = st.radio("", [
                    "🏃 Support during a sport or activity",
                    "🩺 I have a problem / injury I want to treat",
                    "🌙 Everyday comfort (lifestyle / daily support)",
                ], index=None)
                if nav(condition=intent is not None):
                    st.session_state.intent = ("Sport" if "sport" in intent.lower()
                        else "Cure" if any(x in intent.lower() for x in ["pain","injury","treat","cure"]) else "Lifestyle")
                    push(4); st.rerun()

            # ── Step 4: Branch ───────────────────────────────────────────────
            elif step == 4:
                intent = st.session_state.intent
                region = st.session_state.region

                if intent == "Sport":
                    acts = get_activities_for_region(region)
                    st.subheader("What's your activity?")
                    opts = (acts + ["Other / general sport"]) if acts else ["Running / Walking","Gym","Cricket / Football","Badminton / Golf","Yoga / Cycling","General sport"]
                    activity = st.radio("", opts, index=None)
                    other_act = ""
                    if activity == "Other / general sport":
                        other_act = st.text_input("Describe your activity", placeholder="e.g. swimming, cycling...")
                    can = activity is not None and (activity != "Other / general sport" or other_act.strip())
                    if nav(condition=can):
                        st.session_state.activity = other_act.strip() if activity == "Other / general sport" else activity
                        push("sport_support"); st.rerun()

                elif intent == "Cure":
                    st.subheader("Quick safety check")
                    st.caption("Select anything that applies to you right now")
                    flags = [f for f in SAFETY_FLAGS if st.checkbox(f)]
                    if nav():
                        real_flags = [f for f in flags if f != "None of the above"]
                        st.session_state.safety_flags = real_flags
                        push("safety_q_0" if real_flags else 5); st.rerun()

                elif intent == "Lifestyle":
                    st.subheader("What kind of relief are you looking for?")
                    lifestyle = st.radio("", LIFESTYLE_OPTIONS, index=None)
                    if nav(condition=lifestyle is not None):
                        st.session_state.lifestyle_choice = lifestyle; push("ai_check"); st.rerun()

            # ── Safety follow-up ─────────────────────────────────────────────
            elif isinstance(step, str) and step.startswith("safety_q_"):
                idx = int(step.split("_")[-1])
                qs = SAFETY_FOLLOWUP_QUESTIONS
                if idx >= len(qs):
                    push("contact"); st.rerun()
                else:
                    q = qs[idx]
                    st.subheader(q["question"])
                    answer = st.radio("", q["options"], index=None)
                    if nav(condition=answer is not None):
                        st.session_state[q["key"]] = answer
                        next_idx = idx + 1
                        push(f"safety_q_{next_idx}" if next_idx < len(qs) else "contact")
                        st.rerun()

            # ── Step 5: Problem ──────────────────────────────────────────────
            elif step == 5:
                intent = st.session_state.intent
                region = st.session_state.region

                if intent == "Sport":
                    st.subheader("How much support do you want?")
                    support = st.radio("", ["Light","Medium","Maximum"], index=None)
                    st.caption("**Light** — compression & warmth · **Medium** — firm · **Maximum** — heavy duty")
                    if nav("Next →", condition=support is not None):
                        st.session_state.sport_support = support
                        st.session_state.support_mapped = map_support_label(region, support)
                        push("contact"); st.rerun()

                elif intent == "Cure":
                    probs = get_problems_for_region(region)
                    st.subheader("What is the problem?")
                    easy_list = [pb["easy_name"] for pb in probs] if probs else [
                        "General pain / discomfort","Post-injury support","Post-surgery recovery","Chronic condition"]
                    _gender = st.session_state.get("gender", "")
                    _elist = easy_list.copy()
                    if _gender == "Male":
                        _elist = [x for x in _elist if not any(w in x.lower() for w in ["pregnancy","post-delivery","maternity","pregnant"])]
                    elif _gender == "Female":
                        _elist = [x for x in _elist if not any(w in x.lower() for w in ["scrotal","prostate"])]
                    problem = st.radio("", _elist + ["Other — describe your issue","Not sure"], index=None)
                    other_text = ""
                    if problem == "Other — describe your issue":
                        other_text = st.text_input("Describe your problem", placeholder="e.g. knee clicks when walking...")
                    can = problem is not None and (problem != "Other — describe your issue" or other_text.strip())
                    if nav(condition=can):
                        if problem == "Other — describe your issue":
                            st.session_state.problem = other_text.strip()
                            st.session_state.problem_is_freetext = True
                        else:
                            st.session_state.problem = problem
                            st.session_state.problem_is_freetext = False
                        push("sub_location" if region in SUB_LOCATION_QUESTIONS else "region_q_0"); st.rerun()

            # ── Sub-location ─────────────────────────────────────────────────
            elif step == "sub_location":
                region = st.session_state.region
                sub_q  = SUB_LOCATION_QUESTIONS[region]
                _g = st.session_state.get("gender", "")
                _opts = sub_q["options"].copy()
                if _g == "Male":
                    _opts = [o for o in _opts if not any(w in o.lower() for w in ["post-delivery","pregnancy","maternity"])]
                elif _g == "Female":
                    _opts = [o for o in _opts if not any(w in o.lower() for w in ["scrotal"])]
                st.subheader(sub_q["question"])
                answer = st.radio("", _opts, index=None)
                if nav(condition=answer is not None):
                    st.session_state.sub_location = answer
                    if region == "Abdominal":
                        st.session_state.abd_path = answer
                        push("abd_q_0")
                    else:
                        push("severity_q")
                    st.rerun()

            # ── Severity ─────────────────────────────────────────────────────
            elif step == "severity_q":
                st.subheader("How bad is it?")
                severity = st.radio("", ["Mild","Moderate","Severe"], index=None)
                st.caption("**Mild** — manageable · **Moderate** — affects daily activity · **Severe** — very painful")
                if nav(condition=severity is not None):
                    st.session_state.q_severity = severity
                    st.session_state.severity_mapped = map_severity_label(severity)
                    st.session_state.support_mapped = {"Mild":"gentle","Moderate":"firm","Severe":"lock"}[severity]
                    push("ai_check"); st.rerun()

            # ── Region questions ──────────────────────────────────────────────
            elif isinstance(step, str) and step.startswith("region_q_"):
                region = st.session_state.region
                qs = REGION_QUESTIONS.get(region, [])
                idx = int(step.split("_")[-1])
                if idx >= len(qs):
                    push("ai_check"); st.rerun()
                else:
                    q = qs[idx]
                    st.subheader(q["question"])
                    if q.get("caption"): st.caption(q["caption"])
                    answer = st.radio("", q["options"], index=None)
                    if nav(condition=answer is not None):
                        st.session_state[q["key"]] = answer
                        if q["key"] == "q_severity":
                            st.session_state.severity_mapped = map_severity_label(answer)
                        if q["key"] == "q_support":
                            st.session_state.support_mapped = map_support_label(region, answer)
                        next_idx = idx + 1
                        push(f"region_q_{next_idx}" if next_idx < len(qs) else "ai_check")
                        st.rerun()

            # ── Abdominal sub-path ────────────────────────────────────────────
            elif isinstance(step, str) and step.startswith("abd_q_"):
                abd_path = st.session_state.get("abd_path","General abdominal support")
                path_qs  = ABDOMINAL_PATHS.get(abd_path, ABDOMINAL_PATHS["General abdominal support"])
                idx = int(step.split("_")[-1])
                if idx >= len(path_qs):
                    push("ai_check"); st.rerun()
                else:
                    q = path_qs[idx]
                    st.subheader(q["question"])
                    answer = st.radio("", q["options"], index=None)
                    if nav(condition=answer is not None):
                        st.session_state[q["key"]] = answer
                        if "support" in q["key"]:
                            st.session_state.support_mapped = map_support_label("Abdominal", answer)
                        next_idx = idx + 1
                        push(f"abd_q_{next_idx}" if next_idx < len(path_qs) else "ai_check")
                        st.rerun()

            # ── Sport support ─────────────────────────────────────────────────
            elif step == "sport_support":
                st.subheader("How much support do you want?")
                support = st.radio("", ["Light","Medium","Maximum"], index=None)
                st.caption("**Light** — compression & warmth · **Medium** — firm · **Maximum** — heavy duty")
                if nav("Next →", condition=support is not None):
                    st.session_state.sport_support = support
                    st.session_state.support_mapped = map_support_label(st.session_state.region, support)
                    push("ai_check"); st.rerun()

            # ── AI check ─────────────────────────────────────────────────────
            elif step == "ai_check":
                if "ai_flag" not in st.session_state:
                    skeleton_placeholder = st.empty()
                    with skeleton_placeholder.container():
                        st.markdown("✨ Double-checking your answers...")
                        st.markdown('<div class="skeleton" style="width:90%;"></div>', unsafe_allow_html=True)
                        st.markdown('<div class="skeleton" style="width:70%;"></div>', unsafe_allow_html=True)
                    flag, msg = validate_with_ai(dict(st.session_state))
                    st.session_state.ai_flag = flag
                    st.session_state.ai_message = msg
                    skeleton_placeholder.empty()

                if st.session_state.get("ai_message"):
                    st.warning(f"🤔 {st.session_state.ai_message}")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("← Go back and change", use_container_width=True):
                            del st.session_state["ai_flag"]
                            del st.session_state["ai_message"]
                            go_back(); st.rerun()
                    with c2:
                        if st.button("Yes, that's correct →", use_container_width=True, type="primary"):
                            del st.session_state["ai_flag"]
                            del st.session_state["ai_message"]
                            push("contact"); st.rerun()
                else:
                    push("contact"); st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)
