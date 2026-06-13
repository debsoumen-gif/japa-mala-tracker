"""
===============================================================
FILE NAME:
    app.py

PURPOSE:
    Digital Hare Krishna Japa Mala tracker to count chanting rounds,
    track today’s goal, streaks, and progress in a devotional UI.
===============================================================
"""

import streamlit as st
from datetime import datetime, date, timedelta
import math
import json
import os

st.set_page_config(page_title="Hare Krishna Japa Tracker", page_icon="🙏")

# ------------------------------------------------------------
# CSS + GLOBAL STYLES
# ------------------------------------------------------------
st.markdown("""
<style>
body, .stApp {
    background-color: #FFF7E6 !important;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.main-container { max-width: 900px; margin: 0 auto; }
@media (max-width: 768px) { .main-container { padding: 8px !important; } }

@keyframes goalPulse {
    0% { box-shadow: 0 0 0px rgba(255,152,0,0); }
    50% { box-shadow: 0 0 18px rgba(255,152,0,1); }
    100% { box-shadow: 0 0 0px rgba(255,152,0,0); }
}

/* Glow for bead circle when 108/108 */
@keyframes beadGlow {
    0%   { box-shadow: 0 0 0px rgba(255,193,7,0); transform: scale(1.0); }
    50%  { box-shadow: 0 0 22px rgba(255,193,7,1); transform: scale(1.03); }
    100% { box-shadow: 0 0 0px rgba(255,193,7,0); transform: scale(1.0); }
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# JS SOUND BRIDGE
# ------------------------------------------------------------
st.markdown("""
<script>
window.playTap = function() {
    try { new Audio('/assets/tap.mp3').play(); if(navigator.vibrate) navigator.vibrate(30); } catch(e){}
};
window.playRoundComplete = function() {
    try { new Audio('/assets/round_complete.mp3').play(); if(navigator.vibrate) navigator.vibrate([120,60,120]); } catch(e){}
};
window.playGoalComplete = function() {
    try { new Audio('/assets/goal_complete.mp3').play(); if(navigator.vibrate) navigator.vibrate([200,100,200]); } catch(e){}
};
</script>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# PERSISTENCE HELPERS
# ------------------------------------------------------------
def load_user_goal():
    if os.path.exists("user_goal.json"):
        try:
            with open("user_goal.json","r") as f:
                return int(json.load(f).get("goal",16))
        except:
            return 16
    return 16

def save_user_goal(goal:int):
    try:
        with open("user_goal.json","w") as f:
            json.dump({"goal":int(goal)},f)
    except:
        pass

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------
if "current_bead" not in st.session_state: st.session_state.current_bead = 0  # legacy, no longer used for display
if "rounds_today" not in st.session_state: st.session_state.rounds_today = 0
if "total_chants" not in st.session_state: st.session_state.total_chants = 0
if "start_time" not in st.session_state: st.session_state.start_time = None
if "history" not in st.session_state: st.session_state.history = {}
if "streak" not in st.session_state: st.session_state.streak = 0
if "best_streak" not in st.session_state: st.session_state.best_streak = 0
if "user_daily_goal" not in st.session_state: st.session_state.user_daily_goal = load_user_goal()
if "goal_complete_triggered" not in st.session_state: st.session_state.goal_complete_triggered = False
if "last_active_date" not in st.session_state: st.session_state.last_active_date = str(date.today())

# Midnight reset
today_str = str(date.today())
if st.session_state.last_active_date != today_str:
    st.session_state.rounds_today = 0
    st.session_state.last_active_date = today_str

BEADS_PER_ROUND = 108

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def start_session():
    if st.session_state.start_time is None:
        st.session_state.start_time = datetime.now()

def get_time_spent():
    if st.session_state.start_time is None: return "00:00:00"
    delta = datetime.now() - st.session_state.start_time
    return str(timedelta(seconds=int(delta.total_seconds())))

def update_streak():
    today = str(date.today())
    yesterday = str(date.today()-timedelta(days=1))
    today_rounds = st.session_state.history.get(today,0)
    yesterday_rounds = st.session_state.history.get(yesterday,0)
    goal = st.session_state.user_daily_goal
    if today_rounds >= goal:
        st.session_state.streak = st.session_state.streak+1 if yesterday_rounds>=goal else 1
    st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)

def undo_bead():
    if st.session_state.total_chants > 0:
        st.session_state.total_chants -= 1

