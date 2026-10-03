import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
OUTPUTS_DIR = "outputs"


def _get_column(df: pd.DataFrame, candidates: list) -> str:
  """Finds the first existing column from a list of candidate column names."""
  for col in candidates:
    if col in df.columns:
      return col
  return None


def plot_annual_export_trend(df: pd.DataFrame):
  """Generates a Matplotlib line chart showing total export value trend across financial years."""
  val_col = _get_column(
      df, ["export_value", "Export_Value_USD_Million", "export_value_inr"]
  )
  yr_col = _get_column(df, ["year", "Year", "financial_year", "Financial_Year"])

  if not val_col or not yr_col:
    print("[Error]: Missing required year/value columns for trend plotting.")
    return

  trend_data = (
      df.groupby(yr_col)[val_col].sum().reset_index().sort_values(yr_col)
  )

  plt.figure(figsize=(10, 5))
  plt.plot(
      trend_data[yr_col],
      trend_data[val_col],
      marker="o",
      color="#1f77b4",
      linewidth=2.5,
      label="Total Export Value",
  )

  plt.title(
      "Annual Indian Agricultural Export Value", fontsize=13, fontweight="bold"
  )
  plt.xlabel("Year", fontsize=11)
  plt.ylabel("Export Value", fontsize=11)
  plt.grid(True, linestyle="--", alpha=0.6)
  plt.tight_layout()

  os.makedirs(OUTPUTS_DIR, exist_ok=True)
  output_path = os.path.join(OUTPUTS_DIR, "annual_export_trend.png")
  plt.savefig(output_path, dpi=300)
  print(f"[Chart Saved]: {output_path}")
  plt.show()


def plot_commodity_share(df: pd.DataFrame):
  """Generates a Seaborn bar plot showing total export value contribution by commodity."""
  comm_col = _get_column(df, ["commodity", "Commodity_Group", "Commodity"])
  val_col = _get_column(
      df, ["export_value", "Export_Value_USD_Million", "export_value_inr"]
  )

  if not comm_col or not val_col:
    print("[Error]: Missing commodity/value column for comparison.")
    return

  comm_data = (
      df.groupby(comm_col)[val_col]
      .sum()
      .reset_index()
      .sort_values(val_col, ascending=False)
  )

  plt.figure(figsize=(10, 5))
  ax = sns.barplot(
      data=comm_data, x=comm_col, y=val_col, palette="crest", errorbar=None
  )

  plt.title(
      "Total Export Value Share by Commodity", fontsize=13, fontweight="bold"
  )
  plt.xlabel("Commodity Category", fontsize=11)
  plt.ylabel("Total Export Value", fontsize=11)
  plt.xticks(rotation=15, ha="right")
  plt.tight_layout()

  os.makedirs(OUTPUTS_DIR, exist_ok=True)
  output_path = os.path.join(OUTPUTS_DIR, "commodity_share_comparison.png")
  plt.savefig(output_path, dpi=300)
  print(f"[Chart Saved]: {output_path}")
  plt.show()


def plot_correlation_heatmap(df: pd.DataFrame):
  """Generates a Seaborn Heatmap showing numeric feature correlations."""
  numeric_cols = df.select_dtypes(include=["float64", "int64"])

  if numeric_cols.empty or numeric_cols.shape[1] < 2:
    print("[Error]: Insufficient numeric columns for heatmap analysis.")
    return

  plt.figure(figsize=(7, 5))
  sns.heatmap(
      numeric_cols.corr(),
      annot=True,
      cmap="coolwarm",
      fmt=".2f",
      linewidths=0.5,
  )
  plt.title("Numeric Feature Correlation Heatmap", fontsize=13, fontweight="bold")
  plt.tight_layout()

  os.makedirs(OUTPUTS_DIR, exist_ok=True)
  output_path = os.path.join(OUTPUTS_DIR, "feature_correlation_heatmap.png")
  plt.savefig(output_path, dpi=300)
  print(f"[Chart Saved]: {output_path}")
  plt.show()


def get_summary_metrics(df: pd.DataFrame) -> dict:
  """Returns summary statistical dictionary for Member 3's CLI menu."""
  if df.empty:
    return {}

  val_col = _get_column(
      df, ["export_value", "Export_Value_USD_Million", "export_value_inr"]
  )
  qty_col = _get_column(df, ["export_quantity", "Export_Quantity_MT"])
  comm_col = _get_column(df, ["commodity", "Commodity_Group", "Commodity"])
  dest_col = _get_column(df, ["destination_country", "Destination_Country"])

  summary = {}
  if val_col:
    summary["total_export_value"] = round(float(df[val_col].sum()), 2)
  if qty_col:
    summary["total_export_quantity"] = round(float(df[qty_col].sum()), 2)
  if val_col and comm_col:
    summary["top_commodity"] = str(
        df.groupby(comm_col)[val_col].sum().idxmax()
    )
  if val_col and dest_col:
    summary["top_destination"] = str(
        df.groupby(dest_col)[val_col].sum().idxmax()
    )

  return summary
