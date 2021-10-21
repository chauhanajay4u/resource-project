from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from . import views
from user.models import User, UserLogin
from django.urls import reverse



class UserTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        url = "/user/register/"
        data = {
            "email": "admin@test.com",
            "phone": "9999999999",
            "name": "Admin",
            "password": "test123",
            "city": "Mumbai",
            "country": "India"
        }
        client = APIClient()
        response = client.post(url, data, format='json')
        User.objects.update(role="admin")
        cls.user = response.data

    def test_create_user(self):
        """Test for checking user registration"""
        url = "/user/register/"
        data = {
            "email": "user@test.com",
            "phone": "9999999999",
            "name": "User",
            "password": "test123",
            "city": "Mumbai",
            "country": "India"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=response.data.get("user_id")).name, 'User')

    def test_user_login(self):
        UserLogin.objects.all().delete()

        url = "/user/login/"
        data = {
            "email": "admin@test.com",
            "password": "test123"
        }
        # login user with correct password
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data["session_token"], UserLogin.objects.get().session_token)

        # error for user with incorrect password
        data["password"] = "wrong_pass"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_user_logout(self):
        url = "/user/{}/logout/".format(self.user["user_id"])
        data = {
            "logout_all": 1
        }
        # login user with correct password
        self.client.credentials(HTTP_SESSION_TOKEN=self.user["session_token"])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data["message"], "Logout Successful")

