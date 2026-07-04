import psycopg2

def get_db_connection():
      db_connection = psycopg2.connect(
            host="localhost",
            database="parkflow",
            user="parkflow_user",
            password="parkflow_password",
            port="5432"
      )
      return db_connection