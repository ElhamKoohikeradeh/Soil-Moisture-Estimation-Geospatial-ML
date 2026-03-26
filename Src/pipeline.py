from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from .config import (
    DATE_COLUMN_CANDIDATES,
    NDVI_COLUMN_CANDIDATES,
    OUTPUTS_DIR,
    SOIL_MOISTURE_COLUMN_CANDIDATES,
    VV_COLUMN_CANDIDATES,
)
from .loaders import load_registry, standardize_common_columns
from .models import calibrate_linear_model, predict_soil_moisture, regression_metrics
from .plot import plot_combined_parcel_timeseries, plot_scatter_with_fit
from .preprocess import aggregate_duplicate_dates, align_on_common_dates, clean_and_convert_date, merge_multiple_by_date


def run_pipeline(registry: Dict[str, Dict[str, str | Path]]) -> dict:
    loaded = load_registry(registry)
    results = {}

    for parcel, files in loaded.items():
        sar = standardize_common_columns(files["sar"], date_candidates=DATE_COLUMN_CANDIDATES, vv_candidates=VV_COLUMN_CANDIDATES)
        ndvi = standardize_common_columns(files["ndvi"], date_candidates=DATE_COLUMN_CANDIDATES, ndvi_candidates=NDVI_COLUMN_CANDIDATES)
        sm = standardize_common_columns(files["soil_moisture"], date_candidates=DATE_COLUMN_CANDIDATES, sm_candidates=SOIL_MOISTURE_COLUMN_CANDIDATES)

        sar = clean_and_convert_date(sar, "Date")
        ndvi = clean_and_convert_date(ndvi, "Date")
        sm = clean_and_convert_date(sm, "Date")

        sar = aggregate_duplicate_dates(sar, ["VV"], "Date")
        ndvi = aggregate_duplicate_dates(ndvi, ["NDVI"], "Date")
        sm = aggregate_duplicate_dates(sm, ["Soil_Moisture"], "Date")

        sar, ndvi, sm = align_on_common_dates(sar, ndvi, sm, date_column="Date")
        merged = merge_multiple_by_date([sar, ndvi, sm], date_column="Date", how="inner")

        calibration = calibrate_linear_model(merged)
        merged["Predicted_Soil_Moisture"] = predict_soil_moisture(merged, calibration)
        metrics = regression_metrics(merged["Soil_Moisture"], merged["Predicted_Soil_Moisture"])

        parcel_dir = OUTPUTS_DIR / parcel
        parcel_dir.mkdir(parents=True, exist_ok=True)
        merged.to_csv(parcel_dir / f"{parcel}_model_ready.csv", index=False)
        plot_combined_parcel_timeseries(
            merged[["Date", "VV", "NDVI", "Soil_Moisture", "Predicted_Soil_Moisture"]],
            parcel_name=parcel,
            output_path=parcel_dir / f"{parcel}_timeseries.png",
        )
        plot_scatter_with_fit(
            merged,
            x_col="Soil_Moisture",
            y_col="Predicted_Soil_Moisture",
            title=f"{parcel} - Observed vs Predicted Soil Moisture",
            output_path=parcel_dir / f"{parcel}_observed_vs_predicted.png",
        )

        results[parcel] = {"calibration": calibration, "metrics": metrics, "output_dir": parcel_dir}

    return results
