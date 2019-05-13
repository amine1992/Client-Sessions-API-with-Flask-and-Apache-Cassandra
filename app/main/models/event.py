import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

Model.__abstract__ = True
Model.__keyspace__ = "sessions"
class Event(Model):
    """
        Model event by country
    """
    event = columns.Text(primary_key=True)
    session_id = columns.Text()
    country = columns.Text(primary_key=True, partition_key=True) 
    user_id = columns.Text()
    ts = columns.DateTime(primary_key=True, clustering_order='DESC') 

