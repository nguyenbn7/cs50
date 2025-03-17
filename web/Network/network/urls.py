
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post/new", views.new_post, name="post_new"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like"),
    path("post/edit/<int:post_id>", views.edit, name="post_edit"),
    path("following", views.following_posts, name="following"),
]
