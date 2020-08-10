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
# Function to search for the content in tweets
def searchContent(word):
    tweets_result =[]

    for tweet in Twitter.query().order(-Twitter.timestamp):
        if word in tweet.tweet.split():
            tweets_result.append(tweet)
        else:
            continue
    return tweets_result

class SearchContent(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        # Get the content that needs to be searched
        searchcontent = self.request.get('search')
        # fetch the tweets with successful match
        tweets_result = searchContent(searchcontent)
        result_len = len(tweets_result)

        template_values= {'result_len':result_len,'tweet_result':tweets_result}
        template = JINJA_ENVIRONMENT.get_template('searchcontent.html')
        self.response.write(template.render(template_values))
