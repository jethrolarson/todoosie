import cgi, wsgiref.handlers, random, logging, yaml
from django.utils import simplejson as json
from google.appengine.api import users, mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from datetime import datetime

import  models, util
from controllers import TaskList, Task

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render("views/default.html", {}))

application = webapp.WSGIApplication([
    ('/',MainPage),
    ('/list/new', TaskList.Create),
    (r'/list/([^/?]+)/add',Task.Create),
    (r'/list/([^/?]+)/update',TaskList.Update),
    (r'/list/([^/?]+).xml',TaskList.RSS),
    (r'/list/([^/?]+)/order',TaskList.Order),
    (r'/list/([^/?]+)',TaskList.Index),
    ('/task/update',Task.Update),
    #(r'/list/([^/?]+)/secure',MakePrivate),
    #('/user/new',User.New),
    ('.*',util.Error404)
  ],
  debug=True)

def main():
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__': main()
