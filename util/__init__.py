from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

def login_required(func):
  def wrapper(self, *args, **kw):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
    else:
      func(self, *args, **kw)
  return wrapper

def isAjax(rh):
  try:
    return rh.request.headers["X-Requested-With"] == "XMLHttpRequest"
  except:
    return False

def error(rh,code,message):
  rh.error(code)
  if isAjax(rh):
    rh.response.out.write(str(code)+": " + message)
  else:
    rh.response.out.write(template.render("views/error.html", {"message":message, "code":code}))
    
class Error404(webapp.RequestHandler):
  def get(self):
    util.error(self,404,"Page not found")