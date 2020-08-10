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

class SearchProfile(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        profileSearch = self.request.get('search')

        check_profile = MyUser.query().filter(MyUser.userName==profileSearch).fetch(keys_only=True)
        if(len(check_profile )== 0):
            message = "fail"
            template_values= {'message':message}
            template = JINJA_ENVIRONMENT.get_template('searchprofile.html')
            self.response.write(template.render(template_values))
        else:
            search_user_key = ndb.Key('MyUser',check_profile[0].id())
            searched_user_profile = search_user_key.get()
            message = "success"
            template_values= {'search':profileSearch,'message':message,'profile':searched_user_profile,}
            template = JINJA_ENVIRONMENT.get_template('searchprofile.html')
            self.response.write(template.render(template_values))
