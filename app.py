import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="Casino Persona Quiz",
    page_icon="🎰",
    layout="centered"
)

st.markdown("""
<style>
/* Full-width inputs */
div[data-testid="stNumberInput"],
div[data-testid="stTextInput"],
div[data-testid="stSelectbox"] {
    max-width: 100%;
}

/* Info card grid */
.info-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 12px 0 20px 0;
}
.info-card {
    background: #1e1e2e;
    border: 1px solid #333355;
    border-radius: 10px;
    padding: 8px 16px;
    min-width: 100px;
}
.info-card .label {
    font-size: 11px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 2px;
}
.info-card .value {
    font-size: 15px;
    font-weight: 600;
    color: #eee;
}

/* Balance journey box */
.balance-journey {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 32px;
    background: #111122;
    border-radius: 16px;
    padding: 36px 40px;
    margin: 20px 0;
    flex-wrap: wrap;
    text-align: center;
}
.balance-amount { text-align: center; }
.balance-label {
    font-size: 12px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}
.balance-number {
    font-size: 52px;
    font-weight: 800;
    line-height: 1;
}
.balance-arrow { font-size: 40px; color: #555; }
.balance-diff-label {
    font-size: 12px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}
.balance-diff { font-size: 44px; font-weight: 800; line-height: 1; }

/* Bankrupt */
.bankrupt-box {
    background: #1a0000;
    border: 2px solid #cc0000;
    border-radius: 12px;
    padding: 20px 28px;
    text-align: center;
    margin-top: 12px;
}
.bankrupt-title {
    font-size: 28px; font-weight: 900;
    color: #ff3333; letter-spacing: 0.1em; text-transform: uppercase;
}
.bankrupt-sub { font-size: 14px; color: #cc6666; margin-top: 6px; }

/* Persona card layout */
.persona-reveal {
    display: flex;
    gap: 24px;
    align-items: stretch;
    border-radius: 16px;
    padding: 0;
    margin: 12px 0;
    flex-wrap: wrap;
    overflow: hidden;
}
.persona-left {
    flex: 1;
    min-width: 200px;
    display: flex;
    flex-direction: column;
}
.persona-left-top {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    padding: 28px 28px 20px 28px;
}
.persona-left-bottom {
    padding: 16px 28px 28px 28px;
    border-top: 1px solid #ffffff22;
}
.persona-right {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-width: 180px;
    text-align: center;
    padding: 28px 28px;
}
.persona-name-big {
    font-size: 26px; font-weight: 900;
    line-height: 1.2; margin-top: 16px;
}
.persona-explain {
    font-size: 13px;
    color: #aaa;
    line-height: 1.6;
    margin-top: 4px;
}
.trait-tag {
    display: inline-block;
    background: #ffffff18;
    border-radius: 20px;
    padding: 3px 12px;
    margin: 3px;
    font-size: 13px;
}

/* Card-style step indicator */
.step-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 28px;
}
.step-tab {
    flex: 1;
    padding: 10px 12px;
    font-size: 13px;
    font-weight: 600;
    color: #555;
    border: 1.5px solid #333;
    border-radius: 8px;
    cursor: default;
    text-align: center;
    background: #111;
}
.step-tab .step-num {
    display: block;
    font-size: 11px;
    color: #444;
    margin-bottom: 2px;
    font-weight: 400;
}
.step-tab.active {
    color: #a855f7;
    border-color: #a855f7;
    background: #1a0a2e;
}
.step-tab.active .step-num { color: #a855f7; opacity: 0.7; }
.step-tab.done {
    color: #888;
    border-color: #6b21a8;
    background: #120820;
}
.step-tab.done .step-num { color: #6b21a8; }

/* Chart caption */
.chart-caption {
    font-size: 13px; color: #888;
    margin: -8px 0 12px 0; font-style: italic;
}

/* Right-align button helper */
.right-btn { display: flex; justify-content: flex-end; margin-top: 16px; }
</style>
""", unsafe_allow_html=True)


# ==============================
# Load Dataset
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    return df

df = load_data()


