import streamlit as st
import altair as alt
from utils.utils import execute_query
from utils.data import agent_master_query

def agent_sales_amount_chart():
    data_query = agent_master_query()
    final_query = f"""
        select *
        from
        (select 
        dense_rank() over(
                order by sum(Sale_Price) desc
        ) as Agent_Rank,
        Agent_ID,
        round(sum(Sale_Price), 2) as Total_Sales_Amount 
    from ({data_query}) T
    group by
        Agent_ID) T
    where Agent_Rank between 1 and 10;
    """
    df = execute_query(final_query)
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Agent_ID", title='Agent ID', sort=None),
        y=alt.Y("Total_Sales_Amount", title="Total Amount ($)")
    )
    st.write("Highest Sales Revenue")
    st.caption("Top 10 Agents with the most revenue in sales")
    st.altair_chart(chart, use_container_width=True)

def low_avg_closing_chart():
    query = f"""
        select *
        from
        (select
            dense_rank() over(
                order by Avg_Closing_Days
            ) as Agent_Rank,
            Agent_ID,
            Avg_Closing_Days
        from agents) T
        where Agent_Rank between 1 and 10;
    """
    df = execute_query(query)
    
    chart = alt.Chart(df).mark_bar(color='#D13734').encode(
        x= alt.X("Agent_ID", title="Agent ID", sort=None),
        y= alt.Y("Avg_Closing_Days", title="Days")
    )
    st.write("Avg Closing Days")
    st.caption("Top 10 Agents with Lowest average")
    st.altair_chart(chart, use_container_width=True)

def lowest_closing_table():
    data_query = agent_master_query()
    final_query = f"""
        select 
            Agent_ID,
            Days_On_Market,
            listing_ID,
            Date_Listed,
            Date_Sold
        from ({data_query}) T
        where 
            Days_On_Market = (select min(Days_On_Market) from sales)
        order by 
            l.Date_Listed;
    """
    df = execute_query(final_query)
    st.write("Lowest Closing Day")
    st.caption("Agents Recorded with the Lowest Closing Day")
    st.dataframe(df, width='content')

def exp_deals_corr_chart():
    query = "select Agent_ID, Years_Of_Experience, Deals_Closed from agents"
    df = execute_query(query)
    st.write("Experience Vs Deals Closed")
    st.caption("A scatterplot to map how experience affects the deals closed by an Agent")
    st.scatter_chart(
        data=df,
        x='Years_Of_Experience',
        y='Deals_Closed'
    )

def median_commission_rate():
    data_query = agent_master_query()
    final_query = f"""
        select 
            Agent_ID,
            round(((Commission_Rate / 100) * Sale_Price), 2) as Commission_Earned
        from ({data_query}) T
        where (Commission_Rate / 100) * Sale_Price is not null
        order by Agent_ID;
    """
    df = execute_query(final_query)
    chart = alt.Chart(df).mark_boxplot(extent='min-max').encode(
        alt.X("Agent_ID", sort=None).scale(zero=False),
        alt.Y("Commission_Earned", title='Amount ($)')
    )
    st.write("Commission Earned")
    st.caption("Minimum, Median & Maximum Commission Earned By An Agent")
    st.altair_chart(chart)

def active_listing_chart():
    data_query = agent_master_query()
    final_query = f"""
        select
            
            Agent_ID,
            count(*) as Active_Property_Count
        from ({data_query}) T
        where Date_Sold is not null
        group by
            Agent_ID
        order by Agent_ID;
    """
    df = execute_query(final_query)
    chart = alt.Chart(df).mark_bar(color='#D13734').encode(
        x= alt.X("Agent_ID", title="Agent ID", sort=None),
        y= alt.Y("Active_Property_Count", title="Count")
    )
    st.write("Active Listings")
    st.caption("Amount of active listings each agent has")
    st.altair_chart(chart, use_container_width=True)

