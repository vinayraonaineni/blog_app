from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse

from blog.models import *
from google.appengine.ext.db import djangoforms
from django import shortcuts
from google.appengine.api import users
import os


class PostForm(djangoforms.ModelForm):
    class Meta:
        model = Post
        exclude = ["user"]


class CommentForm(djangoforms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post","created"]


def edit_post(request, post_key):
    """ Edit and existing post """     

    user = users.get_current_user()   
    post = Post.get(post_key)    
            
    if request.method == 'POST':
        
        if request.POST.has_key("body") and request.POST["body"]:                        
            title = "No-Title"
            if request.POST["title"]: title = request.POST["title"]
            pf = PostForm(request.POST, instance=post) 
            if pf.is_valid(): 
                post = pf.save(commit=False)
                post.title = title
                post.put()
            return HttpResponseRedirect(reverse("blog.views.post", args=[post_key])) 
    
    form = PostForm(instance=post)
    params = dict(post=post, form=form, edit = True)
    return respond(request, user,'post_form.html',params)
    
    
def post(request,post_key):
    """Single post with comments and a comment form."""
    
    user = users.get_current_user()
    post = Post.get(post_key)
    comments = list(post.comment_set)
    can_editdelete = False
    if user == post.user or users.is_current_user_admin():
        can_editdelete = True
    
    params = dict(post=post,  comments=comments, form=CommentForm(),
                  can_editdelete = can_editdelete)
    return respond(request, user, "post.html", params)


def add_post(request):
    """Add a new post."""
    
    user = users.get_current_user()
    if not user:
        return HttpResponseRedirect( users.create_login_url(request.get_full_path()))

    if request.method == 'POST':
        
        if request.POST.has_key("body") and request.POST["body"]:            
            title = "No-Title"
            if request.POST["title"]: title = request.POST["title"]
            pf = PostForm(data= request.POST)
            if pf.is_valid():
                # Save the data, and redirect to the view page
                post = pf.save(commit=False)
                post.user = user
                post.title = title
                post.put()
            return HttpResponseRedirect(reverse("blog.views.main"))
   
    form = PostForm() # An new form
    params = dict(form = form)
    return respond(request, user,'post_form.html', params)

    
def delete_post(request, post_key):
    """Delete post with primary key `pk` """
    
    post = Post.get(post_key)
    post.delete()
    return HttpResponseRedirect(reverse("blog.views.main"))
    

def delete_comments(request, post_key):
    """Delete selected comment's in POST form"""
    
    cmnt_keys = request.POST.getlist("delete")
    
    for comment_key in cmnt_keys:
        Comment.get(comment_key).delete()
    return HttpResponseRedirect(reverse("blog.views.post", args=[post_key]))

    
def delete_comment(request, post_key, comment_key):
    """Delete single comment for key = comment_key."""
    
    Comment.get(comment_key).delete()
    return HttpResponseRedirect(reverse("blog.views.post", args=[post_key]))


def add_comment(request, post_key):
    """Add a new comment."""

    p = request.POST
    if p.has_key("body") and p["body"]:
        author = "Anonymous"
        if p["author"]: author = p["author"]
        post=Post.get(post_key)
       
        cf = CommentForm(data = request.POST)       
        if cf.is_valid(): 
            comment = cf.save(commit=False)
            comment.post = post
            comment.author = author 
            comment.put()        

    return HttpResponseRedirect(reverse("blog.views.post", args=[post_key]))
    

def main(request):
    """Main listing of Posts and a PostForm"""
    
    user = users.get_current_user()
    posts = Post.all().order("-created")    
    params = dict(posts=posts)
       
    return respond(request, user, "list.html", params)


def respond(request, user, template, params=None):
  """Helper to render a response, passing standard stuff to the response.

  Args:
    request: The request object.
    user: The User object representing the current user; or None if nobody
      is logged in.
    template: The template name; '.html' is appended automatically.
    params: A dict giving the template parameters; modified in-place.

  Returns:
    Whatever render_to_response(template, params) returns.

  Raises:
    Whatever render_to_response(template, params) raises.
  """
  if params is None:
    params = {}
  
  
  if user:
    params['user'] = user
    params['sign_out'] = users.create_logout_url('/')
    params['is_admin'] = (users.is_current_user_admin() and
                          'Dev' in os.getenv('SERVER_SOFTWARE'))
  else:
    params['sign_in'] = users.create_login_url(request.path)
    
  if not template.endswith('.html'):
    template += '.html'
    
  return shortcuts.render_to_response(template, params)



