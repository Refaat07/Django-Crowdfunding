from django.urls import path , include
from users.views import create_user, activate

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register', create_user, name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
]