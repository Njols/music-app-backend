from django.db import models


class User(models.Model):
    user_id = models.BigIntegerField()
    username = models.CharField(max_length=100)


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    picture_url = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_groups"
    )
    members = models.ManyToManyField(User, related_name="groups")
