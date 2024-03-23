from django.urls import path , include
from projects.views import index,create,show,edit,delete,addComment

urlpatterns = [
    path('', index, name='project.index'),
    path('create', create, name='project.create'),
    path('<int:id>', show, name='project.show'),
    path('<int:id>/edit', edit, name='project.edit'),
    path('<int:id>/delete', delete, name='project.delete'),
    path('<int:id>/newcomment', addComment, name='project.newcomment'),
]