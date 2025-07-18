"""
URL configuration for darkart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views, models

urlpatterns = [
    path('login/', views.Login, name="login"),
    path('register/', views.Register, name="register"),
    path("", views.GetAllUsers, name="GetAllUsers"),
    path("<int:user_id>", views.GetUserById, name="GetUserById"),
    path("delete/<int:user_id>/", views.DeleteUser, name="DeleteUser"),
    path("edit/<int:user_id>/", views.EditUser, name="EditUser"),
    path("register/confirmation/<int:user_id>", views.ConfirmRegister, name="ConfirmRegister"),
    path("login/restorepassword/", views.RestorePassword, name="RestorePassword"),    
    path("login/restorepassword/<str:reset_token>", views.SetNewPassword, name="SetNewPassword")    
]