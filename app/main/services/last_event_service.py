from ..persistance import db


def get_last_events(current_time, starting_time):
    countries = []
    result = db.query("SELECT distinct country FROM event")
    for row in result:
        if row.country != "NONE":
            countries.append(row.country)
    query = "SELECT session_id, user_id, ts FROM  event WHERE  event = 'start' AND country=%s AND ts >= '{}' AND ts <= '{}'".format(starting_time, current_time)
    futures = []
    res = {} #defaultdict(list)
    for country in countries:
        futures.append([country, db.async_query(query, [country])])
        res[country] = []
    
    for future in futures:
        rows = future[1].result()
        for elt in rows:
            rec = {}
            rec["session_id"] = elt.session_id
            rec["user_id"] = elt.user_id
            rec["ts"] = elt.ts.strftime("%Y-%m-%dT%H:%M:%S")
            res[future[0]].append(rec)

    return res