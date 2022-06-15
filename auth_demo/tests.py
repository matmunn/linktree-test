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

    def test_allowed_user_can_create_message_for_another(self):
        """Test a user can create a message for another user with permission."""
        user1 = UserFactory()
        user2 = UserFactory()
        # Add user 2 as a parent of user 1
        user1.parents.add(user2)

        self.client.force_login(user2)

        url = reverse("message-list")
        response = self.client.post(
            url, {"message": "Hello", "user": user1.username}, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get("user").get("username"), user1.username)

    def test_disallowed_user_cant_create_message_for_another(self):
        """Test a user can create a message for another user with permission."""
        user1 = UserFactory()
        user2 = UserFactory()
        # User 2 is not a parent of user 1 here

        self.client.force_login(user2)

        url = reverse("message-list")
        response = self.client.post(
            url, {"message": "Hello", "user": user1.username}, format="json"
        )

        self.assertEqual(response.status_code, 403)
