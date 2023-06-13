from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair

urlpatterns = [
    path("token/", token_obtain_pair),
]
