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
from twitter import Twitter
from edittweet import EditTweet
from searchprofile import SearchProfile
from profiledisplay import ProfileDisplay
from searchcontent import SearchContent

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'],
autoescape = True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        if user == None:
            template_values = {
            'login_url' : users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('mainpage_guest.html')
            self.response.write(template.render(template_values))
            return
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser == None:
            myuser = MyUser(userEmail=user.email(),id=user.user_id())
            myuser.put()

            # Redirecting the user to registration page in case the user is first time user to twitter.
            template_values ={'myuser':myuser,'message':"Register yourself before getting started!!"}
            template = JINJA_ENVIRONMENT.get_template('registration.html')
            self.response.write(template.render(template_values))
            return

        # mytweets_key = ndb.Key('Twitter',myuser.userName)
        # my_tweet = mytweets_key.get()

        # Fetch all the following users list to display their tweets on the home page.
        followingList = myuser.followingUsers
        # Appending the current user to the list to fetch their own tweets as well
        followingList.append(myuser.userName)
        # Fetch all the tweets for users in the followingList
        my_tweets = Twitter.query()
        my_tweets = my_tweets.filter(Twitter.userName.IN(followingList))
        # Ordering the tweets based on their timestamp in reverse chronological order
        my_tweets = my_tweets.order(-Twitter.timestamp)


        template_values = {
            'logout_url' : users.create_logout_url(self.request.uri),
            'user':user,
            'myuser':myuser,
            'followTweet':my_tweets.fetch(50), #fetches the first 50 recent tweets from the result tweet list of all following users
            'myuser':myuser,
            'followingLen':len(myuser.followingUsers),
            'followedLen':len(myuser.followedUsers)
            }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        # Fetching the ID of the tweet that needs to be editted
        key_id = str(self.request.params.items()[0][1])
        # Fetching the tweet that need to be updated/deleted
        mytweet_key = ndb.Key('Twitter',key_id)
        mytweet = mytweet_key.get()

        # Deleting the tweet if the action is DELETE
        if action == 'DELETE':
            mytweet.key.delete()
            self.redirect('/')

        # editing the tweet if action is edit
        elif action == "EDIT":
            # Redirecting to edit tweet page for editing the tweet. Passing ID of the tweet that needs to be editted.
            query = "name ={0}".format(key_id)
            self.redirect('/edittweet?'+query)


app = webapp2.WSGIApplication([('/',MainPage),('/registration',Registration),('/addtweet',AddTweet),('/editprofile',EditProfile),
                                ('/searchprofile',SearchProfile),('/profiledisplay',ProfileDisplay),('/searchcontent',SearchContent),
                                ('/edittweet',EditTweet)],debug=True)
