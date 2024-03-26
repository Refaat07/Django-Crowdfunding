from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from projects.models import Project,ProjectRating, Category
from projects.forms import CreateProjectModelForm,EditProjectModelForm,NewCommentModelForm
from django.utils import timezone
from django.db.models import Avg 


# Create your views here.
def entry_point(request):
    return render(request, 'projects/entry_point.html')

def homepage(request):
    return render(request, 'projects/homepage.html')        

def list_projects(request):
    projects = Project.objects.all()
    print(projects)
    return render(request,'projects/index.html',context={"projects":projects})

def show_project(request,id):
    project = get_object_or_404(Project.objects.prefetch_related('comments', 'project_ratings'), id=id)
    comments = project.comments.all()
    ratings = project.project_ratings.all()
    user_current_rating = ratings.filter(user=request.user).first()
    if user_current_rating:
        user_current_rating = user_current_rating.rating
    return render(request, 'projects/show.html',context={
        "project":project,
        "comments": comments,
        'newCommentForm': NewCommentModelForm,
        "ratings":ratings,
        "user_current_rating": user_current_rating
    })

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
    project = get_object_or_404(Project, id=project_id)
    rating_value = request.POST.get('rating')  
    if ProjectRating.objects.filter(project=project, user=request.user).exists():
        rating = ProjectRating.objects.get(project=project, user=request.user)
        rating.rating = rating_value
        rating.save()
    else:
        rating = ProjectRating.objects.create(project=project, user=request.user, rating=rating_value)
    
    return redirect('project_show',id=project_id)

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