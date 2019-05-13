from ..persistance import db
from collections import defaultdict

def get_last_complete(user_id):
    # We will get the list ordered by ts
    query = "SELECT session_id FROM user_session WHERE user_id='{}' AND event=%s".format(user_id)
    end_sessions = []
    futures = []
    res = defaultdict(list)
    # Send asynchronous queries to get list of start and end event of the player
    for evt in ['start', 'end']:
        futures.append([evt, db.async_query(query, [evt])])
    # Loop over the results of the queries 
    for future in futures:
        rows = future[1].result()
        for elt in rows:
            res[future[0]].append(elt.session_id)
    return res        
