from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from projects.models import Project,ProjectRating, Category, Comment, CommentReport, ProjectReport, Donations
from projects.forms import CreateOrUpdateProjectModelForm,EditProjectModelForm, NewCommentModelForm, NewCommentReportModelForm, NewProjectReportModelForm, DonationForm
from django.utils import timezone
from django.db.models import Avg 
from django.contrib import messages
from projects.forms import SearchForm
from django.db.models import Q
from django.http import HttpResponseRedirect


# Create your views here.
def entry_point(request):
    return render(request, 'projects/entry_point.html')

def homepage(request):
    return render(request, 'projects/homepage.html')        

def list_projects(request):
    projects = Project.objects.all()
    print(projects)
    return render(request,'projects/index.html',context={"projects":projects})

@login_required(login_url='/users/login')
def show_project(request,id):
    project = get_object_or_404(Project.objects.prefetch_related('comments', 'project_ratings'), id=id)
    comments = project.comments.all()
    ratings = project.project_ratings.all()
    user_current_rating = ratings.filter(user=request.user).first()
    if user_current_rating:
        user_current_rating = user_current_rating.rating
    return render(request, 'projects/showProject.html',context={
        "project":project,
        "comments": comments,
        'newCommentForm': NewCommentModelForm,
        "ratings":ratings,
        "user_current_rating": user_current_rating,
        'newCommentForm': NewCommentModelForm,
        'reportCommentForm': NewCommentReportModelForm,
        'reportProjectForm': NewProjectReportModelForm,
        'DonationForm': DonationForm,
        'currentUser': request.user
    })

@login_required(login_url='/users/login')
def create_project(request):
    form = CreateOrUpdateProjectModelForm()
    if request.method == 'POST':
        form = CreateOrUpdateProjectModelForm(request.POST, request.FILES)
        if form.is_valid():
            if form.save(commit=True,creator=request.user):
                messages.success(request,"Project created successfully")
            else:
                messages.error(request,"An error occured")
            return redirect('project_list')
    return render(request, 'projects/forms/create.html', context={"form": form})

@login_required(login_url='/users/login')
def edit_project(request, id):
    project = Project.objects.get(id=id)
    form = EditProjectModelForm(instance=project)
    if project.creator.id == request.user.id:
        if request.method == 'POST':
            form = EditProjectModelForm(request.POST, request.FILES, instance=project)
            if form.is_valid():
                if form.save(commit=True,creator=request.user):
                    messages.success(request,"Project updated successfully")
                else:
                    messages.error(request,"An error occured")
                return redirect("project_list")
        return render(request, 'projects/forms/edit.html',context={"form":form})
    return redirect("project_list")

@login_required(login_url='/users/login')
def delete_project(request,id):
    project = Project.objects.get(id=id)
    if project.creator.id == request.user.id:
        if project.delete():
            messages.success(request,"Project updated successfully")
        else:
            messages.error(request,"An error occured")
        return redirect("project_list")
    else:
        messages.error(request,"you can't delete this project")
    return redirect("project_list")


def delete_comment(request,project_id,comment_id):
    project = get_object_or_404(Project, id=project_id)
    comment = get_object_or_404(project.comments, id=comment_id)

    if comment.author.id == request.user.id:
        comment.delete()
        messages.success(request, "Comment deleted successfully")
    else:
        messages.error(request, "You can't delete this comment")

    return redirect(reverse('project_show', args=[project_id]))


@login_required(login_url='/users/login')
def create_rating(request,project_id):
    project = get_object_or_404(Project, id=project_id)
    rating_value = request.POST.get('rating')  
    if ProjectRating.objects.filter(project=project, user=request.user).exists():
        rating = ProjectRating.objects.get(project=project, user=request.user)
        rating.rating = rating_value
        rating.save()
    else:
        rating = ProjectRating.objects.create(project=project, user=request.user, rating=rating_value)
    
    return redirect('project_show',id=project_id)

@login_required(login_url='/users/login')
def addComment(request, id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        print('here')
        form = NewCommentModelForm(request.POST)
        if form.is_valid():
            form.save(commit=True, project=project, user=request.user)
    
    return redirect('project_show', id=id)

@login_required(login_url='/users/login')
def reportComment(request, id, comID):
    comment = Comment.objects.get(id=comID)
    if request.method == 'POST':
        form = NewCommentReportModelForm(request.POST)
        if form.is_valid():
            form.save(commit=True, comment=comment, reporter=request.user)
    
    return redirect('project_show', id=id)


@login_required(login_url='/users/login')
def reportProject(request, id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        form = NewProjectReportModelForm(request.POST)
        if form.is_valid():
            form.save(commit=True, project=project, reporter=request.user)
    
    return redirect('project_show', id=id)

def homepage(request):
    current_datetime = timezone.now()

    top_projects = Project.objects.filter(
        campaign_start_date__lte=current_datetime,
        campaign_end_date__gte=current_datetime
    ).annotate(avg_rating=Avg('ratings__project_ratings')).order_by('-avg_rating')[:5]

    latest_projects = Project.objects.order_by('-created_at')[:5]

    categories = Category.objects.all()

    return render(request, 'projects/homepage.html', {
        'top_projects': top_projects,
        'latest_projects': latest_projects,
        'categories': categories
    })

def get_category_projects(request, id):
    category = get_object_or_404(Category, id=id)
    projects_in_category = category.get_projects()
    return render(request, 'projects/categoryProjects.html', {
        'category': category,
        'projects_in_category': projects_in_category
    })

@login_required(login_url='/users/login')
def donate(request,id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save(commit=True, project=project, donor=request.user)
            
    return redirect('project_show', id=id)


def project_search(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        if query:
            results = Project.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).prefetch_related('pictures').distinct()
            return render(request, 'projects/search_results.html', context={'results': list(results), 'query': query})
        else:
            return render(request, 'projects/search_results.html', context={'results': [], 'query': ''})

def cancelProject(request,id):
    project = Project.objects.get(id=id)
    project.delete()            
    return redirect('project_list')