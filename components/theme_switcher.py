import streamlit as st

def apply_theme():
    # -----------------------------
    # 1. INITIALIZE STATE (CRITICAL)
    # -----------------------------
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    # -----------------------------
    # 2. TOGGLE (SIDEBAR)
    # -----------------------------
    st.sidebar.markdown("### 🌗 Theme")
    toggle = st.sidebar.toggle(
        "Dark Mode",
        value=st.session_state.dark_mode,
        key="theme_toggle"  # prevents duplicate widget errors
    )
    st.session_state.dark_mode = toggle

    # -----------------------------
    # 3. SAFE LOCAL VARIABLE
    # -----------------------------
    dark_mode = st.session_state.dark_mode

    # -----------------------------
    # 4. COLOR SYSTEM
    # -----------------------------
    bg_color       = "#0E1117" if dark_mode else "#F5F3EF"   # cream background
    text_color     = "#FFFFFF" if dark_mode else "#2C2C2C"
    card_color     = "#1c1f26" if dark_mode else "#FFFFFF"
    border_color   = "#333333" if dark_mode else "#E5E1DA"
    sidebar_bg     = "#161A22" if dark_mode else "#EEEAE4"
    accent_color   = "#00C9A7" if dark_mode else "#4A90E2"

    # -----------------------------
    # 5. GLOBAL CSS
    # -----------------------------
    st.markdown(f"""
    <style>
    /* ---------- APP BACKGROUND ---------- */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        transition: all 0.3s ease;
    }}

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
    }}

    section[data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}

    /* ---------- TEXT ---------- */
    h1, h2, h3, h4, h5, h6, p, div, span, label {{
        color: {text_color} !important;
    }}

    /* ---------- CARD SYSTEM ---------- */
    .card {{
        background-color: {card_color};
        border-radius: 18px;
        padding: 20px;
        border: 1px solid {border_color};
        
        /* depth */
        box-shadow: {"0px 6px 20px rgba(0,0,0,0.3)" if dark_mode else "0px 4px 12px rgba(0,0,0,0.08)"};

        /* animation */
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }}

    .card:hover {{
        transform: translateY(-6px) scale(1.01);
        box-shadow: {"0px 10px 30px rgba(0,0,0,0.5)" if dark_mode else "0px 8px 20px rgba(0,0,0,0.12)"};
    }}

    /* ---------- BUTTONS ---------- */
    .stButton > button {{
        background: linear-gradient(135deg, {accent_color}, #6a11cb);
        color: white;
        border-radius: 12px;
        padding: 10px 18px;
        border: none;
        font-weight: 600;
        transition: all 0.2s ease;
    }}

    .stButton > button:hover {{
        transform: scale(1.05);
        opacity: 0.9;
    }}

    /* ---------- INPUTS ---------- */
    .stSelectbox div, .stTextInput input {{
        background-color: {card_color} !important;
        color: {text_color} !important;
        border-radius: 10px !important;
    }}

    /* ---------- CHART FIX ---------- */
    [data-testid="stPlotlyChart"] {{
        background-color: transparent !important;
    }}
    </style>
    """, unsafe_allow_html=True)