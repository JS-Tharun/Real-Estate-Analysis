from utils.utils import execute_query

def listing_id_exists(listing_id):
    query = f"""
        select count(*)
        from listings
        where Listing_ID = '{listing_id}'
    """
    result = execute_query(query)
    return result.iloc[0,0] > 0
