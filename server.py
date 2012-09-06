import json
import random
from bson.objectid import ObjectId

import pymongo
import web
from utils import *

class dict_(dict):

    def json(self):
        json.loads(data, object_hook=_todo_json_decoding)

# set MongoDB connection  
connection = pymongo.Connection("localhost", 27017)
db = connection.test


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
        raise json.response(web.ok, data=list(db.todos.find()))

    def POST(self):
        data = json.request()
        db.todos.save(data, safe=True)
        raise json.response(web.created, data=data)
        # raise custom_error(json.dumps(
        #     { u'message': u'Custom Error raised' }
        # ))

    def PUT(self, _id):
        data = json.request()
        db.todos.save(data, safe=True, multi=False)
        return web.no_content()

    def DELETE(self, _id):
        db.todos.remove(ObjectId(_id), safe=True)
        return web.no_content()


if __name__ == "__main__":
    app.run()