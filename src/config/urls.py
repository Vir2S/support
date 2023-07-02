from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="Support API Documentation",
        default_version="v1",
        description="API Documentation for Support project",
        # terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    permission_classes=[AllowAny],
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/auth/", include("authentication.urls")),
    path("api/pokemons/", include("pokemons.urls")),
    path("api/users/", include("users.urls")),
    path("api/users/create-random-user/", include("examples.users")),
    path("api/tickets/", include("tickets.urls")),
]
