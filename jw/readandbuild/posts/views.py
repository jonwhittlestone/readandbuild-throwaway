from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
# Create your views here.

def post_list(request):

    queryset = Post.objects.active()
    context = {
        "object_list": queryset
    }
    return render(request, "posts/list.html",context)

def post_create(request):
    return render(request, "posts/create.html",{})

def post_detail(request): # read
    return HttpResponse("<h1>Welcome</h1><p>readandbuild.howapped.com</p><p>Delete</p>");



def post_update(request):
    return HttpResponse("<h1>Welcome</h1><p>readandbuild.howapped.com</p><p>Update</p>");

def post_delete(request):
    return HttpResponse("<h1>Welcome</h1><p>readandbuild.howapped.com</p><p>Delete</p>");