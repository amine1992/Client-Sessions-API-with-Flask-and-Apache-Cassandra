from .database import CassandraDBConnector

db = CassandraDBConnector()
db.connect("127.0.0.1","1234")