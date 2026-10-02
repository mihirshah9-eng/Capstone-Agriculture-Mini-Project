from pathlib import Path
import pandas as pd
from src.config import PROCESSED_DATA_PATH, RAW_DATA_PATH


def load_raw(path: Path | str = RAW_DATA_PATH) -> pd.DataFrame:
  """Load the raw export CSV file."""
  path = Path(path)
  if not path.exists():
    raise FileNotFoundError(f"Raw data file not found at: {path}")
  return pd.read_csv(path)


def load_processed(path: Path | str = PROCESSED_DATA_PATH) -> pd.DataFrame:
  """Load the cleaned and processed export CSV file."""
  path = Path(path)
  if not path.exists():
    raise FileNotFoundError(
        f"Processed data file not found at: {path}. Run 'python -m"
        " src.make_dataset' first."
    )
  return pd.read_csv(path)
