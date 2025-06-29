from django.shortcuts import render, HttpResponse
from .models import Artworks
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
  
@csrf_exempt    
def AddArtWorks(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
              title = request.POST.get("title")
              description = request.POST.get("description")
              image = request.FILES.get("image")
              visibility = request.POST.get("visibility", "Public")
              artwork = Artworks.objects.create(
                    user=request.user,
                    title=title,
                    description=description,
                    image=image,
                    visibility=visibility
                )
              return JsonResponse({"success": "Artwork created", "id": artwork.id})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)
        