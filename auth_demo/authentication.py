"""Custom authenticator class for third-party apps to use."""

from rest_framework import authentication, exceptions

from auth_demo.models import ThirdPartyApp


class ThirdPartyAppAuthentication(authentication.BaseAuthentication):
    """Authentication backend for third-party apps."""

    def authenticate(self, request):
        """Authenticate the request."""
        if not (app_name := request.META.get("HTTP_X_EXTERNAL_APP")):
            return None

        try:
            app = ThirdPartyApp.objects.get(app_name=app_name)
        except ThirdPartyApp.DoesNotExist:
            raise exceptions.AuthenticationFailed("App doesn't exist.") from None

        return (None, app)
