from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
import re

class CustomUser(User):
    user_image = models.ImageField(upload_to='users/images/', blank=True)
    phone_number = models.CharField(max_length=15, null=True)
    birth_date = models.DateField(null=True, default=timezone.now)
    facebook = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=20, null=True)

class UserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'phone_number', 'user_image')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("First name field is required.")
        if len(first_name) < 2:
            raise forms.ValidationError("First name must be at least 2 characters long.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("Last name field is required.")
        if len(last_name) < 2:
            raise forms.ValidationError("Last name must be at least 2 characters long.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email field is required.")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError("Please enter a valid email address.")
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError("Phone number field is required.")
        if not re.match(r'^01[0125][0-9]{8}$', phone_number):
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone_number    

    def save(self, commit=True):
        self.instance.password = make_password(password=self.instance.password)
        super().save(commit)
        return self.instance



# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password
# from django.db import models

# class CustomUser(User):
#     user_image = models.ImageField(upload_to='users/images/', blank=True)

# class UserModelForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'email', 'username', 'password', 'user_image')
#         widgets = {
#             'password': forms.PasswordInput()
#         }

#     def save(self, commit=True):
#         self.instance.password = make_password(password=self.instance.password)
#         super().save(commit)
#         return self.instance

#     def clean_name(self):
#         fname = self.cleaned_data['first_name']
#         if len(fname) < 2:
#             raise forms.ValidationError("Name must be at least 2 characters ")
#         return name

#     def clean_name(self):
#         lname = self.cleaned_data['last_name']
#         if len(fname) < 2:
#             raise forms.ValidationError("Name must be at least 2 characters ")
#         return name
