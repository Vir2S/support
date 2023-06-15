from django.urls import path

from core.api import UserRegistrationAPIView

urlpatterns = [
    path("", UserRegistrationAPIView.as_view()),
]
