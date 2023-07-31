from datetime import datetime

from django.db.models import F, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from flights.models import (
    Flight,
    Crew,
    Airplane, AirplaneType
)
from flights.permissions import IsAdminOrIfAuthenticatedReadOnly
from flights.serializers import (
    FlightReadSerializer,
    FlightCreateSerializer,
    FlightDetailSerializer,
    CrewSerializer,
    AirplaneSerializer, AirplaneTypeSerializer
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
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        date = self.request.query_params.get("date")
        route_id_str = self.request.query_params.get("route")

        queryset = self.queryset

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(departure_time__date=date)

        if route_id_str:
            queryset = queryset.filter(route_id=int(route_id_str))

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightReadSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightCreateSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "route",
                type=OpenApiTypes.INT,
                description="Filter by route id (ex. ?route=2)",
            ),
            OpenApiParameter(
                "date",
                type=OpenApiTypes.DATE,
                description=(
                    "Filter by datetime of flight "
                    "(ex. ?date=2022-10-23)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminUser,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminUser,)
