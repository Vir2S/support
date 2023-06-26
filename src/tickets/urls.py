from rest_framework.routers import DefaultRouter

from tickets.api import TicketAPIViewSet


router = DefaultRouter()
router.register("", TicketAPIViewSet, basename="tickets")

urlpatterns = router.urls
