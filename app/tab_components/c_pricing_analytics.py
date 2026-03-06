import streamlit as st
from utils.utils import execute_query
from utils.query import property_master_query

def median_price_chart():
    data_query = property_master_query()
    final_query = f"""
        select
            City,
            round(avg(Listed_Price), 2) as Median_Price
        from
            (select
                City,
                Listed_Price,
                row_number() over (
                    partition by city
                    order by Listed_Price
                ) as Row_Num,
                count(*) over (
                    partition by city
                ) as Total_Count
            from ({data_query}) T1) T2
        where row_num in (
            Floor((Total_Count + 1) / 2),
            Floor((Total_Count + 2) / 2)
        )
        group by
            City
        order by
            City
    """

    df = execute_query(final_query)
    st.write("Median Price Based on City")
    st.bar_chart(
        data=df,
        x='City',
        y='Median_Price',
        y_label='Price ($)'
    )


def avg_price_chart():

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
  st.write("Listing Price By City")
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

def avg_price_per_sqft_chart():
    data_query = property_master_query()
    final_query = f"""
        select
            Property_Type,
            round(avg(Price_Per_Sqft), 2) as Avg_Price_Per_Sqft
        from
            (select
            Property_Type,
            (Listed_Price/sqft) as Price_Per_Sqft
            from 
                ({data_query})T1
            ) T2
        group by
            Property_Type
        order by
            Avg_Price_Per_Sqft
    """
    df = execute_query(final_query)
    st.write("Avg Price-Per-Sqft Based on Property Type")
    st.bar_chart(
        data=df,
        x='Property_Type',
        y='Avg_Price_Per_Sqft',
        x_label='Property Type',
        y_label='Price ($)'
    )

def avg_price_furnishing_status():
    data_query = property_master_query()
    final_query = f"""
        select 
            Furnishing_Status,
            count(*) as Total_Properties,
            round(avg(Listed_Price), 2) as Avg_Price
        from
            ({data_query}) T
        group by
            Furnishing_Status
        order by
            Avg_Price
    """
    df = execute_query(final_query)
    st.write("Avg Price Based on Furnishing Status")
    st.bar_chart(
        data=df,
        x='Furnishing_Status',
        y='Avg_Price',
        x_label='Furnishing Status',
        y_label='Price ($)'
    )

def avg_price_by_metro_distance():
    data_query = property_master_query()
    final_query = f"""
        select
            CASE
                when Metro_Distance <= 2 then '0 - 02'
                when Metro_Distance <= 5 && Metro_Distance > 2 then '02 - 05'
                when Metro_Distance <= 10 && Metro_Distance > 5 then '05 - 10'
                when Metro_Distance <= 15 && Metro_Distance > 10 then '10 - 15'
                else '15+'
            END AS Metro_Distance_In_KM,
            ROUND(AVG(Listed_Price), 2) AS Avg_Price
        from ({data_query}) T
        GROUP BY 
            Metro_Distance_In_KM
        ORDER BY 
            case Metro_Distance_In_KM
                when '0 - 02' then 1
                when '02 - 05' then 2
                when '05 - 10' then 3
                when '10 - 15' then 4
                when '15+' then 5
            end;
    """
    df = execute_query(final_query)
    st.write("Avg Price by Metro Distance")
    st.bar_chart(
        data=df,
        x='Metro_Distance_In_KM',
        y='Avg_Price',
        x_label='Distance From Nearest Metro Station (KM)',
        y_label='Price'
    )