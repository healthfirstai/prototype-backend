from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or ""

DB_USER = os.getenv("POSTGRES_USER") or ""
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD") or ""
DB_HOST = os.getenv("POSTGRES_HOST") or ""
DB_NAME = os.getenv("POSTGRES_DATABASE") or ""
DB_PORT = os.getenv("POSTGRES_PORT") or ""

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or ""
REDIS_HOST = os.getenv("REDIS_HOST") or ""
REDIS_PORT = os.getenv("REDIS_PORT") or 6379

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
