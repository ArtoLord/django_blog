import blog
from django.db.models.manager import BaseManager
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Blog, Post
from .forms import PostForm

class BlogView(View):
    
    @method_decorator(login_required)
    def get(self, request:HttpRequest):
        blogs = map(lambda blog: (blog, blog.subscribers.filter(id = request.user.id)), Blog.objects.all())
        context = {
            "blogs": blogs
        }
        return render(request, 'main/blog_list.html', context)
    
    @method_decorator(login_required)
    def post(self, request:HttpRequest):
        blog_id = request.POST.get("id")
        if not blog_id:
            return HttpResponseBadRequest()
        
        blog_set: BaseManager[Blog] = Blog.objects.filter(id=blog_id)
        if not blog_set:
            return HttpResponseBadRequest()
        
        blog = blog_set.get()
        if not blog.subscribers.filter(id = request.user.id):
            blog.subscribers.add(request.user)
        else:
            blog.subscribers.remove(request.user)
        blog.save()
        
        return HttpResponse()

class NewsView(View):
    
    @method_decorator(login_required)
    def get(self, request:HttpRequest):
        
        posts = Post.objects.filter(blog__subscribers__in=[request.user]).order_by("created_at").reverse()
        
        posts = map(lambda post: (post, post.viewed_by.filter(id = request.user.id)), posts)
        
        context = {
            "posts": posts
        }
        return render(request, 'main/news.html', context)
    
class PostView(View):
    
    @method_decorator(login_required)    
    def get(self, request:HttpRequest):
        post_id = request.GET.get("id")
        if not post_id:
            return HttpResponseBadRequest()
        
        post_set = Post.objects.filter(id=post_id)
        if not post_set:
            return HttpResponseBadRequest()
        post: Post = post_set.get()
        
        return render(request, 'main/post.html', {"post": post})
    
    @method_decorator(login_required)
    def post(self, request:HttpRequest):
        
        post_id = request.POST.get("id")
        if not post_id:
            return HttpResponseBadRequest()
        
        post_set = Post.objects.filter(id=post_id)
        if not post_set:
            return HttpResponseBadRequest()
        post: Post = post_set.get()
        
        if post.viewed_by.filter(id = request.user.id):
            post.viewed_by.remove(request.user)
            post.save()
            return HttpResponse("false")
        post.viewed_by.add(request.user)
        post.save()
        return HttpResponse('true')

class CreatePost(View):
    
    @method_decorator(login_required)    
    def get(self, request:HttpRequest):
        return render(request, 'main/create_post.html', {"form": PostForm()})
    
    @method_decorator(login_required)    
    def post(self, request:HttpRequest):
        post = PostForm(request.POST)
        if not post.is_valid():
            return HttpResponseBadRequest()
        blog = request.user.blog
        Post.objects.create(header=post.data['header'], body=post.data['body'], blog=blog)
        return HttpResponseRedirect("/")
    