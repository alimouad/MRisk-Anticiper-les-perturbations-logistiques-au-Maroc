
import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv


# ============================================================
# 1. CONFIGURATION
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="Weather Risk Dashboard",
    page_icon="🌦️",
    layout="wide"
)


# ============================================================
# 2. DATABASE CONNECTION
# ============================================================

def get_connection():

    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )


# ============================================================
# 3. LOAD DATA
# ============================================================

def load_data():

    conn = get_connection()

    query = """
        SELECT
            c.name AS city,
            wf.forecast_date,
            wf.temperature_max,
            wf.temperature_min,
            wf.precipitation_sum,
            wf.precipitation_probability,
            wf.wind_speed_max,
            wf.wind_gusts_max,
            wr.risk_score,
            wr.risk_level

        FROM weather_forecasts wf

        JOIN cities c
            ON wf.city_id = c.id

        JOIN weather_risks wr
            ON wf.id = wr.weather_id

        ORDER BY wf.forecast_date;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    df["forecast_date"] = pd.to_datetime(
        df["forecast_date"]
    )

    return df


# ============================================================
# 4. GET DATA
# ============================================================

try:

    df = load_data()

except Exception as e:

    st.error(
        f"Erreur de connexion à PostgreSQL : {e}"
    )

    st.stop()


# ============================================================
# 5. TITLE
# ============================================================

st.title("🌦️ Weather Risk Dashboard")

st.write(
    "Visualisation des prévisions météorologiques "
    "et des risques pour les opérations de livraison."
)
       
st.divider()


# ============================================================
# 6. SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filtres")


# ------------------------------------------------------------
# Ville
# ------------------------------------------------------------

cities = sorted(
    df["city"].unique().tolist()
)

selected_city = st.sidebar.selectbox(
    "Ville",
    ["Toutes"] + cities
)


# ------------------------------------------------------------
# Niveau de risque
# ------------------------------------------------------------

risk_levels = [
    "Tous",
    "Faible",
    "Modéré",
    "Élevé",
    "Critique"
]

selected_risk = st.sidebar.selectbox(
    "Niveau de risque",
    risk_levels
)


# ------------------------------------------------------------
# Date
# ------------------------------------------------------------

min_date = df["forecast_date"].min().date()
max_date = df["forecast_date"].max().date()

selected_date = st.sidebar.date_input(
    "Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)


# ------------------------------------------------------------
# Période
# ------------------------------------------------------------

period = st.sidebar.selectbox(
    "Période",
    [
        "Toutes",
        "3 jours",
        "5 jours",
        "7 jours"
    ]
)


# ============================================================
# 7. APPLY FILTERS
# ============================================================

filtered_df = df.copy()


# Filter city

if selected_city != "Toutes":

    filtered_df = filtered_df[
        filtered_df["city"] == selected_city
    ]


# Filter risk

if selected_risk != "Tous":

    filtered_df = filtered_df[
        filtered_df["risk_level"] == selected_risk
    ]


# Filter date

filtered_df = filtered_df[
    filtered_df["forecast_date"].dt.date >= selected_date
]


# Filter period

if period != "Toutes":

    days = int(
        period.split()[0]
    )

    end_date = pd.Timestamp(
        selected_date
    ) + pd.Timedelta(
        days=days - 1
    )

    filtered_df = filtered_df[
        filtered_df["forecast_date"]
        <= end_date
    ]


# ============================================================
# 8. EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "Aucune donnée ne correspond aux filtres."
    )

    st.stop()


# ============================================================
# 9. KPIs
# ============================================================

st.subheader("📊 Indicateurs principaux")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🏙️ Villes",
        filtered_df["city"].nunique()
    )


with col2:

    st.metric(
        "📅 Prévisions",
        len(filtered_df)
    )


with col3:

    average_risk = filtered_df[
        "risk_score"
    ].mean()

    st.metric(
        "⚠️ Risque moyen",
        f"{average_risk:.1f}/100"
    )


with col4:

    critical_count = (
        filtered_df["risk_level"] == "Critique"
    ).sum()

    st.metric(
        "🚨 Critiques",
        critical_count
    )


st.divider()


# ============================================================
# 10. RISK SCORE BY DATE
# ============================================================

st.subheader("📈 Évolution du risque")


risk_by_date = (
    filtered_df
    .groupby("forecast_date")["risk_score"]
    .mean()
)


st.line_chart(
    risk_by_date,
    use_container_width=True
)


# ============================================================
# 11. PRECIPITATION
# ============================================================

st.subheader("🌧️ Précipitations prévues")


rain_by_date = (
    filtered_df
    .groupby("forecast_date")["precipitation_sum"]
    .mean()
)


st.bar_chart(
    rain_by_date,
    use_container_width=True
)


# ============================================================
# 12. TEMPERATURE
# ============================================================

st.subheader("🌡️ Température maximale")


temperature_by_date = (
    filtered_df
    .groupby("forecast_date")["temperature_max"]
    .mean()
)


st.line_chart(
    temperature_by_date,
    use_container_width=True
)


# ============================================================
# 13. WIND
# ============================================================

st.subheader("💨 Vent maximal")


wind_by_date = (
    filtered_df
    .groupby("forecast_date")["wind_speed_max"]
    .mean()
)


st.bar_chart(
    wind_by_date,
    use_container_width=True
)


# ============================================================
# 14. RISK TABLE
# ============================================================

st.subheader("🚨 Prévisions et risques")


display_df = filtered_df[
    [
        "city",
        "forecast_date",
        "temperature_max",
        "precipitation_sum",
        "wind_speed_max",
        "risk_score",
        "risk_level"
    ]
].copy()


display_df = display_df.sort_values(
    "risk_score",
    ascending=False
)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 15. FOOTER
# ============================================================

st.divider()

st.caption(
    "Weather Risk Pipeline | "
    "Bronze → Silver → Gold → PostgreSQL → Streamlit"
)

