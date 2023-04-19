from django.urls import path

from . import views

urlpatterns = [
    path("", views.StartingPage.as_view(), name="starting-page"),
    path("posts", views.ALLPosts.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.Post_Detail.as_view(),
         name="post-detail-page"),  # /posts/my-first-post
    path("read-later", views.ReadLater.as_view(), name = "read-later"),
]
