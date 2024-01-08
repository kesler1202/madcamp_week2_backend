from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from blog.models import User

from .serializers import UserSerializer
from .serializers import UserRegistrationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # User authentication successful
            login(request, user)
            return Response(UserSerializer(user).data)
        else:
            try:
                # Try to get a user with the given email
                user = User.objects.get(email=email)
                # User with the email exists, so the password must be incorrect
                return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                # User with the email does not exist
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

def HomeView(request):
    return HttpResponse("Welcome to the home page!")