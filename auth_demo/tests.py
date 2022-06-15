"""Auth app tests."""

from django.urls import reverse
from rest_framework.test import APITestCase

from auth_demo.factories import UserFactory


class MessagesTestCase(APITestCase):
    """Tests related to messages."""

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
        """Test a user can't create a message for another user without permission."""
        user1 = UserFactory()
        user2 = UserFactory()
        # User 2 is not a parent of user 1 here

        self.client.force_login(user2)

        url = reverse("message-list")
        response = self.client.post(
            url, {"message": "Hello", "user": user1.username}, format="json"
        )

        self.assertEqual(response.status_code, 403)


class AdvertisementsTestCase(APITestCase):
    """Tests related to advertisements."""

    def test_unauthenticated_user_cant_create_ad(self):
        """Test an unauthenticated user can't create a new advert."""
        url = reverse("advertisement-list")
        response = self.client.post(
            url, {"advertisement": "Hello", "user": "foo"}, format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_free_user_cant_create_ad(self):
        """Test an authenticated free user can't create an advert."""
        user = UserFactory()
        self.client.force_login(user)

        url = reverse("advertisement-list")
        response = self.client.post(
            url, {"advertisement": "Hello", "user": user.username}, format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_premium_user_can_create_ad(self):
        """Test an authenticated premium user can create an advert."""
        user = UserFactory(paid_subscriber=True)
        self.client.force_login(user)

        url = reverse("advertisement-list")
        response = self.client.post(
            url, {"advertisement": "Hello", "user": user.username}, format="json"
        )

        self.assertEqual(response.status_code, 201)

    def test_allowed_user_can_create_ad_for_another(self):
        """Test a user can create an advert for another user with permission."""
        user1 = UserFactory(paid_subscriber=True)
        user2 = UserFactory()
        # Add user 2 as a parent of user 1
        user1.parents.add(user2)

        self.client.force_login(user2)

        url = reverse("advertisement-list")
        response = self.client.post(
            url, {"advertisement": "Hello", "user": user1.username}, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get("user").get("username"), user1.username)

    def test_disallowed_user_cant_create_message_for_another(self):
        """Test a user can't create an advert for another user without permission."""
        user1 = UserFactory(paid_subscriber=True)
        user2 = UserFactory()
        # User 2 is not a parent of user 1 here

        self.client.force_login(user2)

        url = reverse("advertisement-list")
        response = self.client.post(
            url, {"advertisement": "Hello", "user": user1.username}, format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_premium_user_cant_create_ad_for_free_user(self):
        """Test a premium user can't create an ad for a free user."""
        user1 = UserFactory()
        user2 = UserFactory(paid_subscriber=True)
        # Add user 2 as a parent of user 1
        user1.parents.add(user2)

        self.client.force_login(user2)

        url = reverse("advertisement-list")
        response = self.client.post(
            url, {"advertisement": "Hello", "user": user1.username}, format="json"
        )

        self.assertEqual(response.status_code, 403)
