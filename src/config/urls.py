from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("api/pokemons/", include("pokemons.urls")),
    path("api/users/", include("users.urls")),
    path("api/users/create-random-user/", include("examples.users")),
    path("api/tickets/", include("tickets.urls")),
]
