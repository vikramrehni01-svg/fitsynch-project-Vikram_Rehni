import pandas as pd
from datetime import datetime

# Function to load and clean the data
def load_data():
    # Read the CSV file into a DataFrame
    file_path = 'data/health_data.csv'
    data = pd.read_csv(file_path)

    # Fill missing 'Steps' values with the median of the 'Steps' column
    if 'Steps' in data.columns:
        data['Steps'].fillna(data['Steps'].median(), inplace=True)

    # Fill missing 'Sleep_Hours' with 7.0
    if 'Sleep_Hours' in data.columns:
        data['Sleep_Hours'].fillna(7.0, inplace=True)

    # Fill missing 'Heart_Rate_bpm' with 68
    if 'Heart_Rate_bpm' in data.columns:
        data['Heart_Rate_bpm'].fillna(68, inplace=True)

    # Fill other columns with their respective median values
    for column in data.columns:
        if data[column].isnull().any() and column not in ['Steps', 'Sleep_Hours', 'Heart_Rate_bpm']:
            data[column].fillna(data[column].median(), inplace=True)

    # Convert the 'Date' column to datetime objects
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Return the cleaned DataFrame
    return data

# Function to calculate the recovery score
def calculate_recovery_score(df):
    # Initialize the recovery score list
    recovery_scores = []

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        recovery_score = 50  # Start with a neutral base score of 50

        # Adjust score based on Sleep_Hours
        sleep_hours = row['Sleep_Hours']
        if sleep_hours >= 7:
            recovery_score += 20  # Good sleep
        elif sleep_hours < 6:
            recovery_score -= 20  # Poor sleep

        # Adjust score based on Heart_Rate_bpm
        heart_rate = row['Heart_Rate_bpm']
        if heart_rate < 60:
            recovery_score += 20  # Excellent heart rate
        elif heart_rate >= 80:
            recovery_score -= 10  # High heart rate

        # Adjust score based on Steps
        steps = row['Steps']
        if steps < 8000:
            recovery_score += 10  # Moderate activity
        elif steps > 12000:
            recovery_score -= 10  # Possible strain from high activity

        # Ensure the score is within the 0 to 100 range
        recovery_score = max(0, min(100, recovery_score))

        # Append the score to the list
        recovery_scores.append(recovery_score)

    # Add the new 'Recovery_Score' column to the DataFrame
    df['Recovery_Score'] = recovery_scores

    # Return the modified DataFrame
    return df

