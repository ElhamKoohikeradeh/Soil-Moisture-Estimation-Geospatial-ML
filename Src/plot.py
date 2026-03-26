from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .config import DEFAULT_OUTPUT_DPI


def find_column(columns, target: str) -> str:
    lowered = {c.lower(): c for c in columns}
    key = target.lower()
    if key not in lowered:
        raise KeyError(f"Column '{target}' was not found.")
    return lowered[key]


def merge_plot_inputs(vsm_df: pd.DataFrame, wcm_df: pd.DataFrame, dubois_df: pd.DataFrame, date_column: str = "Date") -> pd.DataFrame:
    merged = vsm_df.merge(wcm_df, on=date_column, how="inner")
    merged = merged.merge(dubois_df, on=date_column, how="inner")
    return merged


def plot_combined_parcel_timeseries(df: pd.DataFrame, parcel_name: str, output_path: str | Path, date_col: str = "Date") -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    for col in [c for c in df.columns if c != date_col]:
        plt.plot(df[date_col], df[col], label=col)
    plt.title(f"{parcel_name} - Combined Time Series")
    plt.xlabel(date_col)
    plt.ylabel("Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=DEFAULT_OUTPUT_DPI)
    plt.close()
    return output_path


def plot_scatter_with_fit(df: pd.DataFrame, x_col: str, y_col: str, title: str, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    x = df[x_col]
    y = df[y_col]
    m, b = pd.Series(y).corr(pd.Series(x)), 0  # simple placeholder correlation-based annotation

    plt.figure(figsize=(7, 6))
    plt.scatter(x, y)
    if len(df) >= 2:
        fit = pd.Series(y).rolling(window=min(5, len(df)), min_periods=1).mean()
        plt.plot(x, fit)
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.tight_layout()
    plt.savefig(output_path, dpi=DEFAULT_OUTPUT_DPI)
    plt.close()
    return output_path
