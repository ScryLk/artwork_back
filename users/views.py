from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
from password_strength import PasswordPolicy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 2 uppercase letters
    numbers=1,  # need min. 2 digits
    special=1,  # need min. 2 special characters
)

@csrf_exempt
def login(request):
    if request.method == "GET":
        return HttpResponse("Eai")
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")  # Troque para username
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({"success": "user authenticated with success"}, status=200)
        else:
            return JsonResponse({"error": "user authentication failed"}, status=400)
        
@csrf_exempt
def register(request):
  if request.method == "GET":
    return HttpResponse("registro")
  if request.method == "POST":
    data = json.loads(request.body)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
  if not username:
    return JsonResponse({"error": "must be a valid username"}, status=400)
  if policy.test(password):
    return JsonResponse({"error": "must be a valid password"}, status=400)
  if User.objects.filter(email=email).exists():
    return JsonResponse({"error": "email address already exists"}, status=400)
  new_user = User(username=username, email=email, password=password)
  new_user.set_password(password)
  new_user.save()
  return HttpResponse({"success": "register vailed succesfull"}, status=200)