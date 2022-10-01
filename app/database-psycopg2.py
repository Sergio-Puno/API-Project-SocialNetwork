import psycopg2
from psycopg2.extras import RealDictCursor
import configparser

# Connection file when the API was using psycopg2 / configparser and raw SQL queries

# Get Connection Details from config file
parser = configparser.ConfigParser()
parser.read("app/conn.conf")
hostname = parser.get("postgres_fastapi", "hostname")
database = parser.get("postgres_fastapi", "database")
user = parser.get("postgres_fastapi", "username")
password = parser.get("postgres_fastapi", "password")


# Attempt Database Connection
def get_db():
    try:
        conn = psycopg2.connect(host=hostname, database=database, user=user, password=password, cursor_factory=RealDictCursor)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        print("Database connection completed successfully.")
        yield conn, cursor
    finally:
        conn.close()