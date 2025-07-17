from django.shortcuts import render
from .models import Likes
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.
def GetAllLikes(request):
  if request.method == "GET":
    if request.user.is_authenticated:
      try:
        like_data = [
          {
            "id": like.id,
            "artwork_id": like.artwork_id,
            "user_id": like.user_id,
            "created_at": like.created_at
          }
          for like in Likes.objects.all()
        ]
        return JsonResponse({"success": like_data}, status=200)
      except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)


@csrf_exempt
def ToggleLike(request, artwork_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            like = Likes.objects.filter(user=request.user, artwork_id=artwork_id).first()
            if like:
                like.delete()
                return JsonResponse({"success": "Like removed"})
            else:
                Likes.objects.create(user=request.user, artwork_id=artwork_id)
                return JsonResponse({"success": "Like added"})
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)





