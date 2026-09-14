import requests
import pandas as pd
from pathlib import Path
from datetime import datetime


API_URL = "https://api.open-meteo.com/v1/forecast"

CITIES_FILE = Path(
    "data/bronze/cities/cities_raw.csv"
)

OUTPUT_DIR = Path(
    "data/bronze/weather"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def get_weather(latitude, longitude):

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "daily": ",".join([
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "weather_code",
        ]),

        "timezone": "Africa/Casablanca",
        "forecast_days": 7,
    }

    try:

        response = requests.get(
            API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if "daily" not in data:
            raise ValueError(
                "Invalid API response: daily data missing"
            )

        return data

    except requests.exceptions.Timeout:

        print(
            "ERROR: Open-Meteo request timed out"
        )

    except requests.exceptions.HTTPError as e:

        print(
            f"ERROR: HTTP error: {e}"
        )

    except requests.exceptions.RequestException as e:

        print(
            f"ERROR: Request failed: {e}"
        )

    except ValueError as e:

        print(
            f"ERROR: Invalid response: {e}"
        )

    return None


def extract_weather():

    print("Reading cities...")

    cities = pd.read_csv(CITIES_FILE)

    print(
        f"Starting weather extraction "
        f"for {len(cities)} cities..."
    )

    all_weather = []

    for index, city in cities.iterrows():

        city_name = city["city_name"]
        latitude = city["latitude"]
        longitude = city["longitude"]

        print(
            f"[{index + 1}/{len(cities)}] "
            f"Getting weather for {city_name}..."
        )

        weather = get_weather(
            latitude,
            longitude
        )

        if weather is None:
            print(
                f"Skipping {city_name}"
            )
            continue

        daily = weather["daily"]

        for i in range(len(daily["time"])):

            all_weather.append({

                "city_name": city_name,

                "latitude": latitude,

                "longitude": longitude,

                "forecast_date":
                    daily["time"][i],

                "temperature_max":
                    daily["temperature_2m_max"][i],

                "temperature_min":
                    daily["temperature_2m_min"][i],

                "precipitation":
                    daily["precipitation_sum"][i],

                "precipitation_probability":
                    daily[
                        "precipitation_probability_max"
                    ][i],

                "wind_speed":
                    daily[
                        "wind_speed_10m_max"
                    ][i],

                "wind_gusts":
                    daily[
                        "wind_gusts_10m_max"
                    ][i],

                "weather_code":
                    daily["weather_code"][i],

            })

    if not all_weather:

        print(
            "ERROR: No weather data extracted."
        )

        return None

    df = pd.DataFrame(all_weather)

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        OUTPUT_DIR /
        f"weather_{timestamp}.csv"
    )

    # convert data to csv
    df.to_csv(
        output_file,
        index=False
    )

    print()
    print("================================")
    print("Weather extraction completed!")
    print("================================")
    print(f"Cities: {df['city_name'].nunique()}")
    print(f"Records: {len(df)}")
    print(f"Output: {output_file}")

    return df


if __name__ == "__main__":
    extract_weather()