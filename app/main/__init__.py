from flask import Flask
from flask_caching import Cache

from .persistance.database import CassandraDBConnector

db = CassandraDBConnector()
db.connect("127.0.0.1","1234")

def create_app():
    app = Flask(__name__)
    cache = Cache(app,config={'CACHE_TYPE': 'simple'})
    cache.init_app(app)
    app.debug = True
    return app