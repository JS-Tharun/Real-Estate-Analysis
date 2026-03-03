import streamlit as st
from utils import execute_query

filter = {}

def property_filter():
  property_types = list(execute_query("select distinct Property_Type from listings order by Property_Type")["Property_Type"])
  selected_property_type = st.multiselect(
    label="Property Type",
    options=property_types
  )
  filter['Property Type'] = selected_property_type

def city_filter():
  city_list = list(execute_query("select distinct City from listings order by City")["City"])
  selected_city = st.multiselect(
    label="City",
    options=city_list
  )
  filter['City'] = selected_city

def price_filter():
  selected_price_range = st.slider(
    "Price Range", 
    min_value=100000, 
    max_value=5000000,
    step=100000,
    format='dollar',
    value=(100000, 5000000)
  )
  filter['Price_Range'] = selected_price_range

def agent_filter():
  selected_agent = st.selectbox(
    "Agent ID", ['All'] + list(execute_query("select distinct Agent_ID from agents")['Agent_ID'])
  )
  filter['Agent'] = selected_agent

def from_l_date_filter():
  selected_from_l_date_range = st.date_input(
    "From Listed Date (YYY-MM-DD)",
    value='2023-01-01',
    min_value='2023-01-01'
  )
  filter['From Listed Date'] = selected_from_l_date_range

def to_l_date_filter():
  selected_to_l_date_range = st.date_input(
    "To Listed Date (YYY-MM-DD)",
    value='today',
    min_value='2023-01-01'
  )
  filter['To Listed Date'] = selected_to_l_date_range