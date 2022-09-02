from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in successfully')
            return redirect(reverse("market:index"))
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect(reverse('accounts:login_user'))
    else:
        return render(request, 'accounts/login.html')

@login_required    
def logout_user(request):
    auth.logout(request)
    return redirect(reverse("market:index"))
