import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
      db_connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "parkflow"),
            user=os.getenv("DB_USER", "parkflow_user"),
            password=os.getenv("DB_PASSWORD", "parkflow_password"),
            port=os.getenv("DB_PORT", "5432")
      )
      return db_connection