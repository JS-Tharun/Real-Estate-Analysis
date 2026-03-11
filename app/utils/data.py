from utils.filters import filter
from utils.utils import get_connection

def load_property_view_table():
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("drop view if exists property_master_view;")
  
  query = """
    create view property_master_view as
    select *
    from
      (select 
        l.Listing_ID,
        l.City,
        l.Property_Type,
        l.Price as Listed_Price,
        l.Sqft,
        l.Date_Listed,
        l.Agent_ID,
        l.Latitude,
        l.Longitude,
        
        
        p.Attribute_ID,
        p.Bedroom,
        p.Bathroom,
        p.Floor_Number,
        p.Total_Floor,
        p.Year_Built,
        case
        when p.Is_Rented is True then 'Occupied'
          else 'Available'
        end as Rent_Status,
        p.Tenant_Count,
        p.Furnishing_Status,
        p.Metro_Distance,
        case
        when p.Parking_Available is True then 'Yes'
          else 'No'
        end as Parking_Available,
        case
        when p.Power_Backup is True then 'Yes'
          else 'No'
        end as Power_Backup,
        
        
        case
        when s.Date_Sold is not null then 'Sold'
          else 'Unsold'
        end as Property_Status,
        s.Sale_Price,
        s.Date_Sold,
        s.Days_On_Market

    from listings l
    left join property_attributes p
    on l.Listing_ID = p.Listing_ID
    left join sales s
    on p.Listing_ID = s.Listing_ID) T;
  """
  cur.execute(query)

def load_agent_view_table():
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("drop view if exists agent_master_view;")

  query = """
    create view agent_master_view as
    select 
      l.Listing_ID,
        l.City,
        l.Property_Type,
        l.Price,
        l.Sqft,
        l.Date_Listed,
        l.Latitude,
        l.Longitude,
        
        a.Agent_ID,
        a.Commission_Rate,
        a.Deals_Closed,
        a.Rating,
        a.Years_Of_Experience,
        a.Avg_Closing_Days,
        
        s.Sale_Price,
        s.Date_Sold,
        s.Days_On_Market
        
    from listings l
    left join agents a
    on l.Agent_ID = a.Agent_ID
    left join sales s
    on l.Listing_ID = s.Listing_ID;
  """
  cur.execute(query)

def property_master_query():
  load_property_view_table()
  query = f"""
    select * from property_master_view
    where (Listed_Price between {filter['Price Range'][0]} and {filter['Price Range'][1]})
    AND (Metro_Distance between {filter['Metro Distance'][0]} and {filter['Metro Distance'][1]})
    And (Date_Listed between '{filter['From Listed Date']}' AND '{filter['To Listed Date']}')
    And (Bedroom between {filter['Bedroom Range'][0]} AND {filter['Bedroom Range'][1]})
    And (Bathroom between {filter['Bathroom Range'][0]} AND {filter['Bathroom Range'][1]})
    And (Sqft between {filter['Sqft Range'][0]} AND {filter['Sqft Range'][1]})
  """
  
  # Filter Property Status
  if filter['Property Status'] != None:
      query += f" And (Property_Status = '{filter['Property Status']}')"
  
  # Filter City
  if len(filter['City']) != 0:
    city_str = ", ".join([f"'{city}'" for city in filter['City']])
    query += f" AND (City IN ({city_str}))"

  # Filter Property Type
  if len(filter['Property Type']) != 0:
    property_str = ", ".join([f"'{property}'" for property in filter['Property Type']])
    query += f" AND (Property_Type IN ({property_str}))"

  # Filter Furnishing Status
  if len(filter['Furnishing Status']) != 0:
    furnish_str = ", ".join([f"'{furnish}'" for furnish in filter['Furnishing Status']])
    query += f"AND (Furnishing_Status IN ({furnish_str}))"

  # Filter Agent
  if filter['Agent'] != None:
    query += f"And Agent_ID = '{filter['Agent']}'"

  # Filter Parking Availablity
  if filter['Parking'] != None:
    query += f" AND (Parking_Available = '{filter['Parking']}')"

  # Filter Power backup
  if filter['Power Backup'] != None:
    query += f" AND (Power_Backup = '{filter['Power Backup']}')"

  # Filter Is Rented
  if filter['Rent Status'] != None:
    query += f" AND (Rent_Status = '{filter['Rent Status']}')"

  return query

def agent_master_query():
  load_agent_view_table()
  query = f"""
    select * from agent_master_view
  """
  return query

def load_buyer_view_table():
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("drop view if exists buyer_master_view;")

  query = """
    create view buyer_master_view as
    select 
      b.Buyer_ID,
        b.Listing_ID,
        b.Buyer_Type,
        b.Payment_Method,
        b.Loan_Taken,
        b.Loan_Provider,
        b.Loan_Amount,
        
        l.City,
        l.Property_Type,
        l.Price as Listed_Price,
        l.Sqft,
        l.Date_Listed,
        l.Agent_ID,
        
        s.Sale_Price,
        s.Date_Sold,
        s.Days_On_Market
    from buyers b
    left join listings l
    on b.Listing_ID = l.Listing_ID
    left join sales s
    on l.Listing_ID = s.listing_ID;
  """
  cur.execute(query)

def buyer_master_query():
  load_buyer_view_table()
  query = """
    select * from buyer_master_view
    where 1=1
  """
  if filter['Buyer Type'] != None:
    query += f"AND Buyer_Type = '{filter['Buyer Type']}'"

  if filter['Payment Method'] != None:
    query += f"AND Payment_Method = '{filter['Payment Method']}'"

  if filter['Loan Taken'] != 'All':
    query += f"AND Loan_Taken = '{filter['Loan Taken']}'"

  return query
