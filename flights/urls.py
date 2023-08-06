from rest_framework import routers

from flights.views import (
    FlightViewSet,
    CrewViewSet,
    AirplaneViewSet,
    AirplaneTypeViewSet
)

router = routers.DefaultRouter()

router.register("flights", FlightViewSet)
router.register("crews", CrewViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airplane_types", AirplaneTypeViewSet)


urlpatterns = router.urls

app_name = "flights"
