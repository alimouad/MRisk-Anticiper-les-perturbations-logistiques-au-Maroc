import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    return connection