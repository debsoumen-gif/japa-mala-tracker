import streamlit as st
from datetime import datetime, date, timedelta

st.set_page_config(page_title="Hare Krishna Japa Tracker", page_icon="🙏")

# -----------------------------
# Session State
# -----------------------------
if "current_bead" not in st.session_state:
    st.session_state.current_bead = 0  # 0–108
if "rounds_today" not in st.session_state:
    st.session_state.rounds_today = 0
if "total_chants" not in st.session_state:
    st.session_state.total_chants = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "history" not in st.session_state:
    st.session_state.history = {}  # {date_str: rounds}
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "best_streak" not in st.session_state:
    st.session_state.best_streak = 0

DAILY_GOAL_ROUNDS = 16
ROUNDS_PER_MALA = 1
BEADS_PER_ROUND = 108
TOTAL_GOAL_CHANTS = DAILY_GOAL_ROUNDS * BEADS_PER_ROUND  # 1728

# -----------------------------
# Helper Functions
# -----------------------------
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
        today_str = str(date.today())
        st.session_state.history[today_str] = st.session_state.history.get(today_str, 0) + 1
        update_streak()

def update_streak():
    today_str = str(date.today())
    yesterday_str = str(date.today() - timedelta(days=1))

    today_rounds = st.session_state.history.get(today_str, 0)
    yesterday_rounds = st.session_state.history.get(yesterday_str, 0)

    if today_rounds >= DAILY_GOAL_ROUNDS:
        if yesterday_rounds >= DAILY_GOAL_ROUNDS:
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

# -----------------------------
# Header
# -----------------------------
st.markdown("## Hare Krishna 🙏  Radhe Radhe!")

# -----------------------------
# Main Layout
# -----------------------------
tab_japa, tab_history, tab_stats, tab_quotes, tab_settings = st.tabs(
    ["Japa", "History", "Stats", "Quotes", "Settings"]
)

# -----------------------------
# Japa Tab
# -----------------------------
with tab_japa:
    start_session()

    col_left, col_right = st.columns([2, 2])

    with col_left:
        st.markdown("### Current Round")
        st.markdown(
            f"""
            <div style="
                width:220px;
                height:220px;
                border-radius:50%;
                border:6px solid #ff9933;
                margin:auto;
                display:flex;
                align-items:center;
                justify-content:center;
                background:radial-gradient(circle, #fff7e6 0%, #ffe0b2 60%, #ffb74d 100%);
                box-shadow:0 0 18px rgba(255,153,51,0.6);
                font-size:22px;
                font-weight:700;
                color:#5d4037;
            ">
                {st.session_state.current_bead} / {BEADS_PER_ROUND}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="text-align:center; margin-top:10px; font-size:14px; color:#ccc;">
                Hare Krishna Hare Krishna<br>
                Krishna Krishna Hare Hare<br>
                Hare Rama Hare Rama<br>
                Rama Rama Hare Hare
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🕉️ Tap Bead"):
            st.session_state.current_bead += 1
            st.session_state.total_chants += 1
            register_round_if_complete()

        st.caption("One bead • One chant • One step closer to Krishna")

        col_undo, col_reset = st.columns(2)
        with col_undo:
            if st.button("↩️ Undo"):
                undo_bead()
        with col_reset:
            if st.button("🧹 Reset"):
                reset_session()

    with col_right:
        st.markdown("### Time Spent")
        st.markdown(f"**{get_time_spent()}**")

        st.markdown("### Rounds Today")
        st.markdown(f"**{st.session_state.rounds_today} / {DAILY_GOAL_ROUNDS}**")

        st.markdown("### Daily Goal")
        st.markdown(f"**{DAILY_GOAL_ROUNDS} Rounds**")

        st.markdown("### Total Chants")
        st.markdown(
            f"**{st.session_state.total_chants} / {TOTAL_GOAL_CHANTS}**  (108 × {DAILY_GOAL_ROUNDS})"
        )

    st.markdown("---")
    st.markdown("### Today’s Progress")

    milestones = [4, 8, 12, 16]
    cols = st.columns(len(milestones))
    for i, m in enumerate(milestones):
        with cols[i]:
            done = st.session_state.rounds_today >= m
            status = "✓" if done else "…"
            st.markdown(f"**{m} Rounds {status}**")

    st.markdown(
        f"**{st.session_state.rounds_today} / {DAILY_GOAL_ROUNDS} Rounds Completed**"
    )

# -----------------------------
# History Tab
# -----------------------------
with tab_history:
    st.markdown("### Japa History")
    if not st.session_state.history:
        st.write("No history yet. Chant and it will appear here.")
    else:
        for d, r in sorted(st.session_state.history.items(), reverse=True):
            st.write(f"**{d}:** {r} rounds")

# -----------------------------
# Stats Tab
# -----------------------------
with tab_stats:
    st.markdown("### This Week")
    # Simple weekly summary (last 7 days)
    total_week = 0
    for i in range(7):
        day_str = str(date.today() - timedelta(days=i))
        total_week += st.session_state.history.get(day_str, 0)

    weekly_goal = DAILY_GOAL_ROUNDS * 7
    st.markdown(f"**{total_week} / {weekly_goal} Rounds Completed**")

    st.markdown("### Current Streak")
    st.markdown(f"**{st.session_state.streak} Days**")
    st.markdown(f"Best: **{st.session_state.best_streak} Days**")

# -----------------------------
# Quotes Tab
# -----------------------------
with tab_quotes:
    st.markdown("### Srila Prabhupada Says")
    st.markdown(
        """
        > “Chant and be happy. This is the only way.”  
        > — Srila Prabhupada
        """
    )

# -----------------------------
# Settings Tab
# -----------------------------
with tab_settings:
    st.markdown("### Settings")
    new_goal = st.number_input(
        "Daily Goal (Rounds)", min_value=1, max_value=64, value=DAILY_GOAL_ROUNDS
    )
    st.info("For now this is static in code; we can wire it to state if you want.")

# -----------------------------
# Floating Mantra Bar
# -----------------------------
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

# -----------------------------
# Footer
# -----------------------------
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
