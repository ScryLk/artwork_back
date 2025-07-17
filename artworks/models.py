from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

visibility_choices = [
    ("Public", "Public"),
    ("Private", "Private")
]

class Artworks(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  title = models.CharField(max_length=50, null=False)
  description = models.TextField(null=False)
  image = models.ImageField(upload_to="artworks/")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  visibility = models.CharField(choices=visibility_choices, max_length=10)
  
  
  class Meta:
    db_table = "artworks"
