"""Auth app models."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""

    parents = models.ManyToManyField("self", related_name="children")
