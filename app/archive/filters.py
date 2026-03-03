import streamlit as st
from utils import execute_query

# Filter values
filter={}

# Filters
# City Filter (Multi-select)
def city_filter():
  city_list = list(execute_query("select distinct City from listings order by City")["City"])
  selected_city = st.sidebar.multiselect(
    label="City",
    options=city_list
  )
  filter['City'] = selected_city

# Property Filter (Dropdown)
def property_filter():
  selected_property_type = st.sidebar.selectbox(
    label="Property Type", 
    options=["All"] + list(execute_query("select distinct Property_Type from listings order by Property_Type")["Property_Type"])
  )
  filter['Property_Type'] = selected_property_type

# Price Range
def price_filter():
  selected_price_range = st.sidebar.slider(
    "Price Range ($)", 
    min_value=0, 
    max_value=5000000, 
    value=5000000, 
    step=500000, 
    format='dollar'
  )
  filter['Price'] = selected_price_range

# Agent Filter
def agent_filter():
  selected_agent = st.sidebar.selectbox(
    "Agent ID", ['All'] + list(execute_query("select distinct Agent_ID from agents")['Agent_ID'])
  )
  filter['Agent'] = selected_agent

# From Listed Date Range
def from_l_date_filter():
  selected_from_l_date_range = st.sidebar.date_input(
    "From Listed Date (YYY-MM-DD)",
    value='2023-01-01',
    min_value='2023-01-01'
  )
  filter['From Listed Date'] = selected_from_l_date_range

# To Listed Date Range
def to_l_date_filter():
  selected_to_l_date_range = st.sidebar.date_input(
    "To Listed Date (YYY-MM-DD)",
    value='today',
    min_value='2023-01-01'
  )
  filter['To Listed Date'] = selected_to_l_date_range