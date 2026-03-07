import streamlit as st
from streamlit.elements.lib.layout_utils import Height
from utils.filters import property_sidebar_filter, filter
from tab_components.c_overview import property_type_count
from tab_components.c_pricing_analytics import avg_price_chart, avg_price_per_sqft_chart, avg_price_furnishing_status, avg_price_by_metro_distance, median_price_chart, price_bucket_chart
from tab_components.c_geography import listing_by_city_piechart, map, listing_by_city_barchart, property_distribution_chart_1, property_distribution_chart_2
from tab_components.c_data_tables import raw_data
from tab_components.c_sales_market import monthly_sales_price, monthly_sales_revenue, sale_above_listed_per, monthly_sales_count, sale_to_list_price_chart

st.set_page_config(
    page_title="Analytics Dashboard",
    layout='wide'
)

def main():
    
    # Filter Sidebar Bar
    with st.sidebar:
        property_sidebar_filter()

    st.write("# Property Analytics Dashboard")
    st.caption("***Note***: All numbers and charts below are based on the filtered dataset.")
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

        with st.container():
            col1, col2 = st.columns([2, 1], border=True)

            with col1:
                monthly_sales_revenue()

            with col2:
                listing_by_city_barchart()

        
    with tab_pricing_analytics:
        with st.container():
            col1, col2 = st.columns([2, 1], border=True)
            with col1:
                price_bucket_chart()
            with col2:
                avg_price_furnishing_status()
        
        with st.container():
            col1, col2 = st.columns([2, 1], border=True)
            with col1:
                avg_price_by_metro_distance()

            with col2:
                median_price_chart()                

        with st.container():
            col1, col2 = st.columns([2, 1], border=True)
            with col1:
                avg_price_chart()
        
            with col2:
                avg_price_per_sqft_chart()
              

    with tab_sales_market:
        if filter['Property Status'] != 'Unsold':
        # Sales Trend
            with st.container(border=True, height=400):
                monthly_sales_revenue()

            with st.container(border=True, height=400):
                monthly_sales_count() 

            with st.container(border=True, height=390):
                monthly_sales_price()  

            with st.container(height=450):
                col1, col2 = st.columns(2, border=True)

                with col1:
                    sale_above_listed_per()

                with col2:
                    sale_to_list_price_chart()
                                
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