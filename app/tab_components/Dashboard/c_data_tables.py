import streamlit as st
from utils.utils import execute_query
from utils.data import property_master_query, agent_master_query, buyer_master_query

def listing_raw_data():
    data_query = property_master_query()
    df = execute_query(data_query)
    st.subheader("Listings Data")
    st.dataframe(df)

def agents_raw_data():
    data_query = agent_master_query()
    df = execute_query(data_query)
    st.subheader("Agents Data")
    st.dataframe(df)

def buyers_raw_data():
    data_query = buyer_master_query()
    df = execute_query(data_query)
    st.subheader("Buyers Data")
    st.dataframe(df)