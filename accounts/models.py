from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to='avatars/',null=True, blank=True, default='avatars/default.png')
    status = models.CharField(max_length=100, null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [username]  

    def __str__(self):
        return self.email