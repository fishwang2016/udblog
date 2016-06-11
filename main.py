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
class PostHandler(Handler):
    def get(self,post_id):#the mapping url id will go here
        post =Post.get(post_id)
        logging.info(post)
        self.write(post.content)


class MainHandler(Handler):
    def render_front(self,title="",content="",error=""):
        posts = db.GqlQuery("SELECT * From Post ORDER by created DESC")
        self.render("index.html",title=title,content=content,error=error,posts = posts)   
    def get(self):
        self.render_front()
    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        if title and content:
            post =Post(title=title, content=content)
            post.put()
            self.redirect("/")


        else:
            error ="Both title and content are requried!! Please check."
            self.render_front(title =title,content=content,error=error)

app = webapp2.WSGIApplication([
    ('/', MainHandler),(r'/(.*)',PostHandler)
], debug=True)
