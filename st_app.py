import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
import streamlit as st




# Establish MySQL Connection
def get_connection():
  load_dotenv()
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

# Streamlit UI
st.title("Real Enstate Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

# City Filter (Multi-select)
city_list = list(execute_query("select distinct City from listings order by City")["City"])
selected_city = st.sidebar.multiselect(
  label="City",
  options=city_list
)

# Property Filter (Dropdown)
selected_property_type = st.sidebar.selectbox(
  label="Property Type", 
  options=["All"] + list(execute_query("select distinct Property_Type from listings order by Property_Type")["Property_Type"])
)

# Price Range
selected_price_range = st.sidebar.slider(
  "Price Range ($)", 
  min_value=0, 
  max_value=5000000, 
  value=5000000, 
  step=500000, 
  format='dollar'
)

# Agent Filter
selected_agent = st.sidebar.selectbox(
  "Agent ID", ['All'] + list(execute_query("select distinct Agent_ID from agents")['Agent_ID'])
)

# Listed Date Range
selected_from_l_date_range = st.sidebar.date_input(
  "From Listed Date (YYY-MM-DD)",
  value='2023-01-01',
  min_value='2023-01-01'
)

selected_to_l_date_range = st.sidebar.date_input(
  "To Listed Date (YYY-MM-DD)",
  value='today',
  min_value='2023-01-01'
)

# SQL query based on filter
query = f"""
select 
  * 
from 
  listings 
where 
  (Price between 0 AND {selected_price_range}) 
  AND (Date_Listed between '{selected_from_l_date_range}' AND '{selected_to_l_date_range}')
"""

if len(selected_city) != 0:
  city_str = ", ".join([f"'{city}'" for city in selected_city])
  query += f" AND (City IN ({city_str}))"

if selected_property_type != "All":
  query += f" AND (Property_Type = '{selected_property_type}')"

if selected_agent != "All":
  query += f" AND (Agent_ID = '{selected_agent}')"


# Fetch and display Data
df = execute_query(query)
st.dataframe(df)