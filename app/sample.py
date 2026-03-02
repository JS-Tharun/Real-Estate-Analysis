from utils import execute_query
import streamlit as st

st.title("Hello")

filter = {}

def agent_filter():
  selected_agent = st.sidebar.selectbox(
    "Agent ID", ['All'] + list(execute_query("select distinct Agent_ID from agents")['Agent_ID'])
  )
  filter['Agent'] = selected_agent



  
agent_filter()

print(filter['Agent'])