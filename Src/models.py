from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass
class LinearCalibration:
    A: float
    B: float
    C: float


def calculate_weighted_mean(df: pd.DataFrame, columns: Iterable[str]) -> pd.Series:
    cols = list(columns)
    variances = df[cols].var(axis=0, numeric_only=True)
    inv_var = 1.0 / variances.replace(0, np.nan)
    weights = inv_var / inv_var.sum()
    return df[cols].mul(weights, axis=1).sum(axis=1)


def dielectric_from_sm(sm: float | np.ndarray | pd.Series) -> float | np.ndarray | pd.Series:
    return 3.03 + 9.3 * sm + 146 * (sm ** 2) - 76.7 * (sm ** 3)


def roughness_from_sm(sm: float | np.ndarray | pd.Series) -> float | np.ndarray | pd.Series:
    return 0.5 * sm + 0.1


def dubois_model(sm: float | np.ndarray | pd.Series, angle_degrees: float | np.ndarray | pd.Series) -> float | np.ndarray | pd.Series:
    dielectric = dielectric_from_sm(sm)
    roughness = roughness_from_sm(sm)
    angle_rad = np.deg2rad(angle_degrees)
    return 10 * ((dielectric ** 1.5) * (np.tan(angle_rad) ** 2)) / ((0.056 ** 1.5) * roughness)


def wcm_model(sigma_soil, asm, sigma_veg: float = 0.3, a: float = 0.12):
    return sigma_soil * np.exp(-2 * a * asm) + sigma_veg * (1 - np.exp(-2 * a * asm))


def svsim_model(sigma_soil, asm, sigma_veg: float = 0.3, a: float = 0.12):
    return sigma_veg + sigma_soil * np.exp(-2 * a * asm)


def calibrate_linear_model(df: pd.DataFrame, vv_col: str = "VV", ndvi_col: str = "NDVI", target_col: str = "Soil_Moisture") -> LinearCalibration:
    X = df[[vv_col, ndvi_col]].to_numpy(dtype=float)
    y = df[target_col].to_numpy(dtype=float)
    X_design = np.column_stack([X, np.ones(len(X))])
    coeffs, *_ = np.linalg.lstsq(X_design, y, rcond=None)
    return LinearCalibration(A=float(coeffs[0]), B=float(coeffs[1]), C=float(coeffs[2]))


def predict_soil_moisture(df: pd.DataFrame, calibration: LinearCalibration, vv_col: str = "VV", ndvi_col: str = "NDVI") -> pd.Series:
    return calibration.A * df[vv_col] + calibration.B * df[ndvi_col] + calibration.C


def regression_metrics(y_true, y_pred) -> dict:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    residuals = y_true - y_pred
    mse = float(np.mean(residuals ** 2))
    rmse = float(np.sqrt(mse))
    mae = float(np.mean(np.abs(residuals)))
    ss_res = float(np.sum(residuals ** 2))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    r2 = float(1 - ss_res / ss_tot) if ss_tot != 0 else float("nan")
    return {"MAE": mae, "MSE": mse, "RMSE": rmse, "R2": r2}
