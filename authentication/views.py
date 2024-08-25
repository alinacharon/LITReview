from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.decorators import login_required
from . import forms
from .models import User, UserFollows
from django.db import IntegrityError
from django.contrib import messages


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

@login_required
def manage_follows(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user_to_follow = User.objects.get(username=username)
            if user_to_follow != request.user:
                UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
                messages.success(request, f"Vous suivez maintenant {username}.")
            else:
                messages.warning(request, "Vous ne pouvez pas vous suivre vous-même.")
        except User.DoesNotExist:
            messages.error(request, f"L'utilisateur '{username}' n'existe pas.")
        except IntegrityError:
            messages.warning(request, f"Vous suivez déjà {username}.")
    
    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    
    return render(request, 'authentication/manage_follows.html', {
        'following': following,
        'followers': followers,
    })

@login_required
def unsubscribe(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow).delete()
    return redirect('manage_follows')