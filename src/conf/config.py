import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    __DB_NAME = os.getenv("POSTGRES_DB")
    __DB_USER = os.getenv("POSTGRES_USER")
    __DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    __DB_HOST = os.getenv("POSTGRES_HOST", "db")
    __DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_URL = f"postgresql+asyncpg://{__DB_USER}:{__DB_PASSWORD}@{__DB_HOST}:{__DB_PORT}/{__DB_NAME}"

config = Config()