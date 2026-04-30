import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

from components.theme_switcher import apply_theme
apply_theme()


# -----------------------------
# CALL FUNCTION (IMPORTANT)
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

    # softer grid (important for light mode)
    fig.update_xaxes(gridcolor="#E5E1DA")
    fig.update_yaxes(gridcolor="#E5E1DA")

    return fig
# -----------------------------
# HELPER: LOAD DATA
# -----------------------------
def load_data():
    try:
        df = pd.read_csv("data/health_data.csv")
        return df
    except:
        return None

# -----------------------------
# HELPER: GENERATE DAILY ACTIVITY
# -----------------------------
def generate_activity_data(df):
    # If dataset has date column → use it
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        daily_counts = df.groupby(df["date"].dt.date).size()
    else:
        # fallback: simulate activity
        today = datetime.today()
        dates = [today - timedelta(days=i) for i in range(120)]
        counts = np.random.randint(0, 5, size=len(dates))
        daily_counts = pd.Series(counts, index=[d.date() for d in dates])

    return daily_counts

# -----------------------------
# HELPER: HEATMAP GRID
# -----------------------------
def build_heatmap(daily_counts, days=120):
    today = datetime.today()

    date_range = [today - timedelta(days=i) for i in range(days)]
    date_range.reverse()

    values = [daily_counts.get(d.date(), 0) for d in date_range]

    # reshape into grid (like GitHub)
    cols = 12
    rows = int(len(values) / cols)

    grid = np.array(values[:rows * cols]).reshape(rows, cols)
    return grid

# -----------------------------
# HELPER: STREAK
# -----------------------------
def calculate_streak(daily_counts):
    dates = sorted(daily_counts.index)

    streak = 0
    max_streak = 0
    prev = None

    for d in dates:
        if prev is None or (d - prev).days == 1:
            streak += 1
        else:
            streak = 1

        max_streak = max(max_streak, streak)
        prev = d

    return max_streak

# -----------------------------
# MAIN PROFILE PAGE
# -----------------------------
def profile_page():
    st.title("👤 Profile")
    st.subheader("📊 Activity Overview")

    df = load_data()

    # -----------------------------
    # IF NO DATA → STILL SHOW UI
    # -----------------------------
    if df is None or df.empty:
        st.warning("No health data found. Showing demo activity.")

        # generate fake data so UI is never blank
        today = datetime.today()
        dates = [today - timedelta(days=i) for i in range(120)]
        counts = np.random.randint(0, 5, size=len(dates))
        daily_counts = pd.Series(counts, index=[d.date() for d in dates])
    else:
        daily_counts = generate_activity_data(df)

    # -----------------------------
    # HEATMAP
    # -----------------------------
    st.subheader("🔥 Activity Heatmap")

    heatmap = build_heatmap(daily_counts)

    # color intensity
    styled = pd.DataFrame(heatmap).style.background_gradient(cmap="Greens")

    st.dataframe(styled, use_container_width=True)

    # -----------------------------
    # METRICS
    # -----------------------------
    total_days = len(daily_counts[daily_counts > 0])
    total_actions = int(daily_counts.sum())
    max_streak = calculate_streak(daily_counts)

    col1, col2, col3 = st.columns(3)

    col1.metric("Active Days", total_days)
    col2.metric("Total Activity", total_actions)
    col3.metric("Max Streak", max_streak)

    # -----------------------------
    # WEEKLY TREND
    # -----------------------------
    st.subheader("📈 Weekly Activity")

    weekly = pd.Series(daily_counts)
    weekly.index = pd.to_datetime(weekly.index)
    weekly = weekly.resample("W").sum()

    import plotly.express as px

    fig_weekly = px.line(
        x=weekly.index,
        y=weekly.values,
        labels={"x": "Date", "y": "Activity"},
        markers=True
    )

    fig_weekly = apply_plotly_theme(fig_weekly)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(fig_weekly, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # RECENT ACTIVITY
    # -----------------------------
    st.subheader("🕒 Recent Activity")

    recent = pd.DataFrame({
        "date": list(daily_counts.index),
        "activity_count": list(daily_counts.values)
    }).sort_values(by="date", ascending=False).head(10)

    st.dataframe(recent, use_container_width=True)

    # -----------------------------
    # INSIGHT SUMMARY
    # -----------------------------
    st.subheader("💡 Insights")

    if total_days > 0:
        st.success(f"You were active on {total_days} days. Keep it consistent!")
    else:
        st.info("Start tracking your activity to build streaks.")

profile_page()