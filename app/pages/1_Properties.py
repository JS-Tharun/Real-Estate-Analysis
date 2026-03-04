import streamlit as st
from components.c_properties import bathroom_filter, property_filter, city_filter, price_filter, agent_filter, from_l_date_filter, to_l_date_filter, property_status_filter, bedroom_filter
from utils.query import property_query

st.set_page_config(
    page_title="Property Listings",
    layout='wide'
)

def main():

    st.header("PROPERTY LISTING")
    # Filter Bar
    with st.container():
        col1, col2, col3 = st.columns([2, 2, 1], border=True)

        with col1:
            st.subheader("Col 1")

        with col2:
            st.subheader("Col 2")

        with col3:
            st.subheader("Filter By")
            property_status_filter()
            city_filter()
            property_filter()
            price_filter()
            from_l_date_filter()
            to_l_date_filter()
            
            st.divider()
            st.write("### Amenities")
            bedroom_filter()
            bathroom_filter()
            agent_filter()

    with st.container():
        st.subheader("Raw Data")
        df = property_query()
        st.dataframe(df)
        
if __name__ == "__main__":
    main()