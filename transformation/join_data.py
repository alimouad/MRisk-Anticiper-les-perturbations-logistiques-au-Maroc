import pandas as pd
from pathlib import Path


CITIES_FILE = Path(
    "data/silver/cities_clean.csv"
)

WEATHER_FILE = Path(
    "data/silver/weather_clean.csv"
)

OUTPUT_FILE = Path(
    "data/silver/weather_joined.csv"
)


def join_data():

    print("Joining cities and weather data...")

    cities = pd.read_csv(CITIES_FILE)

    weather = pd.read_csv(WEATHER_FILE)

    # Keep city information
    cities = cities[
        [
            "city_name",
            "latitude",
            "longitude"
        ]
    ]

    # Join using city name
    df = weather.merge(
        cities,
        on="city_name",
        how="inner",
        suffixes=(
            "_weather",
            "_city"
        )
    )

    print(f"Joined rows: {len(df)}")

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    return df


if __name__ == "__main__":
    join_data()