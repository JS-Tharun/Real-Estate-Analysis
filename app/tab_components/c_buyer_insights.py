from pandas.io.sql import execute
import streamlit as st
import altair as alt
import plotly.express as px
from utils.utils import execute_query
from utils.data import buyer_master_query
from utils.filters import filter


def investor_enduser_per_chart():
    data_query = buyer_master_query()
    final_query = f"""
        select 
            Buyer_Type,
            round((100 * count(*) / (select count(*) from ({data_query})T1)), 2) as Percentage
        from ({data_query}) T2
        group by
            Buyer_Type;
    """
    df = execute_query(final_query)
    fig = px.pie(df, values="Percentage", names='Buyer_Type')
    st.write("Buyer Type Distribution")
    st.caption("Shows the percentage of end users and investors who have bought the properties so far.")
    st.plotly_chart(fig)

def loan_uptake_rate_chart():
    data_query = buyer_master_query()
    final_query = f"""
        select
            dense_rank() OVER(
                ORDER BY round((100 * (T1.Count) / T2.Total_Buyers), 2) desc
            ) as City_Rank,
            T1.City,
            T1.Count,
            round((100 * (T1.Count) / T2.Total_Buyers), 2) as Percentage
        from

        (select 
            City,
            Loan_Taken,
            count(Loan_Taken) as Count
        from 
            ({data_query}) T
        group by
            City,
            Loan_Taken) T1
        inner join 
        (select
            City,
            count(*) as Total_Buyers
        from 
            ({data_query}) T
        group by
            City)T2
        on T1.City = T2.City
        where Loan_Taken = True;
    """
    df = execute_query(final_query)
    chart = alt.Chart(df).mark_bar().encode(
        x='City',
        y='Percentage',
        tooltip=['City','Percentage','Count']
    )
    st.write("Loan Uptake Percentage")
    st.caption("Shows the percentage of buyers who take loan")
    st.altair_chart(chart, use_container_width=True)

def loan_amount_chart():
    data_query = buyer_master_query()
    final_query = f"""
        select
            Buyer_Type,
            round(avg(Loan_Amount), 2) as Avg_Loan_Amount
        from ({data_query}) T
        where loan_taken = True
        group by
            Buyer_Type;
    """
    df = execute_query(final_query)
    st.write("Average Loan Amount")
    st.caption("Average Loan Amount Taken Based on Buyer Type")
    st.bar_chart(
        data=df,
        x='Buyer_Type',
        y='Avg_Loan_Amount',
        x_label='Buyer Type',
        y_label="Amount ($)"
    )

def payment_method_chart():
    data_query = buyer_master_query()
    final_query = f"""
        select
            dense_rank() over(
                order by (100 * count(*) / (select count(*) from ({data_query})T)) desc
            ) as Payment_Method_Rank,
            Payment_Method,
            count(*) as Count,
            round((100 * count(*) / (select count(*) from ({data_query})T)), 2) as Percentage
        from ({data_query})T
        group by
            Payment_Method;
    """
    df = execute_query(final_query)
    fig = px.pie(df, values="Percentage", names='Payment_Method')
    st.write("Payment Method Distribution")
    st.caption("Shows the payment methods used by buyers")
    st.plotly_chart(fig)
