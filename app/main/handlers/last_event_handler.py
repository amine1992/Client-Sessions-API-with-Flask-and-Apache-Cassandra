from ..services.last_event_service import get_last_events
from datetime import datetime, timedelta

def get_last_events_handler(days):
    """
    Handler for the fetching the events  in the last x days
    """
    # Get current time
    current_time = datetime.now()
    # Get the time of "days" before
    starting_time = current_time - timedelta(days= days)
    # Reformatting
    starting_time = starting_time.strftime("%Y-%m-%dT%H:%M:%S")
    current_time = current_time.strftime("%Y-%m-%dT%H:%M:%S")
    # Get the result of the correspondant query 
    res_query = get_last_events(current_time, starting_time)
    return res_query
