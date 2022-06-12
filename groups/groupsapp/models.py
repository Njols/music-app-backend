from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100)


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    picture_url = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_groups",
        blank=True,
    )
    members = models.ManyToManyField(User, related_name="groups", blank=True)
