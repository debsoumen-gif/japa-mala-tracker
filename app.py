import streamlit as st
from datetime import date

st.set_page_config(page_title="Japa Mala Tracker", page_icon="🙏")

# ------------------------------------------------------------
# 🌿 Tulasi-Green Button Theme
# ------------------------------------------------------------
st.markdown("""
<style>
div.stButton > button {
    background: linear-gradient(90deg, #7cb342, #558b2f);
    color: white;
    border-radius: 10px;
    border: 2px solid #33691e;
    font-weight: 700;
    padding: 10px 18px;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #558b2f, #33691e);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 🌙 Dark Mode
# ------------------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #1a1a1a;
    color: #e6e6e6;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 🌺 Floating Hare Krishna Banner
# ------------------------------------------------------------
st.markdown("""
<style>
.floating-banner {
    position: fixed;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(90deg, #ffcc66, #ff9933, #ff7700);
    padding: 16px 22px;
    border-radius: 14px;
    border: 4px solid gold;
    color: white;
    font-size: 26px;
    font-weight: 800;
    text-align: center;
    width: 92%;
    box-shadow: 0 0 22px rgba(255,153,51,0.85);
    z-index: 9999;
}
</style>

<div class="floating-banner">
    🔱 Hare Krishna Hare Krishna Krishna Krishna Hare Hare —
    Hare Rama Hare Rama Rama Rama Hare Hare 🔱
</div>

<br><br><br><br><br>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Prabhupāda Image
# ------------------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top:10px; margin-bottom:4px;">
        <img src="./assets/prabhupada_mala.png"
             style="width:140px; height:auto; border-radius:12px;
                    box-shadow:0 0 18px rgba(181,126,220,0.45);">
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Session State
# ------------------------------------------------------------
if "beads" not in st.session_state:
    st.session_state.beads = 0
if "mala" not in st.session_state:
    st.session_state.mala = 0
if "sets" not in st.session_state:
    st.session_state.sets = 0

# ------------------------------------------------------------
# Daily Goal
# ------------------------------------------------------------
daily_goal = st.slider(
    "🎯 Daily Goal (Mala)",
    min_value=1,
    max_value=128,
    step=1,
    value=16,
)

# ------------------------------------------------------------
# Virtual Rotating Japa Mālā (visual)
# ------------------------------------------------------------
st.markdown("### 🕉️ Virtual Japa Mālā")

st.markdown("""
<style>
.mala-container {
    position: relative;
    width: 260px;
    height: 260px;
    margin: 0 auto;
    border-radius: 50%;
    animation: rotateMala 18s linear infinite;
}

.bead {
    position: absolute;
    width: 14px;
    height: 14px;
    background: #8d6e63;
    border-radius: 50%;
    box-shadow: 0 0 4px rgba(0,0,0,0.6);
}

@keyframes rotateMala {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
</style>

<div class="mala-container">
""" + "".join([
    f'<div class="bead" style="top:{130 + 110 * __import__("math").sin(2*__import__("math").pi*i/108):.1f}px;'
    f'left:{130 + 110 * __import__("math").cos(2*__import__("math").pi*i/108):.1f}px;"></div>'
    for i in range(108)
]) + """
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Simple Controls (logic still uses counters)
# ------------------------------------------------------------
col_add, col_info = st.columns([2, 1])

with col_add:
    if st.button("🌿 ➕ Add 1 Bead", use_container_width=True):
        st.session_state.beads += 1
        if st.session_state.beads >= 108:
            st.session_state.beads = 0
            st.session_state.mala += 1
            if st.session_state.mala >= 16:
                st.session_state.mala = 0
                st.session_state.sets += 1

with col_info:
    st.write(f"Beads: {st.session_state.beads}")
    st.write(f"Mala: {st.session_state.mala}")
    st.write(f"Sets: {st.session_state.sets}")

# ------------------------------------------------------------
# Mala Progress Tile
# ------------------------------------------------------------
mala_done = st.session_state.mala + (st.session_state.sets * 16)
mala_pending = max(daily_goal - mala_done, 0)

st.markdown(
    f"""
    <div style="
        margin-top:20px;
        padding:15px;
        background:#e8f5e9;
        border:2px solid #33691e;
        border-radius:14px;
        text-align:center;
        width:70%;
        margin-left:auto;
        margin-right:auto;
        box-shadow:0 0 12px rgba(76,175,80,0.35);
    ">
        <div style="font-size:22px; font-weight:700; color:#2e7d32;">
            🕉️ Mala Progress
        </div>
        <div style="font-size:18px; margin-top:6px; color:#2e7d32;">
            {mala_done} done
        </div>
        <div style="font-size:18px; margin-top:4px; color:#2e7d32;">
            {mala_pending} pending
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Bhakti Progress Tracker (no bar)
# ------------------------------------------------------------
st.markdown("### 🌼 Bhakti Progress Tracker")

st.markdown("### 🕉️ Rounds Chanted Today")
st.markdown(
    f"""
    <div style="
        background:#f1f8e9;
        padding:14px;
        border-radius:12px;
        text-align:center;
        border:2px solid #33691e;
        font-weight:600;
        color:#2e7d32;
        font-size:22px;">
        {mala_done} rounds
    </div>
    """,
    unsafe_allow_html=True,
)

reading = st.checkbox("📘 Read Gītā / Bhāgavatam today")
kirtan = st.checkbox("🎶 Participated in kīrtan")
service = st.checkbox("🙏 Performed some seva")

# ------------------------------------------------------------
# Floating Mantra Bar
# ------------------------------------------------------------
st.markdown("""
<div style="
    position:fixed;
    bottom:0;
    left:0;
    width:100%;
    background:#33691e;
    color:white;
    padding:10px;
    text-align:center;
    font-size:18px;
    font-weight:700;
    box-shadow:0 -2px 10px rgba(0,0,0,0.3);
">
    🕉️ Hare Krishna Hare Krishna Krishna Krishna Hare Hare —
    Hare Rama Hare Rama Rama Rama Hare Hare 🕉️
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.markdown(
    """
    <div style="
        margin-top:40px;
        text-align:center;
        font-size:18px;
        font-weight:600;
        color:#ffcc66;
    ">
        ✨ Chant and Be Happy ✨
    </div>
    """,
    unsafe_allow_html=True,
)
