"""Auth app views."""

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from auth_demo.models import Advertisement, Message
from auth_demo.permissions import HasCreatePermission
from auth_demo.serialisers import AdvertisementSerialiser, MessageSerialiser


class MessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """A viewset for messages."""

    serializer_class = MessageSerialiser
    queryset = Message.objects.all()
    permission_classes = (IsAuthenticated, HasCreatePermission)


class AdvertisementViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """A viewset for advertisements."""

    serializer_class = AdvertisementSerialiser
    queryset = Advertisement.objects.all()
