from django.urls import path , include
from projects.views import *

urlpatterns = [
    # Home page
    # path('', homepage, name='homepage'),

    # Search Projects
    path('search/', project_search, name='project_search'),

    # Category Projects
    path('category/<int:id>/', get_category_projects, name='category_projects'),

    # Projects URLs
    path('', list_projects, name='project_list'),
    path('create/', create_project, name='project_create'),
    path('<int:id>/', show_project, name='project_show'),
    path('<int:id>/edit/', edit_project, name='project_edit'),
    path('<int:id>/delete/', delete_project, name='project_delete'),

    # Comments URLs
    path('<int:project_id>/comments/<int:comment_id>/delete/', delete_comment, name='comment_delete'),

    # Ratings URLs
    path('<int:project_id>/ratings/create/', create_rating, name='rating_create'),

    #Refaat URLs
    path('<int:id>/newcomment', addComment, name='project.newcomment'),
    path('<int:id>/reportComment/<int:comID>', reportComment, name='project.reportComment'),
    path('<int:id>/reportProject', reportProject, name='project.reportProject'),
    path('<int:id>/donate', donate, name='project.donate'),
    path('<int:id>/cancel', cancelProject, name='project.cancel')
]