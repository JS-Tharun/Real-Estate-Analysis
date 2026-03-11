from optparse import Option
from turtle import onclick
import streamlit as st
from utils.utils import execute_query
import math

filter = {}

class Reset:
  def __init__(self):
    button = st.button("Reset")

def property_sidebar_filter():
  st.header("Filter Panel")
  st.caption("Narrow the data by price, location, property details, agent, and listing date. All charts and tables below update automatically.")
  price_filter()
  sqft_filter()
  city_filter()
  property_type_filter()
  property_status_filter()
  rent_filter()
  
  st.divider()
  st.write("## Amenities")
  furnishing_filter()
  bedroom_filter()
  bathroom_filter()
  metro_distance_filter()
  parking_filter()
  power_backup_filter()

  st.divider()
  st.write("## Listed By")
  agent_filter()
  from_l_date_filter()
  to_l_date_filter()

  st.divider()
  st.write("### Buyer")
  buyer_type_filter()
  payment_method_filter()
  loan_taken_filter()

def property_type_filter():
  property_types = list(execute_query("select distinct Property_Type from listings order by Property_Type")["Property_Type"])
  selected_property_type = st.multiselect(
    label="Property Type",
    options=property_types,
    placeholder='All'
  )
  filter['Property Type'] = selected_property_type

def city_filter():
  city_list = list(execute_query("select distinct City from listings order by City")["City"])
  selected_city = st.multiselect(
    label="City",
    options=city_list,
    placeholder='All'
  )
  filter['City'] = selected_city

def price_filter():
  # Getting the minimum and maximum price from the dataset
  min_price = int(list(execute_query("select round(min(Price), 0) from listings")['round(min(Price), 0)'])[0])
  max_price = int(list(execute_query("select round(max(Price), 0) from listings")['round(max(Price), 0)'])[0])

  selected_price_range = st.slider(
    "Price Range", 
    min_value=0, 
    max_value= math.ceil(max_price / 100000) * 100000, #Rounding the value to the next multiple of 100,000
    step=100000,
    format='dollar',
    value=(min_price, max_price)
  )
  filter['Price Range'] = selected_price_range

def agent_filter():
  selected_agent = st.selectbox(
    label="Agent ID", 
    options=list(execute_query("select distinct Agent_ID from agents")['Agent_ID']),
    index=None,
    placeholder='All'
  )
  filter['Agent'] = selected_agent

def from_l_date_filter():
  selected_from_l_date = st.date_input(
    "From Listed Date (YYY-MM-DD)",
    value='2023-01-01',
    min_value='2023-01-01'
  )
  filter['From Listed Date'] = selected_from_l_date

def to_l_date_filter():
  selected_to_l_date = st.date_input(
    "To Listed Date (YYY-MM-DD)",
    value='today',
    min_value='2023-01-01'
  )
  filter['To Listed Date'] = selected_to_l_date

def property_status_filter():
  selected_property_status = st.selectbox(
    "Property Status",
    options=['Sold', 'Unsold'],
    index=None,
    placeholder='All'
  )
  filter['Property Status'] = selected_property_status

def bedroom_filter():
  selected_bedroom_range = st.slider(
    "Number of Bedroom",
    min_value=1,
    max_value=5,
    step=1,
    value=(1,5)
  )
  filter['Bedroom Range'] = selected_bedroom_range

def bathroom_filter():
  selected_bathroom_range = st.slider(
    "Number of Bathroom",
    min_value=1,
    max_value=5,
    step=1,
    value=(1,5)
  )
  filter['Bathroom Range'] = selected_bathroom_range

def rent_filter():
  selected_rent_status = st.selectbox(
    "Rent Status",
    options=['Occupied', 'Available'],
    index=None,
    placeholder="All"
  )
  filter['Rent Status'] = selected_rent_status

def furnishing_filter():
  furnish_types = list(execute_query("select distinct Furnishing_Status from property_attributes")["Furnishing_Status"])
  selected_furnishing_status = st.multiselect(
    label="Furnishing Status",
    options=furnish_types,
    placeholder='All'
  )
  filter['Furnishing Status'] = selected_furnishing_status

def metro_distance_filter():
  min_dis = float(list(execute_query("select min(Metro_Distance) from property_attributes")['min(Metro_Distance)'])[0])
  max_dis = float(list(execute_query("select max(Metro_Distance) from property_attributes")['max(Metro_Distance)'])[0])
  selected_distance_range = st.slider(
    "Distance from Nearest Metro Station",
    min_value=0.0,
    max_value=float(math.ceil(max_dis / 10) * 10),
    value=(min_dis, max_dis),
    step=0.50
  )
  filter['Metro Distance'] = selected_distance_range

def parking_filter():
  selected_parking_value = st.selectbox(
    label="Parking Availability",
    options=['Yes', 'No'],
    index=None,
    placeholder='All'
  )
  filter['Parking'] = selected_parking_value

def power_backup_filter():
  selected_power_backup_value = st.selectbox(
    label="Power Backup Availability",
    options=['Yes', 'No'],
    index=None,
    placeholder='All'
  )
  filter['Power Backup'] = selected_power_backup_value


def sqft_filter():

  min_sqft = int(list(execute_query("select round(min(Sqft), 0) from listings")['round(min(Sqft), 0)'])[0])
  max_sqft = int(list(execute_query("select round(max(Sqft), 0) from listings")['round(max(Sqft), 0)'])[0])

  selected_sqft_range = st.slider(
    "Property Sqft Range", 
    min_value=0, 
    max_value= math.ceil(max_sqft / 1000) * 1000, 
    step=500,
    format='',
    value=(min_sqft, max_sqft)
  )
  filter['Sqft Range'] = selected_sqft_range

def buyer_type_filter():
  selected_buyer_type = st.selectbox(
    "Buyer Type",
    options=['End User', 'Investor'],
    index=None,
    placeholder='All'
  )
  filter['Buyer Type'] = selected_buyer_type

def payment_method_filter():
  payment_methods = list(execute_query("select distinct payment_method from buyers")["payment_method"])
  selected_payment_method = st.selectbox(
    "Payment Method",
    options=payment_methods,
    index=None,
    placeholder='All'
  )
  filter['Payment Method'] = selected_payment_method

def loan_taken_filter():
    options = {
        "Yes": True,
        "No": False
    }

    selected_loan_taken = st.selectbox(
        "Loan Taken",
        options=list(options.keys()),
        index=None,
        placeholder='All'
    )

    if selected_loan_taken is not None:
        filter["Loan Taken"] = options[selected_loan_taken]
    else:
        filter["Loan Taken"] = "All"