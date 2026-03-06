from altair import Longitude
import streamlit as st
from utils.utils import execute_query
from utils.query import property_master_query
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


def no_of_listings():
    data_query = property_master_query()
    Total_Properties = int(list(execute_query(f"select count(*) from ({data_query})T")['count(*)'])[0])
    st.write(f"Total - {Total_Properties}")

def property_distribution_chart():
  data_query = property_master_query()
  final_query = f"""
    select
    Property_Type,
      round((100 * count(*) / (select count(*) from listings)), 2) as Percentage
  from ({data_query}) T
  group by Property_Type;
  """
  df = execute_query(final_query)
  st.write("### Property Type Distribution")
  fig = px.pie(df, values="Percentage", names="Property_Type")
  st.plotly_chart(fig)

def property_type_count():
    data_query= property_master_query()
    final_query = f"""
        select
            Property_Type,
            count(*) as Type_Count
        from ({data_query}) T
        group by
            Property_Type
    """
    df = execute_query(final_query)
    st.write(f"### Listing By Property Type")
    no_of_listings()
    st.space('xsmall')
    st.bar_chart(
        data=df,
        x='Property_Type',
        y='Type_Count',
        x_label='Property Type',
        y_label='Number of Properties'
    )

def sales_trend():
    data_query = property_master_query()
    final_query = f"""
        select
        case
            when Month(Date_Sold) = 1 then 'Jan'
            when Month(Date_Sold) = 2 then 'Feb'
            when Month(Date_Sold) = 3 then 'Mar'
            when Month(Date_Sold) = 4 then 'Apr'
            when Month(Date_Sold) = 5 then 'May'
            when Month(Date_Sold) = 6 then 'Jun'
            when Month(Date_Sold) = 7 then 'Jul'
            when Month(Date_Sold) = 8 then 'Aug'
            when Month(Date_Sold) = 9 then 'Sep'
            when Month(Date_Sold) = 10 then 'Oct'
            when Month(Date_Sold) = 11 then 'Nov'
            when Month(Date_Sold) = 12 then 'Dec'
        end as Month_Sold,
        DATE_FORMAT(Date_Sold, '%m') as Month_Number,
        Year(Date_Sold) as Year_Sold,
        count(*) as Total_Properties_Sold,
        round(sum(Sale_Price), 2) as Total_Sale_Amount,
        round(avg(Sale_Price), 2) as Avg_Sale_Price,
        min(Sale_Price) as Min_Sale_Price,
        max(Sale_Price) as Max_Sale_Price
        from ({data_query}) T
        where
            Date_Sold is not null
        group by
            Month_Sold,
            Month_Number,
            Year_Sold
        order by
            year_Sold,
            case Month_Sold
                when 'Jan' then 1
                when 'Feb' then 2
                when 'Mar' then 3
                when 'Apr' then 4
                when 'May' then 5
                when 'Jun' then 6
                when 'Jul' then 7
                when 'Aug' then 8
                when 'Sep' then 9
                when 'Oct' then 10
                when 'Nov' then 11
                when 'Dec' then 12
            end; 
    """

    df = execute_query(final_query)
    df['Year_Month'] = df['Year_Sold'].astype(str) + "/" + df['Month_Number'].astype(str)
    df = df.sort_values("Year_Month")
    

    #st.subheader("Sales Dataframe")
    #st.dataframe(df)

    st.subheader("Monthly Sales Revenue")
    sales_revenue = st.line_chart(
        df, 
        x="Year_Month", 
        y='Total_Sale_Amount',
        x_label='Year/Month',
        y_label='Price ($)'
    )

    st.subheader("Monthly Sales Price")
    sales_trent = st.line_chart(
        df, 
        x="Year_Month", 
        y=["Avg_Sale_Price", "Min_Sale_Price", 'Max_Sale_Price'],
        x_label='Year/Month',
        y_label='Price ($)'
    )

def raw_data():
    data_query = property_master_query()
    df = execute_query(data_query)
    st.dataframe(df)

def avg_listing_price_per_city_graph():
    data_query = property_master_query()
    final_query = f"""
        select
            City,
            round(avg(Price), 2)
        from (data_query) T
        group by City,
        Order by CIty
    """
    df = execute_query(final_query)
    st.dataframe(df)