import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Parameters
num_days = 365
start_date = datetime(2025, 1, 1)

# Create date range
end_date = start_date + timedelta(days=num_days-1)
dates = pd.date_range(start_date, end_date)

# Generate synthetic data
np.random.seed(42)  # for reproducibility

steps = np.random.normal(loc=8500, scale=2000, size=num_days).clip(3000, 18000)
sleep_hours = np.random.normal(loc=7.2, scale=1, size=num_days).clip(4.5, 9.5)
heart_rate = np.random.normal(loc=68, scale=10, size=num_days).clip(48, 110)
calories_burned = np.random.randint(1800, 4200, size=num_days)
active_minutes = np.random.randint(20, 180, size=num_days)

# Create a DataFrame
health_data = pd.DataFrame({
    'Date': dates,
    'Steps': steps,
    'Sleep_Hours': sleep_hours,
    'Heart_Rate_bpm': heart_rate,
    'Calories_Burned': calories_burned,
    'Active_Minutes': active_minutes
})

# Introduce missing values (5% of the data)
for column in health_data.columns[1:]:  # skip 'Date' column
    health_data.loc[health_data.sample(frac=0.05).index, column] = np.nan

# Save to CSV
health_data.to_csv('data/health_data.csv', index=False)

print("Generated health data with 365 days and saved to data/health_data.csv")
