import streamlit as st

from ui.styles import load_theme
from ui.generate_page import generate_page
from ui.library_page import library_page
from ui.screen_page import screen_page

st.set_page_config(
    page_title="Q-Enzyme Quantum Reaction Pathway Screener",
    layout="wide",
    initial_sidebar_state="collapsed"
)
load_theme()

if "candidates" not in st.session_state:
    st.session_state.candidates = []

if "last_simulation" not in st.session_state:
    st.session_state.last_simulation = None

st.markdown(
    """
    <div style="margin-bottom: 1.2rem;">
        <h1 style="margin-bottom: 0.2rem;">
            🔬 Q-Enzyme Quantum Reaction Pathway Screener
        </h1>
        <p style="color:#9aeaff; font-size:1.05rem;">
            Physics-driven screening of catalytic Hamiltonians via
            first-principles quantum dynamics
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.markdown(
    f"""
    <div class="candidate-badge">
        Stored candidates: {len(st.session_state.candidates)} / 5
    </div>
    """,
    unsafe_allow_html=True
)

tab_generate, tab_library, tab_screen = st.tabs(
    [
        "🧪 Generate",
        "📚 Candidate Library",
        "📊 Screen & Rank"
    ]
)

with tab_generate:
    generate_page()

with tab_library:
    library_page()

with tab_screen:
    screen_page()

def reset_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


st.markdown('<div class="reset-container">', unsafe_allow_html=True)

if st.button("Reset session"):
    reset_session()

st.markdown('</div>', unsafe_allow_html=True)
