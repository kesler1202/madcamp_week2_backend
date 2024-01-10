from django.urls import path
from .views import(
    LoginView,
    RegisterView,
    get_user_profile,
    HomeView,
    LogoutView,
    check_user,
    PostList,
    PostListCreateView,
    post_detail
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', get_user_profile, name='get_user_profile'),
    path('checkUser/', check_user, name='check_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView, name='home'),
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),  # 게시물 추가
    path('post/<int:post_id>/', post_detail, name='post_detail'),  # 댓글 추가
]