from django.urls import path , include

from projects.views import entry_point

urlpatterns = [
    path('', entry_point, name='entry_point'),
]