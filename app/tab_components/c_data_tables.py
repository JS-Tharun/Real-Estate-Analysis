from altair import Longitude
import streamlit as st
from utils.utils import execute_query
from utils.query import property_master_query
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

def raw_data():
    data_query = property_master_query()
    df = execute_query(data_query)
    st.dataframe(df)