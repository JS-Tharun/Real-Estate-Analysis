import streamlit as st
from components import render_sidebar, render_dataframe, render_map, render_bar_chart, render_pie_chart

# Filter Sidebar
render_sidebar()

# Streamlit UI
st.title("Real Estate Analysis Dashboard")

# Dataframe
render_dataframe()

# Map
render_map()

# Bar chart
render_bar_chart()

# Pie Chart
render_pie_chart()

