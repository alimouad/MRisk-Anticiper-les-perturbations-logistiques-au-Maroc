import pandas as pd
from pathlib import Path


INPUT_FILE = Path("data/bronze/cities/morocco_cities.csv")
OUTPUT_FILE = Path("data/bronze/cities/cities_raw.csv")


def extract_cities():
    print("Reading SimpleMaps CSV...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Total cities found: {len(df)}")
    print("Columns:", df.columns.tolist())

    # Keep only useful columns
    cities = df[["city", "lat", "lng"]].copy()

    cities = cities.rename(columns={
        "city": "city_name",
        "lat": "latitude",
        "lng": "longitude"
    })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    cities.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Cities saved to: {OUTPUT_FILE}")

    return cities


if __name__ == "__main__":
    extract_cities()