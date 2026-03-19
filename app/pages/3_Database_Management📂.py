import streamlit as st
import datetime
from utils.utils import execute_query, execute_insert, execute_delete
from tab_components.Database.c_insert import listing_id_exists, generate_listing_id, generate_agent_id

# Session State
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = True  

st.write("# Database Management 📂")
st.caption("This page helps with viewing data, adding new data, updating existing data and deleting an existing record from the database.")

tab_read, tab_insert, tab_update, tab_delete = st.tabs([
    "Read Data", "Insert Data", "Update Data", "Delete Data"
])

with tab_read:
    with st.container():
        st.caption("Select the table which you want to view data records")
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
            label="Data Tables",
            options=["Agents", "Listed Properties", "Sold Properties", "Property Attributes", "Buyers"],
            index=None,
            placeholder='Read data from',
            key='read_table'
        )
        
        with st.container(border=True):
            
            if table != None:
                st.write("Result Table")
                read_table(options[table])
            else:
                st.caption("No Table Selected")

with tab_insert:
    with st.container():
        st.caption("Select the table in which you want to insert data record")
        table = st.selectbox(
            "Data Tables",
            ["Agents", "Listed Properties", "Sold Properties", "Property Attributes", "Buyers"],
            index=None,
            placeholder='Insert data in',
            key='insert_table'
        )

        if table == 'Agents':
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

        if table == 'Listed Properties':            
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

        if table == 'Sold Properties':
            with st.form("add_sales"):
                st.write("Fill the Sold Property Details")
                listing_query = f"""
                    select l.listing_id
                    from listings l
                    left join sales s
                    on l.listing_id = s.listing_id
                    where Date_Sold is null;
                """
                listing_id_values = list(execute_query(listing_query)['listing_id'])
                listing_id = st.selectbox(
                    label='Listing ID',
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

        if table == 'Property Attributes':
            with st.form("add_property_attributes"):
                st.write("Fill the Property Attributes")

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

                is_rented = st.checkbox("Is Rented")

                parking_available = st.checkbox("Parking Available")

                power_backup = st.checkbox("Power Backup")

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

        if table == 'Buyers':
            with st.container(border=True):
                st.write("Fill the Buyer Details")
                loan_taken = st.checkbox("Loan Taken")

                if loan_taken:
                    loan_provider = st.selectbox(
                        label='Loan Provider',
                        options= list(execute_query('select distinct Loan_Provider from buyers where Loan_Provider != "NA"')['Loan_Provider'])

                    )

                    loan_amount = st.number_input(
                        label='Loan Amount',
                        min_value=0
                    )

                with st.form("add_buyers", border=False):

                    listing_id = st.selectbox(
                        label='Listing ID',
                        options=list(execute_query('select distinct Listing_ID from sales order by Listing_ID')['Listing_ID']),
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

with tab_update:
    with st.container():
        st.caption("Select the table in which you want to update data record")
        table = st.selectbox(
            "Data Tables",
            ["Agents", "Listed Properties", "Sold Properties", "Property Attributes", "Buyers"],
            index=None,
            placeholder='Update data in',
            key='update_table'
        )

        if table == 'Agents':
            with st.container(border=True):
                st.write("Update Agent Data")
                agent_id = st.selectbox(
                    label='Agent ID',
                    options = list(execute_query('select distinct Agent_ID from agents')['Agent_ID']),
                    index=None,
                    placeholder='Select Agent ID to update'
                )
                
                update_details = st.multiselect(
                    label='Details to Update',
                    options=['Email','Phone','Commission Rate','Deals Closed','Rating','Years Of Experience','Average Closing Days']
                )

                if len(update_details) != 0:
                    with st.form("update_agents", border=False):
                        field_inputs = {}

                        for detail in update_details:
                            if detail == 'Email':
                                field_inputs['email'] = st.text_input(
                                    label='Email Address'
                                )

                            if detail == 'Phone':
                                field_inputs['phone'] = st.text_input(
                                    label="Phone", 
                                    placeholder='10 Digit number', 
                                    max_chars=10)

                            if detail == 'Commission Rate':
                                field_inputs['commission_rate'] = st.slider(
                                    label="Commission Rate", 
                                    min_value=0.00,  
                                    max_value=50.00, 
                                    format='%0.2f'
                                )

                            if detail == 'Deals Closed':
                                field_inputs['deals_closed'] = st.number_input(
                                    label="Deals Closed", 
                                    step=1
                                )

                            if detail == 'Rating':
                                field_inputs['rating'] = st.slider(
                                    label="Rating", 
                                    min_value=0.0, 
                                    max_value=5.0, 
                                    format="%0.1f"
                                )

                            if detail == 'Years Of Experience':
                                field_inputs['years_of_experience'] = st.number_input(
                                    label="Years of Experience", 
                                    min_value=0
                                )

                            if detail == 'Average Closing Days':
                                field_inputs['avg_closing_days'] = st.number_input(
                                    label="Average Closing Days", 
                                    min_value=0
                                )

                        submit = st.form_submit_button("Submit")

                        if submit:
                            if agent_id:

                                old_data = execute_query(f"select * from agents where Agent_ID = '{agent_id}'")

                                set_clause = ", ".join([f"{col} = %s" for col in field_inputs.keys()])
                                values = tuple(field_inputs.values()) + (agent_id,)

                                query = f"""
                                    UPDATE agents
                                    set {set_clause}
                                    where Agent_ID = %s
                                """

                                success, error = execute_insert(query, values)

                                if success:
                                    st.success("Data Updated Successfully")
                                    st.write('Old Data')    
                                    st.dataframe(old_data)
                                    st.write("Updated Data")
                                    new_data = execute_query(f"select * from agents where Agent_ID = '{agent_id}'")
                                    st.dataframe(new_data)

                                    

                                else:
                                    st.error(f"Insert Failed: {error}")

                            else:
                                st.warning("Select Agent ID before submitting")

        if table == 'Listed Properties':
            with st.container(border=True):
                st.write("Update Listing Data")

                listing_id = st.selectbox(
                    label='Listing ID',
                    options=list(execute_query('select distinct Listing_ID from listings')['Listing_ID']),
                    index=None,
                    placeholder="Select Listing ID"
                )

                update_details = st.multiselect(
                    label='Details to Update',
                    options=['City', 'Property Type', 'Price', 'Sqft', 'Listed Date', 'Agent ID', 'Latitude', 'Longitude']
                )

                if len(update_details) != 0:
                    with st.form("update_listings", border=False):
                        field_inputs = {}

                        for detail in update_details:
                            if detail == 'City':
                                field_inputs['City'] = st.selectbox(
                                    label='City',
                                    options=list(execute_query('select distinct City from listings')['City']),
                                    index=None,
                                    placeholder='Select City'
                                )

                            if detail == 'Agent ID':
                                field_inputs['Agent_ID'] = st.selectbox(
                                    label='Agent ID',
                                    options=list(execute_query("select distinct Agent_ID from agents")['Agent_ID']),
                                    index=None
                                )

                            if detail == 'Property Type':
                                field_inputs['Property_Type'] = st.selectbox(
                                    label='Property Type',
                                    options=list(execute_query("select distinct property_type from listings")['property_type']),
                                    index=None,
                                    placeholder='Select Property Type'
                                )

                            if detail == 'Price':
                                field_inputs['Price'] = st.number_input(
                                    label='Listed Price ($)',
                                    min_value=0
                                )

                            if detail == 'Sqft':
                                field_inputs['Sqft'] = st.number_input(
                                    label='Property Area in Sqft',
                                    min_value=0
                                )

                            if detail == 'Listed Date':
                                field_inputs['Date_Listed'] = st.date_input(
                                    label='Listed Date',
                                    min_value=datetime.date(2023, 1, 1),
                                    max_value='today'
                                )

                            if detail == 'Latitude':
                                field_inputs['Latitude'] = st.number_input(
                                    label='Latitude'
                                )

                            if detail == 'Longitude':
                                field_inputs['Longitude'] = st.number_input(
                                    label='Longitude'
                                )

                            
                        submit = st.form_submit_button("Submit")

                        if submit:
                            if listing_id:
                                old_data = execute_query(f"select * from listings where LIsting_ID = '{listing_id}'")

                                set_clause = ", ".join([f"{col} = %s" for col in field_inputs.keys()])
                                values = tuple(field_inputs.values()) + (listing_id,)

                                query = f"""
                                    UPDATE listings
                                    set {set_clause}
                                    where Listing_ID = %s
                                """

                                success, error = execute_insert(query, values)

                                if success:
                                    st.success("Data Updated Successfully")
                                    st.write('Old Data')    
                                    st.dataframe(old_data)
                                    st.write("Updated Data")
                                    new_data = execute_query(f"select * from listings where LIsting_ID = '{listing_id}'")
                                    st.dataframe(new_data)

                                else:
                                    st.error(f"Insert Failed: {error}")

                            else:
                                st.warning("Select Listing ID before submitting")
            
        if table == "Sold Properties":
            with st.container(border=True):
                st.write("Update Sold Property Data")
                sale_id = st.selectbox(
                    label='Sale ID',
                    options=list(execute_query('select Sale_ID from sales order by Sale_ID')['Sale_ID']),
                    index = None,
                    placeholder='Select Sale ID'
                )

                update_details = st.multiselect(
                    label='Details to Update',
                    options=['Listing ID','Sale Price', 'Date Sold', 'Days On Market']
                )

                if len(update_details) != 0:
                    with st.form("update_sales", border=False):
                        field_inputs = {}

                        for detail in update_details:
                            if detail == 'Listing ID':
                                listing_query = f"""
                                    select l.listing_id
                                    from listings l
                                    left join sales s
                                    on l.listing_id = s.listing_id
                                    where Date_Sold is null;
                                """
                                listing_id_values = list(execute_query(listing_query)['listing_id'])
                                field_inputs['Listing_ID'] = st.selectbox(
                                    label='Listing ID',
                                    options=listing_id_values,
                                    index=None,
                                    placeholder='Select the Property Listing ID'
                                )

                            if detail == 'Sale Price':
                                field_inputs['Sale_Price'] = st.number_input(
                                    label='Sale Price ($)',
                                    min_value=0
                                )

                            if detail == 'Date Sold':
                                field_inputs['Date_Sold'] = st.date_input(
                                    label='Date Sold',
                                    max_value='today'
                                )

                            if detail == 'Days On Market':
                                field_inputs['Days_On_Market'] = st.number_input(
                                'Days on Market',
                                min_value=0
                            )

                        submit = st.form_submit_button("Submit")

                        if submit:
                            if sale_id:
                                old_data = execute_query(f"select * from sales where Sale_ID = '{sale_id}'")

                                set_clause = ", ".join([f"{col} = %s" for col in field_inputs.keys()])
                                values = tuple(field_inputs.values()) + (sale_id,)

                                query = f"""
                                    UPDATE sales
                                    set {set_clause}
                                    where Sale_ID = %s
                                """

                                success, error = execute_insert(query, values)

                                if success:
                                    st.success("Data Updated Successfully")
                                    st.write('Old Data')    
                                    st.dataframe(old_data)
                                    st.write("Updated Data")
                                    new_data = execute_query(f"select * from sales where Sale_ID = '{sale_id}'")
                                    st.dataframe(new_data)

                                else:
                                    st.error(f"Insert Failed: {error}")

                            else:
                                st.warning("Select Sale ID before submitting")

        if table == 'Property Attributes':
            with st.container(border=True):
                st.write("Update Property Attributes")

                listing_id = st.selectbox(
                    label="Listing ID",
                    options= list(execute_query('select Listing_ID from property_attributes')['Listing_ID']),
                    index=None,
                    placeholder="Select Property Listing ID"               
                )

                update_details = st.multiselect(
                    label='Details to Update',
                    options=['Bedroom Count','Bathroom Count','Floor Number','Total Floor','Year Built','Is Rented','Tenant Count','Furnishing Status','Metro Distance','Parking Available','Power Backup']
                )

                if len(update_details) != 0:
                    with st.form("update_property_attributes", border=False):
                        field_inputs = {}
                        for detail in update_details:
                            if detail == 'Bathroom Count':
                                field_inputs['Bathroom'] = st.number_input(
                                    label='Bathroom Count',
                                    min_value=0
                                )

                            if detail == 'Bedroom Count':
                                field_inputs['Bedroom'] = st.number_input(
                                    label='Bedroom Count',
                                    min_value=0
                                )
                                
                            if detail == 'Floor Number':
                                field_inputs['Floor_Number'] = st.number_input(
                                    label='Floor Number',
                                    min_value=0
                                )

                            if detail == 'Total Floor':
                                field_inputs['Total_Floor'] = st.number_input(
                                    label='Total Floors',
                                    min_value=0
                                )

                            if detail == 'Year Built':
                                selected_year_built = st.date_input(
                                    label='Year Built'
                                )
                                field_inputs['Year_Built'] = selected_year_built.year

                            if detail == 'Is Rented':
                                field_inputs['Is_Rented'] = st.checkbox('Is Rented')

                            if detail == 'Tenant Count':
                                field_inputs['Tenant_Count'] = st.number_input(
                                    label='Tenant Count',
                                    min_value=0
                                )

                            if detail == 'Furnishing Status':
                                field_inputs['Furnishing_Status'] = st.selectbox(
                                    label='Furnishing Status',
                                    options=list(execute_query('select distinct furnishing_status from property_attributes')['furnishing_status']),
                                    index=None,
                                    placeholder='Select the furnishing Status'
                                )

                            if detail == 'Metro Distance':
                                field_inputs['Metro_Distance'] = st.number_input(
                                    label='Distance from Nearest Metro Station',
                                    min_value=0.00
                                )

                            if detail == 'Parking Available':
                                field_inputs['Parking_Available'] = st.checkbox("Parking Available")

                            if detail == 'Power Backup':
                                field_inputs['Power_Backup'] = st.checkbox("Power Backup")

                        submit = st.form_submit_button("Submit")

                        if submit:
                            if listing_id:
                                old_data = execute_query(f"select * from property_attributes where Listing_ID = '{listing_id}'")

                                set_clause = ", ".join([f"{col} = %s" for col in field_inputs.keys()])

                                values = tuple(field_inputs.values()) + (listing_id,)

                                query = f"""
                                    UPDATE property_attributes
                                    set {set_clause}
                                    where Listing_ID = %s
                                """
                                success, error = execute_insert(query, values)

                                if success:
                                    st.success("Data Updated Successfully")
                                    st.write('Old Data')    
                                    st.dataframe(old_data)
                                    st.write("Updated Data")
                                    new_data = execute_query(f"select * from property_attributes where Listing_ID = '{listing_id}'")
                                    st.dataframe(new_data)

                                else:
                                    st.error(f"Insert Failed: {error}")

                            else:
                                st.warning("Select Listing ID before submitting")

        if table == 'Buyers':
            with st.container(border=True):
                st.write("Update Buyer Data")

                buyer_id = st.selectbox(
                    label="Buyer ID",
                    options=list(execute_query('select Buyer_ID from buyers')['Buyer_ID']),
                    index=None,
                    placeholder='Select Buyer ID'
                )

                update_details = st.multiselect(
                    label='Details to Update',
                    options=['Listing ID', 'Buyer Type', 'Payment Method', 'Loan Status']
                )
                
                field_inputs = {}
                for detail in update_details:
                    if detail == 'Loan Status':
                        field_inputs['Loan_Taken'] = st.checkbox("Loan Taken")

                        st.session_state.disabled = not field_inputs['Loan_Taken']
                        st.session_state.visibility = "visible" if field_inputs['Loan_Taken'] else "hidden"

                        field_inputs['Loan_Provider'] = st.selectbox(
                            label='Loan Provider',
                            options=list(execute_query('select distinct Loan_Provider from buyers')['Loan_Provider']),
                            label_visibility=st.session_state.visibility,
                            disabled=st.session_state.disabled
                        )

                        field_inputs['Loan_Amount'] = st.number_input(
                            label='Loan Amount',
                            min_value=0,
                            label_visibility=st.session_state.visibility,
                            disabled=st.session_state.disabled,
                        )

                with st.form("update_buyers", border=False):
                    for detail in update_details:
                        if detail == 'Listing ID':
                            field_inputs['Listing_ID'] = st.selectbox(
                                label='Listing ID',
                                options=list(execute_query('select distinct Listing_ID from sales order by Listing_ID')['Listing_ID']),
                                index=None
                            )

                        if detail == 'Buyer Type':
                            field_inputs['Buyer_Type'] = st.selectbox(
                                label='Buyer Type',
                                options=list(execute_query('select distinct Buyer_Type from buyers')['Buyer_Type']),
                                index=None
                            )

                        if detail == 'Payment Method':
                            field_inputs['Payment_Method'] = st.selectbox(
                                label='Payment Method',
                                options=list(execute_query('select distinct Payment_Method from buyers')['Payment_Method']),
                                index=None
                            )

                    submit = st.form_submit_button('Submit')

                    if submit:
                        if buyer_id:
                            
                            old_data = execute_query(f"select * from buyers where Buyer_ID = '{buyer_id}'")

                            set_clause = ", ".join([f"{col} = %s" for col in field_inputs.keys()])

                            values = tuple(field_inputs.values()) + (buyer_id,)

                            query = f"""
                                UPDATE buyers
                                set {set_clause}
                                where Buyer_ID = %s
                            """
                            success, error = execute_insert(query, values)

                            if success:
                                st.success("Data Updated Successfully")
                                st.write('Old Data')    
                                st.dataframe(old_data)
                                st.write("Updated Data")
                                new_data = execute_query(f"select * from buyers where Buyer_ID = '{buyer_id}'")
                                st.dataframe(new_data)

                            else:
                                st.error(f"Insert Failed: {error}")

                        else:
                            st.warning("Select Buyer ID before submitting")

with tab_delete:
    with st.container():
        st.caption('Select the table from which you want to delete a data record')
        table = st.selectbox(
            "Data Tables",
            ["Agents", "Listed Properties", "Sold Properties", "Property Attributes", "Buyers"],
            index=None,
            placeholder='Delete data from',
            key='delete_table'
        )

        if table == 'Agents':
            with st.form('delete_agent'):
                st.write("### Delete Agent Data")
                agent_id = st.selectbox(
                    label='Agent ID',
                    options=list(execute_query('select Agent_ID from agents')['Agent_ID']),
                    index=None,
                    placeholder='Select Agent ID'
                )

                submit = st.form_submit_button("Submit")

                if submit:
                    if agent_id:
                        query = f"""
                            delete from agents
                            where Agent_ID = '{agent_id}'
                        """
                        success, error = execute_delete(query)
                        if success:
                            st.success("Data Deleted Successfully")

                        else:
                            st.error(f"Deletion Failed: {error}")

                    else:
                        st.warning("Select the Agent ID")

        if table == "Listed Properties":
            with st.form('delete_listing'):
                st.write("### Delete Listed Property Data")
                listing_id = st.selectbox(
                    label='Listing ID',
                    options=list(execute_query('select Listing_ID from listings')['Listing_ID']),
                    index=None,
                    placeholder='Select Listing ID'
                )

                submit = st.form_submit_button("Submit")

                if submit:
                    if listing_id:
                        query = f"""
                            delete from listings
                            where Listing_ID = '{listing_id}'
                        """
                        success, error = execute_delete(query)
                        if success:
                            st.success("Data Deleted Successfully")

                        else:
                            st.error(f"Deletion Failed: {error}")

                    else:
                        st.warning("Select Listing ID")

        if table == "Sold Properties":
            with st.form('delete_sales'):
                st.write("### Delete Sold Property Data")
                sale_id = st.selectbox(
                    label='Sale ID',
                    options=list(execute_query('select Sale_ID from sales')['Sale_ID']),
                    index=None,
                    placeholder='Select Sale ID'
                )

                submit = st.form_submit_button("Submit")

                if submit:
                    if sale_id:
                        query = f"""
                            delete from sales
                            where Sale_ID = '{sale_id}'
                        """
                        success, error = execute_delete(query)
                        if success:
                            st.success("Data Deleted Successfully")

                        else:
                            st.error(f"Deletion Failed: {error}")

                    else:
                        st.warning("Select Sale ID")
                    
        if table == "Property Attributes":
            with st.form('delete_property_attributes'):
                st.write("### Delete Property Attributes Data")
                listing_id = st.selectbox(
                    label='Listing ID',
                    options=list(execute_query('select Listing_ID from property_attributes')['Listing_ID']),
                    index=None,
                    placeholder='Select Listing ID'
                )

                submit = st.form_submit_button("Submit")

                if submit:
                    if listing_id:
                        query = f"""
                            delete from property_attributes
                            where Listing_ID = '{listing_id}'
                        """
                        success, error = execute_delete(query)
                        if success:
                            st.success("Data Deleted Successfully")

                        else:
                            st.error(f"Deletion Failed: {error}")

                    else:
                        st.warning("Select Listing ID")

        if table == "Buyers":
            with st.form('delete_buyers'):
                st.write("### Delete Buyer Data")
                buyer_id = st.selectbox(
                    label='Buyer ID',
                    options=list(execute_query('select Buyer_ID from buyers')['Buyer_ID']),
                    index=None,
                    placeholder='Select Buyer ID'
                )

                submit = st.form_submit_button("Submit")

                if submit:
                    if buyer_id:
                        query = f"""
                            delete from buyers
                            where Buyer_ID = '{buyer_id}'
                        """
                        success, error = execute_delete(query)
                        if success:
                            st.success("Data Deleted Successfully")

                        else:
                            st.error(f"Deletion Failed: {error}")

                    else:
                        st.warning("Select Buyer ID")



