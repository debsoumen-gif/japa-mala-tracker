import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import math

st.set_page_config(page_title="Hare Krishna Japa Tracker", page_icon="🙏")

# ------------------------------------------------------------
# GLOBAL BACKGROUND + MOBILE TWEAKS
# ------------------------------------------------------------
st.markdown("""
<style>
body, .stApp {
    background-color: #FFF7E6 !important;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Centered main content */
.main-container {
    max-width: 900px;
    margin: 0 auto;
}

/* Mobile-friendly tweaks */
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
    st.session_state.current_bead = 0
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

DAILY_GOAL = 16
BEADS_PER_ROUND = 108
TOTAL_GOAL_CHANTS = DAILY_GOAL * BEADS_PER_ROUND

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

def register_round_if_complete():
    if st.session_state.current_bead >= BEADS_PER_ROUND:
        st.session_state.current_bead = 0
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

    if today_rounds >= DAILY_GOAL:
        if yesterday_rounds >= DAILY_GOAL:
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

# ------------------------------------------------------------
# PAGE HEADER
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
# MAIN LAYOUT (TOP)
# ------------------------------------------------------------
with st.container():
    col_left, col_right = st.columns([2, 2])

    # ------------------ CIRCULAR BEAD RING + TAP ------------------
    with col_left:
        beads_html = []
        center_x, center_y = 130, 130
        radius = 110

        for i in range(BEADS_PER_ROUND):
            angle = 2 * math.pi * i / BEADS_PER_ROUND
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            active = i < st.session_state.current_bead
            color = "#8d6e63" if not active else "#ffcc80"
            beads_html.append(
                f'<div style="position:absolute; width:12px; height:12px; '
                f'border-radius:50%; background:{color}; '
                f'left:{x}px; top:{y}px; box-shadow:0 0 4px rgba(0,0,0,0.5);"></div>'
            )

        circle_html = f"""
        <div style="
            width:260px;
            height:260px;
            border-radius:50%;
            margin:auto;
            position:relative;
            background:radial-gradient(circle, #fff7e6 0%, #ffe0b2 60%, #ffb74d 100%);
            box-shadow:0 0 18px rgba(255,153,51,0.6);
        ">
            {''.join(beads_html)}
            <div style="
                position:absolute;
                top:50%;
                left:50%;
                transform:translate(-50%, -50%);
                font-size:22px;
                font-weight:700;
                color:#5d4037;
                text-align:center;
            ">
                {st.session_state.current_bead} / {BEADS_PER_ROUND}
            </div>
        </div>
        """

        st.markdown(circle_html, unsafe_allow_html=True)

        st.markdown(
            """
        <div style="text-align:center; margin-top:10px; font-size:14px; color:#5d4037;">
            Hare Krishna Hare Krishna<br>
            Krishna Krishna Hare Hare<br>
            Hare Rama Hare Rama<br>
            Rama Rama Hare Hare
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("🕉️ Tap Bead", use_container_width=True):
            st.session_state.current_bead += 1
            st.session_state.total_chants += 1
            components.html("<script>parent.postMessage('tap', '*');</script>", height=0)
            register_round_if_complete()

        st.caption("One bead • One chant • One step closer to Krishna")

        col_undo, col_reset = st.columns(2)
        with col_undo:
            if st.button("↩️ Undo"):
                undo_bead()
        with col_reset:
            if st.button("🧹 Reset"):
                reset_session()

    # ------------------ RIGHT SIDE STATS ------------------
    with col_right:
        st.markdown("### Time Spent")
        st.markdown(f"**{get_time_spent()}**")

        st.markdown("### Rounds Today")
        st.markdown(f"**{st.session_state.rounds_today} / {DAILY_GOAL}**")

        st.markdown("### Daily Goal")
        st.markdown(f"**{DAILY_GOAL} Rounds**")

        st.markdown("### Total Chants")
        st.markdown(f"**{st.session_state.total_chants} / {TOTAL_GOAL_CHANTS}**")

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

cols = st.columns(4)
milestones = [4, 8, 12, 16]

for i, m in enumerate(milestones):
    with cols[i]:
        st.markdown(
            progress_card(f"{m} Rounds", st.session_state.rounds_today >= m),
            unsafe_allow_html=True,
        )

st.markdown(
    f"<div style='text-align:center; margin-top:8px; color:#5d4037; font-weight:600;'>{st.session_state.rounds_today} / {DAILY_GOAL} Rounds Completed</div>",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# PROGRESS OVERVIEW (BOTTOM SECTION)
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

# This Week card
with col_week:
    total_week = 0
    for i in range(7):
        day = str(date.today() - timedelta(days=i))
        total_week += st.session_state.history.get(day, 0)
    weekly_goal = DAILY_GOAL * 7

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

# Current Streak card
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

# Japa History card (wider)
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
        # show last 7 days
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
