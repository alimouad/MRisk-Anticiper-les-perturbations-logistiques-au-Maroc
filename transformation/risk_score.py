import pandas as pd
from pathlib import Path


INPUT_FILE = Path(
    "data/gold/weather_features.csv"
)

OUTPUT_FILE = Path(
    "data/gold/weather_risk.csv"
)


# ==========================================
# 1. Rain Risk
# ==========================================

def calculate_rain_risk(rain):

    if rain == 0:
        return 0

    elif rain < 5:
        return 20

    elif rain < 15:
        return 50

    elif rain < 30:
        return 75

    else:
        return 100


# ==========================================
# 2. Wind Risk
# ==========================================

def calculate_wind_risk(wind):

    if wind < 20:
        return 0

    elif wind < 35:
        return 25

    elif wind < 50:
        return 50

    elif wind < 70:
        return 75

    else:
        return 100


# ==========================================
# 3. Temperature Risk
# ==========================================

def calculate_temperature_risk(temp):

    # Normal temperature
    if 18 <= temp <= 30:
        return 0

    # High temperature
    elif temp <= 35:
        return 30

    # Very high temperature
    elif temp <= 40:
        return 60

    # Extreme temperature
    elif temp <= 45:
        return 80

    # Very extreme
    elif temp > 45:
        return 100

    # Cold temperature
    elif temp < 18:
        return 30


# ==========================================
# 4. Precipitation Probability Risk
# ==========================================

def calculate_probability_risk(probability):

    if probability < 20:
        return 0

    elif probability < 40:
        return 25

    elif probability < 60:
        return 50

    elif probability < 80:
        return 75

    else:
        return 100


# ==========================================
# 5. Risk Level
# ==========================================

def get_risk_level(score):

    if score < 25:
        return "Faible"

    elif score < 50:
        return "Modéré"

    elif score < 75:
        return "Élevé"

    else:
        return "Critique"


# ==========================================
# 6. Create Risk Score
# ==========================================

def create_risk_score():

    print("Starting Risk Score calculation...")

    df = pd.read_csv(
        INPUT_FILE,
        keep_default_na=False
    )

    print(f"Input rows: {len(df)}")

    # --------------------------------------
    # Calculate individual risks
    # --------------------------------------

    df["rain_risk"] = (
        df["precipitation"]
        .apply(calculate_rain_risk)
    )

    df["wind_risk"] = (
        df["wind_speed"]
        .apply(calculate_wind_risk)
    )

    df["temperature_risk"] = (
        df["temperature_max"]
        .apply(calculate_temperature_risk)
    )

    df["probability_risk"] = (
        df["precipitation_probability"]
        .apply(calculate_probability_risk)
    )

    # --------------------------------------
    # Weighted Risk Score
    # --------------------------------------

    df["risk_score"] = (
        df["rain_risk"] * 0.35
        + df["wind_risk"] * 0.30
        + df["temperature_risk"] * 0.20
        + df["probability_risk"] * 0.15
    )

    # Round score
    df["risk_score"] = (
        df["risk_score"]
        .round(2)
    )

    # --------------------------------------
    # Risk Level
    # --------------------------------------

    df["risk_level"] = (
        df["risk_score"]
        .apply(get_risk_level)
    )

    # --------------------------------------
    # Save Gold
    # --------------------------------------

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("================================")
    print("Risk Score calculation completed!")
    print("================================")

    print(f"Rows: {len(df)}")
    print(f"Output: {OUTPUT_FILE}")

    print()
    print("Risk level distribution:")

    print(
        df["risk_level"]
        .value_counts()
    )

    return df


if __name__ == "__main__":

    create_risk_score()