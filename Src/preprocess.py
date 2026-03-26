from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from .config import INTERPOLATION_METHOD


def clean_and_convert_date(df: pd.DataFrame, column_name: str = "Date") -> pd.DataFrame:
    df = df.copy()
    df[column_name] = pd.to_datetime(df[column_name], errors="coerce")
    df = df.dropna(subset=[column_name]).sort_values(column_name).reset_index(drop=True)
    return df


def aggregate_duplicate_dates(df: pd.DataFrame, value_columns: Iterable[str], date_column: str = "Date") -> pd.DataFrame:
    keep_cols = [date_column, *value_columns]
    grouped = df[keep_cols].groupby(date_column, as_index=False).mean(numeric_only=True)
    return grouped


def align_on_common_dates(*dfs: pd.DataFrame, date_column: str = "Date") -> list[pd.DataFrame]:
    if not dfs:
        return []
    common_dates = set(pd.to_datetime(dfs[0][date_column]))
    for df in dfs[1:]:
        common_dates &= set(pd.to_datetime(df[date_column]))
    common_dates = sorted(common_dates)
    aligned = []
    for df in dfs:
        out = df[df[date_column].isin(common_dates)].copy()
        out = out.sort_values(date_column).reset_index(drop=True)
        aligned.append(out)
    return aligned


def reindex_and_interpolate(df: pd.DataFrame, date_column: str = "Date", freq: str = "D") -> pd.DataFrame:
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.sort_values(date_column).set_index(date_column)
    new_index = pd.date_range(df.index.min(), df.index.max(), freq=freq)
    df = df.reindex(new_index)
    df = df.interpolate(method=INTERPOLATION_METHOD)
    df.index.name = date_column
    return df.reset_index()


def merge_by_date(left: pd.DataFrame, right: pd.DataFrame, date_column: str = "Date", how: str = "inner") -> pd.DataFrame:
    return pd.merge(left, right, on=date_column, how=how)


def merge_multiple_by_date(dfs: list[pd.DataFrame], date_column: str = "Date", how: str = "inner") -> pd.DataFrame:
    if not dfs:
        return pd.DataFrame()
    merged = dfs[0].copy()
    for df in dfs[1:]:
        merged = pd.merge(merged, df, on=date_column, how=how)
    return merged


def merge_in_chunks(left_path: str | Path, right_path: str | Path, output_path: str | Path, on: list[str], chunksize: int = 50_000) -> Path:
    left_path = Path(left_path)
    right_path = Path(right_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    right_df = pd.read_csv(right_path)
    first = True
    for chunk in pd.read_csv(left_path, chunksize=chunksize):
        merged = chunk.merge(right_df, on=on, how="left")
        merged.to_csv(output_path, mode="w" if first else "a", header=first, index=False)
        first = False
    return output_path
