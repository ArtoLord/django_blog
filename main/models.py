from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import send_mail
from typing import Type
from blog.settings import HOSTNAME



class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, related_name="subscribes")
    
class Post(models.Model):
    header = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    viewed_by = models.ManyToManyField(User, related_name="viewed_posts")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="posts")
    
def user_create_handler(sender: Type[User], instance: User, created: bool, **kwargs):
    if created:
        Blog.objects.create(author=instance)

def post_create_handler(sender: Type[Post], instance: Post, created: bool, **kwargs):
    if created:
        users_email = map(lambda user: user.email, instance.blog.subscribers.all())
        send_mail(
            'New post',
            f'Hello, this is new post in blog: https://{HOSTNAME}/post?id={instance.id}',
            'django_blog@example.com',
            users_email,
            fail_silently=False,
        )

post_save.connect(user_create_handler, sender=User, weak=False, dispatch_uid="models.user_create_handler")
post_save.connect(post_create_handler, sender=Post, weak=False, dispatch_uid="models.post_create_handler")