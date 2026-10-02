import numpy as np
import pandas as pd
from src.config import TARGET_COMMODITIES


def clean_trade_data(df: pd.DataFrame) -> pd.DataFrame:
  """Cleans raw trade data: standardizes column names, fixes dtypes, removes duplicates,

  filters target commodities, handles aggregate rows, and interpolates missing years.
  """
  df = df.copy()

  # Standardize column naming convention
  column_mapping = {
      'Financial_Year': 'financial_year',
      'Year': 'year',
      'Commodity_Group': 'commodity',
      'Destination_Country': 'destination_country',
      'Export_Quantity_MT': 'export_quantity',
      'Export_Value_USD_Million': 'export_value',
      'Export_Value_INR_Crore': 'export_value_inr',
  }
  df = df.rename(columns=column_mapping)

  # Drop duplicates
  df = df.drop_duplicates()

  # Ensure integer year and numeric export values
  df['year'] = df['year'].astype(int)
  df['export_quantity'] = pd.to_numeric(df['export_quantity'], errors='coerce')
  df['export_value'] = pd.to_numeric(df['export_value'], errors='coerce')

  # Filter target commodities and drop generic aggregate rows
  df = df[df['commodity'].isin(TARGET_COMMODITIES)]

  # Check missing years & interpolate missing values per commodity-destination group
  df['is_imputed'] = False

  cleaned_groups = []
  for (commodity, country), group in df.groupby(
      ['commodity', 'destination_country']
  ):
    group = group.sort_values('year').set_index('year')
    min_yr, max_yr = group.index.min(), group.index.max()

    full_idx = pd.Index(range(min_yr, max_yr + 1), name='year')
    reindexed = group.reindex(full_idx)

    # Flag imputed rows
    missing_mask = reindexed['export_value'].isna()
    reindexed['is_imputed'] = missing_mask
    reindexed['commodity'] = commodity
    reindexed['destination_country'] = country

    # Interpolate short gaps linearly
    reindexed['export_quantity'] = reindexed['export_quantity'].interpolate(
        method='linear'
    )
    reindexed['export_value'] = reindexed['export_value'].interpolate(
        method='linear'
    )

    cleaned_groups.append(reindexed.reset_index())

  cleaned_df = pd.concat(cleaned_groups, ignore_index=True)
  return cleaned_df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
  """Adds unit_value, yoy_growth, and commodity_group features."""
  df = df.copy()

  # Unit Value: USD per Metric Tonne
  df['unit_value'] = np.where(
      df['export_quantity'] > 0,
      (df['export_value'] * 1_000_000) / df['export_quantity'],
      np.nan,
  )

  # Calculate YoY Growth (%) per commodity and destination country
  df['yoy_growth'] = df.groupby(['commodity', 'destination_country'])[
      'export_value'
  ].pct_change() * 100

  # High-level commodity grouping mapping
  group_map = {
      'Rice (Basmati & Non-Basmati)': 'Cereals',
      'Spices': 'Horticulture & Spices',
      'Tea': 'Plantation Crops',
      'Marine Products': 'Animal & Marine',
  }
  df['commodity_group'] = df['commodity'].map(group_map)

  return df


def validate_clean(df: pd.DataFrame) -> None:
  """Validates dataset rules to satisfy interface contracts."""
  required_cols = [
      'year',
      'commodity',
      'commodity_group',
      'export_quantity',
      'export_value',
      'unit_value',
      'yoy_growth',
      'is_imputed',
  ]

  # Check columns
  for col in required_cols:
    if col not in df.columns:
      raise ValueError(f"Missing required column: {col}")

  # Check duplicates
  if df.duplicated(
      subset=['year', 'commodity', 'destination_country']
  ).any():
    raise ValueError(
        'Duplicate records found for year, commodity, and destination country.'
    )

  # Check non-negatives
  if (df['export_value'] < 0).any() or (df['export_quantity'] < 0).any():
    raise ValueError('Dataset contains negative export values or quantities.')
  