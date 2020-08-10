from google.appengine.ext import ndb
class Twitter(ndb.Model):
    tweet = ndb.StringProperty()
    userName = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now=True)
