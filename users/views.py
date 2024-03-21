from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from users.forms import UserModelForm

# Create your views here.

def profile(request):
    url = reverse("home")
    return redirect(url)


def create_user(request):
    form = UserModelForm()
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        # try:
        #     book.image = request.FILES['image']
        # except Exception as e:
        #     pass
        if form.is_valid():
            form.save()
        url = reverse("login")
        return redirect(url)
    return render(request,
                  'users/create_user.html', {'form': form})
