"""Custom DRF permission classes."""

from django.contrib.auth import get_user_model
from rest_framework import permissions

from auth_demo.models import Subscription, ThirdPartyApp, ThirdPartyAppActionPermission

USER_MODEL = get_user_model()


class AuthenticatedOrThirdPartyAppPermission(permissions.BasePermission):
    """Check if a third party is making a request or if a user is authenticated."""

    def has_permission(self, request, view):
        """
        Check permissions.

        If a `Referer` header is provided then check if it represents a valid
        third-party app. If the `Referer` header is not provided then check if the
        user is authenticated.
        """
        if app := request.headers.get("X-External-App"):
            try:
                app = ThirdPartyApp.objects.get(app_name=app)
            except ThirdPartyApp.DoesNotExist:
                # A third-party app was provided but does not exist. Deny permission.
                # NOTE: As this is implemented it can be abused for enumeration.
                return False

            return ThirdPartyAppActionPermission.objects.filter(
                action=view.action, url_name=request.resolver_match.url_name
            ).exists()

        return request.user and request.user.is_authenticated


def _check_user_in_parents(for_user, active_user):
    """Check if the authenticated user can act on behalf of given user."""
    return active_user in for_user.parents.all()


class HasCreatePermission(permissions.BasePermission):
    """Check if a user or app has permission to create an object for the given user."""

    def has_permission(self, request, view):
        """Check if a user has permission to create an object for the given user."""
        if request.method in permissions.SAFE_METHODS:
            # We're only supposed to be checking creation or unsafe HTTP methods here.
            return True

        requested_user = request.data.get("user")

        try:
            for_user = USER_MODEL.objects.get(username=requested_user)
        except USER_MODEL.DoesNotExist:
            # Choosing to return True here so that we progress to where
            # validation fails.
            return True

        if app := request.headers.get("X-External-App"):
            return Subscription.objects.filter(
                app__app_name=app, user=for_user
            ).exists()

        if request.user and request.user.username == requested_user:
            return True

        return _check_user_in_parents(for_user, request.user)


class RequiresPremiumSubscriptionPermission(permissions.BasePermission):
    """Check if a user has a premium subscription."""

    def has_permission(self, request, view):
        """Check if a user has a premium subscription or admins an account that does."""
        if request.method in permissions.SAFE_METHODS:
            # We're only supposed to be checking creation or unsafe HTTP methods here.
            return True

        requested_user = request.data.get("user")

        try:
            for_user = USER_MODEL.objects.get(username=requested_user)
        except USER_MODEL.DoesNotExist:
            # Choosing to return True here so that we progress to where
            # validation fails.
            return True

        if app := request.headers.get("X-External-App"):
            return (
                for_user.paid_subscriber
                and Subscription.objects.filter(
                    app__app_name=app, user=for_user
                ).exists()
            )

        if requested_user != request.user.username:
            return for_user.paid_subscriber and _check_user_in_parents(
                for_user, request.user
            )

        return request.user.is_staff or request.user.paid_subscriber
