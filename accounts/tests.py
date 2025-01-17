from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


USER_CREATE_URL = reverse("accounts:create")


class CustomUserTest(APITestCase):
    def test_create_user(self):
        payload = {
            "email": "email@test.com",
            "password": "mypass1!s",
        }
        response = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_short_pass(self):
        payload = {
            "email": "email@test.com",
            "password": "qq",
        }
        response = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_wrong_email(self):
        payload = {
            "email": "aaasssdddfff",
            "password": "mypass1!s",
        }
        response = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
