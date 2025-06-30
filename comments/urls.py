from django.urls import path
from . import views

urlpatterns = [
    path('<int:artwork_id>/create/', views.AddComments, name="AddComments"),
    path('<int:artwork_id>/comments/', views.GetAllComments, name="GetAllComments"),
    path('<int:comment_id>/', views.GetCommentsById, name="GetCommentsById"),
    path('delete/<int:comment_id>/', views.DeleteComment, name="DeleteComment"),
    path('edit/<int:comment_id>/', views.EditComment, name="EditComment"),
    path('user/<int:user_id>/', views.GetCommentsByUser, name="GetCommentsByUser"),
    
]