from typing import List, Tuple
import pandas as pd
from src.data_loader import load_processed


def get_clean_data() -> pd.DataFrame:
  """Service API: Returns the full cleaned DataFrame for Member B and Member C."""
  return load_processed()


def filter_data(
    df: pd.DataFrame,
    commodities: List[str] = None,
    year_range: Tuple[int, int] = None,
    groups: List[str] = None,
) -> pd.DataFrame:
  """Service API: Filters DataFrame based on selections from UI controls."""
  filtered = df.copy()

  if year_range:
    min_yr, max_yr = year_range
    filtered = filtered[
        (filtered['year'] >= min_yr) & (filtered['year'] <= max_yr)
    ]

  if commodities:
    filtered = filtered[filtered['commodity'].isin(commodities)]

  if groups:
    filtered = filtered[filtered['commodity_group'].isin(groups)]

  return filtered


def list_commodities(df: pd.DataFrame) -> List[str]:
  """Service API: Returns unique sorted commodity names."""
  return sorted(df['commodity'].dropna().unique().tolist())


def get_year_bounds(df: pd.DataFrame) -> Tuple[int, int]:
  """Service API: Returns (min_year, max_year) bounds."""
  return int(df['year'].min()), int(df['year'].max())
