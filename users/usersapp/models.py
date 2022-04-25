from django.db import models
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import UserManager


def default_dict():
    return {"keywords": []}


class User(models.Model):
    username = models.CharField(unique=True, max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    objects = UserManager()

    def __str__(self):
        return "%s %s" % (self.username)
