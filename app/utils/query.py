from utils.utils import execute_query
from components.c_properties import filter

def property_query():
  query = f"""
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
        when p.Is_Rented is True then 'Rented'
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
    on p.Listing_ID = s.Listing_ID) T
    where (Listed_Price between {filter['Price Range'][0]} and {filter['Price Range'][1]})
    AND (Metro_Distance between {filter['Metro Distance'][0]} and {filter['Metro Distance'][1]})
    And (Date_Listed between '{filter['From Listed Date']}' AND '{filter['To Listed Date']}')
    And (Bedroom between {filter['Bedroom Range'][0]} AND {filter['Bedroom Range'][1]})
    And (Bathroom between {filter['Bathroom Range'][0]} AND {filter['Bathroom Range'][1]})
  """
  # Filter Property Status
  if filter['Property Status'] != 'All':
      query += f"And (Property_Status = '{filter['Property Status']}')"

  
  # Filter City
  if len(filter['City']) != 0:
    city_str = ", ".join([f"'{city}'" for city in filter['City']])
    query += f" AND (City IN ({city_str}))"

  # Filter Property Type
  if len(filter['Property Type']) != 0:
    property_str = ", ".join([f"'{property}'" for property in filter['Property Type']])
    query += f" AND (Property_Type IN ({property_str}))"

  if filter['Furnishing Status'] != 'All':
    query += f"AND (Furnishing_Status = '{filter['Furnishing Status']}')"

  if filter['Agent'] != 'All':
    query += f"And Agent_ID = '{filter['Agent']}'"



  df = execute_query(query)
  return df

