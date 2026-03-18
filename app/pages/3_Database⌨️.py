import streamlit as st
import pandas as pd
import datetime
from utils.utils import execute_query, execute_insert, get_connection
from tab_components.Database.c_insert import listing_id_exists, generate_listing_id, generate_agent_id

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
            label="Select Table",
            options=["agents", "listings", "sales", "property_attributes", "buyers"],
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
            with st.form('add_agent', enter_to_submit=False):
                st.write("Fill the Agent Details")
                agent_id = generate_agent_id()
                email = st.text_input("Email", placeholder="agentid@gmail.com")
                phone = st.text_input("Phone", placeholder='10 Digit number', max_chars=10)
                commission_rate = st.slider("Commission Rate", min_value=0.00,  max_value=50.00, format='%0.2f')
                deals_closed = st.number_input("Deals Closed", step=1)
                rating = st.slider("Rating", min_value=0.0, max_value=5.0, format="%0.1f")
                years_of_experience = st.number_input("Years of Experience", min_value=0)
                avg_closing_days = st.number_input("Average Closing Days", min_value=0)

                submit = st.form_submit_button("Submit")
                if submit:
                    if email and phone:
                        query = """
                            Insert into agents
                            (Agent_ID, Email, Phone, Commission_Rate, Deals_Closed, Rating, Years_Of_Experience, Avg_Closing_Days)
                            values (%s, %s, %s, %s, %s, %s, %s, %s)
                        """

                        values = (
                            agent_id,
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

                    else:
                        st.warning("Enter email and phone number")

        if table == 'listings':            
            with st.form("add_listing", enter_to_submit=False):
                st.write("Fill the Property Listing Details")
                listing_id = generate_listing_id()
                agent_id = st.selectbox(
                    label='Agent ID',
                    options=list(execute_query("select distinct Agent_ID from agents")['Agent_ID']),
                    index=None
                )
                city = st.selectbox(
                    label='City',
                    options=list(execute_query('select distinct City from listings')['City']),
                    index=None,
                    placeholder='Select City'
                )
                property_type = st.selectbox(
                    label='Property Type',
                    options=list(execute_query("select distinct property_type from listings")['property_type']),
                    index=None,
                    placeholder='Select Property Type'
                )
                price = st.number_input(
                    label='Listed Price ($)',
                    min_value=0
                )
                sqft = st.number_input(
                    label='Property Area in Sqft',
                    min_value=0
                )
                date_listed = st.date_input(
                    label='Listed Date',
                    min_value= datetime.date(2023, 1, 1),
                    max_value='today'
                )
                latitude = st.number_input(
                    label='Latitude'
                )
                longitude = st.number_input(
                    label='Longitude'
                )
                submit = st.form_submit_button("Submit")

                if submit:
                    if listing_id and agent_id:
                        query = """
                            Insert into listings
                            (Listing_ID, City, Property_Type, Price, Sqft, Date_Listed, Agent_ID, Latitude, longitude)
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """

                        values = (
                            listing_id,
                            city,
                            property_type,
                            price,
                            sqft,
                            date_listed,
                            agent_id,
                            latitude,
                            longitude
                        )

                        success, error = execute_insert(query, values)

                        if success:
                            st.success("Property Listed Successfully")
                        else:
                            st.error(f"Insert Failed: {error}")

                    else:
                        st.warning("Select Listing ID and Agent ID")

        if table == 'sales':
            with st.form("Sales"):
                listing_query = f"""
                    select l.listing_id
                    from listings l
                    left join sales s
                    on l.listing_id = s.listing_id
                    where Date_Sold is null;
                """
                listing_id_values = list(execute_query(listing_query)['listing_id'])
                listing_id = st.selectbox(
                    label='Listing_ID',
                    options=listing_id_values,
                    index=None,
                    placeholder='Select the Property Listing ID'
                )

                sale_price = st.number_input(
                    label='Sale Price ($)',
                    min_value=0
                )

                date_sold = st.date_input(
                    label='Date Sold',
                    max_value='today'
                )

                days_on_market = st.number_input(
                    'Days on Market',
                    min_value=0
                )

                submit = st.form_submit_button("Submit")

                if submit:
                    if listing_id:
                        query = """
                            Insert into sales
                            (Listing_ID, Sale_Price, Date_Sold, Days_On_Market)
                            values (%s, %s, %s, %s)
                        """

                        values = (
                            listing_id,
                            sale_price,
                            date_sold,
                            days_on_market
                        )

                        success, error = execute_insert(query, values)

                        if success:
                            st.success("Added to Sold Properties Successfully")
                        else:
                            st.error(f"Insert Failed: {error}")

                    else:
                        st.warning("Select Listing ID before submitting")

        if table == 'property_attributes':
            with st.form("Property Attributes"):

                binary_values = {
                    'Yes': True,
                    'No': False
                }

                listing_query = """
                    select l.Listing_ID from listings l
                    left join property_attributes p
                    on l.Listing_ID = p.Listing_ID
                    where attribute_id is null;
                """
                listing_id_val = list(execute_query(listing_query)['Listing_ID'])
                listing_id = st.selectbox(
                    label='Listing ID',
                    options=listing_id_val,
                    index=None,
                    placeholder='Select the Property Listing ID'
                )
                bathroom = st.number_input(
                    label='Bathroom Count',
                    min_value=0
                )
                bedroom = st.number_input(
                    label='Bedroom Count',
                    min_value=0
                )
                floor_number = st.number_input(
                    label='Floor Number',
                    min_value=0
                )
                total_floor = st.number_input(
                    label='Total Floors',
                    min_value=0
                )
                selected_year_built = st.date_input(
                    label='Year Built'
                )
                year_built = selected_year_built.year

                selected_is_rented = st.selectbox(
                    label='Is Rented',
                    options=['Yes', 'No']
                )

                is_rented = binary_values[str(selected_is_rented)]
                
                tenant_count = st.number_input(
                    label='Tenant Count',
                    min_value=0
                )

                furnishing_status = st.selectbox(
                    label='Furnishing Status',
                    options=list(execute_query('select distinct furnishing_status from property_attributes')['furnishing_status']),
                    index=None,
                    placeholder='Select the furnishing Status'
                )

                metro_distance = st.number_input(
                    label='Distance from Nearest Metro Station',
                    min_value=0.00
                )

                selected_parking_available = st.selectbox(
                    label='Parking Availability',
                    options=['Yes','No']
                )

                parking_available = binary_values[str(selected_parking_available)]

                selected_power_backup = st.selectbox(
                    label='Power Backup Availability',
                    options=['Yes','No']
                )

                power_backup = binary_values[str(selected_power_backup)]

                submit = st.form_submit_button("Submit")

                if submit:
                    if listing_id:
                        query = """
                            Insert into property_attributes
                            (Listing_ID, Bedroom, Bathroom, Floor_Number, Total_Floor, Year_Built, Is_Rented, Tenant_Count, Furnishing_Status, Metro_Distance, Parking_Available, Power_Backup)
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """

                        values = (
                            listing_id,
                            bedroom,
                            bathroom,
                            floor_number,
                            total_floor,
                            year_built,
                            is_rented,
                            tenant_count,
                            furnishing_status,
                            metro_distance,
                            parking_available,
                            power_backup
                        )

                        success, error = execute_insert(query, values)

                        if success:
                            st.success("Added to Sold Properties Successfully")
                        else:
                            st.error(f"Insert Failed: {error}")

                    else:
                        st.warning("Select the Listing ID before submitting")


        if table == 'buyers':
            with st.container(border=True):
                st.write("Fill the Buyer Details")
                binary_values = {
                        'Yes': True,
                        'No': False
                    }
                selected_loan_taken = st.selectbox(
                    label='Loan Taken',
                    options=['Yes','No'] 
                )

                loan_taken = binary_values[str(selected_loan_taken)]

                if loan_taken:
                    loan_provider = st.selectbox(
                        label='Loan Provider',
                        options= list(execute_query('select distinct Loan_Provider from buyers')['Loan_Provider'])

                    )

                    loan_amount = st.number_input(
                        label='Loan Amount',
                        min_value=0
                    )

                with st.form("Buyers", border=False):

                    listing_id = st.selectbox(
                        label='Listing ID',
                        options=list(execute_query('select distinct Listing_ID from listings')['Listing_ID']),
                        index=None
                    )

                    buyer_type = st.selectbox(
                        label='Buyer Type',
                        options=list(execute_query('select distinct Buyer_Type from buyers')['Buyer_Type']),
                        index=None
                    )

                    payment_method = st.selectbox(
                        label='Payment Method',
                        options=list(execute_query('select distinct Payment_Method from buyers')['Payment_Method']),
                        index=None
                    )

                    submit = st.form_submit_button("Submit")

                    if submit:
                        if listing_id:
                            query = """
                                Insert into buyers
                                (Listing_ID, Buyer_Type, Payment_Method, Loan_Taken, Loan_Provider, Loan_Amount)
                                values (%s, %s, %s, %s, %s, %s)
                            """

                            values = (
                                listing_id,
                                buyer_type,
                                payment_method,
                                loan_taken,
                                loan_provider if loan_taken else 'NA',
                                loan_amount if loan_taken else 0
                            )

                            success, error = execute_insert(query, values)

                            if success:
                                st.success("Buyer Data Inserted")
                            else:
                                st.error(f"Insert Failed: {error}")

                        else:
                            st.warning('Select the Listing ID before submitting')



