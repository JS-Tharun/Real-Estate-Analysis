import streamlit as st
from utils.filters import property_sidebar_filter, filter
from tab_components.Dashboard.c_overview import property_type_count
from tab_components.Dashboard.c_pricing_analytics import avg_price_chart, avg_price_per_sqft_chart, avg_price_furnishing_status, avg_price_by_metro_distance, median_price_chart, price_bucket_chart
from tab_components.Dashboard.c_geography import listing_by_city_piechart, map, listing_by_city_barchart, property_distribution_chart_1, property_distribution_chart_2
from tab_components.Dashboard.c_data_tables import listing_raw_data, agents_raw_data, buyers_raw_data
from tab_components.Dashboard.c_sales_market import monthly_sales_price, monthly_sales_revenue, sale_above_listed_per, monthly_sales_count, sale_to_list_price_chart, avg_days_on_market_chart
from tab_components.Dashboard.c_agent_performance import agent_sales_amount_chart, low_avg_closing_chart, lowest_closing_table, exp_deals_corr_chart, median_commission_rate, active_listing_chart
from tab_components.Dashboard.c_buyer_insights import investor_enduser_per_chart, loan_uptake_rate_chart, loan_amount_chart, payment_method_chart

st.set_page_config(
    page_title="Property Analysis",
    layout='wide'
)
    
# Filter Sidebar Bar
with st.sidebar:
    property_sidebar_filter()

st.write("# Real Estate Analytics Dashboard 📊")
st.caption("This dashboard provides visual insights into real estate market activity using interactive charts and maps.")
st.caption("Users can filter the dataset to analyze specific segments of the market and uncover trends related to pricing, property types, and sales performance.")
st.caption("***Note***: Filters do not apply on Agent Performance.")
tab_overview, tab_pricing_analytics, tab_sales_market, tab_geography, tab_agent_performance, tab_buyer, tab_data_tables = st.tabs([
    "Overview", "Pricing Analytics", "Sales & Market", "Geography", "Agent Performance", "Buyer Insights", "Data Tables"
])

with tab_overview:
    with st.container():
        col1, col2 = st.columns(2, border=True)
        with col1:
                listing_by_city_barchart()
        with col2:
            property_distribution_chart_1()

    with st.container():
        col1, col2 = st.columns(2, border=True)

        with col1:
            monthly_sales_revenue()

        with col2:
            property_type_count()
            
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
        with st.container():
            col1, col2 = st.columns(2, border=True)
            with col1:
                monthly_sales_revenue()
            with col2:
                monthly_sales_count() 
            

        with st.container():
            col1, col2 = st.columns(2, border=True)
            with col1:
                monthly_sales_price()  

            with col2:
                sale_above_listed_per()


        with st.container():
            col1, col2 = st.columns(2, border=True)

            with col1:
                avg_days_on_market_chart()            

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

with tab_agent_performance:
    with st.container():
        col1, col2 = st.columns(2, border=True)
        with col1:
            agent_sales_amount_chart()
        with col2:
            exp_deals_corr_chart()

    with st.container():
        col1, col2 = st.columns(2, border=True)
        with col1:
            low_avg_closing_chart()
        with col2:
            lowest_closing_table()
    
    with st.container(border=True):
        median_commission_rate()

    with st.container(border=True):
        active_listing_chart()
    
with tab_buyer:

    with st.container():
        col1, col2 = st.columns(2, border=True)

        with col1:
            loan_uptake_rate_chart()           

        with col2:
            loan_amount_chart()

    with st.container():
        col1, col2 = st.columns(2, border=True)

        with col1:
            investor_enduser_per_chart()

        with col2:
            payment_method_chart()

with tab_data_tables:
    with st.container(border=True):
        listing_raw_data()

    with st.container(border=True):
        agents_raw_data()

    with st.container(border=True):
        buyers_raw_data()
        
        
