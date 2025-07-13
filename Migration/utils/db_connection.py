# Placeholder for db_connection.py
import psycopg2
from config.db_config import DATABASE_CONFIG

def get_db_connection():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise
