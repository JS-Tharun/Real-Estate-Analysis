import streamlit as st
from components import render_sidebar, render_dataframe, render_map

# Filter Sidebar
render_sidebar()

# Streamlit UI
st.title("Real Estate Analysis Dashboard")

# Dataframe
render_dataframe()

# Map
render_map()

