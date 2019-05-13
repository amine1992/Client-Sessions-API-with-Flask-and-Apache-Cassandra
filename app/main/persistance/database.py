# Python modules
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.query import BatchStatement, ConsistencyLevel

import json
import re
import datetime

# Custom Sessions Modules
from ..models.event import Event
from ..models.user_session import UserSession



def Singleton(cls):
    """ Create Singleton class"""

    instances = {}
    def getInstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getInstance

@Singleton
class CassandraDBConnector:
    """ Cassandra db connector """
    _db_cur = None
    _tables_to_sync = [ UserSession, Event] 
    _batch = 10

    
    def connect(self, host, port, keyspace='sessions'):
        """ Connect with specific host & port """
        connection.setup([host,], "cqlengine", protocol_version=3)
        self._db_connection = Cluster()
        self._db_cur = self._db_connection.connect(keyspace=keyspace)

    def create_connection(self, keyspace):
        """Create connection with specified keyspace"""

        self._db_connection = Cluster()
        self._db_cur = self._db_connection.connect()
        self._keyspace = keyspace

        self._db_cur.execute("""
            DROP KEYSPACE IF EXISTS %s
        """ % self._keyspace)

        self._db_cur.execute("""
            CREATE KEYSPACE IF NOT EXISTS %s WITH REPLICATION = {'class': 'SimpleStrategy',
                                                            'replication_factor': 1};
        """ % self._keyspace)
        self._db_cur = self._db_connection.connect(keyspace=self._keyspace)

    def query(self, query):
        """ query cassandra db """
        return self._db_cur.execute(query)
        
    def async_query(self, query, args):
        """ asynchronous query cassandra db """
        return self._db_cur.execute_async(query, args)

    def sync_db(self):
        """ create tables as models inside self._tables_to_sync """
        for table in self._tables_to_sync:
            sync_table(table)


    def import_from_source(self, source, is_ttl= False):
        """ import data from json to db 
            Source: can be a file of events or batch (list of events)
            is_ttl: boolean to decide if to add an expiration period to each record """

        if isinstance(source, str):
            with open(source, 'r') as f:
                list_records = f.readlines()
        else:
            if isinstance(source, list):
                list_records = source
            # else:
                # TODO
        expiration = ""
        if is_ttl:
            expiration = " USING TTL 31557600"  # Expiration set to one 1 year = 31557600 s
        # insert data in Event
        insert_event_country= self._db_cur.prepare("INSERT INTO EVENT (event, session_id, country, user_id, ts) VALUES ( ?, ?, ?, ?, ? )" + expiration)
        # insert data in user_SESSION
        insert_user_session= self._db_cur.prepare("INSERT INTO user_SESSION (event, session_id, user_id, ts) VALUES ( ?, ?, ?, ? )" + expiration)
        # Instantiate a batchStatement
        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

        for record_dict in list_records:
            if isinstance(source, str):
                record_dict = json.loads(record_dict)
            # Parse ts field from the record to datetime
            dt = datetime.datetime.strptime(record_dict["ts"], "%Y-%m-%dT%H:%M:%S")
            event = record_dict["event"]
            session_id = record_dict["session_id"]
            # For the end event, we don't have the country, we will not need to fill it with the right value
            # from the correspondant start event, so we'll just fill it with "None"
            country = record_dict.get("country","None")  
            # We have (.uk) in the country list, it's straightforward to fix it although we don't have to for this task
            country = re.sub('[\W\_]','',country).upper()
            user_id = record_dict["user_id"]

            while len(batch) > self._batch * len(self._tables_to_sync):
                self._db_cur.execute(batch)
                batch.clear()
            # Add data to batch
            batch.add(insert_event_country, (event, session_id, country, user_id, dt ) )
            batch.add(insert_user_session, (event, session_id, user_id, dt ) )

        if len(batch) != 0:
            self._db_cur.execute(batch)