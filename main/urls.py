from django.urls import path
from .views import BlogView, NewsView, PostView

urlpatterns = [
    path('blogs', BlogView.as_view()),
    path('news', NewsView.as_view()),
    path('post', PostView.as_view())
]