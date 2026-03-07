import streamlit as st
from utils.utils import execute_query
from utils.query import property_master_query


def no_of_listings():
    data_query = property_master_query()
    Total_Properties = int(list(execute_query(f"select count(*) from ({data_query})T")['count(*)'])[0])
    st.write(f"Total - {Total_Properties}")



def property_type_count():
    data_query= property_master_query()
    final_query = f"""
        select
            Property_Type,
            count(*) as Type_Count
        from ({data_query}) T
        group by
            Property_Type
    """
    df = execute_query(final_query)
    st.write(f"### Listing By Property Type")
    no_of_listings()
    st.space('xsmall')
    st.bar_chart(
        data=df,
        x='Property_Type',
        y='Type_Count',
        x_label='Property Type',
        y_label='Number of Properties'
    )