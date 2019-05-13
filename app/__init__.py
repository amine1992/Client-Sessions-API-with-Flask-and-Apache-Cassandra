from flask_restplus import Api
from flask import Blueprint

from .main.routes.batches_route import api as batches_ns
from .main.routes.last_event_route import api as last_event_ns
from .main.routes.complete_sessions_route import api as complete_sessions_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API USER',
          version='1.0',
          description='flask restplus web service'
          )

api.add_namespace(batches_ns, path='/user')
api.add_namespace(last_event_ns, path='/user')   #http://127.0.0.1:5000/user/last-events?days=170
api.add_namespace(complete_sessions_ns, path='/user') #http://127.0.0.1:5000/user/last-sessions-player?player_id=d6313e1fb7d247a6a034e2aadc30ab3f