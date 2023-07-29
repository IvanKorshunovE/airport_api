from django.db.models import F, Count
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from flights.models import Flight
from flights.serializers import (
    FlightReadSerializer,
    FlightCreateSerializer
)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = (
        Flight.objects
        .select_related(
            "route__source",
            "route__destination",
        ).annotate(
            tickets_available=(
                    F("airplane__rows") * F("airplane__seats_in_row")
                    - Count("tickets")
            )
        )
    )
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return FlightReadSerializer
        return FlightCreateSerializer
