import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from components.theme_switcher import apply_theme
apply_theme()

# -----------------------------
# PLOTLY THEME
# -----------------------------
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


# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["Last 7 Days", "Last 30 Days", "All Time"]
)

# -----------------------------
# TITLE
# -----------------------------
st.title("FitSync - Personal Health Analytics")

# -----------------------------
# DATA
# -----------------------------
data = pd.DataFrame({
    "Date": pd.date_range(end=pd.Timestamp.today(), periods=90),
    "Recovery Score": np.random.randint(40, 80, 90),
    "Sleep Hours": np.random.uniform(6, 8, 90).round(1),
    "Steps": np.random.randint(6000, 12000, 90)
})

today = pd.Timestamp.today()

if time_range == "Last 7 Days":
    filtered_data = data[data["Date"] >= today - pd.Timedelta(days=7)]
elif time_range == "Last 30 Days":
    filtered_data = data[data["Date"] >= today - pd.Timedelta(days=30)]
else:
    filtered_data = data

filtered_data = filtered_data.sort_values("Date")

# -----------------------------
# METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("Average Steps", int(filtered_data["Steps"].mean()))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("Avg Sleep Hours", round(filtered_data["Sleep Hours"].mean(), 1))
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("Avg Recovery Score", round(filtered_data["Recovery Score"].mean(), 1))
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# CHARTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Recovery Score & Sleep Trend")

    fig_line = px.line(
        filtered_data,
        x="Date",
        y=["Recovery Score", "Sleep Hours"],
        markers=True
    )

    fig_line = apply_plotly_theme(fig_line)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


with col2:
    st.subheader("Recovery Score vs Steps")

    fig_scatter = px.scatter(
        filtered_data,
        x="Steps",
        y="Recovery Score",
        size="Sleep Hours",
        color="Recovery Score"
    )

    fig_scatter = apply_plotly_theme(fig_scatter)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)