from altair import Longitude
import streamlit as st
from utils.utils import execute_query
from utils.data import property_master_query

def raw_data():
    data_query = property_master_query()
    df = execute_query(data_query)
    st.dataframe(df)