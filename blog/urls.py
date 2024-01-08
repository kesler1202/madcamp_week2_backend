from django.urls import path

from . import views
from .views import (
    LoginView,
    RegisterView,
    get_user_profile,
    HomeView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', get_user_profile, name='get_user_profile'),
    path('checkUser/', views.check_user, name='check_user'),
    path('', HomeView, name='home'),
]