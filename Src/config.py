from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = DATA_DIR / "outputs"
LOGS_DIR = BASE_DIR / "logs"

PARCELS = ["BN", "DB", "GOU", "LAL", "PB"]
YEARS = [2022, 2023, 2024]

DATE_COLUMN_CANDIDATES = ["Date", "DATE", "date"]
SOIL_MOISTURE_COLUMN_CANDIDATES = ["Soil_Moisture", "soil_moisture", "SM", "VSM"]
VV_COLUMN_CANDIDATES = ["VV", "vv"]
VH_COLUMN_CANDIDATES = ["VH", "vh"]
NDVI_COLUMN_CANDIDATES = ["NDVI", "ndvi"]
ANGLE_COLUMN_CANDIDATES = ["angle", "Angle", "INCIDENCE_ANGLE"]

MIN_COMMON_DATES = 10
INTERPOLATION_METHOD = "linear"

DEFAULT_WCM_SIGMA_VEG = 0.3
DEFAULT_WCM_A = 0.12
DEFAULT_OUTPUT_DPI = 300

for path in [RAW_DIR, INTERIM_DIR, PROCESSED_DIR, OUTPUTS_DIR, LOGS_DIR]:
    path.mkdir(parents=True, exist_ok=True)
