from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
# from django.contrib.auth.models import Project


# Create your views here.

def entry_point(request):
    return render(request, 'projects/entry_point.html')

#Show all Projects
def viewProjects(request):
#     projects = Project.objects.all()
#     return render(request, 'projects/viewProjects.html', {'projects':projects})
    pass 

#Create new Project
def createProject(request):
    pass

