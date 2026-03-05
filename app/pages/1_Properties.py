import streamlit as st
from filters.f_properties import property_sidebar_filter, filter
from utils.query import property_master_query
from utils.utils import execute_query
from components.c_properties import map, average_price_chart, no_of_listings, property_distribution_chart, sales_trend, property_type_count

st.set_page_config(
    page_title="Property Listings",
    layout='wide'
)

def main():
    
    # Filter Sidebar Bar
    property_sidebar_filter()

    st.header("PROPERTY LISTING")
    
    # Sales Trend
    with st.container(border=True):
        if filter['Property Status'] != 'Unsold':
            sales_trend()
            
    with st.container():
        col1, col2 = st.columns(2, border=True)
        with col1:
            property_type_count()    
        with col2:
            average_price_chart()            

    with st.container():
        col1, col2 = st.columns(2, border=True)
        with col1:
            property_distribution_chart()
        with col2:
            map()

    st.subheader("Raw Data")
    data_query = property_master_query()
    df = execute_query(data_query)
    st.dataframe(df)

    

    
    
    
        
        
if __name__ == "__main__":
    main()