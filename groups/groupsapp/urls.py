from django.urls import path
from . import views

urlpatterns = [
    path("groups/", views.GroupListController.as_view()),
    path("groups/<int:pk>/", views.GroupDetailController.as_view()),
    path("groups/<int:pk>/join/", views.GroupJoinController.as_view()),
    path("groups/<int:pk>/leave/", views.GroupLeaveController.as_view()),
    path("users/", views.UserListController.as_view()),
]
