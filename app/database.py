import configparser
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get Connection Details from config file
parser = configparser.ConfigParser()
parser.read("app/conn.conf")
hostname = parser.get("postgres_fastapi", "hostname")
database = parser.get("postgres_fastapi", "database")
user = parser.get("postgres_fastapi", "username")
password = parser.get("postgres_fastapi", "password")
port = parser.get("postgres_fastapi", "port")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{hostname}:{port}/{database}"

# Attempt Database Connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()