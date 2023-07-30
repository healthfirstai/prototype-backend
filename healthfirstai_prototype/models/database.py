from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or ""
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY") or ""
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY") or ""
os.environ["PINECONE_ENV_NAME"] = os.getenv("PINECONE_ENV_NAME") or ""
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY") or ""

DB_USER = os.getenv("POSTGRES_USER") or ""
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD") or ""
DB_HOST = os.getenv("POSTGRES_HOST") or ""
DB_NAME = os.getenv("POSTGRES_DATABASE") or ""
DB_PORT = os.getenv("POSTGRES_PORT") or ""

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or ""
REDIS_HOST = os.getenv("REDIS_HOST") or ""
REDIS_PORT = os.getenv("REDIS_PORT") or 6379

conn = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(conn)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
