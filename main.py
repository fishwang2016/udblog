#!/usr/bin/env python
#Udacity Nano degree project
#
import webapp2
import os
import urllib

import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class Handler(webapp2.RequestHandler):
    def write(self,output):
        self.response.write(output)
    def render_str(self,template,**kw ):
        t = jinja_env.get_template(template)
        return t.render(kw) 
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))
import logging
class MainHandler(Handler):
    def get(self):
        self.render('index.html')
    def post(self):
        
        title = self.response.get("title")
        content = self.response.get("conent")
        logging.info(title)
        logging.info(content)
        self.render('index.html',title =title,content=content)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
