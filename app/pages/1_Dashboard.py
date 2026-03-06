import streamlit as st
from filters.f_properties import property_sidebar_filter, filter
from tab_components.c_overview import sales_trend, property_type_count
from tab_components.c_pricing_analytics import avg_price_chart, avg_price_per_sqft_chart, avg_price_furnishing_status, avg_price_by_metro_distance, median_price_chart
from tab_components.c_geography import listing_by_city_piechart, map, listing_by_city_barchart, property_distribution_chart_1, property_distribution_chart_2
from tab_components.c_data_tables import raw_data

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

    tab_overview, tab_pricing_analytics, tab_sales_market, tab_geography, tab_agent_performance,  tab_data_tables = st.tabs([
        "Overview", "Pricing Analytics", "Sales & Market", "Geography", "Agent Performance", "Data Tables"
    ])

    with tab_overview:
                
        with st.container():
            col1, col2 = st.columns(2, border=True)
            with col1:
                property_type_count() 
            with col2:
                property_distribution_chart_1()

        with st.container(border=True):
            listing_by_city_barchart()

    with tab_pricing_analytics:
        col1, col2 = st.columns(2, border=True)
        with col1:
            avg_price_chart()
        with col2:
            median_price_chart()
            

        with st.container():
            col1, col2, col3 = st.columns([1, 1, 2], border=True)
            with col1:
                avg_price_per_sqft_chart()

            with col2:
                avg_price_furnishing_status()

            with col3:
                avg_price_by_metro_distance()
                

    with tab_sales_market:
        # Sales Trend
        with st.container(border=True):
            if filter['Property Status'] != 'Unsold':
                sales_trend()
            else:
                st.write("Clear Property Status Filter to view.")

    with tab_geography:
        with st.container():
            col1, col2 = st.columns([2,1], border=True, vertical_alignment='center')
            with col1:
                map()
            with col2:
                listing_by_city_piechart()
                        
        with st.container():
            col1, col2 = st.columns(2, border=True)
            with col1:
                property_distribution_chart_2()
                
            with col2:
                listing_by_city_barchart()            

    with tab_data_tables:
        st.subheader("Raw Data")
        raw_data()
        
        
if __name__ == "__main__":
    main()