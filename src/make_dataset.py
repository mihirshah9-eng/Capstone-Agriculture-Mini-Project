from src.cleaning import add_features, clean_trade_data, validate_clean
from src.config import PROCESSED_DATA_PATH
from src.data_loader import load_raw


def main():
  print('Loading raw dataset...')
  raw_df = load_raw()

  print('Cleaning trade dataset...')
  cleaned_df = clean_trade_data(raw_df)

  print('Adding engineered features...')
  featured_df = add_features(cleaned_df)

  print('Validating clean dataset...')
  validate_clean(featured_df)

  PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
  featured_df.to_csv(PROCESSED_DATA_PATH, index=False)
  print(f'Pipeline complete! Cleaned dataset saved to: {PROCESSED_DATA_PATH}')


if __name__ == '__main__':
  main()