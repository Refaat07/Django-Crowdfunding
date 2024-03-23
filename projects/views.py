from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from projects.models import Project,Picture,User,Category,Tag
from projects.forms import CreateProjectModelForm,EditProjectModelForm

# Create your views here.
def entry_point(request):
    return render(request, 'projects/entry_point.html')

def index(request):
    projects = Project.objects.all()
    return render(request,'projects/index.html',context={"projects":projects})

def show(request,id):
    project = Project.objects.get(id=id)
    return render(request, 'projects/show.html', context= {"project":project})

@login_required(login_url='/users/login')
def create(request):
    form = CreateProjectModelForm()
    if request.method == 'POST':
        form = CreateProjectModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False,creator=request.user)
            return redirect('project.index')
    return render(request, 'projects/forms/create.html',context={"form":form})

@login_required(login_url='/users/login')
def edit(request, id):
    project = Project.objects.get(id=id)
    form = EditProjectModelForm(instance=project)
    if project.creator.id == request.user.id:
        if request.method == 'POST':
            form = EditProjectModelForm(request.POST, request.FILES, instance=project)
            if form.is_valid():
                form.save(commit=False)
                return redirect("project.index")
        return render(request, 'projects/forms/edit.html',context={"form":form})
    return redirect("project.index")


@login_required(login_url='/users/login')
def delete(request,id):
    project = Project.objects.get(id=id)
    if project.creator.id == request.user.id:
        if project.delete():
            return redirect("project.index")
        return redirect("project.index")
    return redirect("project.index")