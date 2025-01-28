import pandas as pd

# Configuration dictionary for paths and parameters
config = {
    "input_csv_path": "path/to/full_dataframe.csv",  # Path to the original DataFrame
    "baseline_csv_path": "path/to/mean_baseline_2004_2009.csv",  # Path to the baseline mean values
    "output_csv_path": "path/to/anomaly_dataframe.csv",  # Path to save the anomaly DataFrame
    "time_column_name": "time",  # Time column in 'YYYY-MM' format
    "lat_column_name": "lat",  # Latitude column
    "lon_column_name": "lon",  # Longitude column
    "columns_to_analyze": [  # Columns for which anomalies will be calculated
        "RootZoneSoilMoisture",
        "PlantCanopy",
        "Evap_abs",
        "Rainf_abs",
        "SR_abs",
    ],
}

# Extract configuration parameters
input_csv_path = config["input_csv_path"]
baseline_csv_path = config["baseline_csv_path"]
output_csv_path = config["output_csv_path"]
time_column_name = config["time_column_name"]
lat_column_name = config["lat_column_name"]
lon_column_name = config["lon_column_name"]
columns_to_analyze = config["columns_to_analyze"]

# Load the original DataFrame and the baseline mean values
df_original = pd.read_csv(input_csv_path)
mean_baseline = pd.read_csv(baseline_csv_path)

# Convert the 'time' column to datetime format if it's not already
df_original[time_column_name] = pd.to_datetime(df_original[time_column_name], format="%Y-%m")
print(f"Original DataFrame loaded with {len(df_original)} rows.")
print(f"Baseline mean DataFrame loaded with {len(mean_baseline)} rows.")

# Merge the original DataFrame with the baseline mean values on 'lat' and 'lon'
df_with_baseline = pd.merge(
    df_original,
    mean_baseline,
    on=[lat_column_name, lon_column_name],
    suffixes=("", "_baseline")
)
print(f"Merged DataFrame created with {len(df_with_baseline)} rows.")

# Calculate anomalies by subtracting baseline mean values from original values
for column in columns_to_analyze:
    baseline_column = f"{column}_baseline"
    anomaly_column = f"{column}_anomaly"
    df_with_baseline[anomaly_column] = df_with_baseline[column] - df_with_baseline[baseline_column]
    print(f"Anomaly column '{anomaly_column}' calculated.")

# Select columns for the final anomaly DataFrame
anomaly_columns = [f"{col}_anomaly" for col in columns_to_analyze]
output_columns = [lat_column_name, lon_column_name, time_column_name] + anomaly_columns
df_anomalies = df_with_baseline[output_columns]

# Save the resulting anomaly DataFrame to a CSV file
df_anomalies.to_csv(output_csv_path, index=False)
print(f"Anomaly DataFrame saved to {output_csv_path}. Preview:")
print(df_anomalies.head())
