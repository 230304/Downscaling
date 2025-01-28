import pandas as pd

# Configuration dictionary for paths and parameters
config = {
    "anomaly_data_path": "path/to/anomaly_dataframe.csv",  # Path to the anomaly DataFrame
    "rajasthan_coords_path": "path/to/latlon_rajasthan.csv",  # Path to the Rajasthan lat/lon data
    "output_rajasthan_data_path": "path/to/rajasthan_anomalies.csv",  # Path to save Rajasthan-specific anomaly data
    "lat_column_name": "lat",  # Latitude column name
    "lon_column_name": "lon",  # Longitude column name
}

# Extract configuration parameters
anomaly_data_path = config["anomaly_data_path"]
rajasthan_coords_path = config["rajasthan_coords_path"]
output_rajasthan_data_path = config["output_rajasthan_data_path"]
lat_column_name = config["lat_column_name"]
lon_column_name = config["lon_column_name"]

# Load the anomaly data and Rajasthan lat/lon coordinates
df_anomalies = pd.read_csv(anomaly_data_path)
df_rajasthan_coords = pd.read_csv(rajasthan_coords_path)

print(f"Anomaly DataFrame loaded with {len(df_anomalies)} rows.")
print(f"Rajasthan coordinates DataFrame loaded with {len(df_rajasthan_coords)} rows.")

# Merge the anomaly data with Rajasthan coordinates using latitude and longitude
raj_anomalies_data = pd.merge(
    df_anomalies,
    df_rajasthan_coords,
    on=[lat_column_name, lon_column_name],
    how="inner"
)
print(f"Merged Rajasthan-specific anomaly DataFrame created with {len(raj_anomalies_data)} rows.")

# Save the Rajasthan-specific anomaly data to a CSV file
raj_anomalies_data.to_csv(output_rajasthan_data_path, index=False)
print(f"Rajasthan-specific anomaly DataFrame saved to {output_rajasthan_data_path}. Preview:")
print(raj_anomalies_data.head())
