from django.urls import path
from .views import LoginView, RegisterView, get_user_profile, HomeView, LogoutView, check_user

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', get_user_profile, name='get_user_profile'),
    path('checkUser/', check_user, name='check_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView, name='home'),
]