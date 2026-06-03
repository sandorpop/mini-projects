from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.TextChoices):
    USER = 'user', 'User'
    ADMIN = 'admin', 'Admin'

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.email