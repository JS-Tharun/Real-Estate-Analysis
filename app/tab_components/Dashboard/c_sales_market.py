import streamlit as st
import plotly.express as px
from utils.utils import execute_query
from utils.data import property_master_query


def monthly_sales_revenue():
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

    st.write("Monthly Sales Revenue")
    monthly_sales_revenue = st.line_chart(
        df, 
        x="Year_Month", 
        y='Total_Sale_Amount',
        x_label='Year/Month',
        y_label='Price ($)'
    )

def monthly_sales_price():
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

    st.write("Monthly Sales Price")
    monthly_sales_price = st.line_chart(
        df, 
        x="Year_Month", 
        y=["Avg_Sale_Price", "Min_Sale_Price", 'Max_Sale_Price'],
        x_label='Year/Month',
        y_label='Price ($)',
        height='content'
    )

def monthly_sales_count():
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
        count(*) as Total_Properties_Sold
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

    st.write("Monthly Sales Count")
    monthly_sales_count = st.line_chart(
        df, 
        x="Year_Month", 
        y="Total_Properties_Sold",
        x_label='Year/Month',
        y_label='Count',
        color='#D13734'
    )


def sale_above_listed_per():
    data_query = property_master_query()
    final_query = f"""
        select
            case
                when Sale_Price > Listed_Price then 'Above Listed Price'
                when Sale_Price <= Listed_Price then 'Equal and Below Listed Price'
            end as Property_Sold_At,
            count(*) as Property_Count,
            round(100 * count(*) / (select count(*) from ({data_query}) T1 where Sale_Price is not null)) as Percentage
        from ({data_query}) T2
        where Sale_Price is not null
        group by
            Property_Sold_At
    """
    df = execute_query(final_query)
    st.write("Sale Price Relative to Listing Price")
    fig = px.pie(df, values="Percentage", names="Property_Sold_At")
    st.plotly_chart(fig, key='sales', width='content', height='content')

def sale_to_list_price_chart():
    data_query = property_master_query()
    final_query = f"""
        select
            city,
            round(avg(ratio), 4) as Sale_To_List_Price_Ratio
        from
        (select
            City,
            Listed_Price,
            Sale_Price,
            (Sale_Price/Listed_Price) as ratio
        from ({data_query}) T1
        where Sale_Price is not null) T2
        group by
            City;
    """
    df = execute_query(final_query)
    st.write("Sale to List Price Ratio Based on City")
    st.bar_chart(
        data=df,
        x='City',
        y='Sale_To_List_Price_Ratio',
        y_label='Ratio',
        height='content'
    )

def avg_days_on_market_chart():
    data_query = property_master_query()
    final_query = f"""
        select
            City,
            round(avg(Days_On_Market), 0) as Avg_Days_On_Market
        from ({data_query}) T
        group by
            l.City
        order by
            City;
    """
    df = execute_query(final_query)
    st.write("Avg Days On Market By City")
    st.bar_chart(
        data=df,
        x='City',
        y='Avg_Days_On_Market',
        y_label='Days'
    )