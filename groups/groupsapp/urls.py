from django.urls import path
from . import views

urlpatterns = [
    path("groups/", views.GroupListController.as_view()),
    path("groups/<int:pk>/", views.GroupDetailController.as_view()),
]
