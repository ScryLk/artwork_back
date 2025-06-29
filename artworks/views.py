from django.shortcuts import render, HttpResponse
from .models import Artworks
import json
from django.http import JsonResponse

def GetAllArtWorks(request):
  if request.method == "GET":
    try:
      artworks_data = [
        {
          "id": artwork.id,
          "title": artwork.title,
          "desciption": artwork.description,
          "image": artwork.image,
          "created_at": artwork.created_at,
          "updated_at": artwork.updated_at,
          "visibility": artwork.visibility
        }
        for artwork in Artworks.objects.all()
      ]
      return JsonResponse({"success": artworks_data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
      
def AddArtWorks(request):
  if request.method == "POST":
    try:
      data = request.loads(request.body)
      title = data.get("title")
      description = data.get("description")
      image = data.get("image")
      if not title | description | image:
        return JsonResponse({"failed": "Credentials Failed"})
      else:
        artwork = Artworks.objects.create(
          title = title,
          description = description,
          image = image
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
        