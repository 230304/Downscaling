import os
import pandas as pd
import calendar

# Configuration dictionary for user-specific paths
config = {
    "input_csv_path": "path/to/dataframe_for_rf_for_dwnscl.csv",
    "output_csv_path": "path/to/output/processed_dataframe.csv",
    "time_column_name": "time"  # Column containing time in the format 'YYYY-MM'
}

# Extract configuration parameters
input_csv_path = config["input_csv_path"]
output_csv_path = config["output_csv_path"]
time_column_name = config["time_column_name"]

# Load the CSV file
df = pd.read_csv(input_csv_path)

# Drop unnecessary columns (adjust the column name if required)
df = df.drop(columns=["index"], errors="ignore")  # Errors='ignore' prevents issues if the column doesn't exist
print("Dataframe loaded and processed. Preview:")
print(df.head())

# Function to get the number of days in a given month
def get_days_in_month(date_str):
    """
    Get the number of days in the month for a given date in 'YYYY-MM' format.

    Args:
        date_str (str): Date in 'YYYY-MM' format.

    Returns:
        int: Number of days in the specified month.
    """
    year, month = map(int, date_str.split('-'))
    return calendar.monthrange(year, month)[1]

# Convert instantaneous values to monthly accumulations
# Constants:
# - 10800 seconds (3 hours)
# - 8 cycles per day
df["Evap_abs"] = df["Evapotranspiration"] * 10800 * 8 * df[time_column_name].apply(get_days_in_month)
df["Rainf_abs"] = df["Rain"] * 10800 * 8 * df[time_column_name].apply(get_days_in_month)
df["SR_abs"] = df["SurfaceRunoff"] * 8 * df[time_column_name].apply(get_days_in_month)

# Save the processed DataFrame to a new CSV file
df.to_csv(output_csv_path, index=False)
print(f"Processed data saved to {output_csv_path}")
