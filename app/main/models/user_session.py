import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

Model.__abstract__ = True
Model.__keyspace__ = "sessions"

class UserSession(Model):
    """
        Model sessions per player
    """
    user_id = columns.Text(primary_key=True)
    session_id = columns.Text()
    event = columns.Text(primary_key=True, partition_key=True)
    ts = columns.DateTime(primary_key=True, clustering_order='DESC') 