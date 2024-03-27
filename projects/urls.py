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
    path('<int:project_id>/comments/', list_comments, name='comment_list'),
    path('<int:project_id>/comments/create/', create_comment, name='comment_create'),
    path('<int:project_id>/comments/<int:comment_id>/', show_comment, name='comment_show'),
    path('<int:project_id>/comments/<int:comment_id>/edit/', edit_comment, name='comment_edit'),
    path('<int:project_id>/comments/<int:comment_id>/delete/', delete_comment, name='comment_delete'),
    
    # Project Reports URLs
    path('<int:project_id>/reports/', list_reports, name='report_list'),
    path('<int:project_id>/reports/create/', create_report, name='report_create'),
    path('<int:project_id>/reports/<int:report_id>/', show_report, name='report_show'),
    path('<int:project_id>/reports/<int:report_id>/edit/', edit_report, name='report_edit'),
    path('<int:project_id>/reports/<int:report_id>/delete/', delete_report, name='report_delete'),
    
    # Comment Reports URLs
    path('<int:project_id>/comments/<int:comment_id>/reports/', list_comment_reports, name='comment_report_list'),
    path('<int:project_id>/comments/<int:comment_id>/reports/create/', create_comment_report, name='comment_report_create'),
    path('<int:project_id>/comments/<int:comment_id>/reports/<int:report_id>/', show_comment_report, name='comment_report_show'),
    path('<int:project_id>/comments/<int:comment_id>/reports/<int:report_id>/edit/', edit_comment_report, name='comment_report_edit'),
    path('<int:project_id>/comments/<int:comment_id>/reports/<int:report_id>/delete/', delete_comment_report, name='comment_report_delete'),

    # Ratings URLs
    path('<int:project_id>/ratings/', list_ratings, name='rating_list'),
    path('<int:project_id>/ratings/create/', create_rating, name='rating_create'),
    path('<int:project_id>/ratings/<int:rating_id>/', show_rating, name='rating_show'),
    path('<int:project_id>/ratings/<int:rating_id>/edit/', edit_rating, name='rating_edit'),
    path('<int:project_id>/ratings/<int:rating_id>/delete/', delete_rating, name='rating_delete'),

    #Refaat URLs
    path('<int:id>/newcomment', addComment, name='project.newcomment'),
    path('<int:id>/reportComment/<int:comID>', reportComment, name='project.reportComment'),
    path('<int:id>/reportProject', reportProject, name='project.reportProject'),
    path('<int:id>/donate', donate, name='project.donate')
]