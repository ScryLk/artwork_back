from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
# Create your models here.

class CustomUser(AbstractUser):
  confirmation_token = models.TextField(default=False)
  is_confirmed = models.BooleanField(default=False)
  