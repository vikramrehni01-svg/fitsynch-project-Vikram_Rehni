import streamlit as st

def theme_switcher():
    themes = ['Light', 'Dark']
    chosen_theme = st.sidebar.radio('Select Theme', themes)
    
    # Mock application: The theme application logic will be extended 
    st.sidebar.write(f"Selected theme: {chosen_theme}")