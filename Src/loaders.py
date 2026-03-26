from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from .config import RAW_DIR
from .utils import find_first_existing_column
from .validate import require_file


def load_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    path = require_file(path)
    return pd.read_csv(path, **kwargs)


def load_parcel_file(parcel: str, path: str | Path) -> pd.DataFrame:
    df = load_csv(path)
    df["parcel"] = parcel
    return df


def load_registry(registry: Dict[str, Dict[str, str | Path]]) -> Dict[str, Dict[str, pd.DataFrame]]:
    loaded: Dict[str, Dict[str, pd.DataFrame]] = {}
    for parcel, parcel_files in registry.items():
        loaded[parcel] = {}
        for key, path in parcel_files.items():
            loaded[parcel][key] = load_parcel_file(parcel=parcel, path=path)
    return loaded


def calculate_ndvi(df: pd.DataFrame, nir_col: str = "B8", red_col: str = "B4") -> pd.Series:
    return (df[nir_col] - df[red_col]) / (df[nir_col] + df[red_col])


def export_pixel_values(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def standardize_common_columns(df: pd.DataFrame, *, date_candidates, vv_candidates=None, vh_candidates=None, ndvi_candidates=None, sm_candidates=None) -> pd.DataFrame:
    df = df.copy()
    rename_map = {}
    rename_map[find_first_existing_column(df.columns, date_candidates)] = "Date"
    if vv_candidates:
        rename_map[find_first_existing_column(df.columns, vv_candidates)] = "VV"
    if vh_candidates:
        rename_map[find_first_existing_column(df.columns, vh_candidates)] = "VH"
    if ndvi_candidates:
        rename_map[find_first_existing_column(df.columns, ndvi_candidates)] = "NDVI"
    if sm_candidates:
        rename_map[find_first_existing_column(df.columns, sm_candidates)] = "Soil_Moisture"
    return df.rename(columns=rename_map)
