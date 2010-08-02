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
        friends = get_friends(self.username)       
        print friends[1]
        img_url = self.make_chart(friends)
        print img_url
        self.render('results.html', username = self.username, friends=friends, 
                    url=settings["url"], chart_url = img_url )


    def make_chart(self, friends):
        # create a unique filename for this user and this particular friend
        # set. if the user or friendset changes, the filename won't match. 
        sum_f = sum([friend[1]['frequency'] for friend in friends])
        uid_file = '/tmp/' + self.username + str(sum_f)  + '.png'
        # the app will access this file via a url in the static media
        # directory:
        img_path = '/static/charts/' + uid_file[5:]

        if os.path.exists(uid_file):
            return img_path
        
        names_list = [friend[0] for friend in friends]
        names = ','.join(names_list)
        percents_list = [str(friend[1]['percent']) for friend in friends]
        percents = 't:' + ','.join(percents_list)
        # round up to the nearest 10
        max_percent = max(friend[1]['percent'] for friend in friends])
        max_y = 10*((max_percent/10)+1)

        base_url = "http://chart.apis.google.com/chart?"
        args = {
            'cht' : 'ls',
            'chs' : '600x200',
            'chxt' : 'x,y',
            'chd' : percents,
            'chds' : max_y
        }

        print base_url + urllib.urlencode(args)
        fp = urllib2.urlopen(base_url, urllib.urlencode(args))
        chart = open(uid_file, 'w')
        chart.write(fp.read())
        chart.close()

        return img_path

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