# ==============================
# SVG Persona Illustrations (pose 1 — action)
# ==============================
PERSONA_SVG = {
    "casual": """<svg viewBox="0 0 160 180" xmlns="http://www.w3.org/2000/svg" width="140" height="140">
  <style>line,circle,path,rect,ellipse{stroke:#ccc;stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="80" cy="38" r="22" stroke="#2ecc71"/>
  <path d="M70 42 Q80 52 90 42" stroke="#2ecc71"/>
  <circle cx="73" cy="35" r="2" fill="#2ecc71" stroke="none"/>
  <circle cx="87" cy="35" r="2" fill="#2ecc71" stroke="none"/>
  <line x1="80" y1="60" x2="80" y2="115"/>
  <line x1="80" y1="75" x2="50" y2="95"/>
  <line x1="80" y1="75" x2="110" y2="95"/>
  <rect x="108" y="90" width="12" height="16" rx="3" stroke="#2ecc71"/>
  <line x1="110" y1="90" x2="108" y2="84"/><line x1="118" y1="90" x2="120" y2="84"/>
  <line x1="80" y1="115" x2="58" y2="150"/><line x1="80" y1="115" x2="100" y2="148"/>
  <line x1="58" y1="150" x2="52" y2="165"/><line x1="100" y1="148" x2="108" y2="163"/>
</svg>""",
    "impulsive": """<svg viewBox="0 0 160 180" xmlns="http://www.w3.org/2000/svg" width="140" height="140">
  <style>line,circle,path,rect,ellipse{stroke:#ccc;stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="80" cy="35" r="22" stroke="#e74c3c"/>
  <line x1="68" y1="28" x2="76" y2="32" stroke="#e74c3c"/><line x1="92" y1="28" x2="84" y2="32" stroke="#e74c3c"/>
  <path d="M70 44 L90 44" stroke="#e74c3c"/>
  <line x1="73" y1="44" x2="73" y2="48" stroke="#e74c3c"/><line x1="80" y1="44" x2="80" y2="48" stroke="#e74c3c"/><line x1="87" y1="44" x2="87" y2="48" stroke="#e74c3c"/>
  <line x1="80" y1="57" x2="75" y2="112"/>
  <line x1="80" y1="72" x2="45" y2="58"/><rect x="35" y="48" width="14" height="12" rx="3" stroke="#e74c3c"/>
  <line x1="80" y1="72" x2="115" y2="85"/>
  <line x1="100" y1="100" x2="145" y2="100" stroke="#555"/><line x1="100" y1="100" x2="100" y2="125" stroke="#555"/><line x1="145" y1="100" x2="145" y2="125" stroke="#555"/>
  <line x1="75" y1="112" x2="55" y2="155"/><line x1="75" y1="112" x2="95" y2="155"/>
  <line x1="55" y1="155" x2="48" y2="168"/><line x1="95" y1="155" x2="102" y2="168"/>
</svg>""",
    "rational": """<svg viewBox="0 0 160 180" xmlns="http://www.w3.org/2000/svg" width="140" height="140">
  <style>line,circle,path,rect,ellipse{stroke:#ccc;stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="80" cy="36" r="22" stroke="#3498db"/>
  <rect x="66" y="31" width="12" height="9" rx="2" stroke="#3498db"/><rect x="82" y="31" width="12" height="9" rx="2" stroke="#3498db"/>
  <line x1="78" y1="35" x2="82" y2="35" stroke="#3498db"/>
  <line x1="72" y1="46" x2="88" y2="46" stroke="#3498db"/>
  <line x1="80" y1="58" x2="80" y2="115"/>
  <line x1="80" y1="72" x2="50" y2="90"/><rect x="30" y="82" width="22" height="28" rx="2" stroke="#3498db"/>
  <line x1="35" y1="90" x2="47" y2="90" stroke="#3498db"/><line x1="35" y1="96" x2="47" y2="96" stroke="#3498db"/><line x1="35" y1="102" x2="42" y2="102" stroke="#3498db"/>
  <line x1="80" y1="72" x2="110" y2="88"/><line x1="108" y1="86" x2="118" y2="76" stroke="#3498db"/>
  <line x1="80" y1="115" x2="62" y2="155"/><line x1="80" y1="115" x2="98" y2="155"/>
  <line x1="62" y1="155" x2="56" y2="168"/><line x1="98" y1="155" x2="104" y2="168"/>
</svg>""",
    "addicted": """<svg viewBox="0 0 160 180" xmlns="http://www.w3.org/2000/svg" width="140" height="140">
  <style>line,circle,path,rect,ellipse{stroke:#ccc;stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="80" cy="52" r="22" stroke="#c0392b"/>
  <path d="M70 48 Q73 44 76 48" stroke="#c0392b"/><path d="M84 48 Q87 44 90 48" stroke="#c0392b"/>
  <path d="M72 60 Q80 55 88 60" stroke="#c0392b"/>
  <path d="M58 42 Q50 30 62 25" stroke="#c0392b"/><path d="M102 42 Q110 30 98 25" stroke="#c0392b"/>
  <line x1="80" y1="74" x2="80" y2="118"/>
  <line x1="80" y1="85" x2="52" y2="105"/><line x1="80" y1="85" x2="108" y2="105"/>
  <line x1="40" y1="118" x2="120" y2="118" stroke="#555"/>
  <circle cx="60" cy="115" r="5" stroke="#555"/><circle cx="75" cy="115" r="5" stroke="#555"/>
  <line x1="80" y1="118" x2="65" y2="158"/><line x1="80" y1="118" x2="95" y2="158"/>
  <line x1="65" y1="158" x2="58" y2="170"/><line x1="95" y1="158" x2="102" y2="170"/>
</svg>""",
    "loss_averse": """<svg viewBox="0 0 160 180" xmlns="http://www.w3.org/2000/svg" width="140" height="140">
  <style>line,circle,path,rect,ellipse{stroke:#ccc;stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="80" cy="42" r="20" stroke="#27ae60"/>
  <path d="M70 38 Q73 35 76 38" stroke="#27ae60"/><path d="M84 38 Q87 35 90 38" stroke="#27ae60"/>
  <path d="M74 50 Q80 46 86 50" stroke="#27ae60"/>
  <line x1="80" y1="62" x2="80" y2="112"/>
  <line x1="80" y1="78" x2="58" y2="95"/><line x1="80" y1="78" x2="102" y2="95"/>
  <circle cx="56" cy="98" r="5" stroke="#27ae60"/><circle cx="65" cy="95" r="5" stroke="#27ae60"/>
  <line x1="80" y1="112" x2="68" y2="155"/><line x1="80" y1="112" x2="92" y2="155"/>
  <line x1="68" y1="155" x2="63" y2="168"/><line x1="92" y1="155" x2="97" y2="168"/>
</svg>""",
    "analytical": """<svg viewBox="0 0 160 180" xmlns="http://www.w3.org/2000/svg" width="140" height="140">
  <style>line,circle,path,rect,ellipse{stroke:#ccc;stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="80" cy="36" r="22" stroke="#2980b9"/>
  <circle cx="73" cy="33" r="3" stroke="#2980b9"/><circle cx="87" cy="33" r="3" stroke="#2980b9"/>
  <line x1="73" y1="46" x2="87" y2="46" stroke="#2980b9"/>
  <line x1="80" y1="58" x2="80" y2="112"/>
  <line x1="80" y1="75" x2="48" y2="88"/>
  <rect x="18" y="70" width="34" height="34" rx="2" stroke="#2980b9"/>
  <polyline points="24,96 30,82 36,88 42,74" stroke="#2980b9"/>
  <line x1="80" y1="75" x2="112" y2="88"/>
  <rect x="108" y="84" width="18" height="24" rx="3" stroke="#2980b9"/>
  <line x1="112" y1="90" x2="122" y2="90" stroke="#2980b9"/><line x1="112" y1="96" x2="122" y2="96" stroke="#2980b9"/>
  <line x1="80" y1="112" x2="62" y2="155"/><line x1="80" y1="112" x2="98" y2="155"/>
  <line x1="62" y1="155" x2="56" y2="168"/><line x1="98" y1="155" x2="104" y2="168"/>
</svg>""",
    "social": """<svg viewBox="0 0 160 180" xmlns="http://www.w3.org/2000/svg" width="140" height="140">
  <style>line,circle,path,rect,ellipse{stroke:#ccc;stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="80" cy="36" r="22" stroke="#e67e22"/>
  <path d="M68 44 Q80 56 92 44" stroke="#e67e22"/>
  <path d="M70 32 Q73 28 76 32" stroke="#e67e22"/><path d="M84 32 Q87 28 90 32" stroke="#e67e22"/>
  <line x1="80" y1="58" x2="80" y2="112"/>
  <line x1="80" y1="70" x2="48" y2="48"/><line x1="80" y1="70" x2="112" y2="48"/>
  <circle cx="30" cy="70" r="12" stroke="#888"/>
  <line x1="30" y1="82" x2="30" y2="110" stroke="#888"/><line x1="30" y1="90" x2="18" y2="100" stroke="#888"/><line x1="30" y1="90" x2="42" y2="100" stroke="#888"/>
  <circle cx="130" cy="70" r="12" stroke="#888"/>
  <line x1="130" y1="82" x2="130" y2="110" stroke="#888"/><line x1="130" y1="90" x2="118" y2="100" stroke="#888"/><line x1="130" y1="90" x2="142" y2="100" stroke="#888"/>
  <line x1="80" y1="112" x2="62" y2="152"/><line x1="80" y1="112" x2="98" y2="152"/>
  <line x1="62" y1="152" x2="56" y2="166"/><line x1="98" y1="152" x2="104" y2="166"/>
</svg>""",
    "superstitious": """<svg viewBox="0 0 160 180" xmlns="http://www.w3.org/2000/svg" width="140" height="140">
  <style>line,circle,path,rect,ellipse{stroke:#ccc;stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="80" cy="40" r="22" stroke="#8e44ad"/>
  <line x1="70" y1="37" x2="77" y2="37" stroke="#8e44ad"/><line x1="83" y1="37" x2="90" y2="37" stroke="#8e44ad"/>
  <path d="M73 48 Q80 54 87 48" stroke="#8e44ad"/>
  <line x1="80" y1="62" x2="80" y2="115"/>
  <line x1="80" y1="75" x2="68" y2="95"/><line x1="80" y1="75" x2="92" y2="95"/>
  <ellipse cx="80" cy="98" rx="13" ry="8" stroke="#8e44ad"/>
  <line x1="48" y1="22" x2="48" y2="30" stroke="#8e44ad"/><line x1="44" y1="26" x2="52" y2="26" stroke="#8e44ad"/>
  <line x1="112" y1="18" x2="112" y2="26" stroke="#8e44ad"/><line x1="108" y1="22" x2="116" y2="22" stroke="#8e44ad"/>
  <line x1="100" y1="8" x2="100" y2="14" stroke="#8e44ad"/><line x1="97" y1="11" x2="103" y2="11" stroke="#8e44ad"/>
  <path d="M60 28 Q80 10 100 28" stroke="#8e44ad" stroke-dasharray="3,3"/>
  <line x1="80" y1="115" x2="62" y2="155"/><line x1="80" y1="115" x2="98" y2="155"/>
  <line x1="62" y1="155" x2="56" y2="168"/><line x1="98" y1="155" x2="104" y2="168"/>
</svg>"""
}

