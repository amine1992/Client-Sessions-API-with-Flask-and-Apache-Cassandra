from ..services.complete_sessions_service import get_last_complete

def get_last_complete_handler(user_id, num_sess = 20):
    """
    Handler to postprocess the result of the queries to fetch the last 20 complete sessions of the user
    """
    
    # Get result from the service 
    res_query = get_last_complete(user_id)
    
    # Get intersection of list of end events and start events while maintaining the order of the element of the end event
    inter_events = sorted(set(res_query["end"]) & set(res_query["start"]), key = res_query["end"].index)[:num_sess]
    return {user_id : inter_events}

