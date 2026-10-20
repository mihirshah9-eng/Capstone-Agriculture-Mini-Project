import os
import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_FOLDER = "outputs"
def plot_annual_export_trend(df):
    if "Year" not in df.columns or "Export_Value_USD_Million" not in df.columns:
        print("Error! Year and Export_value_USD_Million columns not found!")
        return;
    groupedData = (df.groupby("Year")["Export_Value_USD_Million"].sum().reset_index())
    groupedData = groupedData.sort_values("Year")
    x = groupedData["Year"]
    y = groupedData["Export_Value_USD_Million"]

    plt.figure(figsize=(12,6))
    plt.plot(
        x,
        y,
        marker = "o",
        color = "green",
        linewidth = 2,
        label = "Export Value",
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

def plot_commodity_share(df):
    print("\n[Notice]: Seaborn commodity comparison plot staged for final term evaluation.")
def plot_correlation_heatmap(df):
    print("\n[Notice]: Seaborn correlation heatmap plot staged for final term evaluation.")

def get_summary_metrics(df):
    # This function dynamically verifies dataset column names, computes total export revenue
    # and volume using Pandas .sum(), and identifies the top-performing commodity and country using.
    # groupby() chained with .idxmax(). It packs all metrics into a dictionary and returns it to
    #  main.py for terminal output.
    if df.empty:
        print("warning: df is empty")
    valueCol = ("Export_Value_USD_Million" if "Export_Value_USD_Million" in df.columns else None)
    quantityCol = ("Export_Quantity_MT" if "Export_Quantity_MT" in df.columns else None)
    summary = {}
    if valueCol:
        summary["total_export_value"] = round(df[valueCol].sum(), 2)
    if quantityCol:
        summary["total_export_quantity"] = round(df[quantityCol].sum(), 2)
    if valueCol and "Commodity_Group" in df.columns:
        summary["top_commodity"] = df.groupby("Commodity_Group")[valueCol].sum().idxmax()
    if valueCol and "Destination_Country" in df.columns:
        summary["top_destination"] = df.groupby("Destination_Country")[valueCol].sum().idxmax()
    return summary
