from django.urls import path
from . import views

urlpatterns = [
    # path("", views.starting_page, name="starting-page"),
    path ("", views.StartingPageView.as_view(), name= "starting-page"),
    
    path("posts", views.posts, name="post-page"),
    # path("posts2", views.AllPostView.as_view(), name="post-page"),
    
    # path("posts/<slug:slug>", views.post_detail, name="post-detail-page"), # /posts/my-first-page -> here slug is: my-first-page
    path("posts/<slug:slug>", views.SinglePostView.as_view(), name= "post-detail-page"),
    
    path("read-later", views.ReadLaterView.as_view(), name="read-later")
]