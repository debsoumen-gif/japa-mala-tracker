import streamlit as st
from datetime import date, timedelta

# ------------------------------------------------------------
# Initialize session state
# ------------------------------------------------------------
if "beads" not in st.session_state:
    st.session_state.beads = 0
if "mala" not in st.session_state:
    st.session_state.mala = 0
if "sets" not in st.session_state:
    st.session_state.sets = 0
if "last_streak_date" not in st.session_state:
    st.session_state.last_streak_date = None
if "streak" not in st.session_state:
    st.session_state.streak = 0

# ------------------------------------------------------------
# Page config
# ------------------------------------------------------------
st.set_page_config(page_title="Japa Mala Tracker", page_icon="🙏")

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
# Daily Goal (1 → 128 mala)
# ------------------------------------------------------------
daily_goal = st.slider(
    "🎯 Daily Goal (Mala)",
    min_value=1,
    max_value=128,
    step=1,
    value=16,
)

# ------------------------------------------------------------
# Button Row: Add bead + beads + sets
# ------------------------------------------------------------
col_add, col_beads, col_sets = st.columns([2, 1, 1])

with col_add:
    if st.button("🌸 ➕ Add 1 Bead", use_container_width=True):
        st.session_state.beads += 1

        # 108 beads = 1 mala
        if st.session_state.beads >= 108:
            st.session_state.beads = 0
            st.session_state.mala += 1

            # 16 mala = 1 set
            if st.session_state.mala >= 16:
                st.session_state.mala = 0
                st.session_state.sets += 1

with col_beads:
    st.button(f"Beads: {st.session_state.beads}", use_container_width=True)

with col_sets:
    st.button(f"Sets: {st.session_state.sets}", use_container_width=True)

# ------------------------------------------------------------
# Mala Progress (Centered Tile)
# ------------------------------------------------------------
mala_done = st.session_state.mala + (st.session_state.sets * 16)
mala_pending = max(daily_goal - mala_done, 0)

st.markdown(
    f"""
    <div style="
        margin-top:20px;
        padding:15px;
        background:#f3e8ff;
        border:2px solid #b57edc;
        border-radius:14px;
        text-align:center;
        width:70%;
        margin-left:auto;
        margin-right:auto;
        box-shadow:0 0 12px rgba(181,126,220,0.35);
    ">
        <div style="font-size:22px; font-weight:700; color:#4a2c6d;">
            🕉️ Mala Progress
        </div>
        <div style="font-size:18px; margin-top:6px; color:#4a2c6d;">
            {mala_done} done
        </div>
        <div style="font-size:18px; margin-top:4px; color:#4a2c6d;">
            {mala_pending} pending
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Streak Logic
# ------------------------------------------------------------
today = str(date.today())

if mala_done >= daily_goal:
    if st.session_state.last_streak_date != today:
        st.session_state.streak += 1
        st.session_state.last_streak_date = today

st.markdown(
    f"""
    <div style="
        margin-top:20px;
        padding:12px;
        background:#e6ffe6;
        border:2px solid #4caf50;
        border-radius:12px;
        text-align:center;
        font-size:20px;
        font-weight:600;
        color:#2e7d32;">
        🌸 Sādhanā Streak: {st.session_state.streak} days
    </div>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# 🌺 Flying Hare Krishna Banner
# ------------------------------------------------------------
st.markdown(
    """
    <marquee behavior="alternate" scrollamount="4"
        style="font-size:26px; font-weight:800; color:#b30059; margin-bottom:10px;">
        🌸 Hare Krishna Hare Krishna Krishna Krishna Hare Hare —
        Hare Rama Hare Rama Rama Rama Hare Hare 🌸
    </marquee>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# 🌼 Bhakti Progress Tracker
# ------------------------------------------------------------
st.markdown("### 🌼 Bhakti Progress Tracker")

# Total rounds = mala_done (from your mala logic)
total_rounds_today = mala_done

st.markdown("### 🕉️ Rounds Chanted Today")
st.markdown(
    f"""
    <div style="
        background:#f7e9ff;
        padding:14px;
        border-radius:12px;
        text-align:center;
        border:2px solid #b57edc;
        font-weight:600;
        color:#4a2c6d;
        font-size:22px;">
        {total_rounds_today} rounds
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 📘 Additional Sādhanā Activities
# ------------------------------------------------------------
reading = st.checkbox("📘 Read Gītā / Bhāgavatam today")
kirtan = st.checkbox("🎶 Participated in kīrtan")
service = st.checkbox("🙏 Performed some seva")

# ------------------------------------------------------------
# 🌿 Bhakti Score Calculation
# ------------------------------------------------------------
score = (total_rounds_today / daily_goal) + sum([reading, kirtan, service])
progress_value = min(score / 2, 1.0)

st.progress(progress_value)

# ------------------------------------------------------------
# 🌸 Motivational Message
# ------------------------------------------------------------
if progress_value == 1.0:
    st.success("🌸 Wonderful! Your sādhanā today is complete.")
elif progress_value > 0.5:
    st.info("🌼 You're doing beautifully — keep going.")
else:
    st.write("🕊️ A little more devotion will complete your day.")
