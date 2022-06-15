"""URLs for our auth app."""

from rest_framework import routers

from auth_demo.views import AdvertisementViewSet, MessageViewSet

router = routers.SimpleRouter()
router.register("advertisements", AdvertisementViewSet)
router.register("messages", MessageViewSet)
urlpatterns = router.urls
