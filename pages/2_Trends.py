import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from components.theme_switcher import apply_theme
apply_theme()

def apply_plotly_theme(fig):
    dark_mode = st.session_state.dark_mode

    if dark_mode:
        fig.update_layout(
            paper_bgcolor="#1c1f26",
            plot_bgcolor="#1c1f26",
            font_color="#FFFFFF"
        )
    else:
        fig.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font_color="#2C2C2C"
        )

    fig.update_xaxes(gridcolor="#E5E1DA")
    fig.update_yaxes(gridcolor="#E5E1DA")

    return fig


st.title("Trends & Insights")

# Sidebar
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["Last 7 Days", "Last 30 Days", "All Time"]
)

# Data
data = pd.DataFrame({
    "Date": pd.date_range(end=pd.Timestamp.today(), periods=90),
    "Recovery Score": np.random.randint(40, 80, 90),
    "Sleep Hours": np.random.uniform(6, 8, 90).round(1),
    "Steps": np.random.randint(6000, 15000, 90)
})

today = pd.Timestamp.today()

if time_range == "Last 7 Days":
    df = data[data["Date"] >= today - pd.Timedelta(days=7)]
elif time_range == "Last 30 Days":
    df = data[data["Date"] >= today - pd.Timedelta(days=30)]
else:
    df = data

df = df.sort_values("Date")

# -----------------------------
# SUMMARY
# -----------------------------
st.subheader("Summary Statistics")
st.markdown('<div class="card">', unsafe_allow_html=True)
st.dataframe(df.describe())
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# HISTOGRAMS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(df, x="Steps", nbins=15)
    fig = apply_plotly_theme(fig)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    df["Calories"] = (df["Steps"] * 0.04).astype(int)
    fig = px.histogram(df, x="Calories", nbins=15)
    fig = apply_plotly_theme(fig)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# LINE
# -----------------------------
fig = px.line(df, x="Date", y="Sleep Hours", markers=True)
fig = apply_plotly_theme(fig)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)