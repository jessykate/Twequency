#!/usr/bin/python

'''
Shows twitter friends sorted by tweet frequency.
'''

import urllib, urllib2, datetime
try:
    import json
except:
    import simplejson as json


def list_members(username, list_id):
    members = {}
    cursor = -1
    base = "http://api.twitter.com/1/%s/%s/members.json" % (username, list_id)
    while cursor:
        args = urllib.urlencode({'cursor': cursor})
        fp = urllib2.urlopen(base+args)
        results = json.loads(fp.read())
        cursor = results['next_cursor']
        print "%d results in this API call" % len(results['users'])
        for user in results['users']:
            pass     

def get_friends(username):
    friends = {}
    results = True
    # cursor is used for paging until the value 0 is returned when
    # there are no more results.
    cursor = -1
    base = "http://api.twitter.com/1/statuses/friends.json?"
    while cursor:
        args = urllib.urlencode({'screen_name': username, 'cursor': cursor})
        fp = urllib2.urlopen(base+args)
        results = json.loads(fp.read())
        cursor = results['next_cursor']
        print "%d results in this API call" % len(results['users'])
        for user in results['users']:
            statuses = int(user['statuses_count'])
            dt = user['created_at']
            # slice out the timezone
            created_string = dt[:-11] + dt[-5:]
            created = datetime.datetime.strptime(created_string, "%a %b %d %H:%M:%S %Y")        
            days = (datetime.datetime.now() - created).days
            friends[user['screen_name']] = {
                'created': dt, #store the original string version 
                'statuses': statuses,
                # make frequency a float for those who tweet < once/day
                'frequency': float(statuses)/float(days)
                }

        # what percent of their daily tweets does this person represent?
        per_day = sum([v['frequency'] for v in friends.values()])
        for k,v in friends.iteritems():
            v['percent'] = v['frequency']/float(per_day)
        

    return sort_by_frequency(friends)

def _cmp(t1, t2):
    ''' each tuple has a name and then dict element: (name,
    {}). compare by the dict value of 'frequency' '''
    if t1[1]['frequency'] < t2[1]['frequency']:
        return -1
    if t1[1]['frequency'] > t2[1]['frequency']:
        return 1
    else: return 0

def sort_by_frequency(friends):    
    # f is a list of (name, {}) tuples
    f = zip(friends.keys(), friends.values())
    f.sort(_cmp, reverse=True)
    return f

if __name__ == '__main__':
    username = raw_input("enter your twitter handle: ")
    friends = get_friends(username)

    per_day = 0
    num_friends = 0
    for k,v in friends:        
        per_day += v['frequency']
        num_friends += 1

    # what percent of your daily tweets does this person represent?
    for k,v in friends:
        v['percent'] = v['frequency']/float(per_day)

    print "Screen Name\t\tFrequency/Day\t\tPercent/day"
    for k,v in friends:
        f = v['frequency']
        p = v['percent']
        print "%s\t\t%f\t\t%f" % (k, f, p)
    print ''    
    print 'average number of tweets you receive per day: %d' % per_day
    print "%d friends" % num_friends
