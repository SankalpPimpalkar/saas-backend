from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Create your views here.
@api_view(['POST'])
def register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = User.objects.filter(username=username).exists()

    if user:
        return Response({
            "message": "User already exists with this username"
        },status=status.HTTP_400_BAD_REQUEST)
    
    new_user = User.objects.create_user(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    
    new_user.set_password(password)
    new_user.save()

    return Response({
        "message": "User created successfully",
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({
            "error": "Invalid credentials"
        },status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    
    response = Response({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }, status=status.HTTP_200_OK)
    
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=True,
        samesite='Lax',
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite='Lax',
    )

    return response

@api_view(['POST'])
def logout(request):
    
    response = Response({
        "message": "User logged out successfully"
    },status=status.HTTP_200_OK)

    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response

