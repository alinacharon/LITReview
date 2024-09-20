from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

import authentication.views

urlpatterns = [
    path('', authentication.views.home_page, name='home'),
    path('login/', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('manage-follows/', authentication.views.manage_follows, name='manage_follows'),
    path('unsubscribe/<int:user_id>/', authentication.views.unsubscribe, name='unsubscribe'),
]
