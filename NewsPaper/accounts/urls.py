from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup/', BaseRegisterView.as_view(template_name='accounts/signup.html'), name='signup'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('upgrade/', upgrade_me, name='account_upgrade')
]
