from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from users.forms import UserModelForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import get_user_model
from .tokens import account_activation_token
from django.http import HttpResponseServerError
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login as auth_login, logout as auth_logout
from projects.views import entry_point, homepage 
from .forms import CustomUser
from projects.models import Project
from .forms import UserEditForm


# Create your views here.

def profile(request):
    url = reverse('homepage')
    return redirect(url)

def create_user(request):
    form = UserModelForm()
    if request.method == 'POST':
        form = UserModelForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('homepage')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    return render(request,
                  'users/create_user.html', {'form': form})


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to your email {to_email} inbox and click on \
                received activation link to confirm and complete the registration. \
                Note: Check your spam folder.')
        print("Email sent successfully")
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
        print("Unsuccessfull Operation")


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('/users/login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage')


def edit_profile(request):
    user_id = request.user.id
    user = CustomUser.objects.get(pk=user_id)
    now = timezone.now()


    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                if form.cleaned_data['password']:
                    user.password = make_password(form.cleaned_data['password'])
                if not form.cleaned_data['country']:
                    user.country = 'Default'
                if not form.cleaned_data['facebook']:
                    user.facebook = 'Default'
                if not form.cleaned_data['birth_date']:
                    user.birth_date = now
                user.save()
                messages.success(request,"Profile updated successfully")

                if request.user.is_authenticated:
                    auth_login(request, user)

                return redirect('user_profile')
            except Exception as e:
                print(f"An error occurred while saving the form: {e}")
                return HttpResponseServerError("An error occurred while saving the form.")
    else:
        form = UserEditForm(instance=user)

    return render(request, 'users/edit_form.html', {'form': form})


@login_required(login_url='/users/login')
def user_profile(request):
    user = request.user
    user_id = request.user.id
    
    user = CustomUser.objects.get(pk=user_id)
    image_url = user.user_image.url if user and user.user_image else None
    return render(request, 'users/profile.html', {'user': user, 'image_url':image_url})

@login_required(login_url='/users/login')
def delete_profile(request):
    if request.method == 'GET':
        user = request.user
        user.delete()
        return redirect('homepage') 
    else:
        return HttpResponse(status=405)

from django.forms.models import model_to_dict
def user_projects(request):
    user_projects = Project.objects.filter(id=request.user.id)
    project_list = [model_to_dict(project) for project in user_projects]
    print(project_list)

    return render(request, 'users/user_projects.html', {'user_projects': project_list})
    