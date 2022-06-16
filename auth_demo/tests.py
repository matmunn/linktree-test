"""Auth app tests."""

from django.urls import reverse
from rest_framework.test import APITestCase

from auth_demo.factories import (
    AdvertisementFactory,
    MessageFactory,
    SubscriptionFactory,
    ThirdPartyAppActionPermissionFactory,
    ThirdPartyAppFactory,
    UserFactory,
)


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

    def test_user_cant_create_message_for_nonexistent_user(self):
        """Test an authenticated user can't create a message for non-existent user."""
        user = UserFactory()
        self.client.force_login(user)

        url = reverse("message-list")
        response = self.client.post(
            url, {"message": "Hello", "user": "cow-says-moo"}, format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"User does not exist", response.content)

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

    def test_user_can_list_messages(self):
        """Test a user can list messages that already exist."""
        user = UserFactory()
        for _ in range(3):
            MessageFactory()

        self.client.force_login(user)

        url = reverse("message-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)


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

    def test_user_cant_create_ad_for_nonexistent_user(self):
        """Test an ad can't be created for a user who doesn't exist."""
        user = UserFactory()

        self.client.force_login(user)

        url = reverse("advertisement-list")
        response = self.client.post(
            url, {"advertisement": "Hello", "user": "bleep-bloop"}, format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"User does not exist", response.content)

    def test_free_user_can_list_ads(self):
        """Test a free user can list ads that already exist."""
        user = UserFactory()
        for _ in range(5):
            AdvertisementFactory()

        self.client.force_login(user)

        url = reverse("advertisement-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)


class ThirdPartyAppTestCase(APITestCase):
    """Tests for third-party app behaviours."""

    def test_an_app_can_create_a_message_for_a_subscriber(self):
        """Test an app can create a message for a subscriber."""
        user = UserFactory()

        app = ThirdPartyAppFactory()
        ThirdPartyAppActionPermissionFactory(
            app=app, action="create", url_name="message-list"
        )
        SubscriptionFactory(user=user, app=app)

        url = reverse("message-list")
        response = self.client.post(
            url,
            {"user": user.username, "message": "What a cool message"},
            format="json",
            HTTP_X_EXTERNAL_APP=app.app_name,
        )

        self.assertEqual(response.status_code, 201)

    def test_an_app_cant_create_a_message_for_a_non_subscriber(self):
        """Test an app can't create a message for a non-subscriber."""
        user = UserFactory()

        app = ThirdPartyAppFactory()
        ThirdPartyAppActionPermissionFactory(
            app=app, action="create", url_name="message-list"
        )

        url = reverse("message-list")
        response = self.client.post(
            url,
            {"user": user.username, "message": "What a cool message"},
            format="json",
            HTTP_X_EXTERNAL_APP=app.app_name,
        )

        self.assertEqual(response.status_code, 403)

    def test_an_app_can_create_an_advert_for_a_subscriber(self):
        """Test an app can create an advert for a subscriber."""
        user = UserFactory(paid_subscriber=True)

        app = ThirdPartyAppFactory()
        ThirdPartyAppActionPermissionFactory(
            app=app, action="create", url_name="advertisement-list"
        )
        SubscriptionFactory(user=user, app=app)

        url = reverse("advertisement-list")
        response = self.client.post(
            url,
            {
                "user": user.username,
                "advertisement": "Would you consider buying our thing",
            },
            format="json",
            HTTP_X_EXTERNAL_APP=app.app_name,
        )

        self.assertEqual(response.status_code, 201)

    def test_an_app_cant_create_an_advert_for_a_non_subscriber(self):
        """Test an app can't create an advert for a non-subscriber."""
        user = UserFactory(paid_subscriber=True)

        app = ThirdPartyAppFactory()
        ThirdPartyAppActionPermissionFactory(
            app=app, action="create", url_name="advertisement-list"
        )

        url = reverse("advertisement-list")
        response = self.client.post(
            url,
            {"user": user.username, "advertisement": "Do it, buy our thing"},
            format="json",
            HTTP_X_EXTERNAL_APP=app.app_name,
        )

        self.assertEqual(response.status_code, 403)

    def test_an_app_cant_create_an_advert_for_a_subscriber_with_a_free_account(self):
        """Test an app can't create an advert for a subscriber with a free account."""
        user = UserFactory()

        app = ThirdPartyAppFactory()
        ThirdPartyAppActionPermissionFactory(
            app=app, action="create", url_name="advertisement-list"
        )
        SubscriptionFactory(user=user, app=app)

        url = reverse("advertisement-list")
        response = self.client.post(
            url,
            {"user": user.username, "advertisement": "Do it, buy our thing"},
            format="json",
            HTTP_X_EXTERNAL_APP=app.app_name,
        )

        self.assertEqual(response.status_code, 403)

    def test_an_app_cant_create_a_message_if_it_doesnt_have_permission(self):
        """Test that an app can't create a message if it doesn't have permission."""
        user = UserFactory()

        app = ThirdPartyAppFactory()
        SubscriptionFactory(user=user, app=app)

        url = reverse("message-list")
        response = self.client.post(
            url,
            {"user": user.username, "message": "What a cool message"},
            format="json",
            HTTP_X_EXTERNAL_APP=app.app_name,
        )

        self.assertEqual(response.status_code, 403)

    def test_an_app_cant_create_an_advert_if_it_doesnt_have_permission(self):
        """Test that an app can't create an advert if it doesn't have permission."""
        user = UserFactory(paid_subscriber=True)

        app = ThirdPartyAppFactory()
        SubscriptionFactory(user=user, app=app)

        url = reverse("advertisement-list")
        response = self.client.post(
            url,
            {"user": user.username, "advertisement": "What a cool message"},
            format="json",
            HTTP_X_EXTERNAL_APP=app.app_name,
        )

        self.assertEqual(response.status_code, 403)
