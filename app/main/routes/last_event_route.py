import json
from .utils import json_api
import flask

from flask_restplus import Resource, Namespace
from ..handlers.last_event_handler import get_last_events_handler

api = Namespace('last-events', description='get start events of the last x days')

@api.route("/last-events", methods=["GET"])
@api.param('days', 'The number of days')
class LastEvents(Resource):
	@json_api
	def get(self):
	    x_days = flask.request.args.get("days")
	    x_days  = int(x_days)
	    res = get_last_events_handler(x_days)
	    return res