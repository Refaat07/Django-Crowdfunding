from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import models

class CustomUser(User):
    user_image = models.ImageField(upload_to='users/images/', blank=True)

class UserModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'user_image')
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        self.instance.password = make_password(password=self.instance.password)
        super().save(commit)
        return self.instance



