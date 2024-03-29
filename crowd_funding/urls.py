"""
URL configuration for crowd_funding project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
# from users.views import profile_view
# from users.views import home_index


from users.views import profile
from projects.views import homepage

urlpatterns = [
    path('', homepage, name='homepage'),
    path('projects/', include('projects.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/profile/',profile,  ),
    # path('profile/', profile_view, name='profile'),
    # path('edit-profile/', edit_profile, name='edit_profile'),
    # path('home/', home_index, name='activate'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
