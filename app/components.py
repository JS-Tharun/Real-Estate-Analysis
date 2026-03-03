# This file contains all the render components such as dataframes, bargraphs, lineplots, etc.


import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.pyplot import bar_label
import seaborn as sns
from data import listing_query
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
  data_query = listing_query()
  df = execute_query(data_query)
  st.markdown("""
  ## Filter Result
  """)
  st.dataframe(df)


#Display Map
def render_map():
  data_query = listing_query()

  df = execute_query(data_query)
  st.write("## Map")
  st.map(
    data=df,
    latitude='Latitude',
    longitude='Longitude'
  )

#Display Barchart
def render_bar_chart():

  data_query = listing_query()
  final_query = f"""
    select 
    City,
    count(*) as Number_of_Listings,
    round(avg(price), 2) as Average_Price
  from ({data_query}) T
  group by city;
  """
  

  df = execute_query(final_query)
  st.write("## Average Price by City")
  st.bar_chart(
    data=df,
    x='City', x_label="City",
    y='Average_Price', y_label="Price ($)"
  )


  st.write("## Number of Properties by City")
  st.bar_chart(
    data=df,
    x='City', x_label='City',
    y='Number_of_Listings', y_label="Amount"
  )


def property_distribution_chart():
  data_query = listing_query()
  query = f"""
    select
    Property_Type,
      round((100 * count(*) / (select count(*) from listings)), 2) as Percentage
  from ({data_query}) T
  group by Property_Type;
  """
  df = execute_query(query)
  fig, ax = plt.subplots()
  ax.pie(df['Percentage'], labels=df['Property_Type'], autopct='%.2f%%')
  ax.axis('equal')

  st.write("## Property Type Distribution")
  st.pyplot(fig)



  