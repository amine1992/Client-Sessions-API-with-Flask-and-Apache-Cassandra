import json
from .utils import json_api
import flask

from flask_restplus import Resource, Namespace
from ..handlers.complete_sessions_handler import  get_last_complete_handler

api = Namespace('last-sessions-user', description='get last 20 complete sessions of a user')

@api.route("/last-sessions-user", methods=["GET"])
@api.param('user_id', 'The user identifier')
class LastSessionsuser(Resource):
    @json_api
    def get(self):
        user_id = flask.request.args.get("user_id")
        res = get_last_complete_handler(user_id)
        return res