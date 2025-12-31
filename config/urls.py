from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="RC Shop",
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("apps.auths.urls")),
    path("", include("apps.products.urls")),
    path("orders/", include("apps.orders.urls")),
    path("cart/", include("apps.cart.urls")),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
