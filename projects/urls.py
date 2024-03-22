from django.urls import path , include

from . import views

urlpatterns = [
    path('', views.entry_point, name='entry_point'),
    path('all', views.viewProjects, name='viewProjects'),
    path('createNew', views.viewProjects, name='createProject')
]