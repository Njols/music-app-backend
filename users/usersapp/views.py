from operator import truediv
from urllib import response
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .producer import publish
from .serializers import UserSerializer
from .models import User
from django.contrib.auth.hashers import make_password


class UserDetailController(GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects

    def get(self, request, pk):
        try:
            user = self.queryset.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)

        return Response(serializer.data)

    def put(self, request, pk):
        try:
            user = self.queryset.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish("user_changed", serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = self.queryset.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        publish("user_deleted", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListController(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        new_user = request.data
        new_user["password"] = make_password(self.request.data["password"])
        serializer = self.serializer_class(data=new_user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish("user_created", serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
