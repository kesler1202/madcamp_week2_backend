from django.urls import path
from .views import(
    LoginView,
    RegisterView,
    get_user_profile,
    HomeView,
    LogoutView,
    check_user,
    PostViewSet,
    PostList,
    PostDetail
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', get_user_profile, name='get_user_profile'),
    path('checkUser/', check_user, name='check_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView, name='home'),
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),

]