from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


def require_file(path: str | Path) -> Path:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path


def require_columns(df: pd.DataFrame, required: Iterable[str]) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def require_min_rows(df: pd.DataFrame, min_rows: int, label: str = "dataframe") -> None:
    if len(df) < min_rows:
        raise ValueError(f"{label} contains only {len(df)} rows, but at least {min_rows} are required.")
