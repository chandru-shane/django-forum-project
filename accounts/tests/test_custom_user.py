from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

USER_REGISTER = reverse("customuser:register")
USER_LOGIN = reverse("customuser:login")
USER_LOGOUT = reverse("customuser:logout")


def create_user(username="testuser", email="test@gmail.com", password="maingoal"):
    user = get_user_model()
    created_user = user.objects.create_user(
        username=username, email=email, password=password
    )
    return created_user


class CustomUserModel(TestCase):
    """To test custom user model functionality"""

    def setUp(self):
        self.client = APIClient()

    def test_login_user_with_email(self):
        """To test can login successfully  with email"""
        user = create_user()
        credentials = {"username_or_email": "test@gmail.com", "password": "maingoal"}
        res = self.client.post(USER_LOGIN, credentials)

        self.assertIn("token", res.data)

    def test_login_user_with_username(self):
        """Test that can login successfully with username"""
        create_user()
        credentials = {
            "username_or_email": "testuser",
            "password": "maingoal"
            }
        res = self.client.post(USER_LOGIN, credentials)
        self.assertIn("token", res.data)

    def test_logout(self):
        """Test that user can logout"""
        user = create_user()
        credentials = {"username_or_email": "testuser", "password": "maingoal"}
        res = self.client.post(USER_LOGIN, credentials)
        token = res.data.get("token")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        res = self.client.get(USER_LOGOUT)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.get(USER_LOGOUT)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_new_user(self):
        """Test to verify create register new user
        with the appropriate endpoint"""
        credentials = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "maingoal",
        }
        res = self.client.post(USER_REGISTER, credentials)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data.get("username"), credentials["username"])
        self.assertEqual(res.data.get("email"), credentials["email"])
        self.assertFalse(res.data.get("password"))

    def test_created_user_data(self):
        """Test given data saved correctly"""
        credentials = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "maingoal",
        }
        self.client.post(USER_REGISTER, credentials)
        user = get_user_model()
        current_user = user.objects.get(username=credentials["username"])

        self.assertEqual(credentials["username"], current_user.username)
        self.assertEqual(credentials["email"], current_user.email)
        self.assertNotEqual(current_user.password, credentials["password"])
        self.assertTrue(current_user.check_password(credentials["password"]))
        self.assertTrue(current_user.is_active)
        self.assertFalse(current_user.is_staff)
        self.assertFalse(current_user.is_superuser)

    def test_register_with_lessthan_eight_digit_password(self):
        """Test to user can not register with less eight password"""
        credentials = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "123",
        }
        res = self.client.post(USER_REGISTER, credentials)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_not_valid_email(self):
        """Test to user can not register with non valid email"""
        credentials = {
            "username": "testuser",
            "email": "testuse",
            "password": "123jdfkjj",
        }
        res = self.client.post(USER_REGISTER, credentials)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_same_username(self):
        """Test to user can not register with used username """
        credentials = {
            "username": "testuser",
            "email": "testuse1@gmail.com",
            "password": "123jdfkjj",
        }
        res = self.client.post(USER_REGISTER, credentials)
        credentials = {
            "username": "testuser",
            "email": "testuse@gmail.com",
            "password": "123jdfkjj",
        }
        res = self.client.post(USER_REGISTER, credentials)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_same_email(self):
        """Test to user can not register with used email """
        credentials = {
            "username": "testuser1",
            "email": "testuse@gmail.com",
            "password": "123jdfkjj",
        }
        res = self.client.post(USER_REGISTER, credentials)
        credentials = {
            "username": "testuser2",
            "email": "testuse@gmail.com",
            "password": "123jdfkjj",
        }
        res = self.client.post(USER_REGISTER, credentials)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_without_email(self):
        """Test that user can't register without email"""
        credentials = {"username": "testuser", "password": "123jdfkjj"}
        res = self.client.post(USER_REGISTER, credentials)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_without_username(self):
        """Test that user can't register without username"""
        credentials = {"email": "testuser@gmail.com", "password": "123jdfkjj"}
        res = self.client.post(USER_REGISTER, credentials)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_without_password(self):
        """Test that user can't register without username"""
        credentials = {"username": "testuser", "email": "testuser@gmail.com"}
        res = self.client.post(USER_REGISTER, credentials)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)