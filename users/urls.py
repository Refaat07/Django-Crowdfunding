from django.urls import path , include

from users.views import create_user

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register', create_user, name='register')
]