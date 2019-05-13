import json
import flask
from flask_restplus import Resource, Namespace, fields

from .utils import json_api
from ..services.batches_service import get_batch_data

api = Namespace('batches', description='insert events operation')

# Define an API model to be consumed as part of the POST query
event = api.model('event', {
    'event': fields.String(required=True, description='event type'),
    'session_id': fields.String(required=True, description='session identifier'),
    'user_id': fields.String(required=True, description='user_id'),
    'country': fields.String(description='country'),
    'ts': fields.DateTime(required=True, description='timestamp')
    })

@api.route("/batches", methods=["POST"])
@api.response(200, 'Batch successfully created.')
@api.expect([event])
@api.doc('insert batch of event')
class Batches(Resource):
	@json_api
	def post(self):
	    batch = json.loads(flask.request.data)
	    get_batch_data(batch)
	    return {"message": "success insertion"}