def reset_session():
    st.session_state.current_bead = 0
    st.session_state.rounds_today = 0
    st.session_state.total_chants = 0
    st.session_state.start_time = None

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
start_session()
st.markdown("""
<div class="main-container">
  <div style="text-align:center; margin-top:10px; margin-bottom:20px;">
    <div style="font-size:26px; font-weight:700; color:#5d4037;">Current Round</div>
    <div style="font-size:14px; color:#8d6e63; margin-top:4px;">Hare Krishna Japa Tracker</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# MAIN LAYOUT
# ------------------------------------------------------------
with st.container():
    col_left, col_right = st.columns([2,2])
    
    # LEFT SIDE — BEAD RING
    with col_left:

        total = st.session_state.total_chants

        # Correct mala-style bead number
        if total == 0:
            display_bead = 0
            beads_to_light = 0
        else:
            display_bead = ((total - 1) % BEADS_PER_ROUND) + 1
            beads_to_light = display_bead

        # Glow when completing a round
        circle_extra_style = ""
        if display_bead == BEADS_PER_ROUND:
            circle_extra_style = "animation:beadGlow 1.5s infinite;"

        beads = []
        cx, cy = 130, 130
        r = 110

        for i in range(BEADS_PER_ROUND):
            ang = 2 * math.pi * i / BEADS_PER_ROUND
            x = cx + r * math.cos(ang)
            y = cy + r * math.sin(ang)
            active = i < beads_to_light
            color = "#ffcc80" if active else "#8d6e63"
            beads.append(
                f'<div style="position:absolute;width:12px;height:12px;border-radius:50%;'
                f'background:{color};left:{x}px;top:{y}px;box-shadow:0 0 4px rgba(0,0,0,0.5);"></div>'
            )

        st.markdown(f"""
        <div style="width:260px;height:260px;border-radius:50%;margin:auto;position:relative;
        background:radial-gradient(circle,#fff7e6 0%,#ffe0b2 60%,#ffb74d 100%);
        box-shadow:0 0 18px rgba(255,153,51,0.6);{circle_extra_style}">
            {''.join(beads)}
            <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
            font-size:22px;font-weight:700;color:#5d4037;">
                {display_bead} / {BEADS_PER_ROUND}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center;margin-top:10px;font-size:14px;color:#5d4037;">
            Hare Krishna Hare Krishna<br>Krishna Krishna Hare Hare<br>
            Hare Rama Hare Rama<br>Rama Rama Hare Hare
        </div>
        """, unsafe_allow_html=True)

        if st.button("🕉️ Tap Bead", use_container_width=True):
            st.session_state.total_chants += 1
            st.markdown("<script>window.playTap()</script>", unsafe_allow_html=True)

            # Round complete
            if st.session_state.total_chants % BEADS_PER_ROUND == 0:
                today = str(date.today())
                st.session_state.rounds_today += 1
                st.session_state.history[today] = st.session_state.history.get(today, 0) + 1
                update_streak()
                st.markdown("<script>window.playRoundComplete()</script>", unsafe_allow_html=True)

        st.caption("One bead • One chant • One step closer to Krishna")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("↩️ Undo", key="undo_button"):
                undo_bead()
        with c2:
            if st.button("🧹 Reset", key="reset_button"):
                reset_session()

      # RIGHT SIDE — STATS + TODAY'S GOAL
    with col_right:

        st.markdown("### Time Spent")
        st.markdown(f"**{get_time_spent()}**")

        st.markdown("### Today’s Goal")

        goal = st.session_state.user_daily_goal

        col_minus, col_slider, col_plus = st.columns([1, 6, 1])

        with col_minus:
            if st.button("➖", key="goal_minus"):
                goal = max(0, goal - 1)

        with col_plus:
            if st.button("➕", key="goal_plus"):
                goal = min(192, goal + 1)

        with col_slider:
            slider_value = st.slider(
                "today_goal_slider",
                min_value=0,
                max_value=192,
                value=goal,
                step=1,
                label_visibility="collapsed",
                key="goal_slider"
            )
            goal = slider_value

        if goal != st.session_state.user_daily_goal:
            st.session_state.user_daily_goal = goal
            save_user_goal(goal)

        st.markdown("### Rounds Today")
        st.markdown(f"**{st.session_state.rounds_today} / {goal}**")

        # PROGRESS BAR (ROUNDS-BASED)
        rounds_today = st.session_state.rounds_today
        progress = 0 if goal == 0 else min(rounds_today / goal, 1)
        pct = int(progress * 100)

        if progress >= 1 and not st.session_state.goal_complete_triggered:
            st.markdown("<script>window.playGoalComplete()</script>", unsafe_allow_html=True)
            st.session_state.goal_complete_triggered = True
        elif progress < 1 and st.session_state.goal_complete_triggered:
            st.session_state.goal_complete_triggered = False

        bar = """
            width:{percent}%;
            height:22px;
            background:linear-gradient(90deg,#ff9800,#ff5722,#e65100);
            border-radius:10px;
            transition:width 0.3s ease;
        """
        if progress >= 1:
            bar += "animation:goalPulse 1.2s infinite;"

        st.markdown(f"""
        <div style="width:100%;height:22px;margin-top:6px;border-radius:10px;">
            <div style="{bar.format(percent=pct)}"></div>
        </div>
        <div style="text-align:center;font-weight:600;color:#5d4037;margin-top:4px;">
            {rounds_today} / {goal} Rounds
        </div>
        """, unsafe_allow_html=True)

        total_goal_chants = goal * BEADS_PER_ROUND
        st.markdown("### Total Chants")
        st.markdown(f"**{st.session_state.total_chants} / {total_goal_chants}**")

# ------------------------------------------------------------
# TODAY'S PROGRESS
# ------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align:center;font-size:20px;font-weight:700;color:#5d4037;margin-bottom:10px;">
  Today’s Progress
</div>
""", unsafe_allow_html=True)

def progress_card(text, done):
    color = "#4CAF50" if done else "#BCAAA4"
    return f"""
    <div style="background:white;padding:12px;border-radius:10px;text-align:center;
    box-shadow:0 0 6px rgba(0,0,0,0.15);font-weight:600;color:{color};margin:5px;min-width:120px;">
        {text}
    </div>
    """

cols = st.columns(4)
for i, m in enumerate([4, 8, 12, 16]):
    with cols[i]:
        st.markdown(
            progress_card(f"{m} Rounds", st.session_state.rounds_today >= m),
            unsafe_allow_html=True
        )

st.markdown(
    f"<div style='text-align:center;margin-top:8px;color:#5d4037;font-weight:600;'>"
    f"{st.session_state.rounds_today} / {st.session_state.user_daily_goal} Rounds Completed"
    f"</div>",
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# PROGRESS OVERVIEW
# ------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align:center;font-size:20px;font-weight:700;color:#5d4037;margin-bottom:10px;">
  Progress Overview
</div>
""", unsafe_allow_html=True)

col_week, col_streak, col_hist = st.columns([1, 1, 2])

with col_week:
    total_week = sum(
        st.session_state.history.get(str(date.today() - timedelta(days=i)), 0)
        for i in range(7)
    )
    weekly_goal = st.session_state.user_daily_goal * 7

    st.markdown(f"""
    <div style="background:white;padding:14px;border-radius:10px;text-align:center;
    box-shadow:0 0 6px rgba(0,0,0,0.15);margin:5px;color:#5d4037;font-size:14px;">
        <div style="font-weight:700;margin-bottom:6px;">This Week</div>
        <div>{total_week} / {weekly_goal} rounds</div>
    </div>
    """, unsafe_allow_html=True)

with col_streak:
    st.markdown(f"""
    <div style="background:white;padding:14px;border-radius:10px;text-align:center;
    box-shadow:0 0 6px rgba(0,0,0,0.15);margin:5px;color:#5d4037;font-size:14px;">
        <div style="font-weight:700;margin-bottom:6px;">Current Streak</div>
        <div>{st.session_state.streak} days</div>
        <div style="font-size:12px;color:#8d6e63;">Best: {st.session_state.best_streak} days</div>
    </div>
    """, unsafe_allow_html=True)

with col_hist:
    if not st.session_state.history:
        body = "<div style='text-align:center;color:#8d6e63;'>No history yet. Chant and it will appear here.</div>"
    else:
        body = ""
        for i in range(7):
            d = date.today() - timedelta(days=i)
            rounds = st.session_state.history.get(str(d), 0)
            body += f"<div>{d.strftime('%b %d (%a)')}: <strong>{rounds}</strong> rounds</div>"

    st.markdown(f"""
    <div style="background:white;padding:14px;border-radius:10px;box-shadow:0 0 6px rgba(0,0,0,0.15);
    margin:5px;color:#5d4037;font-size:14px;">
        <div style="font-weight:700;margin-bottom:6px;text-align:center;">Japa History</div>
        <div style="font-size:13px;">{body}</div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# FLOATING MANTRA BAR
# ------------------------------------------------------------
st.markdown("""
<div style="
    position:fixed;bottom:0;left:0;width:100%;
    background:#33691e;color:white;padding:10px;text-align:center;
    font-size:18px;font-weight:700;box-shadow:0 -2px 10px rgba(0,0,0,0.3);
">
    🕉️ Hare Krishna Hare Krishna Krishna Krishna Hare Hare —
    Hare Rama Hare Rama Rama Rama Hare Hare 🕉️
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("""
<div style="margin-top:40px;text-align:center;font-size:18px;font-weight:600;color:#ff9933;">
    ✨ Chant and Be Happy ✨
</div>
""", unsafe_allow_html=True)

