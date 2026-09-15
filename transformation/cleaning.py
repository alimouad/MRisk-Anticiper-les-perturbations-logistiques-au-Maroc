import pandas as pd
from pathlib import Path


CITIES_FILE = Path("data/bronze/cities/cities_raw.csv")
WEATHER_DIR = Path("data/bronze/weather")

SILVER_DIR = Path("data/silver")


def clean_cities():

    print("Cleaning cities data...")

    df = pd.read_csv(CITIES_FILE)

    print(f"Initial rows: {len(df)}")

    # Remove duplicate cities
    df = df.drop_duplicates(subset=["city_name"])

    # Standardize city names
    df["city_name"] = (
        df["city_name"]
        .astype(str)
        .str.strip()
    )

    # Convert coordinates to numeric
    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce"
    )

    # Remove invalid coordinates
    df = df.dropna(
        subset=[
            "city_name",
            "latitude",
            "longitude"
        ]
    )

    # Check Morocco coordinates roughly
    df = df[
        (df["latitude"].between(27, 36)) &
        (df["longitude"].between(-14, -1))
    ]

    print(f"Clean rows: {len(df)}")

    SILVER_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = SILVER_DIR / "cities_clean.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print(f"Saved to: {output_file}")

    return df


def clean_weather():

    print("Cleaning weather data...")

    # Find the latest Bronze weather file
    weather_files = list(
        WEATHER_DIR.glob("weather_*.csv")
    )

    if not weather_files:
        print("ERROR: No weather files found.")
        return None

    latest_file = max(
        weather_files,
        key=lambda file: file.stat().st_mtime
    )

    print(f"Reading: {latest_file}")

    df = pd.read_csv(latest_file)

    print(f"Initial rows: {len(df)}")

    # Standardize city names
    df["city_name"] = (
        df["city_name"]
        .astype(str)
        .str.strip()
    )

    # Convert date
    df["forecast_date"] = pd.to_datetime(
        df["forecast_date"],
        errors="coerce"
    )

    # Convert numeric columns
    numeric_columns = [
        "latitude",
        "longitude",
        "temperature_max",
        "temperature_min",
        "precipitation",
        "precipitation_probability",
        "wind_speed",
        "wind_gusts",
        "weather_code"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove invalid dates
    df = df.dropna(
        subset=[
            "city_name",
            "forecast_date"
        ]
    )

    # Remove duplicates
    df = df.drop_duplicates(
        subset=[
            "city_name",
            "forecast_date"
        ]
    )

    print(f"Clean rows: {len(df)}")

    output_file = SILVER_DIR / "weather_clean.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print(f"Saved to: {output_file}")

    return df


if __name__ == "__main__":

    clean_cities()
    clean_weather()