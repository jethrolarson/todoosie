from google.appengine.ext import webapp,db
from google.appengine.ext.webapp import template
import models, util, yaml, random
class Create(webapp.RequestHandler):
  def post(self):
    tname = self.request.get('name')
    tl = models.TaskList(
      name=tname,
      firstTaskOrder=1, 
      taskCount=1, 
      activeTaskCount=1, 
      insertAtBottom=True)
    tl.put()
    #add empty item
    task = models.Task(
      taskList = tl,
      text="",
      pos = 1
    ).put()
    
    self.redirect("/list/"+str(tl.key()))

class Index(webapp.RequestHandler):
  def get(self,tlkey):
    tl = None
    try:
      lKey = db.Key(tlkey);
      tl = db.get(lKey)
    except:
      util.error(self,404,"List doesn't exist. Are you using the right url?")
    if tl:
      tasks = models.Task.all().filter("taskList = ", lKey).order("order")
      tips = yaml.load(open("views/tips.yaml"))
      ranIndex = random.randrange(0, len(tips))
      tip = tips[ranIndex]
      self.response.out.write(template.render("views/list.html", {"tl":tl,"tasks":tasks, "tip":tip}))
    else:
      util.error(self,404,"List doesn't exist. Are you using the right url?")

  def post(self):
    print "TODO taskList updated"
    
class RSS(webapp.RequestHandler):
  #should only work if requesting an existing tasklist
  def get(self,tlkey):
    tl = db.get(db.Key(tlkey))
    if tl:
      self.response.headers["Content-type"] = "application/rss+xml"
      self.response.out.write(template.render("views/rss.html", {"tl":tl}))
    else:
      util.error(self,404,"List doesn't exist. Make sure you're using the right url.")
      
class Update(webapp.RequestHandler):
  def post(self,tlkey):
    try:
      name = self.request.get("name")
      tlist = db.get(db.Key(tlkey))
      tlist.name = name
      tlist.put()
      if util.isAjax(self):
        self.response.out.write("success")
      else:
        self.redirect("/list/"+str(tlist.key()))
    except:
      util.error(self,500,"There was a problem updating. Please go back and walk")

class Order(webapp.RequestHandler):
  def post(self, tlkey):
    listKey = db.Key(tlkey);
    tlist = db.get(listKey)
    tkey = db.Key(self.request.get("tkey"))
    oldOrder = int(self.request.get("pOrder"))
    newOrder = int(self.request.get("nOrder"))
    if tlist and oldOrder != newOrder:
      step = oldOrder > newOrder and 1 or -1
      tasksQ = models.Task.all().filter("taskList = ", listKey)
      if oldOrder > newOrder:
        tasksQ.filter("taskList = ", listKey).filter("order >= ", newOrder).filter("order < ", oldOrder)
      else:
        tasksQ.filter("taskList = ", listKey).filter("order <= ", newOrder).filter("order > ", oldOrder)
      
      taskMoving = db.get(tkey)
      tasks = tasksQ.fetch(tlist.taskCount)
      for task in tasks:  #there's an aritficial limit of 1000 here need to look at fixing it
        task.order += step
      taskMoving.order = newOrder
      
      #put all the tasks we just updated
      db.put(tasks) 
      taskMoving.put()
    
class MakePrivate(webapp.RequestHandler):
  @util.login_required  
  def post(self):
    print "TODO Attach Authentication to list"

