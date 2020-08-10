from google.appengine.ext import ndb
class MyUser(ndb.Model):
    userName = ndb.StringProperty()
    aboutMe = ndb.StringProperty()
    dob = ndb.DateProperty()
    gender = ndb.StringProperty()
    location = ndb.StringProperty()
    userEmail = ndb.StringProperty()
    followedUsers = ndb.StringProperty(repeated = True)
    followingUsers = ndb.StringProperty(repeated=True)
