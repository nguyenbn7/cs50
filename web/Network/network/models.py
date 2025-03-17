from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey("User", models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} say: {self.content}"

    def is_valid(self):
        return self.content is not None and self.content != "" and self.user is not None


class Like(models.Model):
    user = models.ForeignKey("User", models.CASCADE)
    post = models.ForeignKey("Post", models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True)
    unliked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.post}"


class Follow(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user")
    follower = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="follower")
    followed_date = models.DateTimeField(auto_now_add=True)
    unfollowed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.follower}"
