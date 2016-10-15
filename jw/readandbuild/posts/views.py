from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse()

def post_create(request):
    return HttpResponse("<h1>Welcome</h1><p>readandbuild.howapped.com</p><p>Create</p>");

def post_detail(request): # read
    return HttpResponse("<h1>Welcome</h1><p>readandbuild.howapped.com</p><p>Delete</p>");

def post_list(request):
    return render(request, "posts/list.html",{})
    #return HttpResponse("<h1>Welcome</h1><p>readandbuild.howapped.com</p><p>List</p>");


def post_update(request):
    return HttpResponse("<h1>Welcome</h1><p>readandbuild.howapped.com</p><p>Update</p>");

def post_delete(request):
    return HttpResponse("<h1>Welcome</h1><p>readandbuild.howapped.com</p><p>Delete</p>");