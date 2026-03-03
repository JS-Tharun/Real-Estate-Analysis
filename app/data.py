from filters import filter

def listing_query():
  query = f"""
  select 
    * 
  from 
    listings 
  where 
    (Price between 0 AND {filter['Price']}) 
    AND (Date_Listed between '{filter['From Listed Date']}' AND '{filter['To Listed Date']}')
  """

  if len(filter['City']) != 0:
    city_str = ", ".join([f"'{city}'" for city in filter['City']])
    query += f" AND (City IN ({city_str}))"

  if filter['Property_Type'] != "All":
    query += f" AND (Property_Type = '{filter['Property_Type']}')"

  if filter['Agent'] != "All":
    query += f" AND (Agent_ID = '{filter['Agent']}')"

  return query