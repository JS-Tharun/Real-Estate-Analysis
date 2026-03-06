from altair import Longitude
import streamlit as st
from utils.utils import execute_query
from utils.query import property_master_query
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

def average_price_chart():

  data_query = property_master_query()
  final_query = f"""
    select 
    City,
    count(*) as Number_of_Listings,
    round(avg(Listed_Price), 2) as Average_Price
  from ({data_query}) T
  group by city;
  """
  

  df = execute_query(final_query)
  st.write("### Average Listing Price By City")
  avg_price()
  st.bar_chart(
    data=df,
    x='City', 
    x_label="City",
    y='Average_Price', 
    y_label="Price ($)"
  )

def avg_price():
    data_query = property_master_query()
    avg_price = int(list(execute_query(f"select round(avg(Listed_Price), 2) from ({data_query}) T")['round(avg(Listed_Price), 2)'])[0])
    st.write(f"Total Average - ${avg_price}")