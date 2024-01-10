from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from blog.models import User, Post, Comment
from .forms import CommentForm
from .serializers import UserSerializer, UserRegistrationSerializer, PostSerializer


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        print(f"Email: {email}, Password: {password}")  # Print the received email and password

        user = authenticate(request, email=email, password=password)
        print(f"Authenticated User: {user}")
        if user is not None:
            # User authentication successful
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data})
        else:
            # User authentication failed
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'message': "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@require_GET
def check_user(request):
    email = request.GET.get('email', None)
    response_data = {'exists': False}

    if email:
        try:
            user = User.objects.get(email=email)
            response_data['exists'] = True
        except ObjectDoesNotExist:
            response_data['exists'] = False

    return JsonResponse(response_data)

def check_user_by_name(request, name):
    # Implement the logic to check if a user exists by nickname
    # For example, searching in your User model
    user_exists = User.objects.filter(name=name).exists()

    # Return JSON response
    return JsonResponse({'exists': user_exists})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    print(f"Headers: {request.headers}")  # Debugging line
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Logout the user and delete the token
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def HomeView(request):
    return HttpResponse("Welcome to the home page!")

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
#게시물 생성하기
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

#댓글 생성 및 조회
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'myapp/post_detail.html', {'post': post, 'comments': comments, 'form': form})

def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            # 댓글 생성이 성공했을 때, 생성된 댓글 정보를 JSON 형태로 응답합니다.
            return JsonResponse({
                'id': comment.id,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        else:
            # 폼이 유효하지 않을 경우 에러 응답
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        # POST 요청이 아닐 경우 에러 응답
        return JsonResponse({'error': 'Invalid request method'}, status=400)