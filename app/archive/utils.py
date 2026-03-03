from dotenv import load_dotenv
import os
import mysql.connector
import pandas as pd

load_dotenv()

# Establish MySQL Connection
def get_connection():
  return mysql.connector.connect(
    host = os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database='real_estate'
  )

# Function to execute query and return results as a DataFrame
def execute_query(query):
  conn = get_connection()
  df = pd.read_sql(query, conn)
  conn.close()
  return df