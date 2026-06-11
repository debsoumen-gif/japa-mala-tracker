# ============================================================
#   File Name: app.py
#   Full Path: C:/japa-mala-tracker/app.py
#
#   Author: Soumen
#   Location: Paramus, New Jersey, United States
#   Time Zone: New York (EST)
#   Timestamp: 2026-06-11 08:15 AM EST
#
#   Purpose:
#     Main Streamlit application for the Japa Mala Tracker.
#
#   Functionality:
#     • UI rendering
#     • Bead/round/set tracking
#     • Sādhanā streak logic
#     • Mala visualization
#
#   Notes:
#     • Imports components from /components/
#
#   Debug:
#     • Print session_state to verify transitions
# ============================================================

import streamlit as st
from datetime import date

from components.session_init import init_session_state
from components.mala_renderer import render_mala_html
from components.audio import play_sound

# Initialize session state
init_session_state()

# Load CSS
with open("styles/theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------------------------------------------------
# 🔱 Japa Mala Tracker
# ------------------------------------------------------------
st.markdown("<h3 class='japa-header'>🔱 Japa Mala Tracker</h3>", unsafe_allow_html=True)

# Render mala
mala_html = render_mala_html(
    inner_total=108,
    inner_done=st.session_state.mala_bead_count,
    outer_total=16,
    outer_done=st.session_state.mala_round_count,
    size_px=320,
)
st.markdown(mala_html, unsafe_allow_html=True)

# ------------------------------------------------------------
# Compute progress BEFORE rendering tiles
# ------------------------------------------------------------
sets   = st.session_state.mala_set_count
rounds = st.session_state.mala_round_count
beads  = st.session_state.mala_bead_count

total_rounds_today = (sets * 16) + rounds
daily_goal = 16
progress_ratio = min(total_rounds_today / daily_goal, 1.0)

# ------------------------------------------------------------
# ONE ACTION BUTTON + BEADS + ROUNDS (RING) + SETS
# ------------------------------------------------------------
col_bead_btn, col_bead, col_rounds, col_set = st.columns([2, 1, 1.4, 1])

# --- BUTTON ---
with col_bead_btn:
    if st.button("🌸 ➕ Add 1 bead (current round)", use_container_width=True):
        st.session_state.mala_bead_count += 1

        # 108 beads → +1 round
        if st.session_state.mala_bead_count >= 108:
            st.session_state.mala_bead_count = 0
            st.session_state.mala_round_count += 1
            play_sound("assets/bell.mp3")

            # 16 rounds → +1 set
            if st.session_state.mala_round_count >= 16:
                st.session_state.mala_round_count = 0
                st.session_state.mala_set_count += 1
                play_sound("assets/conch.mp3")

# --- BEADS TILE ---
with col_bead:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Beads</div>
            <div class="metric-value">{beads}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- ROUNDS TILE ---
with col_rounds:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Rounds</div>
            <svg width="110" height="110" style="margin-top:6px;">
                <circle cx="55" cy="55" r="48" stroke="#f3e8ff" stroke-width="10" fill="none"/>
                <circle cx="55" cy="55" r="48"
                    stroke="#b57edc"
                    stroke-width="10"
                    fill="none"
                    stroke-dasharray="{progress_ratio * 302} 302"
                    stroke-linecap="round"
                    transform="rotate(-90 55 55)"
                />
            </svg>
            <div class="metric-value">{total_rounds_today}/{daily_goal}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- SETS TILE ---
with col_set:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Sets</div>
            <div class="metric-value">{sets}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# Devotional progress text
# ------------------------------------------------------------
st.markdown(
    f"""
    <div style="
        margin-top:10px;
        font-size:20px;
        font-weight:600;
        color:#4a2c6d;
        text-align:center;">
        {sets} set + {rounds} rounds 
        = <span style="color:#b57edc;">{total_rounds_today} rounds today</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Sādhanā Streak Counter
# ------------------------------------------------------------
today = str(date.today())

if total_rounds_today >= daily_goal:
    if st.session_state.last_streak_date != today:
        st.session_state.sadhana_streak += 1
        st.session_state.last_streak_date = today

st.markdown(
    f"""
    <div style="
        margin-top:15px;
        padding:12px;
        background:#e6ffe6;
        border:2px solid #4caf50;
        border-radius:12px;
        text-align:center;
        font-size:20px;
        font-weight:600;
        color:#2e7d32;">
        🌸 Sādhanā Streak: {st.session_state.sadhana_streak} days
    </div>
    """,
    unsafe_allow_html=True,
)
