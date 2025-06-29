from django.shortcuts import render
from .models import Comments
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def AddComments(request, artwork_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                if request.content_type == "application/json":
                    data = json.loads(request.body)
                    content = data.get("content")
                else:
                    content = request.POST.get("content")
                if not content:
                    return JsonResponse({"error": "Content is required"}, status=400)
                comment = Comments.objects.create(
                    user=request.user,
                    content=content,
                    artwork_id=artwork_id
                )
                return JsonResponse({"success": "Comment created successfully", "id": comment.id})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)

def GetAllComments(request, artwork_id):
  if request.method=="GET":
    if request.user.is_authenticated:
      try:
        comments_data = [
          {
            "id": comment.id,
            "content": comment.content,
            "created_at": comment.created_at,
            "artwork_id": comment.artwork.id,
            "user_id": comment.artwork.id
          }
        for comment in Comments.objects.filter(artwork_id=artwork_id)
        ]
        return JsonResponse({"success": comments_data})
      except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)

def GetCommentsById(request, comment_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            try:
                comment = Comments.objects.filter(id=comment_id).first()
                if not comment:
                    return JsonResponse({"error": "Comment not found"}, status=404)
                comment_data = {
                    "id": comment.id,
                    "content": comment.content,
                    "created_at": comment.created_at,
                    "artwork_id": comment.artwork.id,
                    "user_id": comment.user.id
                }
                return JsonResponse({"success": comment_data})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)

@csrf_exempt
def DeleteComment(request, comment_id):
  if request.method == "DELETE":
    if request.user.is_authenticated:
      try:
        comment = Comments.objects.filter(id=comment_id).first()
        if not comment:
          return JsonResponse({"error": "Comment not found"}, status=404)
        else:
          comment.delete()
          return JsonResponse({"success": "artwork deleted with success"})
      except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)
      