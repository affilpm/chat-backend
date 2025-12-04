from django.contrib.auth import get_user_model
from typing import Optional

User = get_user_model()

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .selectors import get_user

def create_user(*, username: str, email: str, password: str) -> User:
    return User.objects.create_user(username=username, email=email, password=password)

def login_user(*, email: str, password: str) -> dict:
    user = authenticate(email=email, password=password)
    if user is None:
        return None
        
    refresh = RefreshToken.for_user(user)
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': user
    }
