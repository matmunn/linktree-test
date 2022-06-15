"""Auth app tests."""

from django.urls import reverse
from rest_framework.test import APITestCase

from auth_demo.factories import UserFactory


class AuthorisationTestCase(APITestCase):
    """Tests related to our auth system."""

    def test_unauthenticated_user_cant_create_message(self):
        """Test an unauthenticated user can't create a new message."""
        url = reverse("message-list")
        response = self.client.post(
            url, {"message": "Hello", "user": "foo"}, format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_user_can_create_message(self):
        """Test an authenticated user can create a message for themself."""
        user = UserFactory()
        self.client.force_login(user)

        url = reverse("message-list")
        response = self.client.post(
            url, {"message": "Hello", "user": user.username}, format="json"
        )
        self.assertEqual(response.status_code, 201)
