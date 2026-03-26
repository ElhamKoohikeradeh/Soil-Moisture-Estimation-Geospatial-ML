🌍 Project Overview

This project represents a comprehensive workflow for soil moisture estimation and environmental modeling using multi-source remote sensing data and machine learning techniques. The objective was to bridge the gap between satellite observations, ground measurements, and predictive modeling, building a fully reproducible pipeline from raw data extraction to final model evaluation.

Rather than treating each step independently, the project was designed as a continuous analytical story — where each stage feeds into the next, forming a coherent system for geospatial analysis.

📡 Data Integration and Preprocessing

The workflow begins with the integration of heterogeneous datasets, including:

Sentinel-1 SAR data
Sentinel-2 optical imagery
Precipitation data
Ground-based soil moisture measurements

For each parcel and time period, data were systematically filtered, extracted, and aligned. Pixel-level values were retrieved and exported into structured CSV datasets, ensuring consistency across spatial and temporal dimensions.

To improve data reliability, variance-based weighting techniques were implemented. By calculating inverse variance weights across multiple measurements, a row-wise weighted mean soil moisture was derived, providing a more robust representation of field conditions.

🌱 Physical Modeling of Soil Moisture

The project integrates several well-established physical and semi-empirical models to estimate soil moisture:

Topp’s Equation for dielectric constant estimation
Dubois Model for SAR backscatter interpretation
Water Cloud Model (WCM) for vegetation effects
SV-SIM Model for vegetation–soil interaction

Surface roughness and dielectric properties were computed to enhance the physical interpretation of radar signals. These models were applied iteratively across parcels and time periods, enabling spatially distributed soil moisture estimation.

🛰️ Feature Extraction and Pixel-Level Analysis

A key component of the workflow involved extracting pixel-level information from satellite imagery:

SAR backscatter values (VV, angle)
NDVI from Sentinel-2
Precipitation data

Custom functions were developed to:

Extract pixel values
Export structured datasets
Process data per parcel and year
Avoid system overload through controlled iteration

This step transformed raw satellite imagery into machine learning–ready datasets.

📊 Vegetation Indices and Biophysical Parameters

Vegetation dynamics were incorporated using NDVI-derived metrics. NDVI values were used not only as features but also to estimate:

Leaf Area Index (LAI)
Vegetation Water Content (VWC)

These variables were essential inputs for models such as WCM, allowing the separation of vegetation and soil contributions in radar signals.

🤖 Machine Learning and Model Calibration

Beyond physical models, the project integrates advanced machine learning techniques for calibration and prediction:

XGBoost
Random Forest
CatBoost
LightGBM

These models were used to:

Estimate soil moisture
Fill missing values
Extract feature importance (interpreted as coefficients)
Improve predictive performance

Special attention was given to:

Handling missing values
Data normalization
Temporal alignment
Training-validation splitting

Model calibration was performed using optimization techniques and curve fitting to ensure consistency between predicted and observed values.

🔄 Data Alignment and Time-Series Consistency

One of the major challenges addressed in this project was temporal misalignment between datasets.

To resolve this:

Date columns were standardized
Datasets were merged or aligned based on time
Interpolation techniques were applied when necessary
Independent time-step analysis was implemented for robustness

This ensured that all models operated on consistent and comparable datasets.

📈 Model Evaluation and Comparison

To evaluate performance, multiple models were compared across parcels and time periods. The workflow includes:

Training/testing splits per parcel-year
Error metric computation
Model comparison tables
Prediction exports

This enabled a systematic assessment of model reliability and generalization.

🗺️ Output Generation

Final outputs include:

Geo-referenced TIFF files
Pixel-level CSV datasets
Predicted soil moisture maps
Model coefficients and evaluation metrics

All outputs are structured for further analysis, visualization, or integration into GIS platforms.

🧠 Key Contributions

This project demonstrates:

Integration of physics-based and data-driven models
A scalable workflow for multi-source geospatial data processing
Robust handling of temporal and spatial inconsistencies
End-to-end pipeline from raw satellite data to predictive modeling
🚀 Future Work

Potential extensions of this work include:

Deep learning integration (e.g., LSTM, CNN)
Real-time soil moisture monitoring systems
Cloud-based scalable processing (e.g., Google Earth Engine pipelines)
Deployment as an operational decision-support tool for precision agriculture