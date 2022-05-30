import unittest
import os
from django.contrib.auth.hashers import check_password, make_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
import sys

sys.path.append("../")
import users

django.setup()
from .models import User


class TestCaseUser(unittest.TestCase):
    def test_constructor(self):
        user = User(username="TestGuy", email="testguy@gmail.com", password="TestPass")
        self.assertEqual(user.username, "TestGuy")
        self.assertEqual(user.email, "testguy@gmail.com")

    def test_set_password(self):
        user = User(username="TestGuy", email="testguy@gmail.com", password="TestPass")
        user.set_password("NewPass")
        self.assertTrue(check_password("NewPass", user.password))

    def test_check_password_incorrect(self):
        user = User(username="TestGuy", email="testguy@gmail.com", password="TestPass")
        self.assertFalse(user.check_password("FalsePassword"))

    def test_check_password_correct(self):
        user = User(username="TestGuy", email="testguy@gmail.com", password="TestPass")
        user.set_password("NewPass")
        result = user.check_password("NewPass")
        self.assertTrue(result)

    def test_username(self):
        user = User(username="TestGuy", email="testguy@gmail.com", password="TestPass")
        user.username = "NewUsername"
        self.assertEqual(user.username, "NewUsername")

    def test_email(self):
        user = User(username="TestGuy", email="testguy@gmail.com", password="TestPass")
        user.email = "newemail@gmail.com"
        self.assertEqual(user.email, "newemail@gmail.com")


if __name__ == "__main__":
    unittest.main()
