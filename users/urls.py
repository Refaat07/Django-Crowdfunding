from django.urls import path , include
from users.views import create_user, activate, home_index
from users.views import profile_view
from users.views import edit_profile

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register', create_user, name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]