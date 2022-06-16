from groups.groupsapp.producer import publish
from groupsapp.serializers import GroupSerializer, UserSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Group, User


class GroupListController(GenericAPIView):
    serializer_class = GroupSerializer
    user_serializer = UserSerializer
    user_queryset = User.objects

    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        new_group = request.data
        serializer = self.serializer_class(data=new_group)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish("group_created", serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupDetailController(GenericAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects

    def get(self, request, pk):
        try:
            group = self.queryset.get(pk=pk)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GroupSerializer(group)

        return Response(serializer.data)

    def put(self, request, pk):
        try:
            group = self.queryset.get(pk=pk)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish("group_changed", serializer.data)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            group = self.queryset.get(pk=pk)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        group.delete()
        publish("group_deleted", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListController(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class GroupJoinController(GenericAPIView):
    queryset = Group.objects
    user_queryset = User.objects

    def post(self, request, pk):
        data = request.data
        try:
            group = self.queryset.get(pk=pk)
            user = self.user_queryset.get(user_id=data["user_id"])
        except (Group.DoesNotExist, User.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        group.members.add(user)
        return Response(status=status.HTTP_200_OK)


class GroupLeaveController(GenericAPIView):
    queryset = Group.objects
    user_queryset = User.objects

    def post(self, request, pk):
        data = request.data
        try:
            group = self.queryset.get(pk=pk)
            user = self.user_queryset.get(user_id=data["user_id"])
        except (Group.DoesNotExist, User.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        group.members.remove(user)
        return Response(status=status.HTTP_200_OK)
