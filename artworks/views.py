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
          "image": artwork.image.url,
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

@csrf_exempt
def GetArtWorkById(request, id):
    if request.method == "GET":
        if request.user.is_authenticated:
          try:
              artwork = Artworks.objects.get(id=id)
              data = {
                  "id": artwork.id,
                  "title": artwork.title,
                  "description": artwork.description,  
                  "image": artwork.image.url,
                  "created_at": artwork.created_at,
                  "updated_at": artwork.updated_at,
                  "visibility": artwork.visibility
              }
              return JsonResponse({"success": data})
          except Artworks.DoesNotExist:
              return JsonResponse({"error": "artwork do not exist"}, status=404)
          except Exception as e:
              return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)    

@csrf_exempt
def DeleteArtWork(request, id):
  if request.method == "DELETE":
    if request.user.is_authenticated:
      try:
        artwork = Artworks.objects.filter(id=id)
        if not artwork:
          return JsonResponse({"error": "artwork do not exist"})
        else:
          artwork.delete()
          return JsonResponse({"success": "artwork deleted with success"})
      except Exception as e:
          return JsonResponse({"error": str(e)}, status=500)
    else:
      return JsonResponse({"error": "User not authenticated"}, status=401)

@csrf_exempt
def EditArtWork(request, id):
    if request.method == "PUT":
        if request.user.is_authenticated:
            try:
                artwork = Artworks.objects.filter(id=id).first()
                if not artwork:
                    return JsonResponse({"error": "artwork do not exist"})
                data = json.loads(request.body)
                artwork.title = data.get("title", artwork.title)
                artwork.description = data.get("description", artwork.description)
                artwork.visibility = data.get("visibility", artwork.visibility)
                artwork.save()
                return JsonResponse({"success": "artwork editada com sucesso"})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
          return JsonResponse({"error": "User not authenticated"}, status=401)

@csrf_exempt
def GetArtWorkByUser(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            try:
                artworks = Artworks.objects.filter(user=request.user)
                data = [
                    {
                        "id": artwork.id,
                        "title": artwork.title,
                        "description": artwork.description,
                        "image": artwork.image.url,
                        "created_at": artwork.created_at,
                        "updated_at": artwork.updated_at,
                        "visibility": artwork.visibility
                    }
                    for artwork in artworks
                ]
                return JsonResponse({"success": data})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)
      
      
   
        