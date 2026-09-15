import pandas as pd
from pathlib import Path


CITIES_FILE = Path(
    "data/silver/cities_clean.csv"
)

WEATHER_FILE = Path(
    "data/silver/weather_clean.csv"
)


def validate_cities():

    df = pd.read_csv(CITIES_FILE)

    print("\n=== Cities Quality Check ===")

    print("Rows:", len(df))

    print(
        "Missing values:"
    )
    print(df.isnull().sum())

    print(
        "Duplicate cities:",
        df["city_name"].duplicated().sum()
    )

    print(
        "Invalid latitude:",
        (~df["latitude"].between(27, 36)).sum()
    )

    print(
        "Invalid longitude:",
        (~df["longitude"].between(-14, -1)).sum()
    )


def validate_weather():

    df = pd.read_csv(WEATHER_FILE)

    print("\n=== Weather Quality Check ===")

    print("Rows:", len(df))

    print("\nMissing values:")
    print(df.isnull().sum())

    print(
        "\nDuplicate city/date:",
        df.duplicated(
            subset=[
                "city_name",
                "forecast_date"
            ]
        ).sum()
    )

    print(
        "\nInvalid precipitation:",
        (df["precipitation"] < 0).sum()
    )

    print(
        "Invalid precipitation probability:",
        (
            ~df["precipitation_probability"]
            .between(0, 100)
        ).sum()
    )

    print(
        "Invalid wind speed:",
        (df["wind_speed"] < 0).sum()
    )


if __name__ == "__main__":

    validate_cities()
    validate_weather()