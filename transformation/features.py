import pandas as pd
from pathlib import Path


INPUT_FILE = Path(
    "data/silver/weather_joined.csv"
)

OUTPUT_DIR = Path(
    "data/gold"
)


def create_features():

    print("Starting Feature Engineering...")

    # Read Silver data
    df = pd.read_csv(INPUT_FILE)

    print(f"Input rows: {len(df)}")

    # ==========================================
    # 1. Convert date
    # ==========================================

    df["forecast_date"] = pd.to_datetime(
        df["forecast_date"],
        errors="coerce"
    )

    # ==========================================
    # 2. Temperature Category
    # ==========================================

    def temperature_category(temp):

        if temp < 18:
            return "Cold"

        elif temp < 30:
            return "Normal"

        elif temp < 35:
            return "High"

        elif temp < 40:
            return "Very High"

        else:
            return "Extreme"

    df["temperature_category"] = (
        df["temperature_max"]
        .apply(temperature_category)
    )

    # ==========================================
    # 3. Rain Category
    # ==========================================

    def rain_category(rain):

        if rain == 0:
            return "None"

        elif rain < 5:
            return "Low"

        elif rain < 15:
            return "Moderate"

        elif rain < 30:
            return "High"

        else:
            return "Very High"

    df["rain_category"] = (
        df["precipitation"]
        .apply(rain_category)
    )

    # ==========================================
    # 4. Wind Category
    # ==========================================

    def wind_category(wind):

        if wind < 20:
            return "Low"

        elif wind < 35:
            return "Moderate"

        elif wind < 50:
            return "High"

        elif wind < 70:
            return "Very High"

        else:
            return "Extreme"

    df["wind_category"] = (
        df["wind_speed"]
        .apply(wind_category)
    )

    # ==========================================
    # 5. Date Features
    # ==========================================

    df["forecast_day"] = (
        df["forecast_date"].dt.day
    )

    df["month"] = (
        df["forecast_date"].dt.month
    )

    df["day_of_week"] = (
        df["forecast_date"].dt.day_name()
    )

    # ==========================================
    # 6. Select final Gold columns
    # ==========================================

    df = df[
        [
            "city_name",
            "latitude_city",
            "longitude_city",
            "forecast_date",
            "temperature_max",
            "temperature_min",
            "precipitation",
            "precipitation_probability",
            "wind_speed",
            "wind_gusts",
            "weather_code",
            "temperature_category",
            "rain_category",
            "wind_category",
            "forecast_day",
            "month",
            "day_of_week"
        ]
    ]

    # ==========================================
    # 7. Save Gold
    # ==========================================

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        OUTPUT_DIR / "weather_features.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print("Feature Engineering completed!")

    print(f"Output rows: {len(df)}")

    print(f"Saved to: {output_file}")

    return df


if __name__ == "__main__":
    create_features()