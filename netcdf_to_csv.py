import os
import numpy as np
import pandas as pd
import xarray as xr

# Configuration dictionary for user-specific paths and settings
config = {
    "TWSA_file_path": "path/to/CSR_GRACE_GRACE-FO_TWSA.nc",
    "GLDAS_folder_path": "path/to/GLDAS_NOAH_0.25_folder",
    "output_file_path": "path/to/output/combined_data.csv",
    "start_year": 2002,
    "end_year": 2023
}

# Extract configuration parameters
TWSA_file_path = config["TWSA_file_path"]
GLDAS_folder_path = config["GLDAS_folder_path"]
output_file_path = config["output_file_path"]
years = range(config["start_year"], config["end_year"] + 1)
months = range(1, 13)

# Initialize an empty DataFrame to store the combined data
empty_df = pd.DataFrame()

# Process each year and month
for year in years:
    for month in months:
        try:
            # Construct the file path for the GLDAS file
            GLDAS_file_path = os.path.join(
                GLDAS_folder_path, 
                f"GLDAS_NOAH025_M.A{year}{month:02d}.021.nc4"
            )
            
            # Load GLDAS data
            ds = xr.open_dataset(GLDAS_file_path)
            
            # Extract latitude, longitude, and variables of interest
            lat = ds['lat'].values
            lon = ds['lon'].values
            Evap = ds['Evap_tavg'].values   
            Sur_rnof = ds['Qs_acc'].values
            Soil_0to10 = ds['SoilMoi0_10cm_inst'].values
            Soil_10to40 = ds['SoilMoi10_40cm_inst'].values
            Soil_40to100 = ds['SoilMoi40_100cm_inst'].values
            Soil_100to200 = ds['SoilMoi100_200cm_inst'].values
            Soil_mois = Soil_0to10 + Soil_10to40 + Soil_40to100 + Soil_100to200
            Soil_mois2 = (10 * Soil_0to10 + 30 * Soil_10to40 + 60 * Soil_40to100 + 100 * Soil_100to200) / 200
            RootMoist = ds['RootMoist_inst'].values
            Canop = ds['CanopInt_inst'].values
            Rain = ds['Rainf_f_tavg'].values

            # Create the meshgrid (for reference)
            lon_grid, lat_grid = np.meshgrid(lon, lat)

            # Flatten the meshgrid and variables' arrays
            lat_flat = lat_grid.flatten()
            lon_flat = lon_grid.flatten() + 180

            Evap_flat = Evap.squeeze().flatten()
            Sur_rnof_flat = Sur_rnof.squeeze().flatten()
            RootMoist_flat = RootMoist.squeeze().flatten()
            Canop_flat = Canop.squeeze().flatten()
            Rain_flat = Rain.squeeze().flatten()

            # Create GLDAS DataFrame
            GLDAS_df = pd.DataFrame({
                'lat': lat_flat,
                'lon': lon_flat,
                'Evapotranspiration': Evap_flat,
                'SurfaceRunoff': Sur_rnof_flat,
                'RootZoneSoilMoisture': RootMoist_flat,
                'PlantCanopy': Canop_flat,
                'Rain': Rain_flat
            })

            # Load CSR GRACE TWSA data
            ds = xr.open_dataset(TWSA_file_path)

            # Convert time to standard format
            original_time_values = ds['time'].values
            reference_date = np.datetime64('2002-01-01')
            converted_time_values = pd.to_datetime(reference_date) + pd.to_timedelta(original_time_values, unit='D')
            time_df = pd.DataFrame({
                'Original Time Values': original_time_values,
                'Converted Time': converted_time_values
            })
            time_df['Time (Monthly)'] = time_df['Converted Time'].dt.to_period('M')
            ds = ds.assign_coords(time=pd.to_datetime(time_df['Time (Monthly)'].astype(str)))

            # Select TWSA data for the current year and month
            d1 = ds.sel(time=f'{year}-{month:02d}')
            lwe_d1 = d1['lwe_thickness']
            LWE_df = lwe_d1.to_dataframe().reset_index()

            # Filter LWE DataFrame for matching size with GLDAS data
            LWE_df_filtered = LWE_df[(LWE_df['lat'] >= -59.875) & (LWE_df['lat'] <= 89.875)]

            # Combine GLDAS and CSR TWSA data
            combined_df = pd.merge(GLDAS_df, LWE_df_filtered, on=['lat', 'lon'], how='outer')

            # Drop rows with NaN values in specific columns
            combined_df_cleaned = combined_df.dropna(subset=[
                'Evapotranspiration', 'SurfaceRunoff', 'RootZoneSoilMoisture', 'PlantCanopy', 'Rain'
            ])

            # Standardize time format
            combined_df_cleaned['time'] = pd.to_datetime(combined_df_cleaned['time']).dt.to_period('M').astype(str)

            # Append the cleaned DataFrame to the master DataFrame
            empty_df = pd.concat([empty_df, combined_df_cleaned], ignore_index=True)
        
        except Exception as e:
            print(f"{year}_{month:02d}: Missing month or other issue - {str(e)}")

# Save the combined DataFrame to a CSV file
empty_df.to_csv(output_file_path, index=False)
print(f"Combined data saved to {output_file_path}")
