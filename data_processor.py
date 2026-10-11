import pandas as pd


def load_data(path):
    try:
        df = pd.read_csv(path)
        print("Data loaded successfully!")
        return df
    except FileNotFoundError:
        print("File not found, check the path.")
        return None
    except Exception as e:
        print("Something went wrong:", e)
        return None


def clean_data(df):
    df["Commodity_Group"] = df["Commodity_Group"].str.strip()
    df["Destination_Country"] = df["Destination_Country"].str.strip()

    before = len(df)
    df = df.drop_duplicates()
    print("Duplicates removed:", before - len(df))

    num_cols = df.select_dtypes(include="number").columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    df = df.dropna(subset=["Commodity_Group", "Destination_Country"])
    return df


def add_yoy_growth(df):
    df = df.sort_values(["Commodity_Group", "Destination_Country", "Year"])
    df["YoY_Growth"] = df.groupby(["Commodity_Group", "Destination_Country"])["Export_Value_USD_Million"].pct_change() * 100
    return df


def add_unit_value(df):
    qty_col = [c for c in df.columns if "Quantity" in c][0]
    df["Unit_Value"] = df["Export_Value_USD_Million"] * 1000000 / df[qty_col]
    return df


def filter_by_commodity(df, name):
    return df[df["Commodity_Group"] == name]


def filter_by_country(df, country):
    return df[df["Destination_Country"] == country]


def filter_by_years(df, start, end):
    return df[(df["Year"] >= start) & (df["Year"] <= end)]


def get_clean_data(path):
    df = load_data(path)
    if df is None:
        return None
    df = clean_data(df)
    df = add_yoy_growth(df)
    df = add_unit_value(df)
    return df


if __name__ == "__main__":
    data = get_clean_data("data/processed/exports_clean.csv")
    if data is not None:
        print(data.head())
        print(data.columns.tolist())