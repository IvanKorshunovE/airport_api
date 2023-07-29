from rest_framework import routers

from routes.views import (
    AirportViewSet,
    RouteViewSet
)

router = routers.DefaultRouter()

router.register("routes", RouteViewSet)
router.register("airports", AirportViewSet)

urlpatterns = router.urls

app_name = "routes"
