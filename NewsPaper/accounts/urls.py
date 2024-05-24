from django.urls import path
from .views import IndexView, upgrade_me

urlpatterns = [
    path('profile/', IndexView.as_view(), name='profile'),
    path('upgrade/', upgrade_me, name='account_upgrade')
]
