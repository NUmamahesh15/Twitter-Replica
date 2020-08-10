import webapp2;
import os;
import jinja2;
import random;
from google.appengine.ext import ndb;
from google.appengine.api import users
from myuser import MyUser
from registration import Registration
from editprofile import EditProfile
from addtweet import AddTweet
JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'],
autoescape = True
)

class EditTweet(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        tweet_id = self.request.params.items()[0][1]
        # Fetching the tweet entity to be updated
        update_mytweet_key = ndb.Key('Twitter',tweet_id)
        update_mytweet = update_mytweet_key.get()

        template_values={'message' :"EDIT TWEET","my_tweet":update_mytweet.tweet,'tweet_id':tweet_id}
        template = JINJA_ENVIRONMENT.get_template('edittweet.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        id = self.request.params.items()[0][1]

        if action == 'UPDATE':
            # Successfully update the tweet if action is UPDATE
            update_mytweet_key = ndb.Key('Twitter',id)
            update_mytweet = update_mytweet_key.get()
            update_mytweet.tweet = self.request.get('tweet')
            update_mytweet.put()
            self.redirect('/')
        elif action == 'CANCEL':
            # Redirect to home page in case the user does not want to update the tweet
            self.redirect('/')
