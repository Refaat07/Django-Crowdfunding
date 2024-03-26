from django.urls import path , include
from users.views import create_user, activate, profile, edit_profile, delete_profile, userprofile
from django.conf.urls.static import static

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register', create_user, name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('profile/', userprofile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('delete-profile/', delete_profile, name='delete_profile'),


]
