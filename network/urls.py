
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addPost", views.addPost, name="addPost"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("edit/<int:postId>", views.edit, name="edit"),
    path("addLike/<int:postId>/", views.addLike, name="addLike"),
    path("removeLike/<int:postId>/", views.removeLike, name="removeLike")







]
