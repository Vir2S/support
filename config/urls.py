from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/pokemons/", include("pokemons.urls")),
    path("create-random-user/", include("core.urls")),
]
