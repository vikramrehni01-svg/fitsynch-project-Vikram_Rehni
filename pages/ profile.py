import streamlit as st
import pandas as pd

def profile_page():
    st.title("Profile")
    st.header("Health Stats")
    st.subheader("View your health progress over time")

    # Mock graphs for demonstration purpose
    stats_data = {
        'Daily': [10, 20, 30, 40],
        'Weekly': [100, 150, 200, 250],
        'Monthly': [400, 450, 500, 550],
        'Yearly': [1000, 2000, 3000, 4000],
    }
    
    df = pd.DataFrame(stats_data)

    st.line_chart(df)
    st.info("Mock streak tracker: Keep up with your goals as shown in GitHub style streaks.")
