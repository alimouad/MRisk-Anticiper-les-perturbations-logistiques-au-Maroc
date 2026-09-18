from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator



from extraction.cities import extract_cities
from extraction.weather_api import extract_weather

from transformation.cleaning import (
    clean_cities,
    clean_weather
)

from transformation.validation import (
    validate_cities,
    validate_weather
)

from transformation.join_data import join_data

from transformation.features import create_features

from transformation.risk_score import create_risk_score

from load.load_gold import load_data



default_args = {

    "owner": "mouad",

    "retries": 2,

    "retry_delay": timedelta(minutes=5),
    # "retry_max"

}

with DAG(

    dag_id="weather_risk_pipeline",

    description="Weather Risk ETL Pipeline for Morocco",

    default_args=default_args,

    start_date=datetime(2026, 9, 18),

    schedule="0 6 * * *",

    catchup=False,

    tags=["weather", "ETL", "risk"],

) as dag:


    # ========================================================
    # 1. EXTRACT CITIES
    # ========================================================

    extract_cities_task = PythonOperator(

        task_id="extract_cities",

        python_callable=extract_cities,

    )


    # ========================================================
    # 2. EXTRACT WEATHER
    # ========================================================

    extract_weather_task = PythonOperator(

        task_id="extract_weather",

        python_callable=extract_weather,

    )


    # ========================================================
    # 3. CLEAN DATA
    # ========================================================

    clean_data_task = PythonOperator(

        task_id="clean_data",

        python_callable=lambda: (
            clean_cities(),
            clean_weather()
        ),

    )


    # ========================================================
    # 4. VALIDATE DATA
    # ========================================================

    validate_data_task = PythonOperator(

        task_id="validate_data",

        python_callable=lambda: (
            validate_cities(),
            validate_weather()
        ),

    )


    # ========================================================
    # 5. JOIN DATA
    # ========================================================

    join_data_task = PythonOperator(

        task_id="join_data",

        python_callable=join_data,

    )


    # ========================================================
    # 6. FEATURE ENGINEERING
    # ========================================================

    create_features_task = PythonOperator(

        task_id="create_features",

        python_callable=create_features,

    )


    # ========================================================
    # 7. RISK SCORE
    # ========================================================

    risk_score_task = PythonOperator(

        task_id="calculate_risk",

        python_callable=create_risk_score,

    )


    # ========================================================
    # 8. LOAD TO POSTGRESQL
    # ========================================================

    load_postgres_task = PythonOperator(

        task_id="load_postgres",

        python_callable=load_data,

    )


    # ========================================================
    # TASK DEPENDENCIES
    # ========================================================

    (
        extract_cities_task
        >> extract_weather_task
        >> clean_data_task
        >> validate_data_task
        >> join_data_task
        >> create_features_task
        >> risk_score_task
        >> load_postgres_task
    )

