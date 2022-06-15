"""Auth serialisers."""

from rest_framework import serializers

from auth_demo.models import Advertisement, Message, User


class UserSerialiser(serializers.ModelSerializer):
    """A serialise for a user."""

    class Meta:
        """Meta class."""

        model = User
        fields = ("id", "username", "email")


class UserRepresentationMixin(metaclass=serializers.SerializerMetaclass):
    """Mixin to reduce duplicated code modifying the user field on request/response."""

    user = serializers.CharField()

    def to_representation(self, instance):
        """Change the representation of the user in a response."""
        self.fields["user"] = UserSerialiser()
        return super().to_representation(instance)

    def validate_user(self, value):
        """Validate the user."""
        try:
            return User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.") from None


class MessageSerialiser(UserRepresentationMixin, serializers.ModelSerializer):
    """A serialiser for a message."""

    class Meta:
        """Meta options."""

        model = Message
        fields = ("id", "user", "message")


class AdvertisementSerialiser(UserRepresentationMixin, serializers.ModelSerializer):
    """A serialiser for an advertisement."""

    class Meta:
        """Meta options."""

        model = Advertisement
        fields = ("id", "user", "advertisement")
