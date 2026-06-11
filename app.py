# ============================================================
#   File Name: app.py
#   Full Path: C:/japa-mala-tracker/app.py
#
#   Author: Soumen
#   Location: Paramus, New Jersey, United States
#   Time Zone: New York (EST)
#   Timestamp: 2026-06-11 12:45 PM EST
#
#   Purpose:
#     Main Streamlit application for the Japa Mala Tracker.
#
#   Functionality:
#     • UI rendering
#     • Bead/round/set tracking
#     • Daily goal slider (1–128 rounds)
#     • Sādhanā streak logic
#     • Streak calendar visualization
#     • Mala visualization
#     • Mobile vibration feedback
#     • Dark mode toggle
#     • Reset button
#     • Notes / reflections journal
#     • Devotional share-progress card
#     • Floating mantra bar
#
#   Notes:
#     • Ensure assets/prabhupada_mala.png exists
#     • Ensure tap.mp3, bell.mp3, conch.mp3 exist
#
#   Debug:
#     • Print session_state to verify transitions
# ============================================================

import streamlit as st
from datetime import date, timedelta

from components.session_init import init_session_state
from components.mala_renderer import render_mala_html
from components.audio import play_sound

# Initialize session state
init_session_state()

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "sadhana_history" not in st.session_state:
    st.session_state.sadhana_history = {}
if "today_notes" not in st.session_state:
    st.session_state.today_notes = ""

# ------------------------------------------------------------
# Dark Mode Toggle
# ------------------------------------------------------------
st.session_state.dark_mode = st.toggle("🌙 Dark Mode", st.session_state.dark_mode)

with open("styles/theme.css") as f:
    css = f.read()

if st.session_state.dark_mode:
    css += """
    body, .stApp { background-color:#0d0d0d !important; color:#f5f5f5 !important; }
    .metric-card { background:#1a1a1a !important; border-color:#444 !important; color:#fff !important; }
    .mantra-bar { background:linear-gradient(90deg,#4a148c,#880e4f) !important; color:#fff !important; }
    """

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Centered Prabhupāda Header
# ------------------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top:10px; margin-bottom:4px;">
        <img src="assets/prabhupada_mala.png"
             style="width:140px; height:auto; border-radius:12px;
                    box-shadow:0 0 18px rgba(181,126,220,0.45);">
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h2 style="text-align:center; font-weight:800; color:#4a2c6d;
               margin-top:0px; margin-bottom:20px;">
        Japa Mala Tracker
    </h2>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Daily Goal Slider (1–128)
# ------------------------------------------------------------
daily_goal = st.slider(
    "🎯 Daily Goal (rounds)",
    min_value=1,
    max_value=128,
    step=1,
    value=16,
)

# ------------------------------------------------------------
# Mala Visualization
# ------------------------------------------------------------
mala_html = render_mala_html(
    inner_total=108,
    inner_done=st.session_state.mala_bead_count,
    outer_total=16,
    outer_done=st.session_state.mala_round_count,
    size_px=320,
)
st.markdown(mala_html, unsafe_allow_html=True)

# ------------------------------------------------------------
# Progress Computation
# ------------------------------------------------------------
sets = st.session_state.mala_set_count
rounds = st.session_state.mala_round_count
beads = st.session_state.mala_bead_count

total_rounds_today = (sets * 16) + rounds
progress_ratio = min(total_rounds_today / daily_goal, 1.0)

