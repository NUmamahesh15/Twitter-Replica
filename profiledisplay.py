import webapp2;
import os;
import jinja2;
import random;
from google.appengine.ext import ndb;
from google.appengine.api import users
from myuser import MyUser
from twitter import Twitter
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'],
autoescape = True
)

# Function to check if the user is in the following list
def checkFollowing(user, followingList):
    flag = False
    for userName in range(len(followingList)):
        if str(followingList[userName]) == user:
            flag = True
    return flag


class ProfileDisplay(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = str(self.request.params.items()[0][1])
        # Fetch current users information
        cur_user = users.get_current_user()
        cur_user_key = ndb.Key('MyUser',cur_user.user_id())
        current_user = cur_user_key.get()
# To fetch the ID of the searched user
        query_user = MyUser.query()
        query_user = query_user.filter(MyUser.userName == user).fetch(keys_only=True)
        searched_user_id = query_user[0].id()
# to fetch the user profile using the ID retrieved.
        searched_user_key = ndb.Key('MyUser',searched_user_id)
        searched_user = searched_user_key.get()
# check if the user exists in the current users following list
        check_user_exists = checkFollowing(searched_user.userName, current_user.followingUsers)
# Retrieving the tweets of the searched user
        userTweet = Twitter.query().filter(Twitter.userName==searched_user.userName).order(-Twitter.timestamp)

        template_values = {'searched_user':searched_user,'exists':check_user_exists,'user_tweets':userTweet.fetch(50),'current_user':current_user,
                            'followingLen':len(searched_user.followingUsers),'followedLen':len(searched_user.followedUsers)}
        template = JINJA_ENVIRONMENT.get_template('profiledisplay.html')
        self.response.write(template.render(template_values))
#
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        # Fetch the current users details
        cur_user = users.get_current_user()
        cur_user_key = ndb.Key('MyUser',cur_user.user_id())
        current_user = cur_user_key.get()
        # Get the ID of the user who needs to be followed
        user = str(self.request.params.items()[0][1])
        query_user = MyUser.query()
        query_user = query_user.filter(MyUser.userName == user).fetch(keys_only=True)
        searched_user_id = query_user[0].id()
# get the user profile
        searched_user_key = ndb.Key('MyUser',searched_user_id)
        searched_user = searched_user_key.get()

        if action == 'FOLLOW':
# append the userName to the followingUsers list of the current user
            current_user.followingUsers.append(user)
            current_user.put()
# append the userName to the followedUsers list of the searched user
            searched_user.followedUsers.append(current_user.userName)
            searched_user.put()

            # self.redirect('/profiledisplay')

        elif action == "UNFOLLOW":
# Remove the user from the followingUsers list of the current user
            current_user.followingUsers.remove(user)
            current_user.put()
# Remove the user from the followedUsers list of the searched user
            searched_user.followedUsers.remove(current_user.userName)
            searched_user.put()
        query = "name ={0}".format(searched_user.userName)
        self.redirect('/profiledisplay?'+query)
