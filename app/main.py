import streamlit as st
from filters import render_sidebar, render_filter_dataframe

# Filter Sidebar
render_sidebar()

# Streamlit UI
st.title("Real Estate Analysis Dashboard")

# Filter result
render_filter_dataframe()




