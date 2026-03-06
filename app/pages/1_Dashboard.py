import streamlit as st
from filters.f_properties import property_sidebar_filter, filter
from tab_components.c_overview import property_distribution_chart, sales_trend, property_type_count, raw_data
from tab_components.c_pricing_analytics import average_price_chart
from tab_components.c_geography import listing_by_city_piechart, map, listing_by_city_barchart

st.set_page_config(
    page_title="Analytics Dashboard",
    layout='wide'
)

def main():
    
    # Filter Sidebar Bar
    property_sidebar_filter()

    st.write("# Property Analytics Dashboard")
    st.markdown("""
        * Track listing performance, pricing trends, sales velocity, and agent effectiveness. 

        * Use the sidebar filters to focus on specific cities, price bands, property types, or agents. 

        ***Note***: All numbers and charts below are based on the filtered dataset."""
    )
    st.divider()

    tab_overview, tab_pricing_analytics, tab_sales_market, tab_agent_performance, tab_geography, tab_data_tables = st.tabs([
        "Overview", "Pricing Analytics", "Sales & Market", "Agent Performance", "Geography", "Data Tables"
    ])

    with tab_overview:
                
        with st.container():
            col1, col2 = st.columns(2, border=True)
            with col1:
                property_type_count() 
            with col2:
                property_distribution_chart()

        with st.container(border=True):
            listing_by_city_barchart()

    with tab_pricing_analytics:
        average_price_chart()

    with tab_sales_market:
        # Sales Trend
        with st.container(border=True):
            if filter['Property Status'] != 'Unsold':
                sales_trend()

    with tab_geography:
        with st.container(border=True):
             map()
        
        with st.container():
            col1, col2 = st.columns(2, border=True)
            with col1:
                listing_by_city_barchart()
            with col2:
                listing_by_city_piechart()


    with tab_data_tables:
        st.subheader("Raw Data")
        raw_data()
        
        
if __name__ == "__main__":
    main()