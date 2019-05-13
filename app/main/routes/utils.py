import json
from functools import wraps
from flask import Response
def to_json(data):
    def handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError('Object of type %s with value of %s is not JSON serializable') % (type(obj), repr(obj))

    return json.dumps(data, default=handler,  indent = 4)



def json_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = f(*args, **kwargs)      # call function
        json_result = to_json(result)
        return Response(response=json_result, 
                        status = 200, 
                        mimetype='application/json')
    return decorated_function
