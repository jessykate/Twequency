#!/usr/bin/python

# A template for a Tornado project using forms and MongoDB as the
# backend: takes a form submission and stores it as a record in a
# Mongo DB. Don't forget to start Mongo first with the "mongod"
# command.
#
# To run:
# ./main.py
# and visit localhost:8888

DEBUG = False

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
from lesstweets import get_friends

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
        self.username = self.get_argument('username')
        if DEBUG:
            print '** USING LOCAL CACHE **'
            friends = json.loads(open('friends.json').read())
        else:
            friends = get_friends(self.username)       
        print friends[1]

        per_day = sum([tup[1]['frequency'] for tup in friends])
        num_friends = len(friends)

        self.render('results.html', username = self.username, friends=friends, 
                    per_day=per_day, url=settings["url"])


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "url": "http://www.twitilitics.com",
}
application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/submit', FormHandler),
        ], **settings)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8100)
    tornado.ioloop.IOLoop.instance().start()
