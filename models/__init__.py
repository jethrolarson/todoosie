'''
Created on Jul 31, 2009

@author: Brad Boswell
'''
from google.appengine.ext import db

class User(db.Model):
  user = db.UserProperty(auto_current_user=True)
  created = db.DateTimeProperty(auto_now_add=True)


class TaskList(db.Model):
  created = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now=True)
  name = db.StringProperty(default="untitled list")
  firstTaskOrder = db.IntegerProperty()
  taskCount = db.IntegerProperty()
  activeTaskCount = db.IntegerProperty()
  insertAtBottom = db.BooleanProperty()
  owner = db.ReferenceProperty(User)
  
class Contributer(db.Model):
  user = db.UserProperty(auto_current_user_add=True)
  #taskLists? since a user may have more than one list.
  taskList = db.ReferenceProperty(TaskList, collection_name="contributers")


class Task(db.Model):
  text = db.StringProperty(default="")
  order = db.IntegerProperty()
  done = db.BooleanProperty(default=False)
  created = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now=True)
  completed = db.DateTimeProperty()
  deleted = db.DateTimeProperty()
  taskList = db.ReferenceProperty(TaskList, collection_name="tasks")
  contributer = db.ReferenceProperty(Contributer, collection_name="contributer")
