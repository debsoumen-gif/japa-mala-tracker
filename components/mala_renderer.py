# ============================================================
#   File Name: mala_renderer.py
#   Full Path: C:/japa-mala-tracker/components/mala_renderer.py
#
#   Author: Soumen
#   Location: Paramus, New Jersey, United States
#   Time Zone: New York (EST)
#   Timestamp: 2026-06-11 08:20 AM EST
#
#   Purpose:
#     Render the 108‑bead inner mala and 16‑round outer mala
#     using custom HTML + CSS.
#
#   Functionality:
#     • Generates SVG/HTML for mala rings
#     • Supports dynamic bead/round progress
#     • Integrates with theme.css and mala.css
#
#   Notes:
#     • Ensure CSS files are loaded in app.py
#
#   Debug:
#     • Print generated HTML if beads misalign
# ============================================================

def render_mala_html(inner_total, inner_done, outer_total, outer_done, size_px):
    # Placeholder — you can replace with your full SVG later
    return f"""
    <div style="text-align:center;">
        <div style="font-size:18px; color:#b57edc;">
            Mala Progress: {inner_done}/{inner_total} beads
        </div>
    </div>
    """
