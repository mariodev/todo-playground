"""
Utils

Adding functions into web. namespace:

`web.no_content()`
	: 204, returned when no content needed

`web.custom_error()`
	: 416, custom error test

`json.request()`
	: returns json structure loaded from request payload
	  converts special keys e.g. _id => ObjectId
	  if no argument specified then json takes web.data() as payload
	  
`json.response(status_class[,data=''[,headers={}]])`
	: returns response with json content
	  converts special objects e.g. ObjectId => str
	  'status_class' can be any valid status object, i.e. web.ok, web.created
"""

import json
from bson.objectid import ObjectId
from bson.json_util import dumps, loads

import web


# custom RESTful response used when updating/deleting model
# with no content in response 
web.no_content = web.NoContent = web.webapi._status_code("204 No Content")
web.custom_error = web.CustomError = web.webapi._status_code("416 Error Test")


def _request(data = None):
    if not data:
        data = web.data()
    return loads(data)
json.request = _request

def _response(classname = web.ok, data="", headers={}, **kwargs):
    headers['Content-Type'] = 'application/json'
    headers['Charset'] = 'utf-8'
    data = dumps(data)
    return classname(data, headers, **kwargs)
json.response = _response
