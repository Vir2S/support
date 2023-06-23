from django.urls import path

from users.api import UserRegistrationAPIView

urlpatterns = [
    path("", UserRegistrationAPIView.as_view()),
]
