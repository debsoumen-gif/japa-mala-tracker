# ============================================================
#   File Name: session_init.py
#   Full Path: C:/japa-mala-tracker/components/session_init.py
#
#   Author: Soumen
#   Location: Paramus, New Jersey, United States
#   Time Zone: New York (EST)
#   Timestamp: 2026-06-11 08:20 AM EST
#
#   Purpose:
#     Initialize all Streamlit session_state variables required
#     for the Japa Mala Tracker to function safely.
#
#   Functionality:
#     • Ensures all counters exist before use
#     • Prevents KeyError crashes
#     • Centralizes session initialization logic
#
#   Notes:
#     • Must be imported at the top of app.py
#
#   Debug:
#     • Print st.session_state to verify initialization
# ============================================================

import streamlit as st

def init_session_state():
    defaults = {
        "mala_bead_count": 0,
        "mala_round_count": 0,
        "mala_set_count": 0,
        "sadhana_streak": 0,
        "last_streak_date": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
