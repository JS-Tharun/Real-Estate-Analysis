import streamlit as st
from components.properties import property_filter, city_filter, price_filter, agent_filter, from_l_date_filter, to_l_date_filter
from utils import execute_query

st.set_page_config(
    page_title="Property Listings",
    layout='wide'
)

st.header("Property Listing")

# Filter Bar
with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Col 1")

    with col2:
        st.write("Col 2")

    with col3:
        st.write("### Filter By")
        city_filter()
        property_filter()
        price_filter()
        agent_filter()
        from_l_date_filter()
        to_l_date_filter()

        selected_property_status = st.selectbox(
            "Property Status",
            options=['All', 'Sold', 'Unsold']
        )

        st.write(f"{selected_property_status}")
        