# ------------------------------------------------------------
# Mobile Vibration Script
# ------------------------------------------------------------
st.markdown(
    """
    <script>
    function vibratePhone() {
        if (navigator.vibrate) { navigator.vibrate(40); }
    }
    </script>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# BUTTON ROW: Add bead + beads + sets
# ------------------------------------------------------------
col_add, col_beads, col_sets = st.columns([2, 1, 1])

with col_add:
    if st.button("🌸 ➕ Add 1 bead", use_container_width=True):
        play_sound("assets/tap.mp3")
        st.session_state.mala_bead_count += 1
        st.markdown("<script>vibratePhone()</script>", unsafe_allow_html=True)

        if st.session_state.mala_bead_count >= 108:
            st.session_state.mala_bead_count = 0
            st.session_state.mala_round_count += 1
            play_sound("assets/bell.mp3")

            if st.session_state.mala_round_count >= 16:
                st.session_state.mala_round_count = 0
                st.session_state.mala_set_count += 1
                play_sound("assets/conch.mp3")

with col_beads:
    st.button(f"Beads: {beads}", use_container_width=True)

with col_sets:
    st.button(f"Sets: {sets}", use_container_width=True)

# ------------------------------------------------------------
# Rounds Centered Below
# ------------------------------------------------------------
st.markdown(
    f"""
    <div style="text-align:center; margin-top:10px;">
        <div class="metric-title">Rounds</div>
        <div class="metric-value">{total_rounds_today}/{daily_goal}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Devotional Progress Text
# ------------------------------------------------------------
st.markdown(
    f"""
    <div style="margin-top:10px; font-size:20px; font-weight:600;
                color:#4a2c6d; text-align:center;">
        {sets} set + {rounds} rounds =
        <span style="color:#b57edc;">{total_rounds_today} rounds today</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Sādhanā Streak + History
# ------------------------------------------------------------
today_str = str(date.today())

if total_rounds_today >= daily_goal:
    status = "full"
elif total_rounds_today > 0:
    status = "partial"
else:
    status = st.session_state.sadhana_history.get(today_str, "missed")

st.session_state.sadhana_history[today_str] = status

if total_rounds_today >= daily_goal:
    if st.session_state.last_streak_date != today_str:
        st.session_state.sadhana_streak += 1
        st.session_state.last_streak_date = today_str

st.markdown(
    f"""
    <div style="margin-top:15px; padding:12px; background:#e6ffe6;
                border:2px solid #4caf50; border-radius:12px;
                text-align:center; font-size:20px; font-weight:600;
                color:#2e7d32;">
        🌸 Sādhanā Streak: {st.session_state.sadhana_streak} days
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Streak Calendar (Last 14 Days)
# ------------------------------------------------------------
st.markdown("### 📅 Sādhanā Calendar (Last 14 Days)")

cols = st.columns(14)
for i in range(14):
    day = date.today() - timedelta(days=13 - i)
    day_str = str(day)
    status = st.session_state.sadhana_history.get(day_str, "missed")

    emoji = "🟢" if status == "full" else "🟡" if status == "partial" else "⚪"

    with cols[i]:
        st.markdown(
            f"""
            <div style="text-align:center; font-size:18px;">
                {emoji}<br>
                <span style="font-size:10px;">{day.day}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------
# Notes / Reflections
# ------------------------------------------------------------
st.markdown("### 📝 Today’s Notes / Reflections")

st.session_state.today_notes = st.text_area(
    "Write your reflections here:",
    value=st.session_state.today_notes,
    height=120,
)

# ------------------------------------------------------------
# Share My Progress (Devotional Card)
# ------------------------------------------------------------
st.markdown("### 🌸 Share My Progress")

if st.button("📤 Generate Devotional Card", use_container_width=True):
    card_html = f"""
    <div style="margin-top:10px; margin-bottom:10px; padding:18px;
                border-radius:18px; text-align:center;
                background:radial-gradient(circle at top,#f8e9ff 0%,
                #e0c3fc 40%,#fdfcfb 100%);
                box-shadow:0 0 24px rgba(181,126,220,0.55);
                border:2px solid #b57edc;">
        <img src="assets/prabhupada_mala.png"
             style="width:120px; height:auto; border-radius:12px;
                    box-shadow:0 0 16px rgba(181,126,220,0.45);">
        <div style="font-size:22px; font-weight:800; color:#4a2c6d;
                    margin-top:10px;">
            Japa Mala Progress
        </div>
        <div style="font-size:18px; color:#4a2c6d;">
            Rounds today: <b>{total_rounds_today}</b> / {daily_goal}
        </div>
        <div style="font-size:18px; color:#4a2c6d;">
            Sets: <b>{sets}</b> · Beads: <b>{beads}</b>
        </div>
        <div style="font-size:18px; color:#2e7d32;">
            Sādhanā Streak: <b>{st.session_state.sadhana_streak} days</b>
        </div>
        <div style="font-size:14px; color:#6a1b9a; margin-top:6px;">
            Hare Krishna Hare Krishna, Krishna Krishna Hare Hare<br>
            Hare Rama Hare Rama, Rama Rama Hare Hare
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    st.info("Take a screenshot to share your devotional progress.")

# ------------------------------------------------------------
# Floating Mantra Bar
# ------------------------------------------------------------
st.markdown(
    """
    <div class="mantra-bar">
        Hare Krishna Hare Krishna, Krishna Krishna Hare Hare ·
        Hare Rama Hare Rama, Rama Rama Hare Hare
    </div>
    """,
    unsafe_allow_html=True,
)
