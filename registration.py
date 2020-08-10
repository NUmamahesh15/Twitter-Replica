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

class Registration(webapp2.RequestHandler):
# GET display the form for editing with pre-populated user information
    def get(self):
        message = "Register Yourself before getting started!!"
        user= users.get_current_user()
        template_values = {'message':message}
        template = JINJA_ENVIRONMENT.get_template('registration.html')
        self.response.write(template.render(template_values))

    def post(self):
        action = self.request.get('button')
        user= users.get_current_user()
        if action == 'SUBMIT':
# Fetch the user profile that needs to be updated
            current_user_key = ndb.Key('MyUser',user.user_id())
            current_user = current_user_key.get()
# updating the user information with updated information entered by the user
            current_user.userName = self.request.get('username')
            current_user.dob = datetime.strptime(self.request.get('dob'),'%Y-%m-%d')
            current_user.location = self.request.get('location')
            current_user.gender = self.request.get('mygender')
            current_user.aboutMe = self.request.get('message')

            current_user.put()
            self.redirect('/')

        template_values = {'message':"User Registered successfully"}
        template = JINJA_ENVIRONMENT.get_template('registration.html')
        self.response.write(template.render(template_values))
