from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
from password_strength import PasswordPolicy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import EmailMessage, get_connection
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from uuid import uuid4
import os
import string
import random


User = get_user_model()

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 2 uppercase letters
    numbers=1,  # need min. 2 digits
    special=1,  # need min. 2 special characters
)

def generate_confirmation_token(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def generate_reset_token(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def SendConfirmationEmail(email, username, user, new_token):
    confirm_url = f"{settings.FRONTEND_URL}/confirm-register/{user.id}"
    subject = "Confirmação de cadastro"
    message = (
        f"Olá {username}, seu cadastro foi realizado com sucesso!\n\n"
        f"Confirmation token: {new_token}"
        f"Confirm url: {confirm_url}"
    )
    from_email = "onboarding@resend.dev"
    recipient_list = [email]
    with get_connection(
        host=settings.RESEND_SMTP_HOST,
        port=settings.RESEND_SMTP_PORT,
        username=settings.RESEND_SMTP_USERNAME,
        password=settings.RESEND_URL_API_KEY,
        use_tls=True,
    ) as connection:
        EmailMessage(
            subject=subject,
            body=message,
            to=recipient_list,
            from_email=from_email,
            connection=connection
        ).send()

def SendRestorePasswordEmail(email, user):
  username = user.username
  subject = "Recuperar Senha"
  reset_token = generate_reset_token()
  user.reset_token = reset_token
  restore_url = f"{settings.FRONTEND_URL}/users/login/restorepassword/{reset_token}"
  user.save()
  message = (
    f"Olá {username} sua solicitação de recuperação de senha foi realizada com sucesso "
    f"{restore_url}"
  )
  from_email = "onboarding@resend.dev"
  recipient_list = [email]
  with get_connection(
    host=settings.RESEND_SMTP_HOST,
    port=settings.RESEND_SMTP_PORT,
    username=settings.RESEND_SMTP_USERNAME,
    password=settings.RESEND_URL_API_KEY,
    use_tls=True,
    ) as connection:
    EmailMessage(
      subject=subject,
      body=message,
      to=recipient_list,
      from_email=from_email,
      connection=connection
  ).send()


@csrf_exempt
def Login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    data = json.loads(request.body)
    username = data.get("username")  
    password = data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if not getattr(user, "is_confirmed", False):
            return JsonResponse({"error": "E-mail not confirmed. Please confirm your e-mail before logging in."}, status=403)
        auth_login(request, user)
        return JsonResponse({"success": "User authenticated successfully"}, status=200)
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=401)
        
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
        try:
            new_token = generate_confirmation_token()
            new_user = User(username=username, email=email, is_active=True, confirmation_token=new_token)
            new_user.set_password(password)
            new_user.save()
            SendConfirmationEmail(email, username, new_user, new_token)
            return JsonResponse({"success": "register valid successful"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
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

@csrf_exempt
def ConfirmRegister(request, user_id):
  if request.method == "POST":
    try:
      user = User.objects.filter(id=user_id).first()
      if not user:
        return JsonResponse({"error": "user not found"}, status=400)
      if user.is_confirmed == True:
        return JsonResponse({"error": "account already confirmed"}, status=401)
      data = json.loads(request.body)
      confirmation_token = data.get("confirmation_token")
      user_expected_token = user.confirmation_token
      if confirmation_token != user_expected_token:
        return JsonResponse({"error": "confirmation token invalid"}, status=400)
      else:
        user.is_confirmed = True
        user.save()
        return JsonResponse({"success": "account confirmed with successfuly"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def RestorePassword(request):
  if request.method == "POST":
    try:
      data = json.loads(request.body)
      email = data.get("email")
      user = User.objects.filter(email=email).first()
      if not user:
        return JsonResponse({"error": "user do not exist"})
      SendRestorePasswordEmail(email, user)
      return JsonResponse({"success": "e-mail send with successfuly"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
  
@csrf_exempt  
def SetNewPassword(request, reset_token):
  if request.method == "PUT":
    try:
      data = json.loads(request.body)
      user = User.objects.filter(reset_token=reset_token).first()
      if not user:
        return JsonResponse({"error": "User do not exist"})
      new_password = data.get("password")
      if policy.test(new_password):
          return JsonResponse({"error": "must be a valid password"}, status=400)
      user.password = new_password
      user.save()
      return JsonResponse({"success": "password changed with succesfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
