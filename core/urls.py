from django.urls import path

from core.api import users_router

urlpatterns = [
    path("", users_router),
]
