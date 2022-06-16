"""Model factories for testing."""

import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    """A user factory for testing."""

    username = factory.Faker("user_name")

    class Meta:
        """Meta options."""

        model = get_user_model()


class MessageFactory(DjangoModelFactory):
    """A message factory for testing."""

    user = factory.SubFactory(UserFactory)
    message = factory.Faker("sentence")

    class Meta:
        """Meta options."""

        model = "auth_demo.Message"


class AdvertisementFactory(DjangoModelFactory):
    """An advertisement factory for testing."""

    user = factory.SubFactory(UserFactory)
    advertisement = factory.Faker("sentence")

    class Meta:
        """Meta options."""

        model = "auth_demo.Advertisement"
