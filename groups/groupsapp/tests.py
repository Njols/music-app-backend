import unittest
import os
from django.contrib.auth.hashers import check_password, make_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
import sys

sys.path.append("../")
import groups

django.setup()
from .models import User, Group


class TestCaseGoup(unittest.TestCase):
    def test_constructor(self):
        user = User(user_id=1, username="TestGuy")
        group = Group(
            name="TestGroup", picture_url="https://www.google.com", owner=user
        )
        self.assertEqual(group.name, "TestGroup")
        self.assertEqual(group.picture_url, "https://www.google.com")
        self.assertEqual(group.owner, user)

    def test_name(self):
        user = User(user_id=1, username="TestGuy")
        group = Group(
            name="TestGroup", picture_url="https://www.google.com", owner=user
        )
        group.name = "NewName"
        self.assertEqual(group.name, "NewName")

    def test_picture_url(self):
        user = User(user_id=1, username="TestGuy")
        group = Group(
            name="TestGroup", picture_url="https://www.google.com", owner=user
        )
        group.picture_url = "https://www.facebook.com"
        self.assertEqual(group.picture_url, "https://www.facebook.com")

    def test_owner(self):
        user = User(user_id=1, username="TestGuy")
        group = Group(
            name="TestGroup", picture_url="https://www.google.com", owner=user
        )
        new_user = User(user_id=2, username="NewGuy")
        group.owner = new_user
        self.assertEqual(group.owner, new_user)


if __name__ == "__main__":
    unittest.main()
