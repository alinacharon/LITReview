from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.decorators import login_required
from . import forms

def home_page(request):
    if request.user.is_authenticated:
        return redirect('feed')  
    return render(request, 'authentication/home.html')

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})