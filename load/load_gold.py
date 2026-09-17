
import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

CSV_FILE = "data/gold/weather_risk.csv"


def get_connection():

    return psycopg2.connect(
        host="localhost",
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )


def load_data():

    print("Reading Gold data...")

    df = pd.read_csv(
        CSV_FILE,
        keep_default_na=False
    )

    print(f"Rows found: {len(df)}")

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():

        # ==========================================
        # 1. Insert / Update City
        # ==========================================

        cursor.execute(
            """
            INSERT INTO cities (
                name,
                latitude,
                longitude
            )
            VALUES (%s, %s, %s)

            ON CONFLICT (name)
            DO UPDATE SET
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude

            RETURNING id;
            """,
            (
                row["city_name"],
                row["latitude_city"],
                row["longitude_city"]
            )
        )

        city_id = cursor.fetchone()[0]

        # ==========================================
        # 2. Insert / Update Weather Forecast
        # ==========================================

        cursor.execute(
            """
            INSERT INTO weather_forecasts (
                city_id,
                forecast_date,
                temperature_max,
                temperature_min,
                precipitation_sum,
                precipitation_probability,
                wind_speed_max,
                wind_gusts_max,
                weather_code
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )

            ON CONFLICT (city_id, forecast_date)

            DO UPDATE SET
                temperature_max = EXCLUDED.temperature_max,
                temperature_min = EXCLUDED.temperature_min,
                precipitation_sum = EXCLUDED.precipitation_sum,
                precipitation_probability = EXCLUDED.precipitation_probability,
                wind_speed_max = EXCLUDED.wind_speed_max,
                wind_gusts_max = EXCLUDED.wind_gusts_max,
                weather_code = EXCLUDED.weather_code

            RETURNING id;
            """,
            (
                city_id,
                row["forecast_date"],
                row["temperature_max"],
                row["temperature_min"],
                row["precipitation"],
                row["precipitation_probability"],
                row["wind_speed"],
                row["wind_gusts"],
                row["weather_code"]
            )
        )

        weather_id = cursor.fetchone()[0]

        # ==========================================
        # 3. Insert / Update Risk
        # ==========================================

        cursor.execute(
            """
            INSERT INTO weather_risks (
                weather_id,
                temperature_category,
                precipitation_category,
                wind_category,
                risk_score,
                risk_level
            )
            VALUES (
                %s, %s, %s, %s, %s, %s
            )

            ON CONFLICT (weather_id)

            DO UPDATE SET
                temperature_category =
                    EXCLUDED.temperature_category,

                precipitation_category =
                    EXCLUDED.precipitation_category,

                wind_category =
                    EXCLUDED.wind_category,

                risk_score =
                    EXCLUDED.risk_score,

                risk_level =
                    EXCLUDED.risk_level;
            """,
            (
                weather_id,
                row["temperature_category"],
                row["precipitation_category"],
                row["wind_category"],
                row["risk_score"],
                row["risk_level"]
            )
        )

    # ==========================================
    # Commit
    # ==========================================

    conn.commit()

    cursor.close()
    conn.close()

    print()
    print("========================================")
    print("Gold data loaded successfully!")
    print("========================================")


if __name__ == "__main__":
    load_data()
