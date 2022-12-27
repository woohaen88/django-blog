from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
