import webapp2;
import os;
import jinja2;
import random;
from google.appengine.ext import ndb;
from google.appengine.api import users
from myuser import MyUser
from registration import Registration
from twitter import Twitter
import calendar
import time

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'],
autoescape = True
)

class AddTweet(webapp2.RequestHandler):
    def post(self):
        # Fetch current user information
        user = users.get_current_user()
        user_key = ndb.Key('MyUser',user.user_id())
        user_info = user_key.get()

        action = self.request.get('button')
        # If the action is POST then we create a new tweet
        if action == 'POST':
            tweet_info = self.request.get('tweet');
            # Create new tweet
            new_tweet = Twitter(userName = user_info.userName,id=user_info.userName+"/"+str(calendar.timegm(time.gmtime())))
            new_tweet.tweet = tweet_info
            new_tweet.put()
            # Redirect to home page after posting a tweet
            self.redirect('/')

        elif action == 'CANCEL':
            # redirect to home page upon cancellation
            self.redirect('/')
