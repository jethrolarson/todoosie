from google.appengine.ext import webapp,db
from google.appengine.ext.webapp import template
import models, util, logging, sys
from datetime import datetime
class Create(webapp.RequestHandler):
  def post(self,tlkey):
    try:
      tlist = db.get(db.Key(tlkey))
      pos=0
      if tlist.insertAtBottom:
        pos = tlist.firstTaskOrder + tlist.taskCount
      else:
        pos = tlist.firstTaskOrder - 1
        tlist.firstTaskOrder -= 1
      
      #book keeping on the list
      tlist.taskCount+=1
      tlist.activeTaskCount+=1
      #put the task list to ensure it has a key
      tlist.put()
      
      task = models.Task(
        taskList = tlist,
        order = pos,
      )
      
      task.put()
      if util.isAjax(self):
        self.response.out.write(template.render("views/task.html", {"tl":tlist, "task":task}))
      else:
        self.redirect("/list/"+str(tlist.key()))
    except:
      logging.error(sys.exc_info())
      util.error(self,500,"Something went wrong on our end when creating the todo, please try again")

class Update(webapp.RequestHandler):
  def post(self):
    try:
      tkey=self.request.get("tkey")
      task = db.get(db.Key(tkey))
      task.done = self.request.get("done")=="on"
      if self.request.get("text"):
        task.text = self.request.get("text")
      if self.request.get("delete"):
        task.deleted = datetime.utcnow()
      task.put()
      if util.isAjax(self):
        if task.deleted:
          self.response.out.write("deleted")
        else: 
          self.response.out.write(template.render("views/task.html", {"task":task}))
      else:
        self.redirect("/list/"+str(task.taskList.key())) 
    except:
      logging.error(sys.exc_info())
      util.error(self,500,"Something went wrong on our end when updating the todo, please try again")