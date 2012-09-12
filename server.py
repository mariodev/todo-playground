import json
import random
from bson.objectid import ObjectId

import pymongo
import web
from utils import *


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
web.config.debug = True
# session = web.session.Session(app, web.session.DiskStore('sessions'))

# customize 500 error
def internalerror():
    return web.internalerror(json.dumps({'message': 'Internal server error.'}))
app.internalerror = internalerror


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