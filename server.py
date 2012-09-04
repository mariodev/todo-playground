import web, json, random
import pymongo
from bson.objectid import ObjectId
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
# session = web.session.Session(app, web.session.DiskStore('sessions'))

class home:
    def GET(self):
        return render.index()

class todos:
    def GET(self):
        raise web.json(web.ok, data=list(db.todos.find()))

    def POST(self):
        data = web.json_payload(web.data())
        _id = db.todos.insert(data)
        raise web.json(web.created, data=db.todos.find_one(_id))
        # raise custom_error(json.dumps(
        #     { u'message': u'Custom Error raised' }
        # ))

    def PUT(self, _id):
        data = web.json_payload(web.data())
        db.todos.save(data)
        return web.no_content()

    def DELETE(self, _id):
        db.todos.remove(ObjectId(_id))
        return web.no_content()


if __name__ == "__main__":
    app.run()