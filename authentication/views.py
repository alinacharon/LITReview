from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.decorators import login_required
from . import forms
from .models import User, UserFollows
from django.db import IntegrityError
from django.contrib import messages


def home_page(request):
    """
    Handles the home page view.

    If the user is authenticated, redirects them to the 'feed' page.
    If the user is not authenticated, renders the 'home.html' template.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Redirects to 'feed' if user is authenticated; otherwise, renders 'home.html'.
    """
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'authentication/home.html')


def signup_page(request):
    """
    Handles the user signup page view.

    Displays the signup form and processes user registration.
    If the form is submitted and valid, a new user is created, logged in, and redirected to the login redirect URL.
    Otherwise, the form is rendered again with validation errors if present.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Renders 'signup.html' with the signup form if GET request or if form is invalid;
      redirects to the login redirect URL if POST request with a valid form.
    """
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
    """
    Manages user follow and unfollow actions.

    Processes follow requests sent via POST. If a valid username is provided,
    attempts to follow the specified user. If the user is already followed, or if the user
    tries to follow themselves, appropriate messages are shown.
    Also retrieves and displays the list of users the current user is following and
    the list of users following the current user.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Renders 'manage_follows.html' with lists of users the current user is following
      and followers of the current user.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user_to_follow = User.objects.get(username=username)
            if user_to_follow != request.user:
                UserFollows.objects.create(
                    user=request.user, followed_user=user_to_follow)
                messages.success(request, f"Vous suivez maintenant {username}.")
            else:
                messages.warning(request, "Vous ne pouvez pas suivre vous-même.")
        except User.DoesNotExist:
            messages.warning(request, f"L'utilisateur '{username}' n'existe pas.")
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
    """
    Handles unfollowing a user.

    Retrieves the user specified by the given user_id and removes the follow relationship
    between the current user and the specified user. Redirects to the 'manage_follows' page
    after the unfollow action.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - user_id (int): The ID of the user to unfollow.

    Returns:
    - HttpResponse: Redirects to the 'manage_follows' page after successfully unfollowing the user.
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    UserFollows.objects.filter(
        user=request.user, followed_user=user_to_unfollow).delete()
    return redirect('manage_follows')
