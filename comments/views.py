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
