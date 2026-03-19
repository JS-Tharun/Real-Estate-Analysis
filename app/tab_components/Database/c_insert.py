from utils.utils import execute_query

def listing_id_exists(listing_id):
    query = f"""
        select count(*)
        from listings
        where Listing_ID = '{listing_id}'
    """
    result = execute_query(query)
    return result.iloc[0,0] > 0

def generate_listing_id():
    result = execute_query('select max(Listing_ID) as Max_ID from listings')
    val = str(result.iloc[0,0])
    id_num = int(val[1:]) + 1
    listing_id = 'L' + str(id_num)
    return listing_id

def generate_agent_id():
    result = execute_query('select max(agent_id) from agents')
    val = str(result.iloc[0,0])
    id_num = int(val[1:]) + 1
    agent_id = 'A' + str(id_num).zfill(4)
    return agent_id
