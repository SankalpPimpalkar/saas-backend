from django.urls import path
from .views import *

urlpatterns = [
    path('generate-api-key/', generate_api_key)
]
