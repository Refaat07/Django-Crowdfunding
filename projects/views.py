from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.
def entery_point(request):
    return render(request, 'projects/entry_point.html')

def home_index(request):
    url = reverse('projects.home')
    return redirect(url)    