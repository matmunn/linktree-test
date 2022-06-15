"""Custom DRF permission classes."""

from django.contrib.auth import get_user_model
from rest_framework import permissions

USER_MODEL = get_user_model()


class HasCreatePermission(permissions.BasePermission):
    """Check if a user has permission to create an object for the given user."""

    def _check_user_in_parents(self, username, current_user):
        """Check if the authenticated user can act on behalf of given user."""
        try:
            user = USER_MODEL.objects.get(username=username)
        except USER_MODEL.DoesNotExist:
            return False

        return current_user in user.parents.all()

    def has_permission(self, request, view):
        """Check if a user has permission to create an object for the given user."""
        if request.method in permissions.SAFE_METHODS:
            # We're only supposed to be checking creation or unsafe HTTP methods here.
            return True

        requested_user = request.data.get("user")
        if request.user.username == requested_user:
            return True

        return self._check_user_in_parents(requested_user, request.user)


class RequiresPremiumSubscriptionPermission(permissions.BasePermission):
    """Check if a user has a premium subscription."""

    def has_permission(self, request, view):
        """Check if a user has a premium subscription or admins an account that does."""
        if request.method in permissions.SAFE_METHODS:
            # We're only supposed to be checking creation or unsafe HTTP methods here.
            return True

        requested_user = request.data.get("user")

        try:
            user = USER_MODEL.objects.get(username=requested_user)
        except USER_MODEL.DoesNotExist:
            return False

        if requested_user != request.user.username:
            return user.paid_subscriber and request.user in user.parents.all()

        return request.user.paid_subscriber
