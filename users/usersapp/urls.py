from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserListController.as_view()),
    path("users/<int:pk>/", views.UserDetailController.as_view()),
]
