import numpy as np
import pandas as pd
import pytest
from src.cleaning import add_features, clean_trade_data, validate_clean


@pytest.fixture
def sample_raw_data():
  return pd.DataFrame({
      "Financial_Year": ["2015-16", "2015-16", "2016-17"],
      "Year": [2015, 2015, 2016],
      "Commodity_Group": ["Spices", "Spices", "Spices"],
      "Destination_Country": ["USA", "USA", "USA"],
      "Export_Quantity_MT": [1000.0, 1000.0, 1200.0],
      "Export_Value_USD_Million": [10.0, 10.0, 12.0],
      "Export_Value_INR_Crore": [82.5, 82.5, 99.0],
  })


def test_clean_trade_data(sample_raw_data):
  cleaned = clean_trade_data(sample_raw_data)
  assert len(cleaned) == 2  # Deduplicated
  assert "commodity" in cleaned.columns
  assert "export_value" in cleaned.columns


def test_add_features(sample_raw_data):
  cleaned = clean_trade_data(sample_raw_data)
  featured = add_features(cleaned)
  assert "unit_value" in featured.columns
  assert "yoy_growth" in featured.columns
  assert "commodity_group" in featured.columns


def test_validate_clean(sample_raw_data):
  cleaned = clean_trade_data(sample_raw_data)
  featured = add_features(cleaned)
  validate_clean(featured)  # Should pass without error