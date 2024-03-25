from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from projects.models import Project,Picture,Category,Tag, Comment
from projects.forms import CreateProjectModelForm,EditProjectModelForm,NewCommentModelForm

# Create your views here.
def entry_point(request):
    return render(request, 'projects/entry_point.html')

def list_projects(request):
    projects = Project.objects.all()
    return render(request,'projects/index.html',context={"projects":projects})

def show_project(request,id):
    project = Project.objects.get(id=id)
    comments = project.comments.all()
    return render(request, 'projects/show.html', context= {"project":project, "comments": comments, 'newCommentForm': NewCommentModelForm})

@login_required(login_url='/users/login')
def create_project(request):
    form = CreateProjectModelForm()
    if request.method == 'POST':
        form = CreateProjectModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False,creator=request.user)
            return redirect('project_list')
    return render(request, 'projects/forms/create.html',context={"form":form})

@login_required(login_url='/users/login')
def edit_project(request, id):
    project = Project.objects.get(id=id)
    form = EditProjectModelForm(instance=project)
    if project.creator.id == request.user.id:
        if request.method == 'POST':
            form = EditProjectModelForm(request.POST, request.FILES, instance=project)
            if form.is_valid():
                form.save(commit=False)
                return redirect("project_list")
        return render(request, 'projects/forms/edit.html',context={"form":form})
    return redirect("project_list")

@login_required(login_url='/users/login')
def delete_project(request,id):
    project = Project.objects.get(id=id)
    if project.creator.id == request.user.id:
        if project.delete():
            return redirect("project_list")
        return redirect("project_list")
    return redirect("project_list")

def list_comments(request):
    pass

def create_comment(request):
    pass

def show_comment(request):
    pass

def edit_comment(request):
    pass

def delete_comment(request):
    pass

def list_reports(request):
    pass

def create_report(request):
    pass

def show_report(request):
    pass

def edit_report(request):
    pass

def delete_report(request):
    pass

def list_ratings(request):
    pass

def create_rating(request,project_id):
    pass

def show_rating(request):
    pass

def edit_rating(request):
    pass

def delete_rating(request):
    pass

def list_comment_reports(request):
    pass

def create_comment_report(request):
    pass

def show_comment_report(request):
    pass

def edit_comment_report(request):
    pass

def delete_comment_report(request):
    pass



def addComment(request, id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        print('here')
        form = NewCommentModelForm(request.POST)
        if form.is_valid():
            form.save(commit=True, project=project, user=request.user)
    
    return redirect('project_show', id=id)