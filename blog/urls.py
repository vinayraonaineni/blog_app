from django.conf.urls.defaults import *
from blog.models import *

urlpatterns = patterns('blog.views',
   (r"^post/(?P<post_key>[^\.^/]+)/$", 'post'),
   (r"^add_comment/(?P<post_key>[^\.^/]+)/$", "add_comment"),
   (r"^delete_comments/(?P<post_key>[^\.^/]+)/$", "delete_comments"),
   (r"^delete_comment/(?P<post_key>[^\.^/]+)/(?P<comment_key>[^\.^/]+)/$", "delete_comment"),   
   (r"^add_post/$", "add_post"),
   (r"^delete_post/(?P<post_key>[^\.^/]+)/$", "delete_post"),
   (r"^edit_post/(?P<post_key>[^\.^/]+)/$", "edit_post"),
   
   (r"", "main"),
)
