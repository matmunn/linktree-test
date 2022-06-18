"""Auth app views."""

from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import fields, mixins, viewsets

from auth_demo.models import Advertisement, Message
from auth_demo.permissions import (
    AuthenticatedOrThirdPartyAppPermission,
    HasCreatePermission,
    RequiresPremiumSubscriptionPermission,
)
from auth_demo.serialisers import (
    AdvertisementSerialiser,
    MessageSerialiser,
    UserSerialiser,
)


class AuthenticationPermissionForCreateMixin:
    """A mixin to add the `IsAuthenticated` permission when creating an object."""

    def get_permissions(self):
        """Instantiate and return the list of permissions that this view requires."""
        if self.action == "create":
            self.permission_classes = [
                AuthenticatedOrThirdPartyAppPermission,
                *self.permission_classes,
            ]

        return super().get_permissions()


@extend_schema_view(
    list=extend_schema(
        description="List all the messages.",
        responses=inline_serializer(
            "MessageResponseSerialiser",
            {
                "id": fields.IntegerField(),
                "user": UserSerialiser(),
                "message": fields.CharField(),
            },
        ),
    ),
    create=extend_schema(
        description="Create a new message.",
        responses=inline_serializer(
            "MessageResponseSerialiser",
            {
                "id": fields.IntegerField(),
                "user": UserSerialiser(),
                "message": fields.CharField(),
            },
        ),
    ),
)
class MessageViewSet(
    AuthenticationPermissionForCreateMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """A viewset for messages."""

    serializer_class = MessageSerialiser
    queryset = Message.objects.all()
    permission_classes = [
        HasCreatePermission,
    ]


@extend_schema_view(
    list=extend_schema(
        description="List all the advertisements.",
        responses=inline_serializer(
            "AdvertisementResponseSerialiser",
            {
                "id": fields.IntegerField(),
                "user": UserSerialiser(),
                "advertisement": fields.CharField(),
            },
        ),
    ),
    create=extend_schema(
        description="Create a new advertisement.",
        responses=inline_serializer(
            "AdvertisementResponseSerialiser",
            {
                "id": fields.IntegerField(),
                "user": UserSerialiser(),
                "advertisement": fields.CharField(),
            },
        ),
    ),
)
class AdvertisementViewSet(
    AuthenticationPermissionForCreateMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """A viewset for advertisements."""

    serializer_class = AdvertisementSerialiser
    queryset = Advertisement.objects.all()
    permission_classes = [
        RequiresPremiumSubscriptionPermission,
    ]
