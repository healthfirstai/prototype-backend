from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain.sql_database import SQLDatabase
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or ""
os.environ["SERP_API_KEY"] = os.getenv("SERP_API_KEY") or ""

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

included_tables = ["food_info", "nutrient", "food_info_nutrient_link"] # TODO: Fix the vector datatype not being recognized by the SQLDatabase class then include food_nutrition_vector
sql_agent_db = SQLDatabase(
    engine=engine,
    include_tables=included_tables,
    sample_rows_in_table_info=3,  # Specify sample tables here
    indexes_in_table_info=False,
    custom_table_info=None,  # Maybe update this
    view_support=True,
    max_string_length=300,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# TODO: Transform SQL tables so that the nutrient names are NOT column names and are instead values in the "nutrient_name column".
# Adjust corresponding code to reflect this change.
