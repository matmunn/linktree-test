"""Auth app models."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""

    parents = models.ManyToManyField("self", related_name="children")
    paid_subscriber = models.BooleanField(default=False)


class Message(models.Model):
    """A message."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    message = models.CharField(max_length=200)


class Advertisement(models.Model):
    """An advertisement."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adverts")
    advertisement = models.CharField(max_length=200)


class ThirdPartyApp(models.Model):
    """A third party app."""

    app_name = models.CharField(max_length=200)


class ThirdPartyAppActionPermission(models.Model):
    """A permission for an endpoint that the third-party app can access."""

    app = models.ForeignKey(
        ThirdPartyApp, on_delete=models.CASCADE, related_name="allowed_actions"
    )
    action = models.CharField(max_length=200)
    url_name = models.CharField(max_length=200)


class Subscription(models.Model):
    """A user's subscription to an app."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    app = models.ForeignKey(
        ThirdPartyApp, on_delete=models.CASCADE, related_name="subscriptions"
    )
