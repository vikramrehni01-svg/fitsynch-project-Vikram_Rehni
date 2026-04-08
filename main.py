import streamlit as st
from modules.processor import process_data
import pandas as pd

# Set the Streamlit page configuration
st.set_page_config(layout="wide", page_title="FitSynch")

# Title for the dashboard
st.title("FitSynch - Personal Health Analytics")

# Load and process the data
# This will retrieve the final processed DataFrame
processed_data = process_data()

# Add a sidebar for time filtering
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

# Filter data based on the selected time range
def filter_data_by_time(data, time_range):
    if 'Date' in data.columns:
        max_date = data['Date'].max()
        if time_range == "Last 7 Days":
            min_date = max_date - pd.Timedelta(days=7)
            return data[data['Date'] >= min_date]
        elif time_range == "Last 30 Days":
            min_date = max_date - pd.Timedelta(days=30)
            return data[data['Date'] >= min_date]
    return data  # For "All Time"

# Filter the data based on the sidebar selection
filtered_data = filter_data_by_time(processed_data, time_range)

# Calculate and display metrics from the filtered data
def display_metrics(data):
    avg_steps = data['Steps'].mean()
    avg_sleep = data['Sleep_Hours'].mean()
    avg_recovery = data['Recovery_Score'].mean()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Average Steps", value=f"{avg_steps:.0f}", delta=None)
    with col2:
        st.metric(label="Average Sleep Hours", value=f"{avg_sleep:.1f}", delta=None)
    with col3:
        st.metric(label="Average Recovery Score", value=f"{avg_recovery:.1f}", delta=None)

# Display the metrics from the FILTERED data
st.write("### Key Metrics")
display_metrics(filtered_data)

# Display the data in a table format
st.write("### Processed Health Data")
st.dataframe(processed_data)

# Additional features or sections can be added below to enhance the dashboard
# For example, visualizations, user inputs, analytics summaries, etc.

