from django.contrib.auth import get_user_model

User = get_user_model()

def get_user(*, email: str) -> User:
    return User.objects.get(email=email)
