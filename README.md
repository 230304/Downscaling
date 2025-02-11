# Downscaling GRACE (Work under progress)

## Overview
This repository contains code and workflows for **downscaling GRACE satellite data** to achieve finer spatial resolution. The goal is to improve the applicability of GRACE-derived Total Water Storage Anomalies (TWSA) data for regional and local-scale hydrological studies.

## Key Achievements
- **Processed GRACE & FLDAS Data**: Extracted and converted raw NetCDF data into a structured format for analysis.
- **Monthly Data Aggregation**: Converted instantaneous FLDAS data to monthly accumulations.
- **Region-Specific Masking**: Filtered data to focus on the region of interest.
- **Baseline Calculation & Anomaly Extraction**: Computed long-term mean baselines and calculated anomalies.

## How to Use This Repository
The repository provides a structured workflow for downscaling GRACE data by integrating FLDAS variables. The scripts perform the following tasks:

### 1. Data Extraction & Conversion
#### `netcdf_to_csv.py`
- Extracts data from NetCDF files and converts them into a structured CSV format.
- Facilitates easier data handling and processing.
- **Output:** CSV file containing extracted variables.

### 2. Temporal Aggregation
#### `convert_inst_to_monthly_acc.py`
- Converts instantaneous FLDAS variables to **monthly accumulated values**.
- Essential for aligning the dataset with GRACE's monthly resolution.

### 3. Spatial Filtering
#### `masking_dataframe_using_coordinates.py`
- Filters and extracts data for a specific region using predefined latitude-longitude boundaries.
- Reduces dataset size and focuses on the study area.

### 4. Baseline Computation
#### `calculating_mean_baseline.py`
- Computes the **mean baseline** for key variables over a reference period.
- Used to normalize data and detect deviations from historical averages.

### 5. Anomaly Calculation
#### `calculate_anomaly.py`
- Computes anomalies by subtracting the baseline mean from the absolute values.
- Helps in detecting hydrological variations.

## Requirements
Ensure you have the following dependencies installed before running the scripts:
```bash
pip install numpy pandas xarray netCDF4 geopandas rasterio
```

## Running the Scripts
1. **Extract and Convert Data**
   - Convert NetCDF to CSV: `netcdf_to_csv.py`
   - Aggregate Monthly Data: `convert_inst_to_monthly_acc.py`
2. **Filter Region of Interest**
   - Apply spatial masking: `masking_dataframe_using_coordinates.py`
3. **Compute Anomalies**
   - Calculate long-term baseline: `calculating_mean_baseline.py`
   - Extract anomalies: `calculate_anomaly.py`

## Future Work
- **Enhancing Downscaling Techniques**: Exploring ML-based approaches for finer resolution.
- **Validation with Groundwater Observations**: Comparing downscaled GRACE estimates with observed GWL data.
- **Application to Other Regions**: Extending the methodology to other hydrologically significant areas.

For any questions or contributions, feel free to reach out!

