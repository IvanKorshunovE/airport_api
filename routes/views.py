from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from flights.permissions import IsAdminOrIfAuthenticatedReadOnly
from routes.models import Airport, Route
from routes.serializers import (
    RouteReadSerializer,
    RouteCreateSerializer,
    AirportRouteSerializer,
    AirportImageSerializer,
)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = (
        Route.objects.select_related(
            "source", "destination"
        )
    )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

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
    serializer_class = AirportRouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "upload_image":
            return AirportImageSerializer
        return AirportRouteSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image"
    )
    def upload_image(self, request, pk=None):
        """
        Endpoint for downloading images
        for a specific airport
        """
        airport = self.get_object()
        serializer = self.get_serializer(
            airport, data=self.request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )
