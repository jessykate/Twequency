#!/usr/bin/python

# A template for a Tornado project using forms and MongoDB as the
# backend: takes a form submission and stores it as a record in a
# Mongo DB. Don't forget to start Mongo first with the "mongod"
# command.
#
# To run:
# ./main.py
# and visit localhost:8888

import tornado.httpserver
import tornado.ioloop
import tornado.web
import urllib, urllib2
import os, datetime
try:
    import json
except:
    import simplejson as json
import urllib, urllib2, datetime
from Twequency import get_friends

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class FormHandler(tornado.web.RequestHandler):
    def get(self):
        # arguments is a dict of key:value pairs where each value is a
        # list (even if there is only one item). 
        arguments = self.request.arguments
        print 'Arguments were:'
        print arguments
        friends = get_friends(arguments['username'][0])       
        print friends
        self.render('results.html', friends=json.dumps(friends) )

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/submit', FormHandler),
        ], **settings)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
