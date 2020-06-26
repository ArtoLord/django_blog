from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, related_name="subscribes")
    
class Post(models.Model):
    header = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    viewed_by = models.ManyToManyField(User, related_name="viewed_posts")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="posts")
    