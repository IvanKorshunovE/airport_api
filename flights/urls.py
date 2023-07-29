from rest_framework import routers

from flights.views import FlightViewSet

router = routers.DefaultRouter()

router.register("flights", FlightViewSet)

urlpatterns = router.urls

app_name = "flights"
