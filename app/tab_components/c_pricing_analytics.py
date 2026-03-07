import streamlit as st
from utils.utils import execute_query
from utils.data import property_master_query
import altair as alt

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
        y_label='Price ($)',
        color='#6635f8'
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
  st.write("Average Listing Price By City")
  avg_price()
  st.bar_chart(
    data=df,
    x='City', 
    x_label="City",
    y='Average_Price', 
    y_label="Price ($)",
    color='#6ce57f'
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
        y_label='Price ($)',
        color='#6ce57f'
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
        y_label='Price ($)',
        color='#6ce57f'
    )

def avg_price_by_metro_distance():
    data_query = property_master_query()
    final_query = f"""
        select
            CASE
                when Metro_Distance <= 2 then '0 - 2'
                when Metro_Distance <= 5 && Metro_Distance > 2 then '2 - 5'
                when Metro_Distance <= 10 && Metro_Distance > 5 then '5 - 10'
                when Metro_Distance <= 15 && Metro_Distance > 10 then '10 - 15'
                else '15+'
            END AS Metro_Distance_In_KM,
            ROUND(AVG(Listed_Price), 2) AS Avg_Price
        from ({data_query}) T
        GROUP BY 
            Metro_Distance_In_KM
        ORDER BY 
            case Metro_Distance_In_KM
                when '0 - 2' then 1
                when '2 - 5' then 2
                when '5 - 10' then 3
                when '10 - 15' then 4
                when '15+' then 5
            end;
    """
    df = execute_query(final_query)
    st.write("Avg Price by Metro Distance")

    chart = alt.Chart(df).mark_bar(color="#6ce57f").encode(
        x=alt.X("Metro_Distance_In_KM", title="Distance from Nearest Station (KM)", sort=None),
        y=alt.Y('Avg_Price', title="Price ($)")
    )
    st.altair_chart(chart, use_container_width=True)

def price_bucket_chart():
    data_query = property_master_query()
    final_query = f"""
        select 
            CASE
                WHEN Listed_Price < 250000 THEN '100K - 250K'
                WHEN Listed_Price < 500000 THEN '250K - 500K'
                WHEN Listed_Price < 750000 THEN '500K - 750K'
                WHEN Listed_Price < 1000000 THEN '750K - 1M'
                WHEN Listed_Price < 1500000 THEN '1M - 1.5M'
                WHEN Listed_Price < 2000000 THEN '1.5M - 2M'
                WHEN Listed_Price < 2500000 THEN '2M - 2.5M'
                WHEN Listed_Price < 3000000 THEN '2.5M - 3M'
                WHEN Listed_Price < 3500000 THEN '3M - 3.5M'
                WHEN Listed_Price < 4000000 THEN '3.5M - 4M'
                WHEN Listed_Price < 4500000 THEN '4M - 4.5M'
                WHEN Listed_Price < 5000000 THEN '4.5M - 5M'
                ELSE '5M and above'
            END AS Price_Bucket,
            count(*) as Total_Properties
        from ({data_query}) T
        group by Price_Bucket
        ORDER BY
            CASE Price_Bucket
                WHEN '100K - 250K' THEN 1
                WHEN '250K - 500K' THEN 2
                WHEN '500K - 750K' THEN 3
                WHEN '750K - 1M' THEN 4
                WHEN '1M - 1.5M' THEN 5
                WHEN '1.5M - 2M' THEN 6
                WHEN '2M - 2.5M' THEN 7
                WHEN '2.5M - 3M' THEN 8
                WHEN '3M - 3.5M' THEN 9
                WHEN '3.5M - 4M' THEN 10
                WHEN '4M - 4.5M' THEN 11
                WHEN '4.5M - 5M' THEN 12
                WHEN '5M and above' THEN 13
            END;
    """

    df = execute_query(final_query)
    st.write("Property Count by Price")
    chart = alt.Chart(df).mark_bar(color="#D13734").encode(
        x=alt.X("Price_Bucket", title="Price Bucket", sort=None),
        y=alt.Y('Total_Properties', title="Count")
    )
    st.altair_chart(chart, use_container_width=True)
