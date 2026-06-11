# ============================================================
#   File Name: audio.py
#   Full Path: C:/japa-mala-tracker/components/audio.py
#
#   Author: Soumen
#   Location: Paramus, New Jersey, United States
#   Time Zone: New York (EST)
#   Timestamp: 2026-06-11 08:20 AM EST
#
#   Purpose:
#     Provide audio playback for devotional cues (bell, conch).
#
#   Functionality:
#     • Embeds HTML audio tags
#     • Plays sound on bead/round/set transitions
#
#   Notes:
#     • Audio files must exist under /assets/
#
#   Debug:
#     • Check browser console if audio does not play
# ============================================================

import streamlit as st

def play_sound(path: str):
    audio_html = f"""
        <audio autoplay>
            <source src="{path}" type="audio/mpeg">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
