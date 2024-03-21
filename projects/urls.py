from django.urls import path , include

from projects.views import entery_point

urlpatterns = [
    path('', entery_point, name='entery_point'),
]