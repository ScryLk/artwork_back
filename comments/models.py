from django.db import models
from django.contrib.auth.models import User
from artworks.models import Artworks


# Create your models here.
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    artwork = models.ForeignKey(Artworks, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
      db_table = "comments"
