import pandas as pd

# Configuration dictionary for user-specific paths and parameters
config = {
    "input_csv_path": "path/to/processed_dataframe.csv",
    "output_csv_path": "path/to/mean_baseline_2004_2009.csv",
    "time_column_name": "time",  # Column containing time in 'YYYY-MM' format
    "lat_column_name": "lat",  # Latitude column
    "lon_column_name": "lon",  # Longitude column
    "columns_to_average": [  # Columns to calculate the mean
        "RootZoneSoilMoisture",
        "PlantCanopy",
        "Evap_abs",
        "Rainf_abs",
        "SR_abs",
    ],
    "start_date": "2004-01-01",  # Start date for filtering
    "end_date": "2010-01-01",  # End date for filtering (exclusive)
}

# Extract configuration parameters
input_csv_path = config["input_csv_path"]
output_csv_path = config["output_csv_path"]
time_column_name = config["time_column_name"]
lat_column_name = config["lat_column_name"]
lon_column_name = config["lon_column_name"]
columns_to_average = config["columns_to_average"]
start_date = config["start_date"]
end_date = config["end_date"]

# Load the processed DataFrame
df = pd.read_csv(input_csv_path)

# Convert the 'time' column to datetime if it's not already in datetime format
df[time_column_name] = pd.to_datetime(df[time_column_name], format="%Y-%m")

# Filter data for the specified period
mask = (df[time_column_name] >= start_date) & (df[time_column_name] < end_date)
df_filtered = df[mask]
print(f"Data filtered for the period {start_date} to {end_date}. Number of rows: {len(df_filtered)}")

# Group by latitude and longitude, then calculate the mean for specified columns
mean_baseline = (
    df_filtered.groupby([lat_column_name, lon_column_name])
    .mean()[columns_to_average]
)

# Reset the index for better readability
mean_baseline = mean_baseline.reset_index()

# Save the mean baseline data to a new CSV file
mean_baseline.to_csv(output_csv_path, index=False)
print(f"Mean baseline data saved to {output_csv_path}")

# Preview the calculated mean baseline
print(mean_baseline.head())
