from django.db import models
from google.appengine.ext import db
from google.appengine.api import users


class Post(db.Model):
    title = db.StringProperty(default='No-Title')
    body = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty()

    def __unicode__(self):
        return self.title
    
    def get_key(self):
        return '%s' % self.key()


class Comment(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)
    author = db.StringProperty(default='Anonymous')
    body = db.TextProperty()
    post = db.ReferenceProperty(Post)

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))
    
    def get_key(self):
        return '%s' % self.key()

  
