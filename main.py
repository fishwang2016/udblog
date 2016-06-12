#!/usr/bin/env python
#Udacity Nano degree project
#
import webapp2
import os
import urllib
import jinja2
import logging

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape =True)

from google.appengine.ext import db

class Post(db.Model):
    title = db.StringProperty(required =True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
    def write(self,output):
        self.response.write(output)
    def render_str(self,template,**kw ):
        t = jinja_env.get_template(template)
        return t.render(kw) 
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class LoginHandler(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        email = self.request.get("email")
        if username and password:
            self.write("thanks!")
        else:
            error ="Both User Name and Password are required! Try again!"
            self.render("login.html",username=username, password=password,error=error)

class AboutHandler(Handler):
    def get(self):
        self.render("about.html")

class EditHandler(Handler):
    def get(self):
        self.render("edit.html")
        
    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        if title and content:
            post =Post(title=title, content=content)
            post.put()
            self.redirect("/")
        else:
            error ="Both title and content are requried!! Please check."
            self.render("edit.html",title =title,content=content,error=error)

class PostHandler(Handler):
    def get(self,post_id):#the mapping url id will go here
        post_id= int(post_id)
        try:
           post =Post.get_by_id(post_id)
           if post:
               self.render("post.html",post=post) 
           else:
               self.write("no page found 404")
        except:
           self.write("no page found!404")


class MainHandler(Handler):
    def render_front(self,title="",content="",error=""):
        posts = db.GqlQuery("SELECT * From Post  ORDER by created DESC")
        for post in posts:
            logging.info(post.key().id())
        self.render("index.html",title=title,content=content,error=error,posts = posts)   

    def get(self):
        self.render_front()



app = webapp2.WSGIApplication([
 ('/login',LoginHandler), ('/about',AboutHandler), ('/edit',EditHandler),   ('/', MainHandler),(r'/(\d+)',PostHandler)
], debug=True)
