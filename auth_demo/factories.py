"""Model factories for testing."""

import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    """A user factory for testing."""

    username = factory.Faker("user_name")

    class Meta:
        """Meta options."""

        model = "auth_demo.User"
