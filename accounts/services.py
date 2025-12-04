from django.contrib.auth import get_user_model
from typing import Optional

User = get_user_model()

def create_user(*, username: str, email: str, password: str) -> User:
    return User.objects.create_user(username=username, email=email, password=password)
