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
from projects.views import entry_point, homepage 
# from django.contrib.auth.models import User
from .forms import CustomUser



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
            # url = reverse("login")
            # return redirect(url)
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
        # user.image.save(f'{last_user.pk}.jpg', image_file)
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('/users/login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage')


# def profile(request):
#      user = request.user
#      return render(request, 'profile.html', {'user': user})


@login_required(login_url='/users/login')
def user_profile(request):
    user = request.user
    user_id = request.user.id
    
    user = CustomUser.objects.get(pk=user_id)
    # print(user.)
    image_url = user.user_image.url if user and user.user_image else None
 
    # Pass the image link to the HTML template
    return render(request, 'users/profile.html', {'user': user, 'image_url':image_url})

@login_required(login_url='/users/login')
def delete_profile(request):
    if request.method == 'GET':
        user = request.user
        user.delete()
        return redirect('homepage') 
    else:
        return HttpResponse(status=405)

def user_projects(request):
    user_projects = Project.objects.filter(creator=request.user)

    return render(request, 'users/user_projects.html', {'user_projects': user_projects})
    


# def home_index(request):
#     user_id = request.user.id
    
#     user = CustomUser.objects.get(pk=user_id)
#     # print(user.)
#     image_url = user.user_image.url if user and user.user_image else None
#     print(image_url)
    
#     # Pass the image link to the HTML template
#     return render(request, 'projects\entry_point.html', {'image_url':image_url})
