import streamlit as st
from utils.utils import execute_query
from utils.data import property_master_query
import plotly.express as px
from tab_components.Dashboard.c_overview import no_of_listings


def map():
    master_table = property_master_query()
    data_query = f"""
        select
            Latitude,
            Longitude
        from
            ({master_table})T
    """
    df = execute_query(data_query)
    st.write("Geographic View")
    st.caption("Where your listings are located on the map and how they are distributed across cities. Use this to see coverage, density, and gaps by geography.")
    st.map(
        data=df,
        latitude='Latitude',
        longitude='Longitude'
    )

def listing_by_city_barchart():
    data_query = property_master_query()
    final_query = f"""
        select 
            City,
            count(*) as Total_listings
        from ({data_query}) T
        group by
            city
    """
    df = execute_query(final_query)
    st.write("Listing by City")
    no_of_listings()
    st.bar_chart(
        data=df,
        x='City',
        y='Total_listings',
        y_label='Count',
        color='#D13734'
    )

def listing_by_city_piechart():
    data_query = property_master_query()
    final_query = f"""
        select 
            City,
            round((100 * count(*) / (select count(*) from ({data_query}) T)), 0) as Percentage
        from ({data_query}) T
        group by
            city
    """
    df = execute_query(final_query)
    st.write("Share of Listing By City")
    no_of_listings()
    fig = px.pie(df, values="Percentage", names="City")
    st.plotly_chart(fig)

def property_distribution_chart_1():
  data_query = property_master_query()
  final_query = f"""
    select
    Property_Type,
      round((100 * count(*) / (select count(*) from listings)), 2) as Percentage
  from ({data_query}) T
  group by Property_Type;
  """
  df = execute_query(final_query)
  st.write("Property Type Distribution")
  fig1 = px.pie(df, values="Percentage", names="Property_Type")
  st.plotly_chart(fig1, key='chart1')

def property_distribution_chart_2():
  data_query = property_master_query()
  final_query = f"""
    select
    Property_Type,
      round((100 * count(*) / (select count(*) from listings)), 2) as Percentage
  from ({data_query}) T
  group by Property_Type;
  """
  df = execute_query(final_query)
  st.write("Property Type Distribution")
  fig2 = px.pie(df, values="Percentage", names="Property_Type")
  st.plotly_chart(fig2, key='chart2')

