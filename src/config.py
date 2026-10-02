from pathlib import Path

# Paths relative to repo root
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "indian_agricultural_exports.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "exports_clean.csv"

# Configuration parameters for Agriculture Exports domain
TARGET_COMMODITIES = [
    "Rice (Basmati & Non-Basmati)",
    "Spices",
    "Tea",
    "Marine Products",
]

YEAR_START = 2015
YEAR_END = 2025
TEST_SIZE = 3
HORIZON = 3