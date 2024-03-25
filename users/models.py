from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings

class CustomUser(AbstractUser):
    user_image = models.ImageField(upload_to='users/images', blank=True)
    phone_number = models.CharField(max_length=15, null=True)
    birth_date = models.DateField(null=True, default=timezone.now)
    facebook = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=20, null=True)