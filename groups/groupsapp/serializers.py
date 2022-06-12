from rest_framework import serializers
from .models import Group, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "username"]


class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Group
        fields = ["id", "name", "picture_url", "owner", "members", "user_id"]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        try:
            user = User.objects.get(user_id=user_id)
            instance = Group.objects.create(owner=user, **validated_data)
            return instance
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user id")
