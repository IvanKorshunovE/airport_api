from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("routes/", include("routes.urls", namespace="routes")),
    path("flights/", include("flights.urls", namespace="flights")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("__debug__/", include("debug_toolbar.urls")),
]
