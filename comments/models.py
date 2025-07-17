from django.db import models
from django.contrib.auth.models import User
from artworks.models import Artworks
from django.conf import settings


# Create your models here.
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    artwork = models.ForeignKey(Artworks, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
      db_table = "comments"
