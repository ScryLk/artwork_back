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
def Login(request):
    if request.method == "GET":
        return HttpResponse("Eai")
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")  
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({"success": "user authenticated with success"}, status=200)
        else:
            return JsonResponse({"error": "user authentication failed"}, status=400)
        
@csrf_exempt
def Register(request):
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


def GetAllUsers(request):
  if request.method == "GET":
    if request.user.is_authenticated:
      try:
        data_user = [
          {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "last_login": user.last_login,
            "is_superuser": user.is_superuser,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
          }
          for user in User.objects.all()
        ]
        return JsonResponse({"success": data_user})
      except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)

def GetUserById(request, user_id):
  if request.method == "GET":
    if request.user.is_authenticated:
      try:
        user = User.objects.filter(id=user_id).first()
        if not user:
          return JsonResponse({"error": "user not found"}, status=400)
        else:
          data_user = [
          {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "last_login": user.last_login,
            "is_superuser": user.is_superuser,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
          }
        ]
        return JsonResponse({"success": data_user})
      except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)

@csrf_exempt
def DeleteUser(request, user_id):
  if request.method == "DELETE":
      if request.user.is_authenticated:
        try:
          user = User.objects.filter(id=user_id).first()
          if not user:
            return JsonResponse({"error": "user not found"}, status=400)
          else:
            user.delete()
            return JsonResponse({"success": "user deleted successfuly"}, status=200)
        except Exception as e:
          return JsonResponse({"error": str(e)}, status=500)
  else:
      return JsonResponse({"error": "User not authenticated"}, status=401)
    
@csrf_exempt
def EditUser(request, user_id):
    if request.method == "PUT":
        if request.user.is_authenticated:
            try:
                user = User.objects.filter(id=user_id).first()
                if not user:
                    return JsonResponse({"error": "user not found"}, status=400)
                data = json.loads(request.body)
                user.username = data.get("username", user.username)
                user.email = data.get("email", user.email)
                user.is_superuser = data.get("is_superuser", user.is_superuser)
                user.first_name = data.get("first_name", user.first_name)
                user.last_name = data.get("last_name", user.last_name)
                user.is_active = data.get("is_active", user.is_active)
                user.is_staff = data.get("is_staff", user.is_staff)
                if "password" in data and data["password"]:
                    user.set_password(data["password"])
                user.save()
                return JsonResponse({"success": "User edit with successfully", "id": user.id}, status=200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)
      

          
          



      
