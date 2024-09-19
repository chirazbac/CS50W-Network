from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Post(models.Model):
    content = models.TextField(blank=False)
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_followed")
    user_follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_following")

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_like")
