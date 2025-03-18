from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('get-user/', get_user_details),
    path('refresh-token/', refresh_access_token),
]
