from django.urls import path
from . import views

urlpatterns = [
    path('artworks/<int:artwork_id>/comments/create/', views.AddComments, name="AddComments"),
 #   path('artowrks/<int:artwork_id>/comments', views.GetAllComments, name="GetAllComments"),
 #   path('artworks/<int:artwork_id>/comments/<int:comment_id>/', views.GetCommentsById, name="GetCommentsById"),
]