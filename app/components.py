import streamlit as st
import matplotlib.pyplot as plt
from utils import execute_query
from filters import filter, city_filter, price_filter, property_filter, property_filter, agent_filter, from_l_date_filter, to_l_date_filter


# Generate App Sidebar with Filters
def render_sidebar():
  st.sidebar.header("Filters")

  city_filter()
  property_filter()
  price_filter()
  agent_filter()
  from_l_date_filter()
  to_l_date_filter()

# Display DataFrame 
def render_dataframe():
  query = f"""
  select
    *
  from 
    listings 
  where 
    (Price between 0 AND {filter['Price']}) 
    AND (Date_Listed between '{filter['From Listed Date']}' AND '{filter['To Listed Date']}')
  """

  if len(filter['City']) != 0:
    city_str = ", ".join([f"'{city}'" for city in filter['City']])
    query += f" AND (City IN ({city_str}))"

  if filter['Property_Type'] != "All":
    query += f" AND (Property_Type = '{filter['Property_Type']}')"

  if filter['Agent'] != "All":
    query += f" AND (Agent_ID = '{filter['Agent']}')"

  df = execute_query(query)
  st.markdown("""
  ## Filter Result
  """)
  st.dataframe(df)


#Display Map
def render_map():
  query = f"""
  select 
    * 
  from 
    listings 
  where 
    (Price between 0 AND {filter['Price']}) 
    AND (Date_Listed between '{filter['From Listed Date']}' AND '{filter['To Listed Date']}')
  """

  if len(filter['City']) != 0:
    city_str = ", ".join([f"'{city}'" for city in filter['City']])
    query += f" AND (City IN ({city_str}))"

  if filter['Property_Type'] != "All":
    query += f" AND (Property_Type = '{filter['Property_Type']}')"

  if filter['Agent'] != "All":
    query += f" AND (Agent_ID = '{filter['Agent']}')"

  df = execute_query(query)
  st.write("# Map")
  st.map(
    data=df,
    latitude='Latitude',
    longitude='Longitude'
  )


#Display Barchart

def render_bar_chart():
  query = """
    select 
    City,
    count(*) as Number_of_Listings,
    round(avg(price), 2) as Average_Price
  from listings
  group by city;
  """
  df = execute_query(query)
  st.write("# Average Price by City")
  st.bar_chart(
    data=df,
    x='City', x_label="City",
    y='Average_Price', y_label="Price"
  )
  st.write("# Number of Properties by City")
  st.bar_chart(
    data=df,
    x='City', x_label='City',
    y='Number_of_Listings', y_label="Property Count"
  )


def render_pie_chart():
  query = """
    select
    Property_Type,
      round((100 * count(*) / (select count(*) from listings)), 2) as Percentage
  from listings
  group by Property_Type;
  """
  df = execute_query(query)
  fig, ax = plt.subplots()
  ax.pie(df['Percentage'], labels=df['Property_Type'], autopct='%.2f%%')
  ax.axis('equal')

  st.write("# Property Type Distribution")
  st.pyplot(fig)
