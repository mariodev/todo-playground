import web
import json
import random
import pymongo
import bson


# custom RESTful response used when updating/deleting model
# with no content in response 
web.no_content = NoContent = web.webapi._status_code("204 No Content")
web.custom_error = CustomError = web.webapi._status_code("416 Error Test")

# set MongoDB connection  
connection = pymongo.Connection("localhost", 27017)
db = connection.test

# fix the ObjectId issue when encoding/decoding JSON object
def todo_json_encoding(obj):
    if isinstance(obj, bson.objectid.ObjectId):
        return str(obj)
    else:
        return obj

def todo_json_decoding(obj):
    obj['_id'] = bson.objectid.ObjectId(obj['_id'])
    return obj


urls = (
    '/api/todos/([a-f0-9]+)', 'todos',
    '/api/todos', 'todos',
    '/', 'home',
)

app = web.application(urls, globals())
render = web.template.render('templates/')
# session = web.session.Session(app, web.session.DiskStore('sessions'))

class home:
    def GET(self):
        return render.index()

class todos:
    def GET(self):
        web.header('Content-Type', 'application/json')
        return json.dumps(list(db.todos.find()), default=todo_json_encoding)

    def POST(self):
        _id = db.todos.insert(json.loads(web.data()))
        web.header('Content-Type', 'application/json')
        res = json.dumps(db.todos.find_one(_id), default=todo_json_encoding)
        raise web.created(res)
        # raise custom_error(json.dumps(
        #     { u'message': u'Custom Error raised' }
        # ))

    def PUT(self, _id):
        data = json.loads(web.data(), object_hook=todo_json_decoding)
        db.todos.save(data)

        # res = json.dumps(db.todos.find_one(bson.objectid.ObjectId(_id)), default=todo_json_encoding)
        return web.no_content()

    def DELETE(self, _id):
        db.todos.remove(bson.objectid.ObjectId(_id))
        return web.no_content()


if __name__ == "__main__":
    app.run()