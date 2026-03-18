import streamlit as st
import pandas as pd
from utils.utils import execute_query, execute_insert
from tab_components.Database.c_insert import listing_id_exists

st.write("# Database")

tab_read, tab_insert, tab_update, tab_delete = st.tabs([
    "Read Data", "Insert Data", "Update Data", "Delete Data"
])

with tab_read:
    with st.container(border=True):
        def read_table(table_name):
            if table_name != None:
                query = f"select * from {table_name}"
                df = execute_query(query)
                st.dataframe(df)

        options = {
            'Sold Properties' : 'sales',
            'Agents': 'agents',
            'Buyers' : 'buyers',
            'Listed Properties' : 'listings',
            'Property Attributes': 'property_attributes'
        }

        table = st.selectbox(
            "Select Table",
            ["agents", "listings", "sales", "property_attributes", "buyers"],
            index=None,
            placeholder='Choose a table to read',
            key='read_table'
        )
        st.write("Result Table")
        if table != None:
            read_table(table)
        else:
            st.caption("No Table Selected")

with tab_insert:
    with st.container():

        table = st.selectbox(
            "Select Table",
            ["agents", "listings", "sales", "property_attributes", "buyers"],
            index=None,
            placeholder='Choose a table to insert data in',
            key='insert_table'
        )

        if table == 'agents':

            st.write("Fill the Agent Details")
            with st.form('add_agent'):
                id = st.text_input("Agent ID", placeholder="Eg. A1234")
                email = st.text_input("Email", placeholder="agentid@gmail.com")
                phone = st.text_input("Phone", placeholder='10 Digit number', max_chars=10)
                commission_rate = st.slider("Commission Rate", min_value=0.00,  max_value=50.00, format='%0.2f')
                deals_closed = st.number_input("Deals Closed", step=1)
                rating = st.slider("Rating", min_value=0.0, max_value=5.0, format="%0.1f")
                years_of_experience = st.number_input("Years of Experience", min_value=0)
                avg_closing_days = st.number_input("Average Closing Days", min_value=0)

                submit = st.form_submit_button("Add Agent")
                if submit:
                    query = """
                        Insert into agents
                        (Agent_ID, Email, Phone, Commission_Rate, Deals_Closed, Rating, Years_Of_Experience, Avg_Closing_Days)
                        values (%s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    values = (
                                id,
                                email,
                                phone,
                                commission_rate,
                                deals_closed,
                                rating,
                                years_of_experience,
                                avg_closing_days
                            )

                    success, error = execute_insert(query, values)

                    if success:
                        st.success("Agent Inserted Successfully")
                    else:
                        st.error(f"Insert Failed: {error}")

        if table == 'listings':
            st.write("Fill the Property Listing Details")
            with st.form("add_listing"):
                listing_id = st.text_input("Listing ID", placeholder='Eg: L00001')
                agent_id = st.selectbox(
                    label='Agent ID',
                    options=list(execute_query("select distinct Agent_ID from agents")['Agent_ID'])
                )
                submit = st.form_submit_button("Submit")

                if submit:
                    if listing_id_exists(listing_id):
                        st.error("❌ Listing ID already exists")


