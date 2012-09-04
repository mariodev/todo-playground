"""
Utils

Adding functions into web. namespace:

`web.no_content()`
	: 204, returned when no content needed

`web.custom_error()`
	: 416, custom error test

`web.json_payload(data)`
	: returns json structure loaded from request payload
	  converts special keys e.g. _id => ObjectId
	  web.json_payload(web.data())
	  
`web.json(status_class[,data=''[,headers={}]])`
	: returns response with json content
	  converts special objects e.g. ObjectId => str
	  'status_class' can be any valid status object, i.e. web.ok, web.created
"""

import web, json
from bson.objectid import ObjectId


# custom RESTful response used when updating/deleting model
# with no content in response 
web.no_content = web.NoContent = web.webapi._status_code("204 No Content")
web.custom_error = web.CustomError = web.webapi._status_code("416 Error Test")


# fix the ObjectId issue when encoding/decoding JSON object
def _todo_json_encoding(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

def _todo_json_decoding(obj):
    if obj.has_key('_id'):
        obj['_id'] = ObjectId(obj['_id'])
    return obj

def _json_request(data):
    return json.loads(data, object_hook=_todo_json_decoding)
web.json_payload = _json_request

def _json_response(status_class, data="", headers={}):
    headers['Content-Type'] = 'application/json'
    data = json.dumps(data, default=_todo_json_encoding)
    return status_class(data=data, headers=headers)
web.json = _json_response
