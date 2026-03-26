from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.pipeline import run_pipeline

# Replace these example file paths with your real files.
REGISTRY = {
    "BN": {
        "sar": ROOT / "data" / "raw" / "BN_sar.csv",
        "ndvi": ROOT / "data" / "raw" / "BN_ndvi.csv",
        "soil_moisture": ROOT / "data" / "raw" / "BN_sm.csv",
    },
    # Add DB, GOU, LAL, PB in the same format.
}

if __name__ == "__main__":
    results = run_pipeline(REGISTRY)
    for parcel, info in results.items():
        print(parcel, info["metrics"])
