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
<<<<<<< HEAD

from projects.views import home_index
=======
from projects.views import entry_point
from users.views import profile
>>>>>>> bc946b3a9be3db24fab3b66c30c855f2a552df95

urlpatterns = [
    path('', entry_point, name='entry_point'),
    path('projects/', include('projects.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
    path('accounts/profile/',home_index,  )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
