import os
import sys

import analytics_engine as analytics
import data_processor as processor


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATHS = [
    os.path.join(BASE_DIR, "data", "processed", "exports_clean.csv"),
    os.path.join(BASE_DIR, "data", "indian_agricultural_exports.csv"),
    os.path.join(BASE_DIR, "exports_clean.csv"),
]


def find_data_file():
    for path in DATA_PATHS:
        if os.path.isfile(path):
            return path
    return None


def print_header():
    print("\n" + "=" * 64)
    print("        INDIAN AGRICULTURAL EXPORTS ANALYSER")
    print("                 Python Capstone Project")
    print("=" * 64)


def print_menu():
    print("\nMAIN MENU")
    print("1. View dataset summary")
    print("2. Show annual export trend chart")
    print("3. Compare export value by commodity")
    print("4. Show numeric correlation heatmap")
    print("5. Find top commodities and destination countries")
    print("6. Filter records by commodity")
    print("7. Filter records by destination country")
    print("8. Filter records by year range")
    print("0. Exit")


def pause():
    input("\nPress Enter to return to the main menu...")


def show_summary(df):
    print("\nDATASET SUMMARY")
    print("-" * 42)
    print(f"Total records       : {len(df):,}")
    print(f"Financial years     : {df['Financial_Year'].nunique() if 'Financial_Year' in df.columns else 'N/A'}")
    print(f"Commodity categories: {df['Commodity_Group'].nunique() if 'Commodity_Group' in df.columns else 'N/A'}")
    print(f"Destination countries: {df['Destination_Country'].nunique() if 'Destination_Country' in df.columns else 'N/A'}")

    metrics = analytics.get_summary_metrics(df)
    if "total_export_value" in metrics:
        print(f"Total export value  : {metrics['total_export_value']:,.2f} USD million")
    if "total_export_quantity" in metrics:
        print(f"Total export quantity: {metrics['total_export_quantity']:,.2f} MT")
    if "top_commodity" in metrics:
        print(f"Top commodity       : {metrics['top_commodity']}")
    if "top_destination" in metrics:
        print(f"Top destination     : {metrics['top_destination']}")


def show_top_analysis(df):
    required = {"Commodity_Group", "Destination_Country", "Export_Value_USD_Million"}
    if not required.issubset(df.columns):
        print("The dataset is missing columns needed for this analysis.")
        return

    commodities = df.groupby("Commodity_Group")["Export_Value_USD_Million"].sum().sort_values(ascending=False).head(5)
    countries = df.groupby("Destination_Country")["Export_Value_USD_Million"].sum().sort_values(ascending=False).head(5)

    print("\nTOP 5 COMMODITIES BY TOTAL EXPORT VALUE")
    print("-" * 48)
    for rank, (name, value) in enumerate(commodities.items(), start=1):
        print(f"{rank}. {name:<34} {value:>12,.2f} USD million")

    print("\nTOP 5 DESTINATION COUNTRIES BY TOTAL EXPORT VALUE")
    print("-" * 48)
    for rank, (name, value) in enumerate(countries.items(), start=1):
        print(f"{rank}. {name:<34} {value:>12,.2f} USD million")


def show_commodity_filter(df):
    names = sorted(df["Commodity_Group"].dropna().astype(str).unique())
    print("\nAvailable commodities:")
    for i, name in enumerate(names, start=1):
        print(f"{i}. {name}")
    choice = input("Enter commodity name (or list number): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(names):
        choice = names[int(choice) - 1]
    result = processor.filter_by_commodity(df, choice)
    if result.empty:
        print("No matching commodity found. Check the spelling and try again.")
    else:
        print(f"\nFound {len(result)} records for {choice}.")
        print(result.head(10).to_string(index=False))
        if len(result) > 10:
            print("Showing the first 10 records only.")


def show_country_filter(df):
    names = sorted(df["Destination_Country"].dropna().astype(str).unique())
    print("\nAvailable destination countries:")
    for i, name in enumerate(names, start=1):
        print(f"{i}. {name}")
    choice = input("Enter country name (or list number): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(names):
        choice = names[int(choice) - 1]
    result = processor.filter_by_country(df, choice)
    if result.empty:
        print("No matching country found. Check the spelling and try again.")
    else:
        print(f"\nFound {len(result)} records for {choice}.")
        print(result.head(10).to_string(index=False))
        if len(result) > 10:
            print("Showing the first 10 records only.")


def show_year_filter(df):
    years = sorted(df["Year"].dropna().astype(int).unique())
    if not years:
        print("No year data is available.")
        return
    print(f"Available year range: {years[0]}–{years[-1]}")
    try:
        start = int(input("Enter starting year: ").strip())
        end = int(input("Enter ending year: ").strip())
        if start > end:
            print("Starting year cannot be later than ending year.")
            return
        result = processor.filter_by_years(df, start, end)
        if result.empty:
            print("No records found in that year range.")
        else:
            print(f"\nFound {len(result)} records from {start} to {end}.")
            print(result.head(10).to_string(index=False))
            if len(result) > 10:
                print("Showing the first 10 records only.")
    except ValueError:
        print("Invalid year. Please enter a whole number, such as 2020.")


def main():
    print_header()
    data_path = find_data_file()
    if data_path is None:
        print("\n[ERROR] Export CSV was not found.")
        print("Place exports_clean.csv in the project root, or in data/processed/.")
        print("You can also use data/indian_agricultural_exports.csv.")
        sys.exit(1)

    df = processor.get_clean_data(data_path)
    if df is None or df.empty:
        print("\n[ERROR] Data could not be loaded, or the dataset is empty.")
        sys.exit(1)

    print(f"Dataset loaded from: {os.path.relpath(data_path, BASE_DIR)}")

    while True:
        print_menu()
        choice = input("\nEnter your choice (0-8): ").strip()

        try:
            if choice == "1":
                show_summary(df)
                pause()
            elif choice == "2":
                analytics.plot_annual_export_trend(df)
                pause()
            elif choice == "3":
                analytics.plot_commodity_share(df)
                pause()
            elif choice == "4":
                analytics.plot_correlation_heatmap(df)
                pause()
            elif choice == "5":
                show_top_analysis(df)
                pause()
            elif choice == "6":
                show_commodity_filter(df)
                pause()
            elif choice == "7":
                show_country_filter(df)
                pause()
            elif choice == "8":
                show_year_filter(df)
                pause()
            elif choice == "0":
                print("\nThank you for using the Indian Agricultural Exports Analyser!")
                break
            else:
                print("Invalid choice. Please enter a number from 0 to 8.")
        except (KeyError, ValueError, TypeError) as error:
            print(f"\n[INPUT/DATA ERROR] {error}")
        except Exception as error:
            print(f"\n[ERROR] This operation could not be completed: {error}")
            print("Check the dataset and required Python libraries, then try again.")


if __name__ == "__main__":
    main()
