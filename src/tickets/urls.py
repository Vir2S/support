from django.urls import path
from rest_framework.routers import DefaultRouter

from tickets.api import MessageListCreateAPIView, TicketAPIViewSet

router = DefaultRouter()
router.register("", TicketAPIViewSet, basename="tickets")
urlpatterns = router.urls + [
    path("<int:ticket_id>/messages/", MessageListCreateAPIView.as_view())
]
