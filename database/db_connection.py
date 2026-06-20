import psycopg2

def get_db_connection():
      connection = psycopg2.connect(
            host="localhost",
            database="parkflow",
            user="parkflow_user",
            password="parkflow_password"
      )
      return connection

if __name__ == "__main__":
      connection = get_db_connection()
      if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print("Db connection successful, PostgreSQL version: ", version)
            cursor.close()
            connection.close()
      else:
            print("Failed to connect to the database.")
