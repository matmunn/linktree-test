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
