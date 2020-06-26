from django.db.models.manager import BaseManager
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Blog, Post

class BlogView(View):
    
    @method_decorator(login_required)    
    def get(self, request:HttpRequest):
        context = {
            "blogs": Blog.objects.all()
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
    
