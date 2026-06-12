import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import math

st.set_page_config(page_title="Hare Krishna Japa Tracker", page_icon="🙏")

# ------------------------------------------------------------
# GLOBAL STYLING
# ------------------------------------------------------------
st.markdown("""
<style>
body, .stApp {
    background-color: #FFF7E6 !important;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Main container */
.main-container {
    max-width: 900px;
    margin: 0 auto;
}

/* Glossy purple-gold buttons */
.stButton > button {
    background: linear-gradient(145deg, #5e35b1, #7e57c2);
    color: #ffffff;
    border-radius: 999px;
    border: 2px solid #ffd54f;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    box-shadow: 0 4px 10px rgba(94, 53, 177, 0.6), 0 0 8px rgba(255, 213, 79, 0.7);
    text-shadow: 0 1px 2px rgba(0,0,0,0.4);
}
.stButton > button:hover {
    background: linear-gradient(145deg, #7e57c2, #5e35b1);
    box-shadow: 0 6px 14px rgba(94, 53, 177, 0.8), 0 0 10px rgba(255, 213, 79, 0.9);
}

/* Slider label */
.css-1dp5vir, .css-10trblm {
    color: #5d4037 !important;
}

/* Mobile tweaks */
@media (max-width: 768px) {
    .main-container {
        padding: 8px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# JS BRIDGE FOR SOUND + VIBRATION
# ------------------------------------------------------------
components.html("""
<script>
function playTap() {
    var audio = new Audio('/assets/tap.mp3');
    audio.play();
    if (navigator.vibrate) navigator.vibrate(30);
}
function playRoundComplete() {
    var audio = new Audio('/assets/round_complete.mp3');
    audio.play();
    if (navigator.vibrate) navigator.vibrate([120, 60, 120]);
}
window.addEventListener("message", (event) => {
    if (event.data === "tap") playTap();
    if (event.data === "round_complete") playRoundComplete();
});
</script>
""", height=0)

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------
if "current_bead" not in st.session_state:
    st.session_state.current_bead = 0  # raw taps (including guru bead)
if "rounds_today" not in st.session_state:
    st.session_state.rounds_today = 0
if "total_chants" not in st.session_state:
    st.session_state.total_chants = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "history" not in st.session_state:
    st.session_state.history = {}
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "best_streak" not in st.session_state:
    st.session_state.best_streak = 0
if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = 16  # default

BEADS_PER_ROUND = 108

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def start_session():
    if st.session_state.start_time is None:
        st.session_state.start_time = datetime.now()

def get_time_spent():
    if st.session_state.start_time is None:
        return "00:00:00"
    delta = datetime.now() - st.session_state.start_time
    return str(timedelta(seconds=int(delta.total_seconds())))

def display_bead_count():
    # first tap is guru bead → display starts at 0
    return max(st.session_state.current_bead - 1, 0)

def register_round_if_complete():
    if display_bead_count() >= BEADS_PER_ROUND:
        st.session_state.current_bead = 1  # back to guru bead position
        st.session_state.rounds_today += 1
        today = str(date.today())
        st.session_state.history[today] = st.session_state.history.get(today, 0) + 1
        update_streak()
        components.html("<script>parent.postMessage('round_complete', '*');</script>", height=0)

def update_streak():
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))
    today_rounds = st.session_state.history.get(today, 0)
    yesterday_rounds = st.session_state.history.get(yesterday, 0)
    goal = st.session_state.daily_goal

    if today_rounds >= goal:
        if yesterday_rounds >= goal:
            st.session_state.streak += 1
        else:
            st.session_state.streak = 1

    st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)

def undo_bead():
    if st.session_state.current_bead > 0:
        st.session_state.current_bead -= 1
        st.session_state.total_chants = max(st.session_state.total_chants - 1, 0)

def reset_session():
    st.session_state.current_bead = 0
    st.session_state.rounds_today = 0
    st.session_state.total_chants = 0
    st.session_state.start_time = None

def total_goal_chants():
    return st.session_state.daily_goal * BEADS_PER_ROUND

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
start_session()

st.markdown(
    """
<div class="main-container">
  <div style="text-align:center; margin-top:10px; margin-bottom:20px;">
    <div style="font-size:26px; font-weight:700; color:#5d4037;">
      Current Round
    </div>
    <div style="font-size:14px; color:#8d6e63; margin-top:4px;">
      Hare Krishna Japa Tracker
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# MAIN LAYOUT
# ------------------------------------------------------------
with st.container():
    col_left, col_right = st.columns([2, 2])

    # ------------------ LEFT: BEAD RING + CONTROLS ------------------
    with col_left:
        beads_html = []
        center_x, center_y = 170, 170
        radius = 140

        active_index = display_bead_count()

        for i in range(BEADS_PER_ROUND):
            angle = 2 * math.pi * i / BEADS_PER_ROUND
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            is_active = i < active_index
            base_gradient = (
                "radial-gradient(circle at 30% 30%, #f5e0c8 0%, #d7b894 45%, #b08a5a 80%)"
            )
            active_gradient = (
                "radial-gradient(circle at 30% 30%, #ffe082 0%, #ffca28 45%, #ffb300 80%)"
            )

            color_style = active_gradient if is_active else base_gradient

            beads_html.append(
                f'''
                <div style="
                    position:absolute;
                    width:16px;
                    height:14px;
                    border-radius:50% / 45%;
                    background:{color_style};
                    left:{x}px;
                    top:{y}px;
                    box-shadow:0 2px 4px rgba(0,0,0,0.45);
                    border:1px solid rgba(121,85,72,0.6);
                "></div>
                '''
            )

        circle_html = f"""
        <div style="
            width:340px;
            height:340px;
            border-radius:50%;
            margin:auto;
            position:relative;
            background:radial-gradient(circle, #fff7e6 0%, #ffe0b2 55%, #ffb74d 100%);
            box-shadow:0 0 22px rgba(255,153,51,0.7);
        ">
            {''.join(beads_html)}
            <div style="
                position:absolute;
                top:50%;
                left:50%;
                transform:translate(-50%, -50%);
                font-size:16px;
                font-weight:600;
                color:#5d4037;
                text-align:center;
                line-height:1.3;
            ">
                <div style="font-size:18px; font-weight:700; margin-bottom:6px;">
                    Current Round
                </div>
                <div style="font-size:13px; margin-bottom:4px;">
                    Hare Krishna Hare Krishna<br>
                    Krishna Krishna Hare Hare<br>
                    Hare Rama Hare Rama<br>
                    Rama Rama Hare Hare
                </div>
                <div style="font-size:18px; font-weight:700; margin-top:6px;">
                    {display_bead_count()} / {BEADS_PER_ROUND}
                </div>
            </div>
        </div>
        """

        st.markdown(circle_html, unsafe_allow_html=True)

        # Daily goal slider (DG-2)
        st.markdown(
            "<div style='text-align:center; margin-top:10px; color:#5d4037; font-weight:600;'>Daily Goal (Rounds per Day)</div>",
            unsafe_allow_html=True,
        )
        st.session_state.daily_goal = st.slider(
            "Daily Goal (Rounds per Day)",
            min_value=1,
            max_value=192,
            value=st.session_state.daily_goal,
        )

        if st.button("🕉️ Tap Bead", use_container_width=True):
            st.session_state.current_bead += 1
            st.session_state.total_chants += 1
            components.html("<script>parent.postMessage('tap', '*');</script>", height=0)
            register_round_if_complete()

        col_undo, col_reset = st.columns(2)
        with col_undo:
            if st.button("↩️ Undo"):
                undo_bead()
        with col_reset:
            if st.button("🧹 Reset"):
                reset_session()

    # ------------------ RIGHT: STATS ------------------
    with col_right:
        st.markdown("### Time Spent")
        st.markdown(f"**{get_time_spent()}**")

        st.markdown("### Rounds Today")
        st.markdown(f"**{st.session_state.rounds_today} / {st.session_state.daily_goal}**")

        st.markdown("### Daily Goal")
        st.markdown(f"**{st.session_state.daily_goal} Rounds**")

        st.markdown("### Total Chants")
        st.markdown(f"**{st.session_state.total_chants} / {total_goal_chants()}**")

# ------------------------------------------------------------
# TODAY'S PROGRESS
# ------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
<div style="text-align:center; font-size:20px; font-weight:700; color:#5d4037; margin-bottom:10px;">
  Today’s Progress
</div>
""",
    unsafe_allow_html=True,
)

def progress_card(text, done):
    color = "#4CAF50" if done else "#BCAAA4"
    return f"""
    <div style="
        background:white;
        padding:12px;
        border-radius:10px;
        text-align:center;
        box-shadow:0 0 6px rgba(0,0,0,0.15);
        font-weight:600;
        color:{color};
        margin:5px;
        min-width:120px;
    ">
        {text}
    </div>
    """

goal = st.session_state.daily_goal
milestones = [
    max(1, goal // 4),
    max(1, goal // 2),
    max(1, (3 * goal) // 4),
    goal,
]

cols = st.columns(4)
for i, m in enumerate(milestones):
    with cols[i]:
        st.markdown(
            progress_card(f"{m} Rounds", st.session_state.rounds_today >= m),
            unsafe_allow_html=True,
        )

st.markdown(
    f"<div style='text-align:center; margin-top:8px; color:#5d4037; font-weight:600;'>{st.session_state.rounds_today} / {goal} Rounds Completed</div>",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# PROGRESS OVERVIEW (BOTTOM)
# ------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
<div style="text-align:center; font-size:20px; font-weight:700; color:#5d4037; margin-bottom:10px;">
  Progress Overview
</div>
""",
    unsafe_allow_html=True,
)

col_week, col_streak, col_history = st.columns([1, 1, 2])

# This Week
with col_week:
    total_week = 0
    for i in range(7):
        day = str(date.today() - timedelta(days=i))
        total_week += st.session_state.history.get(day, 0)
    weekly_goal = st.session_state.daily_goal * 7

    week_html = f"""
    <div style="
        background:white;
        padding:14px;
        border-radius:10px;
        text-align:center;
        box-shadow:0 0 6px rgba(0,0,0,0.15);
        margin:5px;
        color:#5d4037;
        font-size:14px;
    ">
        <div style="font-weight:700; margin-bottom:6px;">This Week</div>
        <div>{total_week} / {weekly_goal} rounds</div>
    </div>
    """
    st.markdown(week_html, unsafe_allow_html=True)

# Current Streak
with col_streak:
    streak_html = f"""
    <div style="
        background:white;
        padding:14px;
        border-radius:10px;
        text-align:center;
        box-shadow:0 0 6px rgba(0,0,0,0.15);
        margin:5px;
        color:#5d4037;
        font-size:14px;
    ">
        <div style="font-weight:700; margin-bottom:6px;">Current Streak</div>
        <div>{st.session_state.streak} days</div>
        <div style="font-size:12px; color:#8d6e63;">Best: {st.session_state.best_streak} days</div>
    </div>
    """
    st.markdown(streak_html, unsafe_allow_html=True)

# Japa History (wider)
with col_history:
    history_html_header = """
    <div style="
        background:white;
        padding:14px;
        border-radius:10px;
        box-shadow:0 0 6px rgba(0,0,0,0.15);
        margin:5px;
        color:#5d4037;
        font-size:14px;
    ">
        <div style="font-weight:700; margin-bottom:6px; text-align:center;">Japa History</div>
        <div style="font-size:13px;">
    """
    history_html_footer = """
        </div>
    </div>
    """

    body = ""
    if not st.session_state.history:
        body = "<div style='text-align:center; color:#8d6e63;'>No history yet. Chant and it will appear here.</div>"
    else:
        for i in range(7):
            d = date.today() - timedelta(days=i)
            ds = str(d)
            rounds = st.session_state.history.get(ds, 0)
            body += f"<div>{d.strftime('%b %d (%a)')}: <strong>{rounds}</strong> rounds</div>"

    st.markdown(history_html_header + body + history_html_footer, unsafe_allow_html=True)

# ------------------------------------------------------------
# FLOATING MANTRA BAR
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
# FOOTER
# ------------------------------------------------------------
st.markdown("""
<div style="
    margin-top:40px;
    text-align:center;
    font-size:18px;
    font-weight:600;
    color:#ff9933;
">
    ✨ Chant and Be Happy ✨
</div>
""", unsafe_allow_html=True)
