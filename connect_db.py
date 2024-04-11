import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker


load_dotenv()

dialect = "postgresql"
username = "postgres"
password = os.getenv("DB_PASS")
host = "localhost"
port = 5432
database = "my_hw"

DB_URL = URL.create(
    drivername=dialect,
    username=username,
    password=password,
    host=host,
    port=port,
    database=database
)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)
session = Session()
