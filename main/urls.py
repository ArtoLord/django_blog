from django.urls import path
from .views import BlogView, NewsView, PostView, CreatePost

urlpatterns = [
    path('blogs', BlogView.as_view()),
    path('', NewsView.as_view()),
    path('post', PostView.as_view()),
    path('create_post', CreatePost.as_view())
]