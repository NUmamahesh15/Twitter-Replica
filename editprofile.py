import webapp2
import os
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from myuser import MyUser
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'],
autoescape = True
)

class EditProfile(webapp2.RequestHandler):
# GET fetches the form for editing
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # Fetching the form to update current user information with users information pre-populated.
        user = users.get_current_user()
        user_key = ndb.Key("MyUser",user.user_id())
        myuser = user_key.get()

        template_values ={
        'myuser' : myuser
        }

        template = JINJA_ENVIRONMENT.get_template('editprofile.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        # Check for an action- Update/Cancel
        if action == 'UPDATE':
            user = users.get_current_user()
            user_key = ndb.Key("MyUser",user.user_id())
            cur_myuser = user_key.get()
            # Updating the information provided by the user
            cur_myuser.dob = datetime.strptime(self.request.get('dob'),'%Y-%m-%d')
            cur_myuser.location = self.request.get('location')
            cur_myuser.gender = self.request.get('mygender')
            cur_myuser.aboutMe = self.request.get('message')
            cur_myuser.put()
            self.redirect('/')
        elif action == 'CANCEL':
            self.redirect('/')