# ==============================
# SVG Persona Illustrations (pose 2 — comparison/ranking context)
# ==============================
PERSONA_SVG_2 = {
    "casual": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect{stroke:#2ecc71;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <path d="M52 32 Q60 40 68 32"/>
  <circle cx="55" cy="25" r="1.5" fill="#2ecc71" stroke="none"/>
  <circle cx="65" cy="25" r="1.5" fill="#2ecc71" stroke="none"/>
  <!-- walking away relaxed -->
  <line x1="60" y1="46" x2="60" y2="90"/>
  <line x1="60" y1="58" x2="38" y2="72"/>
  <line x1="60" y1="58" x2="82" y2="68"/>
  <!-- hand waving goodbye -->
  <line x1="82" y1="68" x2="92" y2="58"/>
  <line x1="92" y1="58" x2="96" y2="52"/><line x1="92" y1="58" x2="98" y2="60"/>
  <line x1="60" y1="90" x2="46" y2="118"/>
  <line x1="60" y1="90" x2="74" y2="118"/>
</svg>""",
    "impulsive": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect{stroke:#e74c3c;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <line x1="50" y1="22" x2="57" y2="26"/><line x1="70" y1="22" x2="63" y2="26"/>
  <path d="M52 36 L68 36"/>
  <!-- slamming fists on table -->
  <line x1="60" y1="46" x2="58" y2="85"/>
  <line x1="60" y1="58" x2="30" y2="72"/><line x1="60" y1="58" x2="90" y2="72"/>
  <rect x="20" y="86" width="80" height="8" rx="2"/>
  <line x1="32" y1="72" x2="28" y2="86"/><line x1="88" y1="72" x2="92" y2="86"/>
  <line x1="58" y1="85" x2="44" y2="118"/><line x1="58" y1="85" x2="72" y2="118"/>
</svg>""",
    "rational": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect{stroke:#3498db;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <rect x="50" y="23" width="9" height="7" rx="1.5"/><rect x="61" y="23" width="9" height="7" rx="1.5"/>
  <line x1="59" y1="26" x2="61" y2="26"/>
  <line x1="54" y1="36" x2="66" y2="36"/>
  <!-- arms crossed confidently -->
  <line x1="60" y1="46" x2="60" y2="92"/>
  <line x1="60" y1="60" x2="38" y2="52"/>
  <line x1="60" y1="60" x2="82" y2="52"/>
  <line x1="38" y1="52" x2="78" y2="68"/>
  <line x1="82" y1="52" x2="42" y2="68"/>
  <line x1="60" y1="92" x2="46" y2="118"/><line x1="60" y1="92" x2="74" y2="118"/>
</svg>""",
    "addicted": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect{stroke:#c0392b;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="32" r="18"/>
  <path d="M52 30 Q55 26 58 30"/><path d="M62 30 Q65 26 68 30"/>
  <path d="M54 40 Q60 36 66 40"/>
  <!-- collapsed on knees -->
  <line x1="60" y1="50" x2="60" y2="82"/>
  <line x1="60" y1="62" x2="38" y2="74"/><line x1="60" y1="62" x2="82" y2="74"/>
  <!-- on knees -->
  <line x1="60" y1="82" x2="42" y2="100"/><line x1="60" y1="82" x2="78" y2="100"/>
  <line x1="42" y1="100" x2="34" y2="100"/><line x1="78" y1="100" x2="86" y2="100"/>
  <!-- empty wallet on floor -->
  <rect x="48" y="108" width="24" height="14" rx="3"/>
  <line x1="54" y1="108" x2="54" y2="122"/><line x1="66" y1="108" x2="66" y2="122"/>
</svg>""",
    "loss_averse": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect{stroke:#27ae60;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <path d="M52 26 Q55 23 58 26"/><path d="M62 26 Q65 23 68 26"/>
  <path d="M54 36 Q60 32 66 36"/>
  <!-- peeking around corner nervously -->
  <line x1="60" y1="46" x2="60" y2="92"/>
  <line x1="60" y1="58" x2="40" y2="70"/><line x1="60" y1="58" x2="76" y2="64"/>
  <!-- peeking hand -->
  <line x1="76" y1="64" x2="86" y2="56"/>
  <line x1="60" y1="92" x2="48" y2="118"/><line x1="60" y1="92" x2="72" y2="118"/>
  <!-- shield/barrier -->
  <path d="M90 40 Q100 50 90 70" stroke-dasharray="3,2"/>
</svg>""",
    "analytical": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect,polyline{stroke:#2980b9;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <circle cx="54" cy="25" r="2.5"/><circle cx="66" cy="25" r="2.5"/>
  <line x1="54" y1="35" x2="66" y2="35"/>
  <!-- pointing at floating chart -->
  <line x1="60" y1="46" x2="60" y2="92"/>
  <line x1="60" y1="60" x2="36" y2="72"/><line x1="60" y1="60" x2="84" y2="52"/>
  <line x1="84" y1="52" x2="96" y2="44"/>
  <!-- mini bar chart floating -->
  <rect x="22" y="56" width="8" height="22" rx="1"/>
  <rect x="32" y="62" width="8" height="16" rx="1"/>
  <rect x="42" y="50" width="8" height="28" rx="1"/>
  <line x1="60" y1="92" x2="46" y2="118"/><line x1="60" y1="92" x2="74" y2="118"/>
</svg>""",
    "social": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect{stroke:#e67e22;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <path d="M50 34 Q60 44 70 34"/>
  <path d="M52 24 Q55 20 58 24"/><path d="M62 24 Q65 20 68 24"/>
  <!-- chatting with someone -->
  <line x1="60" y1="46" x2="60" y2="90"/>
  <line x1="60" y1="58" x2="38" y2="50"/><line x1="60" y1="58" x2="84" y2="66"/>
  <!-- speech bubble -->
  <path d="M68 20 Q85 14 88 26 Q91 38 78 40 L72 46 L76 38 Q63 38 64 28 Q65 18 68 20Z"/>
  <line x1="60" y1="90" x2="46" y2="116"/><line x1="60" y1="90" x2="74" y2="116"/>
</svg>""",
    "superstitious": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect,ellipse{stroke:#8e44ad;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <line x1="52" y1="25" x2="58" y2="25"/><line x1="62" y1="25" x2="68" y2="25"/>
  <path d="M54 36 Q60 42 66 36"/>
  <!-- blowing on dice for luck -->
  <line x1="60" y1="46" x2="60" y2="90"/>
  <line x1="60" y1="58" x2="38" y2="70"/><line x1="60" y1="58" x2="82" y2="54"/>
  <line x1="82" y1="54" x2="96" y2="46"/>
  <!-- dice -->
  <rect x="88" y="32" width="20" height="20" rx="3"/>
  <circle cx="94" cy="38" r="2" fill="#8e44ad" stroke="none"/>
  <circle cx="102" cy="46" r="2" fill="#8e44ad" stroke="none"/>
  <!-- puff of air -->
  <path d="M78 50 Q86 44 96 44" stroke-dasharray="2,2"/>
  <line x1="60" y1="90" x2="46" y2="116"/><line x1="60" y1="90" x2="74" y2="116"/>
</svg>"""
}

# ==============================
# SVG Persona Illustrations (pose 3 — aftermath/consequence)
# ==============================
PERSONA_SVG_3 = {
    "casual": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect{stroke:#2ecc71;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <path d="M52 32 Q60 40 68 32"/>
  <circle cx="55" cy="25" r="1.5" fill="#2ecc71" stroke="none"/>
  <circle cx="65" cy="25" r="1.5" fill="#2ecc71" stroke="none"/>
  <!-- sitting relaxed on chair -->
  <line x1="60" y1="46" x2="60" y2="88"/>
  <line x1="60" y1="60" x2="40" y2="70"/>
  <line x1="60" y1="60" x2="80" y2="70"/>
  <!-- chair -->
  <line x1="38" y1="88" x2="82" y2="88"/>
  <line x1="38" y1="88" x2="38" y2="108"/><line x1="82" y1="88" x2="82" y2="108"/>
  <line x1="60" y1="88" x2="50" y2="112"/><line x1="60" y1="88" x2="70" y2="112"/>
  <!-- coin toss in air -->
  <circle cx="90" cy="50" r="6"/>
  <line x1="90" y1="44" x2="90" y2="36"/>
</svg>""",
    "impulsive": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect{stroke:#e74c3c;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <line x1="50" y1="22" x2="57" y2="26"/><line x1="70" y1="22" x2="63" y2="26"/>
  <path d="M52 38 L68 38"/>
  <!-- collapsed sideways on floor -->
  <line x1="60" y1="46" x2="55" y2="88"/>
  <line x1="58" y1="62" x2="35" y2="55"/><line x1="58" y1="62" x2="75" y2="72"/>
  <!-- lying legs -->
  <line x1="55" y1="88" x2="30" y2="100"/>
  <line x1="55" y1="88" x2="50" y2="110"/>
  <!-- empty wallet on ground -->
  <rect x="22" y="108" width="20" height="12" rx="2"/>
  <line x1="27" y1="108" x2="27" y2="120"/><line x1="37" y1="108" x2="37" y2="120"/>
</svg>""",
    "rational": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect{stroke:#3498db;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <rect x="50" y="23" width="9" height="7" rx="1.5"/><rect x="61" y="23" width="9" height="7" rx="1.5"/>
  <line x1="59" y1="26" x2="61" y2="26"/>
  <line x1="54" y1="36" x2="66" y2="36"/>
  <!-- writing notes at desk -->
  <line x1="60" y1="46" x2="60" y2="88"/>
  <line x1="60" y1="60" x2="38" y2="72"/><line x1="60" y1="60" x2="82" y2="68"/>
  <!-- desk -->
  <line x1="20" y1="88" x2="100" y2="88"/>
  <line x1="20" y1="88" x2="20" y2="108"/><line x1="100" y1="88" x2="100" y2="108"/>
  <!-- notepad on desk -->
  <rect x="65" y="78" width="22" height="14" rx="2"/>
  <line x1="68" y1="83" x2="84" y2="83"/><line x1="68" y1="87" x2="80" y2="87"/>
  <line x1="60" y1="88" x2="48" y2="112"/><line x1="60" y1="88" x2="72" y2="112"/>
</svg>""",
    "addicted": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect{stroke:#c0392b;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="30" r="18"/>
  <path d="M52 28 Q55 24 58 28"/><path d="M62 28 Q65 24 68 28"/>
  <path d="M52 40 Q60 34 68 40"/>
  <!-- crawling on floor desperate -->
  <line x1="60" y1="48" x2="52" y2="80"/>
  <line x1="58" y1="62" x2="36" y2="54"/>
  <line x1="58" y1="62" x2="74" y2="72"/>
  <!-- on all fours reaching for chips -->
  <line x1="52" y1="80" x2="28" y2="92"/>
  <line x1="52" y1="80" x2="58" y2="100"/>
  <line x1="28" y1="92" x2="22" y2="82"/>
  <!-- scattered chips on floor -->
  <circle cx="18" cy="80" r="4"/>
  <circle cx="30" cy="108" r="4"/>
  <circle cx="10" cy="96" r="4"/>
</svg>""",
    "loss_averse": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect{stroke:#27ae60;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <path d="M52 26 Q55 22 58 26"/><path d="M62 26 Q65 22 68 26"/>
  <line x1="54" y1="36" x2="66" y2="36"/>
  <!-- hugging self, relieved left early -->
  <line x1="60" y1="46" x2="60" y2="92"/>
  <line x1="60" y1="60" x2="40" y2="52"/>
  <line x1="60" y1="60" x2="80" y2="52"/>
  <line x1="40" y1="52" x2="76" y2="68"/>
  <line x1="80" y1="52" x2="44" y2="68"/>
  <!-- small checkmark -->
  <path d="M82 30 L88 38 L100 22" stroke="#27ae60" stroke-width="2.5"/>
  <line x1="60" y1="92" x2="46" y2="118"/><line x1="60" y1="92" x2="74" y2="118"/>
</svg>""",
    "analytical": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect,polyline{stroke:#2980b9;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <circle cx="54" cy="25" r="2.5"/><circle cx="66" cy="25" r="2.5"/>
  <line x1="54" y1="35" x2="66" y2="35"/>
  <!-- reviewing results on tablet -->
  <line x1="60" y1="46" x2="60" y2="90"/>
  <line x1="60" y1="62" x2="38" y2="74"/><line x1="60" y1="62" x2="82" y2="58"/>
  <!-- tablet in both hands -->
  <rect x="78" y="44" width="28" height="36" rx="3"/>
  <polyline points="82,72 86,60 90,66 94,54 98,58"/>
  <line x1="60" y1="90" x2="46" y2="116"/><line x1="60" y1="90" x2="74" y2="116"/>
</svg>""",
    "social": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect{stroke:#e67e22;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <path d="M50 34 Q60 44 70 34"/>
  <path d="M52 24 Q55 20 58 24"/><path d="M62 24 Q65 20 68 24"/>
  <!-- on phone texting friends -->
  <line x1="60" y1="46" x2="60" y2="90"/>
  <line x1="60" y1="62" x2="40" y2="54"/><line x1="60" y1="62" x2="82" y2="68"/>
  <!-- phone in right hand -->
  <rect x="80" y="54" width="14" height="22" rx="3"/>
  <line x1="83" y1="60" x2="91" y2="60"/><line x1="83" y1="65" x2="91" y2="65"/>
  <line x1="60" y1="90" x2="46" y2="116"/><line x1="60" y1="90" x2="74" y2="116"/>
</svg>""",
    "superstitious": """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" width="110" height="110">
  <style>line,circle,path,rect,ellipse{stroke:#8e44ad;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round;}</style>
  <circle cx="60" cy="28" r="18"/>
  <line x1="52" y1="25" x2="58" y2="25"/><line x1="62" y1="25" x2="68" y2="25"/>
  <path d="M52 38 Q60 34 68 38"/>
  <!-- kneeling and praying after loss -->
  <line x1="60" y1="46" x2="60" y2="82"/>
  <line x1="60" y1="60" x2="42" y2="70"/><line x1="60" y1="60" x2="78" y2="70"/>
  <ellipse cx="60" cy="74" rx="18" ry="8"/>
  <!-- kneeling legs -->
  <line x1="60" y1="82" x2="38" y2="96"/>
  <line x1="60" y1="82" x2="82" y2="96"/>
  <line x1="38" y1="96" x2="30" y2="96"/><line x1="82" y1="96" x2="90" y2="96"/>
  <!-- broken star above -->
  <line x1="60" y1="8" x2="60" y2="16" stroke-dasharray="2,2"/>
  <line x1="54" y1="12" x2="66" y2="12" stroke-dasharray="2,2"/>
</svg>"""
}
def generate_story(age, gender, job, outfit, mood, reason):
    job_str = job if job else "professional"
    gender_str  = "He" if gender == "Male" else "She" if gender == "Female" else "They"
    gender_str2 = "his" if gender == "Male" else "her" if gender == "Female" else "their"

    openings = [
        f"A {age}-year-old {job_str} pushed open the casino doors tonight.",
        f"Tonight's visitor: a {age}-year-old whose day job was {job_str}.",
        f"At {age}, working as a {job_str}, {gender_str.lower()} decided tonight was the night.",
        f"{gender_str} was {age}, a {job_str} by day — but tonight was different.",
        f"Not everyone walks into a casino with a plan. This {age}-year-old {job_str} was one of them.",
    ]
    mood_lines = {
        "Happy":       [f"{gender_str} was in a genuinely good mood — the kind that makes everything feel possible.",
                        f"Something had gone right today, and {gender_str.lower()} was riding that feeling all the way here."],
        "Stressed":    [f"The week had been relentless. {gender_str} needed something — anything — to switch off.",
                        f"Work had piled up, and {gender_str2} head was full. The casino noise felt almost soothing."],
        "Excited":     [f"There was something electric in the air, and {gender_str} had felt it all day.",
                        f"The anticipation had been building since morning. {gender_str} was practically buzzing walking in."],
        "Anxious":     [f"{gender_str} wasn't sure why {gender_str.lower()} came. {gender_str2} hands were already a little cold.",
                        f"Part of {gender_str2} wanted to turn around. The other part kept walking toward the tables."],
        "Bored":       [f"It wasn't really a plan — more like something to do on a night that had nothing else going on.",
                        f"Nothing on TV, no one to call. The casino was at least something different."],
        "Celebrating": [f"Tonight was a celebration, and {gender_str} wanted somewhere that matched the energy.",
                        f"Something good had happened — the kind of thing worth marking properly."],
        "Normal":      [f"Nothing special had happened today. {gender_str} just felt like doing something a little different.",
                        f"{gender_str} wasn't chasing anything in particular. Just a night out."],
    }
    reason_lines = {
        "Just for fun":      [f"{gender_str} wasn't here to get rich. Just to have a good time.",
                              f"No pressure, no plan. Just {gender_str2} and the games."],
        "With friends":      [f"The friends were somewhere nearby, probably already arguing over which table to hit first.",
                              f"The company mattered more than the games. {gender_str} was just here to be part of the night."],
        "Want to win money": [f"There was a number in {gender_str2} head — a target. {gender_str} wasn't leaving until {gender_str.lower()} hit it.",
                              f"This wasn't about fun. This was about walking out ahead."],
        "Need to escape":    [f"The outside world could wait. {gender_str} just needed to be somewhere that wasn't real life.",
                              f"{gender_str} wasn't running away — just pausing. At least, that's what {gender_str.lower()} told {gender_str2}self."],
        "Celebrating":       [f"Tonight was about marking the moment — somewhere that felt alive.",
                              f"{gender_str} was treating {gender_str2}self. {gender_str} had earned it."],
        "First time":        [f"{gender_str} had never done this before. Everything was new.",
                              f"{gender_str} looked around slowly, taking it all in. {gender_str2} first casino."],
        "Just broke up":     [f"The breakup was fresh. {gender_str} needed somewhere loud enough to drown out the thoughts.",
                              f"Some people call friends after a breakup. {gender_str} came here instead."],
        "For vacation":      [f"{gender_str} was on vacation and figured: why not? It was practically required.",
                              f"Vacation meant doing things you wouldn't normally do. This qualified."],
    }
    outfit_lines_with    = [f"{gender_str} had put on {outfit} — whether for luck or just because it felt right.",
                             f"{gender_str} straightened {gender_str2} {outfit} at the entrance and walked in."]
    outfit_lines_without = [f"{gender_str} hadn't dressed up. Didn't feel the need to.",
                             f"Just casual tonight — no fuss, no ceremony."]

    return [
        random.choice(openings),
        random.choice(mood_lines.get(mood, mood_lines["Normal"])),
        random.choice(reason_lines.get(reason, reason_lines["Just for fun"])),
        random.choice(outfit_lines_with if outfit else outfit_lines_without),
    ]


# ==============================
# Persona Info
# ==============================
persona_info = {
    "casual":        {"emoji": "😊", "name": "The Casual Player",      "color": "#2ecc71",
                      "description": "You're here for the experience, not the money. You play conservatively, enjoy the atmosphere, and know when to walk away.",
                      "traits": ["Low average bet", "Leaves early", "Not affected by losses", "Prefers low-risk games"], "risk_level": "🟢 Low Risk"},
    "impulsive":     {"emoji": "🔥", "name": "The Impulsive Player",    "color": "#e74c3c",
                      "description": "Emotions drive every decision. You chase losses, go all-in when frustrated, and ride the highs of winning streaks.",
                      "traits": ["High bets after losses", "Chases losses", "Emotionally driven", "Almost never leaves voluntarily"], "risk_level": "🔴 High Risk"},
    "rational":      {"emoji": "🧠", "name": "The Rational Player",     "color": "#3498db",
                      "description": "You came with a plan and you'll stick to it. Stop-loss and take-profit rules guide every decision.",
                      "traits": ["Fixed bet amounts", "Strict stop-loss rules", "Unaffected by streaks", "Leaves at planned thresholds"], "risk_level": "🟡 Moderate Risk"},
    "addicted":      {"emoji": "😰", "name": "The Compulsive Player",   "color": "#c0392b",
                      "description": "You know you should stop, but you can't. Every loss feels like it's just one win away from being fixed.",
                      "traits": ["Can't leave voluntarily", "Always 'one more round'", "Escalating bets", "Plays until broke"], "risk_level": "🔴 Very High Risk"},
    "loss_averse":   {"emoji": "😟", "name": "The Loss Averse Player",  "color": "#27ae60",
                      "description": "Losing hurts more than winning feels good. You play with extreme caution and leave at the first sign of trouble.",
                      "traits": ["Minimum bets only", "Leaves after small losses", "Very anxious when losing", "Rarely takes risks"], "risk_level": "🟢 Very Low Risk"},
    "analytical":    {"emoji": "📊", "name": "The Analytical Player",   "color": "#2980b9",
                      "description": "You track patterns, calculate odds, and make data-driven decisions. You believe skill can beat the house.",
                      "traits": ["Pattern tracking", "Prefers skill-based games", "Methodical betting", "Exits when model says so"], "risk_level": "🟡 Moderate Risk"},
    "social":        {"emoji": "🎉", "name": "The Social Player",       "color": "#e67e22",
                      "description": "The casino is a social venue for you. Games are just the backdrop for conversations and good vibes.",
                      "traits": ["Influenced by others", "Prefers lively tables", "Inconsistent bets", "Leaves when bored"], "risk_level": "🟠 Moderate-High Risk"},
    "superstitious": {"emoji": "🔮", "name": "The Superstitious Player","color": "#8e44ad",
                      "description": "Signs, omens, and rituals guide your play. You're always one round away from the universe delivering your win.",
                      "traits": ["Ritual-based decisions", "Believes in streaks", "Rarely leaves", "High variance bets"], "risk_level": "🔴 High Risk"},
}

# one-liner for comparison section
PERSONA_TAGLINE = {
    "casual":        "Plays it cool.",
    "impulsive":     "All or nothing.",
    "rational":      "Sticks to the plan.",
    "addicted":      "Can't stop, won't stop.",
    "loss_averse":   "Better safe than sorry.",
    "analytical":    "The odds say so.",
    "social":        "Here for the vibes.",
    "superstitious": "The stars align.",
}


# ==============================
# Scoring Logic
# ==============================
def map_answers_to_persona(q1, q2, q3, q4, q5):
    scores = {p: 0 for p in persona_info.keys()}
    q1_map = {"Just for fun": {"casual": 2, "social": 1}, "Win big": {"impulsive": 2, "addicted": 1},
              "Test strategy": {"rational": 1, "analytical": 2}, "Escape from stress": {"impulsive": 1, "addicted": 2}}
    q2_map = {"Shake it off": {"casual": 2}, "Win it back NOW": {"impulsive": 2, "addicted": 1},
              "Check stop-loss": {"rational": 2}, "Start to panic": {"loss_averse": 2}}
    q3_map = {"Cash out & leave": {"rational": 2, "casual": 1}, "Go all in": {"impulsive": 2, "addicted": 1},
              "Wait and watch": {"analytical": 2}, "Spread the bets": {"rational": 1, "analytical": 1}}
    q4_map = {"Walk away": {"casual": 1, "rational": 2, "loss_averse": 1}, "Hit the ATM": {"addicted": 3},
              "One last big bet": {"impulsive": 2, "addicted": 1}, "Do the math": {"analytical": 2}}
    q5_map = {"Feeling lucky 🍀": {"superstitious": 2}, "Just average": {"casual": 1, "rational": 1},
              "Big win incoming 🔮": {"superstitious": 3}, "Luck? It's all skill": {"analytical": 2, "rational": 1}}
    for q, q_map in [(q1, q1_map), (q2, q2_map), (q3, q3_map), (q4, q4_map), (q5, q5_map)]:
        if q in q_map:
            for p, s in q_map[q].items():
                scores[p] += s
    return max(scores, key=scores.get), scores


# ==============================
# Get Random Player
# ==============================
def get_random_player(persona, df):
    ids = df[df['persona'] == persona]['player_id'].unique()
    sid = random.choice(ids)
    return df[df['player_id'] == sid].copy(), sid


# ==============================
# App State
# ==============================
for key, default in [('step', 1), ('profile', {}), ('results', None)]:
    if key not in st.session_state:
        st.session_state[key] = default


# ==============================
# Step Indicator — tab style
# ==============================
def step_tabs(current):
    steps = ["About You", "Quick Quiz", "Results"]
    html = '<div class="step-tabs">'
    for i, label in enumerate(steps, 1):
        cls = "active" if i == current else ("done" if i < current else "")
        html += f'<div class="step-tab {cls}"><span class="step-num">{i}.</span>{label}</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ==============================
# STEP 1 — Profile
# ==============================
if st.session_state.step == 1:
    st.title("🎰 What's Your Casino Persona?")
    st.markdown("*Based on behavioral patterns from 360 AI-simulated casino players across 8 personality types.*")
    st.markdown("---")
    step_tabs(1)

    st.subheader("👤 Tell us about yourself")

    age    = st.number_input("Age", min_value=18, max_value=99, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Non-binary / Other"])
    job    = st.text_input("Occupation", placeholder="e.g. engineer, teacher...")
    budget = st.number_input("💵 Budget tonight ($)", min_value=20, max_value=5000, value=100, step=10)
    outfit = st.text_input("👗 What are you wearing?", placeholder="e.g. my lucky red jacket...")
    mood   = st.selectbox("😊 How are you feeling tonight?",
                          ["Normal", "Happy", "Stressed", "Excited", "Anxious", "Bored", "Celebrating"])
    reason = st.selectbox("🎯 Why are you visiting?",
                          ["Just for fun", "With friends", "Want to win money",
                           "Need to escape", "Celebrating", "First time", "Just broke up", "For vacation"])

    st.markdown("")
    _, btn_col = st.columns([3, 1])
    with btn_col:
        if st.button("Next →", type="primary", use_container_width=True):
            st.session_state.profile = {
                'age': age, 'gender': gender, 'job': job,
                'budget': budget, 'outfit': outfit, 'mood': mood, 'reason': reason
            }
            st.session_state.step = 2
            st.rerun()


# ==============================
# STEP 2 — Quiz
# ==============================
elif st.session_state.step == 2:
    st.title("🎰 What's Your Casino Persona?")
    st.markdown("---")
    step_tabs(2)

    st.subheader("🎲 5 Quick Questions")
    st.markdown("Pick the answer that feels most like you.")
    st.markdown("")

    q1 = st.radio("**Q1. What are you here for tonight?**",
                  ["Just for fun", "Win big", "Test strategy", "Escape from stress"], index=None)
    st.markdown("")
    q2 = st.radio("**Q2. Lost 3 rounds in a row. You...**",
                  ["Shake it off", "Win it back NOW", "Check stop-loss", "Start to panic"], index=None)
    st.markdown("")
    q3 = st.radio("**Q3. Just doubled your money. You...**",
                  ["Cash out & leave", "Go all in", "Wait and watch", "Spread the bets"], index=None)
    st.markdown("")
    q4 = st.radio("**Q4. Almost out of money. You...**",
                  ["Walk away", "Hit the ATM", "One last big bet", "Do the math"], index=None)
    st.markdown("")
    q5 = st.radio("**Q5. How's your luck tonight?**",
                  ["Feeling lucky 🍀", "Just average", "Big win incoming 🔮", "Luck? It's all skill"], index=None)

    st.markdown("")
    col_back, col_gap, col_submit = st.columns([1, 2, 2])
    with col_back:
        if st.button("← Back"):
            st.session_state.step = 1
            st.rerun()
    with col_submit:
        if st.button("🎲 Reveal My Casino Persona", type="primary", use_container_width=True):
            if not all([q1, q2, q3, q4, q5]):
                st.error("⚠️ Please answer all 5 questions before continuing.")
            else:
                p = st.session_state.profile
                persona, scores = map_answers_to_persona(q1, q2, q3, q4, q5)
                player_df, pid  = get_random_player(persona, df)
                story = generate_story(p['age'], p['gender'], p['job'],
                                       p['outfit'], p['mood'], p['reason'])
                st.session_state.results = {'persona': persona, 'scores': scores,
                                            'player_df': player_df, 'story': story}
                st.session_state.step = 3
                st.rerun()


# ==============================
# STEP 3 — Results
# ==============================
elif st.session_state.step == 3:
    results   = st.session_state.results
    profile   = st.session_state.profile
    persona   = results['persona']
    player_df = results['player_df']
    story     = results['story']
    info      = persona_info[persona]

    initial_balance = player_df['initial_balance'].iloc[0]
    final_balance   = player_df['balance'].iloc[-1]
    net_profit      = final_balance - initial_balance
    total_rounds    = len(player_df)
    win_rate        = player_df['is_win'].mean()
    is_bankrupt     = final_balance <= 0

    st.balloons()

    # ── Header ──────────────────────────────────────
    st.title("🎰 Your Casino Night")
    st.markdown("---")
    step_tabs(3)

    # ── Personal Info Cards ─────────────────────────
    p = profile
    st.markdown(f"""
    <div class="info-cards">
        <div class="info-card"><div class="label">You're a...</div>
            <div class="value">{p['age']}-year-old {p['job'] if p['job'] else '—'}</div></div>
        <div class="info-card"><div class="label">Tonight's Budget</div>
            <div class="value">${p['budget']}</div></div>
        <div class="info-card"><div class="label">Wearing</div>
            <div class="value">{p['outfit'] if p['outfit'] else '—'}</div></div>
        <div class="info-card"><div class="label">Feeling</div>
            <div class="value">{p['mood']}</div></div>
        <div class="info-card"><div class="label">Here to</div>
            <div class="value">{p['reason']}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Story ────────────────────────────────────────
    st.subheader("📖 Your Story Tonight...")
    story_html = "<br>".join(story)
    st.markdown(f'<div style="background:#1a1f3a;border-left:4px solid #3b4fd8;border-radius:6px;padding:16px 20px;font-size:15px;line-height:1.8;color:#c8d0f0;">{story_html}</div>', unsafe_allow_html=True)
    st.markdown("---")

    # ── Your Results ─────────────────────────────────
    st.subheader("🎯 Your Results")
    init_color  = "#aaaaaa"
    final_color = "#2ecc71" if net_profit >= 0 else "#e74c3c"
    diff_sign   = "+" if net_profit >= 0 else ""
    diff_color  = "#2ecc71" if net_profit >= 0 else "#e74c3c"
    final_str   = f"${final_balance:.0f}" if not is_bankrupt else "$0"

    st.markdown(f"""
    <div class="balance-journey">
        <div class="balance-amount">
            <div class="balance-label">Starting Budget</div>
            <div class="balance-number" style="color:{init_color};">${initial_balance:.0f}</div>
        </div>
        <div class="balance-arrow">→</div>
        <div class="balance-amount">
            <div class="balance-label">Final Balance</div>
            <div class="balance-number" style="color:{final_color};">{final_str}</div>
        </div>
        <div class="balance-amount">
            <div class="balance-diff-label">Result</div>
            <div class="balance-diff" style="color:{diff_color};">{diff_sign}{net_profit:.0f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if is_bankrupt:
        st.markdown("""
        <div class="bankrupt-box">
            <div style="font-size:42px;">💸</div>
            <div class="bankrupt-title">BROKE. BUSTED. BANKRUPT.</div>
            <div class="bankrupt-sub">Every last chip is gone. The house always wins.</div>
        </div>""", unsafe_allow_html=True)

    # Rounds + Win Rate — same style box as balance journey
    st.markdown(f"""
    <div class="balance-journey" style="padding:20px 40px;">
        <div class="balance-amount">
            <div class="balance-label">Rounds Played</div>
            <div class="balance-number" style="color:#cccccc;font-size:42px;">{total_rounds}</div>
        </div>
        <div style="width:1px;height:50px;background:#333;"></div>
        <div class="balance-amount">
            <div class="balance-label">Win Rate</div>
            <div class="balance-number" style="color:#cccccc;font-size:42px;">{win_rate*100:.0f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Every Bet You Made ───────────────────────────
    # Emotion timeline
    def get_emotion_svg(state):
        """Return SVG face for 4 states: happy, nervous, worried, despair"""
        if state == "happy":
            return """<svg viewBox="0 0 60 60" width="52" height="52" xmlns="http://www.w3.org/2000/svg">
              <circle cx="30" cy="30" r="26" stroke="#2ecc71" stroke-width="2.5" fill="none"/>
              <path d="M20 34 Q30 44 40 34" stroke="#2ecc71" stroke-width="2.5" fill="none" stroke-linecap="round"/>
              <circle cx="22" cy="25" r="2.5" fill="#2ecc71"/>
              <circle cx="38" cy="25" r="2.5" fill="#2ecc71"/>
              <path d="M18 22 Q22 18 26 22" stroke="#2ecc71" stroke-width="1.8" fill="none"/>
              <path d="M34 22 Q38 18 42 22" stroke="#2ecc71" stroke-width="1.8" fill="none"/>
            </svg>"""
        elif state == "nervous":
            return """<svg viewBox="0 0 60 60" width="52" height="52" xmlns="http://www.w3.org/2000/svg">
              <circle cx="30" cy="30" r="26" stroke="#f39c12" stroke-width="2.5" fill="none"/>
              <path d="M20 38 Q25 34 30 38 Q35 42 40 38" stroke="#f39c12" stroke-width="2.5" fill="none" stroke-linecap="round"/>
              <circle cx="22" cy="26" r="2.5" fill="#f39c12"/>
              <circle cx="38" cy="26" r="2.5" fill="#f39c12"/>
              <path d="M18 22 Q22 26 26 22" stroke="#f39c12" stroke-width="1.8" fill="none"/>
              <path d="M34 22 Q38 26 42 22" stroke="#f39c12" stroke-width="1.8" fill="none"/>
              <line x1="46" y1="18" x2="50" y2="14" stroke="#f39c12" stroke-width="1.5"/>
              <line x1="48" y1="14" x2="52" y2="18" stroke="#f39c12" stroke-width="1.5"/>
            </svg>"""
        elif state == "worried":
            return """<svg viewBox="0 0 60 60" width="52" height="52" xmlns="http://www.w3.org/2000/svg">
              <circle cx="30" cy="30" r="26" stroke="#e67e22" stroke-width="2.5" fill="none"/>
              <path d="M20 40 Q30 32 40 40" stroke="#e67e22" stroke-width="2.5" fill="none" stroke-linecap="round"/>
              <circle cx="22" cy="26" r="3" fill="#e67e22"/>
              <circle cx="38" cy="26" r="3" fill="#e67e22"/>
              <path d="M18 20 Q22 25 26 20" stroke="#e67e22" stroke-width="2" fill="none"/>
              <path d="M34 20 Q38 25 42 20" stroke="#e67e22" stroke-width="2" fill="none"/>
              <path d="M44 10 Q46 16 44 20" stroke="#e67e22" stroke-width="1.5" fill="none"/>
              <circle cx="44" cy="22" r="1.5" fill="#e67e22"/>
            </svg>"""
        else:  # despair
            return """<svg viewBox="0 0 60 60" width="52" height="52" xmlns="http://www.w3.org/2000/svg">
              <circle cx="30" cy="30" r="26" stroke="#e74c3c" stroke-width="2.5" fill="none"/>
              <path d="M18 42 Q30 30 42 42" stroke="#e74c3c" stroke-width="2.5" fill="none" stroke-linecap="round"/>
              <line x1="18" y1="22" x2="26" y2="30" stroke="#e74c3c" stroke-width="2.5" stroke-linecap="round"/>
              <line x1="26" y1="22" x2="18" y2="30" stroke="#e74c3c" stroke-width="2.5" stroke-linecap="round"/>
              <line x1="34" y1="22" x2="42" y2="30" stroke="#e74c3c" stroke-width="2.5" stroke-linecap="round"/>
              <line x1="42" y1="22" x2="34" y2="30" stroke="#e74c3c" stroke-width="2.5" stroke-linecap="round"/>
              <path d="M42 10 Q46 16 44 20" stroke="#e74c3c" stroke-width="1.5" fill="none"/>
              <circle cx="44" cy="22" r="1.5" fill="#e74c3c"/>
              <path d="M48 14 Q52 18 50 22" stroke="#e74c3c" stroke-width="1.5" fill="none"/>
              <circle cx="50" cy="24" r="1.5" fill="#e74c3c"/>
            </svg>"""

    # Persona-specific lines for each emotion state
    PERSONA_LINES = {
        "casual":      {"happy": "Easy money 😌", "nervous": "Hmm, that's odd...", "worried": "Maybe I should stop?", "despair": "Well, that happened."},
        "impulsive":   {"happy": "I'm unstoppable!", "nervous": "No way, I should win!!", "worried": "DOUBLE DOWN NOW.", "despair": "One more round. Please."},
        "rational":    {"happy": "On track.", "nervous": "Approaching stop-loss.", "worried": "Stop-loss triggered.", "despair": "Exit. Loss accepted."},
        "addicted":    {"happy": "This is my night!", "nervous": "Just need one more win...", "worried": "I can still recover this.", "despair": "I can't stop now."},
        "loss_averse": {"happy": "Don't get too excited...", "nervous": "Oh no, oh no, oh no.", "worried": "I knew this was a mistake.", "despair": "Never again. Never."},
        "analytical":  {"happy": "Win rate above expected.", "nervous": "Variance increasing.", "worried": "Model says: stop.", "despair": "Edge case. Noted."},
        "social":      {"happy": "Everyone's watching me win!", "nervous": "This is embarrassing...", "worried": "Should've left an hour ago.", "despair": "Don't tell my friends."},
        "superstitious": {"happy": "The stars aligned!", "nervous": "Bad energy tonight...", "worried": "I need a lucky ritual.", "despair": "The universe betrayed me."},
    }

    def build_emotion_timeline(player_df, persona):
        """Detect emotional turning points and build timeline nodes."""
        balances   = player_df['balance'].tolist()
        rounds     = player_df['round'].tolist()
        initial    = player_df['initial_balance'].iloc[0]
        lines      = PERSONA_LINES.get(persona, PERSONA_LINES["casual"])
        nodes      = []

        # sliding window: detect state per round — based on trend, not vs initial
        def get_state(balance, prev_balance, streak_loss, recent_drop_pct):
            if balance <= 0:
                return "despair"
            elif streak_loss >= 4 or recent_drop_pct <= -25:
                return "worried"
            elif streak_loss >= 2 or recent_drop_pct <= -10:
                return "nervous"
            else:
                return "happy"

        streak_loss = 0
        prev_state  = None
        prev_bal    = balances[0] if balances else initial
        peak_bal    = prev_bal

        for i, (r, bal) in enumerate(zip(rounds, balances)):
            is_loss = bal < prev_bal
            streak_loss = streak_loss + 1 if is_loss else 0
            if bal > peak_bal:
                peak_bal = bal
            # recent drop from peak
            recent_drop_pct = (bal - peak_bal) / peak_bal * 100 if peak_bal > 0 else 0
            state = get_state(bal, prev_bal, streak_loss, recent_drop_pct)
            if state != prev_state:
                nodes.append({"round": r, "state": state, "balance": bal})
                prev_state = state
            prev_bal = bal

        return nodes

    nodes = build_emotion_timeline(player_df, persona)
    lines_dict = PERSONA_LINES.get(persona, PERSONA_LINES["casual"])

    state_colors = {"happy": "#2ecc71", "nervous": "#f39c12", "worried": "#e67e22", "despair": "#e74c3c"}

    # Build timeline HTML
    timeline_html = """
    <div style='font-size:11px;color:#888;font-style:italic;margin-bottom:4px;padding-left:2px;'>
        How you felt along the way
    </div>
    <div style='display:flex;align-items:flex-start;gap:0;overflow-x:auto;padding:8px 0 8px 0;'>"""
    for i, node in enumerate(nodes):
        state = node["state"]
        color = state_colors[state]
        label = lines_dict[state]
        svg   = get_emotion_svg(state)
        connector = f"<div style='flex:1;height:2px;background:{color}44;margin-top:28px;min-width:20px;'></div>" if i < len(nodes)-1 else ""
        timeline_html += f"""
        <div style='display:flex;flex-direction:column;align-items:center;min-width:90px;max-width:110px;'>
            <div style='font-size:10px;color:#888;margin-bottom:4px;'>Round {node["round"]}</div>
            {svg}
            <div style='font-size:11px;color:{color};font-weight:600;text-align:center;margin-top:6px;line-height:1.3;'>{label}</div>
        </div>
        {connector}
        """
    timeline_html += "</div>"

    # ── Balance Journey title ──────────────────────────
    st.subheader("📈 Balance Journey")
    st.markdown("🎲 **Every Bet You Made**")

    # Emotion timeline
    import streamlit.components.v1 as components
    full_html = f"""
    <div style="font-family:sans-serif; background:transparent; padding:4px 0;">
    {timeline_html}
    </div>
    """
    components.html(full_html, height=160, scrolling=False)
    st.markdown("---")

    display_df = player_df[['round', 'game', 'bet', 'is_win', 'balance', 'reasoning']].copy()
    display_df['result'] = display_df['is_win'].apply(lambda x: '✅ WIN' if x else '❌ LOSE')
    display_df = display_df[['round', 'game', 'bet', 'result', 'balance', 'reasoning']]
    display_df.columns = ['Round', 'Game', 'Bet ($)', 'Result', 'Balance ($)', 'Inner Thoughts']
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # ── Balance Chart (after table) ───────────────────
    st.markdown('<p class="chart-caption">The change of your money, round by round — green means above your starting budget, red means below.</p>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(8, 3))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    ax.plot(player_df['round'], player_df['balance'], color=info['color'], linewidth=2, marker='o', markersize=3)
    ax.axhline(y=initial_balance, color='gray', linestyle='--', alpha=0.5)
    ax.fill_between(player_df['round'], player_df['balance'], initial_balance,
                    where=player_df['balance'] >= initial_balance, color='green', alpha=0.15)
    ax.fill_between(player_df['round'], player_df['balance'], initial_balance,
                    where=player_df['balance'] < initial_balance, color='red', alpha=0.15)
    ax.set_xlabel('Round', color='#aaa')
    ax.set_ylabel('Balance ($)', color='#aaa')
    ax.tick_params(colors='#aaa')
    for spine in ax.spines.values():
        spine.set_color('#444')
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    # ── Persona Reveal ───────────────────────────────
    st.subheader("You are...")
    svg_code    = PERSONA_SVG.get(persona, "")
    traits_html = "".join([f'<span class="trait-tag">{t}</span>' for t in info['traits']])

    st.markdown(f"""
    <div class="persona-reveal" style="background:{info['color']}12; border:1px solid {info['color']}44;">
        <div class="persona-left">
            <div class="persona-left-top">
                <p style="margin:0 0 10px 0;font-size:15px;font-weight:700;">{info['risk_level']}</p>
                {traits_html}
            </div>
            <div class="persona-left-bottom">
                <p style="margin:0 0 4px 0;font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.08em;">Explain</p>
                <p class="persona-explain">{info['description']}</p>
            </div>
        </div>
        <div class="persona-right" style="border-left:1px solid {info['color']}33;">
            {svg_code}
            <div class="persona-name-big" style="color:{info['color']};">{info['emoji']} {info['name']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── How Others Like You Played ───────────────────
    st.subheader("📊 How others like you played")

    # Compute stats per persona
    stats = df.groupby(['persona', 'player_id']).agg(
        final_balance=('balance', 'last'),
        initial_balance=('initial_balance', 'first')
    ).reset_index()
    stats['net_pct']   = (stats['final_balance'] - stats['initial_balance']) / stats['initial_balance'] * 100
    stats['bankrupt']  = (stats['final_balance'] <= 0).astype(int)

    avg_stats   = stats.groupby('persona')['net_pct'].mean().reset_index()
    avg_stats   = avg_stats.sort_values('net_pct', ascending=True)
    bk_stats    = stats.groupby('persona')['bankrupt'].mean().reset_index()
    bk_stats['bankrupt_pct'] = bk_stats['bankrupt'] * 100
    # keep same order as avg_stats
    bk_stats    = bk_stats.set_index('persona').reindex(avg_stats['persona']).reset_index()

    # Top 3 "best" performers (highest net_pct)
    top3 = avg_stats.sort_values('net_pct', ascending=False).head(3)

    col_chart, col_right = st.columns([3, 2], vertical_alignment="center")

    with col_chart:
        # Chart 1: Avg Net Profit
        n = len(avg_stats)
        fig2, ax2 = plt.subplots(figsize=(5, n * 0.52))
        fig2.patch.set_alpha(0)
        ax2.set_facecolor('none')

        colors = [info['color'] if p == persona else '#444455' for p in avg_stats['persona']]
        labels = [persona_info[p]['emoji'] + ' ' + persona_info[p]['name'].replace('The ', '') for p in avg_stats['persona']]

        bars = ax2.barh(labels, avg_stats['net_pct'], color=colors, height=0.6)
        for bar, val in zip(bars, avg_stats['net_pct']):
            ax2.text(val - 1.5, bar.get_y() + bar.get_height() / 2,
                     f'{val:+.0f}%', va='center', ha='right', fontsize=7.5, color='white')

        ax2.set_xlim(min(avg_stats['net_pct']) * 1.18, 8)
        ax2.set_ylim(-0.8, n - 0.2)
        ax2.invert_yaxis()
        ax2.axvline(0, color='#666', linewidth=0.8)
        ax2.set_xlabel('Avg Net Profit (%)', color='#aaa', fontsize=9)
        ax2.tick_params(colors='#ccc', labelsize=8)
        for spine in ax2.spines.values():
            spine.set_visible(False)
        ax2.xaxis.label.set_color('#aaa')
        fig2.subplots_adjust(top=0.97, bottom=0.12, left=0.3, right=0.95)
        st.pyplot(fig2)

    with col_right:
        # Get larger SVG by replacing width/height attributes
        svg2_large = PERSONA_SVG_2.get(persona, "").replace('width="110" height="110"', 'width="160" height="160"')
        tagline = PERSONA_TAGLINE.get(persona, "")
        medals  = ["🥇", "🥈", "🥉"]

        # my avg net profit
        my_net = avg_stats[avg_stats['persona'] == persona]['net_pct'].values
        my_net_val  = f"{my_net[0]:+.0f}%" if len(my_net) > 0 else "—"
        my_net_color = "#2ecc71" if (len(my_net) > 0 and my_net[0] >= 0) else "#e74c3c"

        # illustration + tagline + my stat
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:12px 0 8px 0;">
            {svg2_large}
            <div style="font-size:13px;color:{info['color']};font-weight:700;margin-top:8px;">"{tagline}"</div>
            <hr style='border-color:#333;margin:10px 0;width:100%;'/>
            <div style='font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;'>Your avg net profit</div>
            <div style='font-size:36px;font-weight:900;color:{my_net_color};'>{my_net_val}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#333;margin:8px 0;'/>", unsafe_allow_html=True)

        # Top 3 ranking — centered under illustration
        ranking_html = "<div style='text-align:center;'>"
        ranking_html += "<p style='font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;'>🏆 Best Performers</p>"
        for i, (_, row) in enumerate(top3.iterrows()):
            p_key   = row['persona']
            p_info  = persona_info[p_key]
            p_color = p_info['color']
            p_name  = p_info['name'].replace('The ', '')
            p_val   = f"{row['net_pct']:+.0f}%"
            bold    = "font-weight:700;" if p_key == persona else "color:#aaa;"
            ranking_html += (
                f"<div style='font-size:13px;margin-bottom:6px;{bold}'>"
                f"{medals[i]} {p_info['emoji']} {p_name} "
                f"<span style='color:{p_color};'>{p_val}</span></div>"
            )
        ranking_html += "</div>"
        st.markdown(ranking_html, unsafe_allow_html=True)

    # ── Bankruptcy Rate ───────────────────────────────
    st.markdown("<hr style='border-color:#333;margin:24px 0 12px 0;'/>", unsafe_allow_html=True)
    st.markdown('<p class="chart-caption">💀 Bankruptcy rate — how often each type ends up with $0</p>', unsafe_allow_html=True)

    col_bk, col_bk_right = st.columns([3, 2], vertical_alignment="center")
    with col_bk:
        n3 = len(bk_stats)
        fig3, ax3 = plt.subplots(figsize=(5, n3 * 0.52))
        fig3.patch.set_alpha(0)
        ax3.set_facecolor('none')
        bk_colors = [info['color'] if p == persona else '#444455' for p in bk_stats['persona']]
        bk_labels = [persona_info[p]['emoji'] + ' ' + persona_info[p]['name'].replace('The ', '') for p in bk_stats['persona']]
        bars3 = ax3.barh(bk_labels, bk_stats['bankrupt_pct'], color=bk_colors, height=0.6)
        for bar, val in zip(bars3, bk_stats['bankrupt_pct']):
            ax3.text(val + 1, bar.get_y() + bar.get_height() / 2,
                     f'{val:.0f}%', va='center', ha='left', fontsize=7.5, color='white')
        ax3.set_xlim(0, 115)
        ax3.set_ylim(-0.8, n3 - 0.2)
        ax3.invert_yaxis()
        ax3.axvline(0, color='#666', linewidth=0.8)
        ax3.set_xlabel('Bankruptcy Rate (%)', color='#aaa', fontsize=9)
        ax3.tick_params(colors='#ccc', labelsize=8)
        for spine in ax3.spines.values():
            spine.set_visible(False)
        ax3.xaxis.label.set_color('#aaa')
        fig3.subplots_adjust(top=0.97, bottom=0.12, left=0.3, right=0.95)
        st.pyplot(fig3)

    with col_bk_right:
        my_bk     = bk_stats[bk_stats['persona'] == persona]['bankrupt_pct'].values
        my_bk_val = f"{my_bk[0]:.0f}%" if len(my_bk) > 0 else "—"
        svg3_large = PERSONA_SVG_3.get(persona, "").replace('width="110" height="110"', 'width="160" height="160"')
        tagline   = PERSONA_TAGLINE.get(persona, "")
        bk_color  = info['color']
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:12px 0 8px 0;">
            {svg3_large}
            <div style="font-size:13px;color:{bk_color};font-weight:700;margin-top:8px;">"{tagline}"</div>
            <hr style='border-color:#333;margin:12px 0;width:100%;'/>
            <div style='font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;'>Your type goes broke</div>
            <div style='font-size:38px;font-weight:900;color:{bk_color};'>{my_bk_val}</div>
            <div style='font-size:11px;color:#666;margin-top:4px;'>of the time</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#333;margin:8px 0;'/>", unsafe_allow_html=True)

        # Top 3 lowest bankruptcy rate
        top3_bk = bk_stats.sort_values('bankrupt_pct', ascending=True).head(3)
        bk_ranking_html = "<div style='text-align:center;'>"
        bk_ranking_html += "<p style='font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;'>🛡️ Safest Players</p>"
        medals = ["🥇", "🥈", "🥉"]
        for i, (_, row) in enumerate(top3_bk.iterrows()):
            p_key   = row['persona']
            p_info  = persona_info[p_key]
            p_color = p_info['color']
            p_name  = p_info['name'].replace('The ', '')
            p_val   = f"{row['bankrupt_pct']:.0f}%"
            bold    = "font-weight:700;" if p_key == persona else "color:#aaa;"
            bk_ranking_html += (
                f"<div style='font-size:13px;margin-bottom:6px;{bold}'>"
                f"{medals[i]} {p_info['emoji']} {p_name} "
                f"<span style='color:{p_color};'>{p_val}</span></div>"
            )
        bk_ranking_html += "</div>"
        st.markdown(bk_ranking_html, unsafe_allow_html=True)

    # ── Try Again ────────────────────────────────────
    st.markdown("")
    _, btn_col = st.columns([3, 1])
    with btn_col:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.step = 1
            st.session_state.profile = {}
            st.session_state.results = None
            st.rerun()
