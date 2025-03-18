from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import APIKey
from rest_framework import status

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_api_key(request):
    user = request.user
    existing_api_key = APIKey.objects.filter(user=user).first()

    if existing_api_key:
        existing_api_key.delete()
    
    new_api_key = APIKey.objects.create(user=user)
    
    return Response({
        "message": "API Key generated",
        "api_key": new_api_key.key
    },status=status.HTTP_201_CREATED)