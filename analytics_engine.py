import os
import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_FOLDER = "outputs"
def plot_annual_export_trend(df):
  if "year" not in df.columns or "export_value" not in df.columns:
    print("Error: Required columns ('year', 'export_value') not found.")
    return

  grouped_data = df.groupby("year")["export_value"].sum().reset_index()
  grouped_data = grouped_data.sort_values("year")
  x_years = grouped_data["year"]
  y_values = grouped_data["export_value"]

  plt.figure(figsize=(10, 5))
  plt.plot(
      x_years,
      y_values,
      marker="o",
      color="blue",
      linewidth=2,
      label="Export Value",
  )

  plt.title("Annual Indian Agricultural Export Value Trend")
  plt.xlabel("Year")
  plt.ylabel("Total Export Value (USD Million)")
  plt.grid(True)
  plt.legend()

  plt.tight_layout()
  if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
  file_path = os.path.join(OUTPUT_FOLDER, "annual_export_trend.png")
  plt.savefig(file_path)
  print("Chart saved successfully at:", file_path)
  plt.show()


def get_summary_metrics(df):
  if df.empty:
    print("Warning: DataFrame is empty.")
    return
  total_value = df["export_value"].sum()
  total_quantity = df["export_quantity"].sum()
  top_commodity_series = df.groupby("commodity")["export_value"].sum()
  top_commodity = top_commodity_series.idxmax()
  top_country_series = df.groupby("destination_country")["export_value"].sum()
  top_country = top_country_series.idxmax()

  print("--- DATASET SUMMARY METRICS ---")
  print("Total Export Value (USD Million):", round(total_value, 2))
  print("Total Export Quantity (MT):", round(total_quantity, 2))
  print("Top Performing Commodity:", top_commodity)
  print("Top Export Destination Country:", top_country)
  