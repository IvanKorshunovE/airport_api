from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count, F
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from routes.models import Airport, Route
from routes.serializers import (
    AirportSerializer,
    RouteReadSerializer, RouteCreateSerializer,
)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = (
        Route.objects.select_related(
            "source", "destination"
        )
    )
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RouteReadSerializer
        return RouteCreateSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = (
        Airport.objects
        .prefetch_related(
            "source_routes__destination",
        )
        .all()
    )
    serializer_class = AirportSerializer
    permission_classes = [IsAdminUser